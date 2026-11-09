---
name: web-reconnaissance
description: "Recon web/SPA: inventarisasi dan analisis chunk JS (source map, bundle, endpoint dan rute tersembunyi), rekam network tab lewat Chrome DevTools MCP atau HAR manual, baca storage browser (localStorage, sessionStorage, cookie, IndexedDB, Cache Storage), triage token dan sesi, teknologi, subdomain, wayback. Muat saat memetakan aplikasi sebelum scan atau pentest."
license: MIT
compatibility: opencode
metadata:
  audience: web-pentesters
  workflow: reconnaissance
  source: owasp-wstg
---

# Web Recon

Recon yang berguna berdiri di atas empat sumber, dan keempatnya saling mengunci:

| Sumber | Menjawab | Alat | Detail |
|---|---|---|---|
| **Chunk JavaScript** | Apa yang *mungkin* dilakukan aplikasi | Coverage, `list_network_requests(["Script"])` | [js-chunk-discovery.md](references/js-chunk-discovery.md) |
| **Traffic network** | Apa yang *benar-benar* dikirim aplikasi | `chrome-devtools-mcp` atau HAR manual | [network-analysis.md](references/network-analysis.md) |
| **Storage browser** | Apa yang *dipegang* klien | `evaluate_script` atau panel Application | [browser-storage.md](references/browser-storage.md) |
| **Isi chunk** | Kredensial, rute, dan fitur yang disembunyikan | beautify + grep | [js-chunk-analysis.md](references/js-chunk-analysis.md) |

Urutannya tidak boleh dibalik: kumpulkan chunk → rekam traffic saat chunk dipakai → baca storage → analisis. Membalik urutannya membuat Anda menganalisis berkas yang salah.

Bila MCP `chrome-devtools-mcp` aktif, keempat sumber itu dapat diambil tanpa klik manual — lihat [chrome-devtools-mcp.md](references/chrome-devtools-mcp.md).

## Decision Frame

- **Ruang lingkup** — hanya host yang ada di scope. Bila request mengarah ke CDN atau layanan pihak ketiga, catat sebagai konteks; jangan diuji.
- **MCP atau manual?** — periksa daftar tool: bila `list_network_requests` dan `evaluate_script` tersedia, pakai MCP dan simpan body ke disk. Bila tidak, jalankan prosedur manual dan catat alat yang benar-benar dipakai. Jangan menulis "otomatis" untuk capture yang diklik tangan.
- **Berhenti mengumpulkan chunk** bila tiga rute utama sudah terpetakan **dan** satu putaran crawl tidak menambah nama chunk baru. Setelah itu berhenti menambah dan mulai membaca. Source map: `.map` membalas 200 = jalur utama, baca kode aslinya; bila tidak ada, beautify entry chunk + chunk bernama sensitif, lewati vendor chunk.
- **Storage dibaca berlapis** — nama kunci lebih dulu, nilai hanya bila bentuknya mencurigakan. Kunci publik (`pk_`, `AIza`, DSN Sentry) dicatat sebagai konteks, bukan temuan. Token tidak pernah ditulis utuh di laporan, dan data pengguna nyata disamarkan.
- **Status endpoint** — 403 = kandidat masalah otorisasi terkuat, 401 = kandidat setelah login, 404 = berhenti di situ. Maksimal dua varian path per endpoint tanpa persetujuan eksplisit.
- **Batas waktu** — 90 menit untuk satu target kecil. Bila lewat, tulis laporan dengan bukti yang sudah ada daripada mengejar kelengkapan.

## 1. Siapkan Sesi

| Setelan | MCP | Manual |
|---|---|---|
| Profil bersih | `new_page(isolatedContext: "recon")` | jendela incognito baru |
| Service worker dilepas | `list_pages` → periksa `sw-N`, unregister di Application | Application → Service Workers → Unregister |
| Riwayat request dijaga | `includePreservedRequests: true` (tiga navigasi terakhir) | centang **Preserve log** |
| Cache diabaikan saat reload | `navigate_page(type: "reload", ignoreCache: true)` | centang **Disable cache** |

Profil bersih bukan formalitas: cookie dari sesi Anda sendiri dapat membuat aplikasi tampak sudah login, dan storage sisa akan mencemari temuan. Catat juga waktu capture, versi build (bila terlihat), dan apakah target menyajikan source map.

## 2. Inventarisasi Chunk JavaScript

Manual: buka halaman → `Ctrl+Shift+P` → **Coverage** → reload → navigasi satu per satu. Catat setiap berkas `.js` yang muncul.

Otomatis: `list_network_requests` dengan `resourceTypes: ["Script"]`, lalu `get_network_request` per `reqid` ke `responseFilePath` — body tersimpan sebagai berkas, bukan memenuhi konteks.

```bash
curl -s https://target.tld/ | grep -oE '<script[^>]*src="[^"]+"'
ls -la   # setelah menyimpan chunk ke direktori kerja
```

Yang dicari lebih dulu: `runtime.*.js` (berisi tabel chunk), `main.*.js`, dan chunk dengan nama sensitif (`admin`, `internal`, `billing`).

> Baca [js-chunk-discovery.md](references/js-chunk-discovery.md) bila chunk lazy tidak muncul, bila perlu mengekstrak tabel chunk dari `__webpack_require__.u`, atau bila target punya banyak rute dan perlu crawl (`katana -jc`).

## 3. Rekam Traffic

1. Buka tangkapan **sebelum** navigasi; tanpa itu request autentikasi awal hilang.
2. Unregister service worker, lalu muat ulang tanpa cache.
3. Navigasi UI satu per satu untuk memicu rute lazy — chunk di balik peran lain tidak akan muncul sendiri.
4. Filter: `-domain:google-analytics.com -domain:googletagmanager.com`, lalu `mime-type:application/json` untuk melihat API.
5. Catat **Initiator** — kolom ini menghubungkan endpoint ke chunk pemanggilnya.

Untuk analisis ulang atau serah terima, simpan traffic sebagai HAR (**Save all as HAR with content**). HAR berisi token dan cookie: jangan di-commit.

> Baca [network-analysis.md](references/network-analysis.md) untuk resep filter, semantik 401/403/404, GraphQL dan WebSocket, analisis HAR dengan `jq`, serta aturan replay yang aman. Untuk otomasi — filter per tipe resource, simpan body ke disk, penyisipan header auth, dan logpoint lewat source map — lihat [chrome-devtools-mcp.md](references/chrome-devtools-mcp.md).

## 4. Analisis Isi Chunk

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

> Baca [js-chunk-analysis.md](references/js-chunk-analysis.md) untuk memulihkan source map (`sourcesContent`), membaca `__NEXT_DATA__`/`__NUXT__`, menavigasi modul webpack, dan daftar false positive yang harus dibuang.

## 5. Storage, Token, dan Sesi

Enam tempat, dan semuanya perlu diperiksa — bukan hanya yang mudah terlihat:

| Storage | Terbaca dari JS | Yang dicari |
|---|---|---|
| `localStorage` | ya | token bearer, objek user, `tenantId`, peran, feature flag |
| `sessionStorage` | ya | token sementara, state wizard, sisa langkah sebelumnya |
| Cookie | hanya non-`HttpOnly` | nama sesi, flag `Secure`/`SameSite`, cakupan `Domain`, umur |
| IndexedDB | ya (async) | cache respons API, data offline, token di dalam record |
| Cache Storage | ya (async) | HTML/JSON yang di-cache service worker |
| OPFS | ya (async) | berkas besar, ekspor, arsip yang tidak perlu ada di klien |

```javascript
localStorage; sessionStorage; document.cookie;      // sinkron
await caches.keys();                                 // Cache Storage
await indexedDB.databases();                         // nama + versi database
```

Skrip dump lengkap — aman untuk `evaluate_script`, memotong nilai panjang, tidak melempar error — ada di [browser-storage.md](references/browser-storage.md) §2.

**`document.cookie` tidak menampilkan cookie `HttpOnly`.** Cookie sesi yang tidak muncul di JS bisa tetap ada di panel Application dan di header `Cookie` pada request. Karena itu: bandingkan tiga tempat sebelum menyimpulkan apa pun.

Token di storage baru menjadi temuan bila ada jalur bacanya. Token di `localStorage` dibaca oleh **setiap** skrip di origin itu, termasuk skrip pihak ketiga yang dimuat halaman — dan bila token yang sama dikirim sebagai `Authorization` di Network, dampaknya adalah seluruh permukaan API yang menerimanya. Cookie sesi tanpa `HttpOnly` umumnya Medium (CWE-1004), bukan High.

> Baca [browser-storage.md](references/browser-storage.md) untuk skrip IndexedDB dan Cache Storage, decode JWT tanpa verifikasi, triage lima jenis token, pemetaan storage → temuan, dan aturan redaksi.

## 6. Petakan dan Uji Endpoint

Gabungkan endpoint dari langkah 2–5, lalu buat matriks:

| Method | Path | Auth | Status | Catatan |
|---|---|---|---|---|
| GET | `/api/v1/users/1042` | Bearer | 200 | ID berurutan → kandidat IDOR |
| POST | `/api/v1/admin/impersonate` | Cookie | 403 | Ada, ditolak untuk peran ini |

Probe path dokumentasi sekali: `/api/docs`, `/swagger`, `/openapi.json`, `/graphql`, `/actuator`.

Uji minimal, satu varian per hipotesis. 403 lebih menarik daripada 404.

## 7. Identifikasi Teknologi dan Versi

| Sinyal | Teknologi |
|---|---|
| `Server`, `X-Powered-By` | Web server / bahasa |
| `__NEXT_DATA__` | Next.js |
| `window.__NUXT__` | Nuxt |
| `ng-version`, `ng-reflect-*` | Angular (versi ikut terbaca) |
| `PHPSESSID`, `JSESSIONID` | PHP, Java |
| `meta name="generator"` | CMS (WordPress, Drupal) |

Ambil versi bila memungkinkan — versi tanpa patch adalah dasar pencarian CVE.

## 8. CVE yang Relevan

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
- **Storage kosong belum tentu bersih.** Bisa karena profil baru, atau karena token hidup di memori dan dibuat ulang per request — periksa header `Authorization` sebelum menyimpulkan.
- **`document.cookie` yang kosong bukan bukti tidak ada cookie.** `HttpOnly` menyembunyikannya dari JS, bukan dari Application panel maupun header request.
- **MCP tidak punya tool storage.** `localStorage`, cookie, IndexedDB, dan Cache Storage hanya terbaca lewat `evaluate_script`; tanpa menjalankannya, "tidak ada storage" adalah asumsi, bukan hasil.
- **`list_network_requests` menghapus riwayat per navigasi.** `includePreservedRequests` hanya menyimpan tiga navigasi terakhir; simpan body ke disk per gelombang.
- **Membaca seluruh IndexedDB dapat membekukan tab.** Batasi dengan jumlah record dan mulai dari nama object store.
- **Storage bersifat per origin.** `app.target.tld` dan `api.target.tld` tidak berbagi apa pun — dump keduanya bila keduanya dipakai.

## Output Laporan

- **Teknologi**: [backend, frontend, server, versi]
- **Alat capture**: [MCP / manual, HAR disimpan di mana]
- **Inventaris chunk**: [jumlah, entry, chunk bernama sensitif, ada/tidak source map]
- **Endpoint ditemukan**: [matriks method–path–status]
- **Rute tersembunyi**: [path + nama chunk bukti]
- **Storage**: [jenis, nama kunci, bentuk nilai, dikirim sebagai apa]
- **Token/sesi**: [lokasi penyimpanan, flag cookie, header pengirim]
- **Kunci rahasia**: [asli vs publik, masing-masing dengan lokasi berkas]
- **CVE terkait**: [ID + CVSS + versi terpengaruh]
- **Lanjutan**: [endpoint prioritas untuk `web-app-scan` atau `web-pentest-payloads`]

## Referensi

| Berkas | Baca saat |
|---|---|
| [js-chunk-discovery.md](references/js-chunk-discovery.md) | Chunk tidak lengkap, perlu tabel chunk webpack, crawl banyak rute, atau mencari source map |
| [js-chunk-analysis.md](references/js-chunk-analysis.md) | Ingin membaca isi bundle: endpoint, rute, state framework, triage kunci, false positive |
| [network-analysis.md](references/network-analysis.md) | Perlu filter Network, semantik status, GraphQL/WebSocket, analisis HAR, atau replay aman |
| [browser-storage.md](references/browser-storage.md) | Perlu dump localStorage/cookie/IndexedDB/Cache Storage, decode JWT, atau mengubah storage menjadi temuan |
| [chrome-devtools-mcp.md](references/chrome-devtools-mcp.md) | Perlu otomasi: daftar request per tipe, simpan body ke disk, header auth, logpoint, atau fallback manual |
