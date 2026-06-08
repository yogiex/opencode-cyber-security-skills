---
name: "WAF Analysis Cycle & Evasion Strategies"
description: "Systematic 6-phase WAF analysis cycle (Identification, Rule Mapping, Defense Classification, Payload Design, Execution, Adaptation) and 4-layer evasion strategy framework with OPSEC prioritization."
tags: [waf, evasion, methodology, analysis, fingerprinting, opsec]
---

# WAF Analysis Cycle & Evasion Strategies

## Siklus Analisis WAF (6 Fase)

```
PHASE 1: Identifikasi & Fingerprinting
    ↓
PHASE 2: Rule & Logic Mapping
    ↓
PHASE 3: Klasifikasi Mekanisme Defense
    ↓
PHASE 4: Payload Design & Development
    ↓
PHASE 5: Eksekusi & Monitoring
    ↓
PHASE 6: Adaptasi & Optimasi
```

### Phase 1: Identifikasi & Fingerprinting

- Deteksi keberadaan WAF — payload standar return 403/429, response header khusus, block page template
- Identifikasi provider WAF — Cloudflare, Akamai, ModSecurity, AWS WAF, Azure WAF, F5, Imperva
- Tentukan versi dan kemungkinan konfigurasi

**Indikator WAF Presence:**
- Response header: `CF-Ray` (Cloudflare), `Server: cloudflare`, `X-Served-By` (Akamai), `X-Mod-Security` (ModSecurity)
- Block page: Cloudflare challenge page, ModSecurity error page, custom block page
- Status code: 403 Forbidden, 406 Not Acceptable, 429 Too Many Requests, 503 Service Unavailable

### Phase 2: Rule & Logic Mapping

- Kirim payload standar yang diketahui diblokir — catat pola blocking
- Kirim variasi kecil — ubah satu karakter, lihat perbedaan respon
- Identifikasi parameter mana yang diinspeksi dan mana yang tidak
- Tentukan sensitivity level — apakah blocking ketat atau longgar?
- Identifikasi false positive — input legitimate yang diblokir (menandakan rule terlalu agresif)

**Amati:**
- Apakah blocking berdasarkan keyword tertentu (`UNION`, `SELECT`, `<script>`)?
- Apakah blocking case-sensitive?
- Apakah encoding tertentu lolos?
- Apakah content type tertentu tidak diperiksa?

### Phase 3: Klasifikasi Mekanisme Defense

**Signature-Based (Blacklisting):** Mencocokkan request terhadap database pola serangan (regex). Paling umum, paling mudah di-bypass. Bypass: encoding, fragmentasi, case variation.

**Anomaly-Based / Scoring:** Memberi skor pada karakteristik mencurigakan — blokir jika melebihi threshold. Bypass: distribusikan elemen berbahaya di beberapa request, jaga skor tetap rendah.

**Behavioral Analysis:** Melacak sequence request dan rate pattern. Bypass: slow down, humanized pattern, distributed source IP.

**Machine Learning:** Mempelajari pola traffic normal dan mendeteksi anomali. Bypass: ML bisa dikelabui dengan pola yang tidak biasa tapi legitimate-looking.

### Phase 4: Payload Design & Development

Rancang payload based mapping dari phase 1-3. Terapkan teknik obfuscasi sesuai karakteristik WAF. Gunakan multi-layer encoding jika perlu.

**Pipeline Produksi Payload:**
```
Raw Idea → Base Payload → Adaptive Optimization → Testing → Final Payload
```

### Phase 5: Eksekusi & Monitoring

- Kirim payload terkontrol — jangan flood, lakukan bertahap
- Monitor respon WAF — blocked, allowed, challenged
- Analisis perbedaan respon antara payload normal dan payload dengan variasi
- Catat pola yang berhasil dan gagal

### Phase 6: Adaptasi & Optimasi

- Sesuaikan payload berdasarkan feedback dari phase 5
- Kembangkan teknik baru berdasarkan pola yang ditemukan
- Dokumentasikan pola yang berhasil untuk reuse

**Improvement Cycle:**
```
Execute Test → Measure Results → Analyze Gaps → Update Methodology → Refine Approach → Repeat
```

## Evasion Strategies — Empat Lapisan

```
Layer 1: Passive & Non-Destructive Analysis   (30% waktu)
Layer 2: Limited Diagnostic Testing            (25% waktu)
Layer 3: Intelligent & Adaptive Attacks        (35% waktu)
Layer 4: Systematic Exploitation               (10% waktu)
```

### Layer 1: Passive & Non-Destructive Analysis
**OPSEC Priority: Maximum**

- Analisis response headers dari request normal
- Bandingkan pola error — HTTP 403 vs 406 vs 429
- Deteksi perbedaan waktu respon (time-based analysis)
- Pelajari variasi respon di berbagai state

### Layer 2: Limited Diagnostic Testing
**OPSEC Priority: High**

- Kirim payload standar dengan variasi minor
- Uji WAF dengan serangan yang sudah dikenal
- Analisis pola blocking — parameter apa yang diinspeksi?
- Identifikasi false positive dan false negative

### Layer 3: Intelligent & Adaptive Attacks
**OPSEC Priority: Medium**

- Implementasi teknik obfuscasi lanjutan
- Gunakan multi-layer encoding
- Rancang context-aware attack
- Manfaatkan fitur spesifik bahasa/platform backend

### Layer 4: Systematic Exploitation
**OPSEC Priority: Low (final phase)**

- Pilih teknik paling efektif dari phase 3
- Implementasi serangan final
- Monitoring real-time
- Adaptasi dinamis jika ada resistensi

## Best Practices

- Dokumentasi setiap percobaan — apa yang berhasil dan gagal
- Mulai dari Layer 1, jangan langsung Layer 4
- Kirim payload bertahap, jangan flood
- Gunakan kombinasi 2+ teknik independen untuk hasil optimal
