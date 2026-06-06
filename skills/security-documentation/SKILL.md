---
name: security-documentation
description: Membuat laporan pengujian keamanan dalam format LaTeX dan mengompilasi ke PDF, mengikuti template docs/laporan.txt
license: MIT
compatibility: opencode
metadata:
  audience: security-engineers
  workflow: reporting
---

## What I do

Generate laporan pengujian keamanan dalam format LaTeX dan compile ke PDF, dengan struktur yang mengacu pada `docs/laporan.txt`:

### 1. Ringkasan Pengujian
Menulis paragraf naratif non-teknis berdasarkan tiket/incident/permintaan:
- Nomor tiket (jika ada), tujuan pengujian, target yang diuji (website/API/IP/aplikasi), waktu pengujian
- Informasi reverifikasi (nomor dokumen sebelumnya jika ada)
- Disajikan dalam bentuk paragraf atau tabel — bahasa non-teknis agar dipahami pemangku kepentingan

### 2. Ringkasan Temuan Keamanan
Tabel jumlah temuan keseluruhan per severity:
- CRITICAL / HIGH / MEDIUM / LOW / INFO
- Dilengkapi total keseluruhan

### 3. Ringkasan Teknis
Sub-bagian terstruktur:
- **Waktu Pengujian** — kapan pengujian dilaksanakan
- **Cakupan Poin Uji** — area/fitur/modul yang diuji
- **Metode Pengujian** — OWASP WSTG + PTES framework, pendekatan read-only (GET + static JS bundle analysis), tools yang digunakan
- **Temuan Utama** — highlight temuan paling kritis
- **Rekomendasi Utama** — diurutkan dari yang paling urgent, severity dalam bahasa Inggris

### 4. Detail Pengujian
Eksplorasi rinci per temuan:
- Setiap temuan mencakup: Severity table (badge visual), CVSS v3.1 base score, CWE, Deskripsi, Dampak bisnis
- **PoC reproducible** — `curl` command siap copy-paste, bukan raw HTTP
  - Jika tidak bisa direproduksi dalam mode read-only: tulis "PoC tidak dapat direproduksi dalam mode read-only"
- Screenshot bukti menggunakan `\includegraphics` dengan path relatif `notes/`
- Rekomendasi perbaikan

**Konvensi tabel:**
- Temuan HIGH: grid `|p{}|p{}|` dengan `\hline`
- Temuan MEDIUM/LOW/INFO: `longtable` berisi CVSS, CWE, Dampak, Rekomendasi

### 5. Kesimpulan
Ringkasan akhir risiko dan prioritas tindak lanjut.

### 6. Lampiran
- Role & Scope Mapping
- API Endpoint Mapping (150+ endpoint hash)
- Struktur file, akun testing, daftar hash

### LaTeX Conventions
- Packages: graphicx, longtable, booktabs, listings, xcolor, hyperref, enumitem, fancyhdr, titlesec, caption, setspace
- Severity badges: `\riskhigh`, `\riskmed`, `\risklow`, `\riskinfo` via `\colorbox`
- Severity labels: CRITICAL, HIGH, MEDIUM, LOW, INFO (English)
- Section numbering: `\thesection`, `\thesubsection`, `\thesubsubsection`
- Compile: 3-pass `pdflatex` untuk ToC

### CVSS Scoring Standards
- HIGH findings: CVSS v3.1 base score + CWE
- MEDIUM: CVSS + CWE
- LOW/INFO: cukup severity label
- CWE umum: CWE-862 (Missing Authorization), CWE-639 (IDOR), CWE-922 (Sensitive Data in Browser), CWE-200 (Information Exposure), CWE-352 (CSRF), CWE-693 (Missing Security Control)

### Prioritas Rekomendasi
Hanya untuk CRITICAL + HIGH + MEDIUM findings. LOW dan INFO tidak perlu rekomendasi di ringkasan.

## When to use me

**Gunakan ketika:**
- Perlu mendokumentasikan hasil pengujian keamanan web application dalam laporan formal
- Membutuhkan laporan dengan **format standar OWASP WSTG dan/atau PTES**: Ringkasan → Detail → Kesimpulan → Lampiran
- Hasil pengujian perlu dikomunikasikan ke **pemangku kepentingan non-teknis** (manajemen, klien) — ringkasan naratif di bagian depan
- Membutuhkan **PoC reproducible** — setiap temuan menyertakan `curl` command yang bisa diverifikasi reviewer
- Bekerja dalam **mode read-only** (GET-only, static bundle analysis tanpa POST/PUT/DELETE)
- Target menggunakan **arsitektur JWT** — skill menyertakan template analisis JWT structure dan localStorage exposure

**Jangan gunakan ketika:**
- Masih dalam fase eksploitasi aktif (POST/PUT/DELETE)
- Membutuhkan output format selain LaTeX (DOCX, HTML, dll)
- Belum ada data temuan yang terkumpul

## Struktur Laporan (Detail)

Template mengacu pada `docs/laporan.txt` dengan urutan:

1. **Ringkasan Pengujian** — paragraf naratif non-teknis
2. **Ringkasan Temuan Keamanan** — tabel jumlah per severity
3. **Ringkasan Teknis** — 1.2.1 Waktu, 1.2.2 Cakupan, 1.2.3 Metode, 1.2.4 Temuan, 1.2.5 Rekomendasi
4. **Detail Pengujian** — eksplorasi rinci + PoC + screenshot
5. **Kesimpulan**
6. **Lampiran** — Role Mapping, API Endpoints, Struktur File, Akun Testing, Daftar Hash

## PoC Writing Rules
- Gunakan `curl` command siap copy-paste (bukan raw HTTP)
- Sertakan response JSON sebagai bukti
- Jika tidak bisa di-repro dalam mode read-only, tulis: "PoC tidak dapat direproduksi dalam mode read-only"
- Screenshot: gunakan `\includegraphics` dengan path relatif `notes/`

## LaTeX Conventions
- Packages: graphicx, longtable, booktabs, listings, xcolor, hyperref, enumitem, fancyhdr, titlesec, caption, setspace
- Severity badges: \riskhigh, \riskmed, \risklow, \riskinfo via \colorbox
- Severity labels: CRITICAL, HIGH, MEDIUM, LOW, INFO (English)
- Section numbering: \thesection, \thesubsection, \thesubsubsection
- Tabel temuan HIGH: grid `|p{}|p{}|` dengan \hline
- Compile: 3 pass pdflatex untuk ToC

## CVSS Scoring Standards
- HIGH findings: CVSS v3.1 base score + CWE
- MEDIUM: CVSS + CWE
- LOW/INFO: severity label saja
- CWE umum: CWE-862, CWE-639, CWE-922, CWE-200, CWE-352, CWE-693

## Prioritas Rekomendasi
Hanya untuk CRITICAL + HIGH + MEDIUM findings. LOW dan INFO tidak perlu rekomendasi.
