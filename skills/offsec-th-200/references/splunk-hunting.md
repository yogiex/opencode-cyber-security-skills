---
name: "Splunk SPL Hunting Queries Reference"
description: "Complete SPL reference for threat hunting including initial access, execution, persistence, credential access, lateral movement, C2, and exfiltration detection."
tags: [splunk, spl, threat-hunting, detection, c2, lateral-movement, persistence]
---

# Splunk SPL Hunting Queries Reference

## Pipeline Fundamentals

```
index=<index> sourcetype=<sourcetype> earliest=<time> latest=<time>
| <command1> [options]
| <command2> [options]
| table <fields>
```

## Core Commands

| Command | Function | Hunting Use |
|---------|----------|-------------|
| `index=` | Select data source | Always specify index first |
| `sourcetype=` | Filter by log type | Narrow to specific log source |
| `stats` | Aggregate & count | Count occurrences by field |
| `eval` | Create calculated fields | Score risk, flag anomalies |
| `rex` | Regex field extraction | Extract IPs, domains from raw logs |
| `transaction` | Group related events | Session analysis |
| `timechart` | Time-series visualization | Beaconing pattern detection |
| `streamstats` | Running calculations | Time-based anomaly detection |
| `lookup` | Enrich from reference | Threat intel enrichment |
| `inputlookup` | Read lookup table | Threat intel CSV ingestion |

## Initial Access Detection

**Phishing — Suspicious Attachment:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*.exe*" ParentProcessName="*OUTLOOK.EXE*"
| table _time, ComputerName, Account, CommandLine
```

**Web Shell Detection:**
```spl
index=iis sourcetype=WinEventLog:IIS
| search cs_uri_stem="*.aspx*" OR cs_uri_stem="*.php*" AND cs_method="POST"
| stats count by cs_uri_stem, c_ip, cs_username
```

**RDP Brute Force:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4625 LogonType=10
| stats count as FailedCount, dc(Account) as UniqueAccounts by src_ip, ComputerName
| where FailedCount > 20
```

## Execution Detection

**PowerShell Encoded Command:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4688
| search CommandLine="*-enc*" OR CommandLine="*-EncodedCommand*"
| table _time, ComputerName, Account, CommandLine, ParentProcessName
```

**PowerShell Script Block (Event 4104):**
```spl
index=windows sourcetype="WinEventLog:Microsoft-Windows-PowerShell/Operational" EventCode=4104
| search ScriptBlockText="*DownloadString*" OR ScriptBlockText="*IEX*" OR ScriptBlockText="*Invoke-*"
| table _time, ComputerName, Account, ScriptBlockText
```

**Sysmon Process Creation (Event 1):**
```spl
index=sysmon EventCode=1
| search CommandLine="*mimikatz*" OR CommandLine="*Invoke-*" OR CommandLine="*-enc*"
| table _time, ComputerName, User, CommandLine, ParentCommandLine
```

## Persistence Detection

**Scheduled Task (Event 4698):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4698
| search NOT TaskName="*Microsoft*"
| table _time, ComputerName, Account, TaskName, Command
```

**Service Installation (Event 7045):**
```spl
index=windows sourcetype=WinEventLog:System EventCode=7045
| search ImagePath="*\\Users\\*" OR ImagePath="*\\Temp\\*"
| table _time, ComputerName, ServiceName, ImagePath, Account
```

**Registry Run Key (Sysmon 13):**
```spl
index=sysmon EventCode=13
| search TargetObject="*\\CurrentVersion\\Run*"
| table _time, ComputerName, User, TargetObject, Details
```

## Credential Access Detection

**LSASS Access (Sysmon 10):**
```spl
index=sysmon EventCode=10
| search TargetImage="*\\lsass.exe"
| where NOT match(SourceImage, "(?i)(svchost|MsMpEng|WerFault|taskmgr|csrss)")
| table _time, ComputerName, SourceImage, SourceUser, GrantedAccess
```

**Mimikatz:**
```spl
index=windows
| search CommandLine="*sekurlsa*" OR CommandLine="*logonpasswords*" OR CommandLine="*privilege::debug*"
| table _time, ComputerName, Account, CommandLine
```

**DCSync (Event 4662):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4662
| search ObjectType="%19195a5b-6da0-11d0-afd3-00c04fd930c7" AND AccessMask="0x100"
| table _time, ComputerName, Account, ObjectName
```

## Lateral Movement Detection

**Pass-the-Hash (4624 Type 3 + NTLM):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=3
| search LogonProcessName="NtLmSsp" AND AccountName!="ANONYMOUS LOGON$"
| stats count by AccountName, ComputerName, WorkstationName, src_ip
```

**PsExec:**
```spl
index=sysmon EventCode=1
| search Image="*\\PSEXESVC.exe" OR ParentImage="*\\PsExec.exe"
| table _time, ComputerName, User, Image, CommandLine
```

**WMI Remote Execution:**
```spl
index=sysmon EventCode=1
| search ParentImage="*\\WmiPrvSE.exe" AND Image="*\\powershell.exe"
| table _time, ComputerName, User, CommandLine
```

**RDP Logons (4624 Type 10):**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624 LogonType=10
| search NOT AccountName="*$"
| table _time, ComputerName, AccountName, src_ip
```

## C2 Detection

**Beaconing — Regular Intervals:**
```spl
index=proxy sourcetype=proxylogs
| stats count, avg(eval(floor(_time/300)*300)) as bucket_avg by src_ip, dest_ip
| where count > 100 AND count < 5000
| eval regularity = round(bucket_avg, 0)
```

**DNS DGA Domains:**
```spl
index=dns sourcetype=dns
| eval domain_len = len(query)
| where domain_len > 25
| stats count by query, src_ip
| where count > 5
```

**Sysmon Network Connection (Event 3) — Non-Internal:**
```spl
index=sysmon EventCode=3
| search NOT DestIp=10.* AND NOT DestIp=192.168.* AND NOT DestIp=172.1[6-9].* AND NOT DestIp=172.2[0-9].* AND NOT DestIp=172.3[0-1].*
| stats count by ComputerName, DestIp, DestPort, Image
```

## Exfiltration Detection

**Large Data Transfer:**
```spl
index=proxy sourcetype=proxylogs
| stats sum(bytes_out) as TotalBytes, max(bytes_out) as MaxBytes by src_ip, dest_ip
| where TotalBytes > 50000000
| eval TotalMB = round(TotalBytes/1048576, 2)
```

**DNS TXT Query Exfiltration:**
```spl
index=dns sourcetype=dns query_type=TXT
| stats count by query, src_ip
| where len(query) > 50
```

## Advanced Threat Hunting Queries

**Unusual Parent-Child Processes:**
```spl
index=sysmon EventCode=1
| where match(ParentImage, "(?i)(winword|excel|powerpnt|outlook|acrord32|firefox|chrome)")
  AND match(Image, "(?i)(powershell|wscript|cscript|cmd|mshta|regsvr32)")
```

**Executable Downloaded to User Space:**
```spl
index=sysmon EventCode=11
| search TargetFilename="*\\Users\\*\\*.exe"
| where TargetFilename!="*OneDrive*"
```

**Account Created then Added to Admin Group:**
```spl
index=windows sourcetype=WinEventLog:Security
| search EventCode=4720 OR EventCode=4732
| transaction AccountName maxpause=1h
| where mvcount(EventCode) > 1
```

**Kerberoasting:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4769
| search TicketEncryptionType=0x17 ServiceName!="*$"
| stats count by AccountName, ServiceName, ClientAddress
| where count > 5
```

**Time-Based Anomaly — Logons Outside Business Hours:**
```spl
index=windows sourcetype=WinEventLog:Security EventCode=4624
| eval hour = strftime(_time, "%H")
| where hour < 6 OR hour > 18
| stats count by AccountName, ComputerName, src_ip
| where count > 10
```

**New Process Followed by Network Connection:**
```spl
index=sysmon
| search EventCode=1 OR EventCode=3
| sort _time
| transaction ComputerName, Image maxpause=1m
| where mvcount(EventCode) > 1 AND mvfind(EventCode, "1")=0 AND mvfind(EventCode, "3")=1
```

## SPL Performance Tips

- Always specify `index=` and `sourcetype=` first
- Use specific time ranges (`earliest=-24h@h latest=now`)
- Filter early in the pipeline
- Use `tstats` for CIM data model acceleration
- Avoid wildcards at the start of strings
- Use `head 100` to test expensive queries before full scope

## Gotchas

- OSTH exam menggunakan Splunk untuk breadth analysis — pastikan query difilter dengan time range yang tepat
- Jangan gunakan `search *` — selalu specify index dan sourcetype untuk performance
- Data model di exam bisa berbeda dari lab — cek field names dengan `| fields _raw` sebelum menjalankan query kompleks
- `transaction` command mahal secara performa — gunakan terbatas dengan maxpause yang sesuai

## Best Practices

- Bangun SPL query library sebelum exam (20+ copy-paste queries)
- Simpan query yang sudah terbukti bekerja di notes
- Dokumentasikan setiap query dengan konteks penggunaannya
- Gunakan komentar di notes (SPL tidak support inline comments)
