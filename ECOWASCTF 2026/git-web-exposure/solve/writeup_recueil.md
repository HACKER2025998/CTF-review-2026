### 21. Répertoire .git exposé via Web — `git-web-exposure`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `https://uhyfmune56m5tukt.t.ctf.tg/`

**Fichiers d’origine associés :** `Pasted text(20261107-175209).txt`.

#### Énoncé, contexte et périmètre

Sur `https://uhyfmune56m5tukt.t.ctf.tg/`, des objets Git accessibles sous `/.git/` ont été recueillis pour reconstruire un dépôt local `/tmp/be_git`. Des essais de `git-dumper`/`dulwich`, `git fsck`, `git log` et lecture d'objets ont permis d'identifier des commits `4d30a7b`, `3502fb0`, `2af9ed0`, `d06c5b7` et une ancienne sauvegarde `backup.zip`. Un message de commit précisait : « Password hint: The password is 'git_history_rules' ». Des changements ultérieurs semblent viser une phrase plus simple, mais aucun flag final n'est visible dans le journal.

#### Reconnaissance, commandes et résultats observés

Un `.git` exposé est une fuite d'historique : des secrets supprimés des dernières versions peuvent rester dans les blobs antérieurs. Les sorties exactes sont incluses dans les traces afin de ne pas confondre une archive récupérée par HTTP avec `archive(1).zip` fourni séparément.

#### Procédure de reproduction ou reprise technique

```bash
git fsck --full --no-reflogs --unreachable
git log --all --oneline --decorate
git log --all -p
git cat-file -p <object-id>
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Un mot de passe dans une ancienne révision doit être vérifié contre **la bonne archive** ; pas de réutilisation aveugle.
