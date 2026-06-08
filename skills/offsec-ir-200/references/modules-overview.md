---
name: "13 Module Deep-Dive"
description: "Complete breakdown of all IR-200 modules including case studies, attack techniques, detection methods, and exam strategies."
tags: [modules, ir-200, case-studies, mitre-attack, kill-chain]
---

# 13 Module Deep-Dive

## Modul 1: Incident Response Overview

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

## Modul 2: Fundamentals of Incident Response

**NIST SP 800-61 Rev 2:** 4 phases: Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident

**ITIL:** Incident Management (restore ASAP) vs Problem Management (find root cause). Service Desk = first point of contact.

**CSIRT:** Internal, external (MSSP), virtual/coordinated. Tier 1 (triage) → Tier 2 (investigation) → Tier 3 (forensics/threat intel).

## Modul 3: Phases of Incident Response

**Preparation:** IR plan, playbooks, tools, training, communication tree, pre-deployed collection (Sysmon, PowerShell logging, audit policy)

**Detection & Analysis:** IOCs vs IOAs, false positive triage, attack chain reconstruction (Kill Chain / MITRE ATT&CK)

**Containment, Eradication & Recovery:** Short-term (network isolation, disable account, block IP), Long-term (patch, rebuild, rotate creds), Eradication (remove malware, clean registry, verify persistence), Recovery (restore from backup, monitor)

**Post-Incident:** Lessons learned, root cause analysis, control improvements, evidence retention

## Modul 4: Incident Response Communication Plans

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

## Modul 5: Common Attack Techniques

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

## Modul 6: Incident Detection and Identification

**Passive Alerting:** SIEM correlation rules, EDR alerts, email security gateway, network IDS/IPS

**Active Discovery:** Threat hunting (hypothesis-driven), IOC sweep (hash, IP, domain), YARA scan

**False Positive Triage:**
```
Is this activity expected in this environment?
Is the user/admin aware of this activity?
Is there business justification?
→ If no to all, escalate to investigation
```

## Modul 7: Initial Impact Assessment

**CIA Impact Categories:** Confidentiality (data exposed?), Integrity (data modified?), Availability (systems down?)

**Recoverability:** Full (backup available), Partial (some data corrupted), Non-recoverable (data destroyed)

**Priority Matrix:**
```
HIGH IMPACT + HIGH CONFIDENCE → Immediate containment
HIGH IMPACT + LOW CONFIDENCE → Investigate urgently
LOW IMPACT + HIGH CONFIDENCE → Scheduled remediation
LOW IMPACT + LOW CONFIDENCE → Monitor
```

## Modul 8: Digital Forensics for Incident Responders

**Order of Volatility (RFC 3227):** CPU registers → RAM → Network connections → Running processes → Disk → Archive/backup

**Chain of Custody:** Who → What → When → Where → How → Why

**Disk Imaging:** FTK Imager (GUI), dd (CLI), Guymager (Linux)

**Autopsy Workflow:** Create case → Add data source → Configure ingest modules → Manual analysis → Report

**Volatility 3:** pslist, psscan, malfind, netscan, cmdline, dumpfiles

**Windows Forensic Artifacts:** $MFT, $LogFile, $UsnJrnl, Prefetch, Amcache, ShimCache, ShellBags, Registry, Event Logs, SRUM

**Linux Forensic Artifacts:** /var/log/auth.log, syslog, kern.log, .bash_history, wtmp, btmp, journalctl

## Modul 9: Incident Response Case Management

**Case Structure:** Unique case ID, timeline, evidence inventory, findings, actions taken

**Evidence Tracking:** Item #, description, source, hash, collector, date/time, location

**Ticketing Integration:** ServiceNow, Jira, RTIR. Setiap phase IR harus memiliki ticket entry.

## Modul 10: Active Incident Containment

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

## Modul 11: Incident Eradication and Recovery

**Eradication:** Malware removal, service/task removal, user account removal, registry cleanup, file cleanup, image rebuild

**Recovery:** Restore from backup, patch vulnerability, password/key rotation, recovery validation, heightened monitoring (30 days)

**Post-Incident Hardening:** MFA (FIDO2/WebAuthn), network segmentation, EDR deployment, Credential Guard, LAPS, Admin tiering, AppLocker/WDAC

## Modul 12: Post-Mortem Reporting

**Executive Summary (1 page):** What happened? When? Impact? Containment actions? Current status? Recommendations?

**Root Cause Analysis:** 5 Whys, Fishbone diagram, Timeline reconstruction

**Lessons Learned:** Detection speed, containment effectiveness, communication, tools, process

## Modul 13: Challenge Lab

Full-scale breach simulation — mirror image of OSIR exam. Phase 1 (Splunk) + Phase 2 (Forensics). Realistic enterprise network with pre-recorded attacker actions.

**Strategy:** Kerjakan seolah-olah exam — dokumentasi penuh. Buat report lengkap. Ulangi sampai bisa complete all 6 exercises.

## Gotchas

- Case studies di modul 1 sering muncul sebagai referensi di soal — hafal 1-2 kalimat per case
- Modul 8 (Forensics) adalah yang paling kritis dan memiliki bobot soal terbanyak di Phase 2
- Jangan menghafal semua Event ID — fokus pada 20-30 Event ID yang paling sering digunakan

## Best Practices

- Review module dalam urutan: 1-2-3-8-5-6-7-10-11-12-4-9-13 (kelompokkan berdasarkan relevansi)
- Buat mind map untuk setiap case study agar mudah diingat
- Praktikkan Autopsy + Volatility workflow sampai bisa tanpa melihat dokumentasi
