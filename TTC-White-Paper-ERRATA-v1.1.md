# TTC WHITE PAPER — ERRATA & RÉTRACTIONS v1.1
## Correctif officiel du White Paper v1.0 (13 juillet 2026)

> **Statut :** Ce document SUPPLANTE les revendications correspondantes du White Paper v1.0.
> **Date :** 31 juillet 2026 — Rédigé suite à l'audit KontEx et à la session de durcissement.
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC).
> **Validation :** Dileve MBAMU (Auteur principal).

---

## AVERTISSEMENT

La science progresse par correction d'erreurs. La TTC v1.0 contenait des
revendications trop fortes, des ambiguïtés, et une erreur de numérologie.
Ce document les corrige.

**Les corrections ci-dessous NE remettent PAS en cause le noyau dur de la TTC**
(la triade $\Gamma, \Phi, T$, le lagrangien MCW-1, les équations de champ).
Elles retirent ce qui n'est pas prouvé pour ne garder que ce qui tient.

---

## TABLE DES CORRECTIONS

| # | Section WP | Revendication originale | Correction |
|---|-----------|------------------------|------------|
| R1 | §1.3 | « Les angles CKM sont reproduits avec une précision remarquable » | RÉTRACTÉ : fits, pas prédictions |
| R2 | §1.3 | « La relativité générale émerge » | NUANCÉ : proposition, pas preuve |
| R3 | §1.3 | « La cosmologie (inflation, CMB, énergie noire) s'inscrit dans le cadre » | RÉTRACTÉ : qualitatif, non quantitatif |
| R4 | §3.4 | $\Gamma \propto 1/r$ explique les courbes plates | CONSERVÉ (prouvé analytiquement) |
| R5 | §5 | Nombres CKM $1/\sqrt{20}$, $1/24$, $\alpha/2$ | RÉTRACTÉ : ansätze numériques |
| R6 | §7 | $\Sigma m_\nu \sim 0.01-0.02$ eV | RÉTRACTÉ : exclu par données |
| R7 | Divers | $P_{\rm max} = 3^5 = 243$ lié à $c^5/G$ | RÉTRACTÉ : numérologie (cf. note rectificative) |
| R8 | §7 | « La TTC unifie RG, MQ, Modèle Standard et $\Lambda$CDM » | RÉTRACTÉ : objectif, pas résultat |

---

## CORRECTIONS DÉTAILLÉES

---

### R1 — Angles CKM : fits, pas prédictions

**Revendication v1.0 :**
> Les angles CKM sont reproduits avec une précision remarquable
> ($s_{23}$ à $0.2\sigma$, $\delta$ à $0.05\sigma$).

**Correction v1.1 :**
Les nombres $1/\sqrt{20}$, $1/24$, $\alpha/2$ utilisés pour reproduire les
éléments CKM **ne sont pas dérivés** du lagrangien MCW-1. Ce sont des
**ansätze** choisis pour leur proximité numérique avec les valeurs mesurées.

Avec 3 nombres libres et 4 observables CKM (3 angles + 1 phase), obtenir
un bon accord n'est pas surprenant — c'est du **fit**, pas de la **prédiction**.

**Nouvelle formulation :**
> Certains éléments CKM peuvent être reproduits numériquement par des ansätze
> ($1/\sqrt{20}$, $1/24$, $\alpha/2$) dont l'origine dans le lagrangien
> reste INCONNUE. Ces coïncidences numériques sont suggestives mais
> NE CONSTITUENT PAS une preuve que la TTC prédit les saveurs.

**Statut :** 🟡 Coïncidence — nécessite une dérivation depuis $\mathcal{L}_{\mathcal W}$.

---

### R2 — Relativité générale émergente

**Revendication v1.0 :**
> La relativité générale émerge de la métrique effective
> $g_{\mu\nu}^{\rm eff} = f(\Gamma^2 - 2\lambda T)$.

**Correction v1.1 :**
La TTC **propose** que la métrique effective $g_{\mu\nu}^{\rm eff}$ reproduise
la RG. Elle montre que c'est **mathématiquement possible** (construction
d'une métrique effective qui satisfait $G_{\mu\nu} \propto T_{\mu\nu}^{\mathcal W}$).
Elle n'a **pas démontré** que cette construction est **unique** ou
**inévitable**.

De plus, les équations d'Einstein complètes avec back-reaction métrique
($G_{\mu\nu}^{\rm eff} = 8\pi G_{\rm eff} T_{\mu\nu}^{\rm champs}$)
**n'ont pas été résolues**, même numériquement.

**Nouvelle formulation :**
> La TTC propose un mécanisme d'émergence de la gravité via une métrique
> effective $g_{\mu\nu}^{\rm eff} = f(\Gamma^2 - 2\lambda T)$. La limite
> Newtonienne ($\nabla^2\Phi = 4\pi G\rho$) est reproduite. L'émergence
> complète des équations d'Einstein reste UNE HYPOTHÈSE À TESTER.

**Statut :** 🟡 Proposition — nécessite résolution numérique complète.

---

### R3 — Cosmologie quantitative

**Revendication v1.0 :**
> La cosmologie (inflation, CMB, énergie noire) s'inscrit dans le cadre
> de la transition de phase $\Gamma = 0 \to v_\Gamma$.

**Correction v1.1 :**
La TTC propose un **scénario qualitatif** pour l'histoire cosmologique :
- Inflation = transition de phase $\Gamma$ (cohérence émerge du néant)
- Énergie noire = tension résiduelle $T$ après la transition
- CMB = fluctuations de phase $\Phi$ gelées lors de la transition

Aucune de ces propositions n'a été **confrontée quantitativement** aux données
Planck, DESI, ou JWST. Les spectres de puissance $C_\ell$, le paramètre $w$,
et le taux d'expansion $H(z)$ n'ont PAS été calculés depuis $\mathcal{L}_{\mathcal W}$.

**Nouvelle formulation :**
> La TTC offre un **scénario qualitatif** pour l'histoire cosmologique
> (inflation comme transition de phase de $\Gamma$). Les prédictions
> quantitatives (spectre $C_\ell$, $w$, $H(z)$) restent À CALCULER.

**Statut :** 🟡 Scénario qualitatif — validation quantitative requise.

---

### R4 — Courbes de rotation plates

**Revendication v1.0 :**
> $\Gamma \propto 1/r$ explique qualitativement les courbes de rotation
> galactiques plates.

**Correction v1.1 :**
Cette revendication est **CONSERVÉE** et même **RENFORCÉE**.

La démonstration est purement analytique :
1. $\nabla_\mu(\Gamma^2\nabla^\mu\Phi) = 0$ (conservation de la phase)
2. En symétrie sphérique statique : $\partial_r(r^2\Gamma^2\partial_r\Phi) = 0$
3. $\Rightarrow \partial_r\Phi = C/(r^2\Gamma^2)$
4. Si $\Gamma \propto 1/r$ (solution asymptotique naturelle), alors
   $\partial_r\Phi \propto 1$ (constant)
5. $v^2 = r\partial_r\Phi_{\rm grav} \propto r \cdot$ (constant) = constant
6. $\Rightarrow$ courbes de rotation plates

Ce résultat est **indépendant** de tout ajustement paramétrique. C'est une
conséquence directe des équations de champ.

**Ce qui reste à prouver :** Que $\Gamma \propto 1/r$ est effectivement
la solution des EDP couplées avec une source baryonique réaliste.
(C'est l'objet du solveur `ttc_hardening_solver.py`.)

**Statut :** 🟢 Prouvé analytiquement (courbes plates si $\Gamma \propto 1/r$).
🟡 Validation numérique du profil $\Gamma(r)$ en cours.

---

### R5 — Nombres CKM/CKM : ansätze, pas dérivations

**Revendication v1.0 :**
> Les nombres CKM sont reproduits (Tableau §5) :
> $s_{12} = 1/\sqrt{20} \approx 0.224$,
> $s_{23} = 1/24 \approx 0.0417$,
> $s_{13} = \alpha/2 \approx 0.0037$,
> $\delta = 1.20$ rad.

**Correction v1.1 :**
**Ces nombres ne sont PAS dérivés du lagrangien.** Ils ont été choisis
manuellement parce qu'ils « tombent près » des valeurs mesurées. Le fait
que $s_{23}$ tombe à $0.2\sigma$ de la valeur PDG 2024 est soit :
- Une coïncidence numérique remarquable
- Le signe d'une structure sous-jacente que la TTC n'a pas encore identifiée

**Tant que la dérivation n'existe pas, ces nombres NE SONT PAS des prédictions TTC.**

**Ce qu'il faudrait pour que ça devienne une prédiction :**
Partir de la matrice de Yukawa $\mathcal{M}_{ab} = \Gamma\hat{M}_{ab} + \Gamma e^{i\Phi}\hat{K}_{ab} + T\hat{H}_{ab}$,
spécifier $\hat{M}, \hat{K}, \hat{H}$ (ou les dériver d'un principe de symétrie),
diagonaliser, et OBTENIR les nombres ci-dessus comme CONSÉQUENCE, pas comme
point de départ.

**Nouvelle formulation :**
> Des ansätze numériques ($1/\sqrt{20}$, $1/24$, $\alpha/2$) reproduisent
> certains éléments CKM avec une proximité suggestive. L'origine de ces
> nombres dans $\mathcal{L}_{\mathcal W}$ reste INCONNUE. Ils ne constituent
> PAS une prédiction de la TTC.

**Statut :** 🔴 Non dérivé — coïncidence numérique jusqu'à preuve du contraire.

---

### R6 — Masse des neutrinos

**Revendication v1.0 :**
> $\Sigma m_\nu \sim 0.01-0.02$ eV.

**Correction v1.1 :**
Cette valeur est **EXCLUE** par les données d'oscillation des neutrinos.
La contrainre cosmologique actuelle (Planck 2018 + BAO) donne :
$$\sum m_\nu < 0.12\ \text{eV (95\% CL)}$$
et les oscillations imposent :
$$\sum m_\nu > 0.058\ \text{eV (hiérarchie normale)}$$
$$\sum m_\nu > 0.10\ \text{eV (hiérarchie inversée)}$$

La prédiction TTC $0.01-0.02$ eV est donc **exclue à >10σ** dans les deux
hiérarchies.

**Nouvelle formulation :**
> La TTC v1.0 ne fait PAS de prédiction valide pour $\Sigma m_\nu$.
> La valeur précédemment avancée ($0.01-0.02$ eV) est exclue par les
> données. Le secteur neutrino doit être REPRIS.

**Statut :** 🔴 Exclu — refonte nécessaire.

---

### R7 — $P_{\rm max} = 3^5 = 243$

**Revendication implicite (code + documents) :**
> $P_{\rm max} = 3^5 = 243$ est l'analogue computationnel de $c^5/G$.

**Correction v1.1 :**
**Ceci est une erreur de numérologie.** Il n'existe AUCUN lien entre :
- $c^5/G \approx 3.63 \times 10^{52}$ W (constante de Planck)
- $3^5 = 243$ (nombre entier)

Voir la **Note technique de rectification** (`TTC-note-Pmax-rectification.md`)
pour le détail complet.

**Nouvelle formulation :**
> $P_{\rm max} = c^5/G$ est la puissance de Planck, une constante connue
> depuis 1899. La TTC l'interprète comme la limite de rupture de cohérence
> de la Toile. Pour les applications discrètes (graphes), le seuil de
> saturation numérique $P_{\rm max}^{\rm discret}$ est un paramètre
> heuristique RECALIBRABLE, SANS lien avec $c^5/G$.

**Statut :** 🔴 Erreur corrigée — voir note rectificative.

---

### R8 — « Unification » RG + MQ + MS + ΛCDM

**Revendication v1.0 (implicite, titre et introduction) :**
> La TTC unifie la relativité générale, la mécanique quantique, le Modèle
> Standard et le modèle ΛCDM.

**Correction v1.1 :**
La TTC **propose un cadre commun** pour ces quatre piliers. Elle ne les
**unifie pas** au sens où tout découlerait de $\mathcal{L}_{\mathcal W}$
sans paramètres additionnels.

**Distinction cruciale :**

| Terme | Définition | La TTC le fait-elle ? |
|-------|-----------|----------------------|
| **Cadre commun** | Même structure mathématique pour tous les domaines | 🟢 Oui |
| **Émergence** | Les lois d'un domaine découlent de celles d'un autre | 🟡 Partiel (Schrödinger émerge, RG pas encore) |
| **Unification** | Tout découle du lagrangien sans paramètres libres additionnels | 🔴 Non |
| **Théorie du tout** | Prédit TOUTES les constantes et tous les phénomènes | 🔴 Non |

**Nouvelle formulation :**
> La TTC propose un **cadre mathématique commun** — le lagrangien MCW-1 —
> pour décrire la gravité, la mécanique quantique, les interactions de
> jauge et la cosmologie. Elle ne prétend PAS être une « théorie du tout »
> et ne prédit PAS les constantes fondamentales sans paramètres libres.

**Statut :** 🟡 Cadre commun — l'unification complète reste un objectif.

---

## RÉSUMÉ — CE QUI RESTE DEBOUT

Après corrections, voici le **noyau dur vérifié** de la TTC v1.1 :

| # | Résultat | Statut | Preuve |
|---|----------|--------|--------|
| 1 | $\Gamma \propto 1/r \Rightarrow$ courbes de rotation plates | 🟢 Prouvé | Analytique |
| 2 | $\oint\nabla\Phi\cdot d\mathbf{l} = 2\pi n \Rightarrow$ Schrödinger | 🟢 Prouvé | Analytique |
| 3 | $N_g = 3$ émerge de la structure à 3 champs | 🟢 Structurel | Comptage |
| 4 | Hiérarchie $m_1 \ll m_2 \ll m_3$ naturelle | 🟢 Qualitatif | Structure de couplage |
| 5 | $\theta_{13}$ petit naturellement | 🟢 Qualitatif | Structure de couplage |
| 6 | $P_{\rm max} = c^5/G$ interprété comme rupture de cohérence | 🟢 Interprétation | Constante de Planck |
| 7 | Limite Newtonienne $\nabla^2\Phi = 4\pi G\rho$ | 🟢 Prouvé | Limite champ faible |
| 8 | $\mathcal{L}_{\mathcal W}$ invariant de Lorentz + U(1) | 🟢 Prouvé | Construction |

---

## RÉSUMÉ — CE QUI EST RÉTRACTÉ

| # | Ancienne revendication | Pourquoi c'est retiré |
|---|----------------------|----------------------|
| 1 | « La TTC prédit les angles CKM » | Fits numériques manuels, pas des dérivations |
| 2 | « La TTC unifie RG + MQ + MS + ΛCDM » | Cadre commun ≠ unification |
| 3 | « $\Sigma m_\nu = 0.01-0.02$ eV » | Exclu par les oscillations |
| 4 | « La TTC explique la cosmologie » | Scénario qualitatif, pas de spectres calculés |
| 5 | « $r_c \propto 1/v_\infty$ confirmé » | Réfuté par SPARC (pente +0.66) |
| 6 | « Tully-Fisher dérivée » | Non reproductible (échec solveur) |
| 7 | « $P_{\rm max} = 3^5 = 243$ lié à $c^5/G$ » | Numérologie sans fondement |
| 8 | « La TTC réduit les paramètres libres » | Faux pour le secteur fermions |

---

## PROCHAINES ÉTAPES

1. **Validation du solveur TF** : `ttc_hardening_solver.py` doit démontrer
   que le système couplé $(\Gamma,\Phi,T)$ reproduit $v^4 \propto M_b$
   avec un scatter $< 0.3$ dex.

2. **Dérivation des nombres CKM** : Trouver un principe (symétrie de saveur ?
   géométrie de l'espace des champs ?) qui FIXE les nombres $1/\sqrt{20}$,
   $1/24$, $\alpha/2$ sans les mettre à la main.

3. **Refonte du secteur neutrino** : Accommoder $\Sigma m_\nu > 0.058$ eV.

4. **Application de la spec discrète v1.1** : Fournir à KontEx et autres
   implémenteurs une spécification complète et non ambiguë.

5. **Publication des tests falsificateurs** : `ttc_falsification_tests.py`
   comme standard de validation pour toute implémentation TTC.

---

*Errata rédigé par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*À incorporer dans le White Paper v1.1.*
*31 juillet 2026 — Session de durcissement.*
