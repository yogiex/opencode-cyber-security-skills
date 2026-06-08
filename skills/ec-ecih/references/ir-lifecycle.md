---
name: "IR Lifecycle Framework & Preparation"
description: "ECIH 9-stage Incident Handling & Response lifecycle, framework mapping (NIST 800-61, SANS PICERL), stage transitions, and comprehensive Preparation phase — building IR capability, team structure, tools, playbooks, training, communication channels, and external relationships."
tags: [ecih, ir-lifecycle, preparation, nist-800-61, sans-picerl, csirt, playbooks, tabletop-exercise]
---

## IR Lifecycle Framework

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
│     (Komunikasi ke stakeholder yang tepat)              │
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

## Preparation — Building IR Capability

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
