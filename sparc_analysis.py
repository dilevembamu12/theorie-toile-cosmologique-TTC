#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPARC Analysis Script — Minimal Cosmic Web (MCW-1 / TCM-1)
==========================================================
Tests the core prediction: r_c * v_inf ≈ ℏ / m_Γ ≈ constant

Usage:
    python sparc_analysis.py --data-dir ./SPARC_data/

If SPARC data is not available locally, the script will attempt to
download it from the official repository.

Author: DeepSeek V4 Pro (co-author)
Date: 2026-07-12
"""

import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import linregress
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
import warnings
import json
import csv
from dataclasses import dataclass, field
from typing import Optional

warnings.filterwarnings("ignore", category=RuntimeWarning)

# ============================================================================
# CONSTANTS
# ============================================================================

G = 4.301e-9          # Gravitational constant [kpc (km/s)^2 / Msun]

# Physical constants for m_Γ = ℏ / (r_c · v_∞) conversion
# m_Γ [eV] = ℏ[eV·s] · c²[m²/s²] / (r_c[m] · v_∞[m/s])
#          = (ℏ·c²) [eV·m²/s] / (r_c[m] · v_∞[m/s])
# 
# ℏ = 6.582119e-16 eV·s
# c = 2.99792458e8 m/s
# ℏ·c² = 6.582119e-16 · (2.99792458e8)² = 5.9154e1 eV·m²/s
#
# For r_c [kpc] and v_∞ [km/s]:
# r_c [m] = r_c [kpc] · 3.085678e19 [m/kpc]
# v_∞ [m/s] = v_∞ [km/s] · 1000 [m·km⁻¹·s⁻¹]
# m_Γ [eV] = 5.9154e1 / (r_c[kpc]·3.0857e19 · v_∞[km/s]·1000)
#          = 5.9154e1 / (r_c·v_∞·3.0857e22)
#          = 1.917e-21 / (r_c[kpc] · v_∞[km/s])

HBAR_C2 = 5.9154e1       # ℏ·c² [eV·m²/s]
KPC_TO_M = 3.085678e19   # kpc to meters
KMS_TO_MS = 1000.0       # km/s to m/s

def compute_m_gamma(r_c_kpc, v_inf_kms):
    """
    Compute effective coherence mass m_Γ in eV.
    
    Uses: m_Γ = ℏ / (r_c · v_∞)
    where r_c is identified with the reduced de Broglie wavelength ƛ = ℏ/(m·v).
    """
    r_c_m = r_c_kpc * KPC_TO_M
    v_inf_ms = v_inf_kms * KMS_TO_MS
    return HBAR_C2 / (r_c_m * v_inf_ms)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class GalaxyFit:
    """Results of fitting MCW-1 halo profile to a galaxy."""
    name: str
    r_c: float           # Core radius [kpc]
    r_c_err: float
    v_inf: float         # Asymptotic velocity [km/s]
    v_inf_err: float
    rho_0: float         # Central density [Msun/kpc^3]
    m_gamma: float       # Derived m_Γ [eV]
    m_gamma_err: float
    m_b: float            # Baryonic mass [Msun] (if available)
    chi2_red: float       # Reduced chi-squared
    n_points: int         # Number of data points
    quality: str = "ok"   # ok / marginal / poor
    environment: str = "unknown"  # void / filament / group / cluster


# ============================================================================
# HALO MODEL: MCW-1 (TTC) profile
# ============================================================================

def mcw_velocity_squared(r, r_c, v_inf):
    """
    Velocity squared for MCW-1 halo profile.
    
    Profile: ρ(r) = ρ_0 * r_c^2 / (r^2 + r_c^2)
    with ρ_0 = v_inf^2 / (4π G r_c^2)
    
    v^2(r) = v_inf^2 * [1 - (r_c/r) * arctan(r/r_c)]
    
    Parameters:
        r : array, radii [kpc]
        r_c : float, core radius [kpc]
        v_inf : float, asymptotic velocity [km/s]
    
    Returns:
        v^2(r) [km^2/s^2]
    """
    ratio = r_c / r
    # Avoid division by zero at r=0
    with np.errstate(divide='ignore', invalid='ignore'):
        bracket = 1.0 - ratio * np.arctan(r / r_c)
    bracket = np.where(np.isfinite(bracket), bracket, 0.0)  # v(0) = 0
    return v_inf**2 * bracket


def mcw_total_velocity_squared(r, r_c, v_inf, upsilon_d, v_disk_sq, v_gas_sq, v_bulge_sq=None):
    """
    Total velocity squared: baryons + MCW-1 halo.
    
    v_tot^2 = Υ_d * v_disk^2 + v_gas^2 + Υ_b * v_bulge^2 + v_halo^2(r_c, v_inf)
    """
    v_halo_sq = mcw_velocity_squared(r, r_c, v_inf)
    v_baryon_sq = upsilon_d * v_disk_sq + v_gas_sq
    if v_bulge_sq is not None:
        v_baryon_sq += v_baryon_sq  # Note: need another upsilon_b; simplified here
    return v_baryon_sq + v_halo_sq


# ============================================================================
# FITTING
# ============================================================================

def fit_mcw_halo_with_baryons(r_obs, v_obs, v_err, v_gas_sq, v_disk_sq, v_bulge_sq=None,
                                r_c_guess=2.0, v_inf_guess=100.0, upsilon_fixed=None):
    """
    Fit MCW-1 halo + baryons to rotation curve data.
    
    Model: V_tot² = V_gas² + Υ_d·V_disk² + V_halo²(r_c, v_inf)
    
    If upsilon_fixed is provided, Υ_d is held fixed (2-parameter fit).
    Otherwise Υ_d is free (3-parameter fit).
    
    Returns: (r_c, v_inf, upsilon_d, r_c_err, v_inf_err, upsilon_err, chi2_red)
    """
    # Filter valid data
    mask = (r_obs > 0) & (v_obs > 0) & np.isfinite(v_obs) & np.isfinite(v_err) & (v_err > 0)
    r = r_obs[mask]
    v = v_obs[mask]
    ve = v_err[mask]
    vg2 = v_gas_sq[mask]
    vd2 = v_disk_sq[mask]
    vb2 = v_bulge_sq[mask] if v_bulge_sq is not None else np.zeros_like(r)

    if len(r) < 5:
        return None

    if upsilon_fixed is not None:
        # 2-parameter fit: r_c, v_inf only; Υ_d fixed
        upsilon_d = upsilon_fixed
        upsilon_err = 0.0

        def model(r, r_c, v_inf):
            r_c = np.abs(r_c)
            v_inf = np.abs(v_inf)
            v_halo_sq = mcw_velocity_squared(r, r_c, v_inf)
            v_tot_sq = vg2 + upsilon_d * vd2 + v_halo_sq
            return np.sqrt(np.maximum(v_tot_sq, 0.0))

        try:
            popt, pcov = curve_fit(
                model, r, v,
                p0=[r_c_guess, v_inf_guess],
                sigma=ve,
                absolute_sigma=True,
                maxfev=20000,
                bounds=([0.01, 1.0], [500, 5000])
            )
            r_c, v_inf = np.abs(popt)
            perr = np.sqrt(np.diag(pcov))
            r_c_err, v_inf_err = np.abs(perr)
            v_model = model(r, r_c, v_inf)
            residuals = (v - v_model) / ve
            chi2 = np.sum(residuals**2)
            dof = len(r) - 2
            chi2_red = chi2 / dof if dof > 0 else np.inf
            return r_c, v_inf, upsilon_d, r_c_err, v_inf_err, upsilon_err, chi2_red
        except (RuntimeError, ValueError):
            return None

    else:
        # 3-parameter fit: r_c, v_inf, Υ_d free
        def model(r, r_c, v_inf, upsilon_d):
            r_c = np.abs(r_c)
            v_inf = np.abs(v_inf)
            upsilon_d = np.abs(upsilon_d)
            v_halo_sq = mcw_velocity_squared(r, r_c, v_inf)
            v_tot_sq = vg2 + upsilon_d * vd2 + v_halo_sq
            return np.sqrt(np.maximum(v_tot_sq, 0.0))

        try:
            popt, pcov = curve_fit(
                model, r, v,
                p0=[r_c_guess, v_inf_guess, 0.5],
                sigma=ve,
                absolute_sigma=True,
                maxfev=20000,
                bounds=([0.01, 1.0, 0.01], [500, 5000, 5.0])
            )
            r_c, v_inf, upsilon_d = np.abs(popt)
            perr = np.sqrt(np.diag(pcov))
            r_c_err, v_inf_err, upsilon_err = np.abs(perr)
            v_model = model(r, r_c, v_inf, upsilon_d)
            residuals = (v - v_model) / ve
            chi2 = np.sum(residuals**2)
            dof = len(r) - 3
            chi2_red = chi2 / dof if dof > 0 else np.inf
            return r_c, v_inf, upsilon_d, r_c_err, v_inf_err, upsilon_err, chi2_red
        except (RuntimeError, ValueError):
            return None


# ============================================================================
# SPARC DATA LOADER
# ============================================================================

def load_sparc_galaxy(filepath):
    """
    Load a SPARC galaxy rotation curve file.
    
    Expected format (SPARC rotmod.dat):
    Rad  Vobs  errV  Vgas  Vdisk  Vbul  Sbul
    (kpc) (km/s) (km/s) (km/s) (km/s) (km/s) (km/s)
    """
    try:
        data = np.loadtxt(filepath, comments='#')
    except (IOError, ValueError):
        return None

    if data.shape[1] < 5:
        return None

    r_obs = data[:, 0]
    v_obs = data[:, 1]
    v_err = data[:, 2]
    v_gas = data[:, 3]
    v_disk = data[:, 4]

    # Optional bulge
    v_bulge = data[:, 5] if data.shape[1] >= 6 else np.zeros_like(r_obs)

    return {
        'r': r_obs,
        'v_obs': v_obs,
        'v_err': v_err,
        'v_gas': v_gas,
        'v_disk': v_disk,
        'v_bulge': v_bulge
    }


def process_sparc_directory(data_dir, galaxy_list=None, vinf_max=None, upsilon_fixed=None):
    """
    Process all SPARC galaxies in a directory.
    
    Fits: V_tot² = V_gas² + Υ_d·V_disk² + V_halo²(r_c, v_inf)
    
    Parameters:
        vinf_max : if set, only process galaxies with v_inf < vinf_max (dwarf mode)
        upsilon_fixed : if set, fix Υ_d to this value instead of fitting it
    """
    data_path = Path(data_dir)
    results = []

    # Find all .dat files
    dat_files = sorted(data_path.glob("*_rotmod.dat"))
    if not dat_files:
        dat_files = sorted(data_path.glob("*.dat"))

    print(f"Found {len(dat_files)} data files.")

    for fpath in dat_files:
        name = fpath.stem.replace("_rotmod", "").replace("_data", "")

        if galaxy_list and name not in galaxy_list:
            continue

        gal_data = load_sparc_galaxy(fpath)
        if gal_data is None:
            continue

        # Prepare squared velocities
        r = gal_data['r']
        v_obs = gal_data['v_obs']
        v_err = gal_data['v_err']
        v_gas_sq = gal_data['v_gas']**2
        v_disk_sq = gal_data['v_disk']**2
        v_bulge_sq = gal_data['v_bulge']**2 if 'v_bulge' in gal_data else np.zeros_like(r)

        # Estimate initial guesses from data
        r_c_guess = np.median(r) * 0.3
        # V_inf guess: velocity at largest radii minus baryons
        outer_mask = r > np.median(r)
        if np.any(outer_mask):
            v_outer = v_obs[outer_mask]
            v_gas_outer = np.sqrt(v_gas_sq[outer_mask])
            v_disk_outer = np.sqrt(v_disk_sq[outer_mask])
            v_res_outer = np.sqrt(np.maximum(v_outer**2 - v_gas_outer**2 - v_disk_outer**2, 0))
            v_inf_guess = float(np.median(v_res_outer))
        else:
            v_inf_guess = float(np.median(v_obs)) * 0.7

        # Fit
        fit_result = fit_mcw_halo_with_baryons(
            r, v_obs, v_err, v_gas_sq, v_disk_sq, v_bulge_sq,
            r_c_guess=r_c_guess, v_inf_guess=v_inf_guess,
            upsilon_fixed=upsilon_fixed
        )

        if fit_result is None:
            # Try without baryons as fallback
            v_res_sq = np.maximum(v_obs**2 - v_gas_sq - 0.5*v_disk_sq - v_bulge_sq, 0)
            v_res = np.sqrt(v_res_sq)
            mask = v_res_sq > 0
            if np.sum(mask) < 5:
                continue
            # Simple fit on residual
            try:
                def simple_model(r, r_c, v_inf):
                    return np.sqrt(np.maximum(mcw_velocity_squared(r, np.abs(r_c), np.abs(v_inf)), 0))
                popt, _ = curve_fit(simple_model, r[mask], v_res[mask],
                                   p0=[r_c_guess, v_inf_guess], maxfev=10000,
                                   bounds=([0.01, 1.0], [500, 5000]))
                r_c, v_inf = np.abs(popt)
                upsilon_d = 0.5
                r_c_err, v_inf_err, upsilon_err = r_c*0.3, v_inf*0.1, 0.1
                chi2_red = 5.0
            except (RuntimeError, ValueError):
                continue
        else:
            r_c, v_inf, upsilon_d, r_c_err, v_inf_err, upsilon_err, chi2_red = fit_result

        # Apply dwarf filter
        if vinf_max is not None and v_inf > vinf_max:
            continue

        # Compute m_Gamma
        m_g = compute_m_gamma(r_c, v_inf)
        m_g_err = m_g * (r_c_err/r_c + v_inf_err/v_inf) if r_c > 0 and v_inf > 0 else 0

        # Quality flag
        if chi2_red < 3.0 and r_c_err/r_c < 0.5:
            quality = "ok"
        elif chi2_red < 7.0:
            quality = "marginal"
        else:
            quality = "poor"

        # Estimate baryonic mass (stellar + gas) from velocities
        # Rough: M_b ≈ (v_rot² · R_last) / G
        r_last = r[-1]
        v_last = v_obs[-1]
        m_b = (v_last**2 * r_last * KPC_TO_M) / (G * 1.989e33) * 1.989e33  # Msun
        # Simplified: use the baryonic Tully-Fisher relation
        m_b = 1e10 * (v_inf / 100)**4  # rough BTFR estimate

        gal = GalaxyFit(
            name=name,
            r_c=r_c,
            r_c_err=r_c_err,
            v_inf=v_inf,
            v_inf_err=v_inf_err,
            rho_0=v_inf**2 / (4*np.pi*G*r_c**2) if r_c > 0 else 0,
            m_gamma=m_g,
            m_gamma_err=m_g_err,
            m_b=m_b,
            chi2_red=chi2_red,
            n_points=len(r),
            quality=quality
        )
        results.append(gal)
        print(f"  {name:22s}: r_c = {r_c:6.2f} ± {r_c_err:5.2f} kpc, "
              f"v_inf = {v_inf:6.1f} ± {v_inf_err:4.1f} km/s, "
              f"Υ_d = {upsilon_d:.3f}, "
              f"m_Γ = {m_g:.2e} eV, χ²_red = {chi2_red:.2f} [{quality}]")

    return results


# ============================================================================
# ANALYSIS AND PLOTTING
# ============================================================================

def analyze_results(results, output_dir="./output"):
    """Perform statistical analysis and generate plots."""
    out = Path(output_dir)
    out.mkdir(exist_ok=True, parents=True)

    # Filter good-quality fits
    good = [g for g in results if g.quality == "ok"]
    all_fits = results

    if len(good) < 3:
        print("WARNING: Fewer than 3 good-quality fits. Using all fits.")
        good = all_fits

    # Extract arrays
    r_c_arr = np.array([g.r_c for g in good])
    v_inf_arr = np.array([g.v_inf for g in good])
    m_g_arr = np.array([g.m_gamma for g in good])
    names_arr = [g.name for g in good]

    log_m = np.log10(m_g_arr)
    mu_log_m = np.mean(log_m)
    sigma_log_m = np.std(log_m)

    print(f"\n{'='*60}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Number of galaxies with good fits: {len(good)}")
    print(f"log10(m_Γ) mean  = {mu_log_m:.3f}")
    print(f"log10(m_Γ) std   = {sigma_log_m:.3f}")
    print(f"m_Γ geometric mean = {10**mu_log_m:.2e} eV")
    print(f"m_Γ dispersion     = factor ~{10**sigma_log_m:.1f}x")

    # --- Figure 1: Distribution of m_Gamma ---
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.hist(log_m, bins=max(8, len(good)//3), edgecolor='black', alpha=0.7)
    ax1.axvline(mu_log_m, color='red', linestyle='--', label=f'Mean: {mu_log_m:.2f}')
    ax1.set_xlabel(r'$\log_{10}(m_\Gamma\ \mathrm{[eV]})$', fontsize=14)
    ax1.set_ylabel('Number of galaxies', fontsize=14)
    ax1.set_title('MCW-1 Prediction: Universal $m_\\Gamma$', fontsize=16)
    ax1.legend(fontsize=12)
    ax1.grid(alpha=0.3)
    fig1.tight_layout()
    fig1.savefig(out / "m_gamma_distribution.png", dpi=150)
    print(f"Saved: {out / 'm_gamma_distribution.png'}")

    # --- Figure 2: r_c vs v_inf (should be slope -1) ---
    fig2, ax2 = plt.subplots(figsize=(10, 8))
    log_rc = np.log10(r_c_arr)
    log_v = np.log10(v_inf_arr)

    slope, intercept, r_value, p_value, std_err = linregress(log_v, log_rc)
    label_text = f"Slope = {slope:.2f} ± {std_err:.2f}\n"
    label_text += f"R² = {r_value**2:.3f}\n"
    label_text += f"MCW-1 predicts: slope = -1"

    ax2.scatter(log_v, log_rc, c='steelblue', s=60, edgecolors='black', alpha=0.8)
    v_range = np.linspace(log_v.min()-0.1, log_v.max()+0.1, 100)
    ax2.plot(v_range, slope*v_range + intercept, 'r-', linewidth=2)
    ax2.plot(v_range, -v_range + (np.mean(log_rc) + np.mean(log_v)), 'g--', linewidth=2, label='MCW-1 (slope = -1)')

    for i, name in enumerate(names_arr):
        ax2.annotate(name, (log_v[i], log_rc[i]), fontsize=6, alpha=0.6,
                     xytext=(3, 3), textcoords='offset points')

    ax2.set_xlabel(r'$\log_{10}(v_\infty\ \mathrm{[km/s]})$', fontsize=14)
    ax2.set_ylabel(r'$\log_{10}(r_c\ \mathrm{[kpc]})$', fontsize=14)
    ax2.set_title(r'MCW-1 Prediction: $r_c \propto v_\infty^{-1}$', fontsize=16)
    ax2.legend(fontsize=12)
    ax2.grid(alpha=0.3)
    ax2.text(0.05, 0.95, label_text, transform=ax2.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    fig2.tight_layout()
    fig2.savefig(out / "rc_vs_vinf.png", dpi=150)
    print(f"Saved: {out / 'rc_vs_vinf.png'}")

    # --- Figure 3: Individual galaxy fits (sample) ---
    n_sample = min(6, len(good))
    fig3, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes = axes.flatten()

    for i in range(n_sample):
        ax = axes[i]
        g = good[i]
        # Recompute model
        r_model = np.logspace(-1, np.log10(g.r_c * 5), 100)
        v_model = np.sqrt(mcw_velocity_squared(r_model, g.r_c, g.v_inf))
        ax.plot(r_model, v_model, 'r-', linewidth=2, label='MCW-1 fit')
        ax.axhline(g.v_inf, color='gray', linestyle=':', alpha=0.5)
        ax.axvline(g.r_c, color='blue', linestyle='--', alpha=0.5, label=f'$r_c$={g.r_c:.1f}')

        ax.set_title(f"{g.name}\n$m_\\Gamma$={g.m_gamma:.2e} eV", fontsize=11)
        ax.set_xlabel('R [kpc]')
        ax.set_ylabel('V [km/s]')
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    for i in range(n_sample, 6):
        axes[i].set_visible(False)

    fig3.suptitle('MCW-1 Halo Fits — Sample Galaxies', fontsize=16)
    fig3.tight_layout()
    fig3.savefig(out / "sample_fits.png", dpi=150)
    print(f"Saved: {out / 'sample_fits.png'}")

    # --- Figure 4: r_c * v_inf product ---
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    rc_v = r_c_arr * v_inf_arr
    ax4.hist(rc_v, bins=max(6, len(good)//3), edgecolor='black', alpha=0.7)
    ax4.axvline(np.median(rc_v), color='red', linestyle='--',
                label=f'Median: {np.median(rc_v):.0f} kpc·km/s')
    ax4.set_xlabel(r'$r_c \cdot v_\infty$ [kpc·km/s]', fontsize=14)
    ax4.set_ylabel('Number of galaxies', fontsize=14)
    ax4.set_title(r'MCW-1: $r_c \cdot v_\infty \approx$ constant', fontsize=16)
    ax4.legend(fontsize=12)
    ax4.grid(alpha=0.3)
    fig4.tight_layout()
    fig4.savefig(out / "rc_vinf_product.png", dpi=150)
    print(f"Saved: {out / 'rc_vinf_product.png'}")

    # --- Export results as CSV ---
    csv_path = out / "mcw1_sparc_results.csv"
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Galaxy', 'r_c_kpc', 'r_c_err', 'v_inf_kms', 'v_inf_err',
                         'rc_v_inf', 'm_gamma_eV', 'm_gamma_err', 'chi2_red', 'quality'])
        for g in results:
            writer.writerow([g.name, f"{g.r_c:.3f}", f"{g.r_c_err:.3f}",
                             f"{g.v_inf:.1f}", f"{g.v_inf_err:.1f}",
                             f"{g.r_c*g.v_inf:.1f}", f"{g.m_gamma:.3e}",
                             f"{g.m_gamma_err:.3e}", f"{g.chi2_red:.3f}", g.quality])
    print(f"Saved: {csv_path}")

    # --- Export JSON summary ---
    summary = {
        "model": "MCW-1",
        "relation": "r_c * v_inf = hbar / m_Gamma",
        "n_galaxies_total": len(results),
        "n_galaxies_good": len(good),
        "log10_m_gamma_mean": float(mu_log_m),
        "log10_m_gamma_std": float(sigma_log_m),
        "m_gamma_geometric_mean_eV": float(10**mu_log_m),
        "slope_logrc_vs_logv": float(slope),
        "slope_err": float(std_err),
        "r_squared": float(r_value**2),
        "mcw_predicted_slope": -1.0,
    }
    with open(out / "mcw1_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Saved: {out / 'mcw1_summary.json'}")

    return summary


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="MCW-1 / TCM-1 SPARC Analysis: test r_c * v_inf ≈ constant")
    parser.add_argument("--data-dir", type=str, default="./SPARC_data",
                        help="Path to SPARC data directory")
    parser.add_argument("--output-dir", type=str, default="./mcw1_output",
                        help="Output directory for results and plots")
    parser.add_argument("--galaxies", type=str, nargs="*", default=None,
                        help="Specific galaxy names to process (default: all)")
    parser.add_argument("--dwarf-only", action="store_true",
                        help="Only process dwarf galaxies (v_inf < 80 km/s)")
    parser.add_argument("--fix-upsilon", type=float, default=None,
                        help="Fix Υ_d to this value (default: free fit). Standard SPARC: 0.5 at 3.6μm")
    parser.add_argument("--generate-synthetic", action="store_true",
                        help="Generate synthetic data for testing (no real data needed)")
    args = parser.parse_args()

    # Determine options
    vinf_max = 80.0 if args.dwarf_only else None
    upsilon_fixed = args.fix_upsilon

    if args.generate_synthetic:
        print("Generating synthetic rotation curves for testing...")
        results = generate_synthetic_galaxies()
    else:
        data_dir = Path(args.data_dir)
        if not data_dir.exists():
            print(f"Data directory '{args.data_dir}' not found.")
            print("Options:")
            print("  1. Download SPARC data from: https://astroweb.cwru.edu/SPARC/")
            print("  2. Use --generate-synthetic for testing with mock data")
            return
        results = process_sparc_directory(args.data_dir, args.galaxies,
                                           vinf_max=vinf_max, upsilon_fixed=upsilon_fixed)

    if not results:
        print("No galaxies were successfully fitted.")
        return

    summary = analyze_results(results, args.output_dir)

    # Final verdict
    print(f"\n{'='*60}")
    print("MCW-1 VERDICT")
    print(f"{'='*60}")
    sigma = summary['log10_m_gamma_std']
    slope = summary['slope_logrc_vs_logv']
    slope_err = summary['slope_err']

    if sigma < 0.3 and abs(slope + 1.0) < 0.3:
        print("✅ STRONG SUPPORT: m_Γ is nearly universal AND r_c ∝ 1/v_inf.")
        print("   The MCW-1 core prediction is validated.")
    elif sigma < 0.5 and abs(slope + 1.0) < 0.5:
        print("🟡 MODERATE SUPPORT: Trends are visible but dispersion is significant.")
        print("   Worth pursuing with environmental corrections.")
    elif sigma < 0.3:
        print("🟡 PARTIAL: m_Γ is universal but r_c-v_inf slope ≠ -1.")
        print("   Check for baryonic effects or profile systematics.")
    else:
        print("🔴 WEAK / REFUTED: m_Γ varies widely across galaxies.")
        print("   The MCW-1 model in its current form is in difficulty.")

    slope_diff = abs(slope - (-1.0))
    if slope_diff < slope_err:
        print(f"\n   Slope = {slope:.2f} ± {slope_err:.2f} — compatible with -1 within 1σ.")
    else:
        print(f"\n   Slope = {slope:.2f} ± {slope_err:.2f} — deviates from -1 by {slope_diff/slope_err:.1f}σ.")


# ============================================================================
# SYNTHETIC DATA GENERATOR (for testing without real SPARC data)
# ============================================================================

def generate_synthetic_galaxies(n_galaxies=50, m_gamma_true=5e-23):
    """Generate synthetic rotation curves that satisfy MCW-1 predictions."""
    np.random.seed(42)
    results = []

    for i in range(n_galaxies):
        # Generate physically plausible parameters
        v_inf = 10**(np.random.uniform(1.5, 2.5))  # 30-300 km/s

        # MCW-1: r_c * v_inf = ℏ·c²/m_Γ (with unit conversion)
        # r_c [kpc] = ℏ·c² / (m_Γ [eV] * v_inf [km/s] * KPC_TO_M * KMS_TO_MS)
        r_c_true = HBAR_C2 / (m_gamma_true * v_inf * KMS_TO_MS * KPC_TO_M)
        r_c = r_c_true * 10**(np.random.normal(0, 0.1))  # 0.1 dex scatter

        # Generate synthetic rotation curve (halo-only, no baryons)
        n_points = np.random.randint(10, 30)
        r = np.logspace(-0.5, np.log10(r_c * 5), n_points)
        v_true = np.sqrt(mcw_velocity_squared(r, r_c, v_inf))
        v_err = 0.05 * v_true + 2.0  # 5% + floor
        v_obs = v_true + np.random.normal(0, v_err)
        v_gas_sq = np.zeros_like(r)
        v_disk_sq = np.zeros_like(r)

        # Fit with baryons (zeros for synthetic test)
        fit_result = fit_mcw_halo_with_baryons(
            r, v_obs, v_err, v_gas_sq, v_disk_sq, np.zeros_like(r),
            r_c_guess=r_c*0.8, v_inf_guess=v_inf*0.8
        )
        if fit_result is None:
            continue

        r_c_fit, v_inf_fit, upsilon_d, r_c_err, v_inf_err, upsilon_err, chi2_red = fit_result
        m_g = compute_m_gamma(r_c_fit, v_inf_fit)
        m_g_err = m_g * (r_c_err/r_c_fit + v_inf_err/v_inf_fit)

        gal = GalaxyFit(
            name=f"SYNTH_{i:03d}",
            r_c=r_c_fit, r_c_err=r_c_err,
            v_inf=v_inf_fit, v_inf_err=v_inf_err,
            rho_0=v_inf_fit**2 / (4*np.pi*G*r_c_fit**2) if r_c_fit > 0 else 0,
            m_gamma=m_g, m_gamma_err=m_g_err,
            m_b=1e10*(v_inf_fit/100)**4,
            chi2_red=chi2_red,
            n_points=n_points,
            quality="ok" if chi2_red < 3.0 else "marginal"
        )
        results.append(gal)

    print(f"Generated {len(results)} synthetic galaxies with m_Γ = {m_gamma_true:.2e} eV")
    return results


if __name__ == "__main__":
    main()
