#!/usr/bin/env python3
from zipfile import ZipFile
with ZipFile('pieces_jointes/archive.zip') as z: print(z.comment.decode())
