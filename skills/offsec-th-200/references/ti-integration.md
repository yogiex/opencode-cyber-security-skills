---
name: "Threat Intelligence Integration"
description: "Intelligence lifecycle, IOC types, Splunk IOC integration, STIX/TAXII, MISP platform, and threat intel-driven hunting methodologies."
tags: [threat-intelligence, ioc, stix, taxii, misp, ti-integration, intel-driven-hunting]
---

# Threat Intelligence Integration

## Intelligence Lifecycle

```
1. Requirements → 2. Collection → 3. Processing → 
4. Analysis → 5. Dissemination → 6. Feedback
```

## IOC Types

| Type | Example | Hunting Method |
|------|---------|---------------|
| **Hash (SHA256/MD5)** | a1b2c3... | Hash lookup across endpoints |
| **IP Address** | 185.234.72.1 | Network connection logs |
| **Domain** | evil-malware.xyz | DNS logs, proxy logs |
| **URL** | http://evil.com/payload.exe | Proxy logs, web logs |
| **Registry key** | HKLM\...\Run\Malware | Registry auditing |
| **File path** | C:\Users\*\AppData\... | File creation monitoring |
| **Named pipe** | \\.\pipe\srvsvc | Named pipe events (Sysmon 17) |
| **YARA rule** | rule SuspiciousPS {...} | YARA scan on endpoints |

## Integrating Threat Intel into Splunk

**Using inputlookup for IOC Matching:**
```spl
| inputlookup threat_intel_iocs.csv
| search ioc_type="ip"
| rename ioc as dest_ip
| append [search index=* earliest=-7d]
| stats values(ioc_type) as matching_types by dest_ip, src_ip
| where isnotnull(matching_types)
```

**DNS IOC Matching:**
```spl
| inputlookup threat_intel_domains.csv
| search sourcetype=dns
| rename query as ioc
| stats count by query, src_ip
```

**Hash IOC Matching:**
```spl
| inputlookup threat_intel_hashes.csv
| search sourcetype=sysmon EventCode=1
| eval file_hash = sha256(Image)
| where file_hash IN [| inputlookup threat_intel_hashes.csv | fields ioc]
```

## STIX/TAXII Overview

- **STIX** (Structured Threat Information Expression): Standard format for CTI data
- **TAXII** (Trusted Automated eXchange of Indicator Information): Transport protocol

**STIX 2.1 Objects:** indicator, campaign, threat-actor, attack-pattern, malware, report

## MISP (Malware Information Sharing Platform)

**Key MISP Features for Hunting:** Feed management (public + private intel feeds), event correlation, export (STIX, CSV, JSON, OpenIOC), Galaxies (MITRE ATT&CK mapping, threat actor groups).

**MISP to Splunk Integration:** `MISP Feed → Splunk TA for MISP → inputlookup → SPL correlation`

## Intel Report Types

| Type | Audience | Content |
|------|----------|---------|
| **Strategic** | Executive | Risk-focused, big picture |
| **Operational** | Tactical planners | Campaign-focused |
| **Tactical** | Analysts | IoCs, TTPs, technical indicators |
| **Technical** | Engineers | Raw data, hashes, IPs, domains |

## Gotchas

- Threat intel report di exam adalah sumber utama — baca dengan teliti sebelum memulai hunting
- Tidak semua IoCs akan match — wajar. Fokus pada IoCs yang match untuk membangun timeline
- STIX/TAXII tidak akan diminta secara langsung di exam — cukup pahami konsepnya
- MISP query tidak tersedia di exam — fokus pada cara mengintegrasikan intel ke Splunk via inputlookup
- TLP marking penting untuk report — pastikan menggunakan TLP yang benar di laporan

## Best Practices

- Buat IOC checklist dari threat report sebelum memulai query
- Prioritaskan IoCs berdasarkan type: IP/domain (real-time) > hash (post-execution)
- Dokumentasikan setiap IoC match dengan timestamp dan source
- Gunakan threat intel untuk hypothesis-driven hunting (bukan cuma IOC matching)
- Update IOC list secara real-time selama hunting — temuan baru = IoCs baru
