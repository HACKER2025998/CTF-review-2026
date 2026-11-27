# Robben's

- **Category:** DFIR
- **Author:** odytr
- **Difficulty:** Medium
- **Points:** 100 (dynamic, initial 500)
- **Solves:** 52
- **Instance:** none

## Statement

> !!The commands in the log are real, copied from the bot with the addresses swapped. Don't paste them into a shell. Downloads would fail, but other commands like `rm` would still run.!!

The break-in is going to our legal team, and their lawyer won't put anything in the report unless the evidence proves it. She already noticed that the sensor log and the pcap don't seem to agree, so she doesn't trust either one by itself.

The endpoint agent also caught one of the payloads, a file called robben, and deleted it before anyone kept a copy. The only thing left is a dump of its read-only data section.

Her questions:

1. The timestamps in the sensor log end in `Z`? What UTC offset is the sensor clock really using?
2. The sensor says at least one payload download failed. How many bytes of payload builds did the sensor actually receive in total? Every transfer counts
3. The text in robben's data section is hidden. What single-byte key hides it?
4. Botnet families copy each other's code and rename it. What does this one call itself?


Flag format: `RxR{offset_BytesTotal_key_name}`
