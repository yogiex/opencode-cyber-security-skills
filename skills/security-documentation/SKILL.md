---
name: security-documentation
description: "Menyusun laporan pengujian keamanan yang dapat diaudit: struktur baku, template LaTeX siap pakai, tabel CVSS v3.1/CWE, dan bukti reproducible. Muat saat hasil pengujian harus menjadi laporan formal (PDF) untuk klien atau manajemen."
license: MIT
compatibility: opencode
metadata:
  audience: security-engineers
  workflow: reporting
---

# Security Documentation

Mengubah data pengujian menjadi laporan formal. Bagian tersulitnya bukan LaTeX — melainkan memutuskan apa yang layak masuk laporan, pada severity berapa, dan dengan bukti seperti apa.

## Decision Frame

- **Tanpa bukti, tanpa temuan.** Setiap temuan wajib punya langkah reproduksi; bila tidak mungkin dalam mode read-only, tulis persis itu sebagai keterbatasan, jangan menghaluskan.
- **CVSS mengikuti deklarasi, bukan kesan.** Tetapkan `PR`/`UI`/`S` berdasarkan kondisi nyata saat pengujian. Temuan yang butuh login tidak boleh memakai `PR:N`.
- **Severity konfigurasi tanpa rantai serangan = Low/Info.** Header hilang, banner versi, dan `robots.txt` tidak naik menjadi High hanya karena terlihat menakutkan.
- **Cantumkan yang tidak diuji.** Bagian berbasis autentikasi yang tidak tersedia harus disebut di cakupan, agar laporan tidak dibaca sebagai jaminan menyeluruh.
- **Satu halaman per temuan.** Bila lebih, biasanya dua temuan tercampur — pisahkan.
- **Redaksi sebelum kirim.** Token, cookie, dan PII diganti penanda; bukti mentah pindah ke lampiran terbatas.

## Struktur Laporan

Kerangka siap pakai: [assets/report-template.tex](assets/report-template.tex). Urutan bagian tidak diubah:

1. **Ringkasan Pengujian** — paragraf non-teknis: nomor tiket, tujuan, target, waktu, reverifikasi.
2. **Ringkasan Temuan Keamanan** — tabel jumlah per severity (CRITICAL/HIGH/MEDIUM/LOW/INFO) + total.
3. **Ringkasan Teknis** — waktu, cakupan poin uji, metode (OWASP WSTG/PTES, read-only vs aktif), temuan utama, rekomendasi utama.
4. **Detail Pengujian** — satu subbagian per temuan, urut dari severity tertinggi.
5. **Kesimpulan** — risiko akhir dan prioritas tindak lanjut.
6. **Lampiran** — role & scope mapping, endpoint API, struktur berkas, akun uji, daftar hash bukti.

## Anatomi Satu Temuan

| Bagian | Isi |
|---|---|
| Judul | Dampak + komponen, ≤ 12 kata |
| Tabel metadata | Severity badge, CVSS v3.1 + vektor, CWE, komponen |
| Deskripsi | 2–4 kalimat: apa yang terjadi, mengapa mungkin |
| Dampak bisnis | Konsekuensi bagi organisasi, bukan istilah teknis |
| Bukti | `curl` siap tempel + respons terpotong |
| Rekomendasi | Perbaikan akar masalah, bukan mitigasi sementara |

Detail lengkap, tabel vektor CVSS, pemetaan CWE, dan pola `curl` ada di [references/finding-writeup.md](references/finding-writeup.md).

## Konvensi LaTeX

- Packages: `graphicx`, `longtable`, `booktabs`, `listings`, `xcolor`, `hyperref`, `enumitem`, `fancyhdr`, `titlesec`, `caption`, `setspace`.
- Badge severity: `\riskcritical`, `\riskhigh`, `\riskmed`, `\risklow`, `\riskinfo` (didefinisikan di template).
- Label severity dalam bahasa Inggris: CRITICAL, HIGH, MEDIUM, LOW, INFO.
- Tabel temuan HIGH: grid `|p{}|p{}|` dengan `\hline`; MEDIUM/LOW/INFO: `longtable` berisi CVSS, CWE, dampak, rekomendasi.
- Compile: tiga kali `pdflatex` (`pdflatex -interaction=nonstopmode report.tex`).

## Konvensi PoC

- Gunakan `curl` siap copy-paste, bukan raw HTTP.
- Sertakan respons sebagai bukti, dipotong pada bagian yang relevan.
- Untuk injeksi, gunakan penanda unik (mis. `zzq7x1`) — bukan `alert(1)`.
- Bila tidak dapat direproduksi dalam mode read-only, tulis: **"PoC tidak dapat direproduksi dalam mode read-only"**, beserta alasannya.
- Screenshot memakai `\includegraphics` dengan path relatif `notes/`; anotasi bagian yang dibuktikan.

## CVSS dan CWE

- HIGH/CRITICAL: CVSS v3.1 base score + vektor + CWE.
- MEDIUM: CVSS + CWE.
- LOW/INFO: label severity cukup, CWE bila jelas.

CWE yang sering dipakai: CWE-89 (SQLi), CWE-79 (XSS), CWE-639 (IDOR), CWE-862 (otorisasi hilang), CWE-352 (CSRF), CWE-918 (SSRF), CWE-200 (informasi sensitif), CWE-1004 (cookie tanpa HttpOnly), CWE-942 (CORS permisif).

## Prioritas Rekomendasi

Hanya CRITICAL, HIGH, dan MEDIUM masuk ringkasan rekomendasi. LOW dan INFO tetap dicatat di detail, tetapi tidak mengambil ruang ringkasan.

## Kapan Digunakan

**Gunakan ketika:**
- Hasil pengujian harus menjadi laporan formal untuk klien, manajemen, atau audit.
- Dibutuhkan format baku (OWASP WSTG/PTES) dengan ringkasan non-teknis di depan.
- Setiap temuan perlu `curl` yang bisa diverifikasi reviewer.
- Bekerja dalam mode read-only (GET + analisis bundle statis).

**Jangan gunakan ketika:**
- Pengujian masih berjalan dan temuan belum stabil.
- Output yang dibutuhkan bukan PDF/LaTeX (DOCX, HTML, dashboard).
- Belum ada data temuan sama sekali.

## Alur Kerja

1. Salin [assets/report-template.tex](assets/report-template.tex) ke direktori kerja laporan.
2. Isi ringkasan pengujian dari tiket/permintaan — bukan dari ingatan.
3. Untuk setiap temuan, ikuti urutan di [references/finding-writeup.md](references/finding-writeup.md).
4. Compile tiga kali; periksa ToC, nomor halaman, dan tabel yang terpotong.
5. Redaksi token/PII; periksa ulang bagian "tidak diuji".
6. Simpan bukti mentah (HAR, respons, screenshot) di lampiran terpisah.

## Gotchas

- **`pdflatex` sekali jalan menghasilkan ToC kosong dan `??`.** Selalu tiga kali; `longtable` butuh dua pass untuk lebar kolom.
- **`longtable` tidak boleh berada di dalam `table`.** Kalau dibungkus float, tabel panjang terpotong tanpa pesan jelas.
- **Path `\includegraphics` relatif terhadap direktori kerja saat compile**, bukan lokasi `.tex`. Gunakan `\graphicspath` seperti di template.
- **Karakter unicode (`→`, `≠`, `–`) gagal pada `pdflatex`.** Pakai `xelatex`, atau ganti dengan padanan ASCII.
- **Screenshot tanpa anotasi tidak membuktikan apa pun.** Sorot baris respons atau elemen UI yang relevan.
- **CVSS 9.8 untuk temuan yang butuh login adalah kesalahan `PR`.** Bandingkan dengan vektor di referensi sebelum menulis skor.
- **Header keamanan yang hilang dilaporkan sebagai High akan dipertanyakan.** Tanpa rantai serangan, tempatnya Low/Info.
- **Laporan tanpa daftar "tidak diuji" dibaca sebagai jaminan seluruh aplikasi aman.**
- **Lampiran hash/endpoint kerap memuat token.** Periksa ulang sebelum berkas keluar dari tim.

## Referensi

| Berkas | Baca saat |
|---|---|
| [assets/report-template.tex](assets/report-template.tex) | Memulai laporan baru |
| [references/finding-writeup.md](references/finding-writeup.md) | Menulis satu temuan: CVSS, CWE, bukti, redaksi |
