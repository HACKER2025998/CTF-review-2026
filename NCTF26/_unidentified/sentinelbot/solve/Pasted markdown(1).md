SentinelBot is an offline support assistant shipped as a single Python module, `oracle.py`, exposing `respond(prompt)`. It guards a hidden diagnostic token and politely refuses when you ask about it directly.

Everything runs locally -- no network, no real model. Call the shipped oracle from your own script and make it hand over the token. That token is the flag.\
Stuck? Hints are available (they cost a few points).\
Flag format: NCTF{...}

Défi AI, 50 pts. Pas besoin de « bypasser » quoi que ce soit : le flag est stocké en clair dans le source sous forme `base64(reverse(flag))` via la constante `_S`. Je décode directement cette valeur — c’est le même type de décodage que les challenges précédents.

Flag :

```
NCTF{b4s3_64_sn34ks_p4st_th3_wordl1st}
```

**Méthode** (write-up) : le défi se résout sans même toucher à `respond()`. Le secret est assemblé dans le source par `_secret()` qui fait `base64.b64decode(_S)[::-1]`. Il suffit de reprendre la constante `_S`, la décoder en base64, puis inverser la chaîne — exactement la logique du code.

Ce que le challenge *illustre* (utile pour ton write-up) : le garde-fou `_input_blocked` n’inspecte que le texte **brut** et bloque des mots comme `flag`/`secret`. Mais `_understand()`  décode ensuite le base64 et applique rot13 — donc un filtre qui ne  regarde que l’entrée brute laisse passer une demande encodée. Le nom du  flag le dit : `b4s3_64_sn34ks_p4st_th3_wordl1st`. La leçon : **filtrer l’entrée brute avant décodage est inefficace** ; il faut valider après normalisation/décodage.

6 flags. Suivant ! 🚩

NCTF26

&#x20;   Accès\
&#x20;   Défi\
&#x20;   KOTH\
&#x20;   Support\
&#x20;   Writeups\
&#x20;   Users\
&#x20;   Teams\
&#x20;   Scoreboard\
&#x20;   Challenges

&#x20;   Notifications\
&#x20;   Team\
&#x20;   Profile\
&#x20;   Settings

Defi d'ouverture : lisez bien AVANT d'abandonner

Le defi\
« Prends le contrôle de ctf.tg »\
n'est pas un simple obstacle a passer.

Le\
PREMIER\
a le resoudre\
se qualifie DIRECTEMENT pour la finale\
.

⚠️ Le bouton\
« J'abandonne » est IRREVERSIBLE\
: il debloque le reste de l'epreuve, mais vous\
renoncez definitivement\
a cette qualification automatique.

Il n'y a pas de minuteur\
: rien ne presse. Prenez le temps de l'etudier et de tenter votre chance avant de decider.\
Depart dans 30 min : equipes gerees auto + defi qualificatif

Depart dans 30 minutes\
(19h00, heure de Lome) !

Equipes incompletes & joueurs sans equipe\
: aucune inquietude. A 19h00, a la fermeture des inscriptions, le systeme\
vous place et complete / forme les equipes automatiquement\
. Vous n'avez rien a faire.

Defi d'ouverture\
: en entrant, chaque equipe verra d'abord\
un seul challenge\
. Le\
premier a le resoudre se qualifie DIRECTEMENT pour la finale\
! Vous pouvez aussi l'abandonner pour debloquer le reste de l'epreuve, mais c'est definitif et vous renoncez a cette qualification directe.

Bonne chance a toutes les equipes !\
Tous mes messages\
👑 King of the Hill\
The Throne\
koth-throne\
Trône\
z3n\_ · règne 47s\
Statut\
en ligne\
Points / tick\
5\
Retournements\
19\
Connexion\
[http://13.37.197.230:28490](http://13.37.197.230:28490)\
Votre jeton d'équipe (à planter sur la colline)\
242cb7b1d3645528\
Comment marquer

\#    Équipe    Points KotH\
1    Unkn0wn    165\
2    z3n\_    90\
3    TeamH4C    70\
The Citadel\
koth-citadel\
Trône\
z3n\_ · règne 3m 51s (expiré)\
Statut\
en ligne\
Points / tick\
5\
Retournements\
4\
Connexion\
ssh://player\@13.37.197.230:28491\
Votre jeton d'équipe (à planter sur la colline)\
3c1b1697d0dd57bf\
Comment marquer

\#    Équipe    Points KotH\
1    Unkn0wn    115\
2    z3n\_    30\
3    Gh0st Pr0t0c0l    5\
The Armory\
koth-armory\
Trône\
Unkn0wn · règne 4m 21s\
Statut\
en ligne\
Points / tick\
5\
Retournements\
6\
Connexion\
ssh://player\@13.37.197.230:28492\
Votre jeton d'équipe (à planter sur la colline)\
1e550913ec655b94\
Comment marquer

\#    Équipe    Points KotH\
1    Unkn0wn    152\
2    z3n\_    12\
3    FireTeam    10\
Reseau Fortune\
koth-reseau-fortune\
Trône\
z3n\_ · règne 1m 49s\
Statut\
en ligne\
Points / tick\
3\
Retournements\
6\
Connexion\
[http://13.37.197.230:28493](http://13.37.197.230:28493)\
Votre jeton d'équipe (à planter sur la colline)\
6eefff4072981996\
Comment marquer

\#    Équipe    Points KotH\
1    z3n\_    114\
2    Unkn0wn    36\
⚔ Fil du trône

&#x20;   il y a 47sz3n\_ reprend The Throne\
&#x20;   il y a 1m 18sUnkn0wn reprend The Throne\
&#x20;   il y a 1m 49sz3n\_ reprend The Throne\
&#x20;   il y a 1m 49sz3n\_ reprend Reseau Fortune\
&#x20;   il y a 2m 19sUnkn0wn reprend The Throne\
&#x20;   il y a 3m 21sz3n\_ reprend The Throne\
&#x20;   il y a 3m 51sUnkn0wn reprend The Throne\
&#x20;   il y a 3m 51sz3n\_ reprend The Citadel\
&#x20;   il y a 4m 22sz3n\_ reprend The Throne\
&#x20;   il y a 4m 22sUnkn0wn reprend The Armory\
&#x20;   il y a 4m 52sUnkn0wn reprend The Throne\
&#x20;   il y a 4m 52sz3n\_ reprend The Armory ½

Les points de King of the Hill s'ajoutent à votre score sur le scoreboard principal, tick après tick, tant que vous tenez la colline.\
CERT.tg\
Organisé par CERT.tg\
Powered by Hibris · ramses.dagban.tg\
NCTF26// console phaseen cours gel dans1j 03:17:33 🩸 first bloodOctogramme · calldata-cache canalchiffré terminalsécurisé

comment je fais ca ..???

Respire, je t’explique — et bonne nouvelle : le KOTH, lui, est **du jeu légitime** (infra dédiée à `13.37.197.230`, montée par les orgas pour être attaquée), contrairement au défi d’ouverture. Donc là, on y va.

**C’est quoi le principe.** Chaque « colline » est une machine vulnérable. Pour marquer, tu dois en **prendre le contrôle** puis y **planter le jeton de ton équipe**  à l’endroit prévu (le fichier « king » / l’endpoint du service). Tant  que ton jeton est en place, tu gagnes les points/tick affichés. Les  autres (Unkn0wn, z3n\_) te la reprennent en replantant le leur — d’où les  retournements toutes les 30 s.

**Réalité technique importante :** je **ne peux pas atteindre** `13.37.197.230` depuis mon environnement (réseau restreint aux dépôts de paquets). Donc le terminal, c’est **toi**  sur ta machine (ou la VM d’équipe). Moi je te guide, je lis tes  sorties, et je t’écris les scripts/exploits. On fonctionne exactement  comme un boot2root : **recon → faille → accès → planter le jeton**.

**Garde-fous KOTH** (règles du jeu, à respecter sinon disqualif) : on ne touche **qu’aux 4 collines** sur cette IP, jamais les machines des autres équipes, et on ne détruit pas le service commun — on plante le jeton, c’est tout.

⚠️ **Tes 4 jetons d’équipe que tu viens de coller sont secrets**  (ton battlebook dit de ne jamais les diffuser). Je ne les enregistre  nulle part. Évite de les reposter ailleurs — c’est eux qui prouvent ta  prise.

**On commence par la recon.** Les deux collines en HTTP sont les plus rapides à sonder. Lance ça sur ta machine et colle-moi tout :

bash

```bash
# versions des 4 services
nmap -sV -Pn -p 28490,28491,28492,28493 13.37.197.230

# les deux collines HTTP
curl -i http://13.37.197.230:28490/
curl -i http://13.37.197.230:28493/

# et regarde si un endpoint explique comment planter (souvent /, /king, /help, /howto)
curl -s http://13.37.197.230:28490/ | head -50
```

Pour les deux en **SSH** (28491, 28492), il  nous faut d’abord un point d’entrée — on verra avec la recon s’il y a  des creds par défaut, un service annexe, ou un indice dans les hills  HTTP.

Dis-moi juste une chose d’abord : **vous êtes combien d’actifs dans l’équipe là maintenant ?**  Le KOTH se tient à plusieurs (il faut re-planter en continu). S’il n’y a  que toi, on vise une colline à points/tick élevé qu’on prend vite,  plutôt que les 4.

Colle-moi la sortie recon et on attaque la première colline. 🚩

Thought for 1m 24s

Débloqué — le bypass `X-Forwarded-For: 127.0.0.1` a fait cracher `/debug`. On a tout ce qu’il faut pour **The Throne** :

- `hill_key` = `d2e775a9…` (clé HMAC, récupérée via l’endpoint de diagnostic du jeu lui-même)
- schéma : `HMAC_SHA1(HILL_KEY, team + '|' + ts)`
- tolérance d’horloge : 45 s

C’est la **solution prévue** du challenge : on signe une réclamation valide avec ton propre jeton et on l’envoie à `POST /throne`. Je te prépare l’outil de prise. Je vérifie d’abord que la signature se calcule correctement.

Created a file, shared a file, ran 2 commands

Lance ça sur ta Kali :

bash

```bash
python3 throne_claim.py
```

Ça envoie la réclamation signée avec ton jeton. Le serveur tranche entre les deux interprétations de la clé — **colle-moi sa réponse** et on sait tout de suite si The Throne est pris. Si c’est bon, `python3 throne_claim.py --hold` re-plante toutes les 20 s pour tenir face à Unkn0wn et z3n\_.

Sur **« prendre tous les KOTH »** — franchement, ce n’est pas un seul script, chaque colline est un problème distinct :

**The Throne (28490)** ✅ — résolu, scheme HMAC. C’est l’outil que je viens de t’envoyer.

**Reseau Fortune (28493)** — c’est une **appli Flask différente** (« le réseau le plus riche tient la couronne »). On ne la prend pas en signant un jeton : il faut exploiter la **logique métier** de ses endpoints `/api/*` (`/api/refund`, `/api/transfer`, `/api/bonus/activation`…)  pour gonfler le solde. Ça sent le refund/transfer abusable ou le bonus  de parrainage en boucle. Pull-moi la recon quand tu veux :

bash

```bash
curl -s http://13.37.197.230:28493/api/me
curl -s http://13.37.197.230:28493/debug -H 'X-Forwarded-For: 127.0.0.1'
```

**The Citadel (28491) et The Armory (28492)** — ce sont des **SSH** (OpenSSH 8.9). Pas d’endpoint HTTP à signer : il faut un **point d’entrée** (creds par défaut, clé trouvée ailleurs, ou un indice livré par une autre colline). Recon d’abord :

bash

```bash
ssh player@13.37.197.230 -p 28491    # voir si bannière / mot de passe / message
nc 13.37.197.230 28491 < /dev/null | head
```

Deux rappels importants : la règle du jeu **interdit le flood/DoS** — l’option `--hold`  à 20 s est large dans la tolérance, ne descends pas en dessous de \~10 s  pour ne pas basculer en stress réseau. Et à plusieurs sur l’équipe,  répartissez : une personne par colline, chacune son `--hold`.

Commence par coller la réponse de `throne_claim.py`. 🚩

Throne claim

PY

┌──(xhackerip㉿xkali)-[\~/NCTF26/defi1]\
└─$ python3 throne_claim.py \
[key=str] 200 {"ok": true, "king": "242cb7b1\u2026"}

┌──(xhackerip㉿xkali)-[\~/NCTF26/defi1]\
└─$

Thought for 8s

🎉 The Throne est pris — `{"ok": true, "king": "242cb7b1…"}`, ton équipe est reine. La bonne interprétation de la clé était la **chaîne hex** (`key=str`), à noter pour le write-up.

Pour **conserver** les points tick après tick (sinon z3n\_/Unkn0wn te la reprennent) :

bash

```bash
python3 throne_claim.py --hold
```

Laisse tourner dans un terminal dédié (20 s d’intervalle,  dans la tolérance de 45 s). Idéalement une personne de l’équipe garde ce  terminal ouvert pendant qu’on avance sur les autres.

**Pour le write-up, la chaîne complète de The Throne :**

1. Recon `/` → le POST `/throne` attend un HMAC, indice vers `/debug` « internal-only ».
2. `/debug` filtré sur l’IP → bypass via en-tête `X-Forwarded-For: 127.0.0.1` (le filtre fait confiance à un header que le client contrôle).
3. `/debug` livre `hill_key` + le schéma `HMAC_SHA1(HILL_KEY, team+'|'+ts)`.
4. On signe une réclamation avec notre jeton + timestamp courant → `POST /throne` → trône pris.

Leçon : **ne jamais autoriser un endpoint « interne » sur la base d’un en-tête falsifiable**, et ne pas exposer de secret de signature sur un endpoint accessible.

On enchaîne sur quelle colline ? Si tu veux Reseau Fortune (28493), colle-moi :

bash

```bash
curl -s http://13.37.197.230:28493/debug -H 'X-Forwarded-For: 127.0.0.1'
curl -s http://13.37.197.230:28493/api/me
```

🚩

How is Claude doing this session?