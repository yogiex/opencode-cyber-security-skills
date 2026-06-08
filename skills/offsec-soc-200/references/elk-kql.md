---
name: "SIEM: ELK Stack, KQL & OSQuery"
description: "Kibana Query Language reference, common OSDA detection queries, OSQuery SQL reference, and SIEM dashboard tips."
tags: [kql, elk, kibana, osquery, siem, queries, detection, osda]
---

# SIEM: ELK Stack, KQL & OSQuery

## Kibana Query Language (KQL) Reference

### Basic Queries

```kql
# Field-value search
event.code : 4625

# Free text search (across all fields)
"svc-sql1"

# Wildcard
user.name : admin*

# Exists
_exists_ : process.command_line
```

### Boolean Logic

```kql
# AND (implied between conditions)
event.code : 4625 AND user.name : administrator

# OR
event.code : (4625 OR 4771)

# NOT
NOT event.code : 4634

# Complex
(event.code : 4625 OR event.code : 4771) AND host.name : "DC01"
```

### Comparison Operators

```kql
# Numeric comparison
event.code >= 4624 AND event.code <= 4625

# Time range
@timestamp >= "2024-01-01T00:00:00.000Z"

# Exists
_exists_ : source.ip
```

### Common OSDA Detection Queries

```kql
# Find all logons (success + failure)
event.code : (4624 OR 4625)

# Failed logons from specific IP
event.code : 4625 AND source.ip : "192.168.1.100"

# Service installs in last 24h
event.code : (7045 OR 4697)

# Process with encoded PowerShell
process.command_line : *-enc*

# All PowerShell script block logs
event.code : 4104

# Registry persistence detection
event.code : 13 AND registry.path : *Run*

# Scheduled tasks created
event.code : 4698

# Network connections from unknown processes
event.code : 3 AND NOT process.name : "svchost.exe"

# Lateral movement: RDP logons
event.code : 4624 AND winlog.event_data.LogonType : 10

# Kerberoasting: multiple service tickets
event.code : 4769 AND winlog.event_data.TicketEncryptionType : 0x17
```

### Broad Query Strategy (Start Here)

```
Start broad → add specific filters:
1. event.code : * (semua events)
2. Add time range: @timestamp >= phase_start
3. Add host filter: host.name : "web01"
4. Add event.code filter to narrow
5. Add column: process.command_line, user.name
6. Follow PID chain
```

### Column Layout Penting

```
Always add these columns:
- @timestamp
- event.code
- host.name
- process.name
- process.command_line
- process.pid
- process.parent.pid
- user.name
- user.related
- source.ip
- winlog.event_data.LogonType
```

## OSQuery Reference

OSQuery digunakan untuk **active verification** — query state langsung dari endpoint:

```sql
-- All running processes
SELECT * FROM processes;

-- Specific process search
SELECT name, path, pid, parent FROM processes WHERE name LIKE '%powershell%';

-- Listening ports (detect backdoors)
SELECT * FROM listening_ports;

-- Network connections (detect beacons)
SELECT * FROM process_open_sockets;

-- DNS cache (recent resolutions)
SELECT * FROM dns_responses;

-- Services (detect persistence)
SELECT * FROM services WHERE path LIKE '%temp%';

-- Scheduled tasks
SELECT * FROM scheduled_tasks;

-- User accounts
SELECT * FROM users;

-- Running queries from user
SELECT * FROM processes WHERE name LIKE '%sql%' OR name LIKE '%cmd%';

-- Firewall rules
SELECT * FROM firewall_rules;
```

**Kapan menggunakan OSQuery di exam:**
- Verifikasi apakah service benar-benar terinstall (cek services table)
- Verifikasi apakah network connection benar-benar ada (process_open_sockets)
- Cek listening ports untuk backdoor detection
- Cross-check process list dengan process creation events

## Imported Dashboards (Exam Tips)

Pre-built dashboards di ELK sangat membantu:
- **Pre-built alerts**: Beberapa alerts sudah dikonfigurasi oleh OffSec
- **Gunakan sebagai starting point**: Alerts menandai aktivitas mencurigakan
- **Verifikasi manual**: Jangan percaya alerts 100% — kadang ada false positives atau rabbit holes
- **Custom dashboard**: Buat dashboard sendiri untuk phase tracking

## Best Practices

- KQL adalah primary weapon — kecepatan query = kecepatan detection
- Selalu tambahkan `process.command_line` dan `user.name` sebagai columns
- Broad query dulu, narrow down dengan PIDs
- OSQuery untuk verifikasi — jangan sebagai primary detection tool
- Cross-reference minimal 2 log sources sebelum konklusi
