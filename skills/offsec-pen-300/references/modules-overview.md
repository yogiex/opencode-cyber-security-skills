---
name: "PEN-300 16 Module Deep-Dive"
description: "Complete breakdown of all 16 PEN-300 course modules covering OS/programming theory, client-side execution, process injection, AV/EDR evasion, AMSI bypass, AppLocker bypass, network filters, Linux lateral movement, kiosk breakouts, credentials, Windows lateral movement, MSSQL attacks, AD exploitation, ADCS, and final integration."
tags: [pen-300, osep, modules, syllabus, course-content]
---

# PEN-300 16 Module Deep-Dive

## Modul 1: Operating System and Programming Theory

Fundamental programming untuk payload development:

- **Win32 API basics**: `VirtualAlloc`, `CreateThread`, `WaitForSingleObject`, `OpenProcess`, `WriteProcessMemory`, `CreateRemoteThread`
- **C# P/Invoke**: Marshaling, DllImport, StructLayout untuk memanggil Windows API dari .NET
- **PowerShell reflection**: Akses assembly internal via `[Ref].Assembly.GetType()`
- **Process architecture**: PEB, TEB, user space vs kernel space, ring protection

## Modul 2: Client-Side Code Execution with Office

VBA macro development untuk phishing:

- **AutoOpen / Document_Open**: Entry point untuk VBA macro
- **XOR/Caesar cipher**: Encode shellcode di VBA
- **PowerShell download cradle**: VBA execute PowerShell → AMSI bypass → shellcode runner
- **WMI dechain**: Gunakan WMI untuk spawn proses dari VBA

## Modul 3: Client-Side Code Execution with JScript

JScript execution via Windows Script Host (WSH):

- **HTA file**: `.hta` dieksekusi oleh `mshta.exe`
- **WScript.Shell**, **XMLHttpRequest**, **ADODB.Stream**
- **DotNetToJScript**: Load .NET assembly from JScript

## Modul 4: Process Injection and Migration

Lihat [process-injection.md](./process-injection.md) untuk detail lengkap.

## Modul 5: Introduction to Antivirus Evasion

Lihat [av-edr-evasion.md](./av-edr-evasion.md).

## Modul 6: Advanced Antivirus Evasion

Lihat [av-edr-evasion.md](./av-edr-evasion.md).

## Modul 7: Application Whitelisting

Lihat [av-edr-evasion.md](./av-edr-evasion.md).

## Modul 8: Bypassing Network Filters

**DNS Filters**: DNS tunneling (iodine, dnscat2), DoH
**Web Proxies**: Domain fronting via CDN, Hidden.asmx, HTTPS inspection bypass
**IDS/IPS Evasion**: Payload fragmentation, encoding, SSL/TLS

## Modul 9: Linux Lateral Movement

**Shared Library Hijacking**: `LD_PRELOAD / LD_LIBRARY_PATH`
**VI/Vim Backdoor**: Modeline exploit, plugin backdoor
**SSH Key Persistence**: authorized_keys, SSH config tunneling

## Modul 10: Kiosk Breakouts

Browser escape, Task Manager, Windows key, shortcut abuse, Sticky Keys, Utilman.exe

## Modul 11: Windows Credentials

Lihat [referensi.md](./referensi.md) untuk tools.

- **Mimikatz**: `privilege::debug`, `sekurlsa::logonpasswords`, `lsadump::dcsync`
- **SAM Hive Dumping**: `reg save HKLM\SAM` + `impacket-secretsdump`
- **LSASS Dump**: Procdump, Task Manager dump
- **Other sources**: PowerShell history, browser passwords, RDP credentials, GPP cpassword, WSL

## Modul 12: Windows Lateral Movement

- **RDP**: Restricted Admin mode, PTH via xfreerdp
- **Fileless**: WMI, WinRM, PowerShell Remoting, SMB exec, DCOM
- **Mindset**: Get credentials → Test all protocols → Find receptive service → Execute

## Modul 13: Microsoft SQL Attacks

Lihat [mssql-attacks.md](./mssql-attacks.md).

## Modul 14: Active Directory Exploitation

Lihat [ad-exploitation.md](./ad-exploitation.md).

## Modul 15: ADCS

Lihat [ad-exploitation.md](./ad-exploitation.md).

## Modul 16: Combining the Pieces

Integrasi semua teknik ke dalam attack chain:

```
1. Phishing → VBA macro → AMSI bypass → C2 beacon
2. BloodHound → delegation misconfiguration
3. RBCD abuse → DA on Domain A
4. Dump DC → trust key → cross-forest
5. ADCS ESC1 → Enterprise Admin
6. DCSync → full forest compromise → secret.txt
```

## Best Practices

- Setiap modul dibangun di atas modul sebelumnya — kuasai secara berurutan
- Fokus pada modul 4-7 dan 13-15 yang paling sering diuji di exam
- Praktikkan setiap teknik minimal 3 kali sebelum lanjut
