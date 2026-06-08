---
name: "OSCP+ Exam Architecture — Scoring & Restrictions"
description: "Complete OSCP+ exam structure including scoring breakdown, passing combinations, tool restrictions, exam timeline, machine reverts, and what to expect on exam day."
tags: [oscp, exam, scoring, restrictions, architecture]
---

# OSCP+ Exam Architecture

## Scoring (OSCP+ 2024+)

| Komponen | Poin | Detail |
|----------|------|--------|
| AD Set (3 machines) | 40 pts (10+10+20) | Assumed breach: mulai dengan domain user credentials |
| Standalone 1 | 20 pts (10 local + 10 proof) | Initial access + privilege escalation |
| Standalone 2 | 20 pts (10 local + 10 proof) | Initial access + privilege escalation |
| Standalone 3 | 20 pts (10 local + 10 proof) | Initial access + privilege escalation |
| **Passing** | **70/100** | Kombinasi partial credit dimungkinkan |

## Passing Combinations

- 40 pts (AD full) + 3 local.txt flags = 70 pts
- 40 pts (AD full) + 2 local + 1 proof = 70 pts
- 20 pts (AD partial) + 3 local + 2 proof = 70 pts
- 10 pts (AD partial) + 3 standalone full = 70 pts

## Restrictions

- **Metasploit**: hanya boleh digunakan di SATU target
- **AI Chatbots**: DILARANG (ChatGPT, YouChat, OffSec KAI, dll)
- **Commercial tools**: Burp Pro, Metasploit Pro, Nessus, OpenVAS — DILARANG
- **Automatic exploitation**: sqlmap, db_autopwn, browser_autopwn — DILARANG
- **Allowed**: Nmap, NSE, Nikto, Burp Community, ffuf, feroxbuster, manual tooling

## Exam Timeline

- **23h45m**: Hacking phase
- **24h**: Report submission window
- **Format**: PDF via .7z, upload ke upload.offsec.com
- **Nama file**: `OSCP-OS-XXXXX-Exam-Report.7z`

## Best Practices

- Prioritaskan AD set (40 pts — blok terbesar)
- Parallel scan semua IP di 30 menit pertama
- Simpan Metasploit untuk satu machine paling susah
- Gunakan auxiliary modules (scanner, fuzzer) bebas — tidak dihitung sebagai Metasploit restriction
