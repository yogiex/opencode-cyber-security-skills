---
name: "Phase 3 — Threat Modeling"
description: "PTES Phase 3 covering threat modeling methodologies including STRIDE (system design flaws), PASTA (risk-centric), attack trees, OCTAVE (organizational risk), LINDDUN (privacy), and VAST (Agile/DevSecOps) with framework comparison and output deliverables."
tags: [ptes, threat-modeling, stride, pasta, attack-trees, risk-assessment]
---

# Phase 3: Threat Modeling

## Objectives

Identify critical assets and potential attackers. Map attack vectors and likely paths. Prioritize vulnerabilities based on business impact.

## Methodologies Comparison

| Method | Focus | Best For |
|--------|-------|----------|
| STRIDE | System design flaws | Microsoft SDL, app sec |
| PASTA | Risk-centric, 7 stages | Enterprise risk management |
| Attack Trees | Goal-oriented decomposition | Single system depth |
| OCTAVE | Organizational risk | CISOs, program-level |
| LINDDUN | Privacy threats | GDPR compliance |
| VAST | Agile/DevSecOps | Continuous threat modeling |

## Questions to Answer

- What are we protecting? (data, availability, reputation)
- Who is the adversary? (script kiddie, APT, insider)
- What are their goals? (data theft, defacement, ransomware)
- What attacks are most likely?

## Output

- List of prioritized threats (High/Medium/Low)
- Attack surface diagram
- Risk matrix

## Best Practices

- STRIDE for technical system analysis, PASTA for business context
- Attack trees excel for single-component deep dives
- For compliance-heavy engagements, pair with OCTAVE
- In DevSecOps pipelines, VAST enables continuous threat modeling
