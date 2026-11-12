# TTC — ROADMAP : L'ÉNERGIE NOIRE COMME THÉORIE PROUVABLE
## Développement atomique — le plan maître

> **Date :** 15 août 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Méthode :** une étape par session, chaque étape produit un document vérifiable.
> **Principe :** rien n'est affirmé avant d'être dérivé, calculé, et confronté.

---

## LES 8 ÉTAPES ATOMIQUES

| # | Étape | Question traitée | Livrable | Type |
|---|-------|------------------|----------|------|
| 1 | **Formalisme** | ~~Que donnent ρ_T, p_T, w_T depuis MCW-1 en fond FLRW ?~~ **RÉVOQUÉ (erreur interne)** | `step1-formalisme.md` (historique) | 📐 Math |
| **1.5** | **Correction** | Le vrai système à deux champs (Γ, T) — potentiel effectif, masse, vide | `step1.5-correction.md` ✅ | 📐 Math |
| 2 | **Résolution numérique** | Le système COUPLÉ (Γ, T, a) à trois ODE — pas le réduit | Solveur ODE + courbes w(z), H(z) | 💻 Code |
| 3 | **Classification des régimes** | Quels paramètres donnent w ≈ −1 ? w qui dérive ? — avec $m_{\rm eff}^2$, pas $\beta$ | Carte des phases | 📐 Analyse |
| 4 | **Prédictions falsifiables** | Ce qui distingue la TTC de ΛCDM — SANS prétendre au monopole des oscillations | Liste précise | 🎯 Test |
| 5 | **Confrontation aux données** | w₀, w_a mesurés vs prédits — comparaison BAYÉSIENNE (7 params vs 2) | Fit + Bayes | 📊 Data |
| 6 | **Stabilité et perturbations** | **GO/NO-GO** : le champ T est-il exclu par CMB/ISW/5e force ? | Analyse perturbations | 📐 Math |
| 7 | **Falsification formelle** | Le test qui tuerait la théorie | Protocole | 🎯 Test |
| 8 | **Publication** | Rédaction du papier énergie noire TTC | Document final | ✍️ Rédaction |

---

## ÉTAPE 1 (AUJOURD'HUI) : LE FORMALISME

**Contexte physique :** dans un univers FLRW homogène, le champ de cohérence
$\Gamma$ est gelé à son VEV ($\Gamma = v_\Gamma$) après la transition de phase
primordiale. Le champ de phase $\Phi$ est homogène ($\partial\Phi = 0$ — un
gradient de phase homogène serait un fluide raide $w=1$, dilué comme $a^{-6}$,
négligeable aujourd'hui). Le seul champ dynamique restant est la **tension
$T(t)$**.

**Question de l'étape :** que produisent les équations MCW-1 pour $T(t)$ dans
un fond en expansion ? Densité ? Pression ? Équation d'état ?

→ Voir `TTC-dark-energy-step1-formalisme.md`

---

## ÉTAPE 1.5 (FAITE LE 16 AOÛT) : LA CORRECTION

**Contexte :** l'agent vérificateur a réfuté l'Étape 1 sur 7 points. Vérification
indépendante : les 7 failles sont exactes. L'ansatz Γ = v_Γ était
auto-contradictoire.

**Résultats de la correction :**
- Vrai vide : T_eq = (βv_T − λv_Γ²)/(β − 2λ²/α), Γ_eq² = v_Γ² − 2λT_eq/α
- Masse effective : m_eff² = β − 2λ²/α
- Stabilité : αβ > 2λ²
- Vide AdS si v_T = 0 ; de Sitter si v_T = λv_Γ²/β
- Régime oscillant traité par le viriel : ⟨w⟩ = −V_min/(V_min + 2⟨K⟩)
- Contraintes de viabilité : m_eff ≳ H₀, V_min > 0, Ṫ² < V_eff

→ Voir `TTC-dark-energy-step1.5-correction.md`

---

## ÉTAPE 2 : RÉSOLUTION NUMÉRIQUE (SYSTÈME COMPLET)

**Question :** résoudre le système couplé :

$$\ddot T + 3H\dot T + \beta(T - v_T) + \lambda v_\Gamma^2 = 0$$

$$H^2 = \frac{8\pi G}{3}\left(\rho_m + \rho_r + \frac12\dot T^2 + V_{\rm eff}(T)\right)$$

et produire $w(z)$, $H(z)$, la distance de luminosité $d_L(z)$.

**Livrable :** `ttc_dark_energy_solver.py` + courbes comparatives ΛCDM vs TTC.

---

## ÉTAPE 3 : CLASSIFICATION DES RÉGIMES

Trois régimes attendus (analyse qualitative de l'étape 1) :

| Régime | Condition | Comportement | w |
|--------|-----------|--------------|---|
| **Gelé** | $\beta \ll H^2$ | T ne bouge pas → Λ effective | −1 exactement |
| **Slow-roll** | $\beta \sim H^2$ | T dérive lentement | −1 + ε, dérive |
| **Oscillant** | $\beta \gg H^2$ | T oscille autour de T_eq | moyenne ≠ −1, oscillations |

**Question :** quel régime la TTC prédit-elle pour les paramètres observés ?
Quel réglage donne le bon $\rho_\Lambda$ ?

---

## ÉTAPE 4 : PRÉDICTIONS FALSIFIABLES

Candidats attendus :
1. $w(z)$ a une forme fonctionnelle DÉTERMINÉE (pas de fonction libre) —
   à opposer à la paramétrisation phénoménologique $w_0$–$w_a$
2. Si $\beta \sim H_0^2$ : $w$ aujourd'hui mesurablement ≠ −1 avec une
   dérive caractéristique
3. Si $T$ oscille encore : oscillations résiduelles de $w(z)$ — signature
   unique, aucun autre modèle ne la produit de cette façon
4. Cohérence interne : le MÊME champ $T$ doit satisfaire les contraintes
   du système solaire (ou être écranté)

---

## ÉTAPE 5 : CONFRONTATION AUX DONNÉES

Comparer les prédictions TTC aux contraintes publiques :
- DESI 2024 : $w_0 = -0.99^{+0.15}_{-0.13}$ (contraintes en évolution)
- Pantheon+ : module de distance des SNe Ia
- Planck 2018 : paramètres CMB (shift parameters)
- BAO : $H(z)$ à plusieurs redshifts

**Critère :** la TTC doit fitter avec un χ² comparable ou meilleur que ΛCDM
SANS plus de paramètres libres que la différence qu'elle prétend expliquer.

---

## ÉTAPE 6 : STABILITÉ ET CONTRAINTES LOCALES

- Masse effective du champ : $m_T^2 = \beta$. Pour que $T$ n'ait pas d'effets
  mesurables dans le système solaire, il faut soit $m_T \gg$ (échelle locale),
  soit un mécanisme d'écrantage (couplage $\lambda$ faible)
- Stabilité : $V_{\rm eff}$ borné inférieurement ? Le minimum est à
  $T_{\rm eq} = v_T - \lambda v_\Gamma^2/\beta$ avec $V_{\rm min} = \lambda v_T v_\Gamma^2 - \lambda^2 v_\Gamma^4/(2\beta)$
  → signe de $V_{\rm min}$ à analyser

---

## ÉTAPE 7 : FALSIFICATION FORMELLE

Le protocole de mort : quelle mesure, à quelle précision, tuerait la théorie ?
Réponse attendue : une mesure de $w(z)$ incompatible avec la forme fonctionnelle
TTC à Nσ, OU la détection d'oscillations absentes, OU une masse $m_T$ exclue.

---

## ÉTAPE 8 : PUBLICATION

Structure du papier : Formalisme → Résolution → Prédictions → Données →
Discussion → Falsification. Avec les limitations honnêtes (hiérarchie λ,
non-prédiction des paramètres).

---

## RÈGLES DE CONDUITE ATOMIQUE

1. **Chaque étape est autosuffisante** — un document lisible seul
2. **Chaque étape se termine par un bilan** : acquis ✅ / ouvert 🟡 / mort 🔴
3. **Rien n'est promu au rang de résultat** sans calcul ou donnée à l'appui
4. **Les échecs sont documentés aussi précieusement que les succès**
5. **Le journal de session est mis à jour à chaque étape**

---

*Roadmap établie par DeepSeek V4 Pro, 15 août 2026.*
*Première étape : le formalisme — voir `TTC-dark-energy-step1-formalisme.md`.*
