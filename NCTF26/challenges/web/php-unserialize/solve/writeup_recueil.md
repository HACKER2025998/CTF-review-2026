### 33. Portail PHP — base64(serialize) et __wakeup — `php-unserialize`

**Statut :** NON CONFIRMÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `index.php`, `session_cookie.b64`.

#### Énoncé, contexte et périmètre

Le fichier source `index.php` est un handout : le cookie est `base64(serialize($obj))` et l'application envoie la donnée vers `unserialize()`. La classe de session de l'exemple possède `uid` et `role`. Une classe `FlagReveal` déclenche dans `__wakeup()` une décryption liée à un seed de maintenance `rot-2026-maintenance`. Le cookie invité `session_cookie.b64` est fourni comme base de travail.

#### Reconnaissance, commandes et résultats observés

Le point critique est l'utilisation de `unserialize()` sur une entrée non fiable : même une session au rôle invité peut permettre d'instancier une classe et d'exécuter une méthode magique. Aucun essai concluant de désérialisation ni flag final n'est contenu dans les journaux disponibles.

#### Procédure de reproduction ou reprise technique

```bash
base64 -d session_cookie.b64
sed -n '1,180p' index.php
```
Étudier le code et les propriétés de `FlagReveal` avant de construire toute charge utile ; ne pas exécuter du PHP inconnu côté hôte.

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

La sérialisation native n'est pas une méthode sûre pour les cookies utilisateurs ; préférer jetons de session côté serveur.
