# Analisis Kebutuhan — Aspek Web Application pada Vulnerability Assessment

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-14
**Pertanyaan yang dijawab:** aspek apa yang masih kurang pada skill `vulnerability-assessment` untuk VA web application (API, auth/session, CMS, framework, SCA, client-side, business logic, TLS/headers), file reference apa yang perlu ditambah/diperluas, dan bagaimana menjaga kualitas web VA agar tidak menjadi noise scanner.
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md), [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md), [SKILL-QUALITY.md](SKILL-QUALITY.md)
**Hasil brainstorming acuan:** `brainstorm-web-va` (15 topik, 11 berkas baru, 5 berkas existing diperluas, 20 gotchas)

---

## 1. Ringkasan

Skill `vulnerability-assessment` saat ini mencakup VA menyeluruh (network, host, web, cloud, database, container) secara umum, dengan 9 berkas referensi. Namun **aspek web application hanya disinggung tipis** di `scanner-config.md` (bagian "Web (Burp/ZAP)") dan `reporting.md` (contoh temuan). Tidak ada metodologi VA web khusus, tidak ada panduan API (REST/GraphQL/gRPC/WebSocket), auth/session (OAuth/SAML/JWT), CMS, framework, SCA, client-side, business logic, TLS/headers, maupun triase false positive khas web.

Akibatnya, agent yang memakai skill ini untuk VA web cenderung: (a) menjalankan scanner web lalu menyalin output mentah (melanggar Persona Contract #5), (b) melaporkan header yang hilang sebagai High (antipattern web VA), (c) tidak membedakan unauthenticated vs authenticated scan per peran, dan (d) melewatkan kerentanan logika bisnis yang scanner tidak bisa temukan (Persona Contract #6).

Dokumen ini mendefinisikan kebutuhan untuk **memperluas aspek Web Application VA** pada skill `vulnerability-assessment` — bukan skill baru, bukan implementasi eksploitasi. Cakupannya: 11 berkas referensi baru + perluasan 5 berkas existing, dengan 20 gotchas khas web, kriteria penerimaan yang bisa diverifikasi mesin, dan prosedur implementasi yang aman untuk sesi paralel.

---

## 2. Temuan audit (bukti)

Dihitung 2026-11-14 terhadap `skills/vulnerability-assessment/` (9 berkas referensi) dan skill terkait (`web-app-scan`, `web-reconnaissance`, `web-pentest-payloads`).

| ID | Temuan | Cara memeriksa | Akibat |
|---|---|---|---|
| T1 | Tidak ada berkas `web-va-methodology.md` atau padanannya | `ls references/` → tidak ada berkas web-va* | VA web dilakukan ad-hoc; tidak ada siklus kerja web khusus |
| T2 | `scanner-config.md` hanya menyebut Burp/ZAP sekilas (8 baris "Web (Burp/ZAP)") | baca `scanner-config.md` §"Scanner per Target" | konfigurasi kredensial per peran, crawl depth, rate limit web tidak terdokumentasi |
| T3 | `asset-discovery.md` tidak mencakup discovery attack surface web (subdomain, endpoint API, rute SPA, WebSocket, GraphQL) | baca `asset-discovery.md` | coverage web dihitung dari IP, bukan dari endpoint/parameter |
| T4 | `remediation-verification.md` generik; tidak ada verifikasi remediasi web (CSP fix, header, patch dependensi, re-scan DAST) | baca berkas | re-scan web tidak punya kriteria penutupan spesifik |
| T5 | `reporting.md` hanya contoh generik; tidak ada mapping OWASP Top 10 / CWE / WSTG untuk web | baca berkas | laporan web tidak konsisten dengan standar web |
| T6 | `referensi.md` tidak memuat sumber web VA (OWASP WSTG, OWASP ASVS, PortSwigger, OWASP API Top 10) | baca berkas | rujukan web tidak tersedia |
| T7 | Tidak ada panduan API VA (REST/GraphQL/gRPC/WebSocket) | grep `graphql\|grpc\|websocket` di references → 0 | kerentanan API (BOLA, BFLA, mass assignment) tidak tercakup |
| T8 | Tidak ada panduan auth & session VA (OAuth/SAML/JWT) | grep `oauth\|saml\|jwt` → 0 | kerentanan auth tidak tercakup |
| T9 | Tidak ada panduan CMS, framework, SCA, client-side, business logic | grep → 0 | cakupan web VA tidak lengkap |
| T10 | Gotchas SKILL.md hanya 10 butir umum VA; tidak ada gotchas khas web (WAF false negative, SPA 200, header missing ≠ High, dll.) | baca SKILL.md §Gotchas | agen cenderung over-report temuan web |
| T11 | `web-app-scan` dan `web-reconnaissance` adalah skill terpisah (manual, pentest-oriented); belum ada jembatan ke VA terstruktur | baca SKILL.md kedua skill | duplikasi atau gap antara recon/scan manual dan VA |
| T12 | Tidak ada definisi "web-specific false positive triage" | grep `false positive` → hanya scanner-config.md | triase web dilakukan dengan kriteria network VA |

### 2.1 Kondisi saat ini (ringkas)

- `SKILL.md`: 136 baris, 9 referensi, 10 gotchas umum, Persona Contract 6 butir.
- Capability Map: 9 baris, tidak ada grup "Web VA".
- Progressive Disclosure: 9 baris.
- Tidak ada Decision Frame khusus web (hanya umum).

---

## 3. Definisi

**Web Application VA** — identifikasi, triase, scoring, dan pelaporan kerentanan pada aplikasi web dan API yang dimiliki/diotorisasi, dengan cakupan autentikasi per peran, verifikasi manual atas temuan scanner, dan mapping ke standar web (OWASP Top 10, OWASP API Top 10, OWASP WSTG, CWE). Bukan eksploitasi, bukan pentest.

**Attack surface web** — seluruh titik masuk yang bisa dijangkau: host/subdomain, endpoint HTTP/HTTPS, rute SPA, endpoint API (REST/GraphQL/gRPC/WebSocket), parameter, header, cookie, storage klien, dan integrasi pihak ketiga yang berada dalam scope.

**API VA** — pengujian keamanan endpoint API (autentikasi, otorisasi, validasi input, rate limit, mass assignment, BOLA/BFLA) dengan pendekatan terstruktur, bukan fuzzing.

**Auth & session VA** — pengujian mekanisme autentikasi dan sesi (OAuth/OIDC, SAML, JWT, cookie) termasuk konfigurasi, rotasi, pencabutan, dan kontrol akses berbasis peran.

**SCA (Software Composition Analysis)** — identifikasi kerentanan pada dependensi pihak ketiga (npm, pip, composer, Maven, Go modules) beserta transitive dependency dan lockfile.

**Client-side security VA** — pengujian keamanan kode dan storage klien (XSS, DOM-based, CSP, postMessage, storage token, secret di bundle).

**Business logic VA** — pengujian kerentanan logika bisnis (price tampering, IDOR, workflow bypass, race condition) yang tidak dapat ditemukan scanner otomatis.

**Web-specific false positive** — temuan scanner web yang bukan kerentanan nyata karena konteks web (SPA fallback 200, WAF block, header missing tanpa rantai serangan, banner grabbing salah).

**Remediation verification web** — verifikasi perbaikan web dengan re-scan DAST, pemeriksaan header/CSP, re-audit dependensi, dan validasi konfigurasi server/middleware.

---

## 4. Ruang lingkup

**Termasuk:**
- Metodologi VA web (automated DAST vs manual, kapan pakai masing-masing, cakupan autentikasi per peran).
- Discovery attack surface web (subdomain, endpoint, rute SPA, API, WebSocket, GraphQL).
- API VA (REST/GraphQL/gRPC/WebSocket): autentikasi, otorisasi (BOLA/BFLA), validasi input, rate limit, mass assignment.
- Auth & session VA (OAuth/OIDC, SAML, JWT, cookie, sesi, MFA, reset password).
- Web server & middleware VA (path traversal, request smuggling, header injection, konfigurasi).
- CMS VA (WordPress/Drupal/Joomla: core, plugin, theme, konfigurasi).
- Web framework VA (Laravel/Spring/Django/Express/Next.js: debug mode, default credential, endpoint debug, konfigurasi).
- SCA (npm/pip/composer/Maven/Go: dependensi langsung & transitif, lockfile, CVE, license).
- Client-side security VA (XSS DOM, CSP, postMessage, storage, secret di bundle).
- Business logic VA (price tampering, IDOR, workflow bypass, race condition, file upload).
- Authenticated & role-based scanning (akun per peran, matrix akses).
- Web VA reporting (mapping OWASP Top 10, OWASP API Top 10, CWE, WSTG; multi-audiens).
- Web-specific FP triage (SPA fallback, WAF, header missing, banner salah).
- TLS & HTTP headers VA (protokol, cipher, HSTS, CSP, CORS, cookie flags).
- Remediation verification web (re-scan DAST, header check, SCA re-audit, config review).

**Tidak termasuk:**
- Eksploitasi dan pengambilalihan sistem (gunakan `ptes-standard` atau `offsec-pen-300`/`offsec-web-300`).
- Pentest manual mendalam (gunakan `web-app-scan`, `web-pentest-payloads`).
- Recon klien (chunk JS, storage) secara mendalam (gunakan `web-reconnaissance`); VA hanya mengonsumsi hasilnya.
- Audit kepatuhan/GRC penuh (gunakan `security-auditor`).
- VA network/host/cloud/database/container (sudah ada aspek lain / skill terpisah).
- Penulisan exploit/PoC (dilarang; VA berhenti di identifikasi & pelaporan).

---

## 5. Kebutuhan fungsional

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | Memuat skill mengaktifkan peran VA analyst untuk web; jawaban memakai suara persona | tidak kembali ke asisten generik; struktur ringkas → alasan → langkah → bukti → risiko |
| FR-2 | Ada metodologi VA web khusus yang membedakan automated DAST vs manual, dengan kriteria kapan pakai masing-masing | berkas `web-va-methodology.md` ada; Decision Frame memuat ambang |
| FR-3 | Discovery attack surface web mencakup subdomain, endpoint, rute SPA, API, WebSocket, GraphQL | berkas `web-attack-surface-va.md` ada; tabel sumber discovery |
| FR-4 | API VA mencakup REST/GraphQL/gRPC/WebSocket dengan BOLA, BFLA, mass assignment, rate limit | berkas `web-api-va.md` ada; checklist per protokol |
| FR-5 | Auth & session VA mencakup OAuth/OIDC, SAML, JWT, cookie, sesi, MFA, reset password | berkas `web-auth-session-va.md` ada; checklist konfigurasi |
| FR-6 | Web server & middleware VA mencakup path traversal, request smuggling, header injection, konfigurasi | berkas `web-server-middleware-va.md` ada |
| FR-7 | CMS VA mencakup core/plugin/theme dan konfigurasi (WordPress/Drupal/Joomla) | berkas `cms-va.md` ada |
| FR-8 | Web framework VA mencakup debug mode, default credential, endpoint debug, konfigurasi | berkas `web-framework-va.md` ada |
| FR-9 | SCA mencakup npm/pip/composer/Maven/Go, dependensi transitif, lockfile, CVE | berkas `component-sca-va.md` ada |
| FR-10 | Client-side security VA mencakup XSS DOM, CSP, postMessage, storage, secret di bundle | berkas `web-client-side-va.md` ada |
| FR-11 | Business logic VA mencakup price tampering, IDOR, workflow bypass, race condition, upload | berkas `web-business-logic-va.md` ada |
| FR-12 | Web VA reporting memetakan temuan ke OWASP Top 10, OWASP API Top 10, CWE, WSTG | berkas `web-va-reporting.md` ada; tabel mapping |
| FR-13 | Authenticated & role-based scanning terdokumentasi: akun per peran, matrix akses, cakupan per peran | bagian khusus di `web-va-methodology.md` atau `web-auth-session-va.md` |
| FR-14 | Web-specific FP triage terdokumentasi: SPA fallback 200, WAF block, header missing, banner salah | bagian khusus (di `scanner-config.md` diperluas atau berkas baru); minimal 8 kriteria |
| FR-15 | TLS & HTTP headers VA terdokumentasi: protokol, cipher, HSTS, CSP, CORS, cookie flags | bagian khusus (di `scanner-config.md` diperluas atau `web-va-methodology.md`) |
| FR-16 | Remediation verification web terdokumentasi: re-scan DAST, header check, SCA re-audit | `remediation-verification.md` diperluas; kriteria penutupan web |
| FR-17 | `SKILL.md` Capability Map dan Progressive Disclosure memuat grup "Web VA" dengan tautan ke 11 berkas baru | tabel 1:1, tidak ada berkas yatim |
| FR-18 | `asset-discovery.md` diperluas dengan discovery attack surface web | bagian baru; sumber discovery web |
| FR-19 | `referensi.md` diperluas dengan sumber web VA (OWASP WSTG, ASVS, API Top 10, PortSwigger) | tabel sumber baru |
| FR-20 | Scanner config web diperluas: Burp/ZAP config per peran, crawl depth, rate limit, auth scan | `scanner-config.md` §Web diperluas |
| FR-21 | Gotchas khas web minimal 20 butir, dimasukkan di `SKILL.md` (atau berkas web) | ≥20 butir; verifikasi mesin (grep count) |
| FR-22 | Tidak ada materi eksploitasi/PoC; VA berhenti di identifikasi & pelaporan | review isi; tidak ada payload exploit |

---

## 6. Kebutuhan non-fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| NFR-1 | `SKILL.md` tetap 120–200 baris (batas keras 450); kelebihan materi dipindah ke `references/` | hitung baris |
| NFR-2 | Setiap berkas `references/` muncul tepat sekali di Reference Documentation; tidak ada berkas yatim | paritas tabel 1:1 |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`) | tidak ada tautan `../../docs/` |
| NFR-4 | Bahasa Indonesia + istilah teknis Inggris; kode dan komentar berbahasa Inggris | review manual |
| NFR-5 | Setiap penghapusan/perubahan berkas tercatat di `CHANGELOG.md` | entri changelog |
| NFR-6 | Perubahan bisa diverifikasi ulang oleh mesin: grep, hitung baris, resolusi tautan, paritas tabel | skrip pemeriksa |
| NFR-7 | Frontmatter YAML (name/description/tags) pada setiap berkas references baru | pemeriksaan struktur |
| NFR-8 | Tidak ada duplikasi dengan `web-app-scan`/`web-reconnaissance`: web VA mereferensikan, tidak menulis ulang | review isi; rujukan eksplisit |
| NFR-9 | Konsistensi dengan Persona Contract: setiap temuan scanner harus ditriase; output scanner mentah tidak boleh jadi laporan | review isi |

---

## 7. Keterbatasan yang diterima

| ID | Keterbatasan | Mengapa diterima |
|---|---|---|
| LI-1 | VA web tidak bisa menemukan kerentanan logika bisnis secara otomatis; memerlukan uji manual terstruktur | scanner tidak memahami konteks bisnis; dokumentasikan sebagai keterbatasan (Persona Contract #6) |
| LI-2 | Hasil DAST berbeda antar tool (Burp vs ZAP) dan konfigurasi | dokumentasikan tool+versi+policy; jangan klaim kesetaraan |
| LI-3 | Authenticated scan per peran memerlukan akun test yang disediakan klien; tidak bisa dibuat sendiri tanpa izin | scope & otorisasi (Decision Frame #1) |
| LI-4 | SCA bergantung pada lockfile; tanpa lockfile akurasi rendah | laporkan keterbatasan; scan image/container sebagai fallback |
| LI-5 | TLS/headers hasil bisa berbeda antara openssl dan browser (SNI, cipher negotiation) | dokumentasikan alat yang dipakai |
| LI-6 | Web VA tidak mencakup eksploitasi; temuan berhenti di identifikasi & pelaporan | batas skill (Persona Contract #3) |
| LI-7 | Duplikasi dengan `web-app-scan`/`web-reconnaissance` tidak bisa dihilangkan 100%; jembatan berupa rujukan | hindari penulisan ulang (NFR-8) |

---

## 8. Rekomendasi struktur file

### 8.1 Berkas baru (11)

| # | Berkas | Isi utama |
|---|---|---|
| 1 | `references/web-va-methodology.md` | Siklus VA web: automated DAST vs manual, kriteria pilihan, cakupan autentikasi per peran, authenticated & role-based scanning, threshold FP, kapan berhenti |
| 2 | `references/web-attack-surface-va.md` | Discovery attack surface web: subdomain, endpoint, rute SPA, API, WebSocket, GraphQL; sumber inventaris web |
| 3 | `references/web-api-va.md` | API VA REST/GraphQL/gRPC/WebSocket: autentikasi, BOLA/BFLA, validasi input, rate limit, mass assignment, checklist |
| 4 | `references/web-auth-session-va.md` | Auth & session VA: OAuth/OIDC, SAML, JWT, cookie, sesi, MFA, reset password, matrix akses per peran |
| 5 | `references/web-server-middleware-va.md` | Web server & middleware VA: path traversal, request smuggling, header injection, konfigurasi, reverse proxy |
| 6 | `references/cms-va.md` | CMS VA: WordPress/Drupal/Joomla core, plugin, theme, konfigurasi, version disclosure |
| 7 | `references/web-framework-va.md` | Web framework VA: Laravel/Spring/Django/Express/Next.js debug mode, default credential, endpoint debug, konfigurasi |
| 8 | `references/component-sca-va.md` | SCA: npm/pip/composer/Maven/Go, dependensi transitif, lockfile, CVE, license, threshold |
| 9 | `references/web-client-side-va.md` | Client-side security VA: XSS DOM, CSP, postMessage, storage, secret di bundle |
| 10 | `references/web-business-logic-va.md` | Business logic VA: price tampering, IDOR, workflow bypass, race condition, file upload |
| 11 | `references/web-va-reporting.md` | Web VA reporting: mapping OWASP Top 10, OWASP API Top 10, CWE, WSTG; multi-audiens; template |

### 8.2 Berkas existing yang diperluas (5)

| Berkas | Perluasan |
|---|---|
| `references/scanner-config.md` | Bagian "Web" diperluas: Burp/ZAP config per peran, crawl depth, rate limit, auth scan, TLS & HTTP headers, web-specific FP triage (atau rujuk ke berkas baru) |
| `references/asset-discovery.md` | Bagian discovery attack surface web: subdomain, endpoint, rute SPA, API, WebSocket, GraphQL |
| `references/remediation-verification.md` | Kriteria penutupan web: re-scan DAST, header/CSP check, SCA re-audit, config review, regresi web |
| `references/reporting.md` | Mapping OWASP Top 10/API Top 10/CWE/WSTG; contoh temuan web; laporan manajemen web |
| `references/referensi.md` | Sumber web VA: OWASP WSTG, ASVS, API Top 10, PortSwigger, CWE, OWASP Top 10 |

### 8.3 Pembaruan `SKILL.md`

- Capability Map: tambah grup "Web VA" dengan tautan ke 11 berkas baru.
- Progressive Disclosure: tambah 11 baris.
- Reference Documentation: tambah 11 baris (paritas 1:1).
- Gotchas: tambah minimal 20 butir khas web (total ≥30, atau pindahkan sebagian ke berkas web).
- Decision Frame: tambah 2-3 keputusan khusus web (auth scan per peran, TLS/headers threshold, SCA threshold) atau buat sub-bagian.
- Persona Contract: tambah 1 butir web (mis. "Saya membedakan temuan scanner web dari kerentanan nyata dengan verifikasi manual").

**Catatan:** `SKILL.md` harus tetap ≤450 baris; kelebihan materi dipindah ke `references/`.

---

## 9. Gotchas (20 khas web VA)

1. **WAF memblokir uji → false negative.** Bila permintaan benign juga diblokir, catat "pengujian terhalang", jangan simpulkan "aman".
2. **SPA membalas 200 untuk hampir semua path.** `/admin` 200 bukan bukti; periksa `Content-Type` dan isi.
3. **Header keamanan yang hilang bukan High.** Tanpa rantai serangan, tempatnya Low/Info.
4. **`robots.txt` hanya informasi.** Path di dalamnya petunjuk, bukan temuan.
5. **403 pada satu path bukan bukti aman** — coba path admin lain dan method lain sekali.
6. **IDOR tidak boleh diuji pada data pengguna nyata.** Siapkan dua akun sendiri.
7. **Denyut permintaan terlalu cepat memicu blokir IP** dan menghentikan seluruh sesi.
8. **Hasil scanner pihak ketiga tidak boleh disalin.** Reproduksi manual atau buang.
9. **CORS reflection origin tanpa credentials bukan celah.** Celah hanya bila `Allow-Credentials: true` bersama origin yang bisa dikontrol penyerang.
10. **CSP dengan `unsafe-inline`/`unsafe-eval` melemahkan header.** Header ada ≠ aman; nilai yang menentukan.
11. **JWT `alg: none` / weak key / key confusion harus diverifikasi, bukan diasumsikan.** Uji dengan bukti, bukan dugaan.
12. **API key publik (`pk_`, `AIza`) bukan temuan.** Secret key (`sk_`, private key) baru temuan.
13. **SCA: devDependencies tidak sama dengan production.** Jangan laporkan CVE dev sebagai risiko runtime tanpa konteks.
14. **SCA tanpa lockfile = akurasi rendah.** Laporkan keterbatasan, jangan klaim lengkap.
15. **GraphQL introspection terbuka bukan selalu High.** Nilai temuan tergantung data yang bisa diakses.
16. **WebSocket sering lupa authz.** Periksa Origin check dan autentikasi pada handshake.
17. **CMS: version disclosure plugin/theme lebih berisiko daripada core.** Fokus pada plugin yang tidak ter-update.
18. **Framework: debug mode / actuator endpoints sering terbuka di produksi.** Periksa `/actuator`, `/debug`, `/_profiler`.
19. **Request smuggling: hasil berbeda antar reverse proxy.** Verifikasi dengan dua request dan timing.
20. **Business logic: harga/quantity dihitung di klien → price tampering.** Selalu verifikasi kalkulasi di server.
21. **File upload: bypass ekstensi via content-type/double extension/polyglot.** Verifikasi isi, bukan hanya ekstensi.
22. **TLS: hasil openssl vs browser bisa berbeda (SNI).** Dokumentasikan alat yang dipakai.
23. **API versioning: endpoint lama (`/v1`) masih aktif tanpa auth.** Enumerasi versi lama.
24. **Rate limit absen pada login/reset password = temuan.** Uji dengan batas wajar (≤5 percobaan).
25. **SSRF: DNS rebinding, redirect, protocol smuggling.** Uji dengan payload non-destruktif.

*(Minimal 20; daftar di atas 25 butir, pilih ≥20 untuk implementasi.)*

---

## 10. Kriteria penerimaan

Dinyatakan **selesai** bila seluruh butir berikut terbukti:

| ID | Kriteria | Cara verifikasi |
|---|---|---|
| AC-1 | 11 berkas baru ada di `references/` dengan frontmatter YAML valid | `ls` + pemeriksaan frontmatter |
| AC-2 | 5 berkas existing diperluas (diff non-trivial) | `git diff` |
| AC-3 | `SKILL.md` Capability Map & Progressive Disclosure memuat 11 berkas baru (paritas 1:1) | hitung baris vs `ls references/` |
| AC-4 | `SKILL.md` ≤ 450 baris | `wc -l` |
| AC-5 | Tidak ada berkas yatim (setiap references muncul di Reference Documentation) | pemeriksaan struktur |
| AC-6 | Tidak ada tautan `../../docs/` di skill | grep |
| AC-7 | Gotchas khas web ≥ 20 butir | grep count `^- ` di bagian Gotchas |
| AC-8 | Frontmatter YAML pada 11 berkas baru (name/description/tags) | pemeriksaan struktur |
| AC-9 | Tidak ada payload exploit/PoC di berkas baru | review manual |
| AC-10 | Mapping OWASP Top 10 / API Top 10 / CWE ada di `web-va-reporting.md` | baca berkas |
| AC-11 | Authenticated & role-based scanning terdokumentasi | baca berkas |
| AC-12 | Web-specific FP triage terdokumentasi (≥8 kriteria) | baca berkas |
| AC-13 | TLS & HTTP headers VA terdokumentasi | baca berkas |
| AC-14 | Remediation verification web terdokumentasi (re-scan DAST, header check, SCA re-audit) | baca berkas |
| AC-15 | `CHANGELOG.md` mencatat penambahan/perubahan berkas | periksa entri |

---

## 11. Risiko & antipattern

### 11.1 Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Duplikasi dengan `web-app-scan`/`web-reconnaissance` | kebingungan agen, isi ganda | web VA mereferensikan, tidak menulis ulang (NFR-8) |
| Over-reporting temuan web (header missing sebagai High) | noise, hilangnya kepercayaan | Gotchas + kriteria severity di `web-va-reporting.md` |
| Skill `SKILL.md` melebihi 450 baris | melanggar NFR-1 | pindahkan materi ke `references/` |
| Sesi paralel menimpa berkas | konflik git | satu direktori satu pemilik; verifikasi sebelum commit (AGENTS.md) |
| Materi eksploitasi masuk ke VA | melanggar batas skill | review isi; Persona Contract #3 |
| Beras yatim / tautan rusak | kualitas menurun | paritas tabel 1:1; resolusi tautan |

### 11.2 Antipattern yang dilarang

| ID | Antipattern | Mengapa dilarang |
|---|---|---|
| AP-1 | Menyalin output scanner web mentah sebagai laporan | melanggar Persona Contract #5 |
| AP-2 | Melaporkan header yang hilang sebagai High tanpa rantai serangan | over-reporting; menurunkan kredibilitas |
| AP-3 | Menganggap unauthenticated scan = hasil lengkap | melanggar Persona Contract #4 |
| AP-4 | Menulis ulang materi `web-app-scan`/`web-reconnaissance` di web VA | duplikasi; rujuk saja |
| AP-5 | Memasukkan payload exploit/PoC | melanggar batas skill (bukan pentest) |
| AP-6 | Membuat skill baru (web-va terpisah) | ruang lingkup: perluasan skill existing |
| AP-7 | Menghapus pengetahuan teknis agar "ringkas" | menukar satu penyakit dengan penyakit lain |
| AP-8 | Mengganti "scanner" menjadi "assessment" tanpa mengubah isi | pola FP tetap lolos secara semantik |

---

## 12. Prosedur implementasi

1. Baca `SKILL.md` dan 5 berkas existing yang akan diperluas (sudah dilakukan).
2. Buat 11 berkas baru di `references/` dengan frontmatter YAML valid (name/description/tags).
3. Perluas 5 berkas existing dengan bagian web VA (append/insert, jangan hapus isi existing).
4. Perbarui `SKILL.md`: Capability Map, Progressive Disclosure, Reference Documentation, Gotchas (≥20), Decision Frame (web), Persona Contract (+1).
5. Verifikasi `SKILL.md` ≤ 450 baris; jika lebih, pindahkan materi ke `references/`.
6. Verifikasi paritas tabel 1:1 (setiap references muncul tepat sekali).
7. Verifikasi tidak ada tautan `../../docs/`.
8. Verifikasi tidak ada payload exploit/PoC.
9. Catat semua perubahan di `CHANGELOG.md` (entri baru, jangan ubah entri lama).
10. Jalankan `node scripts/check-changelog.js` sebelum commit.
11. Uji manual: buka `SKILL.md`, cek struktur, cek tautan.

**Catatan sesi paralel:** satu direktori satu pemilik. Berkas yang disentuh di sini: `skills/vulnerability-assessment/`. Jangan sentuh skill lain, `manifest.json`, `skills/index.json`, plugin files, `README.md`, `docs/SKILL-QUALITY.md`, `CHANGELOG.md` (kecuali mencatat entri), `scripts/*`.

---

## 13. Keputusan yang dibutuhkan

| ID | Keputusan | Pilihan | Dampak bila ditunda |
|---|---|---|---|
| D1 | Apakah web VA menjadi perluasan skill existing (bukan skill baru)? | ya (disarankan) / tidak | jika skill baru: duplikasi ekosistem, maintenance ganda |
| D2 | Apakah 20 gotchas ditempatkan di `SKILL.md` atau tersebar di berkas web? | di `SKILL.md` (disarankan, konsisten dengan skill existing) / tersebar | jika tersebar: gotchas sulit ditemukan |
| D3 | Apakah TLS & HTTP headers VA menjadi berkas tersendiri atau bagian dari `web-va-methodology.md`/`scanner-config.md`? | bagian dari `scanner-config.md` (disarankan) / berkas baru | jika berkas baru: 12 berkas, perlu update lebih banyak tabel |
| D4 | Apakah web-specific FP triage menjadi berkas tersendiri atau bagian dari `scanner-config.md`? | bagian dari `scanner-config.md` (disarankan) / berkas baru | idem |
| D5 | Apakah `SKILL.md` Decision Frame ditambah butir web atau buat sub-bagian "Decision Frame — Web"? | sub-bagian (disarankan) / tambah butir | jika tambah butir: SKILL.md lebih panjang |
| D6 | Apakah perlu skrip pemeriksa paritas tabel (FR-17, AC-3)? | ya / tunda | verifikasi manual tetap bisa |

---

## 14. Metrik

| Metrik | Kondisi awal (2026-11-14) | Target |
|---|---|---|
| Berkas referensi web VA | 0 | 11 |
| Berkas existing diperluas (web VA) | 0 | 5 |
| Gotchas khas web | 0 | ≥20 |
| Baris `SKILL.md` | 136 | ≤450 (target 180–220) |
| Berkas yatim | 0 | 0 |
| Tautan `../../docs/` | 0 | 0 |
| Mapping OWASP/API Top 10/CWE | 0 | 1 (di `web-va-reporting.md`) |
| Authenticated & role-based scanning terdokumentasi | tidak | ya |
| Web-specific FP triage terdokumentasi | tidak | ya (≥8 kriteria) |
| TLS & HTTP headers VA terdokumentasi | parsial (web-app-scan) | ya |
| Remediation verification web terdokumentasi | parsial (generik) | ya |
| Payload exploit/PoC | 0 | 0 |

---

**Catatan:** Dokumen ini adalah analisis kebutuhan, bukan implementasi. Tidak ada berkas referensi yang dibuat atau diubah oleh dokumen ini. Implementasi mengikuti prosedur §12 setelah keputusan §13 ditetapkan.
