---
name: "Engagement Playbook — Scope, Bukti, dan Serah-Terima"
description: "Alur engagement penetration testing: scope dan rules of engagement, disiplin bukti, urutan penulisan laporan, kriteria berhenti, dan serah-terima ke klien."
tags: [engagement, scope, rules-of-engagement, evidence, reporting, stop-conditions, handover]
---

# Engagement Playbook — Scope, Bukti, dan Serah-Terima

Bagian tersulit engagement bukan shell pertama; itu bagian yang paling ramai ditulis orang lain. Yang menentukan kualitas hasil adalah apakah target yang disentuh memang milik klien, apakah bukti bisa direproduksi setelah sesi selesai, dan apakah klien tahu apa yang harus diperbaiki. Halaman ini mengatur urutan itu.

## 1. Scope dan Rules of Engagement

Sebelum sentuhan pertama, pastikan dokumen berikut ada dan sudah dikonfirmasi klien:

- **Aset in-scope** — hostname, CIDR, aplikasi, akun, atau tenant yang boleh diuji; sebutkan yang eksplisit.
- **Aset out-of-scope** — termasuk layanan pihak ketiga, host produksi tertentu, dan data yang tidak boleh diakses.
- **Window tes** — tanggal, jam, dan zona waktu; perubahan window harus lewat persetujuan tertulis.
- **Larangan teknis** — DoS, social engineering, physical access, modifikasi data, atau teknik lain yang tidak boleh dipakai.
- **Kontak darurat** — siapa yang dihubungi bila layanan terganggu, dan siapa yang berwenang menghentikan tes.
- **Penanganan data** — di mana bukti disimpan, siapa yang boleh melihat, dan kapan dihapus.
- **Format deliverable** — laporan, arsip bukti, sesi walkthrough, atau retest.

Aturan: setiap target dicek terhadap daftar sebelum disentuh. Scope yang ambigu bukan izin untuk menebak — berhenti dan tanya. Perubahan scope di tengah jalan harus tertulis, bukan kesepakatan lisan di chat.

## 2. Disiplin Bukti

Bukti diambil saat akses masih hidup; merekonstruksinya kemudian hampir selalu kehilangan detail.

- **Satu folder per target** — scan, screenshot, catatan, dan output perintah tidak tercampur.
- **Identitas dalam satu frame** — hostname, IP, dan output yang relevan terlihat bersama.
- **Perintah dan output disimpan apa adanya** — bukan ringkasan yang ditulis ulang dari ingatan.
- **Terminal logging aktif** sejak awal sesi; screenshot adalah pelengkap, bukan pengganti log.
- **Sumber exploit asli dicatat** — URL, versi, dan perubahan yang saya buat sendiri.
- **Kredensial dan data sensitif diredaksi** sebelum masuk laporan atau dikirim ke pihak lain.
- **Ambil bukti sebelum pindah target** — shell yang ditutup sebelum bukti diambil berarti pekerjaan diulang.

## 3. Urutan Penulisan Laporan

Tulis paralel dengan eksekusi; laporan yang ditulis di akhir kehilangan detail dan waktu.

1. **Executive Summary (150–200 kata)** — dampak bisnis dan temuan utama, bukan daftar CVE. Ditulis untuk pembaca yang tidak menjalankan perintah.
2. **Methodology Overview** — scope, window, pendekatan, dan batasan yang disepakati.
3. **Detailed Findings per target** — ringkasan, bukti, langkah reproduksi, dampak, dan remediasi.
4. **Appendices** — shellcode, code listing, dan output panjang yang tidak perlu memenuhi badan laporan.

Setiap temuan harus menjawab: apa yang bisa dilakukan penyerang, dari mana, dengan bukti apa, dan apa yang harus diubah. Temuan tanpa langkah reproduksi sulit diverifikasi klien dan mudah dianggap false positive.

## 4. Kriteria Berhenti

Berhenti adalah keputusan operasional, bukan tanda menyerah. Saya berhenti ketika:

- nilai marginal jalur ini sudah di bawah risiko dan waktu yang dibutuhkan;
- langkah berikutnya bisa memutus layanan produksi tanpa persetujuan pemiliknya;
- bukti sudah cukup untuk klaim, dan menambah akses tidak menambah pemahaman klien;
- window tes habis atau kontak darurat meminta tes dihentikan;
- scope menjadi ambigu dan jawabannya butuh persetujuan tertulis;
- saya sudah terlalu lelah untuk menilai risiko dengan benar.

Sebelum berhenti: amankan bukti, catat jalur yang sudah dicoba beserta hasilnya, dan tandai apa yang belum diuji.

## 5. Serah-Terima ke Klien

Serah-terima bukan sekadar mengirim PDF. Yang diserahkan:

- **Laporan** sesuai urutan di atas, dengan tingkat keparahan dan dasar penilaiannya.
- **Arsip bukti** yang tertata per target, dengan catatan retensi dan akses.
- **Walkthrough** temuan utama bersama engineer klien, agar langkah reproduksi bisa dijalankan sendiri.
- **Daftar artefak yang dibersihkan** — webshell, akun, file, dan perubahan konfigurasi — beserta sisa yang sengaja ditinggalkan.
- **Daftar yang belum diuji** — aset di luar scope, jalur yang terblokir, atau tes yang dihentikan.
- **Rencana retest** bila klien memintanya, dengan lingkup yang disepakati.

## 6. Batas dengan Skill Lain

- Fase pentest generik dan struktur metodologi ada di skill `ptes-standard`; halaman ini hanya mengatur disiplin engagement.
- Engagement jaringan berlapis — double pivoting, segmen dalam, OT/SCADA — doktrinnya ada di skill `cpent`.
- Recon web yang mendalam ada di skill `web-reconnaissance`.

## Best Practices

- Baca ulang scope setiap pagi; target yang benar kemarin belum tentu masuk daftar hari ini.
- Simpan bukti dalam format yang bisa dibuka tanpa tool berbayar.
- Tulis temuan setelah selesai satu target, bukan setelah semua target.
- Minta review rekan sebelum laporan dikirim; kesalahan kecil di laporan mahal reputasinya.
- Bersihkan artefak dan dokumentasikan; backdoor yang lupa dihapus adalah temuan baru.
