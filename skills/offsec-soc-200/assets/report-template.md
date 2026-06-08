---
name: "OSDA Report Template"
description: "Structured report template for OSDA exam submission."
tags: [osda, exam, report, template]
---

# OSDA Report Template

Gunakan struktur ini untuk report exam:

```
1. Executive Summary (1 page)
   - High-level attack narrative (10-15 bullet points)
   - Key findings summary
   - Overall risk assessment

2. Per-Phase Analysis
   Phase 1: [Title]
   - Time window
   - Initial access vector
   - Attacker IP / Victim host
   - MITRE ATT&CK mapping
   - KQL queries used
   - Screenshots (query + result)
   - Detailed analysis of each attacker action
   - Indicators of Compromise (IOCs)

3. Indicators of Compromise (Consolidated)
   - IP addresses
   - Process names and PIDs
   - File hashes
   - Registry keys
   - Service names

4. Detection Rules
   - KQL queries created during analysis
   - Sigma rules (if applicable)

5. Appendices
   - Full query list
   - Timeline of events
   - Host-to-IP mapping
   - OSQuery results
```
