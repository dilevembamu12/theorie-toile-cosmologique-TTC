# -*- coding: utf-8 -*-
"""
TTC — Bilan energetique du "deliement" (n = 1 -> 0)
===================================================
Accompagne TTC-deliement-bilan-energetique.md

Partie 1 : identites cinematiques exactes (l'invariant c^2 = v^2 + w^2 est un
           theoreme de la RR a energie constante, pas un axiome).
Partie 2 : energie de la composante de phase d'un noeud d'enroulement n pour un
           coeur de taille delta -> illustration numerique du no-go topologique.

Unites : c = hbar = 1. Longueur de reference R = 1 (rayon exterieur).
Sorties : ttc_deliement_bilan.json, ttc_deliement_bilan.png
"""

import json
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False


# ----------------------------------------------------------------------------
# Partie 1 — cinematique exacte
# ----------------------------------------------------------------------------
def kinematic_table(n_pts=7):
    """E = m0 c^2 constante. Theta = angle de deliement (0 = matiere, pi/2 = transit)."""
    m0 = 1.0
    E = m0                      # c = 1  => E = m0
    thetas = np.radians([0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 89.9])
    rows = []
    for th in thetas:
        v = np.sin(th)          # c = 1
        w = np.cos(th)
        gamma = 1.0 / np.sqrt(max(1.0 - v * v, 1e-300))
        M = m0 / gamma          # masse invariante
        p = v * E               # p = v E / c^2, c = 1
        rows.append(
            {
                "theta_deg": float(np.degrees(th)),
                "beta_v": float(v),
                "w_over_c": float(w),
                "gamma": float(gamma),
                "M_over_m0": float(M / m0),
                "p_over_m0c": float(p / m0),
                "check_v2_plus_w2": float(v * v + w * w),
                "check_M_eq_m0_w": float(M - m0 * w),
                "check_M_from_p": float(M - np.sqrt(max(E * E - p * p, 0.0))),
            }
        )
    return rows


# ----------------------------------------------------------------------------
# Partie 2 — energie d'un coeur d'enroulement n
# ----------------------------------------------------------------------------
def energy_components(rho, n, kappa=1.0, n_grid=300001):
    """
    Gamma(r) = v_Gamma * tanh(r/delta),  Phi = n * theta  (enroulement autour d'un point)

        E/(4 pi v_Gamma^2 R) = int_0^1 [ 1/2 f'^2 + 1/2 f^2 n^2/x^2 + (kappa/4)(f^2-1)^2 ] x^2 dx

    avec x = r/R, rho = delta/R, kappa = alpha v_Gamma^2 R^2.
    Retourne (E_gradient_enroulement, E_potentiel) en unites de 4 pi v_Gamma^2 R,
    les deux composantes separement car elles n'ont pas la meme loi d'echelle en R.
    """
    x = np.linspace(1e-6, 1.0, n_grid)
    u = x / rho
    f = np.tanh(u)
    sech2 = 1.0 - f ** 2          # stable (evite l'overflow de cosh)
    dfdx = sech2 / rho

    grad = 0.5 * dfdx ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        wind = 0.5 * (f ** 2) * (n ** 2) / (x ** 2)
    wind[~np.isfinite(wind)] = 0.5 * n ** 2 / rho ** 2
    pot = 0.25 * kappa * (f ** 2 - 1.0) ** 2

    trapz = getattr(np, "trapezoid", None) or np.trapz
    e_wind = float(trapz((grad + wind) * x ** 2, x))
    e_pot = float(trapz(pot * x ** 2, x))
    return e_wind, e_pot


def radius_scan(radii, n=1, rho_rel=0.01, alpha=1.0):
    """Loi d'echelle : E_gradient ~ R (infrarouge), E_potentiel ~ R^3.
    kappa = alpha v^2 R^2 doit donc varier avec R (v = 1, alpha fixe)."""
    out = []
    for R in radii:
        kappa = alpha * R ** 2
        e_wind, e_pot = energy_components(rho_rel, n=n, kappa=kappa)
        # E = 4 pi v^2 R * (integrale)  ->  on rapporte tout a 4 pi v^2
        E_wind = e_wind * R
        E_pot = e_pot * R
        out.append({"R": float(R),
                    "E_wind": E_wind,
                    "E_pot": E_pot,
                    "E_wind_over_R": E_wind / R,
                    "E_pot_over_R3": E_pot / R ** 3})
    return out


def main():
    kin = kinematic_table(7)
    lines = []
    lines.append("=" * 78)
    lines.append("PARTIE 1 — Identites cinematiques (E = m0 c^2 = const, c = 1)")
    lines.append("=" * 78)
    hdr = f"{'Theta':>7} {'v/c':>8} {'w/c':>8} {'gamma':>9} {'M/m0':>8} {'p/m0c':>8}  {'v2+w2':>8}"
    lines.append(hdr)
    lines.append("-" * 78)
    for r in kin:
        lines.append(
            f"{r['theta_deg']:7.1f} {r['beta_v']:8.5f} {r['w_over_c']:8.5f} "
            f"{r['gamma']:9.4f} {r['M_over_m0']:8.5f} {r['p_over_m0c']:8.5f}  "
            f"{r['check_v2_plus_w2']:8.6f}"
        )
    lines.append("")
    lines.append("=> v^2 + w^2 = 1 exactement ; M/m0 = w/c exactement ; M = sqrt(E^2-p^2).")
    lines.append("=> Le 'deliement' est la conversion progressive M -> 0 a E constante.")

    radii = [1.0, 3.0, 10.0, 30.0, 100.0]
    scan = radius_scan(radii, n=1, rho_rel=0.01, alpha=1.0)
    scan0 = radius_scan(radii, n=0, rho_rel=0.01, alpha=1.0)

    lines.append("")
    lines.append("=" * 78)
    lines.append("PARTIE 2 — Energie du noeud d'enroulement en fonction du rayon R")
    lines.append("(profil tanh, coeur delta = 0.01 R, alpha = 1 ; energies en unites 4 pi v^2)")
    lines.append("=" * 78)
    lines.append(f"{'R':>7} {'E_grad(n=1)':>13} {'E_grad/R':>10} {'E_pot(n=1)':>13} {'E_pot/R^3':>12}")
    lines.append("-" * 78)
    for s in scan:
        lines.append(
            f"{s['R']:7.1f} {s['E_wind']:13.5f} {s['E_wind_over_R']:10.5f} "
            f"{s['E_pot']:13.4e} {s['E_pot_over_R3']:12.4e}"
        )
    lines.append("")
    lines.append("=> E_grad/R -> 0.5  (soit 4*pi*0.5 = 2*pi v^2 par unite de R) : PROPORTIONNEL A R")
    lines.append("=> E_pot/R^3 -> cste  : proportionnel a R^3 (energie volumique)")
    lines.append("=> L'energie du noeud NE depend PAS de la taille du coeur (delta) :")
    lines.append("   elle est dominee par le rayon exterieur. Un 'noeud' d'enroulement")
    lines.append("   dans MCW-1 est un monopole global, pas une particule localisee.")
    lines.append("")
    lines.append("E_noeud = 2*pi*n^2*v_Gamma^2*R   (terme dominant, R = rayon du noeud)")

    # ---- Contrainte sur v_Gamma si le noeud doit avoir la masse du proton ----
    mp_MeV = 938.272
    # E = 2 pi v^2 R et R = 1/m (longueur de Compton) en unites naturelles
    # => 2 pi v^2 / m = m  =>  v = m / sqrt(2 pi)
    v_gamma_MeV = mp_MeV / np.sqrt(2 * np.pi)
    lines.append("")
    lines.append("=" * 78)
    lines.append("PARTIE 3 — Contrainte sur v_Gamma (si le noeud EST le proton)")
    lines.append("=" * 78)
    lines.append(f"E = 2*pi*v_Gamma^2*R avec R = 1/m_p (taille Compton)")
    lines.append(f"  => v_Gamma = m_p/sqrt(2*pi) = {v_gamma_MeV:.1f} MeV")
    lines.append(f"  => soit ~ {v_gamma_MeV / 200.0:.2f} x Lambda_QCD (200 MeV)")
    lines.append("")
    lines.append("Comparer a TTC-White-Paper.md §2.6 : v_Gamma ~ M_Pl = 1.22e28 eV.")
    lines.append("Les deux choix sont incompatibles -> probleme de hierarchie interne.")
    lines.append("")
    lines.append("Condition de coeur stable (kappa = alpha v^2 R^2 >= 1) :")
    alpha_min = 1.0 / ((v_gamma_MeV / mp_MeV) ** 2)
    lines.append(f"  alpha >= 1/(v_Gamma*R)^2 = (m_p/v_Gamma)^2 = {alpha_min:.2f}")
    lines.append("  => couplage fort mais autorise ; a l'inverse alpha ~ 1e-34 (dossier")
    lines.append("     'hierarchie') est incompatible avec un noeud a l'echelle du proton.")

    txt = "\n".join(lines)
    print(txt)

    with open("ttc_deliement_bilan.json", "w", encoding="utf-8") as fh:
        json.dump({"kinematics": kin, "radius_scan_n1": scan, "radius_scan_n0": scan0,
                   "v_gamma_if_knot_is_proton_MeV": float(v_gamma_MeV),
                   "alpha_min_for_stable_core": float(alpha_min)},
                  fh, indent=2, ensure_ascii=False)

    if HAS_MPL:
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))

        th = np.linspace(1e-4, 0.5 * np.pi - 1e-4, 400)
        ax[0].plot(np.degrees(th), np.cos(th), lw=2, label=r"$M/m_0 = \cos\Theta = w/c$")
        ax[0].plot(np.degrees(th), np.sin(th), lw=2, label=r"$\beta_v = \sin\Theta$")
        ax[0].plot(np.degrees(th), 1 / np.cos(th), lw=1.5, ls="--",
                   label=r"$\gamma = 1/\cos\Theta$")
        ax[0].set_xlabel(r"$\Theta$ (deg)   —   0 = nœud  |  90 = transit")
        ax[0].set_ylabel("grandeur normalisée")
        ax[0].set_ylim(0, 6)
        ax[0].set_title(r"§3 — $E=m_0c^2$ constant : $w=cM/m_0$")
        ax[0].legend(fontsize=8)
        ax[0].grid(alpha=0.3)

        R = np.array([s["R"] for s in scan])
        ax[1].loglog(R, [s["E_wind"] for s in scan], "o-", lw=2,
                     label=r"$E_\nabla \simeq 2\pi n^2 v_\Gamma^2 R$  ($\propto R$)")
        ax[1].loglog(R, [s["E_pot"] for s in scan], "s-", lw=2,
                     label=r"$E_U \propto R^3$")
        ax[1].set_xlabel(r"rayon du nœud $R$  (unités $v_\Gamma=1$)")
        ax[1].set_ylabel(r"$E$  (unités $4\pi v_\Gamma^2$)")
        ax[1].set_title(r"§4 — énergie dominée par l'infrarouge, pas par le cœur")
        ax[1].legend(fontsize=8)
        ax[1].grid(alpha=0.3, which="both")

        fig.suptitle("TTC — bilan énergétique du déliement (n=1 → 0)", fontsize=11)
        fig.tight_layout()
        fig.savefig("ttc_deliement_bilan.png", dpi=150)
        print("\n[ok] ttc_deliement_bilan.png écrit")


if __name__ == "__main__":
    main()
