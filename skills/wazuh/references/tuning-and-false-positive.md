---
name: "False Positive dan Tuning Wazuh"
description: "Cara mengklasifikasikan false positive alert Wazuh, akar masalah yang umum, urutan opsi tuning dari yang paling aman ke paling berisiko, format change request, dan cara mengukur dampak tuning."
tags: [wazuh, false-positive, tuning, tuning-rule, whitelist, cdb, ignore, nodiff, frequency, change-request, noise]
---

# False Positive dan Tuning Wazuh

## Klasifikasi Sebelum Tuning

| Jenis | Ciri | Yang diperbaiki |
|---|---|---|
| **Deteksi terlalu luas** | Rule cocok pada pola umum ("error", "failed"), banyak host | Persempit `field`/`regex` atau tambah `if_sid` |
| **Aktivitas sah tak dikenal** | Scanner internal, agen monitoring, backup | CDB whitelist atau rule pengecualian sempit |
| **Baseline belum ada** | "First time seen" pada aktivitas rutin yang baru | Dokumentasikan baseline, bukan matikan rule |
| **Konfigurasi agent salah** | Path log salah, modul ganda, agent duplikat | Perbaiki konfigurasi agent |
| **Duplikasi rule** | Satu event memicu 2+ alert serupa | Nonaktifkan salah satu rule (dengan alasan) |
| **Ambang korelasi terlalu rendah** | `frequency` kecil memicu alert pada pola normal | Naikkan `frequency`/`timeframe` |
| **Data sensitif salah tempat** | Diff FIM memuat kredensial | `nodiff`, bukan menghapus monitoring |

Tuning hanya sah bila jenisnya jelas. "Alert-nya mengganggu" bukan diagnosis.

## Urutan Opsi Tuning

Dari paling aman ke paling berisiko:

| # | Opsi | Aman karena | Risiko |
|---|---|---|---|
| 1 | Perbaiki konfigurasi agent | Tidak menyentuh deteksi | Waktu perubahan di sisi endpoint |
| 2 | Perbaiki decoder (field salah) | Meningkatkan akurasi, bukan menurunkan cakupan | Perlu uji `wazuh-logtest` |
| 3 | Persempit `field`/`regex`/`if_sid` | Mengurangi cocok palsu tanpa mematikan rule | Bisa melewatkan varian nyata |
| 4 | Tambah CDB whitelist (IP/host sah) | Terlihat dan bisa diaudit | Bisa menyembunyikan host yang benar-benar terkompromi |
| 5 | `ignore` / `nodiff` pada path atau rule | Mengurangi banjir alert berulang | Menyembunyikan perubahan beruntun |
| 6 | Naikkan `frequency`/`timeframe` | Mengurangi alert korelasi | Serangan lambat bisa lolos ambang |
| 7 | Turunkan `level` | Mengubah prioritas, bukan menghilangkan alert | Level di bawah `log_alert_level` (3) = alert hilang |
| 8 | `noalert="1"` | Menekan alert sambil mempertahankan evaluasi | Sulit dilacak bila tidak didokumentasi |
| 9 | Nonaktifkan rule | Menghilangkan noise sepenuhnya | Kehilangan deteksi; **butuh persetujuan** |

Urutan ini wajib diikuti: jangan melompat ke opsi 7–9 demi dashboard yang bersih.

## Format Change Request

```markdown
## Ringkasan
Rule 5710 memicu 240 alert/hari dari scanner internal 10.10.5.20.

## Bukti
- 3 sampel alert: <id>, <id>, <id> (level 5, agent web-01/02/03, 11–13 Nov)
- IP terdaftar sebagai scanner (tiket CHG-1234)
- Tidak ada login sukses dari IP tersebut

## Usulan
Whitelist lewat CDB: `etc/lists/scanner-whitelist`, rule 100210 level 0.

## Risiko
Bila 10.10.5.20 dipakai aktor lain, alert tidak akan muncul.

## Verifikasi
Bandingkan jumlah alert rule 5710 sebelum/sesudah 7 hari; uji sampel log dengan wazuh-logtest.
```

## Mengukur Dampak

| Metrik | Cara |
|---|---|
| Volume sebelum/sesudah | Hitung dokumen `rule.id` pada rentang setara |
| Cakupan | Pastikan sampel serangan serupa masih memicu rule |
| Alert baru | Periksa apakah tuning memunculkan alert lain (efek samping) |
| Rasio FP | FP/total per rule, bukan angka global |

Tuning tanpa angka sebelum/sesudah tidak dapat dinilai berhasil atau gagal.

## Kapan Tuning Ditolak

- Sampel < 3 dan alasannya hanya "mengganggu";
- tuning menurunkan deteksi pada kelas yang sedang jadi target (mis. brute force saat ada kampanye aktif);
- usulan menonaktifkan rule tanpa pengganti;
- whitelist mencakup rentang jaringan luas (`10.0.0.0/8`) atau domain publik;
- alasan didasarkan pada satu alert yang tidak diverifikasi.

## Best Practices

- Satu change request per rule; jangan menggabungkan 5 perubahan untuk 5 rule berbeda.
- Simpan alert sampel di pelacak FP (`assets/false-positive-tracker.csv`) agar bukti tidak hilang saat retensi berjalan.
- Setelah tuning diterapkan, restart manager dan verifikasi alert nyata — logtest hanya membuktikan pencocokan, bukan jalur indeks.
- Dokumentasikan siapa yang menyetujui dan kapan; tuning adalah perubahan deteksi, bukan preferensi pribadi.
- Tinjau ulang tuning setelah upgrade ruleset: ID rule bawaan dan level dapat berubah.
