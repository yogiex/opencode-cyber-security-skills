---
name: comptia-cysa
description: Panduan lengkap CompTIA CySA+ (CS0-004 V4) mencakup Security Operations, Vulnerability Management, Incident Response, dan Reporting & Communication untuk mempersiapkan sertifikasi Cybersecurity Analyst.
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, soc analyst, vulnerability analyst, cysa+ candidate
  standard: CompTIA CySA+ CS0-004
  year: "2026"
---

# CompTIA CySA+ (CS0-004 V4) — Panduan Lengkap

Empat domain: Security Operations (34%), Vulnerability Management (26%), Incident Response and Management (24%), dan Reporting & Communication (16%). Ujian 165 menit, 85 soal, passing 750/900.

## When to Use This Skill

Invoke this skill when:
- User asks about CompTIA CySA+ exam preparation or any domain (Security Ops, Vuln Mgmt, IR, Reporting)
- User needs references for SIEM, threat hunting, vulnerability scanning, or incident response processes
- User asks about CVSS, EPSS, risk scoring, or vulnerability prioritization

## Key Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| **Exam Overview** | Exam structure, domain weights, prep strategies | [exam-overview.md](./references/exam-overview.md) |
| **Security Operations** | Logging, indicators, threat intel, hunting, SOAR, AI | [domain1-security-operations.md](./references/domain1-security-operations.md) |
| **Vulnerability Management** | Scanning, assessment tools, prioritization, CVSS, EPSS | [domain2-vulnerability-management.md](./references/domain2-vulnerability-management.md) |
| **Incident Response** | IR lifecycle, Kill Chain, Diamond Model, evidence, containment | [domain3-incident-response.md](./references/domain3-incident-response.md) |
| **Reporting & Communication** | Reports, stakeholder comms, MTTD/MTTR/MTTC | [domain4-reporting.md](./references/domain4-reporting.md) |
| **Tools & Frameworks** | 15 tool categories, 12 frameworks mapped to domains | [tools-frameworks.md](./references/tools-frameworks.md) |

## Reference Documentation

| File | Description |
|------|-------------|
| [exam-overview.md](./references/exam-overview.md) | Exam structure, domain weights, PBQ & MCQ strategies |
| [domain1-security-operations.md](./references/domain1-security-operations.md) | Logging, indicators, threat intel, hunting, process improvement, AI |
| [domain2-vulnerability-management.md](./references/domain2-vulnerability-management.md) | Scanning methods, tools, prioritization, CVSS+EPSS, risk |
| [domain3-incident-response.md](./references/domain3-incident-response.md) | Kill Chain, Diamond Model, 7-phase IR, evidence, containment |
| [domain4-reporting.md](./references/domain4-reporting.md) | Vuln mgmt reporting, IR reporting, stakeholder comms, KPIs |
| [tools-frameworks.md](./references/tools-frameworks.md) | 15 tool categories, 12 frameworks (MITRE, NIST, ISO, CIS) |

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Exam overview and prep strategies | [exam-overview.md](./references/exam-overview.md) |
| Security operations deep-dive | [domain1-security-operations.md](./references/domain1-security-operations.md) |
| Vulnerability management and scanning | [domain2-vulnerability-management.md](./references/domain2-vulnerability-management.md) |
| Incident response process and forensics | [domain3-incident-response.md](./references/domain3-incident-response.md) |
| Reporting templates and KPIs | [domain4-reporting.md](./references/domain4-reporting.md) |
| Tool comparison and framework mappings | [tools-frameworks.md](./references/tools-frameworks.md) |

## Gotchas

1. **CVSS saja tidak cukup**: CVSS mengukur severity teknis, bukan probabilitas eksploitasi. Gunakan CVSS + EPSS + business context untuk prioritas akurat. CVSS 10 dengan EPSS 0.01% mungkin kurang prioritas dibanding CVSS 7 dengan EPSS 90%.
2. **Credentialed vs non-credentialed scanning**: Non-credentialed scan memberikan false positive tinggi dan melewatkan banyak vulnerability. CySA+ menekankan credentialed scanning untuk akurasi. Jika scan non-credentialed, validasi manual diperlukan.
3. **TLP vs classification**: TLP adalah sharing boundary, bukan classification. TLP:AMBER berarti boleh dishare dalam organisasi — bukan "rahasia". Jangan gunakan TLP untuk menggantikan classification system.
4. **IOC-based hunting vs TTP-based hunting**: IOC (hash, IP) berubah dalam jam/hari. TTP-based hunting (teknik, prosedur) memberikan deteksi lebih tahan lama. CySA+ menekankan Pyramid of Pain — fokus pada TTPs untuk deteksi berkelanjutan.
5. **Chain of custody dokumentasi**: Setiap evidence transfer harus dicatat — nama, tanggal, tujuan, alasan. Tanpa chain of custody yang terdokumentasi, evidence tidak bisa digunakan legal. Write blocker wajib untuk forensic acquisition.

## License

MIT
