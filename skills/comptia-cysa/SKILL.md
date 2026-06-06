---
name: comptia-cysa
description: Panduan lengkap CompTIA CySA+ (CS0-004 V4) mencakup Security Operations, Vulnerability Management, Incident Response, dan Reporting & Communication untuk mempersiapkan sertifikasi Cybersecurity Analyst.
license: MIT
compatibility: opencode
metadata:
  audience: security analyst, soc analyst, vulnerability analyst, cysa+ candidate
  standard: CompTIA CySA+ CS0-004
---

# CompTIA CySA+ (CS0-004 V4) — Panduan Lengkap

## Exam Overview

| Item | Detail |
|---|---|
| **Exam Code** | CS0-004 V4 |
| **Launch** | 2026 |
| **Duration** | 165 menit |
| **Questions** | Maksimum 85 (multiple-choice + performance-based) |
| **Passing Score** | 750 / 900 |
| **Recommended Experience** | 4 tahun sebagai SOC analyst (Level 2) atau vulnerability analyst |

### Domain Weight

| Domain | Weight |
|---|---|
| 1.0 Security Operations | 34% |
| 2.0 Vulnerability Management | 26% |
| 3.0 Incident Response and Management | 24% |
| 4.0 Reporting and Communication | 16% |

---

## Domain 1: Security Operations (34%)

### 1.1 Logging Concepts

**Log Ingestion:**
- Centralized logging — semua log dikumpulkan ke satu platform (SIEM)
- Syslog (RFC 5424) — standar untuk network devices, Linux
- Windows Event Log — Event ID: 4624 (login success), 4625 (failed), 4688 (process creation)
- JSON/CEF — format terstruktur untuk integrasi SIEM

**Time Synchronization:**
- Semua sumber log wajib menggunakan **NTP** yang sama
- Gunakan UTC untuk standarisasi
- Time drift > 1 detik harus diperbaiki

**Logging Levels:**
- ERROR, WARNING, INFO, DEBUG
- Semakin rendah level, semakin detail — berdampak pada volume storage

### 1.2 System and Network Architecture

**OS Concepts:**
- **Windows Registry** — lokasi persistence, konfigurasi, startup programs (`HKLM\Software\Microsoft\Windows\CurrentVersion\Run`)
- **System Hardening** — disable unnecessary services, patch management, least functionality
- **File Structure** — `/etc/passwd`, `/etc/shadow` (Linux), `C:\Windows\System32` (Windows)
- **System Processes** — normal vs suspicious (contoh: `svchost.exe` legitimate, `svchost.exe` dari temp folder suspicious)
- **Hardware Architecture** — TPM, secure boot, UEFI vs legacy BIOS

**Infrastructure Concepts:**
- **On-premises** — kontrol penuh, maintenance sendiri
- **Cloud** — IaaS, PaaS, SaaS — shared responsibility model
- **Hybrid** — kombinasi on-prem dan cloud
- **Serverless** — fungsi berjalan tanpa mengelola server (AWS Lambda)
- **Virtualization** — hypervisor (Type 1: bare-metal, Type 2: hosted), VM escape sebagai ancaman
- **Containerization** — Docker, Kubernetes — image security, registry trust, RBAC
- **SDN (Software-Defined Networking)** — kontrol terpusat, policy-based routing

**Network Architecture:**
- **Segmentation** — VLAN, subnet, firewall zones (DMZ, internal, management)
- **Zero Trust** — never trust, always verify — micro-segmentation, least privilege, continuous validation
- **ZTNA (Zero Trust Network Access)** — akses berdasarkan identitas bukan IP
- **SASE (Secure Access Service Edge)** — ZTNA + SWG + CASB + FWaaS
- **SD-WAN** — software-defined WAN untuk koneksi cabang

**Identity and Access Management:**
- **MFA** — something you know + have + are
- **SSO** — satu autentikasi untuk multiple aplikasi (SAML, OIDC)
- **Federation** — trust antar organisasi (ADFS, Shibboleth)
- **PAM (Privileged Access Management)** — akun admin dikelola, password dirotasi, session recorded
- **Passwordless** — FIDO2, Windows Hello, biometric
- **CASB (Cloud Access Security Broker)** — visibilitas dan kontrol akses ke cloud apps

**Encryption:**
- **PKI** — public/private key, certificate authority, certificate revocation
- **SSL/TLS Inspection** — decrypt traffic di perimeter untuk inspeksi (decryption policy, compliance)

**Sensitive Data Protection:**
- **DLP (Data Loss Prevention)** — endpoint, network, cloud — cegah data keluar tanpa izin
- **PII** — Personally Identifiable Information (nama, alamat, SSN, email)
- **CHD** — Cardholder Data (nomor kartu, CVV, PIN) — PCI DSS

### 1.3 Analyze Indicators of Malicious Activity

**Network-Related Indicators:**
- **Bandwidth consumption** — lonjakan traffic tidak wajar
- **Beaconing** — komunikasi periodik ke C2 (interval tetap)
- **Irregular peer-to-peer** — koneksi antar sistem yang biasanya tidak berkomunikasi
- **Rogue devices** — perangkat tidak dikenal di network
- **Scans/sweeps** — port scanning dari internal atau eksternal
- **Unusual traffic spikes** — lonjakan di jam tidak biasa
- **Activity on unexpected ports** — service berjalan di port non-standar

**Host-Related Indicators:**
- **Processor consumption** — CPU tinggi tanpa sebab jelas (mining, malware)
- **Memory consumption** — memory leak atau injection
- **Drive capacity consumption** — disk penuh karena log atau data exfil staging
- **Unauthorized software** — instalasi software tanpa approval
- **Malicious processes** — proses mencurigakan (nama mirip system process)
- **Unauthorized changes** — file, registry, konfigurasi berubah tanpa otorisasi
- **Unauthorized privileges** — privilege escalation
- **Data exfiltration** — file dipindah, di-zip, di-upload
- **Abnormal OS process behavior** — process spawning child process tidak wajar
- **File system changes/anomalies** — file baru di lokasi mencurigakan
- **Registry changes/anomalies** — run key berubah, service baru
- **Unauthorized scheduled tasks** — task scheduler mencurigakan

**Application-Related Indicators:**
- **Anomalous activity** — input tidak wajar, parameter tampering
- **Introduction of new accounts** — akun dibuat tanpa proses
- **Unexpected output** — error message mengandung informasi sensitif
- **Unexpected outbound communication** — aplikasi tiba-tiba connect ke IP asing
- **Service interruption** — service crash, restart tidak wajar
- **Application logs** — log menunjukkan pola serangan (SQLi, XSS, path traversal)

**Cloud-Related Indicators:**
- **Anomalous resource activity** — VM/container dibuat dalam jumlah besar
- **IAM account compromise** — aktivitas akun dari lokasi asing, API calls mencurigakan
- **Cloud storage exfiltration** — bucket tiba-tiba public, download massal

**Identity-Related Indicators:**
- **Impossible travel** — login dari dua lokasi berbeda dalam waktu singkat
- **Account compromise** — perubahan password, MFA reset, akun tidak aktif tiba-tiba aktif
- **Unusual login patterns** — login di jam tidak biasa, device tidak dikenal

**Email-Related Indicators:**
- **BEC (Business Email Compromise)** — impersonasi eksekutif, wire transfer fraud
- **DMARC/DKIM/SPF** — email spoofing detection
- **Obfuscated links** — URL shortening, homograph attack
- **Attachment analysis** — macro, embedded script, encrypted zip

**LOLBins (Living Off the Land Binaries):**
- `powershell.exe`, `cmd.exe`, `wscript.exe`, `mshta.exe`, `rundll32.exe`, `regsvr32.exe`, `certutil.exe`, `bitsadmin.exe`, `wmic.exe`
- Tools legitimate yang disalahgunakan attacker — deteksi melalui parent-child relationship dan parameter tidak wajar

### 1.4 Tools to Determine Malicious Activity

| Kategori | Tools |
|---|---|
| **Packet Capture** | Wireshark, tcpdump, Snort, Suricata, Zeek |
| **Log Analysis** | SIEM (Splunk, ELK, ArcSight, QRadar), SOAR |
| **Endpoint Security** | EDR (CrowdStrike, Defender ATP, SentinelOne), XDR, MDM |
| **Domain/IP Reputation** | WHOIS, AbuseIPDB, GEO-IP |
| **File Analysis** | Strings, VirusTotal, YARA |
| **Sandboxing** | Joe Sandbox, Cuckoo Sandbox |
| **Email Analysis** | MXToolbox, Email header analysis |
| **Decoding/Parsing** | CyberChef |
| **UEBA** | OpenUBA, User and Entity Behavior Analytics |
| **Threat Intelligence** | OTX (AlienVault), MISP, OpenCTI |

**Teknik Umum:**
- **Pattern recognition** — command and control pattern, data exfiltration pattern
- **Email analysis** — header analysis (SPF, DKIM, DMARC), impersonation detection, embedded links
- **File analysis** — hashing (MD5, SHA1, SHA256), file signature (magic bytes)
- **User behavior analysis** — abnormal account activity, impossible travel

**File Formats yang Sering Dianalisis:**
- JSON, XML, YAML, EVTX (Windows Event Log)
- **Scripting Languages:** Python, PowerShell, Shell script
- **Regex** — pattern matching untuk deteksi IoC

### 1.5 Threat Intelligence and Hunting

**Threat Actors:**
| Type | Motivasi | Contoh |
|---|---|---|
| APT | Spionase, geopolitik | APT29, Lazarus |
| Hacktivist | Ideologi | Anonymous |
| Organized Crime | Finansial | FIN7, Wizard Spider |
| Nation-State | Geopolitik | GRU, MSS |
| Script Kiddie | Popularitas, iseng | Tools siap pakai |
| Insider Threat | Finansial, dendam | Karyawan tidak puas |
| Supply Chain | Compromise downstream | SolarWinds |

**TTPs (Tactics, Techniques, Procedures):**
- **Pyramid of Pain** — Hash → IP → Domain → Host Artifact → Network Artifact → TTPs (semakin ke atas semakin sulit diubah attacker)
- **MITRE ATT&CK** — knowledge base TTPs
- **Attribution** — menghubungkan serangan ke group tertentu (sulit, butuh multiple data points)

**Confidence Levels:**
- **Timeliness** — informasi masih relevan?
- **Relevance** — apakah berlaku untuk lingkungan organisasi?
- **Accuracy** — apakah sumber terpercaya?

**Collection Methods and Sources:**
| Source | Contoh |
|---|---|
| **OSINT** | Social media, blogs, government bulletins, CERT/CSIRT, deep/dark web |
| **Closed-source** | Paid feeds (Recorded Future, ThreatConnect), ISACs |
| **Internal** | Log historis, incident records, threat hunts |

**Threat Intelligence Sharing:**
- **ISACs** — Information Sharing and Analysis Centers (FS-ISAC, MS-ISAC)
- **MISP** — Malware Information Sharing Platform
- **STIX/TAXII** — standar pertukaran threat intelligence

**IoC (Indicators of Compromise):**
- **Atomic** — tidak bisa dipecah (IP, hash, domain)
- **Behavioral** — pola aktivitas (login dari IP asing, file download setelah email phishing)
- **Collection → Analysis → Application**

**Threat Hunting:**
- **Hypothesis-driven** — "mungkin ada C2 yang tidak terdeteksi"
- **Baseline-driven** — "apa yang normal di lingkungan ini?"
- **Fokus area:** configurations/misconfigurations, isolated networks, business-critical assets

**Cyber Deception:**
- **Honeypot** — sistem palsu untuk menarik dan mendeteksi attacker
- **Honeytoken** — data palsu (file, credential) yang jika diakses menandakan breach

### 1.6 Process Improvement in Security Operations

**Standardize Processes:**
- **Playbook/Runbook** — prosedur terstandarisasi untuk skenario umum
- **Manage and facilitate team coordination** — shift handover, incident bridge

**Streamline Operations:**
- **SOAR (Security Orchestration, Automation, Response)** — otomatisasi respon, playbook execution
- **IaC (Infrastructure as Code)** — konfigurasi keamanan sebagai kode (Terraform, Ansible)
- **Data enrichment** — enrich IP/domain/hash dengan threat intelligence otomatis
- **Rule/alert tuning** — refine aturan deteksi berdasarkan false positive rate
- **Dashboard creation** — visualisasi untuk SOC monitoring

**Technology and Tool Integration:**
- **APIs** — REST, GraphQL untuk integrasi tool
- **Webhooks** — event-driven notification
- **Plugins** — ekstensibilitas platform

**Single Pane of Glass** — satu dashboard untuk semua monitoring

### 1.7 AI in Security Operations

**AI Risks:**
- **Hallucinations** — AI memberikan informasi palsu dengan yakin
- **Data exposure** — data sensitif bocor melalui AI training/prompts
- **Model poisoning** — attacker mengkompromi model AI
- **Malicious prompts** — prompt injection, jailbreaking

**Governance:**
- **Legal/regulatory compliance** — AI usage policy
- **AI usage policies** — kapan AI boleh digunakan, data apa yang boleh diproses

**Use Cases:**
- Comparing artifacts — membandingkan file/malware samples
- Analyzing log files — natural language query ke log
- Document creation — generate laporan otomatis
- Incident investigation — AI-assisted triage
- Event correlation — menghubungkan event dari berbagai sumber
- Automation and orchestration — AI-driven SOAR playbooks

---

## Domain 2: Vulnerability Management (26%)

### 2.1 Vulnerability Scanning Methods

**Asset Inventory:**
- **Discovery scanning** — menemukan semua perangkat di jaringan
- **Mapping scans** — memetakan topology dan hubungan antar perangkat
- **Device fingerprinting** — menentukan OS, service, versi

**Scanning Considerations:**
- **Scheduling** — waktu scan agar tidak mengganggu operasional
- **Operations** — impact ke network dan sistem
- **Performance** — bandwidth dan resource consumption
- **Sensitivity levels** — sistem critical perlu pendekatan berbeda
- **Segmentation** — scan harus mencakup semua segmen
- **Regulatory requirements** — PCI DSS, HIPAA, SOAR

**Scan Types:**
| Metode | Deskripsi |
|---|---|
| **Internal vs External** | Dari dalam network vs dari internet |
| **Agent vs Agentless** | Software diinstal di host vs remote scanning |
| **Credentialed vs Non-credentialed** | Dengan login vs tanpa login (lebih dangkal) |
| **Passive vs Active** | Monitor traffic vs kirim probes |
| **Discovery** | Menemukan aset (mapping, fingerprinting) |
| **Security Baseline** | CIS benchmarks, PCI DSS, ISO 27000 |

### 2.2 Vulnerability Assessment Tools

| Kategori | Tools |
|---|---|
| **Network Scanning & Mapping** | Angry IP Scanner, Masscan |
| **Multipurpose** | Nmap, Metasploit Framework, Maltego, Recon-ng |
| **Web Application Scanners** | Burp Suite, ZAP, Nikto |
| **Vulnerability Scanners** | Nessus, Nuclei, OpenVAS |
| **Cloud Infrastructure Assessment** | ScoutSuite, Prowler, Trivy, Checkov |
| **Breach Attack Simulation (BAS)** | Atomic Red Team, Caldera |

**Output Analysis:**
- Interpretasi hasil scan — bedakan **true positive**, **false positive**, **true negative**, **false negative**
- Validasi temuan dengan tools berbeda
- Konteks: tidak semua vulnerability sama-sama kritis

### 2.3 Vulnerability Prioritization

**Criteria:**
- **Exploitability** — apakah ada exploit yang tersedia?
- **Active exploitation** — apakah sedang dieksploitasi di wild?
- **Threat intelligence** — apakah threat actor menargetkan vulnerability ini?
- **Asset value** — seberapa penting aset yang terdampak?
- **Impact** — confidentiality, integrity, availability impact
- **Patch/remediation availability** — apakah patch sudah tersedia?

**Scoring Methods:**
- **CVSS v3.1** — Base Score (0-10): Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope, Confidentiality/Integrity/Availability Impact
- **EPSS (Exploitability Prediction Scoring System)** — probabilitas exploitasi di wild (0-100%), melengkapi CVSS
- Gunakan **CVSS + EPSS + Context** untuk prioritas akurat

**Context Awareness:**
- **Internal vs External** — sistem internet-facing lebih prioritas
- **Isolated** — sistem di network terisolasi mungkin kurang prioritas

### 2.4 Mitigation Strategies

- **Attack surface management** — kurangi permukaan serangan
- **Secure coding best practices** — OWASP ASVS, SAMM
- **Patching and configuration management** — patch cycle, change management
- **Exceptions** — jika patch tidak bisa, dokumentasikan risiko
- **Compensating controls** — WAF, network segmentation, monitoring

### 2.5 Control Types and Risk Concepts

**Control Types:**
| Type | Contoh |
|---|---|
| **Administrative** | Policies, procedures, training |
| **Technical** | Firewall, encryption, MFA |
| **Physical** | Locks, guards, CCTV |

**Control Functions:**
| Function | Tujuan |
|---|---|
| **Preventative** | Mencegah sebelum terjadi (firewall) |
| **Detective** | Mendeteksi saat terjadi (IDS) |
| **Responsive** | Merespon setelah terjadi (IR plan) |
| **Corrective** | Memperbaiki setelah terjadi (patching) |

**Risk Concepts:**
- **Risk Appetite** — seberapa banyak risiko yang diterima organisasi
- **Residual Risk** — risiko yang tersisa setelah kontrol diterapkan
- **Inherent Risk** — risiko sebelum kontrol

**Risk Management Strategies:**
- **Accept** — terima risiko
- **Transfer** — pindahkan ke pihak lain (asuransi)
- **Avoid** — hindari aktivitas berisiko
- **Mitigate** — kurangi risiko dengan kontrol

**Application Security:**
- **SAST (Static Application Security Testing)** — white-box, analisis source code
- **DAST (Dynamic Application Security Testing)** — black-box, analisis aplikasi berjalan
- **SAMM (Software Assurance Maturity Model)** — maturity model untuk secure SDLC

**Third-Party Risk:**
- **Supply Chain** — vendor, contractor, SaaS
- **SCA (Software Composition Analysis)** — analisis dependency/library
- **SBOM (Software Bill of Materials)** — daftar semua komponen software

---

## Domain 3: Incident Response and Management (24%)

### 3.1 Attack Methodology Frameworks

**Cyber Kill Chain (Lockheed Martin):**
```
1. Reconnaissance → 2. Weaponization → 3. Delivery
→ 4. Exploitation → 5. Installation → 6. Command & Control
→ 7. Actions on Objectives
```

**Diamond Model:**
```
        Adversary
           │
    Capability —— Infrastructure
           │
         Victim
```
Empat inti: **Adversary, Capability, Infrastructure, Victim** — plus meta-features (timestamp, phase, result, direction, methodology, resources)

**MITRE ATT&CK** — 15 tactics, 200+ techniques — mapping TTPs ke framework

**OSSTMM** — Open Source Security Testing Methodology Manual
**OWASP Testing Guide** — web application testing framework

### 3.2 Incident Response Process (7 Phases)

```
1. Preparation
2. Detection & Analysis
3. Containment, Eradication & Recovery
4. Post-Incident Activity
```

**Preparation:**
- IR plan, playbook, tools, training
- Communication plan — siapa dihubungi, kapan, bagaimana
- Tabletop exercises — simulasi insiden

**Detection & Analysis:**
- **Triage** — true positive, false positive, benign positive
- **Timeline establishment** — kronologi event
- **Root cause analysis** — apa penyebab utama?

**Containment:**
- **Scope** — seberapa luas dampak
- **Impact** — sistem, data, user yang terdampak
- **Isolation** — network segmentation, host isolation, cloud account disable

**Eradication:**
- Remove malware
- Patch vulnerability
- Reset credentials
- Rebuild systems jika perlu

**Recovery:**
- Restore from backup
- Monitor for re-infection
- Gradual return to production

**Post-Incident Activity:**
- **Forensic analysis** — deeper investigation
- **Root cause analysis** — apa yang menyebabkan insiden
- **Lessons learned** — apa yang bisa diperbaiki

### 3.3 Evidence Acquisition

**Chain of Custody:**
Dokumentasi siapa, kapan, di mana, bagaimana evidence dikumpulkan, disimpan, dan dipindahkan:
- **Tag evidence** — unique identifier
- **Log setiap transfer** — nama, tanggal, tujuan, alasan
- **Secure storage** — locked container, access controlled

**Data Integrity Validation:**
- **Hashing** — SHA256/MD5 sebelum dan sesudah analisis
- **Write blocker** — hardware/software write blocker untuk forensic acquisition

**Preservation:**
- **Legal hold** — jangan hapus data yang relevan
- **Snapshot/imaging** — bit-for-bit copy

### 3.4 Containment Strategies

| Strategy | Teknik |
|---|---|
| **Network** | Block IP/domain, disable port, network segmentation |
| **Host** | Isolate host, disable account, kill process |
| **Cloud** | Disable API keys, revoke session, isolate instance |
| **Identity** | Reset credentials, revoke tokens, enable MFA |

### 3.5 Escalation Procedures

- **Criteria** — kapan eskalasi ke tier 2/3, manajemen, legal
- **Notification** — siapa yang harus diberitahu dan dalam waktu berapa lama
- **Stakeholder communication** — tailored per audiens

### 3.6 Eradication Techniques

- Antivirus/EDR scan + clean
- System restore / reimage
- Patch the root cause
- Password reset untuk semua akun terdampak
- Rotate API keys dan certificates
- Block IoCs di perimeter

---

## Domain 4: Reporting and Communication (16%)

### 4.1 Vulnerability Management Reporting

**Vulnerability Scan Reports:**
- **Executive summary** — ringkasan untuk manajemen (risiko bisnis, bukan teknis)
- **Compliance findings** — PCI DSS, HIPAA, SOX
- **Risk scorecards** — visualisasi risiko per sistem/departemen
- **Action plans** — rekomendasi perbaikan, escalation paths, dependencies

**Inhibitors to Remediation:**
- Contractual agreements — vendor lock-in, SLA
- Organizational governance — change management, approval process
- Business process interruption — patch menyebabkan downtime
- Degrading functionality — patch mempengaruhi fitur yang dibutuhkan
- Legacy systems — tidak bisa di-patch
- Proprietary systems — vendor tidak menyediakan patch
- Patch availability — patch belum dirilis

**Stakeholder Identification and Communication:**
| Audience | Fokus |
|---|---|
| Technical team | IoC, timeline, technical details |
| Management | Business impact, risk, recommendations |
| Legal | Compliance, liability, disclosure obligations |
| PR/Customer | Data breach notification |
| Law enforcement | Criminal investigation |

**Metrics and KPIs:**
| Metric | Deskripsi |
|---|---|
| **Trends** | Perubahan jumlah temuan dari waktu ke waktu |
| **Top risks** | Vulnerability paling kritis |
| **SLA compliance** | % perbaikan dalam waktu yang ditentukan |
| **Remediation rate** | Berapa cepat temuan diperbaiki |

### 4.2 Incident Response Reporting

**Incident Declaration and Escalation:**
- Kriteria: confirmed compromise, data breach, service impact
- Tingkat eskalasi: Tier 1 → Tier 2 → Tier 3 → Management → Legal/PR

**Shift/Incident Handover:**
- Status investigasi
- Apa yang sudah dilakukan
- Apa yang masih berjalan
- Priority actions untuk shift berikutnya

**Executive Summary:**
```
Who: Threat actor / affected users
What: Type of incident
When: Timeline of events
Where: Systems and data affected
Why: Root cause (if known)
Impact: Business impact
Recommendations: Actions needed
```

**Internal Threat Intelligence Report:**
- IoCs baru yang ditemukan
- TTPs yang diamati
- Rekomendasi untuk deteksi dan pencegahan

**Communication Plan:**
- Tailored per stakeholder
- Legal team, PR, customer, media, law enforcement, regulatory bodies

**Metrics and KPIs:**
| Metric | Deskripsi |
|---|---|
| **MTTD (Mean Time to Detect)** | Waktu dari compromise ke deteksi |
| **MTTR (Mean Time to Respond)** | Waktu dari deteksi ke respon |
| **MTTC (Mean Time to Close)** | Waktu total dari deteksi ke penutupan |
| **False Positive Rate** | % alert yang false positive |
| **Alert Volume** | Jumlah alert per hari/shift |
| **Phishing Campaign Click Rate** | % user yang klik phishing simulation |

---

## Key Tools Reference

| Category | Tools | CySA+ Focus |
|---|---|---|
| **Packet Analysis** | Wireshark, tcpdump | Network anomaly detection, protocol analysis |
| **IDS/IPS** | Snort, Suricata, Zeek | Signature vs anomaly, alert analysis |
| **Vulnerability Scanner** | Nessus, OpenVAS, Nuclei | Scan configuration, output interpretation |
| **Web App Scanner** | Burp Suite, ZAP, Nikto | Web vulnerability identification |
| **Network Mapper** | Nmap, Masscan, Angry IP | Port scanning, service discovery |
| **SIEM** | Splunk, ELK, QRadar, ArcSight | Log correlation, alerting, dashboard |
| **SOAR** | Splunk SOAR, Palo Alto XSOAR | Automation, playbook, orchestration |
| **EDR/XDR** | CrowdStrike, Defender, SentinelOne | Endpoint detection, process analysis |
| **Threat Intel** | MISP, OTX, OpenCTI | IoC management, threat sharing |
| **File Analysis** | VirusTotal, YARA, Strings | Malware identification, signature |
| **Decoding** | CyberChef | Data decoding, decryption, parsing |
| **Cloud Assessment** | ScoutSuite, Prowler, Trivy, Checkov | Cloud security misconfiguration |
| **BAS** | Atomic Red Team, Caldera | Adversary simulation, detection test |
| **Sandbox** | Joe Sandbox, Cuckoo | Malware behavioral analysis |

## Key Frameworks Reference

| Framework | Domain | Purpose |
|---|---|---|
| **MITRE ATT&CK** | 1, 3 | TTP knowledge base, detection mapping |
| **Cyber Kill Chain** | 3 | 7-phase attack lifecycle |
| **Diamond Model** | 3 | Adversary-intrusion analysis |
| **STRIDE** | 1 | Threat modeling (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation) |
| **OWASP Top 10** | 2 | Web application risks |
| **NIST SP 800-61** | 3 | Incident response guidelines |
| **NIST SP 800-53** | 2 | Security control catalog |
| **NIST CSF** | 1 | Cybersecurity framework (Identify, Protect, Detect, Respond, Recover) |
| **ISO 27001** | 2 | Information security management |
| **CIS Benchmarks** | 2 | Configuration hardening standards |
| **PCI DSS** | 2 | Payment card industry security |
| **PTES** | 2 | Penetration testing standard |

## Exam Preparation Tips

### Performance-Based Questions (PBQ)
- PBQ menguji **praktik langsung**, bukan teori
- Tips:
  1. Baca skenario dengan teliti — perhatikan peran, tools yang tersedia, tujuan
  2. Identifikasi **prioritas** — apa yang paling mendesak?
  3. Gunakan **metodologi** yang benar — IR process, scan methodology
  4. Jangan terlalu lama di satu PBQ — jawab sebisanya, tandai, lanjut

### Multiple-Choice Strategies
- **Eliminasi** — buang opsi yang jelas salah
- **Perhatikan kata kunci:** BEST, FIRST, MOST, LEAST — ini mengubah jawaban
- **Context matters** — jawaban tergantung skenario (bukan definisi absolut)
- **Negative questions** — "Which of the following is NOT..." — baca dengan hati-hati

### Time Management
- 165 menit untuk 85 soal — ~2 menit per soal
- PBQ biasanya butuh waktu lebih lama — alokasikan 5-10 menit per PBQ
- Jangan terjebak di satu soal — tandai dan lanjut

### Recommended Study Path
1. **Exam Objectives** — download dari CompTIA, pelajari setiap sub-objective
2. **Hands-on Labs** — praktik tools: Wireshark, Nmap, Nessus, Burp Suite, Snort
3. **Practice Tests** — familiar dengan format soal dan timming
4. **Review Weak Domains** — berdasarkan hasil practice test

## Kapan Menggunakan Skill Ini

**Gunakan ketika:**
- Mempersiapkan ujian CompTIA CySA+ CS0-004
- Membutuhkan referensi cepat domain Security Operations
- Membutuhkan panduan Vulnerability Management dan prioritization
- Mempelajari Incident Response framework dan proses
- Membutuhkan template reporting dan communication untuk SOC

**Jangan gunakan ketika:**
- Membutuhkan panduan implementasi teknis spesifik (tool config) — gunakan dokumentasi tool
- Membutuhkan threat modeling arsitektur detail — gunakan skill threat-modeling
- Membutuhkan panduan NIST 800-53 — gunakan skill nist-800-53
- Membutuhkan incident response non-teknis (manajerial) — gunakan skill incident-response-plan
