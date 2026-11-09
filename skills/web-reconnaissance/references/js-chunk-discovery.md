---
name: "Penemuan Chunk JavaScript"
description: "Cara menemukan seluruh berkas JavaScript sebuah aplikasi web/SPA: tag script di HTML, manifest build (CRA, webpack, Vite, Next.js), tabel chunk di runtime webpack, panel Coverage DevTools, sampai crawl dan source map."
tags: [javascript, chunk, bundle, source-map, webpack, vite, nextjs, devtools, coverage, spa]
---

# Penemuan Chunk JavaScript

Build modern tidak mengirim satu `bundle.js`. Entry point hanya memuat sebagian kecil kode; sisanya dipecah menjadi *chunk* yang diunduh saat rute, komponen, atau fitur dibuka. Artinya: **membuka halaman depan lalu melihat tab Sources akan selalu memberi gambaran yang tidak lengkap.**

Urutan kerja yang benar:

1. Kumpulkan daftar chunk (file ini).
2. Baca traffic saat chunk itu dipakai ([network-analysis.md](network-analysis.md)).
3. Analisis isinya ([js-chunk-analysis.md](js-chunk-analysis.md)).

Jangan mulai dari analisis. Analisis satu chunk yang salah membuang waktu lebih banyak daripada 10 menit menginventarisasi.

## 1. Titik Masuk dari HTML

Ambil HTML mentah, bukan hasil render DevTools:

```bash
curl -s https://target.tld/ | tee index.html
grep -oE '<script[^>]*src="[^"]+"' index.html
grep -oE '<link[^>]+(modulepreload|preload)[^>]*>' index.html
```

Yang perlu dicatat:

| Pola di HTML | Arti |
|---|---|
| `<script type="module" src="/assets/index-<hash>.js">` | Entry Vite/Rollup |
| `<script src="/static/js/main.<hash>.chunk.js">` | Entry Create React App |
| `<script id="__NEXT_DATA__" type="application/json">` | Next.js — berisi `buildId`, `page`, `props`, `query` |
| `<script>self.__next_f.push(...)</script>` | Next.js App Router — payload RSC, sering memuat data server |
| `<script>window.__NUXT__=...</script>` | Nuxt — state + `runtimeConfig` (kerap membocorkan API base) |
| `<link rel="modulepreload">` | Chunk yang akan segera dimuat — kandidat pertama |
| `<script nomodule>` | Fallback legacy; kadang berisi polyfill + konfigurasi lama |

`__NEXT_DATA__` dan `__NUXT__` hampir selalu lebih berharga daripada kode yang diminifikasi: keduanya JSON biasa berisi data yang disuntikkan server.

## 2. Manifest Build — Cara Termurah Bila Ada

Banyak build tool menerbitkan manifest yang memetakan nama logis → nama file ber-hash. Kalau ada, satu request memberi daftar lengkap tanpa crawl.

```bash
for p in /asset-manifest.json /manifest.json /.vite/manifest.json \
         /_next/static/<buildId>/_buildManifest.js \
         /stats.json /webpack-stats.json; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "https://target.tld$p")
  echo "$code  $p"
done
```

| Build | Berkas yang dicoba | Catatan |
|---|---|---|
| Create React App | `/asset-manifest.json` | Memetakan `main.js`, `runtime-main.js`, dan `chunk.css`/`chunk.js` |
| Vite | `/.vite/manifest.json` atau `/manifest.json` | Hanya ada bila `build.manifest` diaktifkan |
| Next.js | `/_next/static/<buildId>/_buildManifest.js` (`buildId` dari `__NEXT_DATA__`) | Pages Router |
| Webpack umum | `/stats.json`, `/webpack-stats.json` | Jarang ter-deploy, tapi kalau ada isinya emas: daftar modul + alasan split |
| Nuxt 3 | `/_nuxt/builds/meta/<id>.json` | Cari string `builds/meta` di HTML dulu |

**Jangan berasumsi.** Catat status 200/404 untuk setiap probe. Manifest yang 200 tapi isinya HTML (`<!doctype`) berarti SPA fallback — bukan manifest.

## 3. Tabel Chunk di Runtime Webpack

Ini teknik yang paling sering terlewat. Webpack menanam fungsi pemetaan `chunkId → nama file` langsung di runtime, karena browser perlu tahu URL chunk yang belum diunduh.

Cari di entry chunk (biasanya `runtime.*.js` atau `main.*.js`):

```js
__webpack_require__.u = (chunkId) => "static/js/" + chunkId + "." + {
  123: "AdminPanel",
  456: "billing",
  789: "reports"
}[chunkId] + ".chunk.js";
```

Ekstrak objek peta itu secara manual atau dengan grep:

```bash
# temukan deklarasi fungsi nama chunk
grep -oE '__webpack_require__\.u\s*=\s*.{0,400}' main.js

# public path (prefiks URL chunk)
grep -oE '__webpack_require__\.p\s*=\s*"[^"]*"' main.js
```

Dari situ Anda memperoleh **seluruh nama chunk beserta id-nya tanpa membuka satu rute pun**. Nama chunk seperti `AdminPanel`, `billing`, `internal-tools` adalah temuan recon paling berharga: ia memberi tahu fitur apa saja yang ada, termasuk yang tidak tertaut di UI.

Varian lain:

- Vite/Rollup menyimpan daftar dependensi dinamis di `__vite__mapDeps([...])` — array berisi nama file ber-hash.
- Webpack 5 kadang memakai `chunkLoadingGlobal` (`webpackChunk<app>`) dan `.e(chunkId)` untuk memuat chunk.

## 4. Panel Coverage — Menemukan Chunk yang Belum Terunduh

Chrome DevTools:

1. `Ctrl+Shift+P` → ketik **Coverage** → Enter.
2. Klik ikon reload, biarkan halaman selesai.
3. Navigasi ke rute lain, buka menu, klik tombol yang memicu modal.
4. Setiap file baru yang muncul di daftar Coverage = chunk lazy yang baru diunduh.

Kolom *Unused Bytes* menunjukkan berapa banyak kode yang belum dieksekusi. File dengan 100% unused pada satu rute hampir selalu berarti chunk itu milik fitur lain — berharga untuk dipetakan.

Alternatif tanpa membuka panel, dari Console:

```js
performance.getEntriesByType('resource')
  .filter(e => /\.js(\?|$)/.test(e.name))
  .map(e => `${e.name} (${Math.round(e.transferSize/1024)} KB)`)
  .join('\n')
```

`transferSize` = 0 berarti diambil dari cache; tetap catat sebagai pernah dimuat.

## 5. Pencarian Global DevTools

`Ctrl+Shift+F` di panel Sources mencari string di **semua** berkas yang sudah dimuat. Ini cara tercepat menjawab pertanyaan seperti:

- `/admin` ada di chunk mana?
- Siapa yang memanggil `graphql`?
- Di mana `api_key` didefinisikan?

`Ctrl+P` menyaring nama berkas dengan cepat (`?` untuk fuzzy). Gunakan pola `.chunk.js`, `runtime`, `vendor`, `polyfills`.

Vendor chunk (React, lodash, moment) jarang berisi temuan pertama-pihak. Catat lalu lewati; fokus pada chunk dengan nama domain bisnis.

## 6. Source Map

Source map memulihkan kode asli dan nama variabel. Nilainya jauh melebihi beautifikasi manual.

Cara menemukan:

```bash
# 1. komentar di akhir berkas
tail -c 200 main.js | grep -o 'sourceMappingURL=[^ ]*'

# 2. header respons
curl -sI https://target.tld/assets/index-abc.js | grep -iE 'sourceMap|x-sourcemap'

# 3. probe langsung
curl -s -o map.json -w '%{http_code}\n' https://target.tld/assets/index-abc.js.map
head -c 200 map.json
```

Berkas `.map` yang valid diawali `{"version":3`. Periksa tiga hal:

| Kondisi | Arti |
|---|---|
| `"sourcesContent": [...]` terisi | Kode sumber asli lengkap — tidak perlu deobfuscation |
| `"sources": [...]` tapi tanpa `sourcesContent` | Masih butuh `mappings` + berkas asli; pulihkan dengan library `source-map` |
| 200 tapi `{"version":3}` tanpa `sources` | Map kosong — abaikan |

DevTools memuat map otomatis bila tersedia; berkas asli muncul di bawah `.` di panel Sources. Untuk membaca di luar browser, lihat [js-chunk-analysis.md](js-chunk-analysis.md).

## 7. Crawl Saat Jumlah Halaman Banyak

Untuk target dengan banyak rute, DevTools tidak cukup. Gunakan crawler yang mengekstrak URL dari dalam JavaScript:

```bash
# Katana: crawl + parsing JS (-jc), semua jenis form (-kf all)
katana -u https://target.tld -jc -kf all -d 3 -o crawl.txt

# Ambil hanya URL berekstensi .js
grep -Ei '\.js(\?|$)' crawl.txt | sort -u > js.txt
wc -l js.txt
```

Sumber tambahan untuk chunk lama (sering masih ter-deploy):

```bash
# Wayback
curl -s 'http://web.archive.org/cdx/search/cdx?url=target.tld/*&output=text&fl=original&collapse=urlkey' \
  | grep -Ei '\.js$' | sort -u > wayback-js.txt

# Gau (AlienVault/OTX, Wayback, Common Crawl)
gau --subs target.tld | grep -Ei '\.js$' | sort -u > gau-js.txt
```

Chunk lama yang masih 200 adalah temuan: kode yang sudah tidak dirujuk UI tapi masih dapat diunduh. Di situlah kunci dan endpoint yang sudah "dihapus" sering masih hidup.

## 8. Format Inventaris

Simpan satu tabel sebelum mulai membaca kode:

| Chunk | Rute/fitur pemicu | Lazy? | Ukuran | Source map | Prioritas |
|---|---|---|---|---|---|
| `main.a1b2.js` | semua halaman | tidak | 320 KB | ya | 1 |
| `runtime.a1b2.js` | semua halaman | tidak | 3 KB | tidak | 1 (berisi tabel chunk) |
| `admin.9f8e.js` | `/admin` | ya | 180 KB | tidak | 1 (nama sensitif) |
| `vendor.77aa.js` | semua halaman | tidak | 640 KB | tidak | 4 (lewati) |

Prioritas 1 = entry + runtime + nama chunk sensitif. Prioritas 4 = vendor pihak ketiga.

## 9. Kapan Berhenti

Berhenti mengumpulkan dan mulai membaca kode ketika:

- 3 rute utama sudah dipetakan, **dan**
- satu putaran crawl penuh tidak menemukan nama chunk baru, **dan**
- tabel inventaris tidak lagi bertambah baris.

Ambang lengkap ada di `## Decision Frame` pada SKILL.md. Terus menambah chunk tanpa membaca satu pun adalah kegagalan recon yang paling umum.

## Referensi Cepat

- Chrome DevTools Coverage: `Ctrl+Shift+P` → `Coverage`
- Pencarian lintas berkas: `Ctrl+Shift+F` (panel Sources)
- Webpack chunk map: `__webpack_require__.u`, public path `__webpack_require__.p`
- Vite deps array: `__vite__mapDeps`
- Next.js build id: `__NEXT_DATA__.buildId`
- Nuxt state: `window.__NUXT__`
