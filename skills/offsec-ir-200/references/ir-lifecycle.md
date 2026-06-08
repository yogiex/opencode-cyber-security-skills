---
name: "IR Lifecycle & Incident Responder Framework"
description: "NIST SP 800-61 Rev 2 lifecycle, CSIRT roles, ITIL incident vs problem, severity matrices, and IR golden rules."
tags: [nist, csirt, itil, severity, lifecycle, ir-framework]
---

# IR Lifecycle & Incident Responder Framework

## NIST SP 800-61 Rev 2 Lifecycle

```
1. Preparation
   - IR plan, playbooks, tools, training
   - Communication tree (who calls whom)
   - Pre-deployed collection: Sysmon, PowerShell logging, audit policy

2. Detection & Analysis
   - Alert triage (SIEM, EDR, user report)
   - IOC sweep + threat intelligence
   - Attack chain reconstruction
   - Impact assessment

3. Containment, Eradication & Recovery
   - Short-term: isolate host, block IP
   - Long-term: remove malware, rebuild
   - Recovery: restore from clean backup
   - Validation: verify eradication

4. Post-Incident Activity
   - Lessons learned
   - Evidence retention
   - Report writing
   - Control improvements
```

## CSIRT Roles

| Role | Responsibility |
|------|---------------|
| **Incident Commander** | Overall coordination, decisions |
| **Technical Lead** | Forensics, malware analysis, containment |
| **Communications Lead** | Stakeholder updates, regulatory notifications |
| **Legal Counsel** | Chain of custody, privilege, compliance |
| **Scribe** | Timeline documentation, evidence tracking |

CSIRT Types: Internal, external (MSSP), virtual/coordinated. Tiers: Tier 1 (triage) → Tier 2 (investigation) → Tier 3 (forensics/threat intel).

## ITIL Incident vs Problem

| | Incident | Problem |
|---|----------|---------|
| **Definition** | Unplanned interruption | Root cause of incidents |
| **Goal** | Restore service ASAP | Prevent recurrence |
| **Example** | Server infected with ransomware | Missing patch + weak config |
| **IR Focus** | Contain + eradicate | Root cause analysis |

## Severity Matrices

```
CRITICAL: PII exposed, Ransomware, DC compromised → <1h response
HIGH: Suspicious admin activity, malware on server → 2-4h
MEDIUM: Phishing campaign, policy violation → 24h
LOW: Scan, failed login spike → scheduled
```

## 3 Pertanyaan Kunci Saat Stuck

1. **"What is the blast radius?"** — Systems, data, users affected? Prioritaskan containment.
2. **"What does the timeline tell me?"** — Reconstruct sequence. Look for gaps (possible log tampering).
3. **"Have I checked all three sources?"** — Splunk logs, disk artifacts, memory artifacts. Missing one = incomplete picture.

## Golden Rules OSIR

1. **Follow the NIST 800-61r2 lifecycle** — Jangan loncat fase.
2. **Document as you go** — Laporan adalah 30 dari 70 points. Screenshot setiap langkah dengan timestamp.
3. **Splunk is your timeline** — Logs adalah sumber kebenaran utama.
4. **Disk tells the story** — File system artifacts mengungkapkan apa yang tidak tercatat di SIEM.
5. **Memory reveals the truth** — Malware in-memory tidak terlihat di disk.
6. **Contain first, ask later** — Jika host aktif menimbulkan kerusakan, isolate dulu.
7. **Communication is part of IR** — Management perlu executive summary, bukan technical dump.

## Gotchas

- OSIR exam tidak menguji ITIL secara mendalam — cukup tahu perbedaan Incident vs Problem dan CSIRT roles
- Severity matrix di exam bisa berbeda dari yang dipelajari — baca skenario dengan teliti
- CSIRT tiers berbeda dengan SOC tiers — jangan tertukar

## Best Practices

- Buat IR plan template sebelum exam agar tidak mulai dari nol
- Hafalkan NIST lifecycle 4 phases dan urutannya
- Gunakan Diamond Model (Adversary → Infrastructure → Capability → Victim) untuk analisis insiden
