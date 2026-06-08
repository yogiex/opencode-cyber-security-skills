---
name: "IOC Management — STIX, TAXII, MISP, YARA & Sigma"
description: "Indicator of compromise (IOC) management covering indicator types and lifespan, STIX 2.1 domain and relationship objects, TAXII 2.1 transport protocol, MISP event-attribute model and galaxy clusters, TLP 2.0 markings, YARA rule writing, Sigma SIEM rule format, and indicator lifecycle management."
tags: [cti, ioc, stix, taxii, misp, yara, sigma, tlp]
---

# IOC Management & Standards

## Indicator Types & Lifespan

- **Atomic**: IP, domain, hash, email — hours-days
- **Computed**: Hash sets, regex — days-weeks
- **Behavioral**: TTPs, patterns — months-years

## STIX 2.1 (OASIS Standard)

Graph-based language for CTI. Domain Objects (SDOs): Attack Pattern, Campaign, Indicator, Malware, Threat Actor, Tool, Vulnerability, etc. Relationship Objects (SROs): Relationship, Sighting. Cyber-observable Objects (SCOs): File, Process, Network Traffic, IPv4/IPv6, Domain, URL, etc.

## TAXII 2.1

RESTful protocol for STIX transport. Collections (feeds), Channels (streams), API Root discovery.

## MISP Format

Event-attribute model with built-in correlation:
- **Events**: Structured containers for IOCs
- **Attributes**: Individual indicators (ip-src, md5, url, domain)
- **Galaxies**: Knowledge base clusters (ATT&CK, Threat Actors, Ransomware)
- **Taxonomies**: TLP, PAP, estimative-language tags

## TLP 2.0

| Marking | Sharing Boundary |
|---------|-----------------|
| TLP:RED | Recipients only |
| TLP:AMBER | Recipient's organization |
| TLP:AMBER+STRICT | Organization only |
| TLP:GREEN | Recipient's community |
| TLP:CLEAR | Public |

## YARA Rules

Pattern-matching for malware identification. Rule structure: meta, strings, condition.

## Sigma Rules

Generic SIEM detection rules — format-agnostic, convert to Splunk/KQL/Elastic.

## Indicator Lifecycle

Enrich → Score → Contextualize → Distribute → Expire → Revoke

## Best Practices

- Apply consistent TLP markings to all shared intelligence
- Include confidence scores and ATT&CK mapping
- Use machine-readable formats (STIX 2.1, MISP) for automation
- Set TTL on indicators — remove or downgrade after shelf life
