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

## Referensi Lengkap

### NIST Standards & Publications

| Nama | Status | Deskripsi | Link |
|------|--------|-----------|------|
| NIST SP 800-92 Rev. 1 (ipd) | Draft (Oct 2023) | Cybersecurity Log Management Planning Guide — playbook untuk perencanaan log management modern, menggantikan 800-92 asli | [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/92/r1/ipd) |
| NIST SP 800-92 (2006) | Final | Guide to Computer Security Log Management — original standard untuk implementasi log management enterprise | [csrc.nist.gov](https://csrc.nist.gov/pubs/sp/800/92/final) |
| NIST SP 800-53 Rev. 5 | Final | Security & Privacy Controls — AU (Audit & Accountability) family of controls untuk logging | [csrc.nist.gov](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final) |
| NIST SP 800-61 Rev. 2 | Final | Computer Security Incident Handling Guide — logging untuk incident detection & investigation | [csrc.nist.gov](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final) |
| NIST SP 800-207 | Final | Zero Trust Architecture — data analytics & logging untuk zero trust | [csrc.nist.gov](https://csrc.nist.gov/publications/detail/sp/800-207/final) |
| NIST Cybersecurity Framework 2.0 | Final (2024) | Fokus pada Protect (PR.PT) dan Detect (DE) functions untuk logging & monitoring | [nist.gov](https://www.nist.gov/cyberframework) |
| NIST SP 800-88 Rev. 2 | Final | Media Sanitization — secure disposal log media dan destruction certificates | [csrc.nist.gov](https://csrc.nist.gov/publications/detail/sp/800-88/rev-2/final) |

### Buku & Publications

| Judul | Penulis | Tahun | Fokus Utama |
|-------|---------|-------|-------------|
| Logging and Log Management: The Authoritative Guide | Kevin Schmidt, Chris Phillips, Anton Chuvakin | 2012 | Komprehensif — teori, praktik, forensik, compliance, cloud logging |
| Logging in Action | Phil Wilkins | 2022 | Fluentd & Fluent Bit — implementasi logging pipeline dengan CNCF tools |
| Logs and Telemetry | Phil Wilkins | 2025 | Fluent Bit — observability pipeline untuk cloud-native, Kubernetes, OpenTelemetry |
| Software Telemetry | Jamie Riedesel | 2021 | End-to-end telemetry system — logs, metrics, traces, compliance, GDPR |
| The Logstash Book | James Turnbull | 2016 | Logstash — implementasi ELK stack untuk log management |
| Data Engineering for Cybersecurity | James Bonifield | 2024 | Secure data pipelines — Filebeat, Logstash, Kafka, Elasticsearch untuk security telemetry |
| Understanding Log Analytics at Scale (2nd Ed.) | Matt Gillespie, Charles Givre | 2021 | Log analytics architecture — storage, deployment, business outcomes |
| The Practice of Network Security Monitoring | Richard Bejtlich | 2013 | NSM — logging untuk network security monitoring dan threat detection |

### SIEM Platform Comparison

| Platform | Tipe | Kelebihan Utama | Kelemahan Utama | Cocok Untuk |
|----------|------|-----------------|-----------------|-------------|
| Splunk Enterprise Security | Commercial | SPL terkuat, 6000+ integrasi, komunitas besar | Biaya tinggi (per GB), kompleks infrastruktur | Enterprise besar, mature SOC |
| Microsoft Sentinel | Cloud-native | Integrasi dalam dengan M365/Entra/Azure, SOAR built-in | Azure lock-in, KQL learning curve | Lingkungan Microsoft-heavy |
| Elastic Security | Open-source core | Skalabilitas tinggi, full-text search, deployment fleksibel | Kompleksitas operasional, free version lacks advanced SIEM | Cost-sensitive, engineering-heavy |
| Wazuh | Open-source (AGPLv3) | SIEM+EDR+FIM+vuln scan gratis, compliance built-in | Skalabilitas terbatas di very large, community support | SMB, compliance-driven, on-prem |
| Google SecOps (Chronicle) | Cloud-native | Petabyte-scale ingestion, Mandiant threat intel | Google Cloud lock-in, YARA-L learning curve | High-volume, Google-heavy |
| Sumo Logic | Cloud-native | Mid-market sweet spot, mudah deploy | Kurang fleksibel dibanding Splunk/Elastic | Mid-market, hybrid cloud |
| Graylog | Open-source | Mudah setup, alerting built-in, API-driven | Kurang mature detection dibanding Wazuh/Elastic | Teams needing quick deployment |
| Security Onion | Open-source | Bundle IDS+SIEM+hunting tools (Suricata, Zeek, Wazuh) | Konsumsi resource tinggi, kompleks | Threat hunting, blue team labs |

### Log Management Tools

**Collectors & Shippers:**
- **Fluentd** — CNCF graduated, unified logging layer, 1000+ plugins, Ruby-based
- **Fluent Bit** — CNCF, super lightweight (C), cloud-native, Kubernetes native, OpenTelemetry support
- **Logstash** — Elastic stack, pipeline processing, 200+ plugins, Java-based
- **Vector** — High-performance observability pipeline, Rust-based, vendor-agnostic
- **rsyslog** — Rocket-fast syslog processing, Linux default, C-based
- **syslog-ng** — Enterprise syslog, filtering/rewriting, reliable TCP transport
- **Filebeat / Winlogbeat** — Elastic lightweight shippers, kubernetes-native
- **Flume** — Apache, distributed log aggregation, Hadoop ecosystem

**Storage & Analytics:**
- **Elasticsearch** — Distributed search & analytics engine, foundation of ELK
- **OpenSearch** — Apache 2.0 fork of Elasticsearch, AWS-led, community-driven
- **Grafana Loki** — Log aggregation inspired by Prometheus, multi-tenant, cloud-native
- **BigQuery** — Google Cloud serverless data warehouse for log analytics
- **ClickHouse** — Columnar OLAP database, high-performance log storage

**Visualization:**
- **Kibana** — Elasticsearch visualization, dashboards, discover
- **Grafana** — Multi-source dashboarding, Loki integration, alerting
- **OpenSearch Dashboards** — Fork of Kibana, Apache 2.0 licensed

**Queue & Buffer:**
- **Kafka** — Distributed streaming platform, log buffering, replay
- **Redis** — In-memory buffer, log queue between shippers and indexers
- **RabbitMQ** — Message broker, reliable log routing

### Cloud Logging Guidance

| Provider | Layanan Utama | Best Practices |
|----------|---------------|----------------|
| AWS | CloudTrail (API audit), VPC Flow Logs, S3 Access Logs, CloudWatch Logs, GuardDuty | Org-level multi-region trail, S3 Object Lock (COMPLIANCE), log integrity validation SHA-256, CloudWatch metric filters for high-value events, SCP mencegah StopLogging/DeleteTrail |
| Azure | Activity Log, Diagnostic Settings, NSG Flow Logs, Microsoft Entra ID audit/sign-in logs, Sentinel | Log Analytics Workspace sentral, Azure Policy enforce diagnostic settings, immutable storage, TLS 1.2+, workspace replication untuk resilience |
| GCP | Cloud Audit Logs (Admin+Data Access+System Event), VPC Flow Logs, Firewall Rules Logging, Security Command Center | Data Access logs enabled selektif, aggregated sink org-level, BigQuery analytics, retention locks, Access Transparency untuk Google staff access |
| Cross-Cloud | SIEM sentral (Splunk/Sentinel/Elastic), object lock untuk immutability, retention 1-7 tahun sesuai regulasi | Centralized logging account, tiered storage, integrity validation all providers, alerting on log disablement |

### Compliance & Log Retention

| Framework | Minimum Retention | Key Requirements |
|-----------|------------------|------------------|
| PCI DSS v4.0 | 12 bulan (3 bulan immediately available) | Requirement 10 — log semua akses ke CDE, auth events, privileged actions |
| HIPAA Security Rule | 6 tahun | Audit logs untuk akses ePHI, risk assessments, incident records |
| SOX Section 802 | 7 tahun | Audit workpapers, financial system access, change management |
| GDPR Art. 5(1)(e) | Purpose-based (1-3 tahun typical) | Data minimization, documented justification dalam ROPA |
| NIST SP 800-53 Rev. 5 | Defined per policy (AU-11) | Audit record retention, sufficient storage allocation |
| NIST CSF 2.0 | Risk-based | Protect (PR.PT) + Detect (DE) logging controls |
| FedRAMP | 90 hari online, archival per agency | NIST-derived, documented retention schedules |
| CIS Controls v8 | 90-365 days | Control 8 — audit log management, time synchronization |
| ISO 27001 | Defined per policy | A.12.4 — logging & monitoring, retention based on risk |
| DORA (EU) | 5+ tahun (practical) | ICT operational logs, audit trails, incident records |
| SOC 2 | Risk-based (typical 12 bulan) | Trust criteria — security monitoring & retention |

### Sertifikasi & Training

| Nama | Penerbit | Fokus | Biaya |
|------|----------|------|-------|
| GIAC Certified Detection Analyst (GCDA) | GIAC/SANS SEC555 | Detection engineering, SIEM analytics, SOF-ELK | ~$8,780 (includes SEC555) |
| GIAC Certified Forensic Examiner (GCFE) | GIAC | Windows forensics, event log analysis, browser forensics | ~$8,780 |
| GIAC Security Essentials (GSEC) | GIAC | Log management & SIEM (1 domain dari 12) | ~$8,780 |
| PECB Certified Lead Forensics Examiner (CLFE) | PECB | Computer forensics, evidence recovery, multi-platform | ~$3,000 |
| Certified Log & Forensics Security Professional (CLFSP) | SecureSphere Foundation | SOC operations, log analysis, SIEM fundamentals, threat detection | ~$500 |
| SANS SEC540: Cloud Native Security & DevSecOps | SANS | Cloud logging, SIEM, compliance automation | ~$8,780 |
| Splunk Certified Architect | Splunk | Splunk deployment, architecture, SPL | ~$2,500 (exam only) |
| Microsoft Certified: Security Operations Analyst Associate | Microsoft | Microsoft Sentinel, KQL, detection | ~$165 (exam) |

### Komunitas & Curated Lists

| Nama | Deskripsi | Link |
|------|-----------|------|
| awesome-logging (hugo53) | Curated logging infrastructure, shippers, formats | [github.com](https://github.com/hugo53/awesome-logging) |
| awesome-log-analysis (logpai) | 791+ stars — academic papers, datasets, anomaly detection, AIOps | [github.com](https://github.com/logpai/awesome-log-analysis) |
| awesome-sysadmin — Log Management | Tools: fluentd, logstash, rsyslog, graylog, loki | [github.com](https://github.com/awesome-foss/awesome-sysadmin#log-management) |
| NIST Log Management Project Page | Semua publikasi NIST terkait log management | [csrc.nist.gov](https://csrc.nist.gov/Projects/log-management) |
| PCI DSS Effective Daily Log Monitoring | Panduan resmi PCI SSC untuk daily log monitoring | [pcisecuritystandards.org](https://listings.pcisecuritystandards.org/documents/Effective-Daily-Log-Monitoring-Guidance.pdf) |
| Gigamon Comments on SP 800-92r1 | Industry feedback, ZTA integration, logging masa depan | [blog.gigamon.com](https://blog.gigamon.com/2023/12/06/nist-special-publication-800-92r1-cybersecurity-log-management-planning-guide/) |
| Unit 42: Cloud Logging for Security | Palo Alto Networks — AWS/Azure/GCP cloud logging framework | [unit42.paloaltonetworks.com](https://unit42.paloaltonetworks.com/cloud-logging-for-security/) |
| Bloo: Security Log Retention Guide | Compliance retention 2026, multi-framework matrix | [bloo.io](https://bloo.io/blog/security-log-retention) |
| Systems Hardening: Cloud Audit Logs | Hardened config untuk CloudTrail, GCP Audit, Azure Monitor | [systemshardening.com](https://www.systemshardening.com/articles/observability/cloud-provider-audit-logs/) |
