---
name: "Encrypted Traffic Analysis"
description: "TLS metadata, JA3/JA4/JA4S fingerprinting, encrypted traffic analytics (ETA), certificate analysis, SNI/ESNI/ECH, beaconing detection, and tooling (Zeek ssl.log, Suricata, Wireshark) for defensive network monitoring."
tags: [eta, ja3, ja4, ja4s, tls, fingerprinting, sni, esni, ech, certificate, beaconing, zeek, suricata, wireshark, encrypted-traffic, ndr, privacy, compliance, hpke]
---

# Encrypted Traffic Analysis

Even when payloads are encrypted, every TLS connection leaks metadata: protocol version, cipher preferences, extensions, certificate fields, timing, and sizes. Encrypted Traffic Analysis (ETA) turns that metadata into detection signals without breaking confidentiality. This reference covers the core techniques, fingerprints, certificate inspection, hostname privacy (SNI/ESNI/ECH), beaconing detection, tooling, and the privacy/compliance constraints that govern their use.

## TLS Metadata

A TLS handshake exposes far more than "encrypted or not": protocol version and supported versions; cipher suites offered/selected; extensions and their order/values (SNI, ALPN, supported groups, signature algorithms, key share, padding, GREASE); certificate chain (subject, issuer, SANs, validity, key type/size, signature algorithm, serial, extensions, fingerprints); connection metadata (byte counts per direction, packet sizes, IATs, duration, TCP flags, retransmissions); and timing (handshake duration, time to first byte, session resumption/0-RTT).

Metadata is cheap to collect at scale and survives even with perfect forward secrecy and TLS 1.3. It is the foundation of NDR and ETA.

## JA3 / JA4 / JA4S Fingerprinting

TLS client fingerprinting hashes the ClientHello parameters into a stable identifier.

**JA3** (Salesforce) concatenates five fields from the ClientHello — SSLVersion, Ciphers, Extensions, EllipticCurves, EllipticCurvePointFormats — into a comma-separated string and MD5-hashes it:

```
771,4865-4866-4867-49195-49199-49196-49200-52393-49171-49172-156-157-47-53,0-23-65281-10-11-35-16-5-13-18-51-45-43-27-17513,29-23-24,0
MD5 -> e7d705a3286e19ea42f587b344ee6865
```

**JA3S** applies the same idea to the ServerHello (version, cipher, extensions) to fingerprint the server side. Pairing JA3 (client) with JA3S (server) and SNI strengthens identification.

**JA4** (FoxIO) is the successor: a readable, sorted, robust fingerprint that handles TLS 1.3 and QUIC. Format is `protocol+version+snipresence+ciphercount+extensioncount+alpn` followed by sorted cipher-hash and extension-hash segments:

```
t13d1516h2_8daaf6152771_e5627efa2ab1
```

The `JA4` family also includes **JA4S** (server), **JA4X** (X.509 certificate), **JA4H** (HTTP), and **JA4SSH** (SSH). JA4 sorts values before hashing, making it more stable across library updates than JA3, and adds a human-readable prefix.

Usage guidance: maintain allowlists of common browser/agent fingerprints to suppress noise; alert on rare/tooling-associated fingerprints (Cobalt Strike, Sliver, Metasploit, custom Go/Python TLS stacks); combine with SNI, cert issuer, destination reputation, and JA3S for confidence; treat fingerprints as hints, not identity (they change with library updates and can be spoofed via uTLS/curl-impersonate).

## Encrypted Traffic Analytics (ETA)

ETA classifies flows as benign or malicious using ML models trained on metadata features, without decryption.

Typical feature groups:

- TLS handshake: version, cipher, extensions count, curve, SNI presence/length, cert validity, issuer, self-signed flag, ALPN.
- Packet/byte distributions: sizes, directions, counts, entropy of payloads, burst patterns.
- Timing: inter-arrival times, durations, request/response ratios.
- Context: destination reputation, ASN, geolocation, prior history.

Cisco ETA is the canonical commercial implementation; many NDR platforms (Vectra, ExtraHop, Darktrace, Corelight) implement variants. Suricata and Zeek feed the underlying metadata.

Operational notes: requires baselining (models may not transfer across environments); false positives on rare/long-tail apps (correlate with endpoint/identity); defeatable by padding/timing manipulation but raises attacker cost; prefer metadata-first detection, reserve decryption for high-risk, policy-approved cases.

## Certificate Analysis

Certificates are rich, often overlooked signals. Inspect subject/SANs (hostname match, wildcard scope, count, unusual patterns); issuer (unknown/free CAs such as Let's Encrypt for short-lived C2, self-signed, mismatched chain); validity (notBefore/notAfter, very short/long lifetime, expired/not-yet-valid); key (RSA<2048, EC<256, DSA/MD5/SHA-1 weak); signature algorithm (SHA-1/MD5 red flags); extensions (EKU, basic constraints, CT precertificates, OCSP stapling); and the SHA-256 fingerprint of the DER cert tracked across flows.

Red flags for C2/malware: self-signed certs, recently issued certs for new domains, wildcard SANs on suspicious domains, Let's Encrypt with very short lifetimes, mismatched SNI/subject, expired certs still in use, reused serials/keys across unrelated domains. Monitor CT logs for unauthorized issuance for your domains. Check OCSP/CRL where available; treat stapling absence on high-value sites as a signal.

## SNI, ESNI, and ECH

**SNI (Server Name Indication, RFC 6066)** sends the requested hostname in plaintext during the ClientHello, enabling virtual hosting and hostname-based filtering. It is the most common metadata lever for defenders and censors alike.

**ESNI (Encrypted SNI)** was the first attempt to encrypt SNI using a public key published via DNS. It was deprecated in favor of ECH.

**ECH (Encrypted Client Hello, RFC 9849)** encrypts the entire ClientHello (including SNI and extensions) using HPKE (RFC 9180), keyed from DNS HTTPS/SVCB records (RFC 9460), typically fetched over DoH. Fallback (if ECH config unavailable) may leak SNI.

Defender implications: ECH + DoH removes hostname visibility from passive observers, degrading SNI-based filtering; middleboxes must rely on IP/reputation, flow behavior, and endpoint telemetry; ensure your own ECH deployment handles GREASE/fallback and monitor for SNI leakage; encrypted DNS (DoH/DoT) is a prerequisite for ECH, so enforce approved resolvers to retain control.

## Beaconing Detection

Beaconing is periodic C2 communication, often with jitter and small payloads. Detect via:

- **Inter-arrival time (IAT) analysis**: coefficient of variation (CoV) of IATs; low CoV indicates periodicity. Attackers add jitter (e.g., 10-30%) to raise CoV, so use sliding windows and multiple metrics.
- **Autocorrelation / FFT** over time series of connection events to find dominant periods.
- **Byte-volume consistency**: similar orig/resp byte counts across sessions; small payloads.
- **Long-lived, low-and-slow connections**: repeated connections to rare destinations, off-hours activity.
- **Destination rarity**: new/infrequent destinations, recently registered domains, unusual ASNs.

Tools and methods:

- **RITA** (Real Intelligence Threat Analytics): Zeek-based, scores beaconing, DNS tunneling, and long connections.
- **Zeek conn.log** + custom scripts or Jupyter notebooks for IAT/CoV analysis.
- **SIEM/ML**: Splunk MLTK, Elastic ML jobs, or Python (scipy, pandas) for periodicity detection.
- Combine with JA3/JA4, cert reputation, and destination intel; require multiple independent signals before alerting.

Example Python sketch for IAT coefficient of variation:

```python
import pandas as pd, numpy as np
# conn: DataFrame with ts (epoch), src, dst
conn = conn.sort_values("ts")
iat = conn["ts"].diff().dropna()
cov = iat.std() / iat.mean() if iat.mean() else float("inf")
# Low CoV (~<0.3) suggests periodicity; inspect jittered cases with FFT/autocorr
print(f"IAT CoV={cov:.3f}, n={len(iat)}")
```

## Tooling

### Zeek ssl.log

Zeek's `ssl.log` records TLS handshake metadata per connection:

```
#fields ts uid id.orig_h id.orig_p id.resp_h id.resp_p version cipher curve server_name resumed last_alert next_protocol established cert_chain_fuids client_cert_chain_fuids subject issuer client_subject client_issuer validation_status ja3 ja4
```

Key fields for ETA: `version`, `cipher`, `curve`, `server_name` (SNI), `subject`/`issuer`, `validation_status`, `ja3`, `ja4`. Zeek 6+ emits JA4. Analyze with `zeek-cut`, jq, or SIEM ingestion; correlate with `conn.log` for byte/timing features.

Example:

```bash
zeek -r capture.pcap
zeek-cut uid id.orig_h id.resp_h server_name ja3 ja4 < ssl.log | head
```

### Suricata

Suricata's EVE JSON includes a `tls` object with SNI, version, JA3/JA3S, JA4/JA4S, certificate subject/issuer, and fingerprint. Enable `tls` in EVE output and use rules such as `tls.sni`, `ja3.hash`, `ja4.hash`. Suricata 7+ supports JA4. Use for both detection rules and metadata export to SIEM.

### Wireshark / tshark

Wireshark's TLS dissector reveals handshakes, SNI, certificates, and (with keys) decrypted content. Useful filters:

```
tls.handshake.type == 1          # ClientHello
tls.handshake.type == 2          # ServerHello
tls.handshake.extension.type == 0x0000   # SNI extension
```

tshark extracts fields for pipelines:

```bash
tshark -r capture.pcap -Y "tls.handshake.type == 1" \
  -T fields -e ip.src -e ip.dst -e tls.handshake.extensions_server_name
```

For JA3/JA4 in Wireshark, use built-in/external dissectors or export to Zeek/Suricata for canonical fingerprints. `ssldump` and `tshark -r ... -q -z` stats also help for quick triage.

## Privacy and Compliance

Encrypted traffic analysis and TLS inspection raise serious privacy/legal issues:

- Decryption/inspection of user traffic may violate privacy laws (GDPR, ePrivacy, HIPAA, PCI-DSS) and monitoring regulations; some jurisdictions prohibit interception outright.
- Prefer metadata-first detection (JA3/JA4, cert metadata, flow behavior) over payload decryption; less invasive and usually sufficient.
- TLS inspection (MITM proxy) needs a corporate CA, user notice/consent, documented policy, and exemptions for sensitive categories (banking, health, auth).
- SSLKEYLOGFILE/key logging is for controlled-lab troubleshooting only; never capture production user traffic.
- Data minimization: collect only needed metadata; define retention (30-90 days metadata, shorter for PCAP); restrict access; encrypt at rest.
- Conduct a DPIA before deploying inspection; consult legal counsel for cross-border/regulated environments. Publish acceptable-use/monitoring policies; provide opt-out where required.

## Best Practices

- Default to metadata and fingerprinting; decrypt only where policy and law allow and risk justifies.
- Baseline normal TLS fingerprints and certificate patterns per environment; alert on deviations.
- Maintain JA3/JA4 allowlists for browsers/agents; focus alerts on rare/tooling fingerprints.
- Combine multiple signals (fingerprint + SNI + cert + destination reputation + behavior) before alerting.
- Inspect certificates for weak keys, short lifetimes, unknown issuers, and CT anomalies.
- Track ECH/DoH adoption in your environment; update middleboxes and detections accordingly.
- Use Zeek/Suricata for collection, SIEM for correlation, and RITA/ML for beaconing.
- Validate detections with red-team/purple-team exercises and replayed PCAPs.
- Document inspection bypasses and monitor them; review quarterly.
- Sync sensor clocks (NTP) and hash evidence (SHA-256) for forensics.

## Gotchas

- JA3/JA4 change with library/OS updates; fingerprints are hints, not identity, and can be spoofed.
- TLS 1.3 encrypts most handshake (certificates hidden); SNI and ECH determine remaining visibility.
- ECH fallback can leak SNI if not configured carefully; DoH is a prerequisite.
- Beaconing with jitter evades simple periodicity; use multiple statistical methods and longer windows.
- Self-signed/Let's Encrypt certs are common in legitimate infra; correlate before alerting.
- Zeek/Suricata JA4 support requires recent versions; verify field availability in your release.
- Metadata alone cannot confirm malicious intent; always correlate with endpoints and identity.
- Privacy laws may prohibit inspection even with technical capability; get legal review first.
- High-volume TLS metadata still demands storage planning and indexing by 5-tuple/time.

---

*Reference — Encrypted Traffic Analysis (network-security skill).*
