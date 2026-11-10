---
name: "Header Manipulation — X-Forwarded-For, User-Agent, dan Injeksi di Header"
description: "Teknik profesional memanipulasi header request di Burp Suite: spoofing IP lewat X-Forwarded-For, XSS/shell/SQLi lewat User-Agent dan Referer, Host header poisoning, CRLF, request smuggling, override header, cara verifikasi, false positive, dan batas etika."
tags: [headers, x-forwarded-for, user-agent, host-header, crlf, smuggling, burp, xss, command-injection]
---

# Header Manipulation

Header adalah input pengguna yang sering diperlakukan sebagai metadata tepercaya. Di situlah nilainya: server, proxy, CDN, dan logger mempercayai nilai yang sebenarnya bisa dikendalikan penyerang.

## 1. Kapan header menjadi vektor

Empat kondisi yang membuat header layak diuji:

1. **Dipercaya untuk keputusan** — IP klien, host, skema, atau peran diambil dari header.
2. **Dicatat dan ditampilkan** — dashboard admin, SIEM, email, tiket, log viewer.
3. **Diteruskan ke sistem lain** — shell, database, template, API internal.
4. **Diurai berbeda** — proxy dan backend tidak sepakat soal batas request (smuggling).

Jika tidak ada satu pun, manipulasi header hanya menambah noise.

## 2. Katalog header dan hipotesis

| Header | Hipotesis | Contoh nilai uji |
|---|---|---|
| `X-Forwarded-For` | Bypass allowlist IP, rate limit, atau "internal only" | `127.0.0.1`, `::1`, `10.0.0.1` |
| `X-Real-IP`, `X-Client-IP` | Sama, sering dipakai bergantian | idem |
| `X-Originating-IP`, `True-Client-IP`, `CF-Connecting-IP` | Bergantung pada CDN/proxy | idem |
| `Forwarded` | Standar RFC 7239, sering terlewat | `for=127.0.0.1;proto=https` |
| `Host` | Password reset poisoning, redirect absolut, cache poisoning | `evil.example`, `127.0.0.1` |
| `X-Forwarded-Host`, `X-Host` | Cache poisoning dan URL absolut | `evil.example` |
| `User-Agent` | Stored XSS di panel admin, SQLi, command injection | penanda unik + payload |
| `Referer` | XSS, open redirect, cache poisoning | `https://evil.example/` |
| `X-Original-URL`, `X-Rewrite-URL` | Bypass kontrol akses berbasis path | `/admin` |
| `X-HTTP-Method-Override` | Bypass method atau CSRF | `PUT`, `DELETE` |
| `Content-Type`, `charset` | Parser confusion, upload bypass | `application/json`, `text/xml` |
| `Transfer-Encoding`, `Content-Length` | Request smuggling (CL.TE, TE.CL) | lihat §4 |
| `Origin` | CORS salah konfigurasi | `https://evil.example` |
| `Authorization`, `X-Auth-*` | Skema lemah, token tanpa verifikasi | token uji |
| `Cookie` | Injeksi, deserialisasi, trust berlebih | nilai uji |

> Nilai uji harus unik per request (mis. `127.0.0.1-canary-7f3a`) agar bisa dilacak di log, respons, atau cache.

## 3. Pola payload

**Spoofing IP**

```text
127.0.0.1
::1
2130706433        # representasi desimal 127.0.0.1
0177.0.0.1        # oktal
0.0.0.0
10.0.0.1
```

Selalu coba juga **duplikasi header** (`X-Forwarded-For: 127.0.0.1` dua kali) dan urutan berbeda — sebagian stack mengambil nilai pertama, sebagian terakhir.

**XSS lewat header**

```text
User-Agent: <svg onload=alert(document.domain)>
Referer: "><script>alert(1)</script>
```

Header jarang dirender langsung; yang realistis adalah **stored XSS** di panel admin, log viewer, atau email notifikasi. Karena itu gunakan penanda unik, lalu cari penandanya di semua tempat yang menampilkan request.

**Command injection**

```text
User-Agent: ; sleep 5
User-Agent: $(sleep 5)
User-Agent: `sleep 5`
User-Agent: | sleep 5
User-Agent: %0a sleep 5
```

Deteksi dengan waktu atau callback ke Collaborator; setelah terkonfirmasi, eksekusi hanya perintah identitas (`id`, `hostname`).

**SQL injection**

```text
User-Agent: ' OR 1=1-- -
X-Forwarded-For: '; WAITFOR DELAY '0:0:5'-- -
```

Header sering masuk ke query log atau audit; uji time-based dengan baseline tiga kali.

**CRLF / response splitting**

```text
X-Test: value%0d%0aSet-Cookie:canary=1
X-Test: value%0d%0a%0d%0a<script>alert(1)</script>
```

Buktikan header/body baru muncul di respons, bukan hanya di log.

**Host header poisoning**

```text
Host: evil.example
X-Forwarded-Host: evil.example
X-Forwarded-Proto: http
```

Cari efek: link reset password, redirect, absolute URL di email, cache key.

## 4. Request smuggling (hati-hati)

Uji hanya jika RoE mengizinkan; desync dapat merusak koneksi pengguna lain.

```text
# CL.TE
POST / HTTP/1.1
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

Gunakan ekstensi **HTTP Request Smuggler** atau **Turbo Intruder** dengan payload terukur, bukan menebak di produksi. Bukti yang sah: request berikutnya di koneksi yang sama menerima respons yang salah, atau waktu respons berbeda konsisten.

## 5. Alur kerja di Burp

1. **Repeater** — duplikasi request baseline, tambah satu header, bandingkan status, panjang, waktu, dan body.
2. **Match/Replace** (Proxy → Options) — suntikkan header ke semua request saat menguji konsistensi; matikan setelah selesai.
3. **Intruder** — posisi payload di nilai header; gunakan Pitchfork untuk kombinasi header, bukan Cluster Bomb yang meledak.
4. **Turbo Intruder / HTTP Request Smuggler** — hanya untuk desync dan uji throughput terukur.
5. **Collaborator** — OOB untuk command injection, SSRF via `Host`/`X-Forwarded-Host`.
6. **Logger++** — arsip request/response untuk bukti.
7. **Bandingkan respons** — cek `Age`, `X-Cache`, `CF-Cache-Status` untuk membuktikan cache poisoning.
8. **Ulangi dari sesi bersih** — pastikan hasil bukan efek sesi sendiri.

## 6. Verifikasi dan false positive

| Klaim | Bukti yang sah | False positive khas |
|---|---|---|
| Bypass IP allowlist | Akses ke konten/aksi terbatas, bukan sekadar 200 | Halaman error yang tetap 200 |
| Stored XSS via UA | Payload tampil di panel/log viewer sebagai HTML | Refleksi di header respons yang tidak dirender |
| Command injection | Delay konsisten atau callback | Latensi jaringan |
| SQL injection | Delay terukur, berulang | Cache atau rate limit |
| Cache poisoning | Respons beracun diterima dari sesi lain | Cache pribadi browser |
| CRLF | Header/body baru di respons | Encoding yang dinormalisasi |
| Smuggling | Desync konsisten di koneksi sama | Timeout acak |

Status 200 bukan bukti. Bukti adalah perubahan perilaku yang bisa diulang.

## 7. Dampak dan pemetaan

| Temuan | CWE |
|---|---|
| Auth bypass via header tepercaya | CWE-290 |
| Netralisasi header tidak memadai | CWE-644 |
| XSS lewat header yang dirender | CWE-79 |
| Command injection | CWE-78 |
| SQL injection | CWE-89 |
| CRLF injection | CWE-113 |
| Request smuggling | CWE-444 |
| Open redirect / host poisoning | CWE-601 |
| SSRF lewat header | CWE-918 |

Severity mengikuti dampak nyata: bypass admin > cache poisoning terbatas > refleksi tanpa eksekusi.

## 8. Batas dan etika

- **Cache poisoning** hanya dengan nilai canary unik; jangan meracuni cache yang dipakai pengguna nyata.
- **Smuggling** dan **CRLF** dapat memutus koneksi; butuh izin eksplisit dan window khusus.
- **XSS ke admin** hanya dengan akun uji atau persetujuan; jangan menargetkan staf sungguhan.
- **Command injection** berhenti di perintah identitas; jangan membaca data atau membuat persistence.
- Hormati rate limit; header fuzzing cepat memicu WAF dan lockout.

## 9. Jebakan

1. **WAF menormalisasi header** — payload terlihat "berhasil" di respons WAF, bukan backend.
2. **Duplikasi header** — server memilih nilai pertama, terakhir, atau menggabungkan.
3. **HTTP/2** — nama header dipaksa lowercase dan hop-by-hop header ditolak.
4. **Proxy menambah XFF sendiri** — nilai asli tetap appended; cek urutan.
5. **CDN menyembunyikan Host** — uji langsung ke origin bila diizinkan.
6. **Cache key tidak memuat header** — respons berubah tapi tidak tersimpan; klaim poisoning salah.
7. **Log viewer meng-escape** — XSS tidak eksekusi meski payload terlihat.

## Best Practices

- Mulai dari hipotesis: header ini dipakai untuk apa di aplikasi ini?
- Satu header, satu perubahan, satu perbandingan.
- Gunakan canary unik agar efek bisa dilacak.
- Verifikasi dengan bukti perilaku, bukan status code.
- Hentikan uji berisiko (smuggling, cache poisoning) setelah bukti minimum.
- Simpan request mentah dan respons sebagai bukti; tautkan ke [burp-workflow.md](./burp-workflow.md).
- Jika header diblokir WAF, encoding dan obfuscation yang sah ada di [waf-evasion.md](./waf-evasion.md).
