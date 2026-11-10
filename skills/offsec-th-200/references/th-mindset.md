---
name: "Threat Hunting Mindset & Framework"
description: "Filosofi hunting, PEAK framework, CrowdStrike SEARCH methodology, Cyber Kill Chain, MITRE ATT&CK, Diamond Model, tipe hunt, dan cara menyusun hipotesis yang bisa difalsifikasi."
tags: [mindset, peak, search, kill-chain, mitre-attack, diamond-model, hypothesis, hunting]
---

# Threat Hunting Mindset & Framework

## Filosofi Dasar

Doktrin kerjanya satu kalimat: **hunt, jangan hanya bereaksi**. Ini praktik keamanan proaktif — defender aktif mencari ancaman yang belum memicu alert, bukan menunggu antrean tiket. Tiga pilar:

1. **Hypothesis-Driven** — setiap hunt dimulai dengan hipotesis, bukan dengan membuka dashboard.
2. **Data-Driven** — kesimpulan diambil dari telemetri lintas sumber, bukan dari firasat.
3. **Continuous Improvement** — setiap hunt meninggalkan deteksi baru atau data source yang perlu ditambah.

## Golden Rules

1. **Mulai dari intel** — IOC list + deskripsi TTP + profil aktor memberi tahu apa yang dicari.
2. **Berpikir seperti penyerang** — "kalau aku adversary-nya, langkah berikutnya apa?"
3. **Korelasikan semuanya** — satu log adalah noise; log yang terkorelasi lintas Splunk + CrowdStrike + Suricata adalah signal.
4. **Dokumentasikan sambil berburu** — timeline tumbuh saat bukti ditemukan, bukan setelah ingatan memudar.
5. **Splunk adalah timeline, Falcon adalah mikroskop** — Splunk memberi keluasan, Falcon memberi kedalaman.
6. **Hipotesis berevolusi** — hipotesis awal hampir selalu berubah setelah bukti pertama masuk.
7. **Laporan yang membawa temuan** — temuan hanya bernilai bila query, hasil, timestamp, dan host-nya tercatat.

## PEAK Threat Hunting Framework

```
P — Plan & Prepare: Develop hypothesis, identify data sources, define success criteria
E — Execute Hunt: Run queries, analyze results, refine hypothesis
A — Analyze Findings: Correlate across data sources, determine scope, build timeline
K — Knowledge Sharing: Create report, update detection rules, share TTP intel
```

PEAK adalah siklus hunt. Fase `K` bukan formalitas: hunt yang tidak mengubah rule, playbook, atau data source berikutnya berhenti di tengah jalan.

## CrowdStrike SEARCH Methodology

```
S — Sense: Collect broad telemetry, identify anomalous events
E — Enrich: Contextualize data with threat intelligence
A — Analyze: Form and test hypotheses
R — Reconstruct: Build complete attack narrative
C — Communicate: Deliver actionable findings
H — Hone: Improve automated detections
```

SEARCH lebih cocok dipakai sebagai daftar periksa saat hunt sudah berjalan dan perlu dipertajam; PEAK dipakai sebagai kerangka siklus penuh. Keduanya saling melengkapi, bukan bersaing.

## Threat Hunting Types

| Type | Description | Example |
|---|---|---|
| **Intel-Based** | Hunt using known IOCs from threat intel | Search for IP/Domain/Hash from report |
| **Hypothesis-Driven** | Hunt based on TTP hypotheses | "If APT29, they might use PowerShell + Dropbox C2" |
| **Baseline/Anomaly** | Hunt deviations from normal | "Why is this server making outbound connections at 3 AM?" |

## Hypothesis Development

Format: `"Adversary [TTP] on [system] using [technique] to achieve [goal]"`

Contoh:

- "Adversary is using PowerShell encoded commands on WEB01 to establish persistence"
- "Adversary is exfiltrating data via DNS tunneling through the proxy server"
- "Adversary moved laterally from WORKSTATION-01 to DC-01 using Pass-the-Hash"

Hipotesis yang baik punya tiga sifat: bisa difalsifikasi (ada hasil yang akan membatalkannya), bisa dijawab dengan data yang tersedia, dan cukup sempit untuk diselesaikan dalam satu sprint hunt.

## 3 Pertanyaan Kunci Saat Stuck

1. **"Apa yang sebenarnya dikatakan intel brief-nya?"** — baca ulang. IOC mana yang belum dijalankan?
2. **"Di mana lagi penyerang bisa berada?"** — cek cakupan pergerakan lateral, bukan hanya host pertama.
3. **"Data apa yang belum saya cek?"** — Splunk? CrowdStrike? Network log? DNS? Proxy?

## Gotchas

- Intel brief adalah kompas, bukan dekorasi — kembalilah ke sana setiap kali hunt terasa buntu.
- Hipotesis awal hampir selalu berubah setelah menemukan bukti — itu normal; yang berbahaya adalah mempertahankannya demi konsistensi.
- Tidak semua IOC akan match — fokus pada yang match, lalu cari pola tambahan di sekitarnya.
- PEAK dan SEARCH saling melengkapi; memilih salah satu dan membuang yang lain hanya memindahkan titik buta.
- "Tidak ada temuan" tanpa cakupan data adalah asumsi, bukan hasil.

## Best Practices

- Dokumentasikan timeline secara real-time saat hunting.
- Gunakan Diamond Model (Adversary → Infrastructure → Capability → Victim) untuk analisis.
- Mapping setiap temuan ke MITRE ATT&CK untuk standardisasi dan perbandingan antar hunt.
- Tutup setiap hunt dengan satu keputusan: rule baru, data source baru, atau hipotesis berikutnya.
