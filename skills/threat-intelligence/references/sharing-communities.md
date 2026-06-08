---
name: "Sharing & Communities — ISACs, CISA AIS & NIST 800-150"
description: "Threat intelligence sharing frameworks including ISACs by sector (FS-ISAC, H-ISAC, MS-ISAC), CISA Automated Indicator Sharing (AIS) via STIX/TAXII, NIST SP 800-150 recommendations, TLP marking requirements, and sharing best practices for machine-readable formats and confidence scoring."
tags: [cti, sharing, isac, cisa-ais, nist-800-150, tlp, information-sharing]
---

# Sharing & Communities

## ISACs by Sector

- **FS-ISAC** — Financial services
- **H-ISAC** — Healthcare
- **E-ISAC** — Electricity/energy
- **MS-ISAC** — State/local/tribal government
- **Auto-ISAC** — Automotive
- **IT-ISAC** — Information technology

## CISA Automated Indicator Sharing (AIS)

Real-time machine-readable IOC exchange via STIX/TAXII:
- Bidirectional sharing — receive federal intel, submit own
- Default anonymization of submitter identity
- TLP marking required (default: TLP:GREEN)
- Legal protection under CISA 2015
- Free participation — requires PKI certificate + TAXII 2.1 client

## NIST SP 800-150 Key Recommendations

- Establish information sharing rules (TLP, handling guidance)
- Define trust models for sharing partners
- Participate in ISACs, CERTs, government repositories
- Protect PII — strip personal information
- Create sharing agreements before incidents occur

## Sharing Best Practices

- Apply consistent TLP markings to all shared intelligence
- Include confidence scores and estimative language
- Provide context (not just raw IOCs) — map to ATT&CK
- Strip PII not directly related to the threat
- Use machine-readable formats (STIX 2.1, MISP) for automation
