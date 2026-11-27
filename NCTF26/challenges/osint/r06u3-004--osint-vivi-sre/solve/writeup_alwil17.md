# osint-vivi — d'Instagram à la rue du suspect

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/osint-vivi/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Je pars d'un profil Instagram, je pivote vers X via une citation
> repérée dans une story, et les commentaires d'un post me placent une clé USB
> perdue « dans le jardin en face de l'hôtel 2 Février ». Google Maps me donne la
> rue, qui est le flag. **Flag :** `NCTF{rue_…}`.

## 1. Instagram

J'accède au profil du suspect : `kof.fi228`. Une publication contient la photo
`indice.jpg` avec l'étiquette de localisation **Togo**. Dans les stories à la une,
une capture d'écran reprend une **citation** que le suspect a publiée sur X.

## 2. Pivot vers X

Je recopie le texte de la citation dans la recherche X. Elle me ramène le compte du
suspect : **`@mensah_kd`**.

## 3. Le compte X

Sur `@mensah_kd`, une publication montre l'environnement de l'**hôtel 2 Février**.
Les commentaires livrent deux informations :

- un compte tiers : « Ce déjeuner à l'hôtel 2 Février était parfait, on devrait y
  retourner. »
- la réponse du suspect : « Si seulement je n'avais pas égaré ma clé USB dans le
  **jardin d'en face**, quand on est allés s'asseoir sur les bancs… »

La clé a donc été perdue dans un jardin situé en face de l'hôtel 2 Février.

## 4. Google Maps

J'examine les espaces verts en face de l'hôtel 2 Février. En recoupant la
géographie, j'identifie la rue — c'est le flag, au format `NCTF{rue_X_X}`.

## 5. Flag

```text
NCTF{rue_…}
```

## 6. Leçons

- **L'OSINT est un jeu de pivots** : chaque plateforme pointe vers la suivante
  (Instagram → story → citation → X → commentaires → lieu physique).
- Côté hygiène : une citation réutilisée à l'identique sur deux comptes suffit à
  les lier ; les commentaires publics géolocalisent sans le vouloir.
