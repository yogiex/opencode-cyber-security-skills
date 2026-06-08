---
name: offsec-th-200
description: OffSec TH-200 / OSTH (OffSec Threat Hunter) — foundational threat hunting covering proactive threat detection, behavioral analysis, threat actor profiling, Splunk SIEM analysis with SPL, CrowdStrike Falcon endpoint hunting, Suricata IDS/IPS, hypothesis-driven hunting methodologies (PEAK, SEARCH), MITRE ATT&CK mapping, ransomware & APT case studies, cyber threat intelligence integration, and professional hunt reporting.
license: MIT
compatibility: opencode
metadata:
  audience: threat-hunters
  workflow: detection
  source: offsec-th-200
  standard: osth
  year: "2026"
---

# TH-200 — Foundational Threat Hunting (OSTH)

TH-200 (OSTH) adalah sertifikasi threat hunting OffSec — **proactive threat detection** mencari adversary sebelum mereka menyebabkan damage. Berbeda dengan OSDA (reaktif, alert-driven) dan OSIR (incident response), OSTH fokus pada hypothesis-driven hunting menggunakan Splunk, CrowdStrike Falcon, dan Suricata. 8 jam proctored + 24h report window.

| Aspek | OSTH (TH-200) | OSDA (SOC-200) | OSIR (IR-200) |
|-------|---------------|----------------|---------------|
| **Fokus** | Proactive threat hunting | Detection & log analysis | Incident response & forensics |
| **SIEM** | Splunk (SPL) | ELK (KQL) | Splunk (SPL) |
| **Endpoint** | CrowdStrike Falcon (CQL) | OSQuery | Autopsy + Volatility |
| **Network** | Suricata IDS/IPS | Tidak | Tidak |
| **Pendekatan** | Proaktif — hypothesis-driven | Reaktif — alert-driven | Reaktif — incident-driven |
| **Cert expires** | 3 tahun | Tidak | 3 tahun |
| **Passing** | 50/70 | 75/100 | 50/70 |

## Scoring & Exam Environment

7 exercises × 10 pts = **70 pts**. Passing: **50/70**. Exam: Splunk Enterprise, CrowdStrike Falcon console, Suricata IDS logs, network PCAP. Input: Threat intelligence report (IOC list + TTP description + APT profile). Output: Hunt Narrative (timeline + IOC table + impacted systems + evidence). Open book (no AI chatbots).

## 8h Time Management

```
Hour 0-0:30: Read threat intel report, map IOCs to ATT&CK, identify critical systems
Hour 0:30-2: Broad Splunk queries — IOC matching, initial access, timeline skeleton
Hour 2-4: Deep hunt — Network (Suricata/DNS/proxy) + Endpoint (process/registry/services)
Hour 4-5: Hypothesis-driven hunting — refine hypotheses, hunt for unknown IoCs
Hour 5-6: CrowdStrike Falcon — CQL queries, process tree, compromised hosts
Hour 6-7: Complete all 7 exercises — verify with MD5, screenshot everything
Hour 7-8: Final review — verify answers, organize evidence, start report draft
Post-Exam (24h): Complete professional hunt report, submit via OffSec portal
```

## How to Use This Skill

| When you need to... | Load this file |
|---------------------|----------------|
| Understand hunting mindset, PEAK, SEARCH, hypothesis development | `references/th-mindset.md` |
| Review all 8 modules with threat actor landscape | `references/modules-overview.md` |
| Run SPL queries for hunting (all phases) | `references/splunk-hunting.md` |
| Use CrowdStrike Falcon CQL for endpoint hunting | `references/crowdstrike-cql.md` |
| Hunt with Suricata, Zeek, and network data | `references/network-hunting.md` |
| Identify Sysmon and Windows Event Log artifacts | `references/endpoint-hunting.md` |
| Integrate threat intelligence into Splunk queries | `references/ti-integration.md` |
| Study ransomware/APT attack chains and hunt methods | `references/case-studies.md` |
| Use the hunt report template for exam report | `assets/report-template.md` |
| Run copy-paste ready SPL queries | `scripts/spl-queries.spl` |

## Gotchas

- **OSTH ≠ OSIR/OSDA**: OSTH menggunakan Splunk (bukan ELK) seperti OSIR, tapi fokus pada proactive hunting, bukan incident response. Juga menggunakan CrowdStrike Falcon CQL yang tidak ada di OSIR.
- **Threat intel report is key**: Di awal exam, Anda mendapat threat intel report — baca dengan teliti. Semua jawaban exercises berdasarkan report ini.
- **Three data sources**: OSTH exam mewajibkan korelasi antara Splunk (breadth), CrowdStrike (depth), dan Suricata (network). Jangan hanya menggunakan satu sumber.
- **Report weight**: Report = 70 points (bukan 30 seperti OSIR). Screenshot setiap query + timestamp.
- **CQL ≠ SPL**: Syntax CQL mirip Splunk tapi tidak identik. Perhatikan perbedaan operator (`IN`, `LIKE`) dan field naming (CamelCase).
- **Hypotheses evolve**: Hipotesis awal hampir selalu berubah setelah menemukan bukti. Jangan terpaku pada hipotesis awal.
- **Cert expires**: OSTH hanya valid 3 tahun, recertification diperlukan.

## Quick Reference — Key Exam Queries

```spl
/* Broad IOC matching */
index=* | search src_ip IN ("<ip>") OR dest_ip IN ("<ip>") OR query IN ("<domain>")

/* Beaconing detection */
index=proxy | stats count, dc(dest_ip) as UniqueDests by src_ip
| where count > 100 AND UniqueDests < 3

/* Unusual parent-child */
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(winword|excel|powerpnt|outlook)")
  AND match(Image, "(?i)(powershell|wscript|cscript|cmd)")
```

```cql
/* Process creation hunting */
event_simpleName=ProcessRollup2 FileName="powershell.exe"
| table ComputerName, UserName, CommandLine, ParentBaseFileName

/* External connections */
event_simpleName=NetworkConnectIP4
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
| stats count by ComputerName, RemoteAddressIP4, RemotePort
```

## License

MIT — see LICENSE file in repository root.
