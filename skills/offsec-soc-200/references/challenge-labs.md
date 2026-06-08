---
name: "Challenge Labs & Exam Strategy"
description: "Complete strategy for OSDA challenge labs, exam phase methodology, report structure, and anti-patterns to avoid."
tags: [osda, exam, strategy, challenge-labs, report, methodology]
---

# Challenge Labs & Exam Strategy

## Challenge Labs

SOC-200 memiliki 13 Challenge Labs yang harus diselesaikan sebelum exam:

| Lab | Name Focus | Phases | Difficulty |
|-----|------------|--------|------------|
| 1 | SIEM Fundamentals | 3 | Beginner |
| 2 | Windows Endpoint Detection | 3 | Beginner |
| 3 | Windows Server Attacks | 4 | Beginner |
| 4 | Windows Client Attacks | 4 | Easy |
| 5 | Privilege Escalation | 4 | Easy |
| 6 | Windows Persistence | 4 | Medium |
| 7 | Linux Detection | 3 | Medium |
| 8 | Network + AV Detection | 4 | Medium |
| 9 | Active Directory Enumeration | 5 | Medium-Hard |
| 10 | Lateral Movement | 5 | Hard |
| 11 | AD Persistence | 6 | Hard |
| 12 | Multi-Phase Attack Chain | 7 | Very Hard |
| 13 | **Exam Prep** | **8** | **Exam-like** |

**Critical Advice:**
- Labs 1-2: Refresher SIEM — cepat saja jika sudah familiar
- Labs 11-13: **WAJIB diselesaikan** — ini yang paling mendekati exam
- Kerjakan setiap lab minimal 1x, idealnya 2x dengan pendekatan berbeda
- Dokumentasi setiap lab seolah-olah itu report exam

### Lab Methodology

**Per-Lab Workflow:**
```
1. Trigger phase → catat waktu mulai
2. Tunggu 10 menit (attacker scripts running)
3. Broad search di window 10 menit itu
4. Identify initial action (entry point)
5. Follow PID chain → reconstruct full attack flow
6. Cross-reference: Windows + Sysmon + PowerShell + Network
7. OSQuery verification (if needed)
8. Document: queries, screenshots, timeline
9. Answer phase questions / collect flags
10. Move to next phase
```

### Gervin's OSA-SOC-200 Videos

OffSec menyediakan video OSA-SOC-200 (Gervin's sessions):
- ~10 video yang membahas challenge labs
- **Strategi**: Coba lab sendiri dulu → baru tonton video untuk apa yang terlewat
- Gervin menunjukkan **query methodology** dan **pattern recognition** yang sangat berguna

## Exam Strategy Details

**Phase 1-3 (Starting):**
- Gunakan pre-built dashboards untuk quick overview
- Catat semua hostnames + IPs dari logs
- Phase 1 biasanya web server entry — cek IIS logs + 4688
- Pastikan Anda menangkap **initial access vector**

**Phase 4-7 (Middle — tersulit):**
- Attacks semakin stealthy — in-memory execution
- Jika stuck: jangan habiskan >30 menit per phase
- **Broaden query**: remove host filter, check all hosts
- **Check other phases**: kadang phase 8 memberi clue untuk phase 4
- Gunakan OSQuery untuk verifikasi aktif

**Phase 8-10 (Final):**
- Biasanya AD-focused (persistence, DCSync, golden ticket)
- Chain dari phase sebelumnya harus nyambung
- Perhatikan domain admin actions

### Report Template

**Gunakan struktur ini untuk report:**

```
1. Executive Summary (1 page)
   - High-level attack narrative (10-15 bullet points)
   - Key findings summary
   - Overall risk assessment

2. Per-Phase Analysis
   Phase 1: [Title]
   - Time window
   - Initial access vector
   - Attacker IP / Victim host
   - MITRE ATT&CK mapping
   - KQL queries used
   - Screenshots (query + result)
   - Detailed analysis of each attacker action
   - Indicators of Compromise (IOCs)

3. Indicators of Compromise (Consolidated)
   - IP addresses
   - Process names and PIDs
   - File hashes
   - Registry keys
   - Service names

4. Detection Rules
   - KQL queries created during analysis
   - Sigma rules (if applicable)

5. Appendices
   - Full query list
   - Timeline of events
   - Host-to-IP mapping
   - OSQuery results
```

## Anti-Patterns OSDA

| Anti-Pattern | Why It Fails | Fix |
|-------------|--------------|-----|
| **Timeline tunnel vision** | OSDA phases out-of-order | Urutkan berdasarkan phase, bukan timestamp |
| **Ignoring PowerShell 4104** | 4104 captures deobfuscated code | Cari di 4104 dulu sebelum source lain |
| **Not using columns** | Hard to see patterns | Add process.command_line, user.name immediately |
| **Assuming success** | Attacker runs tool but fails | Verify via next event |
| **Skipping OSQuery** | Missing active state data | Use OSQuery for network/services verification |
| **Not documenting queries** | Forgot what query found what | Screenshot query + result together |
| **Over-relying on alerts** | Some alerts are rabbit holes | Verify alerts with manual log inspection |

## Best Practices

- Documentation is 50% of your grade — report yang koheren adalah pembeda pass vs fail
- Challenge Labs 11-13 adalah simulasi exam terbaik — jangan skip
- Jika stuck >30 menit: broaden query atau pindah phase
- Anti-pattern checklist: cek sebelum submit report
