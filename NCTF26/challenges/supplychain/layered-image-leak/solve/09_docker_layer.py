#!/usr/bin/env python3
import io,tarfile,base64
with tarfile.open('pieces_jointes/image.tar') as outer:
 for layer in outer.getmembers():
  if layer.name.endswith('/layer.tar'):
   with tarfile.open(fileobj=io.BytesIO(outer.extractfile(layer).read())) as inner:
    for member in inner.getmembers():
     if member.isfile() and member.name.endswith('secret.env') and not member.name.endswith('.wh.secret.env'):
      data=inner.extractfile(member).read().decode().strip().split('=',1)[1]
      print(base64.b64decode(data).decode())
