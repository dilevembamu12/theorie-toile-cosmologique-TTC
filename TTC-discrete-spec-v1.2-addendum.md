# TTC — ADDENDUM v1.2 à la spécification discrète
## Nouvelles relations, loi de Kirchhoff-TTC, et postulat MCW-3

> **Date :** 15 août 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Objet :** Mise à jour de `TTC-discrete-spec-v1.1.md` suite à l'audit
> KontEx du 2026-08-04 et au prompt AST-Mapping.

---

## 1. LA 6e RELATION TTC : `instantiates`

### 1.1 Définition

Le vocabulaire TTC passe de 5 à **6 relations** :

| # | Relation | Sens physique | Champ dominant |
|---|----------|---------------|----------------|
| 1 | `refines` | Raffinement de cohérence | $\Gamma$ |
| 2 | `references` | Couplage de phase | $\Phi$ |
| 3 | `exemplifies` | Concrétisation d'un contrat | $\Gamma$ |
| 4 | `depends_on` | Dépendance causale | $T$ |
| 5 | `contradicts` | Tension topologique ($T > T_{\rm crit}$) | $T$ |
| 6 | **`instantiates`** | **Création d'instance avec décharge de tension** | **$\Gamma$, $T$** |

### 1.2 Formules

$$\Gamma_B^{\rm(init)} = \Gamma_A \cdot e^{-\kappa T_A}, \qquad T_B^{\rm(init)} = T_A \cdot \gamma_{\rm inst}, \qquad T_A^{\rm(après)} = T_A(1 - \gamma_{\rm inst})$$

avec $\kappa = 0.5$ (amortissement MCW-3) et $\gamma_{\rm inst} = 0.3$ (fraction
de tension transférée).

### 1.3 Statut

**Postulat MCW-3** — non dérivé du lagrangien. Analogie : décroissance
radioactive (la tension se décharge dans la matière créée).
À valider empiriquement.

---

## 2. LE THÉORÈME DE KIRCHHOFF-TTC

### 2.1 Énoncé

> **Théorème.** Dans un graphe TTC, la conservation du courant de phase
> $\nabla_\mu(\Gamma^2\nabla^\mu\Phi) = 0$ est équivalente à la loi des
> nœuds de Kirchhoff :
> $$\forall i : \left|\sum_{j \in \mathcal{N}_{\rm out}(i)} J_{ij} - \sum_{k \in \mathcal{N}_{\rm in}(i)} J_{ki}\right| < \varepsilon$$
> avec $J_{ij} = \Gamma_i^2 w_{ij}(\Phi_j - \Phi_i)$ et $\varepsilon = 10^{-6}$.

### 2.2 Corollaire : admittance TTC

L'admittance d'une arête est $Y_{ij} = \Gamma_i^2 w_{ij}$ — l'analogue TTC
de la conductance électrique. La redistribution d'un résidu Kirchhoff doit
être proportionnelle aux admittances, PAS aux poids seuls.

### 2.3 Corollaire : masse TTC (v2)

Pour les courants dirigés, introduire un nœud de masse $\mathcal{G}$ :
- $\Gamma_\mathcal{G} = v_\Gamma$, $\Phi_\mathcal{G} = 0$, $T_\mathcal{G} = 0$
- Tout courant dirigé se ferme par $\mathcal{G}$ (comme le ground électrique)

---

## 3. LA SYMÉTRIE DE JAUGE COMME GARDE-FOU

La symétrie $\Phi \to \Phi + c$ interdit :
- ❌ Fixer $\Phi = 0$ comme condition initiale absolue
- ❌ Le modulo $\Phi \in [0, 2\pi)$ dans le stockage
- ❌ Des formules qui dépendent de la valeur absolue de $\Phi$

Elle impose :
- ✅ Seules les DIFFÉRENCES $\Phi_j - \Phi_i$ sont physiques
- ✅ $\Phi \in \mathbb{R}$ non compactifié
- ✅ Les initialisations en termes relatifs ($\Phi_B = \Phi_A + \Delta\Phi$)

---

## 4. CONVERSION AST → TTC (table canonique)

| Relation AST | Relation TTC | Champ(s) | Confiance |
|--------------|--------------|----------|:---------:|
| `extends` | `refines` | $\Gamma$ | 0.98 |
| `implements` | `exemplifies` | $\Gamma$ | 0.97 |
| `injects` | `depends_on` | $T$ | 0.95 |
| `calls` | `references:directed` | $\Phi$ | 0.85 |
| `instantiates` | `instantiates` | $\Gamma, T$ | 0.92 |
| `throws` | `depends_on` | $T$ | 0.90 |
| `decorates` | `refines` | $\Gamma$ | 0.93 |
| autre | `references` | $\Phi$ | 0.50 (revue requise) |

**Invariants de conversion :**
1. Aucune arête supprimée (additif)
2. Aucun nœud orphelin créé
3. Réversibilité via `meta.ast_original`
4. Les arêtes TTC existantes sont inchangées

---

## 5. PÉREMPTION ADAPTATIVE PAR DOMAINE

Généralisation de la force d'ancrage :

$$\text{strength}(n) = \min\left(1, \frac{\sum_s \text{quality}(s) \cdot e^{-\lambda_{\rm dom}(s)\, \Delta t_s}}{\max(|\text{sources}|, 1)}\right)$$

Demi-vies par domaine : Mathématiques = ∞, Physique = 10 ans,
Spec de langage = 3 ans, Framework = 1 an, Bibliothèque = 18 mois,
Doc interne = 1 an, Actualités = 30 jours.

---

## 6. CHECKLIST DE CONFORMITÉ v1.2 (ajouts à la v1.1)

- [ ] Le courant $J_{ij}$ est antisymétrique ou fermé par un nœud de masse
- [ ] La loi de Kirchhoff est vérifiée après chaque propagation
- [ ] Les initialisations de $\Phi$ sont relatives (jamais $\Phi = 0$ absolu)
- [ ] La détection de contradiction est exécutée automatiquement à l'ingestion
- [ ] La minimisation d'entropie est déclenchée automatiquement (lot ou horloge)
- [ ] La péremption utilise $\lambda_{\rm domaine}$ par catégorie
- [ ] Les paramètres sont recalibrés sur ≥ 1000 paires avec validation croisée
- [ ] Le mapping AST → TTC suit la table canonique (§4)

---

*Addendum rédigé par DeepSeek V4 Pro, 15 août 2026.*
*À fusionner dans TTC-discrete-spec-v1.2.md lors de la prochaine publication.*
