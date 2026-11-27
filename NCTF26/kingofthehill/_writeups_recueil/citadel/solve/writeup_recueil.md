### 40. The Citadel — service SSH — `koth-citadel`

**Statut :** NON RÉSOLU · **Points :** 5 points/tick · **Instance :** `ssh://player@13.37.197.230:28491`

**Fichiers d’origine associés :** `Pasted markdown(1).md`.

#### Énoncé, contexte et périmètre

Colline SSH sur `13.37.197.230:28491`, OpenSSH 8.9 annoncé, cinq points par tick. L'objectif KOTH consiste à obtenir le contrôle autorisé de la colline et inscrire le jeton d'équipe. Les sorties précédentes recommandaient une inspection de bannière et une connexion `player`, sans trace de succès.

#### Reconnaissance, commandes et résultats observés

Aucune prise ni identité d'accès valide démontrée. La présence d'un port SSH ne permet pas à elle seule de déduire des identifiants faibles.

#### Procédure de reproduction ou reprise technique

```bash
nmap -sV -Pn -p 28491 13.37.197.230
ssh -p 28491 player@13.37.197.230
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Ne pas dépasser le périmètre du jeu ni partager les jetons KOTH.
