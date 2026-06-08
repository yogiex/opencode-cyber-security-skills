---
name: "Splunk SIEM & SPL Reference"
description: "Splunk Search Processing Language (SPL) reference with OSIR-specific detection queries for Windows Event Logs and Sysmon."
tags: [splunk, spl, siem, detection, windows-event-logs, sysmon]
---

# Splunk SIEM & SPL Reference

## Pipeline Fundamentals

SPL menggunakan pipe (`|`) untuk mengalirkan data:

```
index=<index> sourcetype=<sourcetype> [filters]
| <command1> [options]
| <command2> [options]
| table <fields>
```

## Core Commands (80% of SOC work)

| Command | Function | Example |
|---------|----------|---------|
| `index=` | Select data source | `index=windows` |
| `sourcetype=` | Filter by log type | `sourcetype=WinEventLog:Security` |
| `stats` | Aggregate & count | `stats count by Account` |
| `eval` | Create calculated fields | `eval risk=if(EventCode=4625, "HIGH", "LOW")` |
| `rex` | Regex field extraction | `rex field=_raw "IP=(?<ip>\d+\.\d+\.\d+\.\d+)"` |
| `transaction` | Group related events | `transaction session_id maxpause=30m` |
| `table` | Select output columns | `table _time, Account, src_ip` |
| `sort` | Sort results | `sort -count` |
| `dedup` | Remove duplicates | `dedup Account` |
| `timechart` | Time-series aggregation | `timechart count by EventCode` |
| `top` | Most common values | `top limit=10 Account` |
| `where` | Eval-based filter | `where count > 10` |
| `lookup` | Enrich from reference data | `lookup geo_ip src_ip OUTPUT country` |
| `fields` | Keep/remove fields | `fields + Account, src_ip` |
| `rename` | Rename fields | `rename Account as Username` |
| `convert` | Convert field types | `convert timeformat="%Y-%m-%d" ctime(_time)` |
| `streamstats` | Running calculations | `streamstats count by Account` |

## OSIR Detection Queries

### Failed Logons (4625) — Brute Force Detection
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4625
| stats count as FailedCount, dc(Account) as UniqueAccounts by src_ip
| where FailedCount > 20
| sort -FailedCount
```

### Successful Logon (4624) — Track Access
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624
| table _time, Account, ComputerName, LogonType, src_ip
| sort _time
```

### RDP Logons (4624 + LogonType=10) — Lateral Movement
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=10
| table _time, Account, ComputerName, src_ip
| sort -_time
```

### Pass-the-Hash Indicators (4624 Type 3 + NTLM)
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=3 LogonProcessName=NtLmSsp 
| stats count by Account, ComputerName, src_ip
```

### Service Creation (7045 / 4697) — Persistence
```spl
index=windows sourcetype=WinEventLog:System EventCode=7045
| table _time, ServiceName, ImagePath, Account, ComputerName
```

### Process Creation (4688) — Suspicious Commands
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*powershell*" OR CommandLine="*cmd.exe*" OR CommandLine="*wscript*"
| table _time, Account, CommandLine, ComputerName, ParentProcessName
```

### Scheduled Task Creation (4698) — Persistence
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4698
| table _time, Account, TaskName, Command, ComputerName
```

### Account Creation (4720) — Backdoor Account
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4720
| table _time, Account, TargetAccount, ComputerName
```

### Admin Group Modification (4728/4732/4756)
```spl
index=windows sourcetype=WinEventLog:Security EventCode IN (4728, 4732, 4756)
| search GroupName="Domain Admins" OR GroupName="Administrators" OR GroupName="Enterprise Admins"
| table _time, Account, TargetAccount, GroupName, ComputerName
```

### Log Clearing (1102) — Defense Evasion
```spl
index=windows sourcetype=WinEventLog:Security EventCode=1102
| table _time, Account, ComputerName
```

### Kerberoasting (4769 + RC4)
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4769 TicketEncryptionType=0x17
| stats count by Account, ServiceName, ClientAddress
| sort -count
```

### PowerShell Script Block (4104)
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" EventCode=4104
| table _time, ComputerName, Account, ScriptBlockText
```

### Sysmon Process Creation (EventCode 1)
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1
| search CommandLine="*mimikatz*" OR CommandLine="*Invoke-*" OR CommandLine="*-enc*"
| table _time, ComputerName, User, CommandLine, ParentCommandLine
```

### Sysmon Network Connection (EventCode 3) — C2 Detection
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3
| search NOT DestIp=10.* AND NOT DestIp=192.168.* AND NOT DestIp=172.16.*
| stats count by ComputerName, DestIp, DestPort, Image
| sort -count
```

### Sysmon DNS Query (EventCode 22) — DGA Detection
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=22
| stats count by ComputerName, QueryName
| sort -count
```

### Threat Hunting — Beaconing Detection
```spl
index=proxy sourcetype=proxylogs
| stats count by src_ip, dest_ip
| where count > 50 AND count < 500
| eval regularity = count / 24
```

### Threat Hunting — LSASS Access (Sysmon 10)
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=10
| search TargetImage="*\\lsass.exe"
| where NOT match(SourceImage, "(?i)svchost|MpEng|taskmgr|csrss")
| table _time, ComputerName, SourceImage, SourceUser, GrantedAccess
```

## SPL Performance Tips

- Always specify `index=` and `sourcetype=` first
- Always set a time range (earliest/latest)
- Filter early in the pipeline, transform later
- Use `| head 100` to test expensive queries
- Use `fields` to reduce data volume
- Use `tstats` for data model acceleration (if available)

## Splunk Enterprise Security (ES) Concepts

- **CIM (Common Information Model)**: Standardized field names across data sources
- **ESCU (Enterprise Security Content Updates)**: Pre-built correlation searches
- **Risk-Based Alerting (RBA)**: Accumulate risk scores instead of direct alerts
- **Threat Intelligence Framework**: Import STIX/TAXII feeds
- **SOAR/Phantom**: Playbook automation for containment actions

## Gotchas

- Di exam, pastikan time range yang digunakan benar — default "All Time" bisa menyebabkan hasil tidak akurat atau timeout
- SPL di exam Splunk bisa memiliki data model yang berbeda dari lab — selalu cek field names dengan `| fields _raw` dulu
- Sysmon EventCode 22 (DNS) tidak selalu tersedia — tergantung konfigurasi Sysmon di environment exam

## Best Practices

- Simpan query favorites di Notepad/notes selama exam
- Gunakan `| table` di akhir query untuk mengontrol output — jangan tampilkan raw data
- Dokumentasikan setiap query dengan komentar (SPL tidak support comment inline — tulis di notes terpisah)
