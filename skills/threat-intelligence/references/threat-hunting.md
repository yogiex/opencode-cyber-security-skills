---
name: "Threat Hunting — PEAK, ABLE, HMM & Query Examples"
description: "Threat hunting methodology covering PEAK framework (Prepare-Execute-Act), ABLE hypothesis model (Actor-Behavior-Location-Evidence), Hunting Maturity Model (HMM), three hunt approaches (TTP-based, IOC-based, compliance-based), essential data sources, and query examples for Splunk, Elastic, and Microsoft Sentinel."
tags: [cti, threat-hunting, peak, able, hmm, hunting-queries, data-sources]
---

# Threat Hunting

## PEAK Framework (David Bianco / Splunk)

Prepare → Execute → Act, with three hunt types:

| Type | Description |
|------|-------------|
| Hypothesis-Driven | Form testable hypothesis from threat intelligence |
| Baseline Hunting | Search for deviations from established norms |
| Model-Assisted (M-ATH) | Statistical/ML models surface anomalies |

## ABLE Hypothesis Model

- **Actor**: Who is the threat actor or threat category?
- **Behavior**: What specific TTP are you hunting for?
- **Location**: Where in the environment would you find evidence?
- **Evidence**: What data source + query pattern confirms the behavior?

## Hunting Maturity Model (HMM)

| Level | Description |
|-------|-------------|
| 0 — Initial | Relies entirely on automated alerts |
| 1 — Minimal | IOC-based searching from threat feeds |
| 2 — Procedural | Documented TTP-based hunt playbooks |
| 3 — Innovative | Novel hypotheses from intel + environment |
| 4 — Leading | Automated hypotheses + ML anomaly detection |

## Three Hunt Approaches

**TTP-based (highest value):** Hunt for technique behaviors. TTPs harder to change than IOCs. Example: Kerberoasting (T1558.003) — RC4 TGS-REQ spikes.

**IOC-based (lowest value):** Sweep for known-bad indicators. Short shelf life. Automate with SIEM + EDR.

**Compliance-based:** Policy violations, legacy protocols, misconfigurations.

## Essential Data Sources

| Source | Key Telemetry |
|--------|--------------|
| EDR | Process creation, network, file writes |
| Windows Security Log | 4624/4625/4648/4662/4688/4768/4769 |
| Sysmon | Process (1), network (3), process access (10) |
| DNS Logs | Query patterns, DGA, beaconing |
| PowerShell (4104) | Script block logging |
| Network Flow | NetFlow/IPFIX, beaconing |

## Query Examples

**Splunk:** `index=windows EventCode=4624 LogonType=10 | stats count by Account_Name`

**Elastic (EQL):** `sequence by process.pid [process where process.name == "rundll32.exe"] [network where event.type == "connection"]`

**Sentinel (KQL):** `SecurityEvent | where EventID == 4769 | summarize TGS_Count = count() by Account`

## Hunt Execution Workflow

1. Intake intelligence → 2. Form hypothesis → 3. Identify data source → 4. Write query → 5. Execute & iterate → 6. Document findings → 7. Create detection → 8. Archive

## Best Practices

- Prioritize TTP-based hunting over IOC-based
- Time-box each hunt (5-30 min)
- Convert successful hunts into automated detection rules
- Track hunt program effectiveness with metrics
