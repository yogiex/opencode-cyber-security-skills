---
name: web-recon-simple
description: Recon web sederhana: chunk file, network tab, API endpoint, localstorage/token/session, teknologi.
license: MIT
compatibility: opencode
---

# Web Recon Sederhana

Lakukan langkah-langkah ini secara berurutan.

## 1. Cek Chunk File

- Buka DevTools (F12) → Tab **Sources**
- Cari file `*.chunk.js`, `bundle.js`, `main.*.js`
- Scan isinya untuk menemukan:
  - Endpoint API (`/api/`, `/v1/`, `/graphql`)
  - Path internal (`/admin`, `/internal`, `/debug`)
  - Komentar tersembunyi

## 2. Cek Network Tab

- Buka DevTools → Tab **Network**
- Refresh halaman (F5)
- Filter dengan **XHR** atau **Fetch**
- Catat:
  - Request URL dan method (GET, POST, dll)
  - Request headers (Cookie, Authorization, X-API-Key)
  - Response body (apakah ada data sensitif)

## 3. Cek API Endpoint Mapping

- Kumpulkan semua endpoint yang ditemukan dari langkah 1 dan 2
- Lakukan fuzzing manual dengan mencoba:
  - `/api/v1/users`
  - `/api/v1/admin`
  - `/api/docs`, `/swagger`, `/openapi.json`
- Catat endpoint yang merespon status 200, 401 (terautentikasi), atau 403

## 4. Cek LocalStorage, Token, Session

- DevTools → Tab **Application**
- Lihat di bagian **Storage**:
  - **Local Storage** → cari token, user data, session ID
  - **Session Storage** → cari temporary token
  - **Cookies** → perhatikan flag `HttpOnly` (tidak bisa dibaca JS), `Secure` (hanya HTTPS), `SameSite`
- Di console, jalankan:
  ```javascript
  console.log(localStorage);
  console.log(sessionStorage);
  console.log(document.cookie);
  ```

## 5. Cari Jenis Teknologi

- Cek response headers (DevTools → Network → pilih request pertama → Headers):
  - `Server` (misal: nginx, Apache, Cloudflare)
  - `X-Powered-By` (PHP, Express, ASP.NET)
  - `Set-Cookie` (PHPSESSID → PHP, JSESSIONID → Java)
- Cek HTML source (`Ctrl+U`) untuk framework:
  - `__NEXT_DATA__` → Next.js
  - `__NUXT__` → Nuxt
  - `react` atau `ReactDOM` → React
  - `vue` → Vue
- Gunakan tools bantuan: Wappalyzer (extension browser)

## 6. Cari CVE Terbaru

Setelah mengetahui teknologi dan versi yang digunakan, cari CVE yang relevan:

- Gunakan web search untuk setiap teknologi + versi yang ditemukan:
  - `nginx 1.25.0 CVE`
  - `Express 4.18.0 CVE`
  - `Next.js 14.0.0 CVE`
  - `WordPress 6.4 CVE`
- Sumber pencarian:
  - NVD (National Vulnerability Database) — search by product/version
  - Google/Pencarian web untuk laporan CVE terbaru
  - `searchsploit --cve <nama-teknologi>` (read-only, hanya lihat daftar)
- Catat untuk setiap CVE yang ditemukan:
  - **CVE ID** (contoh: CVE-2025-12345)
  - **CVSS Score** (contoh: 8.2 HIGH)
  - **Versi terpengaruh** (contoh: < 1.25.3)
  - **Deskripsi singkat** dan status (Published, Reserved, Rejected)
- **Jangan** menyertakan exploit code atau PoC — cukup identifikasi dan catat kerentanannya

## Contoh Perintah Cepat (opsional)

```bash
# Cek header
curl -I https://target.com

# Cari endpoint di source
curl -s https://target.com | grep -E 'https?://api|/v[0-9]/|/graphql' -i

# Simpan semua endpoint sementara
curl -s https://target.com | grep -oP '(https?://[^"'\'' ]+)' > urls.txt
```

## Output Laporan

Buat ringkasan dengan format:

- **Teknologi**: [backend, frontend, server]
- **Endpoint ditemukan**: [daftar endpoint]
- **Token/Session terekspos**: [ada/tidak, jika ada sebutkan]
- **CVE Terkait**: [daftar CVE ID + CVSS score + versi terpengaruh]
- **Potensi lanjutan**: [rekomendasi fuzzing atau testing lanjutan]

Selesai. Gunakan skill ini saat perlu reconnaissance web cepat dan terstruktur.
