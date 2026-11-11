---
name: "Network Forensics"
description: "PCAP capture and chain of custody, triage workflow, tshark/Wireshark analysis, Zeek logs, flow analysis, timeline reconstruction, artifact extraction, endpoint correlation, and legal considerations for network investigations."
tags: [network-forensics, pcap, pcapng, chain-of-custody, tshark, wireshark, zeek, flow-analysis, netflow, ipfix, timeline, artifact-extraction, dfir, legal, evidence]
---

# Network Forensics

Network forensics is the capture, preservation, and analysis of network traffic to reconstruct events, identify compromise, and support incident response or legal proceedings. Treat every capture as evidence from the moment it is written to disk.

## PCAP Capture and Chain of Custody

Capture at a hardware TAP rather than a SPAN port when fidelity matters: TAPs copy every bit including errors and full-duplex traffic without dropping frames under load. Prefer the **pcapng** format (multiple interfaces, comments, nanosecond timestamps) over legacy pcap, but confirm downstream tool support before standardizing.

Capture commands:

```bash
# tcpdump with size/time rotation (100 MB per file, 10 files)
tcpdump -i eth0 -w /captures/edge_$(date +%Y%m%d_%H%M%S).pcapng -C 100 -W 10 'not port 22'

# tshark capture with ring buffer
tshark -i eth0 -b filesize:100000 -b files:10 -w /captures/edge.pcapng -f "not host 10.0.0.5"
```

Integrity and chain of custody:

```bash
sha256sum capture.pcapng > capture.pcapng.sha256
# verify later
sha256sum -c capture.pcapng.sha256
```

Document collector identity, capture time (UTC), sensor location, tool and version, interface, filter, hash, storage path, and every access. Work only on copies; keep originals read-only (chmod 444 or write-protected media). Encrypt at rest and restrict access to need-to-know. Retain per compliance requirements, then dispose securely.

## Triage Workflow

1. **Scope** the incident window, affected assets, and suspected protocols; confirm authorization.
2. **Validate evidence** — hashes, capture completeness, clock sync, no unexpected gaps.
3. **Quick statistics** — protocol hierarchy, conversations, endpoints, IO graph to find anomalies.
4. **Pivot** to suspicious hosts/flows; follow streams and inspect payloads.
5. **Extract artifacts** — files, credentials, domains, certificates.
6. **Correlate** with flow records, SIEM events, and endpoint telemetry.
7. **Reconstruct timeline** normalized to UTC.
8. **Document** findings, methodology, and limitations; preserve evidence.

Triage commands:

```bash
tshark -r capture.pcapng -q -z io,phs
tshark -r capture.pcapng -q -z conv,tcp
tshark -r capture.pcapng -q -z endpoints,ip
```

## tshark and Wireshark

Capture filters (BPF) reduce volume at collection; display filters refine during analysis. Combine both. Useful patterns:

```bash
# Filter by host and port, emit selected fields
tshark -r capture.pcapng -Y "ip.addr==10.0.0.5 && tcp.port==443" \
  -T fields -e frame.time -e ip.src -e ip.dst -e tcp.len

# Follow a TCP stream (index 5) as ASCII
tshark -r capture.pcapng -q -z follow,tcp,ascii,5

# Extract HTTP objects to a directory
tshark -r capture.pcapng --export-objects "http,/tmp/http_objects"

# DNS queries and answers
tshark -r capture.pcapng -Y "dns" -T fields \
  -e frame.time -e ip.src -e dns.qry.name -e dns.a
```

Merge and slice captures:

```bash
mergecap -a -w merged.pcapng a.pcapng b.pcapng
editcap -A "2026-11-10 00:00:00" -B "2026-11-10 23:59:59" in.pcapng out.pcapng
```

TLS decryption requires the session keys: static RSA private keys for legacy RSA key exchange, or an `SSLKEYLOGFILE` for modern TLS 1.3 with (EC)DHE. Configure keys in Wireshark preferences (Protocols > TLS). Expert info highlights retransmissions, RSTs, and malformed packets; coloring rules speed visual triage.

## Zeek Logs

Run Zeek against a capture to generate structured logs:

```bash
zeek -r capture.pcapng
zeek -r capture.pcapng -C          # ignore checksum errors
zeek -r capture.pcapng LogAscii::use_json=T
```

Key logs and their value:

- **conn.log** — 5-tuple, protocol, service, duration, byte counts, connection state.
- **dns.log** — queries and answers; spot DGA and tunneling.
- **http.log** — URIs, user agents, MIME types, status codes.
- **ssl.log** — TLS versions, cipher suites, SNI, JA3 fingerprints, certificate subjects.
- **files.log** — MIME types, hashes, extracted file paths.
- **notice.log** — Zeek-generated detections and anomalies.

Correlate across logs using the `uid` field. Extract fields with `zeek-cut`:

```bash
cat conn.log | zeek-cut ts uid id.orig_h id.orig_p id.resp_h id.resp_p proto service duration orig_bytes resp_bytes
```

Enable the FileExtract module in `local.zeek` to carve transferred files to disk; match hashes against threat intel. The Intel framework supports IOC matching against domains, IPs, and hashes.

## Flow Analysis

Flow records scale where full PCAP cannot. Use them to identify top talkers, beaconing, lateral movement, and exfiltration, then pivot to PCAP for payloads.

```bash
# nfdump: top source IPs by bytes
nfdump -R /flows -s srcip/bytes -n 20

# Filtered flow listing
nfdump -R /flows 'src ip 10.0.0.5 and dst port 443' \
  -o fmt:'%ts %sa %sp %da %dp %byt'
```

Beaconing appears as periodic connections with low jitter and consistent byte sizes. Watch for asymmetric routing that yields incomplete records. Combine flow telemetry with Zeek and endpoint data for confidence; flows alone lack payload context.

## Timeline Reconstruction

Normalize every timestamp to UTC and document clock skew. Sources include PCAP frame times, Zeek `ts`, flow export times, endpoint logs (Windows Event Log, syslog, EDR), and SIEM events.

```bash
tshark -r capture.pcapng -T fields -e frame.time_epoch -e ip.src -e ip.dst -e tcp.dstport | sort -n
```

Build a sorted timeline with source, host, event, and evidence reference. Use Timesketch, Plaso/log2timeline, or an ELK stack for large datasets. Record original time zones and any applied offsets. Correlate by 5-tuple, host IP, user account, and file hash. Note that PCAP timestamps reflect capture time, not event time.

## Artifact Extraction

Extract files and credentials from unencrypted or decrypted traffic:

```bash
tshark -r capture.pcapng --export-objects "smb,/tmp/smb_objects"
tshark -r capture.pcapng --export-objects "http,/tmp/http_objects"
# Zeek file extraction via FileExtract module; outputs under extracted/
sha256sum /tmp/* /extracted/* | sort
```

Carve unstructured data with `foremost` or `scalpel`. Hunt for:

- **Credentials**: HTTP basic auth, FTP, Telnet, SMTP AUTH, NTLM, Kerberos tickets.
- **DNS**: DGA patterns, tunneling (long TXT records, high entropy).
- **TLS**: SNI, self-signed/expired certificates, JA3/JA4 fingerprints.
- **Email**: SMTP/IMAP artifacts and attachments.

Hash all extracted artifacts and scan with YARA or antivirus. Deduplicate by hash before analysis.

## Correlation with Endpoints

Map IPs to hosts and users via DHCP logs, DNS, Active Directory, and EDR inventory. Align endpoint network connections (Sysmon Event ID 3, EDR telemetry) with PCAP flows by 5-tuple and timestamp. Match extracted file hashes against endpoint file scans and quarantine events. Use a SIEM to join network, endpoint, and identity data. Document gaps: missing endpoint logs, clock skew, or encrypted traffic that cannot be inspected.

## Legal Considerations

- **Authorization**: capture only on networks and systems you own or have written permission to monitor; define scope in the engagement.
- **Privacy**: captures may contain PII, credentials, and personal communications. Minimize collection, redact where policy allows, and comply with GDPR, CCPA, HIPAA, and local law.
- **Admissibility**: maintain chain of custody, document tool versions, avoid altering evidence, use write blockers for media, and hash. Follow jurisdictional rules (e.g., FRE 901/902, Daubert) and organizational policy.
- **Retention and disposal**: define periods per compliance; dispose securely.
- **Cross-border**: respect data residency and transfer restrictions.
- **Consent and notice**: some jurisdictions require employee notification or consent for traffic monitoring.
- **Decryption**: do not decrypt or inspect without authorization; document key handling.

## Best Practices

- Capture at a TAP; hash and document chain of custody from collection.
- Work on copies; keep originals read-only.
- Normalize timestamps to UTC; record and correct clock skew.
- Corroborate findings across tshark, Zeek, and flow tools.
- Extract, hash, and scan all artifacts; deduplicate by hash.
- Correlate network findings with endpoints and identity.
- Encrypt captures at rest; enforce access control and retention limits.
- Document methodology so results are reproducible.
- Validate capture completeness and note dropped frames or collection limits.

## Gotchas

- SPAN ports drop frames under load and miss errors; not forensic-grade alone.
- pcap vs pcapng compatibility: some tools read only legacy pcap.
- TLS 1.3 with perfect forward secrecy cannot be decrypted without session keys or key logs; JA3/JA4 provide metadata only.
- Clock skew breaks correlation; enforce NTP and document offsets.
- Large captures need filters, ring buffers, and indexing to stay manageable.
- Zeek may fail on bad checksums (use `-C`) or heavily fragmented traffic.
- Encrypted payloads hide artifacts, but metadata and timing still inform.
- File extraction produces duplicates and false positives; verify by hash.
- PCAP timestamps reflect capture time, not event time.
- Gaps in chain of custody can invalidate evidence in legal proceedings.
