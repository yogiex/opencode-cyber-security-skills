---
name: "Overview & Exam Structure"
description: "OSDA exam structure, scoring, environment, time management, and comparison with OSIR/OSTH."
tags: [osda, exam, scoring, environment, time-management, offsec]
---

# Overview & Exam Structure

## Apa Itu SOC-200 / OSDA?

SOC-200 (Security Operations and Defensive Analysis) adalah sertifikasi defensive dari OffSec yang mengajarkan **detection, analysis, dan incident investigation** menggunakan SIEM. OSDA fokus pada bagaimana seorang SOC analyst mendeteksi dan merekonstruksi serangan dari log.

OSDA adalah sertifikasi **100% praktikal** — Anda diberi logs pre-recorded di Elastic SIEM + OSQuery, dan harus mengidentifikasi serta mendokumentasikan attacker actions di 10 phases.

### Perbedaan OSDA vs OSIR vs OSTH

| Aspek | OSDA (SOC-200) | OSIR (IR-200) | OSTH (TH-200) |
|-------|----------------|---------------|---------------|
| **Level** | 200 (foundational) | 200 | 200 |
| **Fokus** | Detection & log analysis | Incident response process | Proactive threat hunting |
| **Durasi exam** | 23h45m | 23h45m | 23h45m |
| **Report window** | 24 jam | 24 jam | 24 jam |
| **SIEM tool** | ELK Stack (Kibana + KQL) | ELK Stack | ELK Stack |
| **Phases** | 10 phases | Multiple scenarios | Multiple hunts |
| **Approach** | Reactive — detect attacker actions | Reactive — respond to incidents | Proactive — hunt for threats |
| **Cert expires** | No (does not expire) | No | No |
| **Passing** | 75/100 | 70/100 | 70/100 |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Durasi exam** | 23 jam 45 menit |
| **Report deadline** | 24 jam setelah exam selesai |
| **Total phases** | 10 phases |
| **Points per phase** | 10 points (varying flags per phase) |
| **Passing score** | 75/100 |
| **Format laporan** | PDF atau DOCX — structured report |
| **Upload portal** | OffSec Learning Library |

### Exam Environment

- **Proctoring**: Live proctor via webcam (screen share + room scan)
- **VPN**: Isolated OffSec VPN network — corporate network simulation
- **SIEM**: ELK Stack (Elasticsearch + Kibana) dengan pre-recorded logs
- **Tools**: Kibana (KQL), OSQuery via ELK integration
- **No direct login**: Anda TIDAK bisa login ke machines — analisis hanya dari SIEM
- **Log sources**: Windows Event Log, Sysmon, PowerShell logs, Linux auditd, syslog, network logs
- **13 boxes**: ~15,000 log messages per 10-minute phase window
- **Open book**: Semua sumber kecuali AI chatbots dan LLMs
- **Attacks**: Mostly in-memory — tidak selalu ada dropped binaries

### 24h Time Management

```
Phase 1-3 (0-6 jam):
  - Mulai dengan dashboards + pre-built alerts di Kibana
  - Catat starting time setiap phase
  - Broad query dulu, lalu narrow down dengan process IDs
  - Screenshot setiap query + result
  - Dokumentasi langsung di report template

Break (30-60 menit): makan, stretching

Phase 4-7 (7-13 jam):
  - Attacks semakin stealthy — perhatikan in-memory execution
  - Gunakan OSQuery untuk verifikasi aktif
  - Cross-reference Windows logs + Sysmon + PowerShell
  - Jika stuck: hapus filter, broaden query, atau pindah phase dulu

Break (30-60 menit): istirahat mata, coffee

Phase 8-10 (14-20 jam):
  - Phases terakhir biasanya paling kompleks
  - Perhatikan chain antar machines — lateral movement links phases
  - Verifikasi semua findings masih konsisten

Report Writing (20-24 jam):
  - Compile notes + screenshots → coherent attack story
  - Per-phase summary → attacker IP, victim, TTPs, IOCs
  - Submit sebelum deadline 24 jam
```

## Best Practices

- Prioritaskan broad queries dulu, narrow down dengan process IDs
- Dokumentasi di report template selama exam, jangan nanti
- OSQuery hanya untuk verifikasi — KQL adalah primary weapon
- Jika stuck >30 menit: hapus filter, broaden, atau pindah phase
