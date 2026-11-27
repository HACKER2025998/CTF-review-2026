### 06. Good Luck — Grace D., clavier et mot de passe — `good-luck-photo`

**Statut :** NON RÉSOLU · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `Good_Luck.jpg`, `keyboard_crop.png`, `keys_zoom.png`, `keyfull_bright.png`, `full_small.png`, `note_crop.png`, `legend_crop.png`.

#### Énoncé, contexte et périmètre

**Sujet fourni :** « Ce matin, Grace D., analyste en cybersécurité, arrive au bureau à 8 h 52. Elle pose son café, démarre son ordinateur… puis, 47 secondes plus tard, reçoit un appel d'urgence du SOC. Une alerte critique sur un serveur l'oblige à partir immédiatement. Son bureau est resté exactement dans l'état où elle l'a laissé. Voici une photo prise juste après son départ. Elle n'a consacré que quelques secondes à saisir son mot de passe. Peut-on en déduire qu'il était particulièrement court ? » La photographie montre un clavier 60 % rétroéclairé jaune, un téléphone Samsung, des biscuits, une souris RGB, une note manuscrite `NCTF INVESTIGAT...` et un tapis à lignes topographiques. Le point d'attention demandé par l'utilisateur concerne les **touches qui semblent éteintes**.

#### Reconnaissance, commandes et résultats observés

Un examen visuel précédent indiquait approximativement `5 6`, `R T Y`, `F G H`, `V B` comme touches plus sombres. Des hypothèses `56RTYFGHVB`, `RTYFGHVB` et variantes ont été proposées. **Aucune n'a été soumise avec succès démontré** ; la différence de luminosité n'est pas une preuve que ces touches composent un secret. Le temps de frappe ne permet pas à lui seul d'inférer la longueur d'un mot de passe.

#### Procédure de reproduction ou reprise technique

```bash
file Good_Luck.jpg
exiftool Good_Luck.jpg
strings -a Good_Luck.jpg | grep -Ei 'NCTF|flag|password|hint'
```
Comparer les crops `keys_zoom.png`, `keyboard_crop.png`, `keyfull_bright.png` à l'original pour ne pas interpréter un artefact d'éclaircissement comme une touche éteinte.

#### Résultat / flag

**Flags proposés sans validation : NCTF{56RTYFGHVB}, NCTF{RTYFGHVB}**

#### Pièges, interprétation et enseignement

Ne jamais confondre les suggestions de flag avec un flag observé sur le scoreboard.
