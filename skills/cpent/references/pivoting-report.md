---
name: "Double Pivoting & Report Writing"
description: "Double pivoting methodology for CPENT covering two-layer network penetration, Ligolo-ng, Chisel, and report writing following EC-Council format with executive summary, network diagram, detailed findings, CVSS scoring, and appendix organization."
tags: [pivoting, report-writing, double-pivot, network-diagram, cvss]
---

# Double Pivoting & Report Writing

## Double Pivoting Methodology

Dua lapis jaringan:
```
Attacker → Pivot 1 (gateway) → Subnet A → Host dual-home → Subnet B → Target
```

**Key Insight:**
- Pivot 1 adalah gateway ke subnet A
- Dari subnet A, cari host dual-home (2 network interfaces)
- Host dual-home menjadi Pivot 2 ke subnet B
- Target ada di subnet B — hanya reachable setelah 2 hop

**Tools:**
- Ligolo-ng (TUN-based, recommended)
- Chisel (HTTP tunnel)
- SSH tunneling (local/remote/dynamic)

**Mindset:**
- Setiap shell baru → langsung cek interfaces (`ip addr`, `ifconfig`)
- Selalu ada subnet lain di belakangnya
- Double pivot adalah core skill CPENT

## Report Writing (~30% Nilai)

**EC-Council Format:**
1. Cover Page: Exam ID, name, date
2. Non-Disclosure Agreement
3. Executive Summary (1 page)
4. Methodology (1-2 pages)
5. Network Diagram (attack chain visual)
6. Detailed Findings per target (step-by-step + screenshots)
7. Appendices

**Screenshot Requirements:**
- Shell access: `whoami`, `id`, `hostname`, `ipconfig` — satu screenshot
- Proof files: `type local.txt` / `cat proof.txt`
- Network path: ifconfig sebelum dan sesudah pivoting
- Timestamps: konteks waktu harus visible

**Quality Checklist:**
- Setiap finding memiliki CVSS score
- Setiap langkah reproducible
- Remediation actionable
- PDF test open sebelum submit
- Submit sebelum deadline 7 hari

## Best Practices

- Dokumentasi selama exam — jangan menumpuk di akhir
- Network diagram harus menunjukkan attack path jelas
- Screenshots harus capture IP + hostname + flag
- Report adalah 30% — jangan disepelekan
