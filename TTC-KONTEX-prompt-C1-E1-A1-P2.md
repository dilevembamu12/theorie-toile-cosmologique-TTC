# PROMPT D'IMPLÉMENTATION — Corrections #C1, #E1, #A1, #P2
## Les 4 chantiers restants de l'audit KontEx du 2026-08-04

> **Contexte :** Audit KontEx 2026-08-04 — score 5/10 → cible 8/10
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Date :** 15 août 2026
> **Fichiers concernés :** `coherence.rs`, `propagation.rs`, `anchoring.rs`,
> `entropy.rs`, `ttcEngine.ts`, `constants.rs`

---

## CHANTIER #C1 — Contradictions dormantes 🔴

### Problème

`coherence::analyze_pairwise()` n'est jamais appelée automatiquement.
Le graphe affiche 0 contradiction sur 33 165 liens — statistiquement
impossible, signe d'une détection jamais exécutée.

### Solution : détection automatique à l'ingestion

```rust
// core/src/engine/coherence.rs — AJOUT

/// Appel automatique lors de l'ingestion d'un nouveau nœud.
/// Vérifie les contradictions avec les K voisins les plus proches
/// (pas tout le graphe — complexité maîtrisée).
pub fn auto_detect_on_ingest(graph: &Graph, new_node: NodeId, k: usize) -> Vec<Alert> {
    let mut alerts = Vec::new();
    let neighbors = graph.top_k_similar(new_node, k); // pgvector cosinus

    for &other in &neighbors {
        let tension = analyze_pairwise(new_node, other);
        if tension > 0.7 {
            alerts.push(Alert::high_tension(new_node, other, tension));
        }
        if tension > 0.95 {
            alerts.push(Alert::contradiction(new_node, other, tension));
            // Annoter le lien comme contradicts
            graph.annotate_edge(new_node, other, RelationType::Contradicts);
        }
    }
    alerts
}

/// À appeler dans processIngestJob(), APRÈS le tissage des liens.
pub fn process_ingest_job_with_detection(job: IngestJob) -> IngestResult {
    let result = process_ingest_job(job);           // ingestion existante
    let alerts = auto_detect_on_ingest(&result.graph,
                                       result.new_node,
                                       DEFAULT_K_NEIGHBORS); // K = 20
    result.with_alerts(alerts)
}
```

### Coût

- Analyse pairwise : O(K) par ingestion, K = 20
- ~0.5 ms par nœud en Rust natif
- Sur 10 000 nœuds : 5 s total — négligeable

### Validation

| Métrique | Avant | Après |
|----------|-------|-------|
| Contradictions détectées | 0 | **> 100 attendues** (0.5–2% des 33 165 liens) |
| Alertes tension > 0.7 | 0 | **> 500 attendues** |

---

## CHANTIER #P2 — Recalibration des paramètres MCW 🔴→🟡

### Problème

$\alpha = 0.01$, $\beta = 0.3$, $\lambda = 0.001$ sont calibrés sur
**10 paires** — statistiquement insignifiant. $\gamma$ a été corrigé
d'un facteur 20× manuellement.

### Solution : calibration en 3 étapes

```typescript
// api/src/services/calibration.ts — NOUVEAU FICHIER

interface CalibrationResult {
  params: TtcParams;
  f1: number;
  auc: number;
  confidenceInterval: [number, number];
  nSamples: number;
}

/**
 * Étape 1 : Constituer le dataset d'étalonnage (≥ 1000 paires).
 * Structure : { assertion, reference, label: "hallucination" | "fiable" }
 */
async function buildCalibrationDataset(minPairs = 1000): Promise<Pair[]> {
  // Sources recommandées :
  //  - TruthfulQA (817 questions, hallucinations générées par 6 LLMs)
  //  - HaluEval (35 000 échantillons, hallucination vs fiable)
  //  - Contradictions logiques synthétiques (A ∧ ¬A → tension garantie)
  //  - Paires KontEx internes (assertions vs docs officielles)
}

/**
 * Étape 2 : Recherche en grille sur les paramètres.
 * Plage × pas choisis pour couvrir l'espace sans explosion combinatoire.
 */
async function gridSearch(dataset: Pair[]): Promise<CalibrationResult[]> {
  const grid = {
    alpha: [0.001, 0.003, 0.01, 0.03, 0.1],      // 5 valeurs
    beta:  [0.1, 0.3, 1.0],                       // 3 valeurs
    lambda: [0.0001, 0.001, 0.01],                // 3 valeurs
    gamma: [0.5, 1.0, 2.0, 4.0],                  // 4 valeurs (Φ–T MCW-2)
  };
  // 5 × 3 × 3 × 4 = 180 combinaisons — faisable en ~1h sur benchmark
  
  const results = [];
  for (const p of combinations(grid)) {
    const { f1, auc } = await evaluateOnDataset(p, dataset);
    results.push({ params: p, f1, auc, ... });
  }
  return results.sort((a, b) => b.f1 - a.f1);
}

/**
 * Étape 3 : Validation croisée 5-fold.
 * Le F1 annoncé doit être la moyenne sur les 5 folds,
 * PAS le meilleur fold (évite le surajustement).
 */
async function crossValidate(params: TtcParams, dataset: Pair[]): Promise<CalibrationResult> {
  const folds = kFold(dataset, 5);
  const f1s = folds.map(fold => evaluateOnDataset(params, fold).f1);
  const meanF1 = mean(f1s);
  const ci = confidenceInterval(f1s, 0.95);
  return { params, f1: meanF1, confidenceInterval: ci, nSamples: dataset.length };
}
```

### Règles d'or

1. **Jamais de calibration sur le dataset de test.** Séparer calibration (60%),
   validation (20%), test (20%).
2. **Documenter chaque changement de paramètre** avec la justification
   (comme le commit « γ : 0.1 → 2.0 » — mais avec les chiffres du benchmark).
3. **Analyse de sensibilité** : pour chaque paramètre, tracer F1 en fonction
   de la valeur. Si F1 est plat → le paramètre n'est pas contraint → le
   supprimer ou le fixer (moins de paramètres = moins de surajustement).

### Livrable

Un rapport de calibration avec : la grille explorée, le F1 optimal, l'intervalle
de confiance à 95%, et les courbes de sensibilité. C'est ce document qui
justifiera les paramètres dans la v2 du White Paper.

---

## CHANTIER #E1 — Minimisation d'entropie continue 🟡

### Problème

`minimizeEntropy()` est manuel. L'entropie croît avec chaque insertion.

### Solution : relaxation automatique par lots

```rust
// core/src/engine/entropy.rs — MODIFICATION

/// Exécute minimizeEntropy automatiquement toutes les N insertions.
/// N = 100 est un compromis entre fraîcheur (entropie basse) et coût.
const RELAXATION_BATCH: usize = 100;

pub struct EntropyRelaxer {
    insertions_since_last: usize,
}

impl EntropyRelaxer {
    pub fn on_node_inserted(&mut self, graph: &Graph) -> Option<RelaxationReport> {
        self.insertions_since_last += 1;
        if self.insertions_since_last >= RELAXATION_BATCH {
            self.insertions_since_last = 0;
            Some(minimize_entropy(graph))
        } else {
            None
        }
    }
}

/// Alternative : relaxation par horloge (background task).
/// Toutes les heures, si le graphe a changé, relaxer.
pub fn start_background_relaxer(graph: Arc<Graph>, interval: Duration) {
    thread::spawn(move || loop {
        thread::sleep(interval);
        if graph.dirty() {
            minimize_entropy(&graph);
            graph.mark_clean();
        }
    });
}
```

### Critère de fraîcheur

Exposer une métrique `entropy_staleness` = nombre d'insertions depuis la
dernière relaxation. Si > 100, le dashboard affiche « ⚠️ Toile non relaxée ».

---

## CHANTIER #A1 — Péremption adaptative par domaine 🟡

### Problème

Demi-vie uniforme de 1 an pour toutes les connaissances. Un théorème
mathématique ne périme jamais ; une spec JavaScript périt en 2 ans.

### Solution : $\lambda_{\text{domaine}}$ par catégorie sémantique

```rust
// core/src/engine/anchoring.rs — MODIFICATION

/// Demi-vies par domaine de connaissance.
/// Extension du cadre TTC : la péremption est une propriété du DOMAINE,
/// pas de l'ancre.
pub enum KnowledgeDomain {
    Mathematics,       // ne périme jamais
    Physics,           // périme très lentement (découvertes, pas d'obsolescence)
    LanguageSpec,      // périme avec les versions (ES6 → ES2024)
    Framework,         // périme vite (versions majeures ~2 ans)
    Library,           // périme moyennement
    CompanyDoc,        // périme moyennement (process internes)
    News,              // périme très vite
}

impl KnowledgeDomain {
    pub fn half_life_days(&self) -> f64 {
        match self {
            KnowledgeDomain::Mathematics  => f64::INFINITY,
            KnowledgeDomain::Physics      => 10.0 * 365.0,   // 10 ans
            KnowledgeDomain::LanguageSpec => 3.0 * 365.0,    // 3 ans
            KnowledgeDomain::Framework    => 1.0 * 365.0,    // 1 an
            KnowledgeDomain::Library      => 1.5 * 365.0,    // 18 mois
            KnowledgeDomain::CompanyDoc   => 1.0 * 365.0,
            KnowledgeDomain::News         => 30.0,           // 30 jours
        }
    }
}

/// La formule de péremption devient :
/// freshness = exp(-λ_domaine · Δt)
/// où λ_domaine = ln(2) / half_life_days(domaine)
pub fn freshness_with_domain(source: &Source, domain: KnowledgeDomain,
                             now: DateTime) -> f64 {
    let lambda = LN2 / domain.half_life_days();
    (-lambda * source.age_days(now)).exp()
}
```

### Attribution du domaine

Le domaine est détecté automatiquement à la création de l'ancre :
- URI `*.w3.org`, `*.whatwg.org`, `*.ecma-international.org` → `LanguageSpec`
- URI `docs.rs`, `pkg.go.dev`, `mvnrepository.com` → `Library`
- URI `mathworld.wolfram.com`, `proofwiki.org` → `Mathematics`
- Sinon : heuristique par embedding (classifieur simple, ou LLM prompté)

### Conséquence TTC

La force d'ancrage devient :

$$\text{strength}(n) = \min\left(1, \frac{\sum_s \text{quality}(s) \cdot e^{-\lambda_{\text{dom}(s)} \Delta t_s}}{\max(|\text{sources}|,1)}\right)$$

C'est une **généralisation** de la formule du White Paper §2 — à intégrer
dans la v2.

---

## ORDRE D'EXÉCUTION RECOMMANDÉ

```
1. #C1 — Détection automatique (critique, 1 jour)
2. #P2 — Calibration 1000 paires (critique, 1 semaine)
3. #E1 — Relaxation par lots (simple, ½ jour)
4. #A1 — Péremption par domaine (simple, 1 jour)
```

---

*Prompt rédigé par DeepSeek V4 Pro, 15 août 2026.*
