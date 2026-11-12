# -*- coding: utf-8 -*-
"""
TTC — Test discriminant entre les deux mecanismes de masse (A vs B)
===================================================================
Accompagne TTC-deliement-bilan-energetique.md, section 8.

Mecanisme A : la masse EST l'energie du noeud d'enroulement
              m c^2 = E_noeud = 2*pi*n^2*v_Gamma^2*R      (resultat du script
              ttc_deliement_barrier.py, terme de gradient dominant)

Mecanisme B : la masse est un couplage de Yukawa du fermion a Gamma
              (TTC-White-Paper.md, section 5, ou la derivation est declaree
              "non derivee")

Le test porte sur une unique question : le mecanisme A fournit-il une masse
PREDITE, ou seulement une masse REGLEE ?

Demonstration centrale (Partie 1) : la seule auto-consistance possible
    R = hbar/(m c)   (taille Compton, la seule echelle disponible)
injectee dans  m c^2 = 2*pi*n^2*v_Gamma^2*R  donne

    m^2 = 2*pi*n^2*v_Gamma^2    =>    m = sqrt(2*pi)*|n|*v_Gamma

c'est-a-dire une masse determinee a 100 % par |n| : aucun parametre continu,
donc aucune liberte pour ajuster le spectre. Les seules masses accessibles
sont celles d'un noeud unique (|n|=1), et les rapports de masse doivent etre
des RAPPORTS D'ENTIERS.

Sorties : ttc_mass_mechanism_test.json, ttc_mass_mechanism_test.png
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
# Masses observees (PDG, MeV). Charges de couleur moyennaees pour les quarks.
# ----------------------------------------------------------------------------
FERMIONS = [
    ("e",           0.51099895000),
    ("mu",          105.6583755),
    ("tau",         1776.86),
    ("u (MSbar 2 GeV)",      2.16),
    ("d (MSbar 2 GeV)",      4.67),
    ("s (MSbar 2 GeV)",     93.4),
    ("c (MSbar 2 GeV)",   1270.0),
    ("b (MSbar 2 GeV)",   4180.0),
    ("t (MSbar)",       172690.0),
]


def part1_selfconsistent_mass(v_gamma=1.0, n_max=5):
    """m = sqrt(2 pi) |n| v_Gamma : le spectre entier tient dans |n|."""
    return [{"n": int(n),
             "m_over_vGamma": float(np.sqrt(2.0 * np.pi) * abs(n)),
             "m_over_m1": float(abs(n))} for n in range(1, n_max + 1)]


def part2_implied_vgamma(fermions):
    """Si le mecanisme A doit rendre compte de CHAQUE masse, quel v_Gamma faut-il ?

    m = sqrt(2 pi) |n| v_Gamma , |n| = 1 (noeud elementaire)
    => v_Gamma = m / sqrt(2 pi)
    """
    out = []
    for name, m in fermions:
        out.append({"fermion": name,
                    "m_MeV": m,
                    "v_gamma_required_MeV": float(m / np.sqrt(2.0 * np.pi))})
    vals = np.array([r["v_gamma_required_MeV"] for r in out])
    return out, float(vals.max() / vals.min())


def part3_r_unconstrained():
    """Sous A, la masse est E_noeud(R)/c^2 : elle suit R lineairement.

    R n'est fixe par AUCUNE equation du modele (c'est le rayon exterieur du
    monopole global). On balaye 12 decades de R et on regarde la masse.
    """
    v_gamma = 1.0
    rows = []
    for R in [1e-3, 1.0, 1e3, 1e6, 1e9]:
        m = 2.0 * np.pi * v_gamma ** 2 * R      # n = 1
        rows.append({"R": R, "m_over_vgamma": float(m)})
    masses = [r["m_over_vgamma"] for r in rows]
    return rows, float(max(masses) / min(masses))


def part4_ratio_test(fermions):
    """Test des rapports entiers : si m / m_e doit etre entier, quel ecart ?"""
    m_e = dict(fermions)["e"]
    rows = []
    for name, m in fermions:
        r = m / m_e
        k = round(r)
        rows.append({"fermion": name,
                     "ratio_to_e": float(r),
                     "nearest_int": int(k),
                     "rel_dev_if_int": float(abs(r - k) / r) if k else None})
    return rows


def main():
    L = []
    add = L.append

    # ------------------------------------------------------------------ P1
    add("=" * 78)
    add("PARTIE 1 — Auto-consistance du mecanisme A : la masse est-elle PREDITE ?")
    add("=" * 78)
    add("m c^2 = 2 pi n^2 v_G^2 R   et   R = hbar/(m c)")
    add("  =>  m^2 = 2 pi n^2 v_G^2   =>   m = sqrt(2 pi) |n| v_G")
    add("")
    add(f"{'|n|':>4} {'m/v_Gamma':>12} {'m/m_1':>8}")
    add("-" * 78)
    spec = part1_selfconsistent_mass()
    for r in spec:
        add(f"{r['n']:4d} {r['m_over_vGamma']:12.5f} {r['m_over_m1']:8.2f}")
    add("")
    add("=> Aucun parametre continu : le spectre est entierement determine par |n|.")
    add("   Les rapports de masse ne peuvent etre que des rapports d'ENTIERS.")
    add("   C'est une prediction, donc une prise pour la falsification.")

    # ------------------------------------------------------------------ P2
    add("")
    add("=" * 78)
    add("PARTIE 2 — v_Gamma exige par le mecanisme A, fermion par fermion")
    add("=" * 78)
    add("Si le noeud EST la particule, v_Gamma = m / sqrt(2 pi) doit etre unique.")
    add("")
    add(f"{'fermion':>20} {'m (MeV)':>14} {'v_Gamma requis (MeV)':>22}")
    add("-" * 78)
    vrows, spread = part2_implied_vgamma(FERMIONS)
    for r in vrows:
        add(f"{r['fermion']:>20} {r['m_MeV']:14.5g} {r['v_gamma_required_MeV']:22.5g}")
    add("-" * 78)
    add(f"  etalement max/min de v_Gamma exige : {spread:.3e}")
    add("")
    add("=> Un champ Gamma unique ne peut pas prendre ces valeurs simultanement.")
    add("   Le mecanisme A est REFUTE comme origine du spectre de masse.")

    # ------------------------------------------------------------------ P3
    add("")
    add("=" * 78)
    add("PARTIE 3 — Sous A, la masse n'est pas fixee : elle suit le rayon R")
    add("=" * 78)
    rrows, dyn = part3_r_unconstrained()
    add(f"{'R (unites 1/v_Gamma)':>22} {'m/v_Gamma':>16}")
    add("-" * 78)
    for r in rrows:
        add(f"{r['R']:22.3e} {r['m_over_vgamma']:16.5e}")
    add("-" * 78)
    add(f"  masse balayee sur 12 decades de R : facteur {dyn:.3e}")
    add("")
    add("=> R est le rayon exterieur du monopole GLOBAL : aucune equation de MCW-1")
    add("   ne le fixe. Le mecanisme A ne predit donc aucune masse.")


    # ------------------------------------------------------------------ P4
    add("")
    add("=" * 78)
    add("PARTIE 4 — Test des rapports entiers (corollaire falsifiable de A)")
    add("=" * 78)
    add(f"{'fermion':>20} {'m/m_e':>16} {'entier le plus proche':>22} {'ecart':>10}")
    add("-" * 78)
    rr = part4_ratio_test(FERMIONS)
    for r in rr:
        dev = "" if r["rel_dev_if_int"] is None else f"{100 * r['rel_dev_if_int']:9.3f}%"
        add(f"{r['fermion']:>20} {r['ratio_to_e']:16.6g} {r['nearest_int']:22d} {dev:>10}")
    add("")
    add("=> Test faible isolement (les entiers sont denses aux grands rapports),")
    add("   mais il est inutile : la Partie 1 suffit, et la Partie 2 tranche.")

    # ------------------------------------------------------------------ P5
    add("")
    add("=" * 78)
    add("VERDICT")
    add("=" * 78)
    add("A (masse = energie du noeud) : REFUTE comme mecanisme du spectre.")
    add("   - auto-consistance  => m = sqrt(2 pi)|n| v_Gamma (aucun parametre libre)")
    add("   - v_Gamma exige     => etale de %.1e entre electron et top" % spread)
    add("   - R non fixe        => masse arbitraire, donc non predictive")
    add("")
    add("B (masse = Yukawa a Gamma) : reste le seul mecanisme interne viable.")
    add("   CONSEQUENCE : denouer Phi ne change RIEN a la masse du fermion.")
    add("   Le fermion reste massif ; il n'y a pas de 'soliton de transit'")
    add("   sans masse a trouver. La premisse du deliement tombe, non par")
    add("   barrierre energetique, mais par ABSENCE DE MECANISME.")
    add("")
    add("C (troisieme voie, a instruire) : masse = VEV d'un champ distinct,")
    add("   le noeud etant un soliton SEPARE. Alors le deliement est une")
    add("   affirmation sur le soliton seul, et la masse n'est pas concernee.")
    add("   C'est la seule formulation ou le programme garde un sens physique.")

    txt = "\n".join(L)
    print(txt)

    payload = {
        "monopole_spectrum": spec,
        "vgamma_required": vrows,
        "vgamma_spread_max_over_min": spread,
        "mass_vs_R": rrows,
        "mass_dynamic_range_over_12_decades_R": dyn,
        "integer_ratio_test": rr,
        "verdict": {
            "A": "refute comme mecanisme du spectre de masse",
            "B": "seul mecanisme interne viable ; le deliement ne change pas la masse",
            "C": "troisieme voie a instruire : soliton separe de la masse",
        },
    }
    with open("ttc_mass_mechanism_test.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)

    if HAS_MPL:
        fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))

        names = [r["fermion"].split(" ")[0] for r in vrows]
        vals = [r["v_gamma_required_MeV"] for r in vrows]
        ax[0].barh(names, vals, color="#3d6fa8")
        ax[0].set_xscale("log")
        ax[0].set_xlabel(r"$v_\Gamma$ requis par le mécanisme A  (MeV)")
        ax[0].set_title(r"Mécanisme A : un seul $v_\Gamma$ est impossible")
        ax[0].grid(alpha=0.3, axis="x", which="both")
        ax[0].invert_yaxis()
        ax[0].axvline(374.3, color="crimson", ls="--", lw=1.5)
        ax[0].text(374.3, 0.3, " $m_p/\\sqrt{2\\pi}$", color="crimson", fontsize=8)

        R = np.logspace(-4, 12, 200)
        ax[1].loglog(R, 2 * np.pi * R, lw=2, color="#a8553d")
        ax[1].set_xlabel(r"rayon extérieur du monopôle $R$  (unités $1/v_\Gamma$)")
        ax[1].set_ylabel(r"$m/v_\Gamma = 2\pi R$")
        ax[1].set_title(r"Mécanisme A : la masse suit $R$, que rien ne fixe")
        ax[1].grid(alpha=0.3, which="both")

        fig.suptitle("TTC — A vs B : d'où vient la masse ?", fontsize=11)
        fig.tight_layout()
        fig.savefig("ttc_mass_mechanism_test.png", dpi=150)
        print("\n[ok] ttc_mass_mechanism_test.png écrit")


if __name__ == "__main__":
    main()
