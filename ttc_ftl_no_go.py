# -*- coding: utf-8 -*-
"""
TTC — Peut-on voyager plus vite que la lumiere ? No-go structurel
=================================================================
Accompagne TTC-deliement-bilan-energetique.md, section 10.

On teste les TROIS maillons de l'affirmation
    "delier la matiere en onde  ->  mouvement instantane  ->  via les filaments 1D"

Partie 1 : NEC. T_munu de MCW-1 construit symboliquement (sympy). On montre que
           rho + p_r est une somme de carres et rho + p_t = 0, POUR TOUTE
           configuration et TOUT potentiel U. Consequence : pas de bulle de
           warp, pas de trou de ver traversable (Raychaudhuri).
Partie 2 : metrique effective. Si elle est CONFORME a g, les cones de lumiere
           sont identiques -> aucune propagation supraluminique possible.
           Demonstration numerique de la classification causale invariante.
Partie 3 : filaments. Delai de Shapiro le long d'un filament (ordre de grandeur),
           et cas de la corde cosmique (vraiment 1D) : localement plate.
Partie 4 : etat de transit. M = 0 impose v = c exactement : un objet sans masse
           ne peut PAS etre au repos -> on ne peut ni y monter ni en descendre.
Partie 5 : ce que la TTC autorise vraiment (variation locale de G), et son cout.

Sorties : ttc_ftl_no_go.json
"""

import json
import numpy as np
import sympy as sp

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

# Constantes (SI)
C_LIGHT = 2.99792458e8
MPC = 3.0856775814913673e22
YR = 3.15576e7
G_N = 6.67430e-11


# ---------------------------------------------------------------------------
# Partie 1 — NEC symbolique
# ---------------------------------------------------------------------------
def part1_nec_symbolic():
    """T_munu = somme_f d_mu f d_nu f + g_munu L   (signature -,+,+,+, statique)
    L = -1/2 (G')^2 - 1/2 G^2 (P')^2 - 1/2 (T')^2 - U(G,T)
    """
    r = sp.symbols("r", positive=True)
    Gf = sp.Function("Gamma")(r)
    Pf = sp.Function("Phi")(r)
    Tf = sp.Function("T")(r)
    U = sp.Function("U")(Gf, Tf)

    fields = [Gf, Pf, Tf]
    # poids de chaque champ dans T_munu : Gamma -> 1, Phi -> Gamma^2, T -> 1
    weights = [sp.Integer(1), Gf ** 2, sp.Integer(1)]
    # termes de gradient dans L
    grad_terms = [sp.Rational(-1, 2) * sp.diff(Gf, r) ** 2,
                  sp.Rational(-1, 2) * Gf ** 2 * sp.diff(Pf, r) ** 2,
                  sp.Rational(-1, 2) * sp.diff(Tf, r) ** 2]
    L = sum(grad_terms) - U

    # T_00 = g_00 L = -L   (g_00 = -1, pas de derivees temporelles)
    rho = sp.simplify(-L)
    # T_rr = somme w_f (f')^2 + g_rr L ,  g_rr = 1
    p_r = sp.simplify(sum(w * sp.diff(f, r) ** 2 for w, f in zip(weights, fields)) + L)
    # T_tt / r^2 = g_tt L / r^2 , g_tt = r^2
    p_t = sp.simplify(L)

    nec_radial = sp.simplify(rho + p_r)
    nec_tang = sp.simplify(rho + p_t)

    # forme manifestement positive : somme de carres ponderee
    expected = sum(w * sp.diff(f, r) ** 2 for w, f in zip(weights, fields))

    return {
        "rho": str(rho),
        "p_radial": str(p_r),
        "p_tangentielle": str(p_t),
        "rho_plus_p_radial": str(nec_radial),
        "rho_plus_p_tangentielle": str(nec_tang),
        "somme_de_carres_attendue": str(expected),
        "identite_verifiee": bool(sp.simplify(nec_radial - expected) == 0),
        "tangentielle_nulle": bool(sp.simplify(nec_tang) == 0),
        # controle numerique sur un jeu aleatoire
        "controle_numerique_positif": _numeric_nec_check(),
    }


def _numeric_nec_check(n=20000, seed=7):
    """Verification numerique : rho + p_r >= 0 pour des gradients aleatoires."""
    rng = np.random.default_rng(seed)
    dG = rng.normal(size=n)
    Gf = np.abs(rng.normal(size=n)) * 3.0
    dP = rng.normal(size=n) * 5.0
    dT = rng.normal(size=n)
    U = rng.normal(size=n) * 1e3          # potentiel ARBITRAIRE, meme negatif
    rho = 0.5 * dG ** 2 + 0.5 * Gf ** 2 * dP ** 2 + 0.5 * dT ** 2 + U
    p_r = 0.5 * dG ** 2 + 0.5 * Gf ** 2 * dP ** 2 + 0.5 * dT ** 2 - U
    nec = rho + p_r
    return {"n_echantillons": n,
            "nec_min": float(nec.min()),
            "rho_min": float(rho.min()),
            "rho_negatif_possible": bool(rho.min() < 0),
            "nec_jamais_negatif": bool(nec.min() >= -1e-12)}


# ---------------------------------------------------------------------------
# Partie 2 — invariance conforme de la structure causale
# ---------------------------------------------------------------------------
def part2_conformal():
    """g -> Omega^2 g : la norme de TOUT vecteur est multipliee par Omega^2.
    Le signe de la norme est donc preserve => memes cones de lumiere."""
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    vecs = {
        "genre temps": np.array([2.0, 0.3, 0.0, 0.0]),
        "genre lumiere": np.array([1.0, 1.0, 0.0, 0.0]),
        "genre espace": np.array([0.2, 1.0, 0.0, 0.0]),
    }
    rows = []
    for Om2 in (1.0, 1e-6, 1e6, 1e30):
        g = Om2 * eta
        for name, v in vecs.items():
            norm = float(v @ g @ v)
            sgn = int(np.sign(norm))
            kk = np.linalg.norm(v.astype(float))
            rows.append({"Omega2": Om2, "vecteur": name,
                         "norme": norm, "signe": sgn})
    # coherence par vecteur
    same = all(len({r["signe"] for r in rows if r["vecteur"] == k}) == 1
               for k in vecs)
    return {"table": rows, "classification_inchangee": bool(same)}


# ---------------------------------------------------------------------------
# Partie 3 — filaments
# ---------------------------------------------------------------------------
def part3_filaments():
    """Delai de Shapiro le long d'un filament, et cas de la corde cosmique."""
    rows = []
    for L_Mpc, sigma_kms in ((3.0, 200.0), (10.0, 300.0), (30.0, 500.0)):
        L = L_Mpc * MPC
        sig = sigma_kms * 1e3
        phi = sig ** 2                       # |Phi| ~ sigma^2 (viriel)
        dt = 2.0 * phi * L / C_LIGHT ** 3    # delai de Shapiro
        t_vac = L / C_LIGHT
        rows.append({
            "L_Mpc": L_Mpc, "sigma_kms": sigma_kms,
            "phi_over_c2": float(phi / C_LIGHT ** 2),
            "delay_s": float(dt),
            "delay_yr": float(dt / YR),
            "temps_vide_yr": float(t_vac / YR),
            "delta_relatif": float(dt / t_vac),
            "sens": "RETARD",
        })
    # corde cosmique : localement plate, seulement un angle deficitaire
    Gmu = 1e-7                                # G mu typique (bornes PTA ~1e-11)
    rows_string = [{"Gmu": Gmu,
                    "deficit_angle_rad": float(8 * np.pi * Gmu),
                    "retard": "nul (metrique localement minkowskienne)",
                    "raccourci": "nul"}]
    return {"filaments": rows, "corde_cosmique": rows_string}


# ---------------------------------------------------------------------------
# Partie 4 — etat de transit
# ---------------------------------------------------------------------------
def part4_transit():
    """M = m0/gamma. Atteindre M=0 exige v=c exactement ; un objet sans masse
    ne peut pas etre au repos dans un referentiel, donc n'est pas un vehicule."""
    rows = []
    for Mrel in (1.0, 0.5, 0.1, 1e-2, 1e-4, 1e-8, 0.0):
        Mrel = max(Mrel, 0.0)
        gamma = 1.0 / Mrel if Mrel > 0 else np.inf
        beta = np.sqrt(max(1.0 - 1.0 / gamma ** 2, 0.0)) if np.isfinite(gamma) else 1.0
        # temps de traversee d'une distance d, en unites d/c
        if beta <= 0:
            t_over = None                      # au repos : temps infini
        else:
            t_over = float(1.0 / beta)
        rows.append({"M_over_m0": Mrel,
                     "gamma": float(gamma) if np.isfinite(gamma) else None,
                     "beta_v_over_c": float(beta),
                     "t_over_d_c": t_over})
    return {"table": rows,
            "commentaire": ("t/(d/c) >= 1 toujours ; la borne est atteinte "
                            "seulement a M=0, ou l'objet est sans masse et "
                            "donc ne peut pas etre au repos : pas un vehicule.")}


# ---------------------------------------------------------------------------
# Partie 5 — ce que la TTC autorise : variation locale de G
# ---------------------------------------------------------------------------
def part5_local_G():
    """G proportionnel a 1/v_Gamma^2 (WP 3.2). Changer Gamma localement change G.
    Cout energetique : Delta U = alpha/4 [(Gamma^2-v^2)^2] ; a Gamma=v(1+eps),
    Delta U ~ alpha v^4 eps^2  -> echelle de Planck si v ~ M_Pl, alpha ~ 1."""
    rows = []
    for eps in (1e-6, 1e-3, 0.1, 1.0):
        dG_rel = -2.0 * eps + eps ** 2       # (1+eps)^-2 - 1
        rows.append({"epsilon": eps,
                     "variation_relative_de_G": float(dG_rel)})
    # cout : en unites de v_Gamma^4
    cost = [{"epsilon": eps,
             "DeltaU_over_alpha_v4": float(0.25 * ((1 + eps) ** 2 - 1) ** 2)}
            for eps in (1e-6, 1e-3, 0.1, 1.0)]
    return {"variation_de_G": rows, "cout_en_unites_alpha_vGamma4": cost}


def main():
    L = []
    add = L.append

    # ---- P1
    add("=" * 80)
    add("PARTIE 1 — Condition d'energie nulle (NEC) : verification symbolique")
    add("=" * 80)
    p1 = part1_nec_symbolic()
    add("Tenseur de MCW-1, configuration statique arbitraire Gamma(r), Phi(r), T(r) :")
    add("")
    add("  rho              = " + p1["rho"])
    add("  p_radial         = " + p1["p_radial"])
    add("  p_tangentielle   = " + p1["p_tangentielle"])
    add("-" * 80)
    add("  rho + p_radial      = " + p1["rho_plus_p_radial"])
    add("  rho + p_tangentielle= " + p1["rho_plus_p_tangentielle"])
    add("-" * 80)
    add(f"  identite rho+p_r = somme de carres : {p1['identite_verifiee']}")
    add(f"  rho + p_t = 0 exactement           : {p1['tangentielle_nulle']}")
    nc = p1["controle_numerique_positif"]
    add(f"  controle numerique ({nc['n_echantillons']} tirages, U arbitraire dont negatif) :")
    add(f"    rho minimal = {nc['rho_min']:.3e}   (rho < 0 possible : {nc['rho_negatif_possible']})")
    add(f"    (rho+p_r) minimal = {nc['nec_min']:.3e}   (jamais negatif : {nc['nec_jamais_negatif']})")
    add("")
    add("=> La NEC est PROTEGEE par la structure cinetique (somme de carres),")
    add("   independamment du potentiel U. Une somme de scalaires canoniques")
    add("   ne peut pas violer la NEC. Consequence (Raychaudhuri) :")
    add("   - pas de bulle de type Alcubierre ;")
    add("   - pas de trou de ver traversable.")
    add("   Note : rho peut etre negatif si U < 0, mais la NEC porte sur rho+p,")
    add("   pas sur rho. Une densite negative ne suffit pas.")

    # ---- P2
    add("")
    add("=" * 80)
    add("PARTIE 2 — La metrique effective est CONFORME : les cones sont identiques")
    add("=" * 80)
    add("WP ligne 51 : g_eff = f(Gamma^2 - 2 lambda T) * g  -> facteur conforme.")
    add("Sous g -> Omega^2 g, la norme de tout vecteur est multipliee par Omega^2 :")
    add("le SIGNE est preserve, donc la classification causale aussi.")
    add("")
    p2 = part2_conformal()
    add(f"{'Omega^2':>10} {'vecteur':>16} {'norme':>16} {'signe':>7}")
    add("-" * 80)
    for r in p2["table"]:
        add(f"{r['Omega2']:10.0e} {r['vecteur']:>16} {r['norme']:16.4e} {r['signe']:7d}")
    add("-" * 80)
    add(f"  classification inchangee pour Omega^2 de 1e-6 a 1e30 : "
        f"{p2['classification_inchangee']}")
    add("")
    add("=> Une metrique conforme ne peut PAS deplacer les cones de lumiere.")
    add("   Aucune valeur de Gamma et de T ne rend la lumiere plus rapide.")
    add("   Seule une partie DISFORMEE (proportionnelle a d_mu Gamma d_nu Gamma)")
    add("   changerait les cones -- elle n'est pas ecrite dans MCW-1.")

    # ---- P3
    add("")
    add("=" * 80)
    add("PARTIE 3 — Les filaments : lignes de RETARD, pas des raccourcis")
    add("=" * 80)
    p3 = part3_filaments()
    add(f"{'L (Mpc)':>8} {'sigma':>7} {'|Phi|/c^2':>11} {'retard':>12} "
        f"{'trajet vide':>14} {'relatif':>10}")
    add("-" * 80)
    for r in p3["filaments"]:
        add(f"{r['L_Mpc']:8.0f} {r['sigma_kms']:5.0f}km/s {r['phi_over_c2']:11.2e} "
            f"{r['delay_yr']:9.1f} ans {r['temps_vide_yr']:11.3e} ans "
            f"{r['delta_relatif']:10.2e}")
    add("-" * 80)
    add("=> Le filament est un PUITS de potentiel : il RETARDE (Shapiro),")
    add("   il n'avance pas. Effet relatif ~ 2|Phi|/c^2 ~ 2e-6 : minuscule,")
    add("   et de signe defavorable.")
    add("")
    cs = p3["corde_cosmique"][0]
    add("Corde cosmique (le seul objet VRAIMENT 1D) :")
    add(f"  metrique localement minkowskienne, angle deficitaire = {cs['deficit_angle_rad']:.2e} rad")
    add("  retard : " + cs["retard"])
    add("  raccourci : " + cs["raccourci"])
    add("=> Meme un defaut topologique 1D ne raccourcit RIEN. Il ne fait que")
    add("   lentiller. L'intuition 'filament = couloir' est geometriquement fausse.")

    # ---- P4
    add("")
    add("=" * 80)
    add("PARTIE 4 — L'etat de transit n'est pas un vehicule")
    add("=" * 80)
    p4 = part4_transit()
    add(f"{'M/m0':>10} {'gamma':>14} {'v/c':>12} {'t/(d/c)':>12}")
    add("-" * 80)
    for r in p4["table"]:
        g_ = "infini" if r["gamma"] is None else f"{r['gamma']:.3e}"
        if r["t_over_d_c"] is None:
            t_ = "infini (repos)"
        else:
            t_ = f"{r['t_over_d_c']:.6f}"
        add(f"{r['M_over_m0']:10.0e} {g_:>14} {r['beta_v_over_c']:12.9f} {t_:>14}")
    add("-" * 80)
    add("=> Le temps de traversee ne descend JAMAIS sous d/c.")
    add("   A M = m0 (au repos) il est INFINI. A M = 0 il vaut exactement d/c.")
    add("   Et a M=0 la vitesse est exactement c : l'objet n'a plus de")
    add("   referentiel au repos, donc on ne peut ni y monter ni en descendre.")
    add("   Un vaisseau doit etre massif a l'arret ET a l'arrivee :")
    add("   ce sont precisement les deux etats ou la vitesse est < c.")

    # ---- P5
    add("")
    add("=" * 80)
    add("PARTIE 5 — Ce que la TTC autorise vraiment : changer G localement")
    add("=" * 80)
    add("WP 3.2 : G proportionnel a 1/v_Gamma^2. Donc agir sur Gamma agit sur G.")
    add("")
    p5 = part5_local_G()
    add(f"{'epsilon (Gamma/v-1)':>22} {'variation de G':>18} {'cout / (alpha v^4)':>22}")
    add("-" * 80)
    for a, b in zip(p5["variation_de_G"], p5["cout_en_unites_alpha_vGamma4"]):
        add(f"{a['epsilon']:22.0e} {100 * a['variation_relative_de_G']:17.3e}% "
            f"{b['DeltaU_over_alpha_v4']:22.3e}")
    add("-" * 80)
    add("=> C'est la SEULE ingenierie que la TTC ouvre : une modification locale")
    add("   de G. Elle ne raccourcit pas les distances ; elle change la gravite.")
    add("   Cout : alpha v_Gamma^4. Avec v_Gamma ~ M_Pl et alpha ~ 1, c'est")
    add("   l'echelle de Planck -- hors d'atteinte par des ordres gigantesques.")

    # ---- Verdict
    add("")
    add("=" * 80)
    add("VERDICT — les trois maillons")
    add("=" * 80)
    add("1. 'Delier la matiere en onde'       : REFUTE  (§8 : la masse n'est pas")
    add("   dans l'enroulement de Phi ; §9 : aucune cavite ne reproduit le spectre)")
    add("2. 'L'onde va donc instantanement'   : REFUTE  (M=0 <=> v=c exactement ;")
    add("   t >= d/c toujours ; et la metrique effective est conforme, donc les")
    add("   cones de lumiere sont ceux de la RG ordinaire)")
    add("3. 'Emprunter les filaments 1D'      : REFUTE  (un filament retarde ;")
    add("   une corde cosmique est localement plate : zero raccourci)")
    add("")
    add("Blocage structurel independant des deux premiers :")
    add("   MCW-1 est une somme de scalaires canoniques minimaux -> la NEC est")
    add("   satisfaite identiquement -> aucun warp, aucun trou de ver.")
    add("   Ce n'est pas une limite technologique, c'est une propriete du")
    add("   Lagrangien. Il faudrait en sortir (cinetique non canonique, couplage")
    add("   disforme) pour rouvrir la question -- et ce serait une AUTRE theorie.")

    txt = "\n".join(L)
    print(txt)

    payload = {"part1_nec": p1, "part2_conformal": p2, "part3_filaments": p3,
               "part4_transit": p4, "part5_local_G": p5,
               "verdict": {"delier": "refute (§8, §9)",
                           "instantané": "refute (M=0 <=> v=c ; metrique conforme)",
                           "filaments_1D": "refute (Shapiro ; corde localement plate)",
                           "blocage_structurel": "NEC identiquement satisfaite en MCW-1"}}
    with open("ttc_ftl_no_go.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    print("\n[ok] ttc_ftl_no_go.json écrit")


if __name__ == "__main__":
    main()
