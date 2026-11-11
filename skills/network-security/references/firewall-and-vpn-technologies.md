---
name: "Firewall & VPN Technologies"
description: "Firewall types, rule design and default-deny, NAT, VPN protocols (IPsec/IKEv2, TLS/SSL, WireGuard, OpenVPN), split tunneling, key management, HA, performance, and management-plane security."
tags: [firewall, ngfw, waf, proxy, stateful, nat, vpn, ipsec, ikev2, tls-vpn, wireguard, openvpn, split-tunnel, key-management, ha, management-plane, default-deny]
---

# Firewall & VPN Technologies

## Overview

Firewalls enforce policy at trust boundaries; VPNs extend trusted reachability across untrusted networks. Together they form the perimeter and remote-access backbone of most enterprise networks, covering firewall architectures, rule engineering, address translation, VPN selection, tunneling policy, key lifecycle, availability, performance, and management-plane protection.

## Firewall Types

### Packet-Filtering (Stateless)

Evaluates each packet against ACLs of source/destination IP, ports, and protocol with no connection tracking. Fast and cheap but blind to return-traffic legitimacy and application context; use only for coarse filtering (router ACLs, cloud NACLs) before a stateful device.

### Stateful Inspection

Tracks connection state in a state table, allowing packets belonging to established/related flows even without explicit return rules. Handles TCP handshake, ICMP errors, and related protocols via helpers. Far more secure than stateless filtering at similar throughput; the baseline for most modern firewalls. Limitations: state tables can be exhausted (DoS), and stateful devices still see only L3/L4 unless extended.

### Next-Generation Firewall (NGFW)

Adds application identification (App-ID), user identity (User-ID), integrated IPS, TLS/SSL decryption, threat intelligence, and sandboxing on top of stateful inspection. Policies read as "allow application X for user Y on zone Z." NGFWs are the standard enterprise edge and segmentation enforcement point. Costs: higher latency, throughput reduction under decryption/IPS, and significant tuning to avoid false positives.

### Proxy Firewalls (Application-Level Gateway)

Terminate connections on both sides and relay at the application layer (HTTP, FTP, SMTP). The client never talks directly to the server. Highest security and content control (DLP, malware scanning, protocol normalization) but highest latency and lowest throughput. Modern NGFWs absorb much of this role; explicit proxies remain common for web egress and email.

### Web Application Firewall (WAF)

Specialized L7 firewall for HTTP/S apps, protecting against OWASP Top 10 (SQLi, XSS, RCE, path traversal) and bot abuse. Deployed at reverse proxies, load balancers, CDNs, or cloud edges. Uses managed rule sets (OWASP CRS) plus custom rules, rate limiting, and geo/IP reputation. Tune in detection mode before enforcement.

## Rule Design & Default-Deny


- **Default deny**: implicit drop for traffic not explicitly allowed, both directions. Never ship a device on "permit any."
- **Explicit allow with justification**: every rule documents owner, business purpose, expiry/review date, and ticket reference.
- **Least privilege**: allow the specific source, destination, application, and port—not "any."
- **Order matters**: most specific first, then broader, then deny; many platforms evaluate top-down and stop at first match.
- **Logging**: log denies (always) and allows for sensitive flows; avoid logging high-volume benign traffic.
- **No "temporary" rules**: time-box exceptions and auto-expire; require change review for permanent additions.
- **Rule hygiene**: quarterly review to remove stale/unused rules; track hit counts.

Example (nftables-style):

```text
policy input drop
policy forward drop
ct state established,related accept
tcp dport 443 ip saddr 10.10.0.0/16 accept
udp dport 53 ip saddr 10.10.0.0/16 accept
log prefix "FW-DENY: " level warn
drop
```

## NAT

Address/port rewriting, most commonly IPv4 private↔public.

- **SNAT / masquerade**: rewrite source for outbound traffic from private subnets; many-to-one sharing of a public IP.
- **DNAT / port forwarding**: rewrite destination to publish an internal service.
- **PAT (NAPT)**: port-level multiplexing; common in home/SOHO and cloud NAT gateways.
- **Static NAT**: 1:1 mapping for servers needing a stable public IP.
- **Dynamic NAT**: pool-based mapping without port translation.
- **NAT-T (UDP 4500)**: encapsulates IPsec ESP in UDP so IPsec survives NAT; required when either peer is behind NAT.
- **Hairpin / loopback NAT**: internal clients reach a service via its public IP; often misconfigured—prefer split DNS.
- **Logging**: record original and translated addresses for forensics.

NAT is not a security control by itself (it only hides topology); combine with firewall policy and egress filtering. Watch MTU/fragmentation with tunnels.

## VPN Technologies

### IPsec / IKEv2

L3 encryption and authentication via ESP (confidentiality + integrity) and optionally AH (integrity only). IKEv2 negotiates SAs, handles rekeying, and supports MOBIKE for roaming. Modes: **tunnel** (encapsulates entire IP packet—site-to-site and remote access) and **transport** (payload only—host-to-host). NAT-T (UDP 4500) required when NAT is in path. Prefer IKEv2 over IKEv1 and use AES-GCM + SHA-2 + ECDH (groups 19/20/21) or post-quantum groups. NIST SP 800-77 Rev. 1 governs.

### TLS/SSL VPN

Uses TLS (typically 443) to carry VPN traffic, firewall-friendly and easy to deploy. Flavors: **portal/clientless** (browser-based access to specific apps) and **tunnel/full** (virtual adapter, full network access). Auth via certificates, MFA, SAML/OIDC. TLS 1.3 minimum; disable legacy TLS and weak ciphers. Good for remote users behind restrictive networks; less suited to site-to-site.

### WireGuard

Modern, minimal VPN using Curve25519, ChaCha20-Poly1305, BLAKE2s, SipHash. ~4,000 lines, kernel-space, very high performance, instant connect, cryptokey routing (public key = identity, allowed IPs = routing). No built-in PKI; keys are static and managed manually. Excellent for site-to-site and roaming clients; requires careful key distribution and rotation.

WireGuard config:

```ini
[Interface]
PrivateKey = <server-private-key>
Address = 10.200.200.1/24
ListenPort = 51820

[Peer]
PublicKey = <client-public-key>
AllowedIPs = 10.200.200.2/32, 192.168.1.0/24
PersistentKeepalive = 25
```

### OpenVPN

TLS-based, open-source, UDP (preferred) or TCP (fallback through restrictive firewalls). Highly flexible (custom ciphers, auth plugins, PKI), broad client support, but slower and more complex than WireGuard; userspace. Still common where legacy compatibility or advanced auth integration is required. Use TLS 1.3-capable builds, AEAD ciphers, and certificate + MFA auth.

## Split Tunneling

- **Full tunnel**: all client traffic traverses the VPN; maximum visibility and control, higher gateway load and latency.
- **Split tunnel**: only corporate-bound traffic uses the VPN; internet traffic goes direct. Better performance and gateway capacity, but bypasses corporate controls (DLP, filtering, monitoring) for internet traffic.
- **Split DNS**: resolve internal names via VPN DNS while public names resolve normally; required for split tunnel to reach internal services by name.
- Decide one policy and enforce it; mixed/unenforced split tunneling causes leaks. Mitigate with endpoint posture, ZTNA, and cloud security (CASB/SWG).

## Key Management

- **IPsec**: protect IKE credentials; prefer certificate auth over PSKs; rotate PSKs if used; manage SAs and rekey intervals; store keys in HSM/KMS.
- **TLS VPN / OpenVPN**: run a proper PKI (intermediate CA, short-lived certs, CRL/OCSP); automate issuance via SCEP/EST/ACME; revoke on device loss.
- **WireGuard**: private keys never leave the device; distribute public keys out-of-band; rotate by reissuing peer configs; remove peers on decommission.
- **Storage**: never commit keys to git or config repos; use secret managers (Vault, cloud KMS, HSM); restrict read access and audit.
- **Rotation cadence**: define per key type (device certs 1 year, CA 3-5 years, PSKs 90 days or on suspected compromise); automate and test revocation.

## High Availability

- **Active/passive**: standby takes over on failure; stateful failover requires session/state sync (config, connection tables, VPN SAs).
- **Active/active**: load balance across nodes; requires symmetric routing and shared state or stateless design.
- **VPN HA**: anycast gateways, DNS-based failover, or clustered concentrators; ensure clients reconnect automatically; replicate user/session state.
- **Health checks**: synthetic probes for control and data plane; fail closed or open per documented risk decision.
- **Geo-redundancy**: separate sites/regions with tested failover; measure RTO/RPO.
- Test failover regularly—untested HA is not HA. Watch for asymmetric routing and MTU mismatches after failover.

## Performance

- Throughput drops with deep inspection, TLS decryption, and IPS; size for worst-case inspected throughput, not line rate.
- Use hardware offload (AES-NI, NIC crypto, dedicated appliances) and kernel bypass where supported.
- Tune: connection table size, NAT pool size, fragment handling, MSS clamping for tunnels, and queue/IRQ affinity.
- TLS decryption is CPU-heavy and breaks some apps (pinning, ECH); scope decryption to required zones and maintain exception lists.
- Monitor: CPU, memory, session count, drops, latency, and retransmits; alert before saturation.
- Avoid single points: distribute VPN concentrators and use ECMP/anycast.

## Management Plane Security

The management plane is the highest-value target; compromise equals full control.

- **Out-of-band (OOB) management**: dedicated management network/VRF, not reachable from data plane; jump hosts/bastions with MFA and session recording.
- **Access control**: RBAC with least privilege; separate read-only vs config roles; no shared accounts; MFA for all admins; SSH keys/certs, disable password auth.
- **API security**: token scoping, IP allowlists, rate limiting, audit logs; avoid exposing management APIs to the internet.
- **Hardening**: disable unused services (Telnet, HTTP, SNMPv1/v2c), SNMPv3 auth+priv, signed firmware, secure boot where available.
- **Change control**: IaC + peer review + CI validation; backup configs with integrity checks; tested restore.
- **Monitoring**: alert on config changes, failed logins, new admin accounts, and policy modifications; ship to SIEM with tamper-resistant logging.

## Best Practices

- Default-deny in both directions; allow only documented, reviewed flows.
- Prefer NGFW with App-ID/User-ID at the edge and segmentation points; add WAF in front of every public HTTP endpoint.
- Use IKEv2 with modern crypto (AES-GCM, ECDH) or WireGuard for new VPN deployments; retire IKEv1 and weak ciphers.
- Enforce a single, explicit split-tunneling policy; use split DNS where applicable.
- Run a real PKI with short-lived certs and automated revocation; store keys in HSM/KMS.
- Design HA with tested failover, state sync, and measured RTO/RPO.
- Protect the management plane with OOB access, MFA, RBAC, and change control.
- Review and prune rules quarterly; remove stale exceptions.

## Gotchas

- Stateful tables exhaust under SYN floods or scanning; enable SYN cookies and rate limits.
- NAT masks source IPs—log translations or forensics break.
- IPsec behind NAT requires NAT-T (UDP 4500); forgetting it causes silent tunnel failures.
- MTU/fragmentation issues are common with VPN encapsulation; clamp MSS and test large transfers.
- Split tunneling can leak corporate traffic around controls; decide and enforce one policy.
- Active/active HA without state sync causes dropped sessions on failover.
- Clock skew breaks IPsec/TLS and log correlation; enforce authenticated NTP.
- "Any-any" rules accumulate and erode posture; enforce change review and expiry.

---

*Reference — Firewall & VPN Technologies.*
