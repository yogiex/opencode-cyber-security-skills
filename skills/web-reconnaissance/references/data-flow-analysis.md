---
name: "Alur Data Aplikasi: Source ke Sink"
description: "Merekonstruksi alur data frontend dari bundle: menemukan lapisan API client dan interceptor, menghubungkan aksi UI ke endpoint, memetakan state store, dan mengonfirmasi alur dengan logpoint atau instrumentasi fetch/XHR."
tags: [data-flow, call-graph, source-sink, api-client, interceptor, state-management, webpack-module, logpoint, taint]
---

# Alur Data Aplikasi

Daftar endpoint menjawab "apa saja yang ada". Alur data menjawab pertanyaan yang lebih berguna: **data apa yang masuk dari mana, diubah oleh siapa, dan keluar ke endpoint mana**. Tanpa itu, temuan recon hanya daftar URL tanpa konteks — dan konteks itulah yang menentukan endpoint mana yang layak diuji lebih dulu.

Tiga tingkat kedalaman, dari termurah:

| Tingkat | Cara | Yang didapat | Biaya |
|---|---|---|---|
| **Statis** | baca bundle: nama string endpoint, modul, pemanggil | peta modul → endpoint | menengah; nama fungsi diminifikasi |
| **Semi-statis** | source map bila ada: baca kode asli | alur lengkap dengan nama asli | murah bila `.map` tersedia |
| **Dinamis** | logpoint, patch `fetch`/`XHR`, breakpoint | urutan sebenarnya saat runtime | paling akurat, paling mahal |

Kerjakan berurutan. Statis mempersempit jumlah titik yang perlu dipasangi logpoint; dinamis membuktikan bahwa dugaan statis benar.

## 1. Temukan Lapisan API Client

Hampir semua aplikasi punya satu modul yang membungkus semua request. Di sanalah base URL, header auth, dan penanganan error berkumpul — sehingga satu modul itu menjelaskan seluruh permukaan API.

```bash
# instance dan base URL
grep -nE 'baseURL|axios\.create|fetchBaseQuery|createClient\(' main.pretty.js
# interceptor (tempat token disisipkan)
grep -nE "interceptors\.(request|response)" main.pretty.js
# sink request tingkat rendah
grep -nE 'fetch\(|XMLHttpRequest|\.open\(|sendBeacon' main.pretty.js
# GraphQL
grep -nE '__schema|operationName|/graphql|ApolloClient|urql' main.pretty.js
# SSR/edge fetch
grep -nE '\$fetch|useFetch|getServerSideProps|loader:\s*async' main.pretty.js
```

Nama fungsi hilang saat minifikasi, tetapi **string tetap utuh**. Karena itu anchor pencarian selalu string: path endpoint, nama header, nama library, pesan error.

Dari modul API client, catat:

| Yang dicatat | Contoh | Nilai |
|---|---|---|
| Base URL | `baseURL:"https://api.target.tld/v2"` | host backend sebenarnya, sering berbeda dari host frontend |
| Header tetap | `headers:{"X-Client":"web"}` | penanda yang bisa dipakai membedakan trafik sah |
| Penyisipan token | `config.headers.Authorization="Bearer "+t` | asal token + bentuk skema auth |
| Interceptor respons | `401 → refreshToken()` | memetakan alur refresh (lihat `auth-configuration.md`) |
| Retry/timeout | `timeout:15000`, `retry:2` | perilaku saat diuji |
| Transformasi | `transformResponse`, `decrypt(` | data tidak selalu dikirim apa adanya |

## 2. Bangun Graf Modul, Bukan Graf Fungsi

Webpack mempertahankan batas modul walaupun nama fungsi diacak: modul bernomor `1234` memanggil modul lain lewat `n(5678)`. Itu cukup untuk membangun graf.

```bash
# tabel modul: objek besar berisi "id: (e,t,n)=>{"
grep -oE '[0-9]{2,5}:\(e,t,n\)=>' main.pretty.js | head -50
# edge antar modul
grep -oE 'n\([0-9]{2,5}\)' main.pretty.js | sort -u | head -50
```

Strategi praktis yang lebih cepat daripada membaca seluruh graf:

1. Cari string endpoint (`/api/v2/reports`).
2. Lihat modul mana yang memuatnya — modul itu adalah API client untuk domain tersebut.
3. Cari **pemanggil** modul itu: siapa yang mengimpor id tersebut.
4. Naik satu lapis lagi sampai menemukan nama yang dikenali (`exportReport`, `handleExport`).

Dalam kode bermakna, polanya biasanya: komponen → hook/service → API client → transport. Tiga hop sudah cukup untuk menjawab "aksi UI mana yang memicu endpoint ini".

## 3. Kenali Pola per Framework

| Framework | Pola yang dicari | Arti |
|---|---|---|
| React Query / TanStack | `useQuery({queryKey:["reports"],queryFn:...})` | `queryKey` memberi nama fitur; `queryFn` memanggil API client |
| Redux Toolkit | `createAsyncThunk("reports/fetch",...)` | string pertama adalah nama slice+aksi |
| Zustand | `create((set)=>({loadReports:async()=>...}))` | aksi dan state dalam satu objek |
| Pinia (Vue) | `defineStore("reports",{actions:{fetch(){...}}})` | nama store = nama domain |
| Vue/Nuxt | `onMounted(async()=>{...})`, `$fetch("/api/...")` | titik muat data per komponen |
| Angular | `HttpClient.get<T>("/api/...")`, `providedIn:"root"` | service per domain, sering terlihat di bundle |
| SvelteKit | `export async function load({fetch})` | data dimuat sebelum render |

Nama-nama ini biasanya bertahan di bundle karena muncul sebagai argumen string, bukan identifier.

## 4. Petakan State: Tempat Data Berhenti

Setiap respons API berakhir di suatu tempat. Menemukan tempat itu menjelaskan apa yang dianggap sensitif oleh aplikasi — dan sering mengungkap data yang tidak pernah dirender ke layar.

```bash
grep -nE 'createStore|configureStore|createSlice|defineStore|create\(\(set' main.pretty.js
grep -nE 'localStorage\.setItem|sessionStorage\.setItem|indexedDB' main.pretty.js
```

| Sumber | State tujuan | Persistensi |
|---|---|---|
| `GET /api/me` | store `user` | sering ke `localStorage` |
| `GET /api/reports` | store `reports` + cache query | cache memori, kadang IndexedDB |
| Respons login | store `session` | token ke storage, profil di memori |

Bila sebuah respons masuk ke store lalu dipersist, `browser-storage.md` memberi tahu cara membacanya; nama kunci yang Anda temukan di bundle adalah kunci yang harus dicari di sana.

## 5. Konfirmasi Dinamis

Statis menghasilkan hipotesis; ini yang membuktikannya.

### A. Logpoint pada API client (paling akurat)

Bila ada source map, `set_logpoints` menunjuk berkas asli:

```text
set_logpoints(pageId = <id>, logpoints = [
  "src/api/client.ts:31 'req:', config.method, config.url, config.data"
])
```

Lalu jalankan aksinya di UI dan baca `list_console_messages`. Anda melihat argumen sebenarnya, termasuk header yang disisipkan interceptor.

### B. Instrumentasi `fetch` dan `XHR`

Tanpa source map, bajak transport dan baca jejaknya. Ini hanya membaca, tidak mengubah request.

```javascript
() => {
  if (window.__reconNet) return 'sudah terpasang';
  window.__reconNet = [];
  const rec = (kind, url, method, extra) =>
    window.__reconNet.push({ kind, url: String(url).slice(0, 300), method: method || 'GET', extra });

  const of = window.fetch;
  window.fetch = function (input, init) {
    const url = typeof input === 'string' ? input : (input && input.url);
    rec('fetch', url, init && init.method, new Error().stack);
    return of.apply(this, arguments);
  };

  const oo = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) {
    rec('xhr', u, m, this);
    return oo.apply(this, arguments);
  };
  return 'terpasang';
}
```

Alur: pasang → jalankan aksi UI → baca `window.__reconNet` → lepas dengan memuat ulang halaman.

Catatan: `Error().stack` pada halaman yang diminifikasi memberi nama chunk + nomor baris, bukan nama fungsi. Itu tetap berguna — chunk dan baris itulah yang Anda buka di `js-chunk-analysis.md`. Bila source map tersedia, logpoint (cara A) lebih baik karena sudah dipetakan.

### C. XHR/fetch breakpoint manual

DevTools → Sources → **XHR/fetch Breakpoints** → tambahkan substring URL. Eksekusi berhenti tepat di pemanggil, dengan call stack lengkap dan scope variable. Ini cara tercepat menjawab "kode mana yang mengirim request ini" tanpa membaca bundle.

## 6. Tabel Alur

Keluaran yang bisa diaudit:

| Aksi UI | Handler | Fungsi API | Endpoint | State | Render |
|---|---|---|---|---|---|
| Klik "Ekspor" | `settings.b7f2.js` | `exportReport()` | `POST /api/v2/reports/export` | `jobs[]` | toast + polling status |
| Buka halaman awal | `dashboard.4c1a.js` | `getSummary()` | `GET /api/v2/summary` | `summary` | kartu angka |
| Muat login | `auth.9d0e.js` | `login()` | `POST /auth/token` | `session` | redirect |

Kolom "Handler" diisi nama chunk (atau berkas asli bila ada source map), bukan nama fungsi hasil tebakan.

## 7. Jalur Menuju Sink Berbahaya

Recon bukan pengujian, tetapi alur yang berakhir di sink berbahaya layak dicatat sebagai **calon**, bukan temuan.

| Source | Sink | Yang perlu dibuktikan nanti |
|---|---|---|
| `location.search`, `location.hash` | `innerHTML`, `dangerouslySetInnerHTML` | refleksi tanpa encoding |
| respons API | `innerHTML`, `document.write` | data dari server dipakai sebagai HTML |
| `postMessage` | `eval`, `new Function` | asal pesan diperiksa atau tidak |
| nama berkas unggahan | `setAttribute("href", ...)` | skema `javascript:` disaring atau tidak |
| `localStorage` | header request | token dapat ditulis ulang dari JS |

Catat source → sink beserta chunk-nya. Verifikasi masuk `web-app-scan`, bukan di sini.

## 8. Berhenti di Mana

Alur data tidak punya ujung alami. Batasnya:

- **Tiga hop** dari aksi UI ke endpoint. Bila belum tersambung, tandai "tidak terlacak" dan lanjut.
- **Berhenti setelah satu alur per domain** (auth, data utama, admin) dikonfirmasi dinamis. Sisanya boleh statis.
- **Berhenti menambah endpoint** bila satu putaran crawl tidak menghasilkan path baru.
- **Jangan mengejar** endpoint yang hanya muncul di kode mati (tidak ada pemanggil dan tidak ada di peta rute) — catat sebagai temuan inventaris, bukan alur.

## Jebakan

- **Nama fungsi hasil minifikasi tidak berarti apa-apa.** `c()` bisa jadi apa saja; hanya string dan graf modul yang dapat dipercaya.
- **Satu string endpoint bisa muncul di beberapa chunk.** Yang menentukan adalah pemanggilnya, bukan lokasi string.
- **Base URL sering dirakit dari variabel lingkungan.** `"/"+p+"/api"` tidak akan ditemukan dengan grep `"/api"` — cari `baseURL`, `VITE_`, `NEXT_PUBLIC_`, `runtimeConfig`.
- **Interceptor dapat menulis ulang URL dan header.** Endpoint yang terlihat di bundle belum tentu yang dikirim; cocokkan dengan traffic.
- **Patch `fetch` tidak menangkap `sendBeacon`, WebSocket, atau `EventSource`.** Untuk itu pakai traffic, bukan instrumentasi.
- **Memuat ulang halaman menghapus patch.** Instrumentasi harus dipasang lagi setelah setiap navigasi.
- **`Error().stack` di halaman terminterifikasi menunjuk chunk, bukan sumber.** Jangan menuliskan nama fungsi yang tidak Anda lihat.
- **Kode mati tetap ada di bundle.** Fungsi tanpa pemanggil bisa jadi sisa fitur lama — catat, jangan jadikan dasar prioritas.

## Best Practices

1. Mulai dari modul API client; satu modul itu biasanya menjelaskan 80% permukaan.
2. Cocokkan setiap endpoint hasil statis dengan minimal satu request nyata sebelum masuk tabel.
3. Simpan tabel alur bersama peta API (`architecture-mapping.md`); dua dokumen itu saling melengkapi.
4. Konfirmasi dinamis hanya untuk alur yang akan diuji — bukan semua.
5. Tulis "tidak terlacak" secara eksplisit; ketiadaan bukti bukan bukti ketiadaan.
