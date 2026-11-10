---
name: "Referensi — Sumber Eksternal dan Bacaan Lanjutan"
description: "Sumber rujukan untuk threat hunter: MITRE ATT&CK, dokumentasi Splunk, CrowdStrike, Suricata, Zeek, Wireshark, standar STIX/TAXII dan MISP, TLP, serta bahan latihan — beserta catatan verifikasi dan link rot."
tags: [references, sources, mitre, splunk, crowdstrike, suricata, zeek, stix, taxii, misp, tlp, lab]
---

# Referensi — Sumber Eksternal dan Bacaan Lanjutan

Daftar ini adalah sumber yang dipakai persona untuk memverifikasi klaim dan sintaks. Skill ini bukan salinan dokumentasi; bila detail teknis dibutuhkan, buka sumber aslinya.

> Catatan: tautan dapat berubah. Verifikasi ulang sebelum dipakai di laporan klien atau keputusan berbayar. Snapshot terakhir: 2026-11-10.

## 1. Taksonomi dan pemetaan

| Sumber | Kegunaan |
|---|---|
| [MITRE ATT&CK](https://attack.mitre.org) | taktik/teknik untuk hipotesis, mapping temuan, dan gap analysis |
| [ATT&CK Groups](https://attack.mitre.org/groups/) | profil aktor dan TTP per grup untuk hypothesis-driven hunt |
| [FIRST — DE-TH SIG](https://www.first.org/global/sigs/de-th/) | praktik detection engineering dan threat hunting |

Catatan: atribusi aktor selalu disertai sumber; nama grup tanpa bukti TTP bukan temuan.

## 2. SIEM dan EDR

| Sumber | Kegunaan |
|---|---|
| [Splunk docs](https://docs.splunk.com/Documentation) | SPL, `stats`/`eval`/`transaction`, `tstats`, data model |
| [CrowdStrike](https://www.crowdstrike.com) | event type Falcon, CQL, IOA, publikasi riset |

## 3. Jaringan

| Sumber | Kegunaan |
|---|---|
| [Suricata docs](https://docs.suricata.io) | rule, alert, deteksi protokol, ekstraksi file |
| [Zeek docs](https://docs.zeek.org) | conn/dns/http/ssl/files log dan tipe field |
| [Wireshark docs](https://www.wireshark.org/docs/) | display filter dan analisis PCAP |

## 4. Intel dan pertukaran

| Sumber | Kegunaan |
|---|---|
| [OASIS CTI documentation](https://oasis-open.github.io/cti-documentation/) | STIX 2.1 dan TAXII 2.1 |
| [MISP project](https://www.misp-project.org/) | feed management, korelasi event, export, galaxies |
| [FIRST — TLP](https://www.first.org/tlp/) | label Traffic Light Protocol dan aturan berbagi |

## 5. Endpoint Windows

| Sumber | Kegunaan |
|---|---|
| [SwiftOnSecurity sysmon-config](https://github.com/SwiftOnSecurity/sysmon-config) | baseline konfigurasi Sysmon untuk hunting |
| [Microsoft Learn](https://learn.microsoft.com) | dokumentasi event, PowerShell logging, audit policy |

## 6. Bacaan dan latihan

- **SANS Reading Room** — whitepaper hunting dan detection ([sans.org/white-papers](https://www.sans.org/white-papers/)).
- **Lab mandiri**: satu SIEM, satu EDR, satu sensor jaringan, lalu rekam aksi penyerang terkontrol. Hunt yang dijalankan di estate sendiri lebih berguna daripada membaca studi kasus tanpa pernah menulis narasi.
- **Studi kasus** di skill ini (LockBit, APT29, Lazarus) dipakai sebagai pola, bukan sebagai daftar nama yang dihafal.

## 7. Cara memakai sumber

1. **Klaim teknis** — cek dokumentasi vendor/standar, jangan mengandalkan ingatan.
2. **Angka dan ambang** — sebut baseline yang dipakai; ambang tanpa baseline adalah tebakan.
3. **Perubahan cepat** (event type, rule, teknik ATT&CK) — verifikasi ulang sebelum dipakai.
4. **Kutipan** — gunakan tautan asli, bukan ringkasan pihak ketiga bila memungkinkan.

## Best Practices

- Bedakan sumber primer (vendor/standar) dan sekunder (blog/ringkasan).
- Catat tanggal akses untuk klaim yang bergantung waktu.
- Jangan menyebarkan tautan yang tidak diverifikasi di laporan klien.
- Perbarui daftar ini saat standar atau event type utama berubah.
