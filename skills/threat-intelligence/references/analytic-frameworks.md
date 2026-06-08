---
name: "Analytic Frameworks — Kill Chain, ATT&CK, Diamond Model"
description: "Core CTI analytic frameworks covering Cyber Kill Chain (7 stages), MITRE ATT&CK (tactics, techniques, procedures), Diamond Model (adversary-capability-infrastructure-victim), F3EAD (intelligence-driven operations), and Structured Analytic Techniques (SATs) for mitigating cognitive bias."
tags: [cti, analytic-frameworks, kill-chain, mitre-attack, diamond-model, sat]
---

# Analytic Frameworks

## Cyber Kill Chain (Lockheed Martin, 2011)

Seven sequential stages: Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives.

Defenders need to break the chain at any single point. Prioritize early-chain disruption.

## MITRE ATT&CK (v15)

Non-linear matrix of 14 tactics, 200+ techniques, sub-techniques, and procedures:
- **Tactics**: Initial Access, Execution, Persistence, Privesc, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, C2, Exfiltration, Impact
- **Techniques**: T1133 External Remote Services, T1078 Valid Accounts, T1566 Phishing
- **Groups**: 140+ named threat actors mapped to techniques
- **Software**: 700+ tools and malware families

Use ATT&CK Navigator for detection coverage gap analysis.

## Diamond Model (2013)

Four core features: Adversary, Capability, Infrastructure, Victim. Six pivot paths — any two vertices define a relationship. Find one element → pivot along edges to discover unknown infrastructure or new victims.

## F3EAD

Find → Fix → Finish → Exploit → Analyze → Disseminate. Intelligence-driven operations cycle adapted from military targeting for incident response.

## Structured Analytic Techniques (SATs)

| Technique | Purpose |
|-----------|---------|
| Analysis of Competing Hypotheses (ACH) | Evaluate multiple explanations |
| Key Assumptions Check | Surface hidden premises |
| Indicators of Change | Define metrics for adversary shifts |
| Deception Detection | Check for planted misdirection |
| Devil's Advocacy | Challenge prevailing analysis |
| What If? Analysis | Explore alternative futures |

## Estimative Language

| Confidence | Definition |
|------------|------------|
| High | Strong evidence, multiple independent sources |
| Moderate | Some evidence, partially corroborated |
| Low | Limited evidence, single source |

## Best Practices

- Combine frameworks for richer analysis (Kill Chain + ATT&CK + Diamond)
- Use SATs to mitigate cognitive biases
- Always express confidence levels in assessments
- Map to ATT&CK for standardized adversary behavior taxonomy
