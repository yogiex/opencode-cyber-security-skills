---
name: "Storage Browser: Membaca yang Dipegang Klien"
description: "Cara menginventarisasi dan membaca seluruh storage browser — localStorage, sessionStorage, cookie (termasuk HttpOnly), IndexedDB, Cache Storage, dan OPFS — plus triage token, redaksi, dan cara mengubahnya menjadi temuan yang terbukti."
tags: [storage, localstorage, sessionstorage, cookies, indexeddb, cachestorage, opfs, jwt, token, session, devtools]
---

# Storage Browser

Storage adalah tempat aplikasi menaruh apa pun yang tidak ingin ia minta ulang ke server: token, objek user, tenant, cache respons, draf formulir. Recon yang melewatkannya akan melaporkan "tidak ada kebocoran" padahal token admin duduk di `localStorage` sejak halaman pertama.

Satu hal yang tidak boleh salah: **storage hanya berisi apa yang ditulis klien**. Token yang hidup di memori (state React, variabel modul) tidak akan muncul di sini — untuk itu Anda perlu traffic. Storage dan Network saling melengkapi, bukan menggantikan.

> Untuk membaca *bagaimana* token itu diperbarui dan diakhiri — rotasi refresh, pencabutan, CSRF, OAuth — lanjutkan ke [auth-configuration.md](auth-configuration.md).

## 1. Enam Storage, Enam Pertanyaan

| Storage | Terbaca dari JS? | Isi khas | Yang dicari |
|---|---|---|---|
| **localStorage** | ya | token, objek user, `tenantId`, feature flag | token bearer, peran, id internal, konfigurasi non-publik |
| **sessionStorage** | ya | token sementara, state wizard, OTP flow | token sebelum/sesudah login, data langkah sebelumnya |
| **Cookie** | hanya non-`HttpOnly` | sesi, CSRF token, preferensi | flag `HttpOnly`/`Secure`/`SameSite`, cakupan `Domain`, umur |
| **IndexedDB** | ya (async) | cache respons API, data offline, antrean sinkronisasi | respons terautentikasi yang tersimpan, token di record, id objek |
| **Cache Storage** | ya (async) | respons service worker | HTML/JSON yang di-cache — bisa memuat data user lain di perangkat bersama |
| **OPFS** | ya (async) | berkas besar, model ML, ekspor | arsip/berkas yang tidak seharusnya ada di klien |

Tiga tempat lain yang sering tertukar dengan storage:

- **Service worker** — bukan storage, tetapi dapat menyajikan respons lama dan menyembunyikan request. Daftarkan di Application → Service Workers, lalu **unregister** sebelum capture.
- **`window.name`** — bertahan lintas navigasi dalam satu tab; jarang, tetapi ada aplikasi lama yang menaruh data di sini.
- **WebSQL** — deprecated, masih ada di aplikasi lama. Bila muncul di Application, perlakukan seperti IndexedDB.

## 2. Satu Skrip untuk Semua

Skrip ini mengembalikan JSON yang bisa diserialisasi, memotong nilai panjang, dan tidak melempar error bila satu bagian gagal. Cocok untuk `evaluate_script` MCP (`waitForStableDom: false`) maupun untuk ditempel di Console.

```javascript
async () => {
  const cut = (v, n = 160) => {
    const s = typeof v === 'string' ? v : JSON.stringify(v);
    return s && s.length > n ? s.slice(0, n) + '…' : s;
  };
  const out = { url: location.href, origin: location.origin,
                localStorage: {}, sessionStorage: {}, cookie: [],
                indexedDB: [], caches: [], opfs: [] };

  for (const [k, v] of Object.entries(localStorage)) out.localStorage[k] = cut(v);
  for (const [k, v] of Object.entries(sessionStorage)) out.sessionStorage[k] = cut(v);

  out.cookie = document.cookie.split('; ').filter(Boolean).map(p => {
    const i = p.indexOf('=');
    return { name: p.slice(0, i) || p, value: cut(p.slice(i + 1), 40) };
  });

  for (const db of await indexedDB.databases()) {
    const stores = await new Promise(res => {
      const req = indexedDB.open(db.name);
      req.onsuccess = () => { const d = req.result; const n = [...d.objectStoreNames]; d.close(); res(n); };
      req.onerror = () => res([]);
    });
    out.indexedDB.push({ name: db.name, version: db.version, stores });
  }

  for (const name of await caches.keys()) {
    const c = await caches.open(name);
    const keys = await c.keys();
    out.caches.push({ name, entries: keys.length, sample: keys.slice(0, 15).map(r => r.url) });
  }

  if (navigator.storage && navigator.storage.getDirectory) {
    try {
      for await (const [name] of await navigator.storage.getDirectory()) out.opfs.push(name);
    } catch {}
  }
  return out;
}
```

Catatan pemakaian:

- `indexedDB.open(nama)` **tanpa versi** membuka versi terkini. Tidak membuat database baru karena `databases()` hanya mengembalikan yang sudah ada. Bila sebuah database terkunci tab lain, promise `onerror` mengembalikan daftar kosong — bukan alasan menghentikan recon.
- Skrip ini **tidak membaca isi record** IndexedDB. Itu disengaja: satu object store bisa berisi puluhan ribu record. Baca record hanya setelah nama store mencurigakan (lihat §4).
- Nilai dipotong 160 karakter. Token JWT lebih panjang dari itu — potongannya cukup untuk mengenali format, dan itu memang tujuannya.

## 3. Cookie: Empat Tempat, Empat Kebenaran

`document.cookie` **tidak menampilkan cookie `HttpOnly`**. Karena itu "tidak ada cookie sesi di JS" bukan bukti apa pun sampai Anda memeriksa tiga tempat lain:

| Tempat | Melihat | Kegunaan |
|---|---|---|
| `document.cookie` (skrip §2) | hanya cookie non-`HttpOnly` | membuktikan sebuah cookie **dapat** dibaca JavaScript |
| Application → Cookies | semua, termasuk `HttpOnly` | atribut lengkap: `Secure`, `SameSite`, `Domain`, `Path`, `Expires` |
| Header `Cookie` pada request | semua yang dikirim | cookie mana yang benar-benar dipakai untuk otentikasi |
| Header `Set-Cookie` pada respons | semua yang diset | flag yang diminta server, termasuk `HttpOnly` |

Pemeriksaan atribut:

| Atribut | Nilai berisiko | Arti |
|---|---|---|
| `HttpOnly` | tidak ada | cookie dapat dibaca JS → XSS berujung pencurian sesi |
| `Secure` | tidak ada | cookie dapat terkirim lewat HTTP polos |
| `SameSite` | `None` tanpa `Secure` | cookie ikut pada request lintas situs |
| `Domain` | domain induk (`.target.tld`) | cookie terbaca dari semua subdomain, termasuk yang dipegang pihak ketiga |
| `Path` | `/` | berlaku di seluruh aplikasi, bukan hanya area yang perlu |
| `Expires` | sangat jauh / sesi panjang | memperpanjang jendela penyalahgunaan |

Cookie non-`HttpOnly` adalah temuan **Medium** pada umumnya (CWE-1004), bukan High — naikkan hanya bila ada jalur XSS yang terbukti atau cookie itu sendiri adalah token sesi tanpa pembanding lain. Untuk penulisan temuan, lihat skill `security-documentation`.

## 4. IndexedDB: Baca Setelah Nama Store Mencurigakan

Alur: Application → IndexedDB → pilih database → object store → ikon tabel. Untuk membaca sebagian saja tanpa membanjiri tab:

```javascript
async () => {
  const DB = 'ganti-nama-database', STORE = 'ganti-nama-store', LIMIT = 20;
  const db = await new Promise((res, rej) => {
    const r = indexedDB.open(DB);
    r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
  });
  const tx = db.transaction(STORE, 'readonly');
  const store = tx.objectStore(STORE);
  const keys = await new Promise(res => store.getAllKeys().onsuccess = e => res(e.target.result));
  const rows = await new Promise(res => store.getAll(null, LIMIT).onsuccess = e => res(e.target.result));
  db.close();
  return { totalKeys: keys.length, sampleKeys: keys.slice(0, 20), sampleRows: rows };
}
```

Yang dicari di record: token, `userId`, `accountId`, `role`, email pengguna lain, respons endpoint yang butuh otorisasi. Nama store yang sering berisi: `auth`, `session`, `user`, `cache`, `requests`, `outbox`, `keyval`.

Bila aplikasi memakai library (Dexie, idb-keyval, localForage), nama database sering mengikuti library-nya — `keyval-store` untuk idb-keyval, `localforage` untuk localForage. Isinya biasanya blob terenkode; baca `sampleRows` dulu sebelum menyimpulkan.

## 5. Cache Storage: Respons Lama yang Masih Sah

Service worker menyimpan respons di Cache Storage. Isinya bisa berupa HTML terautentikasi atau JSON `/api/me` — dan pada perangkat bersama, cache itu dapat menyajikan data pengguna sebelumnya.

```javascript
async () => {
  const out = [];
  for (const name of await caches.keys()) {
    const c = await caches.open(name);
    const keys = await c.keys();
    out.push({ name, urls: keys.map(r => r.url) });
  }
  return out;
}
```

Membaca satu entri:

```javascript
async () => {
  const c = await caches.open('ganti-nama-cache');
  const r = await c.match('/api/me');
  return r ? { status: r.status, type: r.headers.get('content-type'),
               cacheControl: r.headers.get('cache-control'),
               body: (await r.text()).slice(0, 500) } : null;
}
```

Relevan bila: aplikasi PWA, ada `sw.js` di root, atau respons API muncul sebagai `(ServiceWorker)` di kolom Size tab Network.

## 6. Triage Token

Token ditemukan. Pertanyaannya bukan "apakah ini terlihat seperti rahasia", tetapi "apakah ini masih berlaku, dan apa yang bisa dibuka".

| Jenis | Sinyal | Yang perlu dicatat | Uji yang aman |
|---|---|---|---|
| **JWT** | tiga segmen dipisah titik | `alg`, `exp`, `sub`, klaim peran/tenant | decode saja, **jangan** verifikasi atau ubah; periksa `exp` |
| **Opaque bearer** | string acak panjang | header pengirim (`Authorization`), masa berlaku | satu request `GET /api/me` dengan sesi sendiri |
| **Refresh token** | disimpan terpisah dari access token | apakah `HttpOnly`, apakah dirotasi | jangan diuji di akun nyata |
| **API key** | prefiks vendor | apakah kunci publik (`pk_`, `AIza`) atau rahasia (`sk_live_`, `AKIA`) | lihat triage di `js-chunk-analysis.md` |
| **CSRF token** | ada di meta/ hidden input/cookie | apakah terikat sesi | cukup dicatat; bukan temuan sendirian |

Decode JWT tanpa verifikasi:

```javascript
() => {
  const raw = (localStorage.getItem('token') || '').trim();
  const pad = s => s + '='.repeat((4 - s.length % 4) % 4);
  const dec = s => JSON.parse(new TextDecoder().decode(
    Uint8Array.from(atob(pad(s.replace(/-/g, '+').replace(/_/g, '/'))), c => c.charCodeAt(0))));
  const [h, p] = raw.split('.');
  if (!h || !p) return { error: 'bukan JWT', length: raw.length };
  return { header: dec(h), payload: dec(p), signatureLength: (raw.split('.')[2] || '').length };
}
```

Yang dibaca dari payload: `exp` (kedaluwarsa), `sub`/`userId` (id internal), `role`/`scope` (hak), `tenant`/`org` (batas isolasi), `iss` (penerbit). Ubahan klaim **tidak** dibuktikan di sini — itu masuk `web-app-scan`, dan hanya bila token ditandatangani dengan kunci yang bisa ditebak (mis. `alg: none` atau HMAC dengan rahasia bocor).

## 7. Dari Storage ke Temuan

Storage baru menjadi temuan bila tiga hal ini terpenuhi:

1. **Lokasi pasti** — origin, jenis storage, nama kunci, dan cuplikan bentuk nilainya.
2. **Jalur baca** — siapa yang bisa membacanya. Token di `localStorage` dibaca oleh **setiap** skrip di origin itu, termasuk skrip pihak ketiga yang dimuat halaman.
3. **Dampak** — apa yang dibuka token itu. Bila token dikirim sebagai `Authorization` pada request yang Anda lihat di Network, dampaknya adalah seluruh permukaan API yang menerima token tersebut.

Pemetaan cepat:

| Kondisi | Temuan | Severity awal |
|---|---|---|
| Token sesi di `localStorage`, dikirim via `Authorization` | XSS → pencurian sesi | Medium–High (tergantung jalur XSS) |
| Cookie sesi tanpa `HttpOnly` | CWE-1004 | Medium |
| Cookie sesi tanpa `Secure` | dapat bocor lewat HTTP | Medium |
| `SameSite` tidak diset pada cookie sesi | CSRF lebih mudah | Low–Medium |
| Data pengguna lain di Cache Storage | kebocoran lintas pengguna di perangkat bersama | High |
| Token/kunci rahasia di bundle JS (bukan storage) | lihat `js-chunk-analysis.md` | sesuai triage kunci |

**Bukan temuan:** adanya `localStorage` berisi preferensi tema/bahasa, `featureFlag` non-sensitif, atau id publik yang juga muncul di HTML.

## 8. Redaksi dan Etika

- Simpan dump mentah di luar repo, di direktori kerja yang tidak di-commit. Sama seperti HAR — keduanya berisi token.
- Di laporan, tulis nama kunci dan **bentuk** nilai, bukan nilainya: `access_token = eyJhbGciOi…` (potong setelah 10 karakter), jangan pernah token utuh.
- Bila pengujian memakai akun nyata, ganti email/nomor telepon dengan penanda sebelum masuk laporan.
- Jangan menguji token yang ditemukan pada akun pengguna lain. Untuk membuktikan dampak, gunakan akun milik sendiri dan tunjukkan bahwa token yang sama membuka data yang sama.
- Storage bersifat per origin. Bila aplikasi memakai `app.target.tld` dan `api.target.tld`, dump keduanya — tidak ada satu pun yang mewakili yang lain.

## 9. Jebakan

- **`document.cookie` kosong bukan berarti tidak ada cookie.** `HttpOnly` menyembunyikannya dari JS, bukan dari Application panel atau header request.
- **Storage kosong bisa berarti profil baru, bukan aplikasi bersih.** Bandingkan sesi logged-out dan logged-in di dua profil terpisah.
- **Token di memori tidak muncul di storage.** Bila tidak menemukan apa pun, periksa header `Authorization` di Network — mungkin token dibuat per request.
- **Membaca seluruh IndexedDB membekukan tab.** Selalu batasi dengan `LIMIT` dan mulai dari nama store.
- **Cache Storage bisa menyajikan data basi.** Entri lama dapat memuat respons user sebelumnya; itu justru inti temuannya, jadi catat waktu cache dan versi SW.
- **`localStorage` dipisah per origin, bukan per path.** Dua aplikasi di origin yang sama berbagi seluruh storage.
- **Logout yang tidak membersihkan storage** meninggalkan token yang masih sah — uji dengan logout lalu buka ulang tab.
- **Skrip `evaluate_script` harus mengembalikan JSON.** `Map`, `Set`, `File`, dan `Blob` harus dikonversi lebih dulu atau hasilnya kosong.

## Best Practices

1. Jalankan skrip §2 sekali di awal, simpan hasilnya sebagai baseline, lalu ulangi setelah login.
2. Baca nama kunci lebih dulu; nilai hanya bila nama atau bentuknya mencurigakan.
3. Bandingkan storage dengan header `Authorization` dan `Cookie` di Network — token yang tidak dikirim ke mana pun bukan temuan.
4. Catat juga **siapa yang menulis**: cari nama kunci di bundle JS untuk menemukan kode yang menyimpannya (`js-chunk-analysis.md`).
5. Redaksi sebelum menyimpan, bukan sebelum mengirim laporan.
