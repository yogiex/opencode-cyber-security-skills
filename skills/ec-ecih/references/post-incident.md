---
name: "Post-Incident Activity & Lessons Learned"
description: "Incident report structure, lessons learned meeting format, blameless post-mortem, root cause analysis (5 Whys, Fishbone), improvement plan framework, IR metrics & KPIs, and evidence retention & destruction policies."
tags: [ecih, post-incident, lessons-learned, root-cause-analysis, incident-report, metrics, kpis, blameless-postmortem]
---

## Post-Incident Activity — Lessons Learned

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
