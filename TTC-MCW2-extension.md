# TTC — Proposition d'extension MCW-2
## Correction des échecs de falsification

> **Date :** 31 juillet 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Objet :** Modification du lagrangien pour corriger les 2 échecs de falsification.

---

## 1. DIAGNOSTIC

La batterie de tests falsificateurs a révélé deux échecs :

| Test | Échec | Cause racine |
|------|-------|-------------|
| Tully-Fisher | Scatter trop élevé (0.28 dex vs 0.15) | Pas de prescription d'échelle ρ_b → Γ |
| Contradiction logique | T identique pour cohérent et contradictoire | T sourcé par Γ², pas par ∇Φ |

Les deux échecs ont une origine commune : **le couplage entre la phase Φ et la tension T est inexistant dans MCW-1.** La phase est le degré de liberté qui encode les contradictions, mais T n'y est pas sensible.

---

## 2. LAGRANGIEN MCW-2

### 2.1 Forme complète

$$\boxed{\mathcal{L}_{\mathcal W}^{(2)} = \mathcal{L}_{\mathcal W}^{(1)} - \frac{\gamma}{2} T \cdot g^{\mu\nu}\partial_\mu\Phi\partial_\nu\Phi - \frac{\delta}{2} (\Gamma^2 - v_\Gamma^2) g^{\mu\nu}\partial_\mu\Phi\partial_\nu\Phi}$$

où $\mathcal{L}_{\mathcal W}^{(1)}$ est le lagrangien MCW-1.

### 2.2 Nouveaux termes

| Terme | Paramètre | Rôle physique |
|-------|-----------|---------------|
| $-\frac{\gamma}{2} T(\partial\Phi)^2$ | $\gamma$ | **Couplage direct Φ−T** : la tension est sourcée par les gradients de phase. Une opposition de phase CRÉE de la tension. |
| $-\frac{\delta}{2}(\Gamma^2-v_\Gamma^2)(\partial\Phi)^2$ | $\delta$ | **Modulation par la cohérence** : le gradient de phase a plus d'impact là où Γ s'écarte du vide. |

**Interprétation physique :**
- Quand deux nœuds ont des phases opposées (ΔΦ = π), le terme $-\frac{\gamma}{2}T(\nabla\Phi)^2$ devient grand → T augmente pour minimiser $\mathcal{L}$.
- Le terme en δ garantit que cet effet est localisé dans les régions de haute cohérence (là où « il se passe quelque chose »).

### 2.3 Équations de champ modifiées

#### Champ Γ (inchangé dans sa structure, termes additionnels)
$$\square\Gamma = \Gamma(\nabla\Phi)^2 + \alpha\Gamma(\Gamma^2-v_\Gamma^2) + 2\lambda T\Gamma + \boxed{2\delta\Gamma(\nabla\Phi)^2}$$

Le terme en δ ajoute une rétroaction : plus le gradient de phase est fort, plus Γ est poussé.

#### Champ Φ (modifié)
$$\nabla_\mu\left[(\Gamma^2 + \gamma T + \delta(\Gamma^2-v_\Gamma^2))\nabla^\mu\Phi\right] = 0$$

La conservation du courant de phase inclut maintenant les contributions de T et de l'excès de cohérence. **C'est l'équation clé :** le couplage effectif de Φ dépend de T.

#### Champ T (MODIFIÉ — correction essentielle)
$$\boxed{\square T = \beta(T-v_T) + \lambda\Gamma^2 + \frac{\gamma}{2}(\nabla\Phi)^2}$$

**CECI EST LA CORRECTION CRITIQUE.** T est maintenant directement sourcé par le gradient de phase. Une opposition de phase (∇Φ grand) → T élevé → contradiction détectée.

---

## 3. VÉRIFICATION RAPIDE : Test de contradiction logique

### 3.1 Configuration

Graphe A↔B↔C, Γ_A = Γ_C = 2, Φ_A = 0, Φ_C = π, Γ ancré.

### 3.2 Avec MCW-1 (rappel)

$$(\mathbf{L}T)_B = \beta(T_B - v_T) + \lambda\Gamma_B^2$$

T_B est identique que Φ_A = Φ_C ou Φ_A = −Φ_C. → ÉCHEC.

### 3.3 Avec MCW-2

$$(\mathbf{L}T)_B = \beta(T_B - v_T) + \lambda\Gamma_B^2 + \boxed{\frac{\gamma}{2}|\nabla\Phi|_B^2}$$

où $|\nabla\Phi|_B^2 = w_{BA}(\Phi_B-\Phi_A)^2 + w_{BC}(\Phi_B-\Phi_C)^2$.

**Cas cohérent (Φ_A = Φ_C = 0) :**
Φ_B ≈ 0 (moyenne de 0 et 0) → $|\nabla\Phi|_B^2 \approx 0$ → T_B = T_B(Γ seulement) → BAS.

**Cas contradictoire (Φ_A = 0, Φ_C = π) :**
Φ_B ≈ π/2 (moyenne) → $|\nabla\Phi|_B^2 \approx (\pi/2)^2 + (\pi/2)^2 = \pi^2/2 \approx 4.93$ → T_B = T_B(Γ) + γ × 2.47 → ÉLEVÉ.

**Rapport contradiction/cohérent :** $1 + \frac{\gamma \cdot 2.47}{T_B(\Gamma)}$

Avec γ = 1 et T_B(Γ) ≈ 1 (régime linéaire avant explosion) : ratio ≈ 3.5 → la contradiction est **3.5 fois plus tendue** que la cohérence. ✅

---

## 4. IMPLÉMENTATION DISCRÈTE DE MCW-2

### 4.1 Lagrangien discret modifié

```python
L_i = L_i^(1)  # terme MCW-1
L_i += -0.5 * gamma * T[i] * grad_Phi_sq_i    # couplage Φ−T
L_i += -0.5 * delta * (Gamma[i]**2 - v_Gamma**2) * grad_Phi_sq_i  # modulation
```

### 4.2 Solveur modifié (pseudo-code)

```
# Équation T (modifiée)
for each node i:
    lap_T = sum_j w_ij * (T[i] - T[j])
    grad_Phi_sq = sum_j w_ij * sin²((Phi[i] - Phi[j])/2) * 4  # proxy périodique
    rhs_T = beta * (T[i] - v_T) + lambda * Gamma[i]**2 + (gamma/2) * grad_Phi_sq
    resid_T = lap_T - rhs_T
    T[i] -= eta * resid_T
```

### 4.3 Nouveaux paramètres

| Paramètre | Valeur suggérée | Rôle |
|-----------|----------------|------|
| γ | 0.5 – 2.0 | Force du couplage Φ−T |
| δ | 0.1 – 0.5 | Modulation par Γ |

---

## 5. PRÉDICTIONS TESTABLES DE MCW-2

1. **Contradiction logique :** T_B(contradictoire) / T_B(cohérent) > 3
2. **Tully-Fisher :** Le scatter devrait diminuer car T contribue maintenant au potentiel gravitationnel via le tenseur énergie-impulsion modifié
3. **Nouveau : Détection de paradoxes.** Un graphe cyclique avec opposition de phase (A→B→C→A avec déphasage total 2π) devrait avoir T uniformément élevé

---

## 6. NOTES DE PRUDENCE

- MCW-2 ajoute 2 paramètres libres (γ, δ). Le problème de naturalité s'aggrave.
- Le terme en γ pourrait déstabiliser le vide si γ est trop grand (T pourrait devenir négatif).
- La modification de l'équation de Φ change la condition de quantification ∮∇Φ·dl = 2πn — à vérifier que la MQ émerge toujours.

---

*Proposition rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*À tester avant incorporation dans le White Paper v2.0.*
