---
name: "Reporting and Communication — Laporan, Stakeholder, Metrik"
description: "Menyampaikan temuan kepada audiens yang berbeda: laporan vulnerability management, hambatan remediasi, template executive summary insiden, fokus komunikasi per stakeholder, serta metrik MTTD/MTTR/MTTC yang dipakai untuk memutuskan."
tags: [reporting, communication, stakeholder, metrics, kpi, mttd, mttr, executive-summary, remediation]
---

# Reporting and Communication — Laporan, Stakeholder, Metrik

Laporan adalah produk kerja analyst, bukan lampiran. Temuan yang benar tetapi tidak dipahami audiensnya tidak akan mengubah apa pun; metrik yang tidak mengubah keputusan sebaiknya tidak ditampilkan.

## 1. Vulnerability management reporting

**Jenis laporan:**

- **Executive summary** — risiko bisnis, bukan detail teknis.
- **Compliance findings** — PCI DSS, HIPAA, SOX sesuai kebutuhan.
- **Risk scorecard** per sistem atau departemen.
- **Action plan** dengan rekomendasi remediasi.

**Hambatan remediasi:** kesepakatan kontraktual, tata kelola organisasi, gangguan proses bisnis, sistem legacy, sistem proprietary, dan ketersediaan patch.

Hambatan yang tidak disebutkan akan muncul lagi sebagai temuan yang sama pada periode berikutnya.

## 2. Stakeholder communication

| Audiens | Fokus |
|---|---|
| Tim teknis | IoC, timeline, detail teknis |
| Manajemen | dampak bisnis, risiko, rekomendasi |
| Legal | kepatuhan, liabilitas, kewajiban disclosure |
| PR/customer | notifikasi kebocoran data |

Satu laporan untuk semua audiens biasanya terlalu teknis untuk manajemen dan terlalu dangkal untuk engineer.

## 3. Incident response reporting

**Template executive summary:**

- **Who** — aktor ancaman atau pengguna terdampak.
- **What** — jenis insiden.
- **When** — timeline.
- **Where** — sistem dan data yang terdampak.
- **Why** — root cause.
- **Impact** — dampak bisnis.
- **Recommendations** — tindakan yang dibutuhkan.

Ringkasan tanpa timeline dan tanpa bukti yang bisa ditunjuk hanyalah narasi.

## 4. Metrics and KPIs

| Metrik | Arti |
|---|---|
| MTTD | Mean Time to Detect |
| MTTR | Mean Time to Respond |
| MTTC | Mean Time to Close |
| False positive rate | persentase alert yang ternyata false positive |
| Alert volume | jumlah alert per hari atau per shift |
| Remediation rate | kecepatan temuan diperbaiki |

Setiap metrik butuh definisi, periode, dan sumber data yang sama agar tren antar-periode bisa dibandingkan dan dipertanggungjawabkan.

## Best Practices

- Sesuaikan komunikasi dengan audiens: teknis untuk engineer, dampak dan keputusan untuk eksekutif.
- Gunakan metrik untuk menunjukkan efektivitas SOC dan dasar perbaikan, bukan untuk pamer.
- Dokumentasikan shift handover secara menyeluruh.
- Sertakan timeline remediasi di dalam laporan.
