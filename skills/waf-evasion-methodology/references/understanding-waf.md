---
name: "Understanding WAF — Models, Parsing, and WAFFLED Research"
description: "Deep dive into WAF security models (negative, positive, behavioral, anomaly scoring with OWASP CRS), parsing discrepancies between WAF and backend, and WAFFLED academic research on 1,207 bypass techniques across 5 major WAF providers."
tags: [waf, models, parsing, waffled, owasp-crs, anomaly-scoring, research]
---

# Understanding WAF — Models, Parsing & WAFFLED Research

## WAF Security Models

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

## Fundamental Mindset

**WAF bukanlah tembok. WAF adalah filter.** Seperti filter lainnya, ia memiliki lubang. Ia bergantung pada signature, aturan, dan pola yang dikenal.

### Prinsip Dasar

- **Parsing Discrepancy** — WAF dan backend tidak menginterpretasi input dengan cara yang sama. Jika WAF melihat sesuatu yang aman tapi backend mengeksekusinya sebagai berbahaya, payload berhasil.
- **Normalization Gap** — WAF melakukan decode satu kali, backend melakukan decode lain — perbedaan ini adalah celah.
- **Context Blindness** — WAF tidak tahu apakah `SELECT` adalah SQL injection atau nama user. Ia hanya mencocokkan pola.
- **Performance vs Security Trade-off** — WAF dioptimalkan untuk kecepatan. Mereka sering memeriksa hanya beberapa KB pertama request atau menggunakan parsing parsial.

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

## Ethical Boundaries

- **Proportionality** — intensitas testing sesuai level otorisasi
- **Minimal Intrusion** — metode paling tidak disruptif terlebih dahulu
- **Transparency** — metodologi didokumentasikan dan dapat direview
- **Accountability** — rantai tanggung jawab yang jelas
- Jangan bypass WAF pada infrastruktur tanpa izin tertulis
- WAF provider mencatat bypass attempts secara agresif

## Best Practices

- Pahami model WAF sebelum memilih teknik evasion
- Parsing discrepancies adalah vector paling powerful — prioritaskan
- OWASP CRS paranoia level 1-2 mudah di-bypass, level 3-4 butuh teknik lanjutan
- Selalu dokumentasikan ethical boundaries dalam test plan
