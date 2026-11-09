---
name: web-app-scan
description: "Penilaian keamanan web application bertahap seperti Nessus/Nikto tetapi manual dan dapat diaudit: fingerprint, config leak, injection, XSS, sesi, akses kontrol, TLS, CORS. Muat saat perlu audit web app terstruktur tanpa scanner otomatis."
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, penetration tester, web developer, system admin
  tool-analogy: Nessus, Nikto, OpenVAS
---

# Web App Scan

Prosedur pemeriksaan bertahap untuk satu aplikasi web. Bukan scanner otomatis: setiap temuan lahir dari permintaan yang dijalankan, diamati, dan dicatat dengan bukti.

## Decision Frame

- **Izin tertulis lebih dulu.** Tanpa itu, hanya boleh pengamatan pasif: `GET` halaman publik, header, dan sertifikat. Tidak ada payload, tidak ada tebakan path.
- **Default read-only.** Uji yang mengubah data (`POST`, `PUT`, `DELETE`, upload, pembuatan akun) hanya dengan izin eksplisit dan pada data milik sendiri.
- **Scanner memberi kandidat, bukan temuan.** Konfirmasi dengan dua kali reproduksi dan penanda unik; yang tidak terkonfirmasi masuk "tidak tereproduksi".
- **Dua varian per parameter, lalu berhenti.** Bila respons tidak berubah, catat dan pindah. Menembak sepuluh payload ke satu parameter adalah fuzzing, bukan assessment.
- **Hormati laju server.** Satu permintaan per detik saat menguji login atau rate limit; berhenti pada `429` dan catat header `Retry-After`.
- **Laporkan cakupan terautentikasi secara terpisah.** Hasil tanpa login tidak boleh dibaca sebagai hasil lengkap.

## A. Persiapan

1. **Target** — URL, subdomain, dan endpoint API yang termasuk.
2. **Ruang lingkup** — tanpa kredensial atau dengan kredensial; apakah area admin, unggah berkas, dan pembayaran termasuk.
3. **Otorisasi** — nomor tiket/surat tugas; simpan rujukannya di laporan.
4. **Batas mode** — pasif / aktif-ringan / aktif-intrusif, disepakati sebelum mulai.
5. **Alat** — `curl`, DevTools, proxy (opsional). Tidak wajib scanner.

## B. Enam Fase

### Fase 1 — Fingerprint

- Teknologi: header `Server`, `X-Powered-By`, `meta generator`, `ng-version`, `__NEXT_DATA__`.
- Header keamanan: `Content-Security-Policy`, `Strict-Transport-Security`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.
- Versi yang terungkap → calon CVE (lihat skill `web-reconnaissance`).

### Fase 2 — Konfigurasi dan Kebocoran Informasi

- Berkas/folder: `robots.txt`, `sitemap.xml`, `.git/HEAD`, `.env`, `backup.zip`, `README`, `CHANGELOG`, `*.sql`, `*.bak`.
- Pesan error: stack trace, path server, nama database.
- Method: `TRACE`, `OPTIONS`, `PUT` yang tidak seharusnya aktif.
- Cookie: `Secure`, `HttpOnly`, `SameSite`, `Domain`, masa berlaku.

### Fase 3 — Injection

- Petakan parameter dari URL, form, JSON body, dan header yang tercermin.
- Uji non-destruktif: kutip tunggal `'`, `AND 1=1`, `OR 1=2`, dan bandingkan status, panjang, serta isi respons.
- Perhatikan pesan error SQL, perbedaan waktu respons (time-based), dan perubahan tipe data.
- Untuk JSON/API: uji tipe (`"1"` vs `1`), nilai `null`, dan array.

### Fase 4 — Cross-Site Scripting

- Reflected: sisipkan penanda unik (`zzq7x1`), cek apakah muncul tanpa encoding dan di konteks apa (HTML, atribut, JS, JSON).
- Stored: kirim ke fitur komentar/profil; verifikasi di permintaan berikutnya, bukan hanya di layar sendiri.
- DOM: periksa `innerHTML`, `document.write`, `eval`, dan `location` pada bundle klien.
- `alert(1)` tidak membuktikan apa pun di bawah CSP ketat — periksa konsol.

### Fase 5 — Autentikasi dan Sesi

- Login lewat HTTPS; tanpa itu, kredensial transitif terekspos.
- Rate limit / captcha pada percobaan gagal (uji maksimal 5 percobaan).
- Timeout idle dan rotasi sesi setelah login.
- Alur reset password: token acak, sekali pakai, kedaluwarsa, tidak bocor di URL.
- Cookie sesi: `HttpOnly` + `Secure` + `SameSite`.

### Fase 6 — Kontrol Akses dan Business Logic

- Akses langsung ke `/admin`, `/api/admin/*` tanpa peran yang sesuai.
- IDOR: ubah id objek — uji hanya dengan dua akun milik sendiri.
- Peran: aksi admin yang dapat dijalankan peran biasa.
- Upload: batas tipe, ukuran, nama berkas; apakah isi diverifikasi, bukan hanya ekstensi.
- Harga/jumlah/kupon: apakah dihitung ulang di server.

## C. Pemeriksaan Tambahan

- **TLS**: protokol usang (1.0/1.1), cipher lemah, rantai sertifikat, masa berlaku. Sebutkan alat dan versinya — hasil `openssl` dan browser bisa berbeda.
- **CORS**: `Access-Control-Allow-Origin: *` bersama `Allow-Credentials: true`; refleksi `Origin` apa pun.
- **Open redirect**: parameter `redirect`, `next`, `return`, `url`.
- **LFI/RFI**: parameter `page`, `file`, `path`, `template`.
- **Endpoint tersembunyi**: `/backup.zip`, `/old`, `/test`, `/api/docs`, `/swagger`, `/openapi.json`, `/actuator`.

## Gotchas

- **WAF memblokir uji dan menghasilkan false negative.** Kirim satu permintaan benign lebih dulu; bila juga diblokir, catat bahwa pengujian terhalang, jangan menyimpulkan "aman".
- **SPA membalas 200 untuk hampir semua path.** `/admin` 200 belum berarti ada; periksa `Content-Type` dan isi.
- **Header keamanan yang hilang bukan High.** Tanpa rantai serangan, tempatnya Low/Info.
- **`robots.txt` hanya informasi.** Path di dalamnya adalah petunjuk, bukan temuan.
- **403 pada satu path bukan bukti aman** — coba path admin lain dan method lain sekali.
- **IDOR tidak boleh diuji pada data pengguna nyata.** Siapkan dua akun sendiri.
- **Denyut permintaan terlalu cepat memicu blokir IP** dan menghentikan seluruh sesi pengujian.
- **Hasil scanner pihak ketiga tidak boleh disalin.** Reproduksi manual atau buang.
- **Pengujian di produksi butuh jendela waktu dan pemberitahuan**, terutama untuk upload dan reset password.

## Output

```markdown
RINGKASAN EKSEKUTIF
Target        : https://contoh.com
Tanggal       : dd/mm/yyyy
Mode          : read-only / aktif-ringan / aktif-intrusif
Cakupan       : publik + terautentikasi (peran user); admin TIDAK diuji
Risiko total  : [Rendah/Sedang/Tinggi/Kritis]

TEMUAN PRIORITAS (CRITICAL/HIGH)
1. [Kritis] SQL injection pada parameter `id` di /product — akses database
2. [Tinggi] Berkas backup terekspos di /backup/db.sql (HTTP 200)

TEMUAN MEDIUM
- Cookie sesi tanpa HttpOnly (CWE-1004)
- Versi jQuery 1.12 rentan CVE-2019-11358

TEMUAN LOW/INFO
- `robots.txt` mengungkap path /admin
- `Server` membocorkan Apache/2.4.41

TIDAK TEREPRODUKSI
- Dugaan SSRF pada parameter `url` — respons identik untuk semua nilai

REKOMENDASI
1. Parameterized query pada semua akses database
2. HttpOnly + Secure + SameSite pada cookie sesi
3. Hapus berkas backup dari direktori publik
```

Setiap temuan harus dapat direproduksi dari laporan ini saja: URL, parameter, perintah, dan respons. Bila tidak, turunkan menjadi kandidat.

Untuk menyusunnya menjadi laporan PDF formal, lanjutkan ke skill `security-documentation`.
