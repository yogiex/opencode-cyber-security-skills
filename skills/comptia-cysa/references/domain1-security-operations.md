---
name: "Security Operations — Logging, Indikator, Hunting"
description: "Operasi keamanan harian: logging terpusat dan sinkronisasi waktu, indikator aktivitas berbahaya per lapisan, threat intelligence, hunting berbasis hipotesis, perbaikan proses dengan SOAR dan IaC, serta risiko dan tata kelola AI di SOC."
tags: [security-operations, logging, siem, ntp, indicators, lolbins, threat-intelligence, hunting, soar, ai]
---

# Security Operations — Logging, Indikator, Hunting

Operasi keamanan adalah tempat data mentah berubah menjadi keputusan. Analyst tidak menambah log sebanyak mungkin; ia memastikan log yang ada bisa dipercaya, waktu antar-sumber bisa dikorelasikan, dan setiap indikator punya konteks sebelum dinaikkan menjadi insiden.

## 1. Logging concepts

- **Sentralisasi lewat SIEM** — Syslog (RFC 5424), Windows Event Log, JSON/CEF sebagai format umum.
- **Sinkronisasi waktu lewat NTP** — standar UTC; drift lebih dari 1 detik harus diperbaiki karena korelasi lintas sumber bergantung pada jam yang sama.
- **Level log** — ERROR, WARNING, INFO, DEBUG; level menentukan apa yang layak masuk alert dan apa yang cukup untuk forensik.

Log yang tidak pernah diparse dengan benar hanya menambah volume. Parsing dan normalisasi lebih penting daripada jumlah sumber.

## 2. Indikator aktivitas berbahaya

| Lapisan | Indikator |
|---|---|
| Network | lonjakan bandwidth, beaconing, peer-to-peer tidak wajar, rogue device, port scan, trafik di port non-standar |
| Host | lonjakan CPU/memory, software atau proses tidak sah, perubahan registry, staging data untuk eksfiltrasi |
| Application | input anomali, akun tak terduga, komunikasi keluar yang tidak wajar, gangguan layanan |
| Cloud | pembuatan resource anomali, kompromi IAM, eksfiltrasi dari storage |
| Identity | impossible travel, kompromi akun, pola login tidak wajar |
| Email | BEC, kegagalan atau penyimpangan DMARC/DKIM/SPF, tautan terobfuskasi, lampiran berbahaya |

**LOLBins** yang sering muncul: `powershell.exe`, `mshta.exe`, `rundll32.exe`, `certutil.exe`, `bitsadmin.exe`. Deteksinya paling kuat lewat **parent-child process relationship**, bukan hanya nama proses — banyak di antaranya executable sah.

## 3. Threat intelligence

- **Aktor**: APT, hacktivist, organized crime, nation-state, insider, supply chain.
- **Pyramid of Pain**: hash → IP → domain → host artifact → network artifact → TTPs.
- **Tingkat keyakinan**: timeliness, relevance, accuracy.
- **Sumber**: OSINT, closed-source (feed berbayar), internal.

Feed yang tidak mengubah deteksi atau keputusan tidak memberi nilai. Sebelum menambah sumber, tentukan pertanyaan yang ingin dijawab.

## 4. Threat hunting

- **Hypothesis-driven** — hunting dimulai dari dugaan yang bisa diuji, bukan dari keinginan melihat log.
- **Baseline-driven** — perilaku normal per segmen dan per host menjadi pembanding.
- **Cyber deception** — honeypot dan honeytoken untuk memunculkan interaksi yang tidak seharusnya terjadi.

Hunting yang berakhir tanpa temuan tetap berguna bila menghasilkan deteksi baru, kontrol baru, atau hipotesis yang gugur — dan semuanya didokumentasikan.

## 5. Process improvement

- **SOAR** untuk mengotomatiskan langkah respons yang berulang.
- **IaC** agar konfigurasi deteksi dan infrastruktur bisa direview dan direproduksi.
- **Data enrichment** (aset, pemilik, reputasi) agar alert sampai dalam bentuk yang bisa diputuskan.
- **Rule/alert tuning** berdasarkan false positive dan hasil triase.
- **Dashboard** dan **single pane of glass** agar investigator tidak berpindah-pindah konsol.

Otomatisasi tanpa runbook hanya memindahkan kekacauan ke kecepatan mesin.

## 6. AI in security operations

**Risiko**: hallucinations, data exposure, model poisoning, malicious prompts.

**Tata kelola**: kepatuhan legal dan kebijakan penggunaan AI yang tertulis — data apa yang boleh masuk, siapa yang boleh memakainya, dan bagaimana output diverifikasi.

**Kegunaan**: artifact comparison, log analysis, document creation, incident investigation.

Output model adalah hipotesis sampai diverifikasi terhadap telemetri mentah. Jangan menyalinnya langsung ke laporan.

## Best Practices

- Standarkan proses dengan playbook dan runbook.
- Otomatiskan respons dengan SOAR setelah langkahnya stabil dan teruji.
- Integrasikan tool lewat API dan webhook, bukan sinkronisasi manual.
- Tuning rule deteksi secara berkelanjutan berdasarkan false positive rate dan hasil triase.
