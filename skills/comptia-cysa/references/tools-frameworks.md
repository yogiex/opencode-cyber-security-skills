---
name: "Tools and Frameworks — Field Kit Analyst"
description: "Kategori tool yang dipakai cyber defense analyst — packet analysis, IDS/IPS, vulnerability scanner, SIEM, SOAR, EDR, threat intel, cloud assessment, BAS — beserta framework acuan dan fokus kerjanya."
tags: [tools, frameworks, wireshark, snort, suricata, nessus, splunk, soar, edr, mitre-attack, nist, cis, owasp]
---

# Tools and Frameworks — Field Kit Analyst

Tool dipilih dari pertanyaan yang harus dijawab, bukan dari daftar yang paling populer. Tabel di bawah adalah peta cepat: kategori, tool yang umum dijumpai, dan framework yang memberi kosakata bersama antar-tim.

## 1. Tools by category

| Kategori | Tool |
|---|---|
| Packet analysis | Wireshark, tcpdump |
| IDS/IPS | Snort, Suricata, Zeek |
| Vulnerability scanner | Nessus, OpenVAS, Nuclei |
| Web app scanner | Burp Suite, ZAP, Nikto |
| Network mapper | Nmap, Masscan, Angry IP |
| SIEM | Splunk, ELK, QRadar, ArcSight |
| SOAR | Splunk SOAR, Palo Alto XSOAR |
| EDR/XDR | CrowdStrike, Defender, SentinelOne |
| Threat intel | MISP, OTX, OpenCTI |
| File analysis | VirusTotal, YARA, Strings |
| Decoding | CyberChef |
| Cloud assessment | ScoutSuite, Prowler, Trivy, Checkov |
| BAS | Atomic Red Team, Caldera |
| Sandbox | Joe Sandbox, Cuckoo |

Satu tool tidak menjawab semua. Nmap memetakan permukaan, scanner membandingkan kerentanan, Wireshark membuktikan apa yang benar-benar lewat di jaringan, dan SIEM mengorelasikan semuanya dalam waktu.

## 2. Frameworks

| Framework | Fokus | Kegunaan |
|---|---|---|
| MITRE ATT&CK | Security operations, incident response | basis pengetahuan TTP |
| Cyber Kill Chain | Incident response | siklus serangan tujuh fase |
| Diamond Model | Incident response | analisis adversary-intrusion |
| STRIDE | Security operations | threat modeling |
| OWASP Top 10 | Vulnerability management, appsec | risiko aplikasi web |
| NIST SP 800-61 | Incident response | panduan penanganan insiden |
| NIST SP 800-53 | Vulnerability management | katalog kontrol keamanan |
| NIST CSF | Security operations | Identify, Protect, Detect, Respond, Recover |
| CIS Benchmarks | Vulnerability management | hardening konfigurasi |
| PCI DSS | Vulnerability management, compliance | keamanan data kartu pembayaran |
| PTES | Vulnerability management | standar penetration testing |

## 3. Cara memilih

- Mulai dari pertanyaan investigasi, lalu pilih tool yang bisa menjawabnya.
- Pastikan tool yang dipakai bisa menghasilkan bukti dengan timestamp dan konteks host.
- Untuk pekerjaan yang sudah punya rumah, rujuk skill terkait daripada menduplikasi: `threat-intelligence` untuk lifecycle CTI, `ptes-standard` untuk fase pentest.
- Tool baru tanpa pemilik, runbook, dan tuning hanya menambah permukaan operasional.

## Best Practices

- Catat versi tool dan konfigurasi saat mengambil bukti.
- Jangan mengandalkan satu sumber data untuk klaim yang berdampak.
- Petakan deteksi ke ATT&CK agar lubang terlihat.
- Tinjau tool yang tidak pernah dipakai; lisensi dan alert yang tidak terpakai adalah biaya.
