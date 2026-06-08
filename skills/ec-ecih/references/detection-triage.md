---
name: "Detection, Triage & Notification"
description: "Recording & detection sources, data collection, common detection patterns, triage prioritization framework, BIA for triage, decision trees, escalation matrix, communication templates, war room protocol, and golden rules for incident notification."
tags: [ecih, detection, triage, notification, escalation, bia, communication, war-room]
---

## Recording & Detection — Finding the Signal

### Esensi Recording

Recording adalah stage pertama setelah insiden terjadi. Ini adalah **proses mengkonfirmasi bahwa suatu kejadian benar-benar insiden keamanan**, bukan false positive atau kejadian non-keamanan.

### Sumber Deteksi

Insiden bisa terdeteksi melalui berbagai sumber:

| Sumber | Contoh | Kelebihan | Kekurangan |
|--------|--------|-----------|------------|
| **Automated Alerts** | SIEM, IDS/IPS, EDR, WAF | Cepat, coverage luas | False positive tinggi |
| **User Reports** | Karyawan melaporkan anomali | Konteks bisnis | Tidak konsisten, subyektif |
| **Threat Intelligence** | IOC feeds, ISAC sharing | Proaktif | Perlu validasi |
| **External Notification** | Customer complaint, researcher report | Sumber eksternal | Krisis reputasi sudah mulai |
| **Audit/Compliance** | Internal audit, regulatory review | Periodik | Tidak real-time |
| **Red Team/Pentest** | Penetration test findings | Deep analysis | Terjadwal |
| **Hunting** | Proactive threat hunting | Menemukan yang tidak terdeteksi | Resource intensive |

### Proses Recording

```
Alert/Report Masuk
       │
       ▼
     ┌────────────────────────────┐
     │  Initial Triage (Level 1)  │
     │  - Apakah ini insiden?     │
     │  - Seberapa urgent?        │
     │  - Siapa yang perlu tahu?  │
     └────────────┬───────────────┘
                  │
          ┌───────┴───────┐
          ▼               ▼
   ┌─────────────┐  ┌───────────┐
   │True Positive│  │False      │
   │             │  │Positive   │
   └──────┬──────┘  └───────────┘
          │             │
          ▼             ▼
   Lanjut Triage   Catat untuk tuning
```

### Data yang Wajib Direkam

Setiap insiden, sekecil apapun, harus direkam dengan data berikut:

| Field | Deskripsi | Contoh |
|-------|-----------|--------|
| **Incident ID** | Unique identifier | INC-2026-0042 |
| **Timestamp** | Waktu deteksi (timezone) | 2026-06-07T14:30:00Z |
| **Source** | Bagaimana terdeteksi | SIEM Alert #4721 |
| **Category** | Jenis insiden | Phishing |
| **Severity** | Initial severity estimate | Medium |
| **Affected Assets** | Sistem atau data terdampak | Mail server, 15 user mailboxes |
| **Initial Reporter** | Siapa yang melaporkan | SOC Analyst Jane Doe |
| **Description** | Narasi singkat | User reported suspicious email with malicious link |
| **Current Status** | Status terkini | Open / In Progress / Resolved |

### Pencatatan Waktu yang Akurat

Salah satu sumber error paling umum dalam IR adalah **waktu yang tidak sinkron**. Pastikan:
- Semua sistem menggunakan NTP dengan source yang sama
- Semua log dalam timezone UTC (gunakan UTC untuk pencatatan)
- Timestamp dictatat dengan format ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- Perhatikan offset timezone jika menggunakan zona lokal

### Common Detection Patterns

Pola yang sering menandakan insiden:

| Pattern | Indikasi | Sumber |
|---------|----------|--------|
| **Multiple failed logins** | Brute force, password spraying | Authentication logs |
| **Successful login after failures** | Successful brute force | Authentication logs |
| **Outbound connection at odd hours** | C2 beaconing | Firewall/Proxy logs |
| **Large data transfer** | Data exfiltration | DLP, netflow |
| **New admin account** | Persistence | AD logs |
| **Scheduled task creation** | Persistence | Windows Event Log |
| **Process launching from temp** | Malware execution | EDR |
| **Unusual parent-child process** | LOLBins, privilege escalation | EDR |
| **DNS query to known bad domain** | C2 communication | DNS logs |
| **Email login from unusual geo** | Account compromise | Email logs |

### Dokumentasi Awal

Dokumentasi bukan birokrasi — dokumentasi adalah **alat investigasi**. Gunakan format **who, what, when, where, why, how** untuk setiap temuan.

---

## Triage & Prioritization — Decision Framework

### Esensi Triage

Triage adalah **proses pengambilan keputusan tentang urutan penanganan insiden**. Tidak semua insiden bisa ditangani bersamaan. Sumber daya terbatas. Triage menentukan mana yang didahulukan.

### Dimensi Triage

```
                    Impact
                       │
                       │
              High Impact ───── Critical
                       │
                       │
          ─────────────┼───────────── Urgency
                       │
                       │
             Low Urgency ──── Monitor
                       │
                       │
                   Confidence
```

Tiga dimensi utama:
1. **Impact**: Seberapa besar kerusakan jika insiden ini tidak ditangani?
2. **Urgency**: Seberapa cepat insiden ini perlu ditangani?
3. **Confidence**: Seberapa yakin kita bahwa ini benar-benar insiden?

### Klasifikasi Insiden

| Kategori | Contoh | Initial Severity |
|----------|--------|-----------------|
| **Malware** | Virus, worm, trojan, ransomware | Medium-High |
| **Network Attack** | DDoS, MITM, DNS poisoning | Medium-Critical |
| **Web Attack** | SQLi, XSS, CSRF, SSRF | Low-Critical |
| **Data Breach** | Data exposure, exfiltration | High-Critical |
| **Insider Threat** | Data theft, sabotage, policy violation | Medium-Critical |
| **Account Compromise** | Credential theft, session hijacking | High-Critical |
| **Phishing/Social Engineering** | Credential harvesting, BEC | Low-Critical |
| **Physical Security** | Theft, unauthorized access | Medium-High |
| **Policy Violation** | AUP violation, PII mishandling | Low-Medium |
| **Availability Incident** | DoS, system failure | Medium-Critical |

### Prioritas Penanganan

Prioritas ditentukan oleh kombinasi Impact × Urgency:

| | Low Impact | Medium Impact | High Impact |
|--|-----------|--------------|-------------|
| **Low Urgency** | Priority 4 (Log) | Priority 3 (Normal) | Priority 2 (High) |
| **Medium Urgency** | Priority 3 (Normal) | Priority 2 (High) | Priority 1 (Critical) |
| **High Urgency** | Priority 2 (High) | Priority 1 (Critical) | Priority 0 (Emergency) |

**Priority Definitions**:

| Priority | SLA | Contoh |
|----------|-----|--------|
| **P0 — Emergency** | Respond < 15 min | Ransomware outbreak, active data exfiltration |
| **P1 — Critical** | Respond < 30 min | Account compromise, DDoS attack |
| **P2 — High** | Respond < 2 hours | Malware on isolated system, phishing campaign |
| **P3 — Normal** | Respond < 8 hours | Single user malware, low-severity policy violation |
| **P4 — Log** | Respond < 1 week | Scans, recon, informational |

### Business Impact Assessment (BIA) untuk Triage

BIA dalam konteks IR membantu menjawab:
- **Apa dampak finansial** dari downtime sistem ini?
- **Apa dampak reputasi** jika insiden ini publik?
- **Apa dampak legal** jika data pelanggan terekspos?
- **Apa dampak operasional** jika sistem tidak tersedia?

Pertanyaan Kunci untuk BIA dalam IR:
1. Sistem apa yang terdampak?
2. Data apa yang ada di sistem itu?
3. Berapa banyak pengguna/customer terdampak?
4. Apakah ada kewajiban regulasi?
5. Apakah insiden ini visible ke publik?
6. Berapa biaya per jam downtime?

### Triage Decision Tree

```
Apakah ini true positive?
  ├── Tidak → Log sebagai false positive, update tuning
  └── Ya → Lanjut
          
Apakah insiden masih aktif?
  ├── Tidak → Catat timeline, lanjut ke forensik
  └── Ya → Prioritaskan containment
          
Apa yang terdampak?
  ├── Data sensitif (PII, finansial, health) → High impact
  ├── Critical infrastructure → High impact
  ├── Internal systems → Medium impact
  └── Non-critical systems → Low impact
          
Seberapa luas penyebaran?
  ├── Satu endpoint → Terkontrol
  ├── Banyak endpoint → Wabah
  ├── Server critical → Segera
  └── Data center → Emergency
          
Apakah legal/regulatory implications?
  ├── GDPR, HIPAA, PCI DSS → Notify legal, high priority
  ├── Internal policy → Medium priority
  └── None → Normal priority
```

### Critical vs Non-Critical Systems

Definisi sistem kritis harus sudah ditetapkan SEBELUM insiden:

| Sistem | Kriteria Kritis |
|--------|----------------|
| **Production** | Revenue-generating, customer-facing |
| **Database** | Customer data, financial data |
| **Authentication** | AD, SSO, MFA |
| **Communication** | Email, collaboration tools |
| **Security** | SIEM, EDR, firewall |
| **Financial** | Payment processing, billing |
| **Regulatory** | Systems under compliance |

---

## Notification & Escalation — Communication Protocols

### Esensi Notification

Notification adalah stage yang sering di-skip dalam tekanan, tapi **justru paling krusial untuk keberhasilan IR**. Tanpa komunikasi yang baik, tindakan teknis terbaik pun gagal karena stakeholder tidak siap, keputusan tertunda, atau ekspektasi tidak dikelola.

### Escalation Matrix

Escalation matrix menentukan **siapa** dihubungi **kapan** untuk **insiden seperti apa**.

```
Level 1 — SOC Analyst
  └── Menangani: False positive, low-severity true positive
      └── Eskalasi ke: Level 2 jika severity medium+

Level 2 — Incident Handler
  └── Menangani: Medium-high severity insiden
      └── Eskalasi ke: Level 3 jika severity critical

Level 3 — IR Manager / CSIRT Lead
  └── Menangani: Critical insiden, crisis
      └── Eskalasi ke: Executive / Legal

Level 4 — Executive / Legal / PR
  └── Menangani: Board notification, public disclosure, regulator
```

### Siapa yang Perlu Dinotifikasi

| Stakeholder | Kapan | Apa yang Diberitahu |
|-------------|-------|---------------------|
| **IR Team** | Segera setelah konfirmasi | Incident details, severity, action needed |
| **System Owner** | Segera setelah identifikasi | Sistem terdampak, containment plan |
| **Management** | Dalam 1 jam untuk critical | Business impact, estimated timeline |
| **Legal** | Jika ada regulatory implication | Data type affected, notification obligations |
| **HR** | Jika insider threat | Employee involved, policy violation |
| **PR/Communications** | Jika publik mungkin tahu | Holding statement, communication strategy |
| **Regulator** | Sesuai regulatory timeline | Incident notification per regulation |
| **Law Enforcement** | Jika criminal activity | Evidence, investigation request |
| **Customers** | Jika data mereka terdampak | Notification per regulation, remediation steps |

### Communication Templates

Setiap IR Plan harus punya template komunikasi yang bisa diisi cepat:

**Internal Notification Template**:
```
Subject: [SEVERITY] Security Incident — [Incident ID]

Summary: [1-2 sentences]
Affected Systems: [List]
Current Status: [Detection / Investigation / Containment / Recovery]
Action Required: [Who needs to do what]
Next Update: [Time]
Point of Contact: [Name, Phone, Email]
```

**Holding Statement for External**:
```
[Organization] is aware of a security incident affecting [scope].
We are investigating the matter thoroughly and have engaged
[internal/external] experts. We will provide updates as more
information becomes available. The security of our systems
and data is our top priority.
```

**Regulatory Notification Timeline**:
| Regulation | Notification Requirement | Timeframe |
|------------|------------------------|-----------|
| **GDPR** | Notify supervisory authority | Within 72 hours |
| **HIPAA** | Notify affected individuals + HHS | Within 60 days |
| **PCI DSS** | Notify acquiring bank + card brands | Immediately, then within 30 days |
| **SOX** | Report to audit committee | As soon as material |
| **State breach laws** | Notify affected residents | Varies (30-90 days) |

### War Room Protocol

Untuk insiden besar, aktifkan war room:

1. **Activate**: Panggil semua anggota inti ke war room (fisik/virtual)
2. **Establish comms**: Buka channel komunikasi dedicated
3. **Assign roles**: Siapa lead, scribe, technical, communications
4. **Set cadence**: Status update setiap 30-60 menit
5. **Document**: Satu orang khusus mencatat timeline dan keputusan
6. **Executive summary**: Siapkan ringkasan untuk management

### Communication Golden Rules

1. **No speculation** — Hanya komunikasikan fakta yang sudah dikonfirmasi
2. **One voice** — Semua komunikasi eksternal lewat satu designated person
3. **Transparency** — Akui apa yang belum diketahui
4. **Timeliness** — Update reguler meski belum ada informasi baru
5. **Audience-appropriate** — Management butuh business impact, teknis butuh detail
6. **Written record** — Semua keputusan penting didokumentasikan
