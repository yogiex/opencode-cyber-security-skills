---
name: "Anatomi Alert Wazuh"
description: "Alur alert dari agent ke indexer, field inti dan field per-modul pada dokumen alert Wazuh 4.x, perbedaan alerts dan archives, serta batas visibilitas yang membuat bukti tidak pernah sampai ke dashboard."
tags: [wazuh, alert, alerts.json, logall, archives, field, schema, level, log_alert_level, indexer, filebeat, visibility]
---

# Anatomi Alert Wazuh

## Alur dari Event ke Dashboard

```text
agent (logcollector, syscheck, syscollector, sca)
   |  TCP 1514 (event), TCP 1515 (enrollment)
   v
manager: remoted -> analysisd (decode + ruleset) -> alerts.json / alerts.log
   |  (jsonout_output harus yes)
   v
Filebeat modul wazuh -> indexer :9200 -> indeks wazuh-alerts-4.x-YYYY.MM.DD
   |
   v
dashboard :443 (Discover, modul per fitur)
```

| Titik putus | Akibat pada triage |
|---|---|
| `jsonout_output` di `<global>` = `no` | Alert tidak pernah diindeks; dashboard kosong meski `alerts.log` terisi |
| Filebeat berhenti / sertifikat salah | `alerts.json` bertambah, indeks tidak |
| `log_alert_level` default 3 | Rule level 0–2 tidak menghasilkan alert sama sekali |
| Retensi ISM menghapus indeks lama | Bukti hilang; timeline tidak bisa direkonstruksi |
| `logall_json` default `no` | Event tanpa alert tidak tersimpan, hanya tabel yang cocok rule |

## Field Inti Dokumen Alert

| Field | Contoh | Dipakai untuk |
|---|---|---|
| `id` | `1684401234.12345` | ID dokumen di indexer; kunci untuk membuka ulang alert |
| `timestamp` | `2026-11-13T02:15:33.000Z` | Waktu manager (UTC); dipakai sebagai time field |
| `@timestamp` | sama, hasil pipeline | Dipakai untuk kueri DSL; jangan tertukar dengan `timestamp` di dashboard |
| `rule.id` | `5710` | Mengidentifikasi rule; dasar tuning dan change request |
| `rule.level` | `9` | Prioritas; lihat tabel level di `SKILL.md` |
| `rule.description` | `sshd: Attempt to login using a non-existent user` | Ringkasan yang dibaca analis |
| `rule.groups` | `["syslog","sshd","invalid_login"]` | Dasar korelasi dan pencarian kelas alert |
| `rule.frequency` | `3` | Ada bila rule memakai penghitung; artinya alert dipicu setelah N event |
| `rule.mitre` | `{id:"T1110", technique:["Brute Force"], tactic:["Credential Access"]}` | Pemetaan ATT&CK bila rule mendefinisikannya |
| `agent.id` / `agent.name` / `agent.ip` | `003` / `web-01` / `10.0.0.5` | Konteks aset; kunci pengelompokan |
| `manager.name` | `wazuh-manager` | Asal alert bila ada beberapa manager |
| `location` | `/var/log/auth.log` | Sumber log; menentukan modul dan cara verifikasi |
| `decoder.name` | `sshd` | Decoder yang cocok; menentukan field `data.*` yang tersedia |
| `full_log` | `Nov 13 02:15:30 web-01 sshd[2211]: Failed password for invalid user admin ...` | Bukti mentah; sering memuat kredensial/PII |
| `previous_output` | baris sebelumnya | Untuk rule dengan `same_*`/`frequency` |

`full_log` bisa ditekan per rule dengan `no_full_log="yes"`, dan hitungan korelasi disembunyikan dengan `no_counter="yes"`; bila kolom itu kosong pada alert, periksa definisi rule sebelum menyimpulkan log hilang.

## Field per Modul

| Modul | Lokasi / penanda | Field khas |
|---|---|---|
| Windows EventChannel | `location: EventChannel` | `data.win.system.eventID`, `data.win.eventdata.targetUserName`, `.ipAddress`, `.subjectUserName`, `.commandLine`, `.ruleName` |
| FIM (`syscheck`) | `location: syscheck` | `syscheck.path`, `.event` (`added`/`modified`/`deleted`), `.mode`, `.changed_attributes`, `.md5_after`, `.sha256_after`, `.perm_before/after`, `.uname_before/after`, `.audit.*` (who-data) |
| SCA | `location: sca` | `data.sca.scan_id`, `.policy`, `.type: check`, `.check.id`, `.check.title`, `.check.result` (`passed`/`failed`/`not applicable`), `.check.status` + `.reason`, `.check.compliance.*` |
| Vulnerability detection (4.8+) | indeks `wazuh-states-vulnerabilities-*` | `vulnerability.id`, `.severity`, `.detected_at`, `package.name/version`, `agent.id` — **tanpa** `@timestamp` |
| Auditd | `location` berkas audit, decoder `audit` | `data.audit.exe`, `.command`, `.uid`, `.auid`, `.syscall`, `.key` |
| Log aplikasi/web | `location` path log | `data.srcip`, `data.url`, `data.id` (status HTTP pada decoder web) |
| Autentikasi Linux | `/var/log/auth.log` / `/var/log/secure` | `data.srcuser`, `data.dstuser`, `data.srcip`, `data.uid` |

Field `data.*` hanya muncul bila decoder mengisinya. Nama field yang salah tidak menghasilkan error: alert tetap ada, nilainya kosong.

## `alerts` vs `archives`

| | `alerts` | `archives` |
|---|---|---|
| Isi | Hanya event yang memicu rule di atas `log_alert_level` | Semua event yang diterima manager |
| Aktif secara default | Ya | Tidak (`logall`/`logall_json` default `no`) |
| Berkas | `/var/ossec/logs/alerts/alerts.json`, `.log` | `/var/ossec/logs/archives/archives.json`, `.log` |
| Indeks | `wazuh-alerts-*` | `wazuh-archives-*` (butuh Filebeat `archives.enabled: true`) |
| Time field dashboard | `timestamp` | `timestamp` (bukan `@timestamp`) |
| Konsekuensi triage | Bukti hanya untuk event beralert | Satu-satunya cara melihat event yang tidak memicu rule |

Mengaktifkan `logall_json` menambah volume dan kebutuhan disk secara signifikan. Aktifkan hanya bila ada kebutuhan investigasi yang jelas, dan sampaikan biaya retensinya ke pemilik platform.

## Kebersihan Data untuk Triage

| Pertanyaan | Periksa |
|---|---|
| Apakah alert terbaru sampai ke indexer? | `GET /_cat/indices/wazuh-alerts-*?v` dan bandingkan waktu dokumen terakhir |
| Berapa lama bukti disimpan? | Kebijakan ISM pada `wazuh-alerts-*` (hapus berdasarkan `min_index_age`) |
| Apakah agent mengirim log? | Status agent + `logcollector` + modul di `ossec.conf` agent |
| Apakah ada field yang hilang karena decoder? | Bandingkan `decoder.name` alert dengan definisi decoder-nya |
| Apakah alert duplikat? | Satu `id` dokumen = satu alert; beberapa alert untuk satu kejadian berarti rule berlapis |

## Best Practices

- Simpan `id` alert di laporan triase; tanpa itu, alert tidak bisa dibuka ulang setelah retensi berjalan.
- Jangan menyimpulkan "tidak ada aktivitas" dari indeks yang lebih pendek dari rentang investigasi.
- Redaksi `full_log` (kredensial, token, cookie, PII) sebelum masuk tiket atau laporan.
- Bila `rule.mitre` kosong, jangan mengarang teknik ATT&CK; catat bahwa rule tidak memetakannya.
- Bedakan "alert tidak ada" dari "alert tidak sampai ke indexer": keduanya punya jalur perbaikan berbeda.
