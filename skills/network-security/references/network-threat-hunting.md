---
name: "Network Threat Hunting"
description: "Hypothesis-driven network threat hunting across flow, DNS, TLS, proxy, and Zeek data: beaconing, lateral movement, and C2 detection (JA3/JA4, domain age, periodicity), PEAK/SEARCH methodologies, hunt narrative, and tradecraft."
tags: [threat-hunting, network-hunting, hypothesis-driven, peak, search, beaconing, lateral-movement, c2, ja3, ja4, zeek, flow, dns, proxy, tls, hunt-narrative, periodicity, domain-age]
---

# Network Threat Hunting

Network threat hunting is the proactive search for adversary activity that has not triggered an alert. It differs from monitoring: the hunter starts with a hypothesis and a defined data set, tests it, and either finds evidence of an intrusion or produces a measurable statement about coverage. This reference focuses on the network layer — flow, DNS, TLS, proxy, and Zeek — and on the tradecraft that turns those sources into a defensible hunt narrative.

## Hypothesis-Driven Hunting

A hunt begins with a testable hypothesis, not with a dashboard. The **ABLE** model (Actor, Behavior, Location, Evidence) keeps it concrete:

- **Actor**: who or what class of threat (e.g., "hands-on-keyboard operator", "commodity loader").
- **Behavior**: the specific TTP (e.g., "periodic HTTPS beacon to a recently registered domain").
- **Location**: where evidence would appear (e.g., "egress flow from finance workstations").
- **Evidence**: the data source and query pattern that would confirm or refute it.

Hypothesis format: `"Adversary [TTP] on [system/segment] using [technique] to achieve [goal]"`. A good hypothesis is falsifiable (a result can disprove it), answerable with available telemetry, and narrow enough to close in one sprint. Three hunt types are used in rotation:

| Type | Description | Best for |
|---|---|---|
| Intel-based | Sweep known IOCs/TTPs from a report | New intel, named actor |
| Hypothesis-driven | Test a TTP hypothesis | Assumed compromise, red-team emulation |
| Baseline/anomaly | Deviations from established norms | Unknown threats, new environments |

IOC-based sweeps have short shelf life; prefer TTP-based hypotheses, since techniques persist while IPs and hashes change within days.

## Data Sources

Each source answers a different question; combine them rather than relying on one.

| Source | What it gives | Hunting use |
|---|---|---|
| **Flow (NetFlow/IPFIX/sFlow)** | 5-tuple, bytes, packets, duration, timestamps | Beaconing, exfiltration, lateral movement, top talkers |
| **DNS logs** | Query name, type, response, client, resolver | DGA, tunneling, C2 domains, fast flux |
| **TLS metadata** | SNI, JA3/JA4, cert subject/issuer/validity, version/cipher | C2 fingerprints, rogue certs, ECH/DoH abuse |
| **Proxy/web logs** | URL, method, status, bytes, user-agent, referer | C2 over HTTP(S), data staging, domain age |
| **Zeek logs** | conn, dns, http, ssl, files, x509, notice | Structured pivot point; file extraction; RITA input |

**Zeek** is the natural join key: `uid` links `conn.log`, `ssl.log`, `dns.log`, and `http.log`, so a single suspicious flow can be pivoted across protocols. **Flow** is the scalable backbone for periodicity analysis but lacks content; **DNS** is the earliest and cheapest signal for C2; **proxy** adds application context (user-agent, bytes up/down); **TLS metadata** survives encryption and is essential for HTTPS C2.

## PEAK and SEARCH Methodologies

**PEAK** (Plan & Prepare → Execute → Analyze → Knowledge Sharing) is the full-cycle framework:

1. **Plan & Prepare**: develop the hypothesis, identify data sources, define success criteria and scope.
2. **Execute**: run queries, inspect results, refine the hypothesis as evidence arrives.
3. **Analyze**: correlate across sources, determine scope, build the timeline.
4. **Knowledge Sharing**: write the hunt report, update detection rules/playbooks, feed intel back.

PEAK is incomplete if phase K is skipped — a hunt that leaves no new detection or data source is half-finished.

**SEARCH** (Sense → Enrich → Analyze → Reconstruct → Communicate → Hone) is the in-flight checklist used to sharpen a hunt already underway:

- **Sense**: collect broad telemetry, spot anomalies.
- **Enrich**: add threat intel and context.
- **Analyze**: form and test hypotheses.
- **Reconstruct**: build the complete attack narrative.
- **Communicate**: deliver actionable findings.
- **Hone**: improve automated detections.

Use PEAK to structure the engagement and SEARCH to drive each day's work; they complement rather than compete. Track maturity with the **Hunting Maturity Model (HMM)**: 0 (alert-only) → 1 (IOC sweeps) → 2 (documented TTP playbooks) → 3 (novel hypotheses) → 4 (automated hypotheses + ML).

## Beaconing Detection

Beaconing is periodic C2 communication, often low-and-slow with jitter. Detection signals:

- **Inter-arrival time (IAT) analysis**: compute the coefficient of variation (CoV = std/mean) of IATs; low CoV (~<0.3) indicates periodicity. Attackers add 10–30% jitter to raise CoV, so combine with autocorrelation/FFT over sliding windows.
- **Byte-volume consistency**: similar orig/resp byte counts across sessions; small, fixed-size payloads.
- **Long-lived, low-and-slow connections**: repeated connections to a rare destination, off-hours activity.
- **Destination rarity**: new or infrequent destinations, recently registered domains, unusual ASNs.

Tools: **RITA** (Zeek-based scoring for beaconing, DNS tunneling, long connections), Zeek `conn.log` with custom Python/pandas analysis, and SIEM ML jobs. Require multiple independent signals before alerting.

```python
import pandas as pd
# flows: DataFrame with ts (epoch seconds), src, dst
flows = flows.sort_values("ts")
iat = flows["ts"].diff().dropna()
cov = iat.std() / iat.mean() if iat.mean() else float("inf")
print(f"IAT CoV={cov:.3f}, n={len(iat)}")
```

## Lateral Movement Hunting

Network-visible lateral movement techniques and their signatures:

- **SMB/RPC (445/135)**: file shares, PsExec, named-pipe activity; look for new SMB sessions between workstations, admin shares (`C$`, `ADMIN$`), and large outbound SMB from a single host.
- **RDP (3389)**: off-hours or unusual source→target pairs, short sessions, concurrent sessions.
- **WinRM/PowerShell remoting (5985/5986)**: WinRM from non-admin workstations; PS remoting to many targets.
- **WMI/DCOM (135)**: RPC to `IWbemServices`; correlate with process creation on the target.
- **Pass-the-Hash / Pass-the-Ticket**: NTLM authentication without a prior interactive logon; Kerberos TGS requests from unusual hosts; event 4624 type 3/9.

Hunting patterns: east-west flow matrices (which hosts talk to which), new edges in the internal graph, service-account authentication from workstations, and authentication bursts followed by remote execution. Honeypots/decoys on unused IPs catch scanning and lateral probing early.

## C2 Hunting (JA3/JA4, Domain Age, Periodicity)

C2 rarely looks like normal browsing. Combine these signals:

- **TLS fingerprints**: JA3 (MD5 of ClientHello fields) and JA4 (readable, sorted, TLS 1.3/QUIC-aware). Maintain allowlists for browsers/agents; alert on tooling-associated fingerprints (Cobalt Strike, Sliver, Metasploit, custom Go/Python TLS stacks). Pair JA3/JA4 with JA3S and SNI for confidence. Fingerprints are hints — they change with library updates and can be spoofed (uTLS, curl-impersonate).
- **Certificate anomalies**: self-signed, recently issued, short lifetimes, unknown/free CAs for high-value names, mismatched SNI/subject, weak keys, reused serials across unrelated domains. Check CT logs for unauthorized issuance.
- **Domain age and reputation**: newly registered domains (<30 days), low-reputation TLDs, privacy-protected WHOIS, DGA-like entropy, fast flux (many IPs, short TTLs).
- **Periodicity**: beaconing metrics above, applied to the C2 channel regardless of protocol.
- **Destination rarity and context**: first-seen domains, connections outside business hours, rare user-agents, direct-to-IP HTTPS, non-browser ALPN.

Example Zeek pivot for suspicious TLS clients:

```bash
zeek -r capture.pcap
zeek-cut uid id.orig_h id.resp_h server_name ja3 ja4 < ssl.log | sort | uniq -c | sort -rn | head
```

## Hunt Narrative

A hunt is only as good as its narrative. Reconstruct the attack as a timeline:

1. **Anchor** on a pivot (suspicious flow, alert, or intel) with timestamp and host.
2. **Expand** backward and forward in time across all sources (flow, DNS, proxy, TLS, Zeek, endpoint/identity).
3. **Correlate** by 5-tuple, `uid`, user, and host; account for clock skew (NTP).
4. **Map** each observed behavior to MITRE ATT&CK techniques and to the Cyber Kill Chain / Diamond Model (Adversary → Infrastructure → Capability → Victim).
5. **Document** queries, raw results, timestamps, and hosts so another analyst can reproduce.
6. **Decide** the hunt's outcome: confirmed intrusion, suspicious-but-unconfirmed, or no evidence — and state the coverage (which hosts/sources were actually checked).

End every hunt with one of: a new detection rule, a new/changed data source, or a follow-up hypothesis. Archive the narrative and the queries for reuse.

## Best Practices

- Start from a written, falsifiable hypothesis with defined success criteria.
- Time-box hunts (suggest 5–30 minutes per iteration) and scope them to a segment or technique.
- Correlate network signals with endpoint and identity telemetry before concluding.
- Prefer TTP-based hypotheses over IOC sweeps; convert confirmed finds into automated detections.
- Use Zeek `uid` as the join key across protocol logs; keep sensor clocks synced via NTP.
- Baseline normal TLS fingerprints, DNS patterns, and east-west traffic per environment.
- Require multiple independent signals (fingerprint + domain age + periodicity + cert) before alerting.
- Document timelines in real time; map findings to ATT&CK.
- Validate detections with red-team/purple-team exercises and replayed PCAPs.
- Retain flow/DNS metadata 30–90 days minimum; longer for regulated environments.

## Gotchas

- "No findings" without verified data coverage is an assumption, not a result.
- Jitter defeats simple periodicity checks; use multiple statistical methods and longer windows.
- JA3/JA4 change with library/OS updates and can be spoofed; treat as hints, not identity.
- Zeek field names differ from Suricata/SIEM (`id.orig_h` vs `src_ip`); do not mix them.
- sFlow sampling misses short/rare flows, including low-volume C2; use unsampled flow for detection.
- New domains and Let's Encrypt certs are common in legitimate infra; correlate before alerting.
- Clock skew breaks correlation; sync all sensors via NTP and record offsets.
- High-volume TLS metadata demands storage planning and indexing by 5-tuple/time.
- ECH + DoH can remove hostname visibility; enforce approved resolvers and monitor SNI leakage.
- Detection fatigue from over-broad hypotheses erodes trust; keep hypotheses narrow and time-boxed.
---

*Reference — Network Threat Hunting (network-security skill).*
