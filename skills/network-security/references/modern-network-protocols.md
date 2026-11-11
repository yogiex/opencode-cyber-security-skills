---
name: "Modern Network Protocols"
description: "Security reference for QUIC/HTTP/3, TLS 1.3, DoH/DoT, WireGuard, eBPF/XDP, HTTP/2 Rapid Reset, WebSocket/WebRTC, MQTT/CoAP, 5G, and ECH — RFCs, cipher suites, implications, mitigations, and hardening."
tags: [quic, http3, tls13, doh, dot, wireguard, ebpf, xdp, http2, rapid-reset, websocket, webrtc, mqtt, coap, 5g, ech, esni, hpke]
---

# Modern Network Protocols

Modern protocols push encryption, performance, and programmability deeper into the stack. Each changes what defenders can see and control. This reference summarizes the key protocols, their RFCs, cipher suites, security implications, mitigations, and operational gotchas.

## QUIC and HTTP/3

**RFCs:** RFC 9000 (QUIC v1 transport), RFC 9001 (TLS for QUIC), RFC 9002 (loss detection and congestion control), RFC 9114 (HTTP/3).

QUIC runs over UDP and integrates TLS 1.3 into the transport. It provides multiplexed streams without TCP head-of-line blocking, connection migration (survives IP/port changes via connection IDs), and 0-RTT early data. HTTP/3 (RFC 9114) maps HTTP semantics onto QUIC streams.

Security implications:

- UDP-based traffic bypasses TCP-centric firewalls, IDS, and NAT assumptions; requires QUIC-aware inspection.
- Connection migration complicates IP-based session tracking and source-based rate limiting.
- 0-RTT early data is replayable; must not carry non-idempotent or state-changing requests without anti-replay handling.
- Amplification risk: a small initial packet can trigger a large response; mitigated by the address validation token and the anti-amplification limit (server sends at most 3x bytes received until the client address is validated).

Mitigations: enable QUIC only where needed; enforce address validation; apply per-connection and per-source rate limits; deploy QUIC-aware proxies/WAFs; monitor for abnormal stream counts and migration events.

Example (nginx enabling HTTP/3):

```nginx
listen 443 quic reuseport;
listen 443 ssl;
ssl_protocols TLSv1.3;
add_header Alt-Svc 'h3=":443"; ma=86400';
```

## TLS 1.3

**RFC:** RFC 8446 (TLS 1.3). Obsoletes TLS 1.2 (RFC 5246) and earlier.

TLS 1.3 reduces handshake latency to 1-RTT (0-RTT with early data) and mandates forward secrecy by removing RSA key transport and static Diffie-Hellman. Removed: CBC mode, RC4, 3DES, compression, renegotiation, and SHA-1 in signatures.

TLS 1.3 cipher suites (RFC 8446 §B.4):

| Cipher Suite | AEAD | Hash |
|---|---|---|
| `TLS_AES_128_GCM_SHA256` | AES-128-GCM | SHA-256 |
| `TLS_AES_256_GCM_SHA384` | AES-256-GCM | SHA-384 |
| `TLS_CHACHA20_POLY1305_SHA256` | ChaCha20-Poly1305 | SHA-256 |

Key exchange uses named groups such as `X25519`, `secp256r1`, `secp384r1`; signatures use ECDSA/RSA-PSS/Ed25519. TLS 1.3 is the only version permitted for QUIC.

Security implications: 0-RTT early data replay; downgrade protection via `supported_versions`; encrypted handshake (certificates hidden from passive observers except SNI, addressed by ECH). Mitigations: disable 0-RTT for sensitive endpoints or use anti-replay windows; enforce TLS 1.3 minimum; enable HSTS and certificate transparency; monitor for downgrade attempts.

## DoH and DoT

**RFCs:** RFC 7858 (DNS over TLS, port 853), RFC 8484 (DNS over HTTPS), RFC 9250 (DNS over QUIC).

DoT wraps DNS in TLS on a dedicated port; DoH carries DNS queries as HTTPS requests, blending with web traffic. Both provide confidentiality and integrity for DNS and defeat on-path spoofing and eavesdropping.

Security implications: centralizes trust in the chosen resolver; DoH can bypass enterprise DNS filtering, RPZ, and logging; complicates detection of DNS tunneling/exfiltration; may leak metadata via SNI/ESNI/ECH gaps. Mitigations: enforce an allowlist of resolvers via MDM/GPO; use DoT/DoH to approved internal resolvers; apply DNS-layer policy at the resolver; monitor for unauthorized resolver use; keep DNSSEC validation.

## WireGuard

WireGuard is a modern VPN using a fixed, minimal cryptographic construction: Curve25519 for ECDH, ChaCha20-Poly1305 for AEAD, BLAKE2s for hashing, SipHash24 for hashtable keys, HKDF for key derivation (Noise protocol IK pattern). It is small (~4k LOC) and auditable, with no cipher agility.

Security implications: no built-in user authentication or PKI — identity is a static public key; long-term static keys require careful rotation and storage; no post-quantum protection; roaming can expose endpoints. Mitigations: distribute keys via a trusted channel; restrict peers with `AllowedIPs`; firewall the UDP port (default 51820); rotate keys periodically; combine with MFA at the identity layer; log handshake events.

Example:

```ini
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.0.0.2/32
```

## eBPF and XDP

eBPF runs sandboxed programs in the kernel for observability, tracing, and networking; XDP (eXpress Data Path) processes packets at the NIC driver before the kernel network stack, enabling high-throughput filtering and DDoS mitigation.

Security implications: powerful kernel-level execution; compromised or malicious eBPF programs can bypass controls or exfiltrate data; requires `CAP_BPF`/root; verifier limits but does not replace review; supply-chain risk in third-party programs. Mitigations: restrict `CAP_BPF`/`CAP_SYS_ADMIN`; require signed/audited programs; enforce LSM and seccomp; monitor loaded programs (`bpftool`); use read-only maps where possible; keep kernels patched.

## HTTP/2 Rapid Reset (CVE-2023-44487)

HTTP/2 (RFC 7540, updated by RFC 9113) multiplexes streams over one connection. Rapid Reset abuses `RST_STREAM` frames to create and immediately cancel streams, forcing servers to allocate and tear down resources rapidly, causing denial of service at low bandwidth.

Mitigations: limit max concurrent streams; rate-limit `RST_STREAM`; set stream reset thresholds and auto-ban abusive clients; patch servers/CDNs; disable HTTP/2 where not needed; deploy edge protection (WAF/CDN) with Rapid Reset mitigations.

## WebSocket and WebRTC

**WebSocket:** RFC 6455 (`ws`/`wss`). Upgrades HTTP to a persistent bidirectional channel. Risks: cross-site WebSocket hijacking (CSWSH) when origin is not validated; auth token leakage; DoS via many connections. Mitigations: validate `Origin`; use short-lived tokens; enforce rate limits and connection caps; terminate TLS (wss only).

**WebRTC:** uses DTLS, SRTP, ICE, STUN/TURN. Risks: IP address leakage (local/public IPs exposed to peers), TURN server abuse, signaling-layer auth gaps. Mitigations: authenticate signaling; restrict TURN with credentials and quotas; disable WebRTC where unnecessary; apply CSP; use mDNS/ICE candidate filtering to reduce IP leak.

## MQTT and CoAP

**MQTT:** 3.1.1/5.0 (OASIS). Lightweight pub/sub for IoT. **CoAP:** RFC 7252 (with DTLS per RFC 7252/9147).

Risks: constrained devices often run without TLS/auth; topic ACL gaps; retained messages exposing stale data; broker compromise; amplification via observe. Mitigations: require TLS/DTLS; enforce username/password or client certs; strict topic ACLs; isolate brokers; disable retained messages where not needed; fuzz and patch firmware.

## 5G Security

5G introduces SUCI (concealed SUPI) to protect subscriber identity, 5G-AKA authentication, network slicing, and edge computing. New surfaces: RAN, core (5GC), signaling (HTTP/2-based service-based architecture), roaming.

Risks: slice isolation failures; signaling abuse; rogue base stations; inter-slice lateral movement; supply-chain firmware. Mitigations: enforce slice isolation and QoS; protect N2/N3 with IPsec; use SUCI; monitor signaling; harden UPF/AMF; secure roaming interfaces.

## Encrypted Client Hello (ECH)

ECH (RFC 9849, formerly ESNI) encrypts the SNI and other ClientHello extensions using HPKE (RFC 9180), preventing on-path observers from reading the requested hostname. It depends on DNS HTTPS records (SVCB/HTTPS, RFC 9460) and DoH to fetch the ECH config.

Security implications: defeats SNI-based filtering/censorship and metadata inspection; shifts control to encrypted DNS; requires key management and config distribution; fallback can leak SNI. Mitigations: deploy DoH alongside ECH; rotate ECH keys; handle GREASE and fallback gracefully; update middleboxes and monitoring to rely on IP/SNI-less signals.

## Best Practices

- Prefer TLS 1.3 minimum; disable legacy versions and weak cipher suites.
- Use QUIC/HTTP/3 deliberately; ensure inspection and rate limiting keep pace.
- Enforce encrypted DNS to approved resolvers; do not let clients pick arbitrary DoH endpoints.
- Treat WireGuard keys as credentials; automate rotation and restrict peers.
- Gate eBPF/XDP deployment on review, signing, and least privilege.
- Patch rapidly for protocol-level CVEs (e.g., HTTP/2 Rapid Reset).
- Authenticate WebSocket/WebRTC signaling; restrict TURN and filter ICE candidates.
- Secure IoT protocols with TLS/DTLS, ACLs, and broker isolation.
- Protect 5G slices and signaling; use SUCI and IPsec on interfaces.
- Deploy ECH with DoH and manage keys; plan for fallback leakage.

## Gotchas

- 0-RTT early data is replayable; never use for state changes.
- DoH can silently bypass corporate DNS controls and logging.
- WireGuard has no user auth or built-in PKI; identity = static key.
- eBPF programs bypass traditional network visibility; audit loaded programs.
- HTTP/2 and QUIC bypass legacy TCP-only WAFs/firewalls.
- WebRTC exposes local IP addresses to peers.
- MQTT/CoAP devices frequently ship with no TLS or default credentials.
- ECH fallback may leak SNI if not configured carefully.
- 5G slice isolation is logical, not physical; misconfiguration enables lateral movement.

---

*Reference — Modern Network Protocols (network-security skill).*
