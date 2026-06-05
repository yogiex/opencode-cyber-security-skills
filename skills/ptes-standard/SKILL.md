---
name: ptes-standard
description: Penetration Testing Execution Standard (PTES) - comprehensive guide for conducting penetration tests across 7 phases: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, and reporting. Use when planning or executing penetration tests, security assessments, or when user asks about PTES methodology.
license: MIT
compatibility: opencode
metadata:
  source: PTES
  version: "1.0"
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
