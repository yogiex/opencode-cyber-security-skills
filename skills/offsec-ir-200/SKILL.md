---
name: offsec-ir-200
description: OffSec IR-200 / OSIR (OffSec Incident Responder) — foundational incident response covering full IR lifecycle (NIST 800-61r2), Splunk SIEM analysis with SPL, digital forensics (Autopsy, Volatility 3, FTK Imager), malware triage with YARA, containment/eradication/recovery strategies, incident communication plans, and post-mortem reporting.
license: MIT
compatibility: opencode
metadata:
  audience: incident-responders
  workflow: detection
  source: offsec-ir-200
  standard: osir
  year: "2026"
---

# IR-200 — Foundational Incident Response (OSIR)

IR-200 (Foundational Incident Response) adalah sertifikasi OffSec yang mengajarkan **full IR lifecycle** — detection, containment, eradication, recovery, hingga post-mortem reporting, termasuk digital forensics (disk + memory) dan incident management. OSIR adalah sertifikasi 100% praktikal: 8 jam proctored lab + 24 jam report window.

| Aspek | OSIR (IR-200) | OSDA (SOC-200) | OSTH (TH-200) |
|-------|---------------|----------------|---------------|
| **Fokus** | Full IR lifecycle, DFIR | Detection & log analysis | Proactive threat hunting |
| **SIEM** | Splunk (SPL) | ELK (KQL) | Splunk (SPL) |
| **Forensics** | Autopsy + Volatility 3 | Tidak | Tidak |
| **Durasi exam** | 8 jam + 24h report | 23h45m | 23h45m |
| **Passing** | 50/70 | 75/100 | 70/100 |

## Scoring & Exam Environment

Phase 1 (Splunk Log Analysis): 4 exercises × 10 pts = **40 pts**. Phase 2 (Disk & Memory Forensics): 2 exercises × 15 pts = **30 pts**. Total: **70 pts**. Passing: **50/70**. Cert valid 3 tahun.

Pass paths: 4/4 Phase 1 + 1/2 Phase 2 (50 pts) ATAU 3/4 Phase 1 + 2/2 Phase 2 (60 pts).

Tools: Splunk Enterprise, Autopsy, Volatility 3, FTK Imager, YARA, strings, PE analysis.

## 8h Time Management Strategy

```
Hour 0-1: Initial triage (Phase 1) — Review Splunk dashboards, identify initial access
Hour 1-3: Deep Splunk analysis — Follow attack chain, answer 2-3 exercises, document IoCs
Hour 3-4: Transition — Load disk in Autopsy, configure ingest, start keyword analysis
Hour 4-6: Disk & Memory Forensics (Phase 2) — Autopsy filesystem, Volatility pslist/malfind/netscan
Hour 6-7: Complete Phase 2 — YARA rule writing, chain of custody, extract flags
Hour 7-8: Final review — Verify all 6 answers, collect screenshots, start report draft
Post-Exam (24h): Complete IR report — executive summary, timeline, containment strategy
```

## How to Use This Skill

| When you need to... | Load this file |
|---------------------|----------------|
| Understand NIST lifecycle, CSIRT roles, severity | `references/ir-lifecycle.md` |
| Review all 13 modules with case studies | `references/modules-overview.md` |
| Run SPL queries for detection / investigation | `references/splunk-siem.md` |
| Perform disk/memory forensics (Autopsy, Volatility) | `references/digital-forensics.md` |
| Plan containment, eradication, and recovery | `references/containment-eradication-recovery.md` |
| Triage malware and write YARA rules | `references/malware-triage.md` |
| Structure post-mortem report and communication | `references/reporting.md` |
| Use incident communication templates | `assets/communication-template.md` |
| Run YARA rules on malware samples | `scripts/yara-rules.yara` |

## Gotchas

- **Splunk vs ELK**: OSIR pakai Splunk (SPL), bukan ELK (KQL) seperti OSDA. Jangan tertukar sintaks query.
- **Report weight**: Report adalah 30 dari 70 points — jangan fokus hanya pada technical analysis. Alokasikan waktu setelah exam untuk report.
- **Autopsy ingest time**: Ingest modules bisa memakan 20-30 menit. Jangan tunggu pasif — kerjakan Phase 1 sambil menunggu.
- **Volatility 3 ≠ Volatility 2**: Volatility 3 tidak memerlukan profile parameter. Cukup `windows.info` untuk identifikasi. Plugin names juga berbeda (gunakan `windows.pslist`, bukan `pslist`).
- **Cert expires**: OSIR hanya valid 3 tahun — perlu recertification, berbeda dengan OSDA yang tidak expire.
- **Containment specificity**: Di report, containment strategy harus spesifik — "block IP 10.0.0.5 at firewall ACL", bukan "block the attacker".
- **Pass paths**: Ada 2 cara lulus — kuasai Phase 1 (Splunk) hampir sempurna, lalu ambil 1 soal Phase 2. Atau 3/4 Phase 1 + 2/2 Phase 2.

## Quick Reference — Key Exam Commands

```bash
# Volatility 3 — memory forensics
vol -f memory.raw windows.info
vol -f memory.raw windows.pslist && vol -f memory.raw windows.psscan
vol -f memory.raw windows.malfind --dump
vol -f memory.raw windows.netscan

# Sleuth Kit — disk forensics
fls -r -o 2048 evidence.dd          # List files with deleted
icat -o 2048 evidence.dd <inode>    # Recover file

# YARA scan
yara -s /path/to/rules.yara suspicious.exe

# Malware triage
file suspicious.exe
strings suspicious.exe | grep -iE "http|https|cmd|powershell|C2"
```

```spl
# Critical SPL queries for Phase 1
index=windows sourcetype=WinEventLog:Security EventCode=4625
| stats count as FailedCount, dc(Account) as UniqueAccounts by src_ip
| where FailedCount > 20

index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| search NOT DestIp=10.* AND NOT DestIp=192.168.*
| stats count by ComputerName, DestIp, DestPort, Image
```

## License

MIT — see LICENSE file in repository root.
