---
name: "Application and Data Protection — Kontrol Aplikasi dan Data"
description: "Proteksi aplikasi dan data dari sisi defender: application control, patch dan WAF lifecycle, klasifikasi dan kontrol akses data, enkripsi at-rest dan in-transit, DLP, backup yang teruji, serta retensi dan pemusnahan data."
tags: [application-control, applocker, wdac, patch, waf, encryption, tls, dlp, backup, retention, data-protection]
---

# Application and Data Protection — Kontrol Aplikasi dan Data

Data adalah yang akhirnya dicuri, diubah, atau dihapus. Kontrol di layer ini menjawab: aplikasi apa yang boleh berjalan, data siapa boleh dibaca, dan bagaimana data dipulihkan setelah insiden.

## 1. Application control

| Pendekatan | Kegunaan | Batas |
|---|---|---|
| Allowlist (AppLocker/WDAC) | mencegah eksekusi biner tak dikenal | butuh inventaris aplikasi dan proses persetujuan |
| Blocklist | cepat, reaktif | selalu tertinggal dari varian baru |
| Sandboxing | membatasi dampak aplikasi berisiko | tidak semua aplikasi kompatibel |
| Patch management | menutup kerentanan yang diketahui | butuh uji dan jadwal |

Allowlist adalah kontrol paling kuat, tetapi paling mahal secara operasional. Mulai dari server dan workstation kritikal, bukan seluruh armada sekaligus.

## 2. Patch dan virtual patching

- **SLA berdasarkan eksposur**: internet-facing dan kerentanan yang dieksploitasi aktif lebih dulu.
- **Uji di ring** sebelum produksi; catat pengecualian dan tanggal review.
- **Virtual patching** (WAF/IPS signature) adalah kompensasi sementara, bukan pengganti patch.
- **Ketahui versi yang benar-benar berjalan**, bukan versi yang tercatat di CMDB.

## 3. WAF lifecycle

1. **Mode monitor** — pelajari trafik normal dan false positive.
2. **Rule set dasar** — OWASP CRS atau vendor, sesuai jenis aplikasi.
3. **Pengecualian sempit** — per endpoint/parameter, bukan mematikan rule.
4. **Mode blocking** untuk rule yang sudah stabil.
5. **Review berkala** — pengecualian kedaluwarsa, rule baru, perubahan aplikasi.
6. **Logging** — request yang diblokir harus bisa dikorelasikan ke aplikasi dan pengguna.

WAF tidak memperbaiki kode. Bila temuan berulang di endpoint yang sama, eskalasi ke tim aplikasi.

## 4. Klasifikasi dan kontrol akses data

- **Klasifikasi** (publik, internal, rahasia, sangat rahasia) menentukan kontrol, retensi, dan enkripsi.
- **Akses berbasis peran**, bukan berbasis tim atau "karena dulu begitu".
- **Review akses berkala** untuk data sensitif; cabut akses yang tidak lagi dibutuhkan.
- **Least privilege** pada akun aplikasi dan basis data; hindari akun `sa`/`root` untuk aplikasi.

## 5. Enkripsi at-rest

- Disk encryption (BitLocker/LUKS) untuk endpoint dan server.
- Enkripsi kolom atau tablespace untuk data sangat sensitif.
- **Manajemen kunci** sama pentingnya dengan enkripsi: rotasi, pemisahan tugas, backup kunci.
- Backup juga harus terenkripsi; kunci tidak boleh disimpan bersama backup.

## 6. Enkripsi in-transit

- TLS 1.2 minimum, TLS 1.3 bila didukung; matikan protokol dan cipher lemah.
- **Siklus sertifikat**: inventaris, masa berlaku, otomasi perpanjangan, pemantauan kedaluwarsa.
- **mTLS** untuk komunikasi service-to-service yang sensitif.
- Enkripsi internal jangan diasumsikan; "jaringan internal" bukan alasan untuk plaintext.
- Verifikasi konfigurasi dengan pengujian eksternal, bukan hanya konfigurasi yang diharapkan.

## 7. Data masking dan tokenization

- Masking untuk lingkungan non-produksi dan tampilan yang tidak membutuhkan data penuh.
- Tokenization untuk data kartu/pribadi yang tidak perlu disimpan mentah.
- Pastikan masking tidak bisa dibalik dari data lain yang tersedia.

## 8. DLP

- **Kebijakan berbasis klasifikasi**, bukan sekadar pola regex.
- **Kanal** yang dipantau: email, web upload, endpoint (USB), cloud storage.
- **Tuning** untuk mengurangi false positive; blokir hanya untuk data yang jelas sensitif.
- **Privasi dan hukum** — pemantauan karyawan punya batas; koordinasikan dengan legal/HR.

## 9. Backup dan pemulihan

| Prinsip | Praktik |
|---|---|
| 3-2-1 | tiga salinan, dua media, satu di lokasi berbeda |
| Immutable | snapshot/object lock agar tidak bisa dienkripsi ransomware |
| Terpisah | backup tidak memakai kredensial yang sama dengan produksi |
| Teruji | restore test berkala dengan waktu tercatat |
| Terdokumentasi | RTO/RPO disepakati pemilik layanan |

Backup yang belum pernah direstore adalah asumsi, bukan kontrol.

## 10. Retensi dan pemusnahan

- Retensi mengikuti kebijakan dan kewajiban hukum; jangan menyimpan "selamanya karena murah".
- Pemusnahan harus dapat dibuktikan: wipe bersertifikat, crypto-shredding untuk media terenkripsi.
- Hapus data dari backup sesuai jadwal; retensi backup sering menjadi celah kepatuhan.

## Best Practices

- Mulai dari klasifikasi data; kontrol mengikuti nilai dan kewajiban.
- Virtual patching selalu punya tanggal berakhir.
- Uji restore, bukan hanya status backup.
- Kelola sertifikat dan kunci sebagai inventaris, bukan kejutan.
- DLP dan pemantauan harus disepakati dengan legal, bukan dipasang diam-diam.
