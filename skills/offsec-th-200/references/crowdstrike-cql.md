---
name: "CrowdStrike Falcon & CQL Reference"
description: "CrowdStrike Query Language (CQL) for endpoint threat hunting including process analysis, network connections, file operations, and IOA detection."
tags: [crowdstrike, falcon, cql, edr, endpoint-hunting, ioa]
---

# CrowdStrike Falcon & CQL Reference

## Falcon Platform Overview

CrowdStrike Falcon adalah cloud-native EDR platform yang menyediakan endpoint visibility (process creation, network connections, file operations, registry), threat intelligence dari CrowdStrike Threat Graph, IOA detection (behavioral-based), dan CQL untuk custom hunting.

## Common Event Types

| Event | Description |
|-------|-------------|
| `ProcessRollup2` | Process creation |
| `NetworkConnectIP4` | IPv4 network connection |
| `NetworkListenIP4` | Listening for connections |
| `DnsRequest` | DNS query |
| `SyntheticProcessRollup2` | Process termination |
| `PeFileWritten` | PE file written to disk |

## Process Hunting Queries

**All PowerShell executions:**
```
event_simpleName=ProcessRollup2 FileName="powershell.exe"
| table ComputerName, UserName, CommandLine, ParentBaseFileName
```

**Encoded PowerShell:**
```
event_simpleName=ProcessRollup2 FileName="powershell.exe"
| search CommandLine=*-enc*
| table ComputerName, UserName, CommandLine
```

**Suspicious parent-child:**
```
event_simpleName=ProcessRollup2
| eval ChildProcess = FileName, ParentProcess = ParentBaseFileName
| search ParentProcess IN ("winword.exe", "excel.exe", "powerpnt.exe")
  AND ChildProcess IN ("powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe")
```

## Network Hunting Queries

**External connections:**
```
event_simpleName=NetworkConnectIP4
| search NOT RemoteAddressIP4 IN (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
| stats count by ComputerName, RemoteAddressIP4, RemotePort
| sort - count
```

**Beaconing detection:**
```
event_simpleName=NetworkConnectIP4
| eval bucket = floor(_time / 300) * 300
| stats count, values(RemoteAddressIP4) as IPs by ComputerName
| where count > 20 AND count < 500
| eval regularity = round(count / 4)
```

**DNS suspicious domains:**
```
event_simpleName=DnsRequest
| eval domain_len = len(DomainName)
| where domain_len > 30
| stats count by ComputerName, DomainName
| sort - count
```

## File System Hunting

**Executable written to user space:**
```
event_simpleName=PeFileWritten
| search FilePath=*\\Users\\*\\*.exe
| eval IsSuspicious = if(FilePath LIKE "*\\AppData\\Local\\Temp\\*", "HIGH", "MEDIUM")
| table ComputerName, UserName, FileName, FilePath, IsSuspicious
```

## Behavioral Hunting (Without IoCs)

**Process tree analysis — unusual parent-child:**
```
event_simpleName=ProcessRollup2
| search ParentProcess IN ("winword.exe", "excel.exe", "outlook.exe")
  AND ChildProcess IN ("powershell.exe", "cmd.exe", "wscript.exe")
```

**Suspicious execution paths:**
```
event_simpleName=ProcessRollup2
| search FilePath=*\\Users\\*\\AppData\\Local\\Temp\\*
| table ComputerName, UserName, FileName, FilePath, CommandLine
```

**Beaconing via CQL:**
```
event_simpleName=NetworkConnectIP4
| stats count by ComputerName, RemoteAddressIP4, RemotePort
| where count > 50 AND count < 2000
| eval beacon_ratio = round(count / 4)
```

## IOA (Indicator of Attack) Hunting

Falcon IOAs provide behavioral detection: Process Injection, Credential Dumping, Ransomware, Persistence.

```
event_simpleName=IndicatorOfAttackEvent
| table ComputerName, UserName, Severity, Description, PatternName
| sort - Severity
```

## SEARCH Methodology in CQL

**S — Sense:** Broad queries for interesting events
```
event_simpleName=ProcessRollup2
| stats count by ComputerName, FileName
```

**E — Enrich:** Add context
```
event_simpleName=NetworkConnectIP4
| lookup geo_ip_table.csv RemoteAddressIP4 OUTPUT country, city
```

**A — Analyze:** Hypothesis-driven
```
event_simpleName=ProcessRollup2
| search ParentBaseFileName="explorer.exe" AND FileName IN ("powershell.exe", "cmd.exe")
| eval Suspicious = if(CommandLine LIKE "*IEX*" OR CommandLine LIKE "*-enc*", "YES", "NO")
| where Suspicious = "YES"
```

## CQL Performance Tips

- Filter early using indexed fields like `event_simpleName`
- Use `stats` instead of `table` for large datasets
- Limit time range to reduce data scanned
- Use `eval` for computed fields rather than `rex` when possible

## Gotchas

- CQL syntax mirip Splunk tapi tidak identik — perhatikan perbedaan di operator `IN` dan `LIKE`
- CrowdStrike Falcon di exam mungkin memiliki data yang berbeda dari yang terlihat di lab
- IOA events tidak selalu muncul — jika tidak ada, fokus pada ProcessRollup2 dan NetworkConnectIP4
- Field names di CQL menggunakan CamelCase (FileName, CommandLine, ParentBaseFileName)

## Best Practices

- Gunakan `event_simpleName=` sebagai filter pertama untuk efisiensi
- Untuk behavioral hunting, fokus pada ProcessRollup2 karena paling kaya informasi
- Simpan CQL queries yang sudah terbukti di notes untuk akses cepat saat exam
- Kombinasikan CQL dengan Splunk untuk coverage lengkap (breadth + depth)
