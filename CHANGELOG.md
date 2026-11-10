# Changelog — Audit Trail Perubahan File

Dokumen ini adalah catatan resmi setiap perubahan file di repo ini. Tujuannya agar setiap penambahan, perubahan, penghapusan, dan penggantian nama file dapat diaudit tanpa harus membaca diff git satu per satu.

## Aturan

1. **Satu entri per perubahan set** (satu PR atau satu rangkaian commit yang koheren), dengan tanggal ISO `YYYY-MM-DD` dan judul ringkas.
2. **Setiap file wajib disebut namanya** — path lengkap relatif terhadap root, dibungkus backtick, di dalam tabel entri.
3. **Kolom wajib:** `File | Perubahan | Alasan | Verifikasi`. Verifikasi adalah perintah atau pemeriksaan yang benar-benar dijalankan.
4. **Artefak turunan tetap dicatat.** `manifest.json`, `skills/index.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` dicatat dengan perintah generator sebagai verifikasi.
5. **Status commit:** tulis `pending` sebelum commit, lalu perbarui dengan hash pada commit berikutnya. Karena hash sebuah commit tidak bisa mencantumkan dirinya sendiri, rujukan akhir adalah `git log -- CHANGELOG.md`; status tidak boleh dibiarkan `pending` lebih dari satu commit.
6. **Jangan menulis ulang sejarah.** Koreksi dilakukan dengan entri baru yang menyebut entri yang dikoreksi.
7. **Wildcard hanya untuk karantina.** Entri wildcard (nama direktori minimal tiga tingkat, diakhiri dua bintang) hanya boleh dipakai untuk perubahan yang bukan milik sesi ini dan belum diputuskan; validator akan menampilkannya sebagai peringatan, bukan audit eksplisit. Wildcard yang terlalu luas ditolak.
8. **Validasi wajib:** `node scripts/check-changelog.js --base <ref>` harus exit 0 sebelum commit.

## [0.21.0] — 2026-11-10 — menggabungkan cabang `feat/ec-cnd-persona-injection` ke `dev`

**Commit dasar:** `c8f9376` (branch `dev`)
**Status:** committed in `e267e08`
**Ruang lingkup:** permintaan langsung — menggabungkan cabang `feat/ec-cnd-persona-injection` (satu commit, `1c51abc`) ke `dev` agar riwayat `ec-cnd` hanya punya satu jalur. Berkas skill-nya sendiri sudah identik dan sudah ada di `dev` sejak `abae7be`, jadi merge tidak mengubah isi `skills/ec-cnd/`, `manifest.json`, maupun `skills/index.json`. Yang berubah hanya dokumen: baris `ec-cnd` akhirnya masuk matriks kualitas, dan entri `0.19.0` versi cabang tidak dipakai karena nomor itu sudah terpakai di `dev` untuk refactor sembilan persona.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `docs/SKILL-QUALITY.md` | baris `ec-cnd` (ya/ya/—/ya/14/ya/Selesai) masuk matriks; total 28 → 29; Selesai 12 → 13; cakupan Frame 23/28 → 24/29 (83%); catatan "berada di cabang" diganti catatan merge; backlog H menunjuk `ec-cnd/references/referensi.md` alih-alih "(cabang)" | ledger harus mencerminkan skill yang sudah ada di pohon | dihitung ulang dari matriks: 29 baris, Frame 24, Selesai 13/Sebagian 11/Belum 5; jumlah berkas `skills/ec-cnd/references/*.md` = 14 |
| `CHANGELOG.md` | entri 0.21.0 ini; blok konflik `0.19.0` versi cabang dibuang | merge menghasilkan konflik teks di berkas ini dan penomoran cabang tidak bisa dipakai | `node scripts/check-changelog.js --base c8f9376` |

### Catatan

Merge dijalankan dengan `git merge --no-ff origin/feat/ec-cnd-persona-injection`. `manifest.json` dan `skills/index.json` auto-merge tanpa selisih terhadap `dev` — `git diff HEAD --` kosong dan `JSON.parse` sukses dengan 29 skill — sehingga tidak ada artefak turunan yang perlu diregenerasi.

Entri `0.19.0` milik cabang sengaja tidak dinaikkan ke `dev`: nomor itu sudah dipakai entri "Sembilan skill bersertifikat menjadi persona praktisi", dan isi entri cabang tersebut — 15 berkas `skills/ec-cnd/` plus `docs/CND-PERSONA-NEEDS.md` yang belum ikut ter-commit — sudah dibereskan oleh `abae7be` dan tercatat pada entri 0.17.0.

Berkas `tmp-check-payload.js` yang masih untracked tidak ikut di-commit.

## [0.20.1] — 2026-11-10 — Koreksi hitungan baris pada entri 0.20.0

**Commit dasar:** `cd8a471` (branch `dev`)
**Status:** committed in `09cf100`
**Ruang lingkup:** entri 0.20.0 mencatat jumlah baris dari `split(/\r?\n/).length` di skrip Node, yang menambahkan satu elemen kosong untuk baris baru di akhir berkas. Konvensi repo — dikoreksi pada 0.16.1 — adalah `(Get-Content <path>).Count`. Semua angka pada entri 0.20.0 karena itu lebih tinggi satu. Entri ini mencatat angka yang benar tanpa mengubah entri 0.20.0.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `CHANGELOG.md` | entri 0.20.0 dikoreksi lewat entri ini: `security-auditor` 339→282 menjadi 338→281; `log-management-nist-800-92` 428→415 menjadi 427→414; `devsecops-mindset` 382→350 menjadi 381→349; `owasp-top10-2025` 376→365→376 menjadi 375→364→375; `ptes-standard/references/referensi.md` 68→62 menjadi 67→61; `threat-modeling` 76→87 menjadi 75→86; `incident-response-plan` 92→103 menjadi 91→102; `risk-management-framework` 107→118 menjadi 106→117 | metode hitung harus konsisten dengan konvensi repo | `(Get-Content <path>).Count` untuk tiap berkas |

### Catatan

Yang salah adalah metodenya, bukan besar perubahannya: selisih setiap angka tepat satu, dan arah perubahan tetap sama. Angka pada entri 0.19.0 tidak terpengaruh karena diukur dengan `(Get-Content).Count`.

## [0.20.0] — 2026-11-10 — Katalog sertifikasi dibersihkan, Decision Frame mencapai 82%

**Commit dasar:** `62fc03d` (branch `dev`)
**Status:** committed in `cd8a471`
**Ruang lingkup:** dua pekerjaan yang saling menutup. **Pertama**, sisa materi ujian lapis B dihapus: empat skill non-sertifikasi masih memuat katalog sertifikasi beserta harga, vendor latihan soal, dan "exam guide", dan satu skill standar masih memuat daftar sertifikasi. **Kedua**, empat skill yang belum punya `## Decision Frame` kini memilikinya, sehingga cakupan frame naik dari 19/28 (68%) ke **23/28 (82%)** — melewati ambang yang `docs/SKILL-QUALITY.md` tetapkan sendiri sejak 0.6.0 untuk menyalakan penegakan Frame.

### Diubah — katalog sertifikasi dihapus

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/security-auditor/SKILL.md` | 339 → 282 baris: `## Certification Path` (tabel 6 sertifikasi + harga + prasyarat), `### CISA vs ISO 27001 Lead Auditor`, `### Career Progression`, `### Sertifikasi Detail` (biaya exam, CPE, renewal, jumlah pemegang), `### Training & Courses` (4 baris `exam prep`/bootcamp), dan 3 baris buku produk ujian dihapus; description dan satu butir "kapan dipakai" diganti | skill ini mengajarkan audit, bukan cara lulus sertifikasi | `grep` `\bexams?\b\|bootcamp\|practice question\|CPE\|passing score` = 0 hasil |
| `skills/log-management-nist-800-92/SKILL.md` | 428 → 415 baris: `### Sertifikasi & Training` (7 sertifikasi dengan label `(exam only)` dan `(exam)`) dihapus | harga ujian bukan pengetahuan log management | idem |
| `skills/devsecops-mindset/SKILL.md` | 382 → 350 baris: `### Sertifikasi DevSecOps` (13 sertifikasi) dan `### Training & Courses` (10 kursus sertifikasi) dihapus | katalog vendor bukan pola pikir DevSecOps | idem |
| `skills/owasp-top10-2025/SKILL.md` | 376 → 365 baris: `### Certifications` (6 sertifikasi + harga) dihapus; `### Training & Courses` dipertahankan karena isinya pelatihan praktik, bukan ujian | bedakan pelatihan praktik dari katalog ujian | idem |
| `skills/ptes-standard/references/referensi.md` | 68 → 62 baris: `## Certifications` (OSCP, GPEN, PenTest+) dihapus; description tidak lagi menyebut `certifications` | PTES adalah standar, bukan jalur sertifikasi | `grep` `certificat` = 0 hasil |

### Diubah — Decision Frame ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/threat-modeling/SKILL.md` | 76 → 87 baris; 6 keputusan operasional: kelayakan waktu, pemilik risiko, kedalaman yang cukup, jalur yang bisa dijelaskan, proporsionalitas mitigasi, hasil yang bisa ditindaklanjuti | tanpa frame, sesi threat modeling berhenti sebagai daftar ancaman | `grep '^## Decision Frame'` = 1 |
| `skills/incident-response-plan/SKILL.md` | 92 → 103 baris; 6 keputusan: insiden vs gangguan, kewenangan menghentikan layanan, containment vs bukti, tenggat notifikasi, satu juru bicara, ambang eskalasi dan pemulihan | rencana IR non-teknis tanpa ambang hanya upacara | idem |
| `skills/risk-management-framework/SKILL.md` | 107 → 118 baris; 6 keputusan: kedalaman RMF, kategori dampak, baseline dan pengecualian, penerima risiko sisa, bukti efektivitas, pemicu tinjauan otorisasi | RMF tanpa pemicu tinjauan menjadi izin permanen | idem |
| `skills/owasp-top10-2025/SKILL.md` | 365 → 376 baris; 6 keputusan: kategori yang berlaku, urutan akses kontrol, salah konfigurasi vs salah desain, eksploitabilitas, bukti klaim, gerbang minimum sebelum rilis | sepuluh kategori adalah kerangka, bukan checklist | idem |

### Diubah — katalog dan ledger

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `docs/SKILL-QUALITY.md` | status 4 skill Belum → Sebagian; ringkasan Selesai 12 / Sebagian 11 / Belum 5; cakupan Frame 19/28 → 23/28; backlog D dan G ditutup, D2 ditambahkan; bagian enforcement diperbarui | ledger harus mencerminkan keadaan setelah perubahan | dihitung ulang dari matriks |
| `README.md` | baris `security-auditor` tidak lagi menyebut "jalur sertifikasi" | deskripsi katalog harus sejalan dengan skill | 0 kemunculan "sertifikasi" pada baris itu |
| `skills/index.json` | deskripsi `security-auditor` diperbarui | indeks harus mencerminkan frontmatter | `node scripts/sync-skills.js` |
| `manifest.json` | deskripsi `security-auditor` diperbarui | manifest adalah sumber kebenaran global | `node scripts/sync-skills.js` |

### Catatan

Yang **tidak** dihapus, dan alasannya: tabel biaya framework di `security-auditor` (SOC 2 $30K–$150K, ISO 27001, PCI DSS) adalah biaya audit dan sertifikasi *organisasi* — informasi kerja bagi auditor, bukan biaya ujian perorangan. Baris `Certification` pada ISO 27001 dan HITRUST adalah status sertifikasi organisasi, juga bukan materi ujian.

`### Training & Courses` di `owasp-top10-2025` dipertahankan karena berisi pelatihan praktik (PortSwigger Web Security Academy, TCM Practical Web Defense), bukan bimbingan ujian. `### CTF & Practice Platforms` juga dipertahankan.

Empat skill masih `Belum`: `security-auditor`, `log-management-nist-800-92`, `devsecops-mindset`, `soc-analyst` — keempatnya monolitik tanpa `references/` (backlog C). Ketiga yang pertama sudah bersih dari materi ujian pada entri ini, tetapi belum punya Decision Frame.

Verifikasi yang dijalankan: `node scripts/check-fact-notes.js`, `node scripts/check-changelog.js --base 62fc03d` di worktree terpisah, `grep` pola materi ujian pada kelima berkas, hitung ulang cakupan `## Decision Frame` (23/28), dan paritas sel tabel pada kelima berkas.

**Tidak dijalankan:** tes perilaku dan A/B ablation (backlog F).

## [0.19.2] — 2026-11-10 — `cpent` dicabut lagi setelah refactor-nya mendarat

**Commit dasar:** `62c4606` (branch `dev`)
**Status:** committed in `434b672`
**Ruang lingkup:** 0.19.1 mengembalikan `cpent` ke `check-fact-notes.js` dengan asumsi refactor `cpent` masih belum di-commit. Asumsi itu salah pada saat commit dibuat: `87500a8` (refactor `cpent`) sudah mendarat di antara `d6279b9` dan `62c4606`, sehingga versi `cpent` yang di-commit sudah tidak memuat blockquote provenance. Hasilnya checker gagal dengan alasan yang berlawanan. Entri ini mencabut pendaftaran itu untuk kedua kalinya, dan kali ini sesuai keadaan repo.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `scripts/check-fact-notes.js` | `cpent` dicabut dari `EXPECTED`; kembali menjadi 2 entri (`mitre-attack`, `nist-800-53`) | `skills/cpent/SKILL.md` pada `87500a8` tidak lagi memuat catatan provenance | `node scripts/check-fact-notes.js` exit 0 |
| `CHANGELOG.md` | entri 0.19.1 ditandai `committed in 62c4606`; entri 0.19.2 ditambahkan | status tidak boleh dibiarkan `pending` lebih dari satu commit | `git log -- CHANGELOG.md` |

### Catatan

Dua entri berturut-turut (0.19.1 dan 0.19.2) saling membatalkan. Keduanya dipertahankan, tidak ditulis ulang, karena aturan 6 melarang menulis ulang sejarah: yang terjadi adalah repo bergerak di antara dua commit, dan jejaknya justru bukti bahwa pemeriksaan dijalankan.

Pelajaran untuk kerja paralel: status checker tidak boleh disimpulkan dari working tree ketika direktori itu juga dipegang sesi lain. Sumber kebenaran adalah `git show HEAD:<path>`.

## [0.19.1] — 2026-11-10 — Perbaikan: `cpent` tetap terdaftar sampai refactor-nya di-commit

**Commit dasar:** `d6279b9` (branch `dev`)
**Status:** committed in `62c4606`
**Ruang lingkup:** 0.19.0 mencabut `cpent` dari `check-fact-notes.js` karena working tree sudah tidak memuat catatan provenance. Itu keliru: `skills/cpent/SKILL.md` yang **sudah di-commit** masih memuat blockquote lama, sehingga commit `d6279b9` meninggalkan repo dengan checker yang gagal. Entri ini mengembalikan pendaftaran itu sampai refactor `cpent` (didokumentasikan pada 0.12.0) ikut di-commit.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `scripts/check-fact-notes.js` | `EXPECTED` memuat kembali `cpent` (3 entri), dengan komentar bahwa pendaftaran hanya berlaku sampai refactor `cpent` di-commit | repo harus lulus checker pada setiap commit, bukan hanya di working tree | `node scripts/check-fact-notes.js` exit 0 |
| `CHANGELOG.md` | entri 0.19.0 ditandai `committed in d6279b9`; entri 0.19.1 ditambahkan | status tidak boleh dibiarkan `pending` lebih dari satu commit | `git log -- CHANGELOG.md` |

### Catatan

Ketika refactor `cpent` di-commit, blockquote provenance ikut hilang dan pendaftaran ini **wajib** dicabut pada commit yang sama. Urutannya tidak bisa dibalik: mencabut lebih dulu membuat commit sebelumnya gagal, sedangkan membiarkan terlalu lama membuat commit berikutnya gagal.

## [0.19.0] — 2026-11-10 — Sembilan skill bersertifikat menjadi persona praktisi

**Commit dasar:** `04c4e1a` (branch `dev`)
**Status:** committed in `d6279b9`
**Ruang lingkup:** permintaan langsung — skill yang tujuannya lulus ujian sertifikasi bukan lagi tempat yang tepat untuk repo ini; tujuannya persona injection agar agent paham cybersecurity. Audit 2026-11-10 menemukan **sembilan** skill dengan sinyal tujuan-ujian (description, artefak ujian, atau Decision Frame berisi taktik ujian). Kesembilan dikonversi ke bentuk persona: identitas peran, mandat, batas klaim, Persona Contract, Decision Frame operasional, doktrin, suara, dan contoh penalaran. Seluruh angka ujian dihapus dan dipusatkan di `docs/CERTIFICATION-FACTS.md`. Standar kerja: `docs/PERSONA-CONVERSION.md`; analisis kebutuhan: `docs/PERSONA-INJECTION-NEEDS.md`.

### Ditambahkan — persona (9 berkas)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/comptia-cysa/references/persona.md` | cyber defense analyst: profil, kedalaman, kebiasaan berpikir, suara, preferensi, batas klaim, 5 jawaban contoh | persona butuh suara, bukan hanya daftar domain | 5 jawaban contoh; bagian batas klaim ada |
| `skills/ec-ecih/references/persona.md` | incident handler: profil, kebiasaan, suara, penolakan, 6 jawaban contoh | idem | 6 jawaban contoh |
| `skills/lf-cks/references/persona.md` | Kubernetes platform security engineer: 5 jawaban contoh | idem | 5 jawaban contoh |
| `skills/offsec-ir-200/references/persona.md` | incident responder: 5 jawaban contoh termasuk penolakan reboot | idem | 5 jawaban contoh |
| `skills/offsec-pen-300/references/persona.md` | evasion / red team operator: 5 jawaban contoh | idem | 5 jawaban contoh |
| `skills/offsec-soc-200/references/persona.md` | detection & defensive analyst: 5 jawaban contoh | idem | 5 jawaban contoh |
| `skills/offsec-th-200/references/persona.md` | threat hunter: 6 jawaban contoh | idem | 6 jawaban contoh |
| `skills/offsec-web-300/references/persona.md` | konsultan web white-box: 6 jawaban contoh | idem | 6 jawaban contoh |
| `skills/oscp-methodology/references/persona.md` | offensive security consultant: 5 jawaban contoh | idem | 5 jawaban contoh |

### Ditambahkan — turunan konversi (16 berkas)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `docs/PERSONA-CONVERSION.md` | 193 baris: audit berbukti, bentuk akhir wajib, larangan isi ujian, disposisi berkas, kriteria selesai | standar kerja harus tertulis sebelum eksekusi | 9 skill diaudit; pola verifikasi §5 dapat dijalankan |
| `docs/PERSONA-INJECTION-NEEDS.md` | 194 baris: temuan tiga lapis, definisi, 8 komponen persona, 10 FR, 6 NFR, 8 antipattern, 8 tes perilaku, metrik, rencana | jawaban atas "seperti memiliki sertifikasi" dan "mindset" perlu terukur, bukan slogan | 8 komponen; 8 skenario uji |
| `skills/offsec-ir-200/references/capability-domains.md` | pengganti nama `modules-overview.md`: 13 "modul" menjadi kemampuan, studi kasus utuh | nomor modul adalah struktur kursus | 0 kemunculan "modul"/"exam" |
| `skills/offsec-pen-300/references/capability-domains.md` | 8 domain kapabilitas menggantikan silabus 16 modul | idem | 0 nomor modul/bobot |
| `skills/offsec-soc-200/references/capability-domains.md` | 9 domain kapabilitas, tanpa nomor modul dan bobot fase | idem | 0 bobot/poin |
| `skills/offsec-th-200/references/capability-domains.md` | 7 domain kapabilitas, aktor dan TLP dipertahankan | idem | 0 bobot |
| `skills/offsec-web-300/references/capability-domains.md` | 10 domain kapabilitas, pola aplikasi nyata | idem | 0 nomor modul |
| `skills/oscp-methodology/references/engagement-playbook.md` | pengganti `exam-strategy.md`: scope/RoE, disiplin bukti, urutan laporan, kriteria berhenti, serah terima | jadwal ujian tidak punya padanan kerja; disiplin delivery punya | 0 jam ujian |
| `skills/offsec-pen-300/references/engagement-playbook.md` | scope, higiene payload, bukti, urutan laporan, stop, pembersihan | idem | 0 jam ujian |
| `skills/offsec-web-300/references/engagement-playbook.md` | laporan sisi klien untuk asesmen white-box, remediasi, retest, redaksi | idem | 0 jadwal ujian |
| `skills/offsec-soc-200/references/detection-labs.md` | 8 latihan mandiri yang bisa dibangun sendiri: sumber telemetri, dataset, temuan yang diharapkan | lab ujian tidak bisa diakses; latihan nyata bisa | 8 latihan |
| `skills/offsec-web-300/references/source-review-playbook.md` | metodologi white-box dipindah dari SKILL.md: entry point, alur data, sink, 7 pola | materi teknis dipindahkan, bukan dibuang | 0 kehilangan bagian |
| `skills/offsec-web-300/references/exploit-development.md` | syarat exploit, template Python, workflow, disiplin uji | idem | 4 snippet |
| `skills/offsec-th-200/references/referensi.md` | sumber eksternal: ATT&CK, Splunk, CrowdStrike, Suricata, Zeek, STIX/TAXII, MISP, TLP | daftar sumber belum ada sebagai berkas | 0 tautan ujian |
| `skills/offsec-web-300/references/referensi.md` | sumber eksternal: OWASP, PortSwigger, HackTricks, php.net, postgresql, CVE, repo tool | daftar sumber dipindah dari SKILL.md | 0 tautan ujian |

### Diubah — SKILL.md menjadi persona

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/comptia-cysa/SKILL.md` | 163 baris; description "untuk mempersiapkan sertifikasi" → persona; "When to Use: exam preparation" → kondisi kerja; Frame #6 waktu ujian diganti keputusan operasional | tujuan skill bukan ujian | 0 pola §5; 6 komponen |
| `skills/ec-ecih/SKILL.md` | 438 baris; bagian "ECIH Exam Overview & Strategy" dan seluruh "Daftar Isi" dihapus; blok persona ditambahkan; 7 keputusan operasional | TOC bernomor tidak bisa dipertahankan saat judul wajib `## Gotchas` | `(Get-Content).Count` = 438; 0 pola §5 |
| `skills/lf-cks/SKILL.md` | 199 baris; tabel bobot domain, "Exam Format", "Strategi 3-Pass", gotcha prasyarat CKA dihapus | bobot domain = blueprint ujian | 0 pola §5 |
| `skills/offsec-ir-200/SKILL.md` | 189 baris; "Scoring & Exam Environment" dan "8h Time Management" dihapus; tabel perbandingan tanpa baris durasi/passing | skema poin bukan keputusan kerja | 0 pola §5 |
| `skills/offsec-pen-300/SKILL.md` | 176 baris; tabel 16 modul dan tangga sertifikasi OSCE³ dihapus; Frame ujian diganti keputusan engagement | silabus kursus bukan taksonomi kerja | 0 pola §5 |
| `skills/offsec-soc-200/SKILL.md` | 186 baris; Frame 10 phase × 10 poin diganti keputusan deteksi; Golden Rules dipertahankan sebagai doktrin | aturan deteksi tetap berlaku, skema poin tidak | 0 pola §5 |
| `skills/offsec-th-200/SKILL.md` | 199 baris; "Scoring & Exam Environment" dan timetable 8 jam menjadi kadens hunt multi-hari; "Key Exam Queries" → "Hunting Queries" | hipotesis tetap, jadwal ujian tidak | 0 pola §5 |
| `skills/offsec-web-300/SKILL.md` | 170 baris; §1 "Overview & Exam Structure" dan §5 "Exam Strategy" dihapus; materi teknis dipindah ke 4 referensi baru | dari 447 baris; isi tidak hilang, hanya berpindah | 4 berkas tujuan; 0 pola §5 |
| `skills/oscp-methodology/SKILL.md` | 180 baris; lima butir Frame yang berisi aturan ujian diganti keputusan engagement | proof.txt dan kuota revert hanya ada di ujian | 0 pola §5 |

### Diubah — referensi (42 berkas)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/comptia-cysa/references/domain1-security-operations.md` | bobot 34% dan framing ujian dihapus; isi logging/CTI/hunting/SOAR utuh | bobot domain adalah cetak biru ujian | isi teknis utuh |
| `skills/comptia-cysa/references/domain2-vulnerability-management.md` | bobot 26% dihapus; tabel tool, CVSS/EPSS, kontrol utuh | idem | idem |
| `skills/comptia-cysa/references/domain3-incident-response.md` | bobot 24% dan catatan konsolidasi fase CompTIA dihapus | idem | idem |
| `skills/comptia-cysa/references/domain4-reporting.md` | bobot 16% dihapus; template executive summary dan KPI utuh | idem | idem |
| `skills/comptia-cysa/references/tools-frameworks.md` | penomoran domain ujian diganti pemetaan fokus | idem | idem |
| `skills/lf-cks/references/referensi.md` | baris logistik ujian (handbook, FAQ, prasyarat CKA, killer.sh, halaman kursus) dihapus; sumber teknis dipertahankan | logistik ujian bukan sumber belajar | 0 tautan ujian |
| `skills/lf-cks/references/runtime-defense.md` | satu gotcha tentang Falco yang sudah terpasang di ujian dihapus | tidak berlaku di cluster nyata | 0 |
| `skills/offsec-ir-200/references/containment-eradication-recovery.md` | description dan 2 kalimat ujian diganti framing insiden nyata | idem | 0 |
| `skills/offsec-ir-200/references/digital-forensics.md` | catatan "di exam" pada waktu ingest Autopsy dihapus | waktu ingest berlaku umum | 0 |
| `skills/offsec-ir-200/references/ir-lifecycle.md` | 3 kalimat ujian diganti disiplin kerja (ITIL, matriks severity lokal, template plan) | idem | 0 |
| `skills/offsec-ir-200/references/malware-triage.md` | 2 kalimat ujian diganti konteks sampel nyata | idem | 0 |
| `skills/offsec-ir-200/references/reporting.md` | description dan 2 kalimat skema nilai diganti disiplin dokumentasi | idem | 0 |
| `skills/offsec-ir-200/references/splunk-siem.md` | 4 kalimat "di exam" diganti "di environment target" | query tetap, konteks diganti | 0 |
| `skills/offsec-pen-300/references/ad-exploitation.md` | description dan best practice bebas ujian | idem | 0 |
| `skills/offsec-pen-300/references/av-edr-evasion.md` | frasa "sebelum exam" pada praktik pengujian dihapus | idem | 0 |
| `skills/offsec-pen-300/references/c2-strategy.md` | heading dan best practice ujian dihapus; panduan C2 netral | idem | 0 |
| `skills/offsec-pen-300/references/mssql-attacks.md` | kalimat "di exam" diganti konteks enterprise | idem | 0 |
| `skills/offsec-pen-300/references/referensi.md` | exam guide, FAQ, halaman sertifikasi, silabus, dan blog "passing the OSEP exam" dihapus; dokumentasi hulu Sliver/Mythic ditambahkan | tautan ujian tetap materi ujian walau berada di URL | 0 `exam` di seluruh berkas |
| `skills/offsec-pen-300/references/shellcode-runners.md` | description bebas ujian | idem | 0 |
| `skills/offsec-soc-200/assets/report-template.md` | bahasa pengumpulan ujian dihapus; struktur laporan utuh | template adalah deliverable kerja | struktur utuh |
| `skills/offsec-soc-200/references/elk-kql.md` | kalimat ujian dihapus | idem | 0 |
| `skills/offsec-soc-200/references/referensi.md` | OSDA Exam Guide, Exam FAQ, OpenExamsPrep practice questions, tabel exam review, study group, logistik kursus, dan 3 video review dihapus; nomor dirapikan 1–82 | vendor latihan soal adalah pelanggaran paling jelas | 0 tautan ujian |
| `skills/offsec-soc-200/references/windows-event-logs.md` | kalimat ujian dihapus; tabel event ID utuh | idem | tabel utuh |
| `skills/offsec-soc-200/scripts/common-detection-queries.kql` | komentar ujian dihapus; query utuh | idem | query utuh |
| `skills/offsec-th-200/assets/report-template.md` | kata ujian di frontmatter/judul dihapus; struktur dan tabel chain of custody utuh | idem | struktur utuh |
| `skills/offsec-th-200/references/case-studies.md` | kalimat ujian diganti disiplin hunt | idem | 0 |
| `skills/offsec-th-200/references/crowdstrike-cql.md` | kalimat ujian diganti konteks hunian | idem | 0 |
| `skills/offsec-th-200/references/endpoint-hunting.md` | idem | idem | 0 |
| `skills/offsec-th-200/references/network-hunting.md` | idem | idem | 0 |
| `skills/offsec-th-200/references/splunk-hunting.md` | idem | idem | 0 |
| `skills/offsec-th-200/references/th-mindset.md` | "OSTH teaches", "report carries the 70 points", dan gotcha exam briefing diganti; PEAK/SEARCH/Diamond utuh | mindset hunt dipertahankan | PEAK/SEARCH utuh |
| `skills/offsec-th-200/references/ti-integration.md` | kalimat ujian diganti konteks hunt | idem | 0 |
| `skills/offsec-th-200/scripts/spl-queries.spl` | header "exam environment" → "your environment"; 30+ query tidak berubah | query tidak perlu diubah | query identik |
| `skills/oscp-methodology/references/ad-attack-chain.md` | prioritas 40 poin dan pembagian waktu ujian dihapus | idem | 0 |
| `skills/oscp-methodology/references/buffer-overflow.md` | catatan ujian dan anggaran 30 menit dihapus | idem | 0 |
| `skills/oscp-methodology/references/enumeration-framework.md` | framing ujian di frontmatter dihapus | idem | 0 |
| `skills/oscp-methodology/references/linux-privesc.md` | idem | idem | 0 |
| `skills/oscp-methodology/references/password-cracking.md` | label dan framing OSCP dihapus | idem | 0 |
| `skills/oscp-methodology/references/pivoting.md` | alasan "for exam" diganti alasan kerja | idem | 0 |
| `skills/oscp-methodology/references/referensi.md` | tautan persiapan ujian dan klaim "145+" dihapus; sumber teknis dipertahankan | klaim jumlah tidak terverifikasi | 0 tautan ujian |
| `skills/oscp-methodology/references/web-attacks.md` | larangan sqlmap diganti trade-off noise/reliability | larangan itu aturan ujian, bukan aturan kerja | 0 |
| `skills/oscp-methodology/references/windows-privesc.md` | framing ujian di frontmatter dihapus | idem | 0 |

### Diubah — ir-200 referensi yang dibawa sesi lain

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/references/file-integrity-check.md` | 211 baris; berkas baru dari sesi paralel, ikut di-commit agar indeks tidak menunjuk berkas yang tidak ada | sudah didokumentasikan pada 0.18.0 | terindeks 1:1 |
| `skills/offsec-ir-200/references/hidden-file-hunting.md` | berkas baru dari sesi paralel, ikut di-commit karena alasan yang sama | didokumentasikan pada 0.15.0 | terindeks 1:1 |
| `skills/offsec-ir-200/references/live-response.md` | berkas baru dari sesi paralel, ikut di-commit karena alasan yang sama | didokumentasikan pada 0.13.0 | terindeks 1:1 |

### Diubah — infra dan katalog

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `scripts/check-fact-notes.js` | `EXPECTED` turun dari 11 menjadi 2 entri (`mitre-attack`, `nist-800-53`); komentar menjelaskan skill bersertifikat kini persona-only | tidak ada lagi skill yang memuat angka ujian untuk dilacak | checker exit 0: "2 fact-bearing skill(s)" |
| `skills/index.json` | deskripsi dan daftar berkas 9 skill diperbarui; total 28 skill | indeks harus mencerminkan berkas yang dapat dimuat | `node scripts/sync-skills.js` |
| `manifest.json` | deskripsi 9 skill menjadi persona; total 28 skill | manifest adalah sumber kebenaran global | `node scripts/sync-skills.js` |
| `README.md` | 9 baris katalog menjadi persona; 6 baris sumber "… Exam Guide" menjadi "OffSec PEN-300 (OSEP)" dan seterusnya dengan tautan `—` | tautan exam guide adalah materi ujian; URL pengganti tidak dikarang | 0 kemunculan `exam` di README |
| `docs/SKILL-QUALITY.md` | kolom **Persona** ditambahkan; Status = Frame + (Provenance atau Persona); 28 skill; Selesai 12 / Sebagian 7 / Belum 9; backlog G dan H | tanpa jalur persona, konversi akan tercatat sebagai kemunduran | dihitung ulang dari matriks |

### Dihapus

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/comptia-cysa/references/exam-overview.md` | dihapus | cetak biru ujian murni: durasi, jumlah soal, passing 750/900, bobot domain | 0 rujukan tersisa |
| `skills/offsec-ir-200/references/modules-overview.md` | diganti nama | struktur 13 modul kursus | pengganti: `capability-domains.md` |
| `skills/offsec-pen-300/assets/exam-checklist.md` | dihapus | checklist pra/saat/pasca ujian | direktori `assets/` ikut dihapus |
| `skills/offsec-pen-300/references/exam-strategy.md` | dihapus | jadwal 47h45m dan kontrol panel | pengganti: `engagement-playbook.md` |
| `skills/offsec-pen-300/references/modules-overview.md` | dihapus | silabus 16 modul | pengganti: `capability-domains.md` |
| `skills/offsec-soc-200/assets/pre-exam-checklist.md` | dihapus | checklist hari ujian | 0 rujukan tersisa |
| `skills/offsec-soc-200/references/challenge-labs.md` | diganti nama | lab tantangan berbayar | pengganti: `detection-labs.md` |
| `skills/offsec-soc-200/references/modules-overview.md` | dihapus | struktur modul kursus | pengganti: `capability-domains.md` |
| `skills/offsec-soc-200/references/overview-exam.md` | dihapus | struktur ujian, skor, lingkungan | 0 rujukan tersisa |
| `skills/offsec-th-200/references/modules-overview.md` | dihapus | struktur modul kursus | pengganti: `capability-domains.md` |
| `skills/offsec-web-300/references/modules-overview.md` | dihapus | daftar modul kursus | pengganti: `capability-domains.md` |
| `skills/oscp-methodology/references/exam-architecture.md` | dihapus | mekanika penilaian, kombinasi lulus, pembatasan tool | tidak ada padanan kerja |
| `skills/oscp-methodology/references/exam-strategy.md` | dihapus | perencanaan waktu ujian | pengganti: `engagement-playbook.md` |

### Catatan

Angka ujian tidak dihapus dari repo: seluruhnya tetap tersedia di `docs/CERTIFICATION-FACTS.md` sebagai arsip fakta. Yang berubah adalah skill tidak lagi mengajarkannya.

Hitungan baris memakai `(Get-Content <path>).Count` mengikuti konvensi yang dikoreksi pada 0.16.1.

Verifikasi yang dijalankan: `node scripts/check-fact-notes.js` (exit 0, 2 skill), `node scripts/check-changelog.js --base 04c4e1a` di worktree terpisah, perhitungan ulang jumlah berkas `references/` per skill, resolusi seluruh tautan relatif, paritas sel tabel, dan `grep` pola materi ujian termasuk di dalam URL.

**Tidak dijalankan:** tes perilaku §9 `docs/PERSONA-INJECTION-NEEDS.md` (8 skenario) dan A/B ablation; keduanya menunggu backlog F.

**Temuan yang belum dikerjakan** (dicatat di backlog G dan H): `security-auditor`, `log-management-nist-800-92`, `devsecops-mindset`, `owasp-top10-2025` masih memuat katalog sertifikasi, harga, dan vendor latihan soal; `ec-cnd` masih menautkan exam blueprint; `ptes-standard` masih menautkan dua halaman sertifikasi. Keempat skill pertama belum disentuh pada entri ini.

`skills/ec-cnd` berada di cabang `feat/ec-cnd-persona-injection` dan tidak ada di `dev`, sehingga tidak ikut di-commit dan tidak masuk matriks. Angka total skill pada `manifest.json`, `skills/index.json`, dan `docs/SKILL-QUALITY.md` konsisten di 28.

## [0.18.0] — 2026-11-10 — offsec-ir-200: verifikasi integritas file

**Commit dasar:** `16a89b9` (branch `dev`)
**Status:** committed in `d6279b9`
**Ruang lingkup:** permintaan langsung — cara membuktikan file mana yang diubah penyerang: metadata `stat` (mtime/ctime, inode, mode, owner, hardlink), verifikasi paket `rpm -Va` dan `dpkg -V`/`debsums`, pembacaan flag, false positive konffile, batas cakupan paket, dan deteksi manipulasi database paket.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/references/file-integrity-check.md` | 210 baris, 6 tabel: Decision Frame 5 butir; tabel alat (`stat` vs verifikasi paket); pembacaan field `stat` dan tabel "apa yang bisa dipalsukan"; sweep `-newermt`, `-newerct`, `-links`; `rpm -Va` dengan tabel 8 flag beserta prioritas investigasi; tiga jebakan rpm (konffile, `%verify`, database ditambal); `dpkg -V` dan `debsums`; area yang tidak dicakup paket beserta manifest hash; tabel flag ke kesimpulan; false positive; batas; referensi; Best Practices | skill hanya menyebut `dpkg -V`/`rpm -Va` satu baris tanpa cara membaca hasil, tanpa batas cakupan, dan tanpa pembeda false positive | paritas kolom 6 tabel diverifikasi skrip Node (0 temuan); 5 tautan relatif diuji `Test-Path` (semua `True`) |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/SKILL.md` | satu baris ditambahkan ke tiga tabel yang ada (Capability Map, Reference Documentation, Progressive Disclosure) menunjuk `file-integrity-check.md` | referensi harus muncul di semua jalur penemuan skill | `Select-String` menemukan 3 kemunculan `file-integrity-check`; 3 tautan `Test-Path`: `True` |
| `skills/offsec-ir-200/references/hidden-file-hunting.md` | kalimat penutup bagian "Kepemilikan paket" diperluas dengan tautan ke `file-integrity-check.md`; tetap 253 baris | pembaca perlu jalan ke pembacaan flag verifikasi yang rinci | 253 baris, 4 tabel, 0 baris rusak |
| `docs/SKILL-QUALITY.md` | kolom Refs `offsec-ir-200` menjadi 11; baris "Diperbarui" menyebut 0.18.0 | jumlah berkas `references/` berubah: +`file-integrity-check.md` dari entri ini, sementara restrukturisasi sesi lain menghapus `modules-overview.md` serta menambah `capability-domains.md` dan `persona.md` | `(Get-ChildItem skills/offsec-ir-200/references -Filter *.md).Count` = 11 |
| `skills/index.json` | daftar berkas `offsec-ir-200` bertambah `references/file-integrity-check.md` | indeks harus mencerminkan berkas yang dapat dimuat | `node scripts/sync-skills.js` |

### Catatan

Perintah ditulis dari dokumentasi tooling (rpm, dpkg, debsums, coreutils, GNU find) dan belum dijalankan terhadap host target sungguhan. Inti pesan referensi: verifikasi paket hanya mencakup file milik paket, sehingga webroot dan `/usr/local` tetap butuh baseline hash sendiri. Entri 0.13.0 dan 0.15.0 pada sesi ini masih `pending`; nomor 0.16.0 sudah dipakai entri README dan 0.17.0 oleh `ec-cnd`, karena itu entri ini memakai 0.18.0.

## [0.17.0] — 2026-11-10 — ec-cnd: persona injection pengguna bersertifikat CND

**Commit dasar:** `16a89b9` (branch `dev`)
**Status:** committed in `abae7be`
**Ruang lingkup:** permintaan langsung — menambahkan skill **persona injection pengguna yang memegang EC-Council CND (Certified Network Defender)**: agent meminjam persona pengguna (profil, suara, preferensi, batas klaim), bukan memerankan praktisi generik atau tutor ujian. Perubahan melewati fase analisis kebutuhan lebih dulu (`docs/CND-PERSONA-NEEDS.md`), lalu membangun 8 domain kapabilitas ke dalam 14 berkas referensi. Seluruh angka ujian sengaja tidak dimuat — paritas dengan `cpent` — sehingga skill tidak didaftarkan di `check-fact-notes.js`.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/ec-cnd/SKILL.md` | 194 baris: profil persona (identitas pengguna), kapan dipakai, Persona Injection (4 aturan mekanis + 6 perilaku), Persona Contract 7 butir, Decision Frame 7 pertanyaan, doktrin 8 butir, workflow, capability map, Gotchas 8 butir, progressive disclosure | entry point persona harus memuat mekanika injection, bukan hanya tautan | 194 < 500 (status 🔶); 14/14 tautan referensi diuji `Test-Path` |
| `skills/ec-cnd/references/persona.md` | 138 baris: mekanika injection (6 aturan), profil pengguna, kedalaman pengetahuan, kebiasaan berpikir, gaya bicara, preferensi, batas klaim, 4 contoh jawaban | persona harus diinjeksikan secara konsisten, bukan sekadar diketahui | 4 contoh jawaban; bagian batas klaim ada |
| `skills/ec-cnd/references/defense-playbook.md` | 123 baris: siklus ketahui-ukur-desain-ubah-operasikan-respons-perbaiki, template perubahan, otorisasi, dokumentasi, metrik | perubahan konfigurasi tanpa desain dan rollback adalah sumber insiden | 7 fase; tabel field perubahan lengkap |
| `skills/ec-cnd/references/network-architecture.md` | 122 baris: trust zone, DMZ, level segmentasi, east-west, NAC, Zero Trust/SDP, hardening routing/switching, DNS/egress, verifikasi | segmentasi adalah kebijakan, bukan daftar VLAN | tabel 7 zone; langkah pembuktian segmentasi |
| `skills/ec-cnd/references/perimeter-controls.md` | 140 baris: anatomi aturan, higiene, desain kebijakan, IDS/IPS tuning, VPN/TLS, WAF, DDoS, rollback | perimeter adalah batas keputusan yang harus diaudit | 10 bagian; perintah review read-only |
| `skills/ec-cnd/references/endpoint-hardening.md` | 109 baris: baseline dan test ring, Windows/AD, Linux, mobile/MDM, IoT/OT, verifikasi | endpoint adalah tempat data dan klik pengguna | perintah verifikasi Windows dan Linux |
| `skills/ec-cnd/references/app-data-protection.md` | 99 baris: application control, patch, WAF lifecycle, klasifikasi dan akses, enkripsi, DLP, backup, retensi | data adalah yang akhirnya dicuri atau dihapus | tabel kontrol dan prinsip backup 3-2-1 |
| `skills/ec-cnd/references/cloud-virtual-wireless.md` | 99 baris: tanggung jawab bersama, IAM, eksposur publik, VPC, container/Kubernetes, SDN/NFV, wireless | lingkungan non-tradisional menuntut kontrol identitas dan kebijakan | tabel tanggung jawab dan kontrol cloud |
| `skills/ec-cnd/references/detection-telemetry.md` | 117 baris: sensor, pilihan pcap/flow, baseline, alur analisis, sumber log, sentralisasi, SIEM, coverage | deteksi dimulai dari pemahaman normal | filter Wireshark dan tabel sumber log |
| `skills/ec-cnd/references/incident-response.md` | 115 baris: batas peran, urutan preservasi, pilihan containment, tindakan per insiden, paket serah-terima, BC/DR | defender menahan dan menyerahkan, bukan eradication penuh | tabel containment 7 opsi; 6 jenis insiden |
| `skills/ec-cnd/references/risk-threat-intel.md` | 117 baris: risk register, perlakuan risiko, vulnerability management, attack surface, CTI, hunting, PIA, metrik | kerja teknis harus bisa diurutkan dan dipertanggungjawabkan | tabel register 8 kolom; tabel jenis CTI |
| `skills/ec-cnd/references/capability-domains.md` | 54 baris: peta 8 domain, kapabilitas inti, bukti khas, kelompok kerja, cara memakai | peta kapabilitas menghubungkan masalah ke kontrol | 8 domain; 4 kelompok kerja |
| `skills/ec-cnd/references/tools-diagnostics.md` | 159 baris: prinsip read-only, inventaris, firewall, trafik, log, endpoint, kerentanan, cloud, wireless, bukti | tanpa pengukuran, keputusan hanya opini | perintah PowerShell dan bash; aturan penyimpanan bukti |
| `skills/ec-cnd/references/reasoning-examples.md` | 133 baris: 6 skenario dengan situasi, pemeriksaan, keputusan, alasan, penolakan, bukti | contoh penalaran lebih berguna daripada daftar perintah | 6 skenario; pola berulang 6 butir |
| `skills/ec-cnd/references/referensi.md` | 88 baris: EC-Council, NIST, CIS/KEV/EPSS, MITRE, OWASP, tool, bacaan, catatan link rot | klaim teknis harus bisa dilacak ke sumber primer | 5 kelompok sumber; tanggal snapshot |
| `docs/CND-PERSONA-NEEDS.md` | 315 baris: konteks repo, fakta blueprint v4 (8 domain/20 sub-domain), klarifikasi persona injection, desain persona, peta kapabilitas, arsitektur 14 referensi, anti-duplikasi, risiko, kriteria penerimaan, 8 keputusan | analisis kebutuhan harus terdokumentasi sebelum implementasi | angka ujian dan domain dicocokkan dengan blueprint v4.0 |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `README.md` | baris `ec-cnd` di tabel Blue Team dan tabel Referensi | skill baru harus terdaftar di katalog manual | `Test-Path skills/ec-cnd` = True |
| `docs/SKILL-QUALITY.md` | baris `ec-cnd` (Trigger ya, Frame ya, Provenance —, Refs 14, Failure modes ya, Status Sebagian); ringkasan Sebagian 8 → 9; 28 → 29 skill; ambang frame ≥24 dari 29 dan allowlist 9 pengecualian | ledger harus mencerminkan kondisi setelah perubahan | dihitung ulang dari matriks: Frame 20/29 |
| `manifest.json` | entri `ec-cnd` dengan 12 kata kunci; total 29 skill | manifest adalah sumber kebenaran global | `node scripts/sync-skills.js` |
| `skills/index.json` | 15 berkas `ec-cnd` (SKILL.md + 14 referensi) | indeks harus mencerminkan berkas yang dapat dimuat | `node scripts/sync-skills.js` |
| `.claude-plugin/plugin.json` | sinkronisasi daftar skill | artefak turunan plugin | `node scripts/sync-skills.js` |
| `.claude-plugin/marketplace.json` | sinkronisasi katalog marketplace | artefak turunan plugin | `node scripts/sync-skills.js` |
| `.cursor-plugin/plugin.json` | sinkronisasi daftar skill | artefak turunan plugin | `node scripts/sync-skills.js` |

### Catatan

Klarifikasi 2026-11-10: tujuan sesi adalah **persona injection pengguna** yang memegang CND, bukan deskripsi praktisi generik. Framing `SKILL.md`, `persona.md`, dan baris README diselaraskan; entri 0.16.0 dari sesi lain sempat menulis ulang baris `ec-cnd` di README, sehingga deskripsi di baris itu diperbarui lagi di entri ini.

Fakta CND diverifikasi 2026-11-09 dari halaman sertifikasi dan blueprint v4.0. Sampul PDF menulis v4.0 sementara footer setiap halaman masih v3.0 — ketidakcocokan ini dicatat di dokumen analisis, dan tidak dipakai di skill karena persona sengaja bebas angka ujian.

Generator `sync-skills.js` dijalankan sekali untuk entri ini; keluarannya juga memuat berkas `offsec-ir-200/references/hidden-file-hunting.md` dan referensi `cpent` dari pekerjaan sesi lain yang auditnya ada di entri masing-masing (0.15.0 dan 0.12.0).

## [0.16.1] — 2026-11-10 — Koreksi hitungan baris pada entri 0.16.0

**Commit dasar:** `1ec45fd` (branch `dev`)
**Status:** committed in `eefad04`
**Ruang lingkup:** entri 0.16.0 mencantumkan jumlah baris dengan metode baris tak kosong (`Measure-Object -Line`), sehingga `LICENSE` tercatat 17, CONTRIBUTING 206, dan README 235. Konvensi repo adalah jumlah baris total — entri 0.15.0 mencatat 253 baris untuk berkas yang totalnya memang 253. Angka yang benar: 21, 287, dan 304 (dari 332).

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `CHANGELOG.md` | entri 0.16.0 dikoreksi lewat entri ini: `./LICENSE` 17 → 21 baris, `.github/CONTRIBUTING.md` 206 → 287 baris, dan `README.md` 332 → 235 menjadi 332 → 304 baris | hitungan pada 0.16.0 memakai baris tak kosong, tidak konsisten dengan konvensi total baris repo | `(Get-Content LICENSE).Count` = 21; `(Get-Content .github/CONTRIBUTING.md).Count` = 287; `(Get-Content README.md).Count` = 304 |

## [0.16.0] — 2026-11-10 — README profesional dan penutupan celah repo

**Commit dasar:** `3b156dd` (branch `dev`)
**Status:** committed in `dc2ffa7`
**Ruang lingkup:** permintaan langsung — README belum layak tampil sebagai repo publik: tanpa badge, tanpa daftar isi, tanpa peringatan penggunaan sah, perintah instalasi menunjuk repo yang salah (`cyber-security/agent-skills`, sedangkan remote adalah `yogiex/opencode-cyber-security-skills`), skill `ec-cnd` tidak terdaftar, dan dua tautan di README menunjuk file yang tidak ada (`.github/CONTRIBUTING.md`, `LICENSE`).

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `./LICENSE` | Teks MIT lengkap, copyright 2026 yogiex | `manifest.json`, kedua `plugin.json`, dan `marketplace.json` menyatakan MIT, tetapi file lisensi tidak ada — GitHub menandai repo tanpa lisensi | `Test-Path LICENSE` = `True`; 17 baris; teks cocok dengan template MIT (SPDX) |
| `.github/CONTRIBUTING.md` | 206 baris: alur kerja 7 langkah, standar struktur skill dan frontmatter, enam pola penulisan (context, procedures, defaults, control, instruction patterns, refine), aturan provenance, aturan changelog, checklist PR, gaya commit/branch, etika dan batas, lisensi | tautan `[CONTRIBUTING.md](.github/CONTRIBUTING.md)` di README dan AGENTS.md sebelumnya rusak (404); esai best-practices 100 baris dipindahkan dari README ke sini agar README dapat dipindai | 8 tautan relatif diuji `[System.IO.Path]::GetFullPath` + `Test-Path` (semua `True`); 24 pagar kode, jumlah genap; 0 tabel cacat kolom |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `README.md` | ditulis ulang (332 → 235 baris): header + 6 badge (CI, skill, referensi, lisensi, commit terakhir, PR); ringkasan angka 29 skill / 190+ dokumen referensi; daftar isi 12 tautan; instalasi memakai slug `yogiex/opencode-cyber-security-skills` dan perintah plugin yang benar (marketplace add + install); legenda status dipindah sebelum tabel; `ec-cnd` ditambahkan ke Blue Team; deskripsi `cpent` diselaraskan dengan frontmatter persona; bagian baru "Penggunaan yang Sah"; struktur repo memuat `docs/`, `LICENSE`, empat skrip, dan job CI; bagian kualitas dan kontribusi menautkan ledger serta changelog; esai best-practices diganti tautan ke CONTRIBUTING | README adalah halaman pertama repo: harus akurat, dapat dipindai, dan tidak memuat tautan mati atau perintah instalasi yang salah | skrip pemeriksa Node: 29/29 skill terdaftar dan cocok dengan direktori, 0 tautan relatif hilang, 0 baris tabel cacat kolom, 12/12 anchor daftar isi cocok dengan heading, 0 kemunculan slug lama; 14 pagar kode genap; angka referensi diberi sufiks "+" karena pekerjaan sesi lain menambah berkas selama perubahan ini berjalan (190 saat diukur, 192 beberapa menit kemudian) |
| `scripts/check-changelog.js` | `normalize()` menghapus prefiks `./` pada path | file root tanpa ekstensi seperti `LICENSE` sebelumnya tidak mungkin tercatat: parser hanya menerima token yang memuat `/`, berawalan `.`, atau berekstensi | uji `node scripts/check-changelog.js` dengan entri `./LICENSE` (sebelum perbaikan: `LICENSE` dilaporkan hilang; sesudah: terhitung) |

### Karantina

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `docs/PERSONA-CONVERSION.md` | berkas dari pekerjaan sesi lain (konversi persona `cpent`/`ec-cnd`), muncul saat perubahan ini dikerjakan | bukan milik entri ini dan belum ada entri pemiliknya; dicatat agar validator tidak memblokir, menunggu entri yang men-supersede | `node scripts/check-changelog.js` |
| `tmp-check-payload.js` | skrip scratch di root repo, belum diputuskan pemiliknya | bukan milik entri ini; kandidat dihapus atau dipindah ke `scripts/` oleh sesi yang membuatnya | `Test-Path tmp-check-payload.js` = `True` |

### Catatan

Perintah instalasi skill memakai slug repo saat ini; bila repo dipindahkan atau di-fork, blok instalasi dan badge perlu diperbarui bersamaan. `manifest.json` masih memuat `homepage` `https://example.com` dan `repository` `https://github.com/cyber-security/agent-skills` — nilai placeholder itu sekarang tidak lagi tersembunyi karena README memakai slug yang benar, tetapi perbaikannya memerlukan perubahan pada sumber kebenaran dan `node scripts/sync-skills.js`, sehingga sengaja tidak dikerjakan di entri ini. Jumlah referensi di README memakai sufiks "+" agar tidak basi setiap kali referensi bertambah; angka pastinya dipelihara di `docs/SKILL-QUALITY.md`.

## [0.15.0] — 2026-11-10 — offsec-ir-200: hidden file hunting

**Commit dasar:** `16a89b9` (branch `dev`)
**Status:** committed in `d6279b9`
**Ruang lingkup:** permintaan langsung — cara sistematis menemukan file yang disembunyikan di server Linux: nama aneh (dotfile, spasi, newline, escape ANSI), lokasi tak lazim (tmpfs, bind mount, `lost+found`), atribut (mtime vs ctime, immutable, setuid, capability, ACL, xattr), file yang tidak diakui manajer paket, trik rootkit, selisih `df` vs `du`, webshell di webroot, dan timeline dari image.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/references/hidden-file-hunting.md` | 253 baris, 4 tabel: Decision Frame 5 butir; tiga pertanyaan penutup celah; nama (listing aman, `find` berbasis spasi/kontrol), lokasi (mount, tmpfs, bind mount), atribut (waktu, permission, capability, xattr, file yatim), kepemilikan paket (`dpkg -V`, `rpm -Va`, loop `dpkg -S`), sumber independen saat rootkit (`lsof +L1`, `df` vs `du`, `debugfs`, `LD_PRELOAD`), konten (pola webshell, `.user.ini`, ekstensi menyamar), timeline (`find -newermt`, `fls`/`mactime`), checklist 15 menit, false positive, batas, Best Practices | pencarian file tersembunyi belum ada di skill mana pun, padahal ini penentu utama pada insiden defacement dan server compromise | paritas kolom 4 tabel diverifikasi skrip Node (0 temuan); 5 tautan relatif diuji `Test-Path` (semua `True`) |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/SKILL.md` | baris baru di tabel "How to Use This Skill": `Hunt hidden files, webshells, and unowned files` → `references/hidden-file-hunting.md` | referensi harus dapat ditemukan dari SKILL.md | `Test-Path` target tautan: `True` |
| `skills/offsec-ir-200/references/live-response.md` | tambah satu butir di "Referensi Terkait" yang menunjuk `hidden-file-hunting.md` (386 → 387 baris) | triage proses dan koneksi harus berlanjut ke pencarian file | 387 baris, 6 tabel, 0 baris tabel rusak |
| `docs/SKILL-QUALITY.md` | kolom Refs `offsec-ir-200` 8 → 9; baris "Diperbarui" menyebut 0.15.0 | jumlah berkas `references/` bertambah satu | `(Get-ChildItem skills/offsec-ir-200/references -Filter *.md).Count` = 9 |
| `skills/index.json` | daftar berkas `offsec-ir-200` bertambah `references/hidden-file-hunting.md` | indeks harus mencerminkan berkas yang dapat dimuat | `node scripts/sync-skills.js` |

### Catatan

Perintah ditulis dari dokumentasi tooling standar (util-linux, e2fsprogs, iproute2, dpkg/rpm, Sleuth Kit) dan belum dijalankan terhadap host target sungguhan. Semua teknik bersifat baca-saja; referensi melarang `chattr`, `mv`, dan `rm` sebelum eradikasi diputuskan. Entri ini juga mencatat penambahan satu baris pada `live-response.md`, sehingga hitungan 386 baris pada entri 0.13.0 tidak lagi berlaku. `manifest.json` dan `skills/index.json` yang baru diregenerasi juga memuat entri `ec-cnd` serta berkas `cpent` dari pekerjaan sesi lain yang belum masuk changelog.

## [0.14.0] — 2026-11-09 — Web payloads: kerangka keputusan dan syarat otorisasi

**Commit dasar:** `4250b37` (branch `dev`)
**Status:** committed in `16a89b9`
**Ruang lingkup:** `web-pentest-payloads` adalah satu-satunya skill dengan 39 referensi tanpa trigger, decision frame, dan gotchas — perpustakaan serangan tanpa aturan kapan dipakai dan kapan berhenti.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-pentest-payloads/SKILL.md` | 172 → 209 baris; `## Kapan Digunakan` (5 kondisi pakai + 2 pengecualian); `## Decision Frame` 6 keputusan (izin, penandaan payload destruktif, baseline, dua varian per hipotesis, urutan kanal blind, bukti minimum); `## Gotchas` 12 butir; langkah "0" pada `## Cara pakai` | katalog 39 berkas tanpa kerangka membuat payload dapat dipakai tanpa baseline dan tanpa batas berhenti | 39 path `references/` yang disebut semuanya ada (0 hilang); 0 tautan markdown rusak; 0 masalah tabel; butir frame 6; butir gotchas 12 |
| `README.md` | baris 162 diperbarui | deskripsi lama tidak menyebut syarat otorisasi dan kerangka keputusan | dicocokkan dengan SKILL.md |
| `docs/SKILL-QUALITY.md` | baris `web-pentest-payloads` menjadi Trigger ya, Frame ya, Failure modes ya, Status Sebagian; ringkasan Sebagian 7 → 8 dan Belum 10 → 9; paragraf provenance menambah "yang kedelapan"; baris tanggal | ledger harus mencerminkan kondisi setelah perubahan | dihitung ulang dari matriks: Frame 19/28, Sebagian 8, Belum 9 |

### Catatan

Tidak ada payload yang dijalankan pada perubahan ini. Frame mengatur napas pengujian — izin, baseline, batas varian, urutan kanal blind — bukan menambah muatan serangan.

Status tetap Sebagian karena provenance belum dipasang: katalog ini dikurasi ulang dari PayloadsAllTheThings, PortSwigger Academy, dan HackTricks, dan tidak satu pun ada di fact sheet sertifikasi.

## [0.13.0] — 2026-11-09 — offsec-ir-200: live response host triage

**Commit dasar:** `122ffa1` (branch `dev`)
**Status:** committed in `d6279b9`
**Ruang lingkup:** permintaan langsung — menambahkan perilaku operasional untuk tiga pemeriksaan saat host diduga terkompromi: seluruh proses berjalan, cron/penjadwal semua user, dan koneksi jaringan keluar. Sebelumnya skill ini hanya menyebut "network connections, process table" di order of volatility tanpa satu pun perintah. Menyusul tinjauan kedua, ditambahkan rantai penelusuran dari proses ke file yang dieksekusi, pencarian file itu di disk, lalu pemeriksaan isi dan perilaku binary-nya.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/references/live-response.md` | 386 baris: Decision Frame 5 butir, aturan main (root, UTC, output ke file), rantai proses → file → isi (`Lacak File yang Dijalankan`, `Temukan File di Disk`, `Periksa Isi & Perilaku File`), cron/penjadwal semua user, koneksi keluar, indikator, tabel false positive per bagian, batas tiap teknik, urutan eksekusi 10 menit, higiene bukti, padanan Windows, referensi terkait, Best Practices | tiga pemeriksaan yang diminta belum punya perintah, cara baca hasil, maupun batas false positive di skill mana pun; ditambah kebutuhan menelusuri file yang dieksekusi sebuah proses sampai isi binary-nya | paritas kolom 6 tabel diverifikasi skrip Node (0 temuan); 5 tautan relatif diuji `Test-Path` |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-ir-200/SKILL.md` | baris baru di tabel "How to Use This Skill": `Triage a live host (processes, cron, outbound connections)` → `references/live-response.md` | referensi harus dapat ditemukan dari SKILL.md | `Test-Path` pada target tautan: `True` |
| `docs/SKILL-QUALITY.md` | kolom Refs `offsec-ir-200` 7 → 8; baris "Diperbarui" menyebut 0.13.0 | jumlah berkas `references/` bertambah satu | `(Get-ChildItem skills/offsec-ir-200/references -Filter *.md).Count` = 8 |
| `skills/index.json` | daftar berkas `offsec-ir-200` bertambah `references/live-response.md` | indeks harus mencerminkan berkas yang dapat dimuat | `node scripts/sync-skills.js` |

### Catatan

Perintah ditulis dari dokumentasi tooling standar (procps, iproute2, util-linux, cron, systemd) dan belum dijalankan terhadap host target sungguhan. Semua perintah bersifat baca-saja, kecuali penulisan output ke direktori kerja yang diperintahkan secara eksplisit di dalam referensi.

## [0.12.0] — 2026-11-09 — CPENT: persona praktisi, bukan persiapan ujian

**Commit dasar:** `122ffa1` (branch `dev`)
**Status:** committed in `87500a8`
**Ruang lingkup:** permintaan langsung — skill `cpent` diposisikan sebagai **persona pengguna yang sudah memegang EC-Council CPENT**: profil, gaya bicara, preferensi, batas klaim, **aturan mengikat R1–R6**, **dua belas hukum mindset**, **prosedur Burp yang disiplin**, **manipulasi header (XFF, User-Agent, Host, injeksi)**, **bypass WAF dan encoding**, dan doktrin kerja praktisi. Seluruh angka ujian, struktur soal, zona, jadwal, dan bobot report dihapus.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/cpent/references/waf-evasion.md` | 194 baris: tiga pertanyaan sebelum bypass, tabel identifikasi WAF, bypass header (case/spasi/duplikasi, Content-Type/charset, path override, HTTP/2), tabel encoding berlapis, fragmentasi SQLi/XSS/CMDi/traversal, smuggling sebagai bypass, alur Burp (Hackvertor, Turbo Intruder, Collaborator), tabel bukti vs status code, batas etika, tujuh jebakan; menautkan skill `waf-evasion-methodology` | permintaan lanjutan — persona perlu prosedur bypass WAF dan encoding header yang bisa dipertanggungjawabkan | 0 tautan rusak |
| `skills/cpent/references/header-manipulation.md` | 192 baris: empat kondisi header menjadi vektor, tabel 15 header + hipotesis, pola payload (IP spoofing, XSS, CMDi, SQLi, CRLF, Host poisoning), request smuggling, alur Burp, tabel verifikasi vs false positive, pemetaan CWE, batas etika, tujuh jebakan; penunjuk ke `waf-evasion.md` | permintaan lanjutan — manipulasi header (XFF, User-Agent, injeksi) adalah kerja harian di Burp dan belum punya prosedur | 0 tautan rusak |
| `skills/cpent/references/burp-workflow.md` | 132 baris: prinsip, delapan langkah konfigurasi (scope, listener, TLS, profil browser, project, sesi, intercept, match/replace), alur history→Repeater→Intruder→scanner, tabel tipe Intruder, Collaborator/OOB, triage scanner, lima ekstensi minimum, §12 manipulasi header, disiplin bukti dan data, kapan tidak memakai Burp, tujuh jebakan | permintaan lanjutan — persona perlu prosedur Burp yang disiplin, bukan sekadar menyebut tool | 0 tautan rusak |
| `skills/cpent/references/mindset.md` | 71 baris: dua belas hukum (objective, graf, bukti, biaya, asumsi, peta, kredensial, topologi, noise, berhenti, keheningan, penjelasan), enam refleks, lima pertanyaan wajib, hubungan hukum versus preferensi | permintaan lanjutan — agent butuh mindset tegas yang bisa dipakai membenarkan atau membatalkan langkah | 0 tautan rusak |
| `skills/cpent/references/rules.md` | 94 baris: hierarki kewenangan, tabel R1–R6 (otorisasi, bukti, eksekusi, kedalaman, persona, kebersihan) dengan konsekuensi per aturan, penegakan tiga pemeriksaan | aturan harus mengikat dan dapat diaudit lewat ID, bukan tersebar sebagai saran | 0 tautan rusak |
| `skills/cpent/references/expert-reasoning.md` | 155 baris: target sebagai graf, empat pertanyaan sebelum aksi, tabel ekonomi eksploitasi, register asumsi, siklus hipotesis, anggaran noise, pustaka 20 pola, triage 60 detik, tujuh anti-pattern, aturan berhenti, pertanyaan pra-engagement | agent harus berpikir seperti operator berpengalaman, bukan menjalankan checklist | 0 tautan rusak |
| `skills/cpent/references/decision-trees.md` | 141 baris: delapan pohon keputusan (Windows, Linux, web→RCE, jalur AD, eskalasi vs lateral, pemilihan tunnel, go/no-go binary, OT) dan aturan berhenti | keputusan lapangan butuh bentuk yang bisa diikuti saat informasi belum lengkap | 0 tautan rusak |
| `skills/cpent/references/field-diagnostics.md` | 73 baris: tabel 19 gejala → penyebab → cek → tindakan, cara membaca keheningan, stabilisasi shell, lima prinsip diagnosis | kegagalan tool adalah titik paling sering menghabiskan waktu; perlu prosedur diagnosis | 0 tautan rusak |
| `skills/cpent/references/reasoning-examples.md` | 98 baris: empat skenario dengan penalaran orang pertama dan kontras respons junior (scan tanpa web, upload vs LFI vs IDOR, dua hop pivot, kerberoast vs ADCS) | contoh penalaran mengajarkan prioritas lebih baik daripada daftar aturan | 0 tautan rusak |
| `skills/cpent/references/persona.md` | 115 baris: profil peran, kedalaman pengetahuan, tujuh kebiasaan berpikir, aturan voice, tabel preferensi, batas klaim, tiga contoh jawaban orang pertama; tautan ke referensi penalaran | inti permintaan — agent harus memerankan pengguna bersertifikat, bukan sekadar menguasai materi | 0 tautan rusak; contoh jawaban adalah ilustrasi, bukan transkrip |
| `skills/cpent/references/engagement-playbook.md` | 106 baris: scoping, rules of engagement, fase kerja, disiplin bukti, kriteria berhenti, eskalasi temuan kritis, metrik kedalaman, anatomi deliverable | pengganti `exam-structure.md`; operator butuh aturan kontrak, bukan aturan ujian | 0 tautan rusak; link checker PowerShell atas seluruh folder |
| `skills/cpent/references/network-topologies.md` | 126 baris: enam arketipe segmen, discovery per host baru, deteksi dual-homed, bukti reachability, pemilihan tunnel, peta kedalaman, level Purdue, enam jebakan | pengganti `exam-zones.md`; pertanyaan sebenarnya "segmen mana yang dapat dijangkau", bukan "zona ujian mana" | 0 tautan rusak |
| `skills/cpent/references/capability-domains.md` | 59 baris: tabel 14 domain kapabilitas beserta bukti khas, kelompok kerja, cara memakai peta | pengganti `modules-overview.md`; silabus kursus diganti peta kompetensi praktisi | 0 tautan rusak |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/cpent/SKILL.md` | 134 → 208 baris; deskripsi frontmatter menyebut aturan dan mindset; bagian baru `## Profil Persona`, `## Cara Memerankan Persona`, `## Dua Belas Hukum Mindset`, `## Aturan Wajib` (10 aturan dengan konsekuensi), dan `## Siklus Kerja`; Decision Frame disederhanakan menjadi 5 keputusan; `## Persona Contract` dan `## Operating Doctrine` dihapus karena diserap ke `rules.md` dan `mindset.md`; 21 baris referensi termasuk Burp, header, dan WAF | aturan dan mindset harus menjadi lapisan pertama yang dibaca agent, bukan catatan kaki | 21 tautan referensi diuji dengan `Test-Path`; heading `## ` dihitung ulang |
| `skills/cpent/references/windows-attacks.md` | 60 → 128 baris: rantai AD, delegasi, ADCS ESC1–ESC8, DCSync, relay/coercion, tabel telemetri deteksi | konten lama membandingkan dengan ujian dan tidak memuat ADCS/delegasi | 0 tautan rusak |
| `skills/cpent/references/linux-attacks.md` | 43 → 101 baris: jalur eskalasi konfigurasi, tabel kernel CVE, persistence terkendali, container escape | menghapus klaim "kernel exploit boleh karena environment ujian stabil" | 0 tautan rusak |
| `skills/cpent/references/web-exploitation.md` | 36 → 125 baris: urutan map→confirm→exploit→evidence, header sebagai permukaan (penunjuk `header-manipulation.md`), uji perilaku WAF (penunjuk `waf-evasion.md`), batas otomatisasi, API, bukti minimum, penunjuk ke `burp-workflow.md` | menghapus frasa "tidak ada batasan tool"; engagement nyata punya rate limit dan data klien | 0 tautan rusak |
| `skills/cpent/references/binary-exploitation.md` | 40 → 92 baris: 7 langkah x86, tabel perbedaan x64, bypass proteksi, SEH, tooling, risiko crash | menghapus klaim "pembeda dari sertifikasi lain" dan arahan "pelajari sebelum exam" | 0 tautan rusak |
| `skills/cpent/references/wireless-iot-scada.md` | 49 → 99 baris: tabel wireless, IoT, tabel protokol OT, aturan keselamatan read-only, pivot dari perangkat | label "Modul 9–11" dan arahan "sebelum exam" dihapus; OT butuh aturan keselamatan | 0 tautan rusak |
| `skills/cpent/references/pivoting-report.md` | 61 → 125 baris: double pivot, Ligolo-ng/Chisel/SSH, peta serangan, struktur laporan, bukti yang diterima, kualitas temuan | menghapus "~30% nilai" dan deadline ujian; laporan diposisikan sebagai deliverable klien | pencarian `30%` dan `deadline` di folder skill: 0 hasil |
| `skills/cpent/references/tools-matrix.md` | 51 → 86 baris: tool per fase, binary statis, wordlist, pemilihan tool berdasarkan kendala, higiene tool; baris Burp menunjuk `burp-workflow.md`, baris HTTP Request Smuggler/Turbo Intruder, WAFW00F/whatwaf, dan Hackvertor | menghapus arahan "siapkan sebelum exam"; diganti field kit engagement | 0 tautan rusak |
| `skills/cpent/references/referensi.md` | 50 → 92 baris: standar metodologi, AD, binary, pivot, web, IoT/OT, lab, komunitas, tautan internal (mindset, rules, Burp, header, WAF, persona, empat referensi penalaran) dan tautan ke skill `waf-evasion-methodology` | blueprint ujian diganti sumber praktik dan tautan ke skill lain | tautan internal menunjuk skill yang ada |
| `scripts/check-fact-notes.js` | entri `"cpent": "sertifikasi"` dihapus dari `EXPECTED` | skill tidak lagi memuat angka ujian sehingga tidak lagi fact-bearing | `node scripts/check-fact-notes.js` |
| `README.md` | baris 158 (deskripsi) dan 275 (sumber) diperbarui | deskripsi lama menyebut "CPENT exam" dan "LPT Master pathway" | dicocokkan dengan frontmatter |
| `docs/SKILL-QUALITY.md` | baris `cpent`: Trigger `—` → `ya`, Provenance `ya` → `—`, Status `Selesai` → `Sebagian`; ringkasan 12/6/10 → 11/7/10; catatan provenance; tanggal | skill dengan persona tidak punya angka ujian untuk dilacak | dihitung ulang dari matriks |
| `manifest.json` | deskripsi dan keywords `cpent` diperbarui | bersumber dari frontmatter | `node scripts/sync-skills.js` |
| `skills/index.json` | daftar berkas `cpent` menjadi 22 entri dengan 13 nama baru | indeks harus mencerminkan berkas yang dapat dimuat | idem |

### Diganti nama

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/cpent/references/exam-structure.md` | dihapus; isi diganti `skills/cpent/references/engagement-playbook.md` | nama lama menyiratkan persiapan ujian | `git status` menampilkan `D` untuk path lama |
| `skills/cpent/references/exam-zones.md` | dihapus; isi diganti `skills/cpent/references/network-topologies.md` | idem | idem |
| `skills/cpent/references/modules-overview.md` | dihapus; isi diganti `skills/cpent/references/capability-domains.md` | idem | idem |

### Catatan

Isi baru adalah doktrin dan prosedur, bukan hasil engagement nyata. Tidak ada target sungguhan yang diuji pada perubahan ini; contoh command ditulis dari pengetahuan tooling dan belum dijalankan pada host target.

`README.md` sudah masuk ke commit `dd8cfd3` — sesi paralel yang mengerjakan `web-reconnaissance` men-stage working tree yang sama. `docs/SKILL-QUALITY.md` ikut commit itu untuk perubahan pertama, lalu diperbarui lagi di working tree ini (Refs `cpent` 11 → 12) ketika `persona.md` ditambahkan.

`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` ditulis ulang generator dengan isi identik, sehingga tidak muncul di `git status`.

## [0.11.1] — 2026-11-09 — Perbaikan tabel: pipe tak ter-escape menggeser kolom

**Commit dasar:** `122ffa1` (branch `dev`)
**Status:** committed in `4250b37`
**Ruang lingkup:** delapan baris tabel di lima berkas berisi karakter `|` tanpa escape, atau kekurangan satu sel. Pada renderer markdown, pipe di dalam sel memotong baris menjadi kolom tambahan sehingga isi sel bergeser — persis gejala yang terlihat pada laporan pengguna.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-pentest-payloads/references/command-injection.md` | tiga baris: `` `\|id` ``, `echo aWQ=\|base64 -d\|sh`, dan `` `\|` `` di sel pembatas — seluruh pipe di dalam sel di-escape | baris ke-17 terbaca 3 sel, ke-92 terbaca 4 sel, dan ke-95 terbaca 3 sel pada tabel dua kolom | pemindai tabel: 0 temuan setelah perbaikan |
| `skills/web-pentest-payloads/references/ldap-xpath-injection.md` | dua baris: pipe di dalam payload LDAP di-escape menjadi `\|` | tabel dua kolom terbaca empat sel karena payload memuat tanda kurung dan karakter pipe | idem |
| `skills/web-pentest-payloads/references/ssti.md` | satu baris: Handlebars `as \|string\|` — pipe di-escape | payload `\|string\|` memotong baris menjadi empat sel pada tabel dua kolom | idem |
| `skills/web-pentest-payloads/references/payload-encoding-evasion.md` | satu baris: sel "Encoding" yang hilang diisi "entity tanpa titik koma" | baris ke-28 hanya punya dua sel pada tabel tiga kolom, sehingga contoh `&#60script` jatuh ke kolom yang salah | idem |
| `skills/waf-evasion-methodology/references/evasion-techniques.md` | satu baris: `` `\|\| 1=1` `` — pipe ganda di-escape | `OR 1=1` → `\|\| 1=1` terbaca empat sel pada tabel dua kolom | idem |

### Catatan

Bug ini ditemukan dengan memeriksa seluruh 207 berkas markdown (skills, docs, README, CHANGELOG) memakai skrip sementara yang mendeteksi baris tabel dengan jumlah sel berbeda dari header, judul markdown di dalam sel, dan baris tabel tanpa blank line sesudahnya. Hasil awal: 8 temuan, semuanya "ragged row"; setelah perbaikan: 0 temuan. Tidak ada judul markdown di dalam sel dan tidak ada tabel yang menempel ke heading tanpa baris kosong.

Gambar yang dilaporkan pengguna **bukan berasal dari repo ini**: teks "What problem does it solve?" dan "SYSTEM DOCUMENTATION & REQUIREMENTS" tidak ada di working tree, tidak ada di seluruh riwayat git (`git log -S`), dan tidak ada di berkas sesi DSH tiga hari terakhir. Gejala pada gambar itu — `## Quick Start` dan tanda `-` tercetak harfiah di dalam sel — disebabkan isi markdown dimasukkan mentah ke sel tabel oleh alat pembuat dokumen, bukan oleh markdown repo ini.

Teks `â†’` yang muncul di konsol bukan kerusakan berkas: shell pada mesin ini PowerShell 5.1 yang membaca UTF-8 sebagai cp1252. Berkasnya berisi U+2192 yang sah; pemindaian dengan pembaca UTF-8 menemukan nol urutan mojibake di seluruh repo.

## [0.11.0] — 2026-11-09 — Web reconnaissance: fingerprint teknologi berkeyakinan

**Commit dasar:** `8ff2289` (branch `dev`)
**Status:** committed in `dd8cfd3`
**Ruang lingkup:** permintaan langsung — fase reconnaissance juga harus mencari informasi teknologi yang dipakai target. Sebelumnya bagian teknologi hanya tabel enam sinyal tanpa metode, tanpa cara mengambil versi, dan tanpa pembeda antara yang terbukti dan yang ditebak.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/references/technology-fingerprinting.md` | 219 baris: empat lapis (infrastruktur, server dan bahasa, framework frontend, pihak ketiga), tabel 20 header dan artinya, tabel cookie ke stack, jalur aset per build tool, ekstraksi versi (banner lisensi, konstanta, atribut `ng-version`, source map, `package.json` terpapar), TLS dan CT logs, tanda halaman error, kolom keyakinan tiga tingkat, alur versi ke CVE, tabel tujuh batas, sepuluh jebakan | versi tanpa keyakinan adalah dasar CVE yang tidak bisa dipertanggungjawabkan; skill hanya menyebut `Server` dan `X-Powered-By` sebagai sinyal tanpa menjelaskan bahwa keduanya dapat dipalsukan dan ditimpa CDN | 0 tautan rusak; tabel disusun dari pengetahuan ekosistem, bukan dari pengukuran target nyata |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/SKILL.md` | 250 → 270 baris; deskripsi frontmatter menyebut identifikasi teknologi dan versi beserta keyakinannya; `## Decision Frame` butir keenam menjadi "Inventaris, keyakinan, dan status" yang mencakup rute, endpoint, dan teknologi (2 sinyal independen atau ditandai terduga); `## 9. Teknologi, Versi, dan CVE` dipecah menjadi `## 9. Identifikasi Teknologi dan Versi` (tabel empat lapis + perintah pengambilan versi + aturan keyakinan) dan `## 10. CVE yang Relevan`; Gotchas 18 → 21 butir; baris Teknologi pada template output menyebut tingkat keyakinan; indeks 9 referensi | satu tabel enam baris tidak cukup untuk menampung empat lapis fingerprinting, dan CVE butuh aturan sendiri karena hanya boleh didasarkan pada keyakinan tinggi | heading `## ` 13 → 14; butir Decision Frame 7; butir Gotchas 21; berkas di `references/` 8 → 9; baris tabel referensi 9 |
| `skills/web-reconnaissance/references/js-chunk-analysis.md` | 211 baris (jumlah tetap, isi blockquote diperluas); penunjuk ke `technology-fingerprinting.md` untuk pembacaan versi dari banner lisensi dan source map | versi paling sering terbaca justru saat analisis bundle, bukan di langkah terpisah | 0 tautan rusak |

### Artefak turunan dan dokumentasi

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | deskripsi `web-reconnaissance` diperbarui | deskripsi bersumber dari frontmatter `SKILL.md` | `node scripts/sync-skills.js` |
| `skills/index.json` | deskripsi dan daftar `files` diperbarui menjadi 10 entri | indeks harus mencantumkan berkas yang dapat dimuat | idem |
| `README.md` | baris 164 diperbarui | deskripsi lama hanya menyebut "teknologi" tanpa versi dan keyakinan | dicocokkan dengan frontmatter |
| `docs/SKILL-QUALITY.md` | kolom Refs baris `web-reconnaissance` 8 → 9; tanggal dan catatan provenance | ledger harus mencerminkan jumlah referensi sebenarnya | dihitung ulang dari isi `references/` |

`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` ditulis ulang generator dengan isi identik, sehingga tidak muncul di `git status`.

### Catatan

Referensi baru ini adalah **prosedur dan tabel rujukan**, bukan hasil pengukuran. Tidak ada satu pun target yang di-fingerprint pada perubahan ini: tabel header, cookie, jalur aset, dan tanda halaman error disusun dari pengetahuan ekosistem, bukan dari pengamatan aplikasi sungguhan.

Sembilan blok JavaScript yang sudah ada tetap lolos uji parse dengan `new Function`; referensi baru tidak memuat blok JavaScript, hanya blok `bash`. MCP `chrome-devtools-mcp` tetap tidak terpasang di mesin ini.

## [0.10.0] — 2026-11-09 — Web reconnaissance: alur data, peta arsitektur, dan konfigurasi auth

**Commit dasar:** `11d94c9` (branch `dev`)
**Status:** committed in `ef7e325`
**Ruang lingkup:** permintaan langsung — fase reconnaissance juga harus bisa (1) membaca alur data aplikasi dari chunk JS, (2) mencari seluruh endpoint lalu memetakan arsitektur URL frontend dan REST API backend, dan (3) melihat konfigurasi autentikasinya seperti JWT atau cookie.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/references/data-flow-analysis.md` | 205 baris: tiga tingkat kedalaman (statis, semi-statis, dinamis), pencarian lapisan API client dan interceptor, pembacaan graf modul webpack, pola pemuatan data per framework, pemetaan state, logpoint dan instrumentasi `fetch`/`XHR` lewat `evaluate_script`, tabel alur, jalur source ke sink, aturan berhenti tiga hop, delapan jebakan | sebelumnya skill hanya bisa menjawab "endpoint apa yang ada", bukan "aksi UI mana memanggil endpoint mana"; tanpa itu daftar endpoint tidak bisa diprioritaskan | blok JavaScript instrumentasi lolos uji parse dengan `new Function`; 0 tautan rusak |
| `skills/web-reconnaissance/references/architecture-mapping.md` | 186 baris: peta rute frontend per framework (React Router v5/v6, Next.js Pages dan App Router, Nuxt, Angular, SvelteKit, Vue Router), rute berpagar peran, arsitektur URL (host, versi, locale, tenant, hash route), sumber endpoint backend, normalisasi path, tabel inventaris API, gabungan rute ke endpoint, diagram, pernyataan cakupan | skill sebelumnya punya matriks endpoint tanpa peta rute dan tanpa normalisasi, sehingga jumlah endpoint tidak bisa dipertanggungjawabkan | 0 tautan rusak; tabel dan contoh normalisasi diperiksa manual |
| `skills/web-reconnaissance/references/auth-configuration.md` | 200 baris: deteksi skema, klaim JWT yang dicatat, perilaku cookie (rotasi, pencabutan, prefiks), alur OAuth2/OIDC dan SAML, perbandingan sesi dan token, pola CSRF, MFA, mesin keadaan autentikasi, tabel observasi ke prioritas, delapan jebakan | skill hanya menyebut token di storage; tidak ada cara membaca skema, alur refresh, atau pencabutan sesi | 0 tautan rusak; klaim yang tidak dapat disimpulkan dari recon ditandai eksplisit |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/SKILL.md` | 195 → 250 baris; deskripsi frontmatter menambah alur data, peta arsitektur, dan auth; paragraf pembuka menunjuk tiga artefak; `## Decision Frame` 6 → 7 keputusan (kedalaman alur data, peta arsitektur dan status endpoint digabung); bagian baru `## 5. Alur Data` dan `## 7. Konfigurasi Autentikasi`; `## 6. Petakan dan Uji Endpoint` menjadi `## 8. Peta Arsitektur` dengan aturan normalisasi dan pernyataan cakupan; teknologi dan CVE digabung menjadi `## 9`; Gotchas 15 → 18; template output menambah peta rute, peta API, alur data, konfigurasi auth, dan cakupan; indeks 8 referensi | kebutuhan baru tidak cukup ditampung dengan menambah butir; strukturnya harus berubah agar alur data dan peta arsitektur punya tempat sendiri | heading `## ` 12 → 13; butir Decision Frame 7; butir Gotchas 18; berkas di `references/` 5 → 8; baris tabel referensi 8 |
| `skills/web-reconnaissance/references/js-chunk-analysis.md` | 209 → 211 baris; blockquote penunjuk ke `data-flow-analysis.md` dan `architecture-mapping.md` | analisis isi bundle adalah titik masuk alur data, bukan tujuan akhir | 0 tautan rusak |
| `skills/web-reconnaissance/references/browser-storage.md` | 234 → 236 baris; blockquote penunjuk ke `auth-configuration.md` | storage menjawab "di mana", bukan "bagaimana skemanya bekerja" | 0 tautan rusak |
| `skills/web-reconnaissance/references/chrome-devtools-mcp.md` | 190 → 192 baris; penunjuk ke `data-flow-analysis.md` pada bagian logpoint | logpoint adalah alat utama konfirmasi alur, bukan sekadar pengambilan data | 0 tautan rusak |
| `skills/web-reconnaissance/references/network-analysis.md` | 199 baris (jumlah baris tetap, isi blockquote diperluas); penunjuk ke `architecture-mapping.md` dan `auth-configuration.md` | traffic adalah bahan mentah kedua peta tersebut | 0 tautan rusak |

### Artefak turunan dan dokumentasi

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | deskripsi `web-reconnaissance` diperbarui | deskripsi bersumber dari frontmatter `SKILL.md` | `node scripts/sync-skills.js` |
| `skills/index.json` | deskripsi dan daftar `files` diperbarui menjadi 9 entri | indeks harus mencantumkan berkas yang dapat dimuat | idem |
| `README.md` | baris 164 diperbarui | deskripsi lama belum menyebut alur data, peta arsitektur, dan auth | dicocokkan dengan frontmatter |
| `docs/SKILL-QUALITY.md` | kolom Refs baris `web-reconnaissance` 5 → 8; tanggal dan catatan provenance | ledger harus mencerminkan jumlah referensi sebenarnya | dihitung ulang dari isi `references/` |

`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` ditulis ulang generator dengan isi identik, sehingga tidak muncul di `git status`.

### Catatan

Ketiga referensi baru adalah **prosedur**, bukan hasil eksekusi. Tidak ada aplikasi nyata yang dipetakan pada perubahan ini: peta rute, peta API, alur data, dan alur autentikasi belum pernah dijalankan pada target sungguhan. Pola per framework ditulis dari pengetahuan umum ekosistem, bukan dari verifikasi terhadap aplikasi berjalan.

Sembilan blok JavaScript di seluruh folder skill lolos uji **parse** dengan `new Function`; tidak ada yang dijalankan di halaman. MCP `chrome-devtools-mcp` tetap tidak terpasang di mesin ini, sehingga `evaluate_script`, `set_logpoints`, dan instrumentasi `fetch` belum pernah dipakai sungguhan.

### Koreksi metode hitung

Entri [0.9.0] menulis "155 → 196 baris" untuk `skills/web-reconnaissance/SKILL.md`. Dengan metode yang dipakai entri ini — baris terakhir yang diakhiri newline tidak dihitung sebagai baris tambahan — berkas yang sama berukuran **195 baris** setelah 0.9.0 dan **250 baris** sekarang. Selisih satu itu berasal dari perbedaan cara menghitung, bukan dari perubahan berkas; angka pada entri 0.9.0 tidak diubah.

## [0.9.1] — 2026-11-09 — Koreksi hitungan pada entri 0.9.0

**Commit dasar:** `660a253` (branch `dev`)
**Status:** committed in `4ae7335`
**Ruang lingkup:** dua angka pada entri [0.9.0] tidak cocok dengan isi berkasnya. Tidak ada berkas skill yang berubah; hanya entri koreksi ini yang ditambahkan.

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `CHANGELOG.md` | entri 0.9.0 menyebut "tabel 14 tool relevan" pada `chrome-devtools-mcp.md` dan "sembilan jebakan" pada `browser-storage.md`; angka yang benar adalah **15 baris tool** dan **8 butir jebakan** | keduanya ditulis tanpa dihitung ulang dari berkas, padahal kolom Verifikasi mensyaratkan pemeriksaan yang benar-benar dijalankan | hitung ulang: tabel pada `## 2. Tool yang Relevan untuk Recon` = 16 baris termasuk header, jadi 15 baris tool; butir pada `## 9. Jebakan` = 8 |

Angka lain pada 0.9.0 — 234 dan 190 baris, lima flag, lima alur, tujuh batas, 155 → 196 baris, heading 11 → 12, Gotchas 9 → 15, Refs 3 → 5 — sudah dihitung dari berkas dan tidak berubah.

## [0.9.0] — 2026-11-09 — Web reconnaissance: storage browser dan Chrome DevTools MCP

**Commit dasar:** `e0567ba` (branch `dev`)
**Status:** committed in `000b60c`
**Ruang lingkup:** permintaan langsung — fase reconnaissance harus benar-benar bisa (1) membaca chunk JS, (2) membaca storage yang ada di browser, dan (3) membaca network tab lewat MCP Chrome DevTools untuk menyadap seluruh informasi situs. Sebelumnya skill hanya menyebut storage dalam satu blok `console.log` dan tidak punya cara merekam apa pun secara otomatis.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/references/browser-storage.md` | 234 baris: tabel enam storage dan tiga tempat lain (service worker, `window.name`, WebSQL), satu skrip dump yang aman untuk `evaluate_script`, empat lokasi kebenaran cookie, pembacaan IndexedDB per object store, Cache Storage, OPFS, triage lima jenis token, decode JWT tanpa verifikasi, pemetaan storage ke temuan, aturan redaksi, sembilan jebakan | `document.cookie` hanya membaca cookie non-`HttpOnly`, dan skrip lama tidak menyentuh IndexedDB maupun Cache Storage — dua tempat yang paling sering memuat data pengguna lain | lima blok JavaScript lolos uji parse dengan `new Function`; 0 tautan rusak |
| `skills/web-reconnaissance/references/chrome-devtools-mcp.md` | 190 baris: konfigurasi MCP dan lima flag, tabel 14 tool relevan beserta parameter, lima alur kerja (rekam traffic, dump storage, kumpulkan chunk, sesi terautentikasi, logpoint lewat source map), tabel tujuh batas, fallback manual, checklist | skill hanya menjelaskan DevTools manual; tidak ada cara memfilter per tipe resource, menyimpan body ke disk, atau menyisipkan header auth secara berulang | nama tool dan parameter dicocokkan satu per satu dengan `docs/tool-reference.md` paket `chrome-devtools-mcp` (diakses 2026-11-09); MCP tidak terpasang di mesin ini sehingga tidak ada alur yang dieksekusi |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/SKILL.md` | 155 → 196 baris; deskripsi frontmatter menyebut MCP dan storage; tabel pembuka 3 → 4 sumber; `## Decision Frame` tetap 6 keputusan dengan dua yang baru (MCP vs manual, kedalaman pembacaan storage); bagian baru `## 1. Siapkan Sesi`; `## 5. Storage, Token, dan Sesi` ditulis ulang (tabel enam storage, tiga pemeriksaan sinkron, aturan `HttpOnly`); Gotchas 9 → 15 butir; template output menambah baris alat capture dan storage; indeks 5 referensi | bagian storage sebelumnya hanya tiga butir dan satu `console.log`; tidak ada panduan kapan memakai MCP dan kapan harus manual | heading `## ` 11 → 12; butir Decision Frame 6; butir Gotchas 9 → 15; berkas di `references/` 3 → 5 |
| `skills/web-reconnaissance/references/js-chunk-discovery.md` | 215 → 216 baris; urutan kerja 3 → 4 langkah dengan penunjuk ke MCP dan browser-storage | langkah penemuan chunk tidak menyebut jalan otomatis maupun kelanjutan ke pembacaan storage | 0 tautan rusak |
| `skills/web-reconnaissance/references/network-analysis.md` | 197 → 199 baris; blockquote penunjuk ke `chrome-devtools-mcp.md` dan `browser-storage.md` | pembaca perlu tahu prosedur ini manual dan ada padanan otomatisnya | 0 tautan rusak |

### Artefak turunan dan dokumentasi

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | deskripsi `web-reconnaissance` diperbarui | deskripsi bersumber dari frontmatter `SKILL.md` | `node scripts/sync-skills.js` |
| `skills/index.json` | deskripsi diperbarui; daftar `files` memuat `browser-storage.md` dan `chrome-devtools-mcp.md` | indeks harus mencantumkan berkas yang dapat dimuat | idem — `files` kini 6 entri |
| `README.md` | baris 164 diperbarui | deskripsi lama tidak menyebut storage browser maupun MCP | dicocokkan dengan frontmatter |
| `docs/SKILL-QUALITY.md` | kolom Refs baris `web-reconnaissance` 3 → 5; tanggal dan catatan provenance | ledger harus mencerminkan jumlah referensi sebenarnya | dihitung ulang dari isi `references/` |

`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` ditulis ulang generator dengan isi identik, sehingga tidak muncul di `git status`.

### Catatan

MCP `chrome-devtools-mcp` **tidak terpasang** di mesin ini dan tidak ada satu pun tool `list_network_requests` atau `evaluate_script` yang tersedia. Seluruh alur di `chrome-devtools-mcp.md` karena itu **belum pernah dijalankan** — bukan "sudah diuji". Nama tool, parameter, dan flag disalin dari `docs/tool-reference.md` dan README paket tersebut pada 2026-11-09; dokumen itu sendiri menyuruh memeriksa ulang setelah upgrade karena nama tool berubah antar versi.

Lima blok JavaScript di `browser-storage.md` lolos uji **parse** dengan `new Function`, bukan uji jalan. Tidak ada browser yang dibuka dan tidak ada storage nyata yang dibaca.

Angka 90 menit, dua varian path, dan tiga navigasi preserved adalah aturan prosedur di skill ini, bukan hasil pengukuran.

## [0.8.0] — 2026-11-09 — Reporting dan web assessment: template nyata, frame, dan gotchas

**Commit dasar:** `659d5ab` (branch `dev`)
**Status:** committed in `f3c7ec7`
**Ruang lingkup:** dua skill backlog D yang berpasangan dalam satu alur kerja — `web-app-scan` menghasilkan temuan, `security-documentation` menuliskannya. Keduanya sebelumnya tanpa Decision Frame dan tanpa Gotchas.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/security-documentation/assets/report-template.tex` | template LaTeX 123 baris: paket, badge severity (`\riskcritical` sampai `\riskinfo`), `longtable` metadata temuan, kerangka enam bagian, `\graphicspath`, perintah compile 3 pass | SKILL.md menyuruh "mengikuti template `docs/laporan.txt`" tetapi berkas itu tidak ada di repo; skill juga tidak membawa template apa pun sehingga tidak bisa dipakai setelah di-install | `Test-Path docs/laporan.txt` = `False`; berkas kini berada di dalam folder skill sehingga ikut tersalin saat instalasi |
| `skills/security-documentation/references/finding-writeup.md` | anatomi 7 bagian temuan, tabel 6 vektor CVSS v3.1 lazim, tabel 16 pemetaan CWE, pola `curl` reproducible, tabel "bukti cukup vs tidak cukup", aturan redaksi, 6 anti-pola | standar penulisan temuan sebelumnya hanya 4 butir; tidak ada cara memilih vektor CVSS maupun membedakan bukti kuat dari lemah | skor vektor dicek terhadap nilai kanonik (9.8 / 8.8 / 7.5 / 6.5 / 6.1 / 5.3); dokumen tetap memerintahkan hitung ulang dengan kalkulator resmi |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/security-documentation/SKILL.md` | rujukan `docs/laporan.txt` (3 tempat) diganti ke `assets/report-template.tex` dan `references/finding-writeup.md`; `## Decision Frame` 6 keputusan; `## Gotchas` 9 butir; bagian duplikat dihapus; alur kerja dan indeks referensi ditambahkan | berkas 117 baris ini memuat "LaTeX Conventions", "CVSS Scoring Standards", dan "Prioritas Rekomendasi" **dua kali** (satu sebagai `###`, satu sebagai `##`), tanpa frame, tanpa gotchas, dan menunjuk berkas yang tidak ada | `Select-String '^#+ (Konvensi LaTeX\|LaTeX Conventions\|CVSS\|Prioritas)'` = 3 hasil (sebelumnya 6); `Select-String 'laporan.txt'` = 0 |
| `skills/web-app-scan/SKILL.md` | `## Decision Frame` 6 keputusan (izin, mode read-only, konfirmasi temuan, batas 2 varian, laju permintaan, cakupan terautentikasi); `## Gotchas` 9 butir; enam fase dirapikan; template output ditambah kolom Mode/Cakupan dan bagian "Tidak tereproduksi"; severity contoh diperbaiki (cookie tanpa HttpOnly → Medium) | prosedur 6 fase ada, tetapi tidak menjelaskan kapan berhenti, bagaimana membedakan kandidat dari temuan, atau bahwa header hilang bukan High | severity contoh dicocokkan dengan CWE-1004 di `references/finding-writeup.md` |

### Artefak turunan dan dokumentasi

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | deskripsi `security-documentation` dan `web-app-scan` diperbarui | deskripsi bersumber dari frontmatter `SKILL.md` | `node scripts/sync-skills.js` |
| `skills/index.json` | dua deskripsi + `files` memuat template `.tex` dan `finding-writeup.md` | indeks harus mencantumkan berkas yang dapat dimuat | idem — 8 baris berubah |
| `README.md` | baris 163 (`web-app-scan`) dan 176 (`security-documentation`) diperbarui | deskripsi lama tidak menyebut batas mode maupun template | dicocokkan dengan isi SKILL.md baru |
| `docs/SKILL-QUALITY.md` | dua baris matriks → Sebagian; ringkasan Sebagian 4→6, Belum 12→10; paragraf provenance; backlog D menyisakan 4 skill; tanggal | ledger harus mencerminkan kondisi setelah 0.8.0 | dihitung ulang: Frame 18/28, Refs 18/28 |

`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` ditulis ulang generator dengan isi identik, sehingga tidak muncul di `git status`.

### Catatan

Template LaTeX **belum dikompilasi** di mesin ini — `pdflatex`, `xelatex`, `latexmk`, dan `tectonic` semuanya tidak terpasang. Kerangka ditulis mengikuti konvensi paket yang dipakai skill, tetapi kebenaran kompilasi harus diverifikasi di lingkungan yang memiliki TeX Live.

Backlog D menyisakan empat skill: `threat-modeling`, `incident-response-plan`, `owasp-top10-2025`, `risk-management-framework`. Backlog C (lima skill monolitik), poin E (fact sheet standar non-sertifikasi), dan poin F (harness evaluasi) belum disentuh.

## [0.7.0] — 2026-11-09 — Web reconnaissance: chunk JS, traffic network, dan analisis bundle

**Commit dasar:** `8a76c3c` (branch `dev`)
**Status:** committed in `eeb49aa`
**Ruang lingkup:** permintaan langsung — `web-reconnaissance` harus benar-benar menjelaskan cara menemukan dan membaca chunk JS, cara membaca network situs, dan cara menganalisis isi chunk, bukan hanya menyebutkannya dalam tujuh butir.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/references/js-chunk-discovery.md` | 9 bagian: titik masuk HTML, manifest build per tool, tabel chunk dari `__webpack_require__.u`, panel Coverage, pencarian global DevTools, source map, crawl (`katana -jc`, Wayback CDX, `gau`), format inventaris, ambang berhenti | SKILL.md lama menulis "cek chunk file: cari berkas .chunk.js di tab Sources" tanpa cara menemukan chunk yang tidak dimuat di halaman awal | probe manifest ditulis sebagai uji status 200/404, bukan jaminan keberadaan; pola `__webpack_require__.u`/`__vite__mapDeps` adalah nama simbol publik webpack/Vite |
| `skills/web-reconnaissance/references/js-chunk-analysis.md` | 9 bagian: beautify, rekonstruksi `sourcesContent`, tabel 15 pola ekstraksi, triage kunci publik vs asli, protokol verifikasi 5 langkah, state framework (`__NEXT_DATA__`, `__NUXT__`, `__APOLLO_STATE__`), navigasi modul webpack, 6 false positive, time box, format temuan | bagian "scan isinya" hanya menyebut tiga substring dan tidak menjelaskan cara membedakan kunci publik dari kunci rahasia — sumber kesalahan laporan paling umum | 6 pola kunci diuji dengan `[regex]` .NET pada bundle contoh: `AKIA`, `pk_live_`, `AIza`, `/api/v2/`, `path:"/…"`, `wss://` semuanya cocok; string acak 60 karakter tidak memicu `AKIA` |
| `skills/web-reconnaissance/references/network-analysis.md` | 12 bagian: setup capture (Preserve log, Disable cache, unregister SW), waterfall dan initiator, 6 resep filter, matriks endpoint, semantik status 401/403/404/405/429, GraphQL, WebSocket/SSE, sesi dan token, ekspor HAR + resep `jq`, replay dengan batas, serah terima, kebersihan data | langkah "Cek Network Tab" lama hanya meminta memfilter XHR tanpa menjelaskan kolom Initiator, semantik status, atau cara menyimpan bukti | resep `jq` ditulis tetapi **tidak dieksekusi** — `jq` tidak terpasang di mesin ini; kebenaran struktural diperiksa terhadap format HAR 1.2 |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-reconnaissance/SKILL.md` | deskripsi menyebut source map/HAR/analisis bundle; tabel tiga sumber di pembuka; `## Decision Frame` 6 keputusan (scope, ambang berhenti chunk, source map, triage kunci, status endpoint, time box 90 menit); langkah 1–3 menunjuk referensi; `## Gotchas` 9 butir; output laporan diperluas (inventaris chunk, rute tersembunyi, kunci asli vs publik); tabel indeks referensi | skill hanya 114 baris tanpa frame, tanpa gotchas, tanpa referensi — status "Belum" di `docs/SKILL-QUALITY.md` | `grep -c '^## Decision Frame'` = 1; 114 → 155 baris (<500 sesuai README); `node scripts/check-fact-notes.js` exit 0 |
| `README.md` | baris 164: deskripsi `web-reconnaissance` diperbarui; baris 299: label `web-recon-simple` → `web-reconnaissance` | label lama tidak cocok dengan nama folder; deskripsi lama tidak mencerminkan isi baru | dicocokkan dengan nama direktori `skills/web-reconnaissance` |
| `docs/SKILL-QUALITY.md` | baris matriks `web-reconnaissance` → Trigger ya / Frame ya / Refs 3 / Failure modes ya / Sebagian; ringkasan Sebagian 3→4 dan Belum 13→12; paragraf "Sebagian" menjelaskan provenance yang sengaja ditunda; `web-reconnaissance` dihapus dari backlog D; tanggal diperbarui | ledger harus mencerminkan kondisi setelah 0.7.0, bukan sebelum | dihitung ulang dari `SKILL.md`: Frame 16/28, Refs 3, Provenance — |

### Artefak turunan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | deskripsi `web-reconnaissance` diperbarui | sumber deskripsi adalah frontmatter `SKILL.md` | `node scripts/sync-skills.js` — 1 baris berubah |
| `skills/index.json` | deskripsi diperbarui + `files` memuat tiga referensi baru | indeks discovery harus mencantumkan berkas yang bisa dimuat | idem — 7 baris berubah |

`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` ditulis ulang oleh generator tetapi **isinya identik** (`git status --porcelain` tidak menampilkannya) karena ketiganya tidak menyimpan deskripsi per skill.

### Catatan

Pekerjaan ini sengaja dibatasi pada satu skill. Enam skill lain di backlog D (`threat-modeling`, `web-app-scan`, `incident-response-plan`, `security-documentation`, `owasp-top10-2025`, `risk-management-framework`) belum disentuh, dan cacat `security-documentation` yang menunjuk `docs/laporan.txt` (tidak ada di repo) masih terbuka.

## [0.6.0] — 2026-11-08 — Decision Frame untuk 3 skill metodologi + ledger kualitas

**Commit dasar:** `b63dc68` (branch `dev`)
**Status:** committed in `c16a2e3`
**Ruang lingkup:** poin B — tiga skill inti yang belum punya kerangka keputusan, plus satu dokumen yang membuat cakupan tuning terlihat.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `docs/SKILL-QUALITY.md` | matriks 28 skill × 5 kriteria (Trigger, Frame, Provenance, Refs, Failure modes), ringkasan 12 selesai / 3 sebagian / 13 belum, backlog C–F, dan alasan penundaan enforcement Frame | cakupan tuning sebelumnya hanya terlihat lewat riwayat commit; checker Frame belum layak dibuat pada 15/28 skill | angka dihitung dengan `node` langsung dari 28 `SKILL.md`, bukan ditebak |

### Diubah — Decision Frame

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/ptes-standard/SKILL.md` | frame 5 keputusan engagement: kriteria keluar fase, depth vs breadth, stop condition ROE, alokasi ≥20% waktu report, standar bukti yang bisa direproduksi | skill hanya memuat 7 fase dan 6 Gotchas; tidak ada logika kapan berhenti atau pindah | tiap butir dibandingkan dengan 6 Gotchas — tidak ada yang mengulang |
| `skills/waf-evasion-methodology/SKILL.md` | frame 5 keputusan: membuktikan WAF yang memblokir (kontrol positif), aturan pivot setelah 2 teknik tanpa perubahan respons, batas noise/scope, WAF pihak ketiga, bukti minimum | Gotchas bersifat taktis (direct IP, `\/`, paranoia level) dan tidak menjawab kapan berhenti mencoba | idem, dibandingkan dengan 5 Gotchas |
| `skills/threat-intelligence/SKILL.md` | frame 5 keputusan produk: audiens/produk (strategic/operational/tactical), bahasa keyakinan berbasis jumlah sumber, actionable vs konteks, berbagi vs keselamatan sumber, titik henti koleksi | Gotchas menutup PIR, TLP, YARA/Sigma/STIX, dan tools — bukan keputusan produk intelijen | idem, dibandingkan dengan 6 Gotchas |

### Diubah — fakta

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/ptes-standard/references/legal-compliance.md` | "PCI DSS v4.0" → "PCI DSS v4.x" + catatan `[UNVERIFIED]` (v4.0.1 terbit Juni 2024) | nomor versi kemungkinan usang; `docs/CERTIFICATION-FACTS.md` sendiri menandai versi PCI DSS belum terverifikasi | dibaca ulang; kategori `[UNVERIFIED]` konsisten dengan fact sheet |

### Diubah — audit

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `CHANGELOG.md` | entri 0.6.0 | aturan 1 | `node scripts/check-changelog.js` |

### Artefak turunan

`node scripts/sync-skills.js`: frontmatter tidak disentuh, sehingga `manifest.json`, `skills/index.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` tidak berubah.

Catatan cakupan: setelah entri ini, **15 dari 28** skill punya `## Decision Frame`; provenance tetap 12 karena `ptes-standard`, `threat-intelligence`, dan `waf-evasion-methodology` sengaja belum didaftarkan ke `check-fact-notes.js` (fact sheet belum memuat PTES, STIX 2.1, TLP 2.0, OWASP CRS).

## [0.5.0] — 2026-11-08 — Provenance note untuk 12 skill fact-bearing + pemeriksa otomatis

**Commit dasar:** `ad0afbe` (branch `dev`)
**Status:** committed in `bbb0da9`
**Ruang lingkup:** poin A — angka di skill fact-bearing harus bisa ditelusuri, dan pelanggarannya harus gagal otomatis, bukan bergantung ingatan.

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `scripts/check-fact-notes.js` | pemeriksa 5 syarat: note ada tepat satu, memakai varian kalimat yang benar, menautkan `docs/CERTIFICATION-FACTS.md`, tanggalnya sama dengan fact sheet, dan posisinya di antara `## Decision Frame` dan H2 berikutnya; juga menolak skill tak terdaftar yang menautkan fact sheet | catatan provenance tanpa penjaga akan basi seperti tanggal 2026-11-07 yang sudah salah sehari | `node scripts/check-fact-notes.js` → 12/12 lolos; **uji negatif:** tanggal di `comptia-cysa` diubah ke 2026-11-07 → exit 1 dengan pesan `note is dated differently from the fact sheet`, lalu dipulihkan |

### Diubah — skill (penanda baru)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/oscp-methodology/SKILL.md`, `skills/lf-cks/SKILL.md`, `skills/ec-ecih/SKILL.md` | penanda provenance varian sertifikasi, tepat setelah Decision Frame | angka ujian tersebar di `SKILL.md` **dan** `references/` (oscp: `exam-architecture.md`, `enumeration-framework.md`; lf-cks: `compliance-hardening.md`), jadi penanda di satu file harus menyatakan cakupan seluruh skill | `node scripts/check-fact-notes.js` |
| `skills/mitre-attack/SKILL.md`, `skills/nist-800-53/SKILL.md` | penanda provenance varian standar (ATT&CK v20.1; SP 800-53 Rev 5.2.0) | keduanya kerangka, bukan ujian — kalimat "fakta ujian" akan menyesatkan | idem |

### Diubah — skill (penanda lama diseragamkan)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/comptia-cysa/SKILL.md`, `skills/cpent/SKILL.md`, `skills/offsec-ir-200/SKILL.md`, `skills/offsec-pen-300/SKILL.md`, `skills/offsec-soc-200/SKILL.md`, `skills/offsec-th-200/SKILL.md`, `skills/offsec-web-300/SKILL.md` | kalimat "Fakta ujian diverifikasi ... (2026-11-07)" → varian baru, tanggal 2026-11-08, klausa cakupan `references/` dan klausa snapshot | tanggal lama sudah basi satu hari dan tidak menyebut cakupan; 7 file memuat 7 salinan tanggal yang bisa berbeda-beda | idem |

### Diubah — tata kelola

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `.github/workflows/validate-and-sync.yml` | job `check-fact-notes` menjalankan pemeriksa | penjaga harus berjalan di CI, bukan hanya lokal | YAML dibaca ulang; job berdiri sendiri tanpa `needs` |
| `AGENTS.md` | header "Symlink to CLAUDE.md" dihapus (file ini regular file, `CLAUDE.md` tidak ada); daftar skrip menambah `check-fact-notes.js`; langkah workflow baru | header menyatakan hal yang tidak benar; pemeriksa harus terdokumentasi agar dipakai | `git ls-files -s AGENTS.md` → mode `100644`, bukan symlink |
| `CHANGELOG.md` | entri 0.5.0 | aturan 1 | `node scripts/check-changelog.js` |

### Artefak turunan

`node scripts/sync-skills.js` dijalankan ulang: frontmatter tidak disentuh, sehingga `manifest.json`, `skills/index.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` tidak berubah dan tidak muncul di `git status`.

## [0.4.1] — 2026-11-08 — Konsistensi prasyarat CKA di skill CKS

**Commit dasar:** `b92d660` (branch `dev`)
**Status:** committed in `e3156ed`
**Ruang lingkup:** menghapus kontradiksi internal di `lf-cks` yang ditemukan saat verifikasi akhir 0.4.0.

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/lf-cks/SKILL.md` | gotcha "tanpa CKA aktif" → "setelah lulus CKA; status aktif tidak dinyatakan eksplisit, konfirmasi ke LF" | bertabrakan dengan bagian Exam Format di file yang sama ("telah lulus CKA", status aktif tidak disyaratkan eksplisit) | dibaca ulang kedua bagian; `docs/CERTIFICATION-FACTS.md` |
| `CHANGELOG.md` | entri 0.4.1 | aturan 1 & 4: setiap change set tercatat | `node scripts/check-changelog.js` |

## [0.4.0] — 2026-11-08 — Tuning lapis 2: report weight, Decision Frame 7 skill, audit di CI

**Commit dasar:** `62bc0ea` (branch `dev`)
**Status:** committed in `32935e5`
**Ruang lingkup:** menghapus klaim bobot report yang salah, menanam Decision Frame di 7 skill sertifikasi sisa, menegakkan changelog lewat CI, dan merapikan README.

### Diubah — fakta (exam guide OffSec diverifikasi ulang 2026-11-08)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/offsec-th-200/SKILL.md` | "Report = 70 points" → report bukan komponen nilai terpisah (70 = 7×10; poin tergantung kelengkapan dokumentasi); tambah Decision Frame | klaim lama menyesatkan alokasi waktu dan menyalahi aritmetika ujian | OSTH Exam Guide: 7 exercise × 10, lulus 50/70 |
| `skills/offsec-th-200/references/th-mindset.md` | golden rule "report is worth 70 points" dikoreksi | idem | idem |
| `skills/offsec-ir-200/references/ir-lifecycle.md` | "laporan 30 dari 70 points" → 4×10 + 2×15; report bukan komponen terpisah | bertabrakan dengan `SKILL.md` yang menyebut 30 poin = 2 exercise forensik | OSIR Exam Guide: Phase 1 4×10, Phase 2 2×15, lulus 50 |
| `skills/offsec-ir-200/references/reporting.md` | idem | idem | idem |
| `skills/oscp-methodology/SKILL.md` | "report 50% nilai" → report adalah gerbang pemberian poin, bukan persentase | OffSec tidak memberi bobot persentase pada report | OSCP+ FAQ: poin hanya untuk objective yang terdokumentasi |
| `skills/offsec-pen-300/SKILL.md` | "report 50% exam" → aturan OSEP sebenarnya (urutan mesin di report = urutan penilaian, proof file wajib di screenshot + control panel, shell interaktif); 48h → 47j45m; Decision Frame | aturan penilaian inti tidak terwakili | OSEP Exam Guide |
| `skills/offsec-pen-300/references/exam-strategy.md` | judul "48h Time Management" → "47h45m" | durasi resmi 47 jam 45 menit | idem |
| `skills/offsec-soc-200/SKILL.md` | dua klaim "report 50% grade" dikoreksi; Decision Frame | klaim tidak berdasar; OSDA menilai 10 phase | OSDA Exam Guide: 10 phase × 10, lulus 75/100 |
| `skills/offsec-soc-200/references/challenge-labs.md` | "Documentation is 50% of your grade" dikoreksi menjadi aturan poin per phase | klaim yang sama muncul lagi di reference, bukan hanya SKILL.md | idem |
| `skills/cpent/SKILL.md` | deadline report 7 → 30 hari (7 hari = perpanjangan berbayar); bobot "30%" ditandai `[UNVERIFIED]`; Decision Frame | deadline tertukar dengan perpanjangan; bobot report tidak dikonfirmasi sumber publik | EC-Council CPENT: report ≤30 hari |
| `skills/cpent/references/pivoting-report.md` | deadline 7 → 30 hari; bobot ~30% ditandai `[UNVERIFIED]` | idem | idem |
| `skills/mitre-attack/SKILL.md` | label Data Components "v14+" → "v14+, kini v20.1" | versi terkini | attack.mitre.org |
| `docs/CERTIFICATION-FACTS.md` | tanggal 2026-11-08; bagian "Report bukan komponen nilai terpisah" dengan kutipan resmi per ujian; bobot report CPENT → `[UNVERIFIED]`; riwayat koreksi baru | sumber kebenaran harus memuat aturan report, bukan hanya angka | 5 exam guide OffSec dibaca ulang |

### Diubah — struktur & tata kelola

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `.github/workflows/validate-and-sync.yml` | job `check-changelog` menjalankan `node scripts/check-changelog.js --base`; path filter menambah CHANGELOG.md, README.md, docs/, dan scripts/ (ditulis tanpa backtick agar tidak dibaca validator sebagai wildcard) | aturan audit sebelumnya hanya kesepakatan sosial, tidak gagal di CI | job memakai merge-base diff; gagal saat ada file tak tercatat |
| `README.md` | label `web-recon-simple` → `web-reconnaissance`; bagian "Audit & Code Security" untuk `security-auditor` dan `code-security-audit` | 2 skill tidak terdaftar, 1 label usang | 28/28 skill kini muncul di README |
| `skills/offsec-web-300/SKILL.md` | Decision Frame (white-box: source→exploit→bukti) | melengkapi pola pikir 7 skill sisa | 7 skill sisa |
| `skills/comptia-cysa/SKILL.md` | Decision Frame (prioritas CVE, scan, TLP, IOC vs TTP, chain of custody) | melengkapi pola pikir analyst | idem |
| `CHANGELOG.md` | entri 0.4.0; **koreksi entri 0.1.0**: klaim "file pukul 18:39 mengandung mojibake `â€”`" salah — pemindaian UTF-8 hari ini menemukan 0 mojibake di seluruh `skills/`, satu kemunculan hanya di `CHANGELOG.md` sendiri | aturan 6: koreksi lewat entri baru, bukan menulis ulang sejarah | `node -e` pemindaian byte UTF-8 atas 193 file `.md` |

### Artefak turunan

`node scripts/sync-skills.js` selesai ("Skill Sync Complete", 28 skill), tetapi `manifest.json`, `skills/index.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` **tidak berubah** karena tidak ada deskripsi frontmatter yang disentuh — kelimanya tidak muncul di `git status` sehingga tidak perlu dicatat sebagai perubahan.

## [0.3.0] — 2026-11-07 — Tuning fondasi: generator, fakta, decision frame

**Commit dasar:** `46a2ab2` (branch `dev`)
**Status:** committed in `0c01fbb`
**Ruang lingkup:** memperbaiki generator yang menghapus metadata, mengoreksi fakta sertifikasi dari sumber resmi, dan menanam decision frame.

### Diubah — generator

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `scripts/sync-skills.js` | normalisasi CRLF/BOM; `keywords` menerima array; `name` dipaksa = nama folder; menolak menulis `description` kosong | checkout Windows (CRLF) membuat parser gagal dan menghapus 26 deskripsi | `node scripts/sync-skills.js` exit 0; 28/28 deskripsi terisi |

### Diubah — fakta sertifikasi (sumber resmi diverifikasi 2026-11-07)

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/oscp-methodology/SKILL.md` | auxiliary Metasploit tidak lagi "bebas"; semua modul terkunci satu mesin; tambah Decision Frame | klaim lama menuntun ke 0 poin/diskualifikasi | dibandingkan dengan OSCP+ Exam Guide |
| `skills/oscp-methodology/references/exam-architecture.md` | catatan scaled scoring 100–500 (lulus 400) mulai 1 Des 2026; koreksi auxiliary | perubahan scoring resmi | OSCP+ Scaled Scoring FAQ |
| `skills/offsec-web-300/SKILL.md` | OSCP 70/100 (bukan 50), OSEP min 100 (bukan 85), durasi OSCP 23j45m, URL exam guide yang benar, klaim "report 85/100" | tiga angka salah + link 404 | WEB-300 & PEN-200 Exam Guide |
| `skills/offsec-soc-200/references/overview-exam.md` | OSIR 8 jam/Splunk/50-70/kedaluwarsa; OSTH 8 jam/50-70; format PDF dalam .7z via upload.offsec.com | profil OSIR/OSTH salah total | OSIR & OSTH Exam Guide |
| `skills/offsec-th-200/SKILL.md` | status kedaluwarsa sertifikat tanpa angka tak bersumber | FAQ OffSec | FAQ sertifikasi |
| `skills/offsec-ir-200/SKILL.md` | bobot report dijelaskan benar; pass path 55/60 | aritmetika lama salah | OSIR Exam Guide |
| `skills/cpent/references/exam-structure.md` | 53 soal/8 domain; cut score 60–85%; report 30 hari; retake | struktur blueprint V2 | EC-Council CPENT blueprint |
| `skills/ec-ecih/SKILL.md` | cut score 60–85%; catatan 9 domain resmi | blueprint ECIH v3 | EC-Council ECIH blueprint |
| `skills/lf-cks/SKILL.md` | K8s v1.37; "telah lulus CKA"; biaya/validitas/retake; dokumen resmi | melengkapi fakta CKS | LF CKS + curriculum v1.37 |
| `skills/lf-cks/references/workload-security.md` | perbaiki field `readOnlyRootRootFilesystem` → `readOnlyRootFilesystem` | typo memicu YAML invalid | cek schema |
| `skills/threat-intelligence/references/analytic-frameworks.md` | ATT&CK v20.1; 15 taktik termasuk Stealth & Defense Impairment; 227 teknik/479 sub/106 DC | versi v15 dan "Defense Evasion" sudah usang | attack.mitre.org |
| `skills/mitre-attack/SKILL.md` | T1525→T1580; Mobile 12 taktik; label LOLBins; contoh macOS; Decision Frame | ID teknik tertukar | attack.mitre.org |
| `skills/nist-800-53/SKILL.md` | RMF 7 langkah; CSF 2.0 6 fungsi (Govern); Decision Frame | dua angka kerangka salah | CSRC 800-37 & CSF 2.0 |
| `skills/owasp-top10-2025/SKILL.md` | ASVS 5.0.0; koreksi klaim A02 "paling umum" | versi & klaim tidak akurat | asvs.owasp.org, top10.owasp.org |
| `skills/log-management-nist-800-92/SKILL.md` | ISO 27001 A.8.15/A.8.16 (2022), bukan A.12.4 (2013) | penomoran usang | ISO 27001:2022 |
| `skills/web-reconnaissance/SKILL.md` | `name` = nama folder; deskripsi pemicu; metadata | nama drift `web-recon-simple` | 28/28 nama sinkron |

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `docs/CERTIFICATION-FACTS.md` | registry fakta 10 sertifikasi + 9 standar, dengan URL dan tanggal verifikasi | satu sumber kebenaran; mencegah drift angka | setiap baris punya URL resmi |
| `.gitignore` | mengabaikan artefak sementara (`.acl-recovery/`, `.port.mjs`, `.t-node.txt`, `.upstream-tmp/`, berkas sementara berawalan `.changelog-tmp-`) | mencegah sampah masuk commit | `git status` bersih dari pola itu |

### Diubah — artefak turunan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | 28 skill; deskripsi terisi; nama = folder | regenerasi | `node scripts/sync-skills.js` |
| `skills/index.json` | 28 skill, daftar file terbaru | regenerasi | idem |
| `.claude-plugin/plugin.json` | regenerasi | metadata plugin | idem |
| `.claude-plugin/marketplace.json` | regenerasi | metadata marketplace | idem |
| `.cursor-plugin/plugin.json` | regenerasi | metadata plugin | idem |
| `skills/code-security-audit/SKILL.md` | metadata `repository` disuntik generator | sinkronisasi author/repository | idem |

### Perubahan eksternal diadopsi

| File | Status | Catatan |
|---|---|---|
| `skills/code-security-audit/**` | ditambahkan ke git | dibuat proses lain pukul 21:15–21:38; sudah lolos sync dan memiliki validator + test; audit konten penuh belum dilakukan |

## [0.2.0] — 2026-11-07 — Skill `web-pentest-payloads`

**Commit dasar:** `69b436d` (branch `dev`)
**Status:** pending
**Ruang lingkup:** skill baru — payload web application pentest (39 reference)

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `skills/web-pentest-payloads/SKILL.md` | file baru | router gejala → reference, workflow, proof standard, tooling | `node scripts/sync-skills.js` membaca frontmatter; 172 baris (<500) |
| `skills/web-pentest-payloads/references/sql-injection.md`, `skills/web-pentest-payloads/references/nosql-injection.md`, `skills/web-pentest-payloads/references/command-injection.md`, `skills/web-pentest-payloads/references/ssti.md`, `skills/web-pentest-payloads/references/xxe.md`, `skills/web-pentest-payloads/references/ldap-xpath-injection.md`, `skills/web-pentest-payloads/references/graphql-attacks.md`, `skills/web-pentest-payloads/references/type-juggling.md`, `skills/web-pentest-payloads/references/injection-misc.md` | file baru | kelas injection & eksekusi | frontmatter tiga field; dibaca ulang |
| `skills/web-pentest-payloads/references/ssrf.md`, `skills/web-pentest-payloads/references/file-inclusion-traversal.md`, `skills/web-pentest-payloads/references/file-upload.md`, `skills/web-pentest-payloads/references/insecure-deserialization.md`, `skills/web-pentest-payloads/references/prototype-pollution.md`, `skills/web-pentest-payloads/references/request-smuggling.md`, `skills/web-pentest-payloads/references/http-cache-deception-poisoning.md`, `skills/web-pentest-payloads/references/host-header-injection.md`, `skills/web-pentest-payloads/references/http-parameter-pollution.md`, `skills/web-pentest-payloads/references/crlf-injection.md`, `skills/web-pentest-payloads/references/race-condition.md`, `skills/web-pentest-payloads/references/websocket-attacks.md`, `skills/web-pentest-payloads/references/infra-misconfig.md` | file baru | kelas server-side & infrastruktur | frontmatter tiga field; dibaca ulang |
| `skills/web-pentest-payloads/references/xss.md`, `skills/web-pentest-payloads/references/csrf.md`, `skills/web-pentest-payloads/references/clickjacking-tabnabbing.md`, `skills/web-pentest-payloads/references/dom-clobbering.md`, `skills/web-pentest-payloads/references/css-injection.md`, `skills/web-pentest-payloads/references/xs-leak.md`, `skills/web-pentest-payloads/references/open-redirect.md`, `skills/web-pentest-payloads/references/cors-misconfiguration.md`, `skills/web-pentest-payloads/references/client-side-path-traversal.md` | file baru | kelas client-side | frontmatter tiga field; dibaca ulang |
| `skills/web-pentest-payloads/references/jwt-oauth-saml.md`, `skills/web-pentest-payloads/references/authentication-bypass.md`, `skills/web-pentest-payloads/references/access-control-idor.md`, `skills/web-pentest-payloads/references/business-logic.md`, `skills/web-pentest-payloads/references/api-security.md`, `skills/web-pentest-payloads/references/prompt-injection.md` | file baru | auth, logika bisnis, API, LLM | frontmatter tiga field; dibaca ulang |
| `skills/web-pentest-payloads/references/payload-encoding-evasion.md`, `skills/web-pentest-payloads/references/oob-and-detection.md` | file baru | lintas kelas: encoding/WAF dan verifikasi OOB | frontmatter tiga field; dibaca ulang |

### Diubah — artefak turunan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `manifest.json` | menambah entri `web-pentest-payloads` | registrasi skill | `node scripts/sync-skills.js` |
| `skills/index.json` | menambah 40 file skill | index discovery | `node scripts/sync-skills.js` |
| `.claude-plugin/plugin.json` | regenerasi | metadata plugin | `node scripts/sync-skills.js` |
| `.claude-plugin/marketplace.json` | regenerasi | metadata marketplace | `node scripts/sync-skills.js` |
| `.cursor-plugin/plugin.json` | regenerasi | metadata plugin Cursor | `node scripts/sync-skills.js` |
| `README.md` | menambah baris di tabel Red Team dan tabel Referensi | README tidak punya marker sync, jadi manual | dibaca ulang; baris `web-pentest-payloads` ada di dua tabel |

### Catatan

- Sempat dibuat file probe `skills/web-pentest-payloads/.gitkeep` tanpa isi berguna; file dihapus pada sesi yang sama dan tidak pernah masuk git, sehingga tidak tercatat sebagai perubahan.
- Baris `updated:` pada frontmatter 28 reference dihapus karena konvensi repo hanya mengizinkan tiga field (`name`, `description`, `tags`).

### Verifikasi entri

- `node scripts/sync-skills.js` → `Updated manifest.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.cursor-plugin/plugin.json`, `skills/index.json`.
- `skills/index.json` berisi 40 file untuk skill ini; `.gitkeep` tidak terdaftar.
- `node scripts/check-changelog.js` → exit 0.

### Lampiran — audit eksplisit

| File | Perubahan |
|---|---|
| `skills/web-pentest-payloads/SKILL.md` | file baru |
| `skills/web-pentest-payloads/references/sql-injection.md` | file baru |
| `skills/web-pentest-payloads/references/nosql-injection.md` | file baru |
| `skills/web-pentest-payloads/references/command-injection.md` | file baru |
| `skills/web-pentest-payloads/references/ssti.md` | file baru |
| `skills/web-pentest-payloads/references/xxe.md` | file baru |
| `skills/web-pentest-payloads/references/ldap-xpath-injection.md` | file baru |
| `skills/web-pentest-payloads/references/graphql-attacks.md` | file baru |
| `skills/web-pentest-payloads/references/type-juggling.md` | file baru |
| `skills/web-pentest-payloads/references/injection-misc.md` | file baru |

## [0.1.0] — 2026-11-07 — Mekanisme changelog dan audit

**Commit dasar:** `69b436d` (branch `dev`)
**Status:** committed in `27a09bd`; revisi validator dan entri eksternal dicatat pada commit lanjutan
**Ruang lingkup:** tata kelola repo (tanpa perubahan konten skill)

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `CHANGELOG.md` | file baru | menjadi catatan resmi perubahan file | dibaca ulang; validator menemukan path ini |
| `scripts/check-changelog.js` | file baru | menghentikan commit jika ada file berubah yang tidak tercatat | `node scripts/check-changelog.js` exit 0 |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `AGENTS.md` | menambah bagian Changelog dan satu langkah workflow | agar aturan ini mengikat agen dan kontributor | dibaca ulang; perintah validasi tercantum |
| `scripts/check-changelog.js` | parser hanya membaca baris tabel; wildcard terlalu luas ditolak | menutup celah: path yang disebut di prosa/aturan tidak lagi dihitung sebagai entri audit | uji negatif `--base 69b436d~1` exit 1; uji normal exit 0 |

### Tidak diubah — perubahan eksternal terdeteksi

Direktori `skills/web-pentest-payloads/` **tidak ada** di baseline `69b436d` dan **bukan dibuat oleh sesi ini**. File muncul saat sesi berjalan (18:36–20:29) dari proses lain, dan sengaja tidak disentuh. Status: menunggu keputusan pemilik repo.

| File | Status | Catatan |
|---|---|---|
| `skills/web-pentest-payloads/**` | untracked, dikarantina | seluruh isi direktori, termasuk `SKILL.md` yang muncul pukul 20:29 |
| `manifest.json` | berubah (eksternal) | proses lain menjalankan `sync-skills.js`; kini memuat 27 skill |
| `skills/index.json` | berubah (eksternal) | 27 entri, termasuk `web-pentest-payloads` |
| `.claude-plugin/plugin.json` | berubah (eksternal) | status M karena line ending; `git diff` tidak menunjukkan perubahan konten |
| `.claude-plugin/marketplace.json` | berubah (eksternal) | idem |
| `.cursor-plugin/plugin.json` | berubah (eksternal) | idem |

Catatan: dukungan wildcard di validator hanya untuk kasus karantina seperti ini; validator tetap menampilkan setiap file yang tertutup wildcard sebagai peringatan, bukan sebagai audit eksplisit. File pukul 18:39 mengandung mojibake `â€”`, tanda encoding salah saat penulisan. Artefak turunan di atas **tidak di-commit** oleh sesi ini; hanya dicatat agar status working tree dapat diaudit.

### Baseline saat entri dibuat

- Baseline `69b436d`: 26 skill, 104 file `references/`, 0 link rusak (audit 2026-11-07).
- Setelah proses eksternal: 27 skill di `manifest.json` dan `skills/index.json` (belum di-commit oleh sesi ini).
- Satu-satunya perubahan pada subtree skills berasal dari proses eksternal di atas; tidak ada file terlacak yang diubah sesi ini.
- Temuan audit yang belum diperbaiki tidak dicatat di sini; changelog hanya mencatat perubahan, bukan backlog.
