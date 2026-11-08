# Certification Facts — Single Source of Truth

Angka ujian (durasi, jumlah soal, bobot, passing score) **hanya boleh** merujuk ke tabel ini. Jika sebuah skill perlu menyebut angka, salin dari sini dan sebutkan tanggal verifikasi.

**Terakhir diverifikasi:** 2026-11-08
**Metode:** `web_fetch` ke domain resmi (tanpa `web_search`). URL yang gagal dicatat di bagian bawah.

## Aturan

1. Jangan menulis angka ujian dari ingatan — ambil dari tabel ini.
2. Jika sumber berubah, perbarui tabel **dan** entri CHANGELOG; jangan edit angka di skill satu per satu tanpa memperbarui tabel.
3. Tandai klaim yang tidak terverifikasi sebagai `[UNVERIFIED]`, bukan angka pasti.
4. Sertifikasi berubah: **OSCP+ beralih ke scaled scoring pada 1 Des 2026** — periksa tanggal sebelum menjawab.

## OffSec

| Sertifikasi | Durasi | Struktur & poin | Passing | Tool/aturan kunci | Sumber |
|---|---|---|---|---|---|
| **OSCP+ (PEN-200)** | 23j45m + 24j report | 3 standalone (60: 10+10) + AD set (40: 10+10+20) | **70/100** untuk ujian sebelum **1 Des 2026 08:00 GMT**; setelahnya skala **100–500, lulus 400** (raw point bervariasi per set) | Metasploit **semua modul** + Meterpreter hanya **satu mesin**, tidak untuk pivoting; AI chatbot dilarang; PDF dalam .7z ≤200MB; 24 revert (reset 1×) | [Exam Guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide), [Scoring FAQ](https://help.offsec.com/hc/en-us/articles/54589877508884) |
| **OSEP (PEN-300)** | 47j45m + 24j | — | **Minimum 100 poin** | Remote interactive shell wajib (web shell/RDP tidak cukup); 50 revert | [Exam Guide](https://help.offsec.com/hc/en-us/articles/360050293792-OSEP-Exam-Guide) |
| **OSWE (WEB-300)** | 47j45m + 24j | — | **85/100** | PoC harus berjalan tanpa interaksi user; `sshfs`/`sftp` & source-code analyzer dilarang; X11 boleh | [Exam Guide](https://help.offsec.com/hc/en-us/articles/360046869951-WEB-300-Advanced-Web-Attacks-and-Exploitation-OSWE-Exam-Guide) |
| **OSDA (SOC-200)** | 23j45m + 24j | 10 phase × 10 = 100 | **75/100** | ELK/KQL; sejak 10 Sep 2025 memakai **pre-recorded logs** (tidak perlu "run the phases"); PDF via upload.offsec.com ≤200MB | [Exam Guide](https://help.offsec.com/hc/en-us/articles/4410105675412-OSDA-Exam-Guide) |
| **OSTH (TH-200)** | 8j + 24j | 7 exercise × 10 = 70 | **50/70** | Splunk + CrowdStrike Falcon + Suricata; sertifikat **kedaluwarsa** | [Exam Guide](https://help.offsec.com/hc/en-us/articles/29141776768148-OSTH-Exam-Guide) |
| **OSIR (IR-200)** | 8j + 24j | Phase 1: 4×10 + Phase 2: 2×15 = 70 | **50/70** | Splunk + disk image/malware analysis (bukan memory forensics); sertifikat **kedaluwarsa** | [Exam Guide](https://help.offsec.com/hc/en-us/articles/30960007786900) |

Masa berlaku: OffSec menyatakan sertifikasi **tidak kedaluwarsa kecuali** OSCC-SEC, OSCC-SJD, OSTH, OSIR, dan OSCP+ ([FAQ](https://help.offsec.com/hc/en-us/articles/4826237411732)). Durasi tahun untuk yang kedaluwarsa tidak dicantumkan di halaman tersebut — `[UNVERIFIED]`.

### Report bukan komponen nilai terpisah

Tidak ada ujian OffSec yang memberi bobot persentase khusus untuk report. Yang berlaku (dinyatakan di exam guide masing-masing):

| Ujian | Kalimat resmi |
|---|---|
| OSCP+ | "Points are only awarded for objectives documented in your report" + "If you don't submit a report, you can't pass" ([FAQ](https://help.offsec.com/hc/en-us/articles/54589877508884)) |
| OSEP | "failure to provide sufficient documentation will result in reduced or zero points"; urutan mesin di report = urutan penilaian; proof file tanpa screenshot + control panel = 0 poin untuk target ([Guide](https://help.offsec.com/hc/en-us/articles/360050293792-OSEP-Exam-Guide)) |
| OSDA | 10 phase × 10 poin; tidak ada komponen report terpisah ([Guide](https://help.offsec.com/hc/en-us/articles/4410105675412-OSDA-Exam-Guide)) |
| OSTH | 7 × 10 = 70; poin "based on submitting the correct answer and the completeness of your findings in the exam report" ([Guide](https://help.offsec.com/hc/en-us/articles/29141776768148-OSTH-Exam-Guide)) |
| OSIR | 4×10 + 2×15 = 70; aturan dokumentasi sama ([Guide](https://help.offsec.com/hc/en-us/articles/30960007786900)) |

Konsekuensi: klaim "report 50% nilai" atau "report = 70 points" **salah**. Report adalah gerbang: tanpa dokumentasi yang memadai, poin tidak diberikan.

## CompTIA / EC-Council

| Sertifikasi | Versi berlaku | Format | Passing | Sumber |
|---|---|---|---|---|
| **CySA+** | **CS0-004 (V4)**, launch 23 Jun 2026; V3 (CS0-003) pensiun 22 Des 2026 | maks 85 soal, 165 menit; bobot **34/26/24/16** | **750/900** (skala 100–900) | [CompTIA](https://www.comptia.org/certifications/cybersecurity-analyst) |
| **CPENT** | **Blueprint V2** | **53 soal praktik, 8 domain** (13/13/14/12/13/11/11/13); 24 jam (1×24 atau 2×12) | cut score **60–85%** per form; ≥90% = CPENT + LPT Master | [EC-Council](https://cert.eccouncil.org/cpent.html) |
| **ECIH** | 212-89 v3 | 100 MCQ, 3 jam; **9 domain** (11/11/11/12/12/11/10/11/11) | cut score **60–85%** | [EC-Council](https://cert.eccouncil.org/ecih.html) |

CPENT: report ≤30 hari (perpanjangan 7 hari, USD100); validitas 3 tahun/120 ECE; biaya recert USD250. `[UNVERIFIED]` kebijakan retake resmi dan bobot report (~30% diklaim di skill, tidak ada halaman publik EC-Council yang mengonfirmasi angka itu).

## CNCF / Kubernetes

| Sertifikasi | Versi | Format | Passing | Sumber |
|---|---|---|---|---|
| **CKS** | Kubernetes **v1.37** | 2 jam; **15–20 task** performance-based; 6 domain **15/15/10/20/20/20** | **67%** | [LF CKS](https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/), [Curriculum](https://github.com/cncf/curriculum/tree/main/cks) |

Prasyarat: **telah lulus CKA** (status aktif tidak disyaratkan eksplisit). Validitas 2 tahun; biaya $445; 1 retake; killer.sh 2×36 jam (17 soal/sesi). Catatan: `cncf/curriculum/cks/README.md` memuat bobot lama (10/15/15/…) — **jangan dikutip**; gunakan PDF kurikulum v1.37 atau halaman LF.

## Standar & kerangka (bukan sertifikasi)

| Standar | Versi/status | Fakta kunci | Sumber |
|---|---|---|---|
| MITRE ATT&CK | **v20.1** (13 Okt 2026) | 15 taktik Enterprise termasuk **Stealth (TA0005)** dan **Defense Impairment (TA0112)**; "Defense Evasion" tidak dipakai lagi; 227 teknik, 479 sub-teknik, 106 Data Components | [Tactics](https://attack.mitre.org/tactics/enterprise/), [Versions](https://attack.mitre.org/resources/versions/) |
| OWASP Top 10 | **2025** | A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions; **SSRF (CWE-918) masuk A01** | [Top 10:2025](https://top10.owasp.org/2025/) |
| OWASP WSTG | **4.2** | 12 kategori, 97 test case | [wstg.owasp.org](https://wstg.owasp.org/v4.2/) |
| OWASP ASVS | **5.0.0** (30 Mei 2025) | — | [asvs.owasp.org](https://asvs.owasp.org) |
| NIST SP 800-53 | Rev 5, rilis minor **5.2.0** (27 Agu 2025) | 20 keluarga kontrol; 5.2.0 menambah SA-15(13), SA-24, SI-02(07) dan merevisi SI-07(12) | [CSRC](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) |
| NIST SP 800-37 | Rev 2 (Des 2018) | RMF **7 langkah** (Prepare, Categorize, Select, Implement, Assess, Authorize, Monitor) | [CSRC](https://csrc.nist.gov/pubs/sp/800/37/r2/final) |
| NIST CSF | **2.0** | **6 fungsi**: Govern, Identify, Protect, Detect, Respond, Recover | [NIST](https://www.nist.gov/cyberframework) |
| NIST SP 800-92 | Final 2006; Rev 1 masih **Initial Public Draft** (11 Okt 2023) | Jangan menyebut Rev 1 sebagai final | [CSRC](https://csrc.nist.gov/pubs/sp/800/92/final) |
| NIST SP 800-218 (SSDF) | v1.1, Feb 2022; 800-218A final | 4 grup praktik: PO, PS, PW, RV | [CSRC](https://csrc.nist.gov/pubs/sp/800/218/final) |

## Tidak terverifikasi (jangan diisi tanpa sumber)

- Versi PCI DSS yang berlaku (halaman resmi tidak mengekstrak konten).
- Jumlah kontrol Annex A ISO/IEC 27001:2022 (dokumen berbayar).
- Tanggal rilis resmi OWASP Top 10:2025.
- Durasi tahun kedaluwarsa OSTH/OSIR/OSCP+.
- Kebijakan retake CPENT.
- Total kontrol SP 800-53 (angka 1.189 tidak dinyatakan di halaman resmi).

## Risiko yang sudah dikoreksi (riwayat)

- Metasploit "auxiliary bebas" → **salah**; semua modul dibatasi satu mesin (0 poin jika dilanggar).
- OSCP "50/100", OSEP "85/100" → **salah**; OSCP 70 raw (lalu 400/500), OSEP min 100.
- OSIR "23j45m, ELK, 70/100, no expiry" → **salah**; 8 jam, Splunk, 50/70, kedaluwarsa.
- ATT&CK "v15, 14 tactics, Defense Evasion" → **basi**; v20.1, 15 taktik, Stealth + Defense Impairment.
- RMF "enam langkah"; CSF "5 fungsi" → **salah**; 7 langkah, 6 fungsi.
- CPENT "5 soal"; ECIH "6 domain" → **salah**; 53 soal/8 domain, 9 domain.
- "Report 50% nilai" (OSCP, OSEP, OSDA) dan "report = 70 points / 30 dari 70" (OSTH, OSIR) → **salah**; report tidak punya bobot persentase, hanya gerbang pemberian poin.
- CPENT "submit 7 hari" → **salah**; deadline 30 hari (7 hari adalah perpanjangan berbayar).
