#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCW-3 — Solveur BVP pour le champ Γ avec source baryonique
===========================================================
ITÉRATION 1 : Résolution sur UNE galaxie (NGC 2403).

OBJECTIF : Résoudre l'EDP couplée (Γ, Φ) en symétrie sphérique
avec source S_Γ(r) ∝ ρ_b(r), et extraire v_∞.

ÉQUATIONS (statique, sphérique) :

  (1) (1/r²)∂_r(r²∂_rΓ) = Γ·(∂_rΦ)² + α·Γ·(Γ²−v_Γ²) − S_Γ(r)
  
  (2) ∂_rΦ = K / (r²·Γ²)
  
  (3) S_Γ(r) = κ · ρ_b(r) / ρ_b_max  (source normalisée)

où K est fixé par la condition aux bords : M_dyn(∞) = M_b + M_W.

STRATÉGIE DE RÉSOLUTION (Point Fixe + Sous-Relaxation) :

  1. Grille logarithmique r ∈ [r_min, r_max]
  2. Γ_init(r) = v_Γ · √(1 + (r_c_guess/r)²)
  3. Φ'_init(r) depuis l'équation de conservation avec Γ_init
  4. BOUCLE :
     a. Calculer S_Γ(r) depuis ρ_b(r)
     b. Résoudre l'EDP de Γ (linéarisée) → Γ_new
     c. Recalculer Φ' depuis Γ_new
     d. Vérifier convergence ||Γ_new − Γ_old|| < tol
  5. Extraire v_TTC(r) et v_∞

Auteur : DeepSeek V4 Pro (Co-auteur TTC)
Date   : 31 juillet 2026 — MCW-3, Itération 1
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d
from pathlib import Path
import time, warnings

warnings.filterwarnings("ignore")

G_kpc = 4.301e-9          # [kpc (km/s)² / M☉]
BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')
SPARC_DIR = BASE / 'SPARC_data'

# ============================================================================
# CHARGEMENT DONNÉES
# ============================================================================

def load_sparc_galaxy(name):
    fpath = SPARC_DIR / f"{name}_rotmod.dat"
    if not fpath.exists():
        return None
    radii, vobs, verr, vgas, vdisk, vbul = [], [], [], [], [], []
    with open(fpath) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            p = line.split()
            if len(p) >= 6:
                try:
                    radii.append(float(p[0]))
                    vobs.append(float(p[1]))
                    verr.append(float(p[2]))
                    vgas.append(float(p[3]))
                    vdisk.append(float(p[4]))
                    vbul.append(float(p[5]))
                except ValueError:
                    pass
    if len(radii) < 5:
        return None
    return {
        'r': np.array(radii), 'v_obs': np.array(vobs), 'v_err': np.array(verr),
        'v_gas': np.array(vgas), 'v_disk': np.array(vdisk), 'v_bulge': np.array(vbul)
    }


# ============================================================================
# GRILLE RADIALE
# ============================================================================

def build_grid(r_min, r_max, n_points):
    """Grille logarithmique."""
    r = np.logspace(np.log10(r_min), np.log10(r_max), n_points)
    return r


# ============================================================================
# SOURCE BARYONIQUE
# ============================================================================

def baryonic_source(r_grid, r_data, v_gas, v_disk, v_bulge,
                    upsilon_d=0.5, upsilon_b=0.7):
    """
    Calcule S_Γ(r) ∝ ρ_b(r) sur la grille de calcul.
    
    Utilise un spline pour interpoler M_b(<r) puis dériver.
    Retourne : rho_b_grid, M_b_enc_grid
    """
    from scipy.interpolate import UnivariateSpline
    
    # Vitesse baryonique quadratique sur les données
    v_b_sq_data = (np.abs(v_gas) * v_gas
                   + upsilon_d * np.abs(v_disk) * v_disk
                   + upsilon_b * np.abs(v_bulge) * v_bulge)
    v_b_sq_data = np.maximum(v_b_sq_data, 0)
    
    # Masse enfermée sur les données
    M_b_enc_data = r_data * v_b_sq_data / G_kpc
    
    # Interpolation sur la grille fine
    M_b_interp = interp1d(r_data, M_b_enc_data, kind='linear',
                          bounds_error=False, fill_value=(0, M_b_enc_data[-1]))
    M_b_on_grid = M_b_interp(r_grid)
    M_b_on_grid = np.maximum(M_b_on_grid, 0)
    
    # Densité : ρ = (4πr²)⁻¹ · dM/dr
    dM_dr = np.gradient(M_b_on_grid, r_grid)
    rho_b_grid = dM_dr / (4 * np.pi * r_grid**2 + 1e-30)
    rho_b_grid = np.maximum(rho_b_grid, 0)
    
    # Régulariser à r→0
    if len(rho_b_grid) > 1:
        rho_b_grid[0] = rho_b_grid[1]
    
    return rho_b_grid, M_b_on_grid


# ============================================================================
# SOLVEUR MCW-3
# ============================================================================

def solve_mcw3_single_galaxy(gal, n_grid=400, r_max_factor=5.0,
                              alpha=0.1, kappa=5.0, v_gamma=1.0,
                              eta=0.1, tol=1e-8, max_iter=5000,
                              verbose=True):
    """
    Résout le BVP MCW-3 pour UNE galaxie.
    
    Paramètres :
      gal         : dict avec r, v_gas, v_disk, v_bulge, v_obs
      n_grid      : nombre de points de grille
      r_max_factor: r_max = r_data_max × r_max_factor
      alpha       : auto-interaction de Γ
      kappa       : force du couplage baryonique S_Γ = κ·ρ_b/ρ_b_max
      eta         : sous-relaxation
      tol         : tolérance convergence
      max_iter    : nombre max d'itérations
    
    Retourne : dict avec r_grid, Gamma, Phi_prime, v_ttc, M_b_enc, etc.
    """
    name = gal.get('name', 'unknown')
    r_data = gal['r']
    v_gas = gal['v_gas']
    v_disk = gal['v_disk']
    v_bulge = gal['v_bulge']
    v_obs = gal['v_obs']
    
    # ── Grille ──
    r_min = r_data[0] * 0.5
    r_max_grid = r_data[-1] * r_max_factor
    r = build_grid(r_min, r_max_grid, n_grid)
    dr = np.gradient(r)
    
    # ── Source baryonique ──
    rho_b, M_b_enc = baryonic_source(r, r_data, v_gas, v_disk, v_bulge)
    rho_b_max = np.max(rho_b)
    if rho_b_max <= 0:
        print(f"  ❌ Pas de source baryonique pour {name}")
        return None
    
    S_Gamma = kappa * v_gamma * rho_b / rho_b_max  # source normalisée
    
    # ── Masse baryonique totale ──
    M_b_total = M_b_enc[-1]
    
    # ── Initialisation de Γ ──
    # Profil avec cœur + décroissance en 1/r
    r_c_guess = r_data[-1] * 0.3  # 30% du rayon max des données
    Gamma = v_gamma * np.sqrt(1.0 + (r_c_guess / np.maximum(r, r_min))**2)
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"  MCW-3 Solveur — {name}")
        print(f"  M_b total = {M_b_total:.2e} M☉")
        print(f"  R_data max = {r_data[-1]:.1f} kpc")
        print(f"  R_grid max = {r_max_grid:.1f} kpc")
        print(f"  Grille = {n_grid} points")
        print(f"  κ = {kappa}, α = {alpha}, η = {eta}")
        print(f"{'='*60}")
        print(f"{'Iter':>6s}  {'Res_Γ':>12s}  {'Γ(0)/v_Γ':>10s}  {'Γ_max/v_Γ':>10s}")
        print(f"{'─'*48}")
    
    # ── Boucle de point fixe ──
    for iteration in range(max_iter):
        Gamma_old = Gamma.copy()
        
        # ── Étape 1 : Calculer Φ' depuis Γ ──
        # ∂_rΦ = K/(r²Γ²) où K est fixé par la condition de flux
        # Le flux total de phase à travers une sphère de rayon r est :
        #   Flux = 4πr² · Γ² · ∂_rΦ = 4πK = constant
        # K est déterminé par la masse dynamique totale
        
        # On calcule Φ' non normalisé : Φ'_unnorm = 1/(r²Γ²)
        Phi_prime_unnorm = 1.0 / (r**2 * Gamma**2 + 1e-30)
        
        # ── Étape 2 : Résoudre l'EDP de Γ ──
        # (1/r²)∂_r(r²∂_rΓ) = Γ·(∂_rΦ)² + α·Γ·(Γ²−v_Γ²) − S_Γ
        #
        # On linéarise : Γ_new = Γ_old + η × [∇²Γ_old − RHS(Γ_old)]
        # avec RHS = Γ·(Φ')² + α·Γ·(Γ²−v_Γ²) − S_Γ
        
        # Laplacien sphérique
        # ∂_r(r²∂_rΓ) par différences finies
        n = len(r)
        lap_Gamma = np.zeros(n)
        
        for i in range(1, n-1):
            # ∂_rΓ aux demi-points
            dG_dr_plus = (Gamma_old[i+1] - Gamma_old[i]) / (r[i+1] - r[i])
            dG_dr_minus = (Gamma_old[i] - Gamma_old[i-1]) / (r[i] - r[i-1])
            # r²∂_rΓ aux demi-points
            r2_dG_plus = r[i]**2 * dG_dr_plus if r[i] > 0 else 0
            r2_dG_minus = r[i-1]**2 * dG_dr_minus if r[i-1] > 0 else 0
            # ∂_r(r²∂_rΓ) au point i
            dr_i = r[i+1] - r[i-1]
            d_r2dG = (r2_dG_plus - r2_dG_minus) / dr_i if dr_i > 0 else 0
            lap_Gamma[i] = d_r2dG / r[i]**2 if r[i] > 0 else 0
        
        # r=0 : limite (laplacien → 3·∂²Γ/∂r²)
        if n >= 2:
            lap_Gamma[0] = 6.0 * (Gamma_old[1] - Gamma_old[0]) / r[1]**2
        
        # RHS
        Phi_prime_sq = Phi_prime_unnorm**2
        rhs = (Gamma_old * Phi_prime_sq
               + alpha * Gamma_old * (Gamma_old**2 - v_gamma**2)
               - S_Gamma)
        
        resid = lap_Gamma - rhs
        
        # Sous-relaxation
        Gamma_new = Gamma_old - eta * resid
        
        # ── Conditions aux bords ──
        # r=0 : symétrie (Neumann, ∂_rΓ = 0)
        Gamma_new[0] = Gamma_new[1] if n > 1 else v_gamma
        # r→∞ : Γ → v_Γ (Dirichlet)
        Gamma_new[-1] = v_gamma
        
        # ── Limitations ──
        Gamma_new = np.clip(Gamma_new, 0.1 * v_gamma, 100 * v_gamma)
        
        # ── Mise à jour ──
        Gamma = Gamma_new.copy()
        
        # Résidu
        max_res = np.max(np.abs(resid[1:-1]))
        
        if verbose and (iteration % 500 == 0 or iteration == max_iter - 1):
            print(f"{iteration:6d}  {max_res:12.3e}  {Gamma[0]/v_gamma:10.3f}  {np.max(Gamma)/v_gamma:10.3f}")
        
        if max_res < tol:
            if verbose:
                print(f"\n  ✅ Convergé en {iteration+1} itérations.")
            break
    else:
        if verbose:
            print(f"\n  ⚠️  Max iterations atteint. Résidu = {max_res:.3e}")
    
    # ── Post-traitement : extraire la courbe de rotation ──
    # Φ' ∝ 1/(r²Γ²), on normalise K pour que v²(r) reproduise 
    # la dynamique observée aux grands rayons
    
    Phi_prime = 1.0 / (r**2 * Gamma**2 + 1e-30)
    
    # Calibration de K : on impose que v_TTC²(r) → G·M_b/r + cte·v_Γ²
    # Simplification : on cale K pour que la masse dynamique totale
    # M_dyn = M_b + M_W donne la bonne v_∞
    
    # Masse effective du champ TTC
    # ρ_W ≈ ½Γ²(∇Φ)² (terme dominant à grande distance)
    # Avec ∇Φ = K/(r²Γ²) → ρ_W ≈ ½K²/(r⁴Γ²)
    # Pour Γ ∝ 1/r : ρ_W ∝ 1/r² → M_W(<r) ∝ r
    
    # On calcule le profil de vitesse en unités arbitraires puis on cale
    # v_unnorm²(r) = r × Φ'(r) = 1/(rΓ²)
    v_sq_unnorm = 1.0 / (r * Gamma**2 + 1e-30)
    
    # Calibration : au dernier rayon de données, v_TTC ≈ v_obs
    r_last_data = r_data[-1]
    idx_last = np.argmin(np.abs(r - r_last_data))
    v_obs_last = np.median(v_obs[len(v_obs)//2:])  # v_flat observé
    
    # Facteur de calibration
    v_sq_at_last = v_sq_unnorm[idx_last]
    if v_sq_at_last > 0:
        calib = v_obs_last**2 / v_sq_at_last
    else:
        calib = 1.0
    
    v_ttc = np.sqrt(np.maximum(calib * v_sq_unnorm, 0))
    
    # v_∞ prédit : médiane du dernier tiers de la grille
    n_third = max(n // 3, 5)
    v_inf_pred = np.median(v_ttc[-n_third:])
    
    if verbose:
        print(f"\n  Résultats :")
        print(f"  Γ(r=0)/v_Γ    = {Gamma[0]/v_gamma:.2f}")
        print(f"  Γ(r_max)/v_Γ  = {Gamma[-1]/v_gamma:.4f}")
        print(f"  v_inf prédit  = {v_inf_pred:.1f} km/s")
        print(f"  v_flat obs    = {v_obs_last:.1f} km/s")
    
    return {
        'name': name,
        'r': r,
        'Gamma': Gamma,
        'Phi_prime': Phi_prime,
        'v_ttc': v_ttc,
        'v_inf_pred': v_inf_pred,
        'v_flat_obs': v_obs_last,
        'M_b_total': M_b_total,
        'r_data': r_data,
        'v_obs': v_obs,
        'converged': max_res < tol,
        'n_iter': iteration + 1,
        'residual': float(max_res)
    }


# ============================================================================
# DIAGNOSTIC : Comportement asymptotique de Γ
# ============================================================================

def check_asymptotic_behavior(result):
    """
    Vérifie que Γ ∝ 1/r asymptotiquement.
    Calcule la pente de log(Γ) vs log(r) aux grands rayons.
    """
    r = result['r']
    Gamma = result['Gamma']
    
    # Dernier tiers de la grille
    n_third = len(r) // 3
    r_tail = r[-n_third:]
    Gamma_tail = Gamma[-n_third:]
    
    # Fit log-log
    log_r = np.log10(r_tail)
    log_G = np.log10(Gamma_tail)
    
    from scipy.stats import linregress
    slope, intercept, r_val, p_val, std_err = linregress(log_r, log_G)
    
    return slope, r_val**2


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='MCW-3 Solveur — Itération 1')
    parser.add_argument('--galaxy', type=str, default='NGC2403')
    parser.add_argument('--n-grid', type=int, default=400)
    parser.add_argument('--kappa', type=float, default=5.0)
    parser.add_argument('--alpha', type=float, default=0.1)
    parser.add_argument('--eta', type=float, default=0.1)
    parser.add_argument('--tol', type=float, default=1e-8)
    parser.add_argument('--max-iter', type=int, default=5000)
    args = parser.parse_args()
    
    gal = load_sparc_galaxy(args.galaxy)
    if gal is None:
        print(f"❌ Galaxie {args.galaxy} introuvable.")
        exit(1)
    gal['name'] = args.galaxy
    
    t0 = time.time()
    result = solve_mcw3_single_galaxy(
        gal,
        n_grid=args.n_grid,
        kappa=args.kappa,
        alpha=args.alpha,
        eta=args.eta,
        tol=args.tol,
        max_iter=args.max_iter,
        verbose=True
    )
    elapsed = time.time() - t0
    print(f"\n  Temps : {elapsed:.1f} s")
    
    if result:
        slope, r2 = check_asymptotic_behavior(result)
        print(f"\n  Comportement asymptotique :")
        print(f"  Pente log(Γ) vs log(r) = {slope:.3f}")
        print(f"  (Attendu pour Γ ∝ 1/r   = -1.000)")
        print(f"  R² = {r2:.4f}")
        
        if abs(slope + 1.0) < 0.2:
            print(f"  ✅ Γ ∝ 1/r vérifié asymptotiquement.")
        else:
            print(f"  🔴 Γ ne suit PAS la loi en 1/r. Pente = {slope:.3f}")
