#!/usr/bin/env python3
"""
TCM-1D v2 — Spherical Γ(r) model fit to SPARC dwarf galaxies
=============================================================
New model: Γ(r) = Γ₀ / √(1 + r²/r₀²)  (smooth transition core→1/r tail)
Gives flat rotation curves naturally in SPHERICAL symmetry.

Parameters: (r₀, v∞) — only 2 free parameters
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import cumulative_trapezoid
from scipy.stats import linregress
import matplotlib.pyplot as plt
from pathlib import Path
import csv
import json
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

G = 4.301e-9  # kpc (km/s)^2 / Msun

# ============================================================================
# NEW MODEL: Γ(r) = Γ₀ / √(1 + r²/r₀²)  —  SPHERICAL
# ============================================================================

def gamma_squared_profile(r, r0):
    """Γ²(r) profile (up to normalization Γ₀²)."""
    return 1.0 / (1.0 + (r/r0)**2)

def phase_density_dimensionless(r, r0):
    """
    Dimensionless density ∝ r² Γ²(r) (dΦ/dr)²
    Derived from smooth Γ(r) profile.
    """
    g2 = gamma_squared_profile(r, r0)
    # dΦ/dr ∝ 1/(r² Γ²(r)) → (dΦ/dr)² ∝ 1/(r⁴ Γ⁴)
    # ρ ∝ Γ² (dΦ/dr)² ∝ 1/(r⁴ Γ²) = (1 + r²/r₀²)/r⁴
    return (1.0 + (r/r0)**2) / r**4

def compute_velocity_profile(r, r0, vinf, n_int=500):
    """
    Compute v(r) for the spherical Γ(r) model.
    
    Uses numerical integration of the density profile.
    Returns v(r) [km/s].
    """
    # Build fine integration grid
    r_min = max(r[0]*0.01, 1e-4)
    r_max = max(r[-1]*2, r0*10)
    r_int = np.logspace(np.log10(r_min), np.log10(r_max), n_int)
    
    # Compute dimensionless density on integration grid
    rho_dim = phase_density_dimensionless(r_int, r0)
    
    # Integrate: M(<r) = 4π ∫₀ʳ ρ(r') r'² dr'
    integrand = rho_dim * r_int**2
    M_cum = cumulative_trapezoid(integrand, r_int, initial=0)
    
    # Normalize so that v(r→∞) = vinf
    # v²(r) = G M(<r) / r
    # Find normalization from large-r behavior
    r_large_idx = len(r_int) - 1
    v_sq_unnorm = G * M_cum / r_int
    norm = vinf**2 / v_sq_unnorm[r_large_idx] if v_sq_unnorm[r_large_idx] > 0 else 1.0
    
    # Interpolate to observed radii
    v_sq_interp = np.interp(r, r_int, v_sq_unnorm * norm)
    return np.sqrt(np.maximum(v_sq_interp, 0))

def fit_spherical_model(r_obs, v_obs, v_err, v_gas_sq, v_disk_sq, r0_guess=2.0, vinf_guess=80.0):
    """
    Fit: V_tot² = V_gas² + 0.5·V_disk² + V_halo²(r₀, v∞)
    
    The halo uses the spherical Γ(r) ∝ 1/r model.
    Υ_d is fixed at 0.5 (SPARC standard).
    """
    mask = (r_obs > 0) & (v_obs > 0) & np.isfinite(v_obs) & np.isfinite(v_err) & (v_err > 0)
    r = r_obs[mask]
    v = v_obs[mask]
    ve = v_err[mask]
    vg2 = v_gas_sq[mask]
    vd2 = v_disk_sq[mask]
    
    if len(r) < 5:
        return None
    
    upsilon_d = 0.5  # fixed
    
    def model(r, r0, vinf):
        r0 = np.abs(r0)
        vinf = np.abs(vinf)
        v_halo = compute_velocity_profile(r, r0, vinf)
        v_tot_sq = vg2 + upsilon_d * vd2 + v_halo**2
        return np.sqrt(np.maximum(v_tot_sq, 0.0))
    
    try:
        popt, pcov = curve_fit(
            model, r, v,
            p0=[r0_guess, vinf_guess],
            sigma=ve,
            absolute_sigma=True,
            maxfev=20000,
            bounds=([0.1, 5.0], [200, 500])
        )
        r0, vinf = np.abs(popt)
        perr = np.sqrt(np.diag(pcov))
        r0_err, vinf_err = np.abs(perr)
        
        v_model = model(r, r0, vinf)
        residuals = (v - v_model) / ve
        chi2 = np.sum(residuals**2)
        dof = len(r) - 2
        chi2_red = chi2 / dof if dof > 0 else np.inf
        
        return r0, vinf, r0_err, vinf_err, chi2_red
    except (RuntimeError, ValueError):
        return None


# ============================================================================
# DATA LOADING (same as before)
# ============================================================================

def load_sparc_galaxy(filepath):
    try:
        data = np.loadtxt(filepath, comments='#')
    except (IOError, ValueError):
        return None
    if data.shape[1] < 5:
        return None
    return {
        'r': data[:, 0], 'v_obs': data[:, 1], 'v_err': data[:, 2],
        'v_gas': data[:, 3], 'v_disk': data[:, 4],
        'v_bulge': data[:, 5] if data.shape[1] >= 6 else np.zeros_like(data[:, 0])
    }

def process_dwarfs(data_dir, vinf_max=80.0):
    data_path = Path(data_dir)
    dat_files = sorted(data_path.glob("*_rotmod.dat"))
    results = []
    all_galaxies = []
    
    print(f"Fitting {len(dat_files)} galaxies (dwarf filter: v∞ < {vinf_max} km/s)...")
    
    for fpath in dat_files:
        name = fpath.stem.replace("_rotmod", "")
        gal = load_sparc_galaxy(fpath)
        if gal is None:
            continue
        
        r, vobs, verr = gal['r'], gal['v_obs'], gal['v_err']
        vg2 = gal['v_gas']**2
        vd2 = gal['v_disk']**2
        
        r0_guess = np.median(r) * 0.5
        vinf_guess = float(np.median(vobs[np.argmax(r)//2:])) * 0.8
        
        fit = fit_spherical_model(r, vobs, verr, vg2, vd2, r0_guess, vinf_guess)
        if fit is None:
            continue
        
        r0, vinf, r0_err, vinf_err, chi2_red = fit
        
        if vinf > vinf_max:
            continue
        
        quality = "ok" if chi2_red < 3.0 and r0_err/r0 < 0.5 else "marginal" if chi2_red < 7.0 else "poor"
        
        all_galaxies.append({
            'name': name, 'r0': r0, 'r0_err': r0_err,
            'vinf': vinf, 'vinf_err': vinf_err,
            'chi2_red': chi2_red, 'quality': quality,
            'r': r, 'vobs': vobs, 'verr': verr
        })
        
        if quality == "ok":
            results.append({
                'name': name, 'r0': r0, 'r0_err': r0_err,
                'vinf': vinf, 'vinf_err': vinf_err, 'chi2_red': chi2_red
            })
        
        print(f"  {name:22s}: r₀ = {r0:6.2f} ± {r0_err:5.2f} kpc, "
              f"v∞ = {vinf:6.1f} ± {vinf_err:4.1f} km/s, "
              f"χ²_red = {chi2_red:.2f} [{quality}]")
    
    return results, all_galaxies


# ============================================================================
# ANALYSIS
# ============================================================================

def analyze(results, all_galaxies, output_dir):
    out = Path(output_dir)
    out.mkdir(exist_ok=True, parents=True)
    
    r0_arr = np.array([g['r0'] for g in results])
    vinf_arr = np.array([g['vinf'] for g in results])
    names = [g['name'] for g in results]
    
    print(f"\n{'='*60}")
    print(f"SPHERICAL Γ(r) MODEL — RESULTS")
    print(f"{'='*60}")
    print(f"Number of good dwarfs: {len(results)}")
    
    # Test: r₀ vs v∞ correlation (no specific prediction, just observing)
    log_r0 = np.log10(r0_arr)
    log_v = np.log10(vinf_arr)
    slope, intercept, r_val, p_val, std_err = linregress(log_v, log_r0)
    
    print(f"r₀ vs v∞ slope = {slope:.2f} ± {std_err:.2f} (R² = {r_val**2:.3f})")
    
    # Test: r₀·v∞ product (analogue to r_c·v∞ in old model)
    r0v = r0_arr * vinf_arr
    print(f"r₀·v∞ = {np.median(r0v):.0f} ± {np.std(r0v):.0f} kpc·km/s")
    
    # --- Plot 1: r₀ vs v∞ ---
    fig1, ax1 = plt.subplots(figsize=(10, 8))
    ax1.errorbar(log_v, log_r0, xerr=0.05, yerr=0.05, fmt='o', 
                 color='steelblue', alpha=0.7, capsize=3)
    v_range = np.linspace(log_v.min()-0.1, log_v.max()+0.1, 100)
    ax1.plot(v_range, slope*v_range + intercept, 'r-', linewidth=2, 
             label=f'Fit: slope={slope:.2f}±{std_err:.2f}')
    
    for i, name in enumerate(names):
        ax1.annotate(name, (log_v[i], log_r0[i]), fontsize=5, alpha=0.6,
                     xytext=(3, 3), textcoords='offset points')
    
    ax1.set_xlabel(r'$\log_{10}(v_\infty$ [km/s])', fontsize=14)
    ax1.set_ylabel(r'$\log_{10}(r_0$ [kpc])', fontsize=14)
    ax1.set_title('Spherical Γ(r) Model: $r_0$ vs $v_\\infty$', fontsize=16)
    ax1.legend(fontsize=12)
    ax1.grid(alpha=0.3)
    fig1.tight_layout()
    fig1.savefig(out / "spherical_r0_vs_vinf.png", dpi=150)
    
    # --- Plot 2: Sample fits ---
    n_show = min(6, len(results))
    fig2, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()
    
    # Sort by vinf for representative sample
    sorted_idx = np.argsort(vinf_arr)
    idx_show = [sorted_idx[0], sorted_idx[len(sorted_idx)//3], sorted_idx[2*len(sorted_idx)//3],
                sorted_idx[-1], sorted_idx[len(sorted_idx)//2], sorted_idx[len(sorted_idx)//4]]
    idx_show = idx_show[:n_show]
    
    for j, idx in enumerate(idx_show):
        ax = axes[j]
        g = all_galaxies[[g2['name'] for g2 in all_galaxies].index(results[idx]['name'])]
        r, vobs = g['r'], g['vobs']
        r_fine = np.logspace(np.log10(r[0]*0.8), np.log10(r[-1]*1.2), 100)
        
        # Recompute model
        v_halo = compute_velocity_profile(r_fine, results[idx]['r0'], results[idx]['vinf'])
        
        # Also compute old MCW profile for comparison
        from sparc_analysis import mcw_velocity_squared
        v_mcw = np.sqrt(mcw_velocity_squared(r_fine, results[idx]['r0'], results[idx]['vinf']))
        
        ax.plot(r_fine, v_halo, 'b-', linewidth=2, label='Sphérique Γ(r)')
        ax.plot(r_fine, v_mcw, 'r--', linewidth=1.5, alpha=0.7, label='MCW-1 (old)')
        ax.errorbar(r, vobs, yerr=g['verr'], fmt='o', color='gray', markersize=3, capsize=2)
        ax.axvline(results[idx]['r0'], color='blue', linestyle=':', alpha=0.5, label=f'$r_0$={results[idx]["r0"]:.1f}')
        
        ax.set_title(f"{results[idx]['name']}\n$r_0$={results[idx]['r0']:.1f} kpc, $v_\\infty$={results[idx]['vinf']:.0f} km/s", fontsize=10)
        ax.set_xlabel('R [kpc]')
        ax.set_ylabel('V [km/s]')
        ax.legend(fontsize=7)
        ax.grid(alpha=0.3)
    
    for j in range(n_show, 6):
        axes[j].set_visible(False)
    
    fig2.suptitle('Spherical Γ(r) Model — Sample Dwarf Galaxy Fits', fontsize=16)
    fig2.tight_layout()
    fig2.savefig(out / "spherical_sample_fits.png", dpi=150)
    
    # --- Export ---
    csv_path = out / "spherical_model_results.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Galaxy', 'r0_kpc', 'r0_err', 'vinf_kms', 'vinf_err', 'r0_vinf', 'chi2_red', 'quality'])
        for g in results:
            writer.writerow([g['name'], f"{g['r0']:.3f}", f"{g['r0_err']:.3f}",
                            f"{g['vinf']:.1f}", f"{g['vinf_err']:.1f}",
                            f"{g['r0']*g['vinf']:.1f}", f"{g['chi2_red']:.3f}", "ok"])
    
    summary = {
        "model": "TCM-1D v2 — Spherical Γ(r) ∝ 1/r",
        "n_dwarfs": len(results),
        "r0_vs_vinf_slope": float(slope),
        "slope_err": float(std_err),
        "r_squared": float(r_val**2),
        "median_r0_vinf": float(np.median(r0v)),
        "std_r0_vinf": float(np.std(r0v)),
    }
    
    with open(out / "spherical_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nResults saved to {out}/")
    return summary


# ============================================================================
# MAIN
# ============================================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(description="TCM-1D v2: Spherical Γ(r) model fit")
    parser.add_argument("--data-dir", default="./SPARC_data")
    parser.add_argument("--output-dir", default="./tcm1d_v2_results")
    parser.add_argument("--vinf-max", type=float, default=80.0)
    args = parser.parse_args()
    
    results, all_galaxies = process_dwarfs(args.data_dir, args.vinf_max)
    
    if len(results) < 3:
        print("Too few good fits. Try adjusting vinf-max or checking data.")
        return
    
    summary = analyze(results, all_galaxies, args.output_dir)
    
    slope = summary['r0_vs_vinf_slope']
    slope_err = summary['slope_err']
    
    print(f"\n{'='*60}")
    print("VERDICT — Spherical Γ(r) Model")
    print(f"{'='*60}")
    print(f"r₀ vs v∞ slope = {slope:.2f} ± {slope_err:.2f}")
    print(f"No strong prediction for this slope in current model.")
    print(f"The key test is whether v∞⁴ ∝ M_b emerges (future work).")


if __name__ == "__main__":
    main()
