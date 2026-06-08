---
name: "WAF Evasion Evaluation Framework & Maturity Model"
description: "Technique evaluation framework with priority formula (Success Probability × Impact × Executability / Complexity), priority matrix, 5-level WAF Evasion Maturity Model from Beginner to Optimizing, and key diagnostic questions for systematic WAF analysis."
tags: [waf, evasion, evaluation, maturity, framework, prioritization]
---

# WAF Evasion Evaluation Framework & Maturity Model

## Teknik Evaluation Framework

### Formula Prioritas
```
Value = (Success Probability × Impact × Executability) / Complexity
```

| Faktor | Komponen |
|--------|----------|
| **Success Probability** | Efektivitas historis, kompatibilitas WAF target, tingkat inovasi |
| **Impact** | Access gained, vulnerability level, target importance |
| **Executability** | Resources required, execution time, necessary skills |
| **Complexity** | Number of steps, need for specific tools, specialized knowledge |

### Matriks Prioritas

| | High Probability | Medium Probability | Low Probability |
|---|---|---|---|
| **High Impact** | Priority 1 | Priority 2 | Priority 3 |
| **Medium Impact** | Priority 2 | Priority 3 | Priority 4 |
| **Low Impact** | Priority 3 | Priority 4 | Priority 5 |

## WAF Evasion Maturity Model

| Level | Karakteristik |
|-------|---------------|
| **1: Beginner** | Random payloads, no understanding of WAF logic, unpredictable results |
| **2: Repeatable** | Basic methodology defined, logical use of techniques, documentation begins |
| **3: Defined** | Formal methodology documented, standard operational procedures, quality metrics |
| **4: Managed** | Methodology continuously measured, process improvement cycles, payload quality tracking |
| **5: Optimizing** | WAF behavior prediction capabilities, automated methodology refinement, continuous innovation |

## Key Diagnostic Questions

1. **"What does the WAF block?"** — Petakan pola blocking secara sistematis
2. **"What does the WAF NOT inspect?"** — Parameter, header, content type apa yang dilewatkan?
3. **"What technology runs on the backend?"** — PHP vs ASP.NET vs Python vs Java — masing-masing menangani parameter duplikat dan encoding berbeda
4. **"Is there a parsing discrepancy I can exploit?"** — Apakah WAF dan backend menginterpretasi request secara berbeda?
5. **"Can I reach the origin directly?"** — Apakah ada side door yang tidak melewati WAF?
6. **"What's the WAF's inspection depth?"** — Apakah WAF memeriksa full request atau hanya beberapa KB pertama?
7. **"What content types are not inspected?"** — Content type mana yang WAF skip?
8. **"Can I combine multiple techniques?"** — Dua teknik independen lebih efektif daripada satu

## Best Practices

- Gunakan formula prioritas untuk memilih teknik — jangan coba semua
- Target Priority 1 (High Impact + High Probability) terlebih dahulu
- Dokumentasikan hasil setiap teknik untuk memperbaiki probability estimation
- Tingkatkan maturity level dengan formalizing methodology dan continuous improvement
