---
name: "Wazuh API dan Otomasi Triage"
description: "Autentikasi JWT, RBAC, WQL, paginasi, dan endpoint Wazuh API yang dipakai saat triage, serta cara memakai dua skrip pendamping tanpa menyimpan kredensial."
tags: [wazuh, api, jwt, rbac, wql, paginasi, agents, syscollector, syscheck, sca, active-response, otomasi]
---

# Wazuh API dan Otomasi Triage

## Autentikasi

```bash
# Token mentah (paling mudah untuk skrip shell)
TOKEN=$(curl -s -k -u wazuh:wazuh -X POST \
  "https://127.0.0.1:55000/security/user/authenticate?raw=true")

# Token JSON
curl -s -k -u wazuh:wazuh -X POST \
  "https://127.0.0.1:55000/security/user/authenticate"

curl -s -k -X GET "https://127.0.0.1:55000/agents?limit=5" \
  -H "Authorization: Bearer $TOKEN"
```

| Fakta | Nilai default | Implikasi triage |
|---|---|---|
| Masa berlaku token | 900 detik | Login ulang di awal sesi kerja; 401 bukan berarti akun rusak |
| `request_timeout` | 10 detik | Operasi lambat (`upgrade`, AR massal) butuh `wait_for_complete` |
| Rate limit | ±300 permintaan/menit | Batch dengan `limit`, jangan loop satu-per-satu |
| Percobaan login | 50 per 300 detik | Jangan menaruh login di dalam loop |
| Kredensial default | `wazuh:wazuh` / dari `wazuh-install-files.tar` | Ganti sebelum dipakai produksi |

Kredensial hanya dari variabel lingkungan atau *secret manager*; jangan menempelkan token/password ke skrip, laporan, atau riwayat shell.

## Bentuk Respons

```json
{
  "data": {
    "affected_items": [ ... ],
    "total_affected_items": 42,
    "failed_items": [ ... ],
    "total_failed_items": 0
  },
  "message": "All selected agents information was returned",
  "error": 0
}
```

| Kode | Arti | Tindakan triage |
|---|---|---|
| HTTP 200 + `error: 0` | Sukses penuh | Lanjut |
| HTTP 200 + `error: 2` | Sukses parsial (sebagian item gagal) | Periksa `failed_items`; jangan anggap data lengkap |
| HTTP 401 | Kredensial/JWT tidak valid atau kedaluwarsa | Login ulang, baru curiga masalah akun |
| HTTP 403 + `error: 4000` | Token valid, RBAC kurang | Minta role, jangan mengulang |
| HTTP 403 kode lain | IP diblokir / kebijakan | Cek konfigurasi API |

## Endpoint yang Relevan

| Endpoint | Method | Kegunaan triage | Catatan |
|---|---|---|---|
| `/agents` | GET | Daftar agent, filter status/OS | `limit`, `offset`, `select`, `q`, `sort`, `search` |
| `/agents/{id}` | GET | Detail satu agent | Termasuk status koneksi |
| `/agents/summary/status` | GET | Ringkasan active/disconnected | Cepat untuk cek telemetri |
| `/syscollector/{id}/os` | GET | OS dan versi | Bukti konteks dasar |
| `/syscollector/{id}/processes` | GET | Snapshot proses | Bukan real-time |
| `/syscollector/{id}/ports` | GET | Port mendengarkan | Untuk exposure CVE |
| `/syscollector/{id}/packages` | GET | Paket terpasang | Untuk verifikasi CVE |
| `/syscollector/{id}/hotfixes` | GET | Patch Windows | Khusus Windows |
| `/syscheck/{id}` | GET | Hasil FIM terakhir | `search`, `hash`, `file` |
| `/syscheck/{id}/last_scan` | GET | Waktu scan FIM | Menentukan kesegaran bukti |
| `/sca/{id}` | GET | Hasil SCA per policy | Termasuk `score` |
| `/sca/{id}/checks/{policy_id}` | GET | Check detail satu policy | Untuk bukti temuan |
| `/vulnerability/{id}` | GET | Kerentanan per agent | **Deprecated sejak 4.7**; gunakan indeks state |
| `/manager/logs` | GET | Log manager | Untuk mendiagnosis rule/ruleset |
| `/manager/status` | GET | Status daemon | Cek process daemon yang mati |
| `/manager/configuration` | GET | Konfigurasi efektif | `section` untuk mempersempit |
| `/rules`, `/decoders` | GET | Metadata ruleset | Untuk memeriksa definisi rule |
| `/cluster/nodes` | GET | Node cluster | All-in-one hanya satu node |
| `/active-response` | PUT | Jalankan AR | Butuh RBAC khusus; **bukan** operasi baca |

`GET /agents` dan beberapa list endpoint mengembalikan hanya item yang boleh dibaca; menyebut resource spesifik yang tidak diizinkan menghasilkan 403, bukan daftar kosong.

## WQL (Parameter `q`)

| Operator | Arti |
|---|---|
| `=` | sama dengan |
| `!=` | tidak sama |
| `<`, `>` | perbandingan |
| `~` | like |
| `()` | pengelompokan |
| `;` | AND |
| `,` | OR |

```bash
# Agent aktif bersistem Linux
curl -G --data-urlencode "q=status=active;os.name=ubuntu" \
  -k "https://127.0.0.1:55000/agents" -H "Authorization: Bearer $TOKEN"

# ID lebih kecil 4 dan nama mengandung "web"
curl -G --data-urlencode "q=id<4;name~web" \
  -k "https://127.0.0.1:55000/agents" -H "Authorization: Bearer $TOKEN"
```

`;` harus di-URL-encode menjadi `%3B` bila tidak memakai `--data-urlencode`. Panjang `q`/`search` dibatasi ±1024 karakter, `select` ±100 field.

## RBAC untuk Triage

| Kebutuhan | Role/policy |
|---|---|
| Membaca agent, syscheck, syscollector, SCA, rules, decoders | `readonly` atau role kustom read-only |
| Menjalankan active response | Policy `agents_commands_*` / aksi `active-response:command` — **tidak** diberikan oleh role read-only |
| Restart manager | Aksi manajemen cluster/manager |

Skrip harus gagal dengan pesan jelas ketika 403, bukan mencoba ulang atau menurunkan operasi menjadi "diam-diam tidak jalan".

## Memakai Skrip Pendamping

```bash
# Konteks lengkap satu agent (read-only)
python scripts/wazuh_api.py agent 003

# Daftar agent dengan filter WQL
python scripts/wazuh_api.py agents --q "status=active" --limit 100

# Log manager yang menyebut rule tertentu
python scripts/wazuh_api.py logs --search 100200

# Mutasi hanya dengan flag eksplisit
python scripts/wazuh_api.py restart --apply --yes
```

| Variabel lingkungan | Default |
|---|---|
| `WAZUH_API_URL` | `https://127.0.0.1:55000` |
| `WAZUH_API_USER` | — (wajib) |
| `WAZUH_API_PASS` | — (wajib) |
| `WAZUH_API_VERIFY` | `1` (verifikasi TLS; `0` = self-signed) |

## Best Practices

- Ambil `error: 2` sebagai sinyal untuk memeriksa `failed_items`; jangan menyimpulkan kelengkapan dari `total_affected_items` saja.
- Batasi `select` pada field yang dipakai agar respons kecil dan cepat.
- Simpan token di memori proses, bukan berkas, dan jangan masuk ke log.
- Jangan menjalankan active response dari skrip ad-hoc; gunakan jalur yang tercatat (lihat [active-response.md](./active-response.md)).
- Untuk data volume besar (alert, state kerentanan), pakai indexer — API manager dirancang untuk operasi, bukan analitik.
