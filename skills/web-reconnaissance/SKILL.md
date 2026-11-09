---
name: web-reconnaissance
description: "Recon web/SPA: inventarisasi dan analisis chunk JS (source map, bundle, endpoint dan rute tersembunyi), baca network tab/HAR dan traffic API, token di localStorage/cookie, teknologi, subdomain, wayback. Muat saat memetakan aplikasi sebelum scan atau pentest."
license: MIT
compatibility: opencode
metadata:
  audience: web-pentesters
  workflow: reconnaissance
  source: owasp-wstg
---

# Web Recon Sederhana

Recon yang berguna berdiri di atas tiga sumber, dan ketiganya saling mengunci:

| Sumber | Menjawab | Detail |
|---|---|---|
| **Chunk JavaScript** | Apa yang *mungkin* dilakukan aplikasi | [references/js-chunk-discovery.md](references/js-chunk-discovery.md) |
| **Traffic network** | Apa yang *benar-benar* dilakukan aplikasi | [references/network-analysis.md](references/network-analysis.md) |
| **Isi chunk** | Kredensial, rute, dan fitur yang disembunyikan | [references/js-chunk-analysis.md](references/js-chunk-analysis.md) |

Kerjakan berurutan: kumpulkan chunk → rekam traffic saat chunk dipakai → analisis. Membalik urutannya membuat Anda menganalisis berkas yang salah.

## Decision Frame

- **Ruang lingkup** — hanya host yang ada di scope. Bila request mengarah ke CDN atau layanan pihak ketiga, catat sebagai konteks; jangan diuji.
- **Berhenti mengumpulkan chunk** bila tiga rute utama sudah terpetakan **dan** satu putaran crawl tidak menambah nama chunk baru. Setelah itu, berhenti menambah dan mulai membaca.
- **Source map** — `.map` membalas 200 = jalur utama, baca kode aslinya. Bila tidak ada, beautify dan batasi ke entry chunk + chunk bernama sensitif; vendor chunk dilewati tanpa dibaca.
- **Kunci rahasia** hanya dilaporkan setelah format cocok dan uji baca non-destruktif lolos. Kunci publik (`pk_`, `AIza`, DSN Sentry) dicatat sebagai konteks, bukan temuan.
- **Status endpoint** — 403 = kandidat masalah otorisasi terkuat, 401 = kandidat setelah login, 404 = berhenti di situ. Maksimal dua varian path per endpoint tanpa persetujuan eksplisit.
- **Batas waktu** — 90 menit untuk satu target kecil. Bila lewat, tulis laporan dengan bukti yang sudah ada daripada mengejar kelengkapan.

## 1. Inventarisasi Chunk JavaScript

Buka halaman → `Ctrl+Shift+P` → **Coverage** → reload → navigasi satu per satu. Catat setiap berkas `.js` yang muncul.

```bash
curl -s https://target.tld/ | grep -oE '<script[^>]*src="[^"]+"'
ls -la   # setelah menyimpan chunk ke direktori kerja
```

Yang dicari lebih dulu: `runtime.*.js` (berisi tabel chunk), `main.*.js`, dan chunk dengan nama sensitif (`admin`, `internal`, `billing`).

> Baca [references/js-chunk-discovery.md](references/js-chunk-discovery.md) bila chunk lazy tidak muncul, bila perlu mengekstrak tabel chunk dari `__webpack_require__.u`, atau bila target punya banyak rute dan perlu crawl (`katana -jc`).

## 2. Rekam dan Baca Traffic

1. Buka DevTools **sebelum** navigasi, centang **Preserve log** dan **Disable cache**.
2. Unregister service worker (Application → Service Workers).
3. Filter: `-domain:google-analytics.com -domain:googletagmanager.com`, lalu `mime-type:application/json`.
4. Untuk setiap request, catat **Initiator** — kolom ini menghubungkan endpoint ke chunk pemanggilnya.

Klik kanan → **Save all as HAR with content** bila traffic perlu dianalisis ulang atau diserahkan ke orang lain.

> Baca [references/network-analysis.md](references/network-analysis.md) untuk resep filter, semantik 401/403/404, GraphQL dan WebSocket, analisis HAR dengan `jq`, serta aturan replay yang aman.

## 3. Analisis Isi Chunk

```bash
npx js-beautify -f main.a1b2.js -o main.pretty.js
grep -oiE '"(https?://[^"]+|/api/v[0-9][^"]*)"' main.pretty.js | sort -u
grep -oiE 'path\s*:\s*"[^"]+"' main.pretty.js | sort -u
```

| Cari | Pola contoh | Arti |
|---|---|---|
| Endpoint API | `/api/v2/`, `baseURL:` | Permukaan uji |
| Rute tersembunyi | `path:"/internal/reports"` | Fitur tak tertaut di UI |
| GraphQL | `operationName`, `/graphql` | Daftar fungsi backend |
| Realtime | `wss://`, `new WebSocket` | Kanal yang sering lupa authz |
| Flag fitur | `isEnabled(`, `feature_` | Fitur di balik flag |
| Host internal | `.internal`, `10.x.x.x` | Jaringan yang tidak publik |

**Triage kunci:** `AKIA…`/`ASIA…` (AWS), `sk_live_` (Stripe secret), `ghp_` (GitHub), blok `BEGIN PRIVATE KEY`, connection string bersandi = **asli**. `pk_live_`, `AIza…`, DSN Sentry, `client_id` OAuth = **publik menurut desain**, catat sebagai konteks.

> Baca [references/js-chunk-analysis.md](references/js-chunk-analysis.md) untuk memulihkan source map (`sourcesContent`), membaca `__NEXT_DATA__`/`__NUXT__`, menavigasi modul webpack, dan daftar false positive yang harus dibuang.

## 4. Petakan dan Uji Endpoint

Gabungkan endpoint dari langkah 1–3, lalu buat matriks:

| Method | Path | Auth | Status | Catatan |
|---|---|---|---|---|
| GET | `/api/v1/users/1042` | Bearer | 200 | ID berurutan → kandidat IDOR |
| POST | `/api/v1/admin/impersonate` | Cookie | 403 | Ada, ditolak untuk peran ini |

Probe path dokumentasi sekali: `/api/docs`, `/swagger`, `/openapi.json`, `/graphql`, `/actuator`.

Uji minimal, satu varian per hipotesis. 403 lebih menarik daripada 404.

## 5. Storage, Token, dan Sesi

DevTools → **Application**:

- **Local Storage** → token, objek user, `tenantId`, flag.
- **Session Storage** → token sementara.
- **Cookies** → periksa `HttpOnly`, `Secure`, `SameSite`. Cookie sesi tanpa `HttpOnly` = dapat dibaca JS (temuan terverifikasi, bukan dugaan).

```javascript
console.log(localStorage, sessionStorage, document.cookie);
```

Bandingkan dengan apa yang dikirim di header `Authorization` pada tab Network: token di JS + dikirim via header berarti XSS berujung pencurian sesi.

## 6. Identifikasi Teknologi dan Versi

| Sinyal | Teknologi |
|---|---|
| `Server`, `X-Powered-By` | Web server / bahasa |
| `__NEXT_DATA__` | Next.js |
| `window.__NUXT__` | Nuxt |
| `ng-version` pada elemen root | Angular (versi ikut terbaca) |
| `PHPSESSID`, `JSESSIONID` | PHP, Java |
| `meta name="generator"` | CMS (WordPress, Drupal) |

Ambil versi bila memungkinkan — versi tanpa patch adalah dasar pencarian CVE.

## 7. CVE yang Relevan

Cari per teknologi + versi: `nginx 1.25.0 CVE`, `Next.js 14.0.0 CVE`, `WordPress 6.4 CVE`.

Sumber: NVD (by product/version), pencarian web untuk laporan terbaru, `searchsploit --cve <teknologi>` (hanya membaca daftar).

Catat: **CVE ID**, **CVSS**, **versi terpengaruh**, status (Published/Reserved/Rejected). Jangan menyertakan exploit atau PoC — cukup identifikasi.

## Gotchas

- **Chunk lazy tidak muncul sebelum rutenya dibuka.** Tab Sources pada halaman awal menampilkan sebagian kecil kode. Jangan menyimpulkan "tidak ada kode admin" hanya karena belum terlihat — pakai Coverage dan navigasi UI.
- **"Disable cache" tidak melepas service worker.** SW dapat menyajikan response lama; HAR yang diambil tanpa unregister tidak mencerminkan server.
- **Hash chunk berubah setiap deploy.** `_next/static/chunks/abc123.js` besok menjadi 404. Simpan salinan lokal saat masih 200.
- **Manifest yang membalas 200 belum tentu manifest.** Bila isinya `<!doctype html`, itu SPA fallback.
- **Regex secret cocok pada base64 dan hash.** Periksa prefiks dan panjang sebelum menyimpulkan kebocoran.
- **Kunci Google/Firebase dibatasi per HTTP referrer.** Gagal dipakai dari origin lain bukan bukti kunci aman, dan berhasil dipakai bukan bukti kebocoran.
- **403 kadang disamarkan menjadi 404.** Bila response 404 konsisten tanpa body, coba sekali dengan sesi sah.
- **HAR berisi token dan cookie.** Jangan commit ke repo; redaksi sebelum dibagikan.
- **Tanpa Preserve log, request pertama hilang** dan endpoint autentikasi awal tidak terlihat.

## Output Laporan

- **Teknologi**: [backend, frontend, server, versi]
- **Inventaris chunk**: [jumlah, entry, chunk bernama sensitif, ada/tidak source map]
- **Endpoint ditemukan**: [matriks method–path–status]
- **Rute tersembunyi**: [path + nama chunk bukti]
- **Token/sesi**: [lokasi penyimpanan, flag cookie, dikirim bagaimana]
- **Kunci rahasia**: [asli vs publik, masing-masing dengan lokasi berkas]
- **CVE terkait**: [ID + CVSS + versi terpengaruh]
- **Lanjutan**: [endpoint prioritas untuk `web-app-scan` atau `web-pentest-payloads`]

## Referensi

| Berkas | Baca saat |
|---|---|
| [js-chunk-discovery.md](references/js-chunk-discovery.md) | Chunk tidak lengkap, perlu tabel chunk webpack, crawl banyak rute, atau mencari source map |
| [js-chunk-analysis.md](references/js-chunk-analysis.md) | Ingin membaca isi bundle: endpoint, rute, state framework, triage kunci, false positive |
| [network-analysis.md](references/network-analysis.md) | Perlu filter Network, semantik status, GraphQL/WebSocket, analisis HAR, atau replay aman |
