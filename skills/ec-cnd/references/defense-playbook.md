---
name: "Defense Playbook — Siklus Kerja dan Change Management"
description: "Siklus kerja defender dari mengetahui aset hingga perbaikan berkelanjutan, dengan penekanan pada otorisasi, template permintaan perubahan, rollback, runbook operasional, dokumentasi, dan metrik yang mengubah keputusan."
tags: [playbook, lifecycle, change-management, rollback, runbook, authorization, documentation, metrics]
---

# Defense Playbook — Siklus Kerja dan Change Management

Pekerjaan defender bukan deretan alat, melainkan siklus yang berulang: **ketahui → ukur → desain → ubah → operasikan → respons → perbaiki**. Kegagalan paling umum bukan pada alat, melainkan pada lompatan dari "masalah" ke "konfigurasi" tanpa melewati desain dan otorisasi.

## 1. Ketahui

Sebelum kontrol apa pun:

- inventaris aset, pemilik, kritikalitas, dan data yang ditangani;
- topologi dan alur data (bukan hanya diagram lama);
- kewajiban (kontrak, regulasi, kebijakan internal);
- siapa yang berwenang menyetujui perubahan dan siapa yang menanggung dampak.

Tanpa ini, setiap keputusan kontrol adalah tebakan yang didandani sebagai keahlian.

## 2. Ukur

- baseline trafik, log, dan konfigurasi;
- skor kepatuhan baseline (CIS/STIG) bila ada;
- cakupan kontrol dan deteksi yang sebenarnya, bukan yang diasumsikan;
- waktu deteksi dan remediasi dari insiden/temuan terakhir.

Pengukuran harus **read-only** dan tidak mengganggu. Hasilnya disimpan sebagai pembanding, bukan laporan sekali pakai.

## 3. Desain

1. Rumuskan masalah dalam satu kalimat: "siapa bisa mencapai apa yang seharusnya tidak".
2. Daftar opsi kontrol di beberapa layer (data, aplikasi, host, jaringan).
3. Untuk tiap opsi: efektivitas, biaya, dampak ketersediaan, kompleksitas operasional.
4. Pilih kontrol termurah yang menutup akar masalah.
5. Tentukan cara membuktikan kontrol bekerja.

Desain yang baik menyebutkan apa yang **tidak** dikerjakan beserta alasannya.

## 4. Ubah

Setiap perubahan memerlukan:

| Field | Isi |
|---|---|
| Tujuan | masalah apa yang diselesaikan |
| Perubahan | perintah/konfigurasi spesifik |
| Blast radius | layanan dan pengguna yang bisa terdampak |
| Window | kapan, berapa lama, siapa yang siaga |
| Rollback | langkah pembatalan yang sudah diuji |
| Verifikasi | koneksi/alert/metrik yang membuktikan hasil |
| Persetujuan | siapa yang menyetujui, kapan |
| Pencabutan | kapan perubahan sementara berakhir |

Aturan: **satu variabel per window** bila memungkinkan. Perubahan bertumpuk menghapus kemampuan atribusi saat terjadi masalah.

## 5. Operasikan

- **Runbook** per alert/kontrol: pemicu, langkah triase, tindakan aman, kapan eskalasi, siapa pemilik.
- **Review berkala** aturan, akun, sertifikat, dan pengecualian.
- **Health check** sensor dan agen; kontrol yang mati diam-diam lebih berbahaya daripada tidak ada.
- **Dokumentasi** keputusan, bukan hanya konfigurasi.

## 6. Respons

- Kenali dan klasifikasikan; jangan menyimpulkan sebelum ada bukti.
- Preservasi bukti jaringan sebelum containment (lihat `incident-response.md`).
- Containment dengan blast radius terkecil; keputusan ketersediaan oleh pemilik layanan.
- Serah-terima dengan timeline, bukti, tindakan, hipotesis, dan pertanyaan terbuka.

## 7. Perbaiki

- Cari **kontrol yang gagal**, bukan hanya penyebab langsung.
- Perbarui deteksi, aturan, dan runbook berdasarkan pelajaran.
- Uji ulang asumsi (restore, failover, segmentasi).
- Catat perubahan pada register risiko dan metrik.

## 8. Otorisasi dan batas

Pekerjaan defensif tetap membutuhkan mandat:

- pemantauan jaringan dan penyimpanan pcap menyentuh privasi — pastikan kebijakan dan legal;
- pemindaian kerentanan harus dijadwalkan dan disetujui, terutama pada sistem pihak ketiga;
- perubahan pada perangkat pihak ketiga (vendor, penyedia) memerlukan koordinasi;
- uji penetrasi/internal simulation memerlukan scope tertulis, meski tujuannya defensif.

## 9. Dokumentasi minimum

1. Inventaris dan pemilik aset.
2. Peta zona dan aturan antar-zona.
3. Aturan firewall dengan pemilik dan tanggal review.
4. Sumber log, retensi, dan pemilik alert.
5. Runbook insiden utama.
6. Register risiko dan pengecualian.
7. Catatan perubahan (change log) dan hasil verifikasinya.

## 10. Metrik yang berguna

- persentase aset dengan baseline diterapkan;
- median waktu remediasi kerentanan kritis;
- rasio false positive dan waktu triase alert;
- cakupan deteksi terhadap teknik yang relevan;
- hasil uji restore/failover terakhir;
- jumlah pengecualian yang melewati tanggal review.

## 11. Kesalahan umum

1. **Langsung mengubah konfigurasi** tanpa desain dan otorisasi.
2. **Perubahan "sementara"** yang menjadi permanen tanpa review.
3. **Rollback ditulis saat insiden**, bukan sebelum perubahan.
4. **Dokumentasi setelah selesai** — detail hilang.
5. **Metrik aktivitas** (jumlah scan, jumlah alert) menggantikan metrik hasil.
6. **Tidak ada pemilik** untuk kontrol atau alert.
7. **Mengabaikan ketersediaan** sebagai bagian dari keputusan keamanan.

## Best Practices

- Mulai dari aset dan pemilik, bukan dari alat.
- Tulis perubahan sebelum mengeksekusi, termasuk rollback.
- Satu variabel per window; ukur sesudahnya.
- Beri setiap kontrol pemilik dan tanggal review.
- Ukur hasil, bukan aktivitas.
