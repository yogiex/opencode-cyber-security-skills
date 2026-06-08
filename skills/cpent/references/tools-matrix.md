---
name: "CPENT Tools Matrix — Essential & Static Binaries"
description: "Curated tools matrix for CPENT exam including critical tools (nmap, Burp Pro, sqlmap, Metasploit, Ligolo-ng, Impacket, BloodHound), static binaries for target upload, and essential wordlists for password cracking and web directory fuzzing."
tags: [tools, nmap, burp, sqlmap, metasploit, ligolo-ng, impacket, wordlists]
---

# CPENT Tools Matrix

## Essential Tools

| Tool | Purpose | Priority |
|------|---------|----------|
| nmap | Port scanning, service detection, NSE | Critical |
| Burp Suite Pro | Web app proxy, scanner, intruder | Critical |
| sqlmap | Automated SQL injection | Critical |
| Metasploit | Exploitation framework | Critical |
| Ligolo-ng | TUN-based pivoting | Critical |
| Chisel | HTTP tunnel pivoting | Critical |
| netexec | SMB/WMI/WinRM/SSH enum | Critical |
| Impacket | wmiexec, psexec, secretsdump | Critical |
| BloodHound | AD attack path visualization | High |
| Certipy | AD CS enumeration & attack | High |
| ffuf/feroxbuster | Web directory fuzzing | High |
| Responder | NTLM relay & capture | High |
| hashcat | Password cracking (GPU) | High |

## Static Binaries (Upload ke Target)

- nc (netcat) — cross-platform
- ligolo-ng agent — single binary
- chisel — single binary
- socat — port forwarding
- tcpdump — network capture
- busybox — embedded Linux Swiss army knife
- python3 static — jika target tidak punya Python
- curl/wget static — download tools

## Wordlists

```bash
/usr/share/wordlists/rockyou.txt                    # Password cracking
/usr/share/seclists/Discovery/Web-Content/common.txt # Web directories
/usr/share/seclists/Usernames/Names/names.txt        # User enumeration
```

## Best Practices

- Siapkan static binaries sebelum exam — compile di lingkungan yang sama
- Prioritaskan Ligolo-ng untuk pivoting (TUN-based, native tool support)
- Burp Pro dan sqlmap allowed — gunakan untuk akselerasi
- Wordlists siapkan di Kali default + SecLists tambahan
