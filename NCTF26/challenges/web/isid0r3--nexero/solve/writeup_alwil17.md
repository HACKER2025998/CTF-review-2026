# Nexero Chat — LFI via l'avatar et le piège du schéma file:

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/nexero/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Nexero préfixe `file:` à l'avatar que je fournis et affiche le fichier
> récupéré. Je ne contrôle que ce qui suit le schéma ; le piège est le nombre de
> slashes : `///etc/passwd` (host vide + chemin absolu) fonctionne là où
> `//etc/passwd` échoue. Un captcha et une PoW gardent l'endpoint. **Flag :**
> `NCTF{…}`.

## 1. La fonctionnalité

La page `/profil` a un champ « chemin de l'avatar ». Le serveur récupère le fichier
et l'affiche : image rendue si c'en est une, sinon le contenu texte brut.

## 2. Le piège du schéma file:

Le serveur préfixe `file:` à ma saisie — je ne contrôle que la suite. La syntaxe du
protocole `file:` est le vrai piège :

- `//etc/passwd` (2 slashes) → échec : interprété comme `host=etc`, `path=/passwd` ;
- `///etc/passwd` (3 slashes) → OK : host vide + chemin absolu `/etc/passwd`.

## 3. Passer les gardes, confirmer la LFI

L'endpoint est précédé d'un captcha arithmétique et d'une **PoW SHA-256** calculée
en JS côté navigateur. Une fois les deux validés, je saisis :

```
///etc/passwd
```

`/etc/passwd` s'affiche — lecture de fichiers arbitraires confirmée.

## 4. Lire le flag

```
///flag.txt
```

Le flag apparaît dans le cadre de résultat.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Ne pas construire d'URL `file:` à partir d'entrée utilisateur.** Servir les
  avatars depuis un stockage dédié, par identifiant, jamais par chemin.
- Captcha et PoW freinent le brute-force mais **ne corrigent pas** la LFI : la
  validation du chemin doit se faire côté serveur (racine verrouillée, pas de
  schéma arbitraire).
