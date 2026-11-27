# Spare Key

- **Category:** DFIR
- **Author:** odytr
- **Difficulty:** Hard
- **Points:** 100 (dynamic, initial 500)
- **Solves:** 66
- **Instance:** dynamic Docker instance (launched from the platform)

## Statement

A hosting company we work with found a file called `key.ppk` in `/tmp` on one of their customers' Linux servers. Right next to it was a crontab entry nobody had added. They think the box was brute forced over SSH and they've asked whether we saw the same people.

We have a sensor called dmz-ssh-01 that's left open on port 22. Its logs from 10 August to 30 September 2026 are loaded into Kibana for you:

link: https://sparekey.redx.site

There's nothing to download.

Connect and start solving to get your flag.

nc: start your instance below; the address appears there.
