#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTC ÉNERGIE NOIRE — Étape 3 : Classification des régimes + signature falsifiable
=================================================================================
1. Scan de μ = m_eff/H₀ → w₀, w_a (paramétrisation CPL : w(a) = w₀ + w_a(1−a))
2. Comparaison à la relation de « thawing » (Caldwell–Linder 2005) :
       w_a ≈ −1.58 (1 + w₀)
3. Contrainte BBN : Ω_φ à z ~ 10⁹ doit rester ≪ 0.1
4. Carte des régimes dans le plan (μ, Ṽ_min)

La relation w_a(w₀) est la signature FALSIFIABLE : si les données DESI/Euclid
tombent hors de la courbe TTC, le modèle est mort.

Auteur : DeepSeek V4 Pro (Co-auteur scientifique TTC)
Date   : 21 septembre 2026 — Série énergie noire, Étape 3/8
"""

import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path
import json

from ttc_dark_energy_solver import (
    solve_dark_energy, compute_wz, calibrate_phi_initial,
    hubble_sq, effective_potential, OMEGA_DE_TARGET
)

BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')

def fit_cpl(z, w):
    """
    Fit w(z) sur z ∈ [0,1] avec la paramétrisation CPL :
        w(a) = w₀ + w_a (1 − a),   a = 1/(1+z)
    Retourne (w₀, w_a, R²).
    """
    a = 1.0 / (1.0 + z)
    # w = w0 + wa*(1-a)  →  w = w0 + wa - wa*a  →  linéaire en a
    # w = b0 + b1 * a  avec b0 = w0 + wa, b1 = -wa
    mask = np.isfinite(w) & (z >= 0) & (z <= 1.0)
    aa = a[mask]
    ww = w[mask]
    if len(aa) < 5:
        return np.nan, np.nan, np.nan
    # moindres carrés simples
    A = np.vstack([np.ones_like(aa), aa]).T
    coeff, *_ = np.linalg.lstsq(A, ww, rcond=None)
    b0, b1 = coeff
    w0 = b0 + b1
    wa = -b1
    # R²
    w_fit = w0 + wa * (1 - aa)
    ss_res = np.sum((ww - w_fit)**2)
    ss_tot = np.sum((ww - ww.mean())**2)
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else np.nan
    return w0, wa, r2

def omega_phi_at_bbn(mu, Vmin, phi_i, z_bbn=1e9):
    """Ω_φ à l'époque de la nucléosynthèse (z ~ 10⁹)."""
    N_bbn = -np.log(1 + z_bbn)   # ~ -20.7
    sol = solve_dark_energy(mu, Vmin, phi_i, N_start=-30.0, N_end=N_bbn, n_eval=500)
    # interpoler à N_bbn
    z_sol, w_sol, h_sol, Om_sol = compute_wz(sol, mu, Vmin)
    N_sol = sol.t
    Om_bbn = np.interp(N_bbn, N_sol, Om_sol)
    return Om_bbn

# ── Scan de μ (cas Ṽ_min = 0 : champ pur, pas de constante cosmologique) ──
print('=' * 66)
print('TTC ÉNERGIE NOIRE — Étape 3 : scan des régimes et signature w_a(w₀)')
print('=' * 66)
print()

mu_values = np.concatenate([
    np.array([0.05, 0.08, 0.1, 0.12, 0.15, 0.18, 0.2, 0.25]),
    np.arange(0.3, 3.01, 0.2),
    np.array([3.5, 4.0, 5.0])
])

results = []
for mu in mu_values:
    try:
        phi_i, resid = calibrate_phi_initial(mu, 0.0)
        if phi_i is None:
            continue
        sol = solve_dark_energy(mu, 0.0, phi_i)
        z, w, h, Om = compute_wz(sol, mu, 0.0)
        w0, wa, r2 = fit_cpl(z, w)
        Om_bbn = omega_phi_at_bbn(mu, 0.0, phi_i)
        if np.isfinite(w0) and np.isfinite(wa):
            results.append({
                'mu': float(mu), 'w0': float(w0), 'wa': float(wa),
                'r2': float(r2), 'Omega_phi_bbn': float(Om_bbn),
                'phi_initial': float(phi_i)
            })
            print(f"  μ={mu:5.2f}  w₀={w0:+.4f}  w_a={wa:+.4f}  R²={r2:.4f}  Ω_φ(BBN)={Om_bbn:.2e}")
    except Exception as e:
        print(f"  μ={mu:5.2f}  échec : {e}")

print()

# ── Analyse ──
mu_arr = np.array([r['mu'] for r in results])
w0_arr = np.array([r['w0'] for r in results])
wa_arr = np.array([r['wa'] for r in results])
bbn_arr = np.array([r['Omega_phi_bbn'] for r in results])

# Relation Caldwell-Linder pour thawing : w_a ≈ −1.58 (1 + w₀)
cl_w0 = np.linspace(-1.0, -0.5, 50)
cl_wa = -1.58 * (1.0 + cl_w0)

# Contrainte BBN : Ω_φ(BBN) < 0.05 (à titre indicatif)
bbn_ok = bbn_arr < 0.05

# ── Figures ──
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

# Panneau 1 : w₀ en fonction de μ
ax = axes[0]
ax.axhline(-1.0, color='gray', ls='--', alpha=0.5)
ax.plot(mu_arr, w0_arr, 'o-', color='#4ade80', markersize=4)
ax.set_xlabel('μ = m_eff / H₀'); ax.set_ylabel('w₀')
ax.set_title('w₀ vs masse effective')
ax.grid(alpha=0.3)

# Panneau 2 : la signature falsifiable w_a vs w₀
ax = axes[1]
ax.plot(cl_w0, cl_wa, '--', color='gray', label='Caldwell–Linder (thawing générique)')
ax.plot(w0_arr, wa_arr, 'o-', color='#c084fc', markersize=5, label='TTC')
# ombrer la zone BBN ok
ax.set_xlabel('w₀'); ax.set_ylabel('w_a')
ax.set_title('Signature w_a(w₀) — falsifiable')
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# Panneau 3 : Ω_φ(BBN) — contrainte de nucléosynthèse
ax = axes[2]
ax.axhline(0.05, color='red', ls='--', alpha=0.7, label='limite BBN indicative')
ax.plot(mu_arr, bbn_arr, 'o-', color='#60a5fa', markersize=4)
ax.set_yscale('log')
ax.set_xlabel('μ = m_eff / H₀'); ax.set_ylabel('Ω_φ à z=10⁹')
ax.set_title('Contrainte BBN (énergie noire subdominante)')
ax.legend(fontsize=8); ax.grid(alpha=0.3, which='both')

plt.tight_layout()
out_png = BASE / 'ttc_dark_energy_step3.png'
plt.savefig(out_png, dpi=130)
plt.close()

# ── Résumé quantitatif ──
print('-' * 66)
print('Résumé')
print('-' * 66)
# Écart à Caldwell-Linder
cl_pred = -1.58 * (1.0 + w0_arr)
deviation = wa_arr - cl_pred
print(f"  Écart moyen à Caldwell–Linder : {np.mean(deviation):+.3f}")
print(f"  Plage de w₀ couverte         : {w0_arr.min():+.3f} → {w0_arr.max():+.3f}")
print(f"  Plage de w_a couverte        : {wa_arr.min():+.3f} → {wa_arr.max():+.3f}")
print(f"  Ω_φ(BBN) max                 : {bbn_arr.max():.2e}")
print(f"  μ pour w₀ ≈ −0.95            : {mu_arr[np.argmin(abs(w0_arr + 0.95))]:.2f}")
print()

# Frontière gelé/thawing : μ où w₀ s'écarte de −1 de plus de 1%
threshold = 0.01
thaw_idx = np.argmax(abs(w0_arr + 1.0) > threshold)
print(f"  Frontière gelé→thawing : μ ≈ {mu_arr[thaw_idx]:.2f} (w₀ = {w0_arr[thaw_idx]:+.4f})")
print()
print(f"  📁 Figure sauvegardée : {out_png.name}")

# Sauvegarde
out_json = BASE / 'ttc_dark_energy_step3_results.json'
with open(out_json, 'w') as f:
    json.dump({'results': results,
               'caldwell_linder': {'slope': -1.58},
               'bbn_limit': 0.05}, f, indent=2)
print(f"  📁 Résultats sauvegardés : {out_json.name}")
