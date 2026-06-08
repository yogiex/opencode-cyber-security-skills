---
name: "Domain 3 — Incident Response and Management (24%)"
description: "CompTIA CySA+ Domain 3 covering attack methodology frameworks (Cyber Kill Chain, Diamond Model, MITRE ATT&CK), 7-phase incident response process (Preparation, Detection, Containment, Eradication, Recovery, Post-Incident), evidence acquisition (chain of custody, hashing, write blockers), containment strategies, and escalation procedures."
tags: [comptia, cysa, incident-response, kill-chain, diamond-model, evidence, containment]
---

# Domain 3: Incident Response and Management (24%)

## Attack Methodology Frameworks

- **Cyber Kill Chain**: Recon → Weaponization → Delivery → Exploitation → Installation → C2 → Actions
- **Diamond Model**: Adversary, Capability, Infrastructure, Victim + meta-features
- **MITRE ATT&CK**: 15 tactics, 200+ techniques for TTP mapping

## IR Process (7 Phases)

1. **Preparation**: IR plan, playbook, tools, training, tabletop exercises
2. **Detection & Analysis**: Triage (true/false positive), timeline, root cause analysis
3. **Containment**: Scope assessment, isolation (network/host/cloud/identity)
4. **Eradication**: Remove malware, patch, reset credentials, rebuild
5. **Recovery**: Restore from backup, monitor for re-infection
6. **Post-Incident Activity**: Forensic analysis, lessons learned
7. (CompTIA consolidates into 4 phases: Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident)

## Evidence Acquisition

- **Chain of Custody**: Tag evidence, log every transfer, secure storage
- **Data Integrity**: SHA256 hashing before/after analysis, write blockers
- **Preservation**: Legal hold, bit-for-bit imaging

## Containment Strategies

| Strategy | Techniques |
|----------|------------|
| Network | Block IP/domain, disable port, segmentation |
| Host | Isolate, disable account, kill process |
| Cloud | Disable API keys, revoke session, isolate instance |
| Identity | Reset credentials, revoke tokens, enable MFA |

## Best Practices

- Define escalation criteria before incidents occur
- Establish clear communication plan per stakeholder
- Document everything — chain of custody is critical
- Conduct post-incident lessons learned for continuous improvement
