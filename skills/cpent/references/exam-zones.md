---
name: "CPENT Exam Zones — Standalone, Complex & IoT"
description: "CPENT exam zone deep-dives covering Zone 1 (standalone machines), Zone 2 (single pivot complex network), Zone 3 (double pivot deep network), Zone 4 (IoT/Industrial/SCADA), with zone-specific strategies and exam day checklist."
tags: [cpent, exam-zones, standalone, pivoting, iot, checklist]
---

# CPENT Exam Zones

## Zone 1: Standalone Machines

2-3 machines, masing-masing perlu initial access + privesc.

**Strategi:**
- Parallel enumeration di 30 menit pertama
- Prioritaskan machine dengan port paling sedikit
- Jangan habiskan >2 jam per machine

## Zone 2: Complex Network (Single Pivot)

Satu network dengan entry point → shell → pivot ke internal subnet.

**Key Insight:**
- Entry point biasanya mudah (known vulnerability)
- Internal subnet punya service tidak exposed ke internet
- Enumeration dari dalam adalah kunci

## Zone 3: Double Pivot

Dua lapis jaringan. Target ada di subnet yang hanya reachable setelah 2 hop.

**Mindset:** Pivot 1 → subnet A → host dual-home → Pivot 2 → subnet B → target.

## Zone 4: IoT/Industrial

IoT devices + SCADA/PLC targets.

**Mindset:**
- IoT via web interface
- SCADA/PLC via protocol-specific exploitation
- Industrial protocols di port non-standard

## Exam Day Checklist

- [ ] VPN connected — verify tun0 interface
- [ ] Parallel Nmap (all ports) on all targets
- [ ] Start web app scanning (Burp, ffuf, Nikto, sqlmap)
- [ ] Note start time, expected end time
- [ ] Breaks every 3-4 hours (eat, drink, walk)
- [ ] All screenshots organized per target
- [ ] Flags listed: IP, hostname, local.txt, proof.txt

## Best Practices

- Prioritaskan Zone 1 untuk quick wins
- Zone 3 dan 4 adalah pembeda dari sertifikasi lain
- Dokumentasi paralel dengan eksekusi
