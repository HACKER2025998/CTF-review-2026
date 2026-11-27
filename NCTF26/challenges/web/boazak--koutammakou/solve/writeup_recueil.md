### 18. Koutammakou — upload ZIP Slip / SSTI — `boazak--koutammakou`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `https://v2vvjuadx2dxbpgf.t.ctf.tg/`

**Fichiers d’origine associés :** `Pasted text(20261107-144123).txt`.

#### Énoncé, contexte et périmètre

Le scénario comporte un service d'upload et de consultation de fichiers ; les explorations visaient une extraction ZIP vulnérable au **ZIP Slip** et une injection de templates. La trace contient des chemins tels que `/uploads/..%2fflag`, `/uploads/%2e%2e%2fflag.txt`, `/uploads/../../app/flag.txt` et des chemins imbriqués sous un identifiant d'upload. L'instance testée était `https://v2vvjuadx2dxbpgf.t.ctf.tg/`. La cible `/flags/flag.txt` a été évoquée dans les essais précédents, sans preuve de lecture de son contenu.

#### Reconnaissance, commandes et résultats observés

Les réponses des chemins livrés étaient majoritairement des 404. Un ZIP Slip survient d'abord à l'**extraction d'un membre d'archive** dont le nom contient `../`; une requête HTTP vers `/uploads/../flag` n'est pas automatiquement un exploit ZIP Slip. L'hypothèse SSTI nécessite également de reconnaître quel champ est interprété par quel moteur de rendu.

#### Procédure de reproduction ou reprise technique

```bash
curl --path-as-is -i 'https://<instance>/uploads/..%2fflag'
# Pour tester ZIP Slip, inspecter d'abord le flux d'upload et le répertoire d'extraction.
```

#### Résultat / flag

**Aucun**

#### Pièges, interprétation et enseignement

Une erreur 404 sur des traversées d'URL ne démontre pas que les chemins d'archive seraient correctement neutralisés.
