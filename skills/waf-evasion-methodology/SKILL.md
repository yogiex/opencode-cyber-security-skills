---
name: waf-evasion-methodology
description: Pola pikir dan metodologi sistematis untuk WAF evasion — memahami parsing discrepancies, encoding gaps, dan logic mismatches antara WAF dan backend application.
license: MIT
compatibility: opencode
metadata:
  audience: penetration tester, red teamer, security researcher, bug bounty hunter
  approach: principles-first
  source: OWASP CRS, MITRE ATT&CK
---

# WAF Evasion — Pola Pikir dan Metodologi

## Fundamental Mindset

**WAF bukanlah tembok. WAF adalah filter.**

Seperti filter lainnya, ia memiliki lubang. Ia bergantung pada signature, aturan, dan pola yang dikenal. Jika Anda bisa membuat traffic berbahaya terlihat "normal," atau menemukan pintu samping yang tidak dijaga WAF, Anda menang.

### Prinsip Dasar

- **Parsing Discrepancy** — WAF dan backend tidak menginterpretasi input dengan cara yang sama. Jika WAF melihat sesuatu yang aman tapi backend mengeksekusinya sebagai berbahaya, payload berhasil.
- **Normalization Gap** — WAF melakukan decode satu kali, backend melakukan decode lain — perbedaan ini adalah celah.
- **Context Blindness** — WAF tidak tahu apakah `SELECT` adalah SQL injection atau nama user. Ia hanya mencocokkan pola.
- **Performance vs Security Trade-off** — WAF dioptimalkan untuk kecepatan. Mereka sering memeriksa hanya beberapa KB pertama request atau menggunakan parsing parsial.

### Pergeseran Pola Pikir

| ❌ Pendekatan Random | ✅ Pendekatan Sistematis |
|---|---|
| Spamming payload list | Memahami parsing tiap layer |
| Berharap satu payload lolos | Mengidentifikasi encoding/decoding gaps |
| Fokus pada tools | Fokus pada metodologi |
| Mencoba-coba tanpa catatan | Dokumentasi dan improvement siklus |
| "WAF adalah musuh yang harus dikalahkan" | "WAF adalah filter — saya perlu format ulang input" |
| Mencari satu teknik ajaib | Kombinasi 2+ teknik independen |

**"In WAF evasion, consistency beats brilliance."** — Metodologi solid yang dijalankan konsisten menghasilkan hasil lebih baik daripada teknik hebat yang diterapkan acak.

---

## Siklus Analisis WAF (6 Fase)

```
PHASE 1: Identifikasi & Fingerprinting
    ↓
PHASE 2: Rule & Logic Mapping
    ↓
PHASE 3: Klasifikasi Mekanisme Defense
    ↓
PHASE 4: Payload Design & Development
    ↓
PHASE 5: Eksekusi & Monitoring
    ↓
PHASE 6: Adaptasi & Optimasi
```

### Phase 1: Identifikasi & Fingerprinting

- Deteksi keberadaan WAF — payload standar return 403/429, response header khusus, block page template
- Identifikasi provider WAF — Cloudflare, Akamai, ModSecurity, AWS WAF, Azure WAF, F5, Imperva
- Tentukan versi dan kemungkinan konfigurasi

**Indikator WAF Presence:**
- Response header: `CF-Ray` (Cloudflare), `Server: cloudflare`, `X-Served-By` (Akamai), `X-Mod-Security` (ModSecurity)
- Block page: Cloudflare challenge page, ModSecurity error page, custom block page
- Status code: 403 Forbidden, 406 Not Acceptable, 429 Too Many Requests, 503 Service Unavailable

### Phase 2: Rule & Logic Mapping

- Kirim payload standar yang diketahui diblokir — catat pola blocking
- Kirim variasi kecil — ubah satu karakter, lihat perbedaan respon
- Identifikasi parameter mana yang diinspeksi dan mana yang tidak
- Tentukan sensitivity level — apakah blocking ketat atau longgar?
- Identifikasi false positive — input legitimate yang diblokir (menandakan rule terlalu agresif)
- Petakan endpoint mana yang dilindungi dan mana yang tidak

**Amati:**
- Apakah blocking berdasarkan keyword tertentu (`UNION`, `SELECT`, `<script>`)?
- Apakah blocking case-sensitive?
- Apakah encoding tertentu lolos?
- Apakah content type tertentu tidak diperiksa?

### Phase 3: Klasifikasi Mekanisme Defense

**Signature-Based (Blacklisting):**
- Mencocokkan request terhadap database pola serangan (regex)
- Paling umum, paling mudah di-bypass
- Bypass: encoding, fragmentasi, case variation

**Anomaly-Based / Scoring:**
- Memberi skor pada karakteristik mencurigakan — blokir jika melebihi threshold
- Bypass: distribusikan elemen berbahaya di beberapa request, jaga skor tetap rendah

**Behavioral Analysis:**
- Melacak sequence request dan rate pattern
- Bypass: slow down, humanized pattern, distributed source IP
- Cloudflare menggunakan JavaScript challenge untuk memverifikasi browser

**Machine Learning:**
- Mempelajari pola traffic normal dan mendeteksi anomali
- Bypass: ML bisa dikelabui dengan pola yang tidak biasa tapi legitimate-looking

### Phase 4: Payload Design & Development

- Rancang payload based mapping dari phase 1-3
- Terapkan teknik obfuscasi sesuai karakteristik WAF
- Gunakan multi-layer encoding jika perlu
- Dokumentasikan setiap percobaan

**Pipeline Produksi Payload:**
```
Raw Idea → Base Payload → Adaptive Optimization → Testing → Final Payload
```

### Phase 5: Eksekusi & Monitoring

- Kirim payload terkontrol — jangan flood, lakukan bertahap
- Monitor respon WAF — blocked, allowed, challenged
- Analisis perbedaan respon antara payload normal dan payload dengan variasi
- Catat pola yang berhasil dan gagal

### Phase 6: Adaptasi & Optimasi

- Sesuaikan payload berdasarkan feedback dari phase 5
- Kembangkan teknik baru berdasarkan pola yang ditemukan
- Dokumentasikan pola yang berhasil untuk reuse

**Improvement Cycle:**
```
Execute Test → Measure Results → Analyze Gaps → Update Methodology → Refine Approach → Repeat
```

---

## Evasion Strategies — Empat Lapisan

```
Layer 1: Passive & Non-Destructive Analysis   (30% waktu)
Layer 2: Limited Diagnostic Testing            (25% waktu)
Layer 3: Intelligent & Adaptive Attacks        (35% waktu)
Layer 4: Systematic Exploitation               (10% waktu)
```

### Layer 1: Passive & Non-Destructive Analysis

**Tujuan:** Memahami WAF tanpa membuat noise.
**OPSEC Priority:** Maximum

- Analisis response headers dari request normal
- Bandingkan pola error — HTTP 403 vs 406 vs 429
- Deteksi perbedaan waktu respon (time-based analysis)
- Pelajari variasi respon di berbagai state
- Kumpulkan intelligence awal tanpa mengirim payload mencurigakan

### Layer 2: Limited Diagnostic Testing

**Tujuan:** Mengidentifikasi aturan dan threshold WAF dengan provokasi minimal.
**OPSEC Priority:** High

- Kirim payload standar dengan variasi minor
- Uji WAF dengan serangan yang sudah dikenal
- Analisis pola blocking — parameter apa yang diinspeksi?
- Identifikasi false positive dan false negative
- Tentukan threshold trigger — berapa banyak variasi sebelum diblokir

### Layer 3: Intelligent & Adaptive Attacks

**Tujuan:** Eksploitasi parsing discrepancies dengan teknik lanjutan.
**OPSEC Priority:** Medium

- Implementasi teknik obfuscasi lanjutan
- Gunakan multi-layer encoding
- Rancang context-aware attack
- Manfaatkan fitur spesifik bahasa/platform backend
- Analisis response differential — bandingkan respon blocked vs allowed

### Layer 4: Systematic Exploitation

**Tujuan:** Eksekusi final dengan presisi tinggi.
**OPSEC Priority:** Low (final phase)

- Pilih teknik paling efektif dari phase 3
- Implementasi serangan final
- Monitoring real-time
- Adaptasi dinamis jika ada resistensi
- Dokumentasi lengkap

---

## Teknik Evasion

### 1. Direct IP Attacks (Side Door)

Cara paling efektif untuk bypass WAF adalah **tidak berinteraksi dengan WAF sama sekali**.

- **Historical DNS Records** — banyak website memulai tanpa WAF, DNS records lama (A Records) mungkin masih指向 IP asli. Gunakan SecurityTrails, ViewDNS, DNSDumpster
- **Certificate Transparency Logs** — gunakan Censys atau crt.sh untuk mencari SSL certificate yang cocok dengan domain target, IP yang terlihat adalah origin server
- **Subdomain Enumeration** — developer sering lupa memproteksi subdomain (mail, dev, staging). Jika subdomain tidak diproxy (gray cloud), ping mengungkap IP asli
- **Cloud Metadata** — pada cloud environment, terkadang origin IP bocor melalui server header, error message, atau informasi di email

**Mental Model:** "Jangan coba menerobos pintu depan jika ada pintu samping yang tidak terkunci."

### 2. Encoding & Decoding Mismatch

WAF melakukan decode dengan aturannya sendiri. Backend melakukan decode dengan aturan berbeda. Gap ini adalah celah.

**URL Encoding:**
- `'` → `%27` — WAF decode jadi `'` lalu blokir. Backend bisa decode dua kali.
- **Double Encoding** — `%2527` → WAF decode sekali jadi `%27` (lihat string literal, aman). Backend decode lagi jadi `'` — SQL injection berhasil.

**Unicode Normalization:**
- `%C0%AE%C0%AE%C0%AF` — overlong UTF-8 encoding untuk `../`
- Unicode homoglyph — `SELLECT` menggunakan karakter yang terlihat seperti `E` tapi berbeda secara encoding
- Full-width ASCII — gunakan karakter full-width (FF01-FF5E) yang dinormalisasi backend jadi ASCII normal

**JSON Escape Sequence (\/):**
- RFC 8259 mendefinisikan `\/` sebagai escape sequence valid untuk `/`
- WAF memeriksa raw bytes — mencari pola `../`, `/etc/passwd` — tidak cocok karena ada backslash
- `JSON.parse()` mendecode `\/` jadi `/` — backend menerima path traversal murni
- Ditemukan efektif terhadap Cloudflare, AWS WAF, Akamai, Imperva

**Base64 Encoding:**
- Enkripsi payload dalam Base64, jika backend mendecode sebelum memproses
- `SELECT * FROM users` → `U0VMRUNUICogRlJPTSB1c2Vycw==`

### 3. HTTP Parameter Pollution (HPP)

**Masalah:** Parameter yang sama muncul beberapa kali. WAF dan backend memilih nilai berbeda.

- **WAF:** Memeriksa parameter pertama (`id=1`, aman)
- **PHP Backend:** Menggunakan parameter terakhir (`id=SELECT`, berbahaya)
- **ASP.NET Backend:** Menggabungkan keduanya
- **Result:** Payload lolos karena WAF mengevaluasi parameter yang salah

**Mental Model:** "WAF dan framework backend kadang tidak setuju parameter mana yang penting."

### 4. HTTP Request Smuggling

Eksploitasi perbedaan interpretasi Content-Length vs Transfer-Encoding antara WAF dan backend.

- **CL.TE** — WAF menggunakan Content-Length, backend menggunakan Transfer-Encoding
- **TE.CL** — WAF menggunakan Transfer-Encoding, backend menggunakan Content-Length
- **Hasil:** Satu request yang terlihat aman oleh WAF menjadi dua request di backend — yang kedua adalah payload berbahaya yang tidak pernah diperiksa WAF

### 5. Chunked Transfer Encoding Abuse

WAF dioptimalkan untuk kecepatan — mereka sering memeriksa hanya beberapa KB pertama request.

- Kirim body dengan `Transfer-Encoding: chunked`
- Fragment payload menjadi potongan kecil: `'`, ` OR`, ` 1=1`, `--`
- WAF melihat potongan terpisah yang tidak berbahaya
- Backend merakit ulang jadi `' OR 1=1--`

### 6. Content-Type Manipulation

Aturan WAF sering bersyarat pada content-type yang dideklarasikan.

- Kirim payload SQLi/XSS dengan `Content-Type: text/plain` — WAF mungkin tidak memeriksa body
- Tapi backend tetap mem-parsing sebagai JSON/X-www-form-urlencoded terlepas dari header
- Ganti `Content-Type: application/json` jadi `Content-Type: text/plain; charset=utf-8` — WAF skip, backend parse
- Multipart boundary manipulation — WAF menggunakan boundary pertama, backend menggunakan boundary continuation (RFC 2231)

**Mental Model:** "Ubah cara data dikirim, bukan hanya apa yang dikirim."

### 7. Payload Padding

Eksploitasi keterbatasan buffer WAF.

- Inject volume besar data benign (JSON array, base64 blobs, random strings)
- Ukuran payload melebihi buffer WAF (8KB-128KB)
- Kode berbahaya disembunyikan di bagian dalam body
- WAF memeriksa hanya segmen awal
- Backend memproses full payload → serangan berhasil

### 8. Obfuscation Payload

**SQL Injection Obfuscation:**
| Teknik | Contoh |
|---|---|
| **Inline Comments** | `UN/**/ION SE/**/LECT` |
| **Whitespace Manipulation** | `UNION%0ASELECT` (newline) |
| **Scientific Notation (MySQL)** | `UNION SELECT 1.0,2.0` |
| **Version Comments** | `/*!12345UNION*/ SELECT` |
| **Null Bytes** | `SEL%00ECT` |
| **Case Variation** | `UnIoN SeLeCt` |
| **Alternative Operators** | `OR 1=1` → `|| 1=1` |

**XSS Obfuscation:**
| Teknik | Contoh |
|---|---|
| **SVG OnLoad** | `<svg onload=alert(1)>` |
| **JavaScript Scheme** | `<a href="javascript:alert(1)">Click</a>` |
| **Unicode Escape** | `\u0061` instead of `a` |
| **Double URL Encoding** | `%253Cscript%253E` |
| **Event Handler Alternatives** | `onfocus`, `onmouseover`, `onerror` |

**Command Injection Obfuscation:**
| Teknik | Contoh |
|---|---|
| **Wildcards** | `cat /etc/pa??wd` |
| **Uninitialized Variables** | `cat /e${u}tc/pas${u}swd` |
| **Backticks** | `` `cat /etc/passwd` `` |
| **Command Substitution** | `$(cat /etc/passwd)` |
| **Environment Variables** | `$HOME/../../etc/passwd` |

### 9. Context Shifting

Pindahkan payload ke lokasi yang tidak diinspeksi WAF:

- **HTTP Headers** — User-Agent, Referer, X-Forwarded-For, Custom headers
- **Less-used parameters** — parameter tidak standar
- **Nested objects** — JSON dengan struktur bersarang
- **Alternative HTTP methods** — PATCH, PUT, OPTIONS (beberapa WAF hanya periksa GET/POST)
- **File upload** — upload file dengan nama yang mengandung payload

### 10. Business Logic & Non-Payload Bypass

WAF fokus pada pola — bukan logika aplikasi:

- **Race Conditions** — TOCTOU attacks
- **IDOR** — akses resource milik user lain lewat parameter
- **SSRF** — melalui trusted domains
- **Authentication Bypass** — JWT manipulation, session fixation
- **Workflow Flaws** — melewati langkah, mengulang langkah, order manipulasi

**Mental Model:** "WAF tidak bisa membaca niat. Ia hanya melihat format."

---

## Aturan Koordinasi Multi-Teknik

Untuk hasil optimal, kombinasikan teknik:

1. **Combination Rule** — gunakan 2+ teknik independen secara simultan
2. **Intelligent Sequencing** — urutkan berdasarkan efektivitas historis
3. **Semantic Preservation** — payload final harus mempertahankan makna asli
4. **Minimum Alteration** — hanya terapkan perubahan yang diperlukan

**Contoh Kombinasi:**
- Double encoding + Case variation + Parameter pollution
- Content-Type manipulation + Chunked transfer + Inline comments
- Payload padding + JSON escape encoding + Direct-to-origin

---

## Teknik Evaluation Framework

### Formula Prioritas

```
Value = (Success Probability × Impact × Executability) / Complexity
```

| Faktor | Komponen |
|---|---|
| **Success Probability** | Efektivitas historis, kompatibilitas WAF target, tingkat inovasi |
| **Impact** | Access gained, vulnerability level, target importance |
| **Executability** | Resources required, execution time, necessary skills |
| **Complexity** | Number of steps, need for specific tools, specialized knowledge |

### Matriks Prioritas

| | High Probability | Medium Probability | Low Probability |
|---|---|---|---|
| **High Impact** | Priority 1 | Priority 2 | Priority 3 |
| **Medium Impact** | Priority 2 | Priority 3 | Priority 4 |
| **Low Impact** | Priority 3 | Priority 4 | Priority 5 |

---

## WAF Evasion Maturity Model

| Level | Karakteristik |
|---|---|
| **1: Beginner** | Random payloads, no understanding of WAF logic, unpredictable results |
| **2: Repeatable** | Basic methodology defined, logical use of techniques, documentation begins |
| **3: Defined** | Formal methodology documented, standard operational procedures, quality metrics |
| **4: Managed** | Methodology continuously measured, process improvement cycles, payload quality tracking |
| **5: Optimizing** | WAF behavior prediction capabilities, automated methodology refinement, continuous innovation |

---

## Memahami WAF: Bagaimana Mereka Berpikir

### Negative Security Model (Blacklisting)
- Blokir "hal buruk yang diketahui"
- Bergantung pada regex signatures — `UNION SELECT`, `<script>`, `../`
- Paling umum, paling mudah di-bypass
- **Kelemahan:** Tidak bisa mendeteksi varian yang tidak ada di signature database

### Positive Security Model (Whitelisting)
- Izinkan hanya "hal baik yang diketahui"
- Jauh lebih sulit di-bypass tapi jarang karena maintenance tinggi
- **Kelemahan:** Bisa menghalangi traffic legitimate

### Behavioral Analysis (Cloudflare)
- Challenge client — JavaScript puzzle untuk verifikasi browser
- Rate limiting berdasarkan pola
- **Kelemahan:** Bisa dilewati dengan slow, humanized patterns

### Anomaly Scoring (OWASP CRS)
- Setiap kecocokan aturan menambah skor
- Request yang melebihi threshold diblokir
- Paranoia level 1-4 — semakin tinggi semakin ketat (tapi juga semakin banyak false positive)
- **Kelemahan:** Payload bisa lolos jika dijaga di bawah threshold

---

## Parsing Discrepancies (WAFFLED Research)

Penelitian akademis menemukan **1,207 bypass** pada 5 WAF besar (Cloudflare, AWS WAF, Azure WAF, Google Cloud Armor, ModSecurity) dengan mengeksploitasi **parsing discrepancies**.

**Pendekatan WAFFLED:**
- Payload tidak dimodifikasi — tetap utuh
- Mutasi diterapkan pada elemen non-payload: boundary multipart, namespace XML, whitespace di header Content-Type
- Tujuan: WAF gagal mem-parse request dengan benar, sementara framework backend berhasil mem-parse dan mengeksekusi payload

**Contoh Mutasi:**
- `--boundary` → `--\x00boundary` (null byte injection di boundary)
- `utf-8` → `Utf-8` (case variation di charset parameter)
- Boundary continuation: `boundary*0=re;boundary*1=al` (RFC 2231)
- Whitespace alteration: boundary dengan tab/whitespace tidak standar

**Implikasi:** 90%+ website menerima berbagai content-type secara interchangeable, membuat teknik ini sangat applicable.

---

## Checklist Sistematis

Gunakan checklist ini saat menghadapi WAF:

### 1. Konfirmasi WAF
- [ ] Payload standar return 403/429/block page?
- [ ] Response header mengindikasikan WAF? (CF-Ray, X-Served-By, dll)
- [ ] Apakah ada endpoint yang tidak diproteksi?
- [ ] Apakah error page memberikan informasi WAF?

### 2. Test Encoding Variations
- [ ] Single URL encoding
- [ ] Double URL encoding
- [ ] Mixed raw + encoded characters
- [ ] Unicode normalization
- [ ] JSON escape sequences (\/)

### 3. Test Case & Format Changes
- [ ] Case variation (`UnIoN SeLeCt`)
- [ ] Whitespace replacement (tab, newline, %0a)
- [ ] Comment injection (`UN/**/ION`)
- [ ] Null byte injection

### 4. Test Content-Type Manipulation
- [ ] `application/x-www-form-urlencoded`
- [ ] `application/json`
- [ ] `multipart/form-data`
- [ ] `text/plain`
- [ ] Multipart boundary manipulation
- [ ] XML namespace mutation

### 5. Test Parameter & Protocol Manipulation
- [ ] HTTP Parameter Pollution (duplicate params)
- [ ] Chunked Transfer Encoding
- [ ] HTTP Request Smuggling (CL.TE / TE.CL)
- [ ] Payload padding (exceed buffer size)
- [ ] Different HTTP methods (PATCH, PUT, OPTIONS)

### 6. Test Context Shifting
- [ ] Headers (User-Agent, Referer, X-Forwarded-For)
- [ ] Less-used parameters
- [ ] Nested JSON objects
- [ ] File upload fields

### 7. Test Non-Payload Vectors
- [ ] Business logic flaws
- [ ] IDOR
- [ ] Race conditions
- [ ] Authentication bypass
- [ ] SSRF through trusted domains

### 8. Test Origin IP Discovery
- [ ] Historical DNS records
- [ ] Certificate Transparency logs
- [ ] Subdomain enumeration (unprotected subdomains)
- [ ] Cloud metadata leaks

---

## Key Questions

1. **"What does the WAF block?"** — Petakan pola blocking secara sistematis
2. **"What does the WAF NOT inspect?"** — Parameter, header, content type apa yang dilewatkan?
3. **"What technology runs on the backend?"** — PHP vs ASP.NET vs Python vs Java — masing-masing menangani parameter duplikat dan encoding berbeda
4. **"Is there a parsing discrepancy I can exploit?"** — Apakah WAF dan backend menginterpretasi request secara berbeda?
5. **"Can I reach the origin directly?"** — Apakah ada side door yang tidak melewati WAF?
6. **"What's the WAF's inspection depth?"** — Apakah WAF memeriksa full request atau hanya beberapa KB pertama?
7. **"What content types are not inspected?"** — Content type mana yang WAF skip?
8. **"Can I combine multiple techniques?"** — Dua teknik independen lebih efektif daripada satu

---

## Ethical Boundaries

- **Proportionality** — intensitas testing sesuai level otorisasi
- **Minimal Intrusion** — metode paling tidak disruptif terlebih dahulu
- **Transparency** — metodologi didokumentasikan dan dapat direview
- **Accountability** — rantai tanggung jawab yang jelas
- Jangan bypass WAF pada infrastruktur tanpa izin tertulis
- WAF provider mencatat bypass attempts secara agresif

---

## Kapan Menggunakan Skill Ini

**Gunakan ketika:**
- Menghadapi WAF saat penetration testing authorized
- Melakukan bug bounty pada aplikasi yang diproteksi WAF
- Mengevaluasi efektivitas WAF organisasi (defensive perspective)
- Merancang payload yang lolos signature-based detection
- Memahami parsing discrepancies antara WAF dan backend

**Jangan gunakan ketika:**
- Membutuhkan panduan tools spesifik (sqlmap, wafw00f) — ini adalah skill mindset, bukan tool guide
- Melakukan scanning otomatis tanpa pemahaman — metodologi ini butuh pendekatan sistematis
- Target adalah production system tanpa authorization — ini ilegal
- Membutuhkan panduan umum web security — gunakan skill web-app-scan
