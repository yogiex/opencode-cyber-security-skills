---
name: "Legal, Compliance & Ethics in Incident Response"
description: "Regulatory framework (GDPR, HIPAA, PCI DSS, SOX, CCPA), key legal concepts (chain of custody, privilege, spoliation, eDiscovery), law enforcement involvement criteria, incident handler ethics, and regulatory notification decision tree."
tags: [ecih, legal, compliance, gdpr, hipaa, pci-dss, ethics, law-enforcement, regulatory-notification, privilege, spoliation]
---

## Legal, Compliance & Ethics

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
