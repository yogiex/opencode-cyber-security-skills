# cyber-security Agent Skills

Koleksi agent skills untuk keamanan siber. Skills ini dirancang untuk meningkatkan kemampuan agen AI dengan menyediakan instruksi, referensi, dan panduan khusus domain keamanan.

## Apa itu Agent Skills?

Agent Skills adalah format open standard (dibuat oleh [Anthropic](https://www.anthropic.com/), diadopsi oleh 20+ agent products) untuk memperluas kemampuan agen AI dengan pengetahuan dan workflow khusus domain.

Setiap skill adalah folder dengan struktur:

```
my-skill/
├── SKILL.md          # Required: metadata (YAML frontmatter) + instructions
├── references/       # Optional: detailed reference documentation
├── scripts/          # Optional: executable code (exploit templates, automation)
└── assets/           # Optional: templates, checklists, resources
```

Agen AI memuat skill melalui **progressive disclosure** dalam 3 tahap:

1. **Discovery** — Saat startup, agen hanya membaca `name` + `description` dari setiap skill (cukup untuk tahu kapan skill relevan).
2. **Activation** — Ketika task cocok dengan deskripsi skill, agen membaca full `SKILL.md`.
3. **Execution** — Agen mengikuti instruksi, opsional memuat file `references/`, mengeksekusi `scripts/`, atau menggunakan template dari `assets/`.

Full instructions hanya dimuat saat diperlukan, sehingga agen bisa menyimpan banyak skill dengan context footprint minimal.

## Best Practices untuk Skill Creators

Panduan ini untuk kontributor dan skill creators. Berdasarkan [Agent Skills Best Practices](https://agentskills.io/skill-creation/best-practices).

### 1. Spending Context Wisely

Setiap token dalam skill Anda bersaing dengan conversation history dan skill lain di context window.

**Add what agent lacks, omit what it knows.** Jangan jelaskan konsep umum (apa itu HTTP, PDF, SQL injection). Fokus ke domain-specific knowledge, non-obvious edge cases, dan project conventions yang agent tidak tahu.

```markdown
<!-- Terlalu panjang — agent sudah tahu apa itu PDF -->
## Extract PDF text
PDF (Portable Document Format) files are a common file format...

<!-- Lebih baik — langsung ke yang agent belum tahu -->
## Extract PDF text
Use pdfplumber for text extraction. For scanned documents, fall back to
pdf2image with pytesseract.
```

Tanyakan pada diri sendiri untuk setiap konten: *"Akankah agent salah tanpa instruksi ini?"* Jika jawabannya tidak, potong.

**Design coherent units.** Skill terlalu sempit → multiple skills perlu di-load untuk satu task (overhead). Skill terlalu luas → sulit diaktivasi secara presisi.

**Aim for moderate detail.** Comprehensive documentation bisa kontraproduktif — agent kesulitan mengekstrak yang relevan. Concise, stepwise guidance + working example > exhaustive docs.

**Structure large skills with progressive disclosure.** SKILL.md wajib <500 lines / 5K tokens. Detail pindahkan ke `references/`. Beri instruksi spesifik: "Read `references/api-errors.md` if the API returns non-200" lebih berguna dari "see references/ for details."

### 2. Favor Procedures over Declarations

Ajarkan *how to approach* suatu masalah kelas tertentu, bukan *what to produce* untuk satu instance.

```markdown
<!-- Specific answer — hanya berguna untuk task ini -->
Join the `orders` table to `customers` on `customer_id`, filter where
`region = 'EMEA'`, and sum the `amount` column.

<!-- Reusable method — work for any analytical query -->
1. Read the schema from `references/schema.yaml` to find relevant tables
2. Join tables using the `_id` foreign key convention
3. Apply any filters from the user's request as WHERE clauses
4. Aggregate numeric columns as needed and format as a markdown table
```

### 3. Provide Defaults, Not Menus

Pilih satu default, sebut alternatif secara singkat.

```markdown
<!-- Terlalu banyak pilihan -->
You can use pypdf, pdfplumber, PyMuPDF, or pdf2image...

<!-- Default jelas dengan escape hatch -->
Use pdfplumber for text extraction. For scanned PDFs requiring OCR,
use pdf2image with pytesseract instead.
```

### 4. Calibrate Control — Match Specificity to Fragility

**Fleksibel** untuk task yang toleran variasi — beri tujuan tanpa langkah rigid.

```markdown
## Code review process
1. Check all database queries for SQL injection (use parameterized queries)
2. Verify authentication checks on every endpoint
3. Look for race conditions in concurrent code paths
```

**Preskriptif** untuk fragile operations — urutan spesifik, jangan modifikasi.

```markdown
## Database migration
Run exactly this sequence:
python scripts/migrate.py --verify --backup
Do not modify the command or add additional flags.
```

### 5. Instruction Patterns yang Efektif

**Gotchas** — lingkungan-spesifik yang melawan asumsi umum. Simpan di SKILL.md (bukan references/) agar terbaca sebelum agent menemui situasi.

```markdown
## Gotchas
- The `users` table uses soft deletes. Queries must include
  `WHERE deleted_at IS NULL`.
- The `/health` endpoint returns 200 even if DB is down. Use `/ready`.
```

> Saat agent membuat mistake, tambahkan koreksinya ke gotchas section. Ini cara paling langsung untuk iterative improvement.

**Templates** — pendek inline di SKILL.md, panjang di `assets/`.

**Checklists** — untuk multi-step workflows, bantu agent track progress.

```markdown
Progress:
- [ ] Step 1: Analyze the form (run `scripts/analyze_form.py`)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping (run `scripts/validate_fields.py`)
```

**Validation loops** — do → validate → fix → repeat until pass.

**Plan-validate-execute** — untuk destructive operations: buat intermediate plan → validate → baru execute.

### 6. Refine dengan Real Execution

First draft hampir selalu perlu refinement. Jalankan skill terhadap task nyata, lalu feed hasilnya (kegagalan maupun keberhasilan) kembali ke proses pembuatan. Minimal 1 pass execute-then-revise.

Baca *execution traces*, bukan cuma final output. Jika agent buang waktu di langkah tidak produktif, cari sebab:
- Instruksi terlalu vague → agent coba beberapa pendekatan
- Instruksi tidak relevan → agent ikuti saja
- Terlalu banyak opsi tanpa default jelas

## Status Struktur Skill

| Status | Arti |
|--------|------|
| ✅ Lean | SKILL.md <500 lines, konten mandiri tanpa references/ (adekuat untuk topik ringan) |
| 🔶 Structured | SKILL.md <500 lines + references/ terorganisir untuk progressive disclosure |
| 📦 Monolithic | SKILL.md >500 lines, belum dipecah — perlu direfactor |

## Available Skills

### 🔴 Red Team (Offensif)

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [oscp-methodology](./skills/oscp-methodology) | 📦 | OSCP (Offensive Security Certified Professional) — mindset, metodologi, dan strategi komprehensif untuk PEN-200/OSCP+ mencakup filsafat Try Harder, 3 attack vectors, enumeration framework, privilege escalation (Linux, Windows, AD), dan reporting. |
| [ptes-standard](./skills/ptes-standard) | 📦 | Penetration Testing Execution Standard (PTES) — panduan komprehensif untuk penetration testing meliputi 7 fase: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, dan reporting. |
| [cpent](./skills/cpent) | 📦 | EC-Council CPENT (Certified Penetration Testing Professional) — mindset, metodologi, dan strategi komprehensif untuk CPENT exam mencakup 14 modul inti, binary exploitation 32/64-bit, IoT/OT/SCADA, double pivoting, report writing, dan LPT Master pathway. |
| [offsec-pen-300](./skills/offsec-pen-300) | 📦 | OffSec PEN-300 / OSEP (Offensive Security Experienced Penetration Tester) — advanced evasion techniques and breaching defenses. AV/EDR evasion, AMSI/AppLocker/CLM bypass, process injection & hollowing, custom C# shellcode runners, MSSQL linked servers, AD exploitation, delegation attacks, ADCS, dan report writing. |
| [offsec-web-300](./skills/offsec-web-300) | 🔶 | OffSec WEB-300 / OSWE (Offensive Security Web Expert) — advanced web application security assessment, white-box testing, source code review (Java, C#, PHP, Python, JavaScript), custom exploit development, .NET deserialization, PHP type juggling, SQLi, SSTI, SSRF, prototype pollution, dan authentication bypass. |
| [waf-evasion-methodology](./skills/waf-evasion-methodology) | 📦 | Pola pikir dan metodologi sistematis untuk WAF evasion — memahami parsing discrepancies, encoding gaps, dan logic mismatches antara WAF dan backend application. |
| [web-app-scan](./skills/web-app-scan) | ✅ | Vulnerability assessment pada web application secara sistematis (deteksi kerentanan umum: SQLi, XSS, config leak, header keamanan, SSL/TLS, dsb) dengan pendekatan terstruktur. |
| [web-recon-simple](./skills/web-reconnaissance) | ✅ | Recon web sederhana: chunk file, network tab, API endpoint, localstorage/token/session, identifikasi teknologi. |

### 🔵 Blue Team (Defensif)

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [ec-ecih](./skills/ec-ecih) | 🔶 | EC-Council ECIH (Certified Incident Handler) v3 — incident handler mindset, IR lifecycle (NIST 800-61 + ECIH 9-stage IH&R), decision frameworks per incident type, forensic readiness, containment strategies, eradication methodology, recovery planning, post-incident lessons learned, dan krisis communication. Berbasis ECIH 212-89 v3 curriculum. |
| [incident-response-plan](./skills/incident-response-plan) | ✅ | Panduan incident response non-teknis untuk organisasi: persiapan, deteksi, analisis, containment, eradikasi, recovery, dan pembelajaran. Cocok untuk tim manajemen, legal, PR, dan koordinator insiden. |
| [log-management-nist-800-92](./skills/log-management-nist-800-92) | ✅ | Panduan log management berdasarkan NIST SP 800-92 untuk perencanaan, pengumpulan, penyimpanan, analisis, dan retensi log keamanan secara terstruktur. |
| [mitre-attack](./skills/mitre-attack) | ✅ | Panduan MITRE ATT&CK framework untuk memahami adversary tactics, techniques, dan prosedur dalam threat intelligence, detection engineering, dan defensive gap analysis. |
| [nist-800-53](./skills/nist-800-53) | ✅ | Panduan Security and Privacy Controls berdasarkan NIST SP 800-53 Rev 5 (Release 5.2.0) untuk pemilihan, implementasi, dan assessment kontrol keamanan dan privasi dalam Risk Management Framework. |
| [risk-management-framework](./skills/risk-management-framework) | ✅ | Panduan NIST Risk Management Framework (SP 800-37) untuk mengelola risiko keamanan dan privasi secara terstruktur, fleksibel, dan berkelanjutan di seluruh siklus hidup sistem. |
| [security-documentation](./skills/security-documentation) | ✅ | Membuat laporan pengujian keamanan dalam format LaTeX dan mengompilasi ke PDF, mengikuti template dokumen yang tersedia. |
| [offsec-ir-200](./skills/offsec-ir-200) | 🔶 | OffSec IR-200 / OSIR (OffSec Incident Responder) — foundational incident response covering full IR lifecycle (NIST 800-61r2), Splunk SIEM analysis with SPL, digital forensics (Autopsy, Volatility 3, FTK Imager), malware triage with YARA, containment/eradication/recovery, and post-mortem reporting. |
| [offsec-th-200](./skills/offsec-th-200) | 📦 | OffSec TH-200 / OSTH (OffSec Threat Hunter) — foundational threat hunting covering proactive threat detection, Splunk SPL, CrowdStrike Falcon CQL, Suricata IDS/IPS, hypothesis-driven hunting (PEAK, SEARCH), MITRE ATT&CK mapping, ransomware & APT case studies, CTI integration, and professional hunt reporting. |
| [offsec-soc-200](./skills/offsec-soc-200) | 🔶 | OffSec SOC-200 / OSDA (OffSec Defense Analyst) — security operations and defensive analysis. SIEM/ELK/KQL, Windows & Linux endpoint detection, attacker methodology, incident investigation, dan SOC analyst framework. |
| [lf-cks](./skills/lf-cks) | 📦 | Certified Kubernetes Security Specialist (CKS) — Kubernetes security mindset, defense-in-depth framework, cluster isolation models, workload segmentation, supply chain trust, authentication & authorization philosophy, network security architecture, runtime protection, compliance posture, dan decision framework untuk securing container platforms. |
| [soc-analyst](./skills/soc-analyst) | ✅ | Pola pikir dan pendekatan untuk Security Analyst dan SOC Analyst dalam mentriage, menyelidiki, merespon insiden, dan berkomunikasi secara efektif. |
| [threat-intelligence](./skills/threat-intelligence) | 📦 | Cyber Threat Intelligence (CTI) — intelligence lifecycle, analytic frameworks (Kill Chain, Diamond Model, ATT&CK), IOC management (STIX/TAXII, MISP, YARA, Sigma), threat hunting (PEAK, ABLE, HMM), dan analyst tradecraft. |

### 🟢 General (Keduanya)

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [comptia-cysa](./skills/comptia-cysa) | 📦 | Panduan lengkap CompTIA CySA+ (CS0-004 V4) mencakup Security Operations, Vulnerability Management, Incident Response, dan Reporting & Communication untuk mempersiapkan sertifikasi Cybersecurity Analyst. |
| [devsecops-mindset](./skills/devsecops-mindset) | ✅ | Panduan pola pikir dan mindset DevSecOps untuk mengintegrasikan keamanan dalam siklus pengembangan secara berkelanjutan, tanpa fokus pada alat/tools tertentu. |
| [owasp-top10-2025](./skills/owasp-top10-2025) | 🔶 | Referensi lengkap OWASP Top 10 2025 untuk risiko keamanan web application. Gunakan saat threat modeling, code review, penetration testing, atau saat membahas kategori A01-A10. |
| [threat-modeling](./skills/threat-modeling) | ✅ | Panduan threat modeling untuk mengidentifikasi, menganalisis, dan memitigasi risiko keamanan pada sistem atau aplikasi secara general dan non-teknis. |

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

Gunakan script scaffold:

```bash
node scripts/add-skill.js <nama-skill> "<deskripsi>"
```

Contoh:

```bash
node scripts/add-skill.js owasp-top10-2025 "OWASP Top 10 2025 vulnerability knowledge and guidance"
```

Setelah scaffold, lakukan refinement:

1. **Jalankan terhadap task nyata** — catat koreksi yang muncul saat agent membuat mistake
2. **Tambahkan gotchas** — masukkan koreksi ke `## Gotchas` di SKILL.md
3. **Terapkan progressive disclosure** — jika SKILL.md >500 lines, pindahkan detail ke `references/`
4. **Validasi** — jalankan `node scripts/sync-skills.js` setelah perubahan

Proses ini (execute-then-revise) adalah cara paling efektif untuk meningkatkan kualitas skill.

## Scripts

| Script | Deskripsi |
| ------ | --------- |
| `node scripts/add-skill.js` | Scaffold skill baru |
| `node scripts/sync-skills.js` | Sinkronisasi manifest.json, plugin files, index.json, dan README |

## Referensi

| Skill | Sumber/Standar | Link |
|------|---------------|------|
| [comptia-cysa](./skills/comptia-cysa) | CompTIA CySA+ CS0-004 | https://www.comptia.org/certifications/cybersecurity-analyst |
| [cpent](./skills/cpent) | EC-Council CPENT, LPT Master | https://www.eccouncil.org/train-certify/certified-penetration-testing-professional-cpent/ |
| [offsec-pen-300](./skills/offsec-pen-300) | OffSec PEN-300, OSEP Exam Guide | https://help.offsec.com/hc/en-us/articles/360050293792-OSEP-Exam-Guide |
| [offsec-web-300](./skills/offsec-web-300) | OffSec WEB-300, OSWE Exam Guide | https://help.offsec.com/hc/en-us/articles/360049792232-OSWE-Exam-Guide |
| [offsec-ir-200](./skills/offsec-ir-200) | OffSec IR-200, OSIR Exam Guide | https://help.offsec.com/hc/en-us/articles/30960007786900 |
| [offsec-th-200](./skills/offsec-th-200) | OffSec TH-200, OSTH Exam Guide | https://help.offsec.com/hc/en-us/articles/29141776768148-OSTH-Exam-Guide |
| [offsec-soc-200](./skills/offsec-soc-200) | OffSec SOC-200, OSDA Exam Guide | https://help.offsec.com/hc/en-us/articles/4410105675412-OSDA-Exam-Guide |
| [oscp-methodology](./skills/oscp-methodology) | OffSec PEN-200, OSCP+ Exam Guide | https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide |
| [devsecops-mindset](./skills/devsecops-mindset) | DevSecOps Principles | - |
| [lf-cks](./skills/lf-cks) | Linux Foundation CKS, CNCF CKS Curriculum, CIS Kubernetes Benchmark | https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/ |
| [ec-ecih](./skills/ec-ecih) | EC-Council ECIH v3 (212-89), NIST SP 800-61, ISO 27035 | https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/ |
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

## Ecosystem

Agent Skills didukung oleh 20+ agent tools dan platform. Lihat [Client Showcase](https://agentskills.io/clients) untuk daftar lengkap.

Beberapa yang kompatibel: OpenCode, Claude Code, Cursor, GitHub Copilot, Gemini CLI, VS Code, OpenAI Codex, Goose, Roo Code, Factory, dan banyak lagi.

## Resources

- [Agent Skills Specification](https://agentskills.io/specification) — Format spesifikasi lengkap
- [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart) — Buat skill pertama kamu
- [Agent Skills Best Practices](https://agentskills.io/skill-creation/best-practices) — Skill creation patterns dan panduan lengkap
- [Evaluating Skill Output Quality](https://agentskills.io/skill-creation/evaluating-skills) — Test cases, assertions, dan grading
- [Optimizing Skill Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — Discovery optimization dan description testing
- [Using Scripts in Skills](https://agentskills.io/skill-creation/using-scripts) — Panduan bundling reusable scripts
- [npx skills](https://skills.sh/) — CLI untuk mengelola skills
- [Validate Agent Skill](https://github.com/marketplace/actions/validate-skill) — GitHub Action untuk validasi
- [Playbooks](https://playbooks.com/skills)
- [Context7 Skills](https://context7.com/docs/skills)

## Kontribusi

Kontribusi sangat diterima! Sebelum menambah atau mengedit skill, baca panduan berikut:

- [Best Practices untuk Skill Creators](#best-practices-untuk-skill-creators) di atas
- [Agent Skills Best Practices](https://agentskills.io/skill-creation/best-practices) — Panduan lengkap patterns dan pitfalls
- [Evaluating Skill Output Quality](https://agentskills.io/skill-creation/evaluating-skills) — Cara sistematis ngetes dan nge-grade skill
- [Optimizing Skill Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — Optimasi discovery biar skill ke-trigger di prompt yang tepat
- [Panduan Kontribusi](.github/CONTRIBUTING.md)

## Lisensi

MIT
