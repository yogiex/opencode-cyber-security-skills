---
name: "Anatomi Penulisan Temuan"
description: "Standar menulis satu temuan: urutan bagian, pemilihan vektor CVSS v3.1, pemetaan CWE, pola curl reproducible, standar bukti, redaksi data sensitif, dan anti-pola yang paling sering merusak laporan."
tags: [reporting, finding, cvss, cwe, poc, evidence, redaction, latex]
---

# Anatomi Penulisan Temuan

Satu temuan ditulis untuk dua pembaca sekaligus: pengambil keputusan yang butuh risiko dalam bahasa bisnis, dan engineer yang butuh mereproduksi bukti. Struktur di bawah memenuhi keduanya tanpa mengulang isi.

## Urutan Bagian (wajib, jangan diacak)

| # | Bagian | Isi | Panjang |
|---|---|---|---|
| 1 | Judul | Dampak + komponen, bukan nama kerentanan saja | ≤ 12 kata |
| 2 | Tabel metadata | Severity, CVSS, CWE, komponen, status | 4–5 baris |
| 3 | Deskripsi | Apa yang terjadi dan mengapa mungkin | 2–4 kalimat |
| 4 | Dampak bisnis | Konsekuensi bagi organisasi | 1–3 kalimat |
| 5 | Bukti | `curl` + respons yang dipotong | blok kode |
| 6 | Rekomendasi | Perbaikan spesifik | 1–3 butir |
| 7 | Referensi | CWE/OWASP/CVE | opsional |

Judul yang baik: "IDOR pada `/api/v1/users/{id}` membocorkan data pengguna lain". Judul yang buruk: "IDOR ditemukan". Pembaca harus memahami risikonya tanpa membuka bagian isi.

## Severity dan CVSS

Severity bukan sinonim skor CVSS. CVSS mengukur **dampak teknis dengan asumsi yang Anda deklarasikan** (misalnya `PR:N` = tanpa login). Deklarasi yang salah adalah sumber inflasi paling umum.

| Kasus | Vektor contoh | Skor | Catatan |
|---|---|---|---|
| SQLi tanpa autentikasi | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | 9.8 | PR:N harus benar-benar tanpa login |
| RCE/injeksi setelah login | `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` | 8.8 | Sering dilaporkan 9.8 secara keliru |
| Baca data pengguna lain (IDOR) | `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` | 6.5 | Hanya kerahasiaan |
| Reflected XSS | `AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N` | 6.1 | `S:C` karena dampak lintas komponen |
| Kebocoran info tanpa login | `AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` | 5.3 | Info yang tidak sensitif tetap 5.3 |
| Endpoint tanpa login mengembalikan PII | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` | 7.5 | Naik karena C:H |

Skor di atas adalah titik awal yang lazim. **Hitung ulang dengan kalkulator CVSS resmi** setiap kali vektor berubah, dan tulis vektornya di samping skor agar dapat diaudit.

Aturan yang menyelamatkan kredibilitas:

- `PR:N` hanya bila tidak butuh kredensial apa pun — termasuk akun gratis yang bisa didaftarkan sendiri.
- `UI:R` bila korban harus mengklik/menempel sesuatu.
- `S:C` hanya bila dampak keluar dari komponen yang rentan (XSS, SSRF ke jaringan internal).
- Temuan konfigurasi tanpa rantai serangan (header hilang, banner versi) umumnya **Low/Info**, bukan High.
- Jangan menaikkan severity karena "klien butuh perhatian". Turunkan ke tingkat yang benar, lalu jelaskan risikonya.

## Pemetaan CWE

| Temuan | CWE |
|---|---|
| SQL injection | CWE-89 |
| Cross-site scripting | CWE-79 |
| IDOR / akses objek tanpa otorisasi | CWE-639 |
| Otorisasi hilang pada fungsi | CWE-862 |
| CSRF | CWE-352 |
| SSRF | CWE-918 |
| Path traversal / LFI | CWE-22 |
| XXE | CWE-611 |
| Unrestricted file upload | CWE-434 |
| Open redirect | CWE-601 |
| CORS permisif | CWE-942 |
| Cookie tanpa HttpOnly | CWE-1004 |
| Cookie tanpa Secure | CWE-614 |
| SameSite tidak diset | CWE-1275 |
| Informasi sensitif terekspos | CWE-200 |
| Kontrol keamanan hilang | CWE-693 |

Satu temuan satu CWE utama; CWE tambahan boleh disebut di deskripsi, bukan di tabel metadata.

## Bukti Reproducible

Bukti minimum: perintah yang dapat dijalankan ulang, respons yang membuktikan klaim, dan penanda unik bila menyangkut injeksi.

```bash
# IDOR: bandingkan dua akun milik sendiri
curl -s -H "Authorization: Bearer $TOKEN_A" https://target.tld/api/v1/users/1042
curl -s -H "Authorization: Bearer $TOKEN_B" https://target.tld/api/v1/users/1042

# Reflected XSS: penanda unik, bukan alert(1)
curl -s 'https://target.tld/search?q=zzq7x1%3Cb%3E' | grep -o 'zzq7x1<b>'

# Header keamanan
curl -sI https://target.tld/ | grep -iE 'content-security-policy|strict-transport|x-frame|x-content-type'

# File sensitif terekspos
curl -s -o /dev/null -w '%{http_code}\n' https://target.tld/.git/HEAD
curl -s -o /dev/null -w '%{http_code}\n' https://target.tld/backup/db.sql
```

| Klaim | Bukti yang cukup | Bukti yang tidak cukup |
|---|---|---|
| XSS | Penanda direfleksikan tanpa encoding + konteks HTML | `alert(1)` muncul di browser pribadi |
| IDOR | Respons berisi data akun lain + dua token berbeda | ID berubah dan halaman tidak error |
| File terekspos | Status 200 + beberapa byte isi berkas | Status 200 saja (bisa SPA fallback) |
| Header hilang | Output `curl -I` | Screenshot browser tanpa header |
| Akses admin | Respons 200 dengan fungsi admin | Status 403 di satu path |

Bila tidak dapat direproduksi dalam mode read-only, tulis persis: **"PoC tidak dapat direproduksi dalam mode read-only"**, sertakan alasan dan bukti pendukung (kode klien, respons parsial). Jangan mengarang langkah.

## Redaksi

Laporan keluar dari tim dan dibaca orang lain. Sebelum dikirim:

- Ganti nilai token/cookie menjadi `REDACTED` atau `eyJ…<dipotong>`.
- Sembunyikan PII: email, NIK, nomor telepon, alamat. Cukup tunjukkan bentuknya.
- Jangan sertakan hash password utuh atau salt.
- Simpan bukti mentah di lampiran terpisah dengan akses terbatas, bukan di badan laporan.

## Anti-Pola

| Anti-pola | Kenapa merusak | Perbaikan |
|---|---|---|
| "Ditemukan XSS" tanpa konteks | Tidak dapat direproduksi | Sertakan URL, parameter, penanda, respons |
| Severity dinaikkan agar diperhatikan | Kredibilitas hilang saat diverifikasi | Turunkan + jelaskan dampak nyata |
| Rekomendasi "gunakan WAF" | Memindahkan masalah, bukan memperbaiki | Perbaiki akar (parameterized query, encoding) |
| Menyalin keluaran scanner | False positive ikut, bukti nol | Reproduksi manual, buang yang tidak terbukti |
| Semua temuan ditulis sepanjang sama | Pembaca kehilangan prioritas | Ringkasan 1 halaman + detail bertingkat |
| Laporan tanpa daftar "tidak diuji" | Membuat kesan seluruh aplikasi aman | Cantumkan batas cakupan |

## Panjang

- Ringkasan eksekutif: **≤ 1 halaman**.
- Satu temuan: **≤ 1 halaman** (tabel + 2 paragraf + bukti).
- Lampiran: data mentah (endpoint, hash, akun uji), boleh panjang.

Bila satu temuan butuh lebih dari satu halaman, biasanya ada dua temuan yang dicampur — pisahkan.
