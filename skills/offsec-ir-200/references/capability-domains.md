---
name: "Peta Kapabilitas Incident Response"
description: "Peta kapabilitas incident response beserta studi kasus, teknik serangan, dan metode deteksi per kemampuan."
tags: [capability, incident-response, case-studies, mitre-attack, kill-chain]
---

# Peta Kapabilitas Incident Response

## Klasifikasi dan Ruang Lingkup Insiden

**Cyber Incident Definitions:**
- **Event**: Any observable occurrence
- **Incident**: Event that impacts confidentiality, integrity, or availability
- **Breach**: Incident resulting in confirmed data disclosure

**Types of Incidents:** Ransomware, BEC (Business Email Compromise), insider threat, supply chain attack, DDoS, APT, commodity malware

**Case Studies:**
- **Colonial Pipeline** (2021): Ransomware → fuel supply disruption — IR failure points: lack of segmentation, single-factor access
- **SolarWinds** (2020): Supply chain — detection took months — lessons: log everything, baseline normal
- **NotPetya** (2017): Destructive malware — contained via network isolation
- **MOVEit** (2023): File transfer vulnerability — mass data exfiltration
- **MGM 2023**: Social engineering → ransomware — lack of MFA

## Kerangka dan Peran: NIST 800-61 dan CSIRT

**NIST SP 800-61 Rev 2:** 4 phases: Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident

**ITIL:** Incident Management (restore ASAP) vs Problem Management (find root cause). Service Desk = first point of contact.

**CSIRT:** Internal, external (MSSP), virtual/coordinated. Tier 1 (triage) → Tier 2 (investigation) → Tier 3 (forensics/threat intel).

## Fase Siklus IR

**Preparation:** IR plan, playbooks, tools, training, communication tree, pre-deployed collection (Sysmon, PowerShell logging, audit policy)

**Detection & Analysis:** IOCs vs IOAs, false positive triage, attack chain reconstruction (Kill Chain / MITRE ATT&CK)

**Containment, Eradication & Recovery:** Short-term (network isolation, disable account, block IP), Long-term (patch, rebuild, rotate creds), Eradication (remove malware, clean registry, verify persistence), Recovery (restore from backup, monitor)

**Post-Incident:** Lessons learned, root cause analysis, control improvements, evidence retention

## Komunikasi Insiden

**Pre-Crisis:** Communication tree, stakeholder contact list, templates (breach notification, press statement)

**During Crisis:** Internal (IR team, executive briefing), External (legal, PR, regulator), Victim communication

**Post-Crisis:** After-action report, regulatory filing, customer notification

**Regulatory Timelines:**
```
GDPR: 72 hours to notify supervisory authority
HIPAA: 60 days for breach notification
US State Laws: Varies (30-60 days)
SEC (2024): 4 days for material cybersecurity incidents
```

## Teknik Serangan yang Sering Ditemui

**MITRE ATT&CK Tactics:**
```
Initial Access (TA0001): T1566 Phishing, T1078 Valid Accounts
Execution (TA0002): T1059 Command & Scripting, T1204 User Execution
Persistence (TA0003): T1543 Create/Modify System Process, T1136 Create Account
Privilege Escalation (TA0004): T1055 Process Injection, T1068 Exploitation
Defense Evasion (TA0005): T1562 Impair Defenses, T1070 Indicator Removal
Credential Access (TA0006): T1003 OS Credential Dumping, T1550.002 Pass the Hash
Discovery (TA0007): T1087 Account Discovery, T1069 Permission Discovery
Lateral Movement (TA0008): T1021 Remote Services, T1550 Use Alternate Auth Material
Collection (TA0009): T1005 Data from Local System, T1074 Data Staged
C2 (TA0011): T1071 Application Layer Protocol, T1573 Encrypted Channel
Exfiltration (TA0010): T1048 Exfiltration Over Alternative Protocol
Impact (TA0040): T1486 Data Encrypted for Impact (Ransomware)
```

**Kill Chain vs ATT&CK:** Kill Chain = linear, high-level. ATT&CK = non-linear, granular.

**Diamond Model:** Adversary → Infrastructure → Capability → Victim

## Deteksi dan Identifikasi

**Passive Alerting:** SIEM correlation rules, EDR alerts, email security gateway, network IDS/IPS

**Active Discovery:** Threat hunting (hypothesis-driven), IOC sweep (hash, IP, domain), YARA scan

**False Positive Triage:**
```
Is this activity expected in this environment?
Is the user/admin aware of this activity?
Is there business justification?
→ If no to all, escalate to investigation
```

## Penilaian Dampak Awal

**CIA Impact Categories:** Confidentiality (data exposed?), Integrity (data modified?), Availability (systems down?)

**Recoverability:** Full (backup available), Partial (some data corrupted), Non-recoverable (data destroyed)

**Priority Matrix:**
```
HIGH IMPACT + HIGH CONFIDENCE → Immediate containment
HIGH IMPACT + LOW CONFIDENCE → Investigate urgently
LOW IMPACT + HIGH CONFIDENCE → Scheduled remediation
LOW IMPACT + LOW CONFIDENCE → Monitor
```

## Forensik Digital untuk Responder

**Order of Volatility (RFC 3227):** CPU registers → RAM → Network connections → Running processes → Disk → Archive/backup

**Chain of Custody:** Who → What → When → Where → How → Why

**Disk Imaging:** FTK Imager (GUI), dd (CLI), Guymager (Linux)

**Autopsy Workflow:** Create case → Add data source → Configure ingest modules → Manual analysis → Report

**Volatility 3:** pslist, psscan, malfind, netscan, cmdline, dumpfiles

**Windows Forensic Artifacts:** $MFT, $LogFile, $UsnJrnl, Prefetch, Amcache, ShimCache, ShellBags, Registry, Event Logs, SRUM

**Linux Forensic Artifacts:** /var/log/auth.log, syslog, kern.log, .bash_history, wtmp, btmp, journalctl

## Manajemen Kasus

**Case Structure:** Unique case ID, timeline, evidence inventory, findings, actions taken

**Evidence Tracking:** Item #, description, source, hash, collector, date/time, location

**Ticketing Integration:** ServiceNow, Jira, RTIR. Setiap phase IR harus memiliki ticket entry.

## Containment Insiden Aktif

**Network Isolation:** ACL block, VLAN isolation, DNS sinkhole, proxy block

**Endpoint Containment:** EDR quarantine, account disable, kill process, service disable

**Credential Protection:** Password reset, Kerberos ticket revocation, API key rotation, MFA enforcement

**Containment Decision Matrix:**
```
Ransomware in progress → Immediate network isolation
Data exfiltration detected → Block C2 IP + contain host
Insider threat → Disable account + preserve evidence
Phishing campaign → Block sender domain + email rules
```

## Eradikasi dan Pemulihan

**Eradication:** Malware removal, service/task removal, user account removal, registry cleanup, file cleanup, image rebuild

**Recovery:** Restore from backup, patch vulnerability, password/key rotation, recovery validation, heightened monitoring (30 days)

**Post-Incident Hardening:** MFA (FIDO2/WebAuthn), network segmentation, EDR deployment, Credential Guard, LAPS, Admin tiering, AppLocker/WDAC

## Pelaporan Post-Mortem

**Executive Summary (1 page):** What happened? When? Impact? Containment actions? Current status? Recommendations?

**Root Cause Analysis:** 5 Whys, Fishbone diagram, Timeline reconstruction

**Lessons Learned:** Detection speed, containment effectiveness, communication, tools, process

## Latihan Mandiri

Simulasi breach skala penuh: jaringan enterprise dengan aksi penyerang yang sudah direkam, agar timeline bisa direkonstruksi dari telemetri yang sama.

**Cara berlatih:** kerjakan dengan dokumentasi penuh — timeline, query, hash, dan laporan. Ulangi sampai semua skenario bisa dijelaskan dari bukti, bukan dari ingatan.

## Gotchas

- Hafalkan satu-dua kalimat kunci per studi kasus — pola yang sama berulang di insiden nyata
- Forensik disk dan memori paling sering menentukan kesimpulan — tetapi jangan mulai dari sana sebelum bukti volatil diamankan
- Jangan menghafal semua Event ID — fokus pada 20-30 Event ID yang paling sering digunakan

## Best Practices

- Review module dalam urutan: 1-2-3-8-5-6-7-10-11-12-4-9-13 (kelompokkan berdasarkan relevansi)
- Buat mind map untuk setiap case study agar mudah diingat
- Praktikkan Autopsy + Volatility workflow sampai bisa tanpa melihat dokumentasi
