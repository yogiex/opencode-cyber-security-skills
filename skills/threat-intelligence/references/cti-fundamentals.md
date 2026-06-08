---
name: "CTI Fundamentals & Intelligence Lifecycle"
description: "Cyber Threat Intelligence fundamentals covering 4 intelligence levels (strategic, operational, tactical, technical), the 6-phase intelligence cycle, Priority Intelligence Requirements (PIRs), Collection Management Framework (CMF), and source reliability assessment using the Admiralty Scale."
tags: [cti, intelligence-cycle, pir, intelligence-levels, collection-management]
---

# CTI Fundamentals & Intelligence Lifecycle

## Intelligence Levels

| Level | Audience | Timeframe | Example Output |
|-------|----------|-----------|----------------|
| Strategic | Executives, board | Months-years | Threat landscape reports, geopolitical risk |
| Operational | SOC managers, hunters | Days-weeks | Campaign tracking, TTP changes |
| Tactical | SOC analysts | Hours-days | IOCs, SIEM rules |
| Technical | Malware analysts | Real-time-hours | Malware signatures, C2 analysis |

## The 6-Phase Intelligence Cycle

1. **Planning & Direction** — Define PIRs, identify stakeholders, establish CMF
2. **Collection** — Gather data from OSINT, telemetry, feeds, dark web, ISACs
3. **Processing** — Normalize to STIX/MISP, deduplicate, enrich, apply TLP/confidence
4. **Analysis** — Apply analytic frameworks (Kill Chain, Diamond, ATT&CK), produce intel
5. **Dissemination** — Deliver to stakeholders (tactical: SIEM feeds; strategic: board reports)
6. **Feedback** — Evaluate utility, adjust PIRs and collection priorities

## PIRs (Priority Intelligence Requirements)

Effective PIRs are specific, answerable, and tied to decisions:
- "Which threat actors are targeting our industry sector?"
- "What TTPs are being used in ransomware attacks against our region?"
- "Are our exposed credentials appearing on criminal marketplaces?"

## Collection Management Framework (CMF)

| Source Type | Examples | Reliability |
|-------------|----------|-------------|
| OSINT | Shodan, VirusTotal, Abuse.ch | Medium |
| Commercial | Recorded Future, Mandiant | High |
| Government | CISA AIS, NCSC | High |
| ISACs | FS-ISAC, H-ISAC | High |
| Internal | EDR, DNS logs, SIEM | Very High |

## Best Practices

- Start with PIRs before collecting anything
- Match intelligence level to audience needs
- Apply consistent confidence scoring and TLP markings
- Close the feedback loop — evaluate intelligence utility
