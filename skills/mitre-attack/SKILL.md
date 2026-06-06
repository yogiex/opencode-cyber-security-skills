---
name: mitre-attack
description: Panduan MITRE ATT&CK framework untuk memahami adversary tactics, techniques, dan prosedur dalam threat intelligence, detection engineering, dan defensive gap analysis.
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, threat hunter, soc analyst, detection engineer, cti analyst, red teamer
  source: MITRE ATT&CK
---

# MITRE ATT&CK Framework

## Apa itu MITRE ATT&CK

MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) adalah **knowledge base** yang mendokumentasikan TTP (Tactics, Techniques, and Procedures) adversary berdasarkan observasi dunia nyata.

### Tiga Matrices

| Matrix | Fokus | Jumlah Tactics |
|---|---|---|
| **Enterprise** | Cloud, container, network, OS, SaaS | 15 tactics |
| **Mobile** | Android, iOS | 14 tactics |
| **ICS** | Industrial Control Systems | 12 tactics |

Skill ini berfokus pada **Enterprise matrix** yang paling banyak digunakan.

### Perbedaan dengan Framework Lain

| Framework | Fokus | Berbasis |
|---|---|---|
| **ATT&CK** | TTP adversary | Observasi nyata |
| **Cyber Kill Chain** | Fase serangan | Linear (7 fase) |
| **Diamond Model** | Relasi antar entitas | 4 dimensi (adversary, capability, infrastructure, victim) |
| **NIST CSF** | Capability organisasi | 5 functions |

ATT&CK paling cocok untuk: **detection mapping**, **gap analysis**, **threat intelligence**, dan **adversary emulation**.

## Komponen Framework

```
                    Tactics (Why)
                        │
                Techniques (How)
                        │
              Sub-techniques (Specific)
                        │
                 Procedures (Instance)
```

### Tactics (Why)

Tactics adalah **tujuan** adversary pada fase tertentu. 15 tactics Enterprise:

| # | Tactic | Tujuan Adversary |
|---|---|---|
| 1 | **Reconnaissance** | Mengumpulkan informasi target sebelum serangan |
| 2 | **Resource Development** | Membangun infrastruktur dan capability |
| 3 | **Initial Access** | Mendapatkan akses awal ke sistem |
| 4 | **Execution** | Menjalankan kode di sistem target |
| 5 | **Persistence** | Mempertahankan akses setelah restart/kredensial berubah |
| 6 | **Privilege Escalation** | Mendapatkan hak akses lebih tinggi |
| 7 | **Stealth** | Menghindari deteksi |
| 8 | **Defense Impairment** | Mematikan atau menghindari mekanisme keamanan |
| 9 | **Credential Access** | Mencuri kredensial |
| 10 | **Discovery** | Mengeksplorasi lingkungan |
| 11 | **Lateral Movement** | Berpindah antar sistem |
| 12 | **Collection** | Mengumpulkan data target |
| 13 | **Command and Control** | Berkomunikasi dengan sistem yang dikompromikan |
| 14 | **Exfiltration** | Mencuri data keluar |
| 15 | **Impact** | Merusak, menghancurkan, atau mengganggu |

### Techniques (How)

Techniques adalah **cara** adversary mencapai tactic. Contoh:

| Tactic | Technique | ID |
|---|---|---|
| Initial Access | Phishing | T1566 |
| Execution | Command and Scripting Interpreter | T1059 |
| Persistence | Create Account | T1136 |
| Credential Access | OS Credential Dumping | T1003 |
| Lateral Movement | Remote Services | T1021 |

Setiap technique memiliki ID unik (contoh: T1059) yang stabil antar versi.

### Sub-Techniques

Teknik spesifik di dalam technique. Format: `T1059.001`:

- **T1059** — Command and Scripting Interpreter
  - **T1059.001** — PowerShell
  - **T1059.002** — AppleScript
  - **T1059.003** — Windows Command Shell
  - **T1059.004** — Unix Shell
  - **T1059.005** — Visual Basic
  - **T1059.006** — Python
  - **T1059.007** — JavaScript
  - **T1059.008** — Network Device CLI

### Procedures (Instance)

Prosedur adalah **implementasi spesifik** dari teknik oleh threat group tertentu:

- *APT29 menggunakan PowerShell untuk credential dumping* → Technique T1059.001 + T1003
- *Lazarus menggunakan Living Off the Land Binaries* → Technique T1218

### Groups, Software, Campaigns

| Entity | Deskripsi | Contoh |
|---|---|---|
| **Group** | Threat actor yang teridentifikasi | APT29, Lazarus, FIN7 |
| **Software** | Tools dan malware yang digunakan | Mimikatz, Cobalt Strike, PlugX |
| **Campaign** | Serangan dengan tujuan spesifik dalam periode tertentu | Operation Sharpshooter |

Setiap group dan software memiliki teknik yang dipetakan — ini memungkinkan profiling TTP.

### Mitigations

Kontrol pencegahan yang mengurangi efektivitas teknik:

- **M1040** — Behavior Prevention on Endpoint → mitigasi untuk berbagai teknik execution
- **M1028** — Operating System Configuration → mitigasi untuk teknik privilege escalation
- **M1018** — User Account Management → mitigasi untuk teknik persistence

### Data Sources

Data yang perlu dikumpulkan untuk mendeteksi teknik tertentu:

| Data Source | Mendeteksi |
|---|---|
| Process | Execution, Persistence, Privilege Escalation |
| Command | Execution via CLI |
| Network Traffic | C2, Exfiltration, Lateral Movement |
| File | Persistence, Defense Impairment |
| Registry | Persistence, Defense Impairment |
| Logon Session | Credential Access, Lateral Movement |
| Cloud API | Discovery, Collection, Impact |

## Menggunakan ATT&CK untuk CTI

### Threat Actor Profiling

1. Identifikasi group dari incident atau intelligence report
2. Lihat teknik yang digunakan group tersebut di ATT&CK
3. Analisis: apa yang mereka incar? Bagaimana mereka masuk? Apa tool favorit mereka?
4. Buat profile: teknik yang digunakan, software terkait, target sektor/geografi

**Contoh Profiling:**

```
Group: APT29 (Cozy Bear)
Tactic favorit: Initial Access (Phishing), Persistence, C2
Teknik khas: T1566.001 (Spearphishing), T1059.001 (PowerShell), T1574 (Hijack Execution Flow)
Software: PowerShell, GoldFinder, GoldMax
Target: Government, think tanks, IT
```

### Tracking Perubahan

ATT&CK di-update beberapa kali setahun. Perhatikan:
- **New techniques** — apakah ada teknik baru yang relevan dengan lingkungan?
- **Technique updates** — apakah group yang dipantau mengubah teknik?
- **Deprecated techniques** — apakah ada teknik yang tidak lagi digunakan?

## Menggunakan ATT&CK untuk Deteksi

### Detection Strategy per Technique

Untuk setiap teknik, tentukan:

1. **Apa yang perlu dideteksi?** — event spesifik apa yang muncul saat teknik digunakan
2. **Data source apa yang dibutuhkan?** — process logs, network logs, file monitoring, registry
3. **Rule atau analytic** — bagaimana mendeteksinya (sigma rule, query, alert)
4. **Expected coverage** — apakah deteksi mencakup semua sub-techniques

### Mapping Detections ke MITRE

Source: Telemetry & Rules → Technique ID → Detection Coverage

```
Sigma Rule: powershell_remote_pwn
    ↓ Maps to
T1059.001 (Command and Scripting Interpreter: PowerShell)
    ↓ Sebagai
Detection for Execution Tactic
```

### Coverage Matrix

Buat matriks coverage untuk setiap teknik:

| Technique ID | Nama | Data Source | Detection Rule | Coverage |
|---|---|---|---|---|
| T1059.001 | PowerShell | Process, Command | sigma: powershell_* | ✅ |
| T1003.001 | LSASS Memory | Process | sysmon: lsass access | ✅ |
| T1566.001 | Spearphish Attachment | Mail, File | email: malicious_* | ✅ |
| T1021.001 | Remote Desktop | Network, Logon | windows: rdp_* | ⚠️ Partial |

## Menggunakan ATT&CK untuk Defensive Gap Analysis

### Langkah Gap Analysis

1. **Prioritize techniques** — teknik mana yang paling berbahaya untuk organisasi? (Berdasarkan threat model, teknologi yang digunakan, data sensitif)
2. **Assess coverage** — apakah teknik tersebut terdeteksi? Apakah ada mitigasi?
3. **Identify gaps** — teknik dengan risk tinggi tapi coverage rendah
4. **Recommend actions** — tambah data source, buat rule baru, implement mitigation

### Contoh Gap Analysis

| Technique | Risk | Detection | Mitigation | Gap |
|---|---|---|---|---|
| T1059.001 (PowerShell) | HIGH | ✅ Yes | ✅ Yes | None |
| T1218.011 (Rundll32) | HIGH | ❌ No | ⚠️ Partial | **GAP** — perlu deteksi |
| T1003.001 (LSASS) | HIGH | ✅ Yes | ⚠️ Partial | Partial — perlu hardened |
| T1567 (Exfiltration Over Web) | MEDIUM | ❌ No | ❌ No | **GAP** — perlu keduanya |

### ATT&CK Navigator

Gunakan ATT&CK Navigator (https://mitre-attack.github.io/attack-navigator/) untuk:
- Visualisasi coverage matrix dalam bentuk heatmap
- Membandingkan coverage antara layers berbeda
- Export/import layer dalam format JSON
- Layer untuk: deteksi, mitigasi, emulasi adversary

## Navigasi Matrix

### Teknik Tree (Parent-Child)

```
T1059 Command and Scripting Interpreter (Parent)
├── T1059.001 PowerShell
├── T1059.003 Windows Command Shell
├── T1059.004 Unix Shell
├── T1059.005 Visual Basic
├── T1059.006 Python
├── T1059.007 JavaScript
└── T1059.008 Network Device CLI
```

Parent technique mencakup **semua** sub-techniques di bawahnya. Saat mapping deteksi, tentukan apakah aturan mendeteksi parent (generic) atau sub-technique spesifik.

### Teknik di Multiple Tactics

Satu teknik bisa muncul di beberapa tactics:

**T1136 — Create Account**
- Persistence (menciptakan akun untuk akses jangka panjang)
- Defense Impairment (menciptakan akun untuk menghindari audit)

Ini berarti deteksi untuk T1136 harus mempertimbangkan **konteks** — kapan dan untuk tujuan apa akun dibuat.

### Platform Coverage

Setiap teknik mencantumkan platform yang terpengaruh:

| Platform | Contoh Teknik |
|---|---|
| Windows | T1059.001 (PowerShell), T1003 (Credential Dumping) |
| Linux | T1059.004 (Unix Shell), T1552.001 (Credentials in Files) |
| macOS | T1059.002 (AppleScript), T1561 (Disk Wipe) |
| Cloud | T1525 (Cloud Infrastructure Discovery), T1613 (Container Discovery) |
| Network | T1059.008 (Network Device CLI), T1557 (Adversary-in-the-Middle) |

## Data Sources & Components

### Data Components (ATT&CK v14+)

ATT&CK kini menggunakan **Data Components** untuk mendefinisikan telemetry yang dibutuhkan:

| Domain | Data Component | Contoh Sumber |
|---|---|---|
| Process | Process Creation, Process Access | EDR, Sysmon, auditd |
| Network | Network Connection, DNS Query | Zeek, firewall, proxy |
| File | File Creation, File Modification, File Deletion | EDR, FIM |
| Registry | Registry Key Creation, Registry Key Modification | Sysmon, EDR |
| Logon | Logon Session, Logoff Session | Windows Event Log, auth.log |
| Cloud | Cloud API Call, Cloud Storage Access | CloudTrail, Audit Log |
| Command | Command Execution | Shell history, auditd |

Mapping **Data Component → Technique** membantu menentukan apakah telemetry yang ada cukup untuk mendeteksi teknik tertentu.

## Groups & Software

### Threat Groups

ATT&CK mendokumentasikan 140+ threat groups. Informasi per group:

- **Name** — APT29, Lazarus, Wizard Spider
- **Associated Groups** — alias (APT29 = Cozy Bear = The Dukes)
- **Description** — origin, target, operasi
- **Techniques Used** — semua teknik yang pernah diamati
- **Software Used** — malware dan tools yang digunakan
- **Targeted Sectors** — government, finance, energy, dll.

### Software (Tools & Malware)

ATT&CK mengklasifikasikan software menjadi:
- **Malware** — dirancang untuk aktivitas jahat (Cobalt Strike, PlugX)
- **Tool** — bisa digunakan legitimate tapi juga oleh adversary (PsExec, BloodHound)

Mapping software ke teknik memungkinkan: "Jika software X terdeteksi, teknik apa yang mungkin menyusul?"

## Key Questions

1. **"What techniques is this group using?"** — Profiling threat actor untuk intelligence dan persiapan deteksi
2. **"Are we detecting this technique?"** — Apakah ada rule/monitoring untuk teknik ini?
3. **"What data sources do we need to detect this technique?"** — Telemetry apa yang harus dikumpulkan?
4. **"What's our detection coverage gap?"** — Teknik prioritas tinggi mana yang belum terdeteksi?
5. **"How would this attack look in our environment?"** — Terjemahkan teknik ke konteks organisasi
6. **"What mitigations can prevent this technique?"** — Kontrol apa yang bisa mencegah teknik ini berhasil?
7. **"What other techniques does this group use alongside this one?"** — Teknik pendamping yang sering digunakan bersamaan
8. **"Is this technique still relevant?"** — Periksa status teknik (deprecated atau masih aktif)

## Kapan Menggunakan Skill Ini

**Gunakan ketika:**
- Menganalisis threat actor dan TTP mereka
- Mendesain atau mengevaluasi deteksi keamanan (detection engineering)
- Melakukan gap analysis defensive coverage
- Menulis threat intelligence report
- Merencanakan purple team exercise atau adversary emulation
- Memetakan telemetry yang ada ke teknik yang perlu dideteksi
- Mengikuti update ATT&CK untuk teknik baru yang relevan

**Jangan gunakan ketika:**
- Membutuhkan panduan incident response langkah-demi-langkah — gunakan skill incident-response-plan atau soc-analyst
- Membutuhkan risk management framework — gunakan skill risk-management-framework
- Membutuhkan kontrol keamanan spesifik — gunakan skill nist-800-53
- Membutuhkan threat modeling arsitektur (STRIDE/DFD) — gunakan skill threat-modeling
- Butuh daftar lengkap semua techniques — lihat langsung di https://attack.mitre.org

## Resources

- ATT&CK Website: https://attack.mitre.org
- ATT&CK Navigator: https://mitre-attack.github.io/attack-navigator/
- ATT&CK STIX Data: https://github.com/mitre/cti
- ATT&CK API: https://attack.mitre.org/resources/working-with-attack/
- ATT&CKcon: https://attack.mitre.org/resources/attackcon/
- Sigma Rules (ATT&CK mapping): https://github.com/SigmaHQ/sigma
- Atomic Red Team (adversary emulation): https://github.com/redcanaryco/atomic-red-team
