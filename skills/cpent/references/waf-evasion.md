---
name: "WAF Evasion — Header, Encoding, dan Bukti"
description: "Bypass WAF yang profesional: mengidentifikasi WAF dan aturan yang memblokir, manipulasi header (case, duplikasi, Content-Type, path override), encoding berlapis (URL, Unicode, charset, chunked), fragmentasi payload, verifikasi eksekusi, dan batas etika."
tags: [waf, bypass, encoding, headers, obfuscation, burp, hackvertor, evasion]
---

# WAF Evasion

WAF bukan tembok; ia parser yang tidak sepakat dengan backend. Bypass yang benar bukan "payload aneh yang lolos", melainkan **perbedaan interpretasi** yang bisa dijelaskan dan diulang.

> Metodologi umum (siklus analisis, 10 teknik, model WAF, evaluasi) ada di skill [waf-evasion-methodology](../../waf-evasion-methodology/SKILL.md). Dokumen ini fokus pada header, encoding, dan cara membuktikannya di Burp.

## 1. Tiga pertanyaan sebelum bypass

1. **Apakah benar WAF yang memblokir?** Kirim payload sama ke endpoint lain, ke origin langsung, dan satu kontrol positif yang pasti diblokir.
2. **Kelas aturan apa yang memicu?** SQLi, XSS, RCE, path traversal, atau rate limit — tiap kelas punya teknik berbeda.
3. **Apa yang backend terima?** Encoding yang tidak dipahami backend bukan bypass, hanya payload rusak.

Tanpa jawaban ini, semua percobaan berikutnya adalah tebakan.

## 2. Identifikasi WAF

| Sinyal | Kemungkinan |
|---|---|
| `cf-ray`, `__cf_bm`, halaman challenge | Cloudflare |
| `AkamaiGHost`, header `akamai-*` | Akamai |
| `x-amzn-requestid` + 403 konsisten | AWS WAF |
| `X-Iinfo`, cookie `incap_ses`/`visid_incap` | Imperva |
| `X-Sucuri-ID`, halaman "Access Denied" | Sucuri |
| Cookie `TS*`, `X-WA-Info` | F5 BIG-IP ASM |
| `Server: Mod_Security` atau block page generik | ModSecurity/CRS |
| 403/406/501 berbeda per endpoint | Aturan spesifik, bukan IP block |

Tool: `wafw00f`, `whatwaf`. Verifikasi manual dengan satu payload jinak vs satu payload terlarang.

Perhatikan juga **perilaku**: blokir instan (aturan) vs jeda (rate limit) vs challenge (JS/cookie). Masing-masing butuh strategi berbeda.

## 3. Bypass level header

### Case, spasi, dan duplikasi

```text
user-agent: <script>alert(1)</script>
User-Agent : <script>alert(1)</script>
X-Forwarded-For: 127.0.0.1
X-Forwarded-For: 10.0.0.1     # duplikat; WAF dan backend bisa memilih berbeda
```

- Nama header **case-insensitive** menurut standar, tetapi parser WAF bisa case-sensitive.
- Spasi sebelum titik dua ilegal, tetapi sebagian parser menerimanya.
- Duplikasi header memicu **HPP**: WAF memeriksa yang pertama, backend memakai yang terakhir (atau sebaliknya).

### Content-Type dan charset

```text
Content-Type: text/plain
Content-Type: application/json; charset=utf-8
Content-Type: application/x-www-form-urlencoded; charset=ibm037
```

WAF sering hanya menginspeksi tipe yang dikenal. Jika backend tetap mem-parse body sebagai form/JSON, payload bisa lolos dari inspeksi. Uji satu per satu dan bandingkan perilaku backend.

### Path override dan method

```text
X-Original-URL: /admin
X-Rewrite-URL: /admin
X-HTTP-Method-Override: PUT
```

Berguna untuk kontrol akses berbasis path dan filter method. Bukan bypass WAF secara langsung, tetapi sering melewati aturan yang dipasang per-path.

### HTTP/2

Header dipaksa lowercase; hop-by-hop ditolak; pseudo-header (`:path`, `:authority`) bisa berbeda dari `Host`. Uji ulang payload di HTTP/2 — hasil di HTTP/1.1 tidak otomatis berlaku.

## 4. Encoding berlapis

| Lapisan | Contoh | Catatan |
|---|---|---|
| URL encode | `%3Cscript%3E` | Backend decode sekali |
| Double encode | `%253Cscript%253E` | Butuh backend yang decode dua kali |
| Unicode escape | `\u003cscript\u003e` (JSON) | Umum di API JSON |
| HTML entity | `&lt;script&gt;` | Efektif bila dirender sebagai HTML |
| Base64 | `PHNjcmlwdD4=` | Hanya jika aplikasi memang decode |
| Hex (SQL) | `0x414243` | Bukan string, tapi ekspresi SQL |
| Chunked | `Transfer-Encoding: chunked` | Bisa memecah signature |
| Gzip | body terkompresi | WAF mungkin tidak membuka |
| Charset | `charset=ibm037` | Bytes berbeda di mata WAF dan backend |

**Aturan praktis:** encoding harus cocok dengan decoder backend. Uji dengan payload yang menghasilkan efek terlihat (alert, delay, callback), bukan dengan asumsi.

## 5. Fragmentasi dan obfuscation payload

**SQLi**

```text
UN/**/ION SEL/**/ECT
/*!50000UNION*/ /*!50000SELECT*/
%55NION %53ELECT
UNION%0ASELECT
```

**XSS**

```text
<svg/onload=alert(1)>
<img src=x onerror=alert(1)>
<ScRiPt>alert(1)</sCrIpT>
<object data="javascript:alert(1)">
```

**Command injection**

```text
;id
%0aid
$(id)
`id`
|id
```

**Path traversal**

```text
..%2f..%2fetc%2fpasswd
%252e%252e%252f
..%5c..%5c
..;/..;/
/./../
```

Gunakan **Hackvertor** di Burp untuk menerapkan encoding berlapis tanpa menulis ulang payload; simpan kombinasi yang berhasil.

## 6. Request smuggling sebagai bypass WAF

Jika backend menerima `Transfer-Encoding` yang diabaikan WAF, request bisa "dibelah": WAF menilai bagian pertama, backend memproses bagian kedua.

```text
Transfer-Encoding: chunked
Transfer-Encoding : chunked
Transfer-Encoding: xchunked
Content-Length: 13
```

Hanya dengan izin eksplisit; desync dapat memutus koneksi pengguna lain. Verifikasi dengan respons tidak konsisten pada koneksi yang sama, bukan dengan tebakan.

## 7. Alur di Burp

1. **Differential harness** — Repeater dengan tiga tab: baseline, payload mentah, payload ter-encode. Bandingkan status, panjang, dan body.
2. **Hackvertor** — encode/decode berlapis pada posisi payload.
3. **Intruder** — payload processing untuk encoding otomatis; batasi thread.
4. **Turbo Intruder** — smuggling dan uji rate-limit yang terukur.
5. **Collaborator** — bukti OOB untuk RCE/SSRF yang tersembunyi di balik WAF.
6. **Logger++** — arsip request/response; bukti harus menunjukkan payload final dan respons backend.

## 8. Verifikasi, bukan status code

| Klaim | Bukti |
|---|---|
| XSS lolos WAF | `alert`/callback di browser atau Collaborator |
| SQLi lolos | Delay konsisten, data terbaca, atau error backend |
| RCE lolos | `id`/`hostname` atau callback OOB |
| Traversal lolos | Isi file yang benar-benar terbaca |
| Smuggling | Respons tidak konsisten pada koneksi yang sama |

403 → 200 tanpa efek bukan bypass. Simpan payload final + kondisi WAF (vendor, waktu, konfigurasi yang terlihat) agar temuan reproducible.

## 9. Batas dan etika

- Hanya pada aset di scope; WAF CDN pihak ketiga sering di luar izin.
- Jangan membanjiri WAF: rate tinggi = DoS bagi klien dan noise bagi SOC.
- Jangan memakai bypass untuk mengakses data di luar bukti minimum.
- Jangan menyerang origin di luar kontrak meski "lebih mudah".
- Dokumentasikan teknik yang berhasil; WAF berubah setiap waktu.

## 10. Jebakan

1. **WAF menormalisasi** — payload terlihat lolos di respons WAF, bukan di backend.
2. **Cache CDN** — respons lama membuat uji tampak konsisten padahal tidak.
3. **Browser vs tool** — browser menormalkan URL/HTML yang tidak dilakukan curl.
4. **Double decoding** — backend yang decode dua kali membuat single-encode gagal.
5. **Charset tidak didukung** — payload lolos WAF tapi ditolak backend.
6. **Learning mode** — WAF yang baru aktif menyesuaikan aturan; ulangi uji dari baseline.
7. **False positive 200** — halaman error yang dikembalikan dengan status 200.

## Best Practices

- Cari origin langsung sebelum berurusan dengan WAF.
- Satu variabel per percobaan; catat mana yang mengubah perilaku.
- Encode sesuai decoder backend, bukan sesuai selera.
- Buktikan eksekusi, bukan status.
- Perlakukan bypass sebagai temuan: jelaskan kelas aturan yang dilewati dan dampaknya.
- Tautkan prosedur HTTP ke [burp-workflow.md](./burp-workflow.md) dan [header-manipulation.md](./header-manipulation.md).
