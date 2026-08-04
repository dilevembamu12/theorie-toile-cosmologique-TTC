#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTC HARDENING — Solver EDP couplé Γ,Φ,T avec source baryonique
================================================================
OBJECTIF : Résoudre NUMÉRIQUEMENT le système couplé des 3 champs
TTC en symétrie sphérique avec une source baryonique M_b(r), et
en extraire la courbe de rotation v(r). Confronter à SPARC.

Ce que ce script fait (que les précédents ne faisaient PAS) :
  1. Discrétise les 3 EDP sur une grille radiale
  2. Résout par relaxation de Jacobi (pas de fit paramétrique)
  3. Injecte M_b(r) comme source dans l'EDP de Γ
  4. Extrait v(r) = √(G M_tot(<r) / r) de la solution
  5. Compare avec les données SPARC réelles

Équations résolues (sphérique, statique) :
  (1) ∇²Γ = Γ(∇Φ)² + αΓ(Γ²−v_Γ²) + 2λTΓ − κ·ρ_b(r)
  (2) ∇·(Γ²∇Φ) = 0
  (3) ∇²T = β(T−v_T) + λΓ²

où ρ_b(r) est la densité baryonique (gaz + disque + bulbe).

Auteur : DeepSeek V4 Pro (Co-auteur TTC)
Date   : 31 juillet 2026 — Session de durcissement
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d
from scipy.stats import linregress
from pathlib import Path
import csv, json, warnings, time

warnings.filterwarnings("ignore")

# ============================================================================
# CONSTANTES PHYSIQUES
# ============================================================================
G_kpc = 4.301e-9          # [kpc (km/s)² / M☉]
G_cgs = 6.67430e-8         # [cm³/g/s²]
KPC_TO_CM = 3.085678e21    # kpc → cm
MSUN_TO_G = 1.98847e33     # M☉ → g
KMS_TO_CMs = 1e5           # km/s → cm/s

# Échelles TTC (unités normalisées pour calcul numérique)
V_GAMMA_DEFAULT = 1.0      # v_Γ normalisé
V_T_DEFAULT = 0.0          # v_T (vide sans tension)

# ============================================================================
# GRILLE RADIALE
# ============================================================================

def build_grid(r_min=0.01, r_max=100.0, n_points=500):
    """Grille logarithmique pour bonne résolution au centre ET à grande distance."""
    r = np.logspace(np.log10(r_min), np.log10(r_max), n_points)
    dr = np.gradient(r)
    return r, dr


# ============================================================================
# PROFIL BARYONIQUE
# ============================================================================

def baryonic_density_from_velocities(r_grid, r_data, v_gas, v_disk, v_bulge=None,
                                      upsilon_d=0.5, upsilon_b=0.7):
    """
    Reconstruit ρ_b(r) à partir des vitesses baryoniques SPARC.
    
    v_b²(r) = v_gas² + Υ_d·v_disk² + Υ_b·v_bulge²
    M_b(<r) = r·v_b²(r) / G  (approximation sphérique)
    ρ_b(r) = (1/4πr²) · dM_b/dr
    """
    if v_bulge is None:
        v_bulge = np.zeros_like(v_gas)
    
    # Vitesse baryonique quadratique
    v_b_sq = (np.abs(v_gas) * v_gas
              + upsilon_d * np.abs(v_disk) * v_disk
              + upsilon_b * np.abs(v_bulge) * v_bulge)
    v_b_sq = np.maximum(v_b_sq, 0)
    
    # Masse baryonique enfermée
    M_b_enc = r_data * v_b_sq / G_kpc
    
    # Interpoler puis dériver sur la grille fine
    # On interpole M_b(<r) puis on dérive
    M_b_interp = interp1d(r_data, M_b_enc, kind='linear',
                          bounds_error=False, fill_value=(0, M_b_enc[-1]))
    M_b_on_grid = M_b_interp(r_grid)
    
    # ρ_b = (1/4πr²) · dM_b/dr
    dM_dr = np.gradient(M_b_on_grid, r_grid)
    rho_b = dM_dr / (4 * np.pi * r_grid**2)
    rho_b = np.maximum(rho_b, 0)
    
    # Régulariser à r→0
    rho_b[0] = rho_b[1] if len(rho_b) > 1 else 0
    
    return rho_b, M_b_on_grid


# ============================================================================
# OPÉRATEURS DIFFÉRENTIELS EN SYMÉTRIE SPHÉRIQUE
# ============================================================================

def laplacian_spherical(f, r, dr):
    """
    Laplacien sphérique : ∇²f = (1/r²)·∂_r(r²·∂_r f)
    Discrétisation par différences finies centrées d'ordre 2.
    """
    n = len(f)
    lap = np.zeros(n)
    
    # Intérieur : schéma centré
    for i in range(1, n-1):
        r_i = r[i]
        dr_f = dr[i]
        # ∂_r f au point i (centré)
        df_dr = (f[i+1] - f[i-1]) / (2 * dr_f)
        # r²·∂_r f aux points i±½
        r2_df_plus = r[i]**2 * (f[i+1] - f[i]) / dr_f
        r2_df_minus = r[i-1]**2 * (f[i] - f[i-1]) / dr_f
        # ∂_r(r²·∂_r f)
        d_r2df_dr = (r2_df_plus - r2_df_minus) / dr_f
        lap[i] = d_r2df_dr / r_i**2 if r_i > 0 else 0
    
    # Bord gauche (r=0) : limite analytique
    # ∇²f → 3·∂²f/∂r² en r=0 (développement de Taylor)
    if n >= 3:
        lap[0] = 6.0 * (f[1] - f[0]) / r[1]**2  # approximation
    
    # Bord droit (r→∞) : condition de Dirichlet (f → VEV)
    lap[-1] = 0.0  # Le champ est gelé à sa VEV
    
    return lap


def gradient_squared_spherical(f, r, dr):
    """(∇f)² = (∂f/∂r)² en symétrie sphérique."""
    n = len(f)
    grad_sq = np.zeros(n)
    
    for i in range(1, n-1):
        df_dr = (f[i+1] - f[i-1]) / (2 * dr[i])
        grad_sq[i] = df_dr**2
    
    # Bords
    if n >= 2:
        grad_sq[0] = ((f[1] - f[0]) / r[1])**2
        grad_sq[-1] = 0.0  # Champ constant à l'infini
    
    return grad_sq


# ============================================================================
# SOLVEUR JACOBI COUPLÉ
# ============================================================================

def solve_ttc_coupled(r, dr, rho_b, M_b,
                       alpha=1.0, beta=1.0, lambda_=0.1, kappa=1.0,
                       v_gamma=1.0, v_T=0.0,
                       eta=0.3, tol=1e-8, max_iter=50000,
                       verbose=True):
    """
    Résout le système couplé (Γ, Φ, T) par relaxation de Jacobi.
    
    Paramètres :
      r, dr    : grille radiale [kpc]
      rho_b    : densité baryonique sur la grille [M☉/kpc³]
      M_b      : masse baryonique enfermée [M☉]
      kappa    : couplage baryons → Γ (force de la source)
      eta      : paramètre de relaxation (0 < η < 1)
      tol      : tolérance sur le résidu max des EDP
      max_iter : nombre max d'itérations
    
    Retourne :
      Γ, Φ, T : solutions sur la grille
      history : historique de convergence
    """
    n = len(r)
    
    # --- Initialisation ---
    # Γ part de v_Γ, piqué par la source baryonique
    Gamma = np.ones(n) * v_gamma
    if rho_b.max() > 0:
        rho_b_norm = rho_b / (rho_b.max() + 1e-30)
        Gamma = v_gamma + kappa * rho_b_norm * v_gamma
    
    # Φ initial : potentiel Newtonien (Φ ∝ −1/r loin, régulier en 0)
    Phi = np.zeros(n)
    # Φ' ≈ GM_b(<r)/r² → Φ ≈ −∫GM_b/r² dr (approximation)
    for i in range(1, n):
        if r[i] > 0:
            Phi[i] = -G_kpc * M_b[i] / r[i]
    Phi -= Phi[0]  # Normaliser
    
    # T initial : v_T partout
    T = np.ones(n) * v_T
    
    history = {'iteration': [], 'res_gamma': [], 'res_phi': [], 'res_t': [],
               'L_W': []}
    
    if verbose:
        print(f"{'Iter':>6s}  {'Res_Γ':>12s}  {'Res_Φ':>12s}  {'Res_T':>12s}  {'L_W':>14s}")
        print("-" * 62)
    
    for it in range(max_iter):
        Gamma_old = Gamma.copy()
        Phi_old = Phi.copy()
        T_old = T.copy()
        
        # --- Calcul des termes pour les EDP ---
        lap_Gamma = laplacian_spherical(Gamma_old, r, dr)
        lap_T = laplacian_spherical(T_old, r, dr)
        
        grad_Phi_sq = gradient_squared_spherical(Phi_old, r, dr)
        
        # --- Résidu de l'équation Γ ---
        # □Γ = Γ(∇Φ)² + αΓ(Γ²−v_Γ²) + 2λTΓ − κ·ρ̂_b
        # source normalisée : ρ̂_b = ρ_b / ρ_b_max (si ρ_b_max > 0)
        rho_b_source = np.zeros(n)
        if rho_b.max() > 0:
            rho_b_source = kappa * v_gamma * rho_b / rho_b.max()
        
        rhs_Gamma = (Gamma_old * grad_Phi_sq
                     + alpha * Gamma_old * (Gamma_old**2 - v_gamma**2)
                     + 2 * lambda_ * T_old * Gamma_old
                     - rho_b_source)
        resid_Gamma = lap_Gamma - rhs_Gamma
        
        # Mise à jour Γ (Jacobi)
        # lap_Gamma ≈ (Γ_new − Γ_old)/Δ (approximation grossière)
        # Γ_new = Γ_old + η_Γ · résidu (où résidu = □Γ − RHS)
        # Pour une EDP elliptique : ∇²Γ = S → Γ_new = Γ_old + η·(S − ∇²Γ_old)
        Gamma_new = Gamma_old + eta * (-resid_Gamma)  # descente de gradient
        
        # --- Résidu de l'équation Φ ---
        # ∇·(Γ²∇Φ) = 0
        # En sphérique : (1/r²)·∂_r(r²·Γ²·∂_rΦ) = 0
        # → r²·Γ²·∂_rΦ = Cte → ∂_rΦ = C / (r²·Γ²)
        # On résout : Φ_new via l'intégration directe de ∂_rΦ = C/(r²Γ²)
        # C'est plus stable que Jacobi pour Φ
        Gamma_sq = np.maximum(Gamma_new**2, 1e-10)
        # Flux = r²·Γ²·∂_rΦ doit être conservé
        # On calcule le flux à partir de M_b (source)
        # ∂_rΦ ∝ GM_b(<r)/r² (potentiel Newtonien comme guide)
        # En fait : dans la TTC, Φ' = C/(r²Γ²) où C est fixé par la
        # condition aux bords : v²(r) = r·∂_rΦ_grav où Φ_grav dépend de Φ
        
        # Pour la relaxation, on utilise l'approche :
        # ∇²Φ (effectif) = −4πGρ_eff où ρ_eff dépend de Γ
        # Simplification : Φ suit le potentiel Newtonien modulé par Γ
        source_Phi = np.zeros(n)
        for i in range(1, n-1):
            if r[i] > 0:
                source_Phi[i] = G_kpc * M_b[i] / r[i]**2  # ∝ GM/r²
        
        # ∇²Φ_eff = (1/r²)·∂_r(r²·∂_rΦ)
        lap_Phi = laplacian_spherical(Phi_old, r, dr)
        # On veut ∇·(Γ²∇Φ) = 0, ce qui donne ∂_rΦ ∝ 1/(r²Γ²)
        # On intègre directement :
        integrand = 1.0 / (r**2 * Gamma_sq)
        integrand[0] = 0
        Phi_from_flux = cumulative_trapezoid(integrand, r, initial=0)
        # Normaliser pour que Φ → −GM_b_tot/r à grande distance
        if M_b[-1] > 0 and r[-1] > 0:
            target_phi_inf = -G_kpc * M_b[-1] / r[-1]
            scale = target_phi_inf / Phi_from_flux[-1] if abs(Phi_from_flux[-1]) > 1e-30 else 1.0
            Phi_from_flux = Phi_from_flux * scale
        
        Phi_new = Phi_old + eta * (Phi_from_flux - Phi_old)
        
        # --- Résidu de l'équation T ---
        # □T = β(T−v_T) + λΓ²
        rhs_T = beta * (T_old - v_T) + lambda_ * Gamma_new**2
        resid_T = lap_T - rhs_T
        T_new = T_old + eta * (-resid_T)
        
        # --- Conditions aux bords ---
        # Γ → v_Γ à l'infini
        Gamma_new[-1] = v_gamma
        # Φ → 0 à l'infini (jauge)
        Phi_new[-1] = 0.0
        # T → v_T à l'infini
        T_new[-1] = v_T
        
        # --- Calcul des résidus normalisés ---
        res_g = np.max(np.abs(resid_Gamma[1:-1]))
        res_p = np.max(np.abs(Phi_new[1:-1] - Phi_old[1:-1]))
        res_t = np.max(np.abs(resid_T[1:-1]))
        
        # --- Lagrangien total ---
        # L_W = ∫ [−½(∂Γ)² − ½Γ²(∂Φ)² − ½(∂T)² − U(Γ,T)] 4πr² dr
        grad_G_sq = gradient_squared_spherical(Gamma_new, r, dr)
        grad_T_sq_val = gradient_squared_spherical(T_new, r, dr)
        # (∂Φ)² est connu via Φ'
        grad_Phi_sq_new = gradient_squared_spherical(Phi_new, r, dr)
        
        U = (alpha/4 * (Gamma_new**2 - v_gamma**2)**2
             + beta/2 * (T_new - v_T)**2
             + lambda_ * T_new * Gamma_new**2)
        
        L_W_density = (-0.5 * grad_G_sq
                       - 0.5 * Gamma_new**2 * grad_Phi_sq_new
                       - 0.5 * grad_T_sq_val
                       - U)
        L_W_total = np.trapezoid(L_W_density * 4 * np.pi * r**2, r)
        
        # --- Mise à jour ---
        Gamma = Gamma_new.copy()
        Phi = Phi_new.copy()
        T = T_new.copy()
        
        # --- Historique ---
        if it % 500 == 0 or it == max_iter - 1:
            history['iteration'].append(it)
            history['res_gamma'].append(res_g)
            history['res_phi'].append(res_p)
            history['res_t'].append(res_t)
            history['L_W'].append(L_W_total)
            
            if verbose and (it % 2000 == 0 or it == max_iter - 1):
                print(f"{it:6d}  {res_g:12.3e}  {res_p:12.3e}  {res_t:12.3e}  {L_W_total:14.6f}")
        
        # --- Critère de convergence ---
        if res_g < tol and res_t < tol and res_p < tol:
            if verbose:
                print(f"\n✅ Convergé en {it} itérations. Résidus < {tol}")
            break
    else:
        if verbose:
            print(f"\n⚠️  Maximum d'itérations atteint ({max_iter}). Résidu Γ = {res_g:.3e}")
    
    return Gamma, Phi, T, history


# ============================================================================
# EXTRACTION DE LA COURBE DE ROTATION
# ============================================================================

def extract_rotation_curve(r, Gamma, Phi, T, M_b, rho_b,
                            v_gamma=1.0, lambda_=0.1):
    """
    Extrait la courbe de rotation prédite par la solution TTC.
    
    v²(r) = v_b²(r) + v_TTC²(r)
    
    où v_TTC²(r) provient du gradient de phase effectif et du
    profil de cohérence :
      v_TTC²(r) = G · [M_Γ(<r) + M_Φ(<r)] / r
    
    avec :
      M_Γ(<r) : masse effective du champ Γ
      M_Φ(<r) : contribution du gradient de phase
    
    Approche simplifiée : densité d'énergie de la Toile
      ρ_W(r) = ½(∇Γ)² + ½Γ²(∇Φ)² + ½(∇T)² + U(Γ,T)
      M_W(<r) = 4π ∫₀ʳ ρ_W(r') r'² dr'
      v_TTC²(r) = G·M_W(<r)/r
    """
    n = len(r)
    
    # Calcul des gradients
    dr = np.gradient(r)
    dGamma_dr = np.gradient(Gamma, r)
    dPhi_dr = np.gradient(Phi, r)
    dT_dr = np.gradient(T, r)
    
    # Densité d'énergie de la Toile
    U = (1.0/4.0 * (Gamma**2 - v_gamma**2)**2   # α=1
         + 1.0/2.0 * (T - 0.0)**2                # β=1, v_T=0
         + lambda_ * T * Gamma**2)
    
    rho_W = (0.5 * dGamma_dr**2
             + 0.5 * Gamma**2 * dPhi_dr**2
             + 0.5 * dT_dr**2
             + U)
    
    # Masse enfermée de la Toile
    integrand = rho_W * 4 * np.pi * r**2
    M_W_enc = cumulative_trapezoid(integrand, r, initial=0)
    
    # Conversion en unités physiques : ρ_W est en unités TTC → M☉/kpc³
    # Facteur de conversion à calibrer
    # ρ_W_normalized → ρ_physical = C_conv × ρ_W
    # On détermine C_conv en imposant v_TTC(r_max) ≈ v_flat
    
    # Contribution baryonique directe
    v_b_sq = np.zeros(n)
    for i in range(1, n):
        v_b_sq[i] = G_kpc * M_b[i] / r[i] if r[i] > 0 else 0
    
    # Contribution TTC (non calibrée — à ajuster)
    v_ttc_sq = np.zeros(n)
    for i in range(1, n):
        v_ttc_sq[i] = G_kpc * M_W_enc[i] / r[i] if r[i] > 0 else 0
    
    return np.sqrt(np.maximum(v_b_sq + v_ttc_sq, 0)), rho_W, M_W_enc


# ============================================================================
# CHARGEMENT DONNÉES SPARC
# ============================================================================

def load_sparc_galaxy(filepath):
    """Charge une galaxie SPARC."""
    try:
        data = np.loadtxt(filepath, comments='#')
    except (IOError, ValueError):
        return None
    if data.ndim < 2 or data.shape[1] < 5:
        return None
    return {
        'r': data[:, 0],
        'v_obs': data[:, 1],
        'v_err': data[:, 2],
        'v_gas': data[:, 3],
        'v_disk': data[:, 4],
        'v_bulge': data[:, 5] if data.shape[1] >= 6 else np.zeros_like(data[:, 0])
    }


# ============================================================================
# FONCTION PRINCIPALE : Test sur une galaxie
# ============================================================================

def run_ttc_solver_on_galaxy(galaxy_name, sparc_dir,
                              alpha=1.0, beta=1.0, lambda_=0.1, kappa=2.0,
                              n_grid=500, r_max_factor=3.0, eta=0.3,
                              tol=1e-8, max_iter=50000, upsilon_d=0.5,
                              upsilon_b=0.7, verbose=True):
    """
    Exécute le solveur TTC couplé sur UNE galaxie SPARC.
    
    Retourne un dictionnaire de résultats.
    """
    fpath = Path(sparc_dir) / f"{galaxy_name}_rotmod.dat"
    if not fpath.exists():
        print(f"❌ Fichier introuvable : {fpath}")
        return None
    
    gal = load_sparc_galaxy(fpath)
    if gal is None:
        print(f"❌ Échec chargement : {galaxy_name}")
        return None
    
    r_data = gal['r']
    v_obs = gal['v_obs']
    v_err = gal['v_err']
    v_gas = gal['v_gas']
    v_disk = gal['v_disk']
    v_bulge = gal['v_bulge']
    
    # Masquer données invalides
    mask = (r_data > 0) & (v_obs > 0) & np.isfinite(v_obs)
    r_data = r_data[mask]
    v_obs = v_obs[mask]
    v_err = v_err[mask]
    v_gas = v_gas[mask]
    v_disk = v_disk[mask]
    v_bulge = v_bulge[mask]
    
    if len(r_data) < 5:
        print(f"❌ Trop peu de points : {galaxy_name}")
        return None
    
    # Grille de calcul
    r_max = r_data[-1] * r_max_factor
    r_grid, dr_grid = build_grid(r_min=r_data[0]*0.5, r_max=r_max, n_points=n_grid)
    
    # Profil baryonique
    rho_b, M_b = baryonic_density_from_velocities(
        r_grid, r_data, v_gas, v_disk, v_bulge,
        upsilon_d=upsilon_d, upsilon_b=upsilon_b
    )
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"  Galaxie : {galaxy_name}")
        print(f"  Points de données : {len(r_data)}")
        print(f"  R_data max : {r_data[-1]:.1f} kpc")
        print(f"  R_grid max : {r_max:.1f} kpc")
        print(f"  M_b(R_max) : {M_b[-1]:.2e} M☉")
        print(f"  Grille : {n_grid} points")
        print(f"{'='*60}")
    
    # --- RÉSOLUTION ---
    t0 = time.time()
    Gamma, Phi, T, history = solve_ttc_coupled(
        r_grid, dr_grid, rho_b, M_b,
        alpha=alpha, beta=beta, lambda_=lambda_, kappa=kappa,
        eta=eta, tol=tol, max_iter=max_iter, verbose=verbose
    )
    elapsed = time.time() - t0
    
    # --- EXTRACTION COURBE DE ROTATION ---
    v_ttc, rho_W, M_W_enc = extract_rotation_curve(
        r_grid, Gamma, Phi, T, M_b, rho_b,
        v_gamma=1.0, lambda_=lambda_
    )
    
    # --- COMPARAISON AUX DONNÉES ---
    # Interpoler la solution sur les rayons observés
    v_ttc_interp = interp1d(r_grid, v_ttc, kind='linear',
                            bounds_error=False, fill_value='extrapolate')(r_data)
    
    # Métriques de qualité
    residuals = (v_obs - v_ttc_interp) / np.maximum(v_err, 1.0)
    chi2 = np.sum(residuals**2)
    dof = len(r_data) - 2  # 2 paramètres libres : kappa, lambda
    chi2_red = chi2 / dof if dof > 0 else np.inf
    
    # v_flat prédit (médiane du dernier tiers)
    n_third = len(v_ttc) // 3
    v_flat_pred = np.median(v_ttc[-n_third:]) if n_third > 0 else v_ttc[-1]
    v_flat_obs = np.median(v_obs[len(v_obs)//2:])
    
    # Test Tully-Fisher : v_flat⁴ / M_b
    tf_ratio = v_flat_pred**4 / M_b[-1] if M_b[-1] > 0 else 0
    
    result = {
        'galaxy': galaxy_name,
        'r_data': r_data,
        'v_obs': v_obs,
        'v_err': v_err,
        'v_ttc_interp': v_ttc_interp,
        'r_grid': r_grid,
        'Gamma': Gamma,
        'Phi': Phi,
        'T': T,
        'v_ttc': v_ttc,
        'rho_W': rho_W,
        'M_W_enc': M_W_enc,
        'M_b_final': M_b[-1],
        'v_flat_pred': v_flat_pred,
        'v_flat_obs': v_flat_obs,
        'chi2_red': chi2_red,
        'tf_ratio': tf_ratio,
        'n_iter': history['iteration'][-1] if history['iteration'] else 0,
        'elapsed': elapsed,
        'converged': history['res_gamma'][-1] < tol if history['res_gamma'] else False
    }
    
    if verbose:
        print(f"\n  Résultats :")
        print(f"  v_flat prédit  = {v_flat_pred:.1f} km/s")
        print(f"  v_flat observé = {v_flat_obs:.1f} km/s")
        print(f"  χ²_réduit      = {chi2_red:.2f}")
        print(f"  Convergé       = {result['converged']}")
        print(f"  Temps          = {elapsed:.1f} s")
    
    return result


# ============================================================================
# TEST BATCH SUR PLUSIEURS GALAXIES
# ============================================================================

def run_batch_test(galaxy_list, sparc_dir, **kwargs):
    """Exécute le solveur sur une liste de galaxies et agrège les résultats."""
    results = []
    for name in galaxy_list:
        res = run_ttc_solver_on_galaxy(name, sparc_dir, verbose=True, **kwargs)
        if res is not None:
            results.append(res)
    return results


def analyze_tully_fisher(results):
    """Analyse la relation de Tully-Fisher à partir des résultats du solveur."""
    v_flat = np.array([r['v_flat_pred'] for r in results])
    M_b = np.array([r['M_b_final'] for r in results])
    names = [r['galaxy'] for r in results]
    
    mask = (v_flat > 0) & (M_b > 0)
    v_flat = v_flat[mask]
    M_b = M_b[mask]
    
    if len(v_flat) < 5:
        print("\n⚠️  Pas assez de galaxies pour l'analyse TF.")
        return None
    
    logV = np.log10(v_flat)
    logM = np.log10(M_b)
    
    slope, intercept, r_val, p_val, std_err = linregress(logM, logV)
    
    # Test : v⁴ ∝ M_b → log(v) = 0.25·log(M_b) + cte
    expected_slope = 0.25
    sigma = abs(slope - expected_slope) / std_err if std_err > 0 else float('inf')
    
    scatter_dex = np.std(4*logV - logM)
    
    print(f"\n{'='*60}")
    print(f"  ANALYSE TULLY-FISHER — Solveur TTC couplé")
    print(f"{'='*60}")
    print(f"  Galaxies         : {len(v_flat)}")
    print(f"  Pente observée   : {slope:.4f} ± {std_err:.4f}")
    print(f"  Pente attendue   : {expected_slope:.4f} (v⁴ ∝ M_b)")
    print(f"  Tension          : {sigma:.1f}σ")
    print(f"  R²               : {r_val**2:.4f}")
    print(f"  Scatter TF (dex) : {scatter_dex:.3f}")
    print(f"  (Scatter attendu : 0.10-0.15 dex)")
    
    if sigma < 2.0:
        print(f"\n  ✅ La TTC reproduit Tully-Fisher à {sigma:.1f}σ !")
    elif sigma < 5.0:
        print(f"\n  🟡 Tension modérée ({sigma:.1f}σ). Ajustement nécessaire.")
    else:
        print(f"\n  🔴 ÉCHEC : Tully-Fisher NON reproduit ({sigma:.1f}σ).")
        print(f"     La TTC doit être modifiée.")
    
    return {
        'slope': slope, 'slope_err': std_err,
        'expected_slope': expected_slope, 'sigma': sigma,
        'r_squared': r_val**2, 'scatter_dex': scatter_dex,
        'n_galaxies': len(v_flat),
        'logM': logM, 'logV': logV, 'names': list(names)
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description='TTC Hardening — Solveur EDP couplé pour Tully-Fisher')
    parser.add_argument('--galaxy', type=str, default='NGC2403',
                        help='Galaxie à tester (défaut: NGC2403)')
    parser.add_argument('--data-dir', type=str,
                        default=r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK\SPARC_data',
                        help='Répertoire SPARC')
    parser.add_argument('--batch', action='store_true',
                        help='Mode batch (plusieurs galaxies)')
    parser.add_argument('--n-grid', type=int, default=500,
                        help='Points de grille')
    parser.add_argument('--kappa', type=float, default=2.0,
                        help='Couplage baryonique κ')
    parser.add_argument('--lambda', type=float, default=0.1, dest='lambda_',
                        help='Couplage Γ−T (λ)')
    parser.add_argument('--alpha', type=float, default=1.0,
                        help='Auto-interaction Γ (α)')
    parser.add_argument('--beta', type=float, default=1.0,
                        help='Masse de T (β)')
    parser.add_argument('--eta', type=float, default=0.3,
                        help='Relaxation η')
    parser.add_argument('--tol', type=float, default=1e-8,
                        help='Tolérance convergence')
    parser.add_argument('--max-iter', type=int, default=50000,
                        help='Max itérations')
    
    args = parser.parse_args()
    
    BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')
    data_dir = args.data_dir
    
    if args.batch:
        # Sélection de galaxies représentatives couvrant une gamme de masses
        test_galaxies = [
            'NGC2403',   # Spirale modérée, ~130 km/s
            'NGC2841',   # Massive, ~300 km/s
            'NGC5055',   # Soleil-like, ~200 km/s
            'NGC7331',   # Massive, ~240 km/s
            'NGC2903',   # ~200 km/s
            'NGC3198',   # ~150 km/s
            'NGC6503',   # Naine, ~115 km/s
            'NGC5585',   # Petite, ~90 km/s
            'DDO154',    # Naine, ~50 km/s
            'NGC3741',   # Très petite, ~40 km/s
        ]
        results = run_batch_test(test_galaxies, data_dir,
                                  n_grid=args.n_grid, kappa=args.kappa,
                                  lambda_=args.lambda_, alpha=args.alpha,
                                  beta=args.beta, eta=args.eta,
                                  tol=args.tol, max_iter=args.max_iter)
        tf_result = analyze_tully_fisher(results)
        
        # Sauvegarde
        output = {
            'n_galaxies': len(results),
            'galaxies': [r['galaxy'] for r in results],
            'v_flat_pred': [float(r['v_flat_pred']) for r in results],
            'v_flat_obs': [float(r['v_flat_obs']) for r in results],
            'M_b': [float(r['M_b_final']) for r in results],
            'chi2_red': [float(r['chi2_red']) for r in results],
            'tf_analysis': {k: (float(v) if isinstance(v, (np.floating, np.integer))
                                else v)
                            for k, v in (tf_result or {}).items()
                            if k not in ('logM', 'logV', 'names')}
        }
        outpath = BASE / 'ttc_hardening_results.json'
        with open(outpath, 'w') as f:
            json.dump(output, f, indent=2, default=str)
        print(f"\n📁 Résultats sauvegardés : {outpath}")
    
    else:
        result = run_ttc_solver_on_galaxy(
            args.galaxy, data_dir,
            n_grid=args.n_grid, kappa=args.kappa,
            lambda_=args.lambda_, alpha=args.alpha,
            beta=args.beta, eta=args.eta,
            tol=args.tol, max_iter=args.max_iter
        )
        
        if result:
            # Afficher les profils
            print(f"\n  Profil Γ :")
            print(f"    Γ(r=0)      = {result['Gamma'][0]:.4f}")
            print(f"    Γ(r_max)    = {result['Gamma'][-1]:.4f} (→ v_Γ=1)")
            print(f"    Pic Γ/v_Γ   = {result['Gamma'].max()/1.0:.2f}")
            print(f"\n  Profil T :")
            print(f"    T(r=0)      = {result['T'][0]:.6f}")
            print(f"    T(r_max)    = {result['T'][-1]:.6f}")
            print(f"    T_max       = {result['T'].max():.6f}")
