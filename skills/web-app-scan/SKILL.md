---
name: web-app-scan
description: Melakukan vulnerability assessment pada web application secara sistematis seperti tools Nessus (deteksi kerentanan umum: SQLi, XSS, config leak, header keamanan, SSL/TLS, dsb) dengan pendekatan terstruktur dan non-teknis.
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, penetration tester, web developer, system admin
  tool-analogy: Nessus, Nikto, OpenVAS
---

## What I do

Saya membantu Anda melakukan **web application security assessment** dengan pendekatan seperti vulnerability scanner (Nessus/OpenVAS) namun dalam bentuk panduan langkah demi langkah yang sistematis. Saya tidak menjalankan scanning otomatis, tetapi memberikan prosedur pemeriksaan yang bisa Anda ikuti sendiri atau Anda minta agent lain menjalankannya.

Berikut yang akan saya lakukan bersama Anda:

### A. Persiapan Assessment

1. **Tentukan target** – URL web app yang akan dinilai (termasuk subdomain dan API endpoint jika ada)
2. **Tentukan ruang lingkup** – Apakah termasuk autentikasi? Form login? Area admin? (tanpa kredensial vs dengan kredensial)
3. **Dapatkan izin** – Pastikan Anda memiliki otorisasi tertulis dari pemilik sistem (ini penting, jangan lewatkan)
4. **Siapkan tools bantuan** (opsional) – Curl, browser devtools, atau extension seperti Wappalyzer

### B. Tahapan Assessment (Seperti yang Dilakukan Nessus)

Saya akan memandu Anda melalui 6 fase berikut:

**Fase 1: Informasi Umum & Fingerprinting**

- Identifikasi teknologi yang digunakan (web server, framework, library) – seperti Nessus melakukan banner grabbing
- Cek header keamanan HTTP yang ada (Content-Security-Policy, X-Frame-Options, HSTS, dll)
- Cek apakah versi software diketahui memiliki kerentanan publik (CVE)

**Fase 2: Pemeriksaan Konfigurasi & Informasi Bocor**

- Cek file/folder sensitif yang terekspos (robots.txt, .git, .env, backup file, readme, changelog)
- Cek apakah error message menampilkan path server, stack trace, atau informasi database
- Cek apakah method HTTP tidak aman (TRACE, OPTIONS) diaktifkan
- Cek session cookie apakah memiliki flag Secure, HttpOnly, SameSite

**Fase 3: Injection Vulnerability (SQL, NoSQL, Command)**

- Identifikasi parameter pada URL, form, atau API
- Uji sederhana dengan payload umum (tanpa merusak data) untuk melihat apakah aplikasi rentan injection
- Contoh: tambahkan kutip tunggal `'` atau `AND 1=1` – amati perubahan respons
- (Saya akan memberikan daftar payload yang aman untuk uji coba non-destruktif)

**Fase 4: Cross-Site Scripting (XSS)**

- Cek apakah input pengguna (search box, komentar, parameter URL) direfleksikan kembali ke halaman tanpa encoding
- Uji dengan payload sederhana seperti `<script>alert('xss')</script>` atau `<img src=x onerror=alert(1)>`
- Cek juga XSS tersimpan (stored) jika ada fitur komentar/profil
- Cek DOM-based XSS pada javascript client-side

**Fase 5: Autentikasi & Manajemen Sesi**

- Cek apakah login page menggunakan HTTPS (wajib)
- Apakah percobaan login gagal dibatasi (rate limiting) atau ada captcha?
- Apakah session timeout diterapkan? (logout otomatis setelah idle)
- Apakah password bisa di-reset tanpa verifikasi yang cukup?
- Cek apakah sesi berubah setelah login (tidak bisa di-export ke perangkat lain tanpa autentikasi ulang)

**Fase 6: Kontrol Akses & Business Logic**

- Coba akses URL admin langsung (misal /admin) tanpa login – apakah diblok?
- Coba ubah parameter ID (misal /user?id=1234 menjadi 1235) – apakah bisa lihat data orang lain? (IDOR)
- Cek apakah role biasa bisa melakukan aksi yang hanya untuk admin (misal menghapus pengguna)
- Cek apakah ada fungsi upload file yang membatasi tipe file (gunakan ekstensi gambar tetapi isi php)

### C. Pemeriksaan Tambahan (Seperti Advanced Scan Nessus)

- **SSL/TLS konfigurasi** – Cek apakah masih menggunakan TLS 1.0/1.1, cipher lemah, atau sertifikat tidak valid
- **Fuzzing endpoint** – Coba temukan endpoint tersembunyi (seperti /backup.zip, /old, /test)
- **CORS misconfiguration** – Apakah header Access-Control-Allow-Origin terlalu permisif (`*`)
- **Open redirect** – Parameter `redirect=` atau `next=` bisa diarahkan ke domain lain
- **File inclusion** – Parameter `page=` atau `file=` bisa memasukkan file lokal/remote (LFI/RFI)

### D. Output Assessment

Setelah melakukan semua fase di atas, saya akan membantu Anda menghasilkan laporan dengan struktur seperti ini:

```markdown
RINGKASAN EKSEKUTIF
Target: https://contoh.com
Tanggal: dd/mm/yyyy
Tingkat risiko keseluruhan: [Rendah/Sedang/Tinggi/Kritis]

TEMUAN PRIORITAS (HIGH & CRITICAL)

1. [Kritis] SQL injection pada parameter `id` di /product – memungkinkan akses database
2. [Tinggi] Session cookie tidak memiliki flag HttpOnly – dapat dicuri via XSS
3. [Tinggi] Backup file terekspos di /backup/db.sql

TEMUAN MEDIUM

- Header CSP tidak ada, berisiko XSS lanjutan
- Versi jQuery 1.12 (tua) diketahui memiliki CVE-2019-11358

TEMUAN RENDAH / INFORMATIONAL

- Robots.txt mengungkap path admin
- Server signature masih terlihat (Apache/2.4.41)

REKOMENDASI

1. Gunakan parameterized query pada semua database
2. Terapkan HttpOnly, Secure, SameSite pada cookie
3. Hapus file backup dari direktori publik
```
