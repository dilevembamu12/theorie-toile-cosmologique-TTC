# TTC SUR GRAPHES DISCRETS — Spécification Complète v1.1
## Chapitre additionnel au White Paper TTC

> **Statut :** Spécification normative pour toute implémentation TTC sur graphes.
> **Audience :** Ingénieurs, implémenteurs (KontEx et autres).
> **Date :** 31 juillet 2026 — Rédigé suite à l'audit KontEx v0.1.
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC).

---

## TABLE DES MATIÈRES

1. [Domaine de validité](#1-domaine-de-validité)
2. [Définitions et conventions](#2-définitions-et-conventions)
3. [Du continu au discret](#3-du-continu-au-discret)
4. [Opérateurs discrets](#4-opérateurs-discrets)
5. [Initialisation des champs](#5-initialisation-des-champs)
6. [Algorithme de résolution](#6-algorithme-de-résolution)
7. [Définition canonique de T](#7-définition-canonique-de-t)
8. [Critère de convergence](#8-critère-de-convergence)
9. [Évaluation du Lagrangien](#9-évaluation-du-lagrangien)
10. [Back-reaction métrique (optionnelle)](#10-back-reaction-métrique-optionnelle)
11. [Seuil de détection T_crit](#11-seuil-de-détection-t_crit)
12. [Nœuds temporaires et dissipation](#12-nœuds-temporaires-et-dissipation)
13. [Checklist de conformité](#13-checklist-de-conformité)

---

## 1. DOMAINE DE VALIDITÉ

La **TTC discrète** (ou TTC-graphe) est une transposition du formalisme TTC
continu aux graphes pondérés. Elle NE PRÉTEND PAS décrire la physique
fondamentale. Elle est un **modèle phénoménologique** pour :

- La détection d'incohérences dans les graphes de connaissance
- L'évaluation de la cohérence de textes, assertions, ou faits
- L'analyse de la structure logique de documents

**La TTC discrète n'est PAS :**
- Une théorie physique
- Un modèle de langage génératif
- Un classifieur binaire standard (son seuil est continu)
- Une preuve de la TTC physique

**Correspondance avec la TTC physique :**
La TTC physique utilise les mêmes structures mathématiques (lagrangien scalaire,
brisure de symétrie) mais dans l'espace-temps continu à 4 dimensions.
La TTC discrète est une **analogie structurelle**, pas une réduction.

---

## 2. DÉFINITIONS ET CONVENTIONS

### 2.1 Graphe

Un graphe pondéré dirigé $G = (V, E, w)$ où :
- $V = \{1, \ldots, N\}$ : ensemble des nœuds
- $E \subseteq V \times V$ : ensemble des arêtes
- $w_{ij} \in [0, 1]$ : poids de l'arête $i \to j$

Le graphe peut être dirigé ou non dirigé. S'il est non dirigé, $w_{ij} = w_{ji}$.

### 2.2 Champs TTC discrets

| Symbole | Définition discrète | Type | Domaine |
|---------|---------------------|------|---------|
| $\Gamma_i$ | Cohérence du nœud $i$ | $\mathbb{R}^+$ | $[v_\Gamma, \infty)$ |
| $\Phi_i$ | Phase du nœud $i$ | $\mathbb{R}$ | $(-\infty, +\infty)$ |
| $T_i$ | Tension du nœud $i$ | $\mathbb{R}$ | $[v_T, \infty)$ typiquement |

> ⚠️ **CRITIQUE :** $\Phi_i \in \mathbb{R}$, **NON** compactifié dans $[0, 2\pi)$.
> La périodicité $\Phi \to \Phi + 2\pi n$ est une symétrie, pas une contrainte.
> Le calcul des gradients $\nabla\Phi_{ij} = \Phi_j - \Phi_i$ se fait directement
> sur les réels, SANS modulo, SANS unwrap.

### 2.3 Constantes (valeurs par défaut)

| Constante | Symbole | Valeur | Statut |
|-----------|---------|--------|--------|
| VEV de cohérence | $v_\Gamma$ | $1.0$ | Normalisation |
| VEV de tension | $v_T$ | $0.0$ | Le vide n'a pas de tension |
| Auto-interaction $\Gamma$ | $\alpha$ | $1.0$ | À calibrer par domaine |
| Masse de $T$ | $\beta$ | $1.0$ | À calibrer par domaine |
| Couplage $\Gamma$-$T$ | $\lambda$ | $0.1$ | À calibrer par domaine |
| Relaxation | $\eta$ | $0.3$ | Pour Jacobi |
| Tolérance résidu | $\varepsilon$ | $10^{-6}$ | × échelle caractéristique |
| Seuil de contradiction | $T_{\rm crit}$ | $0.95$ | Paramètre libre de décision |
| Puissance max discrète | $P_{\rm max}^{\rm disc}$ | À définir | PAS $243$ (voir Note $P_{\rm max}$) |

---

## 3. DU CONTINU AU DISCRET

### 3.1 Correspondance

| Continu (TTC physique) | Discret (TTC-graphe) |
|------------------------|----------------------|
| Espace-temps $\mathcal{M}$ | Graphe $G = (V, E)$ |
| Point $x \in \mathcal{M}$ | Nœud $i \in V$ |
| Métrique $g_{\mu\nu}$ | Poids $w_{ij}$ |
| $\partial_\mu \phi$ | $\nabla\phi_{ij} = \phi_j - \phi_i$ |
| $\square \phi = g^{\mu\nu}\nabla_\mu\nabla_\nu\phi$ | $(\mathbf{L}\phi)_i = \sum_{j} w_{ij}(\phi_i - \phi_j)$ |
| $\int d^4x \sqrt{-g}$ | $\sum_{i \in V}$ |
| Densité lagrangienne $\mathcal{L}(x)$ | $\mathcal{L}_i$ par nœud |

### 3.2 Lagrangien discret

$$\boxed{\mathcal{L}_i = -\frac12 \sum_{j \in \mathcal{N}(i)} w_{ij}(\Gamma_i - \Gamma_j)^2 - \frac12 \Gamma_i^2 \sum_{j \in \mathcal{N}(i)} w_{ij}(\Phi_i - \Phi_j)^2 - \frac12 \sum_{j \in \mathcal{N}(i)} w_{ij}(T_i - T_j)^2 - U(\Gamma_i, T_i)}$$

où $\mathcal{N}(i)$ est l'ensemble des voisins de $i$, et :

$$\boxed{U(\Gamma_i, T_i) = \frac{\alpha}{4}(\Gamma_i^2 - v_\Gamma^2)^2 + \frac{\beta}{2}(T_i - v_T)^2 + \lambda T_i \Gamma_i^2}$$

---

## 4. OPÉRATEURS DISCRETS

### 4.1 Laplacien de graphe

$$\boxed{(\mathbf{L}\phi)_i = \sum_{j \in \mathcal{N}(i)} w_{ij} (\phi_i - \phi_j)}$$

**Propriétés :**
- $\mathbf{L}$ est semi-défini positif
- $\mathbf{L} = \mathbf{D} - \mathbf{A}$ où $\mathbf{D}$ est la matrice des degrés pondérés et $\mathbf{A}$ la matrice d'adjacence pondérée
- Pour un graphe non dirigé, $\mathbf{L}$ est symétrique

**Implémentation de référence (pseudo-code) :**
```
function laplacian(graph, field, node_i):
    result = 0.0
    for each neighbor j of node_i:
        w = graph.weight(i, j)
        result += w * (field[i] - field[j])
    return result
```

### 4.2 Gradient de phase

$$\boxed{(\nabla\Phi)_{ij} = \Phi_j - \Phi_i \quad \text{(NON modulo)}}$$

**Justification :** La condition de quantification $\oint \nabla\Phi \cdot d\mathbf{l} = 2\pi n$
garantit que $\Phi$ est multivaluée avec des sauts de $2\pi$. Sur un graphe,
$\Phi_i \in \mathbb{R}$ non compactifié est la représentation naturelle.

### 4.3 Norme du gradient

$$\boxed{|\nabla\Phi|_i^2 = \sum_{j \in \mathcal{N}(i)} w_{ij} (\Phi_i - \Phi_j)^2}$$

---

## 5. INITIALISATION DES CHAMPS

### 5.1 $\Gamma$ initial (cohérence)

$\Gamma$ est initialisé à partir de la représentation vectorielle (embedding)
du contenu du nœud :

$$\boxed{\Gamma_i^{\rm init} = v_\Gamma + \mu \cdot g(\mathbf{e}_i)}$$

où :
- $\mathbf{e}_i \in \mathbb{R}^d$ est l'embedding du contenu du nœud $i$
- $g : \mathbb{R}^d \to [0, 1]$ est une fonction de normalisation
- $\mu$ est le couplage embedding → cohérence (paramètre libre, défaut $\mu = 1.0$)

**Choix recommandés pour $g$ :**
- $g(\mathbf{e}) = \|\mathbf{e}\| / \|\mathbf{e}\|_{\max}$ (normalisation par la norme max)
- $g(\mathbf{e}) = \sigma(\mathbf{w}^T\mathbf{e} + b)$ (projection apprise + sigmoïde)
- $g(\mathbf{e}) = 1 - \text{entropy}(\text{softmax}(\mathbf{e}))$ (entropie inversée)

**Si pas d'embedding :** $\Gamma_i^{\rm init} = v_\Gamma$ (nœud vide, le champ relaxera).

### 5.2 $\Phi$ initial (phase)

$$\boxed{\Phi_i^{\rm init} = 0 \quad \forall i}$$

La phase n'a pas de source intrinsèque dans le contenu textuel. Elle émerge
de la résolution des EDP. Si une phase initiale non nulle est nécessaire
(ex. relations causales), elle doit être justifiée par le domaine.

### 5.3 $T$ initial (tension) ⚠️ CRITIQUE

**$T^{\rm init}$ N'EST PAS $T$.**

$T^{\rm init}$ est une heuristique d'initialisation. $T$ est la solution
de l'EDP après relaxation. La confusion entre les deux est la source #1
de bugs dans les implémentations TTC.

$$\boxed{T_i^{\rm init} = v_T + \kappa \cdot h(\text{contenu}_i)}$$

où $h$ est une heuristique domaine-spécifique et $\kappa$ un paramètre
de calibration. Exemples de $h$ :

| Domaine | $h$ |
|---------|-----|
| Détection d'hallucinations | $h = 1 - \text{cosine\_similarity}(\text{assertion}, \text{référence})$ |
| Contradictions logiques | $h = \mathbb{1}[\text{negation\_detected}]$ |
| Cohérence de paragraphe | $h = \text{perplexité}(\text{texte}) / \text{perplexité}_{\max}$ |

**Important :** Après résolution des EDP, $T$ (solution) remplace complètement
$T^{\rm init}$. La valeur finale de $T_i$ est déterminée par la physique du
graphe (couplage $\Gamma$-$T$, équation d'onde), PAS par l'heuristique initiale.

---

## 6. ALGORITHME DE RÉSOLUTION

### 6.1 Choix de l'algorithme

| Algorithme | Quand l'utiliser | Avantages | Inconvénients |
|------------|------------------|-----------|---------------|
| **Jacobi** | Graphes cycliques (cas général) | Préserve la symétrie, ordre-indépendant | Convergence lente |
| **Gauss-Seidel** | DAG uniquement | Convergence ~2× plus rapide | Résultat dépend de l'ordre de sweep |
| **Gauss-Seidel randomisé** | Graphes cycliques (alternative) | Compromis vitesse/symétrie | Non déterministe |

**RÈGLE :** Si le graphe contient des cycles, utiliser **Jacobi**. Si le graphe
est un DAG, Gauss-Seidel avec ordre topologique est acceptable.

### 6.2 Algorithme de Jacobi (recommandé)

```
ENTRÉES :
  G = (V, E, w)          // Graphe
  Γ_init, Φ_init, T_init // Champs initiaux
  α, β, λ, v_Γ, v_T      // Paramètres physiques
  η                      // Relaxation ∈ (0, 1)
  ε                      // Tolérance
  max_iter               // Nombre max d'itérations

SORTIES :
  Γ, Φ, T                // Solutions
  converged              // Booléen
  n_iter                 // Nombre d'itérations utilisées

ALGORITHME :
  Γ ← Γ_init, Φ ← Φ_init, T ← T_init
  POUR iter = 1 À max_iter :
    Γ_old ← Γ, Φ_old ← Φ, T_old ← T
    
    POUR CHAQUE i ∈ V (EN PARALLÈLE si possible) :
      // Équation Γ
      lap_Γ ← LAPLACIEN(G, Γ_old, i)
      grad_Φ_sq ← SOMME_{j∈N(i)} w_ij * (Φ_old[i] - Φ_old[j])²
      rhs_Γ ← Γ_old[i] * grad_Φ_sq
               + α * Γ_old[i] * (Γ_old[i]² - v_Γ²)
               + 2λ * T_old[i] * Γ_old[i]
      resid_Γ ← lap_Γ - rhs_Γ
      Γ[i] ← Γ_old[i] - η * resid_Γ
      
      // Équation Φ (intégration directe du flux)
      // ∇·(Γ²∇Φ) = 0 → Φ solution du système linéaire
      // Pour Jacobi : construire la matrice creuse et résoudre
      // Simplification (acceptable pour graphes < 10⁴ nœuds) :
      //   Mettre à jour Φ via relaxation du laplacien pondéré
      poids_Γ ← Γ[i]² + Γ[j]²  // moyenne pour l'arête i-j
      lap_Φ_pond ← SOMME_{j} w_ij * poids_Γ * (Φ_old[i] - Φ_old[j])
      Φ[i] ← Φ_old[i] - η * 0.1 * lap_Φ_pond  // relaxation lente
      
      // Équation T
      lap_T ← LAPLACIEN(G, T_old, i)
      rhs_T ← β * (T_old[i] - v_T) + λ * Γ[i]²
      resid_T ← lap_T - rhs_T
      T[i] ← T_old[i] - η * resid_T
    
    // Conditions aux bords (optionnel)
    // Fixer les nœuds « ancrés » à leur valeur initiale
    POUR CHAQUE nœud ancré a :
      Γ[a] ← Γ_init[a]
      T[a] ← T_init[a]
    
    // Calcul des résidus
    res_Γ ← MAX_i |resid_Γ[i]|
    res_T ← MAX_i |resid_T[i]|
    ΔΦ ← MAX_i |Φ[i] - Φ_old[i]|
    
    SI res_Γ < ε ET res_T < ε ET ΔΦ < ε :
      RETOURNER Γ, Φ, T, VRAI, iter
    
  RETOURNER Γ, Φ, T, FAUX, max_iter
```

### 6.3 Paramètre de relaxation

- $\eta = 0.3$ : recommandé pour la plupart des graphes
- $\eta = 0.1$ : si oscillations (graphes très connectés)
- $\eta = 0.5$ : si convergence trop lente (graphes peu connectés)

**Règle pratique :** Si le résidu oscille, diviser $\eta$ par 2. Si le résidu
décroît monotonement mais lentement, multiplier $\eta$ par 1.5.

---

## 7. DÉFINITION CANONIQUE DE T

> ⚠️ **CECI EST LA SECTION LA PLUS IMPORTANTE DE CE DOCUMENT.**

Il existe **UNE SEULE** définition canonique de $T$ dans la TTC :

$$\boxed{T_i = \text{solution de } (\mathbf{L}T)_i - \beta(T_i - v_T) - \lambda\Gamma_i^2 = 0}$$

Toute autre « définition » de $T$ (bigrammes, tokens, cosine similarity, etc.)
est une **heuristique d'initialisation** $T^{\rm init}$, pas $T$.

**Pipeline correct :**
```
┌──────────────────────────────────────────────────────┐
│ 1. T_heuristique ← h(contenu_texte)                  │
│    ↓                                                  │
│ 2. T_init ← v_T + κ · T_heuristique                  │
│    ↓                                                  │
│ 3. Résolution EDP : (L T) − β(T−v_T) − λΓ² = 0      │
│    ↓                                                  │
│ 4. T_final ← solution de l'EDP                       │
│    ↓                                                  │
│ 5. Détection : T_final > T_crit → contradiction       │
└──────────────────────────────────────────────────────┘
```

**RÈGLE :** Après l'étape 3, $T^{\rm init}$ est OUBLIÉ. Seul $T^{\rm final}$ existe.
Si le code contient une variable nommée `T` après la résolution, elle DOIT
contenir $T^{\rm final}$, PAS $T^{\rm init}$.

---

## 8. CRITÈRE DE CONVERGENCE

### 8.1 Ce qu'il faut vérifier

$$\boxed{\max_i |\text{Résidu}_i^{\rm EDP}| < \varepsilon}$$

où le résidu est :
- $\text{Res}_i^\Gamma = (\mathbf{L}\Gamma)_i - \Gamma_i|\nabla\Phi|_i^2 - \alpha\Gamma_i(\Gamma_i^2 - v_\Gamma^2) - 2\lambda T_i\Gamma_i$
- $\text{Res}_i^T = (\mathbf{L}T)_i - \beta(T_i - v_T) - \lambda\Gamma_i^2$

et $\varepsilon = 10^{-6} \times \text{échelle\_caractéristique}$,
avec $\text{échelle\_caractéristique} = \max(|\Gamma^{\rm init}|, v_\Gamma)$.

### 8.2 Ce qu'il NE FAUT PAS vérifier

❌ $\max_i |\Delta f_i| < \varepsilon$ (variation des champs entre itérations)
❌ $\max_i |f_i^{(n+1)} - f_i^{(n)}| < \varepsilon$ (plateau)

Un plateau ne signifie PAS que l'EDP est satisfaite. Exemple : équilibre
métastable où tous les gradients s'annulent mais l'EDP n'est pas vérifiée.

### 8.3 Convergence du Lagrangien (critère supplémentaire)

$$\boxed{\left|\frac{\mathcal{L}_W^{(n+1)} - \mathcal{L}_W^{(n)}}{\mathcal{L}_W^{(n)}}\right| < 10^{-8}}$$

Si le résidu EDP < ε mais que $\mathcal{L}_W$ continue de décroître, le système
n'est pas encore au minimum. Continuer les itérations.

---

## 9. ÉVALUATION DU LAGRANGIEN

### 9.1 Formule

$$\boxed{\mathcal{L}_W = \sum_{i \in V} \mathcal{L}_i}$$

avec $\mathcal{L}_i$ défini en §3.2. Le lagrangien total $\mathcal{L}_W$ est
la **fonction de coût globale** du système.

### 9.2 Utilités

- **Suivi de convergence :** $\mathcal{L}_W$ doit décroître monotonement (après
  les premières itérations). Une remontée indique une instabilité numérique
  ($\eta$ trop grand).
- **Comparaison de configurations :** Entre deux solutions, celle avec le
  $\mathcal{L}_W$ le plus bas est physiquement favorisée.
- **Détection de minima locaux :** Si $\mathcal{L}_W$ cesse de décroître mais
  le résidu EDP > ε, le système est piégé dans un minimum local.

### 9.3 Implémentation

```
function compute_lagrangian(graph, Gamma, Phi, T, alpha, beta, lambda, v_Gamma, v_T):
    L_total = 0.0
    for each node i:
        // Termes cinétiques
        kin_Gamma = 0.0
        kin_Phi = 0.0
        kin_T = 0.0
        for each neighbor j of i:
            w = graph.weight(i, j)
            kin_Gamma += w * (Gamma[i] - Gamma[j])**2
            kin_Phi   += w * (Phi[i] - Phi[j])**2
            kin_T     += w * (T[i] - T[j])**2
        
        // Potentiel
        U = (alpha/4) * (Gamma[i]**2 - v_Gamma**2)**2 \
            + (beta/2) * (T[i] - v_T)**2 \
            + lambda * T[i] * Gamma[i]**2
        
        L_i = -0.5 * kin_Gamma - 0.5 * Gamma[i]**2 * kin_Phi - 0.5 * kin_T - U
        L_total += L_i
    
    return L_total
```

---

## 10. BACK-REACTION MÉTRIQUE (OPTIONNELLE)

### 10.1 Quand l'activer

La back-reaction métrique est nécessaire quand :

$$\max_{i,j} (\Gamma_i \cdot \Gamma_j \cdot w_{ij}) \gg \max_{i,j} w_{ij}$$

c'est-à-dire quand le produit des cohérences modifie significativement les
poids effectifs. Pour des graphes de connaissance standards ($\Gamma_i \lesssim 2$,
$w_{ij} \in [0,1]$), la back-reaction est **négligeable**.

### 10.2 Équation

$$\boxed{w_{ij}^{\rm eff} = w_{ij} \cdot \Gamma_i \cdot \Gamma_j}$$

### 10.3 Algorithme (si activé)

```
POUR outer_iter = 1 À max_outer :
  // Résoudre les EDP avec métrique fixe w_ij
  Γ, Φ, T ← JACOBI(G, w, ...)
  
  // Mettre à jour la métrique
  POUR CHAQUE arête (i,j) :
    w_ij ← w_ij_initial × Γ_i × Γ_j
  
  // Vérifier la convergence de la métrique
  SI max |Δw_ij| < ε_metric :
    BREAK
```

**Attention :** La back-reaction rend le problème non linéaire. $\eta$ doit
être réduit (typiquement $\eta/2$ pour la boucle externe).

---

## 11. SEUIL DE DÉTECTION $T_{\rm crit}$

### 11.1 Nature

$T_{\rm crit}$ est un **paramètre libre de décision**, PAS une constante
fondamentale. Il n'apparaît pas dans le lagrangien MCW-1.

### 11.2 Valeur par défaut

$$\boxed{T_{\rm crit} = 0.95}$$

Cette valeur est un ordre de grandeur heuristique, calibré pour la détection
d'hallucinations sur un petit échantillon pilote. Elle DOIT être recalibrée
pour chaque domaine d'application.

### 11.3 Calibration

Pour un domaine donné :
1. Constituer un dataset étiqueté (au moins 100 exemples équilibrés)
2. Pour chaque exemple, calculer $T$ (solution EDP)
3. Faire varier $T_{\rm crit}$ de 0 à $\max(T)$
4. Choisir $T_{\rm crit}$ qui maximise le F1-score

### 11.4 Règle d'unification

**TOUS les modules d'une même application DOIVENT utiliser le MÊME $T_{\rm crit}$.**
Un module avec $T_{\rm crit} = 0.50$ et un autre avec $T_{\rm crit} = 0.95$
constitue un **BUG**, pas une divergence d'opinion scientifique.

---

## 12. NŒUDS TEMPORAIRES ET DISSIPATION

### 12.1 Problème

Le lagrangien MCW-1 est conservatif : il n'y a pas de dissipation. Un nœud
ajouté temporairement ne disparaît jamais spontanément.

### 12.2 Solution immédiate (implémentation)

**Tout nœud ajouté pour un test doit être supprimé après le test.**

### 12.3 Solution théorique (extension MCW-2)

Pour les applications où des nœuds doivent pouvoir apparaître et disparaître,
ajouter un terme de dissipation :

$$\boxed{\mathcal{L}_{\rm diss} = -\frac{\gamma}{2} \sum_{i \in V_{\rm temp}} (\Gamma_i - v_\Gamma)^2}$$

où $V_{\rm temp}$ est l'ensemble des nœuds non ancrés (sans source externe).

Cela donne une « durée de vie » effective $\tau = 1/\gamma$ :
- $\Gamma_i(t) \to v_\Gamma$ (le nœud « s'évapore »)
- $T_i(t) \to v_T$ (la tension se dissipe)
- Après $\tau$, le nœud est indistinguable du vide

**Valeur recommandée :** $\gamma = 0.01$ (le nœud disparaît en ~100 itérations).

---

## 13. CHECKLIST DE CONFORMITÉ

Pour qu'une implémentation soit **conforme à la spécification TTC discrète v1.1**,
elle DOIT satisfaire TOUS les points suivants :

### Algorithme
- [ ] Le laplacien discret est $\mathbf{L} = \mathbf{D} - \mathbf{A}$ (ou équivalent)
- [ ] $\Phi \in \mathbb{R}$ non compactifié (PAS de modulo)
- [ ] Jacobi pour les graphes cycliques (ou GS avec ordre documenté)
- [ ] Relaxation $\eta \in (0, 1)$ documentée

### Convergence
- [ ] Critère de convergence = résidu EDP $< \varepsilon$ (PAS variation des champs)
- [ ] $\varepsilon = 10^{-6} \times$ échelle caractéristique (documentée)
- [ ] $\mathcal{L}_W$ évalué à chaque itération (ou périodiquement)

### Champs
- [ ] $\Gamma_i^{\rm init}$ documenté (formule de mapping embedding → $\Gamma$)
- [ ] $\Phi_i^{\rm init} = 0$ (ou justifié autrement)
- [ ] $T^{\rm init}$ documenté comme heuristique, distinct de $T$ final
- [ ] $T$ final = solution de l'EDP, PAS $T^{\rm init}$

### Constantes
- [ ] $v_\Gamma = 1.0$ (normalisation)
- [ ] $v_T = 0.0$ (vide sans tension)
- [ ] $\alpha, \beta, \lambda$ documentés et justifiés pour le domaine
- [ ] $T_{\rm crit}$ UNIQUE dans toute la codebase
- [ ] $P_{\rm max}^{\rm disc}$ documenté (et NON confondu avec $c^5/G$)

### Nettoyage
- [ ] Les nœuds temporaires sont supprimés après usage
- [ ] OU un mécanisme de dissipation est implémenté et documenté

### Tests
- [ ] Test de contradiction logique : $A \land \neg A \to T > T_{\rm crit}$
- [ ] Test du vide : graphe vide → $\Gamma_i = v_\Gamma$, $T_i = v_T$ après relaxation
- [ ] Test de stabilité : solution invariante par permutation des nœuds (Jacobi)

---

## RÉFÉRENCES

1. TTC White Paper v1.0 — Dileve MBAMU & DeepSeek V4 Pro, 13 juillet 2026
2. Audit d'implémentation KontEx v0.1 — Équipe KontEx, juillet 2026
3. Note technique $P_{\rm max}$ — Dileve MBAMU & DeepSeek V4 Pro, 31 juillet 2026
4. TTC Hardening Solver — DeepSeek V4 Pro, 31 juillet 2026

---

*Spécification rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*Version 1.1 — 31 juillet 2026.*
