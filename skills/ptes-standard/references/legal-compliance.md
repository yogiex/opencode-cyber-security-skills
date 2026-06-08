---
name: "Legal & Compliance Notes"
description: "Compliance requirements for penetration testing including PCI DSS v4.0 (Req 11.4), HIPAA Security Rule, GDPR Article 32, SOC 2/ISO 27001, FedRAMP/FISMA, and cloud provider authorization policies for AWS, Azure, and GCP."
tags: [ptes, compliance, pci-dss, hipaa, gdpr, fedramp, legal, cloud-authorization]
---

# Legal & Compliance Notes

## PCI DSS v4.0 (Requirement 11.4)

- Annual external + internal penetration testing required
- Must follow industry-accepted methodology (PTES, OWASP, NIST SP 800-115)
- Segmentation testing every 6 months
- Testers must be Qualified (independent from CDE operations)
- All findings > CVSS 4.0 require remediation verification retest

## HIPAA Security Rule (45 CFR § 164.306)

- Penetration testing is recommended as part of Risk Analysis
- All ePHI-touching systems should be in scope
- Business Associate Agreements must cover testing and data handling
- Avoid PHI extraction — use synthetic data for PoC

## GDPR (Article 32)

- Requires regular testing of Technical and Organizational Measures (TOMs)
- Penetration testing is strong evidence of TOM effectiveness
- DPIA should inform test scope
- Findings must feed into breach response planning

## SOC 2 / ISO 27001

- Penetration testing is expected as part of vulnerability management
- Annual minimum cadence
- Findings must map to Trust Services Criteria (SOC 2) or Annex A controls (ISO 27001)

## FedRAMP / FISMA

- NIST SP 800-115 is the baseline reference
- Annual penetration testing required
- Results documented in Plan of Action and Milestones (POA&M)

## Cloud Provider Authorization

| Cloud | Pre-approval Needed? |
|-------|---------------------|
| AWS | No (for most services); DDoS prohibited |
| Azure | No; acceptable use policy applies |
| GCP | No; social engineering against Google employees prohibited |

## Best Practices

- Know the regulatory requirements before scoping
- Map findings to compliance controls in the report
- Always verify cloud provider pentest policies before testing
- For healthcare: extra caution with PHI data handling
