# Phone home — Write-up

- **Category:** Crypto
- **Author:** FBI_Soldier
- **Flag:** `RxR{call_me_maybe}` *(plaintext recovered; confirm the exact wrapping on the platform)*

## TL;DR

`sms.txt` is an old-phone **multi-tap (T9) keypad** encoding. Each group of
repeated digits is one key press held N times; `0` is a space. Decoding gives the
message, which states the flag.

## Encoding

Classic nokia-style keypad:

```
2=ABC 3=DEF 4=GHI 5=JKL 6=MNO 7=PQRS 8=TUV 9=WXYZ 0=space
```

The number of repeats selects the letter: `4`→G, `44`→H, `444`→I, `7`→P,
`77`→Q, `777`→R, `7777`→S, etc.

## Solve

```python
keys = {'2':"ABC",'3':"DEF",'4':"GHI",'5':"JKL",'6':"MNO",
        '7':"PQRS",'8':"TUV",'9':"WXYZ"}
out = []
for grp in open("sms.txt").read().split():
    if grp == '0':
        out.append(' ')
    else:
        d = grp[0]
        out.append(keys[d][(len(grp)-1) % len(keys[d])])
print(''.join(out))
```

Input:

```
44 33 999 0 444 8 7777 0 6 33 0 8 44 33 0 333 555 2 4 0 444 7777 0 222 2 555 555 0 6 33 0 6 2 999 22 33
```

Decodes to:

```
HEY ITS ME THE FLAG IS CALL ME MAYBE
```

## Flag

The message says the flag is **"call me maybe"**:

```
RxR{call_me_maybe}
```

> Only the plaintext is certain; verify the exact formatting (underscores vs.
> spaces/case) when submitting.
