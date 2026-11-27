### 34. VaultPay — BuildConfig API_SECRET et strings.xml — `vaultpay-apk`

**Statut :** FLAG VÉRIFIÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `app-release.apk`.

#### Énoncé, contexte et périmètre

L'APK `app-release.apk` contient un projet Android décompilé au package `com.vault.app`, version 1.4.2. Dans `res/values/strings.xml`, `enc_blob` encode en Base64 un jeton ; la classe `BuildConfig.java` embarque `API_SECRET`, et `MainActivity.java` effectue un XOR entre les octets décodés et les octets de clé répétés périodiquement. Le source de la méthode explique directement le chiffrement réversible du jeton premium.

#### Reconnaissance, commandes et résultats observés

Le décodage du blob et le XOR ont été vérifiés depuis l'APK fourni. Le texte découvert correspond à la valeur rapportée lors des échanges.

#### Procédure de reproduction ou reprise technique

```python
from zipfile import ZipFile
import base64,re
with ZipFile('app-release.apk') as z:
 xml=z.read('res/values/strings.xml').decode()
 cfg=z.read('sources/com/vault/app/BuildConfig.java').decode()
val=re.search(r'<string name="enc_blob">([^<]+)',xml).group(1)
key=re.search(r'API_SECRET = "([^"]+)"',cfg).group(1).encode()
b=base64.b64decode(val)
print(bytes(c^key[i%len(key)] for i,c in enumerate(b)).decode())
```

#### Résultat / flag

**NCTF{h4rdc0d3d_k3y_in_str1ngs_xml}**

#### Pièges, interprétation et enseignement

Une clé embarquée dans un client mobile n'est jamais un secret inaccessible à l'utilisateur.
