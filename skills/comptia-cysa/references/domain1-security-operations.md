---
name: "Domain 1 — Security Operations (34%)"
description: "CompTIA CySA+ Domain 1 covering logging concepts, system/network architecture, indicators of malicious activity (network, host, application, cloud, identity, email), LOLBins, threat intelligence, threat hunting, process improvement (SOAR, IaC), and AI in security operations."
tags: [comptia, cysa, security-operations, logging, threat-intelligence, hunting, soar]
---

# Domain 1: Security Operations (34%)

## Logging Concepts

- Centralized logging via SIEM (Syslog RFC 5424, Windows Event Log, JSON/CEF)
- Time synchronization via NTP — UTC standard, drift >1s harus diperbaiki
- Logging levels: ERROR, WARNING, INFO, DEBUG

## Indicators of Malicious Activity

**Network:** Bandwidth spikes, beaconing, irregular peer-to-peer, rogue devices, port scans, unusual traffic on non-standard ports.
**Host:** CPU/memory spikes, unauthorized software/processes, registry changes, data exfiltration staging.
**Application:** Anomalous input, unexpected accounts, unusual outbound comms, service interruption.
**Cloud:** Anomalous resource creation, IAM compromise, storage exfiltration.
**Identity:** Impossible travel, account compromise, unusual login patterns.
**Email:** BEC, DMARC/DKIM/SPF, obfuscated links, malicious attachments.
**LOLBins:** powershell.exe, mshta.exe, rundll32.exe, certutil.exe, bitsadmin.exe — deteksi via parent-child relationship.

## Threat Intelligence

Threat actors: APT, Hacktivist, Organized Crime, Nation-State, Insider, Supply Chain.
Pyramid of Pain: Hash → IP → Domain → Host Artifact → Network Artifact → TTPs.
Confidence levels: Timeliness, Relevance, Accuracy.
Sources: OSINT, closed-source (paid feeds), internal.

## Threat Hunting

Hypothesis-driven, baseline-driven. Cyber deception: honeypot, honeytoken.

## Process Improvement

SOAR, IaC, data enrichment, rule/alert tuning, dashboard creation. Single pane of glass.

## AI in Security Operations

Risks: hallucinations, data exposure, model poisoning, malicious prompts.
Governance: legal compliance, AI usage policies.
Use cases: artifact comparison, log analysis, document creation, incident investigation.

## Best Practices

- Standardize processes with playbooks/runbooks
- Automate response with SOAR
- Integrate tools via APIs and webhooks
- Continuously tune detection rules based on false positive rate
