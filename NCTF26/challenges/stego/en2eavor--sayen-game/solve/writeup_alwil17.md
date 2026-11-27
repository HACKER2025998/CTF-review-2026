# Sayen Game — un mot de passe caché dans un forum, un PNG tronqué, une archive 7z

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/sayen-game/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un faux forum cache un mot de passe dans la dernière lettre d'un
> message sur deux. Ce mot de passe ouvre un endpoint `UPDATE /game` qui renvoie
> deux base64 collés : un PNG et une archive 7z chiffrée. La hauteur du PNG est
> falsifiée dans l'`IHDR` ; en la corrigeant, une bande de couleurs apparaît, et
> ces couleurs décodent le mot de passe du 7z qui contient le flag. **Flag :**
> `NCTF{…}`.

## 1. Le forum

La page d'accueil est un fil sur « GTA VI » : 240 messages écrits en dur dans le
JavaScript (`const messages=[...]`). Un `Ctrl+U` me donne tout d'un coup, sans
parcourir les pages.

## 2. Le mot de passe caché

Un membre, Niko, poste un message sur cinq. Un de ses messages sur deux (6, 16,
26, … 236) se termine par une phrase ajoutée, sans rapport avec le reste :

- message 6 : « …qui restent dans nos souvenir**s** »
- message 16 : « …aux scènes avec Luci**a** »
- message 26 : « …chaque plan du traile**r** »

Je prends la dernière lettre de chacun, de 6 à 236 :

```
sarAkawAViViyad3Akpenami
```

Les majuscules viennent de mots en capitales (GT**A**, I**V**, SU**V**), mais le
serveur n'accepte que les minuscules :

```
sarakawaviviyad3akpenami
```

## 3. L'endpoint

```bash
curl -X UPDATE http://HOTE:8080/game \
  -H 'Content-Type: application/json' \
  -d '{"password":"sarakawaviviyad3akpenami"}' -o arena.txt
```

## 4. Deux base64 dans la réponse

`arena.txt` contient deux blocs base64 collés. Le premier finit par
`SUVORK5CYII=` (fin de PNG), le second commence par `N3q8ryc` (signature 7z). Je
coupe après le premier `=` :

```bash
sed 's/=/=\n/' arena.txt > parts.txt
head -1 parts.txt | base64 -d > arena.png
tail -1 parts.txt | base64 -d > file.7z
```

`file.7z` est chiffré et contient `takeit.txt`. Le mot de passe est dans l'image.

## 5. La hauteur falsifiée du PNG

`arena.png` s'affiche en 1536×800, mais le fichier est trop lourd pour ça : les
données IDAT contiennent plus de lignes que l'en-tête n'en annonce. Avec TweakPNG,
j'édite le chunk `IHDR` et je passe `Height` de `800` à `1024` (le CRC est
recalculé automatiquement).

L'image fait maintenant 1536×1024, et une bande de 14 carrés de couleur apparaît
en bas, sous le dessin.

## 6. Les couleurs → le mot de passe

Les 14 couleurs se décodent (table « Gravity Falls ») en le mot de passe du 7z,
en majuscules. J'extrais `takeit.txt` :

```bash
7z x -p'<MOT_DE_PASSE>' file.7z
cat takeit.txt   # NCTF{…}
```

## 7. Flag

```text
NCTF{…}
```

## 8. Leçons

- **Lire la source** d'abord : tout le forum était en clair dans le JS, inutile de
  cliquer 6 pages.
- **Comparer poids et dimensions** d'un PNG : un fichier « trop gros » cache
  souvent des lignes au-delà de la hauteur déclarée dans l'`IHDR`.
- Une chaîne stego peut empiler plusieurs couches (forum → endpoint → PNG →
  7z) ; garder une trace de chaque artefact extrait.
