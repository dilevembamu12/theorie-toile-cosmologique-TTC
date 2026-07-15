#!/usr/bin/env python3
"""TTC Tully-Fisher: Extract a_TTC from one galaxy, predict all others."""
import csv, numpy as np
from pathlib import Path
from scipy.stats import linregress

BASE = Path(r'e:\DILEVE\DILEVE\BUSINESS\PROJECTS\RECHERCHES\TOOILE_COSMOLOGIQUE\DEEPSEEK')
SPARC = BASE / 'SPARC_data'
G_kpc = 4.301e-9  # [kpc (km/s)^2 / Msun]

# Load all galaxies
data = []
for fpath in sorted(SPARC.glob('*_rotmod.dat')):
    name = fpath.stem.replace('_rotmod', '')
    radii, vobs, vgas, vdisk, vbul = [], [], [], [], []
    with open(fpath) as f:
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            p = line.split()
            if len(p) >= 6:
                try:
                    radii.append(float(p[0])); vobs.append(float(p[1]))
                    vgas.append(float(p[3])); vdisk.append(float(p[4]))
                    vbul.append(float(p[5]))
                except: pass
    if len(radii) < 5: continue
    radii = np.array(radii); vobs = np.array(vobs)
    vgas = np.array(vgas); vdisk = np.array(vdisk); vbul = np.array(vbul)

    vb2 = np.abs(vgas)*vgas + np.abs(vdisk)*vdisk + np.abs(vbul)*vbul
    M_b = vb2[-1] * radii[-1] / G_kpc
    if M_b <= 1e8 or M_b > 1e14: continue
    
    n2 = len(vobs) // 2
    v_flat = np.median(vobs[n2:])
    data.append({'name': name, 'M_b': M_b, 'v_flat': v_flat, 'R_max': radii[-1]})

print(f'Loaded {len(data)} galaxies')
M_all = np.array([d['M_b'] for d in data])
V_all = np.array([d['v_flat'] for d in data])

# ====== METHOD 1: Reference galaxy ======
idx_ref = np.argmin(np.abs(np.log10(M_all) - np.median(np.log10(M_all))))
ref = data[idx_ref]
print(f'\nReference: {ref["name"]}  M_b={ref["M_b"]:.2e} Msun  v={ref["v_flat"]:.0f} km/s')

a_TTC = ref['v_flat']**4 / (G_kpc * ref['M_b'])
a_si = a_TTC * 1e6 / 3.086e19
print(f'a_TTC = {a_TTC:.2e} (km/s)^2/kpc = {a_si:.2e} m/s^2')
print(f'a_MOND = 1.2e-10 m/s^2  ->  a_TTC/a_MOND = {a_si/1.2e-10:.2f}')

# Predict all
V_pred1 = (G_kpc * M_all * a_TTC)**0.25
res1 = np.log10(V_all) - np.log10(V_pred1)
s1, _, r1, _, _ = linregress(np.log10(V_pred1), np.log10(V_all))
print(f'\n=== REFERENCE CALIBRATION ===')
print(f'scatter = {np.std(res1):.3f} dex')
print(f'R^2 = {r1**2:.4f}')
print(f'slope(obs vs pred) = {s1:.3f}')

# ====== METHOD 2: Best-fit a_TTC (median) ======
log_v4_over_GM = 4*np.log10(V_all) - np.log10(G_kpc) - np.log10(M_all)
a_best = 10**np.median(log_v4_over_GM)
a_best_si = a_best * 1e6 / 3.086e19
print(f'\n=== BEST-FIT a_TTC (median) ===')
print(f'a_TTC = {a_best:.2e} (km/s)^2/kpc = {a_best_si:.2e} m/s^2')
print(f'Ratio best/ref = {a_best/a_TTC:.3f}')

V_pred2 = (G_kpc * M_all * a_best)**0.25
res2 = np.log10(V_all) - np.log10(V_pred2)
sigma2 = np.std(res2)
s2, _, r2, _, _ = linregress(np.log10(V_pred2), np.log10(V_all))
print(f'scatter = {sigma2:.3f} dex')
print(f'R^2 = {r2**2:.4f}')
print(f'slope(obs vs pred) = {s2:.3f}')

# ====== KEY TEST: Is TF scatter reduced vs standard? ======
log_v4_over_Mb = 4*np.log10(V_all) - np.log10(M_all)
sigma_direct = np.std(log_v4_over_Mb)
print(f'\n=== SCATTER COMPARISON ===')
print(f'Direct v^4/M_b scatter: {sigma_direct:.3f} dex')
print(f'TTC predicted scatter:  {sigma2:.3f} dex')
print(f'Improvement: {sigma_direct/sigma2:.1f}x')

# ====== Cross-validation ======
print(f'\n=== CROSS-VALIDATION (leave-one-out) ===')
preds, obss = [], []
for i in range(len(data)):
    train = [d for j, d in enumerate(data) if j != i]
    M_train = np.array([d['M_b'] for d in train])
    V_train = np.array([d['v_flat'] for d in train])
    a_cv = 10**np.median(4*np.log10(V_train) - np.log10(G_kpc) - np.log10(M_train))
    preds.append((G_kpc * M_all[i] * a_cv)**0.25)
    obss.append(V_all[i])
preds = np.array(preds); obss = np.array(obss)
cv_res = np.log10(obss) - np.log10(preds)
print(f'CV scatter: {np.std(cv_res):.3f} dex')
print(f'CV R^2: {linregress(np.log10(preds), np.log10(obss))[2]**2:.4f}')
