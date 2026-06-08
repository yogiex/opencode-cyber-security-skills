---
name: "WAF Evasion Techniques"
description: "10 WAF evasion techniques with payload examples including Direct IP attacks, encoding mismatches, HTTP parameter pollution, request smuggling, chunked transfer abuse, content-type manipulation, payload padding, obfuscation, context shifting, and business logic bypass."
tags: [waf, evasion, techniques, encoding, obfuscation, hpp, smuggling, xss, sqli]
---

# WAF Evasion Techniques

## 1. Direct IP Attacks (Side Door)

Cara paling efektif untuk bypass WAF adalah **tidak berinteraksi dengan WAF sama sekali**.

- **Historical DNS Records** — banyak website memulai tanpa WAF, DNS records lama (A Records) mungkin masih指向 IP asli. Gunakan SecurityTrails, ViewDNS, DNSDumpster
- **Certificate Transparency Logs** — gunakan Censys atau crt.sh untuk mencari SSL certificate yang cocok dengan domain target
- **Subdomain Enumeration** — developer sering lupa memproteksi subdomain (mail, dev, staging). Jika subdomain tidak diproxy (gray cloud), ping mengungkap IP asli
- **Cloud Metadata** — origin IP bocor melalui server header, error message, atau informasi di email

**Mental Model:** "Jangan coba menerobos pintu depan jika ada pintu samping yang tidak terkunci."

## 2. Encoding & Decoding Mismatch

WAF melakukan decode dengan aturannya sendiri. Backend melakukan decode dengan aturan berbeda. Gap ini adalah celah.

**URL Encoding:**
- `'` → `%27` — WAF decode jadi `'` lalu blokir. Backend bisa decode dua kali.
- **Double Encoding** — `%2527` → WAF decode sekali jadi `%27` (lihat string literal, aman). Backend decode lagi jadi `'`.

**Unicode Normalization:**
- `%C0%AE%C0%AE%C0%AF` — overlong UTF-8 encoding untuk `../`
- Unicode homoglyph — `SELLECT` menggunakan karakter yang terlihat seperti `E` tapi berbeda secara encoding
- Full-width ASCII — gunakan karakter full-width (FF01-FF5E) yang dinormalisasi backend jadi ASCII normal

**JSON Escape Sequence (\/):**
- RFC 8259 mendefinisikan `\/` sebagai escape sequence valid untuk `/`
- WAF memeriksa raw bytes — tidak cocok dengan pola `../` karena ada backslash
- `JSON.parse()` mendecode `\/` jadi `/` — backend menerima path traversal murni
- Efektif terhadap Cloudflare, AWS WAF, Akamai, Imperva

**Base64 Encoding:**
- `SELECT * FROM users` → `U0VMRUNUICogRlJPTSB1c2Vycw==`

## 3. HTTP Parameter Pollution (HPP)

Parameter yang sama muncul beberapa kali. WAF dan backend memilih nilai berbeda.

- **WAF:** Memeriksa parameter pertama (`id=1`, aman)
- **PHP Backend:** Menggunakan parameter terakhir (`id=SELECT`, berbahaya)
- **ASP.NET Backend:** Menggabungkan keduanya
- **Result:** Payload lolos karena WAF mengevaluasi parameter yang salah

**Mental Model:** "WAF dan framework backend kadang tidak setuju parameter mana yang penting."

## 4. HTTP Request Smuggling

Eksploitasi perbedaan interpretasi Content-Length vs Transfer-Encoding antara WAF dan backend.

- **CL.TE** — WAF menggunakan Content-Length, backend menggunakan Transfer-Encoding
- **TE.CL** — WAF menggunakan Transfer-Encoding, backend menggunakan Content-Length
- **Hasil:** Satu request yang terlihat aman oleh WAF menjadi dua request di backend — yang kedua adalah payload berbahaya yang tidak pernah diperiksa WAF

## 5. Chunked Transfer Encoding Abuse

WAF dioptimalkan untuk kecepatan — mereka sering memeriksa hanya beberapa KB pertama request.

- Kirim body dengan `Transfer-Encoding: chunked`
- Fragment payload menjadi potongan kecil: `'`, ` OR`, ` 1=1`, `--`
- WAF melihat potongan terpisah yang tidak berbahaya
- Backend merakit ulang jadi `' OR 1=1--`

## 6. Content-Type Manipulation

Aturan WAF sering bersyarat pada content-type yang dideklarasikan.

- Kirim payload SQLi/XSS dengan `Content-Type: text/plain` — WAF mungkin tidak memeriksa body
- Tapi backend tetap mem-parsing sebagai JSON/X-www-form-urlencoded
- Ganti `Content-Type: application/json` jadi `Content-Type: text/plain; charset=utf-8`
- Multipart boundary manipulation — WAF menggunakan boundary pertama, backend menggunakan boundary continuation (RFC 2231)

**Mental Model:** "Ubah cara data dikirim, bukan hanya apa yang dikirim."

## 7. Payload Padding

Eksploitasi keterbatasan buffer WAF.

- Inject volume besar data benign (JSON array, base64 blobs, random strings)
- Ukuran payload melebihi buffer WAF (8KB-128KB)
- Kode berbahaya disembunyikan di bagian dalam body
- WAF memeriksa hanya segmen awal, backend memproses full payload

## 8. Obfuscation

**SQL Injection:**
| Teknik | Contoh |
|--------|--------|
| Inline Comments | `UN/**/ION SE/**/LECT` |
| Whitespace Manipulation | `UNION%0ASELECT` |
| Scientific Notation (MySQL) | `UNION SELECT 1.0,2.0` |
| Version Comments | `/*!12345UNION*/ SELECT` |
| Null Bytes | `SEL%00ECT` |
| Case Variation | `UnIoN SeLeCt` |
| Alternative Operators | `OR 1=1` → `|| 1=1` |

**XSS:**
| Teknik | Contoh |
|--------|--------|
| SVG OnLoad | `<svg onload=alert(1)>` |
| JavaScript Scheme | `<a href="javascript:alert(1)">Click</a>` |
| Unicode Escape | `\u0061` instead of `a` |
| Double URL Encoding | `%253Cscript%253E` |
| Event Handler Alternatives | onfocus, onmouseover, onerror |

**Command Injection:**
| Teknik | Contoh |
|--------|--------|
| Wildcards | `cat /etc/pa??wd` |
| Uninitialized Variables | `cat /e${u}tc/pas${u}swd` |
| Backticks | `` `cat /etc/passwd` `` |
| Command Substitution | `$(cat /etc/passwd)` |

## 9. Context Shifting

Pindahkan payload ke lokasi yang tidak diinspeksi WAF:

- **HTTP Headers** — User-Agent, Referer, X-Forwarded-For, Custom headers
- **Less-used parameters** — parameter tidak standar
- **Nested objects** — JSON dengan struktur bersarang
- **Alternative HTTP methods** — PATCH, PUT, OPTIONS (beberapa WAF hanya periksa GET/POST)
- **File upload** — upload file dengan nama yang mengandung payload

## 10. Business Logic & Non-Payload Bypass

WAF fokus pada pola — bukan logika aplikasi:

- **Race Conditions** — TOCTOU attacks
- **IDOR** — akses resource milik user lain lewat parameter
- **SSRF** — melalui trusted domains
- **Authentication Bypass** — JWT manipulation, session fixation
- **Workflow Flaws** — melewati langkah, mengulang langkah, order manipulasi

**Mental Model:** "WAF tidak bisa membaca niat. Ia hanya melihat format."

## Aturan Koordinasi Multi-Teknik

1. **Combination Rule** — gunakan 2+ teknik independen secara simultan
2. **Intelligent Sequencing** — urutkan berdasarkan efektivitas historis
3. **Semantic Preservation** — payload final harus mempertahankan makna asli
4. **Minimum Alteration** — hanya terapkan perubahan yang diperlukan

**Contoh Kombinasi:**
- Double encoding + Case variation + Parameter pollution
- Content-Type manipulation + Chunked transfer + Inline comments
- Payload padding + JSON escape encoding + Direct-to-origin

## Best Practices

- Kombinasikan 2+ teknik independen untuk hasil optimal
- Dokumentasikan teknik yang berhasil untuk reuse
- Prioritaskan direct-to-origin attack sebelum teknik kompleks
- Uji encoding variations sebelum mencoba teknik lanjutan
