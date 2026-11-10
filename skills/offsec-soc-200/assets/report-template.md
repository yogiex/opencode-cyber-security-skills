---
name: "Detection Report Template"
description: "Struktur laporan investigasi deteksi: ringkasan eksekutif, analisis per tindakan, IoC terkonsolidasi, aturan deteksi, dan lampiran."
tags: [report, template, detection, investigation, iocs, documentation]
---

# Detection Report Template

Struktur ini dipakai untuk laporan investigasi — baik untuk insiden nyata maupun latihan di lab. Yang membuatnya berguna bukan panjangnya, melainkan bahwa pembaca bisa mengulang setiap langkah.

Gunakan struktur ini:

```
1. Executive Summary (1 page)
   - High-level attack narrative (10-15 bullet points)
   - Key findings summary
   - Overall risk assessment

2. Per-Action Analysis
   Action 1: [Title]
   - Time window
   - Initial access vector
   - Attacker IP / Victim host
   - MITRE ATT&CK mapping
   - KQL queries used
   - Screenshots (query + result)
   - Detailed analysis of each attacker action
   - Indicators of Compromise (IOCs)

3. Indicators of Compromise (Consolidated)
   - IP addresses
   - Process names and PIDs
   - File hashes
   - Registry keys
   - Service names

4. Detection Rules
   - KQL queries created during analysis
   - Sigma rules (if applicable)

5. Appendices
   - Full query list
   - Timeline of events
   - Host-to-IP mapping
   - OSQuery results
```

## Catatan penulisan

- **Analisis per tindakan, bukan per timestamp.** Revert dan ingestion yang tertunda membuat urutan waktu menyesatkan; sebutkan di mana urutannya putus.
- **Query ditulis bersama hasilnya.** Temuan tanpa query, host, dan rentang waktu tidak bisa diverifikasi pembaca.
- **Keyakinan dinyatakan.** Pisahkan yang terbukti, yang paling mungkin, dan yang belum dikecualikan.
- **Sumber yang tidak tersedia dicatat.** "Tidak ada log" dan "tidak ada aktivitas" adalah dua kesimpulan berbeda.
- **IoC harus bisa dipakai.** Alamat, nama proses, hash, dan nama service ditulis apa adanya, siap dimasukkan ke aturan deteksi.
