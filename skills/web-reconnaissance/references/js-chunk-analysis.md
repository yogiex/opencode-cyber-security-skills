---
name: "Analisis Chunk JavaScript"
description: "Cara membaca isi chunk JS yang sudah diminifikasi: beautify, pulihkan source map, ekstrak endpoint/route/GraphQL/WebSocket, triage kunci rahasia (publik vs asli), baca state framework, dan hindari false positive."
tags: [javascript, analysis, beautify, source-map, secret, endpoint, graphql, feature-flag, false-positive]
---

# Analisis Chunk JavaScript

Tujuan analisis bukan "membaca semua kode" — kode produksi bisa puluhan ribu baris hasil minifikasi. Tujuannya **menjawab pertanyaan spesifik**: endpoint apa yang ada, rute apa yang disembunyikan, data apa yang disimpan, dan apakah ada kredensial yang benar-benar sensitif.

Kerjakan berurutan. Setiap langkah mempersempit langkah berikutnya.

> Berkas ini menjawab *apa isinya*. Untuk menghubungkan isi itu menjadi **alur** — aksi UI mana memanggil endpoint mana, lewat state apa — lanjutkan ke [data-flow-analysis.md](data-flow-analysis.md). Untuk menyusun rute dan endpoint menjadi peta arsitektur, lihat [architecture-mapping.md](architecture-mapping.md).

## 1. Siapkan Salinan Lokal

Analisis di DevTools itu menyakitkan: panel tertutup, pencarian lambat, dan tidak bisa memakai grep, diff, atau `jq`.

```bash
mkdir -p work && cd work
curl -sO https://target.tld/assets/index-abc.js
npx js-beautify -f index-abc.js -o index.pretty.js
wc -l index.pretty.js
```

`js-beautify` hanya memperbaiki indentasi dan baris baru — nama variabel tetap `a`, `b`, `t`. Itu cukup untuk membaca string literal, yang justru sumber hampir semua temuan. Membalik nama variabel jarang sepadan waktunya, kecuali source map tersedia.

Bila ada beberapa chunk, beautify semuanya sekaligus:

```bash
for f in *.js; do npx js-beautify -f "$f" -o "${f%.js}.pretty.js"; done
```

## 2. Pulihkan Source Map

Bila `.map` tersedia (lihat [js-chunk-discovery.md](js-chunk-discovery.md) bagian 6), ini jalur tercepat ke kode asli dengan nama variabel dan komentar utuh.

```javascript
// dump-sources.js — node dump-sources.js app.js.map out/
const fs = require('fs'), path = require('path');
const map = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = process.argv[3] || 'out';
map.sources.forEach((src, i) => {
  if (!map.sourcesContent?.[i]) return;
  const p = path.join(out, src.replace(/^(webpack|\.\.?)\//, '').replace(/[<>:"|?*]/g, '_'));
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, map.sourcesContent[i]);
});
console.log(`${map.sources.length} sumber, ${map.sourcesContent?.length || 0} dengan isi`);
```

```bash
node dump-sources.js index-abc.js.map src-dump
grep -rn "API_URL\|apiKey\|secret" src-dump | head -50
```

Bila `sourcesContent` kosong tetapi `mappings` ada, gunakan library `source-map` untuk memetakan posisi, atau cukup lewati: beautified bundle masih memberi semua string literal.

## 3. Ekstraksi: Target, Pola, Arti

Jalankan pola berikut pada versi `.pretty.js`. Semua pencarian **case-insensitive** kecuali disebut lain.

| Target | Pola grep | Arti bila ketemu |
|---|---|---|
| API base URL | `/api/v[0-9]`, `baseURL\s*:`, `VITE_API`, `REACT_APP_` | Titik masuk seluruh permukaan API |
| Rute tersembunyi | `path\s*:\s*["']/`, `path:"/admin` | Rute yang tidak tertaut di UI |
| Lazy import | `import\(["']\./`, `webpackChunkName` | Nama fitur yang dipisah — petunjuk modul besar |
| GraphQL | `/graphql`, `operationName`, `query [A-Z]\w+` | Operasi bernama = daftar fungsi backend |
| WebSocket/SSE | `wss?://`, `new WebSocket`, `EventSource\(` | Kanal realtime; sering tanpa authz per-topik |
| Header auth | `Authorization`, `Bearer `, `x-api-key`, `X-CSRF` | Cara token dikirim → dampak bila XSS |
| Refresh token | `refresh_token`, `/auth/refresh`, `/token` | Alur sesi; titik lemah rotasi |
| Kunci storage | `localStorage\.setItem\(\s*["']`, `sessionStorage\.` | Data apa yang bertahan di klien |
| Feature flag | `isEnabled\(`, `ldclient`, `unleash`, `feature_`, `__FLAGS__` | Fitur tersembunyi di balik flag |
| Peran/izin | `isAdmin`, `role\s*===`, `permissions`, `hasAccess` | Model otorisasi klien — sering hanya kosmetik |
| Host internal | `\.internal`, `\.corp`, `\.local`, `10\.\d+\.\d+\.\d+` | Permukaan yang tidak diekspos publik |
| Bucket/CDN | `s3\.amazonaws\.com`, `storage\.googleapis\.com`, `blob\.core\.windows\.net` | Storage object — cek ACL |
| Debug/actuator | `/debug`, `/actuator`, `/__webpack_hmr`, `/graphiql` | Build dev atau endpoint manajemen |
| Komentar/tiket | `TODO`, `FIXME`, `HACK`, `JIRA-`, `XXX` | Konteks internal, kadang kredensial uji |
| Email/host pegawai | `@target\.tld`, `/home/`, `/Users/` | Kebocoran path build & nama internal |

Contoh penerapan:

```bash
grep -oiE '"(https?://[^"]+|/api/v[0-9][^"]*)"' index.pretty.js | sort -u > endpoints.txt
grep -oiE 'path\s*:\s*"[^"]+"' index.pretty.js | sort -u > routes.txt
grep -oiE 'wss?://[^"'\'' ]+' index.pretty.js | sort -u > ws.txt
wc -l endpoints.txt routes.txt
```

Yang dicari bukan jumlah baris, tapi **yang mengejutkan**: `/api/v2/internal/`, `wss://`, `path:"/super-admin"`.

## 4. Triage Kunci: Publik vs Asli

Ini bagian yang paling sering salah. Banyak kunci di frontend **memang dirancang publik**. Melaporkannya sebagai temuan merusak kredibilitas laporan dan membuang waktu klien.

### Publik menurut desain — catat sebagai konteks, bukan temuan

| Pola | Layanan | Alasan |
|---|---|---|
| `pk_live_…` / `pk_test_…` | Stripe publishable key | Memang untuk browser |
| `AIza…` (35 karakter) | Google API / Firebase | Dibatasi HTTP referrer; risikonya di konfigurasi, bukan kuncinya |
| `https://<x>.ingest.sentry.io/…` | Sentry DSN | Menulis event, tidak membaca |
| `client_id` Auth0/Okta/OAuth | OIDC client id | Publik menurut spesifikasi |
| `6L…` (40 karakter) | reCAPTCHA site key | Publik |
| Algolia *search-only* key | Pencarian | Aman **hanya bila** ACL dibatasi ke indeks itu |
| `https://…/jwks.json`, `/.well-known/` | Kunci publik | Publik menurut desain |

### Asli — verifikasi lalu laporkan

| Pola | Layanan |
|---|---|
| `AKIA[0-9A-Z]{16}`, `ASIA[0-9A-Z]{16}` + secret 40 karakter | AWS |
| `sk_live_[0-9a-zA-Z]{24,}`, `rk_live_` | Stripe secret / restricted |
| `ghp_`, `github_pat_`, `gho_`, `ghs_` | GitHub |
| `xox[baprs]-` | Slack |
| `sk-[A-Za-z0-9]{32,}`, `sk-proj-` | OpenAI dan sejenisnya |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | Kunci privat |
| `postgres://user:pass@`, `mysql://`, `mongodb\+srv://` | Connection string berisi sandi |
| `AC[0-9a-f]{32}` + `auth_token` 32 hex | Twilio |
| `SG\.[\w-]{22}\.[\w-]{43}` | SendGrid |
| JWT dengan `role:admin` yang masih berlaku | Token tertanam |

### Protokol verifikasi (jangan langsung lapor)

1. **Cocokkan format** — panjang dan prefiks harus tepat. String acak 40 karakter bukan kunci AWS.
2. **Cari di traffic** — bila kunci yang sama dipakai pada request yang berhasil dari browser tanpa login, ia publik. DevTools Network adalah bukti terkuat.
3. **Uji non-destruktif, satu panggilan baca** — hanya bila diizinkan ROE. Contoh aman: `GET` metadata, bukan `ListBuckets` penuh.
4. **Hormati batas scope** — jangan menguji kunci pada akun/layanan di luar target hanya untuk memastikan.
5. **Bila ragu, tulis `[PERLU VERIFIKASI]`** dengan bukti yang ada, jangan menyimpulkan "kebocoran kredensial".

Jangan tempelkan kunci utuh di laporan. Tulis 6 karakter pertama + `…` + panjang.

## 5. State Framework: Sering Lebih Kaya dari Kode

JSON yang disuntikkan server biasanya berisi data nyata, bukan kode minif:

| Lokasi | Isi yang dicari |
|---|---|
| `__NEXT_DATA__` | `buildId`, `page`, `query`, `props` (kadang respons API lengkap) |
| `self.__next_f.push([1,"…"])` | Flight/RSC payload — segmen rute, data server, id internal |
| `window.__NUXT__` | `state`, `runtimeConfig` (API base, `public` keys), middleware |
| `window.__APOLLO_STATE__` | Cache GraphQL — daftar tipe, id objek (`User:123`) |
| `window.__INITIAL_STATE__` / `__PRELOADED_STATE__` | Redux store awal — user, tenant, flag |
| `window.__ENV__` / `__CONFIG__` | Konfigurasi runtime hasil injeksi container |

Perintah cepat:

```bash
curl -s https://target.tld/ | grep -oE '__NEXT_DATA__[^<]*' | head -c 2000
curl -s https://target.tld/ | python -c "import sys,re,json,html; m=re.search(r'__NUXT__=(.*?);?</script>', sys.stdin.read(), re.S); print(html.unescape(m.group(1))[:1500] if m else 'tidak ada')"
```

Data di sini biasanya memuat: objek `user` dengan `id`/`role`/`email`, `tenantId`, daftar `permissions`, dan `featureFlags`. Itu bahan untuk memahami model otorisasi **dan** kandidat IDOR saat pengujian aktif.

## 6. Menavigasi Bundle Webpack

Pada build produksi nama modul hilang, tetapi batas modul masih terlihat:

```javascript
/*!************************!*\
  !*** ./src/api/user.ts ***!
  \************************/
```

Bila komentar itu ada (build tanpa `optimization.minimizer` agresif, atau build dev), Anda mendapat peta struktur proyek. Manfaatkan:

```bash
grep -oE '!+\*\*\* \./[^ ]+' index.pretty.js | sort -u | head -50
```

Untuk melompat antar modul, cari `__webpack_require__(<id>)` dan perhatikan id yang sering dipanggil — modul dengan referensi terbanyak biasanya lapisan HTTP client.

## 7. False Positive yang Harus Diabaikan

| Gejala | Sebab | Tindakan |
|---|---|---|
| Regex secret cocok pada string acak | Base64/hash di bundle | Cek prefiks & konteks; buang bila tanpa makna |
| "Endpoint" seperti `/static/media/logo.svg` | Aset, bukan API | Saring ekstensi aset |
| `http://localhost:3000` di banyak tempat | Default dev, tidak dipakai produksi | Catat sebagai sisa build, bukan temuan |
| Kunci Stripe `pk_` dilaporkan bocor | Publik menurut desain | Turunkan ke konteks |
| Seluruh vendor chunk dianalisis | Kode framework, bukan aplikasi | Lewati `react`, `lodash`, `moment`, `core-js` |
| `sourceMappingURL=data:application/json;base64` | Map tertanam inline | Decode sekali, jangan analisis sebagai kode |

## 8. Time Box

Analisis JS bisa menyerap berhari-hari bila tanpa batas. Aturan praktis:

- Chunk entry + runtime: **30 menit**. Ini memberi endpoint dan route utama.
- Chunk dengan nama sensitif (`admin`, `internal`, `billing`): **20 menit masing-masing**.
- Vendor chunk: **0 menit**.
- Bila satu chunk sudah 20 menit tanpa temuan baru, pindah. Tulis di laporan bahwa chunk itu sudah diperiksa.

Ambang berhenti lengkap ada di `## Decision Frame` pada SKILL.md.

## 9. Format Temuan

| Temuan | Bukti | Nilai | Status |
|---|---|---|---|
| Rute `/internal/reports` tidak tertaut UI | `path:"/internal/reports"` di `main.a1b2.js` | Perluas permukaan uji | Terverifikasi di bundle |
| Endpoint `/api/v2/admin/users` | String + `fetch()` pemanggil | Kandidat authz | Terverifikasi di bundle |
| `AIza…` Firebase config | `__NEXT_DATA__.props.firebase` | Konteks (publik) | Bukan temuan |
| `AKIA…` + secret | `src-dump/config.js` | Kritis | `[PERLU VERIFIKASI]` |

Kolom **Bukti** harus berisi nama berkas dan string persis, supaya orang lain bisa mengulang. Tanpa itu, temuan tidak dapat diaudit.

## Referensi Cepat

- Beautify: `npx js-beautify -f a.js -o a.pretty.js`
- Rekonstruksi sumber: `sourcesContent` dari `.map`
- Grep endpoint: `grep -oiE '"(https?://[^"]+|/api/v[0-9][^"]*)"'`
- State framework: `__NEXT_DATA__`, `__NUXT__`, `__APOLLO_STATE__`
