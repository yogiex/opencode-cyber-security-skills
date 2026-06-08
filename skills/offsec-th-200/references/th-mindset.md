---
name: "Threat Hunting Mindset & Framework"
description: "OSTH hunting philosophy, PEAK framework, CrowdStrike SEARCH methodology, Cyber Kill Chain, MITRE ATT&CK, Diamond Model, and hypothesis development."
tags: [mindset, peak, search, kill-chain, mitre-attack, diamond-model, hypothesis]
---

# Threat Hunting Mindset & Framework

## Filosofi Dasar

OSTH mengajarkan **"Hunt, Don't Just React"** — proactive security practice di mana defender aktif mencari threat, bukan menunggu alerts. Tiga pilar:

1. **Hypothesis-Driven** — Setiap hunt dimulai dengan hipotesis
2. **Data-Driven** — Gunakan telemetry dari berbagai sumber
3. **Continuous Improvement** — Setiap hunt menghasilkan insight baru

## Golden Rules OSTH

1. **Start with the threat intel report** — IOC list + TTP description + APT profile = what to hunt for
2. **Think like an attacker** — Ask "if I were the adversary, what would I do next?"
3. **Correlate everything** — Single log = noise. Correlated logs across Splunk + CrowdStrike + Suricata = signal
4. **Document as you hunt** — Timeline should grow as you find evidence
5. **Splunk is your timeline, Falcon is your microscope** — Splunk gives breadth, Falcon gives depth
6. **Hypotheses evolve** — Your initial hypothesis will change as you find evidence
7. **The report is worth 70 points** — Screenshot every query, result, and artifact

## PEAK Threat Hunting Framework (SANS)

```
P — Plan & Prepare: Develop hypothesis, identify data sources, define success criteria
E — Execute Hunt: Run queries, analyze results, refine hypothesis
A — Analyze Findings: Correlate across data sources, determine scope, build timeline
K — Knowledge Sharing: Create report, update detection rules, share TTP intel
```

## CrowdStrike SEARCH Methodology

```
S — Sense: Collect broad telemetry, identify anomalous events
E — Enrich: Contextualize data with threat intelligence
A — Analyze: Form and test hypotheses
R — Reconstruct: Build complete attack narrative
C — Communicate: Deliver actionable findings
H — Hone: Improve automated detections
```

## Threat Hunting Types

| Type | Description | Example |
|------|-------------|---------|
| **Intel-Based** | Hunt using known IOCs from threat intel | Search for IP/Domain/Hash from report |
| **Hypothesis-Driven** | Hunt based on TTP hypotheses | "If APT29, they might use PowerShell + Dropbox C2" |
| **Baseline/Anomaly** | Hunt deviations from normal | "Why is this server making outbound connections at 3 AM?" |

## Hypothesis Development

Format: `"Adversary [TTP] on [system] using [technique] to achieve [goal]"`

Contoh:
- "Adversary is using PowerShell encoded commands on WEB01 to establish persistence"
- "Adversary is exfiltrating data via DNS tunneling through the proxy server"
- "Adversary moved laterally from WORKSTATION-01 to DC-01 using Pass-the-Hash"

## 3 Pertanyaan Kunci Saat Stuck

1. **"What does the threat intel report tell me?"** — Re-read. What IOCs did you miss?
2. **"Where else could the adversary be?"** — Check lateral movement scope
3. **"What data haven't I checked yet?"** — Splunk? CrowdStrike? Network logs? DNS? Proxy?

## Gotchas

- OSTH exam memberikan threat intel report di awal — gunakan sebagai kompas, jangan diabaikan
- Hipotesis awal hampir selalu berubah setelah menemukan bukti — itu normal, refine terus
- Tidak semua IoCs di threat report akan match — fokus pada yang match dan cari pola tambahan
- PEAK dan SEARCH adalah framework complementary, bukan competing — gunakan keduanya

## Best Practices

- Dokumentasi timeline secara real-time saat hunting
- Gunakan Diamond Model (Adversary → Infrastructure → Capability → Victim) untuk analisis
- Mapping setiap temuan ke MITRE ATT&CK untuk standardisasi
