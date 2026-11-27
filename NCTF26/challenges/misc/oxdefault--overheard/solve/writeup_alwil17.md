# Overheard — déchiffrer un WPA2 pour écouter une session d'admin

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/overheard/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — On me donne une capture WPA2-PSK et la clé du réseau
> (`CorpNet` / `Pr1nt3r-2024!`). Je déchiffre le trafic avec le SSID et la PSK,
> et je remonte une session d'administration entre deux serveurs internes où
> passe le flag. **Flag :** `NCTF{…}`.

## 1. Briefing

Une capture `capture.pcapng` prise sur le canal d'un bureau pendant une session
d'admin, plus une note :

```
SSID : CorpNet
PSK  : Pr1nt3r-2024!   (WPA2-PSK / CCMP)
Deux serveurs internes apparaissent dans le trafic.
```

## 2. Analyse

Le trafic est chiffré en WPA2-CCMP, mais j'ai la PSK **et** le SSID. Le couple
(SSID, PSK) dérive la PMK, et le 4-way handshake présent dans la capture fournit
les nonces pour dériver la PTK de chaque session — donc je peux tout déchiffrer.

## 3. Exploitation

### Déchiffrer la capture

Avec Wireshark : *Preferences → Protocols → IEEE 802.11 → Decryption keys* →
ajouter `wpa-pwd : Pr1nt3r-2024!:CorpNet`. (En ligne de commande, `airdecap-ng -e
CorpNet -p 'Pr1nt3r-2024!' capture.pcapng` produit l'équivalent de
`capture.pcapng-dec`.)

Il faut que le 4-way handshake soit dans la capture pour que la dérivation
réussisse — c'est le cas ici.

### Suivre la session d'admin

Une fois en clair, deux serveurs internes dialoguent. Je suis les flux TCP
(`Follow TCP Stream`) de la session d'administration ; le flag y transite (console
d'admin, dont la clé `console.key` accompagne la capture pour la partie
éventuellement chiffrée au-dessus).

## 4. Flag

```text
NCTF{…}
```

## 5. Leçons & remédiation

- **WPA2-PSK n'est pas de la confidentialité** dès que la PSK fuite : quiconque a
  la clé **et** le handshake déchiffre tout le trafic a posteriori.
- Préférer WPA2-Enterprise (clés par utilisateur) ou WPA3 (forward secrecy via
  SAE), et chiffrer les sessions d'administration au-dessus (SSH/TLS) pour que la
  capture Wi-Fi ne suffise pas.
