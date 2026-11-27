# Zémidjan classement — rejouer une route dans la bonne fenêtre

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/zemidjan-classement/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un service de classement de courses de moto-taxi (zémidjan). Le
> journal `courses.log` révèle une fenêtre temporelle `OPEN`/`CLOSE` ; il faut
> rejouer la route de référence (GrandMarché → … → Agoè) **à l'intérieur** de cette
> fenêtre pour valider. **Flag :** `NCTF{…}`.

## 1. Trouver la fenêtre

`courses.log` contient des marqueurs `OPEN` et `CLOSE` : le service n'accepte un
classement que pendant cet intervalle. Hors fenêtre, tout est rejeté.

## 2. La route attendue

Le même log donne la séquence d'arrêts de référence : `GrandMarché → … → Agoè`.
C'est l'itinéraire exact à soumettre, dans l'ordre.

## 3. Rejouer dans la fenêtre

Je script l'envoi : attendre le `OPEN`, pousser la route complète avant `CLOSE`.
Le timing est serré, donc j'automatise plutôt que de jouer à la main :

```python
wait_for("OPEN")
for stop in route:          # GrandMarché ... Agoè
    send(stop)
# soumission validée avant CLOSE -> flag
```

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons

- **Un challenge PPC teste l'automatisation** : la fenêtre temporelle et la
  longueur de la route rendent la résolution manuelle peu fiable. Scripter la
  lecture du log et l'envoi synchronisé est la clé.
