### 41. The Armory — service SSH — `koth-armory`

**Statut :** NON RÉSOLU · **Points :** 5 points/tick · **Instance :** `ssh://player@13.37.197.230:28492`

**Fichiers d’origine associés :** `Pasted markdown(1).md`.

#### Énoncé, contexte et périmètre

Colline SSH sur `13.37.197.230:28492`, OpenSSH 8.9 annoncé, cinq points par tick. Le scénario demandait de placer un jeton d'équipe sur le service qui attribue la couronne.

#### Reconnaissance, commandes et résultats observés

Les notes de reconnaissance ne montrent ni authentification SSH réussie ni prise de la colline. Nous conservons l'identité et le port de l'épreuve sans inventer une solution.

#### Procédure de reproduction ou reprise technique

```bash
nmap -sV -Pn -p 28492 13.37.197.230
ssh -p 28492 player@13.37.197.230
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Le règlement de la compétition était distinct de celui des challenges Web permanents.
