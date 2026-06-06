---
name: incident-response-plan
description: Panduan incident response non-teknis untuk organisasi: persiapan, deteksi, analisis, containment, eradikasi, recovery, dan pembelajaran. Cocok untuk tim manajemen, legal, PR, dan koordinator insiden.
license: MIT
compatibility: opencode
---

# Incident Response Plan (Non-Teknis)

Gunakan sebagai kerangka kerja untuk menangani insiden keamanan informasi dari sisi proses, komunikasi, dan bisnis. Tidak berisi langkah teknis (seperti perintah terminal), tetapi berfokus pada alur keputusan dan koordinasi.

## 1. Persiapan (Sebelum Insiden)

- Bentuk tim IR: manajer insiden, komunikasi (PR/legal), teknis (1 orang koordinator), HR jika terkait.
- Buat daftar kontak darurat (telepon, Signal, WhatsApp) – jangan hanya email.
- Siapkan template komunikasi internal dan eksternal.
- Tentukan tools komunikasi aman (misal: matrix, signal group, slack channel khusus).
- Lakukan simulasi sederhana setiap 6 bulan.

## 2. Deteksi & Pelaporan (Menemukan Insiden)

- Siapa yang bisa melapor? (karyawan, pelanggan, sistem otomatis)
- Saluran pelaporan: email khusus `incident@`, hotline internal, atau form.
- Informasi minimal yang harus dikumpulkan:
  - Waktu kejadian (perkiraan)
  - Gejala (lambat, tidak bisa akses, pesan aneh, file hilang)
  - Dampak yang terlihat (sistem mana, berapa orang terdampak)
- Klasifikasi awal: rendah, sedang, tinggi, kritis.

## 3. Analisis & Konfirmasi (Memahami Insiden)

- Tim IR mengumpulkan fakta (tanpa asumsi).
- Verifikasi apakah benar insiden atau false positive.
- Tentukan jenis insiden:
  - Ransomware / malware
  - Phishing / akun dicuri
  - Penyalahgunaan akses internal
  - Kebocoran data
  - DDoS atau gangguan layanan
- Tentukan ruang lingkup: satu sistem, satu departemen, seluruh perusahaan.

## 4. Containment (Menghentikan Perambatan)

- Tujuan: mencegah kerusakan lebih lanjut.
- Tindakan non-teknis yang bisa diputuskan oleh manajemen:
  - Isolasi bagian jaringan (instruksikan tim teknis)
  - Matikan akses remote sementara
  - Nonaktifkan akun yang dicurigai
  - Cabut kabel LAN jika diperlukan (instruksi ke orang di lapangan)
- Keputusan: lanjutkan bisnis secara manual atau stop layanan.

## 5. Eradikasi (Menghilangkan Penyebab)

- Pimpin rapat koordinasi dengan tim teknis untuk menentukan:
  - Apakah penyebab sudah ditemukan (malware, backdoor, celah konfigurasi)?
  - Tindakan perbaikan apa yang diperlukan (patch, ganti password, hapus akun jahat)?
- Jangan terburu-buru pulihkan sebelum penyebab dihilangkan.
- Dokumentasikan semua perintah yang dijalankan.

## 6. Recovery (Kembali Normal)

- Koordinasikan pemulihan sistem dari backup yang bersih.
- Prioritaskan: sistem paling kritis dulu (email, keuangan, CRM).
- Komunikasikan jadwal pemulihan ke internal dan pelanggan.
- Lakukan verifikasi bahwa sistem sudah bersih sebelum koneksi penuh.

## 7. Komunikasi Sepanjang Insiden

### Internal:

- Kabari tim manajemen setiap jam/kritis.
- Jaga staf yang tidak terkait agar tetap tenang (jangan spekulasi).

### Eksternal:

- Jika data pelanggan terdampak, konsultasikan dengan legal untuk kewajiban notifikasi.
- Siapkan pernyataan publik singkat yang jujur namun tidak membocorkan detail teknis.
- Jangan beri komentar tanpa persetujuan legal/PR.

## 8. Pembelajaran (Post-Incident)

- Selambat-lambatnya 2 minggu setelah insiden selesai, adakan rapat post-mortem.
- Bahas:
  - Apa yang berjalan baik?
  - Apa yang tidak berjalan baik?
  - Mengapa insiden bisa terjadi? (akar masalah)
  - Perbaikan proses atau training apa yang diperlukan?
- Buat laporan ringkas untuk manajemen (tanpa menyalahkan individu).
- Perbarui plan IR berdasarkan pengalaman.

## Template Laporan Singkat untuk Manajemen
