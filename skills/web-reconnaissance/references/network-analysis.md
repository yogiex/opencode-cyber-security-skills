---
name: "Analisis Traffic Network"
description: "Cara membaca tab Network secara sistematis: setup capture yang benar, waterfall dan initiator, filter resep, matriks endpoint, GraphQL/WebSocket, ekspor HAR dan analisisnya dengan jq, serta replay request dengan batas aman."
tags: [network, devtools, har, graphql, websocket, api, waterfall, initiator, jq, replay]
---

# Analisis Traffic Network

Tab Network adalah sumber kebenaran tentang apa yang **benar-benar** dikirim aplikasi ke server — termasuk endpoint yang tidak disebut di kode mana pun yang berhasil Anda baca. Chunk JS memberi tahu apa yang *mungkin* dipanggil; Network membuktikan apa yang *dipanggil*, dengan header, urutan, dan status sebenarnya.

> Prosedur di bawah ini manual. Bila MCP `chrome-devtools-mcp` aktif, langkah yang sama dapat dijalankan lewat `list_network_requests` dan `get_network_request` — lihat [chrome-devtools-mcp.md](chrome-devtools-mcp.md). Untuk membaca cookie dan storage yang muncul di request, lihat [browser-storage.md](browser-storage.md).

## 1. Setup Capture yang Benar

Capture yang salah menghasilkan kesimpulan yang salah. Tiga hal wajib sebelum merekam:

| Setelan | Cara | Kenapa |
|---|---|---|
| DevTools dibuka **sebelum** navigasi | Buka F12 lalu `F5`, atau centang **Preserve log** | Request saat load awal hilang bila panel dibuka belakangan |
| **Disable cache** dicentang | Tab Network | Response dari cache tidak menampilkan header server |
| Service worker dilepas | Application → Service Workers → **Unregister** | SW dapat menyajikan response lama sehingga HAR tidak mencerminkan server |

Bila target adalah aplikasi mobile atau desktop, DevTools tidak berlaku. Gunakan proxy (Burp, Caido, mitmproxy) dan rekam dari sana; konsep membaca traffic tetap sama.

Untuk situs yang memuat puluhan request pihak ketiga, sembunyikan dulu derau:

```
-domain:google-analytics.com -domain:googletagmanager.com -domain:doubleclick.net -domain:facebook.net
```

Tempel ke kotak filter. Sisanya biasanya tinggal belasan request yang relevan.

## 2. Membaca Waterfall dan Initiator

Kolom yang benar-benar berguna (klik kanan header untuk menampilkan yang tersembunyi):

| Kolom | Artinya | Yang perlu dicurigai |
|---|---|---|
| **Name** | Path | Nama generik (`/data`, `/list`) sering berarti API internal |
| **Status** | Kode HTTP | 401/403 pada endpoint tak terdokumentasi = ada tapi dijaga |
| **Type** | `fetch`, `xhr`, `script`, `document`, `ws` | `document` pada path API = SPA fallback, bukan API |
| **Initiator** | Fungsi/berkas pemicu | Menghubungkan endpoint ke chunk — inti pemetaan |
| **Size** | Ukuran terkirim | Response 0 B pada 200 = filter kosong, bukan data |
| **Time** | Total | Bandingkan TTFB vs Content Download |

**Initiator** adalah kolom yang paling sering diabaikan dan paling berharga. Klik nilainya → DevTools membuka stack trace di panel Sources. Dari situ Anda tahu: endpoint ini dipanggil oleh `admin-panel.9f8e.js`, padahal chunk itu tidak tertaut di UI. Itu temuan.

Waterfall: TTFB besar dengan transfer kecil berarti masalah server/DB, bukan jaringan — bukan temuan keamanan, jangan dimasukkan laporan. Transfer besar dengan TTFB kecil adalah kandidat data terbuka (misalnya endpoint tanpa auth mengembalikan 4 MB JSON).

## 3. Resep Filter

Kotak filter Network menerima sintaks khusus. Hafalkan enam ini:

| Filter | Fungsi |
|---|---|
| `-domain:sentry.io` | Buang derau (tanda minus = negasi) |
| `status-code:401` | Semua yang ditolak — kandidat endpoint terproteksi |
| `method:POST` | Mutasi; perhatikan parameter dan CSRF |
| `mime-type:application/json` | API sungguhan, menyaring aset |
| `larger-than:100k` | Response besar — data terbuka atau dump |
| `has-response-header:access-control-allow-origin` | Kebijakan CORS |

Kombinasi berguna: `method:POST mime-type:application/json -status-code:200` → semua POST yang gagal, biasanya berisi pesan error yang membocorkan validasi server.

## 4. Matriks Endpoint

Catat setiap endpoint yang relevan dalam satu tabel. Ini deliverable utama recon, dan menjadi input langsung untuk `web-app-scan`.

| Method | Path | Auth | Status | Content-Type | Catatan |
|---|---|---|---|---|---|
| GET | `/api/v1/me` | Bearer | 200 | json | Objek user lengkap, termasuk `role`, `tenantId` |
| GET | `/api/v1/users/1042` | Bearer | 200 | json | ID numerik berurutan → kandidat IDOR |
| POST | `/api/v1/admin/impersonate` | Cookie | 403 | json | Ada, tetapi ditolak untuk peran ini |
| GET | `/api/v1/export?fmt=csv` | none | 200 | csv | **Tanpa auth** — perlu verifikasi |
| POST | `/graphql` | Bearer | 200 | json | `operationName` bervariasi per halaman |

Kolom **Auth** diisi dari ada/tidaknya `Authorization`/cookie pada request, bukan dugaan. Kolom **Catatan** hanya untuk pengamatan yang bisa dibuktikan dari HAR.

## 5. Semantik Status Code

Jangan samakan "ditolak" dengan "tidak ada". Perbedaannya menentukan prioritas:

| Status | Arti | Tindakan |
|---|---|---|
| 200 | Berhasil | Baca body; cek apakah data sensitif |
| 201/204 | Dibuat / tanpa isi | Mutasi berhasil — catat, jangan ulangi |
| 301/302 ke `/login` | Sesi tidak valid | Ulangi dengan sesi sah sebelum menyimpulkan |
| 401 | Belum terautentikasi | Endpoint ada → kandidat setelah login |
| 403 | Terautentikasi, tidak berwenang | **Paling berharga**: ada kontrol akses → uji authz |
| 404 | Tidak ada (atau disembunyikan) | Jangan fuzz berulang; framework kadang menyamarkan 403 sebagai 404 |
| 405 | Method salah | Coba method lain sekali |
| 429 | Rate limit | Berhenti; catat header `Retry-After` |
| 500 | Error server | Catat body error — sering membocorkan stack trace |

Kalau seluruh endpoint mengembalikan 200 dengan HTML yang sama, kemungkinan besar SPA fallback: cek `Content-Type`.

## 6. GraphQL

GraphQL menyatukan banyak operasi ke satu path, jadi matriks per-path tidak cukup. Yang dicatat:

- **Endpoint**: `/graphql`, `/api/graphql`, `/v1/graphql`.
- **Operation name**: ada di body POST `{"operationName":"GetUserProfile",...}`. Daftar operation = daftar fungsi backend.
- **Auth**: header atau cookie; cek apakah introspection dibatasi saat tidak login.
- **Batching**: body berbentuk array `[{...},{...}]` — bisa dipakai untuk melewati rate limit per request.
- **Persisted queries**: bila hanya `{"id":"abc"}` yang dikirim, definisi query disimpan server; sulit dianalisis dari klien.

Uji introspection secara non-destruktif (satu request):

```bash
curl -s -X POST https://target.tld/graphql \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"query":"{__schema{queryType{name} types{name kind}}}"}' | head -c 800
```

Bila dibalas `errors` berisi "introspection disabled", itu bukan kegagalan — itu konfirmasi ada kebijakan. Catat sebagai pengamatan positif.

## 7. WebSocket dan Server-Sent Events

- Filter tipe **WS** di toolbar Network untuk WebSocket.
- Klik koneksi → tab **Messages** → lihat frame `↑` (klien→server) dan `↓`.
- Perhatikan: apakah token dikirim di query string URL (bocor ke log proxy), apakah setiap frame membawa otorisasi, dan nama channel/room.
- `EventSource` muncul sebagai `eventsource`; isinya teks berbaris `data:` — sering feed notifikasi yang memuat data lintas tenant.

## 8. Sesi dan Token

Yang perlu dipastikan sebelum menyimpulkan apa pun soal token:

1. **Di mana token disimpan** — `Set-Cookie` (dengan `HttpOnly`, `Secure`, `SameSite`) versus body JSON yang disimpan JS. Yang kedua berarti XSS = pencurian sesi.
2. **Bagaimana token dikirim** — header `Authorization` pada XHR (terlihat di HAR) atau cookie otomatis.
3. **Bagaimana token diperbarui** — cari request `/auth/refresh`; catat apakah refresh token ikut di body response.
4. **Masa berlaku** — `exp` pada JWT (decode base64 bagian tengah, tanpa verifikasi tanda tangan).

Cookie tanpa `HttpOnly` adalah temuan yang bisa dibuktikan langsung dari header, bukan spekulasi.

## 9. Ekspor HAR dan Analisis Offline

Klik kanan di daftar request → **Save all as HAR with content**. HAR adalah JSON biasa; `jq` membuatnya mudah ditanyai:

```bash
# Semua request: method, status, URL
jq -r '.log.entries[] | "\(.request.method) \(.response.status) \(.request.url)"' capture.har

# Endpoint unik tanpa query string
jq -r '[.log.entries[] | .request.url | split("?")[0]] | unique | .[]' capture.har

# Request yang membawa Authorization
jq -r '.log.entries[] | select(.request.headers[]? | .name | ascii_downcase == "authorization") | .request.url' capture.har

# Response yang menetapkan cookie
jq -r '.log.entries[] | select(.response.headers[]? | .name | ascii_downcase == "set-cookie") | "\(.request.url) -> \((.response.headers[] | select(.name | ascii_downcase == "set-cookie") | .value))"' capture.har

# Post body (GraphQL operation names)
jq -r '.log.entries[] | select(.request.method=="POST") | .request.postData.text // empty' capture.har | head -20
```

HAR **berisi cookie, token, dan data pribadi**. Jangan pernah commit ke repo, jangan kirim ke layanan pihak ketiga tanpa redaksi. Bila harus dilampirkan, ganti nilai header `Authorization`/`Cookie` menjadi `REDACTED`.

## 10. Replay dengan Batas Aman

Klik kanan request → **Copy** → **Copy as cURL**. Gunanya:

- Mengulang dengan token/peran berbeda untuk membandingkan 200 vs 403 (uji authz dasar).
- Mengubah satu parameter untuk memastikan parameter itu benar-benar dipakai.
- Menguji apakah endpoint menerima method lain.

Batas:

- Maksimal **satu** replay per perubahan variabel. Ini recon, bukan fuzzing.
- Jangan replay request yang bersifat destruktif (DELETE, POST pembayaran, POST kirim email). Bila tidak yakin, jangan.
- Jangan menguji di luar akun/peran yang diberikan.
- Bila hasilnya 429 atau error beruntun, berhenti dan catat.

## 11. Serah Terima ke Pengujian Aktif

Recon selesai ketika matriks endpoint cukup untuk memulai pengujian. Serahkan:

| ke `web-app-scan` | ke `web-pentest-payloads` |
|---|---|
| Daftar endpoint + method + status | Endpoint dengan parameter yang dapat diinjeksi |
| Endpoint 401/403 (kandidat authz) | Parameter yang memengaruhi query/filter |
| Format body (JSON/GraphQL/form) | Titik serialisasi (JSON, XML, multipart) |
| Header CORS dan CSP | Header yang diteruskan ke backend |

Jangan menyerahkan seluruh HAR mentah — ringkas, redaksi, dan sertakan bukti.

## 12. Kebersihan Data

- Simpan artefak di direktori kerja di luar repo (`work/`), bukan di `skills/`.
- Redaksi header sensitif sebelum menyimpan maupun melampirkan.
- Hapus `capture.har` dan dump sumber setelah pekerjaan selesai bila berisi data klien.

## Referensi Cepat

- Filter: `-domain:`, `status-code:`, `method:`, `mime-type:`, `larger-than:`, `has-response-header:`
- Kolom kunci: **Initiator** (pemetaan endpoint→chunk)
- HAR: Save all as HAR with content → `jq`
- Status: 401 = belum auth, 403 = authz, 404 = tidak ada
- WebSocket: filter **WS** → tab Messages
