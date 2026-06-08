---
name: "OSCP+ Exam Strategy — Time Management & Reporting"
description: "Exam strategy for OSCP+ including 23h45m operating plan, golden strategy rules, exam day checklist, reporting philosophy, report structure, and screenshot requirements."
tags: [oscp, exam-strategy, time-management, reporting, checklist]
---

# OSCP+ Exam Strategy & Reporting

## 23h45m Operating Plan

| Time | Activity |
|------|----------|
| 00:00 - 00:30 | Parallel scans on ALL machines (nmap -p- on all IPs) |
| 00:30 - 03:30 | Attack AD set (highest ROI — 40 pts) |
| 03:30 - 08:00 | Continue AD + start standalone machines |
| 08:00 - 12:00 | Push hard on highest-confidence standalone |
| 12:00 - 16:00 | Pivot, privesc, second-order enumeration |
| 16:00 - 20:00 | Convert partials into proofs |
| 20:00 - 22:30 | Final exploitation attempts |
| 22:30 - 23:45 | Verify flags, screenshots, notes, report outline |
| 23:45+ | REPORT WRITING (24h window) |

## Golden Strategy Rules

1. AD set first — 40 pts adalah blok terbesar
2. Enumerate ALL machines in parallel
3. The 30-minute rule: stuck → move on, coba lain
4. Strategic retreat beats stubbornness
5. Screenshot as you go — jangan menumpuk di akhir
6. One folder per target

## Reporting Philosophy

Report yang buruk adalah penyebab kegagalan OSCP yang paling underrated.

**Golden Rules:**
- Reproducibility: setiap langkah harus bisa direproduksi
- Screenshot di setiap langkah kritis
- Format: IP + flag di terminal interaktif (bukan web browser)
- Sertakan URL exploit original + perubahan yang dibuat

**Report Structure:**
1. Executive Summary (150-200 words)
2. Methodology Overview
3. Detailed Findings per target
4. Appendices: shellcode, code listings

**Naming:** `OSCP-OS-XXXXX-Exam-Report.pdf` → `.7z` (max 200MB, NO password)

## Exam Day Checklist

- [ ] VPN connected, tun0 up
- [ ] Burp Suite running
- [ ] Note-taking app open
- [ ] Terminal logging active (`script` command)
- [ ] Exam control panel open
- [ ] Screenshots folder organized per target
- [ ] Known good shells pre-generated
- [ ] Clock started — note exam end time
- [ ] Food, water, snacks ready

## Best Practices

- Sleep strategis: 24 jam itu panjang, tidur 1-2 jam
- Jangan menumpuk screenshot di akhir — lupa, kelelahan
- Report templates: whoisflynn (Word), noraj (Markdown)
