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

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [Threat Hunting Mindset & Framework](#2-threat-hunting-mindset--framework)
3. [8 Module Deep-Dive](#3-8-module-deep-dive)
4. [Splunk SPL Hunting Queries Reference](#4-splunk-spl-hunting-queries-reference)
5. [CrowdStrike Falcon & CQL Reference](#5-crowdstrike-falcon--cql-reference)
6. [Network Hunting: Suricata, Zeek & PCAP Analysis](#6-network-hunting-suricata-zeek--pcap-analysis)
7. [Endpoint Hunting: Sysmon & Windows Event Logs](#7-endpoint-hunting-sysmon--windows-event-logs)
8. [Threat Intelligence Integration](#8-threat-intelligence-integration)
9. [Ransomware & APT Case Studies](#9-ransomware--apt-case-studies)
10. [Exam Strategy & Report Template](#10-exam-strategy--report-template)
11. [Referensi Lengkap](#11-referensi-lengkap)

---

## 1. Overview & Exam Structure

### Apa Itu TH-200 / OSTH?

TH-200 (Foundational Threat Hunting) adalah sertifikasi threat hunting dari OffSec yang mengajarkan **proactive threat detection** — mencari threat sebelum mereka menyebabkan damage. Berbeda dengan OSDA yang reaktif (deteksi dari SIEM alerts) dan OSIR yang berfokus pada incident response, OSTH mengajarkan bagaimana seorang threat hunter proaktif mencari adversary berdasarkan hipotesis, behavioral analysis, dan threat intelligence.

OSTH (OffSec Threat Hunter) adalah sertifikasi 100% praktikal — 8 jam proctored lab + 24 jam report window.

### Perbedaan OSTH vs OSDA vs OSIR

| Aspek | OSTH (TH-200) | OSDA (SOC-200) | OSIR (IR-200) |
|-------|---------------|----------------|---------------|
| **Level** | 200 (foundational) | 200 | 200 |
| **Fokus** | Proactive threat hunting | Detection & log analysis | Incident response & forensics |
| **Durasi exam** | 8 jam | 23h45m | 8 jam |
| **Report window** | 24 jam | 24 jam | 24 jam |
| **SIEM** | **Splunk** (SPL) | **ELK** (KQL) | **Splunk** (SPL) |
| **Endpoint tool** | CrowdStrike Falcon (CQL) | OSQuery | Autopsy + Volatility |
| **Network monitoring** | Suricata IDS/IPS, NetWitness | Tidak | Tidak |
| **Pendekatan** | Proaktif — hypothesis-driven | Reaktif — alert-driven | Reaktif — incident-driven |
| **Threat intel** | Threat intelligence report — WAJIB | Tidak | Tidak |
| **Cert expires** | **3 tahun** (recert needed) | **Tidak** | **3 tahun** |
| **Passing score** | 50/70 | 75/100 | 50/70 |
| **Soal exam** | 7 exercises × 10 pts | 10 phases × 10 pts | 6 exercises (4+2) |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Durasi exam** | 8 jam proctored |
| **Report deadline** | 24 jam setelah exam selesai |
| **Total exercises** | 7 exercises |
| **Points per exercise** | 10 points |
| **Total maksimum** | 70 points |
| **Passing score** | 50/70 |
| **Tools utama** | Splunk (SPL), CrowdStrike Falcon, Suricata |
| **Format laporan** | PDF — OSTH report template |
| **Upload** | OffSec Learning Portal (.7z) |

### Exam Environment

- **Proctoring**: Live proctor via webcam (screen share + room scan)
- **VPN**: Isolated OffSec VPN network — enterprise infrastructure simulation
- **SIEM**: Splunk Enterprise dengan Windows Event Logs, Sysmon, firewall logs
- **Endpoint**: CrowdStrike Falcon console untuk endpoint hunting
- **Network**: Suricata IDS logs, network PCAP
- **Tools**: Splunk SPL, CrowdStrike Query Language (CQL), Suricata rules
- **Input**: Threat intelligence report — IOC list, TTP description, APT group profile
- **Output**: Hunt Narrative — timeline, IOC table, impacted systems, evidence
- **Open book**: Semua sumber kecuali AI chatbots

### 8h Time Management Strategy

```
Hour 0-0:30: Initial recon
  - Read threat intelligence report thoroughly
  - Map IOCs to MITRE ATT&CK tactics
  - Identify critical systems in network topology

Hour 0:30-2: Broad Splunk queries
  - Search for IOCs from threat report
  - Identify initial access vector
  - Build timeline skeleton

Hour 2-4: Deep hunt — Network + Endpoint
  - Network: Suricata alerts, DNS logs, proxy logs
  - Endpoint: Process creation, registry, services
  - Correlate findings across data sources

Hour 4-5: Hypothesis-driven hunting
  - Refine hypotheses based on initial findings
  - Hunt for IoCs not in the threat report
  - Search for beaconing, lateral movement

Hour 5-6: CrowdStrike Falcon investigation
  - CQL queries for endpoint telemetry
  - Process tree analysis
  - Identify all compromised hosts

Hour 6-7: Complete all 7 exercise questions
  - Verify answers with MD5 hashes on Dev machine
  - Screenshot every query + result
  - Document timeline

Hour 7-8: Final review
  - Verify all 7 answers
  - Complete hunt narrative
  - Organize screenshots + evidence
  - Start report draft

Post-Exam (24h):
  - Complete professional hunt report
  - Executive summary + findings + timeline
  - IOCs table + impacted systems
  - Submit via OffSec portal
```

---

## 2. Threat Hunting Mindset & Framework

### Filosofi Dasar Threat Hunting

OSTH mengajarkan **"Hunt, Don't Just React"** — threat hunting adalah proactive security practice di mana defender aktif mencari threat, bukan menunggu alerts. Filosofi ini dibangun di atas tiga pilar:

1. **Hypothesis-Driven** — Setiap hunt dimulai dengan hipotesis: "Apa yang mungkin dilakukan adversary berdasarkan intel yang kita miliki?"
2. **Data-Driven** — Gunakan telemetry dari berbagai sumber (endpoint, network, SIEM) untuk mengkonfirmasi atau menolak hipotesis
3. **Continuous Improvement** — Setiap hunt menghasilkan insight baru yang memperkuat deteksi otomatis

### Golden Rules OSTH

1. **Start with the threat intel report** — The threat report is your compass. IOC list + TTP description + APT profile = what to hunt for.

2. **Think like an attacker** — Ask "if I were the adversary, what would I do next?" Then hunt for evidence of that.

3. **Correlate everything** — Single log = noise. Correlated logs across Splunk + CrowdStrike + Suricata = signal.

4. **Document as you hunt** — Timeline should grow as you find evidence. Don't leave it for the end.

5. **Splunk is your timeline, Falcon is your microscope** — Splunk gives breadth across all hosts; Falcon gives depth on specific endpoints.

6. **Hypotheses evolve** — Your initial hypothesis will change as you find evidence. That's normal. Refine and continue.

7. **The report is worth 70 points** — Screenshot everything. Every query, every result, every artifact.

### Threat Hunting Frameworks

#### PEAK Threat Hunting Framework (SANS)

PEAK adalah framework threat hunting modern dari SANS:

```
P — Plan & Prepare
  - Develop hypothesis based on threat intel
  - Identify data sources needed
  - Define success criteria

E — Execute Hunt
  - Run queries across SIEM + EDR
  - Analyze results, refine hypothesis
  - Document findings

A — Analyze Findings
  - Correlate across data sources
  - Determine scope and impact
  - Build timeline

K — Knowledge Sharing
  - Create hunt report
  - Update detection rules
  - Share TTP intelligence
```

#### CrowdStrike SEARCH Methodology

```
S — Sense
  - Collect broad telemetry from endpoints
  - Identify anomalous events and patterns

E — Enrich
  - Contextualize data with threat intelligence
  - Correlate with known adversary TTPs

A — Analyze
  - Form and test hypotheses
  - Use statistical methods + human intuition

R — Reconstruct
  - Build complete attack narrative
  - Timeline + scope + impact

C — Communicate
  - Deliver actionable findings to responders
  - Clear, accurate, timely

H — Hone
  - Improve automated detections
  - Feed insights back into hunting process
```

#### Cyber Kill Chain (Lockheed Martin)

```
Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives
```

Gunakan Kill Chain untuk:
- **Executive summary**: High-level attack narrative
- **Detection gaps**: Identify which phases had monitoring blind spots
- **Containment priority**: Earlier in the chain = better containment opportunity

#### MITRE ATT&CK Framework

OSTH menekankan mapping setiap temuan ke MITRE ATT&CK:

```
Initial Access (TA0001): T1566 Phishing, T1190 Exploit Public-Facing App
Execution (TA0002): T1059 Command & Scripting, T1204 User Execution
Persistence (TA0003): T1543 Create/Modify System Process, T1136 Create Account
Privilege Escalation (TA0004): T1055 Process Injection, T1068 Exploitation
Defense Evasion (TA0005): T1562 Impair Defenses, T1070 Indicator Removal
Credential Access (TA0006): T1003 OS Credential Dumping
Discovery (TA0007): T1087 Account Discovery, T1069 Permission Discovery
Lateral Movement (TA0008): T1021 Remote Services, T1550 Use Alternate Auth Material
Collection (TA0009): T1005 Data from Local System
C2 (TA0011): T1071 Application Layer Protocol, T1573 Encrypted Channel
Exfiltration (TA0010): T1048 Exfiltration Over Alternative Protocol
Impact (TA0040): T1486 Data Encrypted for Impact
```

#### Diamond Model

```
Adversary → Infrastructure → Capability → Victim
```

Gunakan Diamond Model untuk:
- **Intel analysis**: Hubungkan setiap event ke 4 komponen
- **Attribution**: Identifikasi pola yang menunjuk ke APT group tertentu
- **Hunt expansion**: Dari satu komponen, cari yang lain (e.g., dari IP C2, cari victims lain)

### Hypothesis Development

Setiap hunt dimulai dengan hipotesis yang terstruktur:

```
Format:
  "Adversary [TTP] on [system] using [technique] to achieve [goal]"

Contoh:
  "Adversary is using PowerShell encoded commands on WEB01 to establish persistence"
  "Adversary is exfiltrating data via DNS tunneling through the proxy server"
  "Adversary moved laterally from WORKSTATION-01 to DC-01 using Pass-the-Hash"
```

### Three Types of Threat Hunting

| Type | Description | Example |
|------|-------------|---------|
| **Intel-Based** | Hunt using known IOCs from threat intel | Search for IP/Domain/Hash from threat report |
| **Hypothesis-Driven** | Hunt based on TTP hypotheses | "If APT29 is targeting us, they might use PowerShell + Dropbox C2" |
| **Baseline/Anomaly** | Hunt deviations from normal | "Why is this server making outbound connections at 3 AM?" |

### 3 Pertanyaan Kunci Saat Stuck

1. **"What does the threat intel report tell me?"** — Re-read the report. What IOCs did you miss? What TTPs haven't you searched for?
2. **"Where else could the adversary be?"** — Check lateral movement. If they were on Host A, what other hosts could they reach?
3. **"What data haven't I checked yet?"** — Splunk logs? CrowdStrike telemetry? Network logs? DNS logs? Proxy logs?

---

## 3. 8 Module Deep-Dive

TH-200 memiliki 8 modul (6 modul inti + Challenge Lab + Azure module).

### Modul 1: Threat Hunting Concepts and Practices

Pengenalan threat hunting fundamental:

**Core Concepts:**
- **Threat hunting definition**: Proactive search for threats that evade existing security controls
- **Hunter mindset**: Curiosity, creativity, analytical rigor, attention to detail
- **Hunt types**: Intel-based, hypothesis-driven, baselining/anomaly detection

**Enterprise Threat Hunting Program:**
- **Maturity model**:
  - Level 1: Initial (ad-hoc, reactive)
  - Level 2: Defined (structured processes)
  - Level 3: Managed (metrics-driven, automated)
  - Level 4: Optimizing (continuous improvement, AI-assisted)
- **Team structure**: Embedded in SOC, dedicated hunt team, or hybrid
- **Tools**: SIEM (Splunk), EDR (CrowdStrike), NDR (Suricata), TI platform (MISP)

**Hunt Lifecycle:**
```
1. Trigger → 2. Hypothesis → 3. Data Collection → 
4. Analysis → 5. Findings → 6. Response → 7. Feedback
```

**Mindset**: Threat hunting bukan "search for bad stuff" — ini adalah scientific method applied to security. Hypothesis → Test → Analyze → Conclusion.

### Modul 2: Threat Actor Landscape Overview

Memahami adversary landscape:

**Threat Actor Types:**

| Type | Motivation | Examples |
|------|------------|----------|
| **Nation-State (APTs)** | Espionage, sabotage, geopolitical | APT29 (Cozy Bear), APT41 (Winnti), Lazarus |
| **Cybercrime / eCrime** | Financial gain | LockBit, CLOP, BlackCat/ALPHV |
| **Hacktivists** | Ideological, political | Anonymous, Killnet |
| **Insider Threats** | Financial, revenge, espionage | Disgruntled employees, moles |
| **Terrorist Groups** | Propaganda, disruption | ISIS-affiliated hackers |

**Ransomware Ecosystem:**

```
Initial Access Brokers → Ransomware Group → Affiliates → 
  - Data exfiltration team
  - Negotiation team
  - Leak site operators
```

**Ransomware Groups Deep-Dive:**

**LockBit (LockBit 3.0):**
- RaaS (Ransomware-as-a-Service) model
- Initial access: RDP brute force, phishing, VPN vulnerabilities
- Encryption: AES + RSA, fast encryption
- Exfiltration: StealBit custom exfiltration tool
- TTPs: PsExec lateral movement, GPO-based deployment

**CLOP (CVE-2023-34362 exploitation):**
- Known for MOVEit Transfer exploitation (2023)
- Initial access: Web application vulnerabilities
- TTPs: Web shell deployment, data exfiltration via HTTP
- Notable attack: MOVEit mass exploitation affecting thousands

**BlackCat/ALPHV:**
- First Rust-based ransomware family
- RaaS model with affiliates
- Initial access: VPN vulnerabilities, phishing
- Encryption: Rust, multi-threaded, fast
- TTPs: PowerShell, WMI, PsExec

**APT Groups:**

| Group | Attribution | Focus | Notable TTPs |
|-------|-------------|-------|--------------|
| APT29 (Cozy Bear) | Russia (SVR) | Government, think tanks | PowerShell, C2 via cloud APIs |
| APT41 (Winnti) | China | Gaming, tech, pharma | DLL side-loading, custom backdoors |
| Lazarus | North Korea | Financial, crypto | macOS malware, supply chain attacks |
| MuddyWater | Iran (MSS) | Middle East | PowerShell, VBS, living-off-the-land |
| FIN7 | Russia (eCrime) | Retail, hospitality | Spear phishing, Carbanak backdoor |

### Modul 3: Communication and Reporting for Threat Hunters

Komunikasi dan reporting:

**Traffic Light Protocol (TLP):**
- **TLP:RED** — Hanya untuk individu yang disebutkan (end-to-end)
- **TLP:AMBER** — Terbatas pada organisasi penerima
- **TLP:GREEN** — Terbatas pada komunitas
- **TLP:CLEAR** — Bisa dibagikan secara publik

**Threat Intelligence Reports:**
- **Strategic**: Executive-level, risk-focused
- **Operational**: Tactical planning, campaign-focused
- **Tactical**: IoCs, TTPs, technical indicators
- **Technical**: Raw data, hashes, IPs, domains

**Hunt Narrative Structure:**
```
1. Executive Summary
2. Hypothesis & Methodology
3. Data Sources Used
4. Findings (Timeline + Evidence)
5. Impact Assessment
6. IOCs Table
7. Recommendations
8. MITRE ATT&CK Mapping
```

**Communication Best Practices:**
- **To management**: Business impact, risk level, containment status
- **To SOC**: Technical details, queries used, detection rules
- **To IT**: Affected systems, patches needed, configuration changes
- **To legal**: Regulatory implications, data exposure

### Modul 4: Hunting with Network Data

Menggunakan network telemetry untuk threat hunting:

**Network Data Sources:**
- **NetFlow/IPFIX**: Flow metadata (src/dst IP, ports, bytes, duration)
- **DNS logs**: Query names, response IPs, query types
- **Proxy logs**: URLs, user agents, response codes, content types
- **IDS/IPS alerts**: Suricata rules triggered
- **Firewall logs**: Connection attempts, blocked traffic
- **PCAP**: Full packet capture (deep analysis)
- **NetWitness**: Packet + log correlation

**Suricata IDS/IPS:**
- Open-source IDS/IPS engine
- Rule-based detection using emerging threats rules
- Protocol detection: HTTP, DNS, TLS, SMB
- File extraction: Extract files from network streams

**Key Suricata Rule Fields:**
```
alert tcp $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS
(msg:"Suspicious User-Agent"; content:"|0d 0a|User-Agent: curl/"; 
 sid:1000001; rev:1;)
```

**Common Network Hunting Scenarios:**

**C2 Detection:**
```spl
index=proxy sourcetype=proxylogs
| stats count, dc(dest_ip) as UniqueDests, values(dest_ip) by src_ip
| where count > 100 AND UniqueDests < 3
| eval beacon_ratio = count / UniqueDests
```

**DNS Tunneling:**
```spl
index=dns sourcetype=dns
| eval domain_length = len(query)
| where domain_length > 50
| stats count by query, src_ip
| sort - count
```

**Data Exfiltration via HTTP:**
```spl
index=proxy sourcetype=proxylogs
| stats sum(bytes_out) as TotalBytes by src_ip, dest_ip
| where TotalBytes > 10000000
| sort - TotalBytes
```

**Suricata Alert Triage:**
```spl
index=suricata sourcetype=suricata:alert
| stats count by alert_category, alert_severity, src_ip, dest_ip
| sort - count
```

**Zeek (formerly Bro) Logs:**
- `conn.log`: Connection summaries
- `dns.log`: DNS queries
- `http.log`: HTTP requests
- `ssl.log`: TLS certificates
- `files.log`: File extraction metadata

### Modul 5: Hunting on Endpoints

Menggunakan endpoint telemetry:

**Endpoint Data Sources:**
- **Sysmon**: Process creation, network connections, file changes, registry
- **Windows Event Log**: Security (4624, 4625, 4688), System (7045), PowerShell (4104)
- **EDR telemetry**: CrowdStrike Falcon — process tree, command line, file access
- **Process creation**: Parent-child relationships, command line arguments
- **File system**: Creation, modification, deletion patterns
- **Registry**: Run keys, service entries, persistence mechanisms

**Intel-Based Hunting:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*Invoke-Mimikatz*" OR CommandLine="*sekurlsa*"
| table _time, Account, CommandLine, ComputerName
```

**Hypothesis-Driven Hunting:**
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(winword|excel|powerpnt|outlook)")
  AND match(Image, "(?i)(powershell|wscript|cscript|cmd)")
| table _time, ComputerName, User, ParentImage, Image, CommandLine
```

**Lateral Movement Detection:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=3
| search AccountName!="ANONYMOUS LOGON$"
| search AccountName!="SYSTEM"
| stats count by AccountName, ComputerName, src_ip
| sort - count
```

**Service Creation (Persistence):**
```spl
index=windows sourcetype=WinEventLog:System EventCode=7045
| search ServiceName!="*Microsoft*"
| lookup service_baseline.csv ServiceName OUTPUT NewInstall
| where isnull(NewInstall)
| table _time, ComputerName, ServiceName, ImagePath, Account
```

### Modul 6: Threat Hunting without IoCs

Hunting tanpa indicator yang diketahui:

**Behavioral Analysis:**
- Focus on **behavior** not specific indicators
- Look for deviations from normal baselines
- Identify TTPs, not just IoCs

**CrowdStrike Falcon for Behavioral Hunting:**
- Process tree analysis
- Unusual parent-child relationships
- Suspicious command line patterns
- Anomalous network connections

**CQL for Behavioral Hunts:**

Unusual parent-child:
```
event_simpleName=ProcessRollup2
| eval ChildProcess = FileName, ParentProcess = ParentBaseFileName
| search ParentProcess IN ("winword.exe", "excel.exe", "outlook.exe")
  AND ChildProcess IN ("powershell.exe", "cmd.exe", "wscript.exe")
```

Suspicious execution paths:
```
event_simpleName=ProcessRollup2
| search FilePath=*\\Users\\*\\AppData\\Local\\Temp\\*
| table ComputerName, UserName, FileName, FilePath, CommandLine
```

Beaconing detection:
```
event_simpleName=NetworkConnectIP4
| stats count by ComputerName, RemoteAddressIP4, RemotePort
| where count > 50 AND count < 2000
| eval beacon_ratio = round(count / 4)
```

**Hypothesis Development without IoCs:**
```
"If an attacker compromised the domain controller, they would:
1. Create a new domain admin account (4720 + 4728)
2. Use DCSync to extract hashes (4662 on DS-Replication-Get-Changes)
3. Dump NTDS.dit via ntdsutil

→ Hunt for these behaviors without any prior IoCs"
```

### Modul 7: Threat Hunting Challenge Labs

Challenge Lab adalah simulasi full-scale threat hunt yang mirror image dari exam:

**Lab Structure:**
- Realistic enterprise network with multiple hosts
- Pre-recorded attacker actions spanning Kill Chain phases
- Splunk instance with ingested logs
- CrowdStrike Falcon console for endpoint telemetry
- Threat intelligence report provided

**Strategi Challenge Lab:**
1. Treat it like the real exam — document everything
2. Practice building the hunt narrative in real-time
3. Time yourself — complete in under 8 hours
4. Write the full report after each attempt
5. Repeat until you can complete all 7 questions

**Labs Available:**
- Challenge Lab 1: Basic hunt — single threat actor, limited scope
- Challenge Lab 2: Advanced hunt — multiple TTPs, lateral movement
- (Additional labs as updated by OffSec)

### Modul 8: Threat Hunting in Azure (New Module)

(Modul baru yang ditambahkan oleh OffSec setelah course rilis)

**Azure Threat Hunting:**
- **Azure AD sign-in logs**: Failed logins, MFA failures, conditional access
- **Azure Activity logs**: Resource creation, RBAC changes, policy changes
- **Azure Security Center alerts**: Integrated threat detection
- **Microsoft 365 Defender**: Cross-domain hunting

**KQL for Azure Hunting:**
```
SigninLogs
| where ResultType != "0"
| summarize FailedCount = count() by UserPrincipalName, IPAddress
| where FailedCount > 10
```

**Cloud-Specific TTPs:**
- T1078.004: Cloud Account — Valid accounts in Azure
- T1525: Implant Internal Image — Compromised VM images
- T1613: Container and Resource Discovery — Azure resource enumeration
- T1530: Data from Cloud Storage — Azure Blob access

---

## 4. Splunk SPL Hunting Queries Reference

### SPL Fundamentals for Threat Hunting

**Pipeline Model:**
```
index=<index> sourcetype=<sourcetype> earliest=<time> latest=<time>
| <command1> [options]
| <command2> [options]
| table <fields>
```

**Core Commands:**

| Command | Function | Hunting Use |
|---------|----------|-------------|
| `index=` | Select data source | Always specify index first |
| `sourcetype=` | Filter by log type | Narrow to specific log source |
| `stats` | Aggregate & count | Count occurrences by field |
| `eval` | Create calculated fields | Score risk, flag anomalies |
| `rex` | Regex field extraction | Extract IPs, domains from raw logs |
| `transaction` | Group related events | Session analysis |
| `timechart` | Time-series visualization | Beaconing pattern detection |
| `streamstats` | Running calculations | Time-based anomaly detection |
| `lookup` | Enrich from reference | Threat intel enrichment |
| `table` | Select output columns | Clean output for analysis |
| `where` | Eval-based filter | Conditional filtering |
| `sort` | Sort results | Prioritize findings |
| `dedup` | Remove duplicates | Unique IOC list |
| `inputlookup` | Read lookup table | Threat intel CSV ingestion |

### Initial Access Detection

**Phishing — Suspicious Attachment:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*.exe*" ParentProcessName="*OUTLOOK.EXE*"
| table _time, ComputerName, Account, CommandLine
```

**Web Shell Detection:**
```spl
index=iis sourcetype=WinEventLog:IIS
| search cs_uri_stem="*.aspx*" OR cs_uri_stem="*.php*" 
  AND cs_method="POST"
| stats count by cs_uri_stem, c_ip, cs_username
| sort - count
```

**RDP Brute Force:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4625 LogonType=10
| stats count as FailedCount, dc(Account) as UniqueAccounts by src_ip, ComputerName
| where FailedCount > 20
| sort - FailedCount
```

### Execution Detection

**PowerShell Encoded Command:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*-enc*" OR CommandLine="*-EncodedCommand*"
| table _time, ComputerName, Account, CommandLine, ParentProcessName
```

**PowerShell Script Block Logging (Event 4104):**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" EventCode=4104
| search ScriptBlockText="*DownloadString*" OR ScriptBlockText="*IEX*" OR ScriptBlockText="*Invoke-*"
| table _time, ComputerName, Account, ScriptBlockText
```

**Sysmon Process Creation (Event 1) — Suspicious:**
```spl
index=sysmon EventCode=1
| search CommandLine="*mimikatz*" OR CommandLine="*Invoke-*" OR CommandLine="*-enc*"
| table _time, ComputerName, User, CommandLine, ParentCommandLine
```

### Persistence Detection

**Scheduled Task Creation (Event 4698):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4698
| search NOT TaskName="*Microsoft*"
| table _time, ComputerName, Account, TaskName, Command
```

**Service Installation (Event 7045):**
```spl
index=windows sourcetype=WinEventLog:System EventCode=7045
| search ImagePath="*\\Users\\*" OR ImagePath="*\\Temp\\*"
| table _time, ComputerName, ServiceName, ImagePath, Account
```

**Registry Run Key Modification:**
```spl
index=sysmon EventCode=13
| search TargetObject="*\\CurrentVersion\\Run*"
| table _time, ComputerName, User, TargetObject, Details
```

### Credential Access Detection

**LSASS Access (Sysmon 10):**
```spl
index=sysmon EventCode=10
| search TargetImage="*\\lsass.exe"
| where NOT match(SourceImage, "(?i)(svchost|MsMpEng|WerFault|taskmgr|csrss)")
| table _time, ComputerName, SourceImage, SourceUser, GrantedAccess
```

**Mimikatz Detection:**
```spl
index=windows
| search CommandLine="*sekurlsa*" OR CommandLine="*logonpasswords*" 
  OR CommandLine="*privilege::debug*"
| table _time, ComputerName, Account, CommandLine
```

**DCSync Detection (Event 4662):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4662
| search ObjectType="%19195a5b-6da0-11d0-afd3-00c04fd930c7"  // DS-Replication-Get-Changes
  AND AccessMask="0x100"
| table _time, ComputerName, Account, ObjectName
```

### Lateral Movement Detection

**Pass-the-Hash (Event 4624 Type 3 + NTLM):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=3
| search LogonProcessName="NtLmSsp" AND AccountName!="ANONYMOUS LOGON$"
| stats count by AccountName, ComputerName, WorkstationName, src_ip
| sort - count
```

**PsExec Execution:**
```spl
index=sysmon EventCode=1
| search Image="*\\PSEXESVC.exe" OR ParentImage="*\\PsExec.exe"
| table _time, ComputerName, User, Image, CommandLine
```

**WMI Remote Execution:**
```spl
index=sysmon EventCode=1
| search ParentImage="*\\WmiPrvSE.exe" AND Image="*\\powershell.exe"
| table _time, ComputerName, User, CommandLine
```

**RDP Logons (Event 4624 Type 10):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=10
| search NOT AccountName="*$"
| table _time, ComputerName, AccountName, src_ip
| sort - _time
```

### C2 Detection

**Beaconing — Regular Intervals:**
```spl
index=proxy sourcetype=proxylogs
| stats count, avg(eval(floor(_time/300)*300)) as bucket_avg by src_ip, dest_ip
| where count > 100 AND count < 5000
| eval regularity = round(bucket_avg, 0)
| sort - count
```

**DNS Queries to DGA Domains:**
```spl
index=dns sourcetype=dns
| eval domain_len = len(query)
| where domain_len > 25
| stats count by query, src_ip
| where count > 5
| sort - count
```

**Sysmon Network Connection (Event 3) — Non-Internal:**
```spl
index=sysmon EventCode=3
| search NOT DestIp=10.* AND NOT DestIp=192.168.* AND NOT DestIp=172.1[6-9].* AND NOT DestIp=172.2[0-9].* AND NOT DestIp=172.3[0-1].*
| stats count by ComputerName, DestIp, DestPort, Image
| sort - count
```

### Exfiltration Detection

**Large Data Transfer:**
```spl
index=proxy sourcetype=proxylogs
| stats sum(bytes_out) as TotalBytes, max(bytes_out) as MaxBytes by src_ip, dest_ip
| where TotalBytes > 50000000
| eval TotalMB = round(TotalBytes/1048576, 2)
| sort - TotalBytes
```

**DNS TXT Query Exfiltration:**
```spl
index=dns sourcetype=dns query_type=TXT
| stats count by query, src_ip
| where len(query) > 50
| sort - count
```

### Threat Hunting Queries

**Unusual Parent-Child Processes:**
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(winword|excel|powerpnt|outlook|acrord32|firefox|chrome)")
  AND match(Image, "(?i)(powershell|wscript|cscript|cmd|mshta|regsvr32)")
| table _time, ComputerName, User, ParentImage, Image, CommandLine
```

**Executable Downloaded to User Space:**
```spl
index=sysmon EventCode=11
| search TargetFilename="*\\Users\\*\\*.exe"
| where TargetFilename!="*OneDrive*"
| table _time, ComputerName, User, TargetFilename, Image
```

**Account Created then Added to Admin Group:**
```spl
index=windows sourcetype=WinEventLog:Security
| search EventCode=4720 OR EventCode=4732
| transaction AccountName maxpause=1h
| where mvcount(EventCode) > 1
| table _time, AccountName, TargetAccountName, EventCode
```

**Kerberoasting Detection:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4769
| search TicketEncryptionType=0x17 ServiceName!="*$"
| stats count by AccountName, ServiceName, ClientAddress
| where count > 5
| sort - count
```

**Golden Ticket Detection (Event 4624 + 4672):**
```spl
index=windows sourcetype=WinEventLog:Security
| search EventCode=4624 AccountName="Administrator" LogonType=3
  OR EventCode=4672 AccountName="Administrator"
| stats count by AccountName, ComputerName, src_ip
```

**Time-Based Anomaly — Logons Outside Business Hours:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624
| eval hour = strftime(_time, "%H")
| where hour < 6 OR hour > 18
| stats count by AccountName, ComputerName, src_ip
| where count > 10
```

**New Process Followed by Network Connection:**
```spl
index=sysmon
| search EventCode=1 OR EventCode=3
| sort _time
| transaction ComputerName, Image maxpause=1m
| where mvcount(EventCode) > 1 AND mvfind(EventCode, "1")=0 AND mvfind(EventCode, "3")=1
| table _time, ComputerName, Image, CommandLine, DestIp, DestPort
```

**SPL Performance Tips for Hunting:**
- Always specify `index=` and `sourcetype=` first
- Use specific time ranges (`earliest=-24h@h latest=now`)
- Filter early in the pipeline
- Use `tstats` for CIM data model acceleration
- Avoid wildcards at the start of strings
- Use `head 100` to test expensive queries before running full scope

---

## 5. CrowdStrike Falcon & CQL Reference

### CrowdStrike Falcon Platform Overview

CrowdStrike Falcon adalah cloud-native EDR platform yang menyediakan:
- **Endpoint visibility**: Process creation, network connections, file operations, registry
- **Threat intelligence**: Integrated with CrowdStrike's global threat graph
- **IOA detection**: Behavioral-based detection (Indicator of Attack)
- **CQL**: CrowdStrike Query Language for custom hunting

### CrowdStrike Query Language (CQL)

CQL is Splunk-like query language for Falcon event data:

**Basic CQL Syntax:**
```
event_simpleName=<event_type> 
| <command1> [options]
| <command2> [options]
| table <field1>, <field2>
```

**Common Event Types:**

| Event | Description |
|-------|-------------|
| `ProcessRollup2` | Process creation |
| `NetworkConnectIP4` | IPv4 network connection |
| `NetworkListenIP4` | Listening for connections |
| `DnsRequest` | DNS query |
| `SyntheticProcessRollup2` | Process termination |
| `PeFileWritten` | PE file written to disk |

**Process Hunting Queries:**

Find all PowerShell executions:
```
event_simpleName=ProcessRollup2 FileName="powershell.exe"
| table ComputerName, UserName, CommandLine, ParentBaseFileName
```

Find encoded PowerShell:
```
event_simpleName=ProcessRollup2 FileName="powershell.exe"
| search CommandLine=*-enc*
| table ComputerName, UserName, CommandLine
```

Find processes with suspicious parents:
```
event_simpleName=ProcessRollup2
| eval ChildProcess = FileName, ParentProcess = ParentBaseFileName
| search ParentProcess IN ("winword.exe", "excel.exe", "powerpnt.exe")
  AND ChildProcess IN ("powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe")
```

**Network Hunting Queries:**

External network connections:
```
event_simpleName=NetworkConnectIP4
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
| stats count by ComputerName, RemoteAddressIP4, RemotePort
| sort - count
```

Beaconing detection via CQL:
```
event_simpleName=NetworkConnectIP4
| eval bucket = floor(_time / 300) * 300
| stats count, values(RemoteAddressIP4) as IPs by ComputerName
| where count > 20 AND count < 500
| eval regularity = round(count / 4)
```

DNS queries to suspicious domains:
```
event_simpleName=DnsRequest
| eval domain_len = len(DomainName)
| where domain_len > 30
| stats count by ComputerName, DomainName
| sort - count
```

**File System Hunting:**

Executable written to user space:
```
event_simpleName=PeFileWritten
| search FilePath=*\\Users\\*\\*.exe
| eval IsSuspicious = if(FilePath LIKE "*\\AppData\\Local\\Temp\\*", "HIGH", "MEDIUM")
| table ComputerName, UserName, FileName, FilePath, IsSuspicious
```

**IOA (Indicator of Attack) Hunting:**

Falcon IOAs provide behavioral detection:
- **Process Injection**: Remote thread creation in lsass
- **Credential Dumping**: LSASS access by non-system process
- **Ransomware**: Mass file encryption events
- **Persistence**: Unusual service creation

Query IOAs:
```
event_simpleName=IndicatorOfAttackEvent
| table ComputerName, UserName, Severity, Description, PatternName
| sort - Severity
```

### CrowdStrike SEARCH Methodology in CQL

**S — Sense**: Broad queries to find interesting events
```
event_simpleName=ProcessRollup2
| stats count by ComputerName, FileName
| sort - count
```

**E — Enrich**: Add context to events
```
event_simpleName=NetworkConnectIP4
| lookup geo_ip_table.csv RemoteAddressIP4 OUTPUT country, city
| stats count by country, RemoteAddressIP4
```

**A — Analyze**: Hypothesis-driven queries
```
event_simpleName=ProcessRollup2
| search ParentBaseFileName="explorer.exe" 
  AND FileName IN ("powershell.exe", "cmd.exe")
| eval Suspicious = if(CommandLine LIKE "*IEX*" OR CommandLine LIKE "*-enc*", "YES", "NO")
| where Suspicious = "YES"
```

### CQL Performance Tips
- Filter early using indexed fields like `event_simpleName`
- Use `stats` functions instead of `table` for large datasets
- Limit time range to reduce data scanned
- Use `eval` for computed fields rather than `rex` when possible

---

## 6. Network Hunting: Suricata, Zeek & PCAP Analysis

### Suricata IDS/IPS

Suricata adalah open-source IDS/IPS engine:

**Rule Structure:**
```
action protocol src_ip src_port -> dst_ip dst_port
(msg:"message"; content:"pattern"; sid:1000001; rev:1;)
```

**Key Rule Categories:**
- **ET (Emerging Threats)**: Community + Pro rulesets
- **Protocol anomalies**: Non-standard protocol behavior
- **File extraction**: Extract malware from network streams
- **DNS detection**: DGA, tunneling, unusual query types

**Hunting with Suricata Alerts:**

High severity alerts:
```spl
index=suricata sourcetype=suricata:alert alert_severity=1
| stats count by alert_category, src_ip, dest_ip
| sort - count
```

Alerts by target:
```spl
index=suricata sourcetype=suricata:alert
| stats count by dest_ip, alert_category
| sort - count
```

Alerts by signature:
```spl
index=suricata sourcetype=suricata:alert
| stats count by alert_signature, src_ip
| sort - count
```

### Zeek (formerly Bro)

Zeek provides high-level network analysis:

**conn.log — Suspicious Connections:**
```spl
index=zeek sourcetype=zeek:conn
| where duration > 3600 AND orig_bytes > 10000000
| table ts, id.orig_h, id.resp_h, proto, duration, orig_bytes
```

**dns.log — Unusual Queries:**
```spl
index=zeek sourcetype=zeek:dns
| eval query_len = len(query)
| where query_len > 40
| table ts, id.orig_h, query, qtype_name
```

**http.log — Suspicious User-Agents:**
```spl
index=zeek sourcetype=zeek:http
| search user_agent="curl*" OR user_agent="wget*" OR user_agent="python*"
| table ts, id.orig_h, id.resp_h, uri, user_agent
```

**ssl.log — Suspicious Certificates:**
```spl
index=zeek sourcetype=zeek:ssl
| search NOT server_name="*" 
| stats count by id.orig_h, id.resp_h
| where count > 5
```

### Network IOC Hunting

**Known Bad IP/Domain:**
```spl
index=* 
| search src_ip IN ("<malicious_ip>") OR dest_ip IN ("<malicious_ip>")
  OR query IN ("<malicious_domain>")
| table _time, src_ip, dest_ip, query, sourcetype
```

**Unusual Port/Protocol:**
```spl
index=*
| search port=4444 OR port=8443 OR port=1337 OR port=31337
| stats count by src_ip, dest_ip, dest_port
```

**Protocol Mismatch:**
```spl
| search sourcetype=dns AND dest_port=80
  OR sourcetype=http AND dest_port=53
```

---

## 7. Endpoint Hunting: Sysmon & Windows Event Logs

### Sysmon Event IDs for Threat Hunting

| Event ID | Event Name | Hunting Use |
|----------|------------|-------------|
| 1 | Process creation | Track execution, parent-child analysis |
| 3 | Network connection | C2 detection, beaconing |
| 7 | Image loaded | DLL injection, process hollowing |
| 8 | CreateRemoteThread | Process injection |
| 9 | Raw access read | LSASS dumping (mimikatz) |
| 10 | Process access | Credential dumping |
| 11 | File create | Malware drop, ransomware |
| 12/13/14 | Registry events | Persistence (Run keys) |
| 15 | File stream | ADS execution, hidden malware |
| 17/18 | Named pipe | Inter-process communication, C2 |
| 22 | DNS query | DGA, C2 domain resolution |

### Windows Security Event IDs

| Event ID | Event Name | Hunting Use |
|----------|------------|-------------|
| 4624 | Logon success | Track access, lateral movement |
| 4625 | Logon failure | Brute force detection |
| 4634 | Logoff | Session tracking |
| 4648 | Explicit logon | RunAs, scheduled task context |
| 4662 | Directory access | DCSync detection |
| 4663 | Object access | File access auditing |
| 4672 | Admin logon | Privilege escalation |
| 4688 | Process creation | Execution tracking |
| 4698 | Scheduled task | Persistence |
| 4700/4701 | Scheduled task enable/disable | Defense evasion |
| 4719 | Audit policy change | Defense evasion |
| 4720 | User account created | Backdoor account |
| 4728/4732/4756 | Group membership change | Admin escalation |
| 4768/4769 | Kerberos TGT/TGS | Kerberoasting, Golden Ticket |
| 4776 | Credential validation | Pass-the-hash detection |
| 7045 | Service installed | Persistence |
| 4104 | PowerShell script block | PowerShell abuse |

### Sysmon Configuration

SwiftOnSecurity sysmon-config adalah community standard:

```xml
<Sysmon schemaversion="4.22">
  <EventFiltering>
    <!-- Process Creation (Event 1) -->
    <RuleGroup name="" groupRelation="or">
      <ProcessCreate onmatch="include">
        <CommandLine condition="contains">powershell</CommandLine>
        <CommandLine condition="contains">wscript</CommandLine>
        <CommandLine condition="contains">cscript</CommandLine>
      </ProcessCreate>
    </RuleGroup>
    <!-- Network Connection (Event 3) -->
    <RuleGroup name="" groupRelation="or">
      <NetworkConnect onmatch="exclude">
        <Image condition="image">C:\Windows\System32\svchost.exe</Image>
        <DestinationIp condition="is">127.0.0.1</DestinationIp>
      </NetworkConnect>
    </RuleGroup>
  </EventFiltering>
</Sysmon>
```

### Advanced Endpoint Hunting Patterns

**Process Tree Reconstruction:**
```spl
index=sysmon EventCode=1
| search ComputerName="suspected_host"
| table _time, User, Image, CommandLine, ParentImage, ProcessGuid
| sort _time
```

**DLL Loaded from Suspicious Path:**
```spl
index=sysmon EventCode=7
| search ImageLoaded="*\\Users\\*" AND Image="*\\svchost.exe"
| stats count by ComputerName, ImageLoaded, Image
```

**Named Pipe — Interprocess Communication:**
```spl
index=sysmon EventCode=17
| search PipeName="*\\*"
| table _time, ComputerName, User, PipeName, Image
```

**Raw Disk Access:**
```spl
index=sysmon EventCode=9
| table _time, ComputerName, Image, Device
```

---

## 8. Threat Intelligence Integration

### Intelligence Lifecycle

```
1. Requirements → 2. Collection → 3. Processing → 
4. Analysis → 5. Dissemination → 6. Feedback
```

### IOC Types

| Type | Example | Hunting Method |
|------|---------|---------------|
| **Hash (SHA256/MD5)** | a1b2c3... | Hash lookup across endpoints |
| **IP Address** | 185.234.72.1 | Network connection logs |
| **Domain** | evil-malware.xyz | DNS logs, proxy logs |
| **URL** | http://evil.com/payload.exe | Proxy logs, web logs |
| **Registry key** | HKLM\...\Run\Malware | Registry auditing |
| **File path** | C:\Users\*\AppData\... | File creation monitoring |
| **Named pipe** | \\.\pipe\srvsvc | Named pipe events (Sysmon 17) |
| **YARA rule** | rule SuspiciousPS {...} | YARA scan on endpoints |

### Integrating Threat Intel into Splunk

**Using inputlookup for IOC Matching:**
```spl
| inputlookup threat_intel_iocs.csv
| search ioc_type="ip"
| rename ioc as dest_ip
| append [search index=* earliest=-7d]
| stats values(ioc_type) as matching_types by dest_ip, src_ip
| where isnotnull(matching_types)
```

**DNS IOC Matching:**
```spl
| inputlookup threat_intel_domains.csv
| search sourcetype=dns
| rename query as ioc
| stats count by query, src_ip
```

**Hash IOC Matching:**
```spl
| inputlookup threat_intel_hashes.csv
| search sourcetype=sysmon EventCode=1
| eval file_hash = sha256(Image)
| where file_hash IN [| inputlookup threat_intel_hashes.csv | fields ioc]
```

### STIX/TAXII Overview

- **STIX** (Structured Threat Information Expression): Standard format for CTI data
- **TAXII** (Trusted Automated eXchange of Indicator Information): Transport protocol

**STIX 2.1 Objects:**
- `indicator`: Pattern for detecting threat activity
- `campaign`: Series of attacks with shared goal
- `threat-actor`: Adversary or group
- `attack-pattern`: TTP mapped to MITRE ATT&CK
- `malware`: Malicious software
- `report`: Collection of intelligence

### MISP (Malware Information Sharing Platform)

MISP adalah open-source threat intelligence platform:

**Key MISP Features for Hunting:**
- **Feed management**: Subscribe to public + private intel feeds
- **Event correlation**: Automatically correlate IoCs
- **Export**: STIX, CSV, JSON, OpenIOC
- **Galaxies**: MITRE ATT&CK mapping, threat actor groups

**MISP to Splunk Integration:**
```
MISP Feed → Splunk TA for MISP → inputlookup → SPL correlation
```

---

## 9. Ransomware & APT Case Studies

### Ransomware Attack Chain (Example: LockBit)

```
Phase 1: Initial Access (T1190)
  - Exploit Citrix/Verizon VPN vulnerability
  - Gain foothold on edge server

Phase 2: Defense Evasion (T1070)
  - Disable Windows Defender via registry
  - Delete logs, disable auditing

Phase 3: Credential Access (T1003)
  - Dump LSASS via comsvcs.dll
  - Extract domain admin hashes

Phase 4: Lateral Movement (T1021)
  - PsExec to domain controllers
  - Deploy ransomware via GPO

Phase 5: Exfiltration (T1048)
  - StealBit tool exfiltrates data
  - Encrypted upload to adversary server

Phase 6: Impact (T1486)
  - Encrypt files with AES+RSA
  - Deploy ransom note
  - Data leak site if unpaid

Hunt Indicators:
  Phase 1: VPN connection logs, web shell creation
  Phase 2: Registry changes to Defender, Event 1102 (log clear)
  Phase 3: LSASS access (Sysmon 10), comsvcs.dll usage
  Phase 4: PsExec execution (Sysmon 1), service creation (7045)
  Phase 5: Large outbound data transfers, unusual DNS queries
  Phase 6: Mass file operations (Sysmon 11), extension changes
```

### APT Case Study: APT29 (Cozy Bear)

**Profile:**
- **Attribution**: Russia's SVR (Foreign Intelligence Service)
- **Targets**: Government, think tanks, academia, IT
- **Motivation**: Espionage, geopolitical advantage

**TTPs:**
- **Initial access**: Spear phishing, supply chain (SolarWinds)
- **Persistence**: Golden SAML, Azure AD application registration
- **C2**: Cloud API abuse (Microsoft Graph, Dropbox, Google Drive)
- **Tools**: PowerShell, Cobalt Strike, custom backdoors

**Detection Opportunities:**
- PowerShell with cloud API URLs
- Azure AD app registration by non-admin accounts
- Beaconing via HTTPS to cloud services
- Unusual OAuth token usage

### APT Case Study: Lazarus Group

**Profile:**
- **Attribution**: North Korea (RGB/Reconnaissance General Bureau)
- **Targets**: Financial, crypto, defense
- **Motivation**: Financial gain, espionage

**TTPs:**
- **Initial access**: Social engineering, malicious npm packages
- **Tools**: macOS malware (Dacom, AppleJeus), TraderTraitor
- **C2**: HTTPS, sometimes using compromised legitimate servers
- **Persistence**: Launch agents (macOS), scheduled tasks (Windows)

**Detection Opportunities:**
- npm/pip packages with typosquatting domains
- macOS launch agent plist files
- Process executing from userspace with network connections
- Crypto transaction monitoring

---

## 10. Exam Strategy & Report Template

### OSTH Exam Strategy

**Pre-Exam Preparation:**
- Complete all 7 modules + Challenge Lab thoroughly
- Build a personal SPL query library (copy-paste ready)
- Practice time management — complete challenge lab in <6 hours
- Create report template in advance (Word/LibreOffice)
- Prepare note-taking system (CherryTree, OneNote, etc.)

**During Exam:**
1. **Read the threat intel report FIRST** — Understand adversary profile, IOCs, TTPs
2. **Map IOCs to data sources** — Which logs will contain these indicators?
3. **Start with broad Splunk queries** — IOC matching, timeline scoping
4. **Build timeline as you go** — Don't wait until the end
5. **Screenshot everything** — Every query, every result, with timestamp
6. **Verify answers on Dev machine** — Compare MD5 hashes
7. **Take breaks** — 5 min every hour to stay sharp

**Homework to Do BEFORE Exam:**
```
1. Build Splunk query playbook (20+ copy-paste queries)
2. Practice time-boxed challenge labs (6h limit)
3. Write 2-3 practice reports
4. Create report template with sections pre-filled
5. Install Greenshot or similar screenshot tool
6. Prepare CherryTree or note-taking template
```

### OSTH Report Template

**Gunakan struktur berikut untuk exam report:**

```
1. EXECUTIVE SUMMARY
   - Hunt Overview (1 paragraph)
   - Key Findings (3-5 bullets)
   - Threat Actor Attribution
   - Overall Risk Assessment

2. HYPOTHESIS & METHODOLOGY
   - Initial Hypothesis
   - Data Sources Used
   - Hunting Methodology (Intel-based, Hypothesis-driven, etc.)

3. HUNT NARRATIVE
   Timeline of Events:
   | Timestamp | Event | Host | Source | TTP (MITRE) | Confidence |
   |-----------|-------|------|--------|-------------|------------|
   | 2026-01-15 08:30 | Initial access via web shell | WEB01 | Splunk (IIS) | T1190 | High |
   
   Detailed Analysis:
   - Finding 1: [Description]
     - Query used: [SPL/CQL]
     - Evidence: [Screenshot]
     - Artifact details: [IP, hash, user, process]
   
   - Finding 2-7: (same structure)

4. IOCS TABLE
   | Type | Value | Context | First Seen | Host |
   |------|-------|---------|------------|------|
   | IP | 185.234.72.1 | C2 server | 2026-01-15 09:00 | WEB01 |
   | SHA256 | a1b2c3... | Malicious binary | 2026-01-15 09:05 | WEB01 |

5. IMPACT ASSESSMENT
   - Systems Affected
   - Data Exfiltrated/Encrypted
   - Attacker Objectives Achieved

6. MITRE ATT&CK MAPPING
   | Tactic | Technique ID | Technique | Observed |
   |--------|-------------|-----------|----------|
   | Initial Access | T1190 | Exploit Public-Facing App | Yes |
   | Execution | T1059.001 | PowerShell | Yes |
   
7. RECOMMENDATIONS
   - Detection Recommendations
   - Prevention Recommendations
   - Hunting Recommendations

8. APPENDICES
   - Complete SPL/CQL Queries
   - Full Timeline
   - Evidence Inventory
   - Screenshots
```

### Chain of Custody Template

| Item | Description | Source | Hash | Collected By | Date/Time |
|------|-------------|--------|------|--------------|-----------|
| E-001 | Splunk query results (export) | SIEM | N/A | Analyst | 2026-01-15 10:00 |
| E-002 | CrowdStrike event export | Falcon | SHA256: abc... | Analyst | 2026-01-15 10:30 |
| E-003 | Suricata alert log | Network | SHA256: def... | Analyst | 2026-01-15 11:00 |

---

## 11. Referensi Lengkap

### Official OffSec Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | TH-200 Course Page | https://www.offsec.com/courses/th-200/ |
| 2 | TH-200 Syllabus (PDF) | https://www.offsec.com/documentation/TH-200-Syllabus.pdf |
| 3 | OSTH Exam Guide | https://help.offsec.com/hc/en-us/articles/29141776768148 |
| 4 | OSTH Exam FAQ | https://help.offsec.com/hc/en-us/articles/29141778787220 |
| 5 | TH-200 Course FAQ | https://help.offsec.com/hc/en-us/articles/30060462915348 |
| 6 | OSTH Certification Renewal | https://help.offsec.com/hc/en-us/articles/36010548001812 |
| 7 | OffSec — OSTH Blog: Student Mentor | https://www.offsec.com/blog/a-student-mentors-th-200-and-osth-learning-experience/ |
| 8 | OffSec — OSTH Journey (Mobius) | https://www.offsec.com/blog/my-journey-with-th-200-becoming-an-offsec-certified-threat-hunter-osth/ |
| 9 | NICCS — TH-200 Course Listing | https://niccs.cisa.gov/training/catalog/ata/offsec-th-200-foundational-threat-hunting-osth |
| 10 | OffSec — OSAI AI-300 Course | https://www.offsec.com/courses/ai-300/ |
| 11 | OffSec — SOC-200 Course | https://www.offsec.com/courses/soc-200/ |
| 12 | OffSec — IR-200 Course | https://www.offsec.com/courses/ir-200/ |

### Exam Reviews & Experiences

| # | Author | Title | Year |
|---|--------|-------|------|
| 13 | Under the Appl3Tree | OffSec TH-200 & OSTH Certification Review | 2025 |
| 14 | Cyd Tseng | OSTH: Course Review and Exam Tips (InfoSec Write-ups) | 2025 |
| 15 | AdminStar | My OSIR and OSTH Journey | 2025 |
| 16 | Kyser Clark | Everything About OSTH Certification | 2024 |
| 17 | Prof.Naz | TH-200 / OSTH Review | 2025 |
| 18 | P4n7h3r | A Student Mentor's TH-200 and OSTH Learning Experience | 2025 |
| 19 | QA | OSTH Certification & Exam Guide | 2025 |
| 20 | Fast Lane | TH-200 Foundational Threat Hunting Course Outline | 2025 |
| 21 | Applied Technology Academy | OSTH Training — Syllabus | 2025 |
| 22 | Red & Blue Alliance | TH-200 OSTH Course | 2025 |
| 23 | EFIGO | TH-200 (OSTH) — Topics Covered | 2025 |

### Threat Hunting Frameworks

| # | Resource | URL |
|---|----------|-----|
| 24 | CrowdStrike SEARCH Methodology | https://www.crowdstrike.com/blog/successful-threat-hunting-starts-with-search/ |
| 25 | CrowdStrike — Nowhere to Hide (TH Report) | https://www.crowdstrike.com/wp-content/uploads/2022/09/2021-overwatch-threat-hunting-report.pdf |
| 26 | CrowdStrike — 2021 TH Report (PDF) | https://go.crowdstrike.com/rs/281-OBQ-266/images/Report2021ThreatHunting.pdf |
| 27 | SANS — PICERL IR Model | https://www.sans.org/white-papers/ |
| 28 | SANS — PEAK Threat Hunting Framework | https://www.sans.org/blog/peak-threat-hunting-framework/ |
| 29 | MITRE ATT&CK Official | https://attack.mitre.org |
| 30 | MITRE ATT&CK Navigator | https://mitre-attack.github.io/attack-navigator/ |
| 31 | MITRE ATT&CK — Enterprise Matrix | https://attack.mitre.org/matrices/enterprise/ |
| 32 | MITRE CAR (Cyber Analytics Repository) | https://car.mitre.org/ |
| 33 | MITRE D3FEND | https://d3fend.mitre.org/ |
| 34 | Cyber Kill Chain (Lockheed Martin) | https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html |
| 35 | Diamond Model of Intrusion Analysis | https://www.activeresponse.org/wp-content/uploads/2013/07/diamond.pdf |
| 36 | NIST SP 800-61 Rev 2 (IR Guide) | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |
| 37 | FIRST CVSS v3.1 Calculator | https://www.first.org/cvss/calculator/3.1 |

### Splunk / SPL

| # | Resource | URL |
|---|----------|-----|
| 38 | Splunk SPL Cheat Sheet (Decryption Digest) | https://www.decryptiondigest.com/blog/splunk-spl-queries-cheat-sheet |
| 39 | Splunk SPL Detection Queries (Decryption Digest) | https://www.decryptiondigest.com/blog/splunk-spl-detection-queries-mitre-attack |
| 40 | Splunk SPL Cheat Sheet — 15 SOC Queries (EpicDetect) | https://epicdetect.io/blogs/splunk-spl-cheat-sheet-15-queries-soc-analysts |
| 41 | 23 Top Splunk Queries for Threat Hunting | https://technicalustad.com/splunk-queries-for-threat-hunting/ |
| 42 | Nervi0z/splunk-blue-team (GitHub) | https://github.com/Nervi0z/splunk-blue-team |
| 43 | lucsemassa/splunk_threat_hunting (GitHub) | https://github.com/lucsemassa/splunk_threat_hunting |
| 44 | Splunk Documentation — Search Reference | https://docs.splunk.com/Documentation/Splunk/latest/SearchReference |
| 45 | Splunk — Common Information Model (CIM) | https://docs.splunk.com/Documentation/CIM/latest/User/Overview |
| 46 | Splunk Enterprise Security (ES) | https://www.splunk.com/en_us/software/enterprise-security.html |
| 47 | Splunk — Risk-Based Alerting Guide | https://docs.splunk.com/Documentation/ES/latest/RBA |
| 48 | Splunk Fundamentals Free Training | https://www.splunk.com/en_us/training/free-courses.html |
| 49 | Splunk SOAR Documentation | https://docs.splunk.com/Documentation/SOAR |
| 50 | Splunk Security Content Updates (Blog) | https://www.splunk.com/en_us/blog/security/splunk-security-content-for-threat-detection-response-may-2026-update.html |
| 51 | Splunk Security Content (Research) | https://research.splunk.com/use_cases/advanced-threat-detection/ |
| 52 | Splunk Security Content Nov 2025 Update | https://www.splunk.com/en_us/blog/security/latest-splunk-security-content.html |

### CrowdStrike Falcon / CQL

| # | Resource | URL |
|---|----------|-----|
| 53 | CrowdStrike — SEARCH Methodology | https://www.crowdstrike.com/blog/successful-threat-hunting-starts-with-search/ |
| 54 | CrowdStrike — TH with Falcon Identity Protection | https://www.crowdstrike.com/tech-hub/identity-protection/threat-hunting-with-falcon-identity-protection/ |
| 55 | CrowdStrike Falcon 302 Syllabus | https://assets.crowdstrike.com/is/content/crowdstrikeinc/csu-falcon-302-course-syllabuspdf |
| 56 | CrowdStrike Falcon 202 Syllabus | https://assets.crowdstrike.com/is/content/crowdstrikeinc/csu-falcon-202-course-syllabuspdf |
| 57 | CrowdStrike Foundry — TH Dashboard Tutorial | https://developer.crowdstrike.com/foundry/tutorials/threat-hunting-dashboard/ |
| 58 | CrowdStrike/foundry-tutorial-threat-hunting (GitHub) | https://github.com/CrowdStrike/foundry-tutorial-threat-hunting |
| 59 | CrowdStrike Falcon Query Language Guide | https://www.crowdstrike.com/blog/tech-center/crowdstrike-query-language-cql/ |
| 60 | CrowdStrike Threat Graph Overview | https://www.crowdstrike.com/platform/threat-graph/ |
| 61 | CrowdStrike Falcon OverWatch | https://www.crowdstrike.com/services/threat-hunting/ |

### Suricata / IDS

| # | Resource | URL |
|---|----------|-----|
| 62 | Suricata Official Documentation | https://suricata.readthedocs.io/ |
| 63 | Suricata Rules Documentation | https://suricata.readthedocs.io/en/suricata-7.0/rules/ |
| 64 | Emerging Threats Rules | https://rules.emergingthreats.net/ |
| 65 | Suricata Installation Guide | https://suricata.readthedocs.io/en/suricata-7.0/quickstart.html |
| 66 | Suricata — Rule Management with suricata-update | https://github.com/OISF/suricata-update |

### Zeek / Network Security Monitoring

| # | Resource | URL |
|---|----------|-----|
| 67 | Zeek Official Documentation | https://docs.zeek.org/ |
| 68 | Zeek Quick Start Guide | https://docs.zeek.org/en/current/quickstart.html |
| 69 | Zeek Script Reference | https://docs.zeek.org/en/current/scripting/ |
| 70 | The Practice of Network Security Monitoring (Bejtlich) | Book |

### Windows Event Logs & Sysmon

| # | Resource | URL |
|---|----------|-----|
| 71 | Ultimate Windows Security — Event ID Encyclopedia | https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/ |
| 72 | Microsoft — Windows Security Event ID Reference | https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/sentinel/windows-security-event-id-reference.md |
| 73 | EpicDetect — Event IDs Every SOC Analyst Should Know | https://epicdetect.io/blogs/windows-event-log-ids-soc-analysts |
| 74 | Microsoft — Sysmon Documentation | https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon |
| 75 | SwiftOnSecurity/sysmon-config | https://github.com/SwiftOnSecurity/sysmon-config |
| 76 | olafhartong/sysmon-modular | https://github.com/olafhartong/sysmon-modular |
| 77 | sbousseaden/EVTX-ATTACK-SAMPLES | https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES |
| 78 | Eric Zimmerman — Forensic Tools | https://ericzimmerman.github.io/ |

### Threat Intelligence

| # | Resource | URL |
|---|----------|-----|
| 79 | MISP Official Documentation | https://www.misp-project.org/documentation/ |
| 80 | MISP GitHub Repository | https://github.com/MISP/MISP |
| 81 | STIX 2.1 Documentation (OASIS) | https://oasis-open.github.io/cti-documentation/ |
| 82 | TAXII 2.1 Specification | https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html |
| 83 | MITRE ATT&CK — CTI | https://attack.mitre.org/resources/ |
| 84 | OpenCTI Platform | https://www.opencti.io/ |
| 85 | AlienVault OTX | https://otx.alienvault.com/ |
| 86 | VirusTotal | https://www.virustotal.com |
| 87 | IBM X-Force Exchange | https://exchange.xforce.ibmcloud.com/ |
| 88 | TLP (Traffic Light Protocol) — FIRST | https://www.first.org/tlp/ |

### Ransomware & APT References

| # | Resource | URL |
|---|----------|-----|
| 89 | CISA — StopRansomware Guide | https://www.cisa.gov/stopranshware |
| 90 | CISA — #StopRansomware: LockBit | https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-165a |
| 91 | CISA — CLOP Ransomware Advisory | https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-158a |
| 92 | CISA — BlackCat/ALPHV Advisory | https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-353a |
| 93 | MITRE — APT29 (Cozy Bear) | https://attack.mitre.org/groups/G0016/ |
| 94 | MITRE — Lazarus Group | https://attack.mitre.org/groups/G0032/ |
| 95 | MITRE — APT41 (Winnti) | https://attack.mitre.org/groups/G0096/ |
| 96 | MITRE — MuddyWater | https://attack.mitre.org/groups/G0069/ |
| 97 | MITRE — FIN7 | https://attack.mitre.org/groups/G0046/ |
| 98 | The DFIR Report | https://thedfirreport.com |
| 99 | CrowdStrike — 2024 Global Threat Report | https://www.crowdstrike.com/global-threat-report/ |
| 100 | CrowdStrike — 2025 Threat Hunting Report | https://www.crowdstrike.com/resources/reports/threat-hunting-report/ |

### YARA & Malware Analysis

| # | Resource | URL |
|---|----------|-----|
| 101 | YARA Documentation | https://yara.readthedocs.io/en/stable/ |
| 102 | YARA Rules GitHub | https://github.com/Yara-Rules/rules |
| 103 | YARA — Malware Name Format | https://yara.readthedocs.io/en/stable/writingrules.html |
| 104 | FLOSS (FireEye Obfuscated String Solver) | https://github.com/mandiant/flare-floss |
| 105 | Detect-It-Easy (DIE) | https://github.com/horsicq/Detect-It-Easy |
| 106 | Hybrid Analysis | https://www.hybrid-analysis.com |
| 107 | ANY.RUN (Interactive Sandbox) | https://any.run |

### Books & Learning

| # | Resource | URL / Author |
|---|----------|--------------|
| 108 | Blue Team Handbook: Incident Response (3rd Ed.) | Don Murdoch |
| 109 | Applied Incident Response | Steve Anson |
| 110 | The Practice of Network Security Monitoring | Richard Bejtlich |
| 111 | Practical Malware Analysis | Michael Sikorski & Andrew Honig |
| 112 | Threat Hunting with Splunk | Book |
| 113 | Windows Internals, Part 1 & 2 (7th Ed.) | Pavel Yosifovich et al. |
| 114 | Intelligent Cyber Threat Hunting (Summit 2024) | Book |

### Labs & Practice

| # | Resource | URL |
|---|----------|-----|
| 115 | Hack The Box — SOC Analyst Track | https://www.hackthebox.com |
| 116 | Hack The Box — CDSA (Certified Defensive Security Analyst) | https://www.hackthebox.com/certification/certified-defensive-security-analyst |
| 117 | Blue Team Labs Online (BTLO) | https://blueteamlabs.online |
| 118 | LetsDefend | https://letsdefend.io |
| 119 | CyberDefenders | https://cyberdefenders.org |
| 120 | TryHackMe — DFIR Paths | https://tryhackme.com |
| 121 | RangeForce | https://rangeforce.com |
| 122 | Immersive Labs | https://www.immersivelabs.com |
| 123 | DetectionLab (Chris Long) | https://github.com/clong/DetectionLab |
| 124 | HELK (Hunting ELK) | https://github.com/Cyb3rWard0g/HELK |

### Communities

| # | Resource | URL |
|---|----------|-----|
| 125 | r/ThreatHunting Reddit | https://reddit.com/r/ThreatHunting |
| 126 | r/IncidentResponse Reddit | https://reddit.com/r/IncidentResponse |
| 127 | OffSec Discord | https://discord.gg/offsec |
| 128 | OffSec Community Forums | https://forums.offsec.com |
| 129 | DFIR.Science | https://dfir.science |
| 130 | The DFIR Report | https://thedfirreport.com |
| 131 | SANS DFIR Community | https://www.sans.org/community/ |

### YouTube & Video

| # | Channel | Focus |
|---|---------|-------|
| 132 | 13Cubed | DFIR, memory forensics, threat hunting |
| 133 | SANS Digital Forensics | Memory analysis, timeline analysis |
| 134 | OffSec Official | Course overviews, exam tips |
| 135 | IppSec | General cybersecurity methodology |
| 136 | John Hammond | Malware analysis, RE, IR |
| 137 | OALabs | Malware unpacking, RE |
| 138 | DFIR Science | Research-level DFIR content |
| 139 | CrowdStrike | Falcon platform tutorials, TH demos |
| 140 | Splunk | SPL tutorials, ES demos |
