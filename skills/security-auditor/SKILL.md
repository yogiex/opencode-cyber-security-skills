---
name: security-auditor
description: Panduan mindset, metodologi, dan referensi untuk security auditor — mencakup audit lifecycle, framework comparison, control testing, evidence collection, dan certification path.
license: MIT
compatibility: opencode
metadata:
  audience: auditor, grc-analyst, security-analyst, compliance-officer
  workflow: auditing, compliance, risk-assessment
  standard: cisa, iso-27001, soc2, pci-dss, hipaa, nist-csf
---

# Security Auditor Mindset & Methodology

## Apa Itu Security Auditor

Security auditor adalah profesional yang secara independen mengevaluasi kontrol keamanan, kebijakan, dan infrastruktur organisasi untuk memastikan kesesuaian dengan standar regulasi dan industri. Berbeda dengan penetration tester yang mencari kerentanan teknis, auditor fokus pada **efektivitas kontrol** — apakah kontrol dirancang dengan baik (design) dan berjalan sebagaimana mestinya (operating effectiveness).

### Prinsip Dasar Audit

- **Independence** — auditor harus independen dari area yang diaudit untuk menjaga objektivitas
- **Evidence-based** — setiap temuan harus didukung bukti yang cukup, kompeten, dan relevan
- **Risk-based approach** — fokus pada area dengan risiko tertinggi, bukan mencoba mengaudit semuanya
- **Professional skepticism** — selalu verifikasi, jangan hanya percaya apa yang dikatakan atau ditunjukkan
- **Materiality** — fokus pada kelemahan yang signifikan, bukan ketidaksempurnaan minor

## Core Audit Lifecycle

### 1. Planning

- Pahami business objectives dan konteks organisasi
- Identifikasi regulatory requirements yang berlaku (PCI DSS untuk payment, HIPAA untuk healthcare, dll)
- Tentukan scope audit — sistem, proses, lokasi mana yang termasuk
- Lakukan risk assessment awal untuk prioritasi area audit
- Kembangkan audit program dan timeline

### 2. Scoping

- Identifikasi in-scope systems, data flows, dan third parties
- Tentukan control objectives dan framework reference
- Pilih control sample berdasarkan risk dan materiality
- Dokumentasikan scope exclusions dan justifikasinya
- Koordinasikan dengan auditee untuk akses dan resource

### 3. Fieldwork & Evidence Collection

Teknik pengumpulan bukti:

| Teknik | Deskripsi | Contoh |
|--------|-----------|--------|
| Inquiry | Wawancara dengan staff dan management | "Bagaimana proses access review dilakukan?" |
| Observation | Mengamati pelaksanaan kontrol | "Tunjukkan bagaimana supervisor memverifikasi perubahan" |
| Inspection | Memeriksa dokumen dan konfigurasi | Review kebijakan keamanan, SOP, log |
| Re-performance | Menjalankan ulang kontrol | Ikuti proses provision user dari awal sampai selesai |
| CAATs | Computer-Assisted Audit Techniques | ACL, scripting untuk analisis data massal |
| Walkthrough | Telusuri transaksi dari awal hingga akhir | Ikuti satu change request dari submit ke deploy |

### 4. Control Testing

Test setiap kontrol untuk dua dimensi:

- **Design effectiveness** — apakah kontrol secara teori bisa mencegah/mendeteksi risiko jika berjalan dengan baik?
- **Operating effectiveness** — apakah kontrol berjalan secara konsisten sepanjang periode audit?

Sampling methods:
- **Judgmental sampling** — pilih sample berdasarkan risiko
- **Statistical sampling** — random sample dengan confidence level tertentu
- **Benchmarking** — jika kontrol otomatis, test satu kali dan benchmark selebihnya

### 5. Reporting

Struktur audit report standar:

1. **Executive Summary** — temuan utama, risk level keseluruhan
2. **Scope & Methodology** — apa yang diaudit, bagaimana, periode
3. **Findings & Observations** — setiap temuan: condition, criteria, cause, consequence, recommendation
4. **Risk Ratings** — severity (critical/high/medium/low) + likelihood
5. **Management Response** — action plan, owner, target date
6. **Opinion** — kesimpulan auditor (unqualified, qualified, adverse, disclaimer)

### 6. Remediation Tracking

- Monitor implementasi corrective actions
- Validasi efektivitas remediasi (re-testing)
- Escalate jika target date terlewat
- Update risk register berdasarkan status remediasi

### 7. Follow-up Audit

- Verifikasi bahwa temuan sebelumnya telah diperbaiki
- Pastikan perbaikan bersifat permanen (bukan temporary fix)
- Identifikasi recurring issues yang mengindikasikan systemic problem

## Framework Comparison

| Framework | Tipe | Geografi | Output | Biaya | Ideal Untuk |
|-----------|------|----------|--------|-------|-------------|
| SOC 2 | Attestation (CPA) | US | Type I / Type II report | $30K-$150K | SaaS, B2B service providers |
| ISO 27001:2022 | Certification | Global | Certificate (3yr + surveillance) | $30K-$150K | International, enterprise |
| HIPAA Security Rule | Regulation | US (healthcare) | Self-assessed | $15K-$60K | Healthtech, PHI handlers |
| PCI DSS v4.0 | Industry mandate | Global | RoC / SAQ | $20K-$200K | Payment processors |
| NIST CSF 2.0 | Framework (voluntary) | US | Maturity profile | $10K-$50K | Any org, federal contractors |
| SOX ITGC | Regulation | US (public) | Section 404 attestation | $50K-$200K | Public companies |
| HITRUST CSF | Certification | US (healthcare) | Certified / readiness | $50K-$150K | Healthcare enterprises |

### Framework Mapping — Control Overlap

~80% overlap SOC 2 ↔ ISO 27001. ~40-60% overlap dengan HIPAA dan PCI DSS.

| Control Area | SOC 2 | ISO 27001 | NIST CSF | PCI DSS |
|-------------|-------|-----------|----------|---------|
| Access Control | CC6.1-6.3 | A.8.3-8.5 | PR.AC | Req 7-8 |
| Encryption | CC6.7 | A.8.24 | PR.DS | Req 3-4 |
| Monitoring | CC7.1-7.3 | A.8.15-8.16 | DE.CM | Req 10 |
| Incident Response | CC7.3-7.5 | A.5.24-5.28 | RS.RP | Req 12.10 |
| Risk Assessment | CC3.1-3.4 | A.5.3, 8.8 | ID.RA | Req 12.2 |
| Training | CC1.4 | A.6.3 | PR.AT | Req 12.6 |
| Change Management | CC8.1 | A.8.32 | PR.IP | Req 6.4 |

### Framework Decision Tree

```
Apakah organisasi menangani PHI?
├── Ya → HIPAA mandatory
├── Apakah juga payment card? → + PCI DSS
└── Apakah B2B SaaS? → + SOC 2

Apakah organisasi memproses kartu kredit?
├── Ya → PCI DSS mandatory
└── Apakah bertransaksi internasional? → + ISO 27001

B2B SaaS menjual ke enterprise:
├── US-focused → SOC 2 Type II
└── International → ISO 27001

Federal contractor / critical infrastructure:
└── NIST CSF + specific contract requirements
```

## Control Testing Domains

### ITGC (IT General Controls)

| Domain | Contoh Kontrol | Testing Approach |
|--------|---------------|------------------|
| Logical Access | User provision/deprovision, MFA, access reviews | Sample request tickets, verify access lists, check MFA enforcement |
| Change Management | Change approval, segregation of duties, emergency changes | Trace change lifecycle, verify approval workflow, test emergency bypass |
| Computer Operations | Backup/restore, monitoring, incident handling | Review backup logs, test restore, verify monitoring alerts |
| Program Development | SDLC methodology, code review, test environments | Review project documentation, verify separation of dev/test/prod |
| Program Changes | Patch management, version control, release mgmt | Sample patches, verify testing before production |

### Application Controls

| Jenis | Contoh |
|-------|--------|
| Input | Validasi format data, range check, duplicate detection |
| Processing | Run-to-run totals, balancing, sequence check |
| Output | Report distribution, output verification, data retention |

## Evidence Collection & Documentation

### Standar Bukti Audit

- **Sufficient** — cukup banyak untuk mendukung kesimpulan
- **Competent** — reliable, relevant, dan valid
- **Relevant** — berhubungan langsung dengan control objective
- **Useful** — membantu auditor mencapai kesimpulan

### Dokumentasi Audit (Workpapers)

Setiap workpaper harus mencakup:
- **Header**: client name, audit area, period, auditor name
- **Objective**: apa yang diuji dan mengapa
- **Scope**: sample size, period coverage, population
- **Procedures**: langkah-langkah yang dilakukan
- **Findings**: hasil pengujian, evidence reference
- **Conclusion**: pass/fail, risk rating
- **Review**: reviewer name, date, clearance

### Audit Evidence Matrix

| Source | Contoh | Keandalan |
|--------|--------|-----------|
| Dokumen (eksternal) | Invoice vendor, contract | Tinggi |
| Dokumen (internal) | Kebijakan, SOP, logs | Medium |
| Observasi langsung | Walkthrough | Medium |
| Inquiry (management) | Wawancara | Rendah |
| CAATs | ACL reports, SQL queries | Medium-tinggi |
| Third-party confirmation | SOC 2 report vendor | Tinggi |

## Certification Path

| Sertifikasi | Penerbit | Fokus | Harga | Prasyarat | Ideal Untuk |
|-------------|----------|------|-------|-----------|-------------|
| CISA | ISACA | IT audit, controls, governance | $575-$760 | 5yr IS audit experience | IT auditor, compliance |
| CISSP | (ISC)² | Security leadership, broad | ~$749 | 5yr in 2+ domains | Security manager, CISO track |
| ISO 27001 Lead Auditor | PECB / berbagai | ISMS audit spesifik | ~$3,000 | None formal | ISO 27001 auditor |
| CRISC | ISACA | Risk management, control | $575-$760 | 5yr risk/control exp | Risk manager, GRC |
| CISM | ISACA | Security management | $575-$760 | 5yr security mgmt | Security manager, CISO |
| CompTIA Security+ | CompTIA | Entry-level security | ~$392 | None | Entry point sebelum auditor |

### CISA vs ISO 27001 Lead Auditor

| Aspek | CISA | ISO 27001 Lead Auditor |
|-------|------|------------------------|
| Scope | Broad — IT audit across systems, governance, security | Specialized — ISMS audit based on ISO 27001 |
| Recognition | Very high, enterprise/government | High, ISO-certified environments |
| Career path | IT auditor, risk, compliance, governance | ISO audit, ISMS consultancy |
| Cost | $575-$760 | ~$3,000 |
| Renewal | 20 CPE/year, 120/3yr | Varies by certifying body |

### Career Progression

```
IT Auditor (junior) → Senior IT Auditor → Audit Manager → Director of Audit
                                    ↓
                          IT Risk & Assurance → GRC Lead → CISO
```

Start dengan **IT audit entry-level** atau **compliance analyst**. Dapatkan Security+ atau CISA untuk mempercepat.

## Ketika Menggunakan Skill Ini

**Gunakan ketika:**
- Merencanakan atau menjalankan audit keamanan
- Membandingkan compliance frameworks
- Menentukan certification path
- Menyusun audit program atau workpaper
- Mereview evidence collection strategy
- Mempersiapkan SOC 2, ISO 27001, PCI DSS, atau HIPAA audit

**Jangan gunakan ketika:**
- Membutuhkan technical penetration testing — gunakan oscp-methodology
- Membutuhkan threat modeling detail — gunakan threat-modeling
- Membutuhkan incident response playbook — gunakan incident-response-plan

## Referensi Lengkap

### Standards & Frameworks

| Nama | Penerbit | Deskripsi | Link |
|------|----------|-----------|------|
| ISO/IEC 27001:2022 | ISO | ISMS requirements, 93 Annex A controls | [iso.org](https://www.iso.org/standard/27001) |
| NIST CSF 2.0 | NIST | Cybersecurity Framework — 6 functions (Identify, Protect, Detect, Respond, Recover, Govern) | [nist.gov](https://www.nist.gov/cyberframework) |
| NIST SP 800-53 Rev. 5 | NIST | Security & Privacy Controls — 20+ control families | [csrc.nist.gov](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) |
| SOC 2 Trust Services Criteria | AICPA | 5 criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy | [aicpa.org](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/soc.html) |
| PCI DSS v4.0 | PCI SSC | 12 requirements, 64 new requirements in v4.0 | [pcisecuritystandards.org](https://www.pcisecuritystandards.org/) |
| HIPAA Security Rule | HHS/OCR | Administrative, Physical, Technical Safeguards | [hhs.gov](https://www.hhs.gov/hipaa/for-professionals/security/index.html) |
| COBIT 2019 | ISACA | IT governance framework — goals cascade, capability levels | [isaca.org](https://www.isaca.org/resources/cobit) |
| HITRUST CSF | HITRUST | Healthcare-focused, consolidated from HIPAA/NIST/ISO/PCI | [hitrustalliance.net](https://hitrustalliance.net/) |
| CMMC 2.0 | US DoD | Cybersecurity Maturity Model Certification untuk defense contractors | [dodcmmc.org](https://dodcmmc.org/) |
| FedRAMP | US Government | Cloud service authorization untuk federal agencies | [fedramp.gov](https://www.fedramp.gov/) |

### Buku & Publications

| Judul | Penulis | Fokus |
|-------|---------|-------|
| CISA Review Manual | ISACA | Official CISA exam guide — 5 domains, audit process |
| CISA Questions, Answers & Explanations | ISACA | CISA practice questions database |
| ISO 27001:2022 Lead Auditor Course Materials | PECB | Full ISMS audit training materials |
| Information Security Auditing: A Comprehensive Guide | David W. Baker | Practical IT audit methodology |
| Auditing IT Infrastructures for Compliance | Robert Johnson | Compliance-driven IT auditing approach |
| The Security Auditor's Handbook | Stephen A. Hess | Day-to-day security audit practices |
| Hacking Exposed: Security Auditing & Compliance | Joel Scambray | Security testing meets audit compliance |
| Cybersecurity Auditing for Dummies | ServiceNow | Introduction to cybersecurity auditing |
| Audit and Trace Log Management | Phillip Q. Moore | Log management dari perspektif audit |
| Security Risk Management: Building an Information Security Risk Management Program | Evan Wheeler | Risk management framework untuk auditor |

### Sertifikasi Detail

| Sertifikasi | Biaya Exam | CPE/Year | Renewal Cycle | Global Holders (approx) |
|-------------|-----------|----------|---------------|------------------------|
| CISA | $575 (member) / $760 (non) | 20 | 3 tahun (120 CPE) | ~150,000+ |
| CISSP | $749 | 40 | 3 tahun (120 CPE) | ~150,000+ |
| ISO 27001 Lead Auditor | ~$3,000 (includes training) | Varies | 3 tahun (some lifetime) | ~100,000+ |
| CRISC | $575 (member) / $760 (non) | 20 | 3 tahun | ~50,000+ |
| CISM | $575 (member) / $760 (non) | 20 | 3 tahun | ~50,000+ |
| CompTIA Security+ | $392 | None required | 3 tahun (CE program) | ~500,000+ |

### Audit Tools

**Vulnerability Scanning:**
- **Nessus** (Tenable) — comprehensive vulnerability scanning, compliance checks, CVSS v4/EPSS
- **Qualys** — Cloud-based, 60+ mandates mapped, PCI ASV approved
- **OpenVAS** — Open-source vulnerability scanner

**Compliance Automation:**
- **Vanta** — SOC 2/ISO 27001/HIPAA automation, 1200+ automated tests, AI evidence review
- **Drata** — Continuous monitoring, 100+ integrations, automated evidence collection
- **Scrut** — GRC platform, 80+ frameworks, continuous control monitoring
- **ComplianceKit** — Open-source, 9 frameworks, audit-ready evidence packs, Terraform/kubectl remediation
- **Alvor** — Security architecture + compliance automation, cross-framework mapping
- **OmniSec** — AI-driven GRC, continuous compliance monitoring
- **AquilaX** — Compliance scanner for developers, OWASP/CWE coverage

**GRC Platforms:**
- **ServiceNow GRC** — Enterprise GRC, integrated with ITSM
- **Archer (RSA)** — Mature enterprise GRC platform
- **OneTrust** — Privacy + security GRC
- **SAP GRC** — ERP-focused SoD and access controls

### Training & Courses

| Nama | Provider | Level | Fokus |
|------|----------|-------|-------|
| CISA Exam Preparation | ISACA / Infosec / Cybrary | Advanced | Full 5 domains, exam prep |
| ISO 27001 Lead Auditor (5-day) | PECB / BSI / TÜV SÜD | Advanced | ISMS audit methodology |
| CISSP Bootcamp | (ISC)² / SANS / Infosec | Advanced | 8 domains, exam prep |
| SEC440: Security Essentials | SANS | Intermediate | Foundation for audit |
| CompTIA Security+ | CompTIA / Udemy / PluralSight | Beginner | Entry-level security |
| SOC 2 and ISO 27001 Compliance Bootcamp | Various (Udemy, LinkedIn) | Beginner-Medium | Practical compliance |
| NIST CSF Workshop | NIST / SANS | Intermediate | CSF implementation |

### Komunitas & Curated Lists

| Nama | Deskripsi | Link |
|------|-----------|------|
| ISACA | Global professional association for IT audit, risk, governance | [isaca.org](https://www.isaca.org/) |
| ISACA Journal | Publications, whitepapers, research on IT audit | [isaca.org](https://www.isaca.org/resources/isaca-journal) |
| (ISC)² Community | Cybersecurity professional community | [isc2.org](https://www.isc2.org/members/community) |
| ComplianceKit (GitHub) | Open-source compliance scanner + audit tool | [github.com](https://github.com/darpanzope/compliancekit) |
| NIST CSF Online | NIST CSF 2.0 resources, mappings, quick start | [nist.gov](https://www.nist.gov/cyberframework) |
| AICPA SOC Resources | Official SOC 2 guidance, white papers | [aicpa.org](https://www.aicpa.org/interestareas/frc/assuranceadvisoryservices/soc.html) |
| PCI SSC Documents | Official PCI DSS library, guidance documents | [pcisecuritystandards.org](https://www.pcisecuritystandards.org/) |
| Scrut Blog | Compliance audit best practices, comparison guides | [scrut.io](https://www.scrut.io/blog) |
| Compyl Blog | Multi-framework compliance, control mapping | [compyl.com](https://compyl.com/blog) |
| Episki Framework Guides | Framework comparisons, mapping NIST CSF to others | [episki.com](https://episki.com/frameworks/nistcsf/mapping-to-other-frameworks) |

### Regulasi & Compliance Reference

| Regulasi | Retensi Log | Key Focus | Sanksi |
|----------|-------------|-----------|--------|
| PCI DSS v4.0 | 12 bulan (3 bulan immediately available) | Cardholder data protection | $100K/month |
| HIPAA | 6 tahun | PHI confidentiality | $2.13M/year per kategori |
| SOX Section 802 | 7 tahun | Financial controls integrity | $5M + 20 years |
| GDPR | Purpose-based (1-3 tahun typical) | Personal data protection | EUR 20M / 4% turnover |
| SOC 2 | Risk-based | 5 Trust Services Criteria | Contractual (no regulatory fine) |
| ISO 27001 | Defined per policy | ISMS maturity | Certificate revocation |
| FedRAMP | 90 hari online, archival per agency | Cloud security for federal | Authorization removal |
