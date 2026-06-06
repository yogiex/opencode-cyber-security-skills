---
name: threat-intelligence
description: Cyber Threat Intelligence (CTI) - lifecycle, intelligence frameworks, IOC management, threat hunting, analyst tradecraft. Use when gathering threat intelligence, performing threat hunting, managing IOCs, conducting intelligence-driven analysis, or when user asks about CTI lifecycle, TIP platforms, STIX/TAXII, MISP, OpenCTI, or structured analytical techniques.
license: MIT
metadata:
  source: CTI (community)
  version: "1.0"
---

# Threat Intelligence — CTI Lifecycle, IOC Management, and Threat Hunting

You are an expert in cyber threat intelligence. Provide structured, actionable guidance based on the intelligence lifecycle, analytic frameworks, and threat hunting methodology.

## When to Use This Skill

Invoke this skill when:
- User asks about cyber threat intelligence lifecycle, frameworks, or analyst tradecraft.
- User mentions STIX, TAXII, MISP, OpenCTI, or threat intelligence platforms.
- User asks about indicators of compromise (IOCs), YARA, Sigma, or TLP.
- User needs guidance on threat hunting, hypothesis-driven analysis, or proactive detection.
- User asks about threat actor profiling, attribution, or finished intelligence reporting.

---

## CTI Fundamentals & Lifecycle

### Intelligence Levels

| Level | Audience | Timeframe | Example Output |
|-------|----------|-----------|----------------|
| **Strategic** | Executives, CISOs, board | Months-years | Threat landscape reports, geopolitical risk assessments, industry trends |
| **Operational** | SOC managers, threat hunters, IR leads | Days-weeks | Campaign tracking, threat actor TTP changes, attack path analysis |
| **Tactical** | SOC analysts, detection engineers | Hours-days | Indicators of compromise (IPs, domains, hashes), SIEM rules |
| **Technical** | Malware analysts, reverse engineers | Real-time-hours | Malware signatures, C2 protocol analysis, exploit artifacts |

### The 6-Phase Intelligence Cycle

1. **Planning & Direction** — Define Priority Intelligence Requirements (PIRs). Identify stakeholders, assets to protect, decision points. Establish Collection Management Framework (CMF).
2. **Collection** — Gather raw data from OSINT, internal telemetry, threat feeds, dark web, ISACs, HUMINT, SIGINT, closed forums.
3. **Processing** — Normalize into structured format (STIX, MISP). Deduplicate, enrich, validate. Apply TLP markings and confidence scores.
4. **Analysis** — Apply analytic frameworks (Kill Chain, Diamond Model, ATT&CK). Use structured analytic techniques. Produce finished intelligence.
5. **Dissemination** — Deliver to stakeholders. Tactical: SIEM/SOAR/EDR feeds. Operational: threat bulletins. Strategic: board reports.
6. **Feedback** — Evaluate intelligence utility. Adjust PIRs, collection priorities, and analytic methods for next cycle.

### Priority Intelligence Requirements (PIRs)

PIRs are the foundation of intelligence-driven operations. Effective PIRs are specific, answerable, and tied to decisions:
- "Which threat actors are targeting our industry sector?"
- "What TTPs are being used in ransomware attacks against our region?"
- "Are our exposed credentials appearing on criminal marketplaces?"

### Collection Management Framework (CMF)

Map each PIR to collection sources, assign source reliability (Admiralty Scale A-F), define collection frequency, and identify gaps.

| Source Type | Examples | Reliability |
|-------------|----------|-------------|
| OSINT | Shodan, Censys, VirusTotal, Abuse.ch, AlienVault OTX | Medium |
| Commercial | Recorded Future, Mandiant Advantage, Intel 471 | High |
| Government | CISA AIS, US-CERT, NCSC | High |
| ISACs | FS-ISAC, H-ISAC, MS-ISAC | High |
| Internal | EDR telemetry, DNS logs, proxy logs, SIEM | Very High |
| Dark Web | Flashpoint, ZeroFox, SOCMINT | Variable |
| Human (HUMINT) | Law enforcement, industry partnerships | High (vetted) |

---

## Analytic Frameworks

### Cyber Kill Chain (Lockheed Martin, 2011)

Seven sequential stages of intrusion — defenders need to break the chain at any single point:

1. **Reconnaissance** — Harvest emails, identify infrastructure
2. **Weaponization** — Couple payload with exploit
3. **Delivery** — Email, web, USB
4. **Exploitation** — Trigger the exploit
5. **Installation** — Deploy backdoor/RAT
6. **Command & Control (C2)** — Establish communication channel
7. **Actions on Objectives** — Data exfiltration, ransomware, destruction

**Analyst use:** Map observed adversary behavior to kill chain phases. Identify detection gaps per phase. Prioritize early-chain disruption.

### MITRE ATT&CK (v15, Enterprise + Mobile + ICS)

Non-linear matrix of adversary tactics (14), techniques (200+), sub-techniques, and procedures:
- **Tactics:** The "why" — Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, C2, Exfiltration, Impact
- **Techniques:** The "how" — T1133 External Remote Services, T1078 Valid Accounts, T1566 Phishing
- **Procedures:** Specific implementation — specific malware, tool, or command used
- **Groups:** 140+ named threat actor groups mapped to techniques
- **Software:** 700+ tools, malware families mapped to techniques

**Analyst use:** Standardized adversary behavior taxonomy. Hunt for specific techniques relevant to your threat model. Map detection coverage gaps using ATT&CK Navigator.

### Diamond Model (Caltagirone, Pendergast, Betz, 2013)

Four core features with relationships:

```
         Adversary
        /         \
Infrastructure -- Capability
        \         /
          Victim
```

- **Adversary:** The threat actor or intrusion set
- **Capability:** Tools, techniques, malware used
- **Infrastructure:** IPs, domains, servers, C2 infrastructure
- **Victim:** Target organization, person, system

**Six pivot paths:** Any two vertices define a relationship. Find one element of a known adversary -> pivot along edges to discover unknown infrastructure or new victims.

### F3EAD (Find-Fix-Finish-Exploit-Analyze-Disseminate)

Intelligence-driven operations cycle adapted from military targeting for incident response and CTI:
- **Find:** Intelligence collection, reconnaissance
- **Fix:** Corroborate, localize, attribute
- **Finish:** Contain, remediate
- **Exploit:** Extract IOCs, TTPs from incident
- **Analyze:** Produce intelligence from findings
- **Disseminate:** Share intelligence back to stakeholders

### Structured Analytic Techniques (SATs)

SATs mitigate cognitive biases in intelligence analysis:

| Technique | Purpose | When to Use |
|-----------|---------|-------------|
| Analysis of Competing Hypotheses (ACH) | Evaluate multiple explanations against evidence | Attribution, root cause analysis |
| Key Assumptions Check | Surface hidden premises of analysis | Threat actor assessment |
| Indicators of Change | Define observable metrics for adversary shifts | Campaign tracking |
| Deception Detection | Check for deliberately planted misdirection | Analyzing adversary infrastructure |
| Devil's Advocacy | Challenge prevailing analysis | Peer review, intelligence vetting |
| What If? Analysis | Explore alternative futures | Strategic forecasting |

**Estimative Language & Confidence:**
| Confidence Level | Definition |
|----------------|------------|
| High | Strong evidence, multiple independent corroborating sources |
| Moderate | Some evidence, partially corroborated, reasonable inferences |
| Low | Limited evidence, single source, speculative |

---

## IOC Management & Standards

### Indicator Types & Lifespan

- **Atomic indicators:** IP, domain, hash, email — short shelf life (hours-days)
- **Computed indicators:** Hash sets, regular expressions — moderate shelf life (days-weeks)
- **Behavioral indicators:** TTPs, patterns — long shelf life (months-years)

### STIX 2.1 (OASIS Standard)

Structured Threat Information Expression — graph-based language for CTI:

**STIX Domain Objects (SDOs):** Attack Pattern, Campaign, Course of Action, Grouping, Identity, Indicator, Infrastructure, Intrusion Set, Location, Malware, Malware Analysis, Note, Observed Data, Opinion, Report, Threat Actor, Tool, Vulnerability

**STIX Relationship Objects (SROs):** Relationship, Sighting

**STIX Cyber-observable Objects (SCOs):** File, Process, Network Traffic, IPv4/IPv6 Address, Domain Name, URL, Email Message, Windows Registry Key, Mutex, X509 Certificate

Example STIX Indicator:
```json
{
  "type": "indicator",
  "spec_version": "2.1",
  "id": "indicator--12345678-9abc-def0-1234-56789abcdef0",
  "name": "Malicious IP",
  "pattern": "[ipv4-addr:value = '203.0.113.42']",
  "pattern_type": "stix",
  "valid_from": "2025-01-01T00:00:00Z"
}
```

### TAXII 2.1 (OASIS Standard)

Trusted Automated Exchange of Intelligence Information — RESTful protocol for STIX transport. Collections (feeds), Channels (streams), API Root discovery.

### MISP Format & Galaxy Clusters

MISP uses an event-attribute model with built-in correlation:
- **Events:** Structured containers for IOCs and contextual information
- **Attributes:** Individual indicators with types (ip-src, md5, url, domain, etc.)
- **Galaxies:** Knowledge base clusters (MITRE ATT&CK, Threat Actors, Ransomware, Tools)
- **Galaxy Clusters:** Specific items within galaxies (e.g., specific threat group)
- **Taxonomies:** Classification tags (TLP, PAP, admiralty-scale, estimative-language)
- **Objects:** Complex attribute combinations (file, email, network connection)

### TLP 2.0 (Traffic Light Protocol — FIRST)

| Marking | Sharing Boundary |
|---------|-----------------|
| **TLP:RED** | Recipients only — no further sharing |
| **TLP:AMBER** | Limited disclosure — recipient's organization only |
| **TLP:AMBER+STRICT** | Organization only — no sharing outside |
| **TLP:GREEN** | Limited disclosure — recipient's community |
| **TLP:CLEAR** | Public — no restrictions |

### YARA Rules

Pattern-matching for malware identification:
```yara
rule Suspicious_Mutex_Ransomware {
  meta:
    description = "Detect common ransomware mutex"
    author = "CTI Team"
    tlpmarking = "TLP:AMBER"
  strings:
    $m1 = "Global\\mssecure" ascii wide
  condition:
    $m1
}
```

### Sigma Rules

Generic SIEM detection rules — format-agnostic, convert to Splunk/KQL/Elastic:
```yaml
title: Suspicious LSASS Access
status: experimental
logsource:
  product: windows
  category: process_access
detection:
  selection:
    TargetImage|endswith: '\lsass.exe'
    GrantedAccess: '0x0010'
  filter:
    SourceImage|startswith:
      - 'C:\Windows\System32\'
      - 'C:\Program Files\'
  condition: selection and not filter
```

### Indicator Lifecycle

1. **Enrich:** Add context from VirusTotal, Shodan, Passive DNS
2. **Score:** Assign confidence (low/medium/high) and severity
3. **Contextualize:** Map to MITRE ATT&CK technique
4. **Distribute:** Push to SIEM, EDR, firewall via TAXII/API
5. **Expire:** Set TTL — remove or downgrade after shelf life
6. **Revoke:** Retire indicators with evidence of false positive

---

## Threat Hunting

### PEAK Framework (David Bianco / Splunk)

**P**repare — **E**xecute — **A**ct, with three hunt types:

| Type | Description | Best For |
|------|-------------|----------|
| **Hypothesis-Driven** | Form testable hypothesis from threat intelligence | Mature programs, strategic hunts |
| **Baseline Hunting** | Search for deviations from established norms | Novel threats, insider risks |
| **Model-Assisted Threat Hunting (M-ATH)** | Statistical/ML models surface anomalies | Large-scale, continuous hunting |

### ABLE Hypothesis Model

- **Actor:** Who is the threat actor or threat category?
- **Behavior:** What specific TTP are you hunting for?
- **Location:** Where in the environment would you find evidence?
- **Evidence:** What data source + query pattern confirms the behavior?

**Example hypothesis:**
"APT29 (Actor) may be using Valid Accounts via RDP (Behavior: T1078, T1021.001) against our domain controllers (Location: Windows Security Event 4624 with LogonType 10, source IP not in admin allowlist) (Evidence)."

### Hunting Maturity Model (HMM — Sqrrl)

| Level | Name | Description |
|-------|------|-------------|
| 0 | Initial | Relies entirely on automated alerts |
| 1 | Minimal | IOC-based searching from threat feeds |
| 2 | Procedural | Follows documented TTP-based hunt playbooks |
| 3 | Innovative | Creates novel hypotheses from intel + environment knowledge |
| 4 | Leading | Automated hypotheses + ML anomaly detection + continuous hunting |

### Three Hunt Approaches

**TTP-based hunting (highest value):**
- Hunt for technique behaviors, not specific IOCs
- TTPs are harder for adversaries to change than IPs or hashes
- Example: Kerberoasting (T1558.003) — hunt for RC4 TGS-REQ spikes
- Example: DCSync (T1003.006) — non-DC accounts requesting replication
- Example: LSASS access (T1003.001) — unexpected processes with PROCESS_VM_READ

**IOC-based hunting (lowest value, highest volume):**
- Sweep for known-bad indicators from threat intelligence
- Effective post-advisory, but short shelf life
- Automate with SIEM watchlists + EDR IOC ingestion

**Compliance-based hunting:**
- Search for policy violations, legacy protocols, misconfigurations
- Example: unconstrained delegation, weak cipher usage, over-permissioned service accounts

### Essential Hunting Data Sources

| Source | Key Telemetry | Retention |
|--------|--------------|-----------|
| EDR | Process creation (cmdline), network connections, file writes, registry | 90+ days |
| Windows Security Log | 4624/4625/4648/4662/4688/4698/4768/4769 | 90-365 days |
| Sysmon | Event ID 1 (process), 3 (network), 10 (process access), 11 (file create), 22 (DNS) | 90+ days |
| DNS Logs | Query patterns, DGA detection, beaconing | 90 days |
| PowerShell (4104) | Script block logging, module load events | 90+ days |
| Identity Provider | Okta/Azure AD auth logs, MFA failures, device registration | 90 days |
| Network Flow | NetFlow/IPFIX, connection duration, data volume, beaconing | 30-90 days |

### Query Examples by Platform

**Splunk (SPL):**
```spl
index=windows EventCode=4624 LogonType=10
| stats count by Account_Name, Workstation_Name, IpAddress
| where count > 5
```

**Elastic (EQL):**
```eql
sequence by process.pid
  [process where event.type == "start" and process.name == "rundll32.exe"]
  [network where event.type == "connection" and not destination.ip in (known_domains)]
```

**Microsoft Sentinel (KQL):**
```kusto
SecurityEvent
| where EventID == 4769 and AccountType == "User"
| summarize TGS_Count = count() by Account, ServiceName, TicketEncryptionType
| where TGS_Count > 10
```

### Hunt Execution Workflow

1. **Intake intelligence** — Recent threat reports, ISAC advisories, CISA alerts
2. **Form hypothesis** — Use ABLE model, map to ATT&CK technique
3. **Identify data source** — Which telemetry contains the signal?
4. **Write query** — SPL/KQL/EQL/VQL for hunting
5. **Execute & iterate** — Time-box (5-30 min) — refine hypothesis if no matches
6. **Document findings** — Positive findings = incident escalation; negative = data gaps or detection improvement
7. **Create detection** — Convert successful hunt into automated detection rule
8. **Archive** — Save query and findings in hunt library

### Tracking Hunt Program Effectiveness

| Metric | Definition | Target |
|--------|------------|--------|
| Hunt coverage rate | % of ATT&CK coverage gap hunted per quarter | >50% |
| Hypothesis-to-detection conversion | % of hunts producing new detection rules | >20% |
| Mean dwell time before hunt detection | Days adversary present before hunt discovers | Trending down |
| False negative audit rate | Known-bad test executions vs detection firing | <5% |

---

## Platforms & Tools

### TIP Comparison Matrix

| Platform | Type | Strengths | Weaknesses | Best For | Pricing |
|----------|------|-----------|------------|----------|---------|
| **MISP** | Open source | Largest sharing community, 250+ modules, automatic correlation, ISAC backbone | Dated UI, no built-in intelligence production, requires admin | IOC sharing, ISAC participation, community feeds | Free (self-hosted) |
| **OpenCTI** | Open source | Native STIX 2.1, graph knowledge base, 300+ connectors, MITRE ATT&CK native | Heavy deployment (RabbitMQ, ES, MinIO, Redis) | Internal knowledge management, analyst workflow | Free (self-hosted); SaaS ~$3k-15k/yr |
| **Recorded Future** | Commercial | 1M+ sources, AI enrichment, vulnerability prioritization, dark web coverage | Enterprise pricing ($50k-300k/yr) | Strategic intelligence, threat actor tracking, vulnerability intel | $50k-500k/yr |
| **ThreatConnect** | Commercial | Playbook automation (SOAR native), analyst workflow, TC Exchange | Complex implementation, high cost | Analyst workflow + orchestration | $50k-500k/yr |
| **Anomali ThreatStream** | Commercial | Feed aggregation, Splunk-native, 100+ connectors | UI dated, weaker graph visualization | large-scale IOC management | $30k-200k/yr |
| **Mandiant Advantage** | Commercial | IR pedigree, deep threat actor profiles, ATT&CK mapping | Enterprise pricing, Google Cloud ecosystem | Nation-state actor tracking, attribution | $30k-300k/yr |

### Mature Architecture Pattern

```
Raw Feeds (AlienVault OTX, Abuse.ch, CIRCL)
        |
        v
    MISP (Community sharing + automatic correlation)
        |
        v
  OpenCTI (Knowledge graph + ATT&CK mapping + analyst workflow)
        |
        v
  SIEM/SOAR/EDR (IOC distribution + detection)
```

### Detection Rule Formats

| Format | Tool | Purpose |
|--------|------|---------|
| YARA | YARA | File/memory pattern matching |
| Sigma | Sigma / pySigma | SIEM-agnostic detection rules |
| Snort/Suricata | Suricata, Snort | Network IDS signatures |
| KQL | Microsoft Sentinel | Azure-native detection queries |
| SPL | Splunk | Splunk detection queries |
| EQL | Elastic | Elastic detection queries |

### Key Open-Source Tools

| Tool | Purpose |
|------|---------|
| MISP | IOC sharing, community feeds, automatic correlation |
| OpenCTI | STIX 2.1 knowledge graph, ATT&CK mapping, analyst investigation |
| TheHive | Incident response case management + Cortex integration |
| Cortex | Observable analysis engine (VirusTotal, Shodan, etc.) |
| Yeti | Observable enrichment and threat intelligence |
| IntelMQ | Feed ingestion and correlation automation |
| YARA | Malware pattern matching |
| Sigma | Universal SIEM detection rules |
| Velociraptor | Host-level hunting and incident response |
| OSQuery | SQL-based OS instrumentation |

---

## Sharing & Communities

### ISACs (Information Sharing and Analysis Centers)

Sector-specific threat intelligence sharing:
- **FS-ISAC** — Financial services
- **H-ISAC** — Healthcare
- **E-ISAC** — Electricity/energy
- **MS-ISAC** — State/local/tribal/territorial government
- **Auto-ISAC** — Automotive
- **IT-ISAC** — Information technology

### CISA Automated Indicator Sharing (AIS)

Real-time machine-readable IOC exchange via STIX/TAXII:
- Bidirectional sharing — receive federal intelligence, submit own
- Default anonymization of submitter identity
- TLP marking required (default: TLP:GREEN)
- Legal protection under CISA 2015 (liability protection, privacy protections)
- Free participation — requires PKI certificate + TAXII 2.1 client

### NIST SP 800-150 (Guide to Cyber Threat Information Sharing)

Key recommendations:
- Establish information sharing rules (TLP, handling guidance)
- Define trust models for sharing partners
- Participate in ISACs, CERTs, government repositories
- Protect PII — strip personal information not directly related to threat
- Create sharing agreements before incidents occur

### Sharing Best Practices

- Apply consistent TLP markings to all shared intelligence
- Include confidence scores and estimative language
- Provide context (not just raw IOCs) — mapping to ATT&CK
- Strip PII not directly related to the threat
- Establish data handling agreements with sharing partners
- Use machine-readable formats (STIX 2.1, MISP) for automation

---

## Analyst Tradecraft & Reporting

### Finished Intelligence Product Types

| Type | Audience | Format | Length |
|------|----------|--------|--------|
| Intelligence Assessment | SOC, CTI team | Analytical report | 3-10 pages |
| Threat Actor Profile | CTI team, detection engineers | Entity report with TTP mapping | 5-20 pages |
| Campaign Report | CTI, IR, detection teams | Multi-intrusion analysis with timeline | 10-30 pages |
| Situational Awareness Brief | Executives, board | Dashboard, slide deck | 1-5 slides |
| Warning Notice | All stakeholders | Alert-level notification | 1 page |
| IOC Bulletin | SOC, detection engineers | Structured feed (STIX/MISP) | Machine-readable |

### Intelligence Assessment Template

```
TITLE: [Actor/Topic] — [Key Judgement]
TLP: [Marking] | DATE: [YYYY-MM-DD]

KEY JUDGEMENTS:
1. [Most important finding with confidence]
2. [Second key finding with confidence]
3. [Third key finding with confidence]

BACKGROUND:
[Context — what prompted this assessment]

ANALYSIS:
[Evidence, reasoning, application of analytic frameworks]

OUTLOOK:
[Expected developments, indicators of change]

IMPLICATIONS FOR [ORGANIZATION]:
[Relevance to specific environment/sector]

RECOMMENDATIONS:
[Actionable items for stakeholders]

SOURCES & METHODOLOGY:
[Key sources, confidence levels, analytic techniques used]
```

### Common Cognitive Biases in CTI

| Bias | Description | Mitigation |
|------|-------------|------------|
| Confirmation bias | Seeking evidence that confirms existing beliefs | ACH, Devil's Advocacy |
| Anchoring | Over-relying on first information received | Consider multiple baselines, initial assumptions check |
| Availability bias | Judging likelihood by ease of recall | Systematic data collection, avoid recency effects |
| Groupthink | Consensus-seeking suppresses alternatives | Red team analysis, structured debate |
| Mirror imaging | Assuming adversaries think like us | Adversary-specific cultural/operational analysis |

### Intelligence Writing Principles

1. **Bottom line up front (BLUF)** — Key judgement in first paragraph
2. **Explicit confidence** — Use estimative language consistently
3. **Source attribution** — Distinguish raw intelligence from analyst judgment
4. **Multiple hypotheses** — Don't argue for a single explanation without alternatives
5. **Separate facts from analysis** — Make the distinction clear
6. **Actionable recommendations** — Tie intelligence to decisions
7. **Timeliness over perfection** — 80% confidence now beats 95% too late

### RFI (Request for Information) Management

1. **Triage** — Categorize by urgency and complexity
2. **Scope** — Define the intelligence question precisely
3. **Research** — Leverage TIP, open source, internal telemetry
4. **Draft** — Produce response with confidence and sourcing
5. **Review** — Peer review for bias and quality
6. **Deliver** — Provide in stakeholder-appropriate format
7. **Feedback** — Was the intelligence used? Was it useful?

---

## References

### Official Standards & Frameworks
1. MITRE ATT&CK Enterprise Matrix — https://attack.mitre.org/
2. STIX 2.1 Specification (OASIS) — https://docs.oasis-open.org/cti/stix/v2.1/stix-v2.1.html
3. TAXII 2.1 Specification (OASIS) — https://docs.oasis-open.org/cti/taxii/v2.1/taxii-v2.1.html
4. OASIS STIX Walkthrough Tutorial — https://oasis-open.github.io/cti-documentation/stix/walkthrough.html
5. FIRST TLP 2.0 Standard — https://www.first.org/tlp/docs/tlp-letter.pdf
6. CISA TLP 2.0 User Guide — https://www.cisa.gov/sites/default/files/2023-02/tlp-2-0-user-guide_508c.pdf
7. CISA Automated Indicator Sharing (AIS) — https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing/automated-indicator-sharing-ais
8. CISA AIS 2.0 Submission Guide v1.0 — https://www.cisa.gov/sites/default/files/2023-02/ais_2.0_submission_guide_v1.0_508.pdf
9. CISA AIS Sharing Guidance (2026 Update) — https://www.cisa.gov/sites/default/files/2026-02/NonFederal-Entity-Sharing-Guidance-Nov-2025-Updates-%2B-Feb-2026-Updates.pdf
10. NIST SP 800-150 (Cyber Threat Information Sharing) — https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-150.pdf
11. CISA Cybersecurity Information Sharing Act (CISA 2015) — https://www.cisa.gov/topics/cyber-threats-and-advisories/information-sharing
12. FIRST SIGMA Standard Repository — https://github.com/SigmaHQ/sigma
13. YARA Documentation — https://yara.readthedocs.io/

### Seminal Research Papers
14. Hutchins, E.M., Cloppert, M.J., Amin, R.M., "Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains" (Lockheed Martin, 2011)
15. Caltagirone, S., Pendergast, A., Betz, C., "The Diamond Model of Intrusion Analysis" (CTA, 2013)
16. Strom, B.E. et al., "MITRE ATT&CK: Design and Philosophy" (MITRE, 2018)
17. Heuer, R.J., "Psychology of Intelligence Analysis" (CIA Center for the Study of Intelligence, 1999)
18. Heuer, R.J., Pherson, R.H., "Structured Analytic Techniques for Intelligence Analysis" (CQ Press, 2014)
19. Bianco, D., "The PEAK Threat Hunting Framework" (Splunk, 2023) — https://www.splunk.com/en_us/blog/security/peak-hypothesis-driven-threat-hunting.html
20. Sqrrl, "Threat Hunting Maturity Model" (2015) — https://www.sqrrl.com/hunting-maturity-model
21. Mandiant, "M-Trends 2024/2025" annual report series — https://www.mandiant.com/m-trends
22. Verizon, "Data Breach Investigations Report" (DBIR) annual series — https://www.verizon.com/dbir/

### Platforms & Tools Documentation
23. MISP Project — https://www.misp-project.org/
24. MISP Best Practices — https://www.misp-project.org/best-practices-in-threat-intelligence.html
25. MISP-STIX Release (2026.3.13) — https://www.misp-project.org/2026/03/13/misp-stix_indicator_and_observable_fingerprinting.html/
26. OpenCTI Platform (Filigran) — https://filigran.io/platform/opencti/
27. OpenCTI DeepWiki — Data Import Pipeline — https://deepwiki.com/OpenCTI-Platform/opencti/8.3-data-import-pipeline
28. OpenCTI Connector Library — https://github.com/OpenCTI-Platform/connectors
29. TheHive Project — https://thehive-project.org/
30. Cortex (Observable Analysis) — https://thehive-project.org/
31. Yeti (Yeti Threat Intelligence) — https://github.com/yeti-platform/yeti
32. IntelMQ — https://github.com/IntelMQ/intelmq
33. Velociraptor Documentation — https://docs.velociraptor.app/
34. OSQuery Documentation — https://osquery.readthedocs.io/

### Books
35. Roberts, S.J., Brown, R., "Intelligence-Driven Incident Response" 2nd Ed. (O'Reilly, 2023) — https://www.oreilly.com/library/view/intelligence-driven-incident-response/9781098120672/
36. Costa-Gazcón, V., "Practical Threat Intelligence and Data-Driven Threat Hunting" 2nd Ed. (Packt, 2024) — https://www.oreilly.com/library/view/practical-threat-intelligence/9781803233758/
37. Lee, M., "Cyber Threat Intelligence" (Wiley, 2023) — https://www.wiley.com/en-us/Cyber+Threat+Intelligence-p-9781119861775
38. Recorded Future, "The Intelligence Handbook" 4th Ed. (CyberEdge, 2023) — https://sprotyvg7.com.ua/wp-content/uploads/2023/08/intelligence-handbook-fourth-edition.pdf
39. Martinez, R., "Incident Response with Threat Intelligence" (Packt, 2022) — https://www.packtpub.com/en-us/product/incident-response-with-threat-intelligence-9781801070997
40. Arici, H.Y., "Cyber Threat Intelligence: The Comprehensive Guide" (SAP PRESS, 2026) — https://www.sap-press.com/cyber-threat-intelligence_6261/
41. Dalwigk, F., "Cyber Threat Intelligence" (SAP PRESS, 2026)
42. Stoll, C., "The Cuckoo's Egg: Tracking a Spy Through the Maze of Computer Espionage" (Doubleday, 1989)

### Certifications & Training
43. SANS FOR578: Cyber Threat Intelligence (GIAC GCTI) — https://www.sans.org/cyber-security-courses/cyber-threat-intelligence/
44. SANS FOR478: CTI Foundations — https://www.sans.org/cyber-security-courses/cyber-threat-intelligence-foundations-training/
45. GIAC GCTI Certification — https://www.giac.org/certifications/cyber-threat-intelligence-gcti/
46. EC-Council CTIA — https://www.eccouncil.org/train-certify/certified-threat-intelligence-analyst-ctia/
47. Recorded Future University — https://university.recordedfuture.com/
48. CTI-CRAFT (CBEST/TIBER-EU/DORA TLPT) — https://academy.threatinsights.net/
49. IronCircle Certified CTI Analyst — https://www.ironcircle.com/cybersecurity-training/cyber-defense/certified-cti-analyst/
50. Pluralsight CTI Learning Path — https://www.pluralsight.com/paths/cyber-threat-intel-cti

### Reading Lists & Study Plans
51. Roberts, S.J., "CTI Reading List" — https://sroberts.io/posts/cti-reading-list/
52. Nickels, K., "A Top 10 Reading List for Getting Started in CTI" (Medium, 2019)
53. Nickels, K., "CTI Self-Study Plan Part 1 & Part 2" — https://medium.com/katies-five-cents
54. Curated-Intel, "CTI Fundamentals Repository" — https://github.com/curated-intel/CTI-fundamentals
55. MyHackingCat, "CTI Study Plan for Beginners" (2025) — https://myhackingcat.com/cyber-threat-intelligence-study-plan-for-beginners-2025/

### Academic Papers
56. Knowles, W. et al., "Standardised Penetration Testing? Examining Usefulness of Current PT Methodologies" (ResearchGate, 2019)
57. Imtias, M.B. et al., "Comparative Analysis: OWASP, PTES, NIST SP 800-115" (JAIC, 2025) — https://jurnal.polibatam.ac.id/index.php/JAIC/article/view/9846
58. Naik, N. et al., "Comparative Analysis of Threat Modelling Methods" (Springer, 2024)
59. ESSecA: Automated Penetration Testing (ACM, 2024) — https://dl.acm.org/doi/fullHtml/10.1145/3664476.3670459
60. Mandiant, "CTI Analyst Core Competencies Framework" — https://www.mandiant.com/

### Threat Hunting
61. Splunk PEAK Framework — https://www.splunk.com/en_us/blog/security/peak-hypothesis-driven-threat-hunting.html
62. Cisco Talos Threat Hunting — https://blog.talosintelligence.com/hypotheses-telemetry-and-human-judgment-inside-cisco-talos-threat-hunting/
63. Vectra AI Threat Hunting Guide — https://www.vectra.ai/resources/threat-hunting-guide
64. Dropzone AI, "Complete Guide to Proactive Threat Hunting" (2026) — https://www.dropzone.ai/blog/the-complete-guide-to-proactive-threat-hunting
65. Fortress MSSP, "Threat Hunting Methodology Guide" — https://fortressmssp.com/blog/threat-hunting-methodology-guide
66. Underdefense, "15 Best Threat Hunting Tools 2026" — https://underdefense.com/blog/best-threat-hunting-tools/
67. Decryption Digest, "How to Build a Threat Hunting Program" (2026) — https://www.decryptiondigest.com/blog/how-to-build-threat-hunting-program

### CTI Platforms (Comparisons & Reviews)
68. Decryption Digest, "MISP vs OpenCTI" (2026) — https://www.decryptiondigest.com/blog/misp-vs-opencti-threat-intelligence-platform
69. Decryption Digest, "TIP Comparison" (2026) — https://www.decryptiondigest.com/blog/threat-intelligence-platforms-comparison
70. Decryption Digest, "Best TIPs 2026" — https://www.decryptiondigest.com/blog/guide-finding-best-threat-intelligence-platforms
71. OSINTBench, "Best Threat Intelligence Platforms 2026" — https://osintbench.com/comparisons/best-threat-intelligence-platforms
72. Cyber Secify, "Top TIPs Buyer Guide 2026" — https://cybersecify.com/blog/top-threat-intelligence-platforms-2026/
73. Subrupt, "Best TIPs 2026" — https://subrupt.com/best/threat-intelligence
74. Liberty91, "How to Evaluate a TIP" (2026) — https://liberty91.com/blog/cti-trenches-tools-and-platforms
75. GitHub: evaluating-threat-intelligence-platforms skill — https://github.com/mukul975/anthropic-cybersecurity-skills/blob/main/skills/evaluating-threat-intelligence-platforms/SKILL.md

### Information Sharing & Communities
76. FIRST — Forum of Incident Response and Security Teams — https://www.first.org/
77. FS-ISAC — Financial Services ISAC — https://www.fsisac.com/
78. H-ISAC — Health ISAC — https://h-isac.org/
79. MS-ISAC — Multi-State ISAC — https://www.cisecurity.org/ms-isac/
80. E-ISAC — Electricity ISAC — https://www.eisac.com/
81. AlienVault OTX — https://otx.alienvault.com/
82. Abuse.ch (URLhaus, MalwareBazaar, ThreatFox) — https://abuse.ch/
83. CIRCL OSINT Feeds — https://www.circl.lu/
84. VirusTotal — https://www.virustotal.com/
85. GreyNoise — https://www.greynoise.io/
86. Pulsedive — https://pulsedive.com/
87. SAMA CTI Rulebook — https://www.rulebook.sama.gov.sa/en/entiresection/3092

### CTI News & Analysis
88. Mandiant Advantage (Threat Intelligence) — https://www.mandiant.com/advantage/threat-intelligence
89. Recorded Future Insikt Group — https://www.recordedfuture.com/research
90. Cisco Talos Intelligence — https://talosintelligence.com/
91. Dragos ICS/OT Threat Intelligence — https://www.dragos.com/threat-intelligence/
92. Intel 471 — https://intel471.com/
93. Flashpoint — https://www.flashpoint-intel.com/
94. ZeroFox — https://www.zerofox.com/

### Government & Regulatory
95. UK National Cyber Security Centre (NCSC) — https://www.ncsc.gov.uk/
96. Australian Cyber Security Centre (ACSC) — https://www.cyber.gov.au/
97. European Union Agency for Cybersecurity (ENISA) — https://www.enisa.europa.eu/
98. NIST National Vulnerability Database — https://nvd.nist.gov/
99. CISA Known Exploited Vulnerabilities (KEV) — https://www.cisa.gov/known-exploited-vulnerabilities-catalog
100. UK National Occupational Standards — CTI — https://www.ukstandards.org.uk/en/nos-finder/TECIS609401/carry-out-threat-intelligence-assessments

### Key Industry Reports
101. CrowdStrike, "Global Threat Report" (annual) — https://www.crowdstrike.com/global-threat-report/
102. Mandiant, "M-Trends" (annual) — https://www.mandiant.com/m-trends
103. IBM Security, "Cost of a Data Breach Report" (annual) — https://www.ibm.com/reports/data-breach
104. Verizon, "Data Breach Investigations Report" (annual) — https://www.verizon.com/dbir/
105. SANS, "Threat Hunting Survey" (annual) — https://www.sans.org/white-papers/

### Tools & Integration
106. Splunk SPL Search Reference — https://docs.splunk.com/Documentation/Splunk/latest/SearchReference/
107. Microsoft KQL Reference — https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/
108. Elastic EQL Guide — https://www.elastic.co/guide/en/elasticsearch/reference/current/eql.html
109. PyMISP Library — https://github.com/MISP/PyMISP
110. OpenCTI Python Client — https://github.com/OpenCTI-Platform/client-python
111. SigmaHQ pySigma — https://github.com/SigmaHQ/pySigma
112. YARA Documentation — https://yara.readthedocs.io/en/stable/
113. Suricata IDS Rules — https://suricata.io/features/rule-management/
114. Velociraptor VQL Reference — https://docs.velociraptor.app/docs/vql/
115. ATT&CK Navigator — https://mitre-attack.github.io/attack-navigator/
116. MITRE CALDERA — https://caldera.mitre.org/
