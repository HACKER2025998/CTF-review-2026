### 17. GhostFlag — fichier de credentials, agent et faux flag — `thierry8petstar--ghostflag`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `https://aubq2mwietezp2g3.t.ctf.tg/`

**Fichiers d’origine associés :** `Pasted text(20261107-211824).txt`, `Pasted text(20261107-212850).txt`.

#### Énoncé, contexte et périmètre

La page d'accueil GhostFlag contient un commentaire de développeur concernant un dossier `fnd_password` non sécurisé. L'URL `/secret_files/fnd_password/credentials.txt` a exposé un identifiant d'agent `GHOST-4712` et un mot de passe fictif `P@ssw0rd_2026!`. L'endpoint `/api/agent/check` acceptait un identifiant d'agent en JSON et renvoyait un texte ressemblant à un flag. Le nom même `FAK3_F14G` signale le leurre. Les routes `/admin` et `/backup` renvoyaient 403 ; nombre de chemins inconnus répondaient 200 avec la page d'accueil fallback.

#### Reconnaissance, commandes et résultats observés

Nous avons tenté des chemins encodés, des barres obliques variantes, des en-têtes `X-Forwarded-Host` et des requêtes parallèles. Les fichiers `Pasted text(20261107-211824).txt` et `Pasted text(20261107-212850).txt` gardent les réponses et timeouts. Aucun vrai flag n'a été capturé.

#### Procédure de reproduction ou reprise technique

```bash
curl -i 'https://<instance>/secret_files/fnd_password/credentials.txt'
curl -i 'https://<instance>/admin'
# Réponse 200 sur une page fallback != route d'administration accessible.
```

#### Résultat / flag

**LEURRE : NCTF{FAK3_F14G_TR0P_F4CILE_OUBIEN?}**

#### Pièges, interprétation et enseignement

Identifiant et mot de passe sont les données du challenge, non des secrets de l'utilisateur. Le leurre n'est pas une validation.
