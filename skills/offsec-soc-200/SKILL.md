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

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [SOC-200 Mindset & SOC Analyst Framework](#2-soc-200-mindset--soc-analyst-framework)
3. [19 Module Deep-Dive](#3-19-module-deep-dive)
4. [Windows Event Log & Sysmon Reference](#4-windows-event-log--sysmon-reference)
5. [SIEM: ELK Stack, KQL & OSQuery](#5-siem-elk-stack-kql--osquery)
6. [Challenge Labs & Exam Strategy](#6-challenge-labs--exam-strategy)
7. [Referensi Lengkap](#7-referensi-lengkap)

---

## 1. Overview & Exam Structure

### Apa Itu SOC-200 / OSDA?

SOC-200 (Security Operations and Defensive Analysis) adalah sertifikasi defensive dari OffSec yang mengajarkan **detection, analysis, dan incident investigation** menggunakan SIEM. Berbeda dengan sertifikasi offensive (OSCP, OSEP), OSDA fokus pada bagaimana seorang SOC analyst mendeteksi dan merekonstruksi serangan dari log.

OSDA (OffSec Defense Analyst) adalah sertifikasi **100% praktikal** — tidak ada multiple choice. Anda diberi logs pre-recorded di Elastic SIEM + OSQuery, dan harus mengidentifikasi serta mendokumentasikan attacker actions di 10 phases.

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
  - Catat starting time setiap phase (attacker runs ~10 menit per phase)
  - Broad query dulu, lalu narrow down dengan process IDs
  - Screenshot setiap query + result
  - Dokumentasi langsung di report template

Break (30-60 menit): makan, stretching

Phase 4-7 (7-13 jam):
  - Attacks semakin stealthy — perhatikan in-memory execution
  - Gunakan OSQuery untuk verifikasi aktif (network connections, processes)
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

---

## 2. SOC-200 Mindset & SOC Analyst Framework

### Filosofi Dasar

SOC-200 mengajarkan **"Think Like an Attacker to Detect Like a Defender"** — Anda harus memahami bagaimana serangan bekerja untuk bisa mendeteksinya di logs. Ini bukan sekadar menghafal Event IDs, tapi memahami **behavioral signatures** yang ditinggalkan attacker.

### Golden Rules SOC-200 / OSDA

1. **Logs don't lie — but they are incomplete** — Tidak semua aktivitas tercatat. Jika ada gap 30 menit tanpa logs, mungkin logs dihapus atau ada teknik evasion. Jangan paksakan koneksi yang tidak ada.

2. **Timeline is NOT linear in OSDA** — Attacker actions bisa muncul out-of-order karena revert/reset. Jangan urutkan report berdasarkan timestamp — urutkan berdasarkan **phase** dan **logical attack flow**.

3. **Process IDs are your breadcrumbs** — Attacker meninggalkan jejak process IDs dan parent process IDs. Follow the PID chain untuk merekonstruksi apa yang terjadi.

4. **In-memory attacks are invisible to disk scans** — Kebanyakan serangan di exam adalah fileless. Jangan cari executable mencurigakan — cari **LOLBINs**, **PowerShell**, **WMI**, **service creation** patterns.

5. **The report is 50% of your grade** — Bisa detect semua phases tapi report berantakan = fail. Ceritakan attack story yang koheren dengan bukti screenshot + queries.

6. **Success vs Attempt** — Hanya karena attacker menjalankan tool, belum tentu berhasil. Cek apakah event yang diharapkan benar-benar terjadi (service terinstall? user dibuat? ticket didapat?).

7. **KQL is your primary weapon** — Kuasai Kibana Query Language. Filter, exclude, add columns, pivot by PID. Kecepatan query = kecepatan detection.

8. **OSQuery is your verification tool** — Gunakan OSQuery untuk memverifikasi state aktif (listening ports, running processes, network connections) yang tidak terekam di logs.

### 3 Pertanyaan Kunci Saat Stuck

1. **"What user ran this?"** — user.name, related.user, winlog.user.name — bandingkan ketiganya. User yang berbeda di fase berbeda bisa menunjukkan privilege escalation.

2. **"Did it succeed?"** — Attacker menjalankan perintah, tapi apakah berhasil? Cek event setelahnya: service terinstall? process baru muncul? authentication berhasil?

3. **"What am I not seeing?"** — Apakah ada log source yang mati? Apakah ada gap waktu? Mungkin attacker menghapus logs, atau phase sudah selesai dan Anda perlu pindah.

### SOC Analyst Framework

```
Phase Detection Workflow:
  1. Start time → catat kapan phase dimulai
  2. Broad query → cari anomali di window waktu phase
  3. Add columns → process.command_line, user.name, file.name
  4. Follow PIDs → process.pid + process.parent.pid chain
  5. Cross-source → Windows Log + Sysmon + PowerShell + Network
  6. Verify → OSQuery untuk konfirmasi state
  7. Document → screenshot + queries + conclusion
  8. Next phase → repeat
```

### Pattern Recognition untuk OSDA

- **Initial access** → Web server: command injection, file upload, SQLi → IIS logs + event 4688
- **Phishing** → Office macro → PowerShell -> encoded command → event 4104 (ScriptBlock)
- **Privilege escalation** → Service creation (7045) or UAC bypass → kemudian 4672 (special priv)
- **Persistence** → Registry Run keys (Sysmon 13), Scheduled Tasks (4698), Services (7045/4697)
- **Credential access** → LSASS access via Sysmon 10, Mimikatz in process creation, DCSync
- **Lateral movement** → 4624 Type 3 logons, 4648 explicit creds, service install on remote host
- **Persistence (AD)** → Golden Ticket via 4768 with unusual encryption, group modification 4728/4732

---

## 3. 19 Module Deep-Dive

SOC-200 memiliki 19 modul berdasarkan syllabus resmi OffSec. Modul 1-18 adalah pembelajaran, modul 19 adalah persiapan exam. Dua modul terakhir (SIEM Part 1 & 2) adalah yang paling kritis untuk exam.

### Modul 1: Introduction to SOC-200

Pengenalan course structure, lab environment, VPN connectivity, dan metodologi pembelajaran. Menekankan pentingnya **"Understand Offense to Improve Defense"** — Anda harus mengerti cara attacker bekerja.

### Modul 2: Attacker Methodology Introduction

Pemahaman framework attacker untuk detection:

**Enterprise Network Architecture:**
- DMZ, deployment environments, core vs edge devices
- VPNs dan remote site connectivity

**Lockheed Martin Cyber Kill Chain:**
```
Reconnaissance → Weaponization → Delivery → Exploitation
  → Installation → C2 → Actions on Objectives
```
Gunakan Kill Chain untuk memetakan fase serangan dan mengidentifikasi deteksi di setiap tahap.

**MITRE ATT&CK Framework:**
- Tactics, Techniques, and Sub-Techniques
- Case studies: OilRig, APT3, APT28
- Mapping detected events ke MITRE ATT&CK IDs

**Mindset**: Module ini mengajarkan **kerangka pikir** — bukan hanya tool. Pahami di mana Anda bisa mendeteksi attacker di setiap fase.

### Modul 3: Windows Endpoint Introduction

Fundamental Windows internals untuk detection:

**Windows Processes:**
- System, svchost.exe, lsass.exe, winlogon.exe, explorer.exe
- Process tree hierarchy — penting untuk follow PID chain

**Windows Registry:**
- Hives: HKLM, HKCU, HKCR, HKU, HKCC
- Auto-start locations: Run keys, Winlogon, Services

**Windows Event Log:**
- Channels: Security, System, Application, PowerShell, Sysmon
- Event structure: Event ID, Level, Task Category, Keywords
- PowerShell queries: `Get-WinEvent -FilterHashtable`

**Sysmon (System Monitor):**
- Driver-level logging — lebih detail dari Event Log standar
- Event IDs: 1 (Process), 3 (Network), 7 (Image Load), 11 (File Create), 13 (Registry), 22 (DNS)
- Event Viewer dan PowerShell untuk analysis

**Key Event IDs:**
```
4624 — Successful logon
4625 — Failed logon
4688 — Process creation
4672 — Special privileges assigned
7045 — Service installed (System log)
```

**Mindset**: Kuasai Windows Event Log structure. Jika Anda tidak paham struktur event, Anda tidak bisa query efektif di Kibana.

### Modul 4: Windows Server-Side Attacks

Deteksi serangan terhadap Windows servers:

**Credential Abuse:**
- SAM and Windows Authentication
- **Suspicious logins**: Logon Type 3 (network) dari IP tidak dikenal, Type 10 (RDP) dari non-admin workstation
- **Brute force**: Multiple 4625 dari IP yang sama dalam waktu singkat
- **Pass-the-Hash**: Deteksi via unusual logon patterns + network connections

**Web Application Attacks:**
- **IIS logging**: W3C format, status codes, URIs
- **Local File Inclusion (LFI)**: `../` patterns dalam HTTP requests
- **Command Injection**: Unusual parameters, encoded commands di IIS logs
- **File Upload**: File creation events di web directories (Sysmon 11)

**Binary Exploitation:**
- Buffer overflow detection via WDEG (Windows Defender Exploit Guard) events
- Event ID 1 (Sysmon) untuk process creation dari exploits

**Mindset**: Web servers adalah entry point paling umum. Prioritaskan IIS logs dan process creation events.

### Modul 5: Windows Client-Side Attacks

Deteksi serangan terhadap endpoint users:

**Microsoft Office Attacks:**
- Macro-enabled documents via phishing
- **Detection**: winword.exe/ excel.exe spawning cmd.exe, powershell.exe, wscript.exe
- **Key indicator**: Parent-child process anomaly — Office apps should NOT spawn shells

**PowerShell Logging:**
- **Module logging (4103)**: Cmdlets dan parameters
- **Script block logging (4104)**: Full script content — **captures after deobfuscation**
- **Transcription**: Full session recording

**Detection workflow:**
```
Phishing email → Office document → Macro → PowerShell → 
PowerShell 4104 captures deobfuscated script → AMSI bypass? → C2 beacon
```

**Invoke-Obfuscation:**
- Course mengajarkan Invoke-Obfuscation untuk memahami bagaimana attacker menyembunyikan PowerShell
- Detection: cari pola obfuscation seperti `-enc`, `-e`, base64 strings, reverse strings

**Mindset**: PowerShell Script Block Logging (4104) adalah **detection goldmine** — ia menangkap konten setelah deobfuscation.

### Modul 6: Windows Privilege Escalation

Deteksi teknik privilege escalation:

**UAC Bypass:**
- Registry-based bypasses (fodhelper, eventvwr)
- Detection: Registry modification events (Sysmon 13) + process creation dengan parent tidak biasa

**Service Creation PrivEsc:**
- **Unquoted service paths**: Service path tanpa quotes → Sysmon 1 + Service Install 7045
- **Weak service permissions**: AccessChk + sc sdshow → detection via registry changes
- **Service binary replacement**: File modified di Program Files → Sysmon 11

**Token Abuse:**
- SeImpersonate, SeAssignPrimaryToken → Potato attacks
- Detection: Sysmon 1 + unusual child processes dari SYSTEM-level services

**Key indicators:**
```
Before privesc: Running as low-priv user
After privesc: Process running as NT AUTHORITY\SYSTEM
Look for: service creation (7045) → followed by process as SYSTEM
Look for: UAC bypass → registry changes + process creation
```

### Modul 7: Windows Persistence

Deteksi metode persistence:

**Persistence on Disk:**
- **Windows Services**: `sc create` or `New-Service` → Event 7045 / 4697
- **Scheduled Tasks**: `schtasks` → Event 4698
- **DLL Sideloading/Hijacking**: Sysmon 7 (Image Loaded) dari path tidak standar

**Persistence in Registry:**
- **Run Keys**: `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` → Sysmon 13
- **Winlogon Helper**: `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon` → Sysmon 13

**Key KQL Query:**
```kql
event.code : (7045 or 4698 or 13 or 12) AND host.name : "TARGET_HOST"
```

**Mindset**: Persistence sering menjadi jembatan antar phases. Jika Anda tidak detect persistence, Anda akan kehilangan chain ke phase berikutnya.

### Modul 8: Linux Endpoint Introduction

Fundamental Linux logging:

**Daemons and Logging:**
- syslog/rsyslog: `/var/log/`
- journald: `journalctl`
- Web daemon logs: Apache `/var/log/apache2/`, Nginx `/var/log/nginx/`
- Auth logs: `/var/log/auth.log` (Debian), `/var/log/secure` (RHEL)

**Key Linux Log Files:**
```
/var/log/auth.log     — Authentication events
/var/log/syslog       — System events
/var/log/kern.log     — Kernel messages
/var/log/messages     — General messages (RHEL)
```

**Automating Defensive Analysis:**
- Python untuk log parsing
- grep/awk/sed untuk quick analysis
- DevOps tools untuk scale

**Mindset**: Linux logs di SOC-200 tidak sedetail Windows — fokus pada auth.log dan web server logs.

### Modul 9: Linux Server-Side Attacks

Deteksi serangan terhadap Linux servers:

**Credential Abuse:**
- **Suspicious logins**: SSH from unusual IPs, non-standard hours
- **Brute force**: Multiple Failed password entries in auth.log

**Web Application Attacks:**
- **Command Injection**: Apache/Nginx access logs + process creation events
- **SQL Injection**: Database error logs, unusual query patterns

**Key detection patterns:**
```
auth.log: "Failed password for root" × 50 = brute force
auth.log: "Accepted publickey for www-data" = successful auth
apache2/access.log: "GET /index.php?cmd=id" = command injection
```

### Modul 10: Linux Privilege Escalation

Deteksi privilege escalation di Linux:

**User-Side Attacks:**
- .bashrc / .profile modification — persistence via user config
- SSH key backdoor — authorized_keys modification
- Detection: File modification events + unexpected SSH logins

**System-Side Attacks:**
- **SUID abuse**: `chmod u+s` on binaries → file permission changes
- **Weak permissions**: /etc/shadow readable → world-readable file alerts
- **Kernel exploits**: uname -a → detection via process creation with unusual names

**Key detection:**
```
Before privesc: www-data or low-priv user
After privesc: root
Look for: command injection → shell → sudo / SUID abuse → root
```

### Modul 11: Network Detections

Intrusion Detection Systems dan C2 detection:

**IDS/IPS Fundamentals:**
- Snort rule syntax: `alert tcp $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS`
- Rule components: action, protocol, source/destination, content detection
- Signature vs anomaly-based detection

**Detecting C2 Infrastructure:**
- Beaconing patterns: regular intervals, same payload size
- Domain Generation Algorithms (DGAs): random-looking subdomains
- DNS tunneling: excessive DNS queries from single host
- Detection: Sysmon 22 (DNS query) + Snort rules

### Modul 12: Antivirus Alerts and Evasion

Memahami AV detection dan bypass:

**AV Detection Methods:**
- **Signature-based**: Byte pattern matching — paling mudah di-bypass
- **Heuristic/Behavioral**: Runtime behavior analysis
- **AMSI**: Antimalware Scan Interface untuk script scanning

**AMSI Bypass Detection:**
- **amsiInitFailed**: Patch AMSI via reflection → PowerShell 4104 akan capture ini
- **Registry bypass**: `AmsiEnable = 0` → Registry change (Sysmon 13)
- Detection: Jika AV alert mati mendadak + PowerShell activities, kemungkinan AMSI bypass

**Key insight untuk OSDA:**
- AMSI bypass akan terlihat di PowerShell ScriptBlock logging (4104)
- AV alerts sendiri adalah IoC yang valid — dokumentasikan

### Modul 13: Network Evasion and Tunneling

Deteksi teknik network evasion:

**Network Segmentation:**
- DMZ, internal network, management network
- Segmen seharusnya tidak bisa saling communicate kecuali melalui firewall

**Egress Busting:**
- Attacker mencoba koneksi keluar untuk menemukan port yang diizinkan
- Detection: Connection attempts ke multiple ports dari internal host
- Sysmon 3 (Network connect) atau firewall logs

**Port Forwarding and Tunneling:**
- SSH tunneling, Chisel, Ligolo-ng, socat
- Detection: Unusual outbound connections, port bindings yang mencurigakan
- OSQuery: Cek listening ports → `SELECT * FROM listening_ports`

**Key detection:**
```
Normal: Internal → Internet via port 443 (HTTPS)
Suspicious: Internal → Internet via port 53 (DNS - tunneling)
Suspicious: Internal → Internet via port 22 (SSH - tunnel)
Suspicious: Internal server listening on high port (>1024)
```

### Modul 14: Active Directory Enumeration

Deteksi reconnaissance AD:

**LDAP Abuse:**
- PowerView enumeration: Get-NetUser, Get-NetComputer, Get-NetGroup
- Detection: Unusual LDAP query volume dari non-admin hosts
- Event 4662 (An operation was performed on an object)

**Detecting AD Enumeration:**
- **Auditing Object Access**: Event 4662 untuk sensitive objects
- **Baseline monitoring**: Kenali pattern normal LDAP queries
- **Honey tokens**: Fake objects yang tidak pernah diakses — akses = detection

### Modul 15: Windows Lateral Movement

Deteksi lateral movement di Windows domain:

**Pass-the-Hash:**
- Impacket (wmiexec, psexec, smbexec) → network logon + service creation
- Detection: Event 4624 Type 3 + 7045 + process creation di remote host

**Pass-the-Ticket:**
- Rubeus, Mimikatz → Kerberos ticket abuse
- Detection: Event 4768 TGT request + 4769 service ticket — perhatikan encryption type

**Kerberoasting:**
- Attacker request TGS dengan RC4 encryption → crack offline
- Detection: Multiple 4769 dari satu user dalam waktu singkat, encryption type RC4 (0x17)

**Terminal Services (RDP):**
- Event 4624 Type 10 + Restricted Admin mode
- Detection: RDP logons dari internal host yang tidak biasa

**Key lateral movement detection:**
```
Source: Host A (compromised)
Method: wmiexec / psexec / winrm
Target: Host B
Detection: 
  - Host A → B connection (Sysmon 3 or firewall log)
  - Service created on Host B (7045)
  - New process on Host B (4688) with command line
  - User context: Administrator or Domain Admin
```

### Modul 16: Active Directory Persistence

Deteksi persistence level domain:

**Domain Group Modifications:**
- User added to Domain Admins → Event 4728 / 4732
- User added to Enterprise Admins → Event 4756
- Detection: Account management events dari non-DC hosts

**Golden Tickets:**
- Forged KRBTGT hash → create TGT for any user
- Detection: Event 4768 dengan lifetime > normal (default 10 jam) atau encryption type tidak sesuai
- Event 4672 (Special privileges) untuk user yang tidak seharusnya

**Silver Tickets:**
- Forged service account hash → access specific service
- Detection: Event 4624 dengan Logon Type 3 dari machine account yang mencurigakan

### Modul 17: SIEM Part One — Intro to ELK

ELK Stack fundamental untuk SOC analysis:

**SIEM Concepts:**
- Log collection → parsing → indexing → searching
- Correlation rules → alerts → dashboards
- ELK: Elasticsearch (storage + search), Logstash (parsing), Kibana (visualization)

**Elastic Stack Components:**
```
Beats (Winlogbeat, Filebeat) → Logstash → Elasticsearch → Kibana
  - Winlogbeat: Collect Windows Event Log + Sysmon
  - Filebeat: Collect file-based logs (syslog, IIS)
  - Logstash: Parse, filter, transform
  - Elasticsearch: Index + store
  - Kibana: Search + visualize + dashboard
```

**OSQuery Integration:**
- OSQuery sebagai Elastic Agent integration
- SQL-based queries untuk live system state
- `SELECT * FROM processes WHERE name = 'powershell.exe'`
- `SELECT * FROM listening_ports;`
- `SELECT * FROM dns_responses;`

**ELK Security Features:**
- Rules and alerts: Detection rules berbasis KQL
- Timelines: Case management
- Dashboards: Pre-built visualizations untuk quick overview

**Mindset**: Module 17-18 adalah **yang paling penting untuk exam**. Fokus di sini.

### Modul 18: SIEM Part Two — Combining the Logs

Menggabungkan semua log sources dalam satu SIEM:

**Phase-based detection workflow:**
```
Phase 1: Web Server Initial Access
  - Enumeration + Command Injection on web01
  - Detection rules for command injection patterns
  - Cross-reference IIS logs + Windows Event Log

Phase 2: Lateral Movement to App Server
  - Brute force + authentication to appsrv01
  - Detection rules for brute force + lateral movement
  - Follow PIDs from web01 to appsrv01

Phase 3: Persistence + Privesc on App Server
  - Service creation + privilege escalation
  - Registry persistence + scheduled tasks

Phase 4: Actions on Domain Controller
  - Dumping AD database (ntds.dit)
  - Detection rules for DCSync / ntds.dit access
```

**Mindset**: Module ini mengajarkan **end-to-end detection chain** yang sama persis dengan exam. Pelajari bagaimana setiap phase terhubung.

### Modul 19: Trying Harder — The Labs

Persiapan Challenge Labs dan exam:
- Overview struktur lab
- Strategi phase-based detection
- Pentingnya dokumentasi dan report writing

---

## 4. Windows Event Log & Sysmon Reference

### Windows Security Event ID Reference

#### Authentication Events

| Event ID | Description | Detection Value |
|----------|-------------|-----------------|
| **4624** | Successful logon | Track successful auth — perhatikan Logon Type |
| **4625** | Failed logon | Brute force / password spray detection |
| **4634** | Logoff | Session tracking |
| **4647** | User-initiated logoff | Session tracking |
| **4648** | Explicit credential logon | Lateral movement — credential used explicitly |
| **4672** | Special privileges assigned | Admin-level access |
| **4768** | Kerberos TGT requested | Initial domain auth — watch encryption type |
| **4769** | Kerberos service ticket | Kerberoasting detection |
| **4771** | Kerberos pre-auth failed | Password spray |
| **4776** | NTLM authentication | NTLM usage detection |

#### Logon Types (Critical untuk 4624/4625)

| Logon Type | Name | Description |
|------------|------|-------------|
| 2 | Interactive | Local console / keyboard |
| 3 | Network | SMB, file share, RPC |
| 4 | Batch | Scheduled task |
| 5 | Service | Service startup |
| 7 | Unlock | Screen unlock |
| 8 | NetworkCleartext | IIS basic auth, FTP |
| 9 | NewCredentials | RunAs |
| 10 | RemoteInteractive | RDP |
| 11 | CachedInteractive | Cached domain credentials |

#### Account Management Events

| Event ID | Description |
|----------|-------------|
| **4720** | User account created |
| **4722** | Account enabled |
| **4723** | Password change attempt |
| **4724** | Password reset |
| **4725** | Account disabled |
| **4726** | Account deleted |
| **4728** | Member added to security group |
| **4732** | Member added to local group |
| **4735** | Security group modified |
| **4740** | Account locked out |
| **4756** | Member added to universal group |
| **4781** | Account name changed |

#### Process & Service Events

| Event ID | Source | Description |
|----------|--------|-------------|
| **4688** | Security | Process creation (with command line) |
| **4689** | Security | Process termination |
| **4697** | Security | Service installed (Security log) |
| **7045** | System | Service installed (System log) |
| **7036** | System | Service state change |
| **4698** | Security | Scheduled task created |
| **4699** | Security | Scheduled task deleted |
| **4700** | Security | Scheduled task enabled |

#### Defense Evasion Events

| Event ID | Description |
|----------|-------------|
| **1102** | Security log cleared (almost always malicious) |
| **104** | System log cleared |
| **4719** | Audit policy changed |
| **4657** | Registry value modified |

### Sysmon Event ID Reference

| Event ID | Name | Description |
|----------|------|-------------|
| **1** | Process creation | Full command line, parent, hashes |
| **2** | File creation time changed | Timestomping detection |
| **3** | Network connection | Outbound/inbound connections |
| **4** | Sysmon service state changed | Service start/stop |
| **5** | Process terminated | Process end |
| **6** | Driver loaded | Kernel driver load |
| **7** | Image loaded | DLL loaded into process |
| **8** | CreateRemoteThread | Process injection detection |
| **9** | RawAccessRead | LSASS read detection |
| **10** | ProcessAccess | LSASS access (credential dumping) |
| **11** | FileCreate | File created |
| **12** | RegistryEvent (Create/Delete) | Registry key create/delete |
| **13** | RegistryEvent (Value Set) | Registry value modification |
| **14** | RegistryEvent (Key/Rename) | Registry rename |
| **15** | FileCreateStreamHash | Alternate data stream creation |
| **16** | Sysmon config change | Configuration modification |
| **17** | PipeEvent (Created) | Named pipe creation |
| **18** | PipeEvent (Connected) | Named pipe connection |
| **19** | WmiEventFilter | WMI filter registration |
| **20** | WmiEventConsumer | WMI consumer registration |
| **21** | WmiBindingConsumer | WMI consumer binding |
| **22** | DNSEvent | DNS query |
| **23** | FileDelete | File deletion |
| **24** | ClipboardChange | Clipboard content change |
| **25** | ProcessTampering | Process hollowing/ghosting detection |
| **26** | FileDeleteDetected | File deletion (logged) |
| **27** | FileBlockExecutable | File execution blocked |
| **28** | FileBlockShredding | File shredding blocked |
| **29** | FileExecutableDetected | Executable detected |

### PowerShell Event IDs

| Event ID | Channel | Description |
|----------|---------|-------------|
| **400** | PowerShell | PowerShell engine start |
| **403** | PowerShell | Engine life state change |
| **4103** | Microsoft-Windows-PowerShell/Operational | Module logging — cmdlets + parameters |
| **4104** | Microsoft-Windows-PowerShell/Operational | Script block logging — FULL script content |
| **4105** | Microsoft-Windows-PowerShell/Operational | Script block start |
| **4106** | Microsoft-Windows-PowerShell/Operational | Script block stop |
| **800** | PowerShell-Analytic | Pipeline execution details |

**Critical**: 4104 captures script content **after deobfuscation** — ini adalah detection goldmine.

### Event-to-Attack Mapping

| Attack Technique | Event IDs to Hunt |
|-----------------|-------------------|
| **Brute Force** | Multiple 4625 from same IP |
| **Password Spray** | 4625 to many users, few attempts each |
| **Kerberoasting** | Multiple 4769 with RC4 (0x17) from single user |
| **Golden Ticket** | 4768 with lifetime > 10 jam, unusual encryption |
| **DCSync** | 4662 (DS-Replication-Get-Changes) on domain root |
| **Pass-the-Hash** | 4624 Type 3 + 7045 on remote + 4688 |
| **Phishing (Macro)** | winword.exe → cmd.exe/powershell (parent-child) |
| **AMSI Bypass** | 4104 capturing AMSI bypass code |
| **Service Persistence** | 7045 or 4697 on critical hosts |
| **Scheduled Task** | 4698 on unexpected hosts |
| **Registry Persistence** | Sysmon 13 on Run keys |
| **LSASS Dump** | Sysmon 10 (ProcessAccess to lsass) |
| **Log Clearing** | 1102 (Security log cleared) |

---

## 5. SIEM: ELK Stack, KQL & OSQuery

### Kibana Query Language (KQL) Reference

#### Basic Queries

```kql
# Field-value search
event.code : 4625

# Free text search (across all fields)
"svc-sql1"

# Wildcard
user.name : admin*

# Exists
_exists_ : process.command_line
```

#### Boolean Logic

```kql
# AND (implied between conditions)
event.code : 4625 AND user.name : administrator

# OR
event.code : (4625 OR 4771)

# NOT
NOT event.code : 4634

# Complex
(event.code : 4625 OR event.code : 4771) AND host.name : "DC01"
```

#### Comparison Operators

```kql
# Numeric comparison
event.code >= 4624 AND event.code <= 4625

# Time range
@timestamp >= "2024-01-01T00:00:00.000Z"

# Exists
_exists_ : source.ip
```

#### Common OSDA Detection Queries

```kql
# Find all logons (success + failure)
event.code : (4624 OR 4625)

# Failed logons from specific IP
event.code : 4625 AND source.ip : "192.168.1.100"

# Service installs in last 24h
event.code : (7045 OR 4697)

# Process with encoded PowerShell
process.command_line : *-enc*

# All PowerShell script block logs
event.code : 4104

# Registry persistence detection
event.code : 13 AND registry.path : *Run*

# Scheduled tasks created
event.code : 4698

# Network connections from unknown processes
event.code : 3 AND NOT process.name : "svchost.exe"

# Lateral movement: RDP logons
event.code : 4624 AND winlog.event_data.LogonType : 10

# Kerberoasting: multiple service tickets
event.code : 4769 AND winlog.event_data.TicketEncryptionType : 0x17
```

#### Broad Query Strategy (Start Here)

```
Start broad → add specific filters:
1. event.code : * (semua events)
2. Add time range: @timestamp >= phase_start
3. Add host filter: host.name : "web01"
4. Add event.code filter to narrow
5. Add column: process.command_line, user.name
6. Follow PID chain
```

#### Column Layout Penting

```
Always add these columns:
- @timestamp
- event.code
- host.name
- process.name
- process.command_line
- process.pid
- process.parent.pid
- user.name
- user.related
- source.ip
- winlog.event_data.LogonType
```

### OSQuery Reference

OSQuery digunakan untuk **active verification** — query state langsung dari endpoint:

```sql
-- All running processes
SELECT * FROM processes;

-- Specific process search
SELECT name, path, pid, parent FROM processes WHERE name LIKE '%powershell%';

-- Listening ports (detect backdoors)
SELECT * FROM listening_ports;

-- Network connections (detect beacons)
SELECT * FROM process_open_sockets;

-- DNS cache (recent resolutions)
SELECT * FROM dns_responses;

-- Services (detect persistence)
SELECT * FROM services WHERE path LIKE '%temp%';

-- Scheduled tasks
SELECT * FROM scheduled_tasks;

-- User accounts
SELECT * FROM users;

-- Running queries from user
SELECT * FROM processes WHERE name LIKE '%sql%' OR name LIKE '%cmd%';

-- Firewall rules
SELECT * FROM firewall_rules;
```

**Kapan menggunakan OSQuery di exam:**
- Verifikasi apakah service benar-benar terinstall (cek services table)
- Verifikasi apakah network connection benar-benar ada (process_open_sockets)
- Cek listening ports untuk backdoor detection
- Cross-check process list dengan process creation events

### Imported Dashboards (Exam Tips)

Pre-built dashboards di ELK sangat membantu:
- **Pre-built alerts**: Beberapa alerts sudah dikonfigurasi oleh OffSec
- **Gunakan sebagai starting point**: Alerts menandai aktivitas mencurigakan
- **Verifikasi manual**: Jangan percaya alerts 100% — kadang ada false positives atau rabbit holes
- **Custom dashboard**: Buat dashboard sendiri untuk phase tracking

---

## 6. Challenge Labs & Exam Strategy

### Challenge Labs

SOC-200 memiliki 13 Challenge Labs yang harus diselesaikan sebelum exam:

| Lab | Name Focus | Phases | Difficulty |
|-----|------------|--------|------------|
| 1 | SIEM Fundamentals | 3 | Beginner |
| 2 | Windows Endpoint Detection | 3 | Beginner |
| 3 | Windows Server Attacks | 4 | Beginner |
| 4 | Windows Client Attacks | 4 | Easy |
| 5 | Privilege Escalation | 4 | Easy |
| 6 | Windows Persistence | 4 | Medium |
| 7 | Linux Detection | 3 | Medium |
| 8 | Network + AV Detection | 4 | Medium |
| 9 | Active Directory Enumeration | 5 | Medium-Hard |
| 10 | Lateral Movement | 5 | Hard |
| 11 | AD Persistence | 6 | Hard |
| 12 | Multi-Phase Attack Chain | 7 | Very Hard |
| 13 | **Exam Prep** | **8** | **Exam-like** |

**Critical Advice:**
- Labs 1-2: Refresher SIEM — cepat saja jika sudah familiar
- Labs 11-13: **WAJIB diselesaikan** — ini yang paling mendekati exam
- Kerjakan setiap lab minimal 1x, idealnya 2x dengan pendekatan berbeda
- Dokumentasi setiap lab seolah-olah itu report exam

### Lab Methodology

**Per-Lab Workflow:**
```
1. Trigger phase → catat waktu mulai
2. Tunggu 10 menit (attacker scripts running)
3. Broad search di window 10 menit itu
4. Identify initial action (entry point)
5. Follow PID chain → reconstruct full attack flow
6. Cross-reference: Windows + Sysmon + PowerShell + Network
7. OSQuery verification (if needed)
8. Document: queries, screenshots, timeline
9. Answer phase questions / collect flags
10. Move to next phase
```

### Gervin's OSA-SOC-200 Videos

OffSec menyediakan video OSA-SOC-200 (Gervin's sessions):
- ~10 video yang membahas challenge labs
- **Strategi**: Coba lab sendiri dulu → baru tonton video untuk apa yang terlewat
- Gervin menunjukkan **query methodology** dan **pattern recognition** yang sangat berguna

### Exam Strategy Details

**Phase 1-3 (Starting):**
- Gunakan pre-built dashboards untuk quick overview
- Catat semua hostnames + IPs dari logs
- Phase 1 biasanya web server entry — cek IIS logs + 4688
- Pastikan Anda menangkap **initial access vector**

**Phase 4-7 (Middle — tersulit):**
- Attacks semakin stealthy — in-memory execution
- Jika stuck: jangan habiskan >30 menit per phase
- **Broaden query**: remove host filter, check all hosts
- **Check other phases**: kadang phase 8 memberi clue untuk phase 4
- Gunakan OSQuery untuk verifikasi aktif

**Phase 8-10 (Final):**
- Biasanya AD-focused (persistence, DCSync, golden ticket)
- Chain dari phase sebelumnya harus nyambung
- Perhatikan domain admin actions

### Report Template

**Gunakan struktur ini untuk report:**

```
1. Executive Summary (1 page)
   - High-level attack narrative (10-15 bullet points)
   - Key findings summary
   - Overall risk assessment

2. Per-Phase Analysis
   Phase 1: [Title]
   - Time window
   - Initial access vector
   - Attacker IP / Victim host
   - MITRE ATT&CK mapping
   - KQL queries used
   - Screenshots (query + result)
   - Detailed analysis of each attacker action
   - Indicators of Compromise (IOCs)

3. Indicators of Compromise (Consolidated)
   - IP addresses
   - Process names and PIDs
   - File hashes
   - Registry keys
   - Service names

4. Detection Rules
   - KQL queries created during analysis
   - Sigma rules (if applicable)

5. Appendices
   - Full query list
   - Timeline of events
   - Host-to-IP mapping
   - OSQuery results
```

### Pre-Exam Checklist

```
Pre-Exam (H-1):
  [ ] Kibana KQL queries prepared (template notebook)
  [ ] Report template ready (per-phase sections)
  [ ] Screenshots folder structure
  [ ] VM updated + snapshotted
  [ ] Snacks + drinks ready
  [ ] Webcam + proctor environment set
  [ ] Plan breaks schedule
  [ ] Notes tool ready (Obsidian / Notion)

During Exam:
  [ ] Phase start time recorded
  [ ] Broad search first → narrow down
  [ ] Screenshot query + result together
  [ ] Document IoCs per phase
  [ ] Add process.command_line column immediately
  [ ] Follow PID chain religiously
  [ ] Check all log sources before concluding
  [ ] OSQuery for verification only
  [ ] 30-min rule: stuck? broaden query or move on
  [ ] Take breaks every 3-4 hours

Post-Exam (24h Report):
  [ ] Executive summary written
  [ ] Per-phase analysis complete
  [ ] Screenshots all organized
  [ ] KQL queries documented
  [ ] IoCs consolidated
  [ ] MITRE ATT&CK mappings
  [ ] PDF/DOCX generated
  [ ] Submit via OffSec Learning Library
```

### Anti-Patterns OSDA

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| **Timeline tunnel vision** | OSDA phases out-of-order | Urutkan berdasarkan phase, bukan timestamp |
| **Ignoring PowerShell 4104** | 4104 captures deobfuscated code | Cari di 4104 dulu sebelum source lain |
| **Not using columns** | Hard to see patterns | Add process.command_line, user.name immediately |
| **Assuming success** | Attacker runs tool but fails | Verify via next event — service installed? process created? |
| **Skipping OSQuery** | Missing active state data | Use OSQuery for network/services verification |
| **Not documenting queries** | Forgot what query found what | Screenshot query + result together |
| **Over-relying on alerts** | Some alerts are rabbit holes | Verify alerts with manual log inspection |

---

## 7. Referensi Lengkap

### Official OffSec Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | SOC-200 Course Page | https://www.offsec.com/courses/soc-200/ |
| 2 | SOC-200 Syllabus (PDF) | https://www.offsec.com/documentation/SOC-200-Syllabus.pdf |
| 3 | OSDA Exam Guide | https://help.offsec.com/hc/en-us/articles/4410105675412-OSDA-Exam-Guide |
| 4 | OSDA Exam FAQ | https://help.offsec.com/hc/en-us/articles/10170036616084-OSDA-Exam-FAQ |
| 5 | SOC-200 FAQ | https://help.offsec.com/hc/en-us/articles/4410194410004-SOC-200-FAQ |
| 6 | SOC-200 Course Overview (PDF) | https://assets.ctfassets.net/82ripq7fjls2/b5qRhY35iq5DcjtrqIupO/df320df830723040f37afce4603c5d65/soc-200-foundational-security-operations-and-defensive-analysis-osda-self-paced.pdf |
| 7 | SOC-200 12-Week Learning Plan | https://help.offsec.com/hc/en-us/articles/15728220061076 |
| 8 | SOC-200 24-Week Learning Plan | https://help.offsec.com/hc/en-us/articles/15714670570004 |
| 9 | SOC-200 Offline Video Mapping | https://help.offsec.com/hc/en-us/articles/22495922633108 |
| 10 | OffSec CPE Credits Info | https://help.offsec.com/hc/en-us/articles/15568144981780 |
| 11 | NICCS — SOC-200 Course Listing | https://niccs.cisa.gov/training/catalog/ata/offsec-soc-200-foundational-security-operations-and-defensive-analysis-osda |

### Exam Reviews & Experiences

| # | Author | Title | Year |
|---|--------|-------|------|
| 12 | Melvin Teo | My Approach to SOC-200 / OSDA | 2026 |
| 13 | Dhanishtha Awasthi | The Defense Story — OSDA Experience | 2026 |
| 14 | Kartik D'souza | SOC-200: OSDA Certification Review | 2025 |
| 15 | Seccult | WTH! Weaponized Threat Hunting — OSDA Review | 2025 |
| 16 | OffSec Team | SOC-200 OSDA Review (Official Blog) | 2023 |
| 17 | Leo Tsaousis | A Hacker's Guide to OSDA | 2024 |
| 18 | OffSec | OSDA Review — OffSec Blog | 2023 |
| 19 | detectrespondrepeat | All About OSDA | 2024 |
| 20 | myshinningstar | My OSDA Journey | 2024 |

### GitHub Repositories

| # | Repository | Author | Description |
|---|------------|--------|-------------|
| 21 | deletehead/SOC-200-OSDA | deletehead | Resources and notes for SOC-200 and OSDA exam |
| 22 | Ilias1988/Hacking-Cheatsheets | Ilias1988 | Blue team log analysis cheatsheets |
| 23 | SwiftOnSecurity/sysmon-config | SwiftOnSecurity | Sysmon configuration template |
| 24 | olafhartong/sysmon-modular | olafhartong | Modular Sysmon configuration |
| 25 | sbousseaden/EVTX-ATTACK-SAMPLES | sbousseaden | Windows event log attack samples |
| 26 | huntresslabs/evtx | huntresslabs | EVTX parser for Python |
| 27 | SigmaHQ/sigma | SigmaHQ | Generic signature format for SIEM |

### Windows Event Log & Sysmon

| # | Resource | URL |
|---|----------|-----|
| 28 | Ultimate Windows Security — Event ID Encyclopedia | https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/ |
| 29 | Microsoft — Windows Security Event ID Reference | https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/sentinel/windows-security-event-id-reference.md |
| 30 | EpicDetect — Event IDs Every SOC Analyst Should Know | https://epicdetect.io/blogs/windows-event-log-ids-soc-analysts |
| 31 | Microsoft — Sysmon Documentation | https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon |
| 32 | SwiftOnSecurity — Sysmon Config Guide | https://github.com/SwiftOnSecurity/sysmon-config |
| 33 | Microsoft — PowerShell Logging Documentation | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging |
| 34 | Microsoft — Advanced Audit Policy | https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/advanced-security-audit |
| 35 | Event ID 4688 — Command Line Auditing | https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688 |
| 36 | Event ID 4104 — Script Block Logging | https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows |
| 37 | Sekoia — Event ID Detection Rules Reference | https://docs.sekoia.io/xdr/features/detect/built_in_detection_rules_eventids/ |
| 38 | MalAPI.io — Windows API to ATT&CK Mapping | https://malapi.io/ |

### Kibana / ELK / KQL

| # | Resource | URL |
|---|----------|-----|
| 39 | Elastic — Kibana Query Language Docs | https://www.elastic.co/guide/en/kibana/current/kuery-query.html |
| 40 | KQL Cheat Sheet | https://pulse.support/kb/kibana-query-language |
| 41 | KQL Cheat Sheet (Cheatography) | https://cheatography.com/thesujit/cheat-sheets/kibana-query-language-kql/ |
| 42 | Elastic — SIEM Detection Rules | https://www.elastic.co/guide/en/security/current/rules-ui-create.html |
| 43 | Elastic — OSQuery Integration | https://www.elastic.co/guide/en/kibana/current/osquery.html |
| 44 | Elastic Stack as SIEM Solution | Multiple sources |
| 45 | HTB — Security Monitoring & SIEM Fundamentals | https://purplebyteone.gitbook.io/ |

### MITRE ATT&CK

| # | Resource | URL |
|---|----------|-----|
| 46 | MITRE ATT&CK Official | https://attack.mitre.org |
| 47 | MITRE ATT&CK Navigator | https://mitre-attack.github.io/attack-navigator/ |
| 48 | MITRE ATT&CK — Enterprise Matrix | https://attack.mitre.org/matrices/enterprise/ |
| 49 | MITRE ATT&CK — Detection | https://attack.mitre.org/docs/ATTACK_Detection_November_2020.pdf |
| 50 | CAR — Cyber Analytics Repository | https://car.mitre.org/ |
| 51 | Atomic Red Team | https://github.com/redcanaryco/atomic-red-team |

### SOC Analysis & Blue Team

| # | Resource | URL |
|---|----------|-----|
| 52 | SOC-CMM — SOC Maturity Model | https://www.soc-cmm.com |
| 53 | SANS — SOC Survey Report | https://www.sans.org/white-papers/soc-survey/ |
| 54 | NIST SP 800-61 Rev 2 (IR Guide) | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |
| 55 | NIST SP 800-92 (Log Management) | https://csrc.nist.gov/pubs/sp/800/92 |
| 56 | SANS — Cyber Kill Chain | https://www.sans.org/white-papers/cyber-kill-chain/ |
| 57 | PICERL Model — SANS IR Framework | https://www.sans.org/white-papers/incident-handlers-handbook/ |
| 58 | OpenExamsPrep — OSDA Practice Questions | https://open-exam-prep.com/practice/osda |

### Detection Engineering

| # | Resource | URL |
|---|----------|-----|
| 59 | Sigma — Generic Signature Format | https://github.com/SigmaHQ/sigma |
| 60 | SIGMA — Rules Repository | https://github.com/SigmaHQ/sigma/tree/master/rules |
| 61 | palantir/windows-event-forwarding | https://github.com/palantir/windows-event-forwarding |
| 62 | Detection Engineering — DetectionLab | https://github.com/clong/DetectionLab |
| 63 | HELK — The Hunting ELK | https://github.com/Cyb3rWard0g/HELK |
| 64 | Velociraptor — DFIR Tooling | https://github.com/Velocidex/velociraptor |
| 65 | Hayabusa — Event Log Fast Forensics | https://github.com/Yamato-Security/hayabusa |

### LOLBINs & Living-off-the-Land

| # | Resource | URL |
|---|----------|-----|
| 66 | LOLBAS — Living Off the Land Binaries | https://lolbas-project.github.io |
| 67 | GTFOBins — Unix Binaries | https://gtfobins.github.io |
| 68 | Red Canary — LOLBIN Detection | https://redcanary.com/threat-detection-theory/lolbins/ |
| 69 | API Of LOLS — LOLBIN API reference | https://lolbas-project.github.io/api/ |
| 70 | Oddvar Moe — PowerShell LOLBINs | https://oddvar.moe/ |

### Labs & Practice

| # | Resource | URL |
|---|----------|-----|
| 71 | Hack The Box — SOC Analyst Track | https://www.hackthebox.com |
| 72 | BTLO (Blue Team Labs Online) | https://blueteamlabs.online |
| 73 | TryHackMe — SOC Level 1 & 2 Paths | https://tryhackme.com |
| 74 | LetsDefend | https://letsdefend.io |
| 75 | CyberDefenders | https://cyberdefenders.org |
| 76 | DetectionLab | https://github.com/clong/DetectionLab |
| 77 | HELK — Hunting ELK Stack | https://github.com/Cyb3rWard0g/HELK |
| 78 | Elastic — Free SIEM Training | https://www.elastic.co/training/ |

### Books

| # | Book | Author |
|---|------|--------|
| 79 | Blue Team Handbook: Incident Response Edition (3rd Ed.) | Don Murdoch |
| 80 | Blue Team Field Manual (BTFM) | Alan White & Ben Clark |
| 81 | The Practice of Network Security Monitoring | Richard Bejtlich |
| 82 | Applied Incident Response | Steve Anson |
| 83 | Operationalizing Threat Intelligence | Kyle Neuman |
| 84 | Hunting Cyber Criminals | Vinny Troia |
| 85 | Windows Internals, Part 1 & 2 (7th Ed.) | Pavel Yosifovich et al. |
| 86 | Practical Malware Analysis | Michael Sikorski & Andrew Honig |
| 87 | The Art of Memory Forensics | Michael Ligh et al. |
| 88 | Investigating Windows Systems | Harlan Carvey |
| 89 | Digital Forensics with Kali Linux | Shiva Parasram |
| 90 | Mastering Windows Security and Hardening | Mark Dunkerley |
| 91 | Practical Binary Analysis | Dennis Andriesse |
| 92 | The Hacker Playbook 3 | Peter Kim |
| 93 | Red Team Field Manual v2 | Ben Clark & Nick Downer |
| 94 | Attacking Network Protocols | James Forshaw |

### Communities

| # | Resource | URL |
|---|----------|-----|
| 95 | r/OSDA Reddit | https://reddit.com/r/osda |
| 96 | OffSec Discord | https://discord.gg/offsec |
| 97 | OffSec Community Forums | https://forums.offsec.com |
| 98 | SOSEC — SOC-200 Study Group | Discord community channels |

### YouTube Videos & Playlists

| # | Channel | Focus | URL |
|---|---------|-------|-----|
| 99 | OffSec Official | Course overviews, exam tips | https://www.youtube.com/@offsectraining |
| 100 | Day Johnson | OSDA review, SOC analyst content | https://www.youtube.com/@DayJohnson |
| 101 | InfosecPat | SOC-200 / OSDA course overview | https://www.youtube.com/watch?v=L_uLv3W6_3g |
| 102 | Gervin (OffSec) | OSA-SOC-200 challenge walkthroughs | OffSec Learning Library |
| 103 | 0xdf | Detection methodology | https://www.youtube.com/@0xdf |
| 104 | John Hammond | Malware analysis, detection | https://www.youtube.com/@JohnHammond010 |
| 105 | I.T. Security Zone | CPENT/OSDA reviews | YouTube |

### Other Resources

| # | Resource | URL |
|---|----------|-----|
| 106 | Windows Event Log — Advanced Audit Policy | https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/advanced-security-auditing |
| 107 | Windows Security Log Events (Microsoft Archives) | https://www.microsoft.com/en-us/download/details.aspx?id=50034 |
| 108 | Elastic Common Schema (ECS) | https://www.elastic.co/guide/en/ecs/current/index.html |
| 109 | OSQuery Schema Documentation | https://osquery.io/schema/ |
| 110 | MISP — Threat Sharing | https://www.misp-project.org/ |
| 111 | The DFIR Report | https://thedfirreport.com |

---

> **Catatan Akhir**: OSDA / SOC-200 adalah fondasi defensive security yang solid — mengajarkan Anda bagaimana attacker bekerja dari sudut pandang deteksi. Fokus pada: (1) kuasai KQL — kecepatan query adalah kunci, (2) pahami behavioral signatures bukan hanya Event IDs, (3) dokumentasi adalah 50% nilai — report yang koheren adalah pembeda pass vs fail, (4) Challenge Labs 11-13 adalah simulasi exam terbaik — jangan skip. Ingat: Anda SOC analyst — tugas Anda merekonstruksi cerita serangan dari log. Bukan menghafal, tapi **menghubungkan titik-titik**.
