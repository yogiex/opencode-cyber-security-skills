---
name: "Kueri Indexer dan Dashboard Wazuh"
description: "Pola indeks Wazuh, kueri Discover dengan time field yang benar, DSL OpenSearch minimum untuk triage, agregasi antrean, batas 10.000 hasil, dan pengaruh retensi terhadap bukti."
tags: [wazuh, indexer, opensearch, dsl, discover, dashboard, wazuh-alerts, timestamp, aggs, retensi, ism]
---

# Kueri Indexer dan Dashboard Wazuh

## Pola Indeks

| Pola | Isi | Time field |
|---|---|---|
| `wazuh-alerts-*` (4.x: `wazuh-alerts-4.x-YYYY.MM.DD`) | Alert yang diproduksi ruleset | `timestamp` di dashboard, `@timestamp` di dokumen |
| `wazuh-archives-*` | Semua event, hanya bila `logall_json` aktif | `timestamp` |
| `wazuh-monitoring-*` | Status koneksi agent per periode | `timestamp` |
| `wazuh-statistics-*` | Statistik manager | `timestamp` |
| `wazuh-states-vulnerabilities-*` | State kerentanan (4.8+) | `vulnerability.detected_at` — **tanpa** `@timestamp` |

Membuat index pattern baru: pilih `timestamp` (bukan `@timestamp`) sebagai time field, atau filter waktu akan tampak kosong.

## Discover: Kueri yang Sering Dipakai

| Tujuan | Kueri DQL |
|---|---|
| Alert satu agent | `agent.id: 003` |
| Alert level tinggi | `rule.level >= 12` |
| Kelas autentikasi gagal | `rule.groups: authentication_failed` |
| Satu sumber IP | `data.srcip: "203.0.113.45"` |
| Satu rule | `rule.id: 5710` |
| FIM jalur kritikal | `syscheck.path: "/etc/passwd"` |
| Windows event tertentu | `data.win.system.eventID: 4625` |
| Kecualikan noise internal | `NOT data.srcip: "10.0.0.0/8"` (pakai filter CIDR eksplisit bila perlu) |

Buka tab **JSON** pada dokumen untuk melihat field mentah; inilah yang harus dipakai saat menulis kueri DSL, bukan label tampilan.

## DSL Minimum untuk Triage

```json
GET wazuh-alerts-*/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        { "range": { "@timestamp": { "gte": "now-24h", "lte": "now" } } },
        { "term": { "rule.level": 10 } },
        { "term": { "agent.id": "003" } }
      ]
    }
  },
  "aggs": {
    "per_rule": {
      "terms": { "field": "rule.id", "size": 20 },
      "aggs": { "per_agent": { "terms": { "field": "agent.name", "size": 10 } } }
    }
  }
}
```

| Kebutuhan | Agregasi |
|---|---|
| Antrean per rule | `terms` pada `rule.id` |
| Antrean per agent | `terms` pada `agent.name` |
| Sumber IP terbanyak | `terms` pada `data.srcip` |
| Tren per jam | `date_histogram` pada `@timestamp` dengan `fixed_interval: "1h"` |
| Nilai unik | `cardinality` |

Catatan teknis:

- `index.max_result_window` default **10.000**; untuk data lebih banyak gunakan `size`+`from` bertahap, `search_after`, atau agregasi — jangan menaikkan window sebagai solusi pertama.
- `size: 0` bila hanya butuh agregasi; ini menghemat waktu dan memori.
- Field `data.*` bertipe dinamis: sebagian bisa `text` (tidak cocok untuk `term`) dan sebagian `keyword`. Bila `term` tidak mengembalikan apa pun padahal datanya ada, periksa tipe field lewat `GET wazuh-alerts-*/_mapping` atau gunakan `match` sementara.

## CLI Indexer

```bash
# Daftar indeks dan ukurannya
curl -k -u <user>:<pass> "https://127.0.0.1:9200/_cat/indices/wazuh-*?v"

# Dokumen terbaru satu agent
curl -k -u <user>:<pass> "https://127.0.0.1:9200/wazuh-alerts-*/_search?size=5&sort=timestamp:desc" \
  -H 'Content-Type: application/json' \
  -d '{"query":{"term":{"agent.id":"003"}}}'
```

Gunakan `-k` hanya untuk sertifikat self-signed; untuk produksi, pasang CA dan hilangkan `-k`.

## Retensi dan Kelengkapan Bukti

| Yang menentukan | Dampak |
|---|---|
| Kebijakan ISM pada `wazuh-alerts-*` | Bukti hilang setelah `min_index_age`; timeline panjang tidak mungkin |
| Rotasi harian indeks | Kueri lintas hari menyentuh banyak indeks; sebutkan rentang eksplisit |
| `logall_json` mati | Tidak ada `wazuh-archives-*`; event tanpa alert tidak bisa dicari |
| `jsonout_output` mati | Alert tidak pernah sampai ke indexer |

Sebelum menyatakan "tidak ada aktivitas", pastikan indeks untuk rentang yang dimaksud masih ada.

## Best Practices

- Selalu sebutkan rentang waktu eksplisit pada laporan; "kemarin" bukan rentang yang auditable.
- Simpan kueri yang terbukti berguna sebagai saved search agar shift berikutnya tidak menulis ulang.
- Gunakan `agent.id` (stabil) sebelum `agent.name` (bisa berubah) untuk korelasi.
- Jangan menyalin seluruh hasil kueri ke tiket; ambil dokumen yang relevan dan redaksi.
