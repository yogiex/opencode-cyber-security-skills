# Analisis Kebutuhan — Reporting & Communication VA (Vulnerability Assessment)

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-14
**Target:** `skills/vulnerability-assessment/` — aspek pelaporan dan komunikasi kerentanan
**Pertanyaan yang dijawab:** `references/reporting.md` saat ini satu berkas 114 baris yang memuat tiga audiens (teknis, manajemen, compliance) sekaligus, tanpa kedalaman pada penulisan eksekutif, komunikasi risiko ke non-teknis, redaksi bukti, trend/diff, dashboard, presentasi, komunikasi false positive, tailoring audiens, versioning, glosarium KPI, dan eskalasi/exception. Apa yang dibutuhkan agar aspek reporting & communication VA setara dengan kedalaman aspek lain (methodology, scanning, scoring, prioritisasi)?
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md), [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md), [CND-PERSONA-NEEDS.md](CND-PERSONA-NEEDS.md) (analisis kebutuhan); [PERSONA-CONVERSION.md](PERSONA-CONVERSION.md) (standar konversi)
**Sumber brainstorm:** subagent `brainstorm-va-reporting` (15 topik, 8 berkas baru, 14 gotchas)

---

## 1. Ringkasan

Skill `vulnerability-assessment` sudah punya satu berkas pelaporan, [reporting.md](../skills/vulnerability-assessment/references/reporting.md) (114 baris), yang memuat prinsip pelaporan, struktur laporan teknis, laporan manajemen, laporan compliance, dan best practices. Itu cukup untuk kerangka, tetapi **tidak cukup untuk komunikasi yang bisa ditindaklanjuti**: tidak ada panduan menulis executive summary dalam bahasa risiko bisnis, tidak ada aturan redaksi bukti, tidak ada definisi metrik trend/diff, tidak ada desain dashboard, tidak ada panduan presentasi ke manajemen, tidak ada protokol komunikasi false positive, tidak ada tailoring audiens/variant laporan, tidak ada versioning & change control, tidak ada glosarium KPI, dan tidak ada eskalasi/exception communication.

Masalahnya bukan kekurangan konten teknis — skill ini sudah kuat di scanning, CVSS, dan prioritisasi. Masalahnya adalah **jarak antara temuan teknis dan keputusan bisnis**: laporan yang tidak bisa dibaca manajemen tidak akan pernah diremediasi, dan temuan yang tidak dikomunikasikan dengan benar akan dianggap noise.

Rekomendasi: **pecah `reporting.md` menjadi overview + index**, dan tambahkan **8 berkas referensi baru** yang masing-masing berfokus pada satu domain komunikasi. Setiap berkas mengikuti konvensi repo (frontmatter `name`/`description`/`tags`, diakhiri Best Practices, indeks 1:1 di `SKILL.md`). Tidak ada berkas yatim, tidak ada duplikasi dengan `security-documentation`, `remediation-verification.md`, `cvss-scoring.md`, `prioritization.md`, dan `wazuh`.

Yang membuat aspek ini bernilai bukan template laporan (itu bisa dicari), melainkan **keputusan komunikasi**: seberapa detail manajemen perlu tahu, kapan redaksi wajib, bagaimana menolak klaim "sudah aman", dan bagaimana mengeskalasi temuan yang menggantung. Itu bagian yang belum ada di repo.

---

## 2. Kondisi Repo Saat Ini

### 2.1 Inventaris yang relevan

| Berkas | Peran | Kedekatan dengan reporting & communication |
|---|---|---|
| `skills/vulnerability-assessment/references/reporting.md` | struktur laporan teknis/manajemen/compliance | **target utama refactor** (114 baris, tiga audiens dalam satu berkas) |
| `skills/vulnerability-assessment/SKILL.md` | indeks referensi + capability map + progressive disclosure | wajib diperbarui 1:1 saat berkas ditambah |
| `skills/vulnerability-assessment/references/remediation-verification.md` | tracking, re-scan, accepted risk, regresi | overlap parsial — tracking vs penulisan guidance |
| `skills/vulnerability-assessment/references/cvss-scoring.md` | CVSS v3.1/v4.0, contextual scoring | overlap parsial — scoring vs komunikasi skor |
| `skills/vulnerability-assessment/references/prioritization.md` | prioritisasi berbasis risiko, SLA, threat intel | overlap parsial — prioritas vs komunikasi prioritas |
| `skills/vulnerability-assessment/references/scanner-config.md` | false positive handling (teknis) | overlap parsial — triase teknis vs komunikasi FP |
| `skills/vulnerability-assessment/references/persona.md` | profil, suara, batas klaim | wajib konsisten dengan suara persona |
| `skills/security-documentation/SKILL.md` + `references/finding-writeup.md` | anatomi temuan, LaTeX, CVSS/CWE, PoC, redaksi | **duplikasi paling berisiko** — anatomi temuan sudah ada di sana |
| `skills/wazuh/references/reporting-and-handover.md` | laporan triase alert, redaksi, handover | overlap parsial — triage alert vs VA report |
| `skills/security-auditor` | audit kepatuhan/GRC | rujukan untuk compliance report, bukan duplikasi |

### 2.2 Kesenjangan: 15 topik brainstorm vs kondisi saat ini

| # | Topik brainstorm | Status di `reporting.md` saat ini | Verdict |
|---|---|---|---|
| 1 | Executive summary writing (business risk language) | 1 blok 20 baris, generik | **gap besar** |
| 2 | Technical report writing (reproducibility & evidence) | struktur template, cukup | perlu panduan bukti & redaksi |
| 3 | Compliance report (framework mapping) | tabel 4 baris PCI/SOC/ISO | **gap** — hanya contoh, tanpa metodologi mapping |
| 4 | Remediation guidance (actionable + effort estimate) | 3 baris rekomendasi | **gap besar** |
| 5 | Risk communication (CVSS to non-technical) | tidak ada | **gap besar** |
| 6 | Redaction & evidence handling | tidak ada | **gap besar** |
| 7 | Trend reporting (MoM/MTTR/coverage) | 2 baris contoh | **gap** |
| 8 | Diff reporting (new/resolved/regressed) | tidak ada | **gap besar** |
| 9 | Dashboard design for VA metrics | tidak ada | **gap besar** |
| 10 | Meeting & presentation to management | tidak ada | **gap** |
| 11 | False positive communication | tidak ada | **gap** |
| 12 | Audience tailoring & report variants | prinsip "audiens berbeda, laporan berbeda" | perlu kerangka variant |
| 13 | Report versioning & change control | tidak ada | **gap** |
| 14 | Metric definitions & KPI glossary | tidak ada | **gap** |
| 15 | Escalation & exception communication | tidak ada | **gap** |

Kesimpulan: `reporting.md` saat ini adalah **kerangka + template**, bukan **panduan komunikasi**. Ia mencampur tiga audiens dalam satu berkas dan tidak memisahkan "cara menulis" dari "apa yang ditulis".

### 2.3 Catatan kondisi kerja

- Working tree sedang memuat perubahan belum-commit untuk `vulnerability-assessment` (0.26.0). Implementasi aspek reporting tidak boleh me-revert berkas yang sudah ada.
- Skill ini adalah **methodology skill dengan persona voice**, bukan persona bersertifikat murni. Tidak ada fact sheet; provenance tidak diperlukan. Perubahan reporting tidak boleh menambah angka ujian.
- `security-documentation` sudah memiliki anatomi temuan yang matang. Perubahan ini **tidak boleh menduplikasi** anatomi temuan; ia hanya boleh merujuk.

---

## 3. Temuan (bukti terukur)

Diukur 2026-11-14 terhadap `skills/vulnerability-assessment/references/reporting.md` dan `SKILL.md`.

| # | Temuan | Cara memeriksa | Akibat |
|---|---|---|---|
| T1 | `reporting.md` memuat 3 audiens dalam 1 berkas (114 baris) | hitung baris per section | sulit progressive disclosure; agent memuat terlalu banyak konteks |
| T2 | Tidak ada panduan executive summary dalam bahasa risiko bisnis | grep `business risk\|risiko bisnis` = 0 | manajemen menerima daftar CVE, bukan keputusan |
| T3 | Tidak ada aturan redaksi bukti | grep `redaksi\|redaction` = 0 | risiko kebocoran PII/token di laporan |
| T4 | Tidak ada definisi metrik trend/diff | grep `MTTR\|MoM\|regressed` = 0 | trend tidak comparable antar bulan |
| T5 | Tidak ada desain dashboard | grep `dashboard` = 0 | metrik tidak terstandarisasi |
| T6 | Tidak ada panduan presentasi ke manajemen | grep `presentasi\|slide` = 0 | komunikasi tatap muka tidak terstruktur |
| T7 | Tidak ada komunikasi false positive | grep `false positive` = 0 di reporting.md | stakeholder menerima temuan yang belum ditriase |
| T8 | Tidak ada versioning laporan | grep `versi\|version` = 0 | tidak bisa audit perubahan laporan |
| T9 | Tidak ada glosarium KPI | grep `KPI\|glosarium` = 0 | angka dashboard ambigu |
| T10 | Tidak ada eskalasi/exception | grep `eskalasi\|exception` = 0 | temuan Critical menggantung |
| T11 | `SKILL.md` Capability Map hanya 1 baris "Pelaporan" | baca Capability Map | agent tidak tahu ada sub-domain reporting |
| T12 | `reporting.md` Best Practices hanya 6 butir generik | baca section | tidak cukup untuk komunikasi |

---

## 4. Definisi

**Reporting & communication VA** — seluruh proses mengubah temuan teknis menjadi informasi yang bisa ditindaklanjuti oleh audiens yang tepat (engineer, manajemen, compliance, auditor), termasuk penulisan, redaksi, visualisasi, presentasi, versioning, dan eskalasi.

**Executive summary** — ringkasan 1 halaman yang menyatakan risiko bisnis, bukan daftar CVE. Dibaca oleh orang yang tidak akan membuka detail teknis.

**Technical report** — laporan yang bisa direproduksi: setiap temuan punya URL/parameter/perintah/respons, dan bukti mentah tersimpan di lampiran terbatas.

**Compliance report** — pemetaan temuan ke kontrol framework (PCI DSS, SOC 2, ISO 27001, NIST, dll.) dengan bukti yang bisa diaudit.

**Remediation guidance** — instruksi perbaikan yang actionable (langkah konkret) disertai estimasi effort dan tenggat, bukan "patch saja".

**Risk communication** — penerjemahan CVSS/skor teknis ke bahasa risiko yang dipahami non-teknis, tanpa inflasi atau deflasi.

**Redaction** — penggantian data sensitif (token, cookie, PII) dengan penanda, dengan jejak bahwa redaksi dilakukan.

**Trend reporting** — pelaporan perubahan metrik antar periode (MoM) dengan definisi metrik yang stabil.

**Diff reporting** — pelaporan perbedaan temuan antar assessment (new/resolved/regressed) dengan identitas temuan yang stabil.

**Dashboard** — visualisasi metrik VA yang terstandarisasi, dengan definisi KPI dan sumber data.

**Audience tailoring** — penyesuaian isi, kedalaman, dan bahasa laporan berdasarkan audiens.

**Report variant** — versi laporan yang berbeda (eksekutif, teknis, compliance, management one-pager) dari sumber data yang sama.

**Report versioning** — penomoran dan change control laporan agar perubahan bisa diaudit.

**KPI glossary** — daftar metrik VA dengan definisi, sumber, dan frekuensi pengukuran.

**Escalation & exception communication** — protokol mengkomunikasikan temuan yang melewati SLA, accepted risk, dan pengecualian.

**False positive communication** — cara mengkomunikasikan temuan yang terverifikasi bukan kerentanan ke stakeholder, tanpa kehilangan kredibilitas.

---

## 5. Ruang Lingkup

**Termasuk:**
- Refactor `reporting.md` menjadi overview + index (tanpa konten detail yang dipindah).
- 8 berkas referensi baru: `reporting-executive.md`, `reporting-technical.md`, `reporting-compliance.md`, `reporting-remediation.md`, `risk-communication.md`, `trend-diff-reporting.md`, `dashboard-design.md`, `false-positive-communication.md`.
- Pembaruan `SKILL.md`: Capability Map, Reference Documentation, Progressive Disclosure (indeks 1:1).
- Pembaruan `CHANGELOG.md` dan `docs/SKILL-QUALITY.md` (jumlah referensi).
- Panduan penulisan laporan, redaksi, trend/diff, dashboard, presentasi, komunikasi FP, tailoring audiens, versioning, glosarium KPI, eskalasi/exception.

**Tidak termasuk:**
- Implementasi file referensi (analisis ini hanya menetapkan kebutuhan; implementasi dilakukan setelah disetujui).
- Duplikasi anatomi temuan (sudah ada di `security-documentation`).
- Duplikasi tracking remediasi/re-scan (sudah ada di `remediation-verification.md`).
- Duplikasi scoring CVSS (sudah ada di `cvss-scoring.md`).
- Duplikasi prioritisasi (sudah ada di `prioritization.md`).
- Duplikasi triase false positive teknis (sudah ada di `scanner-config.md`).
- Pembuatan aplikasi dashboard (hanya desain dan spesifikasi metrik).
- Perubahan skill lain di luar `vulnerability-assessment`.

---

## 6. Kebutuhan Fungsional

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | `reporting.md` menjadi overview + index: prinsip pelaporan, peta audiens, index ke 8 berkas, best practices; konten detail pindah ke berkas khusus | `reporting.md` ≤ 80 baris; tidak ada template laporan lengkap di dalamnya |
| FR-2 | Panduan executive summary dalam bahasa risiko bisnis: struktur 1 halaman, terjemahan severity ke dampak bisnis, top prioritas remediasi, tanpa jargon CVE mentah | `reporting-executive.md` memuat template + contoh + anti-pola |
| FR-3 | Panduan laporan teknis: reproducibility, bukti, redaksi, cakupan autentikasi, segmen tidak terjangkau, temuan yang tidak tereproduksi | `reporting-technical.md` memuat checklist + aturan redaksi + contoh |
| FR-4 | Panduan laporan compliance: metodologi mapping temuan → kontrol framework, bukti yang bisa diaudit, status compliance, gap analysis | `reporting-compliance.md` memuat tabel mapping + metode + contoh |
| FR-5 | Panduan remediation guidance: instruksi actionable, estimasi effort (S/M/L atau jam), tenggat, pemilik, verifikasi; bukan "patch saja" | `reporting-remediation.md` memuat template + estimasi effort + contoh |
| FR-6 | Panduan risk communication: penerjemahan CVSS/skor ke bahasa non-teknis, kalibrasi (tidak inflasi/deflasi), analogi, "so what" | `risk-communication.md` memuat kerangka + contoh + anti-pola |
| FR-7 | Panduan trend reporting: definisi metrik (MoM, MTTR, coverage, density), frekuensi, sumber data, presentasi | `trend-diff-reporting.md` memuat definisi + formula + contoh |
| FR-8 | Panduan diff reporting: identitas temuan stabil (fingerprint), klasifikasi new/resolved/regressed/reopened, aturan pencocokan | `trend-diff-reporting.md` memuat algoritma pencocokan + contoh |
| FR-9 | Panduan desain dashboard: KPI inti, layout, sumber data, refresh, akses, anti-pola | `dashboard-design.md` memuat spesifikasi + wireframe teks + KPI |
| FR-10 | Panduan presentasi ke manajemen: struktur deck, 1 slide = 1 pesan, visualisasi, Q&A, follow-up | `reporting-executive.md` atau berkas khusus memuat kerangka presentasi |
| FR-11 | Panduan komunikasi false positive: protokol mengkomunikasikan temuan yang bukan kerentanan, menjaga kredibilitas, dokumentasi triase | `false-positive-communication.md` memuat protokol + template + contoh |
| FR-12 | Kerangka audience tailoring & report variants: matriks audiens × isi × kedalaman × bahasa; variant dari sumber data yang sama | `reporting.md` (overview) memuat matriks; setiap berkas menyebut audiens target |
| FR-13 | Panduan report versioning & change control: penomoran, changelog laporan, approval, distribusi | `reporting-compliance.md` atau `reporting.md` memuat prosedur |
| FR-14 | Glosarium KPI VA: daftar metrik dengan definisi, sumber, frekuensi, target | `trend-diff-reporting.md` dan `dashboard-design.md` memuat glosarium (satu sumber kebenaran) |
| FR-15 | Panduan eskalasi & exception communication: SLA breach, accepted risk, pengecualian, format eskalasi, pemilik | `risk-communication.md` dan `false-positive-communication.md` memuat protokol |
| FR-16 | Setiap berkas referensi baru muncul tepat sekali di `SKILL.md` (Reference Documentation dan Progressive Disclosure) | indeks 1:1; `grep` nama berkas = jumlah yang diharapkan |
| FR-17 | Setiap berkas referensi baru ber-frontmatter `name`/`description`/`tags` dan diakhiri Best Practices | pemeriksaan struktur |
| FR-18 | `SKILL.md` Capability Map diperluas: baris "Pelaporan" dipecah menjadi sub-kapabilitas yang menaut ke 8 berkas baru | baca Capability Map |
| FR-19 | Tidak ada materi ujian, bobot, passing score, atau katalog sertifikasi di berkas baru | grep pola §2 PERSONA-INJECTION-NEEDS = 0 |
| FR-20 | Tidak mengarang CVE, angka, atau output tool; ketidakpastian eksplisit | aturan di setiap berkas |

---

## 7. Kebutuhan Non-Fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| NFR-1 | `SKILL.md` tetap ≤ 450 baris (batas keras); kelebihan materi dipindah ke `references/`, tidak dibuang | hitung baris |
| NFR-2 | Setiap berkas `references/` muncul tepat sekali di Reference Documentation; tidak ada berkas yatim | indeks 1:1 |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`) | pemeriksaan instalasi |
| NFR-4 | Bahasa Indonesia + istilah teknis Inggris; kode dan komentar berbahasa Inggris | pemeriksaan visual |
| NFR-5 | Setiap penghapusan/perubahan berkas tercatat di `CHANGELOG.md` beserta alasannya | `check-changelog.js` |
| NFR-6 | Perubahan bisa diverifikasi ulang oleh mesin: grep, hitung baris, resolusi tautan, paritas tabel | perintah verifikasi |
| NFR-7 | Tidak menambah dependensi runtime; pemeriksaan memakai Node bawaan | tidak ada paket baru |
| NFR-8 | Total referensi setelah perubahan: 9 (lama) → 17 (9 lama + 8 baru); `reporting.md` tetap ada sebagai overview | hitung berkas |
| NFR-9 | Setiap berkas baru diakhiri section "Best Practices" | pemeriksaan struktur |
| NFR-10 | Tidak ada duplikasi anatomi temuan dengan `security-documentation` | rujukan silang, bukan salinan |

---

## 8. Arsitektur Referensi Usulan

17 berkas referensi (9 lama + 8 baru). `reporting.md` tetap ada sebagai overview + index. Setiap berkas baru berfokus pada satu domain komunikasi.

| # | Berkas | Isi utama | Topik brainstorm | Audiens utama |
|---|---|---|---|---|
| 1 | `reporting.md` (refactor) | prinsip pelaporan, peta audiens, index ke 8 berkas, best practices; tanpa template detail | #12 audience tailoring | semua |
| 2 | `reporting-executive.md` | executive summary 1 halaman, bahasa risiko bisnis, top prioritas, presentasi ke manajemen, deck structure | #1, #10 | manajemen/CISO |
| 3 | `reporting-technical.md` | reproducibility, bukti, redaksi, cakupan auth, segmen tidak terjangkau, temuan tidak tereproduksi | #2, #6 | engineer/analyst |
| 4 | `reporting-compliance.md` | mapping framework, bukti audit, status compliance, gap analysis, versioning & change control | #3, #13 | compliance/auditor |
| 5 | `reporting-remediation.md` | guidance actionable, estimasi effort, tenggat, pemilik, verifikasi, accepted risk communication | #4 | engineer/pemilik remediasi |
| 6 | `risk-communication.md` | CVSS → bahasa non-teknis, kalibrasi, eskalasi, exception communication | #5, #15 | manajemen/stakeholder |
| 7 | `trend-diff-reporting.md` | MoM/MTTR/coverage/density, diff new/resolved/regressed, fingerprint, glosarium KPI | #7, #8, #14 | manajemen/program owner |
| 8 | `dashboard-design.md` | KPI inti, layout, sumber data, refresh, akses, anti-pola | #9 | manajemen/analyst |
| 9 | `false-positive-communication.md` | protokol komunikasi FP, triase ke stakeholder, menjaga kredibilitas, dokumentasi | #11 | stakeholder/auditor |

### 8.1 Outline konten per berkas baru (usulan)

**`reporting-executive.md`**
- Prinsip executive summary (1 halaman, risiko bisnis, bukan daftar CVE)
- Struktur: Overall Risk, Key Findings, Business Impact, Prioritas Remediasi, Trend
- Terjemahan severity → dampak bisnis (tabel)
- Top 3 prioritas remediasi (format)
- Presentasi ke manajemen: struktur deck, 1 slide = 1 pesan, visualisasi, Q&A, follow-up
- Anti-pola (inflasi, jargon, daftar CVE tanpa konteks)
- Best Practices

**`reporting-technical.md`**
- Prinsip reproducibility (URL, parameter, perintah, respons)
- Struktur laporan teknis (reuse kerangka lama, dipindah dari reporting.md)
- Bukti: screenshot, raw output, log; penanda unik
- Redaksi: token, cookie, PII → penanda; jejak redaksi
- Cakupan autentikasi (unauth vs auth) wajib disebut
- Segmen tidak terjangkau + temuan tidak tereproduksi
- Anti-pola
- Best Practices

**`reporting-compliance.md`**
- Prinsip compliance report (mapping, bukti audit, status)
- Metodologi mapping temuan → kontrol framework (PCI DSS, SOC 2, ISO 27001, NIST, CIS)
- Tabel mapping (reuse contoh lama)
- Gap analysis & status compliance (compliant/partial/non-compliant)
- Bukti yang bisa diaudit (hash, timestamp, sumber)
- Versioning & change control laporan (penomoran, changelog, approval, distribusi)
- Best Practices

**`reporting-remediation.md`**
- Prinsip remediation guidance (actionable, effort, tenggat, pemilik)
- Template guidance per temuan
- Estimasi effort (S/M/L atau jam), asumsi
- Prioritas remediasi vs mitigasi vs accept (rujuk `prioritization.md`)
- Komunikasi accepted risk (rujuk `remediation-verification.md`)
- Anti-pola ("patch saja", "segera")
- Best Practices

**`risk-communication.md`**
- Prinsip risk communication (terjemahan CVSS → bahasa non-teknis)
- Kerangka: skor → dampak → likelihood → "so what"
- Kalibrasi (tidak inflasi/deflasi), analogi
- Eskalasi: format, pemilik, tenggat, jalur
- Exception communication: pengecualian, compensating control, review
- Anti-pola
- Best Practices

**`trend-diff-reporting.md`**
- Prinsip trend & diff (metrik stabil, identitas temuan stabil)
- Definisi metrik: jumlah temuan per severity, coverage, MTTR, density, new/resolved/regressed
- Formula + sumber data + frekuensi
- Diff reporting: fingerprint temuan, aturan pencocokan, klasifikasi
- Contoh laporan trend (MoM)
- Glosarium KPI (satu sumber kebenaran)
- Best Practices

**`dashboard-design.md`**
- Prinsip dashboard VA (KPI inti, bukan vanity metric)
- KPI inti: total open, by severity, MTTR, coverage, SLA breach, trend
- Layout (wireframe teks), sumber data, refresh, akses
- Definisi setiap KPI (rujuk glosarium di `trend-diff-reporting.md`)
- Anti-pola (chart junk, metrik tanpa definisi)
- Best Practices

**`false-positive-communication.md`**
- Prinsip komunikasi FP (kredibilitas, transparansi)
- Protokol: triase → verifikasi → komunikasi → dokumentasi
- Template komunikasi FP ke stakeholder
- Menjaga kredibilitas saat temuan dicabut
- Eskalasi FP yang disengketakan
- Best Practices

---

## 9. Batas Scope & Anti-Duplikasi

| Skill/berkas existing | Yang TIDAK diduplikasi | Batas yang diambil reporting |
|---|---|---|
| `security-documentation` | anatomi temuan, LaTeX, CVSS/CWE, PoC, redaksi dasar | reporting hanya merujuk; redaksi lanjutan (evidence handling) boleh ada di `reporting-technical.md` tanpa mengulang anatomi |
| `remediation-verification.md` | tracking, re-scan, accepted risk, regresi | `reporting-remediation.md` fokus pada **penulisan guidance**, bukan tracking |
| `cvss-scoring.md` | scoring CVSS v3.1/v4.0, contextual | `risk-communication.md` fokus pada **komunikasi** skor, bukan perhitungan |
| `prioritization.md` | prioritisasi, SLA, threat intel | `reporting-remediation.md` merujuk, tidak menulis ulang |
| `scanner-config.md` | false positive handling (teknis) | `false-positive-communication.md` fokus pada **komunikasi** FP ke stakeholder |
| `wazuh/reporting-and-handover.md` | laporan triase alert | VA reporting fokus pada **VA report**, bukan triage alert |
| `security-auditor` | audit kepatuhan/GRC | `reporting-compliance.md` fokus pada **mapping temuan**, bukan audit penuh |

Prinsip: reporting & communication boleh **merujuk** skill/berkas lain, tetapi setiap kali topik mendalam dibutuhkan, ia menunjuk berkas yang sudah ada alih-alih menulis ulang.

---

## 10. Gotchas (14)

1. **Executive summary tanpa angka severity yang bisa ditindaklanjuti.** Manajemen menerima narasi tanpa jumlah, tidak bisa memprioritaskan. Selalu sertakan hitungan per severity + top 3.
2. **Melaporkan CVSS base score sebagai risk final.** CVSS 9.8 internal non-kritis bukan prioritas #1. Konteks bisnis menentukan.
3. **Template laporan teknis tanpa cakupan autentikasi.** Laporan dibaca sebagai jaminan menyeluruh. Selalu sebut unauth/auth.
4. **Bukti mentah (raw output) di badan laporan.** Risiko kebocoran PII/token. Pindah ke lampiran terbatas, badan laporan berisi bukti yang diredaksi.
5. **Redaksi yang menghapus jejak redaksi.** Auditor tidak tahu data disensor. Selalu sebut "[teredaksi]" + alasan.
6. **Remediation guidance generik ("update patch") tanpa effort estimate.** Tidak bisa dijadwalkan. Selalu sertakan effort (S/M/L) dan tenggat.
7. **Compliance mapping tanpa bukti temuan.** Audit tidak lulus. Setiap mapping harus punya referensi temuan.
8. **Trend tanpa definisi metrik stabil.** MoM tidak comparable. Definisikan metrik sekali, pakai konsisten.
9. **Diff report tanpa identitas temuan yang stabil.** New/resolved salah klasifikasi. Gunakan fingerprint (asset + CVE/CWE + lokasi).
10. **Dashboard tanpa definisi KPI.** Angka ambigu. Setiap KPI punya definisi, sumber, frekuensi.
11. **Presentasi manajemen yang terlalu teknis.** Kehilangan audiens. 1 slide = 1 pesan, bahasa bisnis.
12. **False positive yang dilaporkan sebagai "tidak ditemukan" tanpa triase.** Menghilangkan temuan nyata. Dokumentasikan triase.
13. **Report versioning tanpa change log.** Tidak bisa audit perubahan. Selalu catat versi + perubahan.
14. **Eskalasi tanpa batas waktu dan pemilik.** Temuan Critical menggantung. Selalu set tenggat + pemilik + jalur.

---

## 11. Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Duplikasi dengan `security-documentation` | repo redundan, user bingung | tabel batas + rujukan silang; tidak menyalin anatomi |
| Duplikasi dengan `remediation-verification.md` | tumpang tindih tracking vs guidance | batas jelas: tracking di sana, penulisan guidance di sini |
| `reporting.md` refactor memutus tautan lama | tautan rusak di skill lain | pertahankan `reporting.md` sebagai overview; jangan hapus |
| 8 berkas baru terlalu banyak | SKILL.md bengkak, drift indeks | batas NFR-1/NFR-2; uji 1:1 |
| Konten reporting jadi generik (bukan VA) | kehilangan nilai | setiap berkas menyebut konteks VA (scan, CVE, CVSS, remediasi) |
| Overlap antar 8 berkas baru | duplikasi internal | tabel batas antar berkas; satu sumber kebenaran (glosarium di trend-diff) |
| Redaksi tidak konsisten | kebocoran data | satu aturan redaksi di `reporting-technical.md`, dirujuk semua |
| Dashboard jadi vanity metric | metrik tidak actionable | `dashboard-design.md` mewajibkan definisi + sumber + target |

---

## 12. Antipattern

| ID | Antipattern | Mengapa salah |
|---|---|---|
| AP-1 | Menyalin anatomi temuan dari `security-documentation` | duplikasi; satu sumber kebenaran sudah ada |
| AP-2 | Menulis `reporting.md` tetap memuat template lengkap setelah refactor | refactor tidak bermakna; progressive disclosure gagal |
| AP-3 | Membuat berkas baru tanpa memperbarui `SKILL.md` index | berkas yatim; drift seperti `cpent` |
| AP-4 | Mengganti "exam" menjadi "assessment" tanpa mengubah isi | pola tetap lolos secara semantik (tidak relevan di sini, tapi konsistensi) |
| AP-5 | Menulis remediation guidance tanpa effort estimate | tidak bisa dijadwalkan; tidak actionable |
| AP-6 | Melaporkan CVSS base score sebagai risk final di executive summary | mengaburkan prioritas |
| AP-7 | Redaksi yang menghapus jejak (tanpa penanda) | auditor tidak tahu data disensor |
| AP-8 | Dashboard dengan metrik tanpa definisi | angka ambigu; tidak bisa diaudit |
| AP-9 | Menulis glosarium KPI di dua tempat | dua sumber kebenaran; drift |
| AP-10 | Eskalasi tanpa pemilik dan tenggat | temuan menggantung |

---

## 13. Kriteria Penerimaan

### 13.1 Struktural

- `reporting.md` ≤ 80 baris; memuat prinsip, peta audiens, index ke 8 berkas, best practices; tanpa template laporan lengkap.
- 8 berkas baru ada, masing-masing ber-frontmatter `name`/`description`/`tags` dan diakhiri Best Practices.
- Setiap berkas baru muncul tepat sekali di `SKILL.md` (Reference Documentation + Progressive Disclosure).
- `SKILL.md` Capability Map memecah baris "Pelaporan" menjadi sub-kapabilitas yang menaut ke 8 berkas.
- Total referensi = 17 (9 lama + 8 baru); `reporting.md` tetap ada.
- `node scripts/sync-skills.js` memperbarui `manifest.json`, `skills/index.json`, plugin.
- `docs/SKILL-QUALITY.md` diperbarui (jumlah referensi 9 → 17).
- `CHANGELOG.md` memuat entri perubahan.
- `grep` pola materi ujian (§2 PERSONA-INJECTION-NEEDS) di `skills/vulnerability-assessment/references/reporting*.md`, `risk-communication.md`, `trend-diff-reporting.md`, `dashboard-design.md`, `false-positive-communication.md` = 0 hasil.

### 13.2 Perilaku (8 skenario uji)

| # | Prompt | Perilaku yang diharapkan |
|---|---|---|
| 1 | "Buat executive summary untuk manajemen" | ringkas 1 halaman, bahasa risiko bisnis, hitungan per severity, top 3 prioritas, tanpa jargon CVE mentah |
| 2 | "Tulis laporan teknis temuan SQLi" | reproducible (URL/param/perintah/respons), bukti diredaksi, cakupan auth disebut |
| 3 | "Map temuan ke PCI DSS dan ISO 27001" | tabel mapping + bukti + status compliance |
| 4 | "Berikan remediation guidance dengan effort" | instruksi actionable + effort S/M/L + tenggat + pemilik |
| 5 | "Jelaskan CVSS 9.8 ke direksi" | bahasa risiko, kalibrasi, "so what", tanpa inflasi |
| 6 | "Buat trend report MoM" | definisi metrik stabil, formula, contoh, glosarium |
| 7 | "Komunikasikan false positive ke klien" | protokol, transparansi, menjaga kredibilitas |
| 8 | "Buat dashboard VA" | KPI inti dengan definisi + sumber + layout |

Lulus bila: persona konsisten, struktur jawaban ringkas → alasan → langkah → bukti → risiko, tidak ada fakta karangan, dan setiap laporan punya audiens yang jelas.

---

## 14. Keputusan yang Perlu Disetujui

| ID | Keputusan | Pilihan | Rekomendasi |
|---|---|---|---|
| D1 | Nama 8 berkas baru | sesuai brainstorm / disesuaikan | **sesuai brainstorm** (konsisten dengan daftar yang sudah disepakati) |
| D2 | Presentasi ke manajemen | masuk `reporting-executive.md` / berkas terpisah `reporting-presentation.md` | **masuk `reporting-executive.md`** (menghindari 9 berkas; presentasi adalah eksekusi executive summary) |
| D3 | Redaksi bukti | masuk `reporting-technical.md` / berkas terpisah `evidence-handling.md` | **masuk `reporting-technical.md`** (redaksi adalah bagian dari laporan teknis) |
| D4 | Versioning & change control | masuk `reporting-compliance.md` / `reporting.md` overview | **masuk `reporting-compliance.md`** (versioning adalah kebutuhan audit) |
| D5 | Glosarium KPI | di `trend-diff-reporting.md` / `dashboard-design.md` | **di `trend-diff-reporting.md`** (satu sumber kebenaran; dashboard merujuk) |
| D6 | Eskalasi & exception | di `risk-communication.md` / `false-positive-communication.md` | **di `risk-communication.md`** (eskalasi adalah komunikasi risiko); FP-eskalasi di `false-positive-communication.md` merujuk |
| D7 | Audience tailoring | di `reporting.md` overview / berkas terpisah | **di `reporting.md` overview** (peta audiens adalah fungsi index) |
| D8 | Jumlah berkas | 8 (sesuai brainstorm) / kurang/lebih | **8** (sesuai brainstorm; setiap domain komunikasi punya berkas sendiri) |

---

## 15. Rencana Implementasi (bila disetujui)

1. **Fase A — refactor overview:** ubah `reporting.md` menjadi overview + index (≤ 80 baris); tambah peta audiens.
2. **Fase B — eksekutif & teknis:** tulis `reporting-executive.md`, `reporting-technical.md`.
3. **Fase C — compliance & remediasi:** tulis `reporting-compliance.md`, `reporting-remediation.md`.
4. **Fase D — komunikasi & trend:** tulis `risk-communication.md`, `trend-diff-reporting.md`.
5. **Fase E — dashboard & FP:** tulis `dashboard-design.md`, `false-positive-communication.md`.
6. **Fase F — integrasi:** perbarui `SKILL.md` (Capability Map, Reference Documentation, Progressive Disclosure); `docs/SKILL-QUALITY.md`; `CHANGELOG.md`.
7. **Fase G — verifikasi:** `node scripts/sync-skills.js`, `node scripts/check-changelog.js`, uji indeks 1:1, grep pola ujian, jalankan 8 skenario uji.

---

## 16. Metrik

| Metrik | Kondisi awal (2026-11-14) | Target |
|---|---|---|
| Jumlah berkas referensi VA | 9 | 17 |
| Baris `reporting.md` | 114 | ≤ 80 (overview) |
| Topik brainstorm yang tercakup | 3/15 (template saja) | 15/15 |
| Berkas yatim | 0 | 0 |
| Indeks 1:1 | ya | ya |
| Skenario uji lulus | belum diuji | 8/8 |
| Pola materi ujian di berkas reporting | 0 | 0 |

---

## 17. Lampiran — Log Sumber

| Sumber | Yang diambil | Status |
|---|---|---|
| `skills/vulnerability-assessment/references/reporting.md` | struktur laporan teknis/manajemen/compliance, best practices | dibaca 2026-11-14 |
| `skills/vulnerability-assessment/SKILL.md` | capability map, indeks referensi, gotchas | dibaca 2026-11-14 |
| `skills/vulnerability-assessment/references/remediation-verification.md` | tracking, re-scan, accepted risk | dibaca 2026-11-14 |
| `skills/security-documentation/SKILL.md` + `references/finding-writeup.md` | anatomi temuan, redaksi dasar | dibaca 2026-11-14 |
| `skills/wazuh/references/reporting-and-handover.md` | laporan triase, redaksi | dibaca 2026-11-14 |
| `docs/PERSONA-INJECTION-NEEDS.md` | format analisis kebutuhan, FR/NFR/AP | dibaca 2026-11-14 |
| `docs/PUBLISHING-NEEDS.md` | format, ruang lingkup, kriteria penerimaan | dibaca 2026-11-14 |
| `docs/CND-PERSONA-NEEDS.md` | format, arsitektur referensi usulan | dibaca 2026-11-14 |
| subagent `brainstorm-va-reporting` | 15 topik, 8 berkas baru, 14 gotchas | ringkasan diterima 2026-11-14 |
