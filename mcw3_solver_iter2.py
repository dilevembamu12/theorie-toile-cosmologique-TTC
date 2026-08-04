#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCW-3 — Itération 2 : Solveur BVP stabilisé avec continuation
===============================================================
ADIMENSIONNEMENT + MÉTHODE DE CONTINUATION

Problème de l'Itération 1 : le solveur diverge parce que le terme
Γ(∂Φ)² a une normalisation incorrecte (K ∼ 10⁴ en unités TTC).

SOLUTION :
  1. Adimensionner TOUTES les quantités
  2. Définir r₀ = rayon du disque, v_Γ = 1 (normalisation)
  3. Échelle de Φ : Φ₀ = √(r₀²) = r₀
  4. Méthode de continuation : partir de κ=0 et augmenter progressivement

ÉQUATIONS ADIMENSIONNÉES (tilde omis par clarté) :

  (1/r²)∂_r(r²∂_rΓ) = Γ·(∂_rΦ)² + α̃·Γ·(Γ²−1) − κ̃·S(r)
  
  ∂_rΦ = K̃ / (r²Γ²)
  
  où α̃ = α·v_Γ²·r₀², κ̃ = κ·r₀², K̃ = K/(v_Γ²·r₀)

  v²(r) = r·∂_rΦ  (en unités de v₀², où v₀ = v_Γ·r₀)

STRATÉGIE DE CONTINUATION :
  κ = 0 → 0.1 → 0.2 → ... → κ_target
  Chaque étape utilise la solution précédente comme initial guess.

Auteur : DeepSeek V4 Pro
Date   : 31 juillet 2026 — MCW-3, Itération 2
"""

import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.interpolate import interp1d
from scipy.stats import linregress
from pathlib import Path
import time, warnings

warnings.filterwarnings("ignore")

G_kpc = 4.301e-9
BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')
SPARC_DIR = BASE / 'SPARC_data'

# ============================================================================
# CHARGEMENT
# ============================================================================

def load_sparc_galaxy(name):
    fpath = SPARC_DIR / f"{name}_rotmod.dat"
    if not fpath.exists():
        return None
    radii, vobs, verr, vgas, vdisk, vbul = [], [], [], [], [], []
    with open(fpath) as f:
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            p = line.split()
            if len(p) >= 6:
                try:
                    radii.append(float(p[0])); vobs.append(float(p[1]))
                    verr.append(float(p[2])); vgas.append(float(p[3]))
                    vdisk.append(float(p[4])); vbul.append(float(p[5]))
                except ValueError: pass
    if len(radii) < 5: return None
    return {'r': np.array(radii), 'v_obs': np.array(vobs), 'v_err': np.array(verr),
            'v_gas': np.array(vgas), 'v_disk': np.array(vdisk),
            'v_bulge': np.array(vbul)}


# ============================================================================
# GRILLE ADIMENSIONNÉE
# ============================================================================

def build_dimensionless_grid(r_data, r_max_factor=8.0, n_points=500):
    """
    Grille logarithmique adimensionnée.
    r₀ = rayon_max_données (échelle caractéristique du disque)
    r̃ ∈ [r_min/r₀, r_max_factor]
    """
    r0 = r_data[-1]  # rayon max des données comme échelle
    r_tilde_min = r_data[0] / r0 * 0.5
    r_tilde_max = r_max_factor
    r_tilde = np.logspace(np.log10(r_tilde_min), np.log10(r_tilde_max), n_points)
    return r_tilde, r0


# ============================================================================
# SOURCE BARYONIQUE ADIMENSIONNÉE
# ============================================================================

def build_dimensionless_source(r_tilde, r0, gal, upsilon_d=0.5, upsilon_b=0.7):
    """
    Construit S̃(r̃) = ρ_b(r̃)/ρ_b_max (source normalisée [0,1]).
    """
    r_data = gal['r']
    r_tilde_data = r_data / r0
    
    v_b_sq = (np.abs(gal['v_gas'])*gal['v_gas']
              + upsilon_d*np.abs(gal['v_disk'])*gal['v_disk']
              + upsilon_b*np.abs(gal['v_bulge'])*gal['v_bulge'])
    v_b_sq = np.maximum(v_b_sq, 0)
    
    # M_b(<r) en unités physiques
    M_b_enc_data = r_data * v_b_sq / G_kpc
    M_b_total = M_b_enc_data[-1]
    
    # Interpolation sur grille adimensionnée
    M_b_interp = interp1d(r_tilde_data, M_b_enc_data, kind='linear',
                          bounds_error=False, fill_value=(0, M_b_total))
    M_b_on_grid = M_b_interp(r_tilde)
    M_b_on_grid = np.maximum(M_b_on_grid, 0)
    
    # Densité
    dM_dr_tilde = np.gradient(M_b_on_grid, r_tilde)
    rho_b = dM_dr_tilde / (4*np.pi * r_tilde**2 + 1e-30)
    rho_b = np.maximum(rho_b, 0)
    if len(rho_b) > 1:
        rho_b[0] = rho_b[1]
    
    # Normaliser
    rho_max = np.max(rho_b)
    S_tilde = rho_b / rho_max if rho_max > 0 else np.zeros_like(rho_b)
    
    return S_tilde, M_b_total, M_b_on_grid


# ============================================================================
# SOLVEUR BVP STABILISÉ (MÉTHODE DE CONTINUATION)
# ============================================================================

def solve_bvp_continuation(r_tilde, S_tilde, M_b_total, r0,
                            kappa_target=1.0, alpha_tilde=1.0,
                            eta=0.05, tol=1e-8, max_iter_per_step=3000,
                            n_continuation_steps=20, verbose=True):
    """
    Résout le BVP par continuation en κ.
    
    κ varie de 0 à κ_target en n_continuation_steps.
    À κ=0, la solution est Γ = 1 (vide).
    """
    n = len(r_tilde)
    dr_tilde = np.gradient(r_tilde)
    
    # Solution initiale (κ=0) : Γ = 1 partout, Φ' = K/(r²)
    Gamma = np.ones(n)
    
    # Estimation de K̃
    # v² = r·∂_rΦ où ∂_rΦ = K̃/(r²Γ²)
    # Aux grands r (Γ→1) : v² ≈ K̃/r
    # Le v_flat observé donne K̃ ≈ v_flat² × r_data_max / r₀²... non
    # En unités adimensionnées : ṽ² = r̃·∂_r̃Φ̃ = K̃/(r̃·Γ²)
    # Pour Γ→1 aux grands r̃ : ṽ² ≈ K̃/r̃
    # On veut ṽ² ∼ 1 aux grands r̃ → K̃ ∼ r̃_max
    
    # En pratique, on détermine K̃ pour que ṽ²(r̃=1) ≈ (v_obs/v_Γ)²
    # ṽ = v_obs / v_ref où v_ref est l'échelle de vitesse TTC
    # On fixe K̃ pour que la solution donne la bonne amplitude
    
    # Simplification : on utilise K̃ comme paramètre et on calibre a posteriori
    # Pour l'instant, K̃ = 1 (ordre 1)
    K_tilde = 1.0
    
    kappa_values = np.linspace(0, kappa_target, n_continuation_steps + 1)[1:]
    
    if verbose:
        print(f"\n  Continuation : κ = 0 → {kappa_target} en {n_continuation_steps} étapes")
        print(f"  α̃ = {alpha_tilde:.3f}, K̃ = {K_tilde:.3f}")
        print(f"  {'Étape':>6s} {'κ':>8s}  {'Res_Γ':>12s}  {'Γ(0)':>8s}  {'Iters':>6s}")
        print(f"  {'─'*50}")
    
    for step, kappa in enumerate(kappa_values):
        kappa_tilde = kappa * r0**2  # adimensionnement
        S_eff = kappa_tilde * S_tilde
        
        for iteration in range(max_iter_per_step):
            Gamma_old = Gamma.copy()
            
            # ── Calculer Φ' depuis Γ ──
            # Φ' = K̃/(r̃²Γ²)
            Phi_prime = K_tilde / (r_tilde**2 * Gamma_old**2 + 1e-30)
            Phi_prime_sq = Phi_prime**2
            
            # ── Laplacien de Γ ──
            lap_Gamma = np.zeros(n)
            
            # Points intérieurs : schéma centré d'ordre 2
            for i in range(1, n-1):
                # ∂_r̃Γ aux demi-points
                h_plus = r_tilde[i+1] - r_tilde[i]
                h_minus = r_tilde[i] - r_tilde[i-1]
                dG_plus = (Gamma_old[i+1] - Gamma_old[i]) / h_plus if h_plus > 0 else 0
                dG_minus = (Gamma_old[i] - Gamma_old[i-1]) / h_minus if h_minus > 0 else 0
                
                r2_plus = r_tilde[i]**2 * dG_plus
                r2_minus = r_tilde[i-1]**2 * dG_minus
                
                h_avg = 0.5 * (h_plus + h_minus)
                d_r2dG = (r2_plus - r2_minus) / h_avg if h_avg > 0 else 0
                lap_Gamma[i] = d_r2dG / r_tilde[i]**2 if r_tilde[i] > 0 else 0
            
            # r=0 : développement de Taylor
            if n >= 3:
                lap_Gamma[0] = 6.0 * (Gamma_old[1] - Gamma_old[0]) / r_tilde[1]**2
            
            # ── RHS ──
            rhs = (Gamma_old * Phi_prime_sq
                   + alpha_tilde * Gamma_old * (Gamma_old**2 - 1.0)
                   - S_eff)
            
            resid = lap_Gamma - rhs
            
            # Sous-relaxation adaptative
            max_update = np.max(np.abs(eta * resid))
            if max_update > 0.5:
                eta_eff = eta * 0.5 / max_update
            else:
                eta_eff = eta
            
            Gamma_new = Gamma_old - eta_eff * resid
            
            # ── Conditions aux bords ──
            Gamma_new[0] = Gamma_new[1]  # Neumann en r=0
            Gamma_new[-1] = 1.0           # Dirichlet : Γ → v_Γ à l'infini
            
            # ── Positivité ──
            Gamma_new = np.maximum(Gamma_new, 0.01)
            Gamma_new = np.minimum(Gamma_new, 100.0)
            
            Gamma = Gamma_new.copy()
            
            max_res = np.max(np.abs(resid[1:-1]))
            
            if max_res < tol:
                break
        
        if verbose:
            print(f"  {step+1:6d} {kappa:8.3f}  {max_res:12.3e}  {Gamma[0]:8.3f}  {iteration+1:6d}")
    
    # ── Post-traitement ──
    # Courbe de rotation adimensionnée
    Phi_prime_final = K_tilde / (r_tilde**2 * Gamma**2 + 1e-30)
    v_sq_tilde = r_tilde * Phi_prime_final
    
    # Recalibrer en unités physiques
    # v_phys²(r) = v_ref² × ṽ²(r̃) où v_ref est à déterminer
    # On cale pour que v_TTC coïncide avec v_obs aux grands rayons
    
    # Convertir r_tilde → r_phys
    r_phys = r_tilde * r0
    
    # v_phys²(r) ∝ ṽ²(r̃). On détermine le facteur au dernier point de donnée
    r_data = gal['r'] if 'gal' in dir() else None
    
    return {
        'r_tilde': r_tilde,
        'r0': r0,
        'r_phys': r_phys,
        'Gamma': Gamma,
        'Phi_prime': Phi_prime_final,
        'v_sq_tilde': v_sq_tilde,
        'K_tilde': K_tilde,
        'M_b_total': M_b_total,
        'converged': max_res < tol,
        'residual': float(max_res),
        'n_iter_total': (step+1) * (iteration+1)
    }


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def run_mcw3_iter2(galaxy_name='NGC2403', kappa_target=1.0, alpha_tilde=0.1,
                    eta=0.05, n_continuation=20, n_grid=500, verbose=True):
    """
    Exécute le solveur MCW-3 Itération 2 sur une galaxie.
    """
    gal = load_sparc_galaxy(galaxy_name)
    if gal is None:
        print(f"❌ {galaxy_name} introuvable.")
        return None
    gal['name'] = galaxy_name
    
    # Grille adimensionnée
    r_tilde, r0 = build_dimensionless_grid(gal['r'], n_points=n_grid)
    
    # Source
    S_tilde, M_b_total, M_b_grid = build_dimensionless_source(r_tilde, r0, gal)
    
    if verbose:
        v_flat_obs = np.median(gal['v_obs'][len(gal['v_obs'])//2:])
        print(f"{'='*60}")
        print(f"  MCW-3 ITÉRATION 2 — {galaxy_name}")
        print(f"  M_b total  = {M_b_total:.2e} M☉")
        print(f"  v_flat obs = {v_flat_obs:.1f} km/s")
        print(f"  r₀ (scale) = {r0:.1f} kpc")
        print(f"  Grille     = {n_grid} points, r̃ ∈ [{r_tilde[0]:.3f}, {r_tilde[-1]:.1f}]")
        print(f"{'='*60}")
    
    t0 = time.time()
    result = solve_bvp_continuation(
        r_tilde, S_tilde, M_b_total, r0,
        kappa_target=kappa_target,
        alpha_tilde=alpha_tilde,
        eta=eta,
        max_iter_per_step=3000,
        n_continuation_steps=n_continuation,
        verbose=verbose
    )
    elapsed = time.time() - t0
    
    if result is None:
        return None
    
    # Ajouter les données d'observation
    result['galaxy'] = galaxy_name
    result['r_data'] = gal['r']
    result['v_obs'] = gal['v_obs']
    result['v_gas'] = gal['v_gas']
    result['v_disk'] = gal['v_disk']
    result['elapsed'] = elapsed
    
    # ── Calibration et comparaison ──
    # v_sq_tilde(r̃) = r̃·Φ' est sans dimension.
    # v_phys²(r) = C_calib × v_sq_tilde(r̃)
    # On détermine C_calib en imposant v_TTC(r_data_max/2) ≈ v_obs(r_data_max/2)
    
    r_data = gal['r']
    v_obs = gal['v_obs']
    r_half = r_data[len(r_data)//2]
    v_obs_half = v_obs[len(v_obs)//2]
    
    # Interpoler v_sq_tilde au rayon r_half
    r_tilde_half = r_half / r0
    v_sq_tilde_half = np.interp(r_tilde_half, r_tilde, result['v_sq_tilde'])
    
    if v_sq_tilde_half > 0:
        C_calib = v_obs_half**2 / v_sq_tilde_half
    else:
        C_calib = 1.0
    
    # Courbe de rotation calibrée
    v_ttc_phys = np.sqrt(np.maximum(C_calib * result['v_sq_tilde'], 0))
    
    # v_∞ prédit
    n_third = max(len(v_ttc_phys)//3, 5)
    v_inf_pred = np.median(v_ttc_phys[-n_third:])
    v_flat_obs = np.median(gal['v_obs'][len(gal['v_obs'])//2:])
    
    result['C_calib'] = C_calib
    result['v_ttc_phys'] = v_ttc_phys
    result['v_inf_pred'] = v_inf_pred
    result['v_flat_obs'] = v_flat_obs
    
    # Analyse asymptotique
    n_tail = max(len(r_tilde)//3, 10)
    log_r_tail = np.log10(r_tilde[-n_tail:])
    log_G_tail = np.log10(result['Gamma'][-n_tail:])
    slope, _, r_val, _, _ = linregress(log_r_tail, log_G_tail)
    
    result['asymptotic_slope'] = slope
    result['asymptotic_r2'] = r_val**2
    
    if verbose:
        print(f"\n  ── RÉSULTATS ──")
        print(f"  Convergence      : {'✅' if result['converged'] else '⚠️'}")
        print(f"  Temps            : {elapsed:.1f} s")
        print(f"  Γ(0)             : {result['Gamma'][0]:.3f}")
        print(f"  Γ(r_max)         : {result['Gamma'][-1]:.4f}")
        print(f"  Pente asymptotique: {slope:.3f}  (Γ ∝ 1/r → pente = −1)")
        print(f"  R² asymptotique   : {r_val**2:.4f}")
        print(f"  C_calib           : {C_calib:.1f} (km/s)²")
        print(f"  v_inf prédit      : {v_inf_pred:.1f} km/s")
        print(f"  v_flat observé    : {v_flat_obs:.1f} km/s")
        
        diff_pct = abs(v_inf_pred - v_flat_obs) / v_flat_obs * 100
        print(f"  Différence        : {diff_pct:.1f}%")
        
        if abs(slope + 1.0) < 0.15:
            print(f"\n  ✅ Γ ∝ 1/r vérifié asymptotiquement !")
        elif slope < -0.5:
            print(f"\n  🟡 Γ décroît mais moins vite que 1/r.")
        else:
            print(f"\n  🔴 Γ ne décroît PAS en loi de puissance.")
    
    return result


# ============================================================================
# BALAYAGE DE α̃
# ============================================================================

def scan_alpha(galaxy_name='NGC2403', alpha_values=None):
    """Balaye α̃ pour trouver le régime où Γ ∝ 1/r."""
    if alpha_values is None:
        alpha_values = [0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0]
    
    print(f"\n{'='*60}")
    print(f"  SCAN α̃ — {galaxy_name}")
    print(f"{'='*60}")
    print(f"  {'α̃':>8s}  {'Pente Γ':>10s}  {'R²':>8s}  {'v_inf':>8s}  {'Convergé':>8s}")
    print(f"  {'─'*50}")
    
    results = []
    for at in alpha_values:
        res = run_mcw3_iter2(galaxy_name, kappa_target=1.0, alpha_tilde=at,
                              eta=0.05, n_continuation=10, n_grid=300, verbose=False)
        if res:
            s = res['asymptotic_slope']
            r2 = res['asymptotic_r2']
            vi = res['v_inf_pred']
            conv = '✅' if res['converged'] else '⚠️'
            print(f"  {at:8.3f}  {s:10.3f}  {r2:8.4f}  {vi:8.1f}  {conv:>8s}")
            results.append(res)
    
    if results:
        best = min(results, key=lambda r: abs(r['asymptotic_slope'] + 1.0))
        print(f"\n  Meilleur α̃ = {best['alpha_tilde']:.3f} → pente = {best['asymptotic_slope']:.3f}")
    
    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='MCW-3 Itération 2')
    parser.add_argument('--galaxy', type=str, default='NGC2403')
    parser.add_argument('--kappa', type=float, default=1.0)
    parser.add_argument('--alpha', type=float, default=0.1)
    parser.add_argument('--eta', type=float, default=0.05)
    parser.add_argument('--n-cont', type=int, default=20)
    parser.add_argument('--n-grid', type=int, default=500)
    parser.add_argument('--scan-alpha', action='store_true')
    args = parser.parse_args()
    
    if args.scan_alpha:
        scan_alpha(args.galaxy)
    else:
        run_mcw3_iter2(args.galaxy, kappa_target=args.kappa,
                        alpha_tilde=args.alpha, eta=args.eta,
                        n_continuation=args.n_cont, n_grid=args.n_grid)
