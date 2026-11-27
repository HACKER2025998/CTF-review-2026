#!/usr/bin/env python3
import hashlib
hashed=dict(line.strip().split(':',1) for line in open('pieces_jointes/dump.txt') if ':' in line)
for pw in open('pieces_jointes/wordlist(2).txt'):
 pw=pw.strip()
 for account,digest in hashed.items():
  if hashlib.sha1(pw.encode()).hexdigest()==digest:
   print(account,pw)
