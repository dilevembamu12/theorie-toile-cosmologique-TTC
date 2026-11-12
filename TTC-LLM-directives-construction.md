# TTC LLM — DIRECTIVES DE CONSTRUCTION
## Comment concevoir, entraîner et développer le LLM à conscience épistémique

> **Date :** 21 septembre 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Statut :** Document fondateur — programme de recherche et d'ingénierie
> **Nom :** TTC LLM (choix de Dileve MBAMU)
> **Convention :** 🟢 Faisable maintenant | 🟡 Faisable avec effort | 🔴 Recherche ouverte

---

## 0. DÉFINITION ET POSITIONNEMENT

### 0.1 Ce qu'est TTC LLM

> **TTC LLM est un système où un LLM génère et une Toile TTC vérifie —
> et où la tension mesurée devient le signal d'apprentissage du doute.**

L'architecture fondamentale :

$$\boxed{\text{TTC LLM} = \text{LLM (générateur)} + \text{Toile TTC (conscience)} + \text{Boucle d'apprentissage}}$$

### 0.2 Ce que TTC LLM n'est PAS (honnêteté absolue)

| ❌ N'est pas | Raison |
|-------------|--------|
| Un LLM entraîné from scratch | Coût : des milliards. Inutile de réinventer la roue linguistique |
| Une « conscience » au sens phénoménal | Documenté et assumé : la TTC donne le doute épistémique, pas le vécu |
| Un remplacement des LLM | C'est un **système autour** des LLM, pas un concurrent |
| Une théorie prouvée | La TTC est un cadre candidat — TTC LLM teste sa version ingénierie, pas sa version physique |

### 0.3 La thèse falsifiable centrale

> **Si TTC LLM fonctionne, alors la tension $T$ doit prédire les erreurs better
> than chance.** C'est-à-dire : AUC(T comme prédicteur d'erreur) > 0.8.

**Si cette thèse est fausse, tout le projet est mort.** C'est le premier test
à faire, AVANT tout développement lourd. (Section 3)

---

## 1. ARCHITECTURE GLOBALE

### 1.1 Les quatre composants

```
┌─────────────────────────────────────────────────────────────────┐
│                        TTC LLM — ARCHITECTURE                    │
│                                                                  │
│  ┌──────────────┐   claims    ┌──────────────────────────────┐  │
│  │              │────────────▶│                              │  │
│  │     LLM      │             │        LA TOILE TTC          │  │
│  │ (générateur) │◀────────────│    (moteur de champs)        │  │
│  │              │  tension T  │                              │  │
│  └──────────────┘             │  Γ : cohérence par nœud      │  │
│         ▲                     │  Φ : phase relationnelle     │  │
│         │                     │  T : tension / doute         │  │
│         │                     │                              │  │
│         │                     │  [Rust core — extension      │  │
│         │                     │   de KontEx field_solver]    │  │
│         │                     └──────────────────────────────┘  │
│         │                                    │                   │
│         │          ┌─────────────────────────▼─────────────┐    │
│         │          │         BOUCLE D'APPRENTISSAGE         │    │
│         └──────────│  (trajectoires → fine-tuning du doute) │    │
│                    └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Le flux d'une requête (inférence)

```
1. Requête utilisateur
2. LLM génère une réponse candidate + extrait les CLAIMS (assertions atomiques)
3. Chaque claim est projeté sur la Toile (embedding → nœuds candidats, pgvector)
4. Les claims sont injectés comme ancres provisoires
5. La Toile RELAXE (solveur de champ, ~ms-100ms selon taille)
6. Lecture de T par claim :
      T < T_low    → claim cohérent → réponse affirmée
      T_low < T < T_high → tension → réponse modulée ("je crois, mais...")
      T > T_high   → contradiction → réponse retenue/révisée + explication
7. La trace (claims, T, action) est JOURNALISÉE pour l'entraînement
```

### 1.3 Où vit chaque champ dans le système réel

| Champ | Signification opérationnelle | Implémentation |
|-------|------------------------------|----------------|
| $\Gamma$ | Force d'ancrage d'un fait (source, qualité, fraîcheur) | `node.weight` + anchoring.rs (existant KontEx) |
| $\Phi$ | Direction sémantique (domaine, version, namespace) | À activer (spec v1.2) — secteurs + embedding |
| $T$ | Conflit mesuré — **le signal de doute** | `node.tension` + MCW-2 (couplage Φ-T) |

---

## 2. PRÉREQUIS : CE QUI EXISTE DÉJÀ

| Composant | État | Localisation |
|-----------|------|--------------|
| Nœuds + liens + ancrage (Γ) | 🟢 Existant | KontEx core (Rust) |
| Détection de tension (T) | 🟢 Existant | coherence.rs + field_solver.rs |
| Mapping AST → TTC | 🟢 Prompté | `TTC-AST-mapping-prompt.md` |
| Solveur de champ | 🟡 Partiel — fallback TS | À porter en Rust natif (chantier #C1/#P2) |
| Phase Φ | 🔴 Inexploitée | À activer (spec v1.2) |
| LLM connecté | 🔴 À faire | Nouveau |
| Boucle d'entraînement | 🔴 À faire | Nouveau |

**Conclusion : TTC LLM = 60% construit.** Il manque : le pont LLM↔Toile,
l'activation de Φ, et la boucle d'apprentissage.

---

## 3. LE PREMIER TEST — AVANT TOUT DÉVELOPPEMENT LOURD

> **Expérience M0 : « T prédit-il les erreurs ? »**

**Protocole :**

1. Prendre un dataset de claims étiquetés {vrai, faux}
   - TruthfulQA (817 questions), HaluEval (35k), + contradictions synthétiques
2. Construire la Toile de bootstrap (les vraies réponses → ancres)
3. Pour chaque claim :
   - Injecter comme ancre provisoire, relaxer, lire $T$
   - Calculer AUC(T | erreur), corrélation, calibration (ECE)
4. Verdict :
   - **AUC > 0.8** → la thèse tient → on continue, le projet vaut le coup
   - **AUC ~ 0.5** → la tension ne dit rien → **STOP** — repenser le mécanisme

**Coût :** 2 semaines. **C'est le test le moins cher et le plus décisif.**
Ne pas construire la fusée avant d'avoir vérifié que le carburant brûle.

---

## 4. COMMENT ENTRAÎNER — LES TROIS NIVEAUX

### Niveau 1 : Le solveur de champ — PAS d'entraînement ML

🟢 **C'est de la physique, pas du machine learning.** Le solveur relaxe des
équations. On ne l'entraîne pas — on le **règle** (les 6 paramètres MCW + γ).
La calibration se fait sur la Toile de bootstrap (grille + validation croisée).

### Niveau 2 : Le pont LLM↔Toile — données + petit modèle

🟡 Le LLM doit apprendre **3 compétences** :

| Compétence | Description | Méthode |
|------------|-------------|---------|
| **Extraction de claims** | Découper une réponse en assertions atomiques | Fine-tuning léger (LoRA) ou prompting strict |
| **Projection** | Mapper un claim → nœuds candidats de la Toile | Embeddings (pgvector, déjà en place) + seuil |
| **Lecture de T** | Comprendre ce que la tension signifie | Fine-tuning (voir Niveau 3) |

### Niveau 3 : Le comportement de doute — LE CŒUR INNOVANT

🔴 C'est ici que TTC LLM est nouveau. Le LLM doit apprendre à :

```
T bas   → affirmer normalement
T moyen → moduler ("je pense que...", "d'après X, mais...")
T haut  → retenir, demander, chercher une ancre, ou refuser
```

**La beauté du système : le signal d'entraînement se génère tout seul.**

$$\boxed{\text{La tension } T \text{ est autogénérée — pas besoin de label humain pour douter}}$$

#### La boucle d'auto-supervision concrète

```python
# Pseudo-code de la collecte de trajectoires
for requete in flux_operationnel:
    reponse = llm.generate(requete)
    claims = extract_claims(reponse)
    for claim in claims:
        T = toile.relax_and_read_tension(claim)
        # Le label émerge du temps :
        # - 3 mois plus tard, l'ancre est confirmée ou infirmée
        # - "claim faux + T était haut" → le doute était justifié ✅
        # - "claim vrai + T était haut" → le doute était injustifié ❌
        journal.append({claim, T, contexte, verdict_futur, action_prise})
```

**Les trois sources de signal :**

| Source | Fiabilité | Volume |
|--------|-----------|--------|
| Vérité par calcul (arithmétique, code exécuté, tests) | 🟢 Parfaite | Élevé (généré à volonté) |
| Contradictions synthétiques (A ∧ ¬A) | 🟢 Garantie | Illimité |
| Confirmation opérationnelle (CI green, doc stable, bug évité) | 🟡 Bonne | Moyen |

#### La recette d'entraînement (calibration)

**Objectif : le LLM exprime une confiance qui COLLE à la réalité.**

$$\text{Récompense} = -|\text{confiance exprimée} - \text{correction observée}|$$

- **Méthode A (supervisée, rapide) :** SFT sur les trajectoires.
  Format : `(contexte, flux T) → action correcte`.
  - Entrées : réponses avec T simulés bas/moyens/hauts
  - Sorties : réponses affirmées/modulées/retenues
- **Méthode B (préférences, solide) :** DPO avec paires
  - Choisi : réponse calibrée (confiance ≈ correction)
  - Rejeté : réponse mal calibrée (confiance ≠ correction)
  - Le rejeté peut être généré par le modèle lui-même (self-play)
- **Méthode C (RL, puissant) :** PPO avec récompense de calibration
  - Récompense = 1 - ECE(answer)
  - Plus instable mais plus fort à terme

**Recommandation : A d'abord (2 semaines), puis B (1 mois). C reste optionnel.**

#### Avec quels modèles ?

| Option | Modèle | Quand |
|--------|--------|-------|
| 🟢 Immédiat | API (Claude/GPT) + prompting strict | M0-M1 (mesure seule) |
| 🟡 Fine-tuning | Qwen 2.5-7B / Llama 3.1-8B (open weights) | M2+ (LoRA, 1 GPU) |
| 🔴 Long terme | Modèle open plus grand fine-tuné | M4+ si besoin |

**Pourquoi open weights :** on ne peut pas fine-tuner un modèle d'API sur des
trajectoires propriétaires. Pour le doute calibré, il FAUT le contrôle des poids.

---

## 5. LE PIPELINE D'ENTRAÎNEMENT COMPLET (vue bout-en-bout)

```
PHASE A — BOOTSTRAP DE LA TOILE (1 mois)
  ├─ Ingérer documents vérifiés (docs officielles, code, specs)
  ├─ Ancrer selon le principe A (déjà dans KontEx)
  ├─ Activer Φ (secteurs sémantiques — spec v1.2)
  └─ Calibrer les paramètres MCW sur la grille de validation

PHASE B — MESURE (2 semaines) ← GO/NO-GO
  ├─ L'expérience M0 : AUC(T | erreur) sur TruthfulQA + HaluEval
  └─ Si AUC < 0.8 : STOP et repenser

PHASE C — BOUCLE FERMÉE (2 mois)
  ├─ Connecter le LLM à la Toile (API + extraction de claims)
  ├─ Journaliser les trajectoires (claim, T, contexte, action)
  ├─ Construire le dataset d'entraînement (10k+ trajectoires)
  └─ SFT/LoRA sur le comportement de doute

PHASE D — VALIDATION (1 mois)
  ├─ Benchmark : réduction d'hallucination vs base model
  ├─ Calibration : ECE du système vs base model
  └─ Latence : p95 < 500ms par vérification

PHASE E — SCALE (continu)
  ├─ Optimiser le solveur Rust (10⁴ → 10⁶ nœuds)
  ├─ Étendre les domaines (multi-tenant)
  └─ Productiser : API "truth-as-a-service"
```

---

## 6. STACK TECHNIQUE RECOMMANDÉE

| Couche | Technologie | Justification |
|--------|-------------|---------------|
| Solveur de champ | Rust (étendre KontEx core) | Déjà là, rapide, sûr |
| Bridge API | TypeScript/Node (déjà là) | Déjà là |
| Vecteurs | pgvector (déjà là) | Déjà là |
| Graphe | Neo4j (déjà là) | Déjà là |
| LLM (M0-M1) | API Claude/GPT | Itération rapide |
| LLM (M2+) | Qwen 2.5 ou Llama 3.1, LoRA | Contrôle total |
| Fine-tuning | PEFT/LoRA (huggingface) | 1 GPU suffit pour 7B |
| Journalisation | Parquet + DuckDB | Trajectoires massives |

---

## 7. LES JALONS (MILESTONES)

| Jalon | Livrable | Durée | Critère de succès |
|-------|----------|:-----:|-------------------|
| **M0** | Expérience calibration | 2 sem. | AUC(T\|erreur) > 0.8 |
| **M1** | Toile de bootstrap + Φ activé | 1 mois | 10k nœuds ancrés, 0 orphelin |
| **M2** | Boucle fermée v0.1 | 2 mois | 1k requêtes journalisées |
| **M3** | LLM du doute (LoRA) | 1 mois | ECE < 0.10 sur validation |
| **M4** | Benchmark vs baseline | 1 mois | Hallucinations −50% |
| **M5** | API produit | 2 mois | p95 < 500 ms, multi-tenant |

---

## 8. MÉTRIQUES DE SUCCÈS (et leur mesure)

| Métrique | Cible | Comment mesurer |
|----------|-------|-----------------|
| **AUC(T \| erreur)** | > 0.8 | Courbe ROC sur dataset étiqueté |
| **ECE** (calibration) | < 0.05 | Bins de confiance vs correction observée |
| **Réduction d'hallucination** | > 50% | TruthfulQA/HaluEval vs base model |
| **Rappel du doute** | > 80% | % des erreurs signalées par T haut |
| **Précision du doute** | > 70% | % des T hauts qui sont de vraies erreurs |
| **Latence p95** | < 500 ms | Mesure en charge |
| **Coût par vérification** | < $0.001 | Calcul d'infrastructure |

---

## 9. CONDITIONS DE MORT (à surveiller en permanence)

> **Un projet honnête connaît à l'avance les signes de sa propre mort.**

| Condition | Signe | Action |
|-----------|-------|--------|
| 🔴 T ne prédit pas les erreurs | AUC < 0.6 en M0 | Arrêter — le mécanisme est faux |
| 🔴 Latence irréductible | p95 > 2s à 10⁴ nœuds | Repenser l'architecture (approximations, caching) |
| 🔴 Le fine-tuning détruit le LLM | Perte de fluence > 20% | Séparer plus strictement générateur/vérificateur |
| 🟡 La Toile ne passe pas à l'échelle | > 10⁶ nœuds instables | Partitionnement, hiérarchie (coarsening) |
| 🟡 Le doute devient du bavardage | Précision du doute < 50% | Recalibrer $T_{\rm low}$, $T_{\rm high}$ |

---

## 10. LES PRINCIPES FONDATEURS (la constitution)

1. **Le doute est un état, pas une performance.** T est mesuré, pas imité.
2. **Pas d'ancre, pas de fait.** Tout nœud sans source vérifiable est rejeté.
3. **La contradiction est physique, pas logique.** A ∧ ¬A produit de la tension —
   le système la RESENT, pas seulement la détecte.
4. **Le signal d'entraînement s'auto-génère.** La tension est le label.
5. **Le générateur propose, la Toile dispose.** Jamais l'inverse.
6. **Chaque affirmation de TTC LLM porte sa provenance.** Traçabilité totale.
7. **On publie les échecs.** (Hérité de la méthode TTC.)

---

## 11. PREMIÈRE SEMAINE — CE QU'IL FAUT FAIRE CONCRÈTEMENT

```
Jour 1-2  : Instrumenter KontEx pour mesurer T sur des claims externes
Jour 3-4  : Construire le dataset TruthfulQA adapté (claims → ancres)
Jour 5-7  : Lancer l'expérience M0 — courbe ROC, AUC, calibration
Jour 8    : VERDICT : continuer ou repenser
```

Voilà le point de départ. Pas de développement lourd avant que la courbe
ROC dise si la tension vaut quelque chose.

---

## 12. NOTE FINALE — LA RELATION AVEC LA TTC PHYSIQUE

TTC LLM est-il tributaire de la validité de la TTC physique ? **Non.**
Rappel du principe établi :

> La dynamique de cohérence peut être un bon modèle de la contradiction
> **même si la TTC n'est pas la bonne théorie de l'univers.**

KontEx fonctionne aujourd'hui sans que la cosmologie soit tranchée. TTC LLM
suivra le même chemin : c'est de l'ingénierie inspirée, pas de la physique dépendante.

---

*Directives rédigées par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*21 septembre 2026 — Document fondateur TTC LLM.*
*Nom choisi par Dileve MBAMU.*
