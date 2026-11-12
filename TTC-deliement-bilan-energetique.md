# TTC — Bilan énergétique du « déliement » (n = 1 → 0)

**Question traitée** : lors du passage d'un nœud de matière (n = 1) à l'onde de transit (n = 0),
où passe l'énergie de repos — 938,27 MeV pour le proton, 511 keV pour l'électron ?
**Conclusion** : l'énergie ne disparaît nulle part (elle n'a jamais été séparée du champ), mais la
transition **n'est pas autorisée** par MCW-1 en l'état. Le verrou n'est pas énergétique, il est
**topologique** (§4) — puis, plus grave, **il n'y a pas de mécanisme** : le champ dont on dénoue
l'enroulement n'est pas celui qui porte la masse (§8). Détail ci-dessous.
**Statut de la note** : démonstration + no-go + réfutation du mécanisme A + échappatoires. Ne remplace aucun document.

## 0. Résumé exécutif

| # | Résultat | Stade |
|---|----------|-------|
| 1 | Dans la TTC, $m_0c^2$ **est** l'énergie du champ : $m_0c^2 = \int d^3x\,\rho_{\mathcal W}$. Il n'y a donc aucune « masse-substance » à faire disparaître. | **É** |
| 2 | L'invariant cinématique $c^2=v^2+w^2$ n'est pas un axiome : il se **déduit** de la conservation de $E$ + RR, à condition d'identifier $w \equiv c/\gamma$. | **É** (dérivé ici) |
| 3 | Mais $w$ n'est alors **pas** une vitesse de rotation spatiale : c'est la **fraction de masse au repos** $c\,M/m_0$. | **É** |
| 4 | $n = \frac{1}{2\pi}\oint\nabla\Phi\cdot d\mathbf l$ est protégé (π₁(S¹) = ℤ, $U(1)_\Phi$ non brisé). Un nœud **seul** ne peut pas être dénoué continûment. | **É** (no-go) |
| 5 | Donc « déliement d'un proton isolé pour un coût négligeable » est **faux au sens de la TTC**. Ce qui reste vrai : annihilation de paire, ou annihilation cohérente coûtant ≈ $m_0c^2$. | **É** |
| 6 | Le « Théorème du Déliement Métrique » doit être **requalifié** : ce n'est pas un théorème, c'est une transition inter-site avec barrière. | correction |
| 7 | Le nœud d'enroulement est un **monopôle global** : $E = 2\pi n^2 v_\Gamma^2 R$, croît avec le rayon, indépendant du cœur. | **É** (calculé) |
| 8 | Si le nœud *est* le proton : $v_\Gamma = m_p/\sqrt{2\pi} = 374{,}3$ MeV et $\alpha\gtrsim6{,}3$ — incompatible avec $v_\Gamma\sim M_{\rm Pl}$, $\alpha\sim10^{-34}$. | **É** (contrainte) |
| 9 | Le mécanisme A (masse = énergie du nœud) **est réfuté** : il exigerait un seul $v_\Gamma$ pour tous les fermions, alors que le spectre en demande $10^{5}$ valeurs différentes (0,204 MeV pour $e$ → 68 893 MeV pour $t$). | **É** (réfutation, §8) |
| 10 | En régime B (le seul viable), $\partial m/\partial n = 0$ : dénouer $\Phi$ ne change pas la masse. **Le déliement n'a pas d'objet physique défini** dans MCW-1 en l'état. Seule sortie : le programme C (soliton séparé de la masse). | **É** (verdict, §8.3) |

---

## 1. Préalable : quel mécanisme de masse la TTC utilise-t-elle ?

La question « où passe 938,27 MeV » n'a pas de réponse unique, parce que le corpus contient
**deux** mécanismes de masse incompatibles, et que le déliement en dépend entièrement :

| Cas | Mécanisme | Source dans le dépôt | Conséquence sur le déliement |
|-----|-----------|----------------------|------------------------------|
| **A** | Masse = énergie du nœud de phase ($m_0c^2 = E_{\rm nœud}$) | ontologie « nœud », session 10-11/2026 | Dénouer **doit** supprimer la masse — mais libère $m_0c^2$ |
| **B** | Masse = couplage de Yukawa du fermion à $\Gamma$ | `TTC-White-Paper.md` §5 (aveuglément : « non dérivé ») | Dénouer $\Phi$ ne change **rien** à la masse : le fermion reste massif |

**C'est le point à trancher avant tout calcul de déliement.** En régime **B** (celui du White Paper),
défaire l'enroulement de $\Phi$ laisse la masse intacte : la thèse du déliement s'effondre
d'elle-même, sans même parler d'énergie. En régime **A**, la thèse tient mais doit payer le prix
calculé aux §3–§5.

Toute la suite suppose **A**, c'est-à-dire le cas le plus favorable au déliement.

---

## 2. Le comptage énergétique correct

Le tenseur du White Paper (§2.3) donne, en quasi-statique :

$$\rho_{\mathcal W} = \tfrac12(\nabla\Gamma)^2 + \tfrac12\Gamma^2(\nabla\Phi)^2 + \tfrac12(\nabla T)^2 + U(\Gamma,T)$$

Pour une configuration localisée, la **masse** est par définition

$$m_0c^2 \equiv E_0 = \int d^3x\,\rho_{\mathcal W}\Big|_{\text{statique}}$$

Il n'existe donc, dans la TTC, **aucune** quantité « masse » distincte de l'énergie du champ.
Reformulée correctement, la question « où passe 938,27 MeV ? » devient :

> *Une configuration de $(\Gamma,\Phi,T)$ d'énergie $E_0$ peut-elle évoluer vers une configuration
> d'énergie $E_0$ mais de masse invariante $M = 0$ ? Et si oui, par quel canal l'énergie de repos
> est-elle convertie ?*

Trois quantités **différentes** doivent être suivies séparément — c'est là que le raisonnement
« SF » du journal se perd :

| Quantité | Définition | Conservée ? |
|----------|-----------|-------------|
| Énergie $E$ | $\int T^{00}$ | **Oui** (Noether temporel, exact) |
| Courant de phase $J^\mu_\Phi = \Gamma^2\partial^\mu\Phi$ | charge de Noether de $U(1)_\Phi$ | **Oui** (équation de champ) |
| Enroulement $n$ | $\frac{1}{2\pi}\oint\nabla\Phi\cdot d\mathbf l$ | **Oui, topologiquement** — cf. §4 |
| Masse invariante $M$ | $\sqrt{E^2-p^2c^2}/c^2$ | **Non** (pas une charge de Noether) |

La masse invariante est la **seule** des quatre qui peut varier. C'est elle, et elle seule, que le
déliement peut faire tendre vers zéro. L'énergie, elle, reste.

---

## 3. L'invariant cinématique se déduit — il n'a pas à être postulé

C'est le résultat positif de ce chantier, et il vaut d'être isolé.

**Hypothèses** : (i) $E = m_0c^2$ constante ; (ii) $M^2c^4 = E^2-p^2c^2$ ; (iii) $v = pc^2/E$.

Alors immédiatement :

$$M = \frac{E}{c^2}\sqrt{1-\frac{v^2}{c^2}} = \frac{m_0}{\gamma}$$

Posons $w \equiv c\sqrt{1-v^2/c^2} = c/\gamma$. Il vient, sans aucune hypothèse supplémentaire :

$$\boxed{v^2 + w^2 = c^2}, \qquad \boxed{M = m_0\,\frac{w}{c}}, \qquad \boxed{\omega_{\rm int} = \frac{\omega_Z}{\gamma}}$$

**Lecture correcte** :

1. L'invariant $c^2 = v^2+w^2$ est un **théorème** de la relativité restreinte dès qu'on pose
   $E$ = constante. Il passe donc de **A (axiome)** à **É (dérivé)** — c'est un gain.
2. Mais $w$ **n'est pas une vitesse de rotation dans l'espace**. C'est le **taux de l'horloge
   interne**, c'est-à-dire numériquement $c\,M/m_0$ : la *fraction de l'énergie encore stockée sous
   forme de masse au repos*. « Faire tourner l'axe de vitesse de phase » = faire tourner le point
   dans le plan $(M/m_0,\ \beta)$ — ce n'est pas un mouvement, c'est une **reparamétrisation**.
3. La troisième ligne est le seul contenu physique neuf : la fréquence interne (Zitterbewegung)
   ralentit exactement comme $\gamma$. C'est cohérent, et c'est déjà le contenu standard de la
   dilatation du temps.
4. Conséquence quantitative : au premier ordre (petites vitesses), $p \approx \sqrt{2m_0\,\Delta M\,c^2}$,
   c'est-à-dire que **« perdre de la masse » et « gagner de l'énergie cinétique » sont le même fait**,
   au facteur $1/c^2$ près. Le début d'un déliement est donc strictement indiscernable d'une
   accélération ordinaire : la seule différence apparaît quand $v\to c$.

**Corollaire inconfortable** : puisque $M = m_0/\gamma$, atteindre $M=0$ exige $v = c$ exactement.
Or $v=c$ n'est atteint à énergie finie par **aucune** configuration localisée massive : c'est une
limite asymptotique. Le « soliton de transit » à $w=0$ n'est donc pas une solution, c'est un
**infimum jamais atteint**. Cela suffit à invalider l'affirmation du journal
« fidélité $\mathcal F = 1{,}000000$ » : on ne se place jamais exactement sur l'état $n=0$.

⚠️ Et surtout : *aucune* de ces identités ne fournit un **mécanisme**. Elles disent comment
l'énergie se répartit **si** la transition a lieu ; elles ne disent pas qu'elle peut avoir lieu.
C'est l'objet du §4.

---

## 4. Le no-go : n est une charge topologique, pas un paramètre

Le résultat le plus solide de la TTC — celui qui passe le test #3 de la batterie de falsification
à $10^{-5}$ près — est

$$\oint\nabla\Phi\cdot d\mathbf l = 2\pi n,\qquad n\in\mathbb Z \qquad(\texttt{TTC-White-Paper.md}, \S4)$$

Or $\Phi$ n'apparaît dans $U(\Gamma,T)$ **que** par ses dérivées : la symétrie $U(1)_\Phi$ est
**exacte** et **non brisée** (Γ est neutre sous $U(1)_\Phi$, donc le photon reste sans masse — c'est
cohérent avec `TTC-maxwell-derivation.md`). Dans ce régime :

- $n$ est l'indice d'enroulement d'une application $S^1\to S^1$ ; il ne peut varier que si $\Phi$
  cesse d'être défini sur un point, c'est-à-dire si $\Gamma$ s'annule au cœur ;
- promu en symétrie locale, $n$ devient le **flux magnétique** quantifié du secteur $U(1)_\Phi$ ;
  il est alors conservé par $\nabla\cdot\mathbf B = 0$, c'est-à-dire par la contrainte de Gauss.

**Théorème (no-go).** Dans MCW-1, une configuration d'enroulement $n=1$ ne peut pas évoluer
continûment vers $n=0$. Toute transition doit passer par une configuration où $\Gamma$ s'annule sur
un ensemble de mesure non nulle — et le coût en énergie de ce passage est calculé ci-dessous.

Vérification numérique : `ttc_deliement_barrier.py` (joint). Le calcul **a invalidé mon
estimation initiale** (une divergence en $\ln(R/\delta)$, qui est le cas de la *corde* et non du
*nœud*). Le résultat exact, pour $\Gamma=v_\Gamma\tanh(r/\delta)$ et $\Phi=n\theta$, est :

$$\boxed{E_{\rm nœud} = 2\pi\,n^2\,v_\Gamma^2\,R}\quad(\text{terme de gradient, dominant})$$

vérifié sur 5 décades de $R$ ($E_\nabla/R \to 0{,}5\times 4\pi = 2\pi$ exactement), avec
$E_U \propto R^3$ constant à $5\times10^{-8}$ près. Trois conséquences, toutes inconfortables :

1. **L'énergie ne dépend pas de la taille du cœur $\delta$, elle dépend du rayon extérieur $R$.**
   Un enroulement autour d'un point dans MCW-1 est un **monopôle global**, dont la masse croît
   linéairement avec la région — pas une particule localisée. (C'est le problème classique des
   monopôles globaux : $\Delta = 8\pi G v_\Gamma^2$.)
2. **Le no-go ne vient donc pas d'une barrière ultraviolette mais de l'infrarouge** : $n$ est
   mesuré à l'infini. Le faire varier exige que $\Gamma$ s'annule sur un ensemble qui *sépare
   l'infini* — c'est-à-dire en pratique tout le volume du nœud. Le coût du dénouement est donc de
   l'ordre de l'énergie du nœud lui-même, pas une quantité négligeable.
3. **Contrainte chiffrée sur $v_\Gamma$ (le résultat le plus utile de ce chantier).** Si le nœud
   *est* le proton, il faut $2\pi v_\Gamma^2 R = m_p$ avec $R = \hbar/(m_pc)$, d'où
   $$v_\Gamma = \frac{m_p}{\sqrt{2\pi}} = 374{,}3\ \text{MeV} \;\approx\; 1{,}9\,\Lambda_{\rm QCD}$$
   et la condition de cœur stable ($\alpha v_\Gamma^2R^2\gtrsim1$) donne $\alpha \gtrsim 6{,}3$.
   Or `TTC-White-Paper.md` §2.6 pose $v_\Gamma\sim M_{\rm Pl}$ et le dossier « hiérarchie »
   utilise $\alpha\sim10^{-34}$. **Les deux jeux sont incompatibles.** L'ontologie « particule =
   nœud » force $v_\Gamma$ à l'échelle QCD ; le reste du corpus suppose l'échelle de Planck.
   C'est un problème de hiérarchie *interne*, désormais quantifié — et non un détail.

---

## 5. Les seules échappatoires, et leur prix

Aucune n'est gratuite. Les voici par ordre de plausibilité théorique.

### 5.1 La paire (la seule voie topologiquement propre)

$n = +1$ et $n = -1$ ensemble donnent $n_{\rm total} = 0$ : la paire **peut** disparaître, et elle
libère exactement $2m_0c^2$ en rayonnement cohérent (deux modes $\Phi$ opposés). C'est
l'**annihilation**, et c'est précisément ce que le journal décrit correctement par ailleurs
(« chiralité dextrogyre / lévogyre »).

➜ **Conséquence pour le programme** : le transport doit porter une charge topologique **nulle**
(paire nœud/anti-nœud, ou charge totale nulle). Cela contraint très fortement l'architecture :
on ne « délie » pas un objet, on **délie un objet et son image chirale**. Ce n'est plus le même
cahier des charges.

### 5.2 L'anomalie (la seule voie qui sauve l'esprit du projet)

$n$ n'est conservé exactement que si $U(1)_\Phi$ n'a pas d'anomalie. Or la TTC couple des fermions
au champ (§5, CKM/PMNS). Une anomalie donnerait, à la manière de $U(1)_A$ en QCD :

$$\Delta n = \frac{g^2}{16\pi^2}\int d^4x\, F_{\mu\nu}\tilde F^{\mu\nu}$$

La transition devient alors possible, mais du type **sphaleron** : taux $\propto e^{-S_{\rm sphal}}$,
donc exponentiellement supprimé. Prix : il faut (i) vérifier que l'anomalie n'est pas nulle
(possiblement par annulation de charges, cas le plus fréquent), (ii) calculer $S_{\rm sphal}$ dans
MCW-1.

➜ C'est **le seul cadre cohérent** qui donnerait un jour un « déliement contrôlé » sans violer la
quantification — et il fournit une **prédiction falsifiable** : un seuil laser en $e^{-S}$, pas en
puissance continue.

### 5.3 Le nœud fermé (métastable, pas protégé)

Si le « nœud » est une **boucle fermée** de corde globale plutôt qu'un point, il n'est pas
topologiquement protégé — seulement **énergétiquement**. Il peut donc se contracter et disparaître,
mais en payant sa propre énergie : la barrière vaut $\sim m_0c^2$.

➜ Ici, l'énergie du déliement n'est **pas** négligeable : il faut fournir de l'ordre de l'énergie de
repos, de façon cohérente. Le « laser attoseconde » n'est alors pas un catalyseur mais un
**fournisseur d'énergie**. Cela respecte la conservation, mais ruine l'argument « coût quasi nul »
et rapproche dangereusement le procédé de l'annihilation.

### 5.4 Ce qui ne marche pas

- Postuler $w = 0$ atteint en temps fini (cf. §3, corollaire).
- « Annuler la vrille par une contre-phase » sans paire : c'est le no-go du §4.
- Invoquer une décohérence nulle (le journal, 05/11) : sans opérateur de symétrie exhibé, ce n'est
  pas un résultat.

---

## 6. Verdict et conséquences textuelles

| Énoncé du corpus / du blog | Verdict | Remplacement proposé |
|---|---|---|
| « Le déliement ne détruit pas la matière, il la libère » | **Non démontré**, contredit §4 | « Le déliement est une transition inter-site dans le plan $(M/m_0,\beta)$ ; son existence est conditionnée à §5.2 » |
| « Théorème du Déliement Métrique » | **Requalifier** | « Conjecture du déliement métrique » + conditions 5.1/5.2/5.3 |
| « L'énergie de masse part dans le soliton » | **Correct mais vide** : le soliton à $M=0$ est un paquet d'ondes des champs $(\Gamma,\Phi,T,A)$ | Préciser le canal : rayonnement cohérent de $\Phi$ |
| « $c^2 = v^2+w^2$, invariant fondamental » | **Correct, mais dérivé** (§3) et $w$ mal interprété | « $w = cM/m_0$ : taux de l'horloge interne » |
| « $m_0 = \hbar\omega_Z/c^2$ » | **Faux** (facteur 2) | $m_0 = \hbar\omega_Z/(2c^2)$ |
| « Fidélité $\mathcal F = 1{,}000000$ » | **Faux** : $n=0$ n'est jamais atteint exactement | $\mathcal F \to 1$ asymptotiquement |
| « Un proton seul peut être délié » | **Faux** au sens de MCW-1 (§4) | Paire, ou anomalie, ou annihilation |

---

## 7. Ce qu'il faut calculer ensuite (par ordre)

1. ~~**Trancher A vs B** (§1).~~ **FAIT — §8.** Verdict : A réfuté, B seul viable, donc
   $\partial m/\partial n = 0$ et le déliement n'a pas d'objet. Reste à instruire le programme C.
2. **Trancher $v_\Gamma$ : Planck ou QCD ?** (§4, conséquence 3). C'est une décision à prendre avant
   tout nouveau calcul, car elle change $\alpha$, $\lambda$, $\Lambda$ et la phénoménologie
   galaxies. Le choix « QCD » a l'avantage de supprimer le problème de hiérarchie ; il a le
   coût de devoir refaire le secteur sombre (§6.3) et l'écrantage.
3. **Calculer $S_{\rm sphal}$** dans MCW-1 (configuration interpolant $n=1\to n=0$ par $\Gamma\to0$,
   énergie finie seulement si $U(1)_\Phi$ est jaugée). Objet bien défini, calculable numériquement.
4. **Vérifier l'anomalie** : les charges des fermions de §5 s'annulent-elles dans
   $\sum_i Y_i^3$ ? Si oui, l'échappatoire 5.2 est fermée et il ne reste que 5.1 / 5.3.

---

## 8. Trancher A vs B (§7.1) — le mécanisme A est réfuté, et le déliement tombe avec lui

C'était le préalable déclaré au §1. Il est maintenant tranchable, et le résultat est plus dur que
prévu : **ce n'est pas la barrière énergétique qui bloque le déliement, c'est l'absence de
mécanisme de masse compatible.**

### 8.1 L'argument, en deux branches exhaustives

Le mécanisme A pose $m_0c^2 = E_{\rm nœud} = 2\pi n^2v_\Gamma^2 R$ (§4). La masse n'est alors
déterminée que si $R$ l'est. Or $R$ est le rayon **extérieur** du monopôle global — aucune équation
de MCW-1 ne le fixe. Deux cas seulement, tous deux fatals :

| Cas | Ce qu'on impose à $R$ | Conséquence |
|---|---|---|
| **A1** | rien (statut réel dans MCW-1) | $m \propto R$ : balayage de 12 décades en $R$ ⇒ facteur $10^{12}$ sur la masse. **Aucune prédiction.** |
| **A2** | $R = \hbar/(m_0c)$, seule échelle disponible | $m_0^2 = 2\pi n^2v_\Gamma^2$ ⇒ $m_0 = \sqrt{2\pi}\,|n|\,v_\Gamma$. **Aucun paramètre continu** : le spectre est entièrement contenu dans $|n|$. |

Dans le cas A2 — le plus favorable, puisqu'il rend A prédictif —, les rapports de masse doivent être
des **rapports d'entiers**, et surtout le modèle ne contient **qu'une seule échelle de masse** pour
$|n|=1$. Il faut donc *un* $v_\Gamma$.

### 8.2 Le test chiffré

Si le nœud *est* la particule, $v_\Gamma = m/\sqrt{2\pi}$ doit être **le même** pour tous les
fermions. Calcul (`ttc_mass_mechanism_test.py`, Partie 2) :

| Fermion | $m$ (MeV) | $v_\Gamma$ exigé (MeV) |
|---|---|---|
| $e$ | 0,511 | **0,204** |
| $\mu$ | 105,66 | 42,2 |
| $\tau$ | 1776,9 | 709 |
| $c$ | 1270 | 507 |
| $b$ | 4180 | 1668 |
| $t$ | 172 690 | **68 893** |

**Étalement : $3{,}4\times10^{5}$.** Un champ $\Gamma$ unique ne peut pas valoir simultanément
0,204 MeV et 68 893 MeV. Le mécanisme A est réfuté comme origine du spectre de masse des fermions.

*Réserve d'honnêteté* : le test « rapports entiers » (Partie 4) donne des écarts trompeusement
faibles (0,1 % pour $\mu/e$, 0,007 % pour $\tau/e$) — mais c'est un artefact : les entiers sont
denses aux grands rapports. **Ce test ne prouve rien dans un sens ni dans l'autre** et ne doit pas
être cité ; les §8.1 et §8.2 suffisent.

### 8.3 La conséquence sur le déliement — le vrai verdict

En régime B (Yukawa, la seule voie interne qui survive), la masse du fermion est
$m \propto \Gamma$ **au point où se trouve le fermion**. Défaire l'enroulement de $\Phi$ ne change
donc **rien** à sa masse :

$$\frac{\partial m}{\partial n} = 0 \quad\text{(régime B)}$$

Le fermion reste massif. Il n'y a pas de « soliton de transit » sans masse à trouver, pas de
configuration $M=0$ à atteindre, pas de $\gamma\to\infty$ à approcher. **La prémisse du déliement ne
tombe pas parce qu'une barrière est trop haute : elle tombe parce que le champ dont on dénoue
l'enroulement n'est pas celui qui porte la masse.**

$\Rightarrow$ Le « Théorème du Déliement Métrique » n'a, en l'état du corpus, **pas d'objet
physique défini**. Ce n'est ni vrai ni faux : c'est une affirmation sur une quantité qui n'existe
pas dans le Lagrangien.

### 8.4 La seule sortie qui préserve le programme — mécanisme C

| | Mécanisme | Statut | Effet du déliement |
|---|---|---|---|
| **A** | masse = énergie du nœud | **réfuté** (§8.1–8.2) | supprimerait la masse — mais A est mort |
| **B** | masse = Yukawa à $\Gamma$ (§5 WP) | seul viable en interne | **nul** ; le déliement est sans objet |
| **C** | masse = VEV d'un champ distinct ; le nœud est un soliton **séparé** | **à instruire** | porte sur le soliton, pas sur la masse |

**C est la seule formulation où le programme garde un sens physique** — et elle change le cahier des
charges : le déliement devient une affirmation sur *la structure d'un soliton*, pas sur *la masse
d'une particule*. Concrètement, cela veut dire réintroduire un secteur scalaire supplémentaire (un
VEV distinct de $v_\Gamma$) et montrer que les nœuds de $\Phi$ y sont métastables et manipulables.
Tant que ce secteur n'est pas écrit, toute la littérature « déliement » du journal reste au stade
**P** au mieux, **D** en réalité.

### 8.5 Ce que cela change dans les documents existants

| Document | Ce qu'il faudrait corriger |
|---|---|
| `TTC-White-Paper.md` §5 | déclarer explicitement que la masse **n'est pas** portée par $\Phi$ (ligne déjà présente : « non dérivé ») — et en tirer la conséquence : le déliement est hors sujet dans ce modèle |
| `TTC-White-Paper.md` §6.3 | ajouter que le problème de hiérarchie n'est pas seulement non résolu, il est **mal posé** si $v_\Gamma$ doit valoir 0,2 MeV et $M_{\rm Pl}$ à la fois (§4 conséquence 3) |
| veine « déliement » | requalifier en **programme C** : écrire le secteur scalaire supplémentaire avant toute nouvelle affirmation |

*Note technique — 11/11/2026. Scripts associés : `ttc_deliement_barrier.py` (§4),
`ttc_mass_mechanism_test.py` (§8).*
