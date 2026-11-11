---
name: "Network Monitoring & Detection"
description: "Network visibility, flow telemetry, DPI, NDR, IDS/IPS deployment and tuning, PCAP workflow, SIEM integration, and detection engineering for defensive network monitoring."
tags: [network-monitoring, span, tap, netflow, ipfix, sflow, dpi, zeek, suricata, snort, ndr, eta, ja3, ja4, ids, ips, pcap, siem, syslog, cef, leef, detection-engineering, evasion]
---

# Network Monitoring & Detection

## Visibility: SPAN, TAP, Inline, Passive

Network monitoring begins with getting traffic to sensors. Two capture mechanisms dominate: **SPAN (Switched Port Analyzer / port mirroring)** and **network TAPs**.

- **SPAN** mirrors traffic from one or more switch ports/VLANs to a monitor port. It is cheap and flexible but shares switch backplane bandwidth; under heavy load frames can be dropped, and SPAN ports may not capture error frames or out-of-band traffic. Configure carefully: bidirectional mirroring, filter by VLAN, avoid oversubscription.
- **Network TAPs** (Test Access Points) are inline hardware devices that copy every bit (including errors and full-duplex traffic) to monitor ports without impacting production. Regeneration TAPs fan out to multiple sensors; aggregation TAPs merge directions. Preferred for forensic-grade capture and high-fidelity IDS.
- **Passive monitoring** observes a copy of traffic (SPAN/TAP) without sitting in the data path — zero latency impact, no single point of failure, but cannot block. Used for IDS, NDR, flow collection.
- **Inline monitoring** places the sensor in the forwarding path (IPS, inline proxy, firewall). Enables active blocking and traffic shaping but adds latency and a failure point; requires HA/bypass. Often paired with passive sensors for defense in depth.

Placement guidance: tap at trust boundaries (internet edge, data center core, between zones), on critical segments (domain controllers, databases), and at egress points. Monitor both directions; encrypted traffic still yields metadata.

## Flow Data: NetFlow v5/v9, IPFIX, sFlow

Flow records summarize conversations rather than full payloads, making them scalable for large networks.

- **NetFlow v5** (Cisco): fixed 7-tuple key (src/dst IP, ports, protocol, ToS, input interface) with packet/byte counts and timestamps. Widely supported but rigid; no extensibility.
- **NetFlow v9**: template-based, extensible field definitions; supports IPv6, MPLS, VRF, and custom fields. Templates are exported periodically; collectors must cache them.
- **IPFIX** (RFC 7011-7015): the IETF standard evolution of NetFlow v9; uses Information Elements (IEs) with enterprise-specific extensions, supports bidirectional flows, and is the modern interoperability target. Preferred for new deployments.
- **sFlow** (RFC 3176): statistical sampling (typically 1-in-N packets) plus counter polling; vendor-agnostic and low overhead, but sampled — misses short flows and rare events. Best for capacity planning and high-level visibility, not forensics.

Flow use cases: top talkers, bandwidth accounting, DDoS detection, beaconing/periodicity analysis, lateral movement spotting, and baselining. Export from routers/switches/firewalls; collect with nProbe, ElastiFlow, or SIEM flow modules. Retain at least 30-90 days; watch for asymmetric routing causing incomplete records.

## Deep Packet Inspection (DPI)

DPI examines payload content beyond headers, enabling protocol identification, file extraction, and signature matching.

- **Zeek (formerly Bro)**: scriptable network analysis framework. Produces structured logs (conn, dns, http, ssl, files, etc.) and supports custom scripts for protocol-aware detection. Excellent for metadata and file carving; not a traditional signature IDS but a powerful sensor. Integrates with Suricata for hybrid pipelines.
- **Suricata**: multi-threaded IDS/IPS/NSM engine supporting Emerging Threats (ET) rules, Lua scripting, file extraction, TLS fingerprinting, and protocol parsing. Modes: IDS (passive) and IPS (inline). High performance via AF_PACKET, DPDK, eBPF/XDP.
- **Snort**: classic signature-based IDS/IPS; Snort 3 uses a new config language, multi-threading, and Hyperscan. Large rule ecosystem (Snort Community, Talos). Still common in legacy and Cisco Firepower (Snort-based).
- **Rules**: Suricata/Snort rules use action, protocol, addresses, ports, direction, and content modifiers (`content`, `http.uri`, `file_data`, `tls.sni`, `bsize`, `fast_pattern`, `flowbits`). Tune with `threshold`, `detection_filter`, and rule suppression. Keep rulesets versioned and tested in staging.

DPI limits: TLS encryption hides payloads; requires decryption or metadata-focused detection. High throughput demands hardware acceleration and careful rule selection.

## NDR: Encrypted Traffic Analytics (ETA) and JA3/JA4

Network Detection and Response (NDR) focuses on behavioral and metadata analysis, especially for encrypted traffic.

- **ETA (Encrypted Traffic Analytics)**: derives features from TLS handshakes, packet sizes/timing, and certificate metadata to classify malicious flows without decryption. Uses ML models trained on benign/malicious samples. Effective against C2 over HTTPS but requires baselining and can have false positives on rare apps.
- **JA3 / JA4**: TLS client fingerprinting based on handshake parameters (cipher suites, extensions, elliptic curves). JA3 produces an MD5 hash; JA4 improves robustness with a readable, sorted fingerprint and supports TLS 1.3 and QUIC. Use to identify non-browser clients, malware toolkits, and C2 frameworks; allowlist common browsers/agents to reduce noise.
- Combine JA3/JA4 with SNI, certificate issuer/validity, and destination reputation for higher confidence. Note fingerprints change with library updates and can be spoofed by determined adversaries.

## IDS/IPS Deployment Modes and Tuning

- **IDS (passive)**: monitors copies; alerts only. Safe, no latency, but cannot prevent. Deploy broadly for visibility.
- **IPS (inline)**: inspects and can drop/block. Place at chokepoints (edge, between zones). Requires tuning to avoid blocking legitimate traffic; use fail-open bypass for availability.
- **Hybrid**: passive sensors for detection + selective inline enforcement (e.g., at edge only).

**Tuning methodology**:
1. Start in IDS mode with a conservative ruleset; collect alerts for 1-2 weeks.
2. Suppress noisy rules and whitelist known-good traffic (health checks, backup jobs, internal scanners).
3. Convert high-confidence rules to IPS (block) gradually; keep detection-only for ambiguous ones.
4. Use thresholds and rate-based rules for brute force/scans.
5. Maintain a change log and test rules in staging; measure false positive rate and MTTD.
6. Tune performance: disable unused protocols, limit file extraction size, use multi-queue NICs, and pin CPUs.

## PCAP Workflow

Packet capture is the ground truth for investigation and validation.

1. **Capture**: use `tcpdump`, `tshark`, or sensor PCAP. Ring buffers with size/time limits (e.g., `-C 100 -W 10`) to manage disk. Capture at TAP for fidelity.
2. **Filter**: BPF filters at capture (`host`, `port`, `net`, `tcp flags`) to reduce volume; display filters in Wireshark for analysis.
3. **Analyze**: follow streams, inspect protocols, extract files/objects, check TLS handshakes (JA3), DNS, HTTP. Use Zeek for automated log generation from PCAP (`zeek -r file.pcap`).
4. **Correlate**: align PCAP timestamps with flow records, SIEM events, and endpoint telemetry. Account for clock skew.
5. **Store/retain**: encrypted, access-controlled; define retention per compliance (often 30-90 days full PCAP, longer metadata). Index by 5-tuple and time.
6. **Chain of custody**: hash captures (SHA-256), document collection, restrict access for legal admissibility.

## SIEM Integration: Syslog, CEF, LEEF

Centralize sensor output for correlation and alerting.

- **Syslog** (RFC 5424): standard transport; facilities/severities; reliable via TCP/TLS. Use for generic logs.
- **CEF (Common Event Format)**: ArcSight format; structured key=value pairs with a header (`CEF:0|Vendor|Product|Version|SignatureID|Name|Severity|...`). Widely supported by SIEMs (Splunk, QRadar, Sentinel). Good for IDS alerts.
- **LEEF (Log Event Extended Format)**: IBM QRadar format; `LEEF:Version|Vendor|Product|Version|EventID|key=value` with delimiter handling. Preferred in QRadar environments.
- Best practices: normalize timestamps to UTC, include sensor ID/location, use TLS for transport, set appropriate severity, deduplicate, and validate parsing with SIEM test harnesses. Map fields to a common schema (ECS, OCSF) for cross-source correlation.

## Detection Engineering

Detection engineering turns telemetry into reliable, maintainable detections.

- **Signature-based**: match known bad (hashes, IPs, domains, YARA/Suricata rules). High precision for known threats; blind to novel attacks. Requires constant updates.
- **Anomaly-based**: statistical deviation from baseline (volume, entropy, new destinations, off-hours activity). Catches unknowns but higher false positives; needs tuning and context.
- **Behavioral**: sequence of actions (e.g., LSASS access + network connection + scheduled task) mapped to MITRE ATT&CK techniques. Balances precision and coverage; harder to build but more robust to evasion.

Process: hypothesis → data source → detection logic → testing (true/false positive datasets) → deployment → monitoring/alert fatigue → tuning → retirement. Use version control, peer review, and metrics (FP rate, MTTD, coverage). Prefer detections tied to ATT&CK techniques with documented assumptions and data requirements.

## Evasion

Adversaries evade network monitoring via:
- **Encryption** (TLS/QUIC) hiding payloads; use metadata/ETA/JA3 and selective decryption.
- **Fragmentation** and **encapsulation** (tunnels, VPNs, DNS/ICMP tunneling) to bypass DPI.
- **Domain fronting / CDN abuse** to mask C2 destinations.
- **Low-and-slow beaconing** with jitter to evade periodicity detection.
- **Protocol mimicry** and living-off-the-land tools blending with normal traffic.
- **Packet padding / timing manipulation** to defeat ML models.

Defenses: decrypt where policy allows, monitor metadata and behavior, deploy multiple independent sensors, validate detections with red-team exercises, and assume partial visibility.

## Best Practices

- Tap critical segments and trust boundaries; prefer hardware TAPs for forensics.
- Combine flow + DPI + endpoint + identity telemetry for correlation.
- Start IDS, tune, then selectively enable IPS with change control.
- Centralize logs in SIEM with normalized schemas (ECS/OCSF) and TLS transport.
- Maintain detection-as-code with tests and version control.
- Baseline normal traffic; review detections quarterly; retire stale rules.
- Document exceptions (TLS inspection bypasses) and monitor them.
- Practice incident response with PCAP and flow data; validate chain of custody.

## Gotchas

- SPAN ports drop packets under load and miss errors; do not rely on them for forensics alone.
- sFlow sampling misses short/rare flows; not suitable for detection of low-volume C2.
- NetFlow templates (v9/IPFIX) must be cached by collectors; template loss breaks parsing.
- TLS 1.3 and QUIC reduce visibility; JA3/JA4 and ETA help but are not foolproof.
- Inline IPS can cause outages if poorly tuned; always have bypass and rollback.
- Zeek/Suricata rule updates can spike CPU; schedule and monitor.
- Clock skew breaks correlation; sync all sensors via NTP.
- Detection fatigue from noisy rules erodes trust; measure and tune continuously.
- Encrypted traffic metadata alone cannot confirm malicious intent; correlate with endpoints.
