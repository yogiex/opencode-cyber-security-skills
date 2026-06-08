---
name: "Containment Strategies & Evidence Gathering"
description: "Containment dilemma, containment types by incident, decision framework, short-term vs long-term containment, critical mistakes, order of volatility, chain of custody, forensic acquisition methods, forensic readiness, and evidence documentation."
tags: [ecih, containment, evidence, forensics, chain-of-custody, order-of-volatility, forensic-readiness]
---

## Containment Strategies — Stop the Bleeding

### Esensi Containment

Containment adalah **tindakan menghentikan penyebaran insiden dan membatasi kerusakan**. Ini adalah stage paling kritis karena setiap detik delay berarti attacker punya lebih banyak waktu untuk bergerak.

### Containment Dilemma

```
Cepat ───────────────────────── Akurat
   │                                │
   │  Disconnect power              │
   │  (kehilangan memory evidence)  │
   │                                │
   │  Isolate network               │
   │  (tapi proses masih jalan)     │
   │                                │
   │  Take memory dump dulu         │
   │  (tapi butuh waktu)            │
   │                                │
```

**Golden rule**: Ambil volatile evidence dulu sebelum containment penuh jika memungkinkan. TAPI: jika risiko penyebaran sangat tinggi, containment dulu, evidence kemudian.

### Jenis Containment

| Jenis | Deskripsi | Kapan Digunakan |
|-------|-----------|-----------------|
| **Network Isolation** | Putuskan koneksi network | Aktif C2, lateral movement |
| **Endpoint Isolation** | Isolasi dari network (EDR quarantine) | Malware pada endpoint |
| **Account Disable** | Nonaktifkan user account | Account compromise |
| **Service Stop** | Hentikan service yang terkompromi | Web shell, backdoor service |
| **Firewall Block** | Block IP/domain di perimeter | C2, DDoS, scanning |
| **VM Snapshot/Stop** | Snapshot VM, lalu stop | Forensic preservation |
| **DNS Sinkhole** | Redirect malicious domain | Botnet, malware C2 |
| **Rate Limiting** | Batasi traffic ke sistem | DDoS, brute force |

### Containment Decision Framework

```
Tentukan jenis insiden
       │
       ▼
Apa risiko penyebaran?
  ├── Tinggi → Segera isolasi (evidence sekunder)
  └── Rendah → Kumpulkan evidence dulu
       
Apa yang bisa diisolasi?
  ├── Satu endpoint → Isolasi endpoint
  ├── Satu segment → Isolasi segment
  └── Seluruh network → Pilihan sulit, perlu executive decision
  
Apakah containment akan merusak evidence?
  ├── Ya → Dokumentasi apa yang diubah, kumpulkan sebanyak mungkin dulu
  └── Tidak → Lanjut containment

Apakah containment akan mengganggu bisnis?
  ├── Ya → Informasikan stakeholder, dapatkan approval
  └── Tidak → Lanjut containment

Apakah containment temporary atau permanent?
  ├── Temporary → Siapkan permanent fix di parallel
  └── Permanent → Lanjut ke eradication
```

### Short-term vs Long-term Containment

| Aspek | Short-term | Long-term |
|-------|-----------|-----------|
| **Tujuan** | Stop immediate threat | Maintain operations safely |
| **Contoh** | Disconnect network cable | Apply firewall rules, ACLs |
| **Kecepatan** | Seconds-minutes | Hours-days |
| **Dampak** | High (shutdown) | Low (restricted but running) |
| **Sustainabilitas** | Not sustainable | Sustainable |
| **Evidence preservation** | Poor | Better |

### Containment by Incident Type

**Ransomware**:
1. Segera isolasi endpoint dari network
2. Disable semua share yang terkena
3. Block known ransomware extensions di perimeter
4. Jangan bayar tebusan (keputusan management)
5. Ambil screenshot ransom note sebagai evidence

**Data Breach**:
1. Identifikasi vector exfiltration
2. Block vector exfiltration (disable USB, block upload, revoke access)
3. Isolasi database/sistem yang bocor
4. Reset credentials sistem terdampak
5. Audit akses recent untuk identifikasi scope

**Account Compromise**:
1. Disable atau force reset password akun
2. Revoke semua sessions/tokens
3. Check mailbox rules (forwarding, auto-reply)
4. Check recent activity (email sent, files accessed)
5. Enable MFA setelah remediasi

**Malware**:
1. Isolasi endpoint dari network
2. Kill malicious processes
3. Remove persistence mechanisms
4. Check for lateral movement indicators
5. Scan timeline untuk infection point

**Insider Threat**:
1. Disable akses secara diam-diam (jangan trigger)
2. Preserve evidence dari system dan user activity
3. Koordinasi dengan HR sebelum konfrontasi
4. Jangan konfrontasi sendiri
5. Dokumentasi semua tindakan

**DDoS**:
1. Contact ISP/provider untuk upstream filtering
2. Enable rate limiting di WAF/CDN
3. Blackhole routing jika perlu
4. Scale infrastructure jika memungkinkan
5. Analisis traffic pattern untuk filtering rules

### Critical Containment Mistakes

| Mistake | Dampak |
|---------|--------|
| **Shutdown tanpa memory capture** | Kehilangan volatile evidence |
| **Menginfeksi IR workstation** | IR team kehilangan capacity |
| **Contain di level yang salah** | Attacker pindah ke sistem lain |
| **Tidak dokumentasi containment** | Tidak bisa rekonstruksi nanti |
| **Mengomunikasikan containment ke attacker** | Attacker menghilangkan bukti |
| **Contain tanpa BIA** | Shutdown sistem non-kritis secara tidak perlu |

---

## Evidence Gathering & Forensic Readiness

### Esensi Evidence Gathering

Evidence Gathering adalah **proses sistematis mengumpulkan dan mengamankan bukti digital** sesuai standar hukum sehingga bisa digunakan untuk investigasi internal, tindakan hukum, atau regulatory reporting.

### Order of Volatility

Evidence harus dikumpulkan dari yang paling volatile ke yang paling persistent:

```
Paling Volatile
     │
     ▼
  1. Register, Cache, Memory (RAM)
  2. Network Connections, Process Table
  3. Kernel Statistics, Kernel Modules
  4. Temporary File Systems (/tmp)
  5. Disk (Hard Drive, SSD)
  6. Remote Logs, Backups
  7. Physical Configuration, Hardware
     │
     ▼
Paling Persistent
```

**Mengapa order ini penting?** Data yang paling volatile hilang paling cepat. Matikan listrik, memory hilang. Matikan proses, koneksi network hilang. Evidence yang paling mudah hilang harus dikumpulkan pertama.

### Chain of Custody

Chain of Custody adalah **dokumentasi setiap orang yang menangani evidence** dari saat pengumpulan hingga persidangan. Setiap transfer harus dicatat:

| Field | Deskripsi |
|-------|-----------|
| **Evidence ID** | Unique identifier |
| **Description** | Apa evidence ini |
| **Collected by** | Siapa yang mengumpulkan |
| **Date/Time** | Kapan dikumpulkan |
| **Location** | Dari mana dikumpulkan |
| **Acquired from** | Sistem/device asal |
| **Hash (MD5/SHA1/SHA256)** | Hash sebelum transfer |
| **Transferred to** | Siapa penerima |
| **Transfer date/time** | Kapan ditransfer |
| **Purpose of transfer** | Analisis? Penyimpanan? Pengadilan? |
| **Return date/time** | Kapan dikembalikan |
| **Status** | Intact / Modified / Analyzed |

**Golden rules Chain of Custody**:
- Satu orang bertanggung jawab pada satu waktu
- Setiap transfer harus ditandatangani
- Hash dihitung sebelum dan sesudah analisis (pastikan tidak berubah)
- Simpan evidence di tempat aman dengan akses terbatas
- Dokumentasi semua tindakan yang dilakukan pada evidence

### Jenis Evidence Digital

| Kategori | Contoh | Volatility |
|----------|--------|-----------|
| **Volatile** | RAM, processes, network connections | High |
| **Non-volatile** | Hard drive, SSD, USB | Low |
| **Network** | PCAP, netflow, firewall logs | Medium |
| **Log** | Event logs, syslog, audit logs | Medium-low |
| **Application** | Database, web server, email | Medium |
| **Cloud** | Cloud trail, API logs, bucket logs | Medium |
| **Mobile** | SMS, call logs, app data, location | High |

### Forensic Acquisition Methods

| Metode | Deskripsi | Kapan Digunakan |
|--------|-----------|-----------------|
| **Live acquisition** | Kumpulkan data dari sistem menyala | Sistem kritis tidak bisa di-shutdown |
| **Dead acquisition** | Matikan sistem dulu, baru image disk | Forensic best practice |
| **Logical acquisition** | Kumpulkan file spesifik | Targeted investigation |
| **Physical acquisition** | Bit-for-bit copy seluruh media | Court-admissible evidence |
| **Network acquisition** | Capture network traffic | Real-time investigation |
| **Memory acquisition** | Dump RAM | Malware analysis, rootkit detection |

### Forensic Readiness

Forensic readiness adalah **kesiapan organisasi untuk mengumpulkan evidence secara efektif SEBELUM insiden terjadi**.

**Komponen Forensic Readiness**:

| Komponen | Implementasi |
|----------|--------------|
| **Logging yang adequate** | Semua source log, retention sesuai kebutuhan |
| **Time synchronization** | Semua sistem pakai NTP, source sama |
| **Write blockers** | Hardware/software write blocker untuk imaging |
| **Forensic workstation** | Dedicated machine dengan forensic tools |
| **Evidence storage** | Secure storage dengan akses terbatas |
| **Trained personnel** | Tim yang bisa melakukan acquisition |
| **Policies** | Kebijakan yang mendukung forensic collection |
| **Chain of Custody forms** | Template siap pakai |
| **Hash database** | Known good file hashes (NSRL) |

**Praktik Baik Logging untuk Forensik**:

| Log Source | Durasi Minimum | Detail |
|-----------|----------------|--------|
| Authentication logs | 1 tahun | Successful + failed logins |
| System event logs | 6 bulan | Process creation, service changes |
| Network logs | 3-6 bulan | Connections, DNS, proxy |
| Application logs | 6-12 bulan | Access, errors, transactions |
| Database logs | 1 tahun | Queries, schema changes |
| Cloud logs | 1-2 tahun | API calls, configuration changes |
| Email logs | 1 tahun | Send/receive, attachment |

### Dokumentasi Evidence

Setiap evidence harus didokumentasikan dengan:
1. **Evidence ID** — Unique identifier untuk tracking
2. **Description** — What is this evidence
3. **Source** — Sistem mana, lokasi di sistem
4. **Acquisition method** — Bagaimana dikumpulkan
5. **Acquisition tool** — Tools yang digunakan
6. **Hash value** — SHA256 hash of acquired data
7. **Timestamp** — When acquired (UTC)
8. **Collector** — Who collected it
9. **Witnesses** — Siapa yang menyaksikan (jika untuk pengadilan)
10. **Location** — Di mana evidence disimpan
