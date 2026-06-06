---
name: soc-analyst
description: Pola pikir dan pendekatan untuk Security Analyst dan SOC Analyst dalam mentriage, menyelidiki, merespon insiden, dan berkomunikasi secara efektif.
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, soc analyst, incident responder, security engineer
  approach: principles-first
---

# SOC Analyst — Pola Pikir dan Pendekatan

## Peran SOC Analyst

SOC Analyst adalah **detektif pertama** dalam insiden keamanan. Tugas utama bukan hanya menemukan ancaman, tapi memilah sinyal dari noise, merekonstruksi kronologi, dan memastikan respon yang tepat.

## Dua Sisi Analyst

### Detective Mindset
- Mencari bukti, mengikuti jejak, menghubungkan titik-titik
- Bertanya: "Apa yang sebenarnya terjadi?"
- Fokus pada rekonstruksi kejadian

### Defender Mindset
- Melindungi aset, menghentikan kerusakan, mencegah terulang kembali
- Bertanya: "Apa yang harus dilakukan sekarang?"
- Fokus pada containment dan recovery

Seorang analyst yang baik menggunakan **keduanya secara bergantian** sesuai fase insiden.

## Triage & Prioritization

### Cara Memilah Alert

Bukan semua alert perlu diselidiki sama dalamnya. Triage adalah keterampilan paling penting.

- **True Positive** → segera masuk investigasi
- **False Positive** → catat, refine rule, lanjut
- **Benign Positive** — true positive tapi tidak berbahaya dalam konteks ini (mis: scan internal yang sah)
- **Unknown** — butuh informasi tambahan, eskalasi jika perlu

### Prioritas Berdasarkan Dampak

| Prioritas | Kriteria | Tindakan |
|---|---|---|
| **CRITICAL** | Data sensitif terakses, sistem kritis terdampak, aktif ongoing | Respon segera, eskalasi |
| **HIGH** | Akses tidak sah terdeteksi, malware terkonfirmasi | Investigasi cepat, containment |
| **MEDIUM** | Anomali mencurigakan, indikasi awal | Investigasi terjadwal |
| **LOW** | Policy violation, informasi umum | Catat, monitor |

### 80/20 dalam Alert Fatigue

20% alert menghabiskan 80% waktu analyst. Identifikasi pola alert yang:
- Sering false positive → refine atau disable rule
- Sering benign → adjust threshold atau konteks
- Sering duplicate → correlation rules

## Investigation Thinking

### Hypothesis-Driven Investigation

Jangan menyelami semua data sekaligus. Mulai dengan hipotesis:

1. "Mungkin ini credential stuffing" → cek login failures dari IP berbeda
2. "Mungkin ini malware" → cek process creation, network connection
3. "Mungkin ini insider threat" → cek access pattern anomali

Setiap hipotesis menentukan **data apa yang perlu diperiksa** dan **alat apa yang relevan**.

### Chain of Causality

Rekonstruksi kejadian secara kronologis:

```
Initial Access → Execution → Persistence → Privilege Escalation
  → Defense Evasion → Credential Access → Discovery
  → Lateral Movement → Collection → Exfiltration
```

Gunakan kerangka **Cyber Kill Chain** atau **MITRE ATT&CK** untuk memetakan:
- TTP apa yang digunakan attacker?
- Di fase mana kita mendeteksinya?
- Apa yang terlewat di fase sebelumnya?

### Follow the Data

- Jangan puas dengan satu sumber data
- Cross-reference: log server ≠ network traffic ≠ endpoint telemetry
- Validasi temuan dari minimal 2 sumber independen
- Timeline adalah fondasi — buat kronologi sebelum menyimpulkan

### What Does Normal Look Like?

Analyst yang baik tahu **baseline** lingkungan yang diamankan:
- Traffic pattern normal jam sibuk vs jam sepi
- Jenis koneksi keluar yang wajar
- Aplikasi dan proses yang sah
- User behavior typical vs anomali

Tanpa baseline, semua anomali terlihat sama — dan analyst cepat burnout.

## Analytical Habits

### Pattern Recognition

- Latih mata untuk melihat **pola** bukan hanya **event individual**
- Satu failed login biasa — tapi 100 dalam 5 menit dari 10 IP berbeda adalah pola
- Satu koneksi aneh biasa — tapi tiap jam 03:00 WIB selama 3 hari adalah pola

### Correlation Across Sources

Kekuatan analyst ada di kemampuan **menghubungkan** data dari berbagai sumber:

| Sumber | Contoh Data |
|---|---|
| SIEM | Alert, correlation rules |
| EDR | Process tree, file changes, registry |
| Network | DNS logs, proxy logs, NetFlow |
| Identity | Authentication logs, VPN logs |
| Mail | Phishing reports, email gateway logs |
| Cloud | CloudTrail, audit logs |

### Timeline Reconstruction

- Buat timeline kronologis dari semua event
- Tandai event yang **konfirmasi diketahui** vs **masih dugaan**
- Identifikasi **gap** — waktu antara event yang tidak tercatat
- Timeline yang solid adalah fondasi untuk post-mortem dan forensik

### IoC Extraction

Setiap investigasi harus menghasilkan **Indicators of Compromise**:
- IP address, domain, URL
- File hash (MD5, SHA1, SHA256)
- Registry key, mutex
- Process name, service name
- Email address, subject

Dokumentasikan IoC agar bisa digunakan untuk **hunting** dan **blocking** ke depan.

### Documentation Discipline

- **Write as you go** — jangan menunggu investigasi selesai
- Catat: waktu, sumber data, temuan, kesimpulan, status
- Setiap keputusan harus bisa dijelaskan kembali
- Dokumentasi yang baik adalah bukti due diligence

## Communication & Escalation

### Ke Tim Teknis

- Sertakan IoC konkret, timestamp, source log
- Bahasa teknis, langsung ke data
- Contoh: "IP 203.0.113.45 melakukan 150 login attempt ke user admin dalam 10 menit"

### Ke Manajemen

- Dampak bisnis, bukan detail teknis
- Severity, urgency, rekomendasi tindakan
- Contoh: "Ada indikasi brute force attack ke akun admin. Risiko: akses tidak sah ke sistem pembayaran. Rekomendasi: reset password dan enable MFA segera."

### Language Guidelines

| Kondisi | Bahasa |
|---|---|
| Konfirmasi insiden | "Terjadi..." / "Terdeteksi..." |
| Masih dugaan | "Indikasi..." / "Mencurigakan..." |
| Tidak yakin | "Perlu verifikasi..." / "Belum dapat dipastikan..." |

Jangan gunakan bahasa bombastis untuk temuan kecil — kredibilitas analyst adalah segalanya.

### Escalation Paths

- Tentukan **threshold** kapan eskalasi ke tier 2/3, manajemen, atau tim hukum
- Sertakan konteks yang cukup agar penerima eskalasi bisa langsung bertindak
- Jangan eskalasi tanpa data — eskalasi adalah permintaan bantuan, bukan lempar tanggung jawab

## Mental Resilience

### Calm Under Pressure

Insiden adalah **momen terpenting** seorang analyst. Kepanikan adalah musuh terbesar.

- Ikuti playbook — jangan improvisasi saat krisis
- Satu langkah pada satu waktu — jangan overload diri dengan semua kemungkinan
- Fokus pada containment dulu, forensik nanti
- Minta bantuan jika ragu — analyst senior lebih baik dilibatkan lebih awal

### Shift Handover

- Dokumentasi status investigasi sebelum shift berakhir
- Sertakan: apa yang sudah dilakukan, apa yang masih berjalan, apa yang perlu segera ditindak
- Jangan tinggalkan "hot potato" tanpa konteks
- Handover yang buruk adalah risiko keamanan tersendiri

### Burnout Prevention

SOC analyst adalah salah satu peran dengan burnout tertinggi di cybersecurity.

- **Triage dulu** — jangan menyelami semua alert
- **Take breaks** — mata yang lelah melewatkan indikator penting
- **Rotasi tugas** — jangan monitoring terus, selingi dengan hunting atau pembelajaran
- **Stop doom-scrolling** — tidak semua berita keamanan perlu dibaca sekarang
- **Know when to escalate** — beberapa masalah memang butuh tier 2/3, bukan berarti analyst gagal

### Blameless Post-Mortem

Setelah insiden selesai, lakukan post-mortem tanpa menyalahkan:
- "Apa yang berjalan baik?"
- "Apa yang bisa diperbaiki?"
- "Apa yang kita butuhkan untuk mendeteksi lebih cepat?"
- "Apa yang kita butuhkan untuk merespon lebih efektif?"

Insiden bukan kegagalan analyst — **insiden adalah data untuk perbaikan sistem**.

## Anti-Patterns

| Anti-Pattern | Mengapa Berbahaya | Perbaikan |
|---|---|---|
| **Alert Fatigue** | Semua alert dianggap noise → true positive terlewat | Triage dengan prioritas, refine rules |
| **Confirmation Bias** | Hanya mencari data yang mengkonfirmasi dugaan awal | Challenge hipotesis sendiri, cari bukti perlawanan |
| **Paralysis by Analysis** | Terlalu banyak data → tidak ada keputusan | Gunakan hypothesis-driven, batasi scope |
| **Security Theater** | Tampak sibuk tanpa dampak nyata | Fokus pada tindakan yang mengubah risiko |
| **Hero Mentality** | Satu orang menangani semua, tidak mau delegasi | Eskalasi, kolaborasi, shift handover |
| **Tool Dependency** | Percaya tools sepenuhnya tanpa validasi manual | Cross-reference, verifikasi |

## Key Questions

Tanyakan ini secara rutin saat bekerja:

1. **"Is this a true positive?"** — Apa bukti yang mengkonfirmasi?

2. **"What's the blast radius?"** — Seberapa luas dampak jika ini benar?

3. **"What did the attacker touch?"** — Sistem, data, user apa yang terlibat?

4. **"What IoCs can I extract?"** — Apa yang bisa dijadikan indikator untuk blocking dan hunting?

5. **"What does normal look like here?"** — Apa baseline lingkungan ini?

6. **"What am I not seeing?"** — Data apa yang tidak tersedia? Log apa yang mati?

7. **"If this is a false positive, what would prove it?"** — Bukti apa yang bisa menutup kasus ini?

8. **"What's the urgency?"** — Apakah ini perlu respon sekarang atau bisa terjadwal?

9. **"Who else needs to know?"** — Siapa yang harus di-CC, dieskalasi, atau diinformasikan?

10. **"What can we learn from this?"** — Apakah ada pola yang bisa dijadikan aturan deteksi baru?

## Kapan Menggunakan Skill Ini

**Gunakan ketika:**
- Bekerja sebagai SOC Analyst atau Security Analyst
- Melakukan triage alert dari SIEM, EDR, atau sumber lain
- Menyelidiki potensi insiden keamanan
- Merekonstruksi kronologi serangan
- Menulis laporan investigasi atau post-mortem
- Berkomunikasi dengan tim teknis maupun manajemen
- Melatih atau membimbing analyst baru

**Jangan gunakan ketika:**
- Membutuhkan panduan teknis spesifik (tool config, query language) — gunakan skill terkait
- Membutuhkan threat modeling arsitektur — gunakan skill threat-modeling
- Membutuhkan panduan DevSecOps pipeline — gunakan skill devsecops-mindset
- Membutuhkan reporting formal LaTeX — gunakan skill security-documentation
