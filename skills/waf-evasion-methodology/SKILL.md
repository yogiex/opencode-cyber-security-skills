---
name: waf-evasion-methodology
description: Pola pikir dan metodologi sistematis untuk WAF evasion — memahami parsing discrepancies, encoding gaps, dan logic mismatches antara WAF dan backend application.
license: MIT
compatibility: opencode
metadata:
  audience: penetration tester, red teamer, security researcher, bug bounty hunter
  approach: principles-first
  source: OWASP CRS, MITRE ATT&CK
---

# WAF Evasion — Pola Pikir dan Metodologi

**WAF bukanlah tembok. WAF adalah filter.** Ia bergantung pada signature, aturan, dan pola yang dikenal. Jika Anda bisa membuat traffic berbahaya terlihat "normal," Anda menang.

## When to Use This Skill

Invoke this skill when:
- User asks about WAF evasion techniques or bypassing web application firewalls
- User needs systematic methodology for analyzing and evading WAF protection
- User mentions specific WAF providers (Cloudflare, Akamai, ModSecurity, AWS WAF)
- User asks about parsing discrepancies, encoding mismatches, or HTTP smuggling

## Key Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| **Analysis Cycle** | 6-phase WAF analysis cycle, 4-layer evasion strategy, fingerprinting | [analysis-cycle.md](./references/analysis-cycle.md) |
| **Evasion Techniques** | 10 techniques with payload examples + multi-technique coordination | [evasion-techniques.md](./references/evasion-techniques.md) |
| **WAF Understanding** | Security models, WAFFLED research, parsing discrepancies | [understanding-waf.md](./references/understanding-waf.md) |
| **Evaluation Framework** | Priority formula, maturity model, key diagnostic questions | [evaluation-framework.md](./references/evaluation-framework.md) |

## Reference Documentation

| File | Description |
|------|-------------|
| [analysis-cycle.md](./references/analysis-cycle.md) | 6-phase cycle, 4-layer evasion strategies, OPSEC prioritization |
| [evasion-techniques.md](./references/evasion-techniques.md) | 10 techniques (direct IP, encoding, HPP, smuggling, etc.) |
| [understanding-waf.md](./references/understanding-waf.md) | WAF models, WAFFLED research, parsing discrepancies |
| [evaluation-framework.md](./references/evaluation-framework.md) | Priority formula, maturity model, key questions |

## Assets

| Asset | Description |
|-------|-------------|
| [checklist.md](./assets/checklist.md) | Systematic 8-section testing checklist |

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Systematic WAF analysis methodology | [analysis-cycle.md](./references/analysis-cycle.md) |
| Specific bypass techniques with payloads | [evasion-techniques.md](./references/evasion-techniques.md) |
| WAF internals and parsing research | [understanding-waf.md](./references/understanding-waf.md) |
| Technique prioritization and maturity | [evaluation-framework.md](./references/evaluation-framework.md) |
| Step-by-step testing checklist | [assets/checklist.md](./assets/checklist.md) |

## Gotchas

1. **Direct IP attack before anything else**: Jangan mulai dengan encoding/obfuscation kompleks. Cari origin IP via historical DNS, CT logs, atau subdomain enumeration terlebih dahulu. Jika origin langsung bisa diakses, Anda tidak perlu bypass WAF sama sekali.
2. **JSON escape `\/` adalah low-hanging fruit**: Banyak WAF besar (Cloudflare, AWS WAF, Akamai) tidak menangani `\/` sebagai escape sequence valid untuk `/`. Path traversal `..\/..\/etc\/passwd` lolos karena WAF memeriksa raw bytes, sementara `JSON.parse()` menormalisasi jadi `../`.
3. **OWASP CRS paranoia level matters**: Paranoia level 1-2 mudah di-bypass (bisa dengan case variation atau comment injection). Level 3-4 butuh teknik lanjutan seperti payload fragmentation atau anomaly score manipulation. Cek paranoia level WAF target sebelum menghabiskan waktu di teknik yang tidak perlu.
4. **Content-Type manipulation paling efektif**: WAF sering hanya memeriksa content-type tertentu. Kirim SQLi payload dengan `Content-Type: text/plain` atau ubah `application/json` jadi `text/plain; charset=utf-8`. WAF skip inspection, backend tetap parse dengan benar.
5. **Dokumentasi adalah force multiplier**: Satu payload yang berhasil hari ini mungkin tidak bekerja besok setelah WAF update. Dokumentasikan teknik yang berhasil dengan konteks (WAF version, paranoia level, teknik spesifik) — ini membangun knowledge base yang meningkatkan probabilitas sukses di target berikutnya.

## License

MIT
