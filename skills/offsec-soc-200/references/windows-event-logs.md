---
name: "Windows Event Log & Sysmon Reference"
description: "Complete reference for Windows Security Event IDs, Sysmon Event IDs, PowerShell logging, and Event-to-Attack mapping for OSDA."
tags: [windows, event-logs, sysmon, powershell, event-ids, detection, osda]
---

# Windows Event Log & Sysmon Reference

## Windows Security Event ID Reference

### Authentication Events

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

### Logon Types (Critical untuk 4624/4625)

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

### Account Management Events

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

### Process & Service Events

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

### Defense Evasion Events

| Event ID | Description |
|----------|-------------|
| **1102** | Security log cleared (almost always malicious) |
| **104** | System log cleared |
| **4719** | Audit policy changed |
| **4657** | Registry value modified |

## Sysmon Event ID Reference

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

## PowerShell Event IDs

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

## Event-to-Attack Mapping

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

## Best Practices

- Selalu cek Logon Type pada Event 4624 — Type 10 (RDP) dan Type 3 (Network) adalah kunci lateral movement
- PowerShell 4104 adalah detection goldmine — prioritaskan sebelum source lain
- Jika melihat 1102 (log cleared) — ini hampir selalu malicious
- Follow PID chain: event 4688 (process creation) + Sysmon 1 (full details) untuk rekonstruksi attack flow
- Sysmon 10 (ProcessAccess to lsass) = hampir pasti credential dumping
