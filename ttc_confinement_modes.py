# -*- coding: utf-8 -*-
"""
TTC — Test du comptage de modes : "la matiere est-elle de la lumiere confinee ?"
===============================================================================
Accompagne TTC-deliement-bilan-energetique.md, section 9.

Ontologie testee ("lumiere confinee", notee C-light) :
    la matiere est un MODE d'un champ sans masse (Phi, m_Phi = 0, WP ligne 218)
    confine dans une cavite. La masse du mode est son energie propre :
        loi LINEAIRE    (cavite relativiste, photon) : m_n = hbar c x_n / L
        loi QUADRATIQUE (puits Schrodinger)          : m_n = hbar^2 x_n^2 /(2 mu L^2)
    ou x_n sont les zeros sans dimension fixes par la FORME du puits.

Point cle : L ne fait que fixer l'echelle globale, il ne change AUCUN rapport.
Les rapports de masse sont donc entierement determines par la forme du puits.
C'est une prediction, donc une prise pour la falsification.

Theoreme de comptage (Partie 1)
-------------------------------
Les zeros (l = 0) d'un puits spherique verifient (k-1/2)*pi < x_k < k*pi.
Donc x_N/x_1 < 2N pour un puits a N etats lies.

Corollaire : pour obtenir un rapport m_N/m_1 donne, il faut
        N > (m_N/m_1)^(1/alpha) / 2
Avec les leptons charges (m_tau/m_e = 3477), cela impose un NOMBRE MINIMAL de
generations. On en observe 3.

Sorties : ttc_confinement_modes.json, ttc_confinement_modes.png
"""

import json
import numpy as np
from scipy.special import spherical_jn

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# --- masses observees (MeV) -------------------------------------------------
M_E, M_MU, M_TAU = 0.51099895000, 105.6583755, 1776.86
RATIO_MU = M_MU / M_E        # 206.768
RATIO_TAU = M_TAU / M_E      # 3477.23
SPAN = RATIO_TAU             # etalement du spectre


# ---------------------------------------------------------------------------
# Partie 1 — theoreme de comptage
# ---------------------------------------------------------------------------
def part1_counting_theorem(span=SPAN):
    """N_min tel que x_N/x_1 puisse atteindre span (loi lineaire ou quadratique)."""
    rows = []
    for name, alpha in (("lineaire (cavite relativiste, m ~ x)", 1.0),
                        ("quadratique (puits Schrodinger, m ~ x^2)", 2.0)):
        need = span ** (1.0 / alpha)      # x_N/x_1 requis
        n_min = int(np.floor(need / 2.0)) + 1   # car x_N/x_1 < 2N
        rows.append({"loi": name, "alpha": alpha,
                     "x_N_over_x_1_requis": float(need),
                     "N_min_theorique": n_min})
    return rows


# ---------------------------------------------------------------------------
# Partie 2 — puits sans parametre libre : predictions chiffrees
# ---------------------------------------------------------------------------
def bessel_zeros(l_max=4, n_max=5):
    """Zeros x_{n,l} de j_l."""
    tab = {}
    for l in range(l_max + 1):
        zs = []
        x0 = 1e-3
        # balayage puis bissection
        grid = np.linspace(1e-3, (n_max + 0.6) * np.pi, 200000)
        vals = spherical_jn(l, grid)
        sc = np.where(np.sign(vals[:-1]) * np.sign(vals[1:]) < 0)[0]
        for i in sc[:n_max]:
            a, b = grid[i], grid[i + 1]
            for _ in range(80):
                m = 0.5 * (a + b)
                if np.sign(spherical_jn(l, a)) * np.sign(spherical_jn(l, m)) <= 0:
                    b = m
                else:
                    a = m
            zs.append(float(0.5 * (a + b)))
        tab[l] = zs
    return tab


def part2_parameter_free(ztab, n_states=3):
    """Puits infiniment profond : forme fixe, AUCUN parametre.

    Version la plus favorable a l'ontologie : on autorise TOUS les moments
    cinetiques l <= 4 et on prend les 3 niveaux les plus bas (cela reduit les
    rapports, donc rapproche de l'observation).
    """
    levels = sorted(z for l in ztab for z in ztab[l])[:n_states]
    pred_lin = [float(zz / levels[0]) for zz in levels]
    pred_quad = [float((zz / levels[0]) ** 2) for zz in levels]
    obs = [1.0, RATIO_MU, RATIO_TAU]
    rows = []
    for i in range(n_states):
        rows.append({"niveau": i + 1, "x_n": levels[i],
                     "predit_lineaire": pred_lin[i],
                     "predit_quadratique": pred_quad[i],
                     "observe_m_lepton_m_e": obs[i],
                     "ecart_lineaire": obs[i] / pred_lin[i],
                     "ecart_quadratique": obs[i] / pred_quad[i]})
    return rows


# ---------------------------------------------------------------------------
# Partie 3 — puits fini : UN seul parametre de forme, donc un vrai test
# ---------------------------------------------------------------------------
def finite_well_zeros(VL2, l=0, n_scan=4000):
    """Zeros de x*cot(x) = -sqrt(VL2 - x^2)  (l=0), VL2 = 2 mu V L^2 / hbar^2.
    x doit tomber dans (k*pi + pi/2, (k+1)*pi) ou cot < 0."""
    if VL2 <= 0:
        return []
    R0 = np.sqrt(VL2)
    roots = []
    for k in range(0, int(R0 / np.pi) + 2):
        a, b = k * np.pi + np.pi / 2 + 1e-9, min((k + 1) * np.pi - 1e-9, R0)
        if b <= a:
            continue

        def g(x):
            x = np.asarray(x, dtype=float)
            return x / np.tan(x) + np.sqrt(np.maximum(R0 * R0 - x * x, 0.0))

        xs = np.linspace(a, b, n_scan)
        vs = g(xs)
        ok = np.isfinite(vs)
        sc = [i for i in range(len(vs) - 1)
              if ok[i] and ok[i + 1] and vs[i] * vs[i + 1] < 0]
        for i in sc:
            lo, hi = xs[i], xs[i + 1]
            flo = g(lo)
            for _ in range(120):
                m = 0.5 * (lo + hi)
                if flo * g(m) <= 0:
                    hi = m
                else:
                    lo, flo = m, g(m)
            roots.append(float(0.5 * (lo + hi)))
    return sorted(roots)


def part3_finite_well():
    """Un puits spherique fini n'a qu'UN parametre de forme VL2.

    La fenetre a exactement 3 etats lies est R0 in (5pi/2, 7pi/2), soit
    VL2 in (61.7, 120.9). L'etendue maximale y est atteinte aux bornes :
        x_1 -> pi/2 ,  x_3 -> 3pi   =>   x_3/x_1 -> 6  (et non 2N quelconque)
    On balaye toute la fenetre pour le verifier numeriquement.
    """
    scan = []
    for VL2 in np.linspace(60.0, 122.0, 620):
        zs = finite_well_zeros(VL2)
        if len(zs) == 3:
            scan.append({"VL2": float(VL2),
                         "x": zs,
                         "span_lineaire": zs[-1] / zs[0],
                         "span_quadratique": (zs[-1] / zs[0]) ** 2})
    if not scan:
        return {}, []
    max_lin = max(s["span_lineaire"] for s in scan)
    max_quad = max(s["span_quadratique"] for s in scan)
    summary = {"n_points_3_etats": len(scan),
               "VL2_min": scan[0]["VL2"], "VL2_max": scan[-1]["VL2"],
               "span_lineaire_max_atteignable": float(max_lin),
               "span_quadratique_max_atteignable": float(max_quad),
               "borne_theorique_lineaire": 6.0,
               "borne_theorique_quadratique": 36.0,
               "span_observe": float(SPAN)}
    return summary, scan


# ---------------------------------------------------------------------------
# Partie 4 — bilans de parametres
# ---------------------------------------------------------------------------
def part4_parameter_budget(n_fermions=9):
    """Combien de parametres libres dans chaque ontologie ?"""
    return [
        {"ontologie": "Modele standard (Yukawa)", "parametres": n_fermions,
         "commentaire": "1 couplage de Yukawa par fermion"},
        {"ontologie": "Lumiere confinee, une cavite par fermion",
         "parametres": 2 * n_fermions,
         "commentaire": "profondeur V et taille L par fermion -> 2N"},
        {"ontologie": "Lumiere confinee, une seule forme de puits",
         "parametres": 1,
         "commentaire": "1 parametre de forme, mais REFUTE (Partie 3)"},
    ]


def main():
    L = []
    add = L.append

    # ---- P1
    add("=" * 80)
    add("PARTIE 1 — Theoreme de comptage : une cavite n'a pas de trous")
    add("=" * 80)
    add("Un puits a N etats lies verifie x_N/x_1 < 2N  (zeros l=0).")
    add("Pour atteindre l'etendue observee m_tau/m_e = %.2f :" % SPAN)
    add("")
    p1 = part1_counting_theorem()
    add(f"{'loi de dispersion':<44} {'x_N/x_1 requis':>16} {'N_min':>8}")
    add("-" * 80)
    for r in p1:
        add(f"{r['loi']:<44} {r['x_N_over_x_1_requis']:16.2f} {r['N_min_theorique']:8d}")
    add("-" * 80)
    add("=> NOMBRE MINIMAL DE LEPTONS CHARGES PREDIT :")
    for r in p1:
        add(f"   {r['loi'].split(' (')[0]:<12} : au moins {r['N_min_theorique']} leptons charges")
    add("")
    add("   OBSERVE : 3.")
    add("   => L'ontologie 'lumiere confinee' avec une cavite ordinaire est REFUTEE,")
    add("      quelle que soit la forme du puits (borne independante de la forme).")

    # ---- P2
    add("")
    add("=" * 80)
    add("PARTIE 2 — Puits infiniment profond (forme fixe, zero parametre)")
    add("=" * 80)
    ztab = bessel_zeros()
    p2 = part2_parameter_free(ztab)
    add("Version la plus favorable : tous les moments l <= 4 autorises,")
    add("3 niveaux les plus bas (cela MINORE les rapports).")
    add("")
    add(f"{'niveau':>6} {'x_n':>8} {'predit lin.':>13} {'predit quad.':>13} "
        f"{'OBSERVE':>11} {'ecart lin.':>11}")
    add("-" * 80)
    for r in p2:
        add(f"{r['niveau']:6d} {r['x_n']:8.4f} {r['predit_lineaire']:13.3f} "
            f"{r['predit_quadratique']:13.3f} {r['observe_m_lepton_m_e']:11.3f} "
            f"{r['ecart_lineaire']:10.1f}x")
    add("-" * 80)
    add("=> Le puits sans parametre predit 1 : %.2f : %.2f (lineaire)."
        % (p2[1]["predit_lineaire"], p2[2]["predit_lineaire"]))
    add("   L'observation donne 1 : %.2f : %.2f." % (RATIO_MU, RATIO_TAU))
    add("   Ecart sur la 3e generation : facteur %.0f." % p2[2]["ecart_lineaire"])

    # ---- P3
    add("")
    add("=" * 80)
    add("PARTIE 3 — Puits fini : un seul parametre de forme, donc un VRAI test")
    add("=" * 80)
    s3, scan3 = part3_finite_well()
    if s3:
        add(f"fenetre a 3 etats : R0 dans (5pi/2, 7pi/2)  =>  VL2 dans (61.7, 120.9)")
        add(f"{s3['n_points_3_etats']} puits balayes ; borne LACHE 6 (lin.) et 36 (quad.)")
        add("")
        add(f"  maximum REELLEMENT calcule, loi lineaire    : {s3['span_lineaire_max_atteignable']:.3f}"
            f"   (borne lache {s3['borne_theorique_lineaire']:.0f})")
        add(f"  maximum REELLEMENT calcule, loi quadratique : {s3['span_quadratique_max_atteignable']:.1f}"
            f"   (borne lache {s3['borne_theorique_quadratique']:.0f})")
        add(f"  etendue OBSERVEE (m_tau/m_e)               : {s3['span_observe']:.1f}")
        add("")
        add("=> Meme au mieux, un puits a 3 etats plafonne a %.0f (quadratique) :"
            % s3['span_quadratique_max_atteignable'])
        add("   il manque un facteur %.0f sur l'etendue observee."
            % (s3['span_observe'] / s3['span_quadratique_max_atteignable']))
        add("   Le parametre de forme est donc epuise : ce n'est pas un ajustement")
        add("   possible, c'est une impossibilite.")

    # ---- P4
    add("")
    add("=" * 80)
    add("PARTIE 4 — Bilan des parametres libres")
    add("=" * 80)
    add(f"{'ontologie':<44} {'parametres':>12}")
    add("-" * 80)
    p4 = part4_parameter_budget()
    for r in p4:
        add(f"{r['ontologie']:<44} {r['parametres']:12d}")
    add("-" * 80)
    for r in p4:
        add(f"  {r['ontologie']:<42} : {r['commentaire']}")

    # ---- Verdict
    add("")
    add("=" * 80)
    add("VERDICT")
    add("=" * 80)
    add("1. 'Lumiere confinee dans une cavite ordinaire' est REFUTE :")
    add("   une cavite de N etats a un spectre SANS TROU, donc un rapport")
    add("   m_tau/m_e = 3477 exige des milliers (ou au moins 30) leptons.")
    add("   On en observe 3. Ce n'est pas un defaut d'ajustement : c'est")
    add("   une borne independante de la forme du puits.")
    add("")
    add("2. La seule ontologie 'lumiere confinee' survivante est celle ou le")
    add("   NOMBRE de modes est fixe par la TOPOLOGIE (theoreme d'indice),")
    add("   pas par une cavite. Trois generations = invariant topologique.")
    add("   Mais alors l'ontologie ne dit RIEN des rapports de masse :")
    add("   elle explique le comptage, pas le spectre.")
    add("")
    add("3. Conclusion pour le programme : 'delier de la lumiere confinee'")
    add("   ne peut pas etre la bonne formulation. Il faut soit (a) une")
    add("   cavite par fermion (2N parametres = pire que le MS), soit")
    add("   (b) une protection topologique (qui laisse les masses inexpliquees).")
    add("   Aucune des deux ne rend le deliement plus accessible : dans (a) la")
    add("   masse est l'energie de la cavite, qu'il faut payer ; dans (b) la")
    add("   masse n'est pas dans le mode confine du tout.")

    txt = "\n".join(L)
    print(txt)

    payload = {
        "observed": {"m_mu_over_m_e": float(RATIO_MU),
                     "m_tau_over_m_e": float(RATIO_TAU)},
        "counting_theorem": p1,
        "parameter_free_well": p2,
        "finite_well_3states": s3,
        "parameter_budget": p4,
        "verdict": {
            "cavity_ontology": "refutee : spectre sans trou -> N_min leptons",
            "topological_ontology": "survit pour le comptage, muette sur les rapports",
        },
    }
    with open("ttc_confinement_modes.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    if HAS_MPL:
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))

        # (a) nombre minimal de leptons predit vs observe
        names = [r["loi"].split(" (")[0] for r in p1]
        nmins = [r["N_min_theorique"] for r in p1]
        ax[0].bar(names, nmins, color=["#3d6fa8", "#8a5fa8"])
        ax[0].axhline(3, color="crimson", ls="--", lw=2)
        ax[0].text(0.55, 3.6, "observé : 3 leptons chargés", color="crimson", fontsize=9)
        ax[0].set_yscale("log")
        ax[0].set_ylabel("nombre de leptons chargés prédit (minimum)")
        ax[0].set_title("§9.1 — Une cavité n'a pas de trou dans son spectre")
        ax[0].grid(alpha=0.3, axis="y", which="both")

        # (b) puits fini a 3 etats : etendue atteignable
        if scan3:
            vl = [s["VL2"] for s in scan3]
            sp = [s["span_quadratique"] for s in scan3]
            ax[1].plot(vl, sp, lw=2, color="#a8553d")
            ax[1].axhline(SPAN, color="crimson", ls="--", lw=2)
            ax[1].set_yscale("log")
            ax[1].set_xlabel(r"paramètre de forme du puits  $V L^2$  (unités $\hbar^2/2\mu$)")
            ax[1].set_ylabel(r"étendue atteignable  $(x_3/x_1)^2$")
            ax[1].set_title(r"§9.3 — Un puits à 3 états : plafond $\approx 9$, besoin $3477$")
            ax[1].text(vl[len(vl) // 6], 60.0, r"observé  $m_\tau/m_e = 3477$",
                       color="crimson", fontsize=9)
            ax[1].grid(alpha=0.3, which="both")

        fig.suptitle("TTC — La matière est-elle de la lumière confinée ?", fontsize=11)
        fig.tight_layout()
        fig.savefig("ttc_confinement_modes.png", dpi=150)
        print("\n[ok] ttc_confinement_modes.png écrit")


if __name__ == "__main__":
    main()
