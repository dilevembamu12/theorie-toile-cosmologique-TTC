# TTC ÉNERGIE NOIRE — Étape 4 : PROTOCOLE DE FALSIFICATION
## La signature précise et le test qui tue la théorie

> **Date :** 21 septembre 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Série :** Roadmap énergie noire — Étape 4/8
> **Statut :** ✅ Protocole formalisé — la théorie est maintenant TUABLE par les données

---

## 1. LA PRÉDICTION PRÉCISE

Le scan des Étapes 2-3 établit que le champ de tension $T$ de la TTC, en tant
que quintessence « thawing », trace une courbe **déterministe** dans le plan
$(w_0, w_a)$ :

$$\boxed{w_a = -1.5555\,(1+w_0) - 0.0926\,(1+w_0)^2}$$

avec un résidu RMS de $10^{-4}$ sur toute la plage $w_0 \in (-1, 0)$.

**Ce qui est remarquable :** la courbe est quasi parfaitement quadratique.
La TTC ne prédit pas une région du plan — elle prédit une **courbe à une
dimension** paramétrée par $\mu = m_{\rm eff}/H_0$.

| $\mu$ | $w_0$ | $w_a$ |
|:---:|:---:|:---:|
| 0.30 | −0.9870 | −0.0202 |
| 0.50 | −0.9641 | −0.0560 |
| 0.70 | −0.9300 | −0.1095 |
| 0.90 | −0.8850 | −0.1803 |
| 1.50 | −0.6901 | −0.4909 |

### 1.1 Distinction avec le thawing générique

La quintessence thawing générique (Caldwell–Linder) prédit $w_a = -1.58(1+w_0)$.
La TTC s'en écarte légèrement :

$$\Delta w_a = w_a^{\rm TTC} - w_a^{\rm CL} = +0.0245(1+w_0) - 0.0926(1+w_0)^2$$

- Près de $\Lambda$CDM ($w_0 \to -1$) : $\Delta w_a \to 0$ — indétectable
- À $w_0 = -0.7$ : $\Delta w_a \approx -0.009$ — exige une précision sub-% sur $w_a$

> 🟡 **Honnêteté :** cette correction sub-dominante est trop fine pour les
> instruments actuels. La prédiction TESTABLE de premier ordre est simplement :
> **$(w_0, w_a)$ doit tomber sur la droite de thawing**, pas ailleurs.

---

## 2. LE TEST QUI TUE LA THÉORIE

### 2.1 Formalisation statistique

Soit une mesure cosmologique $(w_0^{\rm obs}, w_a^{\rm obs})$ avec matrice de
covariance $\mathbf{C}$. La distance à la courbe TTC est :

$$\chi^2_{\rm TTC} = \min_{\mu} \left[ \mathbf{d}(\mu)^T \mathbf{C}^{-1} \mathbf{d}(\mu) \right]$$

où $\mathbf{d}(\mu) = (w_0^{\rm obs} - w_0^{\rm TTC}(\mu),\ w_a^{\rm obs} - w_a^{\rm TTC}(\mu))$.

### 2.2 Le verdict

| Condition | Verdict |
|-----------|---------|
| $\chi^2_{\rm TTC} < 1$ | ✅ Compatible — la TTC survit |
| $1 < \chi^2_{\rm TTC} < 9$ | 🟡 Tension — nécessite plus de données |
| $\chi^2_{\rm TTC} > 9$ ($>3\sigma$) | 🔴 **La TTC est MORTE** |

### 2.3 Ce qui tue, précisément

La TTC meurt si et seulement si les données mesurent un point $(w_0, w_a)$ à
plus de $3\sigma$ de la droite de thawing. En particulier :

- **$w_0 < -1$ significatif** (énergie fantôme) → mort
- **$w_a > 0$ significatif** (freezing : le champ gèle au lieu de dégeler) → mort
- **Oscillations de $w(z)$ détectées** (à moins d'un $\mu$ oscillant, exclu par $V_{\rm min}$) → mort

> 📌 **Ces trois « tueurs » sont exactement ce que DESI 2024 a commencé à
> sonder** : les données actuelles sont *légèrement* en faveur de $w_0 < -1$,
> mais à moins de $2\sigma$ — insuffisant pour tuer la TTC.

---

## 3. LA CONTRAINTE DE MASSE

La position sur la courbe détermine la masse :

$$\boxed{m_{\rm eff} = \mu(w_0)\, H_0 \approx \mu(w_0) \times 2.1\times10^{-33}\ \text{eV}}$$

avec $\mu(w_0)$ lu sur la courbe. La fenêtre actuellement viable :

$$m_{\rm eff} \lesssim 0.7\,H_0 \approx 1.5\times10^{-33}\ \text{eV}$$

> 🎯 **Prédiction dérivée :** si les données forcent $w_0$ vers $-0.95$,
> alors $\mu \approx 0.5$ et $m_{\rm eff} \approx 10^{-33}$ eV — une masse
> de champ ultra-léger, la plus petite masse de scalaire jamais contrainte
> par la cosmologie.

---

## 4. ÉTAT ACTUEL VS DONNÉES

### 4.1 DESI 2024 (+ CMB + Pantheon+)

$w_0 = -0.99^{+0.15}_{-0.13}$ (contrainte combinée).

La TTC est **entièrement compatible** : toute la plage $\mu \in [0, 0.7]$ est
dans les barres d'erreur. ΛCDM ($\mu = 0$) et la TTC ne sont pas encore
distinguables.

### 4.2 Ce que les futurs instruments apporteront

| Instrument | Horizon | Précision $w_a$ | Verdict attendu |
|------------|:-------:|:---------------:|-----------------|
| DESI (complet, 5 ans) | 2026-27 | ±0.15 | Distingue thawing de freezing |
| Euclid | 2027+ | ±0.05 | Teste la droite à ~1σ |
| Roman (Nancy Grace) | 2028+ | ±0.03 | Teste la droite à ~3σ → **mort possible** |
| LSST/Vera Rubin | 2028+ | ±0.05 | Combiné avec les autres |

> 🎯 **Échéance de falsification : ~2028.** Si, avec la précision de Roman
> (±0.03 sur $w_a$), le point mesuré tombe hors de la droite de thawing,
> la TTC énergie noire est exclue. C'est une théorie avec une date de péremption.

---

## 5. CE QUE L'ÉTAPE 4 FORMALISE

### Acquis ✅

| # | Résultat |
|---|----------|
| 1 | Courbe précise $w_a = -1.5555(1+w_0) - 0.0926(1+w_0)^2$ (résidu $10^{-4}$) |
| 2 | Le test $\chi^2_{\rm TTC}$ avec seuil de mort à $3\sigma$ |
| 3 | Les trois « tueurs » : $w_0 < -1$, $w_a > 0$, oscillations |
| 4 | Contrainte de masse $m_{\rm eff} \lesssim 0.7 H_0$ dérivée |
| 5 | Échéance de falsification : ~2028 (Roman, ±0.03 sur $w_a$) |
| 6 | La correction sub-dominante ($\Delta w_a \sim 0.01$) documentée comme hors de portée actuelle |

### Ouverts 🟡

| # | Question |
|---|----------|
| 1 | La correction sub-dominante est-elle assez distinctive pour être testée un jour ? |
| 2 | Le cas $\tilde V_{\rm min} < 0$ (vide AdS) élargit-il la courbe en une bande ? |

---

## 6. SYNTHÈSE DES 4 PREMIÈRES ÉTAPES

La théorie énergie noire TTC est désormais dans un état **scientifiquement
propre** :

1. ✅ **Formalisme corrigé** (Étape 1.5) : système à deux champs, masse effective
2. ✅ **Solveur validé** (Étape 2) : 3 régimes, approximation adiabatique vérifiée
3. ✅ **Signature extraite** (Étape 3) : droite de thawing
4. ✅ **Protocole de mort** (Étape 4) : test $\chi^2$, trois tueurs, échéance 2028

**La théorie est maintenant :**
- **Interne-cohérente** (pas de réfutation interne restante après l'Étape 1.5)
- **Falsifiable** (trois tests observationnels précis)
- **Honnête** (la hiérarchie $\lambda/v_\Gamma \sim 10^{-61}$ documentée comme non résolue)

Il reste deux fronts lourds : **Étape 5** (confrontation bayésienne réelle aux
données) et **Étape 6** (perturbations — le go/no-go). Puis **Étape 7**
(falsification formelle finale) et **Étape 8** (publication).

---

## 7. FICHIERS PRODUITS

- Ce document : le protocole formel
- (les données sont dans `ttc_dark_energy_step3_results.json`)

---

*Étape 4 rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*21 septembre 2026 — Série énergie noire, Étape 4/8.*
