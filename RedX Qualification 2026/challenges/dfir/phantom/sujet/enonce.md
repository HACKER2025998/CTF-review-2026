# Phantom

- **Category:** DFIR
- **Author:** odytr
- **Difficulty:** Easy
- **Points:** 100 (dynamic, initial 500)
- **Solves:** 157
- **Instance:** none

## Statement

> !!The commands in the log are real, copied from the bot with the addresses swapped. Don't paste them into a shell. Downloads would fail, but the `rm` would still run. !!

We run an SSH sensor called edge-gw-03 that was left open to the internet on purpose. Over the weekend it logged a successful root login. 

Your lead wants these answered before the 10:00 standup:

1. What password did the attacker log in with?
2. What's the IP of the server the payloads were downloaded from?
3. The payload gets renamed before it runs. What name does it run under?
4. The dropper tries one build per CPU type. How many different builds does it try in total?

The malware file contents were replaced with `[REDACTED MALWARE BODY]` . Sizes and headers are the same.

Flag format: `RxR{password_ip_filename_count}`
