#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTC Tully-Fisher — Refined Test v2
===================================
- Proper M_b calculation (integrated, fixed outer radius)
- Direct TF test: v∞⁴ vs M_b
- Comparison: observed v_flat vs MCW-1 v_inf
- Scatter analysis

Author: Dileve MBAMU (dileve.com)
Co-author: DeepSeek V4 Pro
Date: 2026-07-15
"""

import numpy as np
from scipy.stats import linregress, spearmanr
from pathlib import Path
import csv, warnings
warnings.filterwarnings("ignore")

G_kpc = 4.301e-9  # [kpc (km/s)^2 / Msun]
BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')
SPARC_DIR = BASE / 'SPARC_data'
RESULTS_FILE = BASE / 'mcw1_sparc_results' / 'mcw1_sparc_results.csv'

# ============================================================================
# Load MCW-1 results
# ============================================================================
mcw1 = {}
with open(RESULTS_FILE, 'r') as f:
    for row in csv.DictReader(f):
        mcw1[row['Galaxy']] = {
            'r_c': float(row['r_c_kpc']),
            'v_inf': float(row['v_inf_kms']),
            'm_gamma': float(row['m_gamma_eV'])
        }

# ============================================================================
# Load SPARC data with PROPER M_b calculation
# ============================================================================
galaxies = []
for name, res in mcw1.items():
    fpath = SPARC_DIR / f"{name}_rotmod.dat"
    if not fpath.exists(): continue
    
    radii, vobs, vgas, vdisk, vbul = [], [], [], [], []
    with open(fpath) as f:
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            p = line.split()
            if len(p) >= 6:
                try:
                    radii.append(float(p[0]))
                    vobs.append(float(p[1]))
                    vgas.append(float(p[3]))
                    vdisk.append(float(p[4]))
                    vbul.append(float(p[5]))
                except: pass
    
    if len(radii) < 5: continue
    radii = np.array(radii)
    vobs = np.array(vobs)
    vgas = np.array(vgas)
    vdisk = np.array(vdisk)
    vbul = np.array(vbul)
    
    # Baryonic velocity: V_b² = |Vgas|·Vgas + Υ_d·|Vdisk|·Vdisk + Υ_b·|Vbul|·Vbul
    # Standard SPARC: Υ_d = 0.5, Υ_b = 0.7 (at 3.6μm)
    # But we want a MODEL-INDEPENDENT estimate: use Vgas, Vdisk, Vbul as published
    # (these already include the SPARC M/L ratios)
    v_baryon_sq = np.abs(vgas)*vgas + np.abs(vdisk)*vdisk + np.abs(vbul)*vbul
    v_baryon = np.sqrt(np.maximum(v_baryon_sq, 0))
    
    # Method 1: M_b enclosed at last measured radius
    R_max = radii[-1]
    M_b_last = v_baryon_sq[-1] * R_max / G_kpc if v_baryon_sq[-1] > 0 else 0
    
    # Method 2: Estimate v_flat from observation (median of outer 50% of points)
    n_half = len(vobs) // 2
    v_flat_obs = np.median(vobs[n_half:])
    
    # Method 3: Integrate to get total M_b (cumulative)
    # M_b(<R) at each radius
    M_b_cum = np.cumsum(v_baryon_sq * np.gradient(radii) / G_kpc)
    M_b_total = M_b_cum[-1] if len(M_b_cum) > 0 else 0
    
    if M_b_last <= 0: continue
    
    galaxies.append({
        'name': name,
        'r_c': res['r_c'],
        'v_inf_mcw1': res['v_inf'],
        'v_flat_obs': v_flat_obs,
        'm_gamma': res['m_gamma'],
        'M_b': M_b_last,
        'M_b_total': M_b_total,
        'R_max': R_max,
        'n_points': len(radii),
        'v_baryon_max': np.max(v_baryon)
    })

print(f"Loaded {len(galaxies)} galaxies with M_b > 0")
print()

# Arrays
v_mcw1 = np.array([g['v_inf_mcw1'] for g in galaxies])
v_flat = np.array([g['v_flat_obs'] for g in galaxies])
M_b    = np.array([g['M_b'] for g in galaxies])
M_btot = np.array([g['M_b_total'] for g in galaxies])
r_c    = np.array([g['r_c'] for g in galaxies])
R_max  = np.array([g['R_max'] for g in galaxies])

print(f"Mass range: {M_b.min():.1e} — {M_b.max():.1e} Msun")
print(f"v_flat range: {v_flat.min():.0f} — {v_flat.max():.0f} km/s")
print(f"R_max range: {R_max.min():.1f} — {R_max.max():.1f} kpc")
print()

# ============================================================================
# TEST: Direct Tully-Fisher — v_flat⁴ vs M_b
# ============================================================================
print("="*60)
print("DIRECT TULLY-FISHER: v_flat⁴ vs M_b")
print("="*60)

# Remove extreme outliers (beyond 3σ in log space)
logM = np.log10(M_b)
logV = np.log10(v_flat)
logV4_over_M = 4*logV - logM

median_ratio = np.median(logV4_over_M)
sigma_ratio = np.std(logV4_over_M)
mask_ok = np.abs(logV4_over_M - median_ratio) < 3*sigma_ratio

logM_ok = logM[mask_ok]
logV_ok = logV[mask_ok]

slope, intercept, r_val, p_val, std_err = linregress(logM_ok, logV_ok)
rho, p_rho = spearmanr(logM_ok, logV_ok)

# Expected from v⁴ ∝ M_b: slope = 0.25
expected_slope = 0.25
sigma_tf = abs(slope - expected_slope) / std_err

print(f"\n  log v_flat = a + b · log M_b")
print(f"  Slope b = {slope:.4f} ± {std_err:.4f}")
print(f"  Expected (v⁴∝M_b): b = {expected_slope:.4f}")
print(f"  Tension: {sigma_tf:.1f}σ")
print(f"  R² = {r_val**2:.4f}, Spearman ρ = {rho:.3f}")
print(f"  N = {np.sum(mask_ok)} (outliers removed: {np.sum(~mask_ok)})")

# Scatter in v⁴/M_b
v4_over_Mb = v_flat[mask_ok]**4 / M_b[mask_ok]
log_scatter = np.std(np.log10(v4_over_Mb))
print(f"\n  Scatter in v⁴/M_b: {log_scatter:.3f} dex")
print(f"  (Typical baryonic TF scatter: 0.1-0.15 dex)")

# ============================================================================
# TEST: v_flat⁴ vs M_b using MCW-1 v_inf
# ============================================================================
print("\n" + "="*60)
print("TULLY-FISHER with MCW-1 v_inf")
print("="*60)

logV_mcw1 = np.log10(v_mcw1[mask_ok])
logM_mcw1 = logM_ok
slope_m, intercept_m, r_m, p_m, std_m = linregress(logM_mcw1, logV_mcw1)
sigma_tf_m = abs(slope_m - expected_slope) / std_m

print(f"\n  Slope b = {slope_m:.4f} ± {std_m:.4f}")
print(f"  Tension: {sigma_tf_m:.1f}σ")
print(f"  R² = {r_m**2:.4f}")

# ============================================================================
# TEST: r_c correlation with R_max (is r_c just tracking data extent?)
# ============================================================================
print("\n" + "="*60)
print("r_c vs R_max — Is r_c tracking data extent?")
print("="*60)

slope_rm, _, r_rm, _, _ = linregress(np.log10(R_max[mask_ok]), np.log10(r_c[mask_ok]))
print(f"\n  log r_c vs log R_max: slope = {slope_rm:.3f}, R² = {r_rm**2:.3f}")

# ============================================================================
# TEST: TF binned by v_flat
# ============================================================================
print("\n" + "="*60)
print("TULLY-FISHER — Binned analysis")
print("="*60)

# Bin by v_flat
bins = np.percentile(v_flat[mask_ok], [0, 25, 50, 75, 100])
for i in range(len(bins)-1):
    mask_bin = mask_ok & (v_flat >= bins[i]) & (v_flat < bins[i+1])
    if np.sum(mask_bin) < 5: continue
    logM_bin = np.log10(M_b[mask_bin])
    logV_bin = np.log10(v_flat[mask_bin])
    s, _, r, _, _ = linregress(logM_bin, logV_bin)
    print(f"  Bin {i+1} (v=[{bins[i]:.0f},{bins[i+1]:.0f}] km/s, N={np.sum(mask_bin)}): slope={s:.3f}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)

print(f"""
  Direct Tully-Fisher (observed v_flat):
    Slope: {slope:.4f} ± {std_err:.4f}  (expected 0.250 for v⁴∝M_b)
    Tension: {sigma_tf:.1f}σ  → {'✅ COMPATIBLE' if sigma_tf < 3 else '🟡 TENSION' if sigma_tf < 5 else '🔴 REFUTED'}
    Scatter: {log_scatter:.3f} dex

  MCW-1 Tully-Fisher (fitted v_inf):
    Slope: {slope_m:.4f} ± {std_m:.4f}
    Tension: {sigma_tf_m:.1f}σ  → {'✅ COMPATIBLE' if sigma_tf_m < 3 else '🟡 TENSION' if sigma_tf_m < 5 else '🔴 REFUTED'}

  Mass range: {M_b.min():.1e} — {M_b.max():.1e} Msun
  N = {np.sum(mask_ok)} galaxies
""")

# ============================================================================
# Quick plot
# ============================================================================
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Direct TF
ax = axes[0]
x = logM_ok
y = logV_ok
ax.scatter(x, y, c=v_flat[mask_ok], cmap='plasma', alpha=0.7, s=25)
xp = np.linspace(x.min(), x.max(), 100)
ax.plot(xp, intercept + slope*xp, 'k-', lw=2, label=f'Obs: b={slope:.3f}±{std_err:.3f}')
ax.plot(xp, intercept + 0.25*(xp-xp[0]) + slope*xp[0], 'g--', lw=2, label='TTC: b=0.250 (v⁴∝M_b)')
ax.set_xlabel('log M_b [Msun]')
ax.set_ylabel('log v_flat [km/s]')
ax.set_title(f'Direct Tully-Fisher ({np.sum(mask_ok)} galaxies)')
ax.legend(fontsize=9)

# Plot 2: v⁴/M_b vs M_b (should be flat)
ax = axes[1]
ax.scatter(logM_ok, np.log10(v_flat[mask_ok]**4 / M_b[mask_ok]), 
           c=v_flat[mask_ok], cmap='plasma', alpha=0.7, s=25)
ax.axhline(np.median(np.log10(v_flat[mask_ok]**4 / M_b[mask_ok])), 
           color='r', ls='--', lw=1, label=f'Median')
ax.fill_between([logM_ok.min(), logM_ok.max()], 
                [np.median(np.log10(v_flat[mask_ok]**4 / M_b[mask_ok])) - log_scatter]*2,
                [np.median(np.log10(v_flat[mask_ok]**4 / M_b[mask_ok])) + log_scatter]*2,
                alpha=0.2, color='gray', label=f'±{log_scatter:.2f} dex')
ax.set_xlabel('log M_b [Msun]')
ax.set_ylabel('log(v⁴/M_b)')
ax.set_title(f'v⁴/M_b constancy (scatter={log_scatter:.2f} dex)')
ax.legend(fontsize=9)

plt.tight_layout()
out = BASE / 'TTC-tully-fisher-v2.png'
plt.savefig(out, dpi=150)
print(f"\nPlot saved: {out}")
