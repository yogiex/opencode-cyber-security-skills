---
name: threat-intelligence
description: Cyber Threat Intelligence (CTI) — lifecycle, intelligence frameworks, IOC management, threat hunting, analyst tradecraft. Use when gathering threat intelligence, performing threat hunting, managing IOCs, conducting intelligence-driven analysis, or when user asks about CTI lifecycle, TIP platforms, STIX/TAXII, MISP, OpenCTI, or structured analytical techniques.
license: MIT
metadata:
  source: CTI (community)
  version: "1.0"
---

# Threat Intelligence — CTI Lifecycle, IOC Management & Threat Hunting

## Prerequisites

- Understanding of cybersecurity fundamentals (attacks, defenses, adversaries)
- Familiarity with SIEM concepts and security operations
- Basic knowledge of malware, TTPs, and Indicators of Compromise
- No prior CTI experience required — this skill covers fundamentals to advanced

## When to Use This Skill

Invoke this skill when:
- User asks about cyber threat intelligence lifecycle, frameworks, or analyst tradecraft
- User mentions STIX, TAXII, MISP, OpenCTI, or threat intelligence platforms
- User asks about indicators of compromise (IOCs), YARA, Sigma, or TLP
- User needs guidance on threat hunting, hypothesis-driven analysis, or proactive detection

## Key Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| **CTI Fundamentals** | Intelligence levels, 6-phase cycle, PIRs, CMF | [cti-fundamentals.md](./references/cti-fundamentals.md) |
| **Analytic Frameworks** | Kill Chain, ATT&CK, Diamond Model, SATs | [analytic-frameworks.md](./references/analytic-frameworks.md) |
| **IOC Management** | STIX 2.1, TAXII, MISP, TLP, YARA, Sigma | [ioc-management.md](./references/ioc-management.md) |
| **Threat Hunting** | PEAK, ABLE, HMM, data sources, query examples | [threat-hunting.md](./references/threat-hunting.md) |
| **Platforms & Tools** | TIP comparison, OpenCTI, MISP, detection rules | [platforms-tools.md](./references/platforms-tools.md) |
| **Sharing & Communities** | ISACs, CISA AIS, NIST 800-150, best practices | [sharing-communities.md](./references/sharing-communities.md) |
| **Tradecraft & Reporting** | Intel products, assessment template, biases, writing | [tradecraft-reporting.md](./references/tradecraft-reporting.md) |

## Reference Documentation

| File | Description |
|------|-------------|
| [cti-fundamentals.md](./references/cti-fundamentals.md) | Intelligence levels, 6-phase cycle, PIRs |
| [analytic-frameworks.md](./references/analytic-frameworks.md) | Kill Chain, ATT&CK, Diamond Model, SATs |
| [ioc-management.md](./references/ioc-management.md) | STIX, TAXII, MISP, TLP, YARA, Sigma |
| [threat-hunting.md](./references/threat-hunting.md) | PEAK, ABLE, HMM, queries |
| [platforms-tools.md](./references/platforms-tools.md) | TIP comparison, open-source tools |
| [sharing-communities.md](./references/sharing-communities.md) | ISACs, CISA AIS, NIST 800-150 |
| [tradecraft-reporting.md](./references/tradecraft-reporting.md) | Intel products, biases, writing principles |
| [referensi.md](./references/referensi.md) | 116 external CTI resources |

## Gotchas

1. **PIRs before collection**: Jangan mulai mengumpulkan intelligence sebelum mendefinisikan PIRs. Intelligence tanpa arah = noise. Setiap koleksi harus bisa dijawab: "PIR mana yang ini dukung?"
2. **TLP bukan security classification**: TLP adalah sharing boundary, bukan classification tingkat kerahasiaan. TLP:AMBER ≠ "rahasia" — artinya boleh dishare dalam organisasi. Jangan gunakan TLP sebagai pengganti classification system.
3. **YARA ≠ Sigma ≠ STIX**: Ketiganya untuk tujuan berbeda. YARA untuk file/memory pattern matching. Sigma untuk SIEM detection rules. STIX untuk representasi intelligence. Jangan gunakan YARA untuk mendeteksi network traffic (gunakan Snort/Suricata).
4. **IOC-based hunting is lowest value**: TTP-based hunting memberikan deteksi yang lebih tahan lama. IP dan hash berubah dalam jam/hari, tapi teknik (misal: Kerberoasting) tetap relevan selama bertahun-tahun.
5. **Intelligence tanpa feedback siklus tidak lengkap**: Phase 6 (Feedback) paling sering dilewati. Tanpa feedback, Anda tidak tahu apakah intelligence Anda berguna. Selalu close the loop.
6. **Tool/platform bukan solusi**: MISP atau OpenCTI tanpa analyst yang terlatih hanya database kosong. Tools enable analysts — they don't replace them.

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Intelligence levels and lifecycle fundamentals | [cti-fundamentals.md](./references/cti-fundamentals.md) |
| Analytic frameworks (Kill Chain, ATT&CK, Diamond) | [analytic-frameworks.md](./references/analytic-frameworks.md) |
| IOC formats (STIX, MISP, YARA, Sigma) | [ioc-management.md](./references/ioc-management.md) |
| Threat hunting methodology and queries | [threat-hunting.md](./references/threat-hunting.md) |
| TIP comparison and tool selection | [platforms-tools.md](./references/platforms-tools.md) |
| Intelligence sharing and ISACs | [sharing-communities.md](./references/sharing-communities.md) |
| Intel writing, biases, and RFI management | [tradecraft-reporting.md](./references/tradecraft-reporting.md) |
| External CTI resources | [referensi.md](./references/referensi.md) |

## License

MIT
