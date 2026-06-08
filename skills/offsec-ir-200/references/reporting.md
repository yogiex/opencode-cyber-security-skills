---
name: "Post-Mortem Reporting & Communication Plans"
description: "OSIR exam report structure, executive summary template, incident communication plans, regulatory timelines, and chain of custody."
tags: [reporting, communication, post-mortem, chain-of-custody, templates]
---

# Post-Mortem Reporting & Communication Plans

## Communication Plans

### Pre-Crisis
- Communication tree: siapa di-Cc untuk setiap level severity
- Stakeholder contact list (IT, legal, PR, management, regulator)
- Templates: breach notification draft, press statement draft

### During Crisis
- **Internal**: IR team (Slack/Teams channel), executive briefing
- **External**: Legal (data breach notification), PR (public statement), regulator (GDPR 72h)
- **Victim communication**: jika ada data user yang ter-expose

### Post-Crisis
- After-action report
- Regulatory filing
- Customer notification

### Regulatory Timelines
```
GDPR: 72 hours to notify supervisory authority
HIPAA: 60 days for breach notification
US State Laws: Varies (30-60 days)
SEC (2024): 4 days for material cybersecurity incidents
```

## OSIR Report Template

Gunakan struktur berikut untuk Phase 1 dan Phase 2 report:

```
1. Executive Summary
   - Incident overview (1 paragraph)
   - Key findings (3-5 bullet points)
   - Containment actions summary
   - Current status

2. Timeline of Events
   | Timestamp | Event | Source | Confidence |
   |-----------|-------|--------|------------|

3. Phase 1: SIEM Analysis (Splunk)
   Exercise 1: [Title]
   - Objective
   - SPL Query used
   - Findings (with screenshots)
   - Artifact details (IP, user, process, command)
   Exercise 2-4: (same structure)

4. Phase 2: Forensic Analysis (Autopsy + Volatility)
   Exercise 5: Disk Image Analysis
   - Imaging details (hash, chain of custody)
   - Autopsy ingest results
   - File system artifacts found
   - Keyword search hits
   Exercise 6: Memory Analysis + Malware Triage
   - Volatility analysis results
   - Malware characteristics (type, hash, YARA matches)
   - Static/dynamic analysis summary

5. Containment, Eradication & Recovery
   - Actions taken
   - Timeline of containment
   - Eradication verification
   - Recovery status

6. Incident Classification
   - MITRE ATT&CK mapping
   - Impact assessment (CIA)
   - Severity rating

7. Lessons Learned
   - What went well
   - What could be improved
   - Recommended controls

8. Appendices
   - Full SPL queries
   - Volatility command output
   - YARA rules
   - Evidence inventory (chain of custody)
```

## Chain of Custody Template

| Item # | Description | Source | Hash | Collected By | Date/Time |
|--------|-------------|--------|------|--------------|-----------|
| E-001 | Disk image (evidence.dd) | Host: WEB01 | SHA256: abc... | Analyst | 2026-01-15 09:00 |
| E-002 | Memory dump (memory.raw) | Host: WEB01 | SHA256: def... | Analyst | 2026-01-15 09:05 |
| E-003 | Splunk query results (export) | SIEM | N/A | Analyst | 2026-01-15 10:30 |

## Executive Summary Template

```
On [DATE], at approximately [TIME], [ORGANIZATION] identified suspicious activity on
[HOST/SYSTEM]. Initial detection occurred via [SIEM alert / user report / EDR]. The
incident was classified as [RANSOMWARE / DATA EXFILTRATION / UNAUTHORIZED ACCESS]
with a severity of [CRITICAL / HIGH].

The attacker gained initial access through [VECTOR], then [EXECUTION / PERSISTENCE /
LATERAL MOVEMENT SUMMARY]. A total of [N] systems were affected, including [CRITICAL
SYSTEMS]. [TYPE OF DATA] was compromised.

Immediate containment actions included [ISOLATION / ACCOUNT DISABLE / BLOCK]. The
attacker's [C2 / TOOL] was identified and blocked at [FIREWALL / PROXY]. Eradication
was completed via [REIMAGE / AV SCAN / MANUAL REMOVAL] on [DATE].

Recommendations include: [PATCH / MFA / SEGMENTATION / MONITORING]. Full technical
details are provided in the sections below.
```

## Gotchas

- Report adalah 30 dari 70 points — jangan remehkan. Alokasikan waktu khusus untuk report setelah exam
- Executive summary harus bisa dipahami oleh non-technical stakeholder (management, legal)
- Screenshot harus menyertakan timestamp yang terbaca — screenshot tanpa timestamp tidak berguna untuk report
- Chain of custody adalah komponen yang sering dilupakan — pastikan diisi untuk setiap evidence item

## Best Practices

- Siapkan template report sebelum exam agar tinggal diisi
- Gunakan format PDF/DOCX sesuai ketentuan OffSec
- Pastikan semua exercise questions terjawab di report — jangan sampai ada yang terlewat
- Sertakan MITRE ATT&CK mapping untuk menunjukkan pemahaman TTP
- Lessons learned harus actionable — jangan cuma "improve detection"
