---
name: "Network Detection Engineering"
description: "Detection lifecycle, signature vs anomaly vs behavioral detection, Suricata/Snort rules, Zeek scripts, Sigma for network, tuning and false-positive reduction, ATT&CK mapping, replay testing, and detection metrics."
tags: [detection-engineering, suricata, snort, zeek, sigma, ids, ips, rules, attck, tcpreplay, replay, mttd, false-positive, tuning, network-detection]
---

# Network Detection Engineering

Detection engineering turns raw network telemetry into reliable, maintainable, and measurable detections. This reference covers the full lifecycle, the three detection paradigms, concrete rule/script examples for the major engines, tuning and false-positive (FP) reduction, MITRE ATT&CK mapping, replay-based testing, and the metrics used to judge detection quality.

## Detection Lifecycle

A mature detection program treats detections as software: versioned, reviewed, tested, and retired.

1. **Hypothesis** — Define the adversary behavior to detect (e.g., "Cobalt Strike beaconing over HTTPS") and tie it to a data source that exists.
2. **Data validation** — Confirm the sensor emits required fields and logs reach the SIEM with correct timestamps/normalization.
3. **Detection logic** — Write the rule/script/query; prefer lowest-fidelity data that captures intent; avoid brittle indicators.
4. **Testing** — Validate against TP/TN datasets via replay and synthetic traffic; measure FP rate first.
5. **Deployment** — Ship detection-only first; gate blocking behind change control; canary rollout.
6. **Monitoring & tuning** — Track alert volume, FP rate, MTTD; suppress noise; review quarterly.
7. **Retirement** — Retire stale/deprecated detections; keep an audit trail.

> Tip: Keep detections in version control alongside test fixtures and sample PCAPs. Peer review every rule change, just like code.

## Detection Approaches: Signature vs Anomaly vs Behavioral

| Approach | Mechanism | Strengths | Weaknesses |
|---|---|---|---|
| **Signature** | Match known-bad indicators (IPs, domains, hashes, byte sequences) | High precision for known threats; cheap; explainable | Blind to novel attacks and polymorphic variants; constant upkeep |
| **Anomaly** | Statistical deviation from a baseline (volume, entropy, new destinations, off-hours) | Catches unknowns; good for DDoS/beaconing discovery | High FP rate; needs baselining and context; alert fatigue risk |
| **Behavioral** | Sequence of actions mapped to ATT&CK techniques (e.g., LSASS access → network connection → scheduled task) | Robust to evasion; higher coverage; intent-focused | Harder to build; needs rich telemetry and correlation; higher compute cost |

Combine them: signatures for known malware, anomaly for discovery/hunting, behavioral for high-value detections. Document data sources, FP sources, and confidence.

## Suricata & Snort Rules

Both engines use a similar rule grammar: `action protocol src srcport -> dst dstport (options)`. Suricata adds HTTP/TLS/file keywords and multi-threading; Snort 3 uses a new config language and Hyperscan.

### Suricata rule example — suspicious POST beacon

```
alert http $HOME_NET any -> $EXTERNAL_NET any (
    msg:"ET MALWARE Possible C2 Beacon to gate.php";
    flow:established,to_server;
    content:"POST"; http_method;
    content:"/gate.php"; http_uri; fast_pattern;
    http.header; content:"User-Agent|3a|"; nocase;
    pcre:"/User-Agent:\s*Mozilla\/4\.0/iH";
    threshold:type both, track by_src, count 5, seconds 60;
    classtype:trojan-activity;
    sid:1000001; rev:2;
)
```

Key modifiers used:
- `flow:established,to_server` — only match established client→server flows.
- `fast_pattern` — selects the best content for the fast-path matcher; place on the most unique, longest literal.
- `threshold:type both` — alert only after N matches in a window (rate-based), reducing FP on single hits.
- `http.uri`, `http_method`, `http.header` — sticky buffers that parse the protocol rather than raw bytes.

### Snort 3 rule example — DNS tunneling heuristic

```
alert udp $HOME_NET any -> any 53 (
    msg:"Possible DNS tunneling - long query name";
    content:"|00 01 00 00 00 00 00 00|"; offset:4; depth:8;
    byte_test:2,>,60,0,relative;
    detection_filter:track by_src, count 20, seconds 10;
    sid:1000002; rev:1;
)
```

Tuning knobs: `threshold`/`detection_filter` for rate limiting, `suppress` for known-good (scanners, health checks). Keep rulesets in Git, pin versions, test in staging.

## Zeek Scripts

Zeek is a scriptable network analysis framework that emits structured logs (conn, dns, http, ssl, files, etc.) and supports custom detection logic at the protocol-event level.

### Zeek script example — flag suspicious POSTs

```
event http_request(c: connection, method: string, original_URI: string,
                   unescaped_URI: string, version: string) {
    if (method == "POST" && /gate\.php/ in original_URI) {
        print fmt("suspicious POST %s from %s to %s",
                  original_URI, c$id$orig_h, c$id$resp_h);
        # Emit a notice for downstream alerting
        NOTICE([$note=Suspicious::C2_Beacon,
                $conn=c,
                $msg=fmt("suspicious POST %s", original_URI),
                $identifier=cat(c$id$orig_h, c$id$resp_h)]);
    }
}

# Raise a notice type
redef enum Notice::Type += { Suspicious::C2_Beacon };
```

Zeek strengths: protocol-aware fields, stateful correlation, file extraction/hashing, and `NOTICE` events for SIEMs. Use `@load` policies and test via `btest`.

## Sigma for Network Detections

Sigma is a generic, vendor-agnostic detection rule format. Network Sigma rules typically target normalized logs (Zeek, Suricata EVE JSON, firewall logs) rather than raw PCAP.

### Sigma rule example — dynamic DNS query

```yaml
title: Suspicious DNS Query to Dynamic DNS Provider
status: experimental
logsource:
    category: dns
    product: zeek
detection:
    selection:
        query|endswith:
            - '.duckdns.org'
            - '.no-ip.org'
            - '.ddns.net'
    condition: selection
falsepositives:
    - Legitimate dynamic DNS usage by remote workers
level: medium
tags:
    - attack.command_and_control
    - attack.t1071.004
```

Sigma rules compile to backend queries (Splunk SPL, Elastic KQL/Lucene, Microsoft Sentinel KQL) via `sigmac`/`pySigma`. Keep rules backend-agnostic in the repo and compile per-SIEM in CI. Include `falsepositives` and `level` to guide triage.

## Tuning & False-Positive Reduction

FPs erode analyst trust and inflate MTTD. A systematic tuning loop:

1. **Baseline** — Run rules in detection-only mode for 1–2 weeks; capture alert volume per rule and per source.
2. **Categorize noise** — Group FPs by cause: expected scanners, health checks, backup jobs, CDN traffic, internal tooling, parser artifacts.
3. **Allowlist precisely** — Scope exceptions by source IP/subnet, destination, user-agent, or rule+context. Avoid global disables; prefer `suppress` with `track by_src`.
4. **Thresholds & rate limits** — Convert single-hit alerts to count-based (`threshold`, `detection_filter`) for brute force/scans/beaconing.
5. **Confidence tiering** — Mark rules high/medium/low confidence; only high-confidence rules feed automated blocking or paging.
6. **Whitelist known-good at the sensor** — Drop obvious benign traffic before it hits rules (e.g., internal NTP, backup traffic) to save CPU.
7. **Iterate with metrics** — Track FP rate per rule; retire or rewrite rules above threshold (commonly >5% FP rate is unacceptable for paging).
8. **Change control** — Every tuning change reviewed, tested with replay, and logged with rationale.

> Warning: Over-tuning creates blind spots. Document every exception and review allowlists quarterly; adversary behavior often mimics "known-good" traffic.

## MITRE ATT&CK Mapping

Map each detection to one or more ATT&CK techniques so coverage is measurable and gaps are visible.

| Detection example | ATT&CK Technique |
|---|---|
| C2 beaconing over HTTPS | T1071.001 (Application Layer Protocol: Web) |
| DNS tunneling | T1071.004 (Application Layer Protocol: DNS) |
| Lateral movement via SMB | T1021.002 (SMB/Windows Admin Shares) |
| Data exfiltration over DNS | T1048.003 (Exfiltration Over Alternative Protocol) |
| Port scanning / reconnaissance | T1046 (Network Service Discovery) |

Use the ATT&CK Navigator for a coverage heatmap; prioritize threat-model techniques; validate with red-team exercises. Tag Sigma/SIEM detections with technique IDs.

## Testing: tcpreplay & Replay

Never deploy an untested rule. Replay captured or synthetic PCAPs through the sensor to confirm behavior.

- **tcpreplay** — Replays PCAPs onto an interface at original or modified speeds:
  ```
  tcpreplay -i eth1 --loop=2 --multiplier=10 capture.pcap
  ```
- **tcpreplay-edit** — Rewrite IPs/ports/MACs to fit your lab network:
  ```
  tcpreplay-edit --srcipmap=0.0.0.0/0:10.10.0.1 --dstipmap=0.0.0.0/0:10.10.0.2 lab.pcap
  ```
- **Zeek from PCAP** — `zeek -r capture.pcap` regenerates logs for rule validation.
- **Suricata offline** — `suricata -r capture.pcap -l /tmp/out` runs rules against PCAP without live traffic.
- **Synthetic traffic** — Use Scapy or hping3 to craft edge cases (fragmentation, odd flags) for robustness testing.
- **Test datasets** — Maintain paired TP/TN PCAPs and expected-alert manifests; run in CI on every rule change. Assert alert counts and SIDs match.

> Tip: Keep a "golden" PCAP set of known-malicious/benign traffic; replay after every ruleset update.

## Metrics: MTTD, FP Rate, Coverage

Measure detection quality, not just alert counts.

- **MTTD** — Average time from adversary action to alert; target minutes for high-value assets; track per technique.
- **FP rate** — False positives / total alerts; target <5% for paging rules; track per rule/source.
- **Detection coverage** — % of in-scope ATT&CK techniques with a tested detection; track gaps.
- **Alert volume/noise ratio** — Alerts per analyst per shift; sustained high volume signals tuning debt.
- **Sensor performance** — Packet drop rate, CPU, memory under replay load.

Report monthly; tie improvements to concrete actions.

## Best Practices

- Treat detections as code: Git, PRs, tests, CI, versioned rulesets.
- Map every detection to ATT&CK; document data requirements and assumptions.
- Start detection-only; promote to blocking with evidence and change control.
- Use highest-fidelity data (protocol fields) and `fast_pattern` wisely.
- Maintain TP/TN PCAP datasets; replay in CI on every change.
- Normalize logs to a common schema (ECS/OCSF) for portability.
- Tier by confidence; only high-confidence rules page analysts.
- Correlate with endpoint/identity telemetry before alerting.
- Measure MTTD, FP rate, coverage; report trends.

## Gotchas

- `fast_pattern` on a common string makes Suricata/Snort slow and noisy; choose unique literals.
- Thresholds reset per flow/track; confuse `type limit` vs `type both` and you spam or miss.
- Zeek `NOTICE` events can flood if not deduplicated; use `$identifier` and rate limits.
- Sigma field names must match the normalized schema; mismatches silently yield zero matches.
- Replay at original speed is slow for large PCAPs; use multipliers but watch timing-dependent detections.
- IPS inline changes break things: test in IDS mode first, keep bypass/fail-open, have rollback.
- Encrypted traffic limits payload visibility; metadata-only rules carry higher FP risk.
- Clock skew breaks correlation and MTTD measurement; sync via NTP.
- Rule updates can spike CPU and drop packets; schedule off-peak and monitor.
- Overly broad allowlists create blind spots; scope exceptions tightly.
</content>
