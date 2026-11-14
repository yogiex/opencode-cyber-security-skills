---
name: "Kesehatan Telemetri dan Troubleshooting Alert"
description: "Cara memastikan telemetri Wazuh benar-benar mengalir sebelum menyimpulkan hasil triage: status agent dan logcollector, modul aktif, Filebeat ke indexer, alert hilang/duplikat/terlambat, serta pemeriksaan log manager."
tags: [wazuh, telemetry, troubleshooting, agent, logcollector, filebeat, ossec.log, indexer, alert-hilang, duplikat, terlambat, health]
---

# Kesehatan Telemetri dan Troubleshooting Alert

## Mengapa Ini Bagian dari Triage

Sebagian besar kesalahan triage bukan salah membaca alert, melainkan menyimpulkan dari data yang tidak lengkap. Enam pemeriksaan di bawah menentukan apakah "tidak ada alert" berarti "tidak ada aktivitas" atau "tidak ada data".

## Enam Pemeriksaan Dasar

| # | Pemeriksaan | Cara | Bila gagal |
|---|---|---|---|
| 1 | Agent terhubung | `GET /agents/summary/status`, `GET /agents?q=id=003` | Alert tidak akan datang; triase tidak bisa dilanjutkan |
| 2 | Agent mengirim log | `wazuh-agentd.state`, `wazuh-logcollector.state` di agent | `logcollector` mati atau path log salah |
| 3 | Modul aktif | `ossec.conf` agent/manager (`<syscheck><disabled>`, `<sca>`, `<localfile>`) | Modul `disabled=yes` → tidak ada bukti dari modul itu |
| 4 | Manager memproses | `GET /manager/status`, daemon `wazuh-analysisd` | Antrean menumpuk, alert tidak terbentuk |
| 5 | Alert keluar dari manager | `jsonout_output` = `yes`, `alerts.json` bertambah | Alert tidak pernah sampai ke indexer |
| 6 | Indexer menerima | `GET /_cat/indices/wazuh-alerts-*?v`, dokumen terbaru | Filebeat/sertifikat/ruang disk bermasalah |

## Gejala dan Penyebab

### Alert tidak muncul di dashboard

1. Level di bawah `log_alert_level` (default 3) → alert memang tidak dibuat. Cek `rule.level`.
2. `jsonout_output` atau Filebeat mati → alert ada di `alerts.log` tapi tidak diindeks.
3. Filter waktu dashboard memakai `@timestamp` sementara index pattern memakai `timestamp` → hasil kosong.
4. Retensi sudah menghapus indeks untuk rentang yang dicari.
5. Rule dinonaktifkan atau di-`overwrite` dengan level lebih rendah pada versi ruleset terbaru.

### Alert duplikat

| Penyebab | Cara memastikan |
|---|---|
| Parent + child rule pada event sama | Bandingkan `rule.id` dan `full_log` dua alert |
| Rule korelasi menambah alert di atas alert dasar | Periksa `rule.frequency` dan `previous_output` |
| Agent terdaftar ganda (nama/IP sama) | `GET /agents`, cek `id` berbeda untuk host yang sama |
| Beberapa manager mengirim alert sama | Cek `manager.name` pada dokumen |

### Alert terlambat

| Penyebab | Cara memastikan |
|---|---|
| Agent antre (jaringan lambat) | `wazuh-agentd.state`, `lastKeepAlive` |
| Manager `analysisd` kewalahan | `GET /manager/status`, antrean di `ossec.log` |
| Filebeat tertinggal | Log Filebeat, lag indeks |
| Jam agent/manager tidak sinkron | Bandingkan `timestamp` alert dengan jam host |

Selisih jam adalah penyebab paling sering dari timeline yang tidak masuk akal. Tanpa sinkronisasi waktu, korelasi `±5 menit` bisa salah total.

### Alert dengan field kosong

- `data.*` kosong: decoder tidak mengekstrak field, atau decoder salah yang cocok.
- `syscheck.diff` kosong: `report_changes` tidak aktif atau berkas melebihi `diff_size_limit`.
- `syscheck.audit.*` kosong: who-data tidak aktif atau auditd tidak berjalan.
- `rule.mitre` kosong: rule tidak memetakan ATT&CK (bukan masalah teknis).

## Log yang Dibaca

| Log | Lokasi | Kegunaan |
|---|---|---|
| `ossec.log` | `/var/ossec/logs/ossec.log` | Kesalahan ruleset, decoder, modul, koneksi agent |
| `alerts.log` / `alerts.json` | `/var/ossec/logs/alerts/` | Alert terbentuk di manager |
| `archives.log` / `.json` | `/var/ossec/logs/archives/` | Semua event bila `logall` aktif |
| `active-responses.log` | `/var/ossec/logs/active-responses.log` | Hasil eksekusi active response |
| `api.log` / `api.json` | `/var/ossec/logs/` | Permintaan API dan kesalahannya |
| Log Filebeat | `/var/log/filebeat/filebeat` | Jalur manager → indexer |

Contoh pencarian:

```bash
# Kesalahan ruleset/decoder setelah perubahan
grep -iE "error|warning" /var/ossec/logs/ossec.log | tail -50

# Apakah rule tertentu pernah dimuat
grep -i "100200" /var/ossec/logs/ossec.log

# Filebeat mengirim ke indeks mana
grep -i "wazuh-alerts" /var/log/filebeat/filebeat | tail -20
```

## Uji Cepat Sebelum Menyimpulkan

| Uji | Perintah | Arti bila gagal |
|---|---|---|
| Rule bisa mencocokkan log | `/var/ossec/bin/wazuh-logtest` | Masalah rule/decoder, bukan jalur data |
| Agent menerima konfigurasi | `/var/ossec/bin/verify-agent-conf` (manager) | `agent.conf` grup salah |
| Alerts.json tumbuh | `tail -f /var/ossec/logs/alerts/alerts.json` | Manager tidak memproses atau output JSON mati |
| Indeks terbaru ada | `GET /_cat/indices/wazuh-alerts-*?v` | Filebeat/indexer bermasalah |

## Prinsip Diagnosis

1. **Ikuti jalur data dari hulu ke hilir**: agent → manager → berkas → Filebeat → indexer → dashboard. Berhenti pada titik pertama yang kosong.
2. **Jangan menyimpulkan negatif dari satu titik.** "Tidak ada di dashboard" bukan "tidak ada di manager".
3. **Ubah satu variabel per uji.** Mengubah rule dan Filebeat bersamaan membuat penyebab tidak diketahui.
4. **Catat hasil uji di laporan** agar shift berikutnya tidak mengulang.

## Best Practices

- Jadikan enam pemeriksaan dasar sebagai checklist awal shift, bukan reaksi saat alert hilang.
- Simpan baseline volume alert per hari; penurunan mendadak biasanya masalah telemetri, bukan ketenangan.
- Sinkronkan waktu semua komponen (NTP) dan verifikasi setelah perubahan infrastruktur.
- Saat melaporkan masalah data, sertakan waktu, host, dan titik jalur yang gagal — bukan hanya "alert tidak muncul".
