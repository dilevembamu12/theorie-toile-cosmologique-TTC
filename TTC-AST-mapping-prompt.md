# PROMPT D'IMPLÉMENTATION — Mapping AST → TTC
## Prise en charge des 17 328 arêtes AST dans le vocabulaire TTC

**Contexte :** Audit KontEx du 2026-08-04 — Cassure #X1  
**Score actuel :** 5/10 → **Cible :** 8/10 après implémentation  
**Fichiers concernés :** `core/src/engine/ast_mapper.rs` (nouveau), `core/src/engine/propagation.rs` (modification), `core/src/engine/field_solver.rs` (modification)

---

## 🎯 Objectif du prompt

Ce document est un **prompt d'implémentation exécutable** destiné à un agent IA (DeepSeek, Claude, GPT-4, etc.) ou à un développeur Rust. Il contient toutes les formules, les tables de mapping, les cas limites et le pseudocode nécessaires pour transformer les arêtes AST en arêtes TTC avec ancrage physique dans les champs $\Gamma$, $\Phi$, $T$.

---

## 1. FONDEMENT THÉORIQUE

### 1.1 Rappel du lagrangien MCW-1

$$\mathcal{L}_{\mathcal{W}} = -\frac12 g^{\mu\nu}\partial_\mu\Gamma\partial_\nu\Gamma - \frac12 \Gamma^2 g^{\mu\nu}\partial_\mu\Phi\partial_\nu\Phi - \frac12 g^{\mu\nu}\partial_\mu T\partial_\nu T - U(\Gamma,T)$$

$$U(\Gamma,T) = \frac{\alpha}{4}(\Gamma^2 - v_\Gamma^2)^2 + \frac{\beta}{2}(T - v_T)^2 + \lambda T\Gamma^2$$

### 1.2 Principe d'ancrage

> **Toute relation dans le graphe DOIT être ancrée dans au moins un champ physique ($\Gamma$, $\Phi$, $T$).** Une relation sans ancrage est une « connexion sombre » — invisible à la physique TTC, non soumise aux lois de conservation.

### 1.3 Courant de phase discret

$$J_{ij} = \Gamma_i^2 \cdot w_{ij} \cdot (\Phi_j - \Phi_i)$$

avec $w_{ij} \in [0, 1]$ le poids du lien, $\Gamma_i$ la cohérence au nœud source, $\Phi_i$ la phase au nœud source.

**Loi de conservation (Kirchhoff-TTC) :**

$$\forall i : \left|\sum_{j \in \mathcal{N}_{\text{out}}(i)} J_{ij} - \sum_{k \in \mathcal{N}_{\text{in}}(i)} J_{ki}\right| < \varepsilon$$

où $\varepsilon = 10^{-6}$ et $\mathcal{N}_{\text{out}}(i)$ / $\mathcal{N}_{\text{in}}(i)$ sont les voisins sortants/entrants du nœud $i$.

---

## 2. TABLE DE MAPPING AST → TTC

### 2.1 Mapping principal (7 relations AST)

| # | Relation AST | → Relation TTC | Champ(s) ancré(s) | Direction | Confiance |
|---|-------------|----------------|-------------------|-----------|:---------:|
| 1 | `extends` | `refines` | $\Gamma$ | $A \to B$ (enfant → parent) | 0.98 |
| 2 | `implements` | `exemplifies` | $\Gamma$ | $A \to B$ (impl → interface) | 0.97 |
| 3 | `injects` | `depends_on` | $T$ | $A \to B$ (consommateur → fournisseur) | 0.95 |
| 4 | `calls` | `references:directed` | $\Phi$ | $A \to B$ (appelant → appelé) | 0.85 |
| 5 | `instantiates` | `instantiates` | $\Gamma$, $T$ | $A \to B$ (constructeur → classe) | 0.92 |
| 6 | `throws` | `depends_on` | $T$ | $A \to B$ (thrower → exception) | 0.90 |
| 7 | `decorates` | `refines` | $\Gamma$ | $A \to B$ (décorateur → décoré) | 0.93 |

### 2.2 Sous-typage de `references`

La relation `references` est scindée en deux sous-types car la physique diffère :

| Sous-type | Symétrie de $J_{ij}$ | Usage | Formule |
|-----------|:---:|-------|---------|
| `references:bidirectional` | $J_{ij} = -J_{ji}$ | Imports mutuels, dépendances cycliques légitimes | Standard |
| `references:directed` | $J_{ij} \geq 0$, $J_{ji} = 0$ | Appels de fonction, flux unidirectionnel | $J_{ij} = \Gamma_i^2 \cdot w_{ij} \cdot \max(\Phi_j - \Phi_i, 0)$ |

### 2.3 Nouvelle relation TTC : `instantiates`

La TTC v1.0 définit 5 relations. Le mapping AST en nécessite une 6ᵉ :

$$\boxed{\text{instantiates} : A \xrightarrow{\text{new}} B \quad\Longleftrightarrow\quad \Gamma_B^{\text{(instance)}} = \Gamma_B^{\text{(classe)}} \cdot e^{-\kappa \cdot T_A}}$$

où $\kappa$ est le paramètre d'amortissement de la tension (MCW-3). L'acte d'instanciation consomme de la tension $T_A$ pour créer de la cohérence $\Gamma_B$.

---

## 3. FORMULES D'INITIALISATION DES CHAMPS

Pour chaque arête convertie, les champs $\Gamma$, $\Phi$, $T$ doivent être initialisés au nœud **cible** (celui pointé par la flèche). Les formules ci-dessous sont les valeurs **initiales** — le solveur TTC les fera évoluer ensuite.

### 3.1 `extends` → `refines`

$$\boxed{\begin{aligned}
\Gamma_B^{\text{(init)}} &= \Gamma_A \cdot (1 + \delta_{\text{extends}}) \\[4pt]
\Phi_B^{\text{(init)}} &= \Phi_A \\[4pt]
T_B^{\text{(init)}} &= T_A + \alpha_{\text{inh}} \cdot (\Gamma_B - \Gamma_A)^2
\end{aligned}}$$

| Paramètre | Valeur | Signification |
|-----------|--------|---------------|
| $\delta_{\text{extends}}$ | $0.05$ | Incrément de cohérence par niveau d'héritage |
| $\alpha_{\text{inh}}$ | $0.1$ | Coefficient de tension d'héritage |

### 3.2 `implements` → `exemplifies`

$$\boxed{\begin{aligned}
\Gamma_B^{\text{(init)}} &= \Gamma_A \cdot \eta_{\text{impl}} \\[4pt]
\Phi_B^{\text{(init)}} &= 0 \quad \text{(nouvelle phase — rupture du contrat)} \\[4pt]
T_B^{\text{(init)}} &= T_{\text{base}} + \lambda \cdot (\Gamma_A - \Gamma_B)^2
\end{aligned}}$$

| Paramètre | Valeur | Signification |
|-----------|--------|---------------|
| $\eta_{\text{impl}}$ | $0.7$ | Facteur de concrétisation (l'interface est plus « cohérente » que l'implémentation) |
| $T_{\text{base}}$ | $0.1$ | Tension plancher |

### 3.3 `injects` → `depends_on`

$$\boxed{\begin{aligned}
\Gamma_B^{\text{(init)}} &= \Gamma_B \quad \text{(inchangé)} \\[4pt]
\Phi_B^{\text{(init)}} &= \Phi_B \quad \text{(inchangé)} \\[4pt]
T_A^{\text{(init)}} &= T_A + \Delta T_{\text{inject}} \\[4pt]
\Delta T_{\text{inject}} &= \lambda \cdot \Gamma_B^2 \cdot w_{AB}
\end{aligned}}$$

L'injection **augmente la tension du consommateur** $T_A$ proportionnellement à la cohérence du fournisseur $\Gamma_B^2$. Plus le fournisseur est « cohérent » (gros service), plus la dépendance est risquée.

### 3.4 `calls` → `references:directed`

$$\boxed{\begin{aligned}
J_{AB}^{\text{(init)}} &= \Gamma_A^2 \cdot w_{AB} \cdot \max(\Phi_B - \Phi_A,\ 0) \\[4pt]
\Phi_B^{\text{(init)}} &= \Phi_B + \frac{J_{AB}}{\Gamma_A^2} \quad \text{(transfert de phase)} \\[4pt]
T_B^{\text{(init)}} &= T_B + \beta \cdot |J_{AB}| \quad \text{(échauffement par le flux)}
\end{aligned}}$$

| Paramètre | Valeur | Signification |
|-----------|--------|---------------|
| $\beta$ | $0.3$ | Coefficient d'échauffement (chaque appel « chauffe » la cible) |

### 3.5 `instantiates` → `instantiates`

$$\boxed{\begin{aligned}
\Gamma_B^{\text{(init)}} &= \Gamma_A \cdot e^{-\kappa \cdot T_A} \\[4pt]
\Phi_B^{\text{(init)}} &= 0 \quad \text{(nouvelle instance, phase vierge)} \\[4pt]
T_B^{\text{(init)}} &= T_A \cdot \gamma_{\text{inst}} \\[4pt]
T_A^{\text{(après)}} &= T_A \cdot (1 - \gamma_{\text{inst}}) \quad \text{(la tension se décharge dans l'instance)}
\end{aligned}}$$

| Paramètre | Valeur | Signification |
|-----------|--------|---------------|
| $\kappa$ | $0.5$ | Amortissement de la tension (MCW-3) |
| $\gamma_{\text{inst}}$ | $0.3$ | Fraction de tension transférée à l'instance |

### 3.6 `throws` → `depends_on`

$$\boxed{\begin{aligned}
T_B^{\text{(init)}} &= T_{\text{max}} \cdot \mathbb{1}_{\text{non-catché}} \\[4pt]
\Delta T_A &= \beta \cdot T_B \quad \text{(rétroaction de tension)}
\end{aligned}}$$

Une exception non-catchée injecte $T = T_{\text{max}} = 1.0$ dans le nœud cible. Si elle est catchée, $T = 0.2$ (tension résiduelle). La rétroaction $\Delta T_A$ augmente la tension de la source (le thrower est « responsable » de la tension qu'il crée).

### 3.7 `decorates` → `refines`

$$\boxed{\begin{aligned}
\Gamma_B^{\text{(init)}} &= \Gamma_A \cdot (1 + \delta_{\text{decorate}}) \\[4pt]
T_B^{\text{(init)}} &= T_A + \lambda \cdot (\Gamma_B - \Gamma_A)^2 \cdot \mathbb{1}_{\text{conflict}}
\end{aligned}}$$

Où $\mathbb{1}_{\text{conflict}} = 1$ si plusieurs décorateurs modifient le même comportement, $0$ sinon. $\delta_{\text{decorate}} = 0.03$.

---

## 4. ALGORITHME DE CONVERSION

### 4.1 Pseudocode principal

```
ALGORITHME: convert_ast_edges_to_ttc(graphe G)
  ENTRÉE: G = (N, E_ast ∪ E_ttc) avec |E_ast| = 17 328, |E_ttc| = 15 837
  SORTIE: G' = (N, E'_ttc) avec |E'_ttc| = 33 165

  POUR CHAQUE arête e = (u, v, type_ast) DANS E_ast:
    1. type_ttc, champs, confiance ← MAPPER(type_ast)
    
    2. SI confiance < 0.80 ALORS
         journaliser("⚠️ Mapping incertain", e, confiance)
         e.meta.requires_review ← true
    
    3. INITIALISER_CHAMPS(v, champs, u, type_ttc)
       // v = cible, u = source
       // Utiliser les formules de la Section 3
    
    4. ANNOTER(e):
       e.ttc_relation    ← type_ttc
       e.ast_original    ← type_ast
       e.converted_at    ← timestamp()
       e.confidence      ← confiance
       e.reversible      ← true
       e.field_anchor    ← champs  // ["Γ"] ou ["Φ"] ou ["T"] ou ["Γ","T"]
    
    5. AJOUTER e à E'_ttc
  
  RETOURNER G'
```

### 4.2 Fonction MAPPER

```
FONCTION MAPPER(type_ast: str) → (TtcRelation, Fields, f64):
  MATCH type_ast:
    "extends"       → (Refines,           [Γ],     0.98)
    "implements"    → (Exemplifies,       [Γ],     0.97)
    "injects"       → (DependsOn,         [T],     0.95)
    "calls"         → (ReferencesDirected,[Φ],     0.85)
    "instantiates"  → (Instantiates,      [Γ, T],  0.92)
    "throws"        → (DependsOn,         [T],     0.90)
    "decorates"     → (Refines,           [Γ],     0.93)
    AUTRE           → (References,        [Φ],     0.50)  // fallback conservateur
```

### 4.3 Fonction INITIALISER_CHAMPS

```
FONCTION INITIALISER_CHAMPS(cible: Node, champs: Fields, source: Node, relation: TtcRelation):
  MATCH relation:
    Refines:
      cible.Γ ← source.Γ * (1 + δ)
      cible.Φ ← source.Φ
      cible.T ← source.T + α_inh * (cible.Γ - source.Γ)²
    
    Exemplifies:
      cible.Γ ← source.Γ * η_impl
      cible.Φ ← 0
      cible.T ← T_base + λ * (source.Γ - cible.Γ)²
    
    DependsOn:
      // Pour injects : la tension augmente chez la SOURCE (consommateur)
      source.T ← source.T + λ * cible.Γ² * w(source, cible)
      // Pour throws : la tension est injectée chez la CIBLE
      cible.T ← IF non_catché ALORS T_max SINON 0.2
    
    ReferencesDirected:
      J ← source.Γ² * w(source, cible) * max(cible.Φ - source.Φ, 0)
      cible.Φ ← cible.Φ + J / source.Γ²
      cible.T ← cible.T + β * |J|
    
    Instantiates:
      cible.Γ ← source.Γ * exp(-κ * source.T)
      cible.Φ ← 0
      cible.T ← source.T * γ_inst
      source.T ← source.T * (1 - γ_inst)   // décharge
    
    References:  // fallback
      cible.Φ ← cible.Φ + 0.01 * (source.Φ - cible.Φ)  // faible couplage
```

---

## 5. VÉRIFICATION POST-CONVERSION

### 5.1 Kirchhoff global

Après conversion, exécuter sur **tous** les 33 165 liens :

```
FONCTION verifier_kirchhoff(G'):
  violations ← []
  
  POUR CHAQUE nœud i DANS G':
    J_out ← Σ_{j ∈ N_out(i)} Γ_i² * w_ij * (Φ_j - Φ_i)
    J_in  ← Σ_{k ∈ N_in(i)}  Γ_k² * w_ki * (Φ_i - Φ_k)
    résidu ← |J_out - J_in|
    
    SI résidu ≥ ε ALORS
      violations.ajouter((i, résidu))
      REDISTRIBUER_RESIDU(i, résidu)
  
  RETOURNER violations

FONCTION REDISTRIBUER_RESIDU(i, résidu):
  SI N_out(i) est vide ALORS RETOURNER
  
  poids_total ← Σ_{j ∈ N_out(i)} w_ij
  POUR CHAQUE j ∈ N_out(i):
    correction ← résidu * (w_ij / poids_total)
    Φ_j ← Φ_j + correction / Γ_i²
```

### 5.2 Vérification de tension

```
FONCTION verifier_tensions(G'):
  alertes ← []
  
  POUR CHAQUE nœud i DANS G':
    SI i.T > 0.7 ALORS
      alertes.ajouter((i, "⚠️ tension élevée", i.T))
    SI i.T > 0.95 ALORS
      alertes.ajouter((i, "🔴 contradiction topologique", i.T))
  
  RETOURNER alertes
```

---

## 6. TRAITEMENT DES CAS LIMITES

### 6.1 Héritage en losange (Diamond Problem)

```
DÉTECTER_DIAMOND(G'):
  POUR CHAQUE nœud D:
    parents ← {p | (D, p, "refines") ∈ E}
    SI |parents| ≥ 2 ALORS
      POUR CHAQUE paire (B, C) dans combinaisons(parents, 2):
        ancêtres_B ← ANCÊTRES(B)
        ancêtres_C ← ANCÊTRES(C)
        communs ← ancêtres_B ∩ ancêtres_C
        
        POUR CHAQUE A dans communs:
          T_D ← T_D + λ * (Γ_B - Γ_C)²
          SI T_D > T_critique ALORS
            journaliser("🔴 Diamond tension", D, A, B, C, T_D)
```

### 6.2 Appels polymorphes

```
RÉSOUDRE_POLYMORPHISME(appelant, méthode_interface):
  implémentations ← {m | (m, méthode_interface, "exemplifies") ∈ E}
  
  SI |implémentations| = 0 ALORS RETOURNER méthode_interface
  
  // Distribution proportionnelle du courant
  poids_total ← Σ_{m ∈ implémentations} w(appelant, m)
  
  POUR CHAQUE m dans implémentations:
    fraction ← w(appelant, m) / poids_total
    J_appelant_m ← J_appelant_interface * fraction
    // Créer arête virtuelle appelant → m si elle n'existe pas
    ASSURER_ARÊTE(appelant, m, "references:directed", J_appelant_m)
```

### 6.3 Dépendances circulaires

```
DÉTECTER_CIRCULARITÉ(G', relation_type="depends_on"):
  // Algorithme de Tarjan pour les composantes fortement connexes
  sccs ← TARJAN(G', filtre_relation="depends_on")
  
  POUR CHAQUE scc dans sccs:
    SI |scc| ≥ 2 ALORS
      POUR CHAQUE nœud i dans scc:
        i.T ← max(i.T, 0.95)  // tension critique
      journaliser("🔴 Dépendance circulaire", scc)
```

---

## 7. PARAMÈTRES GLOBAUX (CONSTANTES MCW-1/2/3)

```rust
// core/src/engine/constants.rs

pub struct TtcParams {
    // MCW-1 — lagrangien fondamental
    pub alpha: f64,        // Auto-interaction Γ (Higgs)
    pub beta: f64,         // Masse T
    pub lambda: f64,       // Couplage Γ–T
    pub v_gamma: f64,      // VEV cohérence
    pub v_t: f64,          // VEV tension
    
    // MCW-2 — extension Φ–T
    pub gamma: f64,        // Couplage Φ–T
    
    // MCW-3 — extension instanciation
    pub kappa: f64,        // Amortissement tension → cohérence
    
    // Mapping AST
    pub delta_extends: f64,    // 0.05 — incrément Γ par héritage
    pub eta_impl: f64,         // 0.70 — facteur concrétisation
    pub alpha_inh: f64,        // 0.10 — coefficient tension héritage
    pub delta_decorate: f64,   // 0.03 — incrément Γ par décorateur
    pub gamma_inst: f64,       // 0.30 — transfert de tension à l'instance
    pub t_base: f64,           // 0.10 — tension plancher
    pub t_critique: f64,       // 0.95 — seuil contradiction topologique
    pub t_elevee: f64,         // 0.70 — seuil alerte tension
    
    // Vérification
    pub epsilon_kirchhoff: f64, // 1e-6 — tolérance conservation
    
    // Confiance mapping
    pub confiance_seuil_revue: f64, // 0.80 — seuil de revue humaine
}

impl Default for TtcParams {
    fn default() -> Self {
        Self {
            alpha: 0.01,
            beta: 0.3,
            lambda: 0.001,
            v_gamma: 1.0,
            v_t: 0.0,
            gamma: 2.0,
            kappa: 0.5,
            delta_extends: 0.05,
            eta_impl: 0.70,
            alpha_inh: 0.10,
            delta_decorate: 0.03,
            gamma_inst: 0.30,
            t_base: 0.10,
            t_critique: 0.95,
            t_elevee: 0.70,
            epsilon_kirchhoff: 1e-6,
            confiance_seuil_revue: 0.80,
        }
    }
}
```

---

## 8. ORDRE D'EXÉCUTION

```
1. CHARGER le graphe G avec E_ast ∪ E_ttc
2. POUR CHAQUE arête AST:
      type_ttc, champs, confiance ← MAPPER(type_ast)
      INITIALISER_CHAMPS(cible, champs, source, type_ttc)
      ANNOTER(arête)
3. VÉRIFIER la conservation Kirchhoff sur G'
      → REDISTRIBUER les résidus si nécessaire
4. EXÉCUTER minimizeEntropy() sur G'
5. VÉRIFIER les tensions (alerte si T > 0.7, critique si T > 0.95)
6. DÉTECTER les diamonds, le polymorphisme, les circularités
7. JOURNALISER les résultats :
      - Nombre d'arêtes converties
      - Nombre d'arêtes à revoir (confiance < 0.80)
      - Nombre de violations Kirchhoff
      - Nombre de tensions élevées / critiques
      - Nombre de diamonds / circularités détectés
8. RETOURNER G'
```

---

## 9. VALIDATION EMPIRIQUE

### 9.1 Critères de succès

| Métrique | Valeur actuelle | Cible après conversion |
|----------|:---:|:---:|
| Arêtes ancrées dans TTC | 15 837 (48%) | **33 165 (100%)** |
| Arêtes avec confiance < 0.80 | — | **< 1%** |
| Violations Kirchhoff ($\varepsilon = 10^{-6}$) | — | **0** (après redistribution) |
| Nœuds avec $T > 0.95$ | 0 | **≥ 5** (attendu dans un codebase réel) |
| Nœuds avec $T > 0.7$ | 0 | **≥ 100** (attendu) |
| Diamonds détectés | — | Tous |
| Circularités détectées | — | Toutes |
| Score de conformité audit | 5/10 | **8/10** |

### 9.2 Invariants à préserver

1. **Aucune arête supprimée** — la conversion est additive, pas destructive
2. **Aucun nœud orphelin créé** — chaque arête convertie connecte des nœuds existants
3. **Réversibilité** — `e.meta.ast_original` permet de retrouver le type AST d'origine
4. **Pas de régression** — les 15 837 arêtes TTC existantes sont inchangées

---

## 10. GLOSSAIRE DES SYMBOLES

| Symbole | Signification | Unité |
|---------|---------------|-------|
| $\Gamma_i$ | Cohérence au nœud $i$ | Sans dimension, $\in [0, 1]$ |
| $\Phi_i$ | Phase au nœud $i$ | Radians, $\in [0, 2\pi)$ |
| $T_i$ | Tension au nœud $i$ | Sans dimension, $\in [0, 1]$ |
| $w_{ij}$ | Poids du lien $i \to j$ | $\in [0, 1]$ |
| $J_{ij}$ | Courant de phase de $i$ vers $j$ | $\Gamma^2 \cdot \text{rad}$ |
| $\alpha$ | Auto-interaction $\Gamma$ (potentiel Higgs) | Sans dimension |
| $\beta$ | Masse de $T$ (rappel élastique) | Sans dimension |
| $\lambda$ | Couplage $\Gamma$-$T$ | Sans dimension |
| $\kappa$ | Amortissement $T \to \Gamma$ (MCW-3) | Sans dimension |
| $\varepsilon$ | Tolérance Kirchhoff | Sans dimension |
| $T_{\text{critique}}$ | Seuil de contradiction topologique | 0.95 |
| $T_{\text{max}}$ | Tension maximale (exception non-catchée) | 1.0 |

---

*Prompt généré le 2026-08-04 — DeepSeek V4 Pro (GitHub Copilot)*  
*Destiné à l'équipe KontEx pour l'implémentation du mapping AST → TTC*
