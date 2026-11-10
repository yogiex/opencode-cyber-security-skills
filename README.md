# Cyber Security Agent Skills

<p align="left">
  <a href="https://github.com/yogiex/opencode-cyber-security-skills/actions/workflows/validate-and-sync.yml"><img alt="CI" src="https://github.com/yogiex/opencode-cyber-security-skills/actions/workflows/validate-and-sync.yml/badge.svg?branch=main"></a>
  <img alt="Skills" src="https://img.shields.io/badge/skills-29-blue">
  <img alt="Reference docs" src="https://img.shields.io/badge/reference%20docs-190%2B-informational">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-green"></a>
  <a href="https://github.com/yogiex/opencode-cyber-security-skills/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/yogiex/opencode-cyber-security-skills"></a>
  <a href=".github/CONTRIBUTING.md"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen"></a>
</p>

Kumpulan **Agent Skills** untuk keamanan siber: 29 skill dan 190+ dokumen referensi yang memberi agen AI cara kerja, batas keputusan, dan prosedur yang bisa diaudit untuk pekerjaan red team, blue team, audit, dan rekayasa keamanan.

Repo ini bukan kumpulan prompt. Setiap skill adalah unit terstruktur berisi persona, *decision frame*, referensi bertingkat, dan *gotchas* yang membuat agen berhenti pada batas yang benar — bukan sekadar menghasilkan jawaban yang terdengar meyakinkan.

---

## Daftar Isi

- [Apa itu Agent Skills?](#apa-itu-agent-skills)
- [Mulai Cepat](#mulai-cepat)
- [Available Skills](#available-skills)
- [Struktur Repositori](#struktur-repositori)
- [Kualitas Skill](#kualitas-skill)
- [Menambah Skill Baru](#menambah-skill-baru)
- [Scripts](#scripts)
- [Penggunaan yang Sah](#penggunaan-yang-sah)
- [Referensi dan Sumber](#referensi-dan-sumber)
- [Ekosistem](#ekosistem)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Apa itu Agent Skills?

Agent Skills adalah format open standard (dibuat oleh [Anthropic](https://www.anthropic.com/), diadopsi oleh 20+ produk agen) untuk memperluas kemampuan agen AI dengan pengetahuan dan workflow khusus domain.

Setiap skill adalah folder dengan struktur:

```text
my-skill/
├── SKILL.md          # Wajib: metadata (YAML frontmatter) + instruksi
├── references/       # Opsional: dokumentasi referensi bertingkat
├── scripts/          # Opsional: kode eksekusi (templat exploit, otomasi)
└── assets/           # Opsional: templat, checklist, sumber daya
```

Agen memuat skill melalui **progressive disclosure** dalam tiga tahap:

1. **Discovery** — saat startup, agen hanya membaca `name` + `description` setiap skill.
2. **Activation** — ketika task cocok dengan deskripsi, agen membaca `SKILL.md` secara penuh.
3. **Execution** — agen mengikuti instruksi, lalu memuat `references/`, menjalankan `scripts/`, atau memakai templat dari `assets/` sesuai kebutuhan.

Instruksi lengkap hanya dimuat saat diperlukan, sehingga puluhan skill dapat aktif tanpa membebani context window.

## Mulai Cepat

### Instal via skills CLI

```bash
# Instal semua skill
npx skills add yogiex/opencode-cyber-security-skills

# Instal satu skill saja
npx skills add yogiex/opencode-cyber-security-skills --skill owasp-top10-2025

# Lihat daftar skill yang tersedia
npx skills add yogiex/opencode-cyber-security-skills --list
```

### Claude Code Plugin

```bash
# Daftarkan marketplace dari repo ini
/plugin marketplace add yogiex/opencode-cyber-security-skills

# Instal plugin (berisi seluruh skill)
/plugin install cyber-security-agent-skills@cyber-security-agent-skills
```

> Plugin Claude Code juga didukung di Factory [Droid](https://docs.factory.ai/cli/configuration/plugins#claude-code-compatibility).

### Metode lain

Skill juga dapat dipasang lewat [Playbooks](https://playbooks.com/skills) atau [Context7](https://context7.com/docs/skills):

```bash
# Playbooks
npx playbooks add skill yogiex/opencode-cyber-security-skills

# Context7
npx ctx7 skills install /yogiex/opencode-cyber-security-skills
```

## Available Skills

Legenda status struktur:

| Status | Arti |
|--------|------|
| ✅ Lean | `SKILL.md` <500 baris, mandiri tanpa `references/` — memadai untuk topik ringan |
| 🔶 Structured | `SKILL.md` <500 baris + `references/` terorganisir untuk progressive disclosure |
| 📦 Monolithic | `SKILL.md` >500 baris dan belum dipecah — perlu direfaktor |

### 🔴 Red Team (Offensif)

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [oscp-methodology](./skills/oscp-methodology) | 🔶 | Persona offensive security consultant bersertifikat OSCP — enumerasi bertahap, tiga vektor serangan, privilege escalation Linux/Windows/AD, pivoting, dan disiplin bukti. Bukan untuk persiapan ujian. |
| [ptes-standard](./skills/ptes-standard) | 🔶 | Penetration Testing Execution Standard (PTES) — panduan komprehensif untuk penetration testing meliputi 7 fase: pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, dan reporting. |
| [cpent](./skills/cpent) | 🔶 | Persona pengguna bersertifikat EC-Council CPENT — aturan operasional yang mengikat, dua belas hukum mindset, doktrin kedalaman (double pivoting), jalur serangan Active Directory, eksploitasi binary x86/x64, wireless/IoT/OT-SCADA, dan laporan kelas klien. Dipakai untuk engagement nyata, bukan persiapan ujian. |
| [offsec-pen-300](./skills/offsec-pen-300) | 🔶 | Persona red team operator bersertifikat OSEP — evasion AV/EDR, AMSI/AppLocker/CLM, process injection, shellcode runner kustom, serangan MSSQL, eksploitasi AD/ADCS, dan laporan kelas klien. Bukan untuk persiapan ujian. |
| [offsec-web-300](./skills/offsec-web-300) | 🔶 | Persona konsultan keamanan web white-box bersertifikat OSWE — source code review Java/C#/PHP/Python/JS, deserialization .NET, type juggling PHP, SQLi, SSTI, SSRF, prototype pollution, dan penulisan exploit Python. Bukan untuk persiapan ujian. |
| [waf-evasion-methodology](./skills/waf-evasion-methodology) | 🔶 | Pola pikir dan metodologi sistematis untuk WAF evasion — memahami parsing discrepancies, encoding gaps, dan logic mismatches antara WAF dan backend application. |
| [web-pentest-payloads](./skills/web-pentest-payloads) | 🔶 | Payload dan teknik eksploitasi per kelas kerentanan web: SQLi, NoSQL, command injection, SSTI, XXE, XSS, CSRF, SSRF, LFI/RFI, file upload, deserialization, request smuggling, cache poisoning, JWT/OAuth/SAML, IDOR, business logic, API, prompt injection — dengan syarat otorisasi, decision frame (baseline, dua varian, kanal blind), gotchas, dan bypass filter/WAF. |
| [web-app-scan](./skills/web-app-scan) | ✅ | Penilaian keamanan web application bertahap seperti Nessus/Nikto tetapi manual: fingerprint, config leak, injection, XSS, sesi, akses kontrol, TLS, CORS — dengan batas mode (pasif/aktif), kriteria konfirmasi temuan, dan template output. |
| [web-reconnaissance](./skills/web-reconnaissance) | 🔶 | Recon web/SPA: inventarisasi chunk JS (manifest build, tabel chunk webpack, Coverage, source map), alur data dari aksi UI ke endpoint, analisis bundle, rekam network tab lewat Chrome DevTools MCP atau HAR manual, baca storage browser (localStorage, cookie termasuk HttpOnly, IndexedDB, Cache Storage, OPFS), peta rute frontend + API backend, konfigurasi auth (JWT, cookie, OAuth/OIDC, SAML), identifikasi teknologi dan versi berkeyakinan (header, cookie, jalur aset, banner bundle), triage token, dan CVE. |

### 🔵 Blue Team (Defensif)

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [ec-ecih](./skills/ec-ecih) | 🔶 | Persona incident handler bersertifikat ECIH — siklus IR (NIST 800-61 + ECIH IH&R), triage, containment, eradikasi, pemulihan, kewajiban legal, dan komunikasi krisis. Bukan untuk persiapan ujian. |
| [ec-cnd](./skills/ec-cnd) | 🔶 | Persona pengguna yang sudah memegang sertifikasi EC-Council CND — profil, gaya bicara, dan doktrin operasional untuk memilih kontrol jaringan yang tepat, mengelola perubahan berisiko, membaca telemetri, dan merespons insiden di tingkat jaringan. Persona injection pengguna bersertifikat, bukan tutor ujian. |
| [incident-response-plan](./skills/incident-response-plan) | ✅ | Panduan incident response non-teknis untuk organisasi: persiapan, deteksi, analisis, containment, eradikasi, recovery, dan pembelajaran. Cocok untuk tim manajemen, legal, PR, dan koordinator insiden. |
| [log-management-nist-800-92](./skills/log-management-nist-800-92) | ✅ | Panduan log management berdasarkan NIST SP 800-92 untuk perencanaan, pengumpulan, penyimpanan, analisis, dan retensi log keamanan secara terstruktur. |
| [mitre-attack](./skills/mitre-attack) | ✅ | Panduan MITRE ATT&CK framework untuk memahami adversary tactics, techniques, dan prosedur dalam threat intelligence, detection engineering, dan defensive gap analysis. |
| [nist-800-53](./skills/nist-800-53) | ✅ | Panduan Security and Privacy Controls berdasarkan NIST SP 800-53 Rev 5 (Release 5.2.0) untuk pemilihan, implementasi, dan assessment kontrol keamanan dan privasi dalam Risk Management Framework. |
| [risk-management-framework](./skills/risk-management-framework) | ✅ | Panduan NIST Risk Management Framework (SP 800-37) untuk mengelola risiko keamanan dan privasi secara terstruktur, fleksibel, dan berkelanjutan di seluruh siklus hidup sistem. |
| [security-documentation](./skills/security-documentation) | 🔶 | Menyusun laporan pengujian keamanan yang dapat diaudit: struktur baku, template LaTeX siap pakai (`assets/report-template.tex`), anatomi temuan dengan CVSS v3.1/CWE, bukti `curl` reproducible, dan aturan redaksi. |
| [offsec-ir-200](./skills/offsec-ir-200) | 🔶 | Persona incident responder bersertifikat OSIR — triage host hidup, forensik disk dan memori (Autopsy, Volatility 3), verifikasi integritas berkas, triage malware & YARA, containment, dan post-mortem. Bukan untuk persiapan ujian. |
| [offsec-th-200](./skills/offsec-th-200) | 🔶 | Persona threat hunter bersertifikat OSTH — hunting berbasis hipotesis (PEAK/SEARCH), SPL Splunk, CQL CrowdStrike, Suricata, pemetaan ATT&CK, dan laporan hunt. Bukan untuk persiapan ujian. |
| [offsec-soc-200](./skills/offsec-soc-200) | 🔶 | Persona detection & defensive analyst bersertifikat OSDA — triage Windows/Linux, KQL di ELK, Windows Event Log & Sysmon, deteksi Active Directory, dan rekonstruksi timeline dari telemetri. Bukan untuk persiapan ujian. |
| [lf-cks](./skills/lf-cks) | 🔶 | Persona platform security engineer bersertifikat CKS — trust boundary, isolasi cluster, keamanan workload, supply chain trust, NetworkPolicy, dan runtime defense di Kubernetes. Bukan untuk persiapan ujian. |
| [soc-analyst](./skills/soc-analyst) | ✅ | Pola pikir dan pendekatan untuk Security Analyst dan SOC Analyst dalam mentriage, menyelidiki, merespon insiden, dan berkomunikasi secara efektif. |
| [threat-intelligence](./skills/threat-intelligence) | 🔶 | Cyber Threat Intelligence (CTI) — intelligence lifecycle, analytic frameworks (Kill Chain, Diamond Model, ATT&CK), IOC management (STIX/TAXII, MISP, YARA, Sigma), threat hunting (PEAK, ABLE, HMM), dan analyst tradecraft. |

### 🟢 General (Keduanya)

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [comptia-cysa](./skills/comptia-cysa) | 🔶 | Persona cyber defense analyst bersertifikat CySA+ — triase dan prioritisasi kerentanan (CVSS + EPSS), security operations, respons insiden, dan pelaporan. Bukan untuk persiapan ujian. |
| [devsecops-mindset](./skills/devsecops-mindset) | ✅ | Panduan pola pikir dan mindset DevSecOps untuk mengintegrasikan keamanan dalam siklus pengembangan secara berkelanjutan, tanpa fokus pada alat/tools tertentu. |
| [owasp-top10-2025](./skills/owasp-top10-2025) | 🔶 | Referensi lengkap OWASP Top 10 2025 untuk risiko keamanan web application. Gunakan saat threat modeling, code review, penetration testing, atau saat membahas kategori A01–A10. |
| [threat-modeling](./skills/threat-modeling) | ✅ | Panduan threat modeling untuk mengidentifikasi, menganalisis, dan memitigasi risiko keamanan pada sistem atau aplikasi secara general dan non-teknis. |

### 🟣 Audit & Code Security

| Skill | Status | Deskripsi |
| ----- | ------ | --------- |
| [security-auditor](./skills/security-auditor) | ✅ | Mindset, metodologi, dan referensi untuk security auditor — audit lifecycle, perbandingan framework (ISO 27001, NIST, PCI DSS, SOC 2), kontrol testing, pengumpulan bukti, dan pelaporan temuan yang bisa ditindaklanjuti. Fokus GRC/compliance, bukan hunting kerentanan kode. |
| [code-security-audit](./skills/code-security-audit) | 🔶 | Audit keamanan kode berlapis untuk codebase, API, service, CLI, library, dan daemon: recon terstruktur, coverage ledger deterministik, hunting per-unit dengan subagent terisolasi, validasi adversarial, `findings.json` tervalidasi skema, dan laporan yang bisa diaudit ulang. |

## Struktur Repositori

```text
.
├── manifest.json                  # Sumber kebenaran — konfigurasi global + daftar skill
├── skills/
│   ├── index.json                 # Dibuat otomatis — indeks agent-skills-discovery
│   └── <skill-name>/
│       ├── SKILL.md               # Titik masuk — frontmatter + instruksi + indeks referensi
│       ├── references/            # Dokumentasi referensi bertingkat
│       ├── scripts/               # Skrip pendukung
│       └── assets/                # Aset statis (templat, gambar, CSS)
├── scripts/
│   ├── add-skill.js               # Scaffold skill baru
│   ├── sync-skills.js             # Sinkronisasi manifest, plugin, indeks, marketplace
│   ├── check-changelog.js         # Pastikan setiap perubahan file tercatat
│   └── check-fact-notes.js        # Pastikan klaim faktual punya provenance
├── .claude-plugin/                # Dibuat otomatis — plugin + marketplace Claude Code
├── .cursor-plugin/                # Dibuat otomatis — plugin Cursor
├── .github/
│   ├── workflows/validate-and-sync.yml  # CI — validasi skill/plugin, cek changelog, sync
│   └── CONTRIBUTING.md            # Panduan kontribusi
├── docs/
│   ├── CERTIFICATION-FACTS.md     # Fact sheet — sumber angka dan versi
│   └── SKILL-QUALITY.md           # Ledger kualitas per skill
├── AGENTS.md                      # Instruksi proyek untuk agen AI
├── ARCHITECTURE.md                # Arsitektur dan alur data repo
├── CHANGELOG.md                   # Jejak audit setiap perubahan file
├── LICENSE
└── README.md
```

Alur data: `SKILL.md` frontmatter → `manifest.json` → `sync-skills.js` → `plugin.json`, `marketplace.json`, `skills/index.json`. Detail lengkap ada di [ARCHITECTURE.md](ARCHITECTURE.md).

## Kualitas Skill

Kualitas tidak dinilai dari panjang dokumen, melainkan dari ada tidaknya empat hal:

| Dimensi | Yang diperiksa | Cara diperiksa |
|---------|----------------|----------------|
| **Trigger** | Kondisi pemakaian eksplisit di `description` atau bagian "Kapan Digunakan" | pemeriksaan struktur |
| **Decision Frame** | Bagian `## Decision Frame` berisi aturan keputusan, bukan pertanyaan retoris | `grep '^## Decision Frame'` |
| **Provenance** | Angka dan versi tertaut ke fact sheet | `node scripts/check-fact-notes.js` |
| **Failure modes** | Bagian `Gotchas` berisi koreksi dari eksekusi nyata | `grep '^## .*Gotcha'` |

Matriks status per skill, backlog, dan ringkasan cakupan dipelihara di [docs/SKILL-QUALITY.md](docs/SKILL-QUALITY.md). Klaim faktual bersumber dari [docs/CERTIFICATION-FACTS.md](docs/CERTIFICATION-FACTS.md) dan diverifikasi otomatis di CI.

## Menambah Skill Baru

```bash
# 1. Scaffold
node scripts/add-skill.js <nama-skill> "<deskripsi>"

# 2. Sinkronkan manifest, plugin, dan indeks
node scripts/sync-skills.js

# 3. Verifikasi provenance dan changelog sebelum commit
node scripts/check-fact-notes.js
node scripts/check-changelog.js
```

Setelah scaffold, lakukan refinement:

1. **Jalankan terhadap task nyata** — catat koreksi yang muncul saat agen membuat kesalahan.
2. **Tambahkan gotchas** — masukkan setiap koreksi ke `## Gotchas` di `SKILL.md`.
3. **Terapkan progressive disclosure** — jika `SKILL.md` >500 baris atau >5K token, pindahkan detail ke `references/`.
4. **Pasang decision frame** — nyatakan kapan skill dipakai, kapan berhenti, dan bukti minimum yang harus dikumpulkan.
5. **Catat di CHANGELOG** — setiap file yang ditambah, diubah, atau dihapus wajib disebut namanya.

Panduan lengkap pola dan pitfall ada di [CONTRIBUTING.md](.github/CONTRIBUTING.md). Proses execute-then-revise ini adalah cara paling efektif untuk menaikkan kualitas skill.

## Scripts

| Script | Deskripsi |
| ------ | --------- |
| `node scripts/add-skill.js` | Scaffold skill baru beserta `SKILL.md` |
| `node scripts/sync-skills.js` | Sinkronisasi `manifest.json`, plugin files, `marketplace.json`, dan `skills/index.json` |
| `node scripts/check-changelog.js` | Pastikan setiap file yang berubah tercatat di `CHANGELOG.md` |
| `node scripts/check-fact-notes.js` | Pastikan klaim faktual punya provenance ke fact sheet |

## Penggunaan yang Sah

Skill ofensif di repo ini ditujukan untuk pengujian keamanan yang **berizin**, laboratorium, CTF, dan riset defensif. Gunakan hanya terhadap sistem yang Anda miliki atau yang Anda punya izin tertulis untuk menguji. Setiap skill ofensif menyertakan syarat otorisasi dan batas berhenti; patuhi keduanya. Penulis tidak bertanggung jawab atas penyalahgunaan.

## Referensi dan Sumber

| Skill | Sumber/Standar | Link |
|-------|----------------|------|
| [comptia-cysa](./skills/comptia-cysa) | CompTIA CySA+ CS0-004 | https://www.comptia.org/certifications/cybersecurity-analyst |
| [cpent](./skills/cpent) | EC-Council CPENT | https://www.eccouncil.org/train-certify/certified-penetration-testing-professional-cpent/ |
| [ec-cnd](./skills/ec-cnd) | EC-Council CND | https://www.eccouncil.org/train-certify/certified-network-defender-cnd/ |
| [ec-ecih](./skills/ec-ecih) | EC-Council ECIH v3 (212-89), NIST SP 800-61, ISO 27035 | https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/ |
| [devsecops-mindset](./skills/devsecops-mindset) | DevSecOps Principles | — |
| [incident-response-plan](./skills/incident-response-plan) | NIST SP 800-61, SANS PICERL | — |
| [lf-cks](./skills/lf-cks) | Linux Foundation CKS, CNCF CKS Curriculum, CIS Kubernetes Benchmark | https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/ |
| [log-management-nist-800-92](./skills/log-management-nist-800-92) | NIST SP 800-92 | https://csrc.nist.gov/pubs/sp/800/92 |
| [mitre-attack](./skills/mitre-attack) | MITRE ATT&CK | https://attack.mitre.org |
| [nist-800-53](./skills/nist-800-53) | NIST SP 800-53 Rev 5 (5.2.0) | https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final |
| [offsec-ir-200](./skills/offsec-ir-200) | OffSec IR-200 (OSIR) | — |
| [offsec-pen-300](./skills/offsec-pen-300) | OffSec PEN-300 (OSEP) | — |
| [offsec-soc-200](./skills/offsec-soc-200) | OffSec SOC-200 (OSDA) | — |
| [offsec-th-200](./skills/offsec-th-200) | OffSec TH-200 (OSTH) | — |
| [offsec-web-300](./skills/offsec-web-300) | OffSec WEB-300 (OSWE) | — |
| [oscp-methodology](./skills/oscp-methodology) | OffSec PEN-200 (OSCP+) | — |
| [owasp-top10-2025](./skills/owasp-top10-2025) | OWASP Top 10 2025 | https://owasp.org/Top10/ |
| [ptes-standard](./skills/ptes-standard) | PTES | http://www.pentest-standard.org/ |
| [risk-management-framework](./skills/risk-management-framework) | NIST SP 800-37 Rev 2 | https://csrc.nist.gov/pubs/sp/800/37/r2 |
| [security-documentation](./skills/security-documentation) | OWASP WSTG, PTES | — |
| [soc-analyst](./skills/soc-analyst) | MITRE ATT&CK, NIST SP 800-61 | — |
| [threat-intelligence](./skills/threat-intelligence) | CTI Lifecycle, MITRE ATT&CK, Cyber Kill Chain, Diamond Model, STIX/TAXII | https://attack.mitre.org |
| [threat-modeling](./skills/threat-modeling) | STRIDE, DFD, NIST SP 800-154 | — |
| [waf-evasion-methodology](./skills/waf-evasion-methodology) | OWASP CRS, MITRE ATT&CK | — |
| [web-app-scan](./skills/web-app-scan) | OWASP WSTG, PTES | — |
| [web-pentest-payloads](./skills/web-pentest-payloads) | PayloadsAllTheThings, PortSwigger WSA, OWASP WSTG | https://github.com/swisskyrepo/PayloadsAllTheThings |
| [web-reconnaissance](./skills/web-reconnaissance) | OSINT Framework, OWASP WSTG | — |

## Ekosistem

Agent Skills didukung oleh 20+ agent tools dan platform. Lihat [Client Showcase](https://agentskills.io/clients) untuk daftar lengkap.

Beberapa yang kompatibel: OpenCode, Claude Code, Cursor, GitHub Copilot, Gemini CLI, VS Code, OpenAI Codex, Goose, Roo Code, Factory, dan banyak lagi.

Dokumentasi ekosistem:

- [Agent Skills Specification](https://agentskills.io/specification) — Format spesifikasi lengkap
- [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart) — Membuat skill pertama
- [Agent Skills Best Practices](https://agentskills.io/skill-creation/best-practices) — Pola dan panduan pembuatan skill
- [Evaluating Skill Output Quality](https://agentskills.io/skill-creation/evaluating-skills) — Test case, assertion, dan grading
- [Optimizing Skill Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — Optimasi discovery
- [Using Scripts in Skills](https://agentskills.io/skill-creation/using-scripts) — Panduan bundling skrip
- [npx skills](https://skills.sh/) — CLI untuk mengelola skills
- [Validate Agent Skill](https://github.com/marketplace/actions/validate-skill) — GitHub Action untuk validasi

## Kontribusi

Kontribusi sangat diterima. Sebelum mengirim PR:

1. Baca [CONTRIBUTING.md](.github/CONTRIBUTING.md) — pola penulisan skill yang terbukti efektif.
2. Pahami [ARCHITECTURE.md](ARCHITECTURE.md) — alur data dan apa yang boleh diedit manual.
3. Catat setiap perubahan file di [CHANGELOG.md](CHANGELOG.md).
4. Jalankan pemeriksaan lokal:

```bash
node scripts/check-changelog.js --base origin/main
node scripts/check-fact-notes.js
```

CI menjalankan tiga pemeriksaan: validasi setiap skill yang berubah, validasi plugin terhadap JSON Schema, dan verifikasi changelog. Gunakan **conventional commit** (`feat:`, `fix:`, `docs:`) dan buka PR ke `dev` atau `main` sesuai alur repo.

## Lisensi

Dirilis di bawah [MIT License](LICENSE).
