---
name: "19 Module Deep-Dive"
description: "Complete breakdown of all 19 SOC-200 modules with detection patterns, key concepts, and mindset per module."
tags: [osda, modules, detection, windows, linux, siem, active-directory, offsec]
---

# 19 Module Deep-Dive

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

## Best Practices

- Module 17-18 adalah yang paling kritis — fokus belajar di sini
- Module 2 (Attacker Methodology) adalah fondasi mindset — jangan skip
- Module 19 adalah simulasi exam — kerjakan serius
- Setiap module memiliki "Mindset" takeaway — baca itu sebagai prioritas
