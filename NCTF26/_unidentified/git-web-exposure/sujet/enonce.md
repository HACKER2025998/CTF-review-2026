# git-web-exposure

- **Catégorie :** ?
- **Auteur :** inconnu (à compléter)
- **Points :** —

## Énoncé

Sur `https://uhyfmune56m5tukt.t.ctf.tg/`, des objets Git accessibles sous `/.git/` ont été recueillis pour reconstruire un dépôt local `/tmp/be_git`. Des essais de `git-dumper`/`dulwich`, `git fsck`, `git log` et lecture d'objets ont permis d'identifier des commits `4d30a7b`, `3502fb0`, `2af9ed0`, `d06c5b7` et une ancienne sauvegarde `backup.zip`. Un message de commit précisait : « Password hint: The password is 'git_history_rules' ». Des changements ultérieurs semblent viser une phrase plus simple, mais aucun flag final n'est visible dans le journal.
