#!/usr/bin/env python3
from zipfile import ZipFile
import re,base64
with ZipFile('pieces_jointes/app-release.apk') as z:
 xml=z.read('res/values/strings.xml').decode()
 config=z.read('sources/com/vault/app/BuildConfig.java').decode()
encoded=re.search('<string name="enc_blob">([^<]+)',xml).group(1)
key=re.search('API_SECRET = "([^"]+)"',config).group(1).encode()
blob=base64.b64decode(encoded)
print(bytes(x^key[i%len(key)] for i,x in enumerate(blob)).decode())
