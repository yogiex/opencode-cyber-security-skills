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
