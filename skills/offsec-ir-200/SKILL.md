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

## Decision Frame

1. **Contain dulu atau akuisisi bukti dulu?** — Jika masih ada eksfiltrasi/enkripsi aktif, isolasi mendahului forensik. Jika serangan sudah berhenti, akuisisi dulu agar bukti tidak berubah. Tulis alasan pilihanmu di report.
2. **Poin ini ada di Phase 1 atau Phase 2?** — 4×10 (Splunk) + 2×15 (forensik). Jangan habiskan 5 jam di Splunk lalu kehabisan waktu untuk disk/memory yang nilainya lebih besar per soal.
3. **Sudah aman di ambang lulus?** — Lulus 50/70. Jalur minimal: 4/4 Phase 1 + 1/2 Phase 2. Jika satu soal Phase 1 macet, pindah.
4. **Ini bagian insiden atau noise?** — Korelasikan waktu, host, dan user. Aktivitas administratif sah sering terlihat seperti serangan; sebutkan dasar pengecualiannya.
5. **Bukti ini bisa direplikasi?** — Query SPL, perintah, dan output harus ada di report. Poin hanya diberikan untuk temuan yang terdokumentasi lengkap.

> Fakta ujian diverifikasi di [docs/CERTIFICATION-FACTS.md](../../docs/CERTIFICATION-FACTS.md) (2026-11-07).

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
- **Report weight**: Tidak ada poin report terpisah. Phase 1 (4 task × 10) dan Phase 2 (2 task × 15) dinilai dari jawaban **dan** kelengkapan dokumentasi; total 70, lulus 50. Dokumentasi buruk mengurangi poin task.
- **Autopsy ingest time**: Ingest modules bisa memakan 20-30 menit. Jangan tunggu pasif — kerjakan Phase 1 sambil menunggu.
- **Volatility 3 ≠ Volatility 2**: Volatility 3 tidak memerlukan profile parameter. Cukup `windows.info` untuk identifikasi. Plugin names juga berbeda (gunakan `windows.pslist`, bukan `pslist`).
- **Cert expires**: OSIR termasuk sertifikasi OffSec yang **kedaluwarsa** (bersama OSTH, OSCP+, OSCC-SEC, OSCC-SJD) dan perlu recertification; OSDA tidak.
- **Containment specificity**: Di report, containment strategy harus spesifik — "block IP 10.0.0.5 at firewall ACL", bukan "block the attacker".
- **Pass paths**: Ambang 50/70. Contoh: 4/4 Phase 1 + 1/2 Phase 2 = 55; atau 3/4 Phase 1 + 2/2 Phase 2 = 60.

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
