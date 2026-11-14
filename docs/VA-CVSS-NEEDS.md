# Analisis Kebutuhan — Aspek CVSS Scoring & Risk Quantification pada Vulnerability Assessment

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-14
**Pertanyaan yang dijawab:** apa yang dibutuhkan agar skill `vulnerability-assessment` mencakup aspek CVSS scoring & risk quantification secara memadai — pemilihan versi CVSS, kalkulasi environmental/temporal/supplemental, integrasi EPSS & CISA KEV & threat intel, asset criticality, risk acceptance, alternative scoring, konsistensi skor, scoring temuan tanpa CVE, agregasi portfolio risk, reprodusibilitas & validasi (vector string), serta time decay & re-scoring — tanpa merusak persona praktisi yang sudah ada; bagaimana membaginya ke berkas referensi baru dan perluasan berkas existing; serta bagaimana menjaga konsistensi dengan SKILL.md, Capability Map, dan Gotchas yang sudah ada.
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md), [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md)
**Acuan konten:** [skills/vulnerability-assessment/SKILL.md](../skills/vulnerability-assessment/SKILL.md), `skills/vulnerability-assessment/references/*`, hasil brainstorming topik CVSS scoring & risk quantification (15 topik, 5 berkas baru, 2 berkas existing yang diperluas, 14 gotchas)

---

## 1. Ringkasan

Skill `vulnerability-assessment` saat ini menyediakan dasar CVSS yang cukup untuk VA tradisional: tabel metrik v3.1, severity rating, environmental score secara ringkas, perubahan v4.0, threat metrics, contextual scoring, serta matriks prioritisasi berbasis risiko dengan integrasi threat intel (EPSS, CISA KEV) secara singkat. Namun aspek **CVSS scoring & risk quantification mendalam** belum operasional: tidak ada kalkulasi environmental/temporal yang langkah-demi-langkah, tidak ada panduan pemilihan versi v3.1 vs v4.0 per engagement, tidak ada integrasi EPSS/KEV/threat intel yang terstruktur (skala, batasan, cara kombinasi), tidak ada rubrik asset criticality yang reproducible, tidak ada kriteria risk acceptance yang terdokumentasi, tidak ada alternative scoring (OWASP/DREAD/FAIR) dengan perbandingan, tidak ada mekanisme konsistensi/calibration antar analis, tidak ada rubrik untuk scoring temuan tanpa CVE, tidak ada agregasi portfolio risk, tidak ada validasi vector string, dan tidak ada time decay & re-scoring.

Akibatnya, ketika pengguna meminta scoring atau risk quantification yang serius, agent persona VA harus mengarang angka, mencampur versi CVSS, atau memberi skor "perasaan" — bertentangan dengan kontrak persona (bukti, tidak mengarang) dan dengan prinsip "keputusan scoping, triase, dan prioritisasi" yang menjadi nilai skill ini. Yang belum ada di repo: **definisi operasional** tentang bagaimana skor CVSS dihitung, dikontekstualisasikan, divalidasi, diagregasi, dan dipelihara sepanjang waktu, serta **struktur berkas** yang menampungnya tanpa merusak persona inti.

Yang dibutuhkan: **perluasan terstruktur** yang menambah kapabilitas CVSS scoring & risk quantification tanpa mengubah persona inti, tanpa menggandakan konten yang sudah ada, dan tanpa melanggar batas skill (VA berhenti di identifikasi & pelaporan; bukan eksploitasi, bukan GRC penuh). Hasilnya adalah **5 berkas referensi baru** + **perluasan 2 berkas existing**, dengan **14 gotchas scoring**, pembaruan SKILL.md (Capability Map, Reference Documentation, Progressive Disclosure, Gotchas, Decision Frame), dan verifikasi mesin.

Dokumen ini **hanya analisis kebutuhan**. Tidak ada berkas referensi yang dibuat atau diubah oleh dokumen ini.

---

## 2. Temuan (bukti kondisi saat ini)

Diukur 2026-11-14 terhadap `skills/vulnerability-assessment/`.

| # | Temuan | Lokasi | Akibat |
|---|---|---|---|
| T1 | CVSS v3.1 hanya tabel metrik + severity; tidak ada langkah perhitungan base/environmental/temporal | `references/cvss-scoring.md` §"CVSS v3.1" | Agent tidak bisa menghitung skor secara reproducible |
| T2 | Environmental score hanya 3 butir ringkas (Modified AV, Modified Scope, CIA Requirement) tanpa kalkulasi & rubrik | `references/cvss-scoring.md` §"Environmental Score" | Skor kontekstual diisi asal, tidak reproducible |
| T3 | v4.0 hanya tabel perubahan + Threat Metrics singkat; tidak ada supplemental metrics & kalkulasi | `references/cvss-scoring.md` §"CVSS v4.0" | v4.0 tidak bisa dipakai operasional |
| T4 | Tidak ada panduan pemilihan versi v3.1 vs v4.0 per engagement/program | `references/cvss-scoring.md`, `SKILL.md` | Campur versi tanpa label → prioritas membingungkan |
| T5 | Contextual scoring hanya daftar faktor peningkat/penurun + 3 contoh; tidak ada rubrik/ambang | `references/cvss-scoring.md` §"Contextual Scoring" | Keputusan prioritas tidak terukur |
| T6 | EPSS, CISA KEV, threat intel hanya 4 baris di `prioritization.md`; tidak ada skala, batasan, cara kombinasi | `references/prioritization.md` §"Threat Intelligence Integration" | Integrasi threat intel tidak operasional |
| T7 | Asset criticality hanya "Tier 1/3" di matriks; tidak ada rubrik tier & business impact | `references/prioritization.md` §"Matriks Prioritisasi" | Asset criticality subjektif, tidak reproducible |
| T8 | Risk acceptance hanya satu baris ("Accept risk + dokumentasikan") tanpa kriteria/owner/expiry | `references/prioritization.md` §"Prioritisasi Remediasi" | Temuan "diterima" bisa hilang tanpa jejak |
| T9 | Tidak ada alternative scoring (OWASP/DREAD/FAIR) maupun kapan dipakai | seluruh skill | Tidak bisa membandingkan metodologi |
| T10 | Tidak ada mekanisme konsistensi/calibration antar analis | seluruh skill | Skor berbeda antar analis → "score inflation" |
| T11 | Tidak ada rubrik untuk scoring temuan tanpa CVE (misconfig, config weakness) | seluruh skill | Agent mengarang "CVSS" untuk misconfig |
| T12 | Tidak ada agregasi & portfolio risk (cara menggabungkan banyak temuan) | seluruh skill | Rata-rata CVSS menyesatkan |
| T13 | Tidak ada validasi vector string & reprodusibilitas skor | seluruh skill | Skor tidak bisa diaudit/ulang |
| T14 | Tidak ada time decay & re-scoring (skor statis) | seluruh skill | Temuan lama dengan exploit baru tidak naik prioritas |
| T15 | SKILL.md Capability Map & Progressive Disclosure tidak punya entri scoring mendalam | `SKILL.md` | Berkas baru akan "yatim" jika tidak didaftarkan |
| T16 | Gotchas SKILL.md (10 butir) tidak memuat gotcha khas scoring | `SKILL.md` §Gotchas | Risiko scoring tidak diingatkan |
| T17 | Decision Frame butir 4 hanya "CVSS saja atau konteks bisnis?" tanpa ambang scoring | `SKILL.md` §Decision Frame | Keputusan scoring diambil tanpa ambang |

### Mekanisme yang teramati (bukan asumsi)

1. Skill ini adalah **persona**, bukan katalog: setiap penambahan materi harus masuk ke Decision Frame / Gotchas / contoh penalaran, bukan hanya daftar istilah. (Lihat `PERSONA-INJECTION-NEEDS.md` §4, komponen 5–8.)
2. Pola penamaan berkas referensi: `kebab-case.md`, frontmatter YAML 3 field (`name`, `description`, `tags`), ending "Best Practices" bila berlaku. (`AGENTS.md` §Reference File Conventions.)
3. `SKILL.md` batas keras 450 baris; kelebihan materi dipindahkan ke `references/`. (NFR-1 pada `PERSONA-INJECTION-NEEDS.md` §7.)
4. Setiap berkas `references/` muncul tepat sekali di Reference Documentation; tidak ada berkas yatim. (NFR-2.)
5. Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`). (NFR-3.)
6. Scoring yang baik selalu memisahkan **base**, **environmental**, **temporal/threat**, dan **supplemental** score; mencampurnya merusak prioritas. (Prinsip CVSS; lihat `cvss-scoring.md` §"Contextual Scoring".)
7. Vector string adalah **satu-satunya** representasi skor yang reproducible; skor tanpa vector string tidak bisa diaudit. (Prinsip reprodusibilitas.)

---

## 3. Definisi

**CVSS (Common Vulnerability Scoring System)** — standar terbuka untuk memberi skor severity teknis kerentanan (0.0–10.0), dipakai sebagai titik awal prioritas, bukan keputusan akhir.

**Base score** — skor intrinsik kerentanan yang tidak berubah antar lingkungan: Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope/Subsequent System Impact, CIA Impact.

**Environmental score** — penyesuaian base score dengan konteks lokal: modified metrics dan requirement level (CIA Requirement), mencerminkan dampak pada sistem spesifik.

**Temporal score (v3.1)** — penyesuaian base/environmental dengan ketersediaan exploit & remediasi: Exploit Code Maturity, Remediation Level, Report Confidence.

**Threat metrics (v4.0)** — pengganti temporal score di v4.0: Exploit Maturity (dan metrik ancaman lain), mengukur keberadaan exploit di wild.

**Supplemental metrics (v4.0)** — metrik tambahan v4.0 yang tidak memengaruhi skor numerik tetapi memperkaya konteks: Safety, Automatable, Recovery, Value Density, Vulnerability Response Effort, Provider Urgency.

**EPSS (Exploit Prediction Scoring System)** — probabilitas (0.0–1.0) bahwa sebuah CVE akan dieksploitasi dalam 30 hari ke depan. Pelengkap CVSS, bukan pengganti.

**CISA KEV (Known Exploited Vulnerabilities)** — katalog CVE yang terbukti dieksploitasi di wild. Sinyal prioritas tinggi; keberadaan di KEV menaikkan prioritas.

**Asset criticality** — tingkat kepentingan aset bagi bisnis (Tier 1/2/3) berdasarkan data yang diproses, dampak downtime, dan eksposur.

**Risk acceptance** — keputusan terdokumentasi untuk menerima risiko temuan (dengan owner, alasan, tanggal, dan tanggal review ulang), bukan pengabaian.

**Alternative scoring** — metodologi selain CVSS: OWASP Risk Rating, DREAD, FAIR. Dipakai untuk konteks spesifik (mis. risiko bisnis, aplikasi web) dengan justifikasi.

**Calibration (scoring consistency)** — proses menyelaraskan skor antar analis melalui rubrik, contoh, dan sesi kalibrasi, agar skor reproducible.

**Scoring temuan tanpa CVE** — pemberian skor pada misconfiguration/config weakness yang tidak punya CVE, memakai rubrik internal (bukan CVSS palsu).

**Vector string** — representasi tekstual metrik CVSS (mis. `CVSS:3.1/AV:N/AC:L/...`) yang menjadi satu-satunya bentuk skor yang reproducible dan validatable.

**Time decay** — penurunan/kenaikan prioritas temuan seiring waktu (exploit baru, patch tersedia, mitigasi diterapkan) yang menuntut re-scoring periodik.

**Agregasi & portfolio risk** — cara menggabungkan banyak temuan menjadi gambaran risiko keseluruhan (bukan rata-rata CVSS), mempertimbangkan jumlah, severity, asset exposure, dan korelasi.

**Reprodusibilitas & validasi skor** — kemampuan orang lain mengulang perhitungan skor dari vector string + konteks dan mendapat hasil sama, dengan audit trail.

---

## 4. Ruang lingkup

**Termasuk:**
- Metodologi CVSS scoring mendalam: pemilihan versi, base/environmental/temporal/threat/supplemental, contextual scoring dengan rubrik.
- Integrasi EPSS, CISA KEV, dan threat intel lain (Exploit-DB, Metasploit, vendor advisory) sebagai sinyal prioritas.
- Asset criticality scoring dengan rubrik tier & business impact.
- Risk acceptance criteria (kapan boleh accept, owner, expiry, review).
- Alternative scoring (OWASP/DREAD/FAIR) dengan perbandingan & kapan dipakai.
- Scoring consistency/calibration antar analis.
- Rubrik scoring temuan tanpa CVE (misconfig, config weakness).
- Agregasi & portfolio risk (bukan rata-rata CVSS).
- Reprodusibilitas & validasi skor (vector string, kalkulator, audit trail).
- Time decay & re-scoring periodik.
- Pembaruan SKILL.md (Capability Map, Reference Documentation, Progressive Disclosure, Gotchas, Decision Frame) agar 5 berkas baru tidak yatim.
- Pembaruan 2 berkas existing untuk menyerap topik scoring yang relevan.

**Tidak termasuk:**
- Implementasi berkas referensi (dokumen ini hanya analisis).
- Eksploitasi / red team (di luar batas VA; rujuk `ptes-standard`/`offsec-*`).
- GRC/audit kepatuhan penuh (rujuk `security-auditor`); risk acceptance di sini adalah keputusan teknis VA, bukan kepatuhan.
- Penulisan kalkulator CVSS sendiri — gunakan kalkulator resmi (FIRST) untuk validasi.
- Perubahan persona inti (profil, kontrak 6 butir, decision frame 7 butir yang ada tetap berlaku; hanya ditambah butir scoring-specific).

---

## 5. Topik & pemetaan ke berkas (brainstorming)

15 topik brainstorming dipetakan ke 5 berkas baru + 2 berkas existing. Satu topik boleh menyentuh beberapa berkas, tetapi **satu berkas adalah rumah utama** tiap topik agar tidak duplikat. (Acuan: output subagent `brainstorm-cvss-scoring`.)

| # | Nama Topik | Deskripsi (ringkas) | Prioritas | Penempatan |
|---|---|---|---|---|
| 1 | Pemilihan Versi CVSS: v3.1 vs v4.0 | v3.1 masih dominan di NVD/scanner; v4.0 menambah Threat Metrics, Supplemental Metrics, mengganti Scope. Pakai v3.1 untuk kompatibilitas toolchain lama, v4.0 bila pipeline siap dan butuh sinyal ancaman terintegrasi. Jangan campur versi tanpa normalisasi eksplisit. | High | `cvss-environmental-temporal.md` (rumah utama) |
| 2 | Kalkulasi Environmental Score Mendalam | Modified AV/AC/PR/UI/S/C/I/A + CIA Requirements (Low/Medium/High). Hitung dengan mengganti metrik base yang tidak relevan lalu terapkan requirement; dokumentasikan setiap modifikasi. Jangan ubah base score asli—laporkan base & environmental terpisah. | High | `cvss-environmental-temporal.md` |
| 3 | Temporal Score (v3.1) & Threat Metrics (v4.0) | Temporal v3.1 (ECM, RL, RC) menurunkan skor seiring mitigasi; v4.0 menggantinya dengan Threat Metrics (Exploit Maturity) yang lebih sederhana. Gunakan temporal untuk laporan "hidup", threat metrics untuk adopsi v4.0. | High | `cvss-environmental-temporal.md` |
| 4 | Integrasi EPSS (Probabilitas Eksploitasi) | EPSS memberi probabilitas eksploitasi 30 hari (0–1); gunakan sebagai pengali/penambah prioritas, bukan pengganti CVSS. CVSS tinggi + EPSS tinggi = prioritas tertinggi; EPSS >0.5/top persentil = eskalasi. Perhatikan staleness & bias CVE lama. | High | `epss-kev-integration.md` |
| 5 | Integrasi CISA KEV (Known Exploited = Auto-Critical) | CVE di KEV = dieksploitasi di wild; perlakukan auto-Critical dengan SLA ketat. Cek KEV otomatis (API/feed) saat triase; catat due date, ransomware association, required action. Verifikasi applicability produk/versi. | High | `epss-kev-integration.md` |
| 6 | Asset Criticality Scoring (Bisnis, Data, Availability) | Model tiering (Tier 1: payment, PII, DC; Tier 2: internal business; Tier 3: dev/test) dengan rubrik: sensitivitas data, availability (RTO/RPO), regulasi, dampak revenue. Skor aset jadi pengali risiko. Dokumentasikan owner & review tahunan; hindari "semua Tier 1". | High | `asset-criticality-scoring.md` |
| 7 | Threat Intelligence Integration (Exploit, APT, Ransomware) | Selain KEV/EPSS: ketersediaan exploit (Metasploit/ExploitDB), targeting APT (campaign, sektor), asosiasi ransomware. Sinyal prioritas & input mitigasi. Verifikasi sumber TI (TLP, freshness); jangan over-rely satu feed. | Medium | `epss-kev-integration.md` |
| 8 | Risk Acceptance Criteria (Accept, Dokumentasi, Review Cycle) | Kriteria accept risk (Low/Info pada aset non-kritis, tidak ada exploit, kontrol kompensasi) plus proses: alasan, pemilik risiko, tanggal review, kompensasi. Acceptance bukan penutupan—review berkala. Tolak acceptance untuk Critical/High atau aset kritis tanpa eskalasi. | Medium | `risk-acceptance-and-alternatives.md` |
| 9 | Alternative Scoring (OWASP, DREAD, FAIR, Custom Matrix) | Alternatif untuk konteks bisnis: OWASP Risk Rating (Likelihood×Impact), DREAD (5 faktor), FAIR (kuantitatif $ loss). CVSS untuk severity teknis, alternatif untuk risk bisnis/komunikasi eksekutif. Definisikan kapan pakai yang mana; hindari pencampuran tanpa mapping. | Medium | `risk-acceptance-and-alternatives.md` |
| 10 | Scoring Consistency (Inter-analyst & Calibration) | Rubrik terstandar, contoh anchor (calibration cases), review silang; calibration session berkala; ukur agreement (Cohen's kappa) pada subset temuan. Dokumentasikan keputusan borderline & decision log. | Medium | `scoring-consistency.md` |
| 11 | CVSS v4.0 Supplemental Metrics | Supplemental metrics (Automatable, Recovery, Value Density, Vulnerability Response Effort, Provider Urgency) menambah konteks operasional tanpa mengubah base score. Pakai untuk perencanaan remediasi/kapasitas, bukan severity. Pastikan tool mendukung sebelum adopsi. | Medium | `cvss-environmental-temporal.md` |
| 12 | Scoring Temuan Tanpa CVE | Untuk misconfig, missing patch generik, kerentanan kustom: petakan ke CVSS metric manual atau gunakan risk matrix internal; jangan paksa CVE. Dokumentasikan asumsi & sumber (CWE, vendor advisory). Pertimbangkan CWE + scoring "environmental-style". | Medium | `cvss-environmental-temporal.md` |
| 13 | Agregasi & Portfolio Risk | Agregasikan per aset/bisnis unit untuk risiko kumulatif; akumulasi Low/Medium bisa jadi High. Top-N risk & heat map; prioritaskan remediasi yang menutup banyak temuan (patch OS). Laporkan tren, bukan snapshot. | Medium | `risk-acceptance-and-alternatives.md` |
| 14 | Reprodusibilitas & Validasi Skor (Vector String) | Simpan CVSS vector string lengkap per temuan agar reproducible & auditable; validasi dengan calculator resmi. Bandingkan skor scanner vs manual vs NVD/vendor; selisih besar = triase ulang. Jangan laporkan skor tanpa vector. | Medium | `cvss-environmental-temporal.md` |
| 15 | Time Decay & Re-scoring | Skor/prioritas berubah seiring ancaman (exploit baru, patch, KEV). Jadwalkan re-scoring berkala (bulanan/kuartalan) dan trigger re-scoring saat KEV/EPSS berubah atau patch dirilis. Pertahankan riwayat skor untuk audit. | Low | `risk-acceptance-and-alternatives.md` |

---

## 6. Rekomendasi struktur berkas referensi

(Acuan: output subagent `brainstorm-cvss-scoring`.)

| Nama File | Isi (sections) | Topik yang dicakup |
|---|---|---|
| `cvss-environmental-temporal.md` | Environmental calculation step-by-step (modified metrics, security requirements, contoh perhitungan); Temporal score v3.1 (E/RL/RC tabel nilai); v4.0 Threat Metrics; Vector string & reproducibility; Supplemental Metrics; Scoring temuan tanpa CVE; Pemilihan versi v3.1 vs v4.0 | 1, 2, 3, 11, 12, 14 |
| `epss-kev-integration.md` | EPSS deep dive (API, interpretasi, kombinasi dengan CVSS, staleness); KEV integration (auto-Critical, due date, applicability); Threat intel (exploit availability, APT, ransomware); sumber & TLP | 4, 5, 7 |
| `asset-criticality-scoring.md` | Model tiering; rubrik data sensitivity; availability requirement (RTO/RPO); business impact; pengali risiko; owner & review; anti-pattern "semua Tier 1" | 6 |
| `risk-acceptance-and-alternatives.md` | Risk acceptance criteria & proses; dokumentasi & review cycle; compensating controls; Alternative scoring (OWASP/DREAD/FAIR/custom matrix) dengan mapping ke CVSS; Agregasi & portfolio risk; Time decay & re-scoring | 8, 9, 13, 15 |
| `scoring-consistency.md` | Rubrik terstandar; calibration cases (anchor examples); inter-analyst agreement (Cohen's kappa); QA review; decision log; governance (who approves, audit trail) | 10 |

### Perubahan pada berkas existing

- `cvss-scoring.md`: pertahankan base metrics & severity rating sebagai entry point; tambah pointer/summary ke berkas baru; tambah section "Kapan pakai v3.1 vs v4.0 (ringkas)" + link ke `cvss-environmental-temporal.md`.
- `prioritization.md`: pertahankan matriks & SLA; tambah pointer ke `epss-kev-integration.md`, `asset-criticality-scoring.md`, `risk-acceptance-and-alternatives.md`; tambah baris "Risk acceptance → lihat risk-acceptance-and-alternatives.md".

### Frontmatter contoh (acuan)

```yaml
---
name: "Environmental & Temporal CVSS Scoring"
description: "Kalkulasi environmental/temporal score CVSS, threat metrics v4.0, vector string, supplemental metrics, dan scoring temuan tanpa CVE."
tags: [cvss, environmental, temporal, v3.1, v4.0, vector, supplemental]
---
```

---

## 7. Kebutuhan fungsional

### 7.1 Kebutuhan inti (skill-level)

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | Memuat skill mengaktifkan persona VA yang **juga** mampu melakukan CVSS scoring & risk quantification tanpa kehilangan suara praktisi | Jawaban scoring memakai struktur ringkas → alasan → langkah → bukti → risiko; menyebut ketidakpastian |
| FR-2 | Scoring diperlakukan sebagai **kapabilitas**, bukan skill terpisah: satu persona, satu siklus, kapabilitas tambahan | Tidak ada persona kedua; `SKILL.md` tetap satu skill |
| FR-3 | Setiap skor harus **reproducible**: versi CVSS, vector string, metrik, konteks, sumber threat intel, tanggal | Format skor di berkas scoring mencakup field wajib |
| FR-4 | Memisahkan **base**, **environmental**, **temporal/threat**, dan **supplemental** score; tidak mencampur | `cvss-environmental-temporal.md` punya bagian terpisah per jenis skor |
| FR-5 | Pemilihan versi CVSS (v3.1 vs v4.0) dilakukan **eksplisit** dan konsisten per engagement/program, dengan justifikasi | `cvss-scoring.md` + `cvss-environmental-temporal.md` punya matriks keputusan + aturan konsistensi |
| FR-6 | Environmental score dihitung dengan **rubrik** (modified metrics + CIA Requirement), bukan asal | `cvss-environmental-temporal.md` punya langkah & rubrik |
| FR-7 | Threat intel (EPSS, KEV, Exploit-DB, vendor advisory) diintegrasikan sebagai **sinyal**, bukan pengganti CVSS | `epss-kev-integration.md` punya cara kombinasi & batasan |
| FR-8 | Asset criticality punya **rubrik tier & business impact** yang reproducible | `asset-criticality-scoring.md` punya rubrik + contoh |
| FR-9 | Risk acceptance **terdokumentasi** dengan owner, alasan, tanggal, tanggal review ulang | `risk-acceptance-and-alternatives.md` punya template/kriteria |
| FR-10 | Alternative scoring (OWASP/DREAD/FAIR) hanya dipakai dengan **justifikasi & normalisasi** | `risk-acceptance-and-alternatives.md` punya perbandingan & kapan dipakai |
| FR-11 | Scoring temuan tanpa CVE memakai **rubrik internal**, bukan CVSS palsu | `cvss-environmental-temporal.md` punya rubrik + mapping |
| FR-12 | Konsistensi antar analis (**calibration**) wajib: rubrik, contoh, sesi kalibrasi | `scoring-consistency.md` punya mekanisme calibration |
| FR-13 | Agregasi portfolio risk **tidak** memakai rata-rata CVSS buta; mempertimbangkan jumlah, severity, exposure, korelasi | `risk-acceptance-and-alternatives.md` punya metode agregasi |
| FR-14 | Time decay & re-scoring periodik: skor tidak statis; trigger re-score eksplisit | `risk-acceptance-and-alternatives.md` punya model decay & trigger |
| FR-15 | Vector string **divalidasi** dengan kalkulator resmi; skor tanpa vector string tidak dianggap valid | `cvss-environmental-temporal.md` punya prosedur validasi |
| FR-16 | `SKILL.md` diperbarui: Capability Map, Reference Documentation, Progressive Disclosure, Gotchas, Decision Frame — sehingga 5 berkas baru tidak yatim | Indeks 1:1 (NFR-2) |
| FR-17 | Tidak ada **materi ujian / sertifikasi** yang masuk (konsisten dengan `PERSONA-INJECTION-NEEDS.md` FR-8) | grep pola ujian = 0 hasil termasuk URL |
| FR-18 | Nol **duplikasi** konten yang sudah ada di 2 berkas existing — perluasan hanya menambah bagian scoring mendalam, cross-reference ke berkas baru | Review diff: tidak ada paragraf yang disalin utuh |
| FR-19 | Setiap berkas baru punya frontmatter 3 field + ending "Best Practices" (bila berlaku) | Validasi frontmatter |
| FR-20 | Persona tetap **menolak** overclaim (mengarang CVE/angka) dan eksploitasi, meski dalam scoring | Minimal satu contoh penolakan scoring di contoh penalaran |

### 7.2 Keterbatasan yang diterima (LI-N)

| ID | Keterbatasan | Mengapa diterima |
|---|---|---|
| LI-1 | Tidak membuat kalkulator CVSS sendiri — gunakan kalkulator resmi FIRST untuk validasi | Menulis kalkulator sendiri berisiko salah rumus; validasi cukup |
| LI-2 | Tidak memaksakan satu versi CVSS untuk semua klien — pilih per engagement/program | Klien/toolchain berbeda; konsistensi per program lebih penting |
| LI-3 | Tidak menjanjikan skor "pasti" — selalu ada ketidakpastian & asumsi | CVSS adalah estimasi; overclaim merusak kredibilitas |
| LI-4 | Tidak menggantikan GRC/audit kepatuhan penuh | Batas skill VA; rujuk `security-auditor` |
| LI-5 | Tidak menjamin kesegaran feed TI (EPSS/KEV) — verifikasi freshness | Feed dikelola pihak ketiga; kita hanya mengonsumsi |
| LI-6 | Supplemental metrics (v4.0) tidak mengubah severity numerik | Sesuai spesifikasi CVSS v4.0 |

---

## 8. Kebutuhan non-fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| NFR-1 | `SKILL.md` tetap ≤ 450 baris; materi scoring detail di `references/`, bukan di SKILL.md | hitung baris |
| NFR-2 | Setiap berkas `references/` (termasuk 5 baru) muncul tepat sekali di Reference Documentation & Capability Map | paritas tabel |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa `docs/`) | cek tautan relatif |
| NFR-4 | Bahasa Indonesia + istilah teknis Inggris; kode/komentar Inggris | review |
| NFR-5 | Frontmatter 3 field pada setiap berkas baru | validasi |
| NFR-6 | Tidak ada berkas yatim (semua terdaftar) | cek 1:1 |
| NFR-7 | Verifikasi mesin: grep pola ujian = 0; hitung baris; resolusi tautan; paritas tabel | skrip/check manual |
| NFR-8 | Tidak mengubah persona inti (profil, kontrak 6 butir, decision frame 7 butir yang ada tetap; hanya tambah butir scoring-specific bila perlu) | diff review |
| NFR-9 | Tidak ada duplikasi konten antar berkas (cross-reference, bukan salin) | review |
| NFR-10 | Setiap penghapusan/perubahan berkas tercatat di `CHANGELOG.md` | aturan repo |

---

## 9. Antipattern (yang dilarang)

| ID | Antipattern | Mengapa salah |
|---|---|---|
| AP-1 | Membuat skill scoring terpisah (`cvss-scoring-assessment`) | Memecah persona; duplikasi siklus VA; pengguna harus memilih skill |
| AP-2 | Menyalin output kalkulator CVSS tanpa konteks | Skor tanpa konteks = prioritas salah; melanggar kontrak (bukti) |
| AP-3 | Mencampur v3.1 dan v4.0 tanpa label versi | Prioritas membingungkan; tidak reproducible |
| AP-4 | Menggunakan EPSS sebagai pengganti CVSS | EPSS adalah probabilitas exploit, bukan severity teknis; keduanya saling melengkapi |
| AP-5 | Mengklaim absence di CISA KEV = aman | KEV hanya mencakup CVE yang dieksploitasi di wild; tidak ada di KEV bukan berarti tidak berisiko |
| AP-6 | Mengisi environmental score tanpa rubrik | Skor kontekstual subjektif; tidak reproducible |
| AP-7 | Menggunakan rata-rata CVSS untuk portfolio risk | Menyembunyikan temuan kritis; agregasi harus mempertimbangkan jumlah/severity/exposure/korelasi |
| AP-8 | Membuat "CVSS palsu" untuk misconfig tanpa rubrik | Menyesatkan; gunakan rubrik internal band Low/Med/High/Critical |
| AP-9 | Risk acceptance tanpa owner, expiry, dan review | Temuan "diterima" hilang tanpa jejak; audit gagal |
| AP-10 | Scoring by gut feel tanpa calibration | Skor berbeda antar analis; "score inflation" |

---

## 10. Gotchas (14) — khas CVSS scoring & risk quantification

(Acuan: output subagent `brainstorm-cvss-scoring`.)

1. Mencampur v3.1 dan v4.0 dalam satu laporan tanpa normalisasi membuat skor tidak comparable; pilih satu versi per laporan atau sediakan mapping eksplisit.
2. Mengubah base score "karena konteks" tanpa menyimpan vector string dan alasan → audit gagal dan skor tidak reproducible.
3. Environmental score dihitung tapi tidak dilaporkan → kehilangan konteks lokal; selalu laporkan base dan environmental terpisah.
4. EPSS rendah diartikan "aman" → false security; EPSS hanya probabilitas 30 hari dan tidak mengukur dampak.
5. KEV dianggap berlaku untuk semua versi produk → false positive; selalu cek applicability (vendor, versi, konfigurasi).
6. Asset criticality "semua Tier 1" → prioritas tidak bermakna; paksa distribusi dan review tahunan.
7. Temporal score tidak diperbarui setelah patch → skor stale dan prioritas ketinggalan.
8. Variasi antar analis besar karena tidak ada anchor examples → lakukan calibration session dan simpan decision log.
9. Agregasi Low yang menumpuk tidak dilaporkan → risiko kumulatif tersembunyi; tampilkan top-N dan tren.
10. Re-scoring tidak dijadwalkan → prioritas ketinggalan threat landscape (exploit baru, KEV baru).
11. Scoring temuan tanpa CVE dipaksakan ke CVE terdekat → skor menyesatkan; gunakan risk matrix internal + dokumentasikan asumsi.
12. Supplemental metrics (v4.0) dianggap mengubah severity → salah interpretasi; ia hanya konteks operasional/remediasi.
13. Tidak menyimpan riwayat skor → tidak bisa audit perubahan prioritas seiring waktu.
14. Mengandalkan satu feed TI (KEV/EPSS) tanpa verifikasi → blind spot; gunakan multi-sumber dengan TLP dan freshness check.

---

## 11. Kriteria penerimaan implementasi (AC-N)

| ID | Kriteria | Cara verifikasi |
|---|---|---|
| AC-1 | 5 berkas baru ada dengan frontmatter 3 field + ending "Best Practices" | validasi frontmatter + baca akhir berkas |
| AC-2 | 15 topik brainstorming tertampung (mapping §5) | cek per berkas vs tabel topik |
| AC-3 | `SKILL.md` Capability Map & Reference Documentation mencakup 5 berkas baru (1:1) | paritas tabel |
| AC-4 | `SKILL.md` Progressive Disclosure mencakup 5 berkas baru | cek tabel |
| AC-5 | Gotchas SKILL.md bertambah 14 butir khas scoring | hitung butir |
| AC-6 | `cvss-scoring.md` punya section "Kapan pakai v3.1 vs v4.0 (ringkas)" + link | baca berkas |
| AC-7 | `prioritization.md` punya pointer ke 5 berkas baru + baris "Risk acceptance" | baca berkas |
| AC-8 | Tidak ada berkas yatim (semua terdaftar di SKILL.md) | cek 1:1 |
| AC-9 | grep pola materi ujian = 0 hasil termasuk URL | grep |
| AC-10 | `SKILL.md` ≤ 450 baris | hitung baris |
| AC-11 | Tautan relatif semua berkas baru resolve | resolusi tautan |
| AC-12 | Perubahan tercatat di `CHANGELOG.md` | cek entri |

---

## 12. Tes penerimaan perilaku

| # | Prompt | Perilaku yang diharapkan |
|---|---|---|
| 1 | "Hitung CVSS untuk CVE ini" | Meminta/menyebut versi, metrik, konteks; menghasilkan vector string; tidak mengarang metrik |
| 2 | "Pakai v3.1 atau v4.0?" | Menjawab dengan matriks keputusan + aturan konsistensi; tidak "terserah" |
| 3 | "EPSS rendah, berarti aman?" | Menjelaskan EPSS adalah probabilitas, bukan kepastian; tetap pertimbangkan CVSS & konteks |
| 4 | "CVE ini tidak ada di KEV, berarti tidak urgent?" | Menjelaskan KEV hanya subset; absence bukan bukti aman |
| 5 | "Beri CVSS untuk S3 bucket publik" | Menolak CVSS palsu; menawarkan rubrik internal band + konteks |
| 6 | "Rata-rata CVSS portfolio kita 7.2" | Menjelaskan rata-rata menyesatkan; menawarkan agregasi yang mempertimbangkan jumlah/severity/exposure |
| 7 | "Accept risk untuk semua temuan Low" | Menolak accept tanpa owner/expiry/review; menawarkan kriteria risk acceptance |
| 8 | "Skor ini beda dengan analis lain" | Menyebut calibration & rubrik; menawarkan sesi kalibrasi |
| 9 | "Temuan ini sudah 6 bulan, masih relevan?" | Menyebut time decay & re-scoring; tidak mengklaim skor tetap valid |
| 10 | Kasus baru yang tidak ada di contoh | Urutan penalaran sama (versi → base → environmental → threat → konteks → validasi → agregasi) |

---

## 13. Prosedur implementasi (usulan)

1. Buat 5 berkas baru dengan cakupan minimum §6 (mulai `cvss-environmental-temporal.md` sebagai fondasi).
2. Perluas 2 berkas existing §6 (mulai `cvss-scoring.md`, lalu `prioritization.md`).
3. Perbarui SKILL.md: Capability Map, Reference Documentation, Progressive Disclosure, Gotchas (+14), Decision Frame (+butir scoring).
4. (Opsional ringan) Perbarui `referensi.md` dengan sumber CVSS/EPSS/KEV/FAIR.
5. Jalankan verifikasi mesin: frontmatter, indeks 1:1, grep pola ujian, hitung baris SKILL.md, resolusi tautan.
6. Catat perubahan di `CHANGELOG.md`.
7. (Opsional) Tambah contoh penalaran scoring di `persona.md`.
8. Uji perilaku §12 (10 skenario) secara manual.

Urutan dalam langkah 1: `cvss-environmental-temporal.md` → `epss-kev-integration.md` → `asset-criticality-scoring.md` → `risk-acceptance-and-alternatives.md` → `scoring-consistency.md`.

---

## 14. Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Duplikasi konten antara berkas baru dan existing | Drift, kebingungan | Cross-reference, bukan salin; review diff |
| SKILL.md melebihi 450 baris setelah penambahan Gotchas/Decision Frame | Melanggar NFR-1 | Pindahkan detail ke references; SKILL.md hanya indeks + ringkas |
| Persona berubah menjadi "scoring tutor" | Hilangnya suara praktisi | FR-1, FR-2, FR-20; tambah contoh penalaran scoring |
| Overclaim akurasi skor (seolah pasti) | Kredibilitas runtuh | FR-3, FR-15; wajib ketidakpastian & validasi |
| Score inflation antar analis | Skor tidak konsisten | FR-12; calibration wajib |
| CVSS palsu untuk misconfig | Laporan menyesatkan | FR-11; rubrik internal |
| Risk acceptance tanpa jejak | Audit gagal | FR-9; template + owner + expiry |
| Berkas baru yatim karena lupa update SKILL.md | Tidak ditemukan pengguna | FR-16; verifikasi indeks 1:1 |
| Rata-rata CVSS untuk portfolio | Menyembunyikan temuan kritis | FR-13; metode agregasi |
| Skor statis (tidak re-score) | Temuan lama dengan exploit baru tidak naik | FR-14; time decay |
| Mengandalkan satu feed TI | Blind spot | Gotcha #14; multi-sumber + TLP/freshness |

---

## 15. Keputusan yang dibutuhkan

| ID | Keputusan | Pilihan | Dampak bila ditunda |
|---|---|---|---|
| D1 | Apakah `cvss-environmental-temporal.md` menjadi fondasi wajib sebelum berkas lain? | ya (disarankan) / tidak | Berkas lain tanpa fondasi perhitungan = tidak konsisten |
| D2 | Apakah pemilihan versi CVSS diwajibkan konsisten per engagement/program? | ya (disarankan) / tidak | Campur versi → prioritas membingungkan |
| D3 | Apakah risk acceptance wajib punya owner + expiry + review? | ya (disarankan) / tidak | Temuan "diterima" hilang tanpa jejak |
| D4 | Apakah alternative scoring hanya dipakai dengan justifikasi & normalisasi? | ya (disarankan) / tidak | Perbandingan metodologi menyesatkan |
| D5 | Apakah scoring temuan tanpa CVE wajib memakai rubrik internal (bukan CVSS palsu)? | ya (disarankan) / tidak | Laporan menyesatkan |
| D6 | Apakah menambah contoh penalaran scoring di `persona.md`? | ya / tidak | Persona scoring tidak teruji |
| D7 | Apakah calibration (scoring consistency) diwajibkan per tim? | ya (disarankan) / tidak | Score inflation antar analis |
| D8 | Apakah re-scoring periodik (time decay) diwajibkan? | ya (disarankan) / tidak | Skor statis, temuan lama tidak naik prioritas |

---

## 16. Metrik

| Metrik | Kondisi awal | Target |
|---|---|---|
| Berkas referensi scoring mendalam | 0 (hanya `cvss-scoring.md`, `prioritization.md`) | 5 baru |
| Berkas existing yang diperluas dengan bagian scoring mendalam | 2 (ringkas) | 2 (mendalam) |
| Topik scoring brainstorming yang tertampung | ~6 (base, env ringkas, v4 ringkas, contextual, prioritas, threat intel ringkas) | 15/15 |
| Gotchas khas scoring | 0 (hanya gotcha umum #3) | 14 |
| Indeks SKILL.md (Capability Map/Reference/Progressive) yang mencakup scoring mendalam | 0 | 1:1 untuk 5 berkas baru |
| Pola materi ujian di berkas scoring (FR-17) | 0 | 0 |
| Tautan rusak setelah penambahan | 0 | 0 |
| Berkas yatim | 0 | 0 |

---

## 17. Lampiran — sumber acuan

- `docs/PERSONA-INJECTION-NEEDS.md` — format analisis kebutuhan, anatomi persona, FR/NFR, antipattern, tes penerimaan, metrik, rencana penerapan, risiko.
- `docs/PUBLISHING-NEEDS.md` — format analisis kebutuhan, temuan bukti, definisi, ruang lingkup, FR/NFR, LI-N, opsi & matriks, kriteria penerimaan, risiko & antipattern, prosedur, keputusan, metrik.
- `docs/VA-CLOUD-NEEDS.md` — pola analisis kebutuhan aspek VA (struktur, FR per berkas, gotchas, tes penerimaan, metrik, rencana, risiko, keputusan).
- `skills/vulnerability-assessment/SKILL.md` — persona, kontrak, decision frame, capability map, gotchas.
- `skills/vulnerability-assessment/references/cvss-scoring.md` — kondisi saat ini (CVSS v3.1/v4.0, contextual scoring).
- `skills/vulnerability-assessment/references/prioritization.md` — kondisi saat ini (matriks prioritas, threat intel, SLA).
- Hasil brainstorming CVSS scoring & risk quantification (subagent `brainstorm-cvss-scoring`): 15 topik, 5 berkas baru, 2 berkas existing yang diperluas, 14 gotchas, rekomendasi struktur berkas.

---

**Catatan:** Dokumen ini adalah analisis kebutuhan. Implementasi berkas referensi, perluasan berkas existing, dan pembaruan SKILL.md dilakukan pada langkah berikutnya sesuai rencana penerapan §13, dan setiap perubahan dicatat di `CHANGELOG.md`.
