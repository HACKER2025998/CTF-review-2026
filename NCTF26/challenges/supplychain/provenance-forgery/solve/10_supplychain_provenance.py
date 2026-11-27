#!/usr/bin/env python3
import tarfile,re,base64
with tarfile.open('pieces_jointes/acme-app-1.2.0.tgz') as z:
 s=z.extractfile('dist/app.js').read().decode()
encoded=re.search(r"_t\s*=\s*'([^']+)'",s).group(1)
print(base64.b64decode(encoded).decode())
