---
name: "Endpoint Hunting with Sysmon & Windows Event Logs"
description: "Sysmon Event ID reference, Windows Security Event IDs, Sysmon configuration, and advanced endpoint hunting patterns for threat detection."
tags: [sysmon, windows-event-logs, endpoint-hunting, event-ids, process-tracking]
---

# Endpoint Hunting with Sysmon & Windows Event Logs

## Sysmon Event IDs for Threat Hunting

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

## Windows Security Event IDs

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

## Sysmon Configuration

SwiftOnSecurity sysmon-config adalah community standard:

```xml
<Sysmon schemaversion="4.22">
  <EventFiltering>
    <RuleGroup name="" groupRelation="or">
      <ProcessCreate onmatch="include">
        <CommandLine condition="contains">powershell</CommandLine>
        <CommandLine condition="contains">wscript</CommandLine>
        <CommandLine condition="contains">cscript</CommandLine>
      </ProcessCreate>
    </RuleGroup>
    <RuleGroup name="" groupRelation="or">
      <NetworkConnect onmatch="exclude">
        <Image condition="image">C:\Windows\System32\svchost.exe</Image>
        <DestinationIp condition="is">127.0.0.1</DestinationIp>
      </NetworkConnect>
    </RuleGroup>
  </EventFiltering>
</Sysmon>
```

## Advanced Endpoint Hunting Patterns

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

## Gotchas

- Sysmon Event ID 22 (DNS query) hanya tersedia jika dikonfigurasi — tidak semua environment memilikinya
- Windows Event ID 4104 (PowerShell Script Block) adalah sumber paling kaya untuk hunting PowerShell abuse
- Jangan hanya mengandalkan Event ID 4688 untuk process tracking — Sysmon Event 1 memberikan informasi lebih detail
- Event ID 4662 untuk DCSync detection memerlukan object type GUID yang spesifik — pastikan formatnya benar

## Best Practices

- Hafalkan 10-15 Event ID yang paling sering digunakan untuk hunting
- Gunakan Sysmon Event 1 untuk parent-child process analysis (lebih detail dari 4688)
- Kombinasikan Sysmon Event 3 (network) dengan Event 1 (process) untuk korelasi
- Selalu filter known-good processes untuk mengurangi noise
