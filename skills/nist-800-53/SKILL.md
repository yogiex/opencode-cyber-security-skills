---
name: nist-800-53
description: Panduan Security and Privacy Controls berdasarkan NIST SP 800-53 Rev 5 (Release 5.2.0) untuk pemilihan, implementasi, dan assessment kontrol keamanan dan privasi dalam Risk Management Framework.
license: MIT
compatibility: opencode
metadata:
  audience: security engineer, risk manager, auditor, system owner, privacy officer, authorizing official
  standard: NIST SP 800-53 Rev 5
---

# NIST SP 800-53 — Security and Privacy Controls

## Pendahuluan

NIST SP 800-53 adalah katalog kontrol keamanan dan privasi untuk informasi sistem dan organisasi. Publikasi ini menyediakan **20 keluarga kontrol** yang mencakup aspek teknis, operasional, manajerial, dan privasi.

### Hubungan dengan Standar Lain

```
FIPS 199 (Impact Classification)
    └── FIPS 200 (Minimum Requirements)
            └── SP 800-53 (Control Catalog)
                    └── SP 800-53B (Control Baselines)
                    └── SP 800-53A (Assessment Procedures)
                            └── SP 800-37 (RMF)
```

- **FIPS 199** — menentukan impact level (Low/Moderate/High)
- **FIPS 200** — menetapkan minimum security requirements
- **SP 800-53B** — menyediakan baselines per impact level
- **SP 800-53A** — prosedur assessment untuk setiap kontrol
- **SP 800-37** — Risk Management Framework yang menggunakan kontrol 800-53

### Mengapa NIST 800-53 Penting?

- **Standar federal** — wajib untuk US federal agencies (FISMA)
- **Adopsi luas** — digunakan oleh FedRAMP, StateRAMP, dan industri swasta
- **Comprehensive** — mencakup security + privacy dalam satu katalog
- **Framework agnostic** — dapat dipetakan ke ISO 27001, CSF, PCI DSS
- **Risk-based** — kontrol dipilih berdasarkan risiko, bukan checklist

## Konsep Dasar

### Control

Kontrol adalah **spesifikasi** dari fungsi keamanan atau privasi. Setiap kontrol memiliki:

- **Control ID** — contoh: `AC-1` (Access Control keluarga, kontrol nomor 1)
- **Control Name** — contoh: `Policy and Procedures`
- **Control Text** — pernyataan kontrol yang harus dipenuhi
- **Discussion** — penjelasan dan guidance implementasi
- **Related Controls** — kontrol terkait dari keluarga lain
- **Control Enhancements** — variasi lebih ketat (contoh: AC-2(1), AC-2(2))

### Control Enhancements

Enhancements adalah variasi kontrol yang lebih spesifik atau lebih ketat:

- `AC-2(1)` — Automated System Account Management
- `AC-2(2)` — Removal of Temporary and Emergency Accounts
- `AC-2(3)` — Disable Inactive Accounts

Semakin tinggi nomor enhancement, semakin ketat kontrolnya.

### Baselines

Tiga baseline keamanan berdasarkan **impact level** (FIPS 199):

| Impact Level | Jumlah Kontrol (approx) | Contoh Sistem |
|---|---|---|
| **Low** | ~120 kontrol | Sistem internal non-kritis |
| **Moderate** | ~250 kontrol | Sistem dengan data sensitif |
| **High** | ~350+ kontrol | Sistem misi kritikal, data PII dalam jumlah besar |

Baseline ditentukan oleh **worst-case impact** dari Confidentiality, Integrity, Availability.

### Overlays

Overlay adalah **modifikasi baseline** untuk sektor atau teknologi spesifik:
- Cloud overlay (FedRAMP menambahkan kontrol)
- ICS/SCADA overlay
- Healthcare overlay
- Privacy overlay

### Parameterization

Banyak kontrol memiliki parameter yang diisi organisasi:

```
AC-2: "The organization manages information system accounts, including [Assignment: organization-defined identifiers]..."
```

Parameter memungkinkan kontrol yang sama diterapkan dengan konteks berbeda.

## 20 Control Families

### AC — Access Control
**Tujuan:** Membatasi akses ke sistem dan data sesuai otorisasi.

Kontrol penting: AC-2 (Account Management), AC-3 (Access Enforcement), AC-5 (Separation of Duties), AC-6 (Least Privilege), AC-7 (Unsuccessful Logon Attempts), AC-17 (Remote Access), AC-19 (Mobile Devices)

### AT — Awareness and Training
**Tujuan:** Memastikan personel memahami peran keamanan dan privasi.

Kontrol penting: AT-1 (Policy and Procedures), AT-2 (Literacy Training), AT-3 (Role-Based Training), AT-4 (Training Records)

### AU — Audit and Accountability
**Tujuan:** Mencatat dan memonitor aktivitas sistem untuk akuntabilitas.

Kontrol penting: AU-2 (Audit Events), AU-3 (Content of Audit Records), AU-6 (Audit Review, Analysis, and Reporting), AU-12 (Audit Generation)

### CA — Assessment, Authorization and Monitoring
**Tujuan:** Menilai, mengotorisasi, dan memonitor keamanan sistem secara berkelanjutan.

Kontrol penting: CA-2 (Security Assessments), CA-5 (Plan of Action and Milestones), CA-6 (Authorization), CA-7 (Continuous Monitoring)

### CM — Configuration Management
**Tujuan:** Mengontrol perubahan konfigurasi sistem dan baseline keamanan.

Kontrol penting: CM-2 (Baseline Configuration), CM-3 (Configuration Change Control), CM-6 (Configuration Settings), CM-8 (System Component Inventory)

### CP — Contingency Planning
**Tujuan:** Menyiapkan rencana darurat untuk menjaga operasi saat gangguan.

Kontrol penting: CP-2 (Contingency Plan), CP-7 (Alternate Processing Site), CP-9 (System Backup), CP-10 (System Recovery and Reconstitution)

### IA — Identification and Authentication
**Tujuan:** Memverifikasi identitas pengguna, perangkat, dan proses sebelum akses.

Kontrol penting: IA-2 (Identification and Authentication - Organizational Users), IA-5 (Authenticator Management), IA-8 (Identification and Authentication - Non-Organizational Users)

### IR — Incident Response
**Tujuan:** Mendeteksi, merespon, dan memulihkan dari insiden keamanan.

Kontrol penting: IR-4 (Incident Handling), IR-5 (Incident Monitoring), IR-6 (Incident Reporting), IR-8 (Incident Response Plan)

### MA — Maintenance
**Tujuan:** Melakukan perawatan sistem secara terkontrol dan aman.

Kontrol penting: MA-2 (Controlled Maintenance), MA-3 (Maintenance Tools), MA-4 (Non-local Maintenance), MA-5 (Maintenance Personnel)

### MP — Media Protection
**Tujuan:** Melindungi media digital dan fisik selama siklus hidup.

Kontrol penting: MP-2 (Media Access), MP-5 (Media Transport), MP-6 (Media Sanitization), MP-7 (Media Use)

### PE — Physical and Environmental Protection
**Tujuan:** Melindungi fasilitas fisik, perangkat keras, dan lingkungan pendukung.

Kontrol penting: PE-2 (Physical Access Authorizations), PE-3 (Physical Access Control), PE-6 (Monitoring Physical Access), PE-9 (Power Equipment and Cabling)

### PL — Planning
**Tujuan:** Merencanakan keamanan sistem secara menyeluruh dan terdokumentasi.

Kontrol penting: PL-2 (System Security and Privacy Plan), PL-4 (Rules of Behavior), PL-8 (Security and Privacy Architectures)

### PM — Program Management
**Tujuan:** Mengelola program keamanan dan privasi di tingkat organisasi.

Kontrol penting: PM-1 (Information Security Program Plan), PM-3 (Information Security and Privacy Resources), PM-9 (Risk Management Strategy), PM-32 (Supply Chain Risk Management Program)

### PS — Personnel Security
**Tujuan:** Memastikan personel yang memiliki akses ke sistem adalah pihak tepercaya.

Kontrol penting: PS-2 (Position Risk Designation), PS-3 (Personnel Screening), PS-4 (Personnel Termination), PS-6 (Access Agreements)

### PT — PII Processing and Transparency
**Tujuan:** Melindungi privasi individu melalui pengelolaan PII (Personally Identifiable Information).

Kontrol penting: PT-1 (Policy and Procedures), PT-2 (Authority to Process PII), PT-3 (Purpose Specification), PT-4 (Consent), PT-5 (Privacy Notice), PT-6 (System of Records Notice)

### RA — Risk Assessment
**Tujuan:** Mengidentifikasi dan mengevaluasi risiko keamanan dan privasi.

Kontrol penting: RA-2 (Security Categorization), RA-3 (Risk Assessment), RA-5 (Vulnerability Monitoring and Scanning), RA-7 (Risk Response)

### SA — System and Services Acquisition
**Tujuan:** Memastikan keamanan dalam akuisisi sistem, komponen, dan layanan.

Kontrol penting: SA-4 (Acquisition Process), SA-8 (Security and Privacy Engineering Principles), SA-11 (Developer Testing), SA-22 (Unsupported System Components), SA-24 (Software Bill of Materials)

### SC — System and Communications Protection
**Tujuan:** Melindungi komunikasi dan batas sistem.

Kontrol penting: SC-2 (Separation of System and User Functionality), SC-7 (Boundary Protection), SC-8 (Transmission Confidentiality and Integrity), SC-12 (Cryptographic Key Management), SC-13 (Cryptographic Protection), SC-28 (Protection of Information at Rest)

### SI — System and Information Integrity
**Tujuan:** Menjaga integritas sistem dan informasi yang diproses.

Kontrol penting: SI-2 (Flaw Remediation), SI-4 (System Monitoring), SI-7 (Software, Firmware, and Information Integrity), SI-10 (Information Input Validation), SI-16 (Memory Protection)

### SR — Supply Chain Risk Management
**Tujuan:** Mengelola risiko rantai pasok teknologi informasi.

Kontrol penting: SR-1 (Policy and Procedures), SR-3 (Supply Chain Controls), SR-4 (Provenance), SR-5 (Acquisition Strategies, Tools, and Methods), SR-11 (Component Authenticity)

## Security Baselines

### Memilih Baseline

1. **Categorize system** per FIPS 199 — tentukan impact level untuk Confidentiality, Integrity, Availability
2. **Overall impact** = highest dari ketiga kategori
3. **Select baseline** dari SP 800-53B sesuai overall impact

### Tailoring

Tailoring adalah **penyesuaian** baseline untuk organisasi:

- **Scoping** — exclude kontrol yang tidak relevan (contoh: sistem tidak memiliki mobile users → AC-19 bisa di-scope out)
- **Compensating controls** — gunakan kontrol alternatif jika kontrol utama tidak bisa diimplementasikan
- **Parameterization** — isi parameter sesuai kebutuhan organisasi

**Aturan tailoring:**
- Harap dokumentasikan alasan setiap tailoring
- Jangan tailor out kontrol hanya karena sulit diimplementasikan
- Compensating control harus memberikan protection yang setara atau lebih baik
- Tailoring harus disetujui Authorizing Official

### Contoh Baseline AC Controls per Impact

| Kontrol | Low | Moderate | High |
|---|---|---|---|
| AC-2 (Account Management) | ✓ | ✓ | ✓ |
| AC-2(1) - Automated Management | - | ✓ | ✓ |
| AC-2(2) - Removal of Temp/Emergency | - | ✓ | ✓ |
| AC-2(3) - Disable Inactive | - | - | ✓ |
| AC-3 (Access Enforcement) | ✓ | ✓ | ✓ |
| AC-6 (Least Privilege) | - | ✓ | ✓ |
| AC-17 (Remote Access) | ✓ | ✓ | ✓ |

## Privacy Controls

Rev 5 mengintegrasikan kontrol privasi ke dalam katalog utama (tidak lagi sebagai Appendix J terpisah).

### PT — PII Processing and Transparency

Kontrol PT adalah **wajib** untuk sistem yang memproses PII. Fokus utama:

- **Authority** — dasar hukum untuk memproses PII
- **Purpose** — spesifikasi tujuan pengumpulan PII
- **Consent** — mekanisme persetujuan individu
- **Notice** — transparansi kepada individu
- **SORN** — System of Records Notice
- **Minimization** — kumpulkan PII seminimal mungkin

### Privacy Collaboration

Setiap kontrol keamanan di 800-53 perlu dievaluasi apakah memiliki implikasi privasi:

- **AC controls** — akses ke PII harus dibatasi
- **AU controls** — audit log mungkin mengandung PII
- **SC controls** — enkripsi PII di transit dan di rest
- **SI controls** — integritas data PII

Gunakan **Control Collaboration Index Template** dari NIST untuk mapping security-privacy.

## Control Selection Process

Proses pemilihan kontrol mengikuti RMF (SP 800-37) enam langkah:

### Step 1: Categorize (FIPS 199)
- Tentukan impact level (Low/Moderate/High) untuk C, I, A
- Dokumentasikan dalam System Security and Privacy Plan (SSPP)

### Step 2: Select (SP 800-53B)
- Pilih baseline sesuai impact level
- Lakukan tailoring: scoping, parameterization, compensating controls
- Tambahkan controls dari keluarga lain jika diperlukan
- Dokumentasikan semua keputusan

### Step 3: Implement
- Implementasikan kontrol sesuai spesifikasi
- Dokumentasikan bagaimana setiap kontrol diimplementasikan
- Bukti implementasi: konfigurasi, kebijakan, prosedur

### Step 4: Assess (SP 800-53A)
- Uji setiap kontrol terhadap assessment procedures
- Kumpulkan evidence
- Hasil: pass, fail, atau other than satisfactory

### Step 5: Authorize
- Authorizing Official meninjau risk assessment
- Decision: Authorization to Operate (ATO), Denial, atau Conditions

### Step 6: Monitor
- Continuous monitoring sesuai CA-7
- Annual assessment untuk kontrol tertentu
- Update kontrol saat perubahan signifikan

## Assessment (SP 800-53A)

### Assessment Methods

| Method | Deskripsi | Contoh |
|---|---|---|
| **Examine** | Review dokumen, kebijakan, prosedur | Review kebijakan akses |
| **Interview** | Wawancara personel | Tanya proses incident response |
| **Test** | Eksekusi prosedur untuk verifikasi fungsi | Test authentication mechanism |

### Assessment Results

- **Pass** — kontrol berfungsi sesuai spesifikasi
- **Fail** — kontrol tidak berfungsi atau tidak ada
- **Not Applicable** — kontrol di-scope out dengan alasan sah

Setiap finding harus memiliki POA&M (Plan of Action and Milestones) jika gagal.

## Monitoring & Continuous Assessment

Continuous monitoring bukan hanya scanning:
- **Automated** — scanning, SIEM alerts, configuration compliance
- **Manual** — periodic review, audit log analysis, access review
- **Hybrid** — kombinasi automated + manual

### Key Metrics untuk Monitoring

- **Control effectiveness** — berapa persen kontrol berfungsi sebagaimana mestinya
- **Remediation time** — waktu perbaikan kontrol yang gagal
- **POA&M aging** — berapa lama temuan terbuka
- **Scan coverage** — berapa persen komponen tercakup dalam vulnerability scanning

## Release 5.2.0 Changes (August 2025)

Patch release dengan perubahan:

**New Controls/Enhancements:**
- `SA-15(13)` — Development Process, Standards, and Tools | Automated Vulnerability and Weakness Detection
- `SA-24` — Software Bill of Materials (SBOM)
- `SI-02(07)` — Flaw Remediation | Automated Flaw Remediation and Verification

**Revisions:**
- `SI-07(12)` — Software, Firmware, and Information Integrity | Verified Boot Integrity

**Discussion Updates:**
- SA-04, SA-05, SA-08, SA-08(14), SI-02, SI-02(05)

**Related Controls:**
- Semua -01 controls, AU-02, AU-03, CA-07, IR-04, IR-06, IR-08, SA-15, SI-02, SI-07

## Relationship to Other Frameworks

| Framework | Hubungan |
|---|---|
| **NIST CSF** | 800-53 controls memetakan ke CSF functions (Identify, Protect, Detect, Respond, Recover) |
| **ISO/IEC 27001:2022** | Crosswalk tersedia dari NIST — mapping Annex A controls ke 800-53 |
| **FedRAMP** | Menggunakan Moderate baseline + tambahan kontrol cloud-specific |
| **PCI DSS** | Mapping tidak resmi tapi banyak kontrol overlap (access control, logging, encryption) |
| **NIST Privacy Framework** | PT family dan privacy implications terintegrasi di seluruh kontrol |

## Key Questions

1. **"What's my FIPS 199 impact level?"** — Ini menentukan seluruh baseline yang berlaku
2. **"Which baseline applies — Low, Moderate, or High?"** — Dipilih berdasarkan overall impact level
3. **"What controls can be tailored out and why?"** — Setiap tailoring harus punya justifikasi
4. **"Am I addressing both security AND privacy?"** — Jangan hanya fokus pada security controls
5. **"How do I know a control is working?"** — Assessment dan monitoring harus terjadwal
6. **"What's my POA&M telling me?"** — POA&M adalah indikator kesehatan program keamanan
7. **"Are my controls keeping up with the threat landscape?"** — Controls perlu di-update saat ancaman berubah
8. **"What's the risk if I skip this control?"** — Setiap kontrol yang tidak diimplementasikan adalah risiko yang diterima

## Kapan Menggunakan Skill Ini

**Gunakan ketika:**
- Mendesain atau mengevaluasi keamanan sistem menggunakan framework NIST
- Mempersiapkan authorization (ATO) untuk sistem baru
- Melakukan audit atau assessment kepatuhan 800-53
- Memilih kontrol keamanan berdasarkan risk assessment
- Menerjemahkan persyaratan compliance ke kontrol teknis
- Menulis System Security and Privacy Plan (SSPP)
- Mempersiapkan FedRAMP atau StateRAMP authorization

**Jangan gunakan ketika:**
- Membutuhkan panduan implementasi teknis spesifik (tool konfigurasi) — gunakan dokumentasi tool terkait
- Membutuhkan risk management framework secara keseluruhan — gunakan skill risk-management-framework
- Membutuhkan incident response guidance — gunakan skill incident-response-plan
- Membutuhkan threat modeling — gunakan skill threat-modeling
- Hanya butuh baseline kontrol tanpa konteks — lihat langsung SP 800-53B

## References

- NIST SP 800-53 Rev 5: https://doi.org/10.6028/NIST.SP.800-53r5
- NIST SP 800-53A Rev 5: Assessment Procedures
- NIST SP 800-53B: Control Baselines
- NIST SP 800-37 Rev 2: Risk Management Framework
- FIPS 199: Standards for Security Categorization
- FIPS 200: Minimum Security Requirements
- Release 5.2.0 Summary of Changes (Supplemental Material)
