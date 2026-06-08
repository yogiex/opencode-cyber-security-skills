---
name: "Platforms & Tools — TIP Comparison, OpenCTI, MISP"
description: "Threat intelligence platform (TIP) comparison matrix (MISP, OpenCTI, Recorded Future, ThreatConnect, Anomali, Mandiant), mature architecture pattern (MISP → OpenCTI → SIEM), detection rule formats (YARA, Sigma, Snort, KQL, SPL, EQL), and key open-source CTI tools."
tags: [cti, platforms, tools, tip, misp, opencti, recorded-future, detection-rules]
---

# Platforms & Tools

## TIP Comparison Matrix

| Platform | Type | Strengths | Best For |
|----------|------|-----------|----------|
| **MISP** | Open source | Largest sharing community, 250+ modules, auto correlation | IOC sharing, ISAC participation |
| **OpenCTI** | Open source | Native STIX 2.1, graph knowledge base, 300+ connectors | Internal knowledge management |
| **Recorded Future** | Commercial | 1M+ sources, AI enrichment, dark web | Strategic intel, threat actor tracking |
| **ThreatConnect** | Commercial | Playbook automation, analyst workflow | Analyst workflow + orchestration |
| **Anomali** | Commercial | Feed aggregation, Splunk-native | Large-scale IOC management |
| **Mandiant Advantage** | Commercial | IR pedigree, deep actor profiles | Nation-state actor tracking |

## Mature Architecture Pattern

```
Raw Feeds → MISP → OpenCTI → SIEM/SOAR/EDR
```

## Detection Rule Formats

| Format | Tool | Purpose |
|--------|------|---------|
| YARA | YARA | File/memory pattern matching |
| Sigma | pySigma | SIEM-agnostic detection rules |
| Snort/Suricata | Suricata | Network IDS signatures |
| KQL | Sentinel | Azure-native detection |
| SPL | Splunk | Splunk detection |
| EQL | Elastic | Elastic detection |

## Key Open-Source Tools

MISP, OpenCTI, TheHive, Cortex, Yeti, IntelMQ, YARA, Sigma, Velociraptor, OSQuery.

## Best Practices

- MISP + OpenCTI is the most common open-source stack
- Use detection-as-code workflows (Sigma → pySigma → SIEM)
- Automate feed ingestion with IntelMQ
- Integrate TIP with SOAR for automated response
