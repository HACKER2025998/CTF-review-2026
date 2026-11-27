#!/usr/bin/env python3
import json
s=json.load(open('pieces_jointes/proxy_storage.json'))['0x'+'0'*64]
print(bytes.fromhex(s[2:]).rstrip(bytes([0])).decode())
