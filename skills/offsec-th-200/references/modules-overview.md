---
name: "8 Module Deep-Dive"
description: "Complete breakdown of TH-200 modules including threat hunting concepts, threat actor landscape, network/endpoint hunting methodologies, and Azure threat hunting."
tags: [modules, threat-actor, ransomware, apt, network-hunting, endpoint-hunting, azure]
---

# 8 Module Deep-Dive

## Modul 1: Threat Hunting Concepts and Practices

**Core Concepts:** Threat hunting definition (proactive search for threats evading existing controls), hunter mindset (curiosity, creativity, analytical rigor), hunt types (intel-based, hypothesis-driven, baselining).

**Maturity Model:** Level 1 Initial (ad-hoc) → Level 2 Defined (structured) → Level 3 Managed (metrics-driven) → Level 4 Optimizing (AI-assisted).

**Hunt Lifecycle:** Trigger → Hypothesis → Data Collection → Analysis → Findings → Response → Feedback

## Modul 2: Threat Actor Landscape Overview

| Type | Motivation | Examples |
|------|------------|----------|
| **Nation-State (APTs)** | Espionage, sabotage | APT29, APT41, Lazarus |
| **Cybercrime / eCrime** | Financial gain | LockBit, CLOP, BlackCat |
| **Hacktivists** | Ideological | Anonymous, Killnet |
| **Insider Threats** | Financial, revenge | Disgruntled employees |

**Ransomware Ecosystem:** Initial Access Brokers → Ransomware Group → Affiliates (data exfiltration, negotiation, leak site operators)

**LockBit 3.0:** RaaS, initial access via RDP brute force/phishing/VPN vulns, AES+RSA encryption, StealBit exfiltration tool, PsExec lateral movement.

**CLOP:** Known for MOVEit Transfer exploitation (2023), web shell deployment, data exfiltration via HTTP.

**BlackCat/ALPHV:** First Rust-based ransomware, RaaS model, VPN/phishing initial access, multi-threaded encryption.

**APT Groups:** APT29 (Russia/SVR, PowerShell + cloud C2), APT41 (China, DLL side-loading), Lazarus (North Korea, macOS malware), MuddyWater (Iran, VBS + LoTL), FIN7 (Russia, Carbanak backdoor).

## Modul 3: Communication and Reporting for Threat Hunters

**Traffic Light Protocol (TLP):** RED (individual only), AMBER (organization), GREEN (community), CLEAR (public).

**Intel Report Types:** Strategic (executive), Operational (campaign-focused), Tactical (IoCs/TTPs), Technical (raw data).

**Hunt Narrative Structure:** Executive Summary → Hypothesis & Methodology → Data Sources → Findings → Impact Assessment → IOCs Table → Recommendations → MITRE ATT&CK Mapping.

**Communication:** Management (business impact), SOC (technical details), IT (systems/patches), Legal (regulatory).

## Modul 4: Hunting with Network Data

**Data Sources:** NetFlow/IPFIX, DNS logs, proxy logs, IDS/IPS (Suricata), firewall logs, PCAP, NetWitness.

**Suricata IDS/IPS:** Open-source, rule-based detection, protocol detection (HTTP, DNS, TLS, SMB), file extraction from network streams.

**Zeek (formerly Bro):** conn.log, dns.log, http.log, ssl.log, files.log.

**Key Hunting Scenarios:** C2 detection (beaconing frequency analysis), DNS tunneling (long domain queries), data exfiltration (large outbound transfers via HTTP), Suricata alert triage.

## Modul 5: Hunting on Endpoints

**Data Sources:** Sysmon (process, network, file, registry), Windows Event Log (4624, 4625, 4688, 4104, 7045), CrowdStrike Falcon (process tree, command line).

**Intel-Based Hunting:** Search specific IOCs (hash, IP, domain, registry key) across endpoint logs.

**Hypothesis-Driven Hunting:** Suspicious parent-child (Office spawning PowerShell), lateral movement (logon type 3), persistence (non-Microsoft service creation).

## Modul 6: Threat Hunting without IoCs

**Behavioral Analysis:** Focus on behavior not indicators. Deviations from normal baselines. Identify TTPs.

**CrowdStrike Falcon Behavioral Hunts:** Unusual parent-child, suspicious execution paths (`AppData\Local\Temp`), beaconing detection.

**Hypothesis without IoCs:** "If attacker compromised DC, they would: create domain admin (4720+4728), DCSync (4662), dump NTDS.dit → hunt for these behaviors."

## Modul 7: Threat Hunting Challenge Labs

Full-scale hunt simulation mirroring exam format. Realistic enterprise network with pre-recorded attacker actions. Splunk + CrowdStrike + threat intel report.

**Strategy:** Treat like exam, document everything, build hunt narrative in real-time, time-box to 8h, write full report after each attempt.

## Modul 8: Threat Hunting in Azure (New Module)

**Azure Data Sources:** Azure AD sign-in logs, Activity logs, Security Center alerts, Microsoft 365 Defender.

**KQL for Azure:** `SigninLogs | where ResultType != "0" | summarize FailedCount = count() by UserPrincipalName, IPAddress | where FailedCount > 10`

**Cloud-Specific TTPs:** T1078.004 (Cloud Account), T1525 (Implant Internal Image), T1613 (Container Discovery), T1530 (Cloud Storage Data).

## Gotchas

- Modul 8 (Azure) adalah tambahan baru — pastikan sudah dipelajari sebelum exam karena bisa muncul di soal
- Challenge Lab harus dikerjakan berkali-kali sampai bisa complete all 7 questions dalam waktu <6 jam
- Threat actor landscape (Modul 2) sering muncul di soal yang membutuhkan attribution
- Ransomware ecosystem knowledge diperlukan untuk memahami full attack chain

## Best Practices

- Pelajari modul secara berurutan karena setiap modul membangun konsep dari modul sebelumnya
- Buat mind map untuk setiap threat actor group (TTPs, tools, targets)
- Praktikkan hypothesis development — buat 3 hipotesis berbeda untuk setiap skenario
