---
name: "OSEP Exam Strategy — Challenge Labs & Time Management"
description: "Complete exam strategy guide for OSEP including 8 challenge labs overview, 48-hour time management plan, attack path framework, screenshot requirements, and pre/during/post-exam checklists."
tags: [osep-exam, exam-strategy, challenge-labs, time-management, checklist]
---

# OSEP Exam Strategy

## Challenge Labs

| Lab | Focus |
|-----|-------|
| 1 | Phishing + VBA basics |
| 2 | AV evasion fundamentals |
| 3 | AppLocker/CLM bypass |
| 4 | Process injection techniques |
| 5 | MSSQL attacks + lateral movement |
| 6 | AD exploitation + delegation |
| 7 | **CowMotors** — retired exam |
| 8 | **DenkiAir** — retired exam |

Kerjakan setiap lab minimal 2 kali dengan pendekatan berbeda.

## 48h Time Management

```
Day 1 (16-18 jam):
  00:00-01:00  — Parallel enumeration
  01:00-04:00  — Initial access
  04:00-07:00  — Foothold → BloodHound
  07:00-09:00  — Break + sleep 2h
  09:00-12:00  — Lateral movement → privesc
  12:00-14:00  — AD exploitation
  14:00-16:00  — Cross-domain
  16:00-18:00  — Documentation
  18:00-22:00  — SLEEP (critical)

Day 2 (12-14 jam):
  00:00-01:00  — Review + re-enumeration
  01:00-04:00  — Push stuck machines
  04:00-07:00  — Final push → secret.txt
  07:00-09:00  — Collect remaining flags
  09:00-12:00  — Finalize screenshots
  12:00-14:00  — Report draft
```

## Screenshot Requirements

- Terminal harus menampilkan IP address + hostname + flag content
- Web shell NOT sufficient — harus reverse shell interaktif
- RDP screenshot NOT accepted — harus via command line
- Submit semua flag ke control panel SEBELUM exam ends

## Pre-Exam Checklist

- Kali VM updated + snapshotted
- Windows VM (VS + Office) ready
- All C2 profiles configured
- Payload automation scripts tested
- AMSI bypass scripts prepared (multiple methods)
- AppLocker bypass payloads ready
- Process injection/hollowing C# code compiled
- VBA macros + JScript + HTA files ready
- Python XOR/AES encoder ready
- Note-taking tool with OSEP template
- BloodHound collector hosted
- Tools: Impacket, NetExec, Certipy, Rubeus, Mimikatz

## Best Practices

- Revert is a strategy: stuck >30 menit? revert
- 30-minute rule: stuck? try different bypass/approach
- Dokumentasi setiap flag IMMEDIATELY
- Sleep 6-8 hours — marathon bukan sprint
- Aim for 150+ points (minimum 100)
