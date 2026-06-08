---
name: "CPENT 14 Module Deep-Dive"
description: "Complete breakdown of EC-Council CPENT's 14 core modules covering advanced Windows/Linux attacks, web exploitation, binary exploitation 32/64-bit, wireless, IoT, OT/SCADA, cloud, mobile, pivoting, evasion, and report writing."
tags: [cpent, modules, syllabus, course-content]
---

# CPENT 14 Module Deep-Dive

## Modul 1: Advanced Windows Attacks

Pass-the-Hash, Overpass-the-Hash, DCSync, Kerberos attacks (AS-REP, Kerberoasting, Silver/Golden Ticket), SMB relay. Skala lebih besar dari OSCP — multiple domain, forest trust, cross-domain.

## Modul 2: Advanced Linux Attacks

Kernel exploitation (Dirty Pipe, PwnKit), cron persistence, LD_PRELOAD abuse, SUID shell escape, capabilities abuse. Kernel exploit boleh digunakan — CPENT environment biasanya stable.

## Modul 3: Web Application Exploitation — Part 1

No tool restrictions. sqlmap, Burp Pro, parallel scanning. SQLi advanced, XSS, SSRF, file inclusion.

## Modul 4: Web Application Exploitation — Part 2

Command injection, file upload exploitation, server-side template injection (SSTI), XXE, API testing.

## Modul 5: Exploitation Fundamentals — Part 1

General exploitation methodology: public exploit adaptation, custom payload generation, AV evasion basics.

## Modul 6: Exploitation Fundamentals — Part 2

Metasploit advanced usage: resource scripts, module development, post-exploitation modules.

## Modul 7: Binary Exploitation 32-bit

Stack overflow x86: fuzzing, EIP offset, badchars, JMP ESP, shellcode generation.

## Modul 8: Binary Exploitation 64-bit

x64 calling conventions (fastcall), ROP chains, ROPgadget tool, ASLR bypass via ROP, structured exception handling (SEH).

## Modul 9: Wireless Attacks

WPA/WPA2 cracking (handshake capture, PMKID), WPS PIN attack, Evil Twin, deauthentication, wireless reconnaissance.

## Modul 10: IoT Exploitation

Default credentials, exposed debug interfaces, firmware analysis, MQTT enumeration, HTTP entry into internal networks.

## Modul 11: OT/SCADA Exploitation

Modbus protocol enumeration, PLC manipulation, insecure protocol exploitation, DNP3, industrial control system security.

## Modul 12: Cloud & Mobile

Cloud enumeration basics, mobile application testing, API endpoint discovery.

## Modul 13: Double Pivoting

Dua lapis jaringan. Pivot 1 → subnet A → host dual-home → Pivot 2 → subnet B → target.

## Modul 14: Report Writing

30% dari nilai. Executive summary, methodology, network diagram, detailed findings per target, remediations, appendices.

## Best Practices

- Fokus di modul 1-2 (Windows/Linux attacks) dan 7-8 (binary exploitation)
- Double pivoting (modul 13) adalah pembeda utama dari OSCP
- IoT/SCADA (modul 10-11) adalah zone-specific — pelajari protocol dasar
- Report writing (modul 14) jangan disepelekan — 30% nilai
