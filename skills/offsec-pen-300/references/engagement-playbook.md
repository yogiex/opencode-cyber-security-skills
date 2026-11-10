---
name: "Engagement Playbook — Otorisasi, Payload Hygiene, Bukti & Cleanup"
description: "Disiplin penyampaian engagement evasion: batas otorisasi untuk eksekusi payload, higiene payload dan rahasia, paket bukti yang diterima klien, urutan pelaporan temuan, kriteria berhenti, dan pembersihan artefak."
tags: [engagement, authorization, payload-hygiene, evidence, reporting, stop-conditions, cleanup]
---

# Engagement Playbook

Pekerjaan evasion adalah pekerjaan yang paling mudah berubah menjadi insiden: payload berjalan dengan hak pengguna, kontrol keamanan sengaja dilewati, dan artefak tertinggal di host produksi. Karena itu disiplinnya bukan tambahan — ia bagian dari teknik.

Doktrin scoping, rules of engagement, dan anatomi deliverable lengkap ada di skill `cpent` (`references/engagement-playbook.md`). Dokumen ini tidak mengulanginya; isinya hanya hal yang khas engagement evasion.

## 1. Otorisasi yang harus eksplisit

Otorisasi generik "boleh melakukan penetration testing" tidak cukup untuk pekerjaan ini. Yang harus tertulis dan disepakati sebelum payload pertama:

| Item | Yang harus eksplisit |
|---|---|
| Eksekusi payload | Izin menjalankan kode di host target, termasuk loader, shellcode, dan teknis delivery-nya |
| Teknik evasion | Izin menguji bypass AV/EDR/AMSI/AppLocker/CLM, dan kontrol mana yang tidak boleh disentuh |
| Akses kredensial | Boleh membaca, menyimpan, atau memakai hash/tiket/sertifikat; batas penyimpanan dan pemusnahan |
| Kanal C2 | Domain, IP, port, dan arah egress yang diizinkan; data apa yang boleh melewati kanal itu |
| Data | Batas baca, larangan eksfiltrasi data nyata, dan cara pemusnahan salinan |
| Persistence | Dilarang, atau butuh persetujuan per mekanisme beserta cara pencabutannya |
| Cleanup | Siapa yang bertanggung jawab, kapan dilakukan, dan bagaimana verifikasinya |
| Kontak darurat | Siapa dihubungi saat host down, alert muncul, atau aktivitas uji keluar scope |

Kalau salah satu belum jelas, tanyakan — jangan menganggap "mungkin boleh". Bagian yang tidak diotorisasi tidak diuji, sekalipun secara teknis mudah.

## 2. Higiene payload

Payload adalah kode yang berjalan dengan hak orang lain. Perlakuannya seperti kode produksi, bukan file sementara:

- **Build yang bisa direproduksi.** Simpan source, versi compiler, konfigurasi, tanggal build, dan hash. Tanpa itu, temuan tidak bisa dipertahankan.
- **Tidak ada shellcode plaintext.** Jangan simpan shellcode mentah di source, catatan, atau chat; enkripsi saat disimpan dan saat dikirim.
- **Satu payload untuk satu engagement.** Jangan memakai ulang payload klien lain; artefak dan hash bisa mengaitkan engagement yang berbeda.
- **Persistence hanya dengan persetujuan.** Setiap mekanisme persistence harus punya cara pencabutan yang diketahui sebelum dipasang.
- **Batas sesi dan kill switch.** C2 profile harus punya masa berlaku dan cara memutus beacon; operator harus tahu cara mencabutnya.
- **Catat pengiriman.** Kapan, ke host mana, dengan hash apa, dan hasilnya — termasuk kegagalan.
- **Ubah sesedikit mungkin.** Teknik yang tidak perlu memodifikasi file target lebih mudah dibersihkan dan dijelaskan.

## 3. Paket bukti yang diterima klien

Klien tidak menerima "saya sudah dapat shell". Yang diterima adalah paket yang bisa direproduksi dan diatribusikan:

| Bukti | Keterangan |
|---|---|
| Identitas host | Hostname, IP, dan waktu (dengan zona waktu) dalam frame atau log yang sama |
| Perintah dan output | Perintah persis yang dijalankan dan output aslinya, bukan ringkasan |
| Konteks akses | User, proses, hak, dan jalur masuk yang dipakai |
| Payload | Hash, konfigurasi, dan langkah build yang cukup untuk reproduksi |
| Dampak | Apa yang bisa dicapai — baca data, eksekusi, eskalasi, lateral |
| Batas uji | Sejauh mana uji dilakukan dan apa yang sengaja tidak dilakukan |
| Jejak defender | Alert, log, atau event yang muncul, sebagai bahan perbaikan klien |

Screenshot hanya sah kalau menampilkan identitas host dan perintahnya; shell tanpa identitas host adalah klaim, bukan bukti. Bukti diambil saat akses masih hidup, disimpan terenkripsi, dan dicatat rantai penguasaannya.

## 4. Urutan penyampaian temuan

Laporan mengikuti rantai serangan, bukan urutan penemuan:

1. **Executive summary** — dampak bisnis, jalur yang berhasil, dan apa yang harus segera diperbaiki.
2. **Narasi serangan** — urutan kronologis dari entry sampai objective, termasuk keputusan dan percobaan yang gagal.
3. **Temuan** — diurutkan berdasarkan severity dan kekuatan bukti, bukan berdasarkan kapan ditemukan.
4. **Peluang deteksi** — event, log, dan aturan yang seharusnya menangkap teknik tersebut.
5. **Lampiran** — kode, hash, IoC, daftar host, dan catatan cleanup.

Temuan yang paling terbukti disampaikan lebih dulu; temuan yang masih hipotesis diberi label jelas. Jangan menyembunyikan percobaan yang gagal — justru itu yang menunjukkan kontrol mana yang bekerja.

## 5. Kriteria berhenti

Berhenti dan lapor ketika salah satu terjadi:

- **Objective tercapai** — melanjutkan hanya menambah noise dan risiko.
- **Defender merespons** — alert, isolasi host, atau tim blue team aktif; keputusan melanjutkan ada di klien, bukan di operator.
- **Host tidak stabil** — layanan turun, proses crash berulang, atau data berubah.
- **Keluar scope** — host, akun, atau data yang tidak tercantum di kontrak.
- **Batas data tercapai** — bukti akses sudah cukup; menyalin data nyata tidak menambah nilai.
- **Timebox teknik habis** — batas waktu per pendekatan yang disepakati di awal sudah lewat tanpa informasi baru; ganti pendekatan atau berhenti.
- **Indikasi insiden aktif** — itu domain tim IR; amankan bukti dan serahkan.

Berhenti bukan kegagalan engagement. Engagement yang berhenti tepat waktu dengan bukti lengkap lebih bernilai daripada satu shell tambahan yang memicu insiden.

## 6. Pembersihan artefak

Cleanup dilakukan terencana, bukan saat ingat. Kategorinya:

| Kategori | Contoh | Tindakan |
|---|---|---|
| Implant dan C2 | beacon, stager, service, scheduled task | Hentikan, hapus, verifikasi tidak ada callback |
| Persistence | run key, WMI subscription, akun lokal | Cabut, hapus, verifikasi dengan query ulang |
| Identitas dan objek direktori | computer account, RBCD, tiket, sertifikat | Cabut atau minta klien mencabut; catat nomor sertifikat |
| Perubahan konfigurasi | `xp_cmdshell`, linked server, aturan firewall, exception AppLocker | Kembalikan ke baseline yang tercatat sebelum perubahan |
| File dan tool | binary yang di-upload, script, log sementara | Hapus dan verifikasi absennya |
| Salinan data | loot, screenshot, log C2 | Enkripsi, serahkan sesuai kontrak, musnahkan salinan lokal |
| Infrastruktur C2 | profile, redirector, domain | Nonaktifkan dan catat tanggalnya |

Artefak yang tidak bisa dibersihkan — misalnya sertifikat yang sudah diterbitkan atau perubahan yang butuh change window — wajib didokumentasikan dengan alasan, pemilik, dan rencana pencabutan. Cleanup diverifikasi, bukan diasumsikan, dan hasilnya diserahkan ke klien.

## 7. Best Practices

- Tulis batas otorisasi dan kriteria berhenti di halaman pertama kerja, bukan di kepala.
- Perlakukan hash payload seperti bukti: dicatat saat build, bukan direkonstruksi saat laporan.
- Simpan timeline: kapan payload dikirim, kapan callback, kapan bukti diambil, kapan cleanup.
- Uji bahwa bukti bisa direproduksi oleh engineer lain sebelum laporan dikirim.
- Inventarisasi artefak sebelum eksekusi; cleanup tanpa baseline adalah tebakan.
