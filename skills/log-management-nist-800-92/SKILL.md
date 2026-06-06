---
name: log-management-nist-800-92
description: Panduan log management berdasarkan NIST SP 800-92 untuk perencanaan, pengumpulan, penyimpanan, analisis, dan retensi log keamanan secara terstruktur.
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, system administrator, soc analyst, auditor, infrastructure engineer
  standard: NIST SP 800-92
---

# Log Management — NIST SP 800-92

## Pendahuluan

NIST SP 800-92 (Guide to Computer Security Log Management) adalah standar untuk mengelola log keamanan secara sistematis. Log yang dikelola dengan baik adalah fondasi untuk deteksi insiden, forensik, compliance, dan audit.

### Mengapa Log Management Penting?

- **Deteksi insiden** — log adalah mata dan telinga infrastruktur
- **Forensik** — tanpa log, insiden tidak bisa direkonstruksi
- **Compliance** — banyak regulasi mewajibkan logging dan review berkala
- **Accountability** — log menyediakan jejak siapa melakukan apa dan kapan
- **Troubleshooting** — log membantu diagnosis masalah operasional

## 1. Perencanaan Log Management

Sebelum mengumpulkan log, tentukan apa yang perlu dicatat dan mengapa.

### Kebijakan Log Management

- Tujuan logging — deteksi insiden, compliance, troubleshooting, atau forensik
- Sumber log yang akan dikumpulkan — prioritas berdasarkan risiko aset
- Tingkat detail logging (verbosity) per sumber
- Frekuensi review — real-time untuk critical systems, periodik untuk non-kritis
- Retention period — berapa lama log disimpan sebelum dihapus atau diarsipkan
- Prosedur secure disposal saat log tidak lagi diperlukan

### Penentuan Prioritas Sumber Log

Tidak semua log sama pentingnya. Prioritas berdasarkan:

| Prioritas | Sumber | Alasan |
|---|---|---|
| **KRITIS** | Authentication server, firewall, IDS/IPS, domain controller | Mendeteksi akses tidak sah dan serangan |
| **TINGGI** | Web server, database, aplikasi kritikal, VPN | Mendeteksi eksploitasi dan data breach |
| **SEDANG** | DNS, mail server, file server, cloud API logs | Konteks investigasi dan lateral movement |
| **RENDAH** | Workstation umum, printer, IoT | Hanya jika ada indikasi insiden |

### Staffing

- Tentukan siapa yang bertanggung jawab: review log, maintain infrastructure, respond to alerts
- Pisahkan职责 (duties) — admin log tidak boleh jadi satu-satunya yang diaudit
- Pastikan ada backup personel untuk coverage saat cuti/sakit

## 2. Sumber Log

### Operating System Logs

- **Windows**: Security Event Log (event ID 4624 login, 4625 failed login, 4688 process creation), System Event Log, Application Event Log
- **Linux**: `/var/log/auth.log` atau `/var/log/secure` (authentication), `/var/log/syslog` (system), `/var/log/kern.log` (kernel)
- Penting: pastikan audit policy diaktifkan untuk mencatat login success & failure, privilege use, process tracking, object access

### Application Logs

- Aplikasi kustom — pastikan mencatat: authentication, authorization failures, input validation errors, admin actions, data access
- Web server — akses log (status code, IP, user agent, URI), error log
- Database — query log (terutama untuk deteksi SQL injection), login attempts, privilege changes

### Security Device Logs

- Firewall — koneksi allowed/blocked, source/destination IP, port, protocol
- IDS/IPS — alert signatures, source IP, target, severity
- Antivirus/EDR — malware detected, file quarantined, process blocked
- WAF — blocked requests, attack patterns, false positive analysis

### Network Device Logs

- Router/Switch — configuration changes, interface up/down, ACL violations
- VPN concentrator — connection attempts, authentication, disconnection
- DNS server — query log (untuk deteksi C2 communication dan data exfiltration)

### Cloud & Container Logs

- **Cloud**: CloudTrail (AWS), Audit Log (GCP), Activity Log (Azure) — semua API calls
- **Container**: Docker events, Kubernetes audit logs (kube-apiserver, kubelet), container stdout/stderr
- **Orchestration**: pod creation/deletion, RBAC changes, secret access, network policy changes

## 3. Infrastruktur Log

### Centralized vs Decentralized

| Aspek | Centralized | Decentralized |
|---|---|---|
| **Visibility** | Semua log di satu tempat, correlation mudah | Sulit menghubungkan event antar sistem |
| **Forensik** | Satu sumber kebenaran | Log tersebar, risiko hilang |
| **Scalability** | Butuh infrastruktur besar | Distribusi beban alami |
| **Single point of failure** | Ya — butuh redundancy | Tidak, tapi fragmentasi |
| **Compliance** | Mudah di-audit | Sulit diverifikasi |

Rekomendasi NIST: **Centralized logging** untuk semua sumber kritis, dengan redundancy (hot-standby atau multi-region).

### Transport & Keamanan Log

- **Encryption in transit** — gunakan TLS untuk semua pengiriman log (syslog over TLS, HTTPS)
- **Encryption at rest** — enkripsi log yang disimpan, terutama jika mengandung data sensitif
- **Integrity** — gunakan digital signature atau write-once media untuk mencegah tampering
- **Access control** — hanya personel yang berwenang bisa membaca dan menghapus log

### Timestamp & Time Sync

**NTP adalah fondasi log management.** Tanpa waktu yang sinkron, rekonstruksi insiden tidak mungkin dilakukan.

- Semua sistem wajib menggunakan **NTP** yang sama
- Catat timezone — gunakan UTC untuk standarisasi, konversi ke lokal hanya saat display
- Sertakan timestamp di setiap event log — jangan andalkan file modification time
- Audit time drift secara berkala (deviasi > 1 detik harus diperbaiki)

## 4. Pengumpulan & Penyimpanan

### Format Log

| Format | Kelebihan | Cocok Untuk |
|---|---|---|
| **Syslog (RFC 5424)** | Standar industri, banyak device mendukung | Network devices, Linux, legacy systems |
| **JSON** | Terstruktur, mudah diparsing, flexible schema | Aplikasi modern, cloud services |
| **CEF (Common Event Format)** | Standar ArcSight, field tetap | Security appliances, SIEM integration |
| **Windows Event Log** | Kaya informasi, native Windows | Windows environments |

### Volume Planning

Estimasi volume harian sebelum menentukan infrastruktur:

| Jenis Sumber | Estimasi Volume (per hari) |
|---|---|
| Firewall (edge) | 10-50 GB (tergantung traffic) |
| Web server (1 server) | 100 MB - 5 GB |
| Linux auth log (50 server) | 100 MB - 1 GB |
| Windows Security (100 workstation) | 500 MB - 5 GB |
| IDS/IPS signatures | 1-20 GB |
| CloudTrail (medium org) | 5-50 GB |

Gunakan estimasi x **retention period** untuk menghitung total storage yang dibutuhkan.

### Storage Tiering

- **Hot storage** — 7-30 hari terakhir, akses cepat (SSD/NVMe) untuk analisis real-time
- **Warm storage** — 30-90 hari, akses sedang (HDD) untuk investigasi
- **Cold storage** — 90+ hari hingga retention end, akses lambat (archival/cloud) untuk compliance

### Kompresi

- Log teks: rasio kompresi 5:1 hingga 10:1
- Log JSON: rasio 3:1 hingga 5:1
- Gunakan kompresi lossless (gzip, zstd) — jangan kompresi lossy

## 5. Analisis & Monitoring

### Real-Time Alerting

Tidak semua log perlu di-review manusia secara real-time. Tentukan aturan alerting yang:

- **High fidelity** — hampir selalu true positive (contoh: multiple failed login admin + success)
- **Business critical** — dampak langsung ke bisnis (contoh: firewall config berubah)
- **Regulatory** — diwajibkan oleh compliance (contoh: privilege escalation)

### Periodic Review

Untuk sumber log non-kritis atau yang volume-nya terlalu besar untuk alerting real-time:

- **Daily** — review singkat: total login failures, blocked traffic spikes, error rate anomali
- **Weekly** — review mendalam: pattern analysis, outlier detection, trend comparison
- **Monthly** — executive summary: metrics, incidents, improvement areas

### Correlation Rules

Hubungkan event dari berbagai sumber untuk mendeteksi pola attack:

**Contoh: Brute Force Detection**
```
>= 10 failed login (Authentication Log)
+ 1 successful login within 5 menit (Authentication Log)
+ Login dari IP asing (Geolocation)
+ Akses ke sensitive data dalam 10 menit (Application Log)
```
Tingkat keyakinan: **HIGH** — kemungkinan credential compromise.

### Anomaly Detection

- **Baseline** — pelajari traffic normal, login pattern, process execution
- **Deviation** — alert ketika menyimpang dari baseline (contoh: login jam 3 pagi, traffic 10x normal)
- **Threshold** — tentukan ambang batas untuk mengurangi false positive

### Common Pitfalls in Log Analysis

- **Log overload** — terlalu banyak log tapi tidak ada yang di-review
- **No baseline** — semua event terlihat anomali padahal normal
- **Orphan logs** — log terkumpul tapi tidak ada pemilik yang bertanggung jawab
- **False positive fatigue** — aturan terlalu sensitif, analyst mati rasa
- **Alert without context** — log menunjukkan "apa" tapi tidak bisa dijawab "kenapa"

## 6. Retensi & Disposal

### Retention Policy

Berapa lama log harus disimpan tergantung pada:

- **Regulatory requirements** — PCI DSS (1 tahun), SOX (7 tahun), HIPAA (6 tahun), GDPR (tidak lebih dari diperlukan)
- **Organizational policy** — sesuaikan dengan risk appetite
- **Storage capability** — log tidak berguna jika sudah dihapus karena capacity

Rekomendasi umum:

| Jenis Log | Retention Minimum | Notes |
|---|---|---|
| Authentication logs | 1 tahun | Diperlukan untuk forensik akses |
| Security device logs | 90 hari - 1 tahun | Sesuaikan dengan kapasitas |
| Application logs | 90 hari - 1 tahun | Prioritaskan logs aplikasi kritikal |
| Network device logs | 30 - 90 hari | Volume besar, fokus pada changes |
| Cloud audit logs | 1 - 7 tahun | Immutable, compliance wajib |
| System logs | 30 - 90 hari | Rotate lebih cepat |

### Archival & Disposal

- **Archive** — setelah hot/warm period, pindahkan ke cold storage sebelum dihapus
- **Secure delete** — log berisi data sensitif, hapus dengan metode secure (shred, degauss, cryptographic erasure)
- **Chain of custody** — jika log digunakan untuk legal/forensik, pertahankan chain of custody sampai disposal
- **Automation** — retention dan disposal harus otomatis, jangan manual

## 7. Operational Considerations

### Log Review Frequency

| Jenis Review | Frekuensi | Dilakukan Oleh |
|---|---|---|
| Real-time alerting | 24/7 | SOC Analyst |
| Daily summary | Setiap hari | Security Analyst |
| Weekly deep dive | Mingguan | Senior Analyst / Engineer |
| Monthly metrics | Bulanan | Security Manager |
| Quarterly audit | Triwulan | Internal / External Auditor |

### Playbook untuk Log Review

Setiap jenis log harus memiliki playbook review:

1. **Sumber log apa yang di-review?** — definisi jelas
2. **Apa yang dicari?** — pola, value abnormal, event tertentu
3. **Tindakan jika ditemukan?** — alert, escalate, ignore, investigate lebih lanjut
4. **Dokumentasi** — di mana mencatat temuan?

### Common Operational Issues

- **Log volume tumbuh** — tanpa planning, storage habis dan log terbuang
- **Time drift** — UTC tidak konsisten, timeline tidak bisa direkonstruksi
- **Log format berubah** — update aplikasi mengubah format log, parser rusak
- **Log source mati** — monitoring log health sendiri sering terlupakan
- **Retention not enforced** — log disimpan selamanya, cost membengkak

### Log Health Monitoring

Pastikan infrastruktur log sendiri dimonitor:
- **Agent health** — apakah semua sumber mengirim log?
- **Throughput** — apakah ada bottleneck pengiriman?
- **Storage** — berapa sisa kapasitas?
- **Error rate** — apakah ada log yang gagal terkirim atau corrupt?

## Key Questions

1. **"What logs matter most?"** — Jika hanya bisa menyimpan 10% log, mana yang dipilih?
2. **"Are my timestamps reliable?"** — Apakah NTP dikonfigurasi di semua sistem?
3. **"Who has access to logs?"** — Apakah akses log terbatas dan tercatat?
4. **"How long should I keep this?"** — Apakah retention policy sesuai regulasi dan kebutuhan?
5. **"What happens if a log source stops sending?"** — Apakah ada alert untuk log source yang mati?
6. **"Can we reconstruct an incident from last month?"** — Apakah log yang diperlukan masih ada dan readable?
7. **"Is our log data integrity protected?"** — Apakah log bisa dimodifikasi tanpa terdeteksi?
8. **"What are we not logging?"** — Sumber apa yang tidak tercakup? Apakah itu risiko yang diterima?

## Abbreviations

| Istilah | Kepanjangan |
|---|---|
| NIST | National Institute of Standards and Technology |
| SIEM | Security Information and Event Management |
| CEF | Common Event Format |
| NTP | Network Time Protocol |
| IDS/IPS | Intrusion Detection/Prevention System |
| WAF | Web Application Firewall |
| ACL | Access Control List |
| EDR | Endpoint Detection and Response |
| SCA | Security Content Automation Protocol |
| UTC | Coordinated Universal Time |

## Kapan Menggunakan Skill Ini

**Gunakan ketika:**
- Mendesain atau mengevaluasi infrastruktur logging
- Membuat kebijakan log management untuk organisasi
- Melakukan audit log untuk deteksi insiden
- Membutuhkan guidance retensi log untuk compliance
- Merencanakan implementasi SIEM atau centralized logging
- Menulis procedure review log untuk SOC / security team

**Jangan gunakan ketika:**
- Membutuhkan konfigurasi spesifik tool logging (syslog-ng, rsyslog, Splunk, ELK) — gunakan dokumentasi tool terkait
- Membutuhkan threat modeling — gunakan skill threat-modeling
- Membutuhkan panduan incident response — gunakan skill incident-response-plan
- Membutuhkan forensic analysis detail — ini hanya mencakup management, bukan teknis forensik
