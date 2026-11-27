# Glingo — du DTMF à un BBS de 1995

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/glingo/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un enregistrement audio : tonalité, 9 bips DTMF, sonnerie, puis un
> modem à 2100 Hz. Je décode les DTMF en un numéro de téléphone, je le remets dans
> son contexte historique (indicatif 1955), et une recherche OSINT le retrouve dans
> une liste de BBS Fidonet de 1995 — le **nom du BBS** est le flag. **Flag :**
> `NCTF{…}`.

## 1. Analyser l'audio

Au spectrogramme (Audacity / Sonic Visualiser), trois parties :

- **0–3 s** — une tonalité de ligne puis **9 bips**, chacun à deux fréquences
  superposées → **DTMF** (touches de téléphone) ;
- **3–12 s** — la sonnerie ;
- **12 s → fin** — un sifflement à **2100 Hz** puis du bruit large bande → un
  **modem** qui décroche.

## 2. Décoder les DTMF

```bash
sox glingo.mp3 -t raw -r 22050 -e signed -b 16 -c 1 - | multimon-ng -t raw -a DTMF -
```

Résultat : `0441 81652`.

## 3. Replacer le numéro

`0441` est un ancien indicatif régional (1955). En format international :
`27-441-81652`.

## 4. OSINT — le BBS

En 1995, un modem au bout du fil = presque toujours un **BBS**. Je cherche le numéro
sous ses différentes formes et je tombe sur une liste Fidonet archivée :

```
Herold   <BBS NAME>   27-441-81652   . So. Eu. . .   5:7104/40
```

Colonnes : `Lieu | Nom du BBS | Téléphone | Echos | Adresse Fidonet`. Le **nom du
BBS** (2ᵉ colonne) donne le flag, en respectant la casse de la source.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons

- **Reconnaître une modulation au spectrogramme** (DTMF = paires de fréquences,
  modem = porteuse) oriente tout le reste.
- Un simple numéro devient une piste OSINT une fois replacé dans son époque : ici
  les archives de BBS Fidonet.
