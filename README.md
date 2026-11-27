# 🏴 CTF Review 2026 — archive de challenges

Archive de révision des CTF joués en 2026 : **NCTF26** (CTF national du Togo, organisé par le CERT.tg — finale à Lomé, 19–20 novembre 2026) et **ECOWAS CTF 2026**. Chaque épreuve est rangée avec son sujet, ses fichiers d’origine, son auteur et, quand il existe, son write-up et ses scripts de résolution.

> Équipe **1HUNTERS** — archive tenue par **xhackerip**. Les write-ups sont rédigés progressivement.

## 📊 En chiffres

| | |
|---|---|
| Épreuves NCTF26 (liste officielle) | **525** |
| Catégories | **25** |
| Auteurs identifiés | **15** |
| ✅ Résolues (flag retrouvé) | 56 |
| 📝 Write-up / scripts en cours | 21 |
| 📁 Fichiers présents, à résoudre | 21 |
| ⏳ Sujet à retrouver | 427 |
| Épreuves ECOWAS CTF 2026 / non identifiées | 59 |

## 🗂️ Organisation du dépôt

```
CTF2026 review/
├── README.md
├── NCTF26/
│   ├── INDEX.md              index détaillé des 525 épreuves (statut, flags)
│   ├── scoreboard.md         suivi des flags pendant la compétition
│   ├── challenges/
│   │   └── <catégorie>/
│   │       └── <épreuve>/
│   │           ├── README.md     catégorie, auteur, statut, provenance
│   │           ├── sujet/        enonce.md — énoncé de l’épreuve
│   │           ├── fichiers/     fichiers fournis (intacts)
│   │           └── solve/        writeup.md + scripts de résolution
│   ├── kingofthehill/       boîte à outils KOTH (6 variantes) + write-ups
│   ├── tools/                utilitaires (connexion, triage, battlekit)
│   └── templates/            gabarits notes.md / solve.py / exploit.py
└── ECOWASCTF 2026/           épreuves hors liste NCTF26 (même structure, voir A_CLASSER.md)
```

Le nom d’une épreuve suit la convention de la plateforme : `auteur--nom-du-challenge` quand l’auteur est connu (ex. `boazak--sodabi`), sinon le nom seul.

## 🚀 Utilisation

```bash
git clone https://github.com/HACKER2025998/CTF-review-2026.git
cd CTF-review-2026/NCTF26/challenges/crypto/fermat-twins
cat sujet/enonce.md        # lire le sujet
ls fichiers/                # fichiers du challenge
python3 solve/solve.py      # rejouer la résolution
```

> ⚠️ **Spoilers** : `solve/`, `INDEX.md` et `scoreboard.md` contiennent les solutions et les flags. Pour s’entraîner, ne lisez que `sujet/` et `fichiers/`.
>
> ⚠️ Certains fichiers sont des **binaires ou scripts malveillants volontaires** (épreuves reverse, pwn, forensics, supply chain). Ne les exécutez que dans une VM isolée.

## 📈 Répartition par catégorie

| Catégorie | Épreuves |
|---|---|
| [ai](#ai) | 13 |
| [blockchain](#blockchain) | 11 |
| [boot2root](#boot2root) | 36 |
| [chains](#chains) | 5 |
| [cloud](#cloud) | 46 |
| [cti](#cti) | 4 |
| [defense](#defense) | 5 |
| [crypto](#crypto) | 86 |
| [forensics](#forensics) | 47 |
| [hardware](#hardware) | 8 |
| [ics](#ics) | 1 |
| [iot](#iot) | 3 |
| [misc](#misc) | 18 |
| [ml](#ml) | 11 |
| [mobile](#mobile) | 13 |
| [networking](#networking) | 11 |
| [osint](#osint) | 13 |
| [ppc](#ppc) | 10 |
| [pwn](#pwn) | 22 |
| [reverse](#reverse) | 29 |
| [stego](#stego) | 15 |
| [supplychain](#supplychain) | 14 |
| [sysadmin](#sysadmin) | 12 |
| [warmup](#warmup) | 16 |
| [web](#web) | 76 |

## ✍️ Auteurs

| Auteur | Épreuves |
|---|---|
| boazak | 87 |
| the-darknova | 40 |
| algorithme123 | 18 |
| komisergio | 16 |
| thierry8petstar | 16 |
| oxdefault | 15 |
| fullaccess5 | 11 |
| isid0r3 | 10 |
| 0xfle1j4i | 7 |
| 44r0nmeta | 7 |
| r06u3-004 | 5 |
| en2eavor | 5 |
| hibris | 2 |
| Clawd | 2 |
| hackusman | 1 |
| _non indiqué_ | 285 |

## 📚 Liste complète des épreuves NCTF26

Légende : ✅ résolue · 📝 write-up / scripts en cours · 📁 fichiers présents · ⏳ sujet à retrouver. Colonnes 📁/🛠️ : fichiers du sujet / scripts de résolution présents.


### ai

_13 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [agent-tool-abuse](NCTF26/challenges/ai/agent-tool-abuse/) | — | 📝 |  | ✔ |
| 2 | [ai0-leaked-transcript](NCTF26/challenges/ai/ai0-leaked-transcript/) | — | ⏳ |  |  |
| 3 | [ai1-naive-guard](NCTF26/challenges/ai/ai1-naive-guard/) | — | 📁 | ✔ |  |
| 4 | [ai2-output-filter](NCTF26/challenges/ai/ai2-output-filter/) | — | ⏳ |  |  |
| 5 | [ai3-tool-abuse](NCTF26/challenges/ai/ai3-tool-abuse/) | — | 📝 |  | ✔ |
| 6 | [mcp-manifest-audit](NCTF26/challenges/ai/mcp-manifest-audit/) | — | ⏳ |  |  |
| 7 | [oracle-canary-decoy](NCTF26/challenges/ai/oracle-canary-decoy/) | — | ⏳ |  |  |
| 8 | [oracle-doc-injection](NCTF26/challenges/ai/oracle-doc-injection/) | — | ⏳ |  |  |
| 9 | [oracle-encoding-smuggle](NCTF26/challenges/ai/oracle-encoding-smuggle/) | — | ⏳ |  |  |
| 10 | [oracle-fake-system](NCTF26/challenges/ai/oracle-fake-system/) | — | ⏳ |  |  |
| 11 | [oracle-multi-turn](NCTF26/challenges/ai/oracle-multi-turn/) | — | ⏳ |  |  |
| 12 | [oracle-reverse-emit](NCTF26/challenges/ai/oracle-reverse-emit/) | — | ⏳ |  |  |
| 13 | [oracle-tool-args](NCTF26/challenges/ai/oracle-tool-args/) | — | ⏳ |  |  |

### blockchain

_11 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [airdrop-forge](NCTF26/challenges/blockchain/airdrop-forge/) | — | ⏳ |  |  |
| 2 | [allowance-drift](NCTF26/challenges/blockchain/allowance-drift/) | — | ✅ | ✔ | ✔ |
| 3 | [bitvault-psbt](NCTF26/challenges/blockchain/bitvault-psbt/) | — | ⏳ |  |  |
| 4 | [block-oracle](NCTF26/challenges/blockchain/block-oracle/) | — | ✅ | ✔ | ✔ |
| 5 | [calldata-cache](NCTF26/challenges/blockchain/calldata-cache/) | — | ✅ | ✔ | ✔ |
| 6 | [origin-story](NCTF26/challenges/blockchain/origin-story/) | — | 📝 | ✔ | ✔ |
| 7 | [overflow-mint](NCTF26/challenges/blockchain/overflow-mint/) | — | ⏳ |  |  |
| 8 | [private-ledger](NCTF26/challenges/blockchain/private-ledger/) | — | 📁 | ✔ |  |
| 9 | [proxy-collision](NCTF26/challenges/blockchain/proxy-collision/) | — | ✅ | ✔ | ✔ |
| 10 | [reentrant-vault](NCTF26/challenges/blockchain/reentrant-vault/) | — | ⏳ |  |  |
| 11 | [replay-signer](NCTF26/challenges/blockchain/replay-signer/) | — | ⏳ |  |  |

### boot2root

_36 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [0xfle1j4i--cartograph](NCTF26/challenges/boot2root/0xfle1j4i--cartograph/) | 0xfle1j4i | ⏳ |  |  |
| 2 | [0xfle1j4i--consent](NCTF26/challenges/boot2root/0xfle1j4i--consent/) | 0xfle1j4i | ⏳ |  |  |
| 3 | [0xfle1j4i--devlog](NCTF26/challenges/boot2root/0xfle1j4i--devlog/) | 0xfle1j4i | ⏳ |  |  |
| 4 | [0xfle1j4i--gitforge](NCTF26/challenges/boot2root/0xfle1j4i--gitforge/) | 0xfle1j4i | ⏳ |  |  |
| 5 | [0xfle1j4i--mailroom](NCTF26/challenges/boot2root/0xfle1j4i--mailroom/) | 0xfle1j4i | ⏳ |  |  |
| 6 | [0xfle1j4i--quill](NCTF26/challenges/boot2root/0xfle1j4i--quill/) | 0xfle1j4i | ⏳ |  |  |
| 7 | [0xfle1j4i--signet](NCTF26/challenges/boot2root/0xfle1j4i--signet/) | 0xfle1j4i | ⏳ |  |  |
| 8 | [44r0nmeta--adzogbo](NCTF26/challenges/boot2root/44r0nmeta--adzogbo/) | 44r0nmeta | ⏳ |  |  |
| 9 | [algorithme123--fret-savane-appui](NCTF26/challenges/boot2root/algorithme123--fret-savane-appui/) | algorithme123 | ⏳ |  |  |
| 10 | [algorithme123--niamtougou-cloud](NCTF26/challenges/boot2root/algorithme123--niamtougou-cloud/) | algorithme123 | ⏳ |  |  |
| 11 | [algorithme123--pal-maintenance](NCTF26/challenges/boot2root/algorithme123--pal-maintenance/) | algorithme123 | ⏳ |  |  |
| 12 | [boazak--adja-annuaires](NCTF26/challenges/boot2root/boazak--adja-annuaires/) | boazak | ⏳ |  |  |
| 13 | [boazak--agou](NCTF26/challenges/boot2root/boazak--agou/) | boazak | ⏳ |  |  |
| 14 | [boazak--akpan-backup](NCTF26/challenges/boot2root/boazak--akpan-backup/) | boazak | ⏳ |  |  |
| 15 | [boazak--alome-commande](NCTF26/challenges/boot2root/boazak--alome-commande/) | boazak | ⏳ |  |  |
| 16 | [boazak--ayimolou-session](NCTF26/challenges/boot2root/boazak--ayimolou-session/) | boazak | ⏳ |  |  |
| 17 | [boazak--cinkasse](NCTF26/challenges/boot2root/boazak--cinkasse/) | boazak | ⏳ |  |  |
| 18 | [boazak--fazao](NCTF26/challenges/boot2root/boazak--fazao/) | boazak | ⏳ |  |  |
| 19 | [boazak--gbekui-membres](NCTF26/challenges/boot2root/boazak--gbekui-membres/) | boazak | ⏳ |  |  |
| 20 | [boazak--korbongou](NCTF26/challenges/boot2root/boazak--korbongou/) | boazak | ⏳ |  |  |
| 21 | [boazak--kpakpato-depot](NCTF26/challenges/boot2root/boazak--kpakpato-depot/) | boazak | 📁 | ✔ |  |
| 22 | [boazak--kpeme](NCTF26/challenges/boot2root/boazak--kpeme/) | boazak | ⏳ |  |  |
| 23 | [boazak--nadoba](NCTF26/challenges/boot2root/boazak--nadoba/) | boazak | ⏳ |  |  |
| 24 | [boazak--sotram-runner](NCTF26/challenges/boot2root/boazak--sotram-runner/) | boazak | ⏳ |  |  |
| 25 | [boot2root-c2](NCTF26/challenges/boot2root/boot2root-c2/) | — | ⏳ |  |  |
| 26 | [boot2root-linux](NCTF26/challenges/boot2root/boot2root-linux/) | — | ⏳ |  |  |
| 27 | [boot2root-ssh](NCTF26/challenges/boot2root/boot2root-ssh/) | — | ⏳ |  |  |
| 28 | [komisergio--agbadza](NCTF26/challenges/boot2root/komisergio--agbadza/) | komisergio | ⏳ |  |  |
| 29 | [komisergio--aneho-b2r](NCTF26/challenges/boot2root/komisergio--aneho-b2r/) | komisergio | ⏳ |  |  |
| 30 | [komisergio--ayimolou](NCTF26/challenges/boot2root/komisergio--ayimolou/) | komisergio | ⏳ |  |  |
| 31 | [komisergio--bassar](NCTF26/challenges/boot2root/komisergio--bassar/) | komisergio | ⏳ |  |  |
| 32 | [komisergio--cda](NCTF26/challenges/boot2root/komisergio--cda/) | komisergio | ⏳ |  |  |
| 33 | [komisergio--djaradjara](NCTF26/challenges/boot2root/komisergio--djaradjara/) | komisergio | ⏳ |  |  |
| 34 | [komisergio--pala](NCTF26/challenges/boot2root/komisergio--pala/) | komisergio | ⏳ |  |  |
| 35 | [komisergio--redteam-tg](NCTF26/challenges/boot2root/komisergio--redteam-tg/) | komisergio | ⏳ |  |  |
| 36 | [r06u3-004--kpakpa](NCTF26/challenges/boot2root/r06u3-004--kpakpa/) | r06u3-004 | ⏳ |  |  |

### chains

_5 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [citadel](NCTF26/challenges/chains/citadel/) | — | ⏳ |  |  |
| 2 | [clinic](NCTF26/challenges/chains/clinic/) | — | ⏳ |  |  |
| 3 | [pipeline](NCTF26/challenges/chains/pipeline/) | — | ⏳ |  |  |
| 4 | [relay](NCTF26/challenges/chains/relay/) | — | ⏳ |  |  |
| 5 | [tokenforge](NCTF26/challenges/chains/tokenforge/) | — | ⏳ |  |  |

### cloud

_46 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [artifacts-envexec](NCTF26/challenges/cloud/artifacts-envexec/) | — | ⏳ |  |  |
| 2 | [artifacts-imds](NCTF26/challenges/cloud/artifacts-imds/) | — | ⏳ |  |  |
| 3 | [artifacts-oidc](NCTF26/challenges/cloud/artifacts-oidc/) | — | ⏳ |  |  |
| 4 | [artifacts-prefix](NCTF26/challenges/cloud/artifacts-prefix/) | — | ⏳ |  |  |
| 5 | [backup-envexec](NCTF26/challenges/cloud/backup-envexec/) | — | ⏳ |  |  |
| 6 | [backup-imds](NCTF26/challenges/cloud/backup-imds/) | — | ⏳ |  |  |
| 7 | [backup-oidc](NCTF26/challenges/cloud/backup-oidc/) | — | ⏳ |  |  |
| 8 | [backup-prefix](NCTF26/challenges/cloud/backup-prefix/) | — | ⏳ |  |  |
| 9 | [backup-presign](NCTF26/challenges/cloud/backup-presign/) | — | ⏳ |  |  |
| 10 | [billing-envexec](NCTF26/challenges/cloud/billing-envexec/) | — | ⏳ |  |  |
| 11 | [billing-imds](NCTF26/challenges/cloud/billing-imds/) | — | ⏳ |  |  |
| 12 | [billing-oidc](NCTF26/challenges/cloud/billing-oidc/) | — | ⏳ |  |  |
| 13 | [billing-prefix](NCTF26/challenges/cloud/billing-prefix/) | — | ⏳ |  |  |
| 14 | [billing-presign](NCTF26/challenges/cloud/billing-presign/) | — | ⏳ |  |  |
| 15 | [breach-chain](NCTF26/challenges/cloud/breach-chain/) | — | ⏳ |  |  |
| 16 | [bucket-pivot](NCTF26/challenges/cloud/bucket-pivot/) | — | ⏳ |  |  |
| 17 | [cdn-imds](NCTF26/challenges/cloud/cdn-imds/) | — | ⏳ |  |  |
| 18 | [cdn-oidc](NCTF26/challenges/cloud/cdn-oidc/) | — | ⏳ |  |  |
| 19 | [cdn-prefix](NCTF26/challenges/cloud/cdn-prefix/) | — | ⏳ |  |  |
| 20 | [gateway-imds](NCTF26/challenges/cloud/gateway-imds/) | — | ⏳ |  |  |
| 21 | [gateway-oidc](NCTF26/challenges/cloud/gateway-oidc/) | — | ⏳ |  |  |
| 22 | [gateway-prefix](NCTF26/challenges/cloud/gateway-prefix/) | — | ⏳ |  |  |
| 23 | [gcp-token-scope](NCTF26/challenges/cloud/gcp-token-scope/) | — | ⏳ |  |  |
| 24 | [identity-imds](NCTF26/challenges/cloud/identity-imds/) | — | ⏳ |  |  |
| 25 | [identity-oidc](NCTF26/challenges/cloud/identity-oidc/) | — | ⏳ |  |  |
| 26 | [identity-prefix](NCTF26/challenges/cloud/identity-prefix/) | — | ⏳ |  |  |
| 27 | [imds-ssrf](NCTF26/challenges/cloud/imds-ssrf/) | — | ⏳ |  |  |
| 28 | [leaky-prefix](NCTF26/challenges/cloud/leaky-prefix/) | — | ✅ | ✔ | ✔ |
| 29 | [metrics-imds](NCTF26/challenges/cloud/metrics-imds/) | — | ⏳ |  |  |
| 30 | [metrics-oidc](NCTF26/challenges/cloud/metrics-oidc/) | — | ⏳ |  |  |
| 31 | [metrics-prefix](NCTF26/challenges/cloud/metrics-prefix/) | — | ⏳ |  |  |
| 32 | [oidc-forge](NCTF26/challenges/cloud/oidc-forge/) | — | ⏳ |  |  |
| 33 | [passrole-ladder](NCTF26/challenges/cloud/passrole-ladder/) | — | ⏳ |  |  |
| 34 | [queue-imds](NCTF26/challenges/cloud/queue-imds/) | — | ⏳ |  |  |
| 35 | [queue-oidc](NCTF26/challenges/cloud/queue-oidc/) | — | ⏳ |  |  |
| 36 | [queue-poison](NCTF26/challenges/cloud/queue-poison/) | — | ⏳ |  |  |
| 37 | [queue-prefix](NCTF26/challenges/cloud/queue-prefix/) | — | ⏳ |  |  |
| 38 | [registry-imds](NCTF26/challenges/cloud/registry-imds/) | — | ⏳ |  |  |
| 39 | [registry-oidc](NCTF26/challenges/cloud/registry-oidc/) | — | ⏳ |  |  |
| 40 | [registry-prefix](NCTF26/challenges/cloud/registry-prefix/) | — | ⏳ |  |  |
| 41 | [sas-forge](NCTF26/challenges/cloud/sas-forge/) | — | ⏳ |  |  |
| 42 | [sub-wildcard](NCTF26/challenges/cloud/sub-wildcard/) | — | ✅ | ✔ | ✔ |
| 43 | [the-darknova--ebpf-verifier-mirage](NCTF26/challenges/cloud/the-darknova--ebpf-verifier-mirage/) | the-darknova | ⏳ |  |  |
| 44 | [the-darknova--oci-layer-timebomb](NCTF26/challenges/cloud/the-darknova--oci-layer-timebomb/) | the-darknova | ⏳ |  |  |
| 45 | [the-darknova--spiffe-mtls-ghost](NCTF26/challenges/cloud/the-darknova--spiffe-mtls-ghost/) | the-darknova | 📁 | ✔ |  |
| 46 | [trail-of-keys](NCTF26/challenges/cloud/trail-of-keys/) | — | ⏳ |  |  |

### cti

_4 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [the-darknova--lazarus-bridge-heist](NCTF26/challenges/cti/the-darknova--lazarus-bridge-heist/) | the-darknova | ⏳ |  |  |
| 2 | [the-darknova--sandworm-beacon](NCTF26/challenges/cti/the-darknova--sandworm-beacon/) | the-darknova | ⏳ |  |  |
| 3 | [the-darknova--silent-patch-cve](NCTF26/challenges/cti/the-darknova--silent-patch-cve/) | the-darknova | ⏳ |  |  |
| 4 | [the-darknova--vendor-supply-drop](NCTF26/challenges/cti/the-darknova--vendor-supply-drop/) | the-darknova | ⏳ |  |  |

### defense

_5 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [defense-audit-assigame](NCTF26/challenges/defense/defense-audit-assigame/) | — | ⏳ |  |  |
| 2 | [defense-binaire-guichet](NCTF26/challenges/defense/defense-binaire-guichet/) | — | ⏳ |  |  |
| 3 | [defense-linux-ceet](NCTF26/challenges/defense/defense-linux-ceet/) | — | ⏳ |  |  |
| 4 | [defense-wallet-akpe](NCTF26/challenges/defense/defense-wallet-akpe/) | — | ⏳ |  |  |
| 5 | [defense-web-agbadja](NCTF26/challenges/defense/defense-web-agbadja/) | — | ⏳ |  |  |

### crypto

_86 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [44r0nmeta--dzesido](NCTF26/challenges/crypto/44r0nmeta--dzesido/) | 44r0nmeta | ⏳ |  |  |
| 2 | [affine-relay](NCTF26/challenges/crypto/affine-relay/) | — | ⏳ |  |  |
| 3 | [algorithme123--kpepsi-clearing](NCTF26/challenges/crypto/algorithme123--kpepsi-clearing/) | algorithme123 | ⏳ |  |  |
| 4 | [algorithme123--togocel-legacy](NCTF26/challenges/crypto/algorithme123--togocel-legacy/) | algorithme123 | ⏳ |  |  |
| 5 | [boazak--afa](NCTF26/challenges/crypto/boazak--afa/) | boazak | ⏳ |  |  |
| 6 | [boazak--afagnan](NCTF26/challenges/crypto/boazak--afagnan/) | boazak | 📝 |  | ✔ |
| 7 | [boazak--agbale](NCTF26/challenges/crypto/boazak--agbale/) | boazak | 📁 | ✔ |  |
| 8 | [boazak--aklakou](NCTF26/challenges/crypto/boazak--aklakou/) | boazak | ⏳ |  |  |
| 9 | [boazak--atike](NCTF26/challenges/crypto/boazak--atike/) | boazak | 📁 | ✔ |  |
| 10 | [boazak--bassar](NCTF26/challenges/crypto/boazak--bassar/) | boazak | ⏳ |  |  |
| 11 | [boazak--djobokou](NCTF26/challenges/crypto/boazak--djobokou/) | boazak | ⏳ |  |  |
| 12 | [boazak--enye](NCTF26/challenges/crypto/boazak--enye/) | boazak | 📝 |  | ✔ |
| 13 | [boazak--fufu](NCTF26/challenges/crypto/boazak--fufu/) | boazak | ✅ |  | ✔ |
| 14 | [boazak--glidji](NCTF26/challenges/crypto/boazak--glidji/) | boazak | ⏳ |  |  |
| 15 | [boazak--kara](NCTF26/challenges/crypto/boazak--kara/) | boazak | ⏳ |  |  |
| 16 | [boazak--klo](NCTF26/challenges/crypto/boazak--klo/) | boazak | ⏳ |  |  |
| 17 | [boazak--koklo](NCTF26/challenges/crypto/boazak--koklo/) | boazak | ⏳ |  |  |
| 18 | [boazak--kpalime](NCTF26/challenges/crypto/boazak--kpalime/) | boazak | 📝 | ✔ | ✔ |
| 19 | [boazak--kpata](NCTF26/challenges/crypto/boazak--kpata/) | boazak | 📝 |  | ✔ |
| 20 | [boazak--mango](NCTF26/challenges/crypto/boazak--mango/) | boazak | ⏳ |  |  |
| 21 | [boazak--mawu](NCTF26/challenges/crypto/boazak--mawu/) | boazak | ⏳ |  |  |
| 22 | [boazak--niamtougou](NCTF26/challenges/crypto/boazak--niamtougou/) | boazak | ⏳ |  |  |
| 23 | [boazak--pagne](NCTF26/challenges/crypto/boazak--pagne/) | boazak | 📁 | ✔ |  |
| 24 | [boazak--sakpata](NCTF26/challenges/crypto/boazak--sakpata/) | boazak | ⏳ |  |  |
| 25 | [boazak--sodabi](NCTF26/challenges/crypto/boazak--sodabi/) | boazak | ✅ | ✔ | ✔ |
| 26 | [boazak--sokode-crypto](NCTF26/challenges/crypto/boazak--sokode-crypto/) | boazak | 📝 | ✔ | ✔ |
| 27 | [boazak--tchamba](NCTF26/challenges/crypto/boazak--tchamba/) | boazak | ⏳ |  |  |
| 28 | [boazak--tchoukoutou](NCTF26/challenges/crypto/boazak--tchoukoutou/) | boazak | ⏳ |  |  |
| 29 | [boazak--venovi](NCTF26/challenges/crypto/boazak--venovi/) | boazak | ✅ | ✔ | ✔ |
| 30 | [boazak--yeye](NCTF26/challenges/crypto/boazak--yeye/) | boazak | ✅ |  | ✔ |
| 31 | [boazak--zangbeto](NCTF26/challenges/crypto/boazak--zangbeto/) | boazak | ⏳ |  |  |
| 32 | [commit-bias](NCTF26/challenges/crypto/commit-bias/) | — | ⏳ |  |  |
| 33 | [ecb-echo](NCTF26/challenges/crypto/ecb-echo/) | — | ⏳ |  |  |
| 34 | [en2eavor--big-bang](NCTF26/challenges/crypto/en2eavor--big-bang/) | en2eavor | ⏳ |  |  |
| 35 | [fermat-twins](NCTF26/challenges/crypto/fermat-twins/) | — | ✅ | ✔ | ✔ |
| 36 | [gf2-cipher](NCTF26/challenges/crypto/gf2-cipher/) | — | ⏳ |  |  |
| 37 | [glue-and-extend](NCTF26/challenges/crypto/glue-and-extend/) | — | ⏳ |  |  |
| 38 | [kdf-slip](NCTF26/challenges/crypto/kdf-slip/) | — | ⏳ |  |  |
| 39 | [keystream-reuse](NCTF26/challenges/crypto/keystream-reuse/) | — | ⏳ |  |  |
| 40 | [komisergio--baguida](NCTF26/challenges/crypto/komisergio--baguida/) | komisergio | ⏳ |  |  |
| 41 | [komisergio--kamina](NCTF26/challenges/crypto/komisergio--kamina/) | komisergio | ✅ |  | ✔ |
| 42 | [komisergio--shallow](NCTF26/challenges/crypto/komisergio--shallow/) | komisergio | ✅ | ✔ | ✔ |
| 43 | [lcg-casino](NCTF26/challenges/crypto/lcg-casino/) | — | ⏳ |  |  |
| 44 | [modulus-siblings](NCTF26/challenges/crypto/modulus-siblings/) | — | ⏳ |  |  |
| 45 | [nonce-climb](NCTF26/challenges/crypto/nonce-climb/) | — | ⏳ |  |  |
| 46 | [nonce-sense](NCTF26/challenges/crypto/nonce-sense/) | — | ⏳ |  |  |
| 47 | [notarysvc-ecb](NCTF26/challenges/crypto/notarysvc-ecb/) | — | ⏳ |  |  |
| 48 | [notarysvc-kdf](NCTF26/challenges/crypto/notarysvc-kdf/) | — | ⏳ |  |  |
| 49 | [notarysvc-nonce](NCTF26/challenges/crypto/notarysvc-nonce/) | — | ⏳ |  |  |
| 50 | [notarysvc-padoracle](NCTF26/challenges/crypto/notarysvc-padoracle/) | — | ⏳ |  |  |
| 51 | [notarysvc-signext](NCTF26/challenges/crypto/notarysvc-signext/) | — | ⏳ |  |  |
| 52 | [oracle-cascade](NCTF26/challenges/crypto/oracle-cascade/) | — | ⏳ |  |  |
| 53 | [oxdefault--decode](NCTF26/challenges/crypto/oxdefault--decode/) | oxdefault | ✅ | ✔ | ✔ |
| 54 | [oxdefault--fast-enough](NCTF26/challenges/crypto/oxdefault--fast-enough/) | oxdefault | ⏳ |  |  |
| 55 | [oxdefault--hop](NCTF26/challenges/crypto/oxdefault--hop/) | oxdefault | ⏳ |  |  |
| 56 | [oxdefault--liar](NCTF26/challenges/crypto/oxdefault--liar/) | oxdefault | ⏳ |  |  |
| 57 | [oxdefault--minrank](NCTF26/challenges/crypto/oxdefault--minrank/) | oxdefault | ⏳ |  |  |
| 58 | [oxdefault--quadratic-i](NCTF26/challenges/crypto/oxdefault--quadratic-i/) | oxdefault | 📝 | ✔ | ✔ |
| 59 | [padding-oracle-lite](NCTF26/challenges/crypto/padding-oracle-lite/) | — | ⏳ |  |  |
| 60 | [pbkdf2-crack](NCTF26/challenges/crypto/pbkdf2-crack/) | — | ⏳ |  |  |
| 61 | [sealbox-ecb](NCTF26/challenges/crypto/sealbox-ecb/) | — | ⏳ |  |  |
| 62 | [sealbox-kdf](NCTF26/challenges/crypto/sealbox-kdf/) | — | ⏳ |  |  |
| 63 | [sealbox-nonce](NCTF26/challenges/crypto/sealbox-nonce/) | — | ⏳ |  |  |
| 64 | [sealbox-padoracle](NCTF26/challenges/crypto/sealbox-padoracle/) | — | ⏳ |  |  |
| 65 | [sealbox-signext](NCTF26/challenges/crypto/sealbox-signext/) | — | ⏳ |  |  |
| 66 | [sessiond-ecb](NCTF26/challenges/crypto/sessiond-ecb/) | — | ⏳ |  |  |
| 67 | [sessiond-kdf](NCTF26/challenges/crypto/sessiond-kdf/) | — | ⏳ |  |  |
| 68 | [sessiond-nonce](NCTF26/challenges/crypto/sessiond-nonce/) | — | ⏳ |  |  |
| 69 | [sessiond-padoracle](NCTF26/challenges/crypto/sessiond-padoracle/) | — | ⏳ |  |  |
| 70 | [sessiond-signext](NCTF26/challenges/crypto/sessiond-signext/) | — | ⏳ |  |  |
| 71 | [sign-slip](NCTF26/challenges/crypto/sign-slip/) | — | ⏳ |  |  |
| 72 | [signgate-ecb](NCTF26/challenges/crypto/signgate-ecb/) | — | ⏳ |  |  |
| 73 | [the-darknova--entangled-lcg](NCTF26/challenges/crypto/the-darknova--entangled-lcg/) | the-darknova | ⏳ |  |  |
| 74 | [the-darknova--frost-twisted-nonce](NCTF26/challenges/crypto/the-darknova--frost-twisted-nonce/) | the-darknova | ⏳ |  |  |
| 75 | [the-darknova--isogeny-endo-leak](NCTF26/challenges/crypto/the-darknova--isogeny-endo-leak/) | the-darknova | ⏳ |  |  |
| 76 | [the-darknova--kyber-fault-oracle](NCTF26/challenges/crypto/the-darknova--kyber-fault-oracle/) | the-darknova | ⏳ |  |  |
| 77 | [the-darknova--zk-transcript](NCTF26/challenges/crypto/the-darknova--zk-transcript/) | the-darknova | ⏳ |  |  |
| 78 | [thierry8petstar--pagouda](NCTF26/challenges/crypto/thierry8petstar--pagouda/) | thierry8petstar | ⏳ |  |  |
| 79 | [thierry8petstar--rsa-beginer](NCTF26/challenges/crypto/thierry8petstar--rsa-beginer/) | thierry8petstar | ⏳ |  |  |
| 80 | [thierry8petstar--state-of-the-stream](NCTF26/challenges/crypto/thierry8petstar--state-of-the-stream/) | thierry8petstar | ⏳ |  |  |
| 81 | [thierry8petstar--the-last-oracle](NCTF26/challenges/crypto/thierry8petstar--the-last-oracle/) | thierry8petstar | ⏳ |  |  |
| 82 | [thierry8petstar--warmup-xor](NCTF26/challenges/crypto/thierry8petstar--warmup-xor/) | thierry8petstar | ⏳ |  |  |
| 83 | [thierry8petstar--weird-rsa](NCTF26/challenges/crypto/thierry8petstar--weird-rsa/) | thierry8petstar | ⏳ |  |  |
| 84 | [tlv-vault](NCTF26/challenges/crypto/tlv-vault/) | — | ⏳ |  |  |
| 85 | [twister-tell](NCTF26/challenges/crypto/twister-tell/) | — | ⏳ |  |  |
| 86 | [vigenere-drift](NCTF26/challenges/crypto/vigenere-drift/) | — | ⏳ |  |  |

### forensics

_47 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [Audio FSK](NCTF26/challenges/forensics/Audio%20FSK/) | — | 📁 | ✔ |  |
| 2 | [DNS Exfil](NCTF26/challenges/forensics/DNS%20Exfil/) | — | ⏳ |  |  |
| 3 | [Evasion Timeline](NCTF26/challenges/forensics/Evasion%20Timeline/) | — | ⏳ |  |  |
| 4 | [SRAM Retention](NCTF26/challenges/forensics/SRAM%20Retention/) | — | 📁 | ✔ |  |
| 5 | [USB Keystrokes](NCTF26/challenges/forensics/USB%20Keystrokes/) | — | ⏳ |  |  |
| 6 | [algorithme123--coupure-sokode](NCTF26/challenges/forensics/algorithme123--coupure-sokode/) | algorithme123 | 📁 | ✔ |  |
| 7 | [algorithme123--kds-whitespace-commit](NCTF26/challenges/forensics/algorithme123--kds-whitespace-commit/) | algorithme123 | 📁 | ✔ |  |
| 8 | [algorithme123--lome-transit-0417](NCTF26/challenges/forensics/algorithme123--lome-transit-0417/) | algorithme123 | 📁 | ✔ |  |
| 9 | [algorithme123--zemidjan-classement](NCTF26/challenges/forensics/algorithme123--zemidjan-classement/) | algorithme123 | ⏳ |  |  |
| 10 | [auth-timeline](NCTF26/challenges/forensics/auth-timeline/) | — | ✅ | ✔ | ✔ |
| 11 | [boazak--bras-arme](NCTF26/challenges/forensics/boazak--bras-arme/) | boazak | ⏳ |  |  |
| 12 | [boazak--kouve-memory](NCTF26/challenges/forensics/boazak--kouve-memory/) | boazak | ⏳ |  |  |
| 13 | [boazak--kpessi](NCTF26/challenges/forensics/boazak--kpessi/) | boazak | ⏳ |  |  |
| 14 | [boazak--tandjoaure-pcap](NCTF26/challenges/forensics/boazak--tandjoaure-pcap/) | boazak | ⏳ |  |  |
| 15 | [chunk-hunt](NCTF26/challenges/forensics/chunk-hunt/) | — | ✅ | ✔ | ✔ |
| 16 | [fullaccess5--operation-acces-suspect](NCTF26/challenges/forensics/fullaccess5--operation-acces-suspect/) | fullaccess5 | ⏳ |  |  |
| 17 | [fullaccess5--operation-faux-colis](NCTF26/challenges/forensics/fullaccess5--operation-faux-colis/) | fullaccess5 | ⏳ |  |  |
| 18 | [fullaccess5--operation-flooz-piege](NCTF26/challenges/forensics/fullaccess5--operation-flooz-piege/) | fullaccess5 | 📁 | ✔ |  |
| 19 | [fullaccess5--operation-flux-obscur](NCTF26/challenges/forensics/fullaccess5--operation-flux-obscur/) | fullaccess5 | ⏳ |  |  |
| 20 | [fullaccess5--operation-ombre-numerique](NCTF26/challenges/forensics/fullaccess5--operation-ombre-numerique/) | fullaccess5 | ⏳ |  |  |
| 21 | [fullaccess5--operation-reunion-fantome](NCTF26/challenges/forensics/fullaccess5--operation-reunion-fantome/) | fullaccess5 | ⏳ |  |  |
| 22 | [fullaccess5--operation-swift-hook](NCTF26/challenges/forensics/fullaccess5--operation-swift-hook/) | fullaccess5 | ⏳ |  |  |
| 23 | [fullaccess5--operation-trace-noire](NCTF26/challenges/forensics/fullaccess5--operation-trace-noire/) | fullaccess5 | ⏳ |  |  |
| 24 | [fullaccess5--operation-virement-fantome](NCTF26/challenges/forensics/fullaccess5--operation-virement-fantome/) | fullaccess5 | ⏳ |  |  |
| 25 | [fullaccess5--securecorp-incident-reseau-invite](NCTF26/challenges/forensics/fullaccess5--securecorp-incident-reseau-invite/) | fullaccess5 | ✅ | ✔ | ✔ |
| 26 | [git-archaeology](NCTF26/challenges/forensics/git-archaeology/) | — | ⏳ |  |  |
| 27 | [gzip-tar-nest](NCTF26/challenges/forensics/gzip-tar-nest/) | — | ⏳ |  |  |
| 28 | [http-body-exfil](NCTF26/challenges/forensics/http-body-exfil/) | — | ⏳ |  |  |
| 29 | [icmp-beacon](NCTF26/challenges/forensics/icmp-beacon/) | — | ✅ | ✔ | ✔ |
| 30 | [json-sift](NCTF26/challenges/forensics/json-sift/) | — | ⏳ |  |  |
| 31 | [mem-struct](NCTF26/challenges/forensics/mem-struct/) | — | ⏳ |  |  |
| 32 | [oxdefault--cadence](NCTF26/challenges/forensics/oxdefault--cadence/) | oxdefault | ⏳ |  |  |
| 33 | [oxdefault--flush](NCTF26/challenges/forensics/oxdefault--flush/) | oxdefault | ⏳ |  |  |
| 34 | [oxdefault--le-chant-du-mono](NCTF26/challenges/forensics/oxdefault--le-chant-du-mono/) | oxdefault | ⏳ |  |  |
| 35 | [oxdefault--pressure](NCTF26/challenges/forensics/oxdefault--pressure/) | oxdefault | ⏳ |  |  |
| 36 | [png-magic-fix](NCTF26/challenges/forensics/png-magic-fix/) | — | ✅ | ✔ | ✔ |
| 37 | [spreadsheet-audit](NCTF26/challenges/forensics/spreadsheet-audit/) | — | ⏳ |  |  |
| 38 | [sqlite-wal](NCTF26/challenges/forensics/sqlite-wal/) | — | 📁 | ✔ |  |
| 39 | [the-darknova--chronos-hid](NCTF26/challenges/forensics/the-darknova--chronos-hid/) | the-darknova | ⏳ |  |  |
| 40 | [the-darknova--mirage-1](NCTF26/challenges/forensics/the-darknova--mirage-1/) | the-darknova | ✅ | ✔ | ✔ |
| 41 | [the-darknova--mirage-2](NCTF26/challenges/forensics/the-darknova--mirage-2/) | the-darknova | ⏳ |  |  |
| 42 | [the-darknova--mirage-3](NCTF26/challenges/forensics/the-darknova--mirage-3/) | the-darknova | ⏳ |  |  |
| 43 | [the-darknova--mirage-4](NCTF26/challenges/forensics/the-darknova--mirage-4/) | the-darknova | ⏳ |  |  |
| 44 | [the-darknova--nvme-ftl-wearlevel](NCTF26/challenges/forensics/the-darknova--nvme-ftl-wearlevel/) | the-darknova | ⏳ |  |  |
| 45 | [the-darknova--ot-telemetry](NCTF26/challenges/forensics/the-darknova--ot-telemetry/) | the-darknova | ⏳ |  |  |
| 46 | [thierry8petstar--exfiltrator](NCTF26/challenges/forensics/thierry8petstar--exfiltrator/) | thierry8petstar | ⏳ |  |  |
| 47 | [zip-carve](NCTF26/challenges/forensics/zip-carve/) | — | ⏳ |  |  |

### hardware

_8 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [boot-rom](NCTF26/challenges/hardware/boot-rom/) | — | ⏳ |  |  |
| 2 | [firmware-blob](NCTF26/challenges/hardware/firmware-blob/) | — | ⏳ |  |  |
| 3 | [i2c-sniff](NCTF26/challenges/hardware/i2c-sniff/) | — | ⏳ |  |  |
| 4 | [intel-hex](NCTF26/challenges/hardware/intel-hex/) | — | ⏳ |  |  |
| 5 | [manchester-ook](NCTF26/challenges/hardware/manchester-ook/) | — | ⏳ |  |  |
| 6 | [spi-eeprom](NCTF26/challenges/hardware/spi-eeprom/) | — | ⏳ |  |  |
| 7 | [uart-capture](NCTF26/challenges/hardware/uart-capture/) | — | ✅ | ✔ | ✔ |
| 8 | [vcd-fsm](NCTF26/challenges/hardware/vcd-fsm/) | — | ⏳ |  |  |

### ics

_1 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [komisergio--adjengre](NCTF26/challenges/ics/komisergio--adjengre/) | komisergio | ⏳ |  |  |

### iot

_3 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [the-darknova--canfd-ecu-glitch](NCTF26/challenges/iot/the-darknova--canfd-ecu-glitch/) | the-darknova | ⏳ |  |  |
| 2 | [the-darknova--matter-thread-ghost](NCTF26/challenges/iot/the-darknova--matter-thread-ghost/) | the-darknova | ⏳ |  |  |
| 3 | [the-darknova--riscv-bmc-shadow](NCTF26/challenges/iot/the-darknova--riscv-bmc-shadow/) | the-darknova | ⏳ |  |  |

### misc

_18 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [44r0nmeta--neverlost](NCTF26/challenges/misc/44r0nmeta--neverlost/) | 44r0nmeta | ⏳ |  |  |
| 2 | [Heartbeat](NCTF26/challenges/misc/Heartbeat/) | — | ⏳ |  |  |
| 3 | [boazak--djagble](NCTF26/challenges/misc/boazak--djagble/) | boazak | ⏳ |  |  |
| 4 | [boazak--petit-fally](NCTF26/challenges/misc/boazak--petit-fally/) | boazak | ⏳ |  |  |
| 5 | [en2eavor--princess-habits](NCTF26/challenges/misc/en2eavor--princess-habits/) | en2eavor | ⏳ |  |  |
| 6 | [esolang-jail](NCTF26/challenges/misc/esolang-jail/) | — | ⏳ |  |  |
| 7 | [oxdefault--les-murmures-de-l-omni](NCTF26/challenges/misc/oxdefault--les-murmures-de-l-omni/) | oxdefault | ⏳ |  |  |
| 8 | [oxdefault--overheard](NCTF26/challenges/misc/oxdefault--overheard/) | oxdefault | ⏳ |  |  |
| 9 | [oxdefault--perfect](NCTF26/challenges/misc/oxdefault--perfect/) | oxdefault | ⏳ |  |  |
| 10 | [the-darknova--bgp-rpki-blackhole](NCTF26/challenges/misc/the-darknova--bgp-rpki-blackhole/) | the-darknova | ⏳ |  |  |
| 11 | [the-darknova--git-ofs-ouroboros](NCTF26/challenges/misc/the-darknova--git-ofs-ouroboros/) | the-darknova | ⏳ |  |  |
| 12 | [the-darknova--ieee754-kahan-oracle](NCTF26/challenges/misc/the-darknova--ieee754-kahan-oracle/) | the-darknova | ⏳ |  |  |
| 13 | [the-darknova--orbital-iq-doppler](NCTF26/challenges/misc/the-darknova--orbital-iq-doppler/) | the-darknova | ⏳ |  |  |
| 14 | [the-darknova--qasm-clifford-ghost](NCTF26/challenges/misc/the-darknova--qasm-clifford-ghost/) | the-darknova | ⏳ |  |  |
| 15 | [the-darknova--safetensors-lobotomy](NCTF26/challenges/misc/the-darknova--safetensors-lobotomy/) | the-darknova | ⏳ |  |  |
| 16 | [thierry8petstar--doublepeel](NCTF26/challenges/misc/thierry8petstar--doublepeel/) | thierry8petstar | ⏳ |  |  |
| 17 | [thierry8petstar--oui-ou-non-1](NCTF26/challenges/misc/thierry8petstar--oui-ou-non-1/) | thierry8petstar | ⏳ |  |  |
| 18 | [thierry8petstar--oui-ou-non-2](NCTF26/challenges/misc/thierry8petstar--oui-ou-non-2/) | thierry8petstar | ⏳ |  |  |

### ml

_11 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [adv-flip](NCTF26/challenges/ml/adv-flip/) | — | ⏳ |  |  |
| 2 | [adversarial-gate](NCTF26/challenges/ml/adversarial-gate/) | — | ⏳ |  |  |
| 3 | [embedding-nn](NCTF26/challenges/ml/embedding-nn/) | — | ✅ | ✔ | ✔ |
| 4 | [grad-leak](NCTF26/challenges/ml/grad-leak/) | — | ⏳ |  |  |
| 5 | [member-ids](NCTF26/challenges/ml/member-ids/) | — | ⏳ |  |  |
| 6 | [model-inversion](NCTF26/challenges/ml/model-inversion/) | — | ⏳ |  |  |
| 7 | [pickle-rce](NCTF26/challenges/ml/pickle-rce/) | — | ✅ | ✔ | ✔ |
| 8 | [poison-shift](NCTF26/challenges/ml/poison-shift/) | — | ⏳ |  |  |
| 9 | [surrogate-fit](NCTF26/challenges/ml/surrogate-fit/) | — | ⏳ |  |  |
| 10 | [tree-path](NCTF26/challenges/ml/tree-path/) | — | ⏳ |  |  |
| 11 | [trojan-trigger](NCTF26/challenges/ml/trojan-trigger/) | — | ⏳ |  |  |

### mobile

_13 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [boazak--akodesewa-shield](NCTF26/challenges/mobile/boazak--akodesewa-shield/) | boazak | ⏳ |  |  |
| 2 | [boazak--devo-mobile](NCTF26/challenges/mobile/boazak--devo-mobile/) | boazak | ⏳ |  |  |
| 3 | [boazak--gboto-app](NCTF26/challenges/mobile/boazak--gboto-app/) | boazak | ⏳ |  |  |
| 4 | [boazak--kloto-reseau](NCTF26/challenges/mobile/boazak--kloto-reseau/) | boazak | ⏳ |  |  |
| 5 | [boazak--zio-securite](NCTF26/challenges/mobile/boazak--zio-securite/) | boazak | ⏳ |  |  |
| 6 | [deeplink-guard](NCTF26/challenges/mobile/deeplink-guard/) | — | ⏳ |  |  |
| 7 | [keystore-alias](NCTF26/challenges/mobile/keystore-alias/) | — | ⏳ |  |  |
| 8 | [native-xor](NCTF26/challenges/mobile/native-xor/) | — | ✅ | ✔ | ✔ |
| 9 | [obfuscated-strings](NCTF26/challenges/mobile/obfuscated-strings/) | — | 📁 | ✔ |  |
| 10 | [prefs-vault](NCTF26/challenges/mobile/prefs-vault/) | — | ⏳ |  |  |
| 11 | [root-gate](NCTF26/challenges/mobile/root-gate/) | — | ⏳ |  |  |
| 12 | [strings-goldmine](NCTF26/challenges/mobile/strings-goldmine/) | — | ⏳ |  |  |
| 13 | [webview-bridge](NCTF26/challenges/mobile/webview-bridge/) | — | ⏳ |  |  |

### networking

_11 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [acl-firewall](NCTF26/challenges/networking/acl-firewall/) | — | ✅ | ✔ | ✔ |
| 2 | [bgp-bestpath](NCTF26/challenges/networking/bgp-bestpath/) | — | ⏳ |  |  |
| 3 | [dns-chain](NCTF26/challenges/networking/dns-chain/) | — | ⏳ |  |  |
| 4 | [eui64-slaac](NCTF26/challenges/networking/eui64-slaac/) | — | ⏳ |  |  |
| 5 | [framed-protocol](NCTF26/challenges/networking/framed-protocol/) | — | ⏳ |  |  |
| 6 | [komisergio--elavagnon](NCTF26/challenges/networking/komisergio--elavagnon/) | komisergio | ⏳ |  |  |
| 7 | [netflow-talker](NCTF26/challenges/networking/netflow-talker/) | — | ⏳ |  |  |
| 8 | [subnet-reach](NCTF26/challenges/networking/subnet-reach/) | — | ⏳ |  |  |
| 9 | [tcp-reassembly](NCTF26/challenges/networking/tcp-reassembly/) | — | ⏳ |  |  |
| 10 | [tls-sni](NCTF26/challenges/networking/tls-sni/) | — | ⏳ |  |  |
| 11 | [wire-tap](NCTF26/challenges/networking/wire-tap/) | — | ⏳ |  |  |

### osint

_13 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [algorithme123--memoire-togo-fiche](NCTF26/challenges/osint/algorithme123--memoire-togo-fiche/) | algorithme123 | ⏳ |  |  |
| 2 | [cred-reuse](NCTF26/challenges/osint/cred-reuse/) | — | ✅ | ✔ | ✔ |
| 3 | [ct-log-pivot](NCTF26/challenges/osint/ct-log-pivot/) | — | ⏳ |  |  |
| 4 | [device-backup-geo](NCTF26/challenges/osint/device-backup-geo/) | — | ⏳ |  |  |
| 5 | [doc-metadata](NCTF26/challenges/osint/doc-metadata/) | — | ✅ | ✔ | ✔ |
| 6 | [en2eavor--glingo](NCTF26/challenges/osint/en2eavor--glingo/) | en2eavor | ⏳ |  |  |
| 7 | [entity-graph](NCTF26/challenges/osint/entity-graph/) | — | ⏳ |  |  |
| 8 | [exif-triangulation](NCTF26/challenges/osint/exif-triangulation/) | — | ⏳ |  |  |
| 9 | [fullaccess5--alerte-uvci](NCTF26/challenges/osint/fullaccess5--alerte-uvci/) | fullaccess5 | ⏳ |  |  |
| 10 | [r06u3-004--histoire-vivi](NCTF26/challenges/osint/r06u3-004--histoire-vivi/) | r06u3-004 | ⏳ |  |  |
| 11 | [r06u3-004--osint-vivi-sre](NCTF26/challenges/osint/r06u3-004--osint-vivi-sre/) | r06u3-004 | ⏳ |  |  |
| 12 | [social-export](NCTF26/challenges/osint/social-export/) | — | ⏳ |  |  |
| 13 | [wayback-diff](NCTF26/challenges/osint/wayback-diff/) | — | ⏳ |  |  |

### ppc

_10 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [congruence-vault](NCTF26/challenges/ppc/congruence-vault/) | — | ⏳ |  |  |
| 2 | [dfa-oracle](NCTF26/challenges/ppc/dfa-oracle/) | — | ⏳ |  |  |
| 3 | [dijkstra-relay](NCTF26/challenges/ppc/dijkstra-relay/) | — | ⏳ |  |  |
| 4 | [hull-cipher](NCTF26/challenges/ppc/hull-cipher/) | — | ✅ | ✔ | ✔ |
| 5 | [knapsack-locker](NCTF26/challenges/ppc/knapsack-locker/) | — | ⏳ |  |  |
| 6 | [life-decode](NCTF26/challenges/ppc/life-decode/) | — | ⏳ |  |  |
| 7 | [semiprime-sweep](NCTF26/challenges/ppc/semiprime-sweep/) | — | ⏳ |  |  |
| 8 | [stack-machine](NCTF26/challenges/ppc/stack-machine/) | — | ⏳ |  |  |
| 9 | [sudoku-vault](NCTF26/challenges/ppc/sudoku-vault/) | — | ⏳ |  |  |
| 10 | [z-locator](NCTF26/challenges/ppc/z-locator/) | — | ✅ | ✔ | ✔ |

### pwn

_22 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [44r0nmeta--dzitri](NCTF26/challenges/pwn/44r0nmeta--dzitri/) | 44r0nmeta | ⏳ |  |  |
| 2 | [algorithme123--aneho-manifestd](NCTF26/challenges/pwn/algorithme123--aneho-manifestd/) | algorithme123 | ⏳ |  |  |
| 3 | [boazak--kande-heap](NCTF26/challenges/pwn/boazak--kande-heap/) | boazak | ⏳ |  |  |
| 4 | [boazak--niamtougou-fmt](NCTF26/challenges/pwn/boazak--niamtougou-fmt/) | boazak | ⏳ |  |  |
| 5 | [bridged-protoparse](NCTF26/challenges/pwn/bridged-protoparse/) | — | ⏳ |  |  |
| 6 | [bss-admin-flip](NCTF26/challenges/pwn/bss-admin-flip/) | — | ✅ | ✔ | ✔ |
| 7 | [en2eavor--pew-pew](NCTF26/challenges/pwn/en2eavor--pew-pew/) | en2eavor | ⏳ |  |  |
| 8 | [fmt-key-leak](NCTF26/challenges/pwn/fmt-key-leak/) | — | ⏳ |  |  |
| 9 | [format-string-101](NCTF26/challenges/pwn/format-string-101/) | — | 📁 | ✔ |  |
| 10 | [heap-note](NCTF26/challenges/pwn/heap-note/) | — | ⏳ |  |  |
| 11 | [komisergio--koutammakou](NCTF26/challenges/pwn/komisergio--koutammakou/) | komisergio | ⏳ |  |  |
| 12 | [off-by-one-auth](NCTF26/challenges/pwn/off-by-one-auth/) | — | ⏳ |  |  |
| 13 | [proto-fuzz](NCTF26/challenges/pwn/proto-fuzz/) | — | ⏳ |  |  |
| 14 | [r06u3-004--leta](NCTF26/challenges/pwn/r06u3-004--leta/) | r06u3-004 | ⏳ |  |  |
| 15 | [ret2csu-ish](NCTF26/challenges/pwn/ret2csu-ish/) | — | 📁 | ✔ |  |
| 16 | [ret2win-keyed](NCTF26/challenges/pwn/ret2win-keyed/) | — | ⏳ |  |  |
| 17 | [shellcode-decoder](NCTF26/challenges/pwn/shellcode-decoder/) | — | ⏳ |  |  |
| 18 | [stack-smash-reveal](NCTF26/challenges/pwn/stack-smash-reveal/) | — | ⏳ |  |  |
| 19 | [the-darknova--ring-ipc](NCTF26/challenges/pwn/the-darknova--ring-ipc/) | the-darknova | ⏳ |  |  |
| 20 | [the-darknova--seccomp-shadow-ipc](NCTF26/challenges/pwn/the-darknova--seccomp-shadow-ipc/) | the-darknova | 📝 | ✔ | ✔ |
| 21 | [the-darknova--uring-slab-alchemy](NCTF26/challenges/pwn/the-darknova--uring-slab-alchemy/) | the-darknova | ⏳ |  |  |
| 22 | [the-darknova--wasm-linear-escape](NCTF26/challenges/pwn/the-darknova--wasm-linear-escape/) | the-darknova | ⏳ |  |  |

### reverse

_29 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [44r0nmeta--wotowoto](NCTF26/challenges/reverse/44r0nmeta--wotowoto/) | 44r0nmeta | ⏳ |  |  |
| 2 | [algorithme123--kara-express-billet](NCTF26/challenges/reverse/algorithme123--kara-express-billet/) | algorithme123 | ⏳ |  |  |
| 3 | [boazak--agbelouve](NCTF26/challenges/reverse/boazak--agbelouve/) | boazak | 📝 | ✔ | ✔ |
| 4 | [boazak--blitta-packer](NCTF26/challenges/reverse/boazak--blitta-packer/) | boazak | 📁 | ✔ |  |
| 5 | [boazak--dankpen-wasm](NCTF26/challenges/reverse/boazak--dankpen-wasm/) | boazak | ⏳ |  |  |
| 6 | [boazak--kantoure-vm](NCTF26/challenges/reverse/boazak--kantoure-vm/) | boazak | ⏳ |  |  |
| 7 | [brainfuck-cascade](NCTF26/challenges/reverse/brainfuck-cascade/) | — | ⏳ |  |  |
| 8 | [byte-drift](NCTF26/challenges/reverse/byte-drift/) | — | ✅ | ✔ | ✔ |
| 9 | [crc-forge](NCTF26/challenges/reverse/crc-forge/) | — | ⏳ |  |  |
| 10 | [java-cafe](NCTF26/challenges/reverse/java-cafe/) | — | ⏳ |  |  |
| 11 | [keygen-me](NCTF26/challenges/reverse/keygen-me/) | — | 📁 | ✔ |  |
| 12 | [komisergio--adeta](NCTF26/challenges/reverse/komisergio--adeta/) | komisergio | 📝 | ✔ | ✔ |
| 13 | [maze-vm](NCTF26/challenges/reverse/maze-vm/) | — | ⏳ |  |  |
| 14 | [oxdefault--hogbe-la-machine-de-l-exode](NCTF26/challenges/reverse/oxdefault--hogbe-la-machine-de-l-exode/) | oxdefault | 📁 | ✔ |  |
| 15 | [packed-vm-lite](NCTF26/challenges/reverse/packed-vm-lite/) | — | ⏳ |  |  |
| 16 | [pyc-ghost](NCTF26/challenges/reverse/pyc-ghost/) | — | ⏳ |  |  |
| 17 | [r06u3-004--securevault-license](NCTF26/challenges/reverse/r06u3-004--securevault-license/) | r06u3-004 | ⏳ |  |  |
| 18 | [shell-lock](NCTF26/challenges/reverse/shell-lock/) | — | ✅ | ✔ | ✔ |
| 19 | [stack-vm](NCTF26/challenges/reverse/stack-vm/) | — | ⏳ |  |  |
| 20 | [strings-lie](NCTF26/challenges/reverse/strings-lie/) | — | ✅ | ✔ | ✔ |
| 21 | [synthvm](NCTF26/challenges/reverse/synthvm/) | — | ⏳ |  |  |
| 22 | [the-darknova--chronos-async-vm](NCTF26/challenges/reverse/the-darknova--chronos-async-vm/) | the-darknova | ⏳ |  |  |
| 23 | [the-darknova--dwarf-exception-cfg](NCTF26/challenges/reverse/the-darknova--dwarf-exception-cfg/) | the-darknova | ⏳ |  |  |
| 24 | [the-darknova--nanomite-maze](NCTF26/challenges/reverse/the-darknova--nanomite-maze/) | the-darknova | ⏳ |  |  |
| 25 | [the-darknova--ouroboros-vm](NCTF26/challenges/reverse/the-darknova--ouroboros-vm/) | the-darknova | ⏳ |  |  |
| 26 | [the-darknova--simd-galois-labyrinth](NCTF26/challenges/reverse/the-darknova--simd-galois-labyrinth/) | the-darknova | ⏳ |  |  |
| 27 | [thierry8petstar--bytecode-yeye](NCTF26/challenges/reverse/thierry8petstar--bytecode-yeye/) | thierry8petstar | ⏳ |  |  |
| 28 | [thierry8petstar--stateful-vm](NCTF26/challenges/reverse/thierry8petstar--stateful-vm/) | thierry8petstar | ⏳ |  |  |
| 29 | [triple-wrap](NCTF26/challenges/reverse/triple-wrap/) | — | ⏳ |  |  |

### stego

_15 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [algorithme123--atakpame-zero-width](NCTF26/challenges/stego/algorithme123--atakpame-zero-width/) | algorithme123 | ⏳ |  |  |
| 2 | [algorithme123--greffe-espaces-lome](NCTF26/challenges/stego/algorithme123--greffe-espaces-lome/) | algorithme123 | ✅ | ✔ | ✔ |
| 3 | [algorithme123--rn1-last-photo](NCTF26/challenges/stego/algorithme123--rn1-last-photo/) | algorithme123 | ⏳ |  |  |
| 4 | [algorithme123--tisserands-dapaong](NCTF26/challenges/stego/algorithme123--tisserands-dapaong/) | algorithme123 | ✅ | ✔ | ✔ |
| 5 | [boazak--kabou](NCTF26/challenges/stego/boazak--kabou/) | boazak | ✅ | ✔ | ✔ |
| 6 | [dtmf-dial](NCTF26/challenges/stego/dtmf-dial/) | — | ⏳ |  |  |
| 7 | [en2eavor--sayen-game](NCTF26/challenges/stego/en2eavor--sayen-game/) | en2eavor | ⏳ |  |  |
| 8 | [layered-png](NCTF26/challenges/stego/layered-png/) | — | ⏳ |  |  |
| 9 | [lsb-bmp](NCTF26/challenges/stego/lsb-bmp/) | — | ✅ | ✔ | ✔ |
| 10 | [png-text-chunk](NCTF26/challenges/stego/png-text-chunk/) | — | ⏳ |  |  |
| 11 | [polyglot-onion](NCTF26/challenges/stego/polyglot-onion/) | — | ⏳ |  |  |
| 12 | [trailing-zip](NCTF26/challenges/stego/trailing-zip/) | — | ⏳ |  |  |
| 13 | [twin-palette](NCTF26/challenges/stego/twin-palette/) | — | ⏳ |  |  |
| 14 | [wav-lsb](NCTF26/challenges/stego/wav-lsb/) | — | ⏳ |  |  |
| 15 | [zero-width-note](NCTF26/challenges/stego/zero-width-note/) | — | ⏳ |  |  |

### supplychain

_14 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [build-cache-poison](NCTF26/challenges/supplychain/build-cache-poison/) | — | ⏳ |  |  |
| 2 | [buildfarm-artswap](NCTF26/challenges/supplychain/buildfarm-artswap/) | — | 📝 | ✔ | ✔ |
| 3 | [buildfarm-depconf](NCTF26/challenges/supplychain/buildfarm-depconf/) | — | ⏳ |  |  |
| 4 | [buildfarm-postinstall](NCTF26/challenges/supplychain/buildfarm-postinstall/) | — | ⏳ |  |  |
| 5 | [dependency-confusion](NCTF26/challenges/supplychain/dependency-confusion/) | — | ⏳ |  |  |
| 6 | [git-repo-backdoor](NCTF26/challenges/supplychain/git-repo-backdoor/) | — | ✅ | ✔ | ✔ |
| 7 | [layered-image-leak](NCTF26/challenges/supplychain/layered-image-leak/) | — | ✅ | ✔ | ✔ |
| 8 | [lockfile-integrity-drift](NCTF26/challenges/supplychain/lockfile-integrity-drift/) | — | 📝 | ✔ | ✔ |
| 9 | [pip-postinstall-hook](NCTF26/challenges/supplychain/pip-postinstall-hook/) | — | ✅ | ✔ | ✔ |
| 10 | [poisoned-pipeline](NCTF26/challenges/supplychain/poisoned-pipeline/) | — | ⏳ |  |  |
| 11 | [provenance-forgery](NCTF26/challenges/supplychain/provenance-forgery/) | — | ✅ | ✔ | ✔ |
| 12 | [sbom-component-swap](NCTF26/challenges/supplychain/sbom-component-swap/) | — | ✅ | ✔ | ✔ |
| 13 | [tuf-rollback](NCTF26/challenges/supplychain/tuf-rollback/) | — | ⏳ |  |  |
| 14 | [typosquat-lockfile](NCTF26/challenges/supplychain/typosquat-lockfile/) | — | ✅ | ✔ | ✔ |

### sysadmin

_12 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [alias-slip](NCTF26/challenges/sysadmin/alias-slip/) | — | ✅ | ✔ | ✔ |
| 2 | [auditd-cap](NCTF26/challenges/sysadmin/auditd-cap/) | — | ⏳ |  |  |
| 3 | [auditd-cron](NCTF26/challenges/sysadmin/auditd-cron/) | — | ⏳ |  |  |
| 4 | [bridged-envreuse](NCTF26/challenges/sysadmin/bridged-envreuse/) | — | ⏳ |  |  |
| 5 | [env-forge](NCTF26/challenges/sysadmin/env-forge/) | — | ⏳ |  |  |
| 6 | [mask-slip](NCTF26/challenges/sysadmin/mask-slip/) | — | ⏳ |  |  |
| 7 | [rbac-reveal](NCTF26/challenges/sysadmin/rbac-reveal/) | — | ⏳ |  |  |
| 8 | [rotate-root](NCTF26/challenges/sysadmin/rotate-root/) | — | ⏳ |  |  |
| 9 | [secret-slip](NCTF26/challenges/sysadmin/secret-slip/) | — | ⏳ |  |  |
| 10 | [state-secret](NCTF26/challenges/sysadmin/state-secret/) | — | ⏳ |  |  |
| 11 | [unit-eval](NCTF26/challenges/sysadmin/unit-eval/) | — | ⏳ |  |  |
| 12 | [vault-reuse](NCTF26/challenges/sysadmin/vault-reuse/) | — | ⏳ |  |  |

### warmup

_16 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [atbash-cipher](NCTF26/challenges/warmup/atbash-cipher/) | — | ⏳ |  |  |
| 2 | [base32-decode](NCTF26/challenges/warmup/base32-decode/) | — | ⏳ |  |  |
| 3 | [base64-decode](NCTF26/challenges/warmup/base64-decode/) | — | ⏳ |  |  |
| 4 | [base85-decode](NCTF26/challenges/warmup/base85-decode/) | — | ⏳ |  |  |
| 5 | [binary-ascii](NCTF26/challenges/warmup/binary-ascii/) | — | ✅ | ✔ | ✔ |
| 6 | [csv-cell](NCTF26/challenges/warmup/csv-cell/) | — | ⏳ |  |  |
| 7 | [hex-decode](NCTF26/challenges/warmup/hex-decode/) | — | ⏳ |  |  |
| 8 | [html-entities](NCTF26/challenges/warmup/html-entities/) | — | ⏳ |  |  |
| 9 | [morse-code](NCTF26/challenges/warmup/morse-code/) | — | ⏳ |  |  |
| 10 | [reverse-string](NCTF26/challenges/warmup/reverse-string/) | — | ⏳ |  |  |
| 11 | [rot13-decode](NCTF26/challenges/warmup/rot13-decode/) | — | ⏳ |  |  |
| 12 | [rot47-decode](NCTF26/challenges/warmup/rot47-decode/) | — | ✅ | ✔ | ✔ |
| 13 | [tap-code](NCTF26/challenges/warmup/tap-code/) | — | 📝 | ✔ | ✔ |
| 14 | [url-encoding](NCTF26/challenges/warmup/url-encoding/) | — | ⏳ |  |  |
| 15 | [vigenere-known-key](NCTF26/challenges/warmup/vigenere-known-key/) | — | ⏳ |  |  |
| 16 | [zip-comment](NCTF26/challenges/warmup/zip-comment/) | — | ✅ | ✔ | ✔ |

### web

_76 épreuves_

| # | Épreuve | Auteur | Statut | 📁 | 🛠️ |
|---|---|---|---|---|---|
| 1 | [44r0nmeta--flex](NCTF26/challenges/web/44r0nmeta--flex/) | 44r0nmeta | ⏳ |  |  |
| 2 | [44r0nmeta--kiyena](NCTF26/challenges/web/44r0nmeta--kiyena/) | 44r0nmeta | ⏳ |  |  |
| 3 | [algorithme123--marche-lome-carnet](NCTF26/challenges/web/algorithme123--marche-lome-carnet/) | algorithme123 | ⏳ |  |  |
| 4 | [algorithme123--radio-kloto](NCTF26/challenges/web/algorithme123--radio-kloto/) | algorithme123 | ⏳ |  |  |
| 5 | [bitvault-fees](NCTF26/challenges/web/bitvault-fees/) | — | ⏳ |  |  |
| 6 | [bitvault-refund](NCTF26/challenges/web/bitvault-refund/) | — | ⏳ |  |  |
| 7 | [bitvault-tiers](NCTF26/challenges/web/bitvault-tiers/) | — | ⏳ |  |  |
| 8 | [boazak--adeta](NCTF26/challenges/web/boazak--adeta/) | boazak | ⏳ |  |  |
| 9 | [boazak--agbodrafo](NCTF26/challenges/web/boazak--agbodrafo/) | boazak | ⏳ |  |  |
| 10 | [boazak--agoe](NCTF26/challenges/web/boazak--agoe/) | boazak | ⏳ |  |  |
| 11 | [boazak--agokoli](NCTF26/challenges/web/boazak--agokoli/) | boazak | ⏳ |  |  |
| 12 | [boazak--akloa-rendus](NCTF26/challenges/web/boazak--akloa-rendus/) | boazak | ⏳ |  |  |
| 13 | [boazak--akodessewa](NCTF26/challenges/web/boazak--akodessewa/) | boazak | ⏳ |  |  |
| 14 | [boazak--aledjo](NCTF26/challenges/web/boazak--aledjo/) | boazak | ⏳ |  |  |
| 15 | [boazak--ando-rapports](NCTF26/challenges/web/boazak--ando-rapports/) | boazak | ⏳ |  |  |
| 16 | [boazak--aneho](NCTF26/challenges/web/boazak--aneho/) | boazak | ⏳ |  |  |
| 17 | [boazak--anie](NCTF26/challenges/web/boazak--anie/) | boazak | ⏳ |  |  |
| 18 | [boazak--assahoun-registre](NCTF26/challenges/web/boazak--assahoun-registre/) | boazak | ⏳ |  |  |
| 19 | [boazak--atakpame](NCTF26/challenges/web/boazak--atakpame/) | boazak | ⏳ |  |  |
| 20 | [boazak--be](NCTF26/challenges/web/boazak--be/) | boazak | ⏳ |  |  |
| 21 | [boazak--dapaong](NCTF26/challenges/web/boazak--dapaong/) | boazak | ⏳ |  |  |
| 22 | [boazak--dapaong-sso](NCTF26/challenges/web/boazak--dapaong-sso/) | boazak | ⏳ |  |  |
| 23 | [boazak--kande](NCTF26/challenges/web/boazak--kande/) | boazak | ✅ |  | ✔ |
| 24 | [boazak--klouto](NCTF26/challenges/web/boazak--klouto/) | boazak (KodjoDoDjango) | ✅ |  | ✔ |
| 25 | [boazak--koutammakou](NCTF26/challenges/web/boazak--koutammakou/) | boazak | 📝 |  | ✔ |
| 26 | [boazak--lome](NCTF26/challenges/web/boazak--lome/) | boazak | ⏳ |  |  |
| 27 | [boazak--mono](NCTF26/challenges/web/boazak--mono/) | boazak | ⏳ |  |  |
| 28 | [boazak--nangbeto](NCTF26/challenges/web/boazak--nangbeto/) | boazak | ⏳ |  |  |
| 29 | [boazak--notse](NCTF26/challenges/web/boazak--notse/) | boazak | ⏳ |  |  |
| 30 | [boazak--notse-graphql](NCTF26/challenges/web/boazak--notse-graphql/) | boazak | ⏳ |  |  |
| 31 | [boazak--sokode](NCTF26/challenges/web/boazak--sokode/) | boazak | ⏳ |  |  |
| 32 | [boazak--togbi](NCTF26/challenges/web/boazak--togbi/) | boazak | ⏳ |  |  |
| 33 | [boazak--togoville](NCTF26/challenges/web/boazak--togoville/) | boazak | ⏳ |  |  |
| 34 | [boazak--tsevie](NCTF26/challenges/web/boazak--tsevie/) | boazak | ⏳ |  |  |
| 35 | [boazak--vogan](NCTF26/challenges/web/boazak--vogan/) | boazak | 📝 |  | ✔ |
| 36 | [boazak--vogan-cms](NCTF26/challenges/web/boazak--vogan-cms/) | boazak | ⏳ |  |  |
| 37 | [bridged-deser](NCTF26/challenges/web/bridged-deser/) | hibris, Clawd | ✅ |  | ✔ |
| 38 | [cms-jwtconf](NCTF26/challenges/web/cms-jwtconf/) | — | ⏳ |  |  |
| 39 | [cms-smuggle](NCTF26/challenges/web/cms-smuggle/) | — | 📝 |  | ✔ |
| 40 | [flask-unsign](NCTF26/challenges/web/flask-unsign/) | hibris, Clawd | ✅ | ✔ | ✔ |
| 41 | [forum-sqli2](NCTF26/challenges/web/forum-sqli2/) | — | ⏳ |  |  |
| 42 | [forum-xxe](NCTF26/challenges/web/forum-xxe/) | — | ⏳ |  |  |
| 43 | [graph-climb](NCTF26/challenges/web/graph-climb/) | — | ⏳ |  |  |
| 44 | [graphql-introspection-maze](NCTF26/challenges/web/graphql-introspection-maze/) | — | ⏳ |  |  |
| 45 | [hackusman--tablenest](NCTF26/challenges/web/hackusman--tablenest/) | hackusman | ⏳ |  |  |
| 46 | [hookrelay](NCTF26/challenges/web/hookrelay/) | — | ⏳ |  |  |
| 47 | [isid0r3--bibliotech](NCTF26/challenges/web/isid0r3--bibliotech/) | isid0r3 | ✅ |  | ✔ |
| 48 | [isid0r3--carnet](NCTF26/challenges/web/isid0r3--carnet/) | isid0r3 | ✅ |  | ✔ |
| 49 | [isid0r3--curfew](NCTF26/challenges/web/isid0r3--curfew/) | isid0r3 | 📝 |  | ✔ |
| 50 | [isid0r3--fleuriste2](NCTF26/challenges/web/isid0r3--fleuriste2/) | isid0r3 | ⏳ |  |  |
| 51 | [isid0r3--lazylax-ctf-challenge](NCTF26/challenges/web/isid0r3--lazylax-ctf-challenge/) | isid0r3 | ⏳ |  |  |
| 52 | [isid0r3--linkcard](NCTF26/challenges/web/isid0r3--linkcard/) | isid0r3 | ✅ |  | ✔ |
| 53 | [isid0r3--lockstep](NCTF26/challenges/web/isid0r3--lockstep/) | isid0r3 | 📝 |  | ✔ |
| 54 | [isid0r3--nexero](NCTF26/challenges/web/isid0r3--nexero/) | isid0r3 | ⏳ |  |  |
| 55 | [isid0r3--proformat](NCTF26/challenges/web/isid0r3--proformat/) | isid0r3 | ⏳ |  |  |
| 56 | [isid0r3--quickvote-ctf-challenge](NCTF26/challenges/web/isid0r3--quickvote-ctf-challenge/) | isid0r3 | ⏳ |  |  |
| 57 | [jwt-cousin](NCTF26/challenges/web/jwt-cousin/) | — | ⏳ |  |  |
| 58 | [jwt-forge](NCTF26/challenges/web/jwt-forge/) | — | ⏳ |  |  |
| 59 | [komisergio--adetikope](NCTF26/challenges/web/komisergio--adetikope/) | komisergio | ⏳ |  |  |
| 60 | [mass-assignment](NCTF26/challenges/web/mass-assignment/) | — | ⏳ |  |  |
| 61 | [oxdefault--les-archives-de-togoville](NCTF26/challenges/web/oxdefault--les-archives-de-togoville/) | oxdefault | ⏳ |  |  |
| 62 | [path-traversal-archive](NCTF26/challenges/web/path-traversal-archive/) | — | ⏳ |  |  |
| 63 | [php-unserialize](NCTF26/challenges/web/php-unserialize/) | — | 📝 | ✔ | ✔ |
| 64 | [reset-token-lcg](NCTF26/challenges/web/reset-token-lcg/) | — | ⏳ |  |  |
| 65 | [smuggle-gap](NCTF26/challenges/web/smuggle-gap/) | — | ⏳ |  |  |
| 66 | [sqlite-union](NCTF26/challenges/web/sqlite-union/) | — | ⏳ |  |  |
| 67 | [ssrf-metadata-decoy](NCTF26/challenges/web/ssrf-metadata-decoy/) | — | ⏳ |  |  |
| 68 | [ssti-jinja](NCTF26/challenges/web/ssti-jinja/) | — | ⏳ |  |  |
| 69 | [the-darknova--graphql-ast-alchemist](NCTF26/challenges/web/the-darknova--graphql-ast-alchemist/) | the-darknova | 📁 | ✔ |  |
| 70 | [the-darknova--hpack-h2c-smuggler](NCTF26/challenges/web/the-darknova--hpack-h2c-smuggler/) | the-darknova | ⏳ |  |  |
| 71 | [the-darknova--phantom-cache](NCTF26/challenges/web/the-darknova--phantom-cache/) | the-darknova | ⏳ |  |  |
| 72 | [thierry8petstar--cine-noctambule](NCTF26/challenges/web/thierry8petstar--cine-noctambule/) | thierry8petstar | ✅ | ✔ | ✔ |
| 73 | [thierry8petstar--classic-login](NCTF26/challenges/web/thierry8petstar--classic-login/) | thierry8petstar | ⏳ |  |  |
| 74 | [thierry8petstar--ghostflag](NCTF26/challenges/web/thierry8petstar--ghostflag/) | thierry8petstar | ✅ |  | ✔ |
| 75 | [thierry8petstar--shadow-catalog](NCTF26/challenges/web/thierry8petstar--shadow-catalog/) | thierry8petstar | ⏳ |  |  |
| 76 | [webhook-relay](NCTF26/challenges/web/webhook-relay/) | — | ⏳ |  |  |

## 🌍 ECOWAS CTF 2026 / épreuves à identifier

Épreuves présentes dans l’archive mais absentes de la liste officielle NCTF26 (auteur non encore identifié). Détails et pistes de rangement : [`ECOWASCTF 2026/A_CLASSER.md`](ECOWASCTF%202026/A_CLASSER.md).

| # | Épreuve | Auteur | Statut |
|---|---|---|---|
| 1 | [acme-license](ECOWASCTF%202026/acme-license/) | — | 📁 |
| 2 | [AEGIS-VAULT](ECOWASCTF%202026/AEGIS-VAULT/) | — | ✅ |
| 3 | [archive-olympio](ECOWASCTF%202026/archive-olympio/) | — | 📝 |
| 4 | [bmp-zip](ECOWASCTF%202026/bmp-zip/) | — | ✅ |
| 5 | [bnat-memdump](ECOWASCTF%202026/bnat-memdump/) | — | 📁 |
| 6 | [bnat-vm](ECOWASCTF%202026/bnat-vm/) | — | 📁 |
| 7 | [breach](ECOWASCTF%202026/breach/) | — | ✅ |
| 8 | [bytecode-vm](ECOWASCTF%202026/bytecode-vm/) | — | 📁 |
| 9 | [c2pa-provenance](ECOWASCTF%202026/c2pa-provenance/) | — | 📁 |
| 10 | [c5-ecdlp](ECOWASCTF%202026/c5-ecdlp/) | — | 📝 |
| 11 | [capture-memory](ECOWASCTF%202026/capture-memory/) | — | ✅ |
| 12 | [ch33](ECOWASCTF%202026/ch33/) | — | 📁 |
| 13 | [chall](ECOWASCTF%202026/chall/) | — | ✅ |
| 14 | [chall-pie5](ECOWASCTF%202026/chall-pie5/) | — | 📁 |
| 15 | [ChannelBot](ECOWASCTF%202026/ChannelBot/) | — | ✅ |
| 16 | [checksum-match](ECOWASCTF%202026/checksum-match/) | — | 📁 |
| 17 | [desk-photo](ECOWASCTF%202026/desk-photo/) | — | ✅ |
| 18 | [ecdsa-nonce-reuse](ECOWASCTF%202026/ecdsa-nonce-reuse/) | — | 📝 |
| 19 | [entvault-apk](ECOWASCTF%202026/entvault-apk/) | — | 📁 |
| 20 | [espace-client](ECOWASCTF%202026/espace-client/) | — | 📁 |
| 21 | [exfil-capture](ECOWASCTF%202026/exfil-capture/) | — | 📁 |
| 22 | [exif-decoy](ECOWASCTF%202026/exif-decoy/) | — | 📁 |
| 23 | [finale-pdf](ECOWASCTF%202026/finale-pdf/) | — | 📝 |
| 24 | [foodctf](ECOWASCTF%202026/foodctf/) | — | 📝 |
| 25 | [fzlp](ECOWASCTF%202026/fzlp/) | — | 📁 |
| 26 | [git-web-exposure](ECOWASCTF%202026/git-web-exposure/) | — | 📝 |
| 27 | [halcyon](ECOWASCTF%202026/halcyon/) | — | 📝 |
| 28 | [hastad-broadcast](ECOWASCTF%202026/hastad-broadcast/) | — | ✅ |
| 29 | [hid-tablet](ECOWASCTF%202026/hid-tablet/) | — | 📝 |
| 30 | [host-inventory](ECOWASCTF%202026/host-inventory/) | — | 📝 |
| 31 | [incident-analysis](ECOWASCTF%202026/incident-analysis/) | — | 📁 |
| 32 | [indice](ECOWASCTF%202026/indice/) | — | 📁 |
| 33 | [internal-toolbox](ECOWASCTF%202026/internal-toolbox/) | — | 📁 |
| 34 | [jpg-zip-polyglot](ECOWASCTF%202026/jpg-zip-polyglot/) | — | 📁 |
| 35 | [lcg-stream](ECOWASCTF%202026/lcg-stream/) | — | ✅ |
| 36 | [memdump-raw](ECOWASCTF%202026/memdump-raw/) | — | 📁 |
| 37 | [multi-log-siem](ECOWASCTF%202026/multi-log-siem/) | — | 📝 |
| 38 | [niamtougou](ECOWASCTF%202026/niamtougou/) | — | 📁 |
| 39 | [notsie-ad](ECOWASCTF%202026/notsie-ad/) | — | 📁 |
| 40 | [path-traversal-cdn](ECOWASCTF%202026/path-traversal-cdn/) | — | 📁 |
| 41 | [pe-resources](ECOWASCTF%202026/pe-resources/) | — | 📁 |
| 42 | [php-upload-rce](ECOWASCTF%202026/php-upload-rce/) | — | 📝 |
| 43 | [pop1](ECOWASCTF%202026/pop1/) | — | 📁 |
| 44 | [prison-pipeline](ECOWASCTF%202026/prison-pipeline/) | — | 📝 |
| 45 | [prng-stream](ECOWASCTF%202026/prng-stream/) | — | 📁 |
| 46 | [replay-gate](ECOWASCTF%202026/replay-gate/) | — | 📝 |
| 47 | [rsa-coppersmith](ECOWASCTF%202026/rsa-coppersmith/) | — | 📝 |
| 48 | [rsa-leak-p](ECOWASCTF%202026/rsa-leak-p/) | — | ✅ |
| 49 | [sayen-forum-stego](ECOWASCTF%202026/sayen-forum-stego/) | — | 📝 |
| 50 | [securebank-apk](ECOWASCTF%202026/securebank-apk/) | — | 📁 |
| 51 | [sentinelbot](ECOWASCTF%202026/sentinelbot/) | — | ✅ |
| 52 | [ssrf-ec2](ECOWASCTF%202026/ssrf-ec2/) | — | 📝 |
| 53 | [svg-mosaic](ECOWASCTF%202026/svg-mosaic/) | — | 📁 |
| 54 | [validator](ECOWASCTF%202026/validator/) | — | 📁 |
| 55 | [vault-vlt1](ECOWASCTF%202026/vault-vlt1/) | — | 📁 |
| 56 | [vaultpay-apk](ECOWASCTF%202026/vaultpay-apk/) | — | ✅ |
| 57 | [void](ECOWASCTF%202026/void/) | — | 📁 |
| 58 | [wasm-checker](ECOWASCTF%202026/wasm-checker/) | — | 📁 |
| 59 | [xor-repeat](ECOWASCTF%202026/xor-repeat/) | — | ✅ |

## 🤝 Contribuer

1. Retrouver l’énoncé → `sujet/enonce.md` (copie exacte, avec les points).
2. Déposer les fichiers d’origine, sans les modifier → `fichiers/`.
3. Rédiger `solve/writeup.md` (analyse, exploitation, flag) et ajouter les scripts.
4. Mettre à jour le statut dans le `README.md` de l’épreuve.

## ⚖️ Crédits et avertissement

Les épreuves appartiennent à leurs auteurs respectifs et aux organisateurs (CERT.tg pour le NCTF26). Cette archive est publiée à des fins **pédagogiques** après la fin des compétitions. Les adresses `*.t.ctf.tg` présentes dans les write-ups étaient des instances temporaires, aujourd’hui expirées. Auteur ou organisateur souhaitant le retrait d’une épreuve : ouvrez une *issue*.

