# thierry8petstar--ghostflag

- **Catégorie :** web
- **Auteur :** thierry8petstar
- **Points :** —

## Énoncé

La page d'accueil GhostFlag contient un commentaire de développeur concernant un dossier `fnd_password` non sécurisé. L'URL `/secret_files/fnd_password/credentials.txt` a exposé un identifiant d'agent `GHOST-4712` et un mot de passe fictif `P@ssw0rd_2026!`. L'endpoint `/api/agent/check` acceptait un identifiant d'agent en JSON et renvoyait un texte ressemblant à un flag. Le nom même `FAK3_F14G` signale le leurre. Les routes `/admin` et `/backup` renvoyaient 403 ; nombre de chemins inconnus répondaient 200 avec la page d'accueil fallback.
