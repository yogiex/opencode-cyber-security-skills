---
name: "Referensi Wazuh dan Perbedaan Versi"
description: "Tautan dokumentasi resmi Wazuh per topik triage, cara memastikan versi yang dibaca (4.x vs 5.x), dan daftar perbedaan yang membuat instruksi satu versi tidak berlaku di versi lain."
tags: [wazuh, referensi, dokumentasi, versi, 4x, 5x, api, ruleset, indexer, active-response, vulnerability-detection]
---

# Referensi Wazuh dan Perbedaan Versi

## Sebelum Mengikuti Panduan Apa Pun

Tentukan versi lebih dulu:

```bash
# Dari API
curl -s -k -u <user>:<pass> https://127.0.0.1:55000/ | grep api_version

# Dari manager
/var/ossec/bin/wazuh-control info
```

| Keluaran | Arti |
|---|---|
| `4.x` | Skill ini berlaku; path `/var/ossec`, indeks `wazuh-alerts-4.x-*` |
| `5.x` | Banyak path dan alur berbeda; jangan mencampur panduan 4.x |

## Dokumentasi Resmi per Topik

Gunakan halaman versi spesifik, bukan halaman `current`, bila Anda butuh panduan yang sesuai instalasi. Pola URL 4.x: `https://documentation.wazuh.com/4.14/<path>.html` (tersedia juga padanan `.md` per halaman).

| Topik | Path dokumentasi |
|---|---|
| Arsitektur dan alur data | `/getting-started/architecture.html` |
| Anatomi indeks dan pipeline alert | `/user-manual/wazuh-indexer/wazuh-indexer-indices.html` |
| Event logging, `logall`, archives | `/user-manual/manager/event-logging.html` |
| Sintaks rule | `/user-manual/ruleset/ruleset-xml-syntax/rules.html` |
| Custom rule dan `overwrite` | `/user-manual/ruleset/rules/custom.html` |
| Klasifikasi level | `/user-manual/ruleset/rules/rules-classification.html` |
| Sintaks decoder | `/user-manual/ruleset/ruleset-xml-syntax/decoders.html` |
| Custom decoder dan `decoder_exclude` | `/user-manual/ruleset/decoders/custom.html` |
| Decoder JSON | `/user-manual/ruleset/decoders/json-decoder.html` |
| Pengujian rule/decoder | `/user-manual/ruleset/testing.html` |
| CDB list | `/user-manual/ruleset/cdb-list.html` |
| File integrity monitoring | `/user-manual/capabilities/file-integrity/index.html` |
| Security configuration assessment | `/user-manual/capabilities/sec-config-assessment/index.html` |
| Vulnerability detection | `/user-manual/capabilities/vulnerability-detection/index.html` |
| Active response | `/user-manual/reference/ossec-conf/active-response.html` dan `/user-manual/reference/ossec-conf/commands.html` |
| Skrip active response kustom | `/user-manual/capabilities/active-response/custom-active-response-scripts.html` |
| Wazuh API (mulai) | `/user-manual/api/getting-started.html` |
| Wazuh API (WQL) | `/user-manual/api/queries.html` |
| Wazuh API (RBAC) | `/user-manual/api/rbac/reference.html` |
| Referensi `ossec.conf` | `/user-manual/reference/ossec-conf/index.html` |
| Agent enrollment dan manajemen | `/user-manual/agent/index.html` |
| Dashboard | `/user-manual/wazuh-dashboard/index.html` |
| Use case threat hunting | `/getting-started/use-cases/threat-hunting.html` |
| Use case incident response | `/getting-started/use-cases/incident-response.html` |

## Perbedaan 4.x dan 5.x yang Paling Mengganggu

| Area | 4.x | 5.x |
|---|---|---|
| Lokasi instalasi manager | `/var/ossec` | `/var/wazuh-manager` |
| Nama skrip active response | `firewall-drop`, `host-deny`, `disable-account` | `block-ip`, `disable-account` |
| Vulnerability detection | modul manager (4.3–4.7) lalu state di indeks (4.8+) | pemindaian sisi server, feed lewat indexer |
| Kontrak JSON active response | tanpa `type`/`stateful_timeout` | dapat menyertakan `type` dan `stateful_timeout` |
| Dokumentasi default (`master`/`current`) | — | mengikuti 5.x |

Konsekuensi praktis: contoh `ossec.conf` atau path dari blog/forum bisa berasal dari 4.x atau 5.x. Selalu cocokkan dengan versi instalasi sebelum menyalin.

## Pemeriksaan Cepat Sebelum Salin Perintah

1. `api_version` atau `wazuh-control info` sesuai dengan panduan?
2. Path yang disebut ada di host? (`/var/ossec/...` vs `/var/wazuh-manager/...`)
3. Skrip active response yang dimaksud ada di `/var/ossec/active-response/bin`?
4. Indeks yang disebut ada? (`GET /_cat/indices/wazuh-*`)
5. Endpoint API disebut masih tersedia di versi ini? (`/vulnerability/{id}` deprecated sejak 4.7)

## Sumber Internal yang Layak Dicatat

| Sumber | Isi |
|---|---|
| `ossec.conf` versi produksi | Konfigurasi efektif; sumber kebenaran, bukan contoh dokumentasi |
| `GET /manager/configuration` | Konfigurasi yang benar-benar dimuat manager |
| `alerts.json` beberapa sampel | Membuktikan field yang benar-benar ada pada deployment Anda |
| Log `ossec.log` saat start | Daftar ruleset/decoder yang berhasil dimuat |

## Best Practices

- Catat versi Wazuh pada laporan triase; instruksi tuning tidak selalu portabel antar versi.
- Simpan tautan dokumentasi versi yang dipakai di wiki internal, bukan tautan `current` yang bergeser.
- Uji setiap contoh konfigurasi di `wazuh-logtest` atau lingkungan non-produksi sebelum diterapkan.
- Bila dokumentasi bertentangan dengan perilaku di instalasi Anda, percayai instalasi, lalu catat perbedaannya untuk tim.
- Perbarui referensi ini setelah upgrade mayor, karena path, nama skrip, dan endpoint dapat berubah.
