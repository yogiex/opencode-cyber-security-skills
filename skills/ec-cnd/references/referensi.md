---
name: "Referensi — Sumber Eksternal dan Bacaan Lanjutan"
description: "Sumber rujukan untuk network defender: blueprint CND, publikasi NIST, CIS Benchmarks, MITRE ATT&CK/D3FEND, OWASP, CISA KEV, EPSS, dokumentasi tool, dan bahan latihan — beserta catatan verifikasi dan link rot."
tags: [references, sources, nist, cis, mitre, owasp, cisa, epss, standards, lab]
---

# Referensi — Sumber Eksternal dan Bacaan Lanjutan

Daftar ini adalah sumber yang dipakai persona untuk memverifikasi klaim. Skill ini bukan salinan dokumen; bila detail teknis dibutuhkan, buka sumber aslinya.

> Catatan: tautan dapat berubah. Verifikasi ulang sebelum dipakai untuk keputusan berbayar atau kepatuhan. Snapshot terakhir: 2026-11-09.

## 1. EC-Council

| Sumber | Kegunaan |
|---|---|
| [CND certification](https://cert.eccouncil.org/certified-network-defender.html) | cakupan sertifikasi, audiens |
| [CND Exam Blueprint v4.0](https://cert.eccouncil.org/wp-content/uploads/2024/04/CND-Exam-Blueprint-v4.pdf) | 8 domain dan sub-domain |

Catatan: sampul blueprint menulis v4.0 sementara footer halaman masih v3.0. Bila mengutip nomor versi, sebutkan ketidakcocokan ini.

## 2. NIST

| Publikasi | Relevansi |
|---|---|
| [SP 800-41 Rev.1](https://csrc.nist.gov/pubs/sp/800/41/r1/final) | pedoman firewall dan kebijakan |
| [SP 800-94](https://csrc.nist.gov/pubs/sp/800/94/final) | IDS/IPS |
| [SP 800-61 Rev.2](https://csrc.nist.gov/pubs/sp/800/61/r2/final) | incident handling |
| [SP 800-53 Rev.5](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final) | katalog kontrol |
| [SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | Zero Trust Architecture |
| [SP 800-125](https://csrc.nist.gov/pubs/sp/800/125/final) | keamanan virtualisasi |
| [SP 800-190](https://csrc.nist.gov/pubs/sp/800/190/final) | keamanan container |
| [SP 800-92](https://csrc.nist.gov/pubs/sp/800/92/final) | log management |
| [SP 800-123](https://csrc.nist.gov/pubs/sp/800/123/final) | keamanan server |

## 3. Baseline dan kerentanan

| Sumber | Kegunaan |
|---|---|
| [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks) | baseline OS/aplikasi/cloud |
| [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | kerentanan yang dieksploitasi aktif |
| [EPSS](https://www.first.org/epss) | probabilitas eksploitasi |
| [NVD](https://nvd.nist.gov) | detail CVE dan skor |

## 4. MITRE dan OWASP

| Sumber | Kegunaan |
|---|---|
| [MITRE ATT&CK](https://attack.mitre.org) | taktik/teknik penyerang untuk gap analysis |
| [MITRE D3FEND](https://d3fend.mitre.org) | pemetaan teknik pertahanan |
| [OWASP CRS](https://owasp.org/www-project-modsecurity-core-rule-set/) | rule set WAF |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | verifikasi keamanan aplikasi |
| [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/) | metodologi pengujian (untuk validasi defensif) |

## 5. Tool dan protokol

| Sumber | Kegunaan |
|---|---|
| [nftables wiki](https://wiki.nftables.org) | sintaks dan konsep firewall Linux |
| [Wireshark docs](https://www.wireshark.org/docs/) | display filter dan analisis |
| [Zeek docs](https://docs.zeek.org) | log sesi dan analisis jaringan |
| [Suricata docs](https://docs.suricata.io) | IDS/IPS dan rule |
| [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | TLS 1.3 |
| [RFC 5246](https://www.rfc-editor.org/rfc/rfc5246) | TLS 1.2 |
| [Microsoft security baselines](https://learn.microsoft.com/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines) | baseline Windows |
| [AWS security documentation](https://docs.aws.amazon.com/security/) | kontrol cloud AWS |
| [Azure security benchmarks](https://learn.microsoft.com/azure/security/benchmarks/) | baseline Azure |
| [Google Cloud security best practices](https://cloud.google.com/security/best-practices) | baseline GCP |

## 6. Bacaan dan latihan

- **SANS Reading Room** — whitepaper operasional ([sans.org/white-papers](https://www.sans.org/white-papers/)).
- **CISA resources** — panduan hardening dan respons ([cisa.gov/resources-tools](https://www.cisa.gov/resources-tools)).
- **Lab**: bangun dua segmen dengan router Linux, satu IDS pasif, satu SIEM ringan; uji penolakan antar-segmen, capture, dan triase alert. Latihan yang aman lebih berguna daripada sertifikat tambahan.

## 7. Cara memakai sumber

1. **Klaim teknis** — cek dokumentasi vendor/standar, jangan mengandalkan ingatan.
2. **Angka dan versi** — sebut tanggal verifikasi dan sumbernya.
3. **Perubahan cepat** (CVE, fitur cloud) — verifikasi ulang sebelum dipakai.
4. **Kutipan** — gunakan tautan asli, bukan ringkasan pihak ketiga bila memungkinkan.

## Best Practices

- Bedakan sumber primer (vendor/standar) dan sekunder (blog/ringkasan).
- Catat tanggal akses untuk klaim yang bergantung waktu.
- Jangan menyebarkan tautan yang tidak diverifikasi di laporan klien.
- Perbarui daftar ini saat standar utama berubah.
