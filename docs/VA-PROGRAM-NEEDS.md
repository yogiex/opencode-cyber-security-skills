# Analisis Kebutuhan — Aspek Vulnerability Management Program pada Skill vulnerability-assessment

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-14
**Pertanyaan yang dijawab:** skill `vulnerability-assessment` saat ini kuat pada VA teknis per target (scoping, scanning, triase, CVSS, pelaporan, verifikasi remediasi), tetapi belum memiliki aspek *Vulnerability Management Program* — governance, SLA, exception, metrik, ITSM, otomasi, continuous VA, disclosure, supply chain, data management, maturity, ownership/playbook, dan compliance/audit evidence. Apa yang dibutuhkan agar skill ini juga berfungsi sebagai panduan program VM end-to-end, bukan hanya assessment one-off?
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md), [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md); [skills/vulnerability-assessment/SKILL.md](../skills/vulnerability-assessment/SKILL.md) dan references yang ada; output brainstorm `brainstorm-va-program`.

---

## 1. Ringkasan

Skill `vulnerability-assessment` saat ini berisi 9 berkas referensi yang mencakup metodologi VA, asset discovery, konfigurasi scanner, scoring CVSS, prioritisasi, pelaporan, verifikasi remediasi, persona, dan referensi eksternal. Semua itu berfokus pada **satu engagement VA** (satu target, satu scan, satu laporan). Yang belum ada adalah lapisan **program**: bagaimana VA dikelola sebagai proses berkelanjutan di organisasi — siapa yang bertanggung jawab, SLA berapa hari, bagaimana exception ditangani, bagaimana temuan dideduplikasi lintas scanner, bagaimana dashboards dibangun, dan bagaimana bukti audit dikumpulkan.

Audit 2026-11-14 terhadap `SKILL.md` dan references menemukan **14 celah program** yang tidak tertutup oleh referensi existing. Hasil brainstorming `brainstorm-va-program` mengusulkan **11 berkas referensi baru** dan **pemerluasan 2 berkas existing** (`remediation-verification.md`, `reporting.md`), ditambah **14 gotchas** khas program VM.

Yang belum ada di repo: **definisi operasional "program VM"** (bukan sekadar scan berulang), **peta kapabilitas program** yang menaut ke berkas nyata, **kontrak persona** yang mencakup keputusan program (bukan hanya keputusan teknis per temuan), dan **kriteria penerimaan** yang dapat diverifikasi mesin. Dokumen ini mengisi kekosongan itu, sekaligus menetapkan apa yang **tidak** akan dikerjakan (hanya analisis kebutuhan, bukan implementasi).

---

## 2. Kondisi saat ini (bukti)

Diukur 2026-11-14 terhadap `skills/vulnerability-assessment/`.

| # | Temuan | Bukti (berkas/baris) | Akibat |
|---|---|---|---|
| T1 | `SKILL.md` menyebut "membangun atau mengevaluasi program vulnerability management" sebagai use case, tetapi Capability Map hanya menaut ke 9 referensi teknis per engagement | `SKILL.md` L37, L79–L92 | janji program tidak didukung artefak |
| T2 | `remediation-verification.md` menyebut SLA secara implisit lewat tracking, tetapi tidak ada definisi SLA per severity, breach management, atau eskalasi | `remediation-verification.md` L13–L33 | SLA tidak terukur dan tidak terlacak |
| T3 | `Accepted Risk` hanya 4 baris generik (dokumentasikan, mitigasi alternatif, review 6–12 bulan, eskalasi CISO untuk Critical) | `remediation-verification.md` L64–L71 | exception management tidak standar |
| T4 | `reporting.md` menyebut "Trend" hanya satu baris contoh (MTTR 45 hari) dan compliance mapping hanya tabel 4 temuan | `reporting.md` L91–L93, L96–L106 | dashboards/trend dan audit evidence tidak terstruktur |
| T5 | `prioritization.md` menyebut SLA remediasi per severity (7/30/90/180 hari) tetapi tidak ada mekanisme enforcement/breach | `prioritization.md` L39–L47 | SLA hanya deklarasi, bukan proses |
| T6 | `va-methodology.md` menyebut frekuensi scan (monthly/biweekly/weekly/on-push) tetapi tidak ada orkestrasi/otomasi atau continuous VA | `va-methodology.md` L108–L115 | frekuensi tidak dapat dijalankan konsisten |
| T7 | Tidak ada referensi tentang deduplikasi temuan lintas scanner, asset identity, atau data model temuan | seluruh `references/` | duplikasi temuan membesar, metrik kacau |
| T8 | Tidak ada referensi tentang ITSM integration (Jira/ServiceNow), routing, atau sync status | seluruh `references/` | remediasi tidak terhubung ke sistem tiket |
| T9 | Tidak ada referensi tentang vulnerability disclosure / bug bounty / coordinated disclosure | seluruh `references/` | pengungkapan eksternal tidak terkelola |
| T10 | Tidak ada referensi tentang third-party / supply chain VA (vendor, SBOM, dependency) | seluruh `references/` | rantai pasok tidak tercakup |
| T11 | Tidak ada referensi tentang program maturity / continuous improvement (CMMI, roadmap) | seluruh `references/` | tidak ada baseline dan target perbaikan |
| T12 | Tidak ada referensi tentang charter & governance program VM (scope organisasi, RACI, funding, policy) | seluruh `references/` | program tidak punya mandat formal |
| T13 | Tidak ada referensi tentang metrik & KPI program (MTTR, coverage, density, SLA breach rate, false positive rate) | seluruh `references/` | program tidak terukur |
| T14 | Tidak ada referensi tentang dashboards & trend analytics (definisi widget, sumber data, cadence) | seluruh `references/` | reporting ad-hoc, tidak konsisten |

Catatan: T2–T6 adalah celah pada berkas existing yang **sudah ada materinya tetapi dangkal**; T7–T14 adalah celah **materi sama sekali tidak ada**. Keduanya harus ditangani, tetapi dengan strategi berbeda (pemerluasan vs berkas baru).

---

## 3. Definisi

**Vulnerability Management Program (program VM)** — proses organisasi berkelanjutan yang mengelola seluruh siklus hidup kerentanan: dari inventaris aset, scanning berulang, triase dan deduplikasi, penugasan remediasi, enforcement SLA, penanganan exception, pengukuran metrik, hingga pelaporan ke manajemen dan audit. Berbeda dari **VA engagement** (satu kali scan pada target tertentu) yang menghasilkan laporan; program VM menghasilkan **tren, akuntabilitas, dan perbaikan berkelanjutan**.

**Program vs engagement.** Engagement menjawab "apa kerentanan di target X hari ini?". Program menjawab "apakah organisasi kita menjadi lebih aman dari bulan ke bulan, siapa yang bertanggung jawab, dan bagaimana kita membuktikannya?".

**Charter program** — dokumen mandat yang menetapkan scope organisasi, tujuan, RACI, sumber daya, dan kebijakan (mis. "semua aset Tier-1 discan mingguan, SLA Critical 7 hari"). Tanpa charter, program VM hanya kumpulan scan tanpa akuntabilitas.

**SLA (Service Level Agreement) remediasi** — tenggat waktu maksimum antara temuan diverifikasi dan remediasi terverifikasi, per severity dan per tier aset. Bukan target yang "sebaiknya", melainkan kontrak yang diukur dan dieskalasi bila dilanggar.

**Exception / accepted risk** — keputusan formal untuk tidak meremediasi temuan dalam SLA, dengan alasan, mitigasi alternatif, pemilik yang menyetujui, dan tanggal review. Bukan "nanti saja" atau "terlalu mahal".

**Deduplikasi** — proses menggabungkan temuan yang sama (CVE yang sama pada aset yang sama) dari sumber berbeda (scanner, manual, bug bounty) menjadi satu rekaman kanonik, agar metrik tidak terinflasi.

**Maturity** — tingkat kedewasaan program VM, diukur dari adanya kebijakan, otomasi, metrik, dan perbaikan berkelanjutan. Dipakai untuk menetapkan roadmap, bukan untuk pamer.

---

## 4. Ruang lingkup

**Termasuk:**
- 14 topik program VM (§5) yang belum tertutup oleh referensi existing.
- 11 berkas referensi baru + pemerluasan 2 berkas existing (§5, tabel pemetaan).
- Pembaruan `SKILL.md`: Capability Map, Progressive Disclosure, Persona Contract, Decision Frame, dan Gotchas agar memuat aspek program.
- Konsistensi frontmatter, indeks 1:1, dan paritas tabel dengan konvensi repo (AGENTS.md).

**Tidak termasuk:**
- Implementasi berkas referensi (hanya analisis kebutuhan; implementasi dilakukan pada tahap berikutnya).
- Perubahan konten skill lain (persona, scanning teknis, CVSS) kecuali yang diperlukan untuk integrasi program.
- Integrasi teknis ke Jira/ServiceNow nyata (hanya spesifikasi kebutuhan dan pola).
- Pembuatan dashboard nyata (hanya definisi metrik, widget, dan sumber data).
- Perubahan alur kerja repo (validator, sync, changelog) — tetap berlaku.

---

## 5. Pemetaan topik → artefak

| # | Topik | Artefak (referensi) | Status |
|---|---|---|---|
| 1 | VM program charter & governance | `vm-program-governance.md` | Baru |
| 2 | SLA enforcement & breach management | `sla-enforcement.md` | Baru |
| 3 | Exception & accepted risk management | `exception-management.md` | Baru |
| 4 | VM metrics & KPI | `vm-metrics.md` | Baru |
| 5 | Dashboards & trend analytics | `vm-metrics.md` (widget/trend) + `reporting.md` (diperluas) | Baru + existing |
| 6 | ITSM integration (Jira/ServiceNow) | `itsm-integration.md` | Baru |
| 7 | VA automation & orchestration | `va-automation.md` | Baru |
| 8 | Continuous VA / shift-left | `continuous-va.md` | Baru |
| 9 | Vulnerability disclosure & bug bounty | `vulnerability-disclosure.md` | Baru |
| 10 | Third-party & supply chain VA | `third-party-supply-chain.md` | Baru |
| 11 | Vulnerability data management & deduplication | `vuln-data-management.md` | Baru |
| 12 | Program maturity & continuous improvement | `program-maturity.md` | Baru |
| 13 | Remediation ownership & playbooks | `remediation-verification.md` (diperluas) | Existing |
| 14 | Compliance mapping & audit evidence | `reporting.md` (diperluas) | Existing |

**Keterangan:** 11 berkas baru + 2 berkas existing yang diperluas = 13 artefak untuk 14 topik (topik 5 dan 14 menumpang pada berkas existing yang diperluas agar tidak membuat berkas duplikat). Semua berkas baru wajib memiliki frontmatter YAML (name, description, tags) sesuai konvensi repo.

---

## 6. Kebutuhan fungsional

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | Skill memuat aspek program VM sebagai lapisan di atas VA teknis, tanpa menghapus materi VA teknis | 13 artefak program terdaftar di Capability Map & Reference Documentation; materi existing tidak berkurang |
| FR-2 | Charter & governance program dapat ditulis dari referensi (scope organisasi, RACI, kebijakan, funding) | `vm-program-governance.md` memuat template charter, RACI, dan kebijakan minimal |
| FR-3 | SLA remediasi per severity & tier aset didefinisikan, beserta breach management dan eskalasi | `sla-enforcement.md` memuat tabel SLA, definisi breach, dan alur eskalasi |
| FR-4 | Exception / accepted risk dikelola secara formal (alasan, mitigasi, pemilik, tanggal review, eskalasi) | `exception-management.md` memuat template exception dan aturan eskalasi (termasuk Critical) |
| FR-5 | Metrik & KPI program didefinisikan dengan rumus, sumber data, dan target | `vm-metrics.md` memuat ≥8 metrik dengan rumus dan target |
| FR-6 | Dashboards & trend analytics didefinisikan (widget, cadence, sumber data) | `vm-metrics.md` + `reporting.md` memuat definisi dashboard eksekutif dan teknis |
| FR-7 | ITSM integration dispesifikasikan (Jira/ServiceNow: field mapping, status sync, routing, SLA timer) | `itsm-integration.md` memuat mapping field dan alur sync |
| FR-8 | Otomasi & orkestrasi VA dispesifikasikan (scan scheduling, triase otomatis, notifikasi, dedup) | `va-automation.md` memuat arsitektur dan pola orkestrasi |
| FR-9 | Continuous VA / shift-left dispesifikasikan (frekuensi per target, gate CI/CD, feedback loop) | `continuous-va.md` memuat model continuous dan integrasi pipeline |
| FR-10 | Vulnerability disclosure & bug bounty dispesifikasikan (coordinated disclosure, SLA respons, scope) | `vulnerability-disclosure.md` memuat policy template dan alur |
| FR-11 | Third-party & supply chain VA dispesifikasikan (vendor assessment, SBOM, dependency scan) | `third-party-supply-chain.md` memuat kerangka dan checklist |
| FR-12 | Data management & deduplikasi dispesifikasikan (data model temuan, asset identity, dedup key, sumber kebenaran) | `vuln-data-management.md` memuat skema dan aturan dedup |
| FR-13 | Program maturity & continuous improvement dispesifikasikan (model level, indikator, roadmap) | `program-maturity.md` memuat model maturity dan roadmap |
| FR-14 | Remediation ownership & playbooks diperluas pada `remediation-verification.md` (RACI remediasi, playbook per tipe temuan) | `remediation-verification.md` memuat RACI dan ≥3 playbook |
| FR-15 | Compliance mapping & audit evidence diperluas pada `reporting.md` (mapping framework, bukti yang dikumpulkan, retention) | `reporting.md` memuat mapping multi-framework dan daftar bukti audit |
| FR-16 | Persona contract dan Decision Frame diperbarui agar mencakup keputusan program (charter, SLA breach, exception, maturity) | `SKILL.md` Persona Contract ≥7 butir; Decision Frame ≥7 butir dengan ambang |
| FR-17 | Gotchas program (14 butir, §9) ditambahkan ke `SKILL.md` tanpa menghapus gotchas teknis existing | Gotchas section memuat ≥24 butir (10 existing + 14 baru) |
| FR-18 | Setiap berkas program baru muncul tepat sekali di Reference Documentation dan Progressive Disclosure | indeks 1:1, paritas tabel |
| FR-19 | Bahasa Indonesia + istilah teknis Inggris; kode/komentar Inggris; format markdown sesuai konvensi | pemeriksaan manual + grep |

---

## 7. Kebutuhan non-fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| NFR-1 | `SKILL.md` tetap 120–200 baris target, batas keras 450; kelebihan materi program dipindahkan ke `references/`, tidak dibuang | hitung baris |
| NFR-2 | Setiap berkas `references/` (existing + 11 baru) muncul tepat sekali di Reference Documentation; tidak ada berkas yatim | paritas tabel |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`) | pemeriksaan struktur |
| NFR-4 | Frontmatter YAML (name, description, tags) pada 11 berkas baru | pemeriksaan frontmatter |
| NFR-5 | Perubahan tercatat di `CHANGELOG.md` (penambahan 11 berkas + pemerluasan 2 berkas + pembaruan SKILL.md) | entri changelog |
| NFR-6 | Perubahan dapat diverifikasi ulang oleh mesin: grep, hitung baris, resolusi tautan, paritas tabel | skrip existing |
| NFR-7 | Tidak mengubah validator repo (`check-changelog.js`, `check-fact-notes.js`, `sync-skills.js`) | tidak ada perubahan scripts |
| NFR-8 | Referensi program tidak menduplikasi materi VA teknis; cross-reference dengan tautan, bukan salinan | review manual |

---

## 8. Kebutuhan per topik (detail minimum)

Setiap berkas program harus memuat minimum konten berikut agar dapat disebut "lengkap". Ini adalah spesifikasi isi, bukan implementasi.

### 8.1 `vm-program-governance.md` (Topik 1)
- Definisi program VM vs VA engagement.
- Template charter: tujuan, scope organisasi, RACI (VM Lead, asset owner, remediation owner, CISO), kebijakan (frekuensi scan, SLA, exception), sumber daya, review cadence.
- Peran dan kewenangan: siapa yang boleh accept risk, siapa yang eskalasi.
- Governance cadence: review bulanan/kuartalan, steering committee.
- Best practices.

### 8.2 `sla-enforcement.md` (Topik 2)
- Tabel SLA remediasi per severity × tier aset (Critical/High/Medium/Low × Tier 1/2/3).
- Definisi breach (missed SLA) dan perhitungan waktu (dari verifikasi temuan, bukan dari scan).
- Alur eskalasi per level breach (7 hari, 30 hari, dsb.).
- Aturan pause SLA (exception yang disetujui menunda timer).
- Metrik breach rate.
- Best practices.

### 8.3 `exception-management.md` (Topik 3)
- Definisi exception vs accepted risk vs false positive vs mitigated.
- Template exception: ID, temuan, alasan, mitigasi alternatif, pemilik yang menyetujui, tanggal review, status.
- Aturan: Critical tidak boleh di-accept tanpa eskalasi CISO; review 6–12 bulan; re-evaluasi saat kondisi berubah.
- Alur approval (siapa menyetujui berdasarkan severity).
- Best practices.

### 8.4 `vm-metrics.md` (Topik 4 & 5)
- Minimal 8 metrik: MTTR, coverage %, vulnerability density, SLA breach rate, false positive rate, mean time to detect (MTTD), remediation throughput, exception count.
- Rumus, sumber data, cadence pengukuran, target.
- Definisi dashboard eksekutif (widget, audience) dan dashboard teknis (widget, audience).
- Trend analytics: perbandingan periode, deteksi regresi, top recurring CVE.
- Best practices.

### 8.5 `itsm-integration.md` (Topik 6)
- Pola integrasi dengan Jira/ServiceNow: pembuatan tiket otomatis per temuan, field mapping (severity→priority, asset→CMDB, SLA→due date).
- Status sync dua arah (VM tool ↔ ITSM).
- Routing berdasarkan asset owner / tim.
- Penanganan duplikat dan re-open.
- Best practices.

### 8.6 `va-automation.md` (Topik 7)
- Arsitektur orkestrasi: scheduler, scanner pool, triase otomatis, notifikasi, dedup pipeline.
- Pola: scan on-schedule, scan on-change, scan on-push (container).
- Triase otomatis: false positive rules, allowlist, confidence scoring.
- Notifikasi: email/Slack/Teams, digest, eskalasi.
- Best practices.

### 8.7 `continuous-va.md` (Topik 8)
- Model continuous: frekuensi per target (network monthly, web biweekly, cloud weekly, container on-push, code on-PR).
- Shift-left: integrasi ke CI/CD (SAST/DAST/SCA/secret scan), gate kebijakan (block on Critical).
- Feedback loop: temuan → dev → fix → re-scan.
- Best practices.

### 8.8 `vulnerability-disclosure.md` (Topik 9)
- Coordinated vulnerability disclosure (CVD) policy template.
- Bug bounty: scope, out-of-scope, reward, SLA respons, safe harbor.
- Alur: intake → triase → remediasi → disclosure → credit.
- Penanganan disclosure yang tidak terkoordinasi (0-day, leak).
- Best practices.

### 8.9 `third-party-supply-chain.md` (Topik 10)
- Kerangka third-party VA: vendor assessment, questionnaire, evidence.
- Supply chain: SBOM, dependency scan (SCA), container base image, CI/CD pipeline security.
- Risk rating vendor dan keputusan (approve/conditional/reject).
- Monitoring berkelanjutan (vendor score, re-assessment cadence).
- Best practices.

### 8.10 `vuln-data-management.md` (Topik 11)
- Data model temuan kanonik (field wajib: ID, CVE, asset, severity, status, owner, SLA, sumber).
- Asset identity (CMDB key, hostname, IP, cloud resource ID).
- Dedup key (CVE + asset + port/endpoint).
- Sumber kebenaran (single source of truth) dan sync dari scanner.
- Retention dan arsip.
- Best practices.

### 8.11 `program-maturity.md` (Topik 12)
- Model maturity (mis. 4 level: ad-hoc, defined, managed, optimized) dengan indikator per level.
- Self-assessment checklist.
- Roadmap perbaikan dari level ke level.
- Hubungan maturity dengan metrik.
- Best practices.

### 8.12 Pemerluasan `remediation-verification.md` (Topik 13)
- RACI remediasi (VM Lead, asset owner, remediation owner, verifier).
- Playbook per tipe temuan: missing patch, misconfiguration, weak credential, exposed service, third-party dependency (minimal 5 playbook).
- SLA handoff ke ITSM.
- Eskalasi breach.
- Tetap mempertahankan isi existing (tracking, re-scan, regresi, accepted risk).

### 8.13 Pemerluasan `reporting.md` (Topik 14)
- Compliance mapping multi-framework yang lebih lengkap (PCI DSS, SOC 2, ISO 27001, NIST CSF, CIS) dengan bukti yang dikumpulkan per kontrol.
- Audit evidence: daftar artefak, retention, format, lokasi.
- Dashboards (eksekutif & teknis) dengan definisi widget.
- Tetap mempertahankan isi existing (struktur laporan teknis/manajemen/compliance).

---

## 9. Gotchas program VM (14 butir)

Gotchas ini khas program VM (bukan VA teknis per target). Harus ditambahkan ke `SKILL.md` Gotchas (yang saat ini 10 butir teknis) tanpa menghapus yang ada.

1. **SLA dihitung dari verifikasi temuan, bukan dari scan.** Temuan yang belum ditriase tidak masuk SLA; jika tidak, SLA akan terinflasi oleh false positive.
2. **Exception yang tidak punya tanggal review akan menjadi accept selamanya.** Setiap exception wajib punya tanggal review; tanpa itu, risiko terakumulasi diam-diam.
3. **Critical yang di-accept tanpa eskalasi CISO adalah kegagalan governance.** Jangan izinkan accept risk Critical di level tim.
4. **Dedup yang salah menggandakan metrik.** Temuan yang sama dari 3 scanner harus menjadi 1 rekaman; jika tidak, MTTR dan breach rate tidak bermakna.
5. **Coverage yang dihitung dari aset yang terdaftar, bukan yang ada.** Shadow IT membuat coverage terlihat 100% padahal ada gap. Inventaris harus diverifikasi, bukan dipercaya.
6. **Dashboard yang menampilkan jumlah temuan tanpa tren menyesatkan.** 50 temuan bulan ini vs 30 bulan lalu bisa berarti perbaikan (lebih banyak scan) atau degradasi. Selalu tampilkan tren dan coverage.
7. **Otomasi triase tanpa allowlist akan menutup temuan nyata.** Aturan false positive harus diaudit berkala; jangan percaya aturan lama.
8. **ITSM sync dua arah bisa menimpa status.** Tentukan sumber kebenaran (VM tool atau ITSM) per field; jangan biarkan dua sistem saling menimpa.
9. **Bug bounty scope yang tidak jelas menghasilkan temuan out-of-scope yang membebani triase.** Definisikan scope dan out-of-scope secara eksplisit; bayar hanya in-scope.
10. **Third-party VA tanpa re-assessment cadence akan basi.** Vendor yang dinilai sekali setahun bisa berubah tanpa diketahui. Tetapkan cadence re-assessment.
11. **SBOM yang tidak diperbarui saat release tidak berguna.** SBOM harus dihasilkan per build, bukan per kuartal.
12. **Shift-left gate yang terlalu ketat akan di-bypass developer.** Gate harus realistis (block Critical/High dengan exploit, bukan semua Medium) dan disertai feedback yang jelas.
13. **Maturity model yang dipakai untuk pamer, bukan perbaikan, akan kehilangan kredibilitas.** Pakai maturity untuk roadmap, bukan sertifikat.
14. **Compliance mapping yang tidak didukung bukti akan gagal audit.** Setiap kontrol yang diklaim harus punya artefak bukti yang bisa ditunjukkan.

---

## 10. Kriteria penerimaan (AC)

Dinyatakan **lengkap** bila seluruh butir berikut terbukti:

| ID | Kriteria | Cara verifikasi |
|---|---|---|
| AC-1 | 11 berkas referensi baru ada di `references/` dengan frontmatter valid | cek file + frontmatter |
| AC-2 | `remediation-verification.md` dan `reporting.md` diperluas dengan bagian program (RACI/playbook; compliance evidence/dashboard) | cek section baru |
| AC-3 | Capability Map dan Reference Documentation di `SKILL.md` memuat 9+11=20 berkas (paritas 1:1) | hitung baris tabel |
| AC-4 | Persona Contract ≥7 butir dan Decision Frame ≥7 butir dengan ambang | hitung butir |
| AC-5 | Gotchas ≥24 butir (10 existing + 14 program) | hitung butir |
| AC-6 | Progressive Disclosure memuat 20 entri | hitung baris |
| AC-7 | Tidak ada berkas referensi yatim (setiap berkas muncul di Reference Documentation) | cross-check |
| AC-8 | `SKILL.md` ≤ 450 baris | hitung baris |
| AC-9 | Tidak ada materi VA teknis yang dihapus (AP-1) | diff review |
| AC-10 | Setiap berkas program memuat section "Best Practices" | grep heading |
| AC-11 | Tautan relatif dari `SKILL.md` ke 20 berkas resolve | resolusi tautan |
| AC-12 | Perubahan tercatat di `CHANGELOG.md` | cek entri |

---

## 11. Risiko dan antipattern

### 11.1 Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Program layer membesarkan SKILL.md melewati 450 baris | melanggar NFR-1 | pindahkan detail ke references; SKILL.md hanya indeks + contract + frame |
| 11 berkas baru membuat referensi yatim | melanggar NFR-2 | indeks 1:1 wajib; verifikasi paritas tabel |
| Duplikasi dengan materi VA teknis (SLA, accepted risk) | kebingungan | cross-reference, bukan salinan; tandai "lihat prioritization.md" |
| Persona contract yang terlalu panjang kehilangan fokus | persona jadi checklist | maksimal 7 butir, masing-masing satu kalimat |
| Program layer menggeser fokus dari VA teknis | skill kehilangan kekuatan inti | program adalah lapisan tambahan, bukan pengganti |
| Implementasi terburu-buru menghasilkan berkas dangkal | AC terpenuhi tapi kualitas rendah | gunakan §8 sebagai spesifikasi minimum; review manual |

### 11.2 Antipattern yang dilarang

| ID | Antipattern | Mengapa salah |
|---|---|---|
| AP-1 | Menghapus materi VA teknis agar "muat" program | menukar satu penyakit dengan penyakit lain (lihat PERSONA-INJECTION-NEEDS AP-1) |
| AP-2 | Mengganti label "SLA" menjadi "target" tanpa enforcement | SLA yang tidak diukur bukan SLA |
| AP-3 | Menyalin tabel SLA dari `prioritization.md` ke `sla-enforcement.md` tanpa menambah enforcement | duplikasi, bukan pemerluasan |
| AP-4 | Membuat berkas program tanpa frontmatter | melanggar konvensi repo |
| AP-5 | Menulis charter tanpa RACI | charter tanpa akuntabilitas |
| AP-6 | Menyatakan "program maturity Level 4" tanpa indikator | pamer, bukan perbaikan |
| AP-7 | Menambah gotchas program dengan menghapus gotchas teknis | kehilangan pengetahuan teknis |
| AP-8 | Mengklaim integrasi ITSM "sudah terhubung" tanpa spesifikasi field | janji palsu |

---

## 12. Rencana penerapan (usulan, belum dijalankan)

| Prioritas | Pekerjaan | Alasan urutan |
|---|---|---|
| 1 | Perbarui `SKILL.md`: Capability Map, Reference Documentation, Progressive Disclosure untuk 20 berkas | fondasi indeks sebelum berkas baru ditulis |
| 2 | Perbarui Persona Contract dan Decision Frame agar mencakup keputusan program | persona harus siap sebelum materi program |
| 3 | Tulis 11 berkas referensi baru sesuai §8.1–8.11 | materi inti program |
| 4 | Perluas `remediation-verification.md` (RACI, playbook) dan `reporting.md` (compliance evidence, dashboard) | materi existing diperdalam |
| 5 | Tambahkan 14 gotchas program ke `SKILL.md` | pengetahuan kegagalan |
| 6 | Jalankan validator (`check-changelog.js`, `check-fact-notes.js`, `sync-skills.js`) dan verifikasi AC-1–AC-12 | bukti penerimaan |
| 7 | Catat perubahan di `CHANGELOG.md` | jejak audit |

Langkah 1–7 saat ini **belum dijalankan**. Dokumen ini hanya analisis kebutuhan.

---

## 13. Keputusan yang dibutuhkan

| ID | Keputusan | Pilihan | Dampak bila ditunda |
|---|---|---|---|
| D1 | Apakah program layer ditambahkan ke skill yang sama, atau skill terpisah (`vulnerability-management-program`)? | tambah ke skill yang sama (disarankan) / skill baru | skill baru memecah referensi dan persona; integrasi lebih sulit |
| D2 | Apakah SLA default (7/30/90/180) dipertahankan atau disesuaikan per organisasi? | pertahankan default + override (disarankan) / tetapkan global | organisasi berbeda butuh SLA berbeda |
| D3 | Apakah maturity model 4 level cukup, atau pakai model eksternal (CMMI, OWASP SAMM)? | 4 level internal + referensi eksternal (disarankan) / adopsi penuh | adopsi penuh menambah kompleksitas |
| D4 | Apakah gotchas program digabung dengan gotchas teknis atau section terpisah? | satu section (disarankan) / terpisah | section terpisah memudahkan pembacaan tapi memecah daftar |
| D5 | Apakah dashboard didefinisikan di `vm-metrics.md` atau `reporting.md`? | `vm-metrics.md` (disarankan) / `reporting.md` | hindari duplikasi |

---

## 14. Metrik keberhasilan

| Metrik | Kondisi awal (2026-11-14) | Target |
|---|---|---|
| Berkas referensi skill | 9 | 20 (9 existing + 11 baru) |
| Topik program VM tertutup | 0 dari 14 | 14 dari 14 |
| Gotchas di SKILL.md | 10 | ≥24 |
| Persona Contract butir | 6 | ≥7 |
| Decision Frame butir | 7 | ≥7 (dengan ambang program) |
| Kriteria penerimaan terpenuhi | 0 dari 12 | 12 dari 12 |
| Materi VA teknis yang hilang | 0 | 0 (AP-1) |

---

## 15. Referensi

- [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md) — acuan bentuk analisis kebutuhan.
- [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md) — acuan bentuk analisis kebutuhan.
- [skills/vulnerability-assessment/SKILL.md](../skills/vulnerability-assessment/SKILL.md) — kondisi saat ini.
- [skills/vulnerability-assessment/references/remediation-verification.md](../skills/vulnerability-assessment/references/remediation-verification.md) — berkas existing yang diperluas.
- [skills/vulnerability-assessment/references/reporting.md](../skills/vulnerability-assessment/references/reporting.md) — berkas existing yang diperluas.
- [skills/vulnerability-assessment/references/prioritization.md](../skills/vulnerability-assessment/references/prioritization.md) — sumber SLA default.
- Output brainstorm `brainstorm-va-program` — sumber 14 topik, 11 berkas baru, 14 gotchas.

---

*Analisis kebutuhan ini belum diimplementasikan. Implementasi mengikuti rencana §12 setelah keputusan §13 ditetapkan.*