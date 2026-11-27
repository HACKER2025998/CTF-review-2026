#!/usr/bin/env python3
"""Regenerate the repository README.md from the challenge folders.

Usage (from the repository root):  python3 scripts/generate_readme.py
Each challenge lives in <CTF>/challenges/<category>/<name>/ with README.md,
sujet/ (statement), fichiers/ (original files) and solve/ (write-up + scripts).
"""
import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
REPO = 'https://github.com/HACKER2025998/CTF-review-2026'
TEMPLATE_MARK = ('NCTF{...}', '`...`')

CTFS = [  # (folder, title, description)
    ('NCTF26', 'NCTF26 — Togo National CTF 2026',
     'National CTF of Togo organised by CERT.tg (final in Lomé, 19–20 November 2026). '
     'The full official list of **525 challenges** is archived, each with its author.'),
    ('ECOWASCTF 2026', 'ECOWAS CTF 2026', 'Regional ECOWAS CTF (flag format `EcowasCTF{...}`), West-African themed challenges.'),
    ('RedX Qualification 2026', 'RedX (RedReaper) Qualification 2026',
     'Online qualification round of the RedX / RedReaper CTF (27 November 2026, CTFd, flag format `RxR{...}`). '
     'All **59 challenges** archived with statement, author, difficulty and original files.'),
    ('HackDCTF 2026', 'HackDCTF 2026', 'Challenges from HackDCTF (flag format `HackDCTF{...}` / `HackCTF{...}`).'),
    ('Other platforms/Cyberini', 'Cyberini', 'Training challenges and write-ups from the Cyberini platform.'),
    ('Other platforms/TryHackMe', 'TryHackMe', 'TryHackMe rooms with a write-up.'),
    ('Other platforms/BDSec', 'BDSec', 'Challenges from BDSec CTF.'),
    ('Other platforms/Root-Me', 'Root-Me', 'Root-Me challenge files only — Root-Me rules forbid publishing solutions.'),
    ('Unsorted 2026', 'Unsorted 2026', 'Challenges played in 2026 whose event has not been identified yet.'),
]

def field(text, *keys):
    for k in keys:
        m = re.search(rf'^\| {k} \| (.*?) \|$', text, re.M)
        if m: return m.group(1).strip()
    return ''

def info(d):
    rd = (d / 'README.md').read_text(errors='ignore') if (d / 'README.md').exists() else ''
    author = field(rd, 'Auteur', 'Author')
    if not author or author.lower().startswith(('inconnu', 'unknown')): author = '—'
    flag = field(rd, 'Flag')
    files = (d / 'fichiers').is_dir() and any(p.name != '.gitkeep' for p in (d / 'fichiers').iterdir())
    instance_only = not files and '## Statement' in ((d / 'sujet/enonce.md').read_text(errors='ignore') if (d / 'sujet/enonce.md').exists() else '')
    public = (d / 'solve' / 'writeup_alwil17.md').exists()
    solve = (d / 'solve').is_dir() and any(
        p.name not in ('.gitkeep', 'writeup_alwil17.md') and not (p.name == 'writeup.md' and any(t in p.read_text(errors='ignore') for t in TEMPLATE_MARK)
                                      and len(p.read_text(errors='ignore')) < 600)
        for p in (d / 'solve').iterdir())
    if flag and flag != '—': status = '✅'
    elif solve: status = '📝'
    elif public: status = '📖'
    elif files or instance_only: status = '📁'
    else: status = '⏳'
    return author, status, files, solve or public

def challenges(ctf):
    base = ROOT / ctf / 'challenges'
    if not base.is_dir(): return []
    out = []
    for cat in sorted(p for p in base.iterdir() if p.is_dir()):
        for d in sorted((p for p in cat.iterdir() if p.is_dir()), key=lambda p: p.name.lower()):
            out.append((cat.name, d.name, d, *info(d)))
    return out

def link(path):
    return quote(str(path.relative_to(ROOT))) + '/'

data = {c[0]: challenges(c[0]) for c in CTFS}
unidentified = sorted((p for p in (ROOT / 'NCTF26/_unidentified').iterdir() if p.is_dir() and not p.name.startswith('_')),
                      key=lambda p: p.name.lower()) if (ROOT / 'NCTF26/_unidentified').is_dir() else []
total = sum(len(v) for v in data.values())
st = Counter(r[4] for v in data.values() for r in v)

o = []
o += ['# 🏴 CTF Review 2026 — Challenge Archive', '',
      'A structured archive of the CTF challenges played in **2026**: every challenge has its own folder with the statement, '
      'the original files, the author and — when available — a write-up and solve scripts. Write-ups are being added progressively.', '',
      '> Team **1HUNTERS** — maintained by **xhackerip**.', '']
o += ['## 📊 At a glance', '', '| Event / platform | Challenges |', '|---|---|']
for folder, title, _ in CTFS:
    o.append(f'| [{title}](#{re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")}) | {len(data[folder])} |')
o += [f'| **Total** | **{total}** |', '',
      f'Status: ✅ solved (flag recovered) **{st["✅"]}** · 📝 write-up / scripts in progress **{st["📝"]}** · '
      f'📖 public write-up available **{st["📖"]}** · 📁 files available, not solved yet **{st["📁"]}** · ⏳ statement still to retrieve **{st["⏳"]}**', '']
o += ['## 🗂️ Repository layout', '', '```',
      'CTF-review-2026/',
      '├── README.md',
      '├── scripts/generate_readme.py      regenerates this README',
      '├── NCTF26/',
      '│   ├── INDEX.md                    detailed index (status + flags, French)',
      '│   ├── scoreboard.md               flag tracking during the event',
      '│   ├── challenges/<category>/<challenge>/',
      '│   ├── _unidentified/              NCTF26 material not yet matched to an official challenge',
      '│   ├── kingofthehill/              King of the Hill toolkit + write-ups',
      '│   ├── tools/  templates/',
      '├── ECOWASCTF 2026/challenges/<category>/<challenge>/',
      '├── RedX Qualification 2026/challenges/<category>/<challenge>/',
      '├── HackDCTF 2026/challenges/...',
      '├── Other platforms/{Root-Me,TryHackMe,Cyberini,BDSec}/challenges/...',
      '└── Unsorted 2026/challenges/...',
      '```', '',
      'Every challenge folder follows the same structure:', '',
      '```',
      '<challenge>/',
      '├── README.md     category, author, status, flag, provenance',
      '├── sujet/        statement (enonce.md)',
      '├── fichiers/     original challenge files, left untouched',
      '└── solve/        write-up (writeup.md) and solve scripts',
      '```', '',
      'NCTF26 challenge names follow the platform convention `author--challenge-name` when the author is known '
      '(e.g. `boazak--sodabi`). Folder names `sujet/fichiers/solve` are French for *statement/files/solve*; '
      'NCTF26 write-ups are written in French.', '']
o += ['## 🚀 Usage', '', '```bash', f'git clone {REPO}.git',
      'cd CTF-review-2026/NCTF26/challenges/crypto/fermat-twins',
      'cat sujet/enonce.md       # read the statement', 'ls fichiers/               # challenge files',
      'python3 solve/solve.py     # replay the solution', '```', '',
      '> ⚠️ **Spoilers:** `solve/`, `INDEX.md`, `scoreboard.md` and per-challenge READMEs contain solutions and flags. '
      'To practise, only look at `sujet/` and `fichiers/`.', '>',
      '> ⚠️ Some files are **intentionally malicious** binaries or scripts (reverse, pwn, forensics, supply-chain challenges). '
      'Only run them inside an isolated VM.', '']

legend = ('Legend: ✅ solved · 📝 write-up / scripts in progress · 📖 public write-up (alwil17) · 📁 files available · ⏳ statement to retrieve. '
          'Columns 📁 / 🛠️: challenge files / solve material present.')

for folder, title, desc in CTFS:
    rows = data[folder]
    o += [f'## {title}', '', desc, '']
    if not rows:
        o += ['_No challenge yet._', '']; continue
    cats = Counter(r[0] for r in rows)
    if folder == 'NCTF26':
        authors = Counter()
        for r in rows:
            for a in r[3].split(','):
                a = a.strip().split(' (')[0]
                if a != '—': authors[a] += 1
        o += ['### Categories', '', '| Category | Challenges |', '|---|---|']
        o += [f'| {c} | {n} |' for c, n in sorted(cats.items())]
        o += ['', '### Authors', '', '| Author | Challenges |', '|---|---|']
        o += [f'| {a} | {n} |' for a, n in authors.most_common()]
        o += [f'| _not specified_ | {sum(1 for r in rows if r[3] == "—")} |', '']
        o += ['### Full challenge list', '', legend, '']
        for c in sorted(cats):
            o += ['<details>', f'<summary><b>{c}</b> ({cats[c]} challenges)</summary>', '',
                  '| # | Challenge | Author | Status | 📁 | 🛠️ |', '|---|---|---|---|---|---|']
            for i, r in enumerate((r for r in rows if r[0] == c), 1):
                o.append(f'| {i} | [{r[1]}]({link(r[2])}) | {r[3]} | {r[4]} | {"✔" if r[5] else ""} | {"✔" if r[6] else ""} |')
            o += ['', '</details>', '']
        if unidentified:
            o += ['### Unidentified NCTF26 material', '',
                  f'{len(unidentified)} folders of NCTF26 files and write-ups not yet matched to an official challenge '
                  '(see [`NCTF26/_unidentified/A_CLASSER.md`](NCTF26/_unidentified/A_CLASSER.md) for suggestions).', '',
                  '<details>', '<summary>Show the list</summary>', '',
                  ', '.join(f'[`{p.name}`]({link(p)})' for p in unidentified), '', '</details>', '']
    else:
        o += [legend, '', '| # | Category | Challenge | Author | Status | 📁 | 🛠️ |', '|---|---|---|---|---|---|---|']
        for i, r in enumerate(rows, 1):
            o.append(f'| {i} | {r[0]} | [{r[1]}]({link(r[2])}) | {r[3]} | {r[4]} | {"✔" if r[5] else ""} | {"✔" if r[6] else ""} |')
        o.append('')

o += ['## 🤝 Contributing', '',
      '1. Retrieve the exact statement → `sujet/enonce.md` (with points and author).',
      '2. Add the original files, unmodified → `fichiers/`.',
      '3. Write `solve/writeup.md` (analysis, exploitation, flag) and add the solve scripts.',
      '4. Update the status/flag in the challenge `README.md`, then run `python3 scripts/generate_readme.py`.', '',
      '## 📖 Public write-ups by alwil17', '',
      f'{sum(1 for v in data.values() for r in v if (r[2] / "solve/writeup_alwil17.md").exists())} NCTF26 challenges include a public write-up by '
      '[**alwil17**](https://github.com/Alwil17), copied from <https://alwil17.github.io/ctf-writeups/> '
      '([source](https://github.com/Alwil17/ctf-writeups)) under the MIT License — see '
      '[`THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`](THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE). '
      'They are stored as `solve/writeup_alwil17.md` with a link to the original article. Thanks to alwil17! '
      'Their flags are partially masked, as in the original articles.', '',
      '## ⚖️ Credits & disclaimer', '',
      'All challenges belong to their respective authors and organisers (CERT.tg for NCTF26, the ECOWAS CTF organisers, the RedX / RedReaper team, '
      'HackDCTF, Cyberini, TryHackMe, BDSec, Root-Me). This archive is published for **educational purposes** after the events '
      'ended. The `*.t.ctf.tg` addresses found in write-ups were temporary instances and have expired. '
      'Public NCTF26 write-ups (`writeup_alwil17.md`) are © 2026 [alwil17](https://github.com/Alwil17), MIT License. '
      'If you are an author or organiser and want a challenge removed, please open an issue.', '']

(ROOT / 'README.md').write_text('\n'.join(o) + '\n')
print(f'README.md regenerated: {total} challenges', dict(st))
