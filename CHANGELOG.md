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
