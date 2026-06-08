---
name: "Phase 7 — Reporting"
description: "PTES Phase 7 covering report structure (executive summary, technical findings, risk assessment), risk scoring frameworks (CVSS v3.1, DREAD, FAIR, OWASP), reporting templates, and quality checklist for penetration testing deliverables."
tags: [ptes, reporting, cvss, executive-summary, risk-assessment, templates]
---

# Phase 7: Reporting

## Objectives

Communicate findings clearly to technical and executive audiences. Provide actionable remediation steps. Demonstrate business risk.

## Report Structure

1. **Executive Summary** — Objective, scope, overall posture, top 3 risks
2. **Technical Findings** — Per finding: title, risk rating, description, evidence, reproduction steps, remediation
3. **Risk Assessment Table** — Finding, CVSS, Impact, Likelihood, Risk Rating
4. **Methodology Summary** — Phases performed, tools used
5. **Appendix** — Scan outputs, test cases, exploit code

## Risk Scoring Frameworks

- **CVSS v3.1** — Industry standard (base/temporal/environmental)
- **DREAD** — Damage, Reproducibility, Exploitability, Affected users, Discoverability
- **FAIR** — Quantitative risk analysis ($ amounts)
- **OWASP Risk Rating** — Likelihood + Impact for business context

## Executive Summary Must Answer

1. What was tested and why?
2. What is the worst thing an attacker could do?
3. How bad is the overall risk?
4. What are the top 3 things to fix immediately?
5. What is the general remediation timeline?

## Technical Finding Requirements

- Precise title, CVSS vector + score, CWE/CVE reference
- Reproduction steps detailed enough for dev to verify
- Evidence: sanitized screenshots, request/response pairs
- Business impact specific to this environment
- Remediation: actionable, version/technology-specific

## Quality Checklist

- [ ] All findings have evidence
- [ ] False positives excluded
- [ ] Remediation steps are specific (e.g., "change value X in file Y")
- [ ] No sensitive client data in raw logs
- [ ] Report encrypted when sent

## Best Practices

- Technical audience: detailed reproduction steps
- Executive audience: business impact, risk quantification
- Use CVSS for technical severity, FAIR for business risk
- Include remediation timeline (immediate/short-term/long-term)
