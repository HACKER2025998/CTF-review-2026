# Lomé Transit 04:17 — reconstruire un incident à partir d'artefacts Windows

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/lome-transit-0417/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — Un bundle DFIR Windows. Les journaux de sécurité donnent le compte
> réseau, Prefetch/Amcache identifient la machine hôte, et un dump mémoire livre un
> `STAGE_TOKEN`. J'assemble ces trois éléments pour former l'identifiant d'incident
> demandé. **Flag :** `NCTF{…}`.

## 1. Compte réseau — journaux de sécurité

Les Security Event Logs (ouvertures de session 4624/4625, type réseau) isolent le
**compte** utilisé par l'intrus.

## 2. Machine hôte — Prefetch / Amcache

Prefetch et Amcache tracent les exécutables lancés et leur machine d'origine.
J'en extrais l'identité de l'**hôte** impliqué.

## 3. Jeton — dump mémoire

Le dump mémoire contient un `STAGE_TOKEN` (chaîne de mise en scène du stager). Je le
récupère par recherche de motif dans l'image :

```bash
strings -el memory.dmp | grep -i STAGE_TOKEN
```

## 4. Assembler l'identifiant

L'identifiant d'incident attendu combine compte + hôte + jeton selon le gabarit
indiqué par le challenge. Une fois les trois pièces en main, je le compose — c'est
le flag.

## 5. Flag

```text
NCTF{…}
```

## 6. Leçons

- **Chaque artefact répond à une question** : qui (Security logs), où
  (Prefetch/Amcache), quoi (mémoire). Le DFIR consiste à recoller ces réponses en
  une seule histoire datée.
