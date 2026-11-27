# Ticket

- **Category:** DFIR
- **Author:** odytr
- **Difficulty:** Medium
- **Points:** 100 (dynamic, initial 500)
- **Solves:** 123
- **Instance:** none

## Statement

Our Windows honeypot caught a file on 27 May 2026. Legal won't let us share the file, so all you get is what we put in the ticket:

`sha256:  815eccf206bc39d67ad9c903c823cc76c59ebb5e0e24ff1028b5242c53686a3a`

Nobody on the team has looked at it yet. You do it and answer these:

1. Most AV engines give it a generic name. Which family is it really? Named after a toolkit (one word, no spaces)
2. When was the DLL compiled, according to its PE header? (UTC).
3. A public YARA rule detects this downloader using two strings. One of them is the User-Agent it sends when it fetches its next stage. What product name is in that User-Agent (Before the slash)?
4. Later stages of this family spread over SMB same exploits as WannaCry used. Which Microsoft security bulletin patches them?

Flag format: `RxR{toolkit_yyyy-mm-dd_product_bulletin}`
