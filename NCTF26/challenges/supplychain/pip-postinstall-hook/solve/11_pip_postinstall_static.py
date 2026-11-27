#!/usr/bin/env python3
import tarfile,re
with tarfile.open('pieces_jointes/acme-license-check-1.0.0.tar.gz') as z:
 setup=z.extractfile('acme-license-check-1.0.0/setup.py').read().decode()
encoded=re.search(r'_B\s*=\s*"([0-9a-f]+)"',setup).group(1)
print(bytes(x^91 for x in bytes.fromhex(encoded)).decode())
# This never executes the decoded program or performs a package installation.
