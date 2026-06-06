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

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [IR Mindset & Incident Responder Framework](#2-ir-mindset--incident-responder-framework)
3. [13 Module Deep-Dive](#3-13-module-deep-dive)
4. [Splunk SIEM & SPL Reference](#4-splunk-siem--spl-reference)
5. [Digital Forensics Reference](#5-digital-forensics-reference)
6. [Containment, Eradication, Recovery & Reporting](#6-containment-eradication-recovery--reporting)
7. [Referensi Lengkap](#7-referensi-lengkap)

---

## 1. Overview & Exam Structure

### Apa Itu IR-200 / OSIR?

IR-200 (Foundational Incident Response) adalah sertifikasi incident response dari OffSec yang mengajarkan **full IR lifecycle** — dari detection, containment, eradication, recovery, hingga post-mortem reporting. Berbeda dengan OSDA yang fokus pada detection via SIEM, OSIR menambahkan **digital forensics (disk + memory)** dan **incident management**.

OSIR (OffSec Incident Responder) adalah sertifikasi 100% praktikal — 8 jam proctored lab + 24 jam report window.

### Perbedaan OSIR vs OSDA vs OSTH

| Aspek | OSIR (IR-200) | OSDA (SOC-200) | OSTH (TH-200) |
|-------|---------------|----------------|---------------|
| **Level** | 200 (foundational) | 200 | 200 |
| **Fokus** | Full IR lifecycle, DFIR | Detection & log analysis | Proactive threat hunting |
| **Durasi exam** | 8 jam | 23h45m | 23h45m |
| **Report window** | 24 jam | 24 jam | 24 jam |
| **SIEM** | **Splunk** (SPL) | **ELK** (KQL) | **Splunk** (SPL) |
| **Disk forensics** | Autopsy / FTK Imager — WAJIB | Tidak | Tidak |
| **Memory forensics** | Volatility 3 — WAJIB | Tidak | Tidak |
| **Malware triage** | YARA, PE analysis | Tidak | Tidak |
| **Incident management** | ITIL, CSIRT, comms plans | Tidak | Tidak |
| **Passing score** | 50/70 | 75/100 | 70/100 |
| **Cert expires** | **3 tahun** (recert needed) | **Tidak** | **3 tahun** |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Phase 1 — Splunk Log Analysis** | 4 exercises × 10 pts = **40 points** |
| **Phase 2 — Disk & Memory Forensics** | 2 exercises × 15 pts = **30 points** |
| **Total** | **70 points** |
| **Passing** | **50/70** |
| **Pass paths** | 4/4 Phase 1 + 1/2 Phase 2 (50 pts) ATAU 3/4 Phase 1 + 2/2 Phase 2 (60 pts) |
| **Durasi praktikal** | 8 jam proctored |
| **Report deadline** | 24 jam setelah exam |
| **Format laporan** | PDF/DOCX — IR report template |
| **Sertifikasi valid** | 3 tahun |

### Exam Environment

- **Proctoring**: Live proctor via webcam
- **VPN**: Isolated OffSec VPN network
- **SIEM**: Splunk Enterprise dengan Windows Event Logs, Sysmon, firewall logs
- **Forensics tools**: Autopsy (disk), Volatility 3 (memory), FTK Imager
- **Malware analysis**: strings, PE analysis, YARA, hash lookup
- **Open book**: Semua sumber kecuali AI chatbots
- **Tools diizinkan**: Splunk SPL, Autopsy, Volatility, FTK Imager, YARA

### 8h Time Management Strategy

```
Hour 0-1: Initial triage (Phase 1)
  - Review Splunk dashboards + alerts
  - Identify initial access vector
  - Screenshot queries + results

Hour 1-3: Deep Splunk analysis (Phase 1 cont.)
  - Follow attack chain via logs
  - Answer 2-3 exercise questions
  - Document IoCs + timeline

Hour 3-4: Transition to Phase 2
  - Load disk image in Autopsy
  - Configure ingest modules
  - Start keyword + hash analysis

Hour 4-6: Disk & Memory Forensics (Phase 2)
  - Autopsy file system analysis + deleted files
  - Volatility 3: pslist, psscan, netscan, malfind
  - Extract and triage malware sample

Hour 6-7: Complete all Phase 2 questions
  - YARA rule writing for malware
  - Chain of custody documentation
  - Extract flags / artifacts

Hour 7-8: Final review
  - Verify all 6 exercise answers
  - Collect all screenshots
  - Organize report notes
  - Start report draft

Post-Exam (24h):
  - Complete IR report with containment, eradication, recovery strategy
  - Executive summary + timeline
  - Submit via OffSec Learning Library
```

---

## 2. IR Mindset & Incident Responder Framework

### Filosofi Dasar

OSIR mengajarkan **"Calm Under Fire"** — incident response bukan hanya soal technical skill, tapi kemampuan untuk tetap tenang, sistematis, dan komunikatif saat terjadi breach. Anda harus bisa:

1. **Triase cepat** — mana yang benar-benar incident vs false positive
2. **Rekonstruksi akurat** — apa yang terjadi, kapan, bagaimana
3. **Keputusan containment** — apakah isolate, shutdown, atau monitor
4. **Komunikasi efektif** — ke management, legal, PR, regulator
5. **Pembelajaran** — lessons learned agar tidak terulang

### Golden Rules OSIR

1. **Follow the NIST 800-61r2 lifecycle** — Preparation → Detection → Containment → Eradication → Recovery → Post-Incident. Jangan loncat fase.

2. **Document as you go** — Laporan adalah 30 dari 70 points. Screenshot setiap langkah dengan timestamp.

3. **Splunk is your timeline** — Logs adalah sumber kebenaran utama. Gunakan SPL untuk merekonstruksi kronologi serangan.

4. **Disk tells the story** — File system artifacts (Prefetch, $MFT, Registry, Event Logs) mengungkapkan apa yang tidak tercatat di SIEM.

5. **Memory reveals the truth** — Malware in-memory tidak terlihat di disk. Volatility malfind adalah teman terbaik.

6. **Contain first, ask later** — Jika host aktif menimbulkan kerusakan, isolate dulu. Forensik bisa menunggu.

7. **Communication is part of IR** — Management perlu executive summary, bukan technical dump. Hukum perlu chain of custody.

### Incident Responder Framework

```
IR Lifecycle (NIST SP 800-61 Rev 2):
  1. Preparation
     - IR plan, tools, team, training
     - Pre-deployed collection infrastructure

  2. Detection & Analysis
     - Alert triage (SIEM, EDR, user report)
     - IOC sweep + threat intelligence
     - Attack chain reconstruction
     - Impact assessment

  3. Containment, Eradication & Recovery
     - Short-term: isolate host, block IP
     - Long-term: remove malware, rebuild
     - Recovery: restore from clean backup
     - Validation: verify eradication

  4. Post-Incident Activity
     - Lessons learned
     - Evidence retention
     - Report writing
     - Control improvements
```

### ITIL Incident vs Problem

| | Incident | Problem |
|---|----------|---------|
| **Definition** | Unplanned interruption | Root cause of incidents |
| **Goal** | Restore service ASAP | Prevent recurrence |
| **Example** | Server infected with ransomware | Missing patch + weak config |
| **IR Focus** | Contain + eradicate | Root cause analysis |

### CSIRT Roles

| Role | Responsibility |
|------|---------------|
| **Incident Commander** | Overall coordination, decisions |
| **Technical Lead** | Forensics, malware analysis, containment |
| **Communications Lead** | Stakeholder updates, regulatory notifications |
| **Legal Counsel** | Chain of custody, privilege, compliance |
| **Scribe** | Timeline documentation, evidence tracking |

### 3 Pertanyaan Kunci Saat Stuck

1. **"What is the blast radius?"** — Systems, data, users affected? Prioritaskan containment.
2. **"What does the timeline tell me?"** — Reconstruct sequence. Look for gaps (possible log tampering).
3. **"Have I checked all three sources?"** — Splunk logs, disk artifacts, memory artifacts. Missing one = incomplete picture.

---

## 3. 13 Module Deep-Dive

IR-200 memiliki 13 modul berdasarkan syllabus resmi OffSec. Modul 1-12 adalah pembelajaran, modul 13 adalah Challenge Lab.

### Modul 1: Incident Response Overview

Pengenalan incident response dan lanskap ancaman:

**Cyber Incident Definitions:**
- **Event**: Any observable occurrence
- **Incident**: Event that impacts confidentiality, integrity, or availability
- **Breach**: Incident resulting in confirmed data disclosure

**Types of Incidents:**
- Ransomware, BEC (Business Email Compromise), insider threat, supply chain attack, DDoS, APT, commodity malware

**Case Studies (diajarkan di module):**
- **Colonial Pipeline** (2021): Ransomware → fuel supply disruption — IR failure points: lack of segmentation, single-factor access
- **SolarWinds** (2020): Supply chain — detection took months — lessons: log everything, baseline normal
- **NotPetya** (2017): Destructive malware — contained via network isolation
- **MOVEit** (2023): File transfer vulnerability — mass data exfiltration
- **MGM 2023**: Social engineering → ransomware — lack of MFA

**Mindset**: Incident types menentukan strategi respons. Ransomware ≠ insider threat ≠ APT — setiap jenis punya containment strategy berbeda.

### Modul 2: Fundamentals of Incident Response

Fundamental framework dan standar IR:

**NIST SP 800-61 Rev 2:**
- Standar de facto untuk incident response
- 4 phases: Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident

**ITIL (Information Technology Infrastructure Library):**
- Incident Management: restore normal service ASAP
- Problem Management: find root cause to prevent recurrence
- Service Desk: first point of contact for incident reporting

**CSIRT (Computer Security Incident Response Team):**
- **Types**: Internal, external (MSSP), virtual/coordinated
- **Staffing**: 24/7 rotation for enterprise SOCs
- **Tiers**: Tier 1 (triage) → Tier 2 (investigation) → Tier 3 (forensics/threat intel)

**Severity Matrices:**
```
CRITICAL: PII exposed, Ransomware, DC compromised → <1h response
HIGH: Suspicious admin activity, malware on server → 2-4h
MEDIUM: Phishing campaign, policy violation → 24h
LOW: Scan, failed login spike → scheduled
```

**Mindset**: IR bukan hanya teknis — framework dan proses menentukan seberapa efektif respons.

### Modul 3: Phases of Incident Response

Deep dive NIST 800-61r2 phases dengan praktik:

**Preparation Phase:**
- IR plan, playbooks, tools, training
- Communication tree (who calls whom)
- Pre-deployed collection: Sysmon, PowerShell logging, audit policy

**Detection & Analysis Phase:**
- Indicators of Compromise (IOCs) vs Indicators of Attack (IOAs)
- False positive triage — jangan langsung panic
- Attack chain reconstruction: map to Kill Chain / MITRE ATT&CK

**Containment, Eradication & Recovery Phase:**
- **Short-term containment**: network isolation, disable account, block IP
- **Long-term containment**: apply patches, rebuild, rotate creds
- **Eradication**: remove malware, clean registry, verify persistence
- **Recovery**: restore from backup, monitor for reinfection

**Post-Incident Phase:**
- Lessons learned meeting
- Root cause analysis
- Control improvements
- Evidence retention (check legal requirements)

### Modul 4: Incident Response Communication Plans

Komunikasi adalah aspek yang sering diremehkan:

**Pre-Crisis:**
- Communication tree: siapa di-Cc untuk setiap level severity
- Stakeholder contact list (IT, legal, PR, management, regulator)
- Templates: breach notification draft, press statement draft

**During Crisis:**
- **Internal**: IR team (Slack/Teams channel), executive briefing
- **External**: Legal (data breach notification), PR (public statement), regulator (GDPR 72h)
- **Victim communication**: jika ada data user yang ter-expose

**Post-Crisis:**
- After-action report
- Regulatory filing
- Customer notification

**Regulatory Timelines:**
```
GDPR: 72 hours to notify supervisory authority
HIPAA: 60 days for breach notification
US State Laws: Varies (30-60 days)
SEC (2024): 4 days for material cybersecurity incidents
```

**Mindset**: Komunikasi yang buruk bisa mengubah incident menjadi crisis PR. Selalu update stakeholder sebelum mereka dengar dari berita.

### Modul 5: Common Attack Techniques

Memahami TTP attacker untuk detection dan analysis:

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

**Cyber Kill Chain vs MITRE ATT&CK:**
- Kill Chain: linear, high-level (7 phases)
- ATT&CK: non-linear, granular (14 tactics, hundreds of techniques)
- Gunakan keduanya: Kill Chain untuk executive summary, ATT&CK untuk technical report

**Diamond Model:**
- Adversary → Infrastructure → Capability → Victim
- Setiap incident bisa dimodelkan dalam diamond

**Mindset**: Kenali TTP bukan hanya untuk detection, tapi untuk menentukan containment strategy.

### Modul 6: Incident Detection and Identification

Teknik deteksi dan identifikasi insiden:

**Passive Alerting:**
- SIEM correlation rules
- EDR alerts (behavioral)
- Email security gateway
- Network IDS/IPS

**Active Discovery:**
- Threat hunting: hypothesis-driven search
- IOC sweep: hash, IP, domain, registry key
- YARA scan: custom rules on endpoints

**Attack Chain Reconstruction:**
```
Initial Access → Execution → Persistence → Privesc → 
Credential Access → Lateral Movement → C2 → Exfiltration/Impact
```

**False Positive Triage:**
```
Is this activity expected in this environment?
Is the user/admin aware of this activity?
Is there business justification?
→ If no to all, escalate to investigation
```

**Common False Positive Sources:**
- Legitimate admin tools (PowerShell, WMI, PsExec)
- Scheduled maintenance tasks
- Software updates
- Penetration testing (if authorized)

### Modul 7: Initial Impact Assessment

Menilai dampak insiden secara cepat:

**CIA Impact Categories:**
- **Confidentiality**: Data exposed? Type of data? (PII, PHI, IP)
- **Integrity**: Data modified? Systems compromised?
- **Availability**: Systems down? Ransomware?

**Recoverability:**
- Full recovery possible? (backup available?)
- Partial recovery? (some data corrupted)
- Non-recoverable? (data destroyed, no backup)

**Priority Matrix:**
```
HIGH IMPACT + HIGH CONFIDENCE → Immediate containment
HIGH IMPACT + LOW CONFIDENCE → Investigate urgently
LOW IMPACT + HIGH CONFIDENCE → Scheduled remediation
LOW IMPACT + LOW CONFIDENCE → Monitor
```

**Blast Radius Analysis:**
- Which systems are affected?
- Which users/data are impacted?
- Can attacker move laterally? (check AD + firewall rules)
- Is C2 active? (check DNS logs, proxy logs)

### Modul 8: Digital Forensics for Incident Responders

**Modul paling kritis** — forensik untuk incident response:

**Evidence Handling:**
- **Order of Volatility** (RFC 3227):
  1. CPU registers, cache
  2. RAM (memory dump)
  3. Network connections
  4. Running processes
  5. Disk (forensic image)
  6. Archive/backup
- **Chain of Custody**: Who → What → When → Where → How → Why
- **Write blockers**: Hardware write blocker untuk imaging

**Disk Imaging:**
```
FTK Imager: GUI-based, supports E01/raw
dd: Linux CLI, bit-for-bit copy
  dd if=/dev/sda of=evidence.dd bs=4M conv=noerror,sync
Guymager: Linux GUI imager with hash verification
```

**Autopsy (The Sleuth Kit):**
- Open source GUI forensics platform
- **Workflow:**
  1. Create case → Add data source (disk image)
  2. Configure ingest modules
  3. Manual analysis (filesystem, keywords)
  4. Report generation

**Key Autopsy Ingest Modules:**
```
Recent Activity: Browser history, downloads, cookies
Hash Lookup: Compare against NSRL (NIST known-good) + known-bad
File Type Identification: Magic byte signature matching
Keyword Search: Index content for full-text search
Extension Mismatch Detector: Find file rename attempts
Email Parser: PST, MBOX, EML extraction
Exif Parser: Image metadata (GPS, timestamps)
Encryption Detection: Find encrypted files/containers
Interesting Files Identifier: Custom rule-based flagging
Picture Analyzer: Image categorization
Data Source Integrity: Verify image hash
```

**Memory Forensics with Volatility 3:**
```
Windows plugins:
  windows.pslist        — List running processes (EPROCESS list)
  windows.pstree        — Process tree (parent-child)
  windows.psscan        — Pool scanner (find hidden processes)
  windows.cmdline       — Command line arguments
  windows.malfind       — Find injected code
  windows.netscan       — Network connections
  windows.dlllist       — Loaded DLLs per process
  windows.modules       — Loaded kernel modules
  windows.handles       — Open handles
  windows.callbacks     — Kernel callbacks
  windows.registry      — Registry hives
  windows.dumpfiles     — Dump process memory
  windows.memmap        — Memory map of process
  timeliner.Timeliner   — Generate super timeline
```

**Memory Analysis Workflow:**
```
1. Identify profile: windows.info
2. Process list: windows.pslist + windows.psscan
3. Hidden processes: bandingkan pslist vs psscan
4. Command lines: windows.cmdline — cari PowerShell encoded, suspicious args
5. Injected code: windows.malfind — cari RWX memory regions
6. Network: windows.netscan — cari C2 connections
7. Dump: windows.dumpfiles — extract suspicious processes
```

**Windows Forensic Artifacts:**
```
$MFT: Master File Table — all files, timestamps, sizes
$LogFile: Transaction log of NTFS changes
$UsnJrnl: Update sequence number journal — file change history
Prefetch: Application execution traces (last 8 runs)
Amcache: Application compatibility cache (installed executables)
ShimCache: Application compatibility cache (another source)
ShellBags: Folder view settings (user directory navigation)
Registry: HKLM\System, HKLM\Sam, HKLM\Security, NTUSER.DAT
Event Logs: Security.evtx, System.evtx, PowerShell.evtx
SRUM: System Resource Usage Monitor (network, energy usage)
```

**Linux Forensic Artifacts:**
```
/var/log/auth.log: Authentication logs
/var/log/syslog: System logs
/var/log/kern.log: Kernel messages
/var/log/apache2/ or /var/log/nginx/: Web server logs
.bash_history: User command history
/var/log/lastlog: Last login records
/var/log/wtmp: Login records (who/w)
/var/log/btmp: Failed login records
journalctl: Systemd journal
/etc/shadow: Password hashes
/etc/passwd: User accounts
```

**Mindset**: Di OSIR, forensik bukan untuk investigasi kriminal — ini untuk incident response. Fokus pada: apa yang terjadi, bagaimana, dan bagaimana menghentikannya.

### Modul 9: Incident Response Case Management

Manajemen kasus insiden:

**Case Structure:**
- Unique case ID (e.g., IR-2026-001)
- Timeline of events
- Evidence inventory
- Findings and conclusions
- Actions taken

**Evidence Tracking:**
```
Item #: E-001
Description: Email phishing with malicious attachment
Source: User workstation
Hash: SHA256:<hash>
Collected by: Analyst Name
Date/Time: 2026-01-15 14:30 UTC
Location: /cases/IR-2026-001/evidence/phishing.eml
```

**Ticketing Integration:**
- ServiceNow, Jira, RTIR untuk incident tracking
- Setiap phase IR harus memiliki ticket entry
- SLA tracking untuk containment time

### Modul 10: Active Incident Containment

Teknik containment aktif — **modul yang paling penting untuk OSIR report**:

**Network Isolation:**
- **ACL block**: Block IP di firewall
- **VLAN isolation**: Isolate host ke quarantine VLAN
- **DNS sinkhole**: Redirect malicious domain to sinkhole
- **Proxy block**: Block C2 domain at proxy

**Endpoint Containment:**
- **EDR quarantine**: Isolate host from network (Windows Defender for Endpoint, CrowdStrike)
- **Account disable**: Disable compromised account
- **Kill process**: Terminate malicious process
- **Service disable**: Stop malicious service

**Credential Protection:**
- **Password reset**: Reset compromised accounts
- **Kerberos ticket revocation**: Invalidate TGT/TGS
- **API key rotation**: Rotate keys for cloud services
- **MFA enforcement**: If not already enabled

**Containment Decision Matrix:**
```
Ransomware in progress → Immediate network isolation
Data exfiltration detected → Block C2 IP + contain host
Insider threat → Disable account + preserve evidence
Phishing campaign → Block sender domain + email rules
```

### Modul 11: Incident Eradication and Recovery

Membersihkan dan memulihkan setelah containment:

**Eradication:**
- **Malware removal**: Antivirus scan, manual registry cleanup
- **Service/task removal**: Stop + delete malicious services/scheduled tasks
- **User account removal**: Delete backdoor accounts
- **Registry cleanup**: Remove Run keys, Winlogon entries
- **File cleanup**: Delete malicious files
- **Image rebuild**: Reimage from known-good golden image (most thorough)

**Recovery:**
- **Restore from backup**: Clean backup from pre-incident date
- **Patch vulnerability**: Address root cause
- **Password/key rotation**: All affected accounts
- **Recovery validation**: Verify system integrity
- **Heightened monitoring**: 30-day post-recovery monitoring window

**Post-Incident Hardening:**
```
Phishing-resistant MFA (FIDO2/WebAuthn)
Network segmentation (DMZ, VoIP, Corp, Guest)
EDR deployment on all endpoints
Credential Guard (Windows Defender Credential Guard)
LAPS for local admin passwords
Admin tiering (Tier 0/1/2 model)
AppLocker or WDAC (Windows Defender Application Control)
```

### Modul 12: Post-Mortem Reporting

**Modul report writing** — kritis untuk OSIR karena 30/70 points dari report:

**Executive Summary (1 page):**
```
What happened?
When did it happen?
What was the impact?
What was done to contain/eradicate?
What is the current status?
What are the recommendations?
```

**Root Cause Analysis (RCA):**
- **5 Whys**: Ask "why" 5 times to find root cause
- **Fishbone diagram**: Categorize causes (people, process, technology)
- **Timeline reconstruction**: Chronological event list

**Damage Assessment:**
- Systems affected
- Data compromised (type, volume, sensitivity)
- Business impact (revenue, reputation, regulatory)
- Recovery cost estimation

**Lessons Learned (What went well / What went wrong):**
```
Detection: Were we too slow? Missed signals?
Containment: Was it effective? Quick enough?
Communication: Were stakeholders informed timely?
Tools: Were tools adequate?
Process: Did playbook help or hinder?
```

### Modul 13: Challenge Lab

Full-scale breach simulation — **mirror image of the OSIR exam**:

**Structure:**
- Same format as exam: Phase 1 (Splunk) + Phase 2 (Forensics)
- Realistic enterprise network environment
- Pre-recorded attacker actions
- Disk image + memory dump for analysis

**Strategi:**
- Kerjakan seolah-olah exam — dokumentasi penuh
- Buat report lengkap dengan containment + eradication strategy
- Identifikasi gaps: apa yang Anda lewatkan?
- Ulangi jika perlu sampai bisa complete all 6 exercises

---

## 4. Splunk SIEM & SPL Reference

### Splunk Search Processing Language (SPL) Reference

#### Pipeline Fundamentals

SPL menggunakan pipe (`|`) untuk mengalirkan data:
```
index=<index> sourcetype=<sourcetype> [filters]
| <command1> [options]
| <command2> [options]
| table <fields>
```

#### Core Commands (80% of SOC work)

| Command | Function | Example |
|---------|----------|---------|
| `index=` | Select data source | `index=windows` |
| `sourcetype=` | Filter by log type | `sourcetype=WinEventLog:Security` |
| `stats` | Aggregate & count | `stats count by Account` |
| `eval` | Create calculated fields | `eval risk=if(EventCode=4625, "HIGH", "LOW")` |
| `rex` | Regex field extraction | `rex field=_raw "IP=(?<ip>\d+\.\d+\.\d+\.\d+)"` |
| `transaction` | Group related events | `transaction session_id maxpause=30m` |
| `table` | Select output columns | `table _time, Account, src_ip` |
| `sort` | Sort results | `sort -count` |
| `dedup` | Remove duplicates | `dedup Account` |
| `timechart` | Time-series aggregation | `timechart count by EventCode` |
| `top` | Most common values | `top limit=10 Account` |
| `where` | Eval-based filter | `where count > 10` |
| `lookup` | Enrich from reference data | `lookup geo_ip src_ip OUTPUT country` |
| `fields` | Keep/remove fields | `fields + Account, src_ip` |
| `rename` | Rename fields | `rename Account as Username` |
| `convert` | Convert field types | `convert timeformat="%Y-%m-%d" ctime(_time)` |
| `streamstats` | Running calculations | `streamstats count by Account` |

#### OSIR Detection Queries

**Failed Logons (4625) — Brute Force Detection:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4625
| stats count as FailedCount, dc(Account) as UniqueAccounts by src_ip
| where FailedCount > 20
| sort -FailedCount
```

**Successful Logon (4624) — Track Access:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624
| table _time, Account, ComputerName, LogonType, src_ip
| sort _time
```

**RDP Logons (4624 + LogonType=10) — Lateral Movement:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=10
| table _time, Account, ComputerName, src_ip
| sort -_time
```

**Pass-the-Hash Indicators (4624 Type 3 + NTLM):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=3 LogonProcessName=NtLmSsp 
| stats count by Account, ComputerName, src_ip
```

**Service Creation (7045 / 4697) — Persistence:**
```spl
index=windows sourcetype=WinEventLog:System EventCode=7045
| table _time, ServiceName, ImagePath, Account, ComputerName
```

**Process Creation (4688) — Suspicious Commands:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*powershell*" OR CommandLine="*cmd.exe*" OR CommandLine="*wscript*"
| table _time, Account, CommandLine, ComputerName, ParentProcessName
```

**Scheduled Task Creation (4698) — Persistence:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4698
| table _time, Account, TaskName, Command, ComputerName
```

**Account Creation (4720) — Backdoor Account:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4720
| table _time, Account, TargetAccount, ComputerName
```

**Admin Group Modification (4728/4732/4756):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode IN (4728, 4732, 4756)
| search GroupName="Domain Admins" OR GroupName="Administrators" OR GroupName="Enterprise Admins"
| table _time, Account, TargetAccount, GroupName, ComputerName
```

**Log Clearing (1102) — Defense Evasion:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=1102
| table _time, Account, ComputerName
```

**Kerberoasting (4769 + RC4):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4769 TicketEncryptionType=0x17
| stats count by Account, ServiceName, ClientAddress
| sort -count
```

**PowerShell Script Block (4104):**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" EventCode=4104
| table _time, ComputerName, Account, ScriptBlockText
```

**Sysmon Process Creation (EventCode 1):**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
| search CommandLine="*mimikatz*" OR CommandLine="*Invoke-*" OR CommandLine="*-enc*"
| table _time, ComputerName, User, CommandLine, ParentCommandLine
```

**Sysmon Network Connection (EventCode 3) — C2 Detection:**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| search NOT DestIp=10.* AND NOT DestIp=192.168.* AND NOT DestIp=172.16.*
| stats count by ComputerName, DestIp, DestPort, Image
| sort -count
```

**Sysmon DNS Query (EventCode 22) — DGA Detection:**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=22
| stats count by ComputerName, QueryName
| sort -count
```

**Threat Hunting — Beaconing Detection:**
```spl
index=proxy sourcetype=proxylogs
| stats count by src_ip, dest_ip
| where count > 50 AND count < 500
| eval regularity = count / 24
```

**Threat Hunting — LSASS Access (Sysmon 10):**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=10
| search TargetImage="*\\lsass.exe"
| where NOT match(SourceImage, "(?i)svchost|MpEng|taskmgr|csrss")
| table _time, ComputerName, SourceImage, SourceUser, GrantedAccess
```

**SPL Performance Tips:**
- Always specify `index=` and `sourcetype=` first
- Always set a time range (earliest/latest)
- Filter early in the pipeline, transform later
- Use `| head 100` to test expensive queries
- Use `fields` to reduce data volume
- Use `tstats` for data model acceleration (if available)

### Splunk Enterprise Security (ES) Concepts

- **CIM (Common Information Model)**: Standardized field names across data sources
- **ESCU (Enterprise Security Content Updates)**: Pre-built correlation searches
- **Risk-Based Alerting (RBA)**: Accumulate risk scores instead of direct alerts
- **Threat Intelligence Framework**: Import STIX/TAXII feeds
- **SOAR/Phantom**: Playbook automation for containment actions

---

## 5. Digital Forensics Reference

### Disk Forensics with Autopsy

**Autopsy Workflow:**
```
1. Create Case: Name, number, examiner
2. Add Data Source: Disk image (dd/E01/VMDK/VHD)
3. Configure Ingest Modules:
   - Recent Activity (browser, documents)
   - Hash Lookup (NSRL known-good, known-bad)
   - File Type Identification (magic bytes)
   - Keyword Search (full-text index)
   - Extension Mismatch Detector
4. Manual Analysis:
   - File system tree + deleted files (marked with X)
   - Keyword hits review
   - Timeline analysis (Tools → Timeline)
   - Tag evidence (Evidence-Critical, Supporting)
5. Generate Report: HTML/Excel/Text
```

**Sleuth Kit CLI Commands:**
```bash
# Verify image
img_stat evidence.dd

# Partition layout
mmls evidence.dd

# List files (with deleted)
fls -r -o 2048 evidence.dd

# Recover file by inode
icat -o 2048 evidence.dd 14523 > recovered.doc

# Generate timeline bodyfile
fls -r -m "/" -o 2048 evidence.dd > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv

# Search file signatures
sigfind -o 2048 evidence.dd 25504446  # PDF header
```

**Key Artifacts to Examine:**
- **Prefetch**: `C:\Windows\Prefetch\*.pf` — application execution (last 8)
- **Amcache**: `C:\Windows\AppCompat\Programs\Amcache.hve` — installed EXEs
- **$MFT**: All files + timestamps on NTFS volume
- **Registry**: `NTUSER.DAT` (user activity), `SAM` (local accounts), `SYSTEM` (config)
- **Event Logs**: `Security.evtx`, `System.evtx`, `PowerShell.evtx`
- **Browser artifacts**: History, downloads, cookies, bookmarks
- **Jump Lists**: Recent documents per user
- **SRUM**: System Resource Usage Monitor — network/energy/CPU per app

### Memory Forensics with Volatility 3

**Essential Volatility 3 Commands:**
```bash
# Identify system
vol -f memory.raw windows.info

# List processes
vol -f memory.raw windows.pslist
vol -f memory.raw windows.pstree
vol -f memory.raw windows.psscan       # Finds hidden processes

# Command lines
vol -f memory.raw windows.cmdline
vol -f memory.raw windows.cmdline --pid 1234

# Network
vol -f memory.raw windows.netscan
vol -f memory.raw windows.netstat

# Malware detection
vol -f memory.raw windows.malfind       # Injected code / RWX regions
vol -f memory.raw windows.malfind --dump
vol -f memory.raw windows.apihooks      # API hook detection
vol -f memory.raw windows.ssdt          # SSDT hook detection

# Process details
vol -f memory.raw windows.dlllist --pid 1234
vol -f memory.raw windows.modules
vol -f memory.raw windows.handles --pid 1234
vol -f memory.raw windows.cmdline --pid 1234

# Registry
vol -f memory.raw windows.registry.hives
vol -f memory.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Dump artifacts
vol -f memory.raw windows.dumpfiles --pid 1234
vol -f memory.raw windows.memmap --pid 1234 --dump

# Timeline
vol -f memory.raw timeliner.Timeliner
```

**Suspicious Process Indicators:**
- **Hidden process**: In psscan but NOT in pslist → DKOM manipulation
- **No parent**: process with PPID 0 or orphaned
- **Suspicious path**: Running from `C:\Users\*\AppData\Local\Temp\`, `C:\Windows\Temp\`
- **Mismatched name**: `svchost.exe` in wrong path
- **RWX memory**: `malfind` shows executable + writable regions (code injection)
- **Network connections**: Process with no reason to be on network (e.g., notepad.exe calling out)

**Memory Analysis Workflow:**
```
1. Profile: windows.info → system version + profile
2. Process list: pslist + psscan → compare for hidden processes
3. Process tree: pstree → unusual parent-child (cmd.exe spawned by word.exe = phishing)
4. Command line: cmdline → encoded PowerShell, suspicious arguments
5. Injected code: malfind → process injection indicators
6. Network: netscan → C2 connections from suspicious PIDs
7. Dump: dumpfiles on suspicious processes → further malware analysis
```

### Malware Triage

**Static Analysis:**
```bash
# File type
file suspicious.exe

# Strings extraction
strings suspicious.exe | grep -iE "http|https|cmd|powershell|run|C2"

# Entropy (high = packed/encrypted)
python -c "import struct; f=open('suspicious.exe','rb').read(); 
import math; h=0; [exec('global h; h+='+str(b)+'*math.log2('+str(b)+')') for b in [f.count(i) for i in range(256)] if b>0]; print(8-h/math.log2(256))"

# PE analysis
peview suspicious.exe       # GUI
python -c "import pefile; pe=pefile.PE('suspicious.exe'); print([s.Name for s in pe.DIRECTORY_ENTRY_IMPORT])"
```

**Tools:**
- **Detect-It-Easy (DIE)**: Packer detection
- **PEview / CFF Explorer**: PE structure analysis
- **strings**: Extract readable content
- **VirusTotal**: Hash lookup
- **ANY.RUN**: Interactive sandbox
- **Hybrid Analysis**: Automated sandbox

**YARA Rules:**
```yara
rule SuspiciousPowerShell {
    meta:
        description = "Detects suspicious PowerShell usage"
        author = "OSIR Analyst"
    strings:
        $enc = "-enc" nocase
        $iex = "IEX" nocase
        $download = "DownloadString" nocase
    condition:
        any of ($enc, $iex) and $download
}

rule Mimikatz {
    meta:
        description = "Detects Mimikatz strings"
    strings:
        $s1 = "mimikatz"
        $s2 = "sekurlsa"
        $s3 = "logonpasswords"
        $s4 = "privilege::debug"
    condition:
        2 of them
}

rule C2Domain {
    meta:
        description = "Detects suspicious C2 domains"
    strings:
        $ip = /\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/
        $long = /[a-z0-9]{20,}\.(com|net|xyz)/
    condition:
        $long or #ip > 3
}
```

---

## 6. Containment, Eradication, Recovery & Reporting

### Containment Strategy Reference

| Scenario | Short-Term | Long-Term |
|----------|------------|-----------|
| **Ransomware** | Network isolate infected host, block ransomware C2 IP | Reimage host, restore from clean backup, patch entry point |
| **Phishing** | Disable compromised account, block sender domain | Password reset, MFA enrollment, user training |
| **C2 Beacon** | Block C2 IP/Domain at firewall, DNS sinkhole | Host EDR scan, remove persistence, verify clean |
| **Data Exfiltration** | Block outbound to unknown IPs, disable risky accounts | Rotate API keys, audit data access, DLP rules |
| **Lateral Movement** | Segment affected VLAN, disable source account | Credential rotation, implement LAPS, tiered admin model |

### Eradication Checklist

```
[ ] Malware removed via AV/EDR scan
[ ] Malicious services stopped + deleted
[ ] Scheduled tasks removed
[ ] Registry persistence entries cleaned
[ ] Backdoor accounts identified + disabled
[ ] Web shells removed from web servers
[ ] Compromised creds rotated
[ ] API keys rotated
[ ] System reimaged (if necessary)
[ ] Verify eradication via re-scan
```

### Recovery Validation

```
[ ] System operational (verified by IT)
[ ] Service restored to users
[ ] Data integrity verified
[ ] Backup validated as clean
[ ] Patches applied (root cause addressed)
[ ] Monitoring re-enabled with heightened alerting
[ ] Incident documented in case management system
```

### OSIR Report Template

**Gunakan struktur berikut untuk Phase 1 dan Phase 2 report:**

```
1. Executive Summary
   - Incident overview (1 paragraph)
   - Key findings (3-5 bullet points)
   - Containment actions summary
   - Current status

2. Timeline of Events
   | Timestamp | Event | Source | Confidence |
   |-----------|-------|--------|------------|
   | 2026-01-15 08:30 | Initial access via web shell | Splunk (IIS logs) | High |
   | 2026-01-15 08:35 | PowerShell download cradle | Splunk (4688) | High |

3. Phase 1: SIEM Analysis (Splunk)
   Exercise 1: [Title]
   - Objective
   - SPL Query used
   - Findings (with screenshots)
   - Artifact details (IP, user, process, command)

   Exercise 2-4: (same structure)

4. Phase 2: Forensic Analysis (Autopsy + Volatility)
   Exercise 5: Disk Image Analysis
   - Imaging details (hash, chain of custody)
   - Autopsy ingest results
   - File system artifacts found
   - Keyword search hits

   Exercise 6: Memory Analysis + Malware Triage
   - Volatility analysis results
   - Malware characteristics (type, hash, YARA matches)
   - Static/dynamic analysis summary

5. Containment, Eradication & Recovery
   - Actions taken
   - Timeline of containment
   - Eradication verification
   - Recovery status

6. Incident Classification
   - MITRE ATT&CK mapping
   - Impact assessment (CIA)
   - Severity rating

7. Lessons Learned
   - What went well
   - What could be improved
   - Recommended controls

8. Appendices
   - Full SPL queries
   - Volatility command output
   - YARA rules
   - Evidence inventory (chain of custody)
```

### Chain of Custody Template

| Item # | Description | Source | Hash | Collected By | Date/Time |
|--------|-------------|--------|------|--------------|-----------|
| E-001 | Disk image (evidence.dd) | Host: WEB01 | SHA256: abc... | Analyst | 2026-01-15 09:00 |
| E-002 | Memory dump (memory.raw) | Host: WEB01 | SHA256: def... | Analyst | 2026-01-15 09:05 |
| E-003 | Splunk query results (export) | SIEM | N/A | Analyst | 2026-01-15 10:30 |

### Executive Summary Template

```
On [DATE], at approximately [TIME], [ORGANIZATION] identified suspicious activity on
[HOST/SYSTEM]. Initial detection occurred via [SIEM alert / user report / EDR]. The
incident was classified as [RANSOMWARE / DATA EXFILTRATION / UNAUTHORIZED ACCESS]
with a severity of [CRITICAL / HIGH].

The attacker gained initial access through [VECTOR], then [EXECUTION / PERSISTENCE /
LATERAL MOVEMENT SUMMARY]. A total of [N] systems were affected, including [CRITICAL
SYSTEMS]. [TYPE OF DATA] was compromised.

Immediate containment actions included [ISOLATION / ACCOUNT DISABLE / BLOCK]. The
attacker's [C2 / TOOL] was identified and blocked at [FIREWALL / PROXY]. Eradication
was completed via [REIMAGE / AV SCAN / MANUAL REMOVAL] on [DATE].

Recommendations include: [PATCH / MFA / SEGMENTATION / MONITORING]. Full technical
details are provided in the sections below.
```

---

## 7. Referensi Lengkap

### Official OffSec Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | IR-200 Course Page | https://www.offsec.com/courses/ir-200/ |
| 2 | IR-200 Syllabus (PDF) | https://www.offsec.com/documentation/IR-200-Syllabus.pdf |
| 3 | IR-200 Syllabus (Alt PDF) | https://manage.offsec.com/app/uploads/2024/10/IR-200_-Foundational-Incident-Response-Syllabus-final.pdf |
| 4 | OSIR Exam Guide | https://help.offsec.com/hc/en-us/articles/30960007786900 |
| 5 | OSIR Exam FAQ | https://help.offsec.com/hc/en-us/articles/30960026046356 |
| 6 | OSIR Certification Renewal | https://help.offsec.com/hc/en-us/articles/36010548001812 |
| 7 | IR-200 Course FAQ | https://help.offsec.com/hc/en-us |
| 8 | OffSec — OSIR Blog Announcement | https://www.offsec.com/blog/announcing-ir-200/ |
| 9 | OffSec — OSIR Journey Blog | https://www.offsec.com/blog/my-journey-with-ir-200-becoming-an-offsec-certified-incident-responder-osir/ |
| 10 | NICCS — IR-200 Course Listing | https://niccs.cisa.gov/training/catalog |

### Exam Reviews & Experiences

| # | Author | Title | Year |
|---|--------|-------|------|
| 11 | Under the Appl3Tree | OffSec IR-200 & OSIR Certification Review | 2025 |
| 22 | AdminStar | My OSIR and OSTH Journey | 2025 |
| 13 | Kyser Clark | Everything About OSIR Certification | 2025 |
| 14 | OffSec (Mobius) | My Journey with IR-200 — OSIR | 2025 |
| 15 | OpenExamPrep | Free OSIR Practice Test | 2026 |
| 16 | LAC devblog | OSIR合格体験記 (Japanese) | 2026 |
| 17 | QA | OSIR Certification & Exam Guide | 2025 |
| 18 | QA — OSIR Course | OSIR: Incident Response (QAOSIR90) | 2026 |

### NIST Standards & Government Frameworks

| # | Resource | URL |
|---|----------|-----|
| 19 | NIST SP 800-61 Rev 2 (IR Guide) | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |
| 20 | NIST SP 800-86 (Forensic Techniques) | https://csrc.nist.gov/publications/detail/sp/800-86/final |
| 21 | NIST SP 800-115 (Security Testing) | https://csrc.nist.gov/publications/detail/sp/800-115/final |
| 22 | NIST SP 800-184 (Cybersecurity Event Recovery) | https://csrc.nist.gov/publications/detail/sp/800-184/final |
| 23 | NIST SP 800-53 Rev 5 (Security Controls) | https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final |
| 24 | NIST CSF 2.0 (Cybersecurity Framework) | https://www.nist.gov/cyberframework |
| 25 | CISA — Incident Response Resources | https://www.cisa.gov/incident-response |
| 26 | CISA — Incident Response Playbook | https://www.cisa.gov/resources-tools/resources/incident-response-playbook |
| 27 | CISA — Ransomware Guide | https://www.cisa.gov/stopransomware |
| 28 | CIS Controls v8 | https://www.cisecurity.org/controls/v8 |
| 29 | RFC 3227 — Order of Volatility | https://datatracker.ietf.org/doc/html/rfc3227 |
| 30 | FIRST CVSS v3.1 Calculator | https://www.first.org/cvss/calculator/3.1 |
| 31 | NIST NSRL — Hash Sets | https://www.nist.gov/itl/ssd/software-quality-group/national-software-reference-library-nsrl |

### Splunk / SPL

| # | Resource | URL |
|---|----------|-----|
| 32 | Splunk SPL Cheat Sheet (Decryption Digest) | https://www.decryptiondigest.com/blog/splunk-spl-queries-cheat-sheet |
| 33 | Splunk SPL Cheat Sheet — 15 SOC Queries (EpicDetect) | https://epicdetect.io/blogs/splunk-spl-cheat-sheet-15-queries-soc-analysts |
| 34 | Splunk SPL Cheatsheet (EpicDetect) | https://epicdetect.io/resources/spl-cheatsheet |
| 35 | Nervi0z/splunk-blue-team — SPL Detection Queries | https://github.com/Nervi0z/splunk-blue-team |
| 36 | irevanescence/soc-splunk-windows-security | https://github.com/irevanescence/soc-splunk-windows-security |
| 37 | Splunk Documentation — Search Reference | https://docs.splunk.com/Documentation/Splunk/latest/SearchReference |
| 38 | Splunk — Common Information Model (CIM) | https://docs.splunk.com/Documentation/CIM/latest/User/Overview |
| 39 | Splunk Enterprise Security (ES) | https://www.splunk.com/en_us/software/enterprise-security.html |
| 40 | Splunk — Risk-Based Alerting Guide | https://docs.splunk.com/Documentation/ES/latest/RBA |
| 41 | Splunk Fundamentals Free Training | https://www.splunk.com/en_us/training/free-courses.html |
| 42 | Splunk SOAR Documentation | https://docs.splunk.com/Documentation/SOAR |

### Digital Forensics — Volatility

| # | Resource | URL |
|---|----------|-----|
| 43 | Volatility 3 Official Documentation | https://volatility3.readthedocs.io/ |
| 44 | Volatility 2 & 3 Cheatsheet (Encient) | https://encient.github.io/cheatsheets/dfir/volatility/ |
| 45 | Volatility Cheat Sheet (1337skills) | https://1337skills.com/cheatsheets/volatility/ |
| 46 | ilyess-sellami/Volatility3-Memory-Analysis-Playbook | https://github.com/ilyess-sellami/Volatility-3-Memory-Analysis-Playbook |
| 47 | HackTricks — Volatility Cheatsheet | https://book.hacktricks.wiki/en/generic-methodologies-and-resources/basic-forensic-methodology/memory-dump-analysis/volatility-cheatsheet.html |
| 48 | Volatility Foundation | https://www.volatilityfoundation.org/ |
| 49 | Volatility 3 GitHub | https://github.com/volatilityfoundation/volatility3 |

### Digital Forensics — Autopsy & Sleuth Kit

| # | Resource | URL |
|---|----------|-----|
| 50 | Autopsy User Documentation | https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/ |
| 51 | Autopsy Workflow Guide | https://sleuthkit.org/autopsy/docs/user-docs/4.22.1/workflow_page.html |
| 52 | Autopsy Ingest Modules Guide | https://sleuthkit.org/autopsy/docs/user-docs/4.23.0/ingest_page.html |
| 53 | Sleuth Kit (TSK) Documentation | https://sleuthkit.org/sleuthkit/docs.php |
| 54 | Autopsy Downloads | https://sleuthkit.org/autopsy/download.php |
| 55 | TSK GitHub Repository | https://github.com/sleuthkit/sleuthkit |

### Malware Analysis & YARA

| # | Resource | URL |
|---|----------|-----|
| 56 | YARA Documentation | https://yara.readthedocs.io/en/stable/ |
| 57 | YARA Rules GitHub | https://github.com/Yara-Rules/rules |
| 58 | YARA — Malware Name Format | https://yara.readthedocs.io/en/stable/writingrules.html |
| 59 | Detect-It-Easy (DIE) | https://github.com/horsicq/Detect-It-Easy |
| 60 | PEfile (Python PE Parser) | https://github.com/erocarrera/pefile |
| 61 | VirusTotal | https://www.virustotal.com |
| 62 | ANY.RUN (Interactive Sandbox) | https://any.run |
| 63 | Hybrid Analysis | https://www.hybrid-analysis.com |
| 64 | Joe Sandbox | https://www.joesandbox.com |
| 65 | Cuckoo Sandbox | https://cuckoosandbox.org/ |
| 66 | PEview | https://www.ericzimmerman.com/ |
| 67 | CFF Explorer | https://ntcore.com/?page_id=388 |
| 68 | FLOSS (FireEye Obfuscated String Solver) | https://github.com/mandiant/flare-floss |

### Windows Forensic Artifacts

| # | Resource | URL |
|---|----------|-----|
| 69 | Ultimate Windows Security — Event ID Encyclopedia | https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/ |
| 70 | Microsoft — Windows Security Event ID Reference | https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/sentinel/windows-security-event-id-reference.md |
| 71 | EpicDetect — Event IDs Every SOC Analyst Should Know | https://epicdetect.io/blogs/windows-event-log-ids-soc-analysts |
| 72 | Microsoft — Sysmon Documentation | https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon |
| 73 | SwiftOnSecurity/sysmon-config | https://github.com/SwiftOnSecurity/sysmon-config |
| 74 | olafhartong/sysmon-modular | https://github.com/olafhartong/sysmon-modular |
| 75 | sbousseaden/EVTX-ATTACK-SAMPLES | https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES |
| 76 | Eric Zimmerman — Forensic Tools | https://ericzimmerman.github.io/ |
| 77 | KAPE (Kroll Artifact Parser Extractor) | https://www.kroll.com/en/services/cyber-security/investigate-and-respond/kape |
| 78 | Hayabusa — Event Log Forensics | https://github.com/Yamato-Security/hayabusa |
| 79 | Chainsaw — Fast Event Log Hunting | https://github.com/WithSecureLabs/chainsaw |
| 80 | EVTX Explorer | https://github.com/omerbsezer/EVTX-Explorer |

### MITRE ATT&CK

| # | Resource | URL |
|---|----------|-----|
| 81 | MITRE ATT&CK Official | https://attack.mitre.org |
| 82 | MITRE ATT&CK Navigator | https://mitre-attack.github.io/attack-navigator/ |
| 83 | MITRE ATT&CK — Enterprise Matrix | https://attack.mitre.org/matrices/enterprise/ |
| 84 | MITRE CAR (Cyber Analytics Repository) | https://car.mitre.org/ |
| 85 | Atomic Red Team | https://github.com/redcanaryco/atomic-red-team |
| 86 | MITRE D3FEND | https://d3fend.mitre.org/ |

### Incident Response Frameworks & Books

| # | Resource | URL |
|---|----------|-----|
| 87 | SANS — Incident Handler's Handbook | https://www.sans.org/white-papers/incident-handlers-handbook/ |
| 88 | SANS — PICERL IR Model | https://www.sans.org/white-papers/ |
| 89 | NIST SP 800-160 (Systems Security Engineering) | https://csrc.nist.gov/publications/detail/sp/800-160/vol-1/final |
| 90 | ITIL Foundation (AXELOS) | https://www.axelos.com/certifications/itil-service-management/ |
| 91 | Blue Team Handbook: Incident Response (3rd Ed.) | Don Murdoch |
| 92 | Applied Incident Response | Steve Anson |
| 93 | Incident Management for Operations | Rob Schnepp et al. |
| 94 | The Practice of Network Security Monitoring | Richard Bejtlich |
| 95 | Practical Malware Analysis | Michael Sikorski & Andrew Honig |
| 96 | The Art of Memory Forensics | Michael Ligh et al. |
| 97 | Investigating Windows Systems | Harlan Carvey |
| 98 | Digital Forensics and Incident Response (2nd Ed.) | Gerard Johansen |
| 99 | Windows Internals, Part 1 & 2 (7th Ed.) | Pavel Yosifovich et al. |

### Labs & Practice

| # | Resource | URL |
|---|----------|-----|
| 100 | Hack The Box — SOC Analyst Track | https://www.hackthebox.com |
| 101 | Blue Team Labs Online (BTLO) | https://blueteamlabs.online |
| 102 | LetsDefend | https://letsdefend.io |
| 103 | CyberDefenders | https://cyberdefenders.org |
| 104 | TryHackMe — DFIR Paths | https://tryhackme.com |
| 105 | RangeForce | https://rangeforce.com |
| 106 | Immersive Labs | https://www.immersivelabs.com |
| 107 | DetectionLab (Chris Long) | https://github.com/clong/DetectionLab |
| 108 | HELK (Hunting ELK) | https://github.com/Cyb3rWard0g/HELK |
| 109 | Sicura — Volatility Practice | https://sicura.us/ |

### Communities

| # | Resource | URL |
|---|----------|-----|
| 110 | r/IncidentResponse Reddit | https://reddit.com/r/IncidentResponse |
| 111 | OffSec Discord | https://discord.gg/offsec |
| 112 | OffSec Community Forums | https://forums.offsec.com |
| 113 | DFIR.Science | https://dfir.science |
| 114 | The DFIR Report | https://thedfirreport.com |
| 115 | SANS DFIR Community | https://www.sans.org/community/ |

### YouTube & Video

| # | Channel | Focus |
|---|---------|-------|
| 116 | 13Cubed | DFIR, memory forensics, Volatility tutorials |
| 117 | SANS Digital Forensics | Memory analysis, timeline analysis |
| 118 | OffSec Official | Course overviews, exam tips |
| 119 | IppSec | General cybersecurity methodology |
| 120 | John Hammond | Malware analysis, RE, IR |
| 121 | OALabs | Malware unpacking, RE |
| 122 | DFIR Science | Research-level DFIR content |

---

> **Catatan Akhir**: OSIR adalah sertifikasi incident response yang unik di industri — menggabungkan SIEM analysis (Splunk), disk forensics (Autopsy), memory forensics (Volatility 3), dan full IR lifecycle management. Fokus pada: (1) kuasai SPL — kecepatan query Splunk adalah kunci Phase 1, (2) praktik Volatility + Autopsy sampai hafal plugin utama, (3) report adalah 30/70 points — template report yang solid adalah investasi, (4) containment strategy harus realistis — jangan cuma "block IP", tapi tulis langkah konkret. Ingat: IR bukan hanya soal technical analysis — ini soal membuat keputusan cepat, komunikasi efektif, dan pemulihan sistem.
