---
name: ec-ecih
description: EC-Council ECIH (Certified Incident Handler) v3 — incident handler mindset, IR lifecycle framework (NIST 800-61 + ECIH 9-stage IH&R), decision frameworks per incident type, forensic readiness, containment strategies, eradication methodology, recovery planning, post-incident lessons learned, dan komunikasi krisis. Berbasis ECIH 212-89 v3 curriculum.
license: MIT
compatibility: opencode
metadata:
  audience: incident-handler
  workflow: incident-response
  source: ec-council
  standard: ecih
  year: "2026"
---

# ECIH — Certified Incident Handler Mindset

## Daftar Isi

1. [Incident Handler Mindset](#1-incident-handler-mindset)
2. [ECIH Exam Overview & Strategy](#2-ecih-exam-overview--strategy)
3. [IR Lifecycle Framework](#3-ir-lifecycle-framework)
4. [Preparation — Building IR Capability](#4-preparation--building-ir-capability)
5. [Recording & Detection — Finding the Signal](#5-recording--detection--finding-the-signal)
6. [Triage & Prioritization — Decision Framework](#6-triage--prioritization--decision-framework)
7. [Notification & Escalation — Communication Protocols](#7-notification--escalation--communication-protocols)
8. [Containment Strategies — Stop the Bleeding](#8-containment-strategies--stop-the-bleeding)
9. [Evidence Gathering & Forensic Readiness](#9-evidence-gathering--forensic-readiness)
10. [Eradication — Removing the Threat](#10-eradication--removing-the-threat)
11. [Recovery — Restoring Operations](#11-recovery--restoring-operations)
12. [Post-Incident Activity — Lessons Learned](#12-post-incident-activity--lessons-learned)
13. [Incident Types & Response Playbooks](#13-incident-types--response-playbooks)
14. [Legal, Compliance & Ethics](#14-legal-compliance--ethics)
15. [Decision Framework & Trade-offs](#15-decision-framework--trade-offs)
16. [Referensi Lengkap](#16-referensi-lengkap)

---

## 1. Incident Handler Mindset

### Filosofi Dasar

Menjadi incident handler bukan tentang menghafal playbook atau command forensik. Ini tentang **membuat keputusan sulit di bawah tekanan** dengan informasi yang tidak lengkap. Seorang incident handler berpikir dalam kerangka:

```
Terdeteksi → Triage → Analisis → Contain → Evidence → Eradicate → Recover → Learn
```

Setiap langkah adalah **decision point**. Setiap decision point punya trade-off antara kecepatan, akurasi, dan risiko.

### Prinsip Inti Incident Handler

| Prinsip | Artinya | Pertanyaan Kritis |
|---------|---------|-------------------|
| **Assume Breach** | Anggap sistem sudah dikompromikan sampai terbukti bersih | "Apa yang kita lakukan KALAU ini benar-benar serangan?" |
| **Preserve Evidence** | Jangan merusak bukti selama containment | "Apakah tindakan ini akan mengubah data forensik?" |
| **Contain Before Eradicate** | Hentikan penyebaran dulu, baru bersihkan | "Apa risiko malware menyebar selama kita analisis?" |
| **Communicate Constantly** | Semua stakeholder harus tahu status | "Siapa yang perlu tahu sekarang?" |
| **Learn Without Blame** | Post-incident bukan untuk mencari siapa yang salah | "Apa yang bisa diperbaiki secara sistemik?" |
| **Risk-Based Decision** | Tidak semua insiden perlu respon penuh | "Apa dampak bisnis dari insiden ini?" |

### Mental Model Incident Handler

```
┌──────────────────────────────────────────────┐
│            FIND: Detect & Triage              │
│  (Apakah ini insiden? Seberapa parah?)         │
├──────────────────────────────────────────────┤
│          FIX: Contain & Eradicate             │
│  (Bagaimana hentikan? Bagaimana bersihkan?)    │
├──────────────────────────────────────────────┤
│         FINISH: Recover & Learn               │
│  (Kapan pullh? Apa yang dipelajari?)           │
└──────────────────────────────────────────────┘
```

### Sifat Insiden Keamanan

Insiden keamanan memiliki karakteristik yang membuatnya berbeda dari insiden IT biasa:

| Karakteristik | Implikasi |
|--------------|-----------|
| **Adversarial** | Ada musuh yang adaptif, bukan kegagalan acak |
| **Time-sensitive** | Setiap menit delay memperbesar dampak |
| **Uncertain** | Tidak pernah punya informasi lengkap |
| **Evolving** | Situasi berubah selama respon |
| **High-stakes** | Risiko reputasi, finansial, dan legal |
| **Multi-dimensional** | Teknis, legal, PR, bisnis semua terlibat |

### Incident Handler vs SOC Analyst

SOC Analyst biasanya fokus pada **triage dan investigasi awal** — menentukan apakah alert adalah true positive atau false positive. Incident Handler mengambil alih **setelah konfirmasi** dan bertanggung jawab atas keseluruhan lifecycle:

```
SOC Analyst:  Alert → Triage → Escalate
Incident Handler: Escalate → Contain → Evidence → Eradicate → Recover → Post-Mortem
```

### Pola Pikir Kritis

**"What if I'm wrong?"** — Selalu tanyakan ini. Setiap asumsi yang salah bisa menyebabkan:
- Membiarkan attacker terus bergerak (under-response)
- Shutdown sistem yang tidak perlu (over-response)
- Melewatkan bukti kritis
- Mengomunikasikan status yang salah ke manajemen

**"What is the worst-case scenario?"** — Rencanakan untuk skenario terburuk. Jika worst-case bisa diterima, maka respon sudah cukup. Jika tidak, perlu tindakan lebih agresif.

**"What does success look like?"** — Definisikan endpoint sebelum mulai. Apakah sukses berarti:
- Attacker terhenti?
- Data aman?
- Forensik lengkap?
- Recovery penuh?
- Semua di atas?

---

## 2. ECIH Exam Overview & Strategy

### Tentang ECIH v3 (212-89)

| Item | Detail |
|------|--------|
| **Certification** | EC-Council Certified Incident Handler (ECIH) v3 |
| **Exam code** | 212-89 |
| **Format** | 100 multiple-choice questions |
| **Duration** | 3 hours |
| **Passing score** | 70% |
| **Cost** | $449 (exam voucher) |
| **Prerequisites** | 1 year of cybersecurity experience recommended |
| **Accreditation** | ANAB accredited, DoD 8140 approved, CREST CCIM compliant |
| **Validity** | 3 years (need 120 ECE credits for renewal) |

### Exam Domains (Weight Distribution)

| Domain | Weight |
|--------|--------|
| Incident Handling & Response Lifecycle | 35% |
| Preparation & Prevention | 15% |
| Detection & Triage | 15% |
| Containment & Eradication | 15% |
| Recovery & Post-Incident | 10% |
| Legal & Compliance | 10% |

### Strategi Ujian ECIH

**Mindset**: ECIH menguji **kemampuan mengambil keputusan dalam incident response**, bukan pengetahuan teknis mendalam tentang tools. Soal-soal ECIH sering menyajikan skenario dan menanyakan "Apa yang harus dilakukan SELANJUTNYA?"

**Tips Kunci**:
1. **Urutan IH&R stages itu absolut** — Preparation selalu sebelum Detection, Containment selalu sebelum Eradication, Eradication selalu sebelum Recovery. Jangan tertukar.
2. **Evidence first** — Sebelum containment penuh, kumpulkan evidence. Sebelum eradication, dokumentasi evidence. Ini yang sering diuji.
3. **Chain of Custody** — Dokumentasi siapa, kapan, bagaimana menangani evidence. Setiap transfer harus tercatat.
4. **BIA menentukan prioritas** — Business Impact Assessment adalah dasar semua keputusan triage dan containment.
5. **Communication is key** — Insiden besar harus dikomunikasikan ke management, legal, PR, dan regulator. Jangan lupa step ini.
6. **Post-incident bukan hukuman** — Lessons learned bukan untuk mencari kambing hitam.
7. **Read the scenario completely** — Banyak soal ECIH memberikan skenario panjang. Jangan lompat ke jawaban sebelum membaca semua detail.

**Trick Questions yang Sering Muncul**:
- "What is the FIRST step?" — Jawabannya pasti Preparation (semua lifecycle dimulai dari persiapan)
- "What should the incident handler do NEXT?" — Perhatikan urutan IH&R stages
- "Which evidence should be collected FIRST?" — Volatile evidence (memory, network connections) sebelum persistent (disk)
- "Should containment be done before evidence collection?" — DILEMA: Idealnya kumpulkan evidence dulu, TAPI jika risiko penyebaran tinggi, contain dulu. Soal sering menguji prioritas.

### Cara Belajar ECIH

1. **Pahami lifecycle-nya dulu** — IH&R 9 stages adalah backbone. Hafal urutan dan apa yang terjadi di setiap stage.
2. **Latihan skenario** — ECIH bukan hafalan definisi. Bacalah skenario, putuskan tindakan, periksa jawaban.
3. **Understand framework, not tools** — ECIH tidak menguji tool spesifik. Fokus pada konsep seperti chain of custody, BIA, SLAs, playbooks.
4. **Legal knowledge** — Pelajari perbedaan hukum siber antar negara, GDPR, HIPAA, SOX, PCI DSS relevansinya dengan IR.
5. **Practice tests** — Kerjakan soal-soal latihan ECIH. Perhatikan pola soal.

---

## 3. IR Lifecycle Framework

### ECIH 9-Stage Incident Handling & Response (IH&R)

ECIH v3 mendefinisikan 9 stages dalam Incident Handling & Response:

```
┌──────────────────────────────────────────────────────┐
│                     Preparation                        │
│             (Kesiapan sebelum insiden)                 │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                       Recording                        │
│           (Pencatatan dan dokumentasi awal)            │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                        Triage                          │
│         (Prioritasi dan klasifikasi insiden)           │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                     Notification                       │
│     (Komunikasi ke stakeholder yang tepat)             │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                     Containment                        │
│         (Isolasi dan penghentian penyebaran)           │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                  Evidence Gathering                    │
│         (Koleksi bukti forensik secara legal)          │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                      Eradication                       │
│           (Penghapusan root cause dan artifact)        │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                       Recovery                         │
│           (Pengembalian ke operasi normal)             │
└─────────────────────┬────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────┐
│                   Post-Incident                        │
│     (Lessons learned, reporting, improvement)          │
└──────────────────────────────────────────────────────┘
```

Perbedaan utama dari NIST 800-61 (4 phases: Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident) adalah ECIH memecah Detection & Analysis menjadi Recording, Triage, Notification, dan memisahkan Containment, Evidence Gathering, Eradication, Recovery menjadi stages terpisah. Ini memberi granularitas lebih pada proses IR.

### Mapping ECIH ↔ NIST 800-61

| ECIH Stage | NIST 800-61 Phase |
|------------|-------------------|
| Preparation | Preparation |
| Recording | Detection & Analysis |
| Triage | Detection & Analysis |
| Notification | Detection & Analysis |
| Containment | Containment, Eradication & Recovery |
| Evidence Gathering | Containment, Eradication & Recovery |
| Eradication | Containment, Eradication & Recovery |
| Recovery | Containment, Eradication & Recovery |
| Post-Incident | Post-Incident Activity |

### Mapping ECIH ↔ SANS PICERL

| ECIH Stage | SANS PICERL |
|------------|-------------|
| Preparation | Preparation |
| Recording | Identification |
| Triage | Identification |
| Notification | (Implicit in all phases) |
| Containment | Containment |
| Evidence Gathering | (Integrated in Containment & Eradication) |
| Eradication | Eradication |
| Recovery | Recovery |
| Post-Incident | Lessons Learned |

### IR Lifecycle Decision Flow

Setiap stage memiliki **input, process, output**:

```
Stage: Preparation
  Input:  Risk assessment, business requirements
  Process: Build IR team, tools, playbooks, training
  Output: IR plan, ready team, configured tools

Stage: Recording
  Input:  Alerts, logs, user reports, IDS/IPS events
  Process: Validate alert, document initial findings
  Output: Incident ticket with initial data

Stage: Triage
  Input:  Incident ticket with initial data
  Process: Classify, prioritize, assess impact
  Output: Priority level, incident category, assigned handler

Stage: Notification
  Input:  Priority level and incident details
  Process: Notify stakeholders per escalation matrix
  Output: Stakeholders informed, IR team activated

Stage: Containment
  Input:  Confirmed incident with scope
  Process: Isolate affected systems, stop spread
  Output: Containment plan implemented, evidence preserved

Stage: Evidence Gathering
  Input:  Contained environment
  Process: Collect forensic data, chain of custody
  Output: Documented evidence package

Stage: Eradication
  Input:  Evidence collected, environment contained
  Process: Remove malware, patch vulnerabilities, rebuild
  Output: Root cause eliminated, clean systems

Stage: Recovery
  Input:  Clean systems
  Process: Restore from backup, monitor, validate
  Output: Systems back in production, validated clean

Stage: Post-Incident
  Input:  Incident fully resolved
  Process: Lessons learned, report, improve
  Output: Incident report, improvement plan, updated playbooks
```

### Kriteria Stage Transitions

Tidak semua insiden melewati semua stages secara linear. Beberapa insiden mungkin:
- **Loop back**: Evidence Gathering menemukan indikasi bahwa containment belum sempurna → kembali ke Containment
- **Skip stages**: False positive → Triage → Notification (false positive) → Post-Incident (update tuning)
- **Parallel stages**: Evidence Gathering bisa berjalan paralel dengan Containment (ambil memory dump sebelum disconnect)

Transisi antar stages diputuskan berdasarkan:
| Kriteria | Contoh |
|----------|--------|
| **Stage goals met** | Containment berhasil → lanjut Evidence Gathering |
| **New intelligence** | Ditemukan IOCs baru → kembali ke Detection |
| **Resource constraints** | Tim tidak cukup → hold di stage tertentu |
| **External factors** | Legal meminta lanjutan → lanjut |
| **Risk change** | Risiko meningkat → percepat containment |

---

## 4. Preparation — Building IR Capability

### Esensi Preparation

Preparation adalah **satu-satunya stage yang terjadi SEBELUM insiden**. Stage ini menentukan seberapa efektif seluruh respon nantinya. Tidak ada IR yang bagus tanpa persiapan yang matang.

### Komponen IR Preparation

```
┌──────────────────────────────────────────────────────┐
│                   IR Preparation                       │
├──────────────────────────────────────────────────────┤
│  1. IR Policy & Plan                                  │
│  2. IR Team Structure                                 │
│  3. Tools & Infrastructure                            │
│  4. Playbooks & Runbooks                              │
│  5. Training & Exercises                              │
│  6. Communication Channels                            │
│  7. Legal & Compliance Framework                      │
│  8. External Relationships                            │
└──────────────────────────────────────────────────────┘
```

### 1. IR Policy & Plan

**Incident Response Policy** adalah dokumen tingkat tinggi yang mendefinisikan:
- Tujuan dan ruang lingkup IR
- Definitions (apa itu "insiden"?)
- Roles and responsibilities
- Management commitment
- Regulatory requirements
- Enforcement

**Incident Response Plan** adalah dokumen operasional:
- Step-by-step procedures per phase
- Communication templates
- Escalation matrix
- Contact lists
- Decision authority

Karakteristik IR Plan yang baik:
| Ciri | Penjelasan |
|------|------------|
| **Practical** | Bisa diikuti dalam situasi stres |
| **Clear** | Tidak ambigu tentang siapa melakukan apa |
| **Flexible** | Bisa adaptasi untuk berbagai jenis insiden |
| **Accessible** | Tersedia offline dan online |
| **Tested** | Sudah diuji melalui tabletop exercises |
| **Versioned** | Selalu diperbarui |

### 2. IR Team Structure

Struktur tim IR bisa bervariasi tergantung organisasi:

```
                    IR Commander
                         │
        ┌────────────────┼────────────────┐
        │                │                │
   Technical Lead    Communication     Legal Counsel
        │                │                │
   ┌────┴────┐       PR Team         Compliance
   │         │
   Analyst   Forensics
    Team       Team
```

**Model Tim IR**:

| Model | Deskripsi | Cocok Untuk |
|-------|-----------|-------------|
| **Centralized** | Satu tim IR pusat untuk seluruh organisasi | Organisasi kecil-menengah |
| **Distributed** | Masing-masing unit punya IR team sendiri | Organisasi besar dengan banyak segmen |
| **Hybrid** | Tim pusat + liaison di setiap unit | Organisasi besar dan kompleks |
| **Virtual/CSIRT** | Tim dibentuk saat insiden dari berbagai fungsi | Organisasi yang tidak punya dedicated IR team |

**Peran Kunci dalam IR Team**:

| Role | Tanggung Jawab |
|------|----------------|
| **IR Manager/Commander** | Overall coordination, decision authority, management interface |
| **Technical Lead** | Investigasi teknis, containment, eradication |
| **Forensic Analyst** | Evidence collection, analysis, chain of custody |
| **Communications Lead** | Internal & external communication, PR |
| **Legal Counsel** | Legal advice, regulatory compliance, disclosure obligations |
| **HR Representative** | Jika insiden melibatkan insider threat |
| **SME (Subject Matter Expert)** | Untuk sistem spesifik (database, network, cloud) |

### 3. Tools & Infrastructure

IR team harus memiliki akses ke tools yang sudah dikonfigurasi dan siap pakai:

| Kategori | Tools |
|----------|-------|
| **SIEM/SOAR** | Aggregation log, alert correlation, automated response |
| **Endpoint Detection** | EDR agents, antivirus, HIDS |
| **Network Detection** | NIDS, network capture, netflow |
| **Forensic** | Memory acquisition, disk imaging, timeline analysis |
| **Malware Analysis** | Sandbox, disassembler, YARA |
| **Communication** | Encrypted chat, conference bridge, war room |
| **Case Management** | Ticketing system, evidence management, documentation |

**Golden Image** — Siapkan workstation IR yang sudah dilengkapi semua tools, forensic toolkit, dan terisolasi dari network produksi. Jangan menginstal tools di sistem yang terkompromi.

### 4. Playbooks & Runbooks

Perbedaan playbook dan runbook:
- **Playbook**: Panduan strategis — apa yang dilakukan untuk jenis insiden tertentu
- **Runbook**: Panduan teknis — bagaimana melakukan langkah spesifik

Playbook harus mencakup:
| Skenario | Tujuan |
|----------|--------|
| Ransomware | Containment, communication, recovery decision |
| Data breach | Evidence preservation, notification, legal |
| DDoS | Mitigation, upstream communication |
| Insider threat | HR coordination, legal, evidence |
| Phishing | User notification, mailbox investigation |
| Malware outbreak | Network isolation, endpoint scanning |
| Cloud incident | Provider coordination, misconfiguration fix |
| APT/long-term | Threat hunting, persistence removal |

Setiap playbook harus menjawab:
1. **What**: Jenis insiden apa ini?
2. **Who**: Siapa yang perlu dilibatkan?
3. **When**: Kapan tindakan tertentu diambil?
4. **How**: Langkah-langkah teknis apa?
5. **Stop**: Kapan kita tahu sudah selesai?

### 5. Training & Exercises

| Jenis | Deskripsi | Frekuensi |
|-------|-----------|-----------|
| **Awareness training** | Untuk semua karyawan: cara report insiden | Yearly |
| **Technical training** | Untuk IR team: tools, techniques | Quarterly |
| **Tabletop exercise** | Diskusi skenario tanpa sistem nyata | Quarterly |
| **Walkthrough** | Simulasi teknis di lab | Semi-annual |
| **Full exercise** | Simulasi penuh dengan sistem nyata | Annual |

**Tabletop Exercise Framework**:

```
1. Skenario diperkenalkan
2. Peserta mendiskusikan respon secara verbal
3. Facilitator memperkenalkan inject (twist)
4. Peserta menyesuaikan respon
5. Debrief dan lessons learned
```

### 6. Communication Channels

Siapkan jalur komunikasi yang terpisah dari infrastruktur reguler (karena infrastruktur regular mungkin ikut terkena insiden):

| Channel | Use Case | Backup |
|---------|----------|--------|
| Encrypted messaging | Real-time team coordination | SMS |
| Conference bridge | Voice coordination | PSTN |
| Email/List | Formal communication | Out-of-band email |
| War room | Physical/virtual central coordination | Alternate location |
| Status page | External communication | Social media |

**Prinsip golden**: Punya out-of-band communication yang tidak bergantung pada infrastruktur yang sama.

### 7. Legal & Compliance Framework

Sebelum insiden:
- Tentukan yurisdiksi yang relevan
- Pahami kewajiban notifikasi (GDPR 72 jam, HIPAA, dll)
- Siapkan kontrak dengan forensic firms, legal counsel
- Tentukan kebijakan disclosure

### 8. External Relationships

Bangun hubungan SEBELUM insiden:
| Hubungan | Tujuan |
|----------|--------|
| **Law enforcement** | Cybercrime reporting, evidence handling |
| **ISACs/ISAOs** | Threat intelligence sharing |
| **Forensic firms** | Third-party investigation capacity |
| **PR/Communications** | Crisis communication preparation |
| **Internet provider/Cloud provider** | Abuse reporting, mitigation support |
| **Regulator** | Reporting requirements |

---

## 5. Recording & Detection — Finding the Signal

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

Dokumentasi bukan birokrasi — dokumentasi adalah **alat investigasi**. Dokumentasi yang baik membantu:
- Mengingat detail saat membuat laporan
- Mentransfer pengetahuan antar shift
- Menyediakan bukti untuk legal
- Mengukur efektivitas respon

Gunakan format **who, what, when, where, why, how** untuk setiap temuan.

---

## 6. Triage & Prioritization — Decision Framework

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

## 7. Notification & Escalation — Communication Protocols

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

---

## 8. Containment Strategies — Stop the Bleeding

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

## 9. Evidence Gathering & Forensic Readiness

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

---

## 10. Eradication — Removing the Threat

### Esensi Eradication

Eradication adalah **proses menghilangkan root cause dan semua artifact insiden dari lingkungan**. Containment menghentikan penyebaran, eradication membersihkan.

### Eradication vs Containment

```
Containment:  "Stop the bleeding" — tindakan sementara
Eradication:  "Heal the wound" — solusi permanen
```

Eradication TIDAK boleh dilakukan sebelum:
1. Evidence sudah dikumpulkan (jangan bersihkan bukti)
2. Root cause sudah diidentifikasi (jangan hanya treat symptom)
3. Scope sudah diketahui (jangan bersihkan hanya satu titik)
4. Containment sudah berhasil (jangan eradication di lingkungan yang masih aktif)

### Eradication Strategy

| Strategi | Deskripsi | Cocok Untuk |
|----------|-----------|-------------|
| **Clean** | Remove malware, close backdoor, patch | Infeksi ringan, root cause jelas |
| **Rebuild** | Reimage sistem dari golden image | Kompromi berat, root cause tidak jelas |
| **Replace** | Ganti dengan hardware/instance baru | Hardware compromised, cloud |
| **Patch** | Tutup vulnerability | Exploit via vulnerability |
| **Restore from backup** | Kembalikan ke state sebelum insiden | Data corruption, ransomware |
| **Reconfigure** | Perbaiki konfigurasi | Misconfiguration, policy bypass |

Pertimbangkan: **Clean vs Rebuild** adalah keputusan besar.

| Aspek | Clean | Rebuild |
|-------|-------|---------|
| **Kecepatan** | Lebih cepat | Lebih lambat |
| **Kepastian** | Kurang yakin bersih | Yakin bersih |
| **Resource** | Lebih murah | Lebih mahal |
| **Evidence** | Bisa merusak evidence | Evidence sudah diambil |
| **Root cause** | Bisa dipelajari | Root cause harus sudah diketahui |

### Langkah-langkah Eradication

1. **Identify root cause**: Bagaimana attacker masuk pertama kali?
2. **Identify all persistence**: Scheduled tasks, services, registry, startup items, cron, systemd
3. **Identify backdoors**: New accounts, SSH keys, web shells, reverse shells
4. **Identify C2 mechanisms**: Beaconing, DNS tunneling, domain fronting
5. **Remove all artifacts**: Files, registry keys, processes, services
6. **Patch vulnerability**: Fix the root cause
7. **Change compromised credentials**: All passwords, tokens, keys
8. **Verify eradication**: Scan for IOCs, check for persistence

### Common Persistence Mechanisms

**Windows**:
| Mechanism | Detection |
|-----------|-----------|
| Registry Run keys | Autoruns, Sysinternals |
| Scheduled tasks | schtasks, event log |
| Service installation | services.msc, sc query |
| Startup folder | Shell:startup |
| WMI persistence | wmic, WMI Explorer |
| DLL hijacking | Process Monitor |
| Bootkit/MBR | Secure Boot check |
| Group Policy | GPMC |
| Active Directory | ADSI Edit |

**Linux**:
| Mechanism | Detection |
|-----------|-----------|
| Cron jobs | crontab -l, /etc/cron* |
| systemd services | systemctl list-units |
| .bashrc / .profile | Check user home dirs |
| SSH authorized_keys | ~/.ssh/authorized_keys |
| LD_PRELOAD | Check environment |
| Kernel modules | lsmod |
| Web shells | Web server logs, file scan |
| init.d / rc.local | Check rc scripts |

**Cloud**:
| Mechanism | Detection |
|-----------|-----------|
| IAM backdoor users | Cloud trail, IAM audit |
| Access keys | IAM last used |
| Lambda persistence | Cloud trail |
| API Gateway | API logs |
| Container escape | Audit logs |
| Service meshes | mTLS audit |

### Eradication Verification

Setelah eradication, verifikasi:
1. **Scan ulang** — Full AV/EDR scan, YARA rules, custom IOC scan
2. **Log review** — Pastikan tidak ada aktivitas mencurigakan setelah eradication
3. **Persistence check** — Periksa semua persistence mechanisms
4. **Network monitoring** — Pantau C2 communication
5. **User activity** — Periksa user accounts yang terlibat
6. **Timeline analysis** — Pastikan semua activity berhenti di titik eradication

### Common Eradication Mistakes

| Mistake | Dampak | Pencegahan |
|---------|--------|------------|
| **Hanya hapus malware tanpa patch** | Re-infection | Fix root cause |
| **Lupa backdoor user** | Attacker masuk lagi | Full account audit |
| **Hanya bersihkan satu endpoint** | Lateral movement | Full scope eradication |
| **Skip verification** | False sense of security | Always verify |
| **Hapus evidence** | Legal implications | Evidence sudah dikumpulkan |
| **Restore dari backup terkompromi** | Re-infection | Verify backup is clean |

---

## 11. Recovery — Restoring Operations

### Esensi Recovery

Recovery adalah **proses mengembalikan sistem ke operasi normal** setelah eradication selesai. Recovery bukan hanya "nyalakan lagi" — tapi memastikan sistem kembali dengan aman, dimonitor ketat, dan siap didukung.

### Recovery Decision Framework

```
Apakah root cause sudah diidentifikasi?
  ├── Tidak → Kembali ke Eradication
  └── Ya → Lanjut
          
Apakah eradikasi sudah diverifikasi?
  ├── Tidak → Lakukan verifikasi dulu
  └── Ya → Lanjut
          
Apa sumber recovery?
  ├── Rebuild from golden image → Paling aman
  ├── Restore from backup → Verifikasi backup bersih
  └── Clean existing system → Risiko residual terbesar
          
Bagaimana urutan recovery?
  ├── Non-critical → Critical (progressive)
  ├── Read-only → Read-write (by risk)
  └── Isolated → Connected (by trust)

Apakah monitoring diperketat?
  ├── Tidak → Jangan recovery dulu
  └── Ya → Lanjut recovery
```

### Recovery Types

| Type | Deskripsi | Cocok Untuk |
|------|-----------|-------------|
| **Rebuild from golden image** | OS + aplikasi dari image bersih | Full compromise |
| **Restore from backup** | Data dari backup pra-insiden | Ransomware, data corruption |
| **Automated recovery** | Infrastructure as Code deploy | Cloud, container |
| **Manual recovery** | Step-by-step reconfiguration | Simple systems |
| **Hot standby failover** | Switch to DR site | Critical systems |
| **Gradual recovery** | Per-service recovery | Complex environments |

### Recovery Sequence

1. **Non-critical systems first** — Test recovery process di lingkungan non-kritis
2. **Read-only systems** — Pastikan tidak ada write-back ke sistem yang belum clean
3. **Isolated validation** — Nyalakan di network terisolasi, validasi functionality
4. **Monitor intensif** — Aktifkan monitoring ekstra, pantau anomali
5. **Connect carefully** — Hubungkan ke production network secara bertahap
6. **User access restoration** — Kembalikan akses user setelah konfirmasi aman
7. **Full operation** — Kembali ke operasi normal
8. **Continued monitoring** — Pantau untuk residual activity

### Recovery Monitoring Checklist

| Monitor | What to Look For |
|---------|-----------------|
| **Authentication** | Anomalous logins, privilege escalation |
| **Network** | Unexpected outbound connections, data transfer |
| **Process** | Unknown processes, unusual parent-child |
| **File system** | New files in unusual locations |
| **Registry/Config** | Unexpected changes |
| **User activity** | Abnormal behavior |
| **Performance** | Unusual CPU/memory/disk |
| **DNS** | Queries to known-bad domains |

### Rollback Plan

Setiap recovery harus punya rollback plan:
1. **Jika monitoring mendeteksi anomali** → Apa yang dilakukan?
2. **Jika sistem tidak stabil** → Kapan kembali ke backup?
3. **Jika user melapor masalah** → Siapa yang handle?
4. **Jika compliance tidak terpenuhi** → Siapa yang approve?

### Recovery Validation

Setelah recovery:
- **Functional validation**: Apakah sistem bekerja normal?
- **Security validation**: Apakah monitoring menunjukkan aktivitas bersih?
- **Compliance validation**: Apakah kontrol keamanan masih berfungsi?
- **Performance validation**: Apakah performa normal?
- **Data integrity validation**: Apakah data akurat dan lengkap?

---

## 12. Post-Incident Activity — Lessons Learned

### Esensi Post-Incident

Post-Incident adalah **proses belajar dari insiden untuk mencegah terulang dan meningkatkan kemampuan IR**. Stage ini paling sering di-skip karena "sudah selesai, move on" — padahal ini yang paling bernilai jangka panjang.

### Komponen Post-Incident

```
Post-Incident
├── 1. Incident Report
├── 2. Lessons Learned Meeting
├── 3. Root Cause Analysis (RCA)
├── 4. Improvement Plan
├── 5. Playbook Update
├── 6. Metrics & KPIs
└── 7. Evidence Retention & Destruction
```

### Incident Report

Incident report adalah **dokumentasi lengkap seluruh lifecycle insiden**. Ini berbeda dari timeline operational — ini adalah laporan formal.

**Struktur Incident Report**:

```
1. Executive Summary
   - Apa yang terjadi, dampak, tindakan kunci
   - 1-2 paragraph untuk management

2. Incident Timeline
   - Chronological order of events
   - Detection → Response → Recovery → Closure

3. Scope & Impact
   - Systems affected
   - Data affected
   - Business impact
   - Financial impact (if calculable)

4. Root Cause Analysis
   - Why did this happen?
   - Contributing factors

5. Response Evaluation
   - What went well
   - What went wrong
   - What was unexpected

6. Evidence Summary
   - Evidence collected
   - Chain of custody

7. Lessons Learned
   - Technical lessons
   - Process lessons
   - Team lessons
   - Communication lessons

8. Recommendations
   - Immediate actions
   - Short-term (1-3 months)
   - Long-term (3-12 months)

9. Action Items
   - Owner, deadline, priority
```

### Lessons Learned Meeting

Format Lessons Learned (juga disebut Post-Incident Review / PIR):

**Peserta Wajib**:
- IR team yang terlibat
- System owner
- Management representative
- Legal (optional)

**Agenda**:
1. Timeline review — what happened chronologically
2. What went well — celebrate successes
3. What went wrong — blameless identification
4. What was missing — gaps in tools, people, process
5. What surprised us — things we didn't anticipate
6. Recommendations — concrete improvements
7. Action items — who, what, when

**Aturan Blameless Post-Mortem**:
- Fokus pada sistem dan proses, bukan individu
- Asumsi semua orang melakukan yang terbaik dengan informasi yang ada
- Ganti "siapa yang salah" dengan "apa yang bisa diperbaiki"
- Setiap rekomendasi harus actionable

### Root Cause Analysis (RCA)

RCA bertujuan menjawab: **Mengapa insiden ini terjadi?** Teknik yang sering digunakan:

**5 Whys**:
1. Why did the attacker gain access? → Spear-phishing email
2. Why did the user click? → Email looked legitimate
3. Why didn't security filter catch it? → DMARC not enforced
4. Why is DMARC not enforced? → Migration to new email provider incomplete
5. Why was migration incomplete? → No project owner assigned

**Fishbone Diagram**:
```
People              Process              Technology
  │                    │                    │
  │ Lack of training   │ No verification    │ Missing DMARC
  │ Fatigue            │ No escalation      │ No spam filter
  │                    │                    │
  └────────────────────┼────────────────────┘
                      │
                      ▼
                 Insiden Phishing
                      ▲
  ┌────────────────────┼────────────────────┐
  │                    │                    │
  │ No policy          │ No review cycle    │ No budget
  │ No SLA             │ Overworked team    │
  │                    │                    │
Policy              Management            Budget
```

### Improvement Plan

Setiap lessons learned harus menghasilkan **actionable improvements**:

| Kategori | Contoh Improvement |
|----------|-------------------|
| **People** | Training tambahan, hire specialist, tabletop exercise |
| **Process** | Playbook baru, escalation update, communication template |
| **Technology** | Tool deployment, logging enhancement, SIEM rule |
| **Policy** | Policy baru, policy update, approval process |
| **Partnership** | New vendor, retainer agreement, ISAC membership |

Setiap action item harus:
- **Specific**: Apa yang harus dilakukan
- **Measurable**: Bagaimana tahu sudah selesai
- **Assignable**: Ada owner yang jelas
- **Realistic**: Dapat dilakukan dengan resource yang ada
- **Time-bound**: Ada deadline

### Metrics & KPIs

Ukur efektivitas IR:

| Metric | Formula | Target |
|--------|---------|--------|
| **Time to Detect (TTD)** | Waktu dari kompromi ke deteksi | < 1 jam |
| **Time to Triage (TTT)** | Waktu dari deteksi ke triage | < 15 menit |
| **Time to Contain (TTC)** | Waktu dari deteksi ke containment | < 1 jam |
| **Time to Eradicate (TTE)** | Waktu dari containment ke eradication | < 4 jam |
| **Time to Recover (TTR)** | Waktu dari eradication ke recovery | < 8 jam |
| **Mean Time to Resolve (MTTR)** | Rata-rata waktu dari deteksi ke closure | < 24 jam |
| **False Positive Rate** | False positives / Total alerts | < 10% |
| **Escalation Rate** | Escalated incidents / Total incidents | < 20% |

### Evidence Retention & Destruction

Evidence hasil investigasi perlu diatur:

| Jenis Evidence | Retention Period | Destruction Method |
|---------------|------------------|--------------------|
| **For ongoing legal** | Sampai kasus selesai | Secure wipe + certificate |
| **For regulatory** | Sesuai regulation (1-7 tahun) | Secure wipe + certificate |
| **For internal learning** | 6-12 bulan setelah final report | Deletion |
| **Negative findings** | 3-6 bulan | Deletion |
| **Logs** | Sesuai log retention policy | Overwrite |

---

## 13. Incident Types & Response Playbooks

### Esensi Playbook

Playbook adalah **panduan strategis untuk jenis insiden tertentu**. Setiap playbook memberikan langkah-langkah keputusan yang sudah teruji, mengurangi waktu berpikir saat krisis.

### Playbook 1: Ransomware

**Tujuan**: Menghentikan penyebaran ransomware dan meminimalkan data loss.

**Triage & Detection**:
- Endpoint melaporkan file terenkripsi
- Ransom note muncul di desktop
- File extension berubah (contoh: .encrypted, .lockbit)
- Log menunjukkan proses encryption massal

**Containment**:
1. Isolasi endpoint dari network segera
2. Disable semua network share di segment terkena
3. Block ransomware extensions di perimeter (jika sudah diketahui)
4. Jangan matikan endpoint — capture memory dulu

**Evidence**:
1. Screenshot ransom note
2. Capture memory dari affected endpoint
3. Collect sample encrypted file + ransom note
4. Log timestamps dari encryption start

**Decision Points**:
- Bayar tebusan? → Hanya keputusan EXECUTIVE, dengan input legal
- Restore dari backup? → Verifikasi backup tidak terenkripsi
- Notify law enforcement? → Ya, ransomware adalah criminal activity

**Eradication & Recovery**:
1. Reimage semua endpoint terkena
2. Restore data dari backup bersih
3. Patch initial vector (biasanya RDP, phishing, atau vulnerability)

**Prevention untuk masa depan**:
- Backup 3-2-1 rule
- Network segmentation ketat
- Disable RDP from internet
- Email security gateway
- EDR dengan anti-ransomware

### Playbook 2: Data Breach / Data Exfiltration

**Tujuan**: Menghentikan kebocoran data, menentukan scope, memenuhi kewajiban notifikasi.

**Triage & Detection**:
- DLP alert
- Unusual large outbound data transfer
- Customer notification
- Dark web discovery

**Containment**:
1. Identifikasi dan block exfiltration vector
2. Revoke compromised credentials
3. Isolasi database atau share yang bocor
4. Block IP tujuan exfiltration di firewall

**Evidence**:
1. Log transfer data (siapa, kapan, berapa)
2. Data yang bocor (sample untuk identifikasi)
3. Akses log dari akun terkompromi
4. Timeline exfiltration

**Decision Points**:
- Apakah data termasuk PII/PHI? → Regulatory notification wajib
- Apakah data finansial? → PCI DSS notification
- Apakah data terenkripsi? → Kurangi severity
- Berapa jumlah record? → Threshold notification

**Eradication & Recovery**:
1. Patch vulnerability
2. Reset semua credentials terkait
3. Implement additional monitoring
4. Prepare disclosure notifications

**Regulatory Timelines**:
- GDPR: 72 jam ke supervisory authority
- HIPAA: 60 hari ke affected + HHS
- State breach laws: 30-90 hari

### Playbook 3: Account Compromise

**Tujuan**: Menghentikan akses unauthorized dan memulihkan akun.

**Triage & Detection**:
- Successful login dari lokasi tidak biasa
- Multiple failed logins lalu success
- User reports suspicious activity dari akunnya
- SIEM alert: impossible travel

**Containment**:
1. Disable akun
2. Force logout semua sessions
3. Revoke semua tokens, API keys, sessions
4. Reset password (jika disable bukan pilihan)

**Evidence**:
1. Log login history (lokasi, IP, timestamp, user agent)
2. Email access log (email read, sent, forwarding rules)
3. File access log (files viewed, downloaded)
4. API calls log (jika cloud)

**Decision Points**:
- Apakah MFA aktif? → Jika tidak, kritikalitas lebih tinggi
- Apakah akun admin? → Scope lebih luas, prioritaskan
- Apakah email terakses? → Check forwarding rules, email content

**Eradication & Recovery**:
1. Remove malicious forwarding rules
2. Remove malicious email filters
3. Check for persistence (OAuth apps, service principals)
4. Enable MFA
5. User awareness reinforcement

### Playbook 4: Phishing / BEC (Business Email Compromise)

**Tujuan**: Mengidentifikasi scope, menghentikan propagation, memulihkan akun.

**Triage & Detection**:
- User reports suspicious email
- SIEM alert: multiple users clicking same link
- Finance department receives invoice change request
- Email security gateway alert

**Containment**:
1. Remove malicious email dari semua mailbox (search & destroy)
2. Block sender domain/IP
3. Block malicious URL di web gateway
4. Disable compromised accounts

**Evidence**:
1. Full email header
2. Email copy (with attachments)
3. URL analysis (where it leads)
4. Mailbox rules created
5. Sent items (what was sent from compromised account)

**Decision Points**:
- Apakah BEC? → Transaction reversal mungkin perlu
- Apakah credential harvesting? → Force password reset
- Apakah malware delivery? → Endpoint scan
- Scope: berapa banyak user yang menerima?

**Eradication & Recovery**:
1. Password reset untuk semua user yang klik
2. MFA enforcement
3. User training — this is a teaching moment
4. Update email security rules

### Playbook 5: Insider Threat

**Tujuan**: Menghentikan aktivitas insider sambil meminimalkan risiko legal dan mempertahankan employment rights.

**Triage & Detection**:
- Unusual data access (malam, weekend, large volume)
- HR notification (resignation, disciplinary)
- Policy violation report
- DLP alert on user

**PENTING**: Insider threat adalah **yang paling sensitif secara legal**. Koordinasi dengan HR dan Legal SEBELUM tindakan apapun.

**Containment**:
1. Disable akses secara rahasia (jangan trigger)
2. Preserve data — jangan konfrontasi
3. Monitor activity lebih ketat
4. HR involvement before any action

**Evidence**:
1. Access logs (file, system, building)
2. Email and communication
3. Data transfer logs
4. Physical security logs (badge access)
5. HR records (employment status, performance)

**Decision Points**:
- Apakah ini pelanggaran policy? → Internal action
- Apakah ini kriminal? → Law enforcement
- Apakah ini terminasi? → HR process
- Apakah ini unintentional? → Training

**Recovery**:
1. Access revocation
2. Asset return
3. IT deprovisioning
4. Documentation for legal

### Playbook 6: DDoS / Availability Attack

**Tujuan**: Mengembalikan availability layanan.

**Triage & Detection**:
- Traffic spike dari banyak source IP
- Service slow atau down
- Cloud/CDN scaling alerts
- Customer complaints

**Containment**:
1. Enable DDoS mitigation (cloud provider, CDN)
2. Rate limiting di WAF/load balancer
3. Blackhole routing jika perlu
4. Scale infrastructure

**Evidence**:
1. Traffic capture (PCAP)
2. Logs — source IPs, patterns, duration
3. Bandwidth utilization graphs
4. Mitigation effectiveness data

**Decision Points**:
- Apakah ini DDoS atau DoS? → Multiple sources?
- Apakah ini application layer atau network layer? → Layer 7 vs Layer 3/4
- Apakah ada extortion? → Law enforcement

**Recovery**:
1. Monitor traffic for residual
2. Analyze attack patterns
3. Update WAF rules
4. Implement permanent mitigation

### Playbook 7: Cloud Incident

**Tujuan**: Mengidentifikasi dan menghentikan akses unauthorized di cloud environment.

**Triage & Detection**:
- Cloud trail alert
- Unusual API calls
- New resources deployed unexpectedly
- Billing spike
- CSP notification

**Containment**:
1. Revoke compromised keys
2. Restrict IAM policy
3. Isolate compromised resources (security group, VAC)
4. Enable CloudTrail/audit logging if disabled

**Evidence**:
1. Cloud trail logs
2. IAM access logs
3. Resource configuration history
4. Billing data

**Decision Points**:
- Apakah ini misconfiguration atau intentional attack?
- Apakah data di bucket publik?
- Apakah compute instance compromised?

**Eradication & Recovery**:
1. Remove unauthorized resources
2. Fix misconfigurations
3. Rotate ALL keys (not just compromised)
4. Implement IaC with security scanning

### Playbook 8: Web Application Compromise

**Tujuan**: Mengidentifikasi dan menutup vulnerability web application.

**Triage & Detection**:
- WAF alerts
- Web server logs showing exploitation attempts
- File integrity monitoring alert
- Customer reports defacement

**Containment**:
1. Take application offline if necessary
2. Block attacking IPs
3. WAF rule update
4. Disable compromised functionality

**Evidence**:
1. Web server logs (access, error)
2. Application logs
3. Database logs
4. File system changes
5. Network connections from web server

**Eradication & Recovery**:
1. Remove web shells
2. Patch vulnerability
3. Update WAF rules
4. Code review for similar vulnerabilities
5. Re-deploy from clean codebase

---

## 14. Legal, Compliance & Ethics

### Esensi Legal dalam IR

Insiden keamanan hampir selalu memiliki dimensi legal. **Setiap tindakan IR bisa menjadi bukti di pengadilan** atau menjadi dasar gugatan. Pahami implikasi hukum dari setiap langkah.

### Regulasi yang Relevan

| Regulation | Scope | IR Impact |
|-----------|-------|-----------|
| **GDPR** | EU personal data | 72-hour notification, DPO involvement |
| **HIPAA** | US health data | 60-day notification, OCR investigation |
| **PCI DSS** | Cardholder data | Forensic investigation required, brand notification |
| **SOX** | Public companies | Materiality assessment, board reporting |
| **GLBA** | Financial services | Customer notification, regulator notification |
| **CCPA/CPRA** | California residents | Consumer notification, right to know |
| **State breach laws** | All 50 US states | Varying notification timelines |

### Key Legal Concepts

**Chain of Custody**: Tanpa chain of custody yang valid, evidence bisa ditolak di pengadilan. Setiap transfer evidence harus tercatat.

**Privilege**: Komunikasi dengan legal counsel mungkin dilindungi oleh attorney-client privilege. Tandai komunikasi dengan "PRIVILEGED AND CONFIDENTIAL — ATTORNEY CLIENT COMMUNICATION" jika legal involved.

**Spoliation**: Menghancurkan atau mengubah evidence yang relevan dengan litigasi. Bisa mengakibatkan: default judgment, monetary sanctions, adverse inference.

**Electronic Discovery (eDiscovery)**: Proses discovery untuk electronic evidence dalam litigasi. IR team harus koordinasi dengan legal untuk preservation hold.

**Data Privacy**: IR team mungkin mengakses data pengguna selama investigasi. Ini harus sesuai dengan privacy policy dan regulasi.

### Kapan Libatkan Law Enforcement

| Faktor | Pertimbangan |
|--------|-------------|
| **Type of crime** | Cybercrime, fraud, child safety → wajib |
| **Financial loss** | > threshold tertentu → pertimbangkan |
| **Critical infrastructure** | Wajib notifikasi |
| **Jurisdiction** | Cross-border → perlu koordinasi |
| **Evidence preservation** | Law enforcement punya tools lebih baik |
| **Public interest** | Jika publik berisiko |

### Etika Incident Handler

| Prinsip | Implementasi |
|---------|--------------|
| **Confidentiality** | Jangan diskusikan insiden di luar need-to-know |
| **Integrity** | Jangan mengubah evidence atau timeline |
| **Objectivity** | Jangan bias berdasarkan siapa yang terlibat |
| **Professionalism** | Tetap tenang, metodis, dan terdokumentasi |
| **Accountability** | Akui kesalahan, catat keputusan yang salah |
| **Transparency** | Jangan menyembunyikan informasi dari stakeholder yang berhak |

### Regulatory Notification Decision Tree

```
Apakah insiden melibatkan personal data?
  ├── Tidak → Mungkin tidak perlu notifikasi
  └── Ya → Lanjut

Apakah data termasuk dalam regulated category?
  ├── PII (GDPR/CCPA) → Notifikasi
  ├── Health (HIPAA) → Notifikasi
  ├── Financial (PCI/GLBA) → Notifikasi
  └── Internal only → Mungkin tidak

Apakah ada risiko harm pada individu?
  ├── Ya (identity theft, fraud) → Notifikasi wajib
  └── Tidak → Mungkin tidak perlu

Apakah data terenkripsi?
  ├── Ya, dengan key yang aman → Notifikasi mungkin tidak perlu
  └── Tidak atau key compromised → Notifikasi

Apakah regulator sudah menetapkan threshold?
  ├── Ya, dan exceed → Notifikasi
  └── Ya, dan di bawah → Dokumentasi tapi mungkin tidak notifikasi
```

---

## 15. Decision Framework & Trade-offs

### Esensi Decision Framework

Incident handler terus-menerus membuat keputusan dengan informasi tidak lengkap di bawah tekanan waktu. Decision framework membantu membuat keputusan **konsisten dan dapat dipertanggungjawabkan**.

### OODA Loop dalam IR

OODA (Observe, Orient, Decide, Act) adalah framework pengambilan keputusan militer yang sangat relevan untuk IR:

```
Observe ───→ Orient ───→ Decide ───→ Act
   ↑                                      │
   └──────────────────────────────────────┘
```

**Observe**: Kumpulkan data (alert, logs, report)
**Orient**: Analisis dalam konteks (BIA, threat intel, knowledge base)
**Decide**: Pilih tindakan berdasarkan analisis
**Act**: Eksekusi tindakan
**Loop**: Evaluasi hasil, observe lagi

### Decision Points Sepanjang IR Lifecycle

| Stage | Decision Point | Options |
|-------|---------------|---------|
| **Detection** | Is this an incident? | Yes / No / Need more data |
| **Triage** | What priority? | P0-P4 |
| **Notification** | Who needs to know? | IR team / Management / Legal / Regulator / Public |
| **Containment** | Contain first or evidence first? | Evidence → Contain / Contain → Evidence |
| **Containment** | Isolate or disconnect? | Network isolate / Power off / Do nothing |
| **Containment** | Temporary or permanent? | Short-term / Long-term |
| **Evidence** | What to collect? | Full disk / Memory only / Targeted |
| **Eradication** | Clean or rebuild? | Clean / Rebuild / Replace |
| **Recovery** | When to restore? | Now / Wait / Gradual |
| **Recovery** | Restore or rebuild? | Restore backup / Rebuild |
| **Post-Incident** | What to improve? | People / Process / Technology |

### Trade-off Matrix

| Trade-off | When to Choose A | When to Choose B |
|-----------|-----------------|------------------|
| **Speed vs Accuracy** | Fast: Active spread, data exfiltration | Accurate: Isolated malware, forensics needed |
| **Containment vs Evidence** | Contain: High spread risk | Evidence: Legal case, root cause analysis |
| **Isolate vs Monitor** | Isolate: Active threat | Monitor: APT, intel gathering |
| **Clean vs Rebuild** | Clean: Low compromise, quick fix | Rebuild: Heavy compromise, unknown scope |
| **Internal vs External** | Internal: Low severity, known cause | External: High severity, need expertise |
| **Disclose vs Stay Silent** | Disclose: Legal obligation, customer trust | Stay silent: Under investigation, no legal obligation |
| **Prosecute vs Remediate** | Prosecute: Deterrence, justice | Remediate: Speed, resource, reputation |

### Risk-Based Decision Making

Setiap keputusan IR pada dasarnya adalah **risk management**:

```
Risk = Likelihood × Impact
```

**Pertanyaan untuk setiap opsi**:
1. Apa risiko TIDAK melakukan tindakan ini?
2. Apa risiko MELAKUKAN tindakan ini?
3. Apa risiko MENUNDA keputusan?
4. Opsi mana yang punya risk/reward terbaik?

**Contoh: Containment Decision**

| Opsi | Likelihood of Success | Impact jika Gagal | Risk Score |
|------|----------------------|-------------------|------------|
| Network isolate | 90% | Attacker moves to other systems | 10 |
| Power off | 100% | Lose evidence, downtime | 50 |
| Do nothing | 0% | Full compromise | 100 |

### Communication Decision Tree

```
Siapa yang perlu tahu?
  ├── IR team → Full technical details
  ├── System owner → Technical summary + impact
  ├── Management → Business impact + timeline
  ├── Legal → Regulatory implications + evidence
  ├── PR/Communications → Public-facing narrative
  ├── Regulator → Compliance-focused notification
  ├── Law enforcement → Criminal evidence + request
  └── Customers → Customer-facing notification

Apa format komunikasi?
  ├── Verbal (urgent, real-time)
  ├── Email (documented, formal)
  ├── Written report (comprehensive)
  └── Presentation (for management)

Kapan? → Sesuai SLA dan urgency
```

### Mental Shortcuts (Heuristics) untuk IR

Heuristics yang berguna dalam situasi tekanan:

1. **"When in doubt, isolate"** — Jika tidak yakin scope, isolasi dulu. Lebih baik over-contain daripada under-contain.
2. **"Evidence first, ask later"** — Jika ada kesempatan ambil evidence tanpa risiko besar, ambil dulu.
3. **"Assume worst case, plan for best case"** — Rencanakan untuk skenario terburuk, tapi berharap yang terbaik.
4. **"Nobody ever got fired for documenting too much"** — Dokumentasi berlebihan lebih baik daripada kurang.
5. **"The attacker is probably still there"** — Setelah containment, asumsikan ada residual sampai terbukti bersih.
6. **"Time is the enemy"** — Semakin lama, semakin besar damage. Prioritaskan kecepatan untuk containment.
7. **"You can't un-notify"** — Pikir dua kali sebelum komunikasi eksternal. Lebih baik telat dan akurat daripada cepat dan salah.

---

## 16. Referensi Lengkap

### Standar & Framework

| Referensi | Sumber | Link |
|-----------|--------|------|
| ECIH v3 (212-89) Official Curriculum | EC-Council | https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/ |
| ECIH v3 Exam Blueprint | EC-Council | https://cert.eccouncil.org/ecih/ |
| NIST SP 800-61 Rev 2 — Computer Security Incident Handling Guide | NIST | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |
| NIST SP 800-86 — Guide to Integrating Forensic Techniques into Incident Response | NIST | https://csrc.nist.gov/publications/detail/sp/800-86/final |
| NIST SP 800-83 Rev 1 — Guide to Malware Incident Prevention and Handling | NIST | https://csrc.nist.gov/publications/detail/sp/800-83/rev-1/final |
| SANS PICERL — The Incident Response Process | SANS | https://www.sans.org/white-papers/incident-response-process/ |
| ISO/IEC 27035 — Information Security Incident Management | ISO | https://www.iso.org/standard/78973.html |
| ISO/IEC 27037 — Digital Evidence Handling Guidelines | ISO | https://www.iso.org/standard/44381.html |
| FIRST CSIRT Framework | FIRST | https://www.first.org/resources/guides/csirt-framework |
| ENISA Incident Handling Guide | ENISA | https://www.enisa.europa.eu/publications/incident-handling-guide |

### Regulasi & Hukum

| Referensi | Sumber | Link |
|-----------|--------|------|
| GDPR Art. 33 — Personal Data Breach Notification | EU | https://gdpr-info.eu/art-33-gdpr/ |
| HIPAA Breach Notification Rule | HHS | https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html |
| PCI DSS v4.0 Incident Response Requirements | PCI SSC | https://listings.pcisecuritystandards.org/documents/PCI-DSS-v4-0-Requirements-and-Testing-Procedures.pdf |
| CCPA Breach Notification | CA Legislature | https://oag.ca.gov/privacy/ccpa |
| SOX Compliance Reporting | SEC | https://www.sec.gov/about/forms/form-sarbanes-oxley.pdf |

### Forensic & Evidence

| Referensi | Sumber | Link |
|-----------|--------|------|
| NIST SP 800-86 — Forensic Techniques | NIST | https://csrc.nist.gov/publications/detail/sp/800-86/final |
| SANS Forensic Acquisition Guides | SANS | https://www.sans.org/digital-forensics/ |
| Order of Volatility Reference | SANS Forensics | https://www.sans.org/blog/order-of-volatility/ |
| Digital Forensic Research Workshop (DFRWS) | DFRWS | https://dfrws.org/ |
| Electronic Discovery Reference Model (EDRM) | EDRM | https://edrm.net/ |

### Threat Intelligence & Sharing

| Referensi | Sumber | Link |
|-----------|--------|------|
| MITRE ATT&CK — Enterprise | MITRE | https://attack.mitre.org/ |
| FIRST — Traffic Light Protocol (TLP) | FIRST | https://www.first.org/tlp/ |
| FS-ISAC | FS-ISAC | https://www.fsisac.com/ |
| MS-ISAC (Multi-State ISAC) | CIS | https://www.cisecurity.org/ms-isac/ |
| CISA Cyber Incident Reporting | CISA | https://www.cisa.gov/report |
| CISA — Known Exploited Vulnerabilities Catalog | CISA | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |

### Tools & Technology (Referensi Konseptual)

| Kategori | Contoh (untuk referensi) |
|----------|------------------------|
| **SIEM** | Splunk, ELK Stack, QRadar, Sentinel, Chronicle |
| **EDR** | CrowdStrike, SentinelOne, Defender, Carbon Black |
| **SOAR** | Splunk SOAR, Palo Alto XSOAR, Siemplify |
| **Forensic** | FTK Imager, EnCase, Autopsy, Volatility, Sleuth Kit |
| **Malware Analysis** | Cuckoo Sandbox, CAPE, IDA Pro, Ghidra |
| **Network Forensics** | Wireshark, tcpdump, NetworkMiner, Zeek |
| **Threat Intel** | MISP, OpenCTI, ThreatConnect |
| **Case Management** | TheHive, RTIR, ServiceNow |
| **Backup & Recovery** | Veeam, Commvault, Rubrik, Avamar |

### Organisasi & Komunitas

| Organisasi | Fokus | Link |
|-----------|-------|------|
| FIRST (Forum of Incident Response and Security Teams) | CSIRT global | https://www.first.org/ |
| CISA (Cybersecurity & Infrastructure Security Agency) | US gov IR | https://www.cisa.gov/ |
| ENISA (European Union Agency for Cybersecurity) | EU cybersecurity | https://www.enisa.europa.eu/ |
| APACERT (Asia Pacific Computer Emergency Response Team) | APAC CSIRT | https://www.apcert.org/ |
| OWASP | Web security | https://owasp.org/ |
| (ISC)² | Security certification | https://www.isc2.org/ |

### Buku & Referensi Akademis

| Buku | Penulis | Fokus |
|------|---------|-------|
| Incident Response & Computer Forensics (3rd Ed.) | Luttgens, Pepe, Mandia | IR standard reference |
| The Practice of Network Security Monitoring | Richard Bejtlich | NSM mindset |
| Threat Hunting: Open Source Intelligence in Action | Richard A. | Threat hunting |
| Digital Forensics and Incident Response | Gerard Johansen | Practical IR |
| The Art of Memory Forensics | Ligh, Case, Levy, Walters | Memory forensics |
| Practical Malware Analysis | Sikorski, Honig | Malware reverse engineering |
| Network Forensics: Tracking Hackers | Davidoff, Ham | Network investigation |
| Incident Management for Operations | Rob Schnepp | Operational IR |
| The CERT Guide to Insider Threats | Cappelli et al. | Insider threat |
| Data and Goliath | Bruce Schneier | Privacy & security |

### EC-Council Resources

| Resource | Link |
|----------|------|
| ECIH Official Page | https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/ |
| EC-Council Exam Portal | https://www.eccouncil.org/programs/ |
| EC-Council Continuing Education (ECE) | https://www.eccouncil.org/continuing-education/ |
| ECIH Exam Blueprint v3 | https://cert.eccouncil.org/ecih/ |
| EC-Council Code of Ethics | https://www.eccouncil.org/code-of-ethics/ |

### Incident Report Templates

| Template | Source | Use |
|----------|--------|-----|
| NIST SP 800-61 Incident Report Template | NIST | Standard IR report |
| SANS Incident Handler's Handbook | SANS | Quick reference |
| FIRST PSIRT Incident Response Framework | FIRST | Vendor IR |
| ENISA Incident Reporting Template | ENISA | EU compliant |
| CISA Incident Response Report | CISA | US government |

### Checklist Cepat IR

| Phase | Checklist Item |
|-------|---------------|
| **All** | Apakah dokumentasi sudah diupdate? |
| **Preparation** | Apakah IR Plan sudah di-review tahun ini? |
| **Detection** | Apakah alert sudah dikonfirmasi sebagai true positive? |
| **Triage** | Apakah severity sudah ditentukan berdasarkan BIA? |
| **Notification** | Apakah semua stakeholder sudah di-notify sesuai SLA? |
| **Containment** | Apakah evidence volatile sudah diamankan sebelum containment? |
| **Evidence** | Apakah chain of custody sudah diisi? |
| **Eradication** | Apakah root cause sudah diidentifikasi sebelum cleanup? |
| **Recovery** | Apakah monitoring sudah diperketat selama recovery? |
| **Post-Incident** | Apakah lessons learned meeting sudah dijadwalkan? |

### Key Terms & Definitions

| Term | Definition (ECIH Context) |
|------|---------------------------|
| **Incident** | Any event that violates an organization's security policy and poses a threat to the confidentiality, integrity, or availability of information assets |
| **Event** | Any observable occurrence in a system or network |
| **IR Plan** | Documented set of procedures for detecting, responding to, and recovering from security incidents |
| **Playbook** | Specific step-by-step guide for handling a particular type of incident |
| **BIA** | Business Impact Assessment — process of identifying critical systems and quantifying impact of disruption |
| **MTTD** | Mean Time to Detect |
| **MTTR** | Mean Time to Respond/Resolve |
| **RTO** | Recovery Time Objective — maximum acceptable downtime |
| **RPO** | Recovery Point Objective — maximum acceptable data loss |
| **SLA** | Service Level Agreement — agreed response times |
| **Chain of Custody** | Documentation trail that tracks evidence from collection to court |
| **Order of Volatility** | Sequence for collecting digital evidence from most to least volatile |
| **Root Cause** | The underlying cause of an incident, not just the symptom |
| **Lessons Learned** | Process of reviewing an incident to identify improvements |
| **False Positive** | Alert that incorrectly indicates malicious activity |
| **True Positive** | Alert that correctly identifies malicious activity |
| **Containment** | Actions taken to stop an incident from spreading |
| **Eradication** | Actions taken to remove the threat from the environment |
| **Recovery** | Actions taken to restore normal operations |

---

## Referensi Lengkap Framework

Hubungan antar framework yang sering digunakan dalam IR:

```
ECIH IH&R (9 stages)
   │
   ├── NIST SP 800-61 (4 phases)
   │     └── Basis untuk IR plan organisasi
   │
   ├── SANS PICERL (6 phases)
   │     └── Populer di kalangan praktisi
   │
   ├── ISO 27035 (5 phases)
   │     └── Standar internasional
   │
   └── FIRST CSIRT Framework
         └── Untuk CSIRT maturity assessment
```

Semua framework ini memiliki kesamaan esensi: **Prepare → Detect → Respond → Recover → Improve**. Perbedaannya hanya pada granularitas dan terminologi. Sebagai incident handler, kuasai SATU framework dengan dalam (ECIH 9-stage) dan pahami mapping ke framework lain.

---

*ECIH — Certified Incident Handler Mindset*
*Based on EC-Council ECIH v3 (212-89) curriculum*
*License: MIT*
