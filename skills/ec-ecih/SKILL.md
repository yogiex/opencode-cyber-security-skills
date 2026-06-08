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

## How to Use This Skill

Load the right reference file based on what you need:

| When you need to... | Load this file |
|---------------------|----------------|
| Follow the full IR lifecycle or build IR capability | `references/ir-lifecycle.md` |
| Detect, triage, classify, or notify stakeholders | `references/detection-triage.md` |
| Contain an active threat or collect forensic evidence | `references/containment-evidence.md` |
| Eradicate root cause or recover operations | `references/eradication-recovery.md` |
| Write an incident report or run lessons learned | `references/post-incident.md` |
| Handle a specific incident type (ransomware, phishing, DDoS, etc.) | `references/playbooks.md` |
| Determine legal obligations or regulatory notification | `references/legal-compliance.md` |

---

## Daftar Isi

1. [Incident Handler Mindset](#1-incident-handler-mindset)
2. [ECIH Exam Overview & Strategy](#2-ecih-exam-overview--strategy)
3. [Decision Framework & Trade-offs](#3-decision-framework--trade-offs)
4. [Gotchas — Common IR Mistakes](#4-gotchas--common-ir-mistakes)
5. [Incident Report Template](#5-incident-report-template)
6. [IR Quick Reference Checklists](#6-ir-quick-reference-checklists)
7. [Key Terms](#7-key-terms)
8. [Framework Relationships](#8-framework-relationships)

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
│  (Kapan pulih? Apa yang dipelajari?)           │
└──────────────────────────────────────────────┘
```

### Sifat Insiden Keamanan

| Karakteristik | Implikasi |
|--------------|-----------|
| **Adversarial** | Ada musuh yang adaptif, bukan kegagalan acak |
| **Time-sensitive** | Setiap menit delay memperbesar dampak |
| **Uncertain** | Tidak pernah punya informasi lengkap |
| **Evolving** | Situasi berubah selama respon |
| **High-stakes** | Risiko reputasi, finansial, dan legal |
| **Multi-dimensional** | Teknis, legal, PR, bisnis semua terlibat |

### Incident Handler vs SOC Analyst

SOC Analyst biasanya fokus pada **triage dan investigasi awal** — menentukan apakah alert adalah true positive atau false positive. Incident Handler mengambil alih **setelah konfirmasi**:

```
SOC Analyst:  Alert → Triage → Escalate
Incident Handler: Escalate → Contain → Evidence → Eradicate → Recover → Post-Mortem
```

### Pola Pikir Kritis

**"What if I'm wrong?"** — Setiap asumsi yang salah bisa menyebabkan under-response, over-response, melewatkan bukti kritis, atau komunikasi yang salah ke manajemen.

**"What is the worst-case scenario?"** — Rencanakan untuk skenario terburuk. Jika worst-case bisa diterima, respon sudah cukup.

**"What does success look like?"** — Definisikan endpoint sebelum mulai. Apakah sukses berarti attacker terhenti? Data aman? Forensik lengkap? Recovery penuh?

---

## 2. ECIH Exam Overview & Strategy

### Tentang ECIH v3 (212-89)

| Item | Detail |
|------|--------|
| **Format** | 100 multiple-choice, 3 jam, passing 70% |
| **Cost** | $449, ANAB accredited, DoD 8140, CREST CCIM |
| **Validity** | 3 years (120 ECE credits) |
| **Prerequisites** | 1 year cybersecurity experience recommended |

### Exam Domains

| Domain | Weight |
|--------|--------|
| Incident Handling & Response Lifecycle | 35% |
| Preparation & Prevention | 15% |
| Detection & Triage | 15% |
| Containment & Eradication | 15% |
| Recovery & Post-Incident | 10% |
| Legal & Compliance | 10% |

### Strategi Ujian

ECIH menguji **kemampuan mengambil keputusan dalam incident response**, bukan pengetahuan teknis tools. Soal sering menyajikan skenario dan menanyakan "Apa yang harus dilakukan SELANJUTNYA?"

**Tips Kunci**:
1. **Urutan IH&R stages itu absolut** — Preparation selalu sebelum Detection, Containment sebelum Eradication, Eradication sebelum Recovery
2. **Evidence first** — Sebelum containment penuh, kumpulkan evidence. Sebelum eradication, dokumentasi evidence
3. **Chain of Custody** — Dokumentasi siapa, kapan, bagaimana menangani evidence
4. **BIA menentukan prioritas** — Business Impact Assessment adalah dasar semua keputusan
5. **Communication is key** — Insiden besar harus dikomunikasikan ke management, legal, PR, regulator
6. **Post-incident bukan hukuman** — Lessons learned bukan untuk mencari kambing hitam

**Common Trick Questions**:
- "What is the FIRST step?" → Preparation
- "What should the incident handler do NEXT?" → Perhatikan urutan IH&R stages
- "Which evidence should be collected FIRST?" → Volatile evidence (memory, network)
- "Should containment be done before evidence collection?" → DILEMA: idealnya evidence dulu, TAPI jika risiko penyebaran tinggi, contain dulu

---

## 3. Decision Framework & Trade-offs

### OODA Loop dalam IR

```
Observe ───→ Orient ───→ Decide ───→ Act
   ↑                                      │
   └──────────────────────────────────────┘
```

**Observe**: Kumpulkan data (alert, logs, report)
**Orient**: Analisis dalam konteks (BIA, threat intel, knowledge base)
**Decide**: Pilih tindakan berdasarkan analisis
**Act**: Eksekusi tindakan

### Decision Points Sepanjang IR Lifecycle

| Stage | Decision Point | Options |
|-------|---------------|---------|
| Detection | Is this an incident? | Yes / No / Need more data |
| Triage | What priority? | P0-P4 |
| Notification | Who needs to know? | IR team / Management / Legal / Regulator / Public |
| Containment | Contain first or evidence first? | Evidence → Contain / Contain → Evidence |
| Containment | Isolate or disconnect? | Network isolate / Power off / Do nothing |
| Evidence | What to collect? | Full disk / Memory only / Targeted |
| Eradication | Clean or rebuild? | Clean / Rebuild / Replace |
| Recovery | When to restore? | Now / Wait / Gradual |
| Post-Incident | What to improve? | People / Process / Technology |

### Trade-off Matrix

| Trade-off | When to Choose A | When to Choose B |
|-----------|-----------------|------------------|
| **Speed vs Accuracy** | Fast: Active spread, data exfiltration | Accurate: Isolated malware, forensics needed |
| **Containment vs Evidence** | Contain: High spread risk | Evidence: Legal case, root cause analysis |
| **Isolate vs Monitor** | Isolate: Active threat | Monitor: APT, intel gathering |
| **Clean vs Rebuild** | Clean: Low compromise, quick fix | Rebuild: Heavy compromise, unknown scope |
| **Disclose vs Stay Silent** | Disclose: Legal obligation, customer trust | Stay silent: Under investigation, no legal obligation |

### Risk-Based Decision Making

```
Risk = Likelihood × Impact
```

**Pertanyaan untuk setiap opsi**:
1. Apa risiko TIDAK melakukan tindakan ini?
2. Apa risiko MELAKUKAN tindakan ini?
3. Apa risiko MENUNDA keputusan?
4. Opsi mana yang punya risk/reward terbaik?

### Mental Shortcuts (Heuristics)

1. **"When in doubt, isolate"** — Lebih baik over-contain daripada under-contain
2. **"Evidence first, ask later"** — Ambil evidence tanpa risiko besar, ambil dulu
3. **"Assume worst case, plan for best case"** — Rencanakan terburuk, harap terbaik
4. **"Nobody ever got fired for documenting too much"** — Dokumentasi berlebihan > kurang
5. **"The attacker is probably still there"** — Asumsikan residual sampai terbukti bersih
6. **"Time is the enemy"** — Prioritaskan kecepatan untuk containment
7. **"You can't un-notify"** — Lebih baik telat dan akurat daripada cepat dan salah

---

## 4. Gotchas — Common IR Mistakes

- **Shutdown = evidence loss**: Powering off destroys memory evidence (processes, connections, encryption keys). Perform memory capture first unless lateral movement risk is critical.
- **Chain of custody retroactive**: Courts reject evidence where chain of custody was filled after the fact. Document BEFORE transferring evidence.
- **GDPR clock**: The 72-hour notification clock starts at DETECTION of the breach, not confirmation of scope. File initial notification even if investigation is ongoing.
- **Backup re-infection**: Restoring from backup without verifying the backup predates the compromise = guaranteed re-infection. Always validate backup integrity.
- **Contain before evidence**: If you power off before capturing memory, you lose all volatile evidence. Make the containment-vs-evidence decision consciously, not by reflex.
- **Attacker in the IR channel**: If the attacker has access to email/chat, they'll see your containment plans. Use out-of-band communication.
- **Scope creep**: Containment often reveals new affected systems. Don't assume initial scope is complete — keep hunting.
- **Missing persistence**: Attackers often have multiple backdoors. Removing only one is not eradication — do full persistence audit.
- **Legal hold failure**: Failing to issue a legal hold before remediation can result in spoliation sanctions. Involve legal early.

---

## 5. Incident Report Template

```
1. Executive Summary
   - Apa yang terjadi, dampak, tindakan kunci (1-2 paragraph)

2. Incident Timeline
   - Chronological: Detection → Response → Recovery → Closure

3. Scope & Impact
   - Systems affected, Data affected, Business impact

4. Root Cause Analysis
   - Why did this happen? Contributing factors?

5. Response Evaluation
   - What went well? What went wrong? What was unexpected?

6. Evidence Summary
   - Evidence collected, Chain of custody

7. Lessons Learned
   - Technical, Process, Team, Communication

8. Recommendations
   - Immediate, Short-term (1-3 months), Long-term (3-12 months)

9. Action Items
   - Owner, deadline, priority
```

---

## 6. IR Quick Reference Checklists

### Phase Checklist

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

### Communication Template

```
Subject: [SEVERITY] Security Incident — [Incident ID]

Summary: [1-2 sentences]
Affected Systems: [List]
Current Status: [Detection / Investigation / Containment / Recovery]
Action Required: [Who needs to do what]
Next Update: [Time]
Point of Contact: [Name, Phone, Email]
```

### Evidence Documentation Template

| Field | Value |
|-------|-------|
| Evidence ID | |
| Description | |
| Source | |
| Acquisition method | |
| Acquisition tool | |
| Hash (SHA256) | |
| Timestamp (UTC) | |
| Collector | |
| Location | |

---

## 7. Key Terms

| Term | Definition (ECIH Context) |
|------|---------------------------|
| **Incident** | Event that violates security policy, threatens CIA of information assets |
| **IR Plan** | Documented procedures for detecting, responding to, recovering from incidents |
| **Playbook** | Step-by-step guide for handling a specific incident type |
| **BIA** | Business Impact Assessment — identifies critical systems, quantifies impact |
| **MTTD/MTTR** | Mean Time to Detect / Mean Time to Respond |
| **RTO/RPO** | Recovery Time Objective / Recovery Point Objective |
| **Chain of Custody** | Documentation trail tracking evidence from collection to court |
| **Order of Volatility** | Sequence for collecting evidence from most to least volatile |
| **Containment** | Actions to stop an incident from spreading |
| **Eradication** | Actions to remove the threat from the environment |
| **Recovery** | Actions to restore normal operations |

---

## 8. Framework Relationships

```
ECIH IH&R (9 stages)
   ├── NIST SP 800-61 (4 phases) — Basis untuk IR plan organisasi
   ├── SANS PICERL (6 phases) — Populer di kalangan praktisi
   ├── ISO 27035 (5 phases) — Standar internasional
   └── FIRST CSIRT Framework — Untuk CSIRT maturity assessment
```

Semua framework memiliki kesamaan esensi: **Prepare → Detect → Respond → Recover → Improve**.

---

## Referensi Lengkap

### Standar & Framework

| Referensi | Link |
|-----------|------|
| ECIH v3 (212-89) Official Curriculum | https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/ |
| NIST SP 800-61 Rev 2 | https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final |
| NIST SP 800-86 — Forensic Techniques | https://csrc.nist.gov/publications/detail/sp/800-86/final |
| SANS PICERL | https://www.sans.org/white-papers/incident-response-process/ |
| ISO/IEC 27035 | https://www.iso.org/standard/78973.html |
| ISO/IEC 27037 | https://www.iso.org/standard/44381.html |
| FIRST CSIRT Framework | https://www.first.org/resources/guides/csirt-framework |
| ENISA Incident Handling Guide | https://www.enisa.europa.eu/publications/incident-handling-guide |

### Regulasi

| Referensi | Link |
|-----------|------|
| GDPR Art. 33 — Data Breach Notification | https://gdpr-info.eu/art-33-gdpr/ |
| HIPAA Breach Notification Rule | https://www.hhs.gov/hipaa/for-professionals/breach-notification/index.html |
| PCI DSS v4.0 IR Requirements | https://listings.pcisecuritystandards.org/documents/PCI-DSS-v4-0-Requirements-and-Testing-Procedures.pdf |
| CCPA Breach Notification | https://oag.ca.gov/privacy/ccpa |

### Threat Intelligence & Sharing

| Referensi | Link |
|-----------|------|
| MITRE ATT&CK | https://attack.mitre.org/ |
| FIRST TLP | https://www.first.org/tlp/ |
| CISA Cyber Incident Reporting | https://www.cisa.gov/report |
| CISA KEV Catalog | https://www.cisa.gov/known-exploited-vulnerabilities-catalog |

### Organisasi

| Organisasi | Link |
|-----------|------|
| FIRST | https://www.first.org/ |
| CISA | https://www.cisa.gov/ |
| ENISA | https://www.enisa.europa.eu/ |
| APACERT | https://www.apcert.org/ |

### EC-Council

| Resource | Link |
|----------|------|
| ECIH Official Page | https://www.eccouncil.org/train-certify/certified-incident-handler-ecih/ |
| EC-Council Exam Portal | https://www.eccouncil.org/programs/ |
| ECE Credit System | https://www.eccouncil.org/continuing-education/ |
| EC-Council Code of Ethics | https://www.eccouncil.org/code-of-ethics/ |

---

*ECIH — Certified Incident Handler Mindset*
*Based on EC-Council ECIH v3 (212-89) curriculum*
*License: MIT*
