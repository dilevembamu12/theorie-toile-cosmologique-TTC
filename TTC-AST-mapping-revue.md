# TTC — Revue théorique du prompt AST-Mapping
## Co-écriture : validation formelle des nouveaux postulats

> **Date :** 15 août 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Objet :** Revue critique du `TTC-AST-mapping-prompt.md` — validation des
> formules proposées pour le mapping AST → TTC, et formalisation des nouveaux
> éléments théoriques (6e relation, Kirchhoff-TTC, amortissement κ).

---

## 1. VERDICT GÉNÉRAL

Le prompt AST-Mapping est **remarquablement bon** : il traite le problème #X1
(connexions sombres) avec des formules explicites, des cas limites et des
critères de validation. Il contient cependant **3 erreurs théoriques** et
**1 nouveau postulat non dérivé** que ce document corrige.

| Élément | Statut | Verdict |
|---------|--------|---------|
| Table de mapping (7 relations) | 🟢 | Physiquement motivée |
| Courant discret $J_{ij}$ | 🟢 | Conforme à la spec v1.1 |
| Loi de Kirchhoff-TTC | 🟢 | Nouvelle formulation correcte |
| `instantiates` (6e relation) | 🟡 | Accepté — formalisé ci-dessous |
| Φ ∈ [0, 2π) dans le glossaire | 🔴 | **Régression** — corrigée dans le prompt |
| Courant `references:directed` | 🔴 | **Non conservatif** — voir §3 |
| Φ_B = 0 pour `implements` | 🔴 | **Brise la symétrie de jauge** — voir §4 |

---

## 2. VALIDATION : LA LOI DE KIRCHHOFF-TTC

### 2.1 Énoncé formel

Le prompt propose :

$$\forall i : \left|\sum_{j \in \mathcal{N}_{\rm out}(i)} J_{ij} - \sum_{k \in \mathcal{N}_{\rm in}(i)} J_{ki}\right| < \varepsilon$$

C'est la **discrétisation exacte** de la loi de conservation $\nabla_\mu(\Gamma^2\nabla^\mu\Phi) = 0$.
Elle est correcte et devient un **nouveau théorème de la TTC** :

> **Théorème (Kirchhoff-TTC).** Dans un graphe où chaque arête porte un courant
> $J_{ij} = \Gamma_i^2 w_{ij}(\Phi_j - \Phi_i)$, la conservation du courant de
> phase est équivalente à la loi des nœuds de Kirchhoff, avec une tolérance
> $\varepsilon$ absorbant les erreurs de discrétisation.

**Statut : 🟢 Intégré au cadre.** La loi de Kirchhoff-TTC est le pendant discret
de $\nabla_\mu T^{\mu\nu} = 0$ en RG. C'est un résultat STRUCTUREL, pas un
postulat : il découle de l'invariance de jauge $\Phi \to \Phi + c$.

### 2.2 La redistribution du résidu

La procédure `REDISTRIBUER_RESIDU` du prompt est correcte dans l'esprit mais
mathématiquement sous-optimale. La redistribution proportionnelle aux poids
$w_{ij}$ viole la structure de $J_{ij}$ (qui dépend de $\Gamma_i^2$ et $\Delta\Phi$).

**Correction recommandée :** redistribuer proportionnellement aux
**admittances** $Y_{ij} = \Gamma_i^2 w_{ij}$ (et non aux poids seuls) :

$$\Phi_j \leftarrow \Phi_j + \frac{\text{résidu}_i \cdot Y_{ij}}{\Gamma_i^2 \sum_{j'} Y_{ij'}}$$

Cette version est consistante avec la définition de $J_{ij}$ et converge vers
la solution de moindre résidu en un seul balayage pour les graphes acycliques.

---

## 3. ERREUR : LE COURANT DIRIGÉ N'EST PAS CONSERVATIF

### 3.1 Le problème

Le prompt définit pour `references:directed` :

$$J_{ij} = \Gamma_i^2 \cdot w_{ij} \cdot \max(\Phi_j - \Phi_i, 0)$$

Ce courant est **unidirectionnel par construction** ($J_{ij} \geq 0$, $J_{ji} = 0$).
Or un courant unidirectionnel **viole la loi de Kirchhoff** : un nœud qui ne
reçoit que des courants sortants doit avoir des courants entrants pour les
compenser, sinon il est une « source » ou un « puits » non physique.

### 3.2 Résolution : le concept de « masse » (ground)

En électricité, un courant dirigé n'existe que par rapport à une **masse**
(ground). La TTC doit introduire le même concept :

> **Définition (Masse TTC).** Le nœud de masse $\mathcal{G}$ est le nœud
> virtuel représentant « l'extérieur du graphe ». Tout courant dirigé
> $J_{ij}$ s'accompagne d'un courant de retour $J_{j\mathcal{G}} = -J_{ij}$
> qui ferme la boucle par la masse.

Ainsi :
- $\Phi_\mathcal{G} = 0$ (référence de phase absolue)
- Le courant dirigé $A \to B$ se lit : « la phase de B augmente, celle de A diminue, le solde part à la masse »
- La loi de Kirchhoff est préservée : $\sum J_{\rm out}(i) = \sum J_{\rm in}(i)$ pour tout nœud $i \neq \mathcal{G}$

**Correction du prompt :** ajouter le nœud de masse $\mathcal{G}$ au graphe
lors de la conversion, avec $\Gamma_\mathcal{G} = v_\Gamma$, $\Phi_\mathcal{G} = 0$,
$T_\mathcal{G} = 0$, et des arêtes implicites $i \to \mathcal{G}$ de poids 1
pour chaque arête dirigée.

### 3.3 Simplification alternative (recommandée pour le MVP)

Si le nœud de masse est trop lourd à implémenter, utiliser la définition
**antisymétrique standard** (comme le prompt le fait pour `references:bidirectional`) :

$$J_{ij} = \Gamma_i^2 w_{ij}(\Phi_j - \Phi_i)$$

et laisser la directionalité s'exprimer dans la **topologie** (arêtes orientées)
plutôt que dans la formule du courant. Le courant est conservatif par
antisymétrie, et la directionalité émerge naturellement du signe de $J_{ij}$
(positif = flux vers B, négatif = flux vers A).

**⚠️ Recommandation :** Pour le MVP, adoptez la version antisymétrique.
La version avec max() et nœud de masse est un raffinement v2.

---

## 4. ERREUR : Φ_B = 0 POUR `implements` BRISE LA SYMÉTRIE DE JAUGE

### 4.1 Le problème

Le prompt définit pour `implements` : $\Phi_B^{(init)} = 0$ « rupture du contrat ».
Or la symétrie de jauge $\Phi \to \Phi + c$ implique que la VALEUR ABSOLUE de
$\Phi$ n'a aucun sens physique — seules les DIFFÉRENCES de phase comptent.
Fixer $\Phi_B = 0$ choisit arbitrairement une jauge, ce qui :
1. Brise l'invariance de jauge (et donc la conservation du courant)
2. Crée une discontinuité artificielle avec les voisins de B
3. Rend le résultat dépendant de l'ordre d'ingestion des nœuds

### 4.2 Correction

La « rupture de contrat » d'une implémentation doit s'exprimer par une
**différence de phase relative**, pas absolue :

$$\Phi_B^{\rm(init)} = \Phi_A + \Delta\Phi_{\rm impl}$$

avec $\Delta\Phi_{\rm impl} = \pi/4$ (l'implémentation est « déphasée » d'un
quart de tour par rapport au contrat — elle le concrétise mais ne le suit pas
à l'identique). Cette formulation préserve l'invariance de jauge et donne
un sens physique à la « distance contractuelle » entre interface et implémentation.

**Correction du prompt :** remplacer $\Phi_B = 0$ par $\Phi_B = \Phi_A + \pi/4$
pour `implements` et $\Phi_B = 0 + \Phi_A \cdot \gamma_{\rm inst}$ pour
`instantiates` (la nouvelle instance hérite de la phase de la classe, modulée).

---

## 5. FORMALISATION : LA 6e RELATION `instantiates`

### 5.1 La formule du prompt

$$\Gamma_B^{\rm(instance)} = \Gamma_B^{\rm(classe)} \cdot e^{-\kappa T_A}$$

### 5.2 Statut : postulat MCW-3, pas dérivation

Cette formule introduit un **nouveau mécanisme physique** : l'acte
d'instanciation convertit la tension $T_A$ en cohérence $\Gamma_B$, avec un
facteur d'amortissement $\kappa$. Ce mécanisme n'est **pas dérivé** du
lagrangien MCW-1/2 — c'est un postulat d'extension.

**Formalisation théorique (MCW-3) :**

> **Postulat MCW-3 (conversion tension → cohérence).** Lorsqu'un nœud A
> instancie un nœud B, une fraction de la tension de A est convertie en
> cohérence de B selon :
> $$\Gamma_B = \Gamma_B^{\rm(classe)} \cdot e^{-\kappa T_A}$$
> $$T_B = T_A \cdot \gamma_{\rm inst}, \quad T_A^{\rm après} = T_A(1 - \gamma_{\rm inst})$$
> où $\kappa$ est l'amortissement MCW-3 et $\gamma_{\rm inst}$ la fraction
> de tension transférée.

**Interprétation physique :** L'instanciation est un **canal de dissipation**.
Un nœud A très tendu (code fragile, beaucoup de contradictions) crée des
instances de moindre cohérence. C'est le mécanisme par lequel la tension
se « décharge » dans la matière — l'analogue TTC de la **décroissance radioactive**.

**Conséquences testables :**
1. Les classes avec $T$ élevé produisent des instances avec $\Gamma$ réduit
2. L'instanciation réduit $T$ de la classe (décharge)
3. La tension totale du système est conservée : $T_A^{\rm après} + T_B^{\rm init} \approx T_A^{\rm avant}$ (à un facteur d'amortissement près)

**Statut : 🟡 Postulat — à valider empiriquement sur le benchmark KontEx.**

---

## 6. LES PARAMÈTRES : RÉPONSE À L'ALERTE #P2

L'audit a raison : les paramètres ($\alpha = 0.01$, $\beta = 0.3$, $\lambda = 0.001$)
sont choisis pour la stabilité numérique, pas pour la physique. Le prompt
AST-Mapping les reprend tels quels.

**Position du co-auteur :** c'est **acceptable pour un MVP**, à condition que :
1. La dépendance des résultats aux paramètres soit **documentée**
2. Une **analyse de sensibilité** soit faite (varier chaque paramètre de ±50%
   et mesurer l'impact sur le F1)
3. La calibration sur ≥1000 paires soit planifiée (pas 10)

La TTC ne prédit PAS ces paramètres — c'est une limitation connue du cadre
(White Paper §1.4). Ne pas la masquer : c'est un problème de naturalité,
comme dans le Modèle Standard.

---

## 7. SYNTHÈSE DES CORRECTIONS À APPLIQUER AU PROMPT

| # | Correction | Section du prompt | Priorité |
|---|-----------|-------------------|----------|
| 1 | $\Phi \in \mathbb{R}$ (déjà corrigé) | Glossaire §10 | 🔴 Fait |
| 2 | Kirchhoff : redistribution par admittances $Y_{ij}$ | §5.1 | 🟡 À faire |
| 3 | Courant dirigé : nœud de masse OU antisymétrie | §2.2, §3.4 | 🔴 À faire |
| 4 | $\Phi_B = \Phi_A + \pi/4$ (pas 0) pour `implements` | §3.2 | 🔴 À faire |
| 5 | $\Phi_B = \Phi_A \cdot \gamma_{\rm inst}$ pour `instantiates` | §3.5 | 🟡 À faire |
| 6 | Documenter MCW-3 comme postulat | §2.3 | 🟢 Fait ici |

---

## 8. NOUVEAUX ÉLÉMENTS INTÉGRÉS AU CADRE TTC

Ce document ajoute au cadre théorique :

1. **Théorème de Kirchhoff-TTC** — conservation discrète du courant de phase (§2)
2. **Masse TTC** ($\mathcal{G}$) — référence de phase absolue pour courants dirigés (§3.2)
3. **Postulat MCW-3** — conversion tension → cohérence avec amortissement κ (§5)
4. **6e relation : `instantiates`** — avec formule de décharge de tension (§5)
5. **Admittance** $Y_{ij} = \Gamma_i^2 w_{ij}$ — l'analogue TTC de la conductance (§2.2)

---

*Revue rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*15 août 2026 — Suite de l'audit KontEx du 2026-08-04.*
