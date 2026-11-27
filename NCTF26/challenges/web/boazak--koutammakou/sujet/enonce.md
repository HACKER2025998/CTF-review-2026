# boazak--koutammakou

- **Catégorie :** web
- **Auteur :** boazak
- **Points :** —

## Énoncé

Le scénario comporte un service d'upload et de consultation de fichiers ; les explorations visaient une extraction ZIP vulnérable au **ZIP Slip** et une injection de templates. La trace contient des chemins tels que `/uploads/..%2fflag`, `/uploads/%2e%2e%2fflag.txt`, `/uploads/../../app/flag.txt` et des chemins imbriqués sous un identifiant d'upload. L'instance testée était `https://v2vvjuadx2dxbpgf.t.ctf.tg/`. La cible `/flags/flag.txt` a été évoquée dans les essais précédents, sans preuve de lecture de son contenu.
