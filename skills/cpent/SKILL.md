---
name: cpent
description: EC-Council CPENT (Certified Penetration Testing Professional) — mindset, metodologi, dan strategi komprehensif untuk CPENT exam mencakup 14 modul inti, binary exploitation 32/64-bit, IoT/OT/SCADA, double pivoting, report writing, dan LPT Master pathway.
license: MIT
compatibility: opencode
metadata:
  audience: penetration-testers
  workflow: exploitation
  source: ec-council-cpent
  standard: cpent
  year: "2026"
---

# CPENT — Metodologi & Pola Pikir

## Prerequisites

- CEH or equivalent penetration testing foundation
- OSCP-level exploitation skills
- Binary exploitation basics (x86 assembly, stack concepts)
- Web application security fundamentals
- Basic networking and pivoting concepts

## Quick Start Workflow

```bash
# 1. Parallel enumeration (30 menit pertama)
nmap -Pn -p- --min-rate 10000 -T4 $TARGETS -oA nmap/allports
nmap -Pn -sC -sV -p $(ports) $TARGET -oA nmap/services

# 2. Automated scanning (all tools allowed)
sqlmap -u "$URL" --batch --random-agent --level 3 --risk 2

# 3. Web app → initial access → pivot
ffuf -w $WORDLIST -u "$URL/FUZZ"
# Get shell, check interfaces, deploy pivot agent

# 4. Double pivot (core CPENT skill)
# Pivot 1 → subnet A → host dual-home → Pivot 2 → subnet B

# 5. Document every step with screenshots
```

## CPENT Mindset — "Penetrate Deeper"

CPENT berbeda dari OSCP. OSCP mengajarkan "Try Harder". CPENT mengajarkan **"Penetrate Deeper"** — setelah dapat satu machine, bagaimana masuk ke network yang lebih dalam, melewati firewall, pivoting multiple hops.

### Golden Rules

1. **CPENT is a marathon** — 24 jam. Jaga energi, makan, minum.
2. **Pivoting is the core skill** — seberapa dalam Anda bisa menembus.
3. **Double pivot mindset** — setiap shell baru, cek interfaces.
4. **Document during the exam** — report adalah 30% dari nilai.
5. **Automation is allowed** — sqlmap, Metasploit, Burp Pro semua boleh.
6. **Binary exploitation 64-bit** — pelajari calling convention x64.
7. **IoT & SCADA are different beasts** — industrial protocols behave differently.

### Pattern Recognition

- Web app frontend → SQLi → shell → pivoting → internal services
- IoT device → default creds → exposed debug interface → internal network
- SCADA/PLC → Modbus enumeration → insecure protocol → control system
- Windows AD → SMB → PtH → lateral movement → DC
- Linux → SUID abuse → root → SSH key → pivot

## Key Techniques

| Category | Description | Reference |
|----------|-------------|-----------|
| **Exam Structure** | Scoring, format, time management | [exam-structure.md](./references/exam-structure.md) |
| **14 Modules** | Full course syllabus breakdown | [modules-overview.md](./references/modules-overview.md) |
| **Windows Attacks** | PtH, DCSync, Kerberos, SMB relay | [windows-attacks.md](./references/windows-attacks.md) |
| **Linux Attacks** | Kernel exploits, cron, LD_PRELOAD | [linux-attacks.md](./references/linux-attacks.md) |
| **Web Exploitation** | sqlmap, Burp, XSS, SSRF, CMDi | [web-exploitation.md](./references/web-exploitation.md) |
| **Binary Exploit** | x86 stack overflow, x64 ROP chains | [binary-exploitation.md](./references/binary-exploitation.md) |
| **Wireless/IoT/SCADA** | WPA cracking, Modbus, PLC | [wireless-iot-scada.md](./references/wireless-iot-scada.md) |
| **Pivoting & Report** | Double pivot, EC-Council report format | [pivoting-report.md](./references/pivoting-report.md) |
| **Exam Zones** | Standalone, complex, double pivot, IoT | [exam-zones.md](./references/exam-zones.md) |
| **Tools Matrix** | Essential tools & static binaries | [tools-matrix.md](./references/tools-matrix.md) |

## Reference Documentation

| File | Description |
|------|-------------|
| [exam-structure.md](./references/exam-structure.md) | Scoring, passing, time management |
| [modules-overview.md](./references/modules-overview.md) | 14 CPENT modules deep-dive |
| [windows-attacks.md](./references/windows-attacks.md) | PtH, DCSync, Kerberos, SMB relay |
| [linux-attacks.md](./references/linux-attacks.md) | Kernel exploits, persistence |
| [web-exploitation.md](./references/web-exploitation.md) | sqlmap, Burp, all tools allowed |
| [binary-exploitation.md](./references/binary-exploitation.md) | x86 stack overflow, x64 ROP |
| [wireless-iot-scada.md](./references/wireless-iot-scada.md) | WPA, IoT, Modbus, PLC |
| [pivoting-report.md](./references/pivoting-report.md) | Double pivot + EC-Council report format |
| [exam-zones.md](./references/exam-zones.md) | Zone strategies + checklist |
| [tools-matrix.md](./references/tools-matrix.md) | Essential tools, static binaries, wordlists |
| [referensi.md](./references/referensi.md) | External CPENT resources |

## Gotchas

1. **CPENT vs OSCP mindset berbeda**: OSCP batasi Metasploit, CPENT malah encourage. Tapi tetap harus paham manual exploitation — jangan hanya andalkan automation.
2. **Double pivot bukan single pivot × 2**: Dua lapis jaringan dengan host dual-home. Ligolo-ng TUN interface sangat membantu karena semua tool bisa langsung jalan.
3. **Binary exploitation 64-bit ≠ 32-bit**: Calling convention berbeda (rcx, rdx, r8, r9). ROP chains diperlukan untuk bypass NX/DEP. Siapkan template exploit untuk kedua arsitektur.
4. **Report adalah 30% nilai**: EC-Council sangat ketat tentang bukti screenshot. Setiap screenshot harus capture IP + hostname + flag. Submit dalam 7 hari — jangan ditunda.
5. **IoT/SCADA protokol non-standard**: Modbus (port 502), DNP3 (port 20000), BACnet (port 47808). Pelajari protocol dasar sebelum exam.
6. **Exam environment bisa berubah per cycle**: Jumlah soal dan zonasi bisa berbeda. Fleksibel dan adaptif adalah kunci.

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Scoring, format, and time plan | [exam-structure.md](./references/exam-structure.md) |
| Module-by-module syllabus breakdown | [modules-overview.md](./references/modules-overview.md) |
| Windows AD attacks and exploitation | [windows-attacks.md](./references/windows-attacks.md) |
| Linux kernel and privilege escalation | [linux-attacks.md](./references/linux-attacks.md) |
| Web app exploitation with automation | [web-exploitation.md](./references/web-exploitation.md) |
| Binary exploitation (x86 and x64) | [binary-exploitation.md](./references/binary-exploitation.md) |
| Wireless, IoT, and SCADA attacks | [wireless-iot-scada.md](./references/wireless-iot-scada.md) |
| Double pivoting and report writing | [pivoting-report.md](./references/pivoting-report.md) |
| Zone-specific exam strategies | [exam-zones.md](./references/exam-zones.md) |
| Essential tools and wordlists | [tools-matrix.md](./references/tools-matrix.md) |
| External CPENT resources | [referensi.md](./references/referensi.md) |

## License

MIT
