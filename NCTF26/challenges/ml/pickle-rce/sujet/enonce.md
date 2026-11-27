# pickle-rce

- **Catégorie :** ml
- **Auteur :** inconnu (à compléter)
- **Points :** ?

## Énoncé

ModelHub charge un pickle uploadé et renvoie repr(objet chargé). Le flag est dans /flag sur l'hôte, jamais renvoyé. But : faire en sorte que l'objet chargé SOIT le contenu de /flag. Bac à sable : refuse os, subprocess, sys, builtins, importlib, ... Leurre : /flag.decoy (à ignorer).
