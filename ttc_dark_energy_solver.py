#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTC ÉNERGIE NOIRE — Étape 2 : Solveur numérique du champ effectif
===================================================================
Système corrigé (Étape 1.5). Après intégration adiabatique de Γ, le secteur
énergie noire se réduit à un scalaire massif déplacé de son minimum :

    V(X) = V_min + (1/2) m_eff² X²,   m_eff² = β − 2λ²/α

Ce script résout, en fond FLRW plat, le système adimensionné en N = ln a :

    φ'' + (3 + h'/h) φ' + μ² φ = 0        (équation du champ)
    h²  = [Ω_m0 a⁻³ + Ω_r0 a⁻⁴ + ½μ²φ² + Ṽ_min] / (1 − ½φ'²)

avec :
    φ    = (8πG/3)^{1/2} X          (champ adimensionné)
    μ    = m_eff / H₀                (masse adimensionnée)
    Ṽ_min = (8πG/3 H₀²) V_min        (énergie du vide adimensionnée)
    '    = d/dN

Produit : w(z), H(z) pour les trois régimes (gelé / slow-roll / oscillant)
et vérifie la condition de validité de l'approximation adiabatique.

Auteur : DeepSeek V4 Pro (Co-auteur scientifique TTC)
Date   : 21 septembre 2026 — Série énergie noire, Étape 2/8
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from pathlib import Path
import json

BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')

# ── Constantes cosmologiques (Planck 2018, plate) ────────────────────────
OMEGA_M0 = 0.3111
OMEGA_R0 = 9.2e-5
OMEGA_DE_TARGET = 1.0 - OMEGA_M0 - OMEGA_R0   # ≈ 0.6888

# ── Système ODE (variable indépendante N = ln a) ──────────────────────────
def effective_potential(phi, mu, Vmin):
    """Ṽ(φ) = ½μ²φ² + Ṽ_min"""
    return 0.5 * mu**2 * phi**2 + Vmin

def hubble_sq(phi, dphi, N, mu, Vmin):
    """Contrainte de Friedmann : h² en fonction de (φ, φ', N)."""
    a_inv3 = np.exp(-3.0 * N)
    a_inv4 = np.exp(-4.0 * N)
    numer = OMEGA_M0 * a_inv3 + OMEGA_R0 * a_inv4 + effective_potential(phi, mu, Vmin)
    denom = 1.0 - 0.5 * dphi**2
    if denom <= 0:
        return np.nan
    return numer / denom

def rhs(N, y, mu, Vmin):
    """y = [φ, φ'=dφ/dN]. Retourne [φ', φ'']. h et h'/h calculés via la contrainte."""
    phi, dphi = y

    h2 = hubble_sq(phi, dphi, N, mu, Vmin)
    if not np.isfinite(h2) or h2 <= 0:
        # Repli sécurisé (ne devrait pas arriver dans les régimes viables)
        return [dphi, 0.0]

    h = np.sqrt(h2)
    V = effective_potential(phi, mu, Vmin)
    a_inv4 = np.exp(-4.0 * N)

    # w_eff total = p_tot/ρ_tot, en utilisant la contrainte ρ_tot = 3H₀²h²/(8πG)
    # p_tot (adim) = (1/3)Ω_r0 a⁻⁴ + ½h²φ'² − Ṽ(φ)
    p_tot = (1.0/3.0) * OMEGA_R0 * a_inv4 + 0.5 * h2 * dphi**2 - V
    w_eff = p_tot / h2

    # h'/h = d ln h / dN = −(3/2)(1 + w_eff)   (Raychaudhuri)
    hprime_over_h = -1.5 * (1.0 + w_eff)

    # Équation du champ : φ'' + (3 + h'/h) φ' + μ²φ/h² = 0
    d2phi = -(3.0 + hprime_over_h) * dphi - (mu**2 / h2) * phi

    return [dphi, d2phi]

# ── Résolution et diagnostics ──────────────────────────────────────────────
def solve_dark_energy(mu, Vmin, phi_initial, N_start=-15.0, N_end=0.0, n_eval=2000):
    """
    Intègre de N_start (ère radiative) à N_end (aujourd'hui).
    φ' initial = 0 (champ gelé par le frottement de Hubble).
    Retourne les diagnostics à N_end : Ω_φ, w_φ, et les courbes.
    """
    y0 = [phi_initial, 0.0]
    N_span = (N_start, N_end)
    sol = solve_ivp(rhs, N_span, y0, args=(mu, Vmin),
                    method='LSODA', rtol=1e-10, atol=1e-12,
                    t_eval=np.linspace(N_start, N_end, n_eval))
    return sol

def omega_phi_today(phi_initial, mu, Vmin):
    """Ω_φ aujourd'hui pour un φ_initial donné (pour le root-finding)."""
    sol = solve_dark_energy(mu, Vmin, phi_initial)
    phi = sol.y[0, -1]
    dphi = sol.y[1, -1]
    N = sol.t[-1]
    h2 = hubble_sq(phi, dphi, N, mu, Vmin)
    V = effective_potential(phi, mu, Vmin)
    rho_phi_dimless = 0.5 * h2 * dphi**2 + V   # = Ω_φ (car h²=ρ_tot/ρ_c0)
    return rho_phi_dimless / h2

def calibrate_phi_initial(mu, Vmin, phi_guess=1.0):
    """
    Trouve φ_initial tel que Ω_φ(aujourd'hui) = OMEGA_DE_TARGET.
    (le champ est gelé au départ, donc φ_initial ~ φ_aujourd'hui pour μ petit)
    """
    # Balayage large d'abord pour localiser la bonne racine
    guesses = np.logspace(-2, 2, 50)
    best = None
    best_diff = np.inf
    for g in guesses:
        try:
            om = omega_phi_today(g, mu, Vmin)
        except Exception:
            continue
        if np.isfinite(om):
            diff = abs(om - OMEGA_DE_TARGET)
            if diff < best_diff:
                best_diff = diff
                best = g
    if best is None:
        return None, None

    # Affinage par bissection autour de la meilleure estimation
    try:
        lo, hi = best * 0.1, best * 10.0
        f_lo = omega_phi_today(lo, mu, Vmin) - OMEGA_DE_TARGET
        f_hi = omega_phi_today(hi, mu, Vmin) - OMEGA_DE_TARGET
        if np.sign(f_lo) == np.sign(f_hi):
            return best, best_diff
        root = brentq(lambda p: omega_phi_today(p, mu, Vmin) - OMEGA_DE_TARGET,
                      lo, hi, xtol=1e-6)
        return root, abs(omega_phi_today(root, mu, Vmin) - OMEGA_DE_TARGET)
    except Exception:
        return best, best_diff

def compute_wz(sol, mu, Vmin):
    """Calcule w_φ(z) et h(z) depuis la solution."""
    N = sol.t
    z = np.exp(-N) - 1.0
    phi = sol.y[0]
    dphi = sol.y[1]

    w = np.zeros_like(N)
    h = np.zeros_like(N)
    Omega_phi = np.zeros_like(N)
    for i in range(len(N)):
        h2 = hubble_sq(phi[i], dphi[i], N[i], mu, Vmin)
        if not np.isfinite(h2) or h2 <= 0:
            w[i] = np.nan; h[i] = np.nan; Omega_phi[i] = np.nan
            continue
        V = effective_potential(phi[i], mu, Vmin)
        h[i] = np.sqrt(h2)
        # ρ_φ = ½φ̇² + V, p_φ = ½φ̇² − V ; φ̇ = H φ'
        rho_phi = 0.5 * h2 * dphi[i]**2 + V
        p_phi = 0.5 * h2 * dphi[i]**2 - V
        w[i] = p_phi / rho_phi if abs(rho_phi) > 1e-30 else np.nan
        Omega_phi[i] = rho_phi / h2
    return z, w, h, Omega_phi

# ── Vérification de l'approximation adiabatique ─────────────────────────────
def adiabatic_validity(alpha, lambda_, v_gamma, beta, H0, mu, z_range_max=2.0):
    """
    Vérifie si Γ peut être intégré adiabatiquement.
    Condition : m_Γ² ≫ H² ET m_Γ² ≫ m_T², sur toute l'histoire pertinente.
    m_Γ² = 2α v_Γ², m_T² = m_eff² = β − 2λ²/α.
    Retourne un dict de diagnostics.
    """
    m_Gamma2 = 2.0 * alpha * v_gamma**2
    m_T2 = beta - 2.0 * lambda_**2 / alpha
    # H² maximal dans l'intervalle [aujourd'hui, z_max]
    H2_max = H0**2 * (OMEGA_M0 * (1+z_range_max)**3 + OMEGA_R0 * (1+z_range_max)**4 + OMEGA_DE_TARGET)
    ratio_H = m_Gamma2 / H2_max
    ratio_T = m_Gamma2 / m_T2 if m_T2 > 0 else np.inf
    return {
        'm_Gamma2': m_Gamma2,
        'm_T2': m_T2,
        'm_T2_positive': m_T2 > 0,
        'm_Gamma2_over_H2_max': ratio_H,
        'm_Gamma2_over_m_T2': ratio_T,
        'valid_adiabatic': (ratio_H > 100) and (ratio_T > 100)
    }

# ── MAIN ────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    # Trois régimes (masses adimensionnées μ = m_eff/H₀)
    regimes = [
        {'name': 'gelé (μ=0.3)',       'mu': 0.3,  'Vmin': 0.68, 'label': 'frozen'},
        {'name': 'slow-roll (μ=1.5)',  'mu': 1.5,  'Vmin': 0.0,  'label': 'thawing'},
        {'name': 'oscillant (μ=30)',   'mu': 30.0, 'Vmin': 0.60, 'label': 'oscillating'},
    ]

    results = []
    print('=' * 66)
    print('TTC ÉNERGIE NOIRE — Étape 2 : solveur du champ effectif')
    print('=' * 66)
    print(f'  Ω_m0 = {OMEGA_M0}, Ω_r0 = {OMEGA_R0:.2e}, cible Ω_DE = {OMEGA_DE_TARGET:.4f}')
    print()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4.5))

    for i, reg in enumerate(regimes):
        mu, Vmin = reg['mu'], reg['Vmin']
        phi_i, residual = calibrate_phi_initial(mu, Vmin)
        sol = solve_dark_energy(mu, Vmin, phi_i)
        z, w, h, Om = compute_wz(sol, mu, Vmin)

        # Masquer z < 0 (futur) pour la présentation
        mask = z >= 0
        w_today = w[-1]
        Om_today = Om[-1]

        print(f"  Régime {reg['name']}:")
        print(f"    φ_initial (calibré) = {phi_i:.4f}  (résidu Ω = {residual:.2e})")
        print(f"    Ω_φ aujourd'hui     = {Om_today:.4f}  (cible {OMEGA_DE_TARGET:.4f})")
        print(f"    w_φ aujourd'hui     = {w_today:.4f}")
        print(f"    w_φ à z=1           = {np.interp(1.0, z[mask][::-1], w[mask][::-1]):.4f}")
        print()

        results.append({
            'regime': reg['name'], 'mu': mu, 'Vmin': Vmin,
            'phi_initial': float(phi_i), 'Omega_phi_today': float(Om_today),
            'w_today': float(w_today), 'residual': float(residual)
        })

        ax1.plot(z[mask], w[mask], label=reg['name'], linewidth=2)
        ax2.plot(z[mask], h[mask], label=reg['name'], linewidth=2)
        ax3.plot(z[mask], Om[mask], label=reg['name'], linewidth=2)

    ax1.axhline(-1.0, color='gray', linestyle='--', alpha=0.6)
    ax1.set_xlabel('redshift z'); ax1.set_ylabel('w_φ(z)'); ax1.set_title('Équation d\'état')
    ax2.set_xlabel('redshift z'); ax2.set_ylabel('h(z) = H/H₀'); ax2.set_title('Taux d\'expansion')
    ax3.set_xlabel('redshift z'); ax3.set_ylabel('Ω_φ(z)'); ax3.set_title('Densité d\'énergie noire')
    for a in (ax1, ax2, ax3):
        a.legend(fontsize=8); a.grid(alpha=0.3)

    plt.tight_layout()
    out_png = BASE / 'ttc_dark_energy_step2.png'
    plt.savefig(out_png, dpi=130)
    plt.close()

    # ── Vérification adiabatique ──
    print('-' * 66)
    print('Vérification de l\'approximation adiabatique (intégration de Γ)')
    print('-' * 66)
    # H₀ en eV : 1.44e-33 eV ; on travaille en unités naturelles ħ=c=1
    H0_eV = 1.44e-33
    # Cas test : α grand (Γ massif), λ tel que m_eff ~ H₀ (μ=1)
    # m_eff² = β − 2λ²/α = H₀²  → β = H₀² + 2λ²/α
    alpha_test = 1.0
    lambda_test = 1e-4 * H0_eV   # petit couplage
    v_gamma_test = 1e28          # ~ M_Pl en eV
    beta_test = H0_eV**2 + 2.0 * lambda_test**2 / alpha_test
    diag = adiabatic_validity(alpha_test, lambda_test, v_gamma_test, beta_test, H0_eV, mu=1.0)
    print(f"  α={alpha_test}, λ={lambda_test:.2e} eV, v_Γ={v_gamma_test:.1e} eV, β={beta_test:.2e} eV²")
    print(f"  m_Γ² = {diag['m_Gamma2']:.2e} eV², m_T² = {diag['m_T2']:.2e} eV²")
    print(f"  m_Γ²/H²_max = {diag['m_Gamma2_over_H2_max']:.2e} (doit être ≫ 1)")
    print(f"  m_Γ²/m_T²   = {diag['m_Gamma2_over_m_T2']:.2e} (doit être ≫ 1)")
    print(f"  m_T² > 0    = {diag['m_T2_positive']}")
    print(f"  → Adiabatique valide : {'OUI' if diag['valid_adiabatic'] else 'NON'}")
    print()
    print(f"  📁 Figure sauvegardée : {out_png.name}")

    # Sauvegarde JSON
    out_json = BASE / 'ttc_dark_energy_step2_results.json'
    with open(out_json, 'w') as f:
        json.dump({'regimes': results, 'adiabatic': diag}, f, indent=2, default=str)
    print(f"  📁 Résultats sauvegardés : {out_json.name}")
