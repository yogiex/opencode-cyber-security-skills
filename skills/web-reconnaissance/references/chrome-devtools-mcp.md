---
name: "Chrome DevTools MCP: Otomasi Capture"
description: "Memakai MCP server chrome-devtools-mcp untuk merekam network, mengekspor body chunk, mengevaluasi skrip halaman, membaca logpoint lewat source map, dan mengisi form login — dengan daftar tool, lima alur kerja, serta batas yang harus diakui."
tags: [mcp, chrome-devtools, devtools, network, automation, evaluate-script, logpoint, puppeteer, har]
---

# Chrome DevTools MCP

Tab Network dan Application bisa diklik manual, tetapi recon yang dapat diulang butuh capture yang menghasilkan berkas. `chrome-devtools-mcp` mengendalikan Chrome sungguhan lewat Model Context Protocol: ia membuka halaman, mendaftar request, menyimpan body respons ke disk, dan menjalankan JavaScript di halaman.

Bedanya dengan HAR: HAR adalah snapshot sekali simpan; MCP adalah kontrol berulang. Anda bisa memfilter berdasarkan tipe resource, menarik hanya chunk yang belum dimiliki, lalu mengulang setelah login tanpa menavigasi UI dari awal.

> **Prasyarat:** MCP server harus sudah dikonfigurasi di klien Anda. Skill ini tidak memasangnya. Bila tool seperti `list_network_requests` tidak muncul di daftar tool agen, MCP belum aktif — pakai prosedur manual di [network-analysis.md](network-analysis.md) dan jangan mengklaim capture otomatis.

## 1. Konfigurasi

Tambahkan ke konfigurasi MCP klien:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest", "--isolated", "--no-usage-statistics"]
    }
  }
}
```

| Flag | Kapan dipakai | Kenapa penting untuk recon |
|---|---|---|
| `--isolated` | selalu, untuk recon | profil sementara yang bersih: tidak ada cookie, ekstensi, atau storage sisa sesi Anda |
| `--headless` | capture otomatis tanpa mengganggu layar | SPA dengan animasi tetap merender; berguna untuk batch |
| `--slim` | hanya bila butuh tool minimal | mengekspos sebagian tool saja — jangan pakai untuk recon yang butuh network |
| `--no-usage-statistics` | selalu | statistik pemakaian aktif secara default |
| `--no-performance-crux` | bila memakai trace | mencegah URL trace dikirim ke CrUX |

Batas yang perlu diketahui di depan:

- Hanya **Chrome** dan **Chrome for Testing** yang didukung resmi. Browser berbasis Chromium lain "mungkin berjalan" — jangan jadikan dasar prosedur.
- Server membuka isi browser kepada klien MCP. Jangan arahkan ke profil pribadi Anda.
- Nama tool dan parameter berubah antar versi. Rujukan di dokumen ini diverifikasi pada versi terbaru per 2026-11-09; setelah upgrade, periksa `docs/tool-reference.md` di repo paketnya.

## 2. Tool yang Relevan untuk Recon

| Tool | Parameter penting | Dipakai untuk |
|---|---|---|
| `new_page` | `url`, `isolatedContext`, `background` | membuka target di konteks terisolasi; konteks berbeda = cookie/storage terpisah |
| `list_pages` | — | melihat page id dan service worker (`sw-N`) |
| `select_page` | `pageId` | menjadikan satu tab sebagai target tool berikutnya |
| `navigate_page` | `pageId`, `type` (`url`/`reload`/`back`), `url`, `ignoreCache`, `initScript` | reload tanpa cache; `initScript` menyisipkan skrip sebelum dokumen dimuat |
| `list_network_requests` | `pageId`, `resourceTypes`, `includePreservedRequests`, `pageSize`, `pageIdx` | daftar request sejak navigasi terakhir |
| `get_network_request` | `pageId`, `reqid`, `requestFilePath`, `responseFilePath` | detail header + body; menyimpan body ke disk |
| `evaluate_script` | `pageId`, `function`, `format`, `filePath`, `serviceWorkerId`, `waitForStableDom` | dump storage, decode JWT, panggil `fetch` dari origin halaman |
| `take_snapshot` | `pageId`, `verbose`, `filePath` | pohon aksesibilitas + `uid` untuk `click`/`fill` |
| `click` / `fill_form` | `pageId`, `uid` / `elements` | menavigasi UI agar rute lazy termuat; login |
| `wait_for` | `pageId`, `text`, `visible`, `timeout` | menunggu render sebelum capture |
| `list_console_messages` | `pageId`, `types`, `includePreservedMessages`, `includeStackTraces` | error, warning, dan keluaran `set_logpoints` |
| `set_logpoints` | `pageId`, `logpoints` | mencatat ekspresi pada baris source asli (source-map aware) tanpa menghentikan eksekusi |
| `take_screenshot` | `pageId`, `filePath`, `fullPage` | bukti visual |
| `emulate` | `pageId`, `extraHttpHeaders`, `userAgent` | menyisipkan header `Authorization` pada semua request halaman |
| `performance_start_trace` | `pageId`, `filePath`, `reload`, `ignoreCache` | trace lengkap (waterfall) bila daftar request tidak cukup |

**Yang tidak ada:** tidak ada tool khusus storage. `localStorage`, cookie, IndexedDB, dan Cache Storage hanya terbaca lewat `evaluate_script` — lihat [browser-storage.md](browser-storage.md).

Nilai `resourceTypes` mengikuti tipe resource DevTools. Yang lazim dipakai: `Document`, `Script`, `XHR`, `Fetch`, `Stylesheet`, `Image`, `Font`, `WebSocket`, `Other`. Bila filter menghasilkan daftar kosong padahal request terlihat di UI, panggil tanpa filter lebih dulu dan periksa nilai tipe yang dikembalikan.

## 3. Alur 1 — Rekam Seluruh Traffic

1. `new_page` dengan `url: "https://target.tld"` dan `isolatedContext: "recon"`.
2. `list_network_requests` dengan `pageSize: 200` — inilah baseline load awal.
3. `take_snapshot`, lalu `click` pada menu/tombol utama untuk memicu rute lazy. Ulangi satu per satu; setiap klik menambah request baru.
4. `list_network_requests` dengan `includePreservedRequests: true` setelah beberapa navigasi.
5. Filter bertahap: `resourceTypes: ["Script"]` untuk chunk, `["XHR", "Fetch"]` untuk API.
6. Untuk request penting, `get_network_request` dengan `responseFilePath: "recon/api/users.json"` — body tersimpan ke disk, bukan ke konteks percakapan.

Aturan praktis:

- Simpan **hanya** yang akan dibaca. Menyimpan 300 responden gambar memperlambat tanpa menambah pemahaman.
- `get_network_request` mengembalikan header `Cookie` dan `Set-Cookie`. Perlakukan keluarannya seperti kredensial.
- Request yang bertanda `(ServiceWorker)` di DevTools tetap muncul di daftar; unregister service worker lebih dulu bila Anda ingin melihat request asli ke server.

## 4. Alur 2 — Dump Storage

```text
evaluate_script(
  pageId = <id>,
  function = <skrip dump dari browser-storage.md §2>,
  waitForStableDom = false,
  filePath = "recon/storage-before-login.json"
)
```

Lalu ulangi setelah login dengan `filePath` berbeda. Dua berkas itu menjadi pembanding: apa yang ditulis saat sesi dibuat, dan apa yang tertinggal setelah logout.

`waitForStableDom: false` penting — skrip ini hanya membaca, dan menunggu DOM stabil pada SPA yang terus berdenyut akan kehabisan waktu.

## 5. Alur 3 — Kumpulkan Chunk Tanpa Panel Coverage

1. `list_network_requests` dengan `resourceTypes: ["Script"]`.
2. Untuk setiap request `.js`, `get_network_request` dengan `responseFilePath` ke `recon/chunks/<nama-asli>.js`.
3. Jalankan langkah analisis yang sama seperti pada [js-chunk-analysis.md](js-chunk-analysis.md): `js-beautify`, lalu grep endpoint/rute/kunci.

Keuntungan: tidak ada klik manual, dan daftar chunk tercatat sebagai berkas. Keterbatasan: hanya chunk yang **benar-benar dimuat** yang tertangkap — chunk di balik peran lain tidak akan muncul sampai rutenya dibuka. Karena itu langkah `click` pada alur 1 bukan opsional.

Alternatif untuk SPA besar: `performance_start_trace` dengan `reload: true`, lalu `performance_stop_trace` menyimpan trace JSON. Trace memuat seluruh request beserta timing — berguna untuk melihat urutan pemuatan, tetapi filenya jauh lebih besar daripada daftar request.

## 6. Alur 4 — Recon Terautentikasi

Dua cara, pilih satu:

**A. Login lewat UI** — `take_snapshot` → `fill_form` dengan kredensial uji → `click` tombol submit → `wait_for` teks dashboard → baru capture. Ini menirukan alur nyata, termasuk request yang hanya muncul setelah login.

**B. Menyisipkan header** — `emulate` dengan `extraHttpHeaders: "{\"Authorization\": \"Bearer <token-uji>\"}"`. Header berlaku untuk setiap request dari halaman dan bertahan lintas navigasi sampai dikosongkan. Cocok bila aplikasi memakai bearer token dan Anda ingin melewati UI.

Bandingkan hasil sebelum dan sesudah login:

| Yang dibandingkan | Pertanyaan |
|---|---|
| Daftar request | endpoint mana yang hanya muncul setelah login |
| Storage | kunci apa yang ditulis saat sesi dibuat |
| Status | endpoint yang berubah dari 401 menjadi 200 |
| Cookie | flag yang berubah setelah autentikasi |

Untuk menguji keadaan logout: `new_page` dengan `isolatedContext` baru — konteks berbeda tidak berbagi cookie maupun storage.

## 7. Alur 5 — Logpoint lewat Source Map

`set_logpoints` mencatat ekspresi pada baris tertentu tanpa menghentikan eksekusi, dan lokasinya **diselesaikan lewat source map** — Anda menunjuk berkas TypeScript asli, bukan bundle hasil build.

```text
set_logpoints(pageId = <id>, logpoints = [
  "src/api/client.ts:42 'request:', options.url, options.headers",
  "src/auth/session.ts:118 'session:', session.user, session.expiresAt"
])
```

Keluarannya muncul di `list_console_messages`. Ini teknik recon yang jarang dipakai: alih-alih menebak dari nama fungsi di bundle, Anda melihat argumen sebenarnya saat aplikasi berjalan — termasuk objek yang tidak pernah menyentuh storage maupun network.

Bila aplikasi tidak punya source map, `set_logpoints` tetap bisa menunjuk berkas hasil build selama URL-nya diketahui dari daftar request.

> Untuk alur lengkap dari aksi UI ke endpoint — termasuk instrumentasi `fetch`/`XHR` bila sumber asli tidak tersedia — lihat [data-flow-analysis.md](data-flow-analysis.md).

## 8. Batas dan Cara Mengakalinya

| Batas | Dampak | Mitigasi |
|---|---|---|
| Tidak ada tool storage | storage hanya lewat `evaluate_script` | pakai skrip dump; jangan menyimpulkan "tidak ada storage" tanpa menjalankannya |
| `list_network_requests` menghapus riwayat per navigasi | request lama hilang | `includePreservedRequests: true` (tiga navigasi terakhir) atau simpan per gelombang |
| Tidak ada penargetan iframe lintas origin | storage di iframe pihak ketiga tidak terbaca dari frame atas | buka origin iframe sebagai halaman sendiri, dengan izin scope |
| `evaluate_script` harus mengembalikan JSON | `Map`, `Set`, `Blob`, `File` hilang | konversi ke array/string sebelum `return` |
| Body respons sangat besar | respons terpotong atau lambat | simpan ke `responseFilePath`, jangan inline |
| `--slim` memangkas tool | tool network/evaluate bisa tidak tersedia | jalankan tanpa `--slim` untuk recon |
| Tool dapat berubah antar versi | perintah di dokumen ini bisa usang | pin versi server; periksa `docs/tool-reference.md` setelah upgrade |

## 9. Fallback Tanpa MCP

Bila MCP tidak tersedia, seluruh tujuan di atas tetap bisa dicapai secara manual:

| Kebutuhan | Pengganti manual |
|---|---|
| Daftar request | Tab Network, filter per tipe, **Preserve log** dicentang |
| Body chunk | klik kanan request → **Save response**, atau `curl` URL chunk |
| Storage | Console: skrip §2 di [browser-storage.md](browser-storage.md) |
| Login | isi form sendiri; bandingkan capture sebelum/sesudah |
| Logpoint | Tab Sources → klik nomor baris → **Add logpoint** |
| Trace | Tab Performance → rekam → **Export** |

Yang **tidak** boleh dilakukan: menulis di laporan bahwa capture dilakukan otomatis bila MCP tidak aktif. Catat alat yang benar-benar dipakai.

## 10. Checklist

- [ ] MCP aktif dan `list_network_requests` muncul di daftar tool
- [ ] Server dijalankan dengan `--isolated` dan `--no-usage-statistics`
- [ ] `new_page` memakai `isolatedContext` bernama
- [ ] Service worker di-unregister sebelum capture
- [ ] Navigasi UI dijalankan sampai rute lazy termuat
- [ ] Request `.js` disimpan ke `recon/chunks/`
- [ ] Dump storage diambil sebelum **dan** sesudah login
- [ ] Header `Cookie`/`Set-Cookie` dan token diredaksi sebelum keluar dari mesin
- [ ] Batas tool dicatat di laporan (mis. "storage iframe tidak diperiksa")
- [ ] Tool diverifikasi cocok dengan versi server yang terpasang

## Best Practices

1. Mulai dari satu halaman, satu konteks, satu tujuan: daftar request yang bisa dijelaskan.
2. Simpan body ke `responseFilePath`, bukan ke percakapan — konteks agen terbatas, disk tidak.
3. Perlakukan setiap keluaran `get_network_request` sebagai bahan sensitif, setara HAR.
4. Ulangi alur yang sama setelah login; perbedaan antara dua capture adalah hasil recon-nya.
5. Bila hasil tool tampak kosong, periksa `list_pages` lebih dulu — sering kali targetnya adalah tab yang salah.

> Rujukan tool dan parameter disalin dari `docs/tool-reference.md` paket `chrome-devtools-mcp` (diakses 2026-11-09). Ini snapshot, bukan kontrak permanen: periksa ulang setelah upgrade server.
