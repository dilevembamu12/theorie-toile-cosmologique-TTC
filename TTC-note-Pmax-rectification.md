# NOTE TECHNIQUE : $P_{\rm max} = 3^5 = 243$ — Rectification

> **Objet :** Correction de l'erreur de numérologie $P_{\rm max} = c^5/G \leftrightarrow 3^5 = 243$.
> **Date :** 31 juillet 2026 — Rédigé suite à l'audit KontEx v0.1.
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC).
> **Impact :** Cette note doit être lue conjointement avec `TTC-note-Pmax-c5-sur-G.md`
> et `TTC-puissance-max-onde.md`.

---

## 1. L'ERREUR

Dans certaines implémentations (notamment KontEx), on trouve :

```
P_max = 243.0  # commenté « c⁵/G computational analog »
```

avec la justification implicite : $3^5 = 243$ et la TTC a 3 champs, et $c^5/G$ a un exposant 5.

**Ceci est une erreur.** Il n'existe AUCUN lien mathématique ou physique entre :

- $c^5/G \approx 3.63 \times 10^{52}$ Watts (constante physique)
- $3^5 = 243$ (nombre entier)

Le fait que les deux expressions impliquent le nombre 5 (exposant de $c^5/G$,
nombre de champs $3 \to 3^5$) est une **coïncidence numérique fortuite**,
pas une dérivation.

---

## 2. ORIGINE DE LA CONFUSION

La confusion provient probablement d'un raisonnement analogique :

1. $E = mc^2$ → la masse a une énergie maximale
2. $P_{\rm max} = c^5/G$ → l'onde a une puissance maximale
3. La TTC a 3 champs scalaires → « 3 »
4. L'analogie $E=mc^2$ (exposant 2) ↔ $P_{\rm max} = c^5/G$ (exposant 5)
5. Donc $3^5 = 243$ serait « l'analogue computationnel »

Ce raisonnement est **fallacieux**. Les exposants physiques ($c^2$, $c^5$) n'ont
aucun rapport avec le nombre de champs de la théorie. On pourrait tout aussi
bien dire $3^2 = 9$ (pour $E=mc^2$) ou $3^8 = 6561$ (pour le tenseur de Riemann).
Ce sont des **coïncidences sans signification physique**.

---

## 3. LA VÉRITABLE SIGNIFICATION DE $P_{\rm max} = c^5/G$

La combinaison $c^5/G$ est la **puissance de Planck** — connue depuis Max Planck
(1899). Elle émerge de l'analyse dimensionnelle :

$$P_{\rm Planck} = \frac{c^5}{G} = \frac{M_{\rm Planck} \cdot c^2}{t_{\rm Planck}}$$

où $M_{\rm Planck} = \sqrt{\hbar c/G}$ et $t_{\rm Planck} = \sqrt{\hbar G/c^5}$.

La TTC **ne dérive pas** cette formule. Elle l'interprète physiquement comme :

> La puissance maximale qu'une onde peut transporter avant que la cohérence
> de la Toile ne se rompe et ne forme un trou noir.

L'apport de la TTC est :
1. Le mécanisme de **rupture de cohérence** comme origine de la limite
2. Le coefficient $\alpha_{\rm TTC} = 1$ (vs $\alpha = 1/4$ pour Gibbons-Schiller)
3. Le lien d'unification masse ($E=mc^2$) ↔ onde ($P_{\rm max}=c^5/G$) via $\Gamma$

**Aucun de ces apports n'implique le nombre 243.**

---

## 4. QUE FAIRE DU $P_{\rm max}$ DISCRET ?

Pour les applications sur graphes (TTC discrète), $P_{\rm max}$ n'a **pas**
de valeur numérique dérivée de $c^5/G$. La puissance sur un graphe est une
quantité abstraite, mesurée en unités arbitraires.

### Recommandation

1. **Renommer** la constante : `P_MAX_COMPUTATIONAL` (pas `P_MAX` tout court)
2. **Documenter** le commentaire :
   ```
   // P_MAX_COMPUTATIONAL : seuil de saturation numérique pour le solveur
   // sur graphe. AUCUN lien avec la constante physique c⁵/G.
   // La valeur 243 = 3⁵ est heuristique (3 champs TTC).
   // À RECALIBRER par domaine d'application.
   ```
3. **Ne pas** faire référence à $c^5/G$ dans le code de graphes
4. **Si** un lien physique est souhaité, dériver $P_{\rm max}^{\rm discret}$ depuis
   les paramètres du graphe ($\max \Gamma_i$, $\max w_{ij}$, connectivité), pas
   depuis $c^5/G$

### Calibration pratique

Pour un graphe de connaissance à $N$ nœuds :

$$P_{\rm max}^{\rm discret} = N \cdot \max_i |\Gamma_i|^2 \cdot \max_{ij} w_{ij}$$

C'est une limite de stabilité numérique : si le flux d'énergie calculé dépasse
cette valeur, le solveur diverge. Cette définition est **opérationnelle**,
pas fondamentale.

---

## 5. CORRECTIF POUR LES DOCUMENTS TTC

### Documents à corriger

| Document | Correction |
|----------|-----------|
| `TTC-note-Pmax-c5-sur-G.md` | Ajouter un avertissement : « La valeur $3^5=243$ est une heuristique numérique SANS lien avec $c^5/G$. » |
| `TTC-puissance-max-onde.md` | Clarifier que $P_{\rm max} = c^5/G$ est la constante physique de Planck. La TTC l'interprète, ne la dérive pas. |
| Code KontEx (`coherence.rs`) | Renommer `P_MAX` en `P_MAX_COMPUTATIONAL`, documenter l'absence de lien avec $c^5/G$ |
| `TTC-demo-Pmax-etape-par-etape.md` | Ajouter une note de bas de page sur la distinction |

### Ce qu'il ne faut PAS faire

- ❌ Continuer à propager $3^5 = 243$ comme « preuve » que la TTC prédit $c^5/G$
- ❌ Laisser le commentaire « $c^5/G$ computational analog » sans correction
- ❌ Prétendre que $243$ est une constante fondamentale de la TTC

### Ce qu'il faut faire

- ✅ Documenter $P_{\rm max} = c^5/G$ comme une réinterprétation TTC d'une
  constante de Planck connue
- ✅ Documenter $P_{\rm max}^{\rm discret} = 243$ comme un seuil de saturation
  numérique heuristique, recalibrable
- ✅ Tracer une frontière claire entre les constantes physiques (TTC physique)
  et les paramètres numériques (TTC discrète)

---

## 6. LEÇON POUR LA TTC

Cette erreur illustre un problème plus général : la TTC v1.0 mélange
**dérivation physique**, **interprétation analogique** et **heuristique
numérique** sans les distinguer clairement.

La v1.1 doit introduire une **taxonomie explicite** :

| Type d'énoncé | Exemple | Statut |
|---------------|---------|--------|
| **Dérivé** | $\oint\nabla\Phi\cdot d\mathbf{l}=2\pi n \Rightarrow$ Schrödinger | Découle du lagrangien |
| **Interprété** | $P_{\rm max}=c^5/G$ comme limite de rupture de cohérence | Lecture TTC d'une constante connue |
| **Heuristique** | $P_{\rm max}^{\rm discret}=243$ | Paramètre numérique pratique, pas une constante |

---

*Note rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*À ajouter en annexe du White Paper v1.1.*
