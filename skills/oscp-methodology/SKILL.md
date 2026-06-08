---
name: oscp-methodology
description: OSCP (Offensive Security Certified Professional) — mindset, metodologi, dan strategi komprehensif untuk PEN-200/OSCP+ mencakup filsafat Try Harder, 3 attack vectors, enumeration framework, privilege escalation AD/Linux/Windows, dan reporting.
license: MIT
compatibility: opencode
metadata:
  audience: penetration-testers
  workflow: exploitation
  source: offsec-pen-200
  standard: oscp
  year: "2026"
---

# OSCP — Metodologi & Pola Pikir

## Prerequisites

- Basic networking (TCP/IP, ports, protocols)
- Linux command line proficiency
- Basic scripting (Python, Bash, PowerShell)
- Understanding of web application fundamentals (HTTP, cookies, sessions)

## Quick Start Workflow

```bash
# 1. Parallel enumeration (30 menit pertama)
nmap -Pn -p- --min-rate 10000 -T4 $IP1 $IP2 $IP3 $IP4 $IP5 -oA nmap/all
nmap -Pn -sC -sV -p $(ports) $IP -oA nmap/services

# 2. Prioritize AD set (40 pts — blok terbesar)
bloodhound-python -d DOMAIN -u USER -p PASS -dc $DC -c All

# 3. Attack 3 vectors per service: version → misconfig → sensitive info
searchsploit $version
# Check default creds, anonymous access, file permissions

# 4. Escalate: sudo -l → SUID → capabilities → cron → creds → kernel

# 5. Document everything with screenshots (IP + hostname + flag)
```

## OSCP Mindset — "Try Harder"

OSCP bukan tentang tools. Tools berubah setiap tahun. OSCP adalah tentang **metodologi yang repeatable**, **pattern recognition**, dan **resourcefulness**.

### Golden Rules

1. **Enumerate everything before exploiting** — 80% waktu untuk enumeration
2. **Every version number matters** — searchsploit setiap versi
3. **Credentials found = try on ALL other services** — password reuse
4. **Stuck >30 menit → re-enumerate** — jangan gali rabbit hole
5. **Screenshots: IP + hostname + whoami + flag di frame yang SAMA**
6. **Metasploit on ONE machine max** — simpan untuk machine paling susah
7. **Breaks every 3-4 hours** — mandatory, not optional

### Pattern Recognition (Radiologist Model)

Latih ribuan machine sampai pattern langsung terlihat. Tapi pattern recognition saja tidak cukup — Anda juga butuh **repeatable process sistematis**: service berperilaku aneh? → check version → searchsploit → Google → check config → manual test.

### 3 Pertanyaan Kunci Saat Stuck

1. Apa yang saya lewatkan?
2. Sudahkah saya enumerate port non-standard?
3. Sudahkah saya mencoba credentials yang ditemukan di service lain?

## Key Techniques

| Category | Description | Reference |
|----------|-------------|-----------|
| **3 Attack Vectors** | Vulnerable versions, misconfigurations, sensitive info | [enumeration-framework.md](./references/enumeration-framework.md) |
| **Web Attacks** | SQLi, LFI→RCE, CMDi, file upload bypass | [web-attacks.md](./references/web-attacks.md) |
| **Buffer Overflow** | 7-step x86 Windows BOF methodology | [buffer-overflow.md](./references/buffer-overflow.md) |
| **Linux Privesc** | sudo, SUID, capabilities, cron, creds, kernel | [linux-privesc.md](./references/linux-privesc.md) |
| **Windows Privesc** | Token abuse, service misconfig, AlwaysInstallElevated | [windows-privesc.md](./references/windows-privesc.md) |
| **AD Attack Chain** | BloodHound, Kerberoast, ADCS, delegation, DCSync | [ad-attack-chain.md](./references/ad-attack-chain.md) |
| **Pivoting** | Ligolo-ng, Chisel, SSH tunneling, socat | [pivoting.md](./references/pivoting.md) |
| **Password Cracking** | Hashcat layered strategy, rules, modes | [password-cracking.md](./references/password-cracking.md) |
| **Exam Strategy** | 23h45m time plan, reporting, checklist | [exam-strategy.md](./references/exam-strategy.md) |

## Reference Documentation

| File | Description |
|------|-------------|
| [exam-architecture.md](./references/exam-architecture.md) | Scoring, passing combinations, tool restrictions |
| [enumeration-framework.md](./references/enumeration-framework.md) | Nmap workflow, 3 attack vectors, service checklists |
| [web-attacks.md](./references/web-attacks.md) | SQLi, LFI, CMDi, file upload methodology |
| [buffer-overflow.md](./references/buffer-overflow.md) | 7-step x86 BOF exploitation |
| [linux-privesc.md](./references/linux-privesc.md) | 7 Linux privesc vectors |
| [windows-privesc.md](./references/windows-privesc.md) | 6 Windows privesc vectors |
| [ad-attack-chain.md](./references/ad-attack-chain.md) | Full AD attack chain from enumeration to DCSync |
| [pivoting.md](./references/pivoting.md) | Ligolo-ng, Chisel, SSH tunneling |
| [password-cracking.md](./references/password-cracking.md) | Hashcat strategies and modes |
| [exam-strategy.md](./references/exam-strategy.md) | Time management, reporting, checklist |
| [referensi.md](./references/referensi.md) | 145+ external resources |

## Gotchas

1. **Metasploit hanya untuk SATU machine**: Gunakan Metasploit hanya pada satu target. Untuk target lain, gunakan manual exploit atau searchsploit PoC yang diadaptasi. Auxiliary modules (scanner, fuzzer) tidak dihitung — gunakan bebas.
2. **SQLMap dilarang**: Manual SQLi adalah keharusan. Latih UNION-based, blind, dan time-based injection tanpa automation tools.
3. **Screenshot wajib dari terminal interaktif**: Screenshot lewat web shell atau RDP tidak diterima. Semua bukti harus dari command line dengan IP + hostname + flag di frame sama.
4. **AD set bukan berarti ADCS selalu ada**: Jangan asumsi ADCS aktif. Prioritaskan BloodHound mapping sebelum mengejar specific attack path.
5. **Kernel exploit = LAST RESORT**: Kernel exploit bisa crash target dan menghabiskan revert. Selalu cek sudo, SUID, capabilities, cron, dan credential hunting dulu.
6. **Report adalah 50% nilai**: Reproducibility adalah kunci. Screenshot setiap langkah, sertakan exact commands dan output. Report yang buruk = fail meskipun compromise semua sistem.

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Scoring, passing, and exam restrictions | [exam-architecture.md](./references/exam-architecture.md) |
| Enumeration framework and attack vectors | [enumeration-framework.md](./references/enumeration-framework.md) |
| SQLi, LFI, CMDi techniques | [web-attacks.md](./references/web-attacks.md) |
| Buffer overflow 7-step workflow | [buffer-overflow.md](./references/buffer-overflow.md) |
| Linux privilege escalation | [linux-privesc.md](./references/linux-privesc.md) |
| Windows privilege escalation | [windows-privesc.md](./references/windows-privesc.md) |
| Active Directory attack chain | [ad-attack-chain.md](./references/ad-attack-chain.md) |
| Pivoting and tunneling setup | [pivoting.md](./references/pivoting.md) |
| Password cracking with hashcat | [password-cracking.md](./references/password-cracking.md) |
| Exam strategy, time plan, and reporting | [exam-strategy.md](./references/exam-strategy.md) |
| 145+ external OSCP resources | [referensi.md](./references/referensi.md) |

## License

MIT
