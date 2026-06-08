---
name: offsec-soc-200
description: OffSec SOC-200 / OSDA (OffSec Defense Analyst) — security operations and defensive analysis. Covers SOC operations, Windows & Linux endpoint detection, SIEM analysis with ELK/Kibana/KQL, attacker methodology (Kill Chain, MITRE ATT&CK), Windows Event Log & Sysmon analysis, Active Directory threat detection, network detections, and incident investigation.
license: MIT
compatibility: opencode
metadata:
  audience: soc-analysts
  workflow: detection
  source: offsec-soc-200
  standard: osda
  year: "2026"
---

# SOC-200 — Security Operations & Defensive Analysis (OSDA)

SOC-200 (OSDA) adalah sertifikasi defensive OffSec yang mengajarkan **detection, analysis, dan incident investigation** menggunakan ELK SIEM. Fokus pada merekonstruksi serangan dari log — memahami bagaimana attacker bekerja untuk mendeteksi mereka dari behavioral signatures.

## How to Use This Skill

| When you need to... | Load this file |
|---------------------|----------------|
| Understand exam structure, scoring, and environment | `references/overview-exam.md` |
| Deep-dive into all 19 modules with detection patterns | `references/modules-overview.md` |
| Look up Windows Event IDs, Sysmon, or PowerShell logging | `references/windows-event-logs.md` |
| Write KQL queries or use OSQuery | `references/elk-kql.md` |
| Strategy for challenge labs and exam | `references/challenge-labs.md` |
| Report template for exam submission | `assets/report-template.md` |
| Pre-exam / during-exam / post-exam checklist | `assets/pre-exam-checklist.md` |
| Reusable KQL detection queries | `scripts/common-detection-queries.kql` |
| Complete list of 110+ external references | `references/referensi.md` |

## SOC-200 Mindset

### Golden Rules OSDA

1. **Logs don't lie — but they are incomplete** — Jika ada gap 30 menit tanpa logs, mungkin logs dihapus atau ada teknik evasion. Jangan paksakan koneksi yang tidak ada.

2. **Timeline is NOT linear in OSDA** — Attacker actions bisa muncul out-of-order karena revert/reset. Urutkan report berdasarkan **phase** dan **logical attack flow**, bukan timestamp.

3. **Process IDs are your breadcrumbs** — Follow PID chain untuk merekonstruksi apa yang terjadi.

4. **In-memory attacks are invisible to disk scans** — Jangan cari executable mencurigakan — cari **LOLBINs**, **PowerShell**, **WMI**, **service creation** patterns.

5. **The report is 50% of your grade** — Bisa detect semua phases tapi report berantakan = fail. Ceritakan attack story yang koheren.

6. **Success vs Attempt** — Hanya karena attacker menjalankan tool, belum tentu berhasil. Cek apakah event yang diharapkan benar-benar terjadi.

7. **KQL is your primary weapon** — Kuasai Kibana Query Language. Kecepatan query = kecepatan detection.

8. **OSQuery is your verification tool** — Gunakan OSQuery untuk memverifikasi state aktif yang tidak terekam di logs.

### 3 Pertanyaan Kunci Saat Stuck

1. **"What user ran this?"** — user.name, related.user, winlog.user.name — bandingkan ketiganya.
2. **"Did it succeed?"** — Cek event setelahnya: service terinstall? process baru? authentication berhasil?
3. **"What am I not seeing?"** — Apakah ada log source yang mati? Gap waktu? Mungkin attacker menghapus logs.

### Pattern Recognition untuk OSDA

- **Initial access** → Web server: command injection, file upload → IIS logs + event 4688
- **Phishing** → Office macro → PowerShell encoded command → event 4104
- **Privilege escalation** → Service creation (7045) or UAC bypass → 4672 (special priv)
- **Persistence** → Registry Run keys (Sysmon 13), Scheduled Tasks (4698), Services (7045)
- **Credential access** → LSASS access via Sysmon 10, Mimikatz, DCSync
- **Lateral movement** → 4624 Type 3 logons, 4648 explicit creds, service install on remote host
- **Persistence (AD)** → Golden Ticket via 4768 with unusual encryption, group modification 4728

## Gotchas

- Timelines are NOT linear — urutkan report berdasarkan phase, bukan timestamp
- 50% grade dari report — detect semua phases tapi report berantakan = fail
- In-memory attacks tidak terlihat di disk — cari LOLBINs, PowerShell, WMI patterns
- Success vs Attempt — attacker run tool belum tentu berhasil, verify via next event
- OSQuery untuk active verification, KQL untuk primary detection
- Jangan over-rely pada pre-built alerts — ada rabbit holes, verify manual

## Quick Reference

### Key Event IDs

| ID | Event | Use Case |
|----|-------|----------|
| 4624 | Successful logon | Cek Logon Type (3=network, 10=RDP) |
| 4625 | Failed logon | Brute force detection |
| 4688 | Process creation | Follow PID chain |
| 7045 | Service installed | Persistence / lateral movement |
| 4104 | PowerShell ScriptBlock | Deobfuscated script content |
| 4769 | Kerberos service ticket | Kerberoasting (RC4 0x17) |
| 1102 | Security log cleared | Almost always malicious |

### Basic KQL Patterns

```kql
event.code : 4625 AND source.ip : "192.168.1.100"
event.code : (7045 OR 4697)
process.command_line : *-enc*
event.code : 4104
```

### Detection Workflow

```
Broad search → add time range → host filter → event.code filter
→ column layout (command_line, user.name) → follow PID chain
→ cross-source verification → document
```
