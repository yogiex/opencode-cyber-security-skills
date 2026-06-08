# Refactoring Milestones

## Legend

```
[ ] Pending    [/] In Progress    [X] Completed
```

---

## Milestone 1 — Big Three: OffSec Defensive Stack

> OSDA + OSIR + OSTH. Tiga sertifikasi defensive OffSec yang saling terkait (SOC analysis → Incident Response → Threat Hunting). Refactor berturut-turut karena banyak konsep overlap (Splunk SPL, Windows Event Logs, MITRE ATT&CK).

| # | Skill | Lines | Est. | Status |
|---|-------|-------|------|--------|
| 1 | offsec-soc-200 (OSDA) | 1,227 → 106 | ~60m | [x] |
| 2 | offsec-ir-200 (OSIR) | 1,325 | ~60m | [ ] |
| 3 | offsec-th-200 (OSTH) | 1,709 | ~60m | [ ] |

**Total:** 4,261 lines → target ~1,200 lines  
**Est. time:** ~3 jam  

---

## Milestone 2 — Offensive Exploitation

> OSEP + OSCP. Advanced evasion + foundational pentesting. OSEP adalah natural next-step dari OSCP.

| # | Skill | Lines | Est. | Status |
|---|-------|-------|------|--------|
| 4 | offsec-pen-300 (OSEP) | 1,253 | ~60m | [x] |
| 5 | oscp-methodology | 990 | ~45m | [x] |

**Total:** 2,243 lines → target ~800 lines  
**Est. time:** ~1 jam 45m  

---

## Milestone 3 — Infrastructure & Container Security

> CKS + CPENT. Kubernetes security + advanced pentesting (binary exploitation, IoT/OT, double pivoting). Domain berbeda tapi sama-sama infrastruktur-heavy.

| # | Skill | Lines | Est. | Status |
|---|-------|-------|------|--------|
| 6 | lf-cks (CKS) | 1,574 | ~60m | [ ] |
| 7 | cpent | 878 | ~45m | [ ] |

**Total:** 2,452 lines → target ~800 lines  
**Est. time:** ~1 jam 45m  

---

## Milestone 4 — Standards & Methodologies

> PTES + CySA+ + TI + WAF. Framework dan pengetahuan umum yang tidak terikat satu vendor sertifikasi.

| # | Skill | Lines | Est. | Status |
|---|-------|-------|------|--------|
| 8 | ptes-standard | 785 | ~45m | [ ] |
| 9 | comptia-cysa | 640 | ~30m | [ ] |
| 10 | threat-intelligence | 672 | ~30m | [ ] |
| 11 | waf-evasion-methodology | 525 | ~30m | [ ] |

**Total:** 2,622 lines → target ~1,200 lines  
**Est. time:** ~2 jam 15m  

---

## Progress Summary

| Milestone | Skills | Lines Now | Target Lines | Est. Time | Status |
|-----------|--------|-----------|--------------|-----------|--------|
| M1: Defensive Stack | 3 | 4,261 | ~1,200 | ~3h | [ ] |
| M2: Offensive | 2 | 2,243 | ~800 | ~1h 45m | [ ] |
| M3: Infra/Container | 2 | 2,452 | ~800 | ~1h 45m | [ ] |
| M4: Standards | 4 | 2,622 | ~1,200 | ~2h 15m | [ ] |
| **Total** | **11** | **11,578** | **~4,000** | **~9h** | |

## Definition of Done per Milestone

- [ ] Semua skill di milestone已完成 refactor (memenuhi 8 quality gates)
- [ ] README.md status icons updated (📦 → 🔶)
- [ ] REFACTOR-PLAN.md checklist diupdate
- [ ] `node scripts/sync-skills.js` passes
- [ ] All changes committed dengan prefix `refactor:`
