---
name: "Laporan dan Handover Triage"
description: "Struktur laporan triase alert Wazuh yang bisa diaudit, pemetaan ATT&CK dan ekstraksi IoC, penyesuaian bahasa untuk audiens teknis dan manajemen, aturan redaksi, serta format handover shift."
tags: [wazuh, reporting, laporan, handover, ioc, mitre, att&ck, redaksi, komunikasi, eskalasi, triage]
---

# Laporan dan Handover Triage

## Prinsip

1. Laporan harus bisa dipahami orang yang tidak melihat dashboard.
2. Setiap klaim punya bukti: alert ID, waktu, host, dan sumber data.
3. Verdict dan alasan dipisahkan dari narasi.
4. Data sensitif diredaksi, bukan dihilangkan tanpa jejak (sebut bahwa ada redaksi).

## Struktur Laporan per Alert

```markdown
# Triage — <rule.id> pada <agent.name>

## Ringkasan
Satu paragraf: apa yang terdeteksi, di mana, kapan, dan verdict-nya.

## Identitas Alert
- Alert ID: <id>
- Rule: <rule.id> — <rule.description> (level <level>)
- Agent: <agent.id> / <agent.name> / <agent.ip>
- Waktu: <timestamp UTC> (<waktu lokal>)
- Sumber log: <location> (decoder: <decoder.name>)

## Bukti
| # | Bukti | Sumber | Nilai |
|---|---|---|---|
| 1 | Log mentah | full_log | <potongan teredaksi> |
| 2 | Proses berjalan | syscollector/processes | <proses relevan> |
| 3 | Perubahan file | syscheck | <path, event> |
| 4 | Korelasi | indexer | <n alert terkait dalam X menit> |

## Verdict
**TP / FP / Benign / Unknown** — alasan dalam 1–2 kalimat.

## Prioritas
P<n> — level <x>, aset <kritikal/tidak>, keyakinan bukti <tinggi/sedang/rendah>.

## Tindakan
- [ ] Tutup dengan alasan
- [ ] Monitor <rentang waktu>
- [ ] Eskalasi ke <pemilik> karena <pemicu>
- [ ] Usulan tuning: <ringkas> (lihat change request terpisah)

## IoC (bila ada)
| Tipe | Nilai | Konteks | Keyakinan |
|---|---|---|---|
| IP | <ip> | sumber login gagal | tinggi |

## ATT&CK (bila rule memetakan)
T<id> — <tactic/technique>. Bila rule tidak memetakan, tulis "rule tidak memetakan ATT&CK".

## Catatan dan Keterbatasan
Data yang tidak tersedia, agent yang mati, retensi yang pendek, atau redaksi yang dilakukan.
```

## Ekstraksi IoC

| Tipe | Sumber di alert |
|---|---|
| IP sumber/tujuan | `data.srcip`, `data.dstip`, `data.win.eventdata.ipAddress` |
| Domain/URL | `data.url`, `full_log` |
| Hash | `syscheck.sha256_after`, `data.virustotal.*` |
| Akun | `data.srcuser`, `data.dstuser`, `data.win.eventdata.targetUserName` |
| Proses/berkas | `data.audit.exe`, `syscheck.path` |

IoC tanpa konteks tidak berguna: selalu sertakan host, waktu, dan peran (sumber serangan, korban, atau keduanya). Bila indikator dikirim ke pihak eksternal, periksa kebijakan data organisasi lebih dulu.

## Bahasa untuk Berbagai Audiens

| Audiens | Isi | Hindari |
|---|---|---|
| L2/IR | Alert ID, rule, log, endpoint, endpoint API, timeline | Ringkasan bisnis panjang |
| Manajemen | Dampak, aset, status, keputusan yang dibutuhkan, tenggat | `decoder.name`, sintaks XML |
| Pemilik aset | Apa yang perlu dilakukan, kapan, apa risikonya bila tidak | Jargon SOC |
| Auditor | Bukti, waktu, siapa menyetujui, perubahan yang dilakukan | Opini tanpa bukti |

Kalimat verdict yang baik:

- "Login sukses oleh `admin` dari 203.0.113.45 setelah 60 kegagalan berturut-turut — indikasi brute force berhasil."
- "Perubahan `/etc/nginx/nginx.conf` sesuai change request CHG-1234 pada 11:05 — aktivitas sah."

Kalimat yang harus dihindari: "kemungkinan besar aman", "sepertinya false positive", "sudah dicek".

## Redaksi

| Data | Perlakuan |
|---|---|
| Password, token, cookie, kunci API | Hapus; ganti `<REDACTED>` |
| Hash kredensial (NTLM, dsb.) | Tampilkan 8 karakter pertama saja bila perlu |
| PII (email, nama pelanggan, nomor identitas) | Samarkan sebagian |
| `full_log` panjang | Kutip baris relevan, bukan seluruh baris |
| Path internal sensitif | Sebut direktori induk, bukan path lengkap, bila tidak relevan |

Selalu catat bahwa redaksi dilakukan agar pembaca tahu ada informasi yang tidak ditampilkan.

## Handover Shift

```markdown
# Handover <tanggal> <shift>

## Antrean
- Terbuka: <n> (P0: <n>, P1: <n>, P2: <n>, P3/P4: <n>)
- Rule terbanyak: <rule.id> (<n> alert) — <status triage>

## Belum selesai
| Alert ID | Rule | Agent | Status | Langkah berikutnya |
|---|---|---|---|---|

## Menunggu eskalasi
| Tiket | Pemilik | Sejak | Yang diminta |
|---|---|---|---|

## Perubahan hari ini
| Waktu | Perubahan | Disetujui oleh | Alasan |
|---|---|---|---|

## Telemetri
- Agent mati/tidak melapor: <daftar>
- Modul nonaktif: <daftar>
- Indeks/retensi: <catatan>

## Risiko 12 jam ke depan
- <mis. agent 003 masih offline, alert FIM tidak akan muncul>
```

## Best Practices

- Tulis laporan sambil bekerja; rekonstruksi setelah shift selesai selalu kehilangan detail.
- Satu baris ringkasan di awal agar pembaca bisa berhenti di situ bila hanya butuh status.
- Sertakan tindakan yang **tidak** diambil beserta alasannya; itu bagian dari keputusan.
- Jangan menyalin seluruh respons API; ambil field yang mendukung klaim saja.
- Akhiri setiap laporan dengan pertanyaan yang masih terbuka — itu yang dibawa ke shift berikutnya.
