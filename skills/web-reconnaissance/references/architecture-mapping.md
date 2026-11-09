---
name: "Peta Arsitektur: Rute Frontend dan API Backend"
description: "Menyusun dua inventaris yang bisa diaudit — seluruh rute frontend (React Router, Vue Router, Next.js, Nuxt, Angular, SvelteKit) dan seluruh endpoint REST backend (base URL, versi, GraphQL, gRPC-web, WebSocket) — lalu menggabungkannya menjadi satu peta arsitektur dengan pernyataan cakupan."
tags: [architecture, routing, react-router, vue-router, nextjs, nuxt, angular, sveltekit, rest-api, graphql, openapi, inventory]
---

# Peta Arsitektur

Recon yang matang menghasilkan dua inventaris dan satu penggabungan:

| Artefak | Isi | Menjawab |
|---|---|---|
| **Peta rute frontend** | path, komponen/chunk, guard peran, parameter | halaman apa yang ada, mana yang butuh login |
| **Peta API backend** | host, base path, versi, method, path, auth | permukaan serangan sebenarnya |
| **Gabungan** | rute → endpoint yang dipanggil | halaman mana menyentuh data apa |

Tanpa penggabungan, Anda punya dua daftar yang tidak bisa diprioritaskan. Dengan penggabungan, pertanyaan "halaman mana yang paling berisiko" punya jawaban yang bisa dipertahankan.

## 1. Peta Rute Frontend

Rute adalah string yang bertahan saat minifikasi. Cari konfigurasinya, bukan hasil tebakannya.

```bash
# React Router v6 / TanStack Router
grep -nE 'path:\s*"[^"]+"|createBrowserRouter|createRoute\(' main.pretty.js
# React Router v5 (JSX)
grep -nE '<Route[^>]+path=' main.pretty.js
# Vue Router / Nuxt
grep -nE 'routes:\s*\[|component:\s*\(\)\s*=>\s*import' main.pretty.js
# Angular
grep -nE 'RouterModule\.forRoot|loadChildren|path:\s*"[^"]+"' main.pretty.js
# lazy loading — penanda rute yang ada tapi belum dimuat
grep -nE 'import\(|lazy:|loadComponent' main.pretty.js
```

| Framework | Di mana rute terlihat | Catatan |
|---|---|---|
| **React Router v6** | objek `{path:"...", element:...}` | `createBrowserRouter` memuat semua rute di satu tempat |
| **React Router v5** | JSX `<Route path="/x">` | sering terpecah per komponen |
| **Next.js Pages** | `__NEXT_DATA__.page` + `_buildManifest.js` | `buildId` dari `__NEXT_DATA__`; manifest memetakan rute → chunk |
| **Next.js App Router** | payload `self.__next_f.push(...)` | segmen rute ada di payload RSC, bukan di HTML |
| **Nuxt** | `__NUXT__` (`routePath`, `router.base`) | rute dinamis terlihat dari nama chunk `_nuxt/` |
| **Angular** | `RouterModule.forRoot([...])`, `loadChildren` | rute lazy menyebut path modul |
| **SvelteKit** | `manifest` di `_app/immutable/` | rute per berkas; `data-sveltekit-preload` menandai tautan |
| **Vue Router** | `routes:[{path:"/x",component:()=>import(...)}]` | nama komponen muncul di nama chunk |

Rute yang tidak tertaut di UI tetap muncul di konfigurasi ini. Itulah nilainya: `/internal/reports` atau `/settings/billing` yang hanya dirender untuk peran tertentu tetap terdaftar, walaupun tidak ada di menu.

### Rute tersembunyi dan berpagar

| Jenis | Tanda | Cara memastikan |
|---|---|---|
| Berpagar peran | guard di sekitar rute (`role==="admin"`, `RequireAuth`) | cari kondisi di dekat definisi rute |
| Di balik flag | `isEnabled("feature_x")`, `flags.x` | cari nama flag di bundle yang sama |
| Mati | tidak ada pemanggil, tidak ada di peta rute | bandingkan dengan chunk yang benar-benar dimuat |
| Dinamis | `path:"/r/:slug"` | parameter menentukan data; catat polanya |

Jangan menguji rute berpagar dengan menebak URL di produksi. Cukup dicatat; pengujiannya masuk `web-app-scan` dengan izin.

## 2. Arsitektur URL

Sebelum menyusun tabel, petakan bentuk URL-nya:

- **Host terpisah** — `app.target.tld` (frontend), `api.target.tld` (REST), `auth.target.tld` (IdP), `ws.target.tld`, `cdn.target.tld`.
- **Prefiks base** — `/api/v1`, `/graphql`, `/rpc`, `/ws`, `/v2`.
- **Versi** — v1 dan v2 sering punya aturan auth berbeda; catat keduanya.
- **Locale** — `/en/`, `/id/` mendahului path sebenarnya; normalisasi sebelum menghitung.
- **Tenant** — `{tenant}.target.tld` atau `/t/{tenant}/...`; batas isolasi yang perlu dicatat, bukan diuji.
- **Hash route** — `#/users/42` tidak pernah sampai ke server, tetapi ada di bundle dan di histori browser.

## 3. Peta API Backend

Sumber endpoint, dari termurah:

| Sumber | Cara | Cakupan |
|---|---|---|
| Bundle | `grep -nE '"/api/[^"]+"'` + `baseURL` | semua yang direferensikan kode, termasuk yang belum dipanggil |
| Traffic | tab Network / `list_network_requests` | hanya yang benar-benar dipanggil pada sesi itu |
| Spesifikasi | probe `/openapi.json`, `/swagger.json`, `/v3/api-docs`, `/api-docs`, `/docs` | lengkap bila terbuka |
| GraphQL | `operationName` di bundle; introspeksi bila diizinkan | per operasi, bukan per path |
| gRPC-web | path berbentuk `/paket.Layanan/Metode`, `content-type: application/grpc-web+proto` | per metode |
| WebSocket | `wss://`, `new WebSocket`, `socket.io` | kanal + event |
| Sumber pihak ketiga | `googleapis.com`, `*.sentry.io`, `*.stripe.com` | konteks, bukan permukaan uji |

Probe spesifikasi sekali per host, catat status **dan** `Content-Type`. Status 200 dengan `text/html` adalah SPA fallback, bukan OpenAPI.

Introspeksi GraphQL adalah **POST** — perlakukan sebagai permintaan aktif; jalankan hanya bila izin mencakupnya. Bila ragu, cukup catat nama operasi dari bundle.

## 4. Normalisasi dan Deduplikasi

Endpoint mentah berisi id konkret. Normalisasi sebelum menghitung, atau daftar Anda akan berisi ratusan baris yang sama.

| Mentah | Normal |
|---|---|
| `/api/v2/users/1042` | `/api/v2/users/:id` |
| `/api/v2/users/1042/orders/77` | `/api/v2/users/:id/orders/:id` |
| `/api/v2/search?q=budi&page=2` | `/api/v2/search?q=:q&page=:n` |
| `/api/v1/files/a1b2c3.pdf` | `/api/v1/files/:name` |

Aturan:

1. Path parameter yang terlihat seperti id/angka/uuid/hash → `:id`.
2. Nama parameter query dipertahankan; nilainya diganti `:n` atau `:q`.
3. **Jangan** gabungkan `me`, `self`, `current` menjadi `:id` — semantiknya berbeda dan sering punya otorisasi berbeda.
4. Pertahankan prefiks versi dan tenant apa adanya.
5. Simpan satu contoh konkret di kolom terpisah sebagai bukti.

## 5. Tabel Inventaris API

| Host | Base | Method | Path | Auth | Sumber | Status |
|---|---|---|---|---|---|---|
| api.target.tld | /v2 | GET | /users/:id | Bearer | bundle `main.js`, HAR | 200 |
| api.target.tld | /v2 | POST | /reports/export | Bearer | bundle `reports.c4d1.js` | 202 |
| api.target.tld | /v1 | GET | /admin/audit | Cookie | traffic (sesi admin) | 403 |
| auth.target.tld | / | POST | /oauth/token | — | traffic | 200 |
| ws.target.tld | / | WS | /socket | Bearer (query) | bundle + traffic | 101 |

Kolom **Status** hanya diisi dari request yang benar-benar dijalankan. Kolom **Sumber** membedakan "ada di kode" dari "terbukti dipanggil".

## 6. Gabungan: Rute ke Endpoint

| Rute | Guard | Chunk | Endpoint | Catatan |
|---|---|---|---|---|
| `/` | publik | `dashboard.4c1a.js` | `GET /v2/summary` | — |
| `/settings` | login | `settings.b7f2.js` | `GET /v2/me`, `PATCH /v2/me` | — |
| `/admin/users` | peran admin | `admin.9e3d.js` | `GET /v2/admin/users`, `DELETE /v2/admin/users/:id` | DELETE butuh izin eksplisit untuk diuji |
| `/r/:slug` | publik | `public.1a2b.js` | `GET /v2/public/:slug` | parameter menentukan objek |

Yang dicari dari tabel ini:

- Rute publik yang memanggil endpoint terautentikasi — atau sebaliknya.
- Rute peran rendah yang memanggil endpoint admin (kandidat masalah otorisasi).
- Rute dengan parameter path yang langsung menjadi id objek — kandidat IDOR.
- Rute tanpa guard yang memuat chunk bernama sensitif.

## 7. Diagram Arsitektur

Satu diagram teks sudah cukup untuk laporan:

```
app.target.tld (SPA)
├── /                     publik    → GET /v2/summary
├── /settings             login     → GET/PATCH /v2/me
├── /admin/users          admin     → GET /v2/admin/users
└── /r/:slug              publik    → GET /v2/public/:slug
     │
     ├── api.target.tld/v2   REST, Bearer
     ├── auth.target.tld     OIDC (authorize + token)
     └── ws.target.tld       WebSocket, token di query
```

## 8. Pernyataan Cakupan

Inventaris tanpa pernyataan cakupan akan dibaca sebagai "lengkap". Tulis batasnya:

```text
Cakupan peta arsitektur
  Chunk dibaca      : 14 dari 21 yang terdaftar (7 vendor dilewati)
  Rute ditemukan    : 23; rute dikunjungi: 9
  Endpoint ditemukan: 61 (bundle 61, traffic 38, openapi tidak tersedia)
  Sesi              : anonim + user; admin TIDAK diuji
  Tidak tercakup    : area pembayaran, rute peran admin, GraphQL introspeksi (tidak diizinkan)
  Waktu             : 90 menit
```

Angka di dalamnya harus berasal dari hitungan berkas, bukan perkiraan.

## Jebakan

- **Rute klien bukan rute server.** `/admin` yang dibalas 200 oleh SPA tidak membuktikan apa pun tentang otorisasi server. Yang menentukan adalah endpoint yang dipanggil setelah render.
- **SPA membalas 200 untuk hampir semua path.** Probe path harus memeriksa `Content-Type` dan isi, bukan hanya status.
- **Hash route tidak terlihat di log server.** `#/users/42` hanya ada di klien; jangan menyimpulkan "tidak ada halaman user" dari akses log.
- **Endpoint di bundle bisa usang.** Kode mati tetap dikirim. Cocokkan dengan traffic sebelum memasukkan ke kolom prioritas.
- **`baseURL` relatif dirakit dari variabel build.** `"/"+p+"/api"` lolos dari grep; cari `VITE_`, `NEXT_PUBLIC_`, `runtimeConfig`, `import.meta.env`.
- **Normalisasi berlebihan menghapus perbedaan penting.** `me` bukan `:id`; `v1` bukan `v2`.
- **GraphQL bukan satu endpoint untuk inventaris.** Satu path `/graphql` dapat memuat puluhan operasi; inventariskan per `operationName`.
- **Rute dengan guard tetap harus dicatat.** "Butuh admin" adalah informasi, bukan alasan melewatkannya.
- **Jangan menebak path admin di produksi.** Catat dari bundle; uji hanya dengan izin.

## Best Practices

1. Susun peta rute lebih dulu — ia memberi tahu chunk mana yang layak dibaca.
2. Simpan tiga artefak terpisah: rute, API, gabungan. Jangan campur dalam satu tabel besar.
3. Selalu isi kolom Sumber; pembaca harus bisa membedakan kode dan traffic.
4. Normalisasi sebelum menghitung; hitungan yang benar adalah dasar pernyataan cakupan.
5. Serahkan peta ini ke `web-app-scan` bersama daftar prioritas, bukan seluruh daftar.
