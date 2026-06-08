---
name: "Phase Deep-Dives & Response Style"
description: "Expanded PTES guidance including scoping questionnaire, advanced OSINT levels (L1-L3), tool-by-phase matrix, and standards comparison (PTES vs OWASP WSTG vs NIST SP 800-115 vs OSSTMM vs ISSAF) with complementary usage patterns."
tags: [ptes, deep-dive, scoping, osint-levels, tools-matrix, standards-comparison]
---

# Phase Deep-Dives

## Response Style

When asked about a specific phase: state objectives, list 2-3 key activities, mention typical tools, give concrete example. Always emphasize legal authorization.

## Tool-by-Phase Matrix

| Tool | Phase | Purpose |
|------|-------|---------|
| Nmap | 2 (IG) | Port scanning, service detection |
| Amass | 2 (IG) | Subdomain enumeration |
| Nessus | 4 (VA) | Vulnerability scanning |
| Nuclei | 4 (VA) | Template-based vuln scanner |
| Burp Suite | 4 (VA) / 5 (EX) | Web app scanning & exploitation |
| Metasploit | 4 (VA) / 5 (EX) / 6 (PE) | Exploitation framework |
| sqlmap | 5 (EX) | Automated SQL injection |
| Hashcat | 5 (EX) | Password cracking |
| Mimikatz | 6 (PE) | Windows credential dumping |
| BloodHound | 3 (TM) / 6 (PE) | AD attack path mapping |
| Impacket | 5 (EX) / 6 (PE) | Windows protocol suite |
| Chisel | 6 (PE) | TCP/UDP tunnel over HTTP |
| Ligolo-ng | 6 (PE) | Tunneling/pivoting |
| Prowler | 4 (VA) | Cloud security assessment |

## Standards Comparison

| Aspect | PTES | OWASP WSTG | NIST SP 800-115 | OSSTMM |
|--------|------|------------|-----------------|--------|
| Scope | Full engagement | Web apps + APIs | IT infrastructure | All security channels |
| Approach | 7-phase | 91 test cases | 4-phase | Metrics-based |
| Exploitation | Deep | Per-test case | Moderate | Varies |
| Threat modeling | Dedicated phase | Not covered | Not covered | Trust analysis |
| Post-exploitation | Dedicated | Not covered | Not covered | Channel-dependent |

**Complementary usage:** PTES for lifecycle, OWASP WSTG for web depth within Phase 4-5, NIST for compliance, MITRE ATT&CK for red team ops.

## Best Practices

- PTES + OWASP WSTG = most effective combination for web app pentests
- For compliance: PTES lifecycle + NIST control mapping + CVSS scoring
- For red teams: PTES pre-engagement → MITRE ATT&CK for execution
