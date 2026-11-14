---
name: "Verdict dan Prioritas Triage"
description: "Definisi TP/FP/Benign/Unknown untuk alert Wazuh, matriks kecukupan bukti, formula prioritas level x kekritisan aset x keyakinan, contoh verdict dengan alasan, dan kesalahan penalaran yang sering terjadi."
tags: [wazuh, verdict, true-positive, false-positive, benign, unknown, prioritas, severity, keyakinan, triage]
---

# Verdict dan Prioritas Triage

## Empat Verdict

| Verdict | Definisi | Syarat minimum |
|---|---|---|
| **TP — True Positive** | Aktivitas berbahaya/terlarang benar terjadi dan rule mendeteksinya dengan benar | ≥ 2 sumber, satu di antaranya menunjukkan dampak atau niat |
| **FP — False Positive** | Rule cocok, tetapi aktivitasnya sah dan dapat dijelaskan | ≥ 2 sumber, termasuk penjelasan mengapa rule cocok |
| **Benign** | Aktivitas tidak sah secara konfigurasi tetapi tidak berbahaya pada konteks ini (mis. scanner internal) | Sumber kegiatan teridentifikasi (pemilik, jadwal, tiket) |
| **Unknown** | Bukti tidak cukup untuk memutuskan dalam batas waktu | Daftar bukti yang sudah diambil + yang masih dibutuhkan |

`Benign` bukan sinonim `FP`. Dalam `FP`, deteksi salah sasaran; dalam `Benign`, deteksi benar mendeteksi sesuatu yang disengaja dan tidak berbahaya. Perbedaan ini menentukan apakah yang diperbaiki rule atau ekspektasi.

## Matriks Kecukupan Bukti

| Kombinasi yang tersedia | Keyakinan | Verdict yang boleh |
|---|---|---|
| Alert + konteks agent + log sumber + korelasi | Tinggi | TP / FP / Benign |
| Alert + konteks agent | Sedang | FP hanya bila penyebabnya terbukti dari konteks; selain itu Unknown |
| Alert + `full_log` saja | Rendah | Unknown |
| Alert tanpa telemetri agent (agent mati) | Sangat rendah | Unknown + eskalasi masalah telemetri |
| Alert + penjelasan pemilik aset (tiket/jadwal) | Tinggi untuk Benign | Benign |

## Prioritas

```text
prioritas dasar  = level alert (tabel SKILL.md)
+1 tingkat       = aset kritikal (daftar aset disepakati, bukan tebakan)
-1 tingkat       = keyakinan bukti rendah (lihat matriks di atas)
prioritas akhir  = hasil pembatasan P0..P4
```

| Prioritas | Respons | Contoh |
|---|---|---|
| **P0** | Segera, eskalasi paralel | Rule 14–16 pada domain controller, malware aktif menyebar |
| **P1** | ≤ 30 menit | Login sukses setelah brute force, perubahan biner sistem |
| **P2** | Jam kerja yang sama | FIM pada konfigurasi layanan, SCA gagal pada host produksi |
| **P3** | ≤ 1 hari kerja | Auth gagal tersebar, rule kata kunci |
| **P4** | Backlog terencana | Event sukses pada host non-kritikal |

Prioritas **bukan** level. Level 12 pada laptop uji bisa P2; level 8 pada server pembayaran bisa P1.

## Contoh Verdict

### 1. Brute force gagal tanpa login sukses → FP (scanner internal)

- Fakta: 240 alert rule 5710 dari `10.10.5.20` ke 12 host, window 10 menit; IP terdaftar sebagai scanner vulnerability.
- Bukti: daftar agent + syscollector netaddr; tiket pemindaian terjadi pada jam yang sama.
- Verdict: Benign (bukan FP — rule bekerja benar).
- Tindakan: whitelist IP scanner via CDB; catat di pelacak FP.

### 2. Login sukses setelah 60 percobaan gagal → TP

- Fakta: rule 5710 berulang dari satu IP, lalu `authentication_success` untuk user yang sama.
- Bukti: timeline dua arah, log sumber `auth.log` di host, sesi berikutnya.
- Verdict: TP; prioritas P1 (naik karena akun dengan sudo).
- Tindakan: eskalasi + containment (blokir IP), reset kredensial.

### 3. Perubahan `/etc/nginx/nginx.conf` → Benign (deploy terjadwal)

- Fakta: `syscheck.path` pada file konfigurasi, `syscheck.event: modified`, hash berubah.
- Bukti: tiket change management pada jam yang sama; `syscheck.audit` menunjukkan user deploy.
- Verdict: Benign.
- Tindakan: catat; pertimbangkan `nodiff`/ignore terarah hanya bila pola berulang.

### 4. YARA hit pada file sementara → Unknown

- Fakta: rule malware cocok pada file di `/tmp`, hash belum dikenal, host offline sejak 2 jam.
- Bukti: alert + syscollector (snapshot lama) — tidak ada konfirmasi proses.
- Verdict: Unknown; eskalasi L2 dengan permintaan triage host.
- Tindakan: minta owner menghidupkan agent; jangan menutup sebagai FP.

### 5. SCA check gagal pada host non-kritikal → FP? Tidak.

- Fakta: `data.sca.check.result: failed` untuk hardening SSH.
- Verdict: bukan alert serangan; ini temuan kepatuhan. Klasifikasikan sesuai proses SCA organisasi (temuan hardening), bukan TP/FP keamanan.
- Tindakan: catat sebagai temuan konfigurasi; prioritas P2/P3 sesuai kebijakan.

## Kesalahan Penalaran Umum

| Pola | Mengapa salah | Perbaikan |
|---|---|---|
| "Level tinggi berarti nyata" | Level adalah desain rule, bukan bukti | Cari bukti dampak |
| "Sudah sering muncul, berarti FP" | Frekuensi bukan bukti | Cek sampel dan sumbernya |
| "Agent diam, jadi aman" | Telemetri mati justru risiko | Periksa status agent dan logcollector |
| "Tidak ada alert lain, jadi satu-satunya" | Retensi/`logall` bisa menyembunyikan | Cek ketersediaan indeks dan arsip |
| "IP internal, jadi aman" | Lateral movement berasal dari internal | Cek apakah host itu normally berkomunikasi ke sana |
| "Rule ATT&CK-nya T1110, jadi brute force" | Pemetaan rule bisa kasar | Baca `full_log` dan pola waktunya |

## Best Practices

- Tulis verdict dalam satu kalimat yang memuat subjek, aksi, dan alasan: "Login sukses oleh `admin` dari 203.0.113.45 setelah 60 kegagalan — percobaan brute force berhasil."
- Simpan sampel alert (`id`) untuk setiap FP; tuning tanpa sampel akan ditolak saat change request.
- Jangan menaikkan prioritas karena tekanan eksternal tanpa bukti baru; catat permintaan dan alasan penolakannya.
- Bila ragu antara TP dan Unknown, pilih Unknown dan eskalasi — keputusan yang bisa direvisi lebih baik daripada klaim yang salah.
