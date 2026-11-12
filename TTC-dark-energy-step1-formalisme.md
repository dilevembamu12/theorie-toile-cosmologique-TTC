# TTC ÉNERGIE NOIRE — Étape 1 : LE FORMALISME
## Dérivation complète de ρ_T, p_T, w_T en fond FLRW

> ⚠️ **RÉVOQUÉ — 16 août 2026**
> Ce document contient une erreur interne majeure identifiée par l'agent
> vérificateur : l'ansatz $\Gamma = v_\Gamma$ n'est PAS une solution de
> l'équation du champ $\Gamma$ quand $\lambda \neq 0$ et $T \neq 0$.
> La masse de $T$ n'est pas $\beta$ mais $m_{\rm eff}^2 = \beta - 2\lambda^2/\alpha$.
> **Voir la correction : `TTC-dark-energy-step1.5-correction.md`**
> Ce document est conservé pour l'historique (et pour la pédagogie de l'erreur).

> **Date :** 15 août 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Série :** Roadmap énergie noire — Étape 1/8
> **Statut :** 🔴 RÉVOQUÉ — remplacé par l'Étape 1.5

---

## 1. HYPOTHÈSES DE DÉPART

Dans un univers FLRW homogène et isotrope, après la transition de phase
primordiale ($\Gamma : 0 \to v_\Gamma$), on pose :

| Hypothèse | Justification | Statut |
|-----------|---------------|--------|
| $\Gamma = v_\Gamma$ partout | Le champ de cohérence est gelé à son VEV | 🟢 Standard |
| $\partial_\mu\Phi = 0$ (homogène) | Un $\Phi(t)$ homogène donne un fluide raide $w=1$ dilué en $a^{-6}$ — négligeable aujourd'hui | 🟢 Argument solide |
| $T = T(t)$ homogène | C'est le champ candidat de l'énergie noire | 🟢 Hypothèse de travail |
| Métrique FLRW plate : $ds^2 = -dt^2 + a^2(t)[dr^2 + r^2 d\Omega^2]$ | Cohérent avec les données (Ω_k ≈ 0) | 🟢 Standard |

**Remarque de rigueur :** l'hypothèse $\partial_\mu\Phi = 0$ exclut pour
l'instant les gradients spatiaux de phase. S'ils étaient non nuls, ils
contribueraient $\rho_\Phi = \frac12\Gamma^2|\nabla\Phi|^2/a^2$ — à traiter
dans l'étape 6 (perturbations).

---

## 2. LE LAGRANGIEN EFFECTIF DU SECTEUR $T$

Le lagrangien MCW-1 :

$$\mathcal{L}_{\mathcal W} = -\frac12(\partial\Gamma)^2 - \frac12\Gamma^2(\partial\Phi)^2 - \frac12(\partial T)^2 - U(\Gamma,T)$$

avec $U(\Gamma,T) = \frac{\alpha}{4}(\Gamma^2-v_\Gamma^2)^2 + \frac{\beta}{2}(T-v_T)^2 + \lambda T\Gamma^2$.

Avec $\Gamma = v_\Gamma$ et $\partial\Phi = 0$, seuls survivent les termes en $T$ :

$$\boxed{\mathcal{L}_T = \frac12 \dot T^2 - V_{\rm eff}(T)}$$

> **Dérivation du signe :** $-\frac12 g^{\mu\nu}\partial_\mu T\partial_\nu T$
> avec $g^{00} = -1$ (signature $-,+,+,+$) donne $+\frac12\dot T^2$. Le champ
> $T$ a donc un **terme cinétique standard** (pas de fantôme). ✅

Le potentiel effectif :

$$\boxed{V_{\rm eff}(T) = \frac{\beta}{2}(T - v_T)^2 + \lambda v_\Gamma^2\, T}$$

Les deux contributions :
- $\frac{\beta}{2}(T-v_T)^2$ : rappel quadratique vers le VEV de tension
- $\lambda v_\Gamma^2 T$ : **pente linéaire** — la cohérence du vide « pousse »
  la tension vers le bas

---

## 3. DIMENSIONS (rappel de l'errata v1.1)

| Quantité | Dimension |
|----------|-----------|
| $T$, $v_T$, $v_\Gamma$ | $[E]^1$ (énergie) |
| $\beta$ | $[E]^2$ (masse au carré) — **corrigé de l'errata** |
| $\lambda$ | $[E]^1$ (masse) — **corrigé de l'errata** |

Le potentiel effectif a bien $[E]^4$ : $\beta T^2 \sim E^2 \cdot E^2$ ✓,
$\lambda v_\Gamma^2 T \sim E \cdot E^2 \cdot E$ ✓.

---

## 4. ÉQUATION DU MOUVEMENT

Variation de $S_T = \int d^4x\, a^3 \mathcal{L}_T$ :

$$\boxed{\ddot T + 3H\dot T + \frac{dV_{\rm eff}}{dT} = 0}$$

avec le frottement de Hubble $3H\dot T$ (l'expansion freine la relaxation) et :

$$\frac{dV_{\rm eff}}{dT} = \beta(T - v_T) + \lambda v_\Gamma^2$$

D'où l'équation complète :

$$\boxed{\ddot T + 3H\dot T + \beta(T - v_T) + \lambda v_\Gamma^2 = 0}$$

### 4.1 Le point d'équilibre (tadpole)

Le terme $\lambda v_\Gamma^2$ est une **force constante** (tadpole). L'équilibre
n'est PAS à $T = v_T$ mais à :

$$\boxed{T_{\rm eq} = v_T - \frac{\lambda v_\Gamma^2}{\beta}}$$

### 4.2 Reformulation en déplacement

Posons $X = T - T_{\rm eq}$. L'équation devient :

$$\boxed{\ddot X + 3H\dot X + \beta X = 0}$$

**C'est un oscillateur harmonique amorti** — masse au carré $m_T^2 = \beta$,
frottement $3H$. Le champ oscille autour de $T_{\rm eq}$ avec une fréquence
$\sqrt{\beta}$, amortie par l'expansion.

---

## 5. DENSITÉ D'ÉNERGIE ET PRESSION

Tenseur énergie-impulsion d'un scalaire minimalement couplé :

$$T_{\mu\nu} = \partial_\mu T\,\partial_\nu T + g_{\mu\nu}\mathcal{L}_T$$

En fond FLRW :

$$\boxed{\rho_T = \frac12\dot T^2 + V_{\rm eff}(T)}$$

$$\boxed{p_T = \frac12\dot T^2 - V_{\rm eff}(T)}$$

> **Vérification :** $T_{00} = \dot T^2 + g_{00}\mathcal{L}_T = \dot T^2 - (\frac12\dot T^2 - V_{\rm eff}) = \frac12\dot T^2 + V_{\rm eff}$ ✓
> $p_T = T_{ii}/g_{ii} = \mathcal{L}_T = \frac12\dot T^2 - V_{\rm eff}$ ✓

---

## 6. ÉQUATION D'ÉTAT

$$\boxed{w_T = \frac{p_T}{\rho_T} = \frac{\frac12\dot T^2 - V_{\rm eff}}{\frac12\dot T^2 + V_{\rm eff}}}$$

### 6.1 Cas limites immédiats

| Régime | Condition | w_T |
|--------|-----------|-----|
| Dominé par le potentiel | $\dot T^2 \ll V_{\rm eff}$ | **−1** (constante cosmologique) |
| Dominé par la cinétique | $\dot T^2 \gg V_{\rm eff}$ | **+1** (fluide raide) |
| Équilibre exact | $\dot T = 0$ | **−1** quel que soit $V_{\rm eff} \neq 0$ |

### 6.2 Condition d'accélération

L'équation de Friedmann :

$$\frac{\ddot a}{a} = -\frac{4\pi G}{3}(\rho_T + 3p_T + \rho_m + 2\rho_r)$$

L'accélération ($\ddot a > 0$) requiert $\rho_T + 3p_T < 0$, soit :

$$\boxed{\dot T^2 < V_{\rm eff}(T)}$$

**L'énergie cinétique du champ doit rester sous son énergie potentielle.**
C'est la condition de slow-roll standard.

---

## 7. LE POTENTIEL EFFECTIF EN FORME CANONIQUE

En variable $X = T - T_{\rm eq}$ :

$$\boxed{V_{\rm eff}(X) = V_{\rm min} + \frac{\beta}{2}X^2}$$

avec le **minimum du potentiel** :

$$\boxed{V_{\rm min} = \lambda v_T v_\Gamma^2 - \frac{\lambda^2 v_\Gamma^4}{2\beta}}$$

> **Dérivation :** $V_{\rm eff}(T_{\rm eq}) = \frac{\beta}{2}(-\frac{\lambda v_\Gamma^2}{\beta})^2 + \lambda v_\Gamma^2(v_T - \frac{\lambda v_\Gamma^2}{\beta})$
> $= \frac{\lambda^2 v_\Gamma^4}{2\beta} + \lambda v_T v_\Gamma^2 - \frac{\lambda^2 v_\Gamma^4}{\beta}$
> $= \lambda v_T v_\Gamma^2 - \frac{\lambda^2 v_\Gamma^4}{2\beta}$ ✓

### 7.1 Le signe de $V_{\rm min}$ — point critique

| Cas | $V_{\rm min}$ | Conséquence |
|-----|--------------|-------------|
| $v_T = 0$ | $-\lambda^2 v_\Gamma^4/(2\beta) < 0$ | Le minimum est NÉGATIF — le « vrai vide » de la Toile a une énergie négative |
| $v_T = \lambda v_\Gamma^2/(2\beta)$ | $0$ | Minimum nul |
| $v_T > \lambda v_\Gamma^2/(2\beta)$ | $> 0$ | Minimum positif (de Sitter intrinsèque) |

**Interprétation (hypothèse à travailler aux étapes suivantes) :** si $v_T = 0$
(le choix de normalisation de KontEx et de la spec discrète), le vide de la
Toile a une énergie négative. L'univers observé (avec $\rho_\Lambda > 0$)
correspondrait alors à un champ $T$ **déplacé au-dessus de son minimum** —
un univers qui n'a pas encore atteint son état fondamental. C'est cohérent
avec le scénario de relaxation : le Big Bang a laissé $T$ excité, et l'énergie
noire est le transitoire de cette relaxation.

---

## 8. ANALOGIE FORMELLE : UNE CLASSE DE MODÈLES CONNUE

> 🟢 **Résultat d'identification :** le secteur $T$ de la TTC est formellement
> équivalent à un **scalaire massif sur une pente linéaire** :

$$V(T) = \frac{m_T^2}{2}T^2 + c\cdot T \quad \text{avec} \quad m_T^2 = \beta,\ c = \lambda v_\Gamma^2 - \beta v_T$$

C'est la classe des **« linear quintessence » / axion monodromie** étudiée
dans la littérature (Agrawal et al., Liddle & Scherrer, …). La TTC n'invente
donc pas un objet exotique : elle MOTIVE une classe de potentiels déjà connue,
et — c'est son apport — la relie aux deux autres champs $\Gamma$ et $\Phi$
par le lagrangien unifié.

**Avantage immédiat :** la phénoménologie connue des linear quintessence
s'applique. Leurs limites sur les paramètres s'appliquent. L'étape 3
(classification) pourra s'appuyer sur cette littérature.

---

## 9. LE SYSTÈME COSMOLOGIQUE COMPLET (pour l'étape 2)

Le système couplé à résoudre numériquement :

$$\boxed{\begin{aligned}
\ddot T + 3H\dot T + \beta(T - v_T) + \lambda v_\Gamma^2 &= 0 \\[6pt]
H^2 = \frac{8\pi G}{3}\left(\rho_{m0}a^{-3} + \rho_{r0}a^{-4} + \frac12\dot T^2 + V_{\rm eff}(T)\right)
\end{aligned}}$$

avec les valeurs de référence :
- $\rho_{m0} \approx 3.1\times10^{-11}\ \text{eV}^4$, $\rho_{r0} \approx 2.5\times10^{-15}\ \text{eV}^4$
- Cible : $\rho_T$ aujourd'hui $\approx 2.8\times10^{-11}\ \text{eV}^4$ (≈ (2.3 meV)⁴)

**Deux ODE couplées** — c'est tout le problème. L'étape 2 les résout.

---

## 10. BILAN DE L'ÉTAPE 1

### Acquis ✅

| # | Résultat |
|---|----------|
| 1 | $\rho_T = \frac12\dot T^2 + V_{\rm eff}$, $p_T = \frac12\dot T^2 - V_{\rm eff}$ — dérivé |
| 2 | $w_T = -1 \iff \dot T^2 \ll V_{\rm eff}$ (régime slow-roll) — dérivé |
| 3 | $T_{\rm eq} = v_T - \lambda v_\Gamma^2/\beta$ — l'équilibre est décalé par le tadpole — dérivé |
| 4 | $V_{\rm min}$ calculé exactement — signe dépendant de $v_T$ — dérivé |
| 5 | Identification formelle : linear quintessence / axion monodromie — dérivé |
| 6 | Le champ $T$ n'est PAS un fantôme (cinétique standard) — dérivé |

### Ouverts 🟡

| # | Question |
|---|----------|
| 1 | Quel choix de paramètres donne le bon $\rho_\Lambda$ ? (hiérarchie) |
| 2 | Le régime physique est-il gelé, slow-roll, ou oscillant ? |
| 3 | Le signe de $V_{\rm min}$ : le vide de la Toile est-il dS, Minkowski, ou AdS ? |
| 4 | Pourquoi $\beta \sim H_0^2$ ? (naturalité de la masse) |

### Rien de mort 🔴

Aucune réfutation interne — la structure mathématique est saine et non triviale.

---

## 11. PROCHAINE ÉTAPE

**Étape 2 :** implémenter le système d'ODE (deux équations couplées) dans un
solveur numérique, produire $w(z)$ et $H(z)$, et visualiser les trois régimes
(gelé / slow-roll / oscillant) pour des choix de paramètres représentatifs.

---

*Étape 1 rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*15 août 2026 — Série énergie noire, Étape 1/8.*
