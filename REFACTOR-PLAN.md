# Refactoring Plan — 11 Monolithic Skills

## Overview

Refactor 11 oversized SKILL.md files (>500 lines) into progressive disclosure structure:
- SKILL.md <500 lines (core instructions + gotchas + progressive disclosure table)
- `references/` — detailed reference docs (YAML frontmatter required)
- `assets/` — templates, checklists, reusable resources
- `scripts/` — executable exploit/hunting templates

Total: **12,578 lines → target ~4,400 lines** (~65% reduction).

---

## What Stays vs Moves

| Component | Stay in SKILL.md | Move to references/ | Move to assets/ | Move to scripts/ |
|-----------|-----------------|--------------------|-----------------|------------------|
| YAML frontmatter | ✅ | ❌ | ❌ | ❌ |
| Overview (1-2 paragraf) | ✅ | ❌ | ❌ | ❌ |
| Progressive disclosure table | ✅ (wajib) | ❌ | ❌ | ❌ |
| Gotchas | ✅ (wajib) | ❌ | ❌ | ❌ |
| Exam strategy checklist | ✅ (ringkas) | ❌ | Full checklist | ❌ |
| Quick reference commands | ✅ | ❌ | ❌ | ❌ |
| Module deep-dives | ❌ | ✅ | ❌ | ❌ |
| Tool references | ❌ | ✅ | ❌ | ❌ |
| Technique guides | ❌ | ✅ | ❌ | ❌ |
| Case studies | ❌ | ✅ | ❌ | ❌ |
| Report templates | ❌ | ❌ | ✅ | ❌ |
| Communication templates | ❌ | ❌ | ✅ | ❌ |
| Reusable checklists | ❌ | ❌ | ✅ | ❌ |
| Python exploit scripts | ❌ | ❌ | ❌ | ✅ |
| YARA rules | ❌ | ❌ | ❌ | ✅ |
| Config files (OSQuery, etc.) | ❌ | ❌ | ❌ | ✅ |
| SPL/KQL query collections | ❌ | ✅ (docs) | ❌ | ✅ (executable) |

---

## Cross-Skill Deduplication Notes

| Content | Skills that share it | Decision |
|---------|--------------------|----------|
| Splunk SPL reference | offsec-th-200, offsec-ir-200 | **Keep separate** — different use cases (hunting vs IR). Both reference files stay in their respective skill dirs. |
| CTI integration | offsec-th-200, threat-intelligence | **Keep separate** — offsec-th-200 treats CTI as hunting input; threat-intelligence covers full CTI lifecycle. |
| IR lifecycle | offsec-ir-200, ec-ecih, comptia-cysa | **Keep separate** — each uses different standards (NIST 800-61r2 vs ECIH 9-stage vs CySA+ domain). |
| MITRE ATT&CK | offsec-soc-200, offsec-th-200, mitre-attack skill | **Keep separate** — each applies ATT&CK differently (detection mapping vs hunting hypothesis vs general reference). |

---

## Quality Gates (per skill)

Setelah refactor, **semua** checklist ini harus terpenuhi:

- [ ] **Gate 1: SKILL.md <500 lines** — `wc -l < skills/<name>/SKILL.md`
- [ ] **Gate 2: YAML frontmatter valid** — minimal `name` + `description` ada
- [ ] **Gate 3: Progressive disclosure table** — tabel "When you need to... → Load this file" wajib
- [ ] **Gate 4: Gotchas section** — minimal 3 concrete gotchas
- [ ] **Gate 5: Reference YAML frontmatter** — semua file di references/ punya `name`, `description`, `tags`
- [ ] **Gate 6: No broken links** — semua internal link diverifikasi
- [ ] **Gate 7: sync-skills.js passes** — `node scripts/sync-skills.js` tanpa error
- [ ] **Gate 8: index.json updated** — file-file baru muncul di index.json

---

## Workflow Per Skill

1. **Read** — Baca full SKILL.md, mapping boundaries
2. **Create reference files** — Buat file di `references/` sesuai breakdown
3. **Create assets** — Pindahkan templates/checklists ke `assets/`
4. **Create scripts** — Pindahkan executable code ke `scripts/`
5. **Compress SKILL.md** — Sisakan frontmatter + overview + progressive disclosure table + gotchas
6. **Verify** — Jalankan quality gates
7. **Sync** — `node scripts/sync-skills.js`
8. **Update README.md** — Ubah status icon 📦 → 🔶
9. **Update REFACTOR-PLAN.md** — Checklist item
10. **Test** — Jalankan skill terhadap task nyata, pastikan agent bisa navigasi
11. **Commit** — `refactor: split <skill-name> into progressive disclosure structure`

---

## Estimated Effort

| Tier | Skills | Est. time per skill | Total |
|------|--------|--------------------|-------|
| 🥇 Large (1,200-1,700 lines) | 5 | ~60 min | ~5 jam |
| 🥈 Medium (700-1,000 lines) | 4 | ~45 min | ~3 jam |
| 🥉 Small (500-700 lines) | 2 | ~30 min | ~1 jam |
| **Total** | **11** | | **~9 jam** |

---

## Priority 1 — Large Certification Skills (5.5K+ lines, ~60 min each)

### 1. offsec-th-200 (1,709 lines) — OSTH

**Current structure:**
- Overview & Exam Structure (lines 32-130)
- Threat Hunting Mindset & Framework (lines 131-283)
- 8 Module Deep-Dive (lines 284-613) — **largest section**
- Splunk SPL Hunting Queries Reference (lines 614-895)
- CrowdStrike Falcon & CQL Reference (lines 896-1037)
- Network Hunting: Suricata, Zeek & PCAP Analysis (lines 1038-1137)
- Endpoint Hunting: Sysmon & Windows Event Logs (lines 1138-1235)
- Threat Intelligence Integration (lines 1236-1315)
- Ransomware & APT Case Studies (lines 1316-1394)
- Exam Strategy & Report Template (lines 1395-1493)
- Referensi Lengkap (lines 1494-1709)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/th-mindset.md` | Threat hunting mindset, PEAK, SEARCH methodologies, hypothesis framework |
| `references/splunk-hunting.md` | Splunk SPL hunting queries, detection logic, pivots |
| `references/crowdstrike-cql.md` | CrowdStrike Falcon CQL reference, endpoint hunting patterns |
| `references/network-hunting.md` | Suricata, Zeek, PCAP analysis, network IOCs |
| `references/endpoint-hunting.md` | Sysmon, Windows Event Logs, endpoint artifacts |
| `references/ti-integration.md` | CTI integration, intelligence-driven hunting |
| `references/case-studies.md` | Ransomware & APT case studies, TTP mapping |

**Assets:** `assets/report-template.md`
**Scripts:** `scripts/spl-queries.spl`

---

### 2. lf-cks (1,574 lines) — CKS

**Current structure:**
- Kubernetes Security Mindset (lines 36-115)
- Exam Overview & Strategy (lines 116-200)
- Trust Boundaries & Attack Surface (lines 201-340)
- Cluster Isolation Model (lines 341-405)
- Authentication & Authorization Framework (lines 406-503)
- Workload Security Posture (lines 504-641)
- Data Security at Rest & In Transit (lines 642-733)
- Supply Chain Trust Model (lines 734-851)
- Runtime Defense Framework (lines 852-965)
- Compliance & Hardening Posture (lines 966-1047)
- Network Security Architecture (lines 1048-1151)
- Incident Response untuk Kubernetes (lines 1152-1236)
- Decision Framework & Trade-offs (lines 1237-1324)
- Study Strategy & Mindset (lines 1325-1407)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/auth-authz.md` | RBAC, ServiceAccount, OIDC, Node authorization |
| `references/workload-security.md` | Pod Security Standards, PSA, OPA/Gatekeeper, seccomp, AppArmor |
| `references/supply-chain.md` | Image signing, Cosign, admission controller, SBOM |
| `references/runtime-defense.md` | Falco, audit logging, runtime security |
| `references/network-security.md` | NetworkPolicy, Cilium, encryption in transit, mTLS |
| `references/data-security.md` | Encryption at rest, KMS, Secret management, etcd encryption |
| `references/cluster-isolation.md` | Namespace isolation, multi-tenancy, resource quotas |
| `references/compliance-hardening.md` | CIS Benchmark, hardening guidelines, compliance frameworks |

**Special:** Decision framework (section 13) stays in SKILL.md as gotchas/pocket reference.

---

### 3. offsec-ir-200 (1,325 lines) — OSIR

**Current structure:**
- Overview & Exam Structure (lines 28-117)
- IR Mindset & Incident Responder Framework (lines 118-199)
- 13 Module Deep-Dive (lines 200-647)
- Splunk SIEM & SPL Reference (lines 648-820)
- Digital Forensics Reference (lines 821-1003)
- Containment, Eradication, Recovery & Reporting (lines 1004-1133)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/ir-lifecycle.md` | IR lifecycle (NIST 800-61r2), CSIRT structure, severity classification |
| `references/modules-overview.md` | 13 module case studies |
| `references/splunk-siem.md` | Splunk SPL queries for IR, log sources, detection patterns |
| `references/digital-forensics.md` | Autopsy, FTK Imager, Volatility 3, forensic artifact collection |
| `references/containment-eradication-recovery.md` | Containment strategies, eradication, recovery planning |
| `references/malware-triage.md` | YARA rules, PE analysis, malware classification |
| `references/reporting.md` | Post-mortem reporting, communication plans, templates |

**Assets:** `assets/communication-template.md`
**Scripts:** `scripts/yara-rules.yara`

---

### 4. offsec-pen-300 (1,253 lines) — OSEP

**Current structure:**
- Overview & Exam Structure (lines 28-94)
- OSEP Mindset (lines 95-140)
- 16 Module Deep-Dive (lines 141-721) — **largest section**
- Evasion Techniques Deep-Dive (lines 722-839)
- C2 Framework Strategy (lines 840-917)
- Challenge Labs & Exam Strategy (lines 918-1066)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/modules-overview.md` | 16 module case studies |
| `references/av-edr-evasion.md` | AV/EDR evasion, AMSI bypass, AppLocker, CLM |
| `references/process-injection.md` | Process injection, hollowing, reflective DLL, APC |
| `references/shellcode-runners.md` | C# shellcode runners, payload encryption, sandbox evasion |
| `references/mssql-attacks.md` | MSSQL linked servers, relay attacks, command execution |
| `references/ad-exploitation.md` | AD delegation attacks, trusts, ADCS, forest trusts |
| `references/c2-strategy.md` | Metasploit, Sliver, Mythic, traffic shaping |

**Assets:** `assets/shellcode-runner.cs`, `assets/exam-checklist.md`
**Scripts:** Exploit development helper scripts

---

### 5. offsec-soc-200 (1,227 lines) — OSDA

**Current structure:**
- Overview & Exam Structure (lines 28-106)
- SOC-200 Mindset & SOC Analyst Framework (lines 107-164)
- 19 Module Deep-Dive (lines 165-577)
- Windows Event Log & Sysmon Reference (lines 578-717)
- SIEM: ELK Stack, KQL & OSQuery (lines 718-881)
- Challenge Labs & Exam Strategy (lines 882-1041)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/soc-framework.md` | SOC analyst framework, Kill Chain, ATT&CK mapping |
| `references/modules-overview.md` | 19 module case studies |
| `references/windows-event-logs.md` | Event IDs, Sysmon, process creation, network events |
| `references/elk-kql.md` | ELK Stack, Kibana Query Language, OSQuery reference |
| `references/linux-endpoint.md` | Linux auditd, auth.log, syslog analysis |
| `references/ad-detection.md` | AD threat detection, Kerberos attacks, Golden Ticket |

**Assets:** `assets/kql-templates.md`
**Scripts:** `scripts/osquery.conf`

---

## Priority 2 — Medium Certification Skills (2.6K+ lines, ~45 min each)

### 6. oscp-methodology (990 lines)

**Current structure:**
- Filosofi OSCP (lines 35-63)
- OSCP+ Exam Architecture (lines 64-103)
- 3 Attack Vectors methodology (lines 104-156)
- Recon & Enumeration Framework (lines 157-201)
- Web Application Attacks (lines 202-256)
- Buffer Overflow Methodology (lines 257-286)
- Linux PE (lines 287-382)
- Windows PE (lines 383-460)
- AD — Full Attack Chain (lines 461-567)
- Pivoting & Lateral Movement (lines 568-638)
- Reporting (lines 639-676)
- Exam Strategy (lines 677-717)
- Password Cracking (lines 718-760)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/enumeration-framework.md` | Port scanning, service enumeration, version detection, searchsploit |
| `references/web-attacks.md` | SQLi, XSS, LFI/RFI, file upload, shenanigans |
| `references/buffer-overflow.md` | BoF methodology for OSCP (x86) |
| `references/linux-pe.md` | Linux PE methodology, SUID, cron, kernel exploits |
| `references/windows-pe.md` | Windows PE methodology, service misconfigs, kernel |
| `references/ad-attack-chain.md` | AD full chain: enum → kerberoast → AS-REP → DCSync → ACL |
| `references/pivoting.md` | SSH tunneling, chisel, ligolo, port forwarding |
| `references/password-cracking.md` | Hashcat rules, wordlists, rule-based attacks |

**Assets:** `assets/report-template.md`, `assets/exam-checklist.md`
**Special:** Golden rules tetap di SKILL.md gotchas.

---

### 7. cpent (878 lines)

**Current structure:**
- Overview & Exam Structure (lines 28-99)
- CPENT Mindset (lines 100-128)
- 14 Modul Inti (lines 129-532)
- Exam Zone Deep-Dives (lines 533-603)
- Tools Matrix (lines 604-655)
- Report Writing (lines 656-746)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/binary-exploitation.md` | 32/64-bit BoF, ROP, shellcode development |
| `references/iot-ot-scada.md` | IoT/OT/SCADA pentesting, protocols, access methods |
| `references/pivoting-double.md` | Single & double pivoting, proxychains, sshuttle |
| `references/exam-zones.md` | Exam zone deep-dives, scoring strategy |
| `references/tools-matrix.md` | CPENT tools categorized by phase |
| `references/report-writing.md` | Report structure, finding documentation, LPT Master requirements |

**Assets:** `assets/report-template.md`

---

### 8. ptes-standard (785 lines)

**Current structure:**
- 7 phases overview + detailed per phase (lines 23-247)
- Response Style (lines 248-263)
- Phase Deep-Dives (lines 264-401)
- Tool-by-Phase Matrix (lines 402-439)
- Standards Comparison (lines 440-464)
- Modern Infrastructure Adaptations (lines 465-514)
- Legal & Compliance Notes (lines 515-558)
- Reporting Templates (lines 559-633)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/phase1-pre-engagement.md` | Scoping, ROE, legal agreements |
| `references/phase2-intelligence.md` | OSINT, passive/active recon |
| `references/phase3-threat-modeling.md` | Threat modeling methodologies |
| `references/phase4-vuln-analysis.md` | Automated + manual vuln discovery |
| `references/phase5-exploitation.md` | Exploitation methodologies |
| `references/phase6-post-exploitation.md` | Persistence, pivoting, exfil |
| `references/phase7-reporting.md` | Reporting standards, risk ratings |
| `references/modern-infra.md` | Cloud, container, API pentesting adaptations |
| `references/legal-compliance.md` | Legal notes, compliance requirements |

**Assets:** `assets/reporting-templates.md`

---

### 9. threat-intelligence (672 lines)

**Current structure:**
- CTI Fundamentals & Lifecycle (lines 25-67)
- Analytic Frameworks (lines 68-145)
- IOC Management & Standards (lines 146-247)
- Threat Hunting (lines 248-355)
- Platforms & Tools (lines 356-411)
- Sharing & Communities (lines 412-452)
- Analyst Tradecraft & Reporting (lines 453-527)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/cti-lifecycle.md` | 6-phase intelligence cycle, PIRs, intelligence levels |
| `references/analytic-frameworks.md` | Kill Chain, Diamond Model, ATT&CK, structured analysis |
| `references/ioc-management.md` | STIX/TAXII, MISP, YARA, Sigma, TLP, confidence scoring |
| `references/threat-hunting.md` | PEAK, ABLE, HMM methodologies, hypothesis development |
| `references/platforms-tools.md` | TIP comparison, OpenCTI, MISP deployment, integrations |
| `references/tradecraft-reporting.md` | Intel report writing, source validation, briefing skills |

**Note:** CTI is documentation-heavy, template-light — no assets needed.

---

## Priority 3 — Smaller but Oversized (1.1K+ lines, ~30 min each)

### 10. comptia-cysa (640 lines)

**Current structure:**
- Domain 1: Security Operations (34%) (lines 35-265)
- Domain 2: Vulnerability Management (26%) (lines 266-375)
- Domain 3: Incident Response and Management (24%) (lines 376-483)
- Domain 4: Reporting and Communication (16%) (lines 484-563)
- Key Tools Reference (lines 564-582)
- Key Frameworks Reference (lines 583-599)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/security-operations.md` | Domain 1 — logging, monitoring, SIEM, threat intel |
| `references/vulnerability-management.md` | Domain 2 — scanning, prioritization, remediation |
| `references/incident-response.md` | Domain 3 — IR lifecycle, forensic basics, chain of custody |
| `references/reporting-communication.md` | Domain 4 — metrics, reports, stakeholder communication |
| `references/tools-reference.md` | Tool catalog by category |
| `references/frameworks-reference.md` | NIST, ISO, ATT&CK mappings |

**Special:** Exam tips tetap di SKILL.md gotchas.

---

### 11. waf-evasion-methodology (525 lines)

**Current structure:**
- Fundamental Mindset (lines 14-41)
- 6-Phase Analysis Cycle (lines 42-135)
- Evasion Strategies — 4 Lapisan (lines 136-190)
- Teknik Evasion (lines 191-330)
- Aturan Koordinasi Multi-Teknik (lines 331-346)
- Teknik Evaluation Framework (lines 347-371)
- WAF Evasion Maturity Model (lines 372-383)
- Memahami WAF (lines 384-409)
- Parsing Discrepancies (lines 410-428)
- Checklist Sistematis (lines 429-487)

**Proposed reference files:**
| File | Content |
|------|---------|
| `references/evasion-techniques.md` | All evasion techniques with payload examples |
| `references/parsing-discrepancies.md` | WAFFLED research, normalization gaps, encoding tricks |
| `references/analysis-cycle.md` | 6-phase WAF analysis cycle, fingerprinting methodology |
| `references/evaluation-framework.md` | Technique evaluation, maturity model |

**Assets:** `assets/checklist.md`

---

## Quality Gates Checklist (global)

- [ ] **01 — offsec-th-200** → all 8 gates pass, README updated, committed
- [ ] **02 — lf-cks** → all 8 gates pass, README updated, committed
- [x] **03 — offsec-ir-200** → all 8 gates pass, README updated, committed
- [ ] **04 — offsec-pen-300** → all 8 gates pass, README updated, committed
- [x] **05 — offsec-soc-200** → all 8 gates pass, README updated, committed
- [ ] **06 — oscp-methodology** → all 8 gates pass, README updated, committed
- [ ] **07 — cpent** → all 8 gates pass, README updated, committed
- [ ] **08 — ptes-standard** → all 8 gates pass, README updated, committed
- [ ] **09 — threat-intelligence** → all 8 gates pass, README updated, committed
- [ ] **10 — comptia-cysa** → all 8 gates pass, README updated, committed
- [ ] **11 — waf-evasion-methodology** → all 8 gates pass, README updated, committed
- [ ] **Final** — `node scripts/sync-skills.js` full run, repo-wide verify

**Total reference files to create:** ~73
**Total assets to create:** ~14
**Total scripts to create:** ~5

---

## Reference File Template

```markdown
---
name: "Human-Readable Title"
description: "One-line summary."
tags: [tag1, tag2, tag3]
---

# Title

## Overview

[Key concepts, when to use this reference]

## Content

[Focused, detailed content on one domain]

## Gotchas

[Environment-specific facts that defy assumptions]

## Best Practices

[Actionable recommendations]
```

## SKILL.md Template (post-refactor)

```markdown
---
name: skill-name
description: "..."
license: MIT
compatibility: opencode
metadata:
  audience: ...
  workflow: ...
  source: ...
  standard: ...
  year: "2026"
---

# Title — Brief Overview

[1-2 paragraph overview]

## How to Use This Skill

| When you need to... | Load this file |
|---------------------|----------------|
| ... | `references/...` |
| ... | `references/...` |
| Use a template | `assets/...` |
| Run a script | `scripts/...` |

## Gotchas

- Concrete correction 1
- Concrete correction 2
- Concrete correction 3

## Quick Reference

[Key commands, patterns, or decision trees — keep under 20 lines]
```
