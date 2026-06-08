---
name: "OSTH Hunt Report Template"
description: "Professional hunt report template for OSTH exam including executive summary, timeline, IoCs table, MITRE ATT&CK mapping, and recommendations."
tags: [report-template, osth, exam, hunt-narrative]
---

# OSTH Hunt Report Template

## Executive Summary

```
Hunt Overview:
[One paragraph describing the hunt scope, methodology, and key findings]

Key Findings:
- [Finding 1]
- [Finding 2]
- [Finding 3]

Threat Actor Attribution: [APT Group / Unattributed]
Overall Risk Assessment: [CRITICAL / HIGH / MEDIUM / LOW]
```

## Hypothesis & Methodology

```
Initial Hypothesis:
"[Adversary TTP] on [system] using [technique] to achieve [goal]"

Data Sources Used:
- Splunk: [indexes and sourcetypes]
- CrowdStrike Falcon: [event types]
- Suricata: [alert categories]
- Other: [Zeek, DNS, Proxy, etc.]

Hunting Methodology:
- [Intel-Based / Hypothesis-Driven / Baseline]
```

## Hunt Narrative — Timeline

| Timestamp | Event | Host | Source | TTP (MITRE) | Confidence |
|-----------|-------|------|--------|-------------|------------|
| YYYY-MM-DD HH:MM | Initial access via... | WEB01 | Splunk (IIS) | T1190 | High |

### Finding 1: [Title]

- **Description**: [Detailed description of finding]
- **Query used**: `[SPL or CQL query]`
- **Evidence**: [Screenshot reference]
- **Artifact details**: IP, hash, user, process, registry key
- **MITRE ATT&CK**: [Tactic] - [Technique ID] - [Technique Name]

### Finding 2-7: (same structure)

## IOCs Table

| Type | Value | Context | First Seen | Host |
|------|-------|---------|------------|------|
| IP | 185.234.72.1 | C2 server | YYYY-MM-DD HH:MM | WEB01 |
| SHA256 | a1b2c3... | Malicious binary | YYYY-MM-DD HH:MM | WEB01 |
| Domain | evil-malware.xyz | C2 domain | YYYY-MM-DD HH:MM | WEB01 |
| Registry | HKLM\...\Run\Malware | Persistence | YYYY-MM-DD HH:MM | WEB01 |

## Impact Assessment

```
Systems Affected:
- Hostname 1 (IP, role)
- Hostname 2 (IP, role)

Data Exfiltrated/Encrypted:
- [Type and volume of data]

Attacker Objectives Achieved:
- [Objective 1]
- [Objective 2]
```

## MITRE ATT&CK Mapping

| Tactic | Technique ID | Technique | Observed |
|--------|-------------|-----------|----------|
| Initial Access | T1190 | Exploit Public-Facing App | Yes |
| Execution | T1059.001 | PowerShell | Yes |
| Persistence | T1543.003 | Windows Service | Yes |

## Recommendations

```
### Detection Recommendations
- [Rule/alert to add]

### Prevention Recommendations
- [Configuration change, patch, control]

### Hunting Recommendations
- [Future hunt hypothesis or data source to add]
```

## Appendices

```
- Complete SPL/CQL Queries
- Full Timeline
- Evidence Inventory
- Screenshots
```

## Chain of Custody

| Item | Description | Source | Hash | Collected By | Date/Time |
|------|-------------|--------|------|--------------|-----------|
| E-001 | Splunk query results (export) | SIEM | N/A | Analyst | YYYY-MM-DD HH:MM |
| E-002 | CrowdStrike event export | Falcon | SHA256: ... | Analyst | YYYY-MM-DD HH:MM |
| E-003 | Suricata alert log | Network | SHA256: ... | Analyst | YYYY-MM-DD HH:MM |
