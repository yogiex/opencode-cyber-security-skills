---
name: "Engagement Playbook — White-Box Assessment & Laporan Klien"
description: "Disiplin engagement white-box web assessment: scope dan otorisasi, penanganan source code klien, pengambilan bukti, kriteria berhenti, struktur laporan klien (ringkasan, lokasi kode, PoC, remediasi, retest), dan redaksi data."
tags: [engagement, reporting, scope, authorization, evidence, remediation, retest, white-box, client-deliverable]
---

# Engagement Playbook — White-Box Assessment & Laporan Klien

White-box assessment menghasilkan dua hal yang harus dipertanggungjawabkan: **bukti** bahwa aplikasi bisa dieksploitasi, dan **laporan** yang membuat developer bisa memperbaikinya. Keduanya disiapkan selama engagement, bukan setelahnya.

## 1. Scope dan otorisasi

Sebelum menyentuh apa pun:

- Aset mana yang masuk scope: repo/arsip source, lingkungan (staging atau produksi), endpoint, dan akun uji.
- Apakah source code boleh disalin keluar lingkungan klien; di mana hasil review disimpan.
- Aksi yang dilarang: DoS, penghapusan data, upload persisten, perubahan konfigurasi, aksi di luar jam.
- Window kerja, kontak darurat, dan siapa yang berwenang menyetujui aksi write.
- Format deliverable, bahasa, dan penerima laporan.

Tanpa butir di atas tertulis, pekerjaan belum boleh dimulai. Aksi destructive butuh persetujuan eksplisit per aksi, bukan persetujuan umum di awal kontrak.

## 2. Bukti

Bukti yang berguna menjawab tiga pertanyaan: **apa** yang dikirim, **apa** yang terjadi, dan **di mana** penyebabnya di kode.

| Jenis bukti | Bentuk yang disimpan |
|---|---|
| Request/response | Salinan mentah dari Burp Repeater atau output `requests`, dengan host dan waktu |
| Lokasi kode | `file:line` dan potongan fungsi yang bertanggung jawab |
| Eksekusi | Output perintah, isi berkas yang hanya bisa dibaca identitas istimewa |
| Reproduksi | Perintah persis, dependensi, dan versi target |
| Riwayat | Catatan perubahan state target selama engagement |

Aturan praktis: bukti diambil **saat akses masih hidup**. Sesi, token, dan state sering tidak bisa dibuat ulang setelah target di-restart atau patch.

## 3. Kapan berhenti

- Objective tercapai dan bukti sudah lengkap → hentikan eksploitasi, mulai kunci bukti.
- Nilai marginal temuan berikutnya lebih kecil daripada risiko noise, downtime, atau perubahan state.
- Otorisasi habis (window, aksi, atau aset) → berhenti dan lapor, bukan "sekalian".
- Target menunjukkan tanda tidak stabil (error 500 berulang, layanan turun) → hentikan dan hubungi pemilik sistem.

Berhenti lebih awal dengan bukti lengkap lebih berguna daripada satu temuan tambahan dengan aplikasi yang tidak bisa dipulihkan.

## 4. Menulis sambil menguji

Tulis temuan saat masih di depan kode yang bersangkutan. Alasan:

- konteks (mengapa filter gagal, mengapa rantai bisa nyambung) hilang setelah berpindah target;
- bukti yang belum ditulis sering tidak sempat diambil ulang;
- laporan yang ditulis di akhir cenderung berisi klaim tanpa potongan kode.

Pola yang saya pakai: setiap rantai punya satu catatan berisi lokasi kode, request pembuktian, output, dampak, dan usulan perbaikan. Catatan itu yang dirapikan menjadi laporan.

## 5. Struktur laporan klien

Laporan white-box bukan daftar kerentanan; ia peta rantai dan perbaikannya.

```markdown
## Ringkasan Eksekutif
- Apa yang diuji, kapan, dan atas otorisasi siapa
- Dampak utama dalam bahasa risiko bisnis (bukan istilah exploit)

## Scope dan Metode
- Aset, source code, lingkungan, akun uji
- Pendekatan: source review → verifikasi manual → exploit

## Temuan
### <Nama temuan> — <dampak satu kalimat>
- **Lokasi**: <file:line>
- **Akar masalah**: <mengapa kode ini salah>
- **Rantai**: <langkah 1 → langkah 2 → dampak>
- **Proof of concept**: <request/response, perintah, output>
- **Dampak**: <apa yang bisa dicapai, data apa yang terpapar>
- **Remediasi**: <perbaikan di akar masalah>
- **Retest**: <langkah yang membuktikan perbaikan berhasil>

## Lampiran
- Artefak exploit, daftar endpoint yang diperiksa, catatan redaksi
```

## 6. Remediasi dan retest

- Perbaikan di akar masalah: parameterized query, serializer yang aman, validasi tipe, allowlist sink, penghapusan kunci hardcoded.
- WAF dan filter darurat dicatat sebagai **mitigasi sementara** dengan tanggal pencabutan, bukan sebagai perbaikan.
- Temuan yang tidak bisa diperbaiki segera harus punya kompensasi yang bisa diuji.
- Retest memakai langkah yang sama dengan uji awal; kalau langkahnya berubah, hasilnya tidak sebanding.

## 7. Redaksi dan penanganan data

- Jangan menyalin kredensial, token, atau data pelanggan ke laporan; ganti dengan placeholder dan sebutkan jenisnya.
- Potongan source code yang dikutip dibatasi pada baris yang relevan.
- Simpan artefak di kanal yang disepakati; hapus salinan lokal setelah serah-terima.
- Sebutkan artefak yang ditinggalkan di target dan status pembersihannya.

## 8. Best Practices

- Konfirmasi scope dan kontak sebelum hari pertama, bukan saat insiden pertama.
- Perlakukan source code klien sebagai rahasia setingkat data produksi.
- Setiap temuan harus bisa dijelaskan tanpa jargon exploit kepada developer yang akan memperbaikinya.
- Sertakan apa yang **tidak** ditemukan dan area yang tidak diuji — batas kepercayaan laporan.
- Tutup engagement dengan retest atau kesepakatan tertulis bahwa retest terpisah.

## 9. Rujukan

- [PTES](../../ptes-standard/SKILL.md) — fase engagement dan pelaporan.
- [security-documentation](../../security-documentation/SKILL.md) — standar penulisan dokumen keamanan.
