### 07. Forensic USB — reconstruction par SCSI WRITE(10) — `usb-write10`

**Statut :** FLAG RAPPORTÉ · **Points :** — · **Instance :** `—`

**Fichiers d’origine associés :** `capture(1).pcap`, `recovered_usb.png`.

#### Énoncé, contexte et périmètre

Le défi de forensic consiste à réassembler une image écrite sur un périphérique USB à partir d'une capture (`capture(1).pcap`). Les échanges antérieurs évoquent des commandes SCSI `WRITE(10)` et les secteurs 2048 à 2073. Une image `recovered_usb.png` a été produite/conservée comme résultat.

#### Reconnaissance, commandes et résultats observés

Le flag communiqué lors des échanges est documenté, mais la trace détaillée de toutes les trames extraites n'est pas montée. On conserve donc la PCAP et la PNG comme preuves à reprendre au besoin.

#### Procédure de reproduction ou reprise technique

```bash
file 'capture(1).pcap' recovered_usb.png
tshark -r 'capture(1).pcap' -q -z io,phs
xxd -l 32 recovered_usb.png
```
Extraire les LBA des WRITE(10), ordonner les blocs et contrôler la signature PNG, pas seulement les rechercher comme chaînes dans le flux.

#### Résultat / flag

**NCTF{t0ut_c3_qu1_3st_3cr1t_r3st3}**

#### Pièges, interprétation et enseignement

Le résultat est rapporté dans une conversation antérieure ; conserver la distinction avec la preuve de reconstruction complète.
