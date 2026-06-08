---
name: "Reconnaissance & Enumeration Framework"
description: "Systematic enumeration methodology for OSCP including 3 attack vectors (vulnerable versions, misconfigurations, sensitive information), Nmap workflow, and per-service enumeration checklists for ports 21-27017."
tags: [enumeration, reconnaissance, nmap, attack-vectors, service-enumeration]
---

# Reconnaissance & Enumeration Framework

## 3 Attack Vectors Methodology

Setiap fase (initial access, privilege escalation, AD) harus menggunakan siklus berulang:

```
Enumerate 3 Vectors → Analyze → Prioritize → Attack → Escalate/Pivot → Re-enumerate 3 Vectors
```

### A. Vulnerable Versions
Service version diketahui → cari public exploit:
```bash
searchsploit service_name version
```
Setiap versi adalah potensi CVE. Versi lawas (Apache 2.4.49, OpenSSL, SMBv1) sering punya public exploit.

### B. Misconfigurations
- Default credentials (admin:admin, root:toor)
- Anonymous FTP, SMB null session
- Directory listing enabled
- Weak file permissions
- Sudo misconfiguration (NOPASSWD, LD_PRELOAD)
- SUID/SGID pada binary custom
- Unquoted service paths (Windows)
- AlwaysInstallElevated (Windows)
- Token privileges (SeImpersonate, SeBackup, SeDebug)

Misconfigurations lebih reliable daripada kernel exploit. Cek ini dulu.

### C. Sensitive Information
- Database credentials di config files (wp-config.php, .env)
- SSH keys world-readable
- Bash/PowerShell history
- Backup files (*.bak, *.old, ~)
- Hardcoded API keys/tokens
- Registry entries (Windows)
- Unattended installation files (unattend.xml, autounattend.xml)

Credentials adalah emas. Setiap credential harus segera dicoba di SEMUA service lain.

## Nmap Workflow Optimal

```bash
# Step 1: Fast full port scan
nmap -Pn -p- --min-rate 10000 -T4 $IP -oA nmap/allports

# Step 2: Service version + default scripts
nmap -Pn -sC -sV -p $PORTS $IP -oA nmap/services
```

## Service Enumeration per Port

| Port | Service | Checklist |
|------|---------|-----------|
| 21 | FTP | Anonymous login? Version exploits? Writable directory? |
| 22 | SSH | Version exploits? Default creds? Key-based auth? |
| 25 | SMTP | User enumeration (VRFY, EXPN)? Open relay? |
| 53 | DNS | Zone transfer? Subdomain enumeration? |
| 80/443 | HTTP/S | Web app full checklist |
| 139/445 | SMB | Null session? Share listing? EternalBlue? |
| 389/636 | LDAP | Anonymous bind? Dump domain info? |
| 161 | SNMP | Public community string? |
| 2049 | NFS | showmount -e? no_root_squash? |
| 3306 | MySQL | Root login? Version exploits? |
| 3389 | RDP | Version? BlueKeep? Creds reuse? |
| 5985/5986 | WinRM | Credentialed access? Evil-WinRM? |
| 6379 | Redis | No-auth access? RCE via cron/SSH key? |
| 8080 | HTTP-alt | Same as 80/443 |
| 27017 | MongoDB | No-auth access? Data dump? |

## Best Practices

- Jangan hanya scan port umum — service kritis sering di high ports
- Simpan output dengan `-oA` untuk bukti report
- Credential stuffing: setiap credential langsung di-test ke semua service
- Re-enumerate setelah dapat akses — running services dari dalam bisa reveal attack path baru
- Stuck >30 menit? Re-enumerate, jangan gali rabbit hole
