# MCW-3 — ROADMAP & ANALYSE DE SCALING
## Résoudre le problème de Tully-Fisher dans la TTC

> **Date :** 31 juillet 2026
> **Statut :** Itération 1 terminée — scaling identifié, solveur BVP à stabiliser.
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)

---

## 1. RAPPEL DU PROBLÈME

La TTC (MCW-2) passe 2/3 tests falsificateurs. Le test Tully-Fisher échoue :
- Scatter en $v^4/M_b$ : 0.28–0.43 dex (attendu < 0.15 dex)
- La prescription simple $\Gamma^2 \propto \rho_b$ donne une pente **négative** (−0.34)

**Cause racine :** La TTC n'a pas de prescription qui détermine l'amplitude $A$ de la queue asymptotique $\Gamma \sim A/r$ en fonction de $M_b$. Sans cette relation $A(M_b)$, le scatter de Tully-Fisher est inévitable.

---

## 2. LE MÉCANISME MCW-3

### 2.1 Équation maîtresse

En symétrie sphérique statique, l'EDP de $\Gamma$ est :

$$\boxed{\frac{1}{r^2}\partial_r(r^2\partial_r\Gamma) = \Gamma(\partial_r\Phi)^2 + \alpha\Gamma(\Gamma^2 - v_\Gamma^2) - S_\Gamma(r)}$$

avec :
- $\partial_r\Phi = K/(r^2\Gamma^2)$ (conservation de la phase)
- $S_\Gamma(r) = \kappa \cdot v_\Gamma \cdot \rho_b(r)/\rho_b^{\max}$ (source baryonique)

### 2.2 Comportement asymptotique

Loin de la galaxie ($S_\Gamma \to 0$, $\Gamma \to v_\Gamma$) :

$$\frac{1}{r^2}\partial_r(r^2\partial_r\Gamma) \approx \Gamma \cdot \frac{K^2}{r^4\Gamma^4}$$

Pour $\Gamma = v_\Gamma + \delta\Gamma$ avec $\delta\Gamma \ll v_\Gamma$ :

$$\partial_r(r^2\partial_r\delta\Gamma) \approx \frac{K^2}{v_\Gamma^3 r^2}$$

D'où $\delta\Gamma \propto 1/r$ asymptotiquement. **Le profil $\Gamma \propto 1/r$ est bien une solution du régime linéarisé.**

### 2.3 Amplitude $A$ en fonction de $M_b$

L'amplitude $A$ de la queue $\Gamma \sim v_\Gamma + A/r$ est déterminée par l'intégrale de la source :

$$A \propto \int_0^\infty S_\Gamma(r) \cdot r^2 \, dr \propto \kappa \cdot M_b$$

**Donc $A \propto M_b$.** C'est le chaînon manquant. La constante de proportionalité dépend de $\alpha$, $v_\Gamma$, et de la structure interne de $\rho_b(r)$.

### 2.4 Vitesse asymptotique

$$v_\infty^2 = \lim_{r\to\infty} \frac{G M_{\rm dyn}(<r)}{r}$$

où $M_{\rm dyn} = M_b + M_{\mathcal W}$, et $M_{\mathcal W}$ est la contribution du champ TTC.

Pour $\Gamma \sim v_\Gamma + A/r$ :
- $\partial_r\Phi \propto 1/(r^2\Gamma^2) \approx 1/(r^2 v_\Gamma^2)$ 
- La densité d'énergie $\rho_{\mathcal W} \approx \frac12 \Gamma^2(\partial_r\Phi)^2 \propto 1/r^2$
- $M_{\mathcal W}(<r) \propto r$ → $v^2 \propto$ constant ✓

Et $v_\infty \propto A \propto M_b$ → $v_\infty^4 \propto M_b$ ✓✓

---

## 3. PROBLÈMES DE SCALING — DIAGNOSTIC DE L'ITÉRATION 1

Le solveur BVP actuel (`mcw3_solver_iter1.py`) ne converge PAS. Causes identifiées :

### 3.1 Normalisation de $\Phi'$

**Problème :** $\Phi'$ a des dimensions physiques. Dans l'équation :
$$\partial_r\Phi = \frac{K}{r^2\Gamma^2}$$

$K$ a pour dimension $[\Gamma^2 \cdot L^2]$. Si $\Gamma \sim v_\Gamma$ et $r \sim$ kpc, alors $K \sim v_\Gamma^2 \cdot (\text{kpc})^2$.

Pour une galaxie, $K \sim G M_b / v_\Gamma^2$ (en unités normalisées). Pour NGC 2403 : $M_b \sim 10^{13} M_\odot$, $G = 4.3\times10^{-9}$ kpc·(km/s)²/M⊙, donc $K \sim 4.3\times10^4$. Cette valeur est énorme comparée à $v_\Gamma^2 = 1$, ce qui fait exploser le terme $\Gamma(\partial_r\Phi)^2$.

**Solution :** Adimensionner. Définir $\tilde{r} = r/r_0$, $\tilde{\Gamma} = \Gamma/v_\Gamma$, $\tilde{\Phi} = \Phi/\Phi_0$. Choisir $r_0$ et $\Phi_0$ pour que tous les termes soient $O(1)$.

### 3.2 Échelles caractéristiques

| Quantité | Symbole | Valeur typique (NGC 2403) |
|----------|---------|--------------------------|
| Masse baryonique | $M_b$ | $1.3 \times 10^{13}\,M_\odot$ |
| Rayon du disque | $r_d$ | $\sim 5$ kpc |
| Vitesse de rotation | $v_\infty$ | $\sim 130$ km/s |
| Rayon de cœur (fit) | $r_c$ | $\sim 5$ kpc |

Échelles TTC dérivées :
- $r_0 = r_d \sim 5$ kpc
- $v_\Gamma$ normalisé à 1
- $\Phi_0 = G M_b / (r_0 v_\Gamma^2)$ — à déterminer

### 3.3 Instabilité du terme $\Gamma(\partial_r\Phi)^2$

Ce terme couple $\Gamma$ et $\Phi'$ de façon **positive** : plus Γ est grand, plus Φ' dépend de Γ (via $1/\Gamma^2$), et plus (Φ')² est grand, ce qui pousse Γ encore plus haut. C'est une boucle de rétroaction positive.

**Solution :** Résoudre l'équation de Φ **implicitement** plutôt que de la découpler. Le système couplé doit être résolu comme un BVP non linéaire, pas par point fixe.

---

## 4. PLAN POUR LES ITÉRATIONS SUIVANTES

### Itération 2 — Scaling correct + solveur stabilisé
- [ ] Adimensionner complètement les équations
- [ ] Utiliser une méthode de **continuation** : partir de $\alpha = 0$, $\kappa = 0$ (solution triviale $\Gamma = v_\Gamma$) et augmenter progressivement
- [ ] Stabiliser avec sous-relaxation adaptative ($\eta$ qui diminue si le résidu augmente)
- [ ] Tester sur 1 galaxie (NGC 2403) jusqu'à convergence
- [ ] Vérifier $\Gamma \propto 1/r$ asymptotiquement

### Itération 3 — Calibration et batch 10 galaxies
- [ ] Déterminer $\kappa$ optimal sur 10 galaxies
- [ ] Vérifier que $\kappa$ est UNIVERSEL (même valeur pour toutes)
- [ ] Extraire $v_\infty$ et comparer à $M_b$ → pente et scatter TF
- [ ] Si scatter < 0.20 dex → succès préliminaire

### Itération 4 — 150 galaxies et verdict
- [ ] Exécuter sur les 150 galaxies SPARC
- [ ] Mesurer pente et scatter de la relation $v_\infty$ vs $M_b$
- [ ] Si succès : MCW-3 validé, score 3/3
- [ ] Si échec : identifier la physique manquante

### Itération 5 (si nécessaire) — Raffinement
- [ ] Ajouter le champ $T$ (couplage complet Γ-Φ-T)
- [ ] Effets de back-reaction métrique
- [ ] Dépendance environnementale (amas, vide)

---

## 5. LIVRABLES DE L'ITÉRATION 1

| Fichier | Contenu | Statut |
|---------|---------|--------|
| `mcw3_solver_iter1.py` | Solveur BVP (structure correcte, diverge) | 🟡 À stabiliser |
| `TTC-MCW3-roadmap.md` | Ce document — analyse et plan | ✅ |

---

## 6. NOTE THÉORIQUE : LE RÔLE DE $v_\Gamma$

Une question fondamentale : $v_\Gamma$ est-elle une constante fondamentale ou un paramètre effectif ?

Dans la TTC, $v_\Gamma$ est le VEV de cohérence — la valeur de $\Gamma$ dans le vide. Si $v_\Gamma \sim M_{\rm Planck}$ (échelle gravitationnelle), alors $\Gamma$ est énorme comparé aux échelles galactiques, et les effets TTC sont minuscules. Mais si $v_\Gamma$ est un paramètre effectif qui dépend de l'échelle (comme la constante de couplage en QCD), alors $v_\Gamma^{\rm gal} \ll M_{\rm Planck}$.

**Hypothèse pour MCW-3 :** $v_\Gamma$ n'est PAS une constante fondamentale unique. Elle dépend de l'échelle d'énergie du système. Pour les galaxies, $v_\Gamma^{\rm gal} \sim v_\infty / c \times M_{\rm Planck}$ — à déterminer empiriquement.

---

*Roadmap rédigée par DeepSeek V4 Pro, 31 juillet 2026.*
*Prochaine session : Itération 2 — adimensionnement et solveur stabilisé.*
