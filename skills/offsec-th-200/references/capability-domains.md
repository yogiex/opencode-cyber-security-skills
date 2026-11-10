---
name: "Capability Domains — Peta Kompetensi Threat Hunter"
description: "Peta tujuh domain kapabilitas threat hunter — konsep dan siklus hunt, lanskap aktor, komunikasi temuan, hunting data jaringan, hunting endpoint, hipotesis tanpa IOC, dan hunting di cloud — beserta bukti yang membuktikan tiap domain."
tags: [capability-map, domains, hunting, threat-actor, reporting, network, endpoint, cloud, azure, maturity]
---

# Capability Domains

Tujuh domain di bawah adalah peta kemampuan yang melekat pada persona ini. Ini bukan silabus yang dihafal berurutan, melainkan daftar "kalau pertanyaannya di sini, ini yang saya kuasai dan ini buktinya". Penomoran hanya untuk rujukan, bukan urutan materi; urutan pengerjaan ditentukan hipotesis, bukan bab.

## Peta domain

| # | Domain | Kapabilitas inti | Bukti khas |
|---|---|---|---|
| 1 | Konsep & siklus hunt | definisi hunting, mindset, maturity model, siklus hunt | hipotesis tertulis, catatan hunt, metrik hunt |
| 2 | Lanskap aktor | nation-state/APT, eCrime, hacktivist, insider, ekosistem ransomware | pemetaan TTP ke ATT&CK, profil aktor di intel brief |
| 3 | Komunikasi & laporan | TLP, struktur hunt narrative, penyesuaian audiens | laporan hunt, ringkasan eksekutif, IOC table |
| 4 | Hunting data jaringan | NetFlow, DNS, proxy, Suricata, Zeek, firewall, PCAP | query beaconing, temuan DNS tunneling |
| 5 | Hunting endpoint | Sysmon, Windows Event Log, Falcon (process tree, command line) | timeline host, rekonstruksi process tree |
| 6 | Hunting tanpa IOC | analisis perilaku, deviasi baseline, identifikasi TTP | hipotesis perilaku, temuan tanpa indikator |
| 7 | Hunting di cloud (Azure) | AAD sign-in log, Activity log, Defender, KQL | query sign-in, temuan cloud TTP |

## Kelompok kerja

### Fondasi (1, 2, 3)

Tiga domain pertama membuat hunt bisa dimulai dan bisa selesai: tahu apa yang sedang dicari, tahu siapa yang mungkin melakukannya, dan tahu bagaimana hasilnya disampaikan. Hunt yang tidak punya ketiganya berhenti sebagai eksplorasi pribadi yang tidak bisa dipakai orang lain.

### Telemetri (4, 5)

Di sinilah bukti berada. Jaringan memberi konteks lintas host dan batas estate; endpoint memberi penyebab dan urutan kejadian. Keduanya saling melengkapi dan jarang sepakat sepenuhnya — selisihnya sering justru petunjuk paling berguna.

### Pergeseran ke perilaku dan cloud (6, 7)

Dua domain terakhir menandai pergeseran dari indikator ke perilaku, dan dari estate on-prem ke identitas. Keduanya menuntut baseline yang lebih matang karena tidak ada daftar IOC yang bisa diikuti.

## 1. Konsep dan siklus hunt

**Definisi kerja:** pencarian proaktif terhadap ancaman yang lolos dari kontrol yang sudah ada. Mindset yang dibutuhkan: rasa ingin tahu, kreativitas, dan ketelitian analitis — bukan kecepatan menutup tiket.

**Tipe hunt:** intel-based (memakai IOC yang diketahui), hypothesis-driven (berdasarkan TTP), dan baseline/anomaly (deviasi dari normal). Ketiganya dipakai bergantian dalam satu hunt.

**Maturity model:**

| Level | Nama | Ciri |
|---|---|---|
| 1 | Initial | ad-hoc, tergantung inisiatif individu |
| 2 | Defined | terstruktur, ada prosedur dan dokumentasi |
| 3 | Managed | digerakkan metrik, ada evaluasi hasil |
| 4 | Optimizing | dibantu otomasi/AI, deteksi ikut berevolusi |

**Siklus hunt:** Trigger → Hypothesis → Data Collection → Analysis → Findings → Response → Feedback. Siklus berulang; feedback yang menjadi trigger berikutnya adalah tanda hunt benar-benar berjalan.

## 2. Lanskap aktor

| Tipe | Motivasi | Contoh |
|---|---|---|
| Nation-State (APTs) | Espionage, sabotage | APT29, APT41, Lazarus |
| Cybercrime / eCrime | Financial gain | LockBit, CLOP, BlackCat |
| Hacktivists | Ideological | Anonymous, Killnet |
| Insider Threats | Financial, revenge | Karyawan tidak puas dengan akses sah |

**Ekosistem ransomware:** Initial Access Brokers → Ransomware Group → Affiliates (data exfiltration, negosiasi, operator leak site). Peran ini terpisah, jadi indikator di satu tahap sering tidak muncul di tahap lain.

**LockBit 3.0:** RaaS; initial access lewat RDP brute force, phishing, atau kerentanan VPN; enkripsi AES+RSA; alat eksfiltrasi StealBit; pergerakan lateral dengan PsExec.

**CLOP:** dikenal karena eksploitasi MOVEit Transfer (2023), deployment web shell, dan eksfiltrasi data lewat HTTP.

**BlackCat/ALPHV:** ransomware berbasis Rust pertama, model RaaS, initial access lewat VPN/phishing, enkripsi multi-threaded.

**Kelompok APT:** APT29 (Rusia/SVR, PowerShell + C2 lewat cloud), APT41 (China, DLL side-loading), Lazarus (Korea Utara, malware macOS), MuddyWater (Iran, VBS + living-off-the-land), FIN7 (Rusia, backdoor Carbanak).

Rantai serangan lengkap per aktor beserta indikator tiap fase ada di [case-studies.md](./case-studies.md).

## 3. Komunikasi dan laporan

**Traffic Light Protocol (TLP):**

| Label | Boleh dibagikan ke |
|---|---|
| RED | individu tertentu saja |
| AMBER | organisasi sendiri |
| GREEN | komunitas terbatas |
| CLEAR | publik |

**Struktur hunt narrative:** Executive Summary → Hypothesis & Methodology → Data Sources → Findings → Impact Assessment → IOCs Table → Recommendations → MITRE ATT&CK Mapping. Template kerja ada di [report-template.md](../assets/report-template.md).

**Audiens dan isi:** manajemen butuh dampak bisnis; SOC butuh detail teknis dan query; IT butuh sistem dan patch; legal butuh implikasi regulasi. Satu laporan untuk semua audiens biasanya tidak berguna untuk siapa pun.

Jenis laporan intel (strategic, operational, tactical, technical) beserta karakteristiknya ada di [ti-integration.md](./ti-integration.md).

## 4. Hunting data jaringan

**Sumber data:** NetFlow/IPFIX, DNS log, proxy log, IDS/IPS (Suricata), firewall log, PCAP, NetWitness.

**Suricata:** IDS/IPS open-source berbasis rule; deteksi per protokol (HTTP, DNS, TLS, SMB); ekstraksi file dari aliran jaringan.

**Zeek (dulu Bro):** conn.log, dns.log, http.log, ssl.log, files.log.

**Skenario kunci:** deteksi C2 lewat analisis frekuensi beaconing, DNS tunneling lewat query domain panjang, eksfiltrasi data lewat transfer keluar berukuran besar, dan triase alert Suricata. Query siap pakai ada di [network-hunting.md](./network-hunting.md).

## 5. Hunting endpoint

**Sumber data:** Sysmon (process, network, file, registry), Windows Event Log (4624, 4625, 4688, 4104, 7045), CrowdStrike Falcon (process tree, command line).

**Intel-based:** cari IOC spesifik — hash, IP, domain, registry key — di seluruh log endpoint.

**Hypothesis-driven:** parent-child mencurigakan (Office memunculkan PowerShell), pergerakan lateral (logon type 3), persistence (pembuatan service non-Microsoft).

Detail Event ID dan pola query ada di [endpoint-hunting.md](./endpoint-hunting.md) dan [crowdstrike-cql.md](./crowdstrike-cql.md).

## 6. Hunting tanpa IOC

**Analisis perilaku:** fokus pada perilaku, bukan indikator; deviasi dari baseline; identifikasi TTP. Ini yang membuat hunt tetap berjalan ketika daftar IOC dari intel brief sudah habis.

**Behavioral hunt di Falcon:** parent-child tidak lazim, jalur eksekusi mencurigakan (`AppData\Local\Temp`), dan deteksi beaconing.

**Hipotesis tanpa IOC:** "Jika penyerang sudah menguasai DC, ia akan membuat domain admin (4720+4728), melakukan DCSync (4662), dan mengambil NTDS.dit" — lalu cari ketiga perilaku itu, bukan menunggu indikator.

## 7. Hunting di cloud (Azure)

**Sumber data Azure:** Azure AD sign-in log, Activity log, Security Center alert, Microsoft 365 Defender.

**KQL untuk Azure:**

```
SigninLogs | where ResultType != "0"
| summarize FailedCount = count() by UserPrincipalName, IPAddress
| where FailedCount > 10
```

**TTP khas cloud:** T1078.004 (Cloud Account), T1525 (Implant Internal Image), T1613 (Container Discovery), T1530 (Cloud Storage Data).

KQL di sini adalah bahasa query Azure/Microsoft 365, bukan SPL dan bukan CQL Falcon. Untuk deteksi reaktif berbasis ELK/KQL, skill yang tepat adalah `offsec-soc-200`.

## Latihan mandiri

Bangun estate kecil dengan telemetri yang lengkap — satu SIEM, satu EDR, satu sensor jaringan — lalu rekam aksi penyerang terkontrol di dalamnya. Jalankan hunt end-to-end dari hipotesis sampai narasi, dan bandingkan temuan dengan hipotesis awal. Mulai dari satu hipotesis, bukan dari seluruh ATT&CK; latihan yang selesai lebih berguna daripada cakupan yang luas tetapi tidak pernah ditutup.

## Cara memakai peta ini

1. **Saat menerima pertanyaan hunt** — petakan ke satu atau dua domain; jangan memaksakan semua domain relevan.
2. **Saat memilih langkah pertama** — tanyakan domain mana yang paling murah memberi bukti pemalsu.
3. **Saat melapor** — sebut domain, hipotesis, dan buktinya; bukan nama alat yang dipakai.
4. **Saat menilai diri** — domain tanpa bukti nyata adalah domain yang belum dikuasai.

## Best Practices

- Pilih domain berdasarkan hipotesis, bukan berdasarkan alat yang paling nyaman.
- Satu query yang menjawab pertanyaan lebih bernilai daripada lima dashboard yang tidak dibaca.
- Simpan bukti per domain; itu bahan laporan sekaligus evaluasi cakupan.
- Domain 7 sering butuh koordinasi pemilik identitas/cloud sebelum tindakan, bukan sesudahnya.
