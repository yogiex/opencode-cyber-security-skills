---
name: "Engagement Playbook — Scope, Rules of Engagement & Deliverables"
description: "Alur engagement penetration testing profesional dari scoping sampai retest: rules of engagement, disiplin bukti, kriteria berhenti, penanganan temuan kritis, dan anatomi deliverable yang bisa dipertahankan di depan klien maupun auditor."
tags: [engagement, scoping, rules-of-engagement, evidence, deliverables, methodology]
---

# Engagement Playbook

Engagement adalah kontrak, bukan eksperimen. Setiap langkah teknis harus bisa dijawab dengan tiga pertanyaan: atas otorisasi apa, apa dampaknya kalau gagal, dan bagaimana buktinya sampai ke klien.

## 1. Scoping — sebelum paket pertama dikirim

| Item | Yang harus terjawab |
|---|---|
| Aset | Daftar host/CIDR/domain/API; mana produksi, staging, atau replika |
| Out of scope | Host pihak ketiga, tenant cloud lain, layanan vendor, data pelanggan |
| Window | Jam uji, blackout, change freeze, periode retest |
| Rate limit | Request/detik, koneksi paralel, larangan DoS dan password spraying agresif |
| Kredensial | Akun uji yang disediakan, cara penyimpanan, cara pemusnahan di akhir |
| OT/ICS | Zona yang boleh disentuh, izin write, prosedur rollback, pendamping operator |
| Kontak darurat | Siapa dihubungi saat host down, temuan kritis, atau keluar scope |
| Deliverable | Format, bahasa, audiens, tanggal, tingkat redaksi data sensitif |

Tanpa tabel ini terisi, jangan mengirim paket pertama. Ketidakjelasan scope adalah sumber utama insiden hukum dan insiden produksi.

## 2. Rules of Engagement minimum

1. **Otorisasi tertulis** — nama penandatangan, aset, tanggal mulai/berakhir, dan batas wewenang.
2. **Bukti wewenang** — domain verification untuk pengujian web, surat tugas untuk uji internal.
3. **Batasan teknik** — apa yang dilarang: DoS, social engineering terhadap karyawan, physical, data exfiltration nyata.
4. **Penanganan data** — temuan dan bukti disimpan terenkripsi, diakses hanya tim, dimusnahkan sesuai jadwal.
5. **Kanal komunikasi** — jalur aman untuk melaporkan temuan kritis (bukan tiket publik, bukan email massal).
6. **Eskalasi** — kriteria kapan pekerjaan dihentikan dan siapa yang memutuskan melanjutkan.

> Uji coba yang tidak punya butir 1 dan 2 adalah aktivitas ilegal, bukan penetration testing. Berhenti dan minta dokumennya.

## 3. Fase kerja

```
Pre-engagement → Reconnaissance → Foothold → Depth (pivot & privesc) → Objective → Reporting → Retest
```

| Fase | Keluaran yang harus ada |
|---|---|
| Pre-engagement | Scope, RoE, jadwal, kontak, metode bukti |
| Reconnaissance | Peta aset, layanan, versi, permukaan serang, hipotesis |
| Foothold | Akses awal yang terverifikasi + bukti identitas host |
| Depth | Peta pivot, segmen baru, hak akses, jalur menuju objective |
| Objective | Bukti objective tercapai (data, akses, kontrol) sesuai kontrak |
| Reporting | Deliverable final + arsip bukti |
| Retest | Verifikasi perbaikan, bukan pengujian ulang penuh |

## 4. Disiplin bukti

Setiap temuan butuh paket bukti yang konsisten:

- **Identitas host** — hostname, IP, dan waktu di frame yang sama.
- **Perintah dan output** — perintah persis yang dijalankan, bukan ringkasan.
- **Reproduksi** — langkah yang bisa diulang engineer lain tanpa menebak.
- **Dampak** — apa yang bisa dicapai (baca data, eksekusi, eskalasi, lateral).
- **Batas** — sejauh mana uji dilakukan dan apa yang sengaja tidak dilakukan.

Bukti diambil saat kejadian, bukan direkonstruksi setelah sesi selesai. Sesi yang berakhir tanpa bukti adalah sesi yang tidak pernah terjadi.

## 5. Kriteria berhenti

Berhenti dan lapor ketika salah satu terjadi:

- Objective kontrak tercapai — melanjutkan hanya menambah risiko tanpa nilai.
- Dampak produksi terdeteksi (layanan down, data berubah, alert masif).
- Keluar scope secara tidak sengaja (host pihak ketiga, tenant lain, data pelanggan).
- Batas waktu sesi habis.
- Menemukan bukti insiden aktif — itu domaine tim IR, bukan penetration test.

## 6. Temuan kritis

Temuan yang bisa dipakai langsung (RCE tanpa autentikasi, kredensial domain, akses ke data pelanggan) dilaporkan **segera**, tidak menunggu laporan akhir. Format singkat: apa, di mana, dampak, bukti minimum, rekomendasi segera. Detail masuk laporan akhir.

## 7. Metrik kedalaman

Report yang baik menjawab "seberapa dalam", bukan hanya "apa yang ditemukan":

| Metrik | Contoh |
|---|---|
| Segmen dijangkau | 3 dari 5 segmen dalam scope |
| Trust boundary dilintasi | workstation → server → domain controller |
| Hak akhir | domain user → local admin → domain admin |
| Jalur | entry → pivot 1 → pivot 2 → objective |

## 8. Anatomi deliverable

1. **Cover dan distribusi** — klasifikasi, penerima, versi.
2. **Executive summary** — 1 halaman, bahasa risiko bisnis, tanpa jargon.
3. **Metodologi** — standar yang dipakai (PTES, OWASP WSTG, NIST SP 800-115), fase, batasan.
4. **Peta serangan** — diagram jalur dari entry sampai objective.
5. **Temuan** — per temuan: judul, severity, CVSS 3.1, CWE, bukti, dampak, remediasi.
6. **Rekomendasi** — prioritas berdasarkan risiko, bukan urutan penemuan.
7. **Lampiran** — command log, daftar host, bukti tambahan, redaksi.

## 9. Best Practices

- Tulis scope dan kriteria berhenti di halaman pertama kerja, bukan di kepala.
- Satu temuan = satu paket bukti; jangan mencampur bukti beberapa host dalam satu screenshot.
- Simpan timeline: kapan mulai, kapan berhenti, kapan pivot terjadi.
- Uji laporan dengan mata orang lain sebelum dikirim — reproducible atau tidak.
- Retest hanya memverifikasi remediasi; temuan baru adalah engagement baru.
