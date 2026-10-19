# Tutoriel : des agents Claude pour gerer une bibliotheque de photos

Ce tutoriel montre comment construire un systeme de subagents Claude Code pour aider a gerer une
bibliotheque de photos personnelles — pas pour remplacer une application de stockage photo, mais
pour analyser et rapporter au-dessus de celle-ci (metadonnees, doublons, sauvegardes, albums,
cout de stockage, confidentialite).

Si tu ne connais pas encore la mecanique de base des subagents (anatomie, ou les ranger, comment
les invoquer), lis d'abord le
[tutoriel general](../../docs/tutoriel-creer-des-agents-claude.md) : ce document part directement
sur l'application au cas "photos".

## 1. Principe : des agents qui analysent, jamais qui agissent

Une bibliotheque de photos est un patrimoine personnel irremplacable. Le risque principal d'un
agent automatise ici n'est pas qu'il se trompe dans un rapport (facile a corriger), c'est qu'il
**supprime, deplace ou partage quelque chose par erreur** (souvent irreversible, ou tres couteux a
reparer). Ce projet applique donc une regle stricte, repetee dans `CLAUDE.md` et dans chaque
subagent :

> Un subagent lit, analyse et ecrit un rapport Markdown. Il ne supprime, ne deplace, ne renomme,
> n'archive, ne partage et ne publie jamais un fichier lui-meme. C'est toujours l'utilisateur qui
> agit, dans son application de stockage photo ou son gestionnaire de fichiers, apres avoir lu le
> rapport.

C'est le meme principe de gouvernance que dans `travel-planner-agent/` (qui ne reserve ni ne paie
jamais a la place de l'utilisateur) : les agents preparent la decision, ils ne la prennent pas.

## 2. Les 6 subagents

| Subagent | Role | A lancer... |
|---|---|---|
| `metadata-enricher` | Lit l'EXIF (date, GPS, appareil), resout le lieu, propose une legende d'accessibilite | A chaque nouvel import |
| `duplicate-detector` | Repere doublons exacts (hash) et quasi-doublons (similarite), propose lequel garder | Avant tout archivage ou nettoyage (proactif) |
| `backup-integrity-checker` | Compare bibliotheque source et sauvegarde (fichiers manquants, hash different, orphelins) | Regulierement, en tache planifiee |
| `album-curator` | Regroupe les photos deja enrichies par date/lieu, propose des titres d'album | Une fois les metadonnees enrichies |
| `storage-cost-optimizer` | Mesure la croissance du stockage, propose des candidats a l'archivage froid | Quand le volume devient une preoccupation |
| `privacy-reviewer` | Verifie GPS precis et elements visibles sensibles avant un partage | Avant toute publication/partage externe (proactif) |

Chaque subagent est un fichier Markdown dans `.claude/agents/`, avec un champ `description` qui dit
explicitement quand l'utiliser (et parfois quand ne pas l'utiliser) — c'est ce que Claude Code lit
pour decider automatiquement quel subagent invoquer face a une demande.

Exemple (en-tête de `duplicate-detector.md`) :
```markdown
---
name: duplicate-detector
description: A utiliser pour reperer des photos probablement dupliquees ou quasi-identiques dans une bibliotheque. Proposer une liste a valider, ne jamais supprimer un fichier. Utiliser PROACTIVEMENT avant tout archivage ou nettoyage de bibliotheque.
tools: Read, Bash, Write
model: sonnet
skills: duplicate-report
---
```

Deux pièges à connaître dans cet en-tête (c'est du YAML) :
- `skills: duplicate-report` **précharge** la Skill de format dans le subagent : sans ce champ, il ne
  voit pas forcément la Skill et risque d'inventer son propre format ;
- dans `description`, évite la suite de caractères `: ` (deux-points + espace), par exemple
  `(ex: deplacer...)` : le YAML devient invalide et le subagent n'est pas chargé. Écris
  `(par exemple ...)` ou mets la description entre guillemets.

## 3. Les Skills : un format de rapport standard

Chaque subagent ecrit son resultat en suivant une Skill (`.claude/skills/<nom>/SKILL.md`), qui
impose un gabarit Markdown fixe. L'interet : que l'utilisateur (ou un autre agent, ou un script)
puisse lire n'importe quel rapport `backup-integrity` sans avoir a redecouvrir sa structure chaque
fois.

| Skill | Utilisee par | Premiere ligne du document |
|---|---|---|
| `metadata-report` | `metadata-enricher` | Resume (dates/GPS manquants) |
| `duplicate-report` | `duplicate-detector` | Resume (groupes de doublons) |
| `backup-integrity-report` | `backup-integrity-checker` | **STATUT GLOBAL** (a jour / action requise) |
| `album-proposal` | `album-curator` | Liste des albums proposes |
| `storage-cost-report` | `storage-cost-optimizer` | Taille totale + croissance |
| `privacy-scan-report` | `privacy-reviewer` | **VERDICT** (OK pour partage / a nettoyer) |

Les deux Skills `backup-integrity-report` et `privacy-scan-report` imposent un statut en toutes
lettres sur la premiere ligne : ce sont les deux rapports ou une personne pressee doit pouvoir
savoir en une seconde si une action est necessaire, sans lire tout le document.

## 4. Pourquoi pas de hash de contenu naif pour les doublons ?

Un hash exact (sha256) ne detecte que des fichiers strictement identiques bit a bit. Deux photos
de la meme scene prises a quelques secondes d'intervalle (rafale), ou la meme photo re-exportee a
une qualite differente, auront des hash totalement differents mais sont visuellement des
quasi-doublons. La pratique courante pour ce cas est le **hachage perceptuel** (perceptual
hashing, ex. pHash/dHash) : deux images visuellement proches produisent des hash proches, meme
sans etre identiques bit a bit — voir l'explication detaillee de
[Ben Hoyt sur la detection de doublons par hachage perceptuel](https://benhoyt.com/writings/duplicate-image-detection/).
C'est pour ca que le subagent `duplicate-detector` et sa Skill distinguent explicitement "doublons
exacts" (hash de contenu) et "quasi-doublons" (similarite estimee, a verifier par l'utilisateur) —
jamais presentes avec le meme niveau de certitude.

## 5. Sauvegarde : s'inspirer de la regle 3-2-1

Le subagent `backup-integrity-checker` ne remplace pas une strategie de sauvegarde, il **verifie**
qu'une sauvegarde existante est complete et non corrompue. La regle classique pour une
bibliotheque photo est la regle "3-2-1" : au moins 3 copies des fichiers, sur 2 types de support
differents, dont 1 copie hors site — voir par exemple
[l'explication de Shutter Muse sur la strategie de sauvegarde 3-2-1 pour les photographes](https://shuttermuse.com/what-is-3-2-1-backup-strategy)
ou [le guide d'IONOS sur la sauvegarde de photos](https://www.ionos.com/en-ie/digitalguide/server/security/photo-backup/).
`backup-integrity-checker` peut etre lance une fois par copie de sauvegarde (NAS local, disque
externe, service cloud) pour verifier chacune independamment.

## 6. Metadonnees et confidentialite : pourquoi un subagent dedie

Une photo contient souvent plus d'informations que ce qu'on voit a l'ecran : coordonnees GPS
precises, modele d'appareil, parfois l'heure a la seconde. Voir par exemple
[le guide de Fast.io sur l'extraction des metadonnees de geolocalisation des photos](https://www.fast.io/resources/geolocation-metadata-extraction-from-photos.md)
et [la sensibilisation du FBI (bureau de Portland) sur les risques des donnees EXIF](https://www.fbi.gov/contact-us/field-offices/portland/news/press-releases/oregon-fbi-tech-tuesday-building-a-digital-defense-against-dangers-of-exif-data).
C'est pour ca que ce projet separe clairement :
- `metadata-enricher` : **utilise** le GPS pour enrichir (resoudre un lieu), en interne.
- `privacy-reviewer` : **verifie** avant tout partage que ce meme GPS (et tout element visible
  sensible dans l'image) ne va pas sortir accidentellement de la bibliotheque.

Ne jamais fusionner ces deux roles en un seul subagent : l'un enrichit pour un usage interne,
l'autre protege avant un usage externe — les confondre risquerait de republier du GPS precis sans
y penser.

## 7. Automatisation : pourquoi pas un simple workflow GitHub Actions cloud

Dans `travel-planner-agent/`, la veille tarifaire tourne dans un workflow GitHub Actions cloud
(`price-watch.yml`) parce qu'elle n'interroge que des API web. Une bibliotheque de photos est en
general sur un disque local ou un NAS domestique : un runner GitHub Actions dans le cloud n'y a pas
acces. Ce projet est donc pense pour une execution **locale** planifiee.

Exemple de ligne crontab (`crontab -e` sur une machine Linux/macOS où le dépôt est cloné et où la
bibliothèque est accessible) pour lancer la vérification de sauvegarde chaque dimanche à 7h. Une ligne
crontab doit tenir sur **une seule ligne** (pas de `\` de continuation), et cron ne charge pas ton
profil shell : il faut donc donner des chemins absolus et la clé API (ici lue depuis un fichier `.env`
non commité) :
```cron
0 7 * * 0 . /chemin/vers/photo-storage-agent/.env && /chemin/vers/photo-storage-agent/.venv/bin/python /chemin/vers/photo-storage-agent/agent-sdk/check_backup_integrity.py --source /chemin/photos --backup /chemin/sauvegarde >> /chemin/vers/photo-storage-agent/reports/cron.log 2>&1
```
avec un fichier `.env` contenant `export ANTHROPIC_API_KEY=...` (déjà ignoré par Git).

Les scripts de `agent-sdk/` tournent avec des garde-fous stricts (`permission_mode="dontAsk"`, seule
commande shell autorisée : `./scripts/hash_scan.sh`, écriture limitée à `reports/`, plafond de coût) :
voir [`agent-sdk/README.md`](../agent-sdk/README.md). Le script `hash_scan.sh` produit des **chemins
relatifs** au dossier scanné, ce qui permet de comparer directement l'inventaire de la bibliothèque et
celui de sa sauvegarde.

Si ta bibliotheque est elle-meme hebergee sur un service accessible par API (un bucket cloud avec
API REST, par exemple), le meme principe que `price-watch.yml` redevient applicable : un workflow
planifie dans le cloud peut alors fonctionner, puisqu'il n'a plus besoin d'un disque local.

## 8. Scenario complet

1. Import d'un nouveau lot de photos de vacances → `metadata-enricher` enrichit dates, lieux,
   legendes → `reports/metadata/vacances-2026.md`.
2. Avant de nettoyer le dossier d'import → `duplicate-detector` → `reports/duplicates/vacances-2026.md`
   → l'utilisateur supprime lui-meme les doublons valides.
3. `album-curator` regroupe les photos enrichies → `reports/albums/vacances-2026.md` → l'utilisateur
   cree les albums dans son application de stockage.
4. Chaque dimanche (cron) → `backup-integrity-checker` → `reports/backup-integrity/<date>.md` → si
   "ACTION REQUISE", l'utilisateur relance une sauvegarde.
5. Avant de partager 3 photos sur un reseau social → `privacy-reviewer` →
   `reports/privacy-scan/<lot>.md` → l'utilisateur nettoie les metadonnees si necessaire avant de
   publier.
6. Une fois par trimestre, ou a une alerte de quota → `storage-cost-optimizer` →
   `reports/storage-cost/<date>.md` → l'utilisateur decide d'archiver ou non les candidats
   proposes.

## 9. Limites et bonnes pratiques

- Les agents ne remplacent pas une vraie strategie de sauvegarde (3-2-1) : ils la **verifient**.
- "Quasi-doublon" et "candidat a l'archivage" sont toujours des propositions, jamais des
  certitudes : valider ligne par ligne avant toute action destructive.
- Toute donnee sensible (GPS precis, information personnelle visible) reste dans le rapport
  interne, jamais republiee automatiquement ailleurs.
- Pas d'invention de donnees : si une metadonnee est absente, le rapport le dit explicitement.
- Comme pour les deux autres projets de ce depot, chaque subagent a un `tools` et une
  `description` restreints a son role precis — ca limite le risque qu'un agent fasse "un peu plus
  que prevu".

## 10. Pour aller plus loin

- [Claude Code Subagents: A 2026 Practical Guide (Tembo)](https://tembo.io/blog/claude-code-subagents)
- [Duplicate image detection with perceptual hashing in Python (Ben Hoyt)](https://benhoyt.com/writings/duplicate-image-detection/)
- [What Is a 3-2-1 Backup Strategy and How Should Photographers Use It? (Shutter Muse)](https://shuttermuse.com/what-is-3-2-1-backup-strategy)
- [How to back up photos (IONOS Digital Guide)](https://www.ionos.com/en-ie/digitalguide/server/security/photo-backup/)
- [How to Extract Geolocation Metadata from Photos (Fast.io)](https://www.fast.io/resources/geolocation-metadata-extraction-from-photos.md)
- [Building a Digital Defense Against Dangers of EXIF Data (FBI, bureau de Portland)](https://www.fbi.gov/contact-us/field-offices/portland/news/press-releases/oregon-fbi-tech-tuesday-building-a-digital-defense-against-dangers-of-exif-data)

### Podcasts
- [Everyday AI Podcast — "Desktop agent lingo simplified: goals, loops, plans, subagents..."](https://podcastrex.com/shows/everyday-ai-podcast-an-ai-and-chatgpt-podcast/ep-806-desktop-agent-lingo-simplified-goals-loops-plans-subagents-and-how-it-works-in-codex-and-claude-code)
- [Inside Photo Organizing — "Season 4, Episode 32: Ana Carvajal on metadata"](https://shows.acast.com/inside-photo-organizing/episodes/season-4-episode-32-ana-carvajal-on-metadata)
- [Privacy Files — "The Data Your Photos Leak"](https://pocketcasts.com/podcast/privacy-files/ec8c8f10-6f7f-013b-f263-0acc26574db2/the-data-your-photos-leak/8a8eb56b-18cb-4666-8ae5-5b53c2bc902b)
