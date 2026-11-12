# TTC ÉNERGIE NOIRE — Étape 1.5 : CORRECTION MAJEURE
## Le système à deux champs (Γ, T) — réponse au vérificateur

> **Date :** 16 août 2026
> **Auteur :** DeepSeek V4 Pro (Co-auteur scientifique TTC)
> **Série :** Roadmap énergie noire — Correction de l'Étape 1
> **Déclencheur :** Réfutation interne par l'agent vérificateur (7 failles)
> **Statut :** ✅ Correction complète — l'Étape 1 est RÉVOQUÉE, ce document la remplace

---

## 0. RECONNAISSANCE

L'agent vérificateur a identifié une erreur interne grave dans l'Étape 1 :

> **L'ansatz $\Gamma = v_\Gamma$ n'est PAS une solution de l'équation du champ $\Gamma$
> quand $\lambda \neq 0$ et $T \neq 0$.**

**J'ai revérifié ses calculs un par un : les 7 failles sont exactes.**
La correction est entièrement acceptée. Ce document remplace l'Étape 1.

**Leçon de processus :** la vérification atomique fonctionne. C'est exactement
le rôle du vérificateur — attraper l'erreur AVANT le solveur numérique.
Meilleure issue possible : l'erreur est morte ici, pas dans un papier publié.

---

## 1. LE VRAI SYSTÈME : DEUX CHAMPS COUPLÉS

Les équations du mouvement complètes, en fond FLRW homogène ($\partial\Phi = 0$) :

$$\boxed{\begin{aligned}
\ddot\Gamma + 3H\dot\Gamma + \alpha\Gamma(\Gamma^2 - v_\Gamma^2) + 2\lambda T\Gamma &= 0 \\[4pt]
\ddot T + 3H\dot T + \beta(T - v_T) + \lambda\Gamma^2 &= 0
\end{aligned}}$$

C'est un **système couplé non linéaire**. L'Étape 1 a traité le second membre
de la première équation comme nul (faux) et a gardé $\lambda v_\Gamma^2$ dans
la seconde (incohérent avec l'ansatz).

---

## 2. LE VRAI VIDE : MINIMUM À DEUX CHAMPS

Le minimum du potentiel $U(\Gamma, T)$ vérifie $\partial U/\partial\Gamma = \partial U/\partial T = 0$ :

$$\begin{aligned}
\alpha\Gamma(\Gamma^2 - v_\Gamma^2) + 2\lambda T\Gamma &= 0 \\
\beta(T - v_T) + \lambda\Gamma^2 &= 0
\end{aligned}$$

Sur la branche brisée ($\Gamma \neq 0$) :

$$\boxed{\Gamma_{\rm eq}^2 = v_\Gamma^2 - \frac{2\lambda T_{\rm eq}}{\alpha}}$$

En injectant dans la seconde équation :

$$\boxed{T_{\rm eq} = \frac{\beta v_T - \lambda v_\Gamma^2}{\beta - \frac{2\lambda^2}{\alpha}}}$$

> ✅ Conforme au résultat du vérificateur (recalculé indépendamment).

### 2.1 Conséquence physique nouvelle : le VEV de cohérence est DÉCALÉ

Le vrai vide n'est PAS $\Gamma = v_\Gamma$. La tension déplace la cohérence :

$$\Gamma_{\rm eq}^2 = v_\Gamma^2 - \frac{2\lambda T_{\rm eq}}{\alpha}$$

Pour $v_T = 0$ (le choix de normalisation) et $m_{\rm eff}^2 > 0$ :
$T_{\rm eq} < 0$ donc $\Gamma_{\rm eq}^2 > v_\Gamma^2$ — **la tension négative
du vide renforce la cohérence au-dessus de sa valeur nue.**

> 🟡 **Hypothèse à explorer :** le « $v_\Gamma$ effectif » de l'univers réel
> n'est pas le paramètre nu du lagrangien, mais $\Gamma_{\rm eq}(T_{\rm eq})$.
> C'est cohérent avec la spec discrète où KontEx ancre $\Gamma$ par des
> sources externes : les deux points de vue se rejoignent si les ancres
> représentent précisément le décalage $2\lambda T/\alpha$.

---

## 3. LE POTENTIEL EFFECTIF CORRECT (intégration adiabatique)

Si $\Gamma$ est massif (grand $\alpha$), il suit son minimum adiabatiquement :
$\Gamma^2 \approx \Gamma_{\rm eq}^2(T) = v_\Gamma^2 - 2\lambda T/\alpha$,
valide tant que $\Gamma_{\rm eq}^2 > 0$, c'est-à-dire $T < \frac{\alpha v_\Gamma^2}{2\lambda}$.

Substitution dans $U$ :

$$\boxed{U_{\rm eff}(T) = \left(\frac{\beta}{2} - \frac{\lambda^2}{\alpha}\right)T^2 + \left(\lambda v_\Gamma^2 - \beta v_T\right)T + \frac{\beta v_T^2}{2}}$$

> ✅ Conforme au résultat du vérificateur. Dérivation pas à pas :
> $\frac{\alpha}{4}(\Gamma_{\rm eq}^2-v_\Gamma^2)^2 = \frac{\alpha}{4}\cdot\frac{4\lambda^2T^2}{\alpha^2} = \frac{\lambda^2T^2}{\alpha}$ ;
> $\lambda T\Gamma_{\rm eq}^2 = \lambda v_\Gamma^2T - \frac{2\lambda^2T^2}{\alpha}$ ;
> somme des termes en $T^2$ : $\frac{\beta}{2} - \frac{\lambda^2}{\alpha}$ ✓

### 3.1 La masse effective corrigée

$$\boxed{m_{T,\rm eff}^2 = \beta - \frac{2\lambda^2}{\alpha}}$$

**La masse de $T$ n'est PAS $\beta$.** L'Étape 1 était fausse sur ce point
central. La condition de stabilité :

$$\boxed{\alpha\beta > 2\lambda^2 \quad\Longleftrightarrow\quad m_{T,\rm eff}^2 > 0}$$

Si $\alpha\beta < 2\lambda^2$, le champ $T$ est **tachyonique** : l'oscillateur
harmonique amorti de l'Étape 1 n'existe pas, et le système dévale vers la
branche $\Gamma = 0$ (symétrie restaurée — la « bulle de néant » de
l'exploration trous noirs).

### 3.2 Le point d'équilibre corrigé

$$\boxed{T_{\rm eq} = \frac{\beta v_T - \lambda v_\Gamma^2}{m_{T,\rm eff}^2}}$$

Le résultat de l'Étape 1 ($T_{\rm eq} = v_T - \lambda v_\Gamma^2/\beta$) n'est
valable que dans la limite $\frac{2\lambda^2}{\alpha\beta} \to 0$ — limite
que je n'avais JAMAIS justifiée. C'est une approximation incontrôlée.

---

## 4. L'ÉNERGIE DU VIDE CORRIGÉE

Au minimum :

$$U_{\rm eff}(T_{\rm eq}) = \frac{\beta v_T^2}{2} - \frac{(\beta v_T - \lambda v_\Gamma^2)^2}{2m_{T,\rm eff}^2}$$

> **Dérivation :** $U_{\rm eff}(T) = \frac{m^2}{2}T^2 + (\lambda v_\Gamma^2-\beta v_T)T + \frac{\beta v_T^2}{2}$
> avec $\lambda v_\Gamma^2-\beta v_T = -m^2 T_{\rm eq}$. Donc
> $U_{\rm eff}(T_{\rm eq}) = \frac{m^2}{2}T_{\rm eq}^2 - m^2T_{\rm eq}^2 + \frac{\beta v_T^2}{2}
> = \frac{\beta v_T^2}{2} - \frac{m^2 T_{\rm eq}^2}{2}$ ✓

### 4.1 Les trois vides possibles (corrigés)

| Cas | $U_{\rm eff}(T_{\rm eq})$ | Nature du vide |
|-----|--------------------------|----------------|
| $v_T = 0$ | $-\frac{\lambda^2 v_\Gamma^4}{2m_{T,\rm eff}^2} < 0$ | **AdS** — énergie négative |
| $v_T = \frac{\lambda v_\Gamma^2}{\beta}$ | $\frac{\lambda^2 v_\Gamma^4}{2\beta} > 0$ | **de Sitter** — $T_{\rm eq} = 0$ exactement |
| Cas général | signe selon $v_T$ | Transition AdS → dS |

> ✅ Le vérificateur avait raison : avec $v_T = 0$, le vide est AdS. Et :
> **l'accélération est impossible au voisinage de ce minimum** ($V_{\rm eff}<0
> \Rightarrow \dot T^2 < V_{\rm eff}$ ne peut jamais être satisfaite).

### 4.2 Le scénario viable devient clair

Pour avoir de l'énergie noire POSITIVE aujourd'hui, deux options :

1. **Option dS :** $v_T = \lambda v_\Gamma^2/\beta$ — le vide est de Sitter
   positif, $T_{\rm eq}=0$, et l'énergie noire est la valeur d'équilibre.
   Mais alors on retrouve le problème de constante cosmologique : pourquoi
   $U_{\rm eff}(0)$ est-il si petit ?
2. **Option transitoire :** $v_T = 0$, le champ roule vers le minimum AdS.
   L'énergie noire est un transitoire POSITIF si $T$ est encore au-dessus de
   zéro (région $V_{\rm eff} > 0$ existe pour $T > 0$ : $V_{\rm eff} = \frac{m^2}{2}T^2 + \lambda v_\Gamma^2 T > 0$).
   **Mais le champ roule.** Le temps de roulement est la question centrale —
   le vérificateur a raison de l'exiger.

---

## 5. LE TEMPS DE ROULEMENT (la question que j'ai esquivée)

Le champ roule de $T_0$ vers $T_{\rm eq}$ avec l'équation
$\ddot X + 3H\dot X + m_{\rm eff}^2 X = 0$. Le temps caractéristique :

$$\boxed{\tau_{\rm roll} \sim \max\left(\frac{1}{m_{\rm eff}}, \frac{1}{H}\right)}$$

- Si $m_{\rm eff} \gg H_0$ : le champ a fini de rouler depuis longtemps —
  il serait AU minimum AdS, et l'univers ne pourrait pas accélérer. **Scénario mort.**
- Si $m_{\rm eff} \sim H_0$ : $\tau_{\rm roll} \sim t_{\rm Hubble}$ — le champ
  roule encore. C'est le seul régime où le transitoire est vivant aujourd'hui.
- Si $m_{\rm eff} \ll H_0$ : le champ est gelé par le frottement de Hubble —
  comportement de constante cosmologique effective.

> 🟡 **Conséquence immédiate :** $m_{\rm eff} \gtrsim H_0$ EST un prérequis,
> pas une coïncidence optionnelle. La masse de $T$ doit être « juste assez
> grande » pour que le roulement soit encore en cours. C'est une contrainte
> de viabilité, pas une prédiction.

---

## 6. CLASSIFICATION DES RÉGIMES — CORRIGÉE

La classification de l'Étape 1 utilisait $\beta$ ; elle doit utiliser $m_{\rm eff}^2$ :

| Régime | Condition (corrigée) | w effectif |
|--------|---------------------|------------|
| **Tachyonique** | $m_{\rm eff}^2 < 0$ ($\alpha\beta < 2\lambda^2$) | ⚠️ Runaway — modèle invalide dans ce régime |
| **Gelé** | $m_{\rm eff} \ll H$ | −1 (Λ effective) |
| **Slow-roll** | $m_{\rm eff} \sim H$, $\dot T^2 \ll V_{\rm eff}$ | −1 + ε, dérive |
| **Oscillant** | $m_{\rm eff} \gg H$ | voir §6.1 |

### 6.1 Le régime oscillant — traitement viriel correct

Pour un scalaire quadratique oscillant autour de $V_{\rm min}$ :

$$\left\langle \frac12\dot T^2\right\rangle = \left\langle \frac{m_{\rm eff}^2}{2}\delta T^2\right\rangle \quad \text{(viriel)}$$

d'où la moyenne temporelle de l'équation d'état :

$$\boxed{\langle w\rangle = -\frac{V_{\rm min}}{V_{\rm min} + 2\langle K\rangle}}$$

avec $K = \frac12\dot T^2$. Les cas :

| $V_{\rm min}$ | $K \ll |V_{\rm min}|$ | $K \sim |V_{\rm min}|$ |
|---------------|----------------|---------------------|
| **positif** | $w \to -1$ (Λ effective) | $w$ remonte vers 0 |
| **négatif** | pas d'accélération possible | pas d'accélération possible |

> ✅ Le vérificateur a raison : le régime oscillant n'est PAS automatiquement
> de l'énergie noire. Avec $V_{\rm min}<0$, il n'en est JAMAIS.

**Bilan du régime oscillant :** l'énergie noire oscillante n'est viable que
si $V_{\rm min} > 0$ ET l'amplitude d'oscillation est faible devant $V_{\rm min}$.
C'est un couloir étroit.

---

## 7. RÉPONSE AUX FAILLES 5, 6, 7 (acceptées intégralement)

### Faille 5 — Prédictivité

**Acceptée.** Le secteur énergie noire seul a $(\alpha, \beta, \lambda, v_\Gamma, v_T, T_0, \dot T_0)$
= 7 paramètres contre 2 pour $w_0$-$w_a$. La comparaison brute des χ² est
trompeuse. **Position corrigée :**

> La TTC ne prétend PLUS avoir une forme fonctionnelle plus prédictive que
> $w_0$-$w_a$ DANS LE SECTEUR ÉNERGIE NOIRE SEUL. Sa prédictivité éventuelle
> est GLOBALE : les mêmes paramètres $(\alpha,\beta,\lambda,v_\Gamma,v_T)$
> doivent décrire AUSSI le secteur galactique, la spec discrète, et les tests
> falsificateurs 1-3. C'est à ce niveau-là que le compte des paramètres
> se compare — pas secteur par secteur.

**L'affirmation « oscillations = signature unique » est RETIRÉE.** Les
modèles axioniques et autres quintessences non monotones produisent aussi
des oscillations de $w(z)$. La TTC n'a pas de monopole là-dessus.

### Faille 6 — Naturalité

**Acceptée.** Le terme $\lambda T\Gamma^2$ brise la symétrie de translation
de $T$. Rien ne protège $m_T^2$ contre les corrections radiatives. Si
$\beta \sim H_0^2$, le modèle a le problème de la constante cosmologique
déguisé. **Position corrigée :**

> La TTC ne résout PAS le problème de naturalité de l'énergie noire. Elle le
> REPARAMÉTRISE. C'est une limitation à documenter noir sur blanc, pas une
> question rhétorique. Piste future : un mécanisme de type axion (symétrie
> de jauge de $\Phi$ étendue) — hors du périmètre actuel.

### Faille 7 — Perturbations et contraintes locales

**Acceptée.** Un scalaire de masse $m \sim H_0$ a une longueur de Compton
$\sim$ taille de Hubble. Ses perturbations affectent CMB, ISW, croissance
des structures. **Position corrigée :**

> Ce n'est PAS reportable indéfiniment. Les contraintes de perturbation
> deviennent un **go/no-go de l'Étape 6** : si le champ $T$ est exclu par
> les données CMB+ISW dans tous les régimes viables, la théorie énergie
> noire TTC est morte, quel que soit le reste.

---

## 8. LE SYSTÈME COMPLET POUR L'ÉTAPE 2 (RÉVISÉ)

Le solveur numérique doit traiter les **DEUX champs couplés**, pas le système
réduit :

$$\boxed{\begin{aligned}
\ddot\Gamma + 3H\dot\Gamma + \alpha\Gamma(\Gamma^2 - v_\Gamma^2) + 2\lambda T\Gamma &= 0 \\[4pt]
\ddot T + 3H\dot T + \beta(T - v_T) + \lambda\Gamma^2 &= 0 \\[4pt]
H^2 = \frac{8\pi G}{3}\left(\rho_{m0}a^{-3} + \rho_{r0}a^{-4} + \frac12\dot\Gamma^2 + \frac12\dot T^2 + U(\Gamma,T)\right)
\end{aligned}}$$

Trois ODE couplées. L'Étape 2 produira :
1. La solution complète $(\Gamma(t), T(t), a(t))$
2. La comparaison avec la solution adiabatique (§3) — valider ou invalider l'approximation $\alpha$ grand
3. $w(z)$, $H(z)$ pour les régimes corrigés du §6

---

## 9. BILAN DE LA CORRECTION

### Ce qui était faux dans l'Étape 1 (révoqué)

| # | Erreur |
|---|--------|
| 1 | Ansatz $\Gamma = v_\Gamma$ auto-contradictoire |
| 2 | Masse de $T$ = $\beta$ (la vraie : $m_{\rm eff}^2 = \beta - 2\lambda^2/\alpha$) |
| 3 | Équilibre $T_{\rm eq} = v_T - \lambda v_\Gamma^2/\beta$ (limite non justifiée) |
| 4 | « Rien de mort 🔴 » — il y avait une réfutation interne majeure |
| 5 | « Oscillations = signature unique » — retirée |
| 6 | « Forme fonctionnelle déterminée » sans réserve sur les 7 paramètres |

### Ce qui survit

| # | Résultat correct |
|---|------------------|
| 1 | ρ_T, p_T, w_T pour un scalaire : formules inchangées |
| 2 | Pas de fantôme : cinétique standard |
| 3 | Identification linear quintessence — SURVIT avec les paramètres corrigés |
| 4 | Le mécanisme de relaxation comme image de l'énergie noire |

### Nouvelles contraintes de viabilité (découvertes par la correction)

| # | Contrainte |
|---|-----------|
| 1 | $\alpha\beta > 2\lambda^2$ (pas de tachyon) |
| 2 | $m_{\rm eff} \gtrsim H_0$ (le roulement doit être en cours) |
| 3 | $V_{\rm min} > 0$ pour tout régime d'accélération durable |
| 4 | $\dot T^2 < V_{\rm eff}$ au présent (slow-roll) |

---

## 10. REMERCIEMENT AU VÉRIFICATEUR

La critique est exacte sur 7/7 points. C'est la contribution la plus précieuse
que le processus puisse produire : une réfutation interne AVANT publication.
L'Étape 1 est révoquée ; l'Étape 1.5 la remplace.

---

*Correction rédigée par DeepSeek V4 Pro, Co-auteur scientifique TTC.*
*16 août 2026 — en réponse à l'agent vérificateur.*
