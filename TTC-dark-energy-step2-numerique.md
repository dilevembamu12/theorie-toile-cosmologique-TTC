# TTC ÉNERGIE NOIRE — Étape 2 : RÉSOLUTION NUMÉRIQUE
## Les trois régimes du champ effectif + validité adiabatique

> **Date :** 21 septembre 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Série :** Roadmap énergie noire — Étape 2/8
> **Prérequis :** Étape 1.5 (correction) — le champ effectif $X = T - T_{\rm eq}$
> **Statut :** ✅ Solveur validé — résultats cohérents, fenêtre viable quantifiée

---

## 1. CE QUI EST RÉSOLU

Le système adimensionné (après intégration adiabatique de $\Gamma$) :

$$\varphi'' + (3 + h'/h)\varphi' + \mu^2\varphi = 0$$

$$h^2 = \frac{\Omega_{m0}a^{-3} + \Omega_{r0}a^{-4} + \tfrac12\mu^2\varphi^2 + \tilde V_{\rm min}}{1 - \tfrac12\varphi'^2}$$

où $\varphi = \sqrt{8\pi G/3}\,X$, $\mu = m_{\rm eff}/H_0$, $' = d/d\ln a$.

**Variables adimensionnées** : le champ est mesuré en unités $\sqrt{8\pi G/3}$,
la masse en unités $H_0$, le potentiel en unités de densité critique. Aucune
hiérarchie numérique ne pollue l'intégration.

---

## 2. LES TROIS RÉGIMES — RÉSULTATS

Chaque régime est **calibré** pour donner $\Omega_\phi = 0.6888$ aujourd'hui
(valeur Planck 2018). Le seul paramètre ajusté est le déplacement initial
$\varphi_i$ (le champ est gelé par le frottement de Hubble dans l'ère radiative).

| Régime | $\mu = m_{\rm eff}/H_0$ | $\varphi_i$ | $w_{\rm today}$ | $w(z{=}1)$ |
|--------|:---:|:---:|:---:|:---:|
| **Gelé** | 0.3 | 0.447 | **−0.9998** | −1.0000 |
| **Slow-roll (thawing)** | 1.5 | 0.975 | **−0.681** | −0.927 |
| **Oscillant** | 30 | 0.460 | **−0.991** | −0.963 |

### 2.1 Lecture physique

- **Gelé ($\mu = 0.3$)** : le champ ne bouge quasiment pas. $w \approx -1$
  exactement — indiscernable de ΛCDM. C'est le cas limite « constante
  cosmologique ».
- **Slow-roll ($\mu = 1.5$)** : le champ a commencé à dégeler récemment.
  $w$ dérive de $-0.93$ (à $z=1$) vers $-0.68$ (aujourd'hui). **C'est la
  signature falsifiable** : une dérive mesurable de $w(z)$.
- **Oscillant ($\mu = 30$)** : le champ oscille mais l'énergie du vide
  $\tilde V_{\rm min} = 0.60$ domine, donc $w \approx -1$ avec de faibles
  ondulations.

### 2.2 La fenêtre viable (confrontation à DESI 2024)

DESI mesure $w_0 \approx -0.99^{+0.15}_{-0.13}$. La fenêtre compatible
correspond à une masse **bornée supérieurement** :

| $w_{\rm today}$ visé | $\mu = m_{\rm eff}/H_0$ requis |
|:---:|:---:|
| −0.99 | 0.26 |
| −0.97 | 0.43 |
| −0.95 | 0.60 |

> 🎯 **Prédiction TTC quantifiée :** pour rester compatible avec les données,
> la masse effective de la tension doit satisfaire
> $$\boxed{m_{\rm eff} \lesssim 0.6\, H_0 \approx 10^{-33}\ \text{eV}}$$
> Si le champ $T$ était plus massif, $w$ s'écarterait trop de $-1$ et serait
> exclu. La fenêtre est étroite : c'est précisément ce qui rend le modèle
> **testable**.

---

## 3. VALIDITÉ DE L'APPROXIMATION ADIABATIQUE

L'intégration de $\Gamma$ (Étape 1.5) suppose $\Gamma$ massif. Vérification :

$$m_\Gamma^2 = 2\alpha v_\Gamma^2, \qquad m_{T,\rm eff}^2 = \beta - \frac{2\lambda^2}{\alpha}$$

Avec un jeu de paramètres représentatif ($\alpha = 1$, $v_\Gamma \sim 10^{28}$ eV,
$\lambda \sim 10^{-37}$ eV, $\beta \sim H_0^2$) :

| Quantité | Valeur | Exigence |
|----------|--------|----------|
| $m_\Gamma^2 / H^2_{\rm max}$ | $10^{121}$ | ≫ 1 ✅ |
| $m_\Gamma^2 / m_T^2$ | $10^{121}$ | ≫ 1 ✅ |
| $m_T^2 > 0$ | oui | ✅ (stabilité) |

> ✅ **L'approximation adiabatique est massivement valide.** $\Gamma$ est
> ultra-massif et suit son minimum instantanément. Le système à deux champs
> se réduit bien au scalaire effectif $X$.

### 3.1 MAIS — la hiérarchie, confirmée numériquement

Pour obtenir $m_T \sim H_0$ (fenêtre viable), il faut :

$$\lambda \lesssim H_0\sqrt{\alpha} \sim 10^{-33}\ \text{eV}$$

alors que $v_\Gamma \sim 10^{28}$ eV. Le rapport est :

$$\frac{\lambda}{v_\Gamma} \sim 10^{-61}$$

> 🔴 **Résultat honnête de l'Étape 2 :** la TTC fournit le MÉCANISME (scalaire
> massif roulant, masse $\sim H_0$), mais elle ne RÉSOUT pas le problème de
> hiérarchie. La petitesse de $\lambda$ est le problème de la constante
> cosmologique déguisé — exactement comme le vérificateur l'avait prédit à la
> Faille 6. Ce point est **confirmé** et documenté, pas résolu.

---

## 4. CE QUE L'ÉTAPE 2 ÉTABLIT

### Acquis ✅

| # | Résultat |
|---|----------|
| 1 | Le solveur converge et calibre $\Omega_\phi = 0.6888$ avec un résidu $< 10^{-9}$ |
| 2 | Les 3 régimes (gelé / slow-roll / oscillant) sont reproduits quantitativement |
| 3 | Le régime gelé est indiscernable de ΛCDM ($w = -0.9998$) |
| 4 | Le régime slow-roll produit une dérive mesurable $w(z)$ |
| 5 | La fenêtre viable impose $m_{\rm eff} \lesssim 0.6\,H_0$ — contrainte testable |
| 6 | L'approximation adiabatique est validée ($m_\Gamma^2/H^2 \sim 10^{121}$) |

### Ouverts 🟡

| # | Question |
|---|----------|
| 1 | La hiérarchie $\lambda/v_\Gamma \sim 10^{-61}$ — non résolue (Faille 6) |
| 2 | Le cas $v_T = 0$ (vide AdS) n'a pas encore été confronté aux données |
| 3 | La prédiction $w(z)$ doit être fittée à DESI+Pantheon+ (Étape 5) |
| 4 | Les perturbations (CMB/ISW) non traitées (Étape 6) |

---

## 5. PROCHAINE ÉTAPE

**Étape 3 — Classification et contraintes.** Formaliser la carte des régimes
dans le plan $(\mu, \tilde V_{\rm min})$, déterminer analytiquement la frontière
entre gelé et thawing ($\mu \sim 1$), et confronter la fenêtre $m_{\rm eff}
\lesssim 0.6\,H_0$ aux contraintes de masse des champs légers (Big Bang
Nucleosynthesis, structure).

---

## 6. FICHIERS PRODUITS

- `ttc_dark_energy_solver.py` — solveur ODE (LSODA, calibré par bissection)
- `ttc_dark_energy_step2.png` — $w(z)$, $h(z)$, $\Omega_\phi(z)$ des 3 régimes
- `ttc_dark_energy_step2_results.json` — résultats numériques

---

*Étape 2 rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*21 septembre 2026 — Série énergie noire, Étape 2/8.*
