---
name: "Network Security Fundamentals & Standards"
description: "Core network security concepts, trust boundaries, attack surface, zones, hardening baselines, and governing standards/frameworks (NIST SP 800-41/77/123/207, CIS Controls v8, ISO/IEC 27033, IPsec/TLS RFCs) for defensive network engineering."
tags: [network-security, fundamentals, standards, nist, cis-controls, iso-27033, zero-trust, ipsec, tls, dmz, hardening, stig, firewall, segmentation]
---

# Network Security Fundamentals & Standards

## Core Concepts

### CIA Triad in Networking

- **Confidentiality** — protects data in transit and at rest. Enforced via TLS 1.3, IPsec ESP, VPN tunnels, WPA3, MACsec, and access control lists that restrict who can read a flow.
- **Integrity** — detects unauthorized modification. Uses HMAC, AEAD cipher suites (AES-GCM, ChaCha20-Poly1305), IPsec AH, TLS record MACs, and DNSSEC/RRSIG. Also covers ARP/DNS spoofing protection.
- **Availability** — keeps services reachable under load and failure. Redundancy (HA pairs, anycast), DDoS mitigation (scrubbing, rate limiting), QoS, capacity planning, and tested failover.

### Trust Boundaries

A trust boundary is the line where data or control crosses between entities with differing trust levels: user to application, application to database, internal to external, management plane to data plane. Every crossing must be treated as untrusted until authenticated and authorized. Document boundaries in architecture diagrams; place inspection (firewall, WAF, IDS/IPS) at each. Common mistakes: treating internal east-west traffic as trusted, or assuming a VPN endpoint implies a trusted device.

### Attack Surface

The set of reachable entry points an adversary can interact with: open TCP/UDP ports, exposed services and APIs, wireless SSIDs, VPN concentrators, management interfaces, cloud metadata endpoints, and DNS. Reduce it by disabling unused services, closing ports, removing default accounts, patching, and restricting management access to allowlisted IPs. Measure it with port scanning, attack-surface management (ASM) tools, and cloud security posture management (CSPM).

### Defense in Depth

Layered, independent controls so no single failure is catastrophic: edge firewall → WAF/DDoS → IDS/IPS → internal segmentation firewall → host firewall → application controls → encryption → monitoring/SIEM. Each layer must be able to stand alone; correlated failures (same vendor, same bug class) defeat the purpose. Document which control covers which threat so gaps are visible.

### Least Privilege

Grant the minimum network access, protocol permissions, and administrative rights required for a role or workload. Applies to human users, service accounts, devices, containers, and microservices. Implement with microsegmentation (identity-based policies per workload), read-only default accounts, and just-in-time (JIT) elevation with approval and time limits. Review entitlements on a fixed cadence.

### Fail-Safe Defaults

When a control fails or is misconfigured, it must deny access rather than permit it. Firewalls default to drop, ACLs default to deny, new accounts start with no permissions, and a crashed inspection engine fails closed (or fails open only with documented, monitored exception). Avoid "permit any" rules created to "make it work" during incidents; they tend to become permanent.

## Standards & Frameworks

| Standard | Scope | Key Points |
|----------|-------|------------|
| NIST SP 800-41 Rev. 1 (2009) | Firewalls and firewall policy | Types (packet filter, stateful, proxy, NGFW), policy design, logging, management, change control |
| NIST SP 800-77 Rev. 1 (2020) | IPsec VPNs | IKEv2, ESP/AH, tunnel vs transport mode, SA management, key exchange, NAT-T |
| NIST SP 800-123 (2008) | Server security | OS hardening, patching, service minimization, logging, backup and recovery |
| NIST SP 800-207 (2020) | Zero Trust Architecture | No implicit trust, continuous verification, microsegmentation, policy engine (PE) + policy enforcement point (PEP) |
| CIS Controls v8 (2021) | Network controls (Safeguard 12.x) | 12.1 boundary, 12.2 secure infrastructure, 12.3 manage devices, 12.4 segment, 12.5 centralize management, 12.6 secure protocols, 12.7 remote access via VPN, 12.8 device inventory |
| ISO/IEC 27033 (parts 1–6) | Network security | Architecture, controls, VPNs, secure communications, wireless, IP network security, convergence |
| RFC 4301 / 4302 / 4303 | IPsec architecture, AH, ESP | Security associations, traffic selectors, encapsulation, integrity/confidentiality |
| RFC 7296 | IKEv2 | Key exchange, SA negotiation, rekeying, NAT traversal (NAT-T, UDP 4500) |
| RFC 8446 | TLS 1.3 | Handshake, 0-RTT resumption, AEAD suites, forward secrecy, removal of legacy ciphers |
| RFC 9000 / 9114 | QUIC / HTTP/3 | UDP-based transport, integrated TLS 1.3, connection migration, 0-RTT |

**How to use standards in practice:** map each control to a standard clause for audit evidence, then verify with automated checks (CIS-CAT, STIG Viewer) rather than manual review. Standards are baselines, not ceilings; layer organization-specific requirements on top.

## Network Security Zones

| Zone | Trust Level | Typical Contents | Controls |
|------|-------------|------------------|----------|
| External / Internet | Untrusted | Public users, SaaS, threat actors | Edge firewall, WAF, DDoS protection, CDN |
| DMZ | Semi-trusted | Public-facing servers, reverse proxies, mail gateways | Strict inbound rules, no direct internal access, egress filtering |
| Internal / Trusted | Trusted | Workstations, internal apps, databases | Segmentation, NAC, internal firewall, EDR |
| Management Plane | Highly trusted | Admin interfaces, jump hosts, OOB network | Out-of-band, MFA, session recording, source allowlist |
| Control Plane | Infrastructure | Routing/switching control, SDN controllers, DNS | Isolation, authentication, integrity checks, change control |
| Data Plane | Traffic path | User/application traffic forwarding | ACLs, QoS, encryption in transit |

Principle: every packet between zones must cross an inspection point (firewall, proxy, or gateway). Flat networks are an anti-pattern; VLANs alone are not segmentation without firewall enforcement between them.

## Hardening Baselines

Baselines provide a measurable, repeatable secure configuration.

- **CIS Benchmarks** — device-specific hardening for Cisco IOS, Juniper JunOS, Palo Alto, Fortinet, Linux, Windows. Scored Level 1 (baseline, low operational impact) and Level 2 (defense-in-depth, higher impact).
- **DISA STIGs** — DoD security technical implementation guides for network devices, OS, and applications; mandatory in US federal environments, widely adopted as a strong baseline.
- **Vendor hardening guides** — Cisco, Juniper, F5, etc. baseline templates aligned to CIS/STIG.

**Key baseline actions**

- Disable unused services and ports; remove default accounts.
- AAA via TACACS+ or RADIUS; SSH only (disable Telnet); SNMPv3 with auth + priv (no v1/v2c communities).
- NTP with authentication; centralized syslog/SIEM; config backups with integrity checks.
- Firmware/OS patching on a defined cadence; track end-of-life.
- Enable management-plane protection (CoPP/control-plane policing).

**Example: Cisco IOS baseline snippet**

```text
no ip http server
ip http secure-server
transport input ssh
line vty 0 4
 transport input ssh
 login local
 exec-timeout 10 0
!
snmp-server group NETOPS v3 priv
snmp-server user monitor NETOPS v3 auth sha <auth> priv aes 256 <priv>
!
ntp server 10.0.0.10 key 1
ntp authenticate
ntp trusted-key 1
!
logging host 10.0.0.20
logging trap informational
```

**Example: firewall policy (default-deny, explicit allow)**

```text
# Default deny
deny ip any any log

# Allow documented flows only
allow tcp 10.10.0.0/16 any eq 443 stateful
allow udp 10.10.0.0/16 any eq 53 stateful
allow tcp 10.20.0.0/24 10.30.0.5 eq 8443 stateful
```

Validate baselines in CI/CD using infrastructure-as-code (Terraform/Ansible) plus CIS-CAT or STIG Viewer; fail the pipeline on regression.

## Key Decision Points & Tradeoffs

| Decision | Options | Tradeoff |
|----------|---------|----------|
| Firewall type | Packet filter / stateful / NGFW / proxy | Performance vs deep inspection; proxy = highest security, highest latency |
| VPN | IPsec / TLS-VPN / WireGuard | Enterprise compatibility (IPsec) vs ease of deployment (TLS) vs performance + simplicity (WireGuard) |
| Segmentation | VLANs / microsegmentation (ZTNA) | Cost and complexity vs granular, identity-based control |
| IDS/IPS placement | Inline (IPS) vs passive (IDS) | Active blocking risk (false positives drop traffic) vs visibility only |
| Encryption | Edge TLS termination vs end-to-end | Operational simplicity vs confidentiality through the full chain |
| Management access | In-band vs out-of-band (OOB) | Cost vs isolation and security of admin plane |
| Zero Trust adoption | Overlay on legacy vs greenfield | Disruption and effort vs security posture and agility |
| TLS inspection | Decrypt and inspect vs passthrough | Visibility into encrypted threats vs privacy, cert pinning breakage, app compatibility |

## Best Practices

- Default-deny all firewall policies; allow only documented, reviewed flows.
- Segment by trust level and data sensitivity; eliminate flat networks.
- Encrypt all traffic in transit (TLS 1.3 minimum; IPsec for site-to-site; WPA3 for wireless).
- Centralize logging and monitoring in a SIEM; retain per compliance requirements.
- Patch firmware and OS on a defined cadence; track and retire end-of-life devices.
- Use AAA with MFA for all administrative access; prefer out-of-band management.
- Document firewall rules with owners and business justification; review quarterly; remove stale rules.
- Validate configurations against CIS Benchmarks/STIGs in CI/CD (infrastructure-as-code).
- Test backups and failover regularly; measure RTO/RPO.

## Gotchas

- Default vendor configurations are insecure: default passwords, Telnet enabled, SNMPv2c community strings.
- Stateful firewalls can be bypassed by fragmented or encapsulated traffic without proper inspection (enable fragmentation handling and protocol inspection).
- VPN split tunneling can leak traffic around corporate controls; decide and enforce a single policy.
- Misconfigured NAT can mask source IPs, breaking forensics and access control; log original IPs.
- Flat networks allow lateral movement; VLANs alone are not segmentation without firewall enforcement between them.
- TLS inspection (SSL decryption) breaks certificate pinning and some applications; maintain an exception list and monitor.
- "Zero Trust" as a product label is not an architecture; it requires identity, device posture, and a policy engine/PEP.
- Overly broad firewall rules ("any-any") accumulate over time and erode security posture; enforce change review.
- Clock skew breaks TLS, IPsec, and logging correlation; enforce authenticated NTP everywhere.