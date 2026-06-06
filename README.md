# cyber-security Agent Skills

Koleksi agent skills untuk keamanan siber. Skills ini dirancang untuk meningkatkan kemampuan agen AI dengan menyediakan instruksi, referensi, dan panduan khusus domain keamanan.

## Apa itu Agent Skills?

Agent Skills adalah folder berisi instruksi, skrip, dan sumber daya yang dapat digunakan agen AI untuk bekerja lebih akurat dan efisien. Skills ini kompatibel dengan semua agen AI yang mendukung [standar Agent Skills](https://agentskills.io).

## Available Skills

### 🔴 Red Team (Offensif)

| Skill | Deskripsi |
| ----- | --------- |
| [oscp-methodology](./skills/oscp-methodology) | OSCP (Offensive Security Certified Professional) — mindset, metodologi, dan strategi komprehensif untuk PEN-200/OSCP+ mencakup filsafat Try Harder, 3 attack vectors, enumeration framework, privilege escalation (Linux, Windows, AD), dan reporting. |
| [ptes-standard](./skills/ptes-standard) | Penetration Testing Execution Standard (PTES) — panduan komprehensif untuk penetration testing meliputi 7 fase: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, dan reporting. |
| [cpent](./skills/cpent) | EC-Council CPENT (Certified Penetration Testing Professional) — mindset, metodologi, dan strategi komprehensif untuk CPENT exam mencakup 14 modul inti, binary exploitation 32/64-bit, IoT/OT/SCADA, double pivoting, report writing, dan LPT Master pathway. |
| [waf-evasion-methodology](./skills/waf-evasion-methodology) | Pola pikir dan metodologi sistematis untuk WAF evasion — memahami parsing discrepancies, encoding gaps, dan logic mismatches antara WAF dan backend application. |
| [web-app-scan](./skills/web-app-scan) | Vulnerability assessment pada web application secara sistematis (deteksi kerentanan umum: SQLi, XSS, config leak, header keamanan, SSL/TLS, dsb) dengan pendekatan terstruktur. |
| [web-recon-simple](./skills/web-reconnaissance) | Recon web sederhana: chunk file, network tab, API endpoint, localstorage/token/session, identifikasi teknologi. |

### 🔵 Blue Team (Defensif)

| Skill | Deskripsi |
| ----- | --------- |
| [incident-response-plan](./skills/incident-response-plan) | Panduan incident response non-teknis untuk organisasi: persiapan, deteksi, analisis, containment, eradikasi, recovery, dan pembelajaran. Cocok untuk tim manajemen, legal, PR, dan koordinator insiden. |
| [log-management-nist-800-92](./skills/log-management-nist-800-92) | Panduan log management berdasarkan NIST SP 800-92 untuk perencanaan, pengumpulan, penyimpanan, analisis, dan retensi log keamanan secara terstruktur. |
| [mitre-attack](./skills/mitre-attack) | Panduan MITRE ATT&CK framework untuk memahami adversary tactics, techniques, dan prosedur dalam threat intelligence, detection engineering, dan defensive gap analysis. |
| [nist-800-53](./skills/nist-800-53) | Panduan Security and Privacy Controls berdasarkan NIST SP 800-53 Rev 5 (Release 5.2.0) untuk pemilihan, implementasi, dan assessment kontrol keamanan dan privasi dalam Risk Management Framework. |
| [risk-management-framework](./skills/risk-management-framework) | Panduan NIST Risk Management Framework (SP 800-37) untuk mengelola risiko keamanan dan privasi secara terstruktur, fleksibel, dan berkelanjutan di seluruh siklus hidup sistem. |
| [security-documentation](./skills/security-documentation) | Membuat laporan pengujian keamanan dalam format LaTeX dan mengompilasi ke PDF, mengikuti template dokumen yang tersedia. |
| [soc-analyst](./skills/soc-analyst) | Pola pikir dan pendekatan untuk Security Analyst dan SOC Analyst dalam mentriage, menyelidiki, merespon insiden, dan berkomunikasi secara efektif. |
| [threat-intelligence](./skills/threat-intelligence) | Cyber Threat Intelligence (CTI) — intelligence lifecycle, analytic frameworks (Kill Chain, Diamond Model, ATT&CK), IOC management (STIX/TAXII, MISP, YARA, Sigma), threat hunting (PEAK, ABLE, HMM), dan analyst tradecraft. |

### 🟢 General (Keduanya)

| Skill | Deskripsi |
| ----- | --------- |
| [comptia-cysa](./skills/comptia-cysa) | Panduan lengkap CompTIA CySA+ (CS0-004 V4) mencakup Security Operations, Vulnerability Management, Incident Response, dan Reporting & Communication untuk mempersiapkan sertifikasi Cybersecurity Analyst. |
| [devsecops-mindset](./skills/devsecops-mindset) | Panduan pola pikir dan mindset DevSecOps untuk mengintegrasikan keamanan dalam siklus pengembangan secara berkelanjutan, tanpa fokus pada alat/tools tertentu. |
| [owasp-top10-2025](./skills/owasp-top10-2025) | Referensi lengkap OWASP Top 10 2025 untuk risiko keamanan web application. Gunakan saat threat modeling, code review, penetration testing, atau saat membahas kategori A01-A10. |
| [threat-modeling](./skills/threat-modeling) | Panduan threat modeling untuk mengidentifikasi, menganalisis, dan memitigasi risiko keamanan pada sistem atau aplikasi secara general dan non-teknis. |

## Instalasi

### Skills

Gunakan [skills](https://skills.sh/) untuk menginstal skills secara langsung:

```bash
# Install semua skills
npx skills add cyber-security/agent-skills

# Install skill spesifik
npx skills add cyber-security/agent-skills --skill owasp-top10-2025

# Lihat daftar skills yang tersedia
npx skills add cyber-security/agent-skills --list
```

### Claude Code Plugin

Instal melalui plugin system Claude Code:

```bash
# Tambahkan plugin (termasuk semua skills)
/plugin add cyber-security/agent-skills
```

> Claude Code plugins juga didukung di Factory [Droid](https://docs.factory.ai/cli/configuration/plugins#claude-code-compatibility).

### Metode Instalasi Lain

Agent skills juga bisa diinstal melalui perintah berikut dari [Playbooks](https://playbooks.com/skills) atau [Context7](https://context7.com/docs/skills):

```bash
# Playbooks
npx playbooks add skill cyber-security/agent-skills

# Context7
npx ctx7 skills install /cyber-security/agent-skills
```

## Menambah Skill Baru

Gunakan script yang tersedia untuk menambah skill baru:

```bash
node scripts/add-skill.js <nama-skill> "<deskripsi>"
```

Contoh:

```bash
node scripts/add-skill.js owasp-top10-2025 "OWASP Top 10 2025 vulnerability knowledge and guidance"
```

Script ini akan membuat struktur skill dan otomatis memperbarui manifest.json, platform plugin files, skills/index.json, dan README.

## Scripts

| Script | Deskripsi |
| ------ | --------- |
| `node scripts/add-skill.js` | Menambah skill baru ke repository |
| `node scripts/sync-skills.js` | Sinkronisasi manifest.json, platform plugin files, skills/index.json, dan README dengan direktori skills |

## Referensi

| Skill | Sumber/Standar | Link |
|---|---|---|
| [comptia-cysa](./skills/comptia-cysa) | CompTIA CySA+ CS0-004 | https://www.comptia.org/certifications/cybersecurity-analyst |
| [cpent](./skills/cpent) | EC-Council CPENT, LPT Master | https://www.eccouncil.org/train-certify/certified-penetration-testing-professional-cpent/ |
| [oscp-methodology](./skills/oscp-methodology) | OffSec PEN-200, OSCP+ Exam Guide | https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide |
| [devsecops-mindset](./skills/devsecops-mindset) | DevSecOps Principles | - |
| [incident-response-plan](./skills/incident-response-plan) | NIST SP 800-61, SANS PICERL | - |
| [log-management-nist-800-92](./skills/log-management-nist-800-92) | NIST SP 800-92 | https://csrc.nist.gov/pubs/sp/800/92 |
| [mitre-attack](./skills/mitre-attack) | MITRE ATT&CK | https://attack.mitre.org |
| [nist-800-53](./skills/nist-800-53) | NIST SP 800-53 Rev 5 (5.2.0) | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final |
| [owasp-top10-2025](./skills/owasp-top10-2025) | OWASP Top 10 2025 | https://owasp.org/Top10/ |
| [ptes-standard](./skills/ptes-standard) | PTES | http://www.pentest-standard.org/ |
| [risk-management-framework](./skills/risk-management-framework) | NIST SP 800-37 Rev 2 | https://csrc.nist.gov/pubs/sp/800/37/r2 |
| [security-documentation](./skills/security-documentation) | OWASP WSTG, PTES | - |
| [soc-analyst](./skills/soc-analyst) | MITRE ATT&CK, NIST SP 800-61 | - |
| [threat-intelligence](./skills/threat-intelligence) | CTI Lifecycle, MITRE ATT&CK, Cyber Kill Chain, Diamond Model, STIX/TAXII | https://attack.mitre.org |
| [threat-modeling](./skills/threat-modeling) | STRIDE, DFD, NIST SP 800-154 | - |
| [waf-evasion-methodology](./skills/waf-evasion-methodology) | OWASP CRS, MITRE ATT&CK | - |
| [web-app-scan](./skills/web-app-scan) | OWASP WSTG, PTES | - |
| [web-recon-simple](./skills/web-reconnaissance) | OSINT Framework, OWASP WSTG | - |

## Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [npx skills](https://skills.sh/)
- [Validate Agent Skill](https://github.com/marketplace/actions/validate-skill)
- [Playbooks](https://playbooks.com/skills)
- [Context7 Skills](https://context7.com/docs/skills)

## Kontribusi

Kontribusi sangat diterima! Silakan baca [Panduan Kontribusi](.github/CONTRIBUTING.md) untuk informasi lebih lanjut.

## Lisensi

MIT
