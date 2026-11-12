# TTC — Bilan énergétique du « déliement » (n = 1 → 0)

**Question traitée** : lors du passage d'un nœud de matière (n = 1) à l'onde de transit (n = 0),
où passe l'énergie de repos — 938,27 MeV pour le proton, 511 keV pour l'électron ?
**Conclusion** : l'énergie ne disparaît nulle part (elle n'a jamais été séparée du champ), mais la
transition **n'est pas autorisée** par MCW-1 en l'état. Le verrou n'est pas énergétique, il est
**topologique**. Détail ci-dessous.
**Statut de la note** : démonstration + no-go + échappatoires. Ne remplace aucun document.

---

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

1. **Trancher A vs B** (§1). Sans cela, tout le reste est suspendu. Test : la masse d'un fermion
   suit-elle l'enroulement ? Si oui → A, et il faut réécrire §5 du White Paper ; si non → le
   déliement est sans objet et il faut le dire.
2. **Trancher $v_\Gamma$ : Planck ou QCD ?** (§4, conséquence 3). C'est une décision à prendre avant
   tout nouveau calcul, car elle change $\alpha$, $\lambda$, $\Lambda$ et la phénoménologie
   galaxies. Le choix « QCD » a l'avantage de supprimer le problème de hiérarchie ; il a le
   coût de devoir refaire le secteur sombre (§6.3) et l'écrantage.
3. **Calculer $S_{\rm sphal}$** dans MCW-1 (configuration interpolant $n=1\to n=0$ par $\Gamma\to0$,
   énergie finie seulement si $U(1)_\Phi$ est jaugée). Objet bien défini, calculable numériquement.
4. **Vérifier l'anomalie** : les charges des fermions de §5 s'annulent-elles dans
   $\sum_i Y_i^3$ ? Si oui, l'échappatoire 5.2 est fermée et il ne reste que 5.1 / 5.3.

*Note technique — 11/11/2026. Script associé : `ttc_deliement_barrier.py`.*
