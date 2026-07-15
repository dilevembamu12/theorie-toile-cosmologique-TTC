# 📋 SKILLS.md — Commandes Git & Workflow

> Fiche pratique pour la gestion du dépôt TTC (Théorie de la Toile Cosmologique)

---

## 🚀 Commandes essentielles

### Voir l'état du dépôt
```bash
git status
git log --oneline -10
git log --graph --oneline --all
```

### Ajouter et commiter
```bash
git add -A
git commit -m "Description du changement"
# OU en une ligne :
git add -A ; git commit -m "Description"
```

### Pousser vers GitHub
```bash
git push origin master
# Première fois (si branche non suivie) :
git push -u origin master
```

### Récupérer les mises à jour
```bash
git pull origin master
```

---

## 🌿 Branches

```bash
git branch                        # Lister les branches locales
git branch -a                     # Lister toutes (locales + distantes)
git checkout -b nom-branche       # Créer et basculer sur une nouvelle branche
git checkout master               # Revenir sur master
git merge nom-branche             # Fusionner une branche dans la branche courante
git branch -d nom-branche         # Supprimer une branche locale
```

---

## ⏪ Annulations

```bash
git reset --soft HEAD~1           # Défaire le dernier commit (garde les modifs)
git reset --hard HEAD~1           # Défaire le dernier commit (perd les modifs !!)
git checkout -- nomfichier        # Restaurer un fichier modifié
git revert HEAD                   # Créer un commit inverse (safe)
```

---

## 📦 Gestion du remote

```bash
git remote -v                     # Voir les remotes configurés
git remote add origin <URL>       # Ajouter un remote
git remote set-url origin <URL>   # Changer l'URL du remote
git remote remove origin          # Supprimer le remote
```

---

## 🏷️ Tags (versions)

```bash
git tag                           # Lister les tags
git tag -a v1.0 -m "Version 1.0"  # Créer un tag annoté
git push origin v1.0              # Pousser un tag
git push origin --tags            # Pousser tous les tags
```

---

## 🔍 Utilitaires

```bash
git diff                          # Voir les modifications non stagées
git diff --staged                 # Voir les modifications stagées
git rm --cached fichier           # Enlever un fichier du suivi (garde en local)
git blame fichier                 # Voir qui a modifié quoi
```

---

## ⚙️ Configuration locale (déjà faite)

```bash
git config user.name "dilevembamu12"
git config user.email "emodiembamu@gmail.com"
```

---

## 📂 Structure du dépôt

```
DEEPSEEK/
├── .gitignore                     # Fichiers exclus du suivi
├── README.md                      # Description du projet
├── SKILLS.md                      # Ce fichier — Aide-mémoire Git
├── TTC-White-Paper.md             # White Paper principal
├── TTC-session-globale.md         # Journal de session complet
├── TTC-benchmark-catalogue.md     # Catalogue des postulats & formules
├── TTC-maxwell-derivation.md      # Dérivation Maxwell depuis TTC
├── TTC-puissance-max-onde.md      # Puissance maximale des ondes TTC
├── TTC-note-Pmax-c5-sur-G.md      # Note Pmax, c⁵/G
├── TTC-demo-Pmax-etape-par-etape.md # Démo pas à pas
├── TTC-tully-fisher-sparc.md      # Test Tully-Fisher sur données SPARC
├── TTC-thumbnail-Pmax.html        # Visuel thumbnail
├── analyse-critique-TTC-deepseek.md # Analyse critique complète
├── critique-contreverification-chatgpt.md # Contre-vérification
├── sparc_analysis.py              # Script analyse SPARC
├── tcm1d_v2_spherical.py          # Modèle sphérique MCW-1
├── test_aTTC.py                   # Test aTTC
├── test_tully_fisher.py           # Test Tully-Fisher
├── test_tully_fisher_v2.py        # Test Tully-Fisher v2
├── mcw1_dwarf_fixed/              # Résultats MCW-1 naines corrigées
├── mcw1_output/                   # Résultats MCW-1 output
├── mcw1_sparc_results/            # Résultats MCW-1 SPARC
└── SPARC_data/                    # Données SPARC (175 galaxies)
```

---

> **Dernière mise à jour :** 15 juillet 2026 — Dileve MBAMU & DeepSeek V4 Pro
