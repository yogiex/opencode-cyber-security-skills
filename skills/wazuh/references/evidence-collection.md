---
name: "Pengumpulan Bukti Triage"
description: "Checklist bukti yang diambil saat triage alert Wazuh: urutan termurah lebih dulu, pemetaan pertanyaan ke sumber data, batas waktu per kelas alert, dan sumber yang dianggap independen."
tags: [wazuh, evidence, triage, syscollector, syscheck, sca, full_log, bukti, checklist, korelasi]
---

# Pengumpulan Bukti Triage

## Aturan Bukti

- **Dua sumber independen** sebelum verdict: alert (manager/indexer) + telemetri agent (syscollector, syscheck, SCA, log sumber).
- **Urutan termurah lebih dulu**: alert → konteks agent → log sumber → korelasi → enrichment. Jangan mulai dari enrichment IoC.
- **Snapshot bukan real-time**: syscollector melaporkan keadaan pada scan terakhir; proses yang sudah mati bisa tidak terlihat, dan proses baru bisa belum tercatat. Sebutkan keterbatasan ini di laporan.
- **Bukti harus bisa diambil ulang**: catat endpoint, filter, dan rentang waktu yang dipakai.

## Urutan Pengambilan

| Langkah | Pertanyaan | Sumber | Perintah / lokasi |
|---|---|---|---|
| 1 | Apa yang memicu? | Alert | `full_log`, `rule.*`, `decoder.name` |
| 2 | Host apa dan sejak kapan aktif? | Manager API | `GET /agents?q=id=003`, `GET /agents/summary/status` |
| 3 | Sistem apa? | Manager API | `GET /syscollector/003/os` |
| 4 | Proses/port/paket saat itu? | Manager API | `GET /syscollector/003/processes`, `/ports`, `/packages` |
| 5 | Ada perubahan file? | Manager API / alert | `GET /syscheck/003`, alert `syscheck.*` |
| 6 | Konfigurasi menyimpang? | Manager API | `GET /sca/003` |
| 7 | Ada CVE relevan? | Indexer / API | `wazuh-states-vulnerabilities-*`, `GET /vulnerability/003` (deprecated 4.7) |
| 8 | Apa lagi yang terjadi di sekitar waktu itu? | Indexer | timeline `agent.id` pada window |
| 9 | Apakah alert lain terkait? | Indexer | kueri `rule.groups`, `data.srcip`, `agent.ip` |
| 10 | Apakah indikator ini dikenal? | CDB / intel | list lokal, `threat-intelligence` untuk konteks |

## Checklist per Kelas Alert

### Autentikasi Linux / SSH

| Bukti | Cara |
|---|---|
| User yang dicoba (valid/invalid) | `full_log`, `data.dstuser` |
| Sumber IP | `data.srcip` |
| Jumlah percobaan dan rentang waktu | korelasi `data.srcip` + `rule.groups: authentication_failed` |
| Apakah ada login sukses setelahnya | cari `rule.groups: authentication_success` dari IP/user sama |
| Apakah user itu ada | syscollector users, atau log `invalid user` |

### Autentikasi Windows

| Bukti | Cara |
|---|---|
| Event ID | `data.win.system.eventID` (4625 gagal, 4624 sukses, 4672 privilege, 4688 proses) |
| Akun target dan subjek | `data.win.eventdata.targetUserName`, `.subjectUserName` |
| Logon type | `data.win.eventdata.logonType` (3 jaringan, 10 RDP, 2 interaktif) |
| IP sumber | `data.win.eventdata.ipAddress` |
| Proses setelah login | `data.win.eventdata.commandLine`, event 4688 pada window sama |

### FIM (syscheck)

| Bukti | Cara |
|---|---|
| Path dan jenis perubahan | `syscheck.path`, `syscheck.event` |
| Atribut yang berubah | `syscheck.changed_attributes` |
| Isi perubahan | `syscheck.diff` (hanya bila `report_changes="yes"`) |
| Hash sebelum/sesudah | `syscheck.md5_after`, `.sha256_after` |
| Siapa yang mengubah | `syscheck.audit.*` (hanya bila who-data aktif) |
| Proses yang menulis | korelasi auditd/4688 pada window |

### Malware / YARA / VirusTotal

| Bukti | Cara |
|---|---|
| File yang ditandai | `syscheck.path` atau `data.virustotal.*` |
| Hash | `syscheck.sha256_after`, kirim ke intel pihak ketiga bila diizinkan |
| Proses induk | syscollector processes, event 4688 |
| Koneksi keluar | syscollector ports/netaddr, log firewall/proxy |

### Web / Aplikasi

| Bukti | Cara |
|---|---|
| URL dan parameter | `data.url`, `data.id` (status), `full_log` |
| Sumber IP dan user agent | `data.srcip`, `full_log` |
| Pola serupa sebelumnya | kueri `rule.groups` + `data.srcip` pada 7 hari |
| Apakah berhasil | status respons, log aplikasi, perubahan file |

### CVE / SCA

| Bukti | Cara |
|---|---|
| CVE, severity, paket | state kerentanan, `data.vulnerability.*` (4.3–4.7) atau indeks state (4.8+) |
| Apakah paket masih terpasang | syscollector packages |
| Exposure | apakah layanan mendengarkan port terkait (syscollector ports) |
| Check SCA yang gagal | `data.sca.check.result`, `data.sca.check.compliance` |

## Batas Waktu

| Kelas | Waktu maksimum pengumpulan bukti |
|---|---|
| Level 3–7 | 5 menit; setelah itu putuskan tutup/monitor |
| Level 8–11 | 15 menit |
| Level 12+ | 10 menit untuk bukti awal, sisanya sambil eskalasi berjalan |
| Investigasi L2 | 2 jam sebelum update status ke pemilik insiden |

## Sumber Independen: Apa yang Dihitung

| Kombinasi | Independen? | Alasan |
|---|---|---|
| Alert + `full_log` | Tidak | `full_log` adalah bagian dari alert yang sama |
| Alert + syscollector | Ya | Data berbeda, jalur pengumpulan berbeda |
| Alert + log sumber (auth.log, EventChannel) | Ya, bila masih tersedia | Membuktikan log benar-benar ada di host |
| Alert + aturan rule di ruleset | Tidak | Itu membaca logika deteksi, bukan kejadian |
| Dua alert dari rule berbeda pada event sama | Sebagian | Sering satu event, dua rule berlapis |

## Best Practices

- Tuliskan bukti yang **tidak** tersedia beserta alasannya; ketiadaan bukti adalah temuan, bukan kekosongan laporan.
- Hindari mengirim hash atau IP ke layanan eksternal bila kebijakan data melarangnya; catat keputusan itu.
- Simpan potongan log seperlunya, bukan seluruh `full_log`, dan redaksi sebelum dibagikan.
- Bila bukti saling bertentangan, jangan memilih yang paling nyaman; catat kontradiksinya dan eskalasi.
