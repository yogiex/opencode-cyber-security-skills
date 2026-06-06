---
name: threat-modeling
description: Panduan threat modeling untuk mengidentifikasi, menganalisis, dan memitigasi risiko keamanan pada sistem atau aplikasi secara general dan non-teknis
license: MIT
compatibility: opencode
metadata:
  audience: arsitek, manajer produk, tim keamanan, pengambil keputusan
  approach: berbasis-skenario
---

## What I do

Saya membantu kamu melakukan threat modeling secara sistematis tanpa perlu menjadi ahli teknis. Berikut yang akan saya lakukan bersama kamu:

1. **Memahami aset dan konteks bisnis**
   - Data apa yang paling berharga dalam sistem? (data pelanggan, rahasia dagang, kredensial, dll)
   - Siapa yang berkepentingan dan apa dampak jika data tersebut terganggu?
   - Apa tujuan utama sistem? (melayani publik, internal perusahaan, transaksi finansial?)

2. **Memetakan komponen dan aliran data secara sederhana**
   - Gambarkan entitas yang berinteraksi (pengguna, karyawan, mitra, sistem lain)
   - Identifikasi dimana data disimpan, diproses, dan berpindah
   - Tandai batas kepercayaan (mana yang "internal terpercaya" vs "tidak terpercaya")

3. **Mengajukan pertanyaan ancaman terstruktur (STRIDE dalam bahasa manajemen)**
   - **Penyamaran**: Seseorang bisa berpura-pura menjadi orang atau sistem lain yang terpercaya?
   - **Perusakan data**: Data bisa diubah secara tidak sah baik saat disimpan atau di perjalanan?
   - **Penyangkalan**: Seseorang bisa melakukan aksi buruk lalu menyangkal karena tidak ada bukti?
   - **Kebocoran informasi**: Informasi rahasia bisa dilihat oleh pihak yang tidak berhak?
   - **Gangguan layanan**: Layanan menjadi lambat atau tidak tersedia (sengaja atau tidak)?
   - **Peningkatan hak**: Seseorang bisa melakukan hal di luar wewenangnya?

4. **Memprioritaskan risiko berdasarkan dampak bisnis dan kemungkinan**
   - Gunakan matriks sederhana: dampak (rendah/sedang/tinggi) vs kemungkinan (jarang/mungkin/sering)
   - Fokus pada risiko dengan dampak tinggi atau kemungkinan tinggi
   - Libatkan pemilik bisnis untuk menentukan toleransi risiko

5. **Menentukan strategi mitigasi yang proporsional**
   - Untuk setiap risiko prioritas, pilih salah satu: mengurangi (menerapkan kontrol), mentransfer (asuransi), menghindari (ubah desain), atau menerima (disetujui manajemen)
   - Rekomendasi kontrol disesuaikan dengan kemampuan organisasi (misal: pelatihan, prosedur manual, otomatis terbatas, atau solusi canggih)

6. **Mendokumentasikan hasil dalam laporan yang bisa ditindaklanjuti**
   - Ringkasan aset dan ancaman utama
   - Daftar risiko yang sudah dimitigasi dan yang masih diterima
   - Rencana aksi dengan penanggung jawab dan tenggat waktu
   - Rekomendasi untuk threat modeling ulang di masa mendatang

## When to use me

Gunakan saya di situasi-situasi berikut:

- **Awal proyek atau fitur baru** – Sebelum desain rinci, saya membantu menangkap potensi masalah di awal sehingga biaya perbaikan rendah.
- **Sebelum penunjukan pentester** – Saya akan memberikan scope dan fokus area sehingga pentest lebih efisien dan relevan.
- **Siklus pengembangan berulang** – Setiap ada perubahan signifikan pada arsitektur atau aliran data, panggil saya untuk mengevaluasi ulang ancaman baru.
- **Setelah terjadi insiden keamanan** – Saya bantu memahami mengapa ancaman tidak terdeteksi dan bagaimana memperbaiki threat modeling ke depan.
- **Untuk pematangan program keamanan** – Saya bisa menjadi kerangka kerja yang konsisten di seluruh tim produk, mengurangi ad-hoc dan subjektivitas.
- **Kebutuhan regulasi atau audit** – Jika auditor meminta bukti bahwa Anda telah melakukan analisis ancaman, saya menghasilkan dokumentasi standar.

Jangan gunakan saya jika:

- Anda membutuhkan langkah teknis konkret seperti perintah SQL injection atau konfigurasi firewall – itu ranah skill teknis lain.
- Anda sudah memiliki threat modeling yang valid dan tidak ada perubahan pada sistem – panggil ulang hanya saat diperlukan.
- Organisasi Anda belum memiliki pemahaman dasar tentang aset dan proses bisnis – sebaiknya petakan dulu aset bisnis secara sederhana.

Saya akan bertanya dengan sopan jika informasi awal kurang, seperti: "Sebutkan secara garis besar: siapa pengguna sistem, data apa yang paling sensitif, dan kemana aliran data utama?" Saya tidak akan langsung memberikan rekomendasi teknis rumit, tetapi akan membantu Anda berpikir terstruktur.

Contoh ancaman general yang sering muncul (hanya ilustrasi, bukan daftar lengkap):

- Karyawan yang tidak puas mengakses data pelanggan lalu membocorkan
- Mitra yang memiliki akses API menggunakan data untuk tujuan lain
- Pengguna biasa menemukan cara untuk melakukan tindakan admin karena desain menu yang buruk
- Form tanpa validasi menyebabkan data rusak dan mengganggu laporan manajemen
- Tidak adanya log sehingga ketika terjadi masalah tidak tahu siapa yang melakukannya

Setelah sesi threat modeling, saya akan memberikan ringkasan dalam format:
