---
name: "Risk and Threat Intelligence — Prioritisasi Pertahanan"
description: "Menghubungkan kerja teknis ke risiko: risk register praktis, siklus vulnerability management dan prioritas berbasis eksploitasi, attack surface management, konsumsi cyber threat intelligence, threat hunting, penilaian dampak privasi, dan metrik pertahanan."
tags: [risk, vulnerability-management, epss, kev, attack-surface, cti, ioc, ioa, threat-hunting, pia, metrics]
---

# Risk and Threat Intelligence — Prioritisasi Pertahanan

Defender tidak bisa mengerjakan semua hal. Nilai utamanya adalah **mengurutkan**: risiko mana yang paling mungkin, paling mahal, dan paling murah ditutup — lalu mengukur apakah keputusan itu bekerja.

## 1. Risk register praktis

| Kolom | Isi |
|---|---|
| Aset | apa yang berisiko, siapa pemiliknya |
| Ancaman | siapa/apa yang bisa memanfaatkan |
| Kerentanan | kelemahan spesifik (konfigurasi, patch, desain) |
| Kemungkinan | rendah/sedang/tinggi, dengan alasan |
| Dampak | ketersediaan, integritas, kerahasiaan, kepatuhan |
| Kontrol | yang sudah ada dan yang diusulkan |
| Pemilik risiko | siapa yang menerima sisa risiko |
| Tanggal review | kapan dievaluasi ulang |

Register yang tidak pernah dibaca adalah dokumen, bukan kontrol.

## 2. Perlakuan risiko

- **Mitigasi** — kontrol teknis atau proses.
- **Transfer** — asuransi, kontrak, penyedia.
- **Hindari** — hentikan layanan/proses.
- **Terima** — dengan persetujuan eksplisit dan tanggal review.

Penerimaan risiko tanpa pemilik dan tanpa tanggal adalah kelalaian yang didokumentasikan.

## 3. Vulnerability management

1. **Inventaris** — Anda tidak bisa memindai yang tidak diketahui.
2. **Deteksi** — scanner, advisory vendor, temuan pentest, bug bounty.
3. **Prioritas** — jangan hanya CVSS. Gabungkan eksploitasi nyata (CISA KEV), probabilitas (EPSS), eksposur (internet-facing?), dan nilai aset.
4. **Remediasi** dengan SLA berdasarkan prioritas.
5. **Verifikasi** — temuan benar-benar tertutup, bukan sekadar tiket ditutup.
6. **Pengecualian** — alasan, kompensasi, pemilik, tanggal review.

Scanner yang dijalankan tanpa proses remediasi hanya menghasilkan laporan.

## 4. Attack surface management

- **Eksternal**: domain, subdomain, sertifikat, port terbuka, layanan yang tidak diinventaris.
- **Internal**: host dengan layanan manajemen terbuka, share, akun default.
- **IoE (Indicator of Exposure)** — sinyal yang menunjukkan eksposur, bukan kompromi.
- **Simulasi serangan** terkontrol untuk memvalidasi kontrol, bukan untuk mencari sensasi.
- **Kurangi** permukaan: matikan layanan tidak perlu, batasi akses, hapus aset bayangan.

## 5. CTI yang bisa dipakai

| Jenis | Kegunaan defender |
|---|---|
| IoC (hash, IP, domain) | deteksi cepat, blocking sementara |
| IoA (perilaku) | deteksi yang lebih tahan perubahan |
| Laporan taktis | konteks kampanye dan TTP |
| Laporan strategis | prioritas manajemen dan investasi |

Aturan konsumsi:

- **Sumber tepercaya** dan beragam; jangan bergantung pada satu feed.
- **Kualitas di atas kuantitas**; IoC usang menghasilkan false positive.
- **Kadaluarsa** — IOC harus punya masa berlaku dan review.
- **TLP** dihormati saat berbagi.
- **Aksi** — TI yang tidak mengubah kontrol atau deteksi tidak memberi nilai.

Untuk lifecycle CTI mendalam, gunakan `threat-intelligence`; untuk struktur ATT&CK, gunakan `mitre-attack`.

## 6. Threat hunting

- **Hipotesis** dari ATT&CK, TI terkini, atau anomali baseline.
- **Data yang dibutuhkan** dicek dulu; hunting tanpa telemetri adalah spekulasi.
- **Hasil** bisa berupa deteksi baru, kontrol baru, atau hipotesis yang gugur — semuanya berguna.
- **Dokumentasikan** query, temuan, dan keputusan.
- Hunting bukan pengganti deteksi otomatis; ia mengisi lubang yang belum diketahui.

## 7. Privasi dan PIA

- Pemantauan jaringan dan log menyentuh data pribadi; lakukan **Privacy Impact Assessment** untuk sistem baru.
- Minimalkan data, batasi akses, tetapkan retensi.
- Koordinasikan dengan legal/HR sebelum memantau pengguna secara luas.
- Enkripsi dan redaksi data sensitif dalam log/pcap.

## 8. Metrik

| Metrik | Arti |
|---|---|
| Coverage kontrol | persentase aset dengan kontrol wajib |
| Waktu remediasi | median waktu dari deteksi ke perbaikan |
| Rasio false positive | kualitas alert |
| MTTD/MTTR | kecepatan deteksi dan respons |
| Tren risiko | register yang bergerak, bukan statis |
| Uji restore | bukti pemulihan, bukan asumsi |

Metrik dipakai untuk memutuskan, bukan untuk dipamerkan. Metrik yang tidak mengubah keputusan sebaiknya dihapus.

## 9. Kesalahan umum

1. **Prioritas berdasarkan CVSS saja.**
2. **Memindai tanpa kewenangan** atau di luar jadwal yang disepakati.
3. **Menumpuk feed TI** tanpa kapasitas analisis.
4. **Register risiko** yang tidak punya pemilik.
5. **Hunting tanpa hipotesis** — hanya menjelajah log.
6. **Mengukur jumlah temuan**, bukan penurunan risiko.
7. **Pengecualian patch** yang diperpanjang tanpa review.

## Best Practices

- Urutkan berdasarkan eksploitasi nyata dan eksposur, bukan skor mentah.
- Setiap risiko punya pemilik dan tanggal review.
- Konsumsi TI yang bisa ditindaklanjuti; buang yang tidak.
- Ukur hasil, bukan aktivitas.
- Libatkan legal sejak awal untuk pemantauan dan data pribadi.
