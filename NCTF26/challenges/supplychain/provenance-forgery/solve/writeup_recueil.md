### 25. ACME — signature in-toto/SLSA forgée — `acme-provenance`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `acme-app-1.0.0.tgz`, `acme-app-1.1.0.tgz`, `acme-app-1.2.0.tgz`, `acme-app-1.3.0.tgz`, `1.0.0.intoto.json`, `1.1.0.intoto.json`, `1.2.0.intoto.json`, `1.3.0.intoto.json`, `ci-signing.key`.

#### Énoncé, contexte et périmètre

Les quatre versions `acme-app-1.0.0.tgz` à `1.3.0.tgz` ont chacune une déclaration in-toto/SLSA. Dans la version `1.2.0`, `dist/app.js` diffère des autres : une chaîne Base64 `_t` figure dans un commentaire de hotfix. `1.2.0.intoto.json` prétend utiliser `acme-ci` et porte une signature codée entièrement en zéros. La présence formelle d'un document de provenance ne valide ni l'identité du builder ni l'intégrité de son sujet.

#### Reconnaissance, commandes et résultats observés

L'extraction de `dist/app.js` en version 1.2.0 et le décodage de `_t` ont été vérifiés localement. Les fichiers d'attestation et la clé fournie sont archivés pour les tests d'authenticité ultérieurs.

#### Procédure de reproduction ou reprise technique

```bash
for p in acme-app-*.tgz; do echo "--- $p"; tar -xOzf "$p" dist/app.js; done
sha256sum acme-app-*.tgz
# Comparer les digests au champ subject[].digest.sha256
```

#### Résultat / flag

**NCTF{w3ak_provenance_sig_forged_release_4e7a}**

#### Pièges, interprétation et enseignement

Une attestation non vérifiée ne constitue pas une provenance fiable, même si les champs JSON sont conformes au standard.
