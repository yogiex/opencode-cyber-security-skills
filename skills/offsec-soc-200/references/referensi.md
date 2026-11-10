---
name: "Referensi Lengkap"
description: "Kumpulan sumber eksternal untuk detection and defensive analyst: dokumentasi event Windows, ELK/KQL, MITRE ATT&CK, Sigma, dataset dan lab yang bisa dibangun sendiri, buku, dan komunitas teknis."
tags: [references, detection, windows, sysmon, elk, kql, mitre-attack, sigma, labs, books]
---

# Referensi Lengkap

Sumber di bawah dipilih untuk pekerjaan analisis: dokumentasi vendor, spesifikasi format, dataset, dan bahan lab. Tautan yang isinya soal atau strategi sertifikasi tidak dimasukkan — untuk pekerjaan, yang berguna adalah dokumentasi primer dan data yang bisa dipakai ulang.

## Dokumentasi kursus dan taksonomi

| # | Resource | URL |
|---|---|---|
| 1 | SOC-200 Course Page | https://www.offsec.com/courses/soc-200/ |
| 2 | SOC-200 Syllabus (PDF) | https://www.offsec.com/documentation/SOC-200-Syllabus.pdf |
| 3 | SOC-200 Course Overview (PDF) | https://assets.ctfassets.net/82ripq7fjls2/b5qRhY35iq5DcjtrqIupO/df320df830723040f37afce4603c5d65/soc-200-foundational-security-operations-and-defensive-analysis-osda-self-paced.pdf |

## Repositori GitHub

| # | Repository | Author | Description |
|---|---|---|---|
| 4 | Ilias1988/Hacking-Cheatsheets | Ilias1988 | Blue team log analysis cheatsheets |
| 5 | SwiftOnSecurity/sysmon-config | SwiftOnSecurity | Sysmon configuration template |
| 6 | olafhartong/sysmon-modular | olafhartong | Modular Sysmon configuration |
| 7 | sbousseaden/EVTX-ATTACK-SAMPLES | sbousseaden | Windows event log attack samples |
| 8 | huntresslabs/evtx | huntresslabs | EVTX parser for Python |
| 9 | SigmaHQ/sigma | SigmaHQ | Generic signature format for SIEM |

## Windows Event Log dan Sysmon

| # | Resource | URL |
|---|---|---|
| 10 | Ultimate Windows Security — Event ID Encyclopedia | https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/ |
| 11 | Microsoft — Windows Security Event ID Reference | https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/sentinel/windows-security-event-id-reference.md |
| 12 | EpicDetect — Event IDs Every SOC Analyst Should Know | https://epicdetect.io/blogs/windows-event-log-ids-soc-analysts |
| 13 | Microsoft — Sysmon Documentation | https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon |
| 14 | SwiftOnSecurity — Sysmon Config Guide | https://github.com/SwiftOnSecurity/sysmon-config |
| 15 | Microsoft — PowerShell Logging Documentation | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging |
| 16 | Microsoft — Advanced Audit Policy | https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/advanced-security-audit |
| 17 | Event ID 4688 — Command Line Auditing | https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688 |
| 18 | Event ID 4104 — Script Block Logging | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows |
| 19 | Sekoia — Event ID Detection Rules Reference | https://docs.sekoia.io/xdr/features/detect/built_in_detection_rules_eventids/ |
| 20 | MalAPI.io — Windows API to ATT&CK Mapping | https://malapi.io/ |

## Kibana, ELK, dan KQL

| # | Resource | URL |
|---|---|---|
| 21 | Elastic — Kibana Query Language Docs | https://www.elastic.co/guide/en/kibana/current/kuery-query.html |
| 22 | KQL Cheat Sheet | https://pulse.support/kb/kibana-query-language |
| 23 | KQL Cheat Sheet (Cheatography) | https://cheatography.com/thesujit/cheat-sheets/kibana-query-language-kql/ |
| 24 | Elastic — SIEM Detection Rules | https://www.elastic.co/guide/en/security/current/rules-ui-create.html |
| 25 | Elastic — OSQuery Integration | https://www.elastic.co/guide/en/kibana/current/osquery.html |
| 26 | HTB — Security Monitoring and SIEM Fundamentals | https://purplebyteone.gitbook.io/ |

## MITRE ATT&CK

| # | Resource | URL |
|---|---|---|
| 27 | MITRE ATT&CK Official | https://attack.mitre.org |
| 28 | MITRE ATT&CK Navigator | https://mitre-attack.github.io/attack-navigator/ |
| 29 | MITRE ATT&CK — Enterprise Matrix | https://attack.mitre.org/matrices/enterprise/ |
| 30 | MITRE ATT&CK — Detection | https://attack.mitre.org/docs/ATTACK_Detection_November_2020.pdf |
| 31 | CAR — Cyber Analytics Repository | https://car.mitre.org/ |
| 32 | Atomic Red Team | https://github.com/redcanaryco/atomic-red-team |

## Analisis SOC dan blue team

| # | Resource | URL |
|---|---|---|
| 33 | SOC-CMM — SOC Maturity Model | https://www.soc-cmm.com |
| 34 | SANS — SOC Survey Report | https://www.sans.org/white-papers/soc-survey/ |
| 35 | NIST SP 800-61 Rev 2 (IR Guide) | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |
| 36 | NIST SP 800-92 (Log Management) | https://csrc.nist.gov/pubs/sp/800/92 |
| 37 | SANS — Cyber Kill Chain | https://www.sans.org/white-papers/cyber-kill-chain/ |
| 38 | PICERL Model — SANS IR Framework | https://www.sans.org/white-papers/incident-handlers-handbook/ |

## Detection engineering

| # | Resource | URL |
|---|---|---|
| 39 | Sigma — Generic Signature Format | https://github.com/SigmaHQ/sigma |
| 40 | SIGMA — Rules Repository | https://github.com/SigmaHQ/sigma/tree/master/rules |
| 41 | palantir/windows-event-forwarding | https://github.com/palantir/windows-event-forwarding |
| 42 | Detection Engineering — DetectionLab | https://github.com/clong/DetectionLab |
| 43 | HELK — The Hunting ELK | https://github.com/Cyb3rWard0g/HELK |
| 44 | Velociraptor — DFIR Tooling | https://github.com/Velocidex/velociraptor |
| 45 | Hayabusa — Event Log Fast Forensics | https://github.com/Yamato-Security/hayabusa |

## LOLBINs dan living-off-the-land

| # | Resource | URL |
|---|---|---|
| 46 | LOLBAS — Living Off the Land Binaries | https://lolbas-project.github.io |
| 47 | GTFOBins — Unix Binaries | https://gtfobins.github.io |
| 48 | Red Canary — LOLBIN Detection | https://redcanary.com/threat-detection-theory/lolbins/ |
| 49 | API Of LOLS — LOLBIN API reference | https://lolbas-project.github.io/api/ |
| 50 | Oddvar Moe — PowerShell LOLBINs | https://oddvar.moe/ |

## Lab, dataset, dan latihan

| # | Resource | URL |
|---|---|---|
| 51 | Hack The Box — SOC Analyst Track | https://www.hackthebox.com |
| 52 | BTLO (Blue Team Labs Online) | https://blueteamlabs.online |
| 53 | TryHackMe — SOC Level 1 dan 2 Paths | https://tryhackme.com |
| 54 | LetsDefend | https://letsdefend.io |
| 55 | CyberDefenders | https://cyberdefenders.org |
| 56 | DetectionLab | https://github.com/clong/DetectionLab |
| 57 | HELK — Hunting ELK Stack | https://github.com/Cyb3rWard0g/HELK |
| 58 | Elastic — Free SIEM Training | https://www.elastic.co/training/ |

## Buku

| # | Book | Author |
|---|---|---|
| 59 | Blue Team Handbook: Incident Response Edition (3rd Ed.) | Don Murdoch |
| 60 | Blue Team Field Manual (BTFM) | Alan White dan Ben Clark |
| 61 | The Practice of Network Security Monitoring | Richard Bejtlich |
| 62 | Applied Incident Response | Steve Anson |
| 63 | Operationalizing Threat Intelligence | Kyle Neuman |
| 64 | Hunting Cyber Criminals | Vinny Troia |
| 65 | Windows Internals, Part 1 dan 2 (7th Ed.) | Pavel Yosifovich et al. |
| 66 | Practical Malware Analysis | Michael Sikorski dan Andrew Honig |
| 67 | The Art of Memory Forensics | Michael Ligh et al. |
| 68 | Investigating Windows Systems | Harlan Carvey |
| 69 | Digital Forensics with Kali Linux | Shiva Parasram |
| 70 | Mastering Windows Security and Hardening | Mark Dunkerley |
| 71 | Practical Binary Analysis | Dennis Andriesse |
| 72 | The Hacker Playbook 3 | Peter Kim |
| 73 | Red Team Field Manual v2 | Ben Clark dan Nick Downer |
| 74 | Attacking Network Protocols | James Forshaw |

## Kanal teknis

| # | Channel | Focus | URL |
|---|---|---|---|
| 75 | 0xdf | Detection methodology | https://www.youtube.com/@0xdf |
| 76 | John Hammond | Malware analysis, detection | https://www.youtube.com/@JohnHammond010 |

## Sumber lain

| # | Resource | URL |
|---|---|---|
| 77 | Windows Event Log — Advanced Audit Policy | https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/advanced-security-auditing |
| 78 | Windows Security Log Events (Microsoft Archives) | https://www.microsoft.com/en-us/download/details.aspx?id=50034 |
| 79 | Elastic Common Schema (ECS) | https://www.elastic.co/guide/en/ecs/current/index.html |
| 80 | OSQuery Schema Documentation | https://osquery.io/schema/ |
| 81 | MISP — Threat Sharing | https://www.misp-project.org/ |
| 82 | The DFIR Report | https://thedfirreport.com |

## Cara memakai daftar ini

- **Saat membaca event yang tidak dikenal** — mulai dari ensiklopedia event ID, lalu dokumentasi Microsoft untuk semantik field.
- **Saat menulis query** — pakai dokumentasi KQL, bukan contoh yang belum diuji.
- **Saat menyusun deteksi** — bandingkan dengan aturan Sigma yang sudah ada; jangan menyalin tanpa menguji ke data sendiri.
- **Saat butuh data latihan** — pakai EVTX-ATTACK-SAMPLES atau bangun lab sendiri; dataset pihak ketiga tidak mengajarkan apa yang hilang di lingkungan Anda.

## Best Practices

- Dokumentasi primer lebih berharga daripada ringkasan orang lain; periksa versi dan tanggalnya.
- Repositori konfigurasi (Sysmon, Sigma) adalah titik awal, bukan kebenaran — sesuaikan dengan lingkungan dan uji ulang.
- Dataset publik dipakai untuk melatih cara membaca, bukan untuk menyimpulkan bahwa lingkungan Anda aman.
- Simpan tautan yang benar-benar Anda pakai; daftar panjang yang tidak pernah dibuka hanya menambah beban.
