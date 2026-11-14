---
name: network-security
description: Network security for defensive engineers: architecture, segmentation, modern protocols, Wi-Fi (WPA3, 802.1X/RADIUS, controllers), monitoring, hardening, cloud/container, wireless/OT, and emerging threats.
license: MIT
compatibility: opencode
metadata:
  author: "yogiex"
  repository: "https://github.com/yogiex/opencode-cyber-security-skills"
  version: "1.0.0"
  audience: network engineers, security engineers, soc analysts, cloud engineers
  workflow: defensive-engineering
  source: network-security
  keywords: "network security, wifi, wpa3, wpa2, sae, 802.1x, eap, radius, wifite, wireless controller, zero trust, segmentation, tls, quic, sase, ndr, ddos, dns, firewall, vpn, kubernetes"
---

# Network Security — Architecture, Protocols, Monitoring & Hardening

## Decision Frame

1. **What is the trust boundary?** — Identify where trust levels change (Internet, DMZ, internal, OT, cloud, cluster). Every crossing needs authentication, authorization, and inspection. Never assume "inside = trusted."
2. **What is the blast radius if this control fails?** — Segment so a single compromise cannot move laterally. Default-deny and least privilege at every layer.
3. **Is the traffic visible?** — If you cannot observe it (encrypted east-west, cloud flow logs, SPAN drops), you cannot detect or respond. Plan visibility before detection.
4. **Confidentiality vs availability vs safety?** — In IT, confidentiality often wins; in OT, availability and safety dominate. Choose controls that do not break real-time or safety functions.
5. **Build or buy, overlay or greenfield?** — Match Zero Trust/SASE/microsegmentation to environment maturity and budget; migrate in phases with rollback.

Stop and reassess if a proposed control breaks production traffic without a rollback plan or if it creates a single point of failure in the forwarding path.

## When to Use This Skill

**Use when:**
- Designing or reviewing network architecture, segmentation, or Zero Trust
- Hardening firewalls, VPNs, DNS, TLS/PKI, or network devices
- Selecting or tuning monitoring/detection (IDS/IPS, NDR, flow, PCAP)
- Securing cloud VPCs, Kubernetes clusters, service meshes
- Assessing wireless, IoT, or OT/ICS network security
- Investigating network attacks (DDoS, MITM, DNS, BGP, C2, lateral movement)
- Evaluating modern protocols (QUIC/HTTP/3, TLS 1.3, DoH/DoT, WireGuard, eBPF, 5G)

**Do not use when:**
- You need application-layer vulnerability testing — use web pentest skills
- You need GRC/compliance audit framing — use security-auditor or nist-800-53
- You need incident response runbooks — use ec-ecih or offsec-ir-200
- You need Kubernetes cluster hardening beyond networking — use lf-cks

## Core Principles

- **Default-deny, allow-list**: firewalls, ACLs, security groups, NetworkPolicies.
- **Segment by trust and data sensitivity**: VLANs are not segmentation; enforce at workload/identity granularity where risk warrants.
- **Encrypt in transit**: TLS 1.3 minimum for external; mTLS for east-west in zero-trust environments.
- **Visibility first**: taps/SPAN, flow logs, Zeek/Suricata, centralized SIEM.
- **Assume breach**: design for lateral-movement resistance and fast detection.
- **Safety-aware in OT**: never impair safety functions; use compensating controls and data diodes.

## Quick Start Workflow

1. **Inventory** assets, data flows, and trust boundaries.
2. **Baseline** normal traffic (flow, DNS, TLS metadata) before changes.
3. **Segment** with default-deny policies; validate application dependencies.
4. **Harden** devices and protocols (SSH-only, SNMPv3, TLS 1.3, DNSSEC/DoH).
5. **Monitor** with taps/SPAN + NDR/IDS; tune signatures; track false positives.
6. **Test** with game days, replay (tcpreplay), and failover drills.
7. **Review** rules and policies quarterly; use IaC and GitOps.

## Reference Documentation

| File | Description |
|------|-------------|
| [network-security-fundamentals.md](./references/network-security-fundamentals.md) | Core concepts, standards (NIST/CIS/ISO), zones, hardening baselines, tradeoffs |
| [modern-network-protocols.md](./references/modern-network-protocols.md) | QUIC/HTTP/3, TLS 1.3, DoH/DoT, WireGuard, eBPF, HTTP/2, WebSocket/WebRTC, MQTT/CoAP, 5G, ECH |
| [network-architecture-segmentation.md](./references/network-architecture-segmentation.md) | Traditional segmentation, microsegmentation, Zero Trust, SASE, SD-WAN, service mesh |
| [zero-trust-architecture.md](./references/zero-trust-architecture.md) | NIST SP 800-207: principles, components, deployment models, migration |
| [sase-and-sse.md](./references/sase-and-sse.md) | SASE/SSE components, architecture, migration, vendor evaluation |
| [firewall-and-vpn-technologies.md](./references/firewall-and-vpn-technologies.md) | Firewall types, rule design, NAT, VPN types, HA, management plane |
| [dns-security.md](./references/dns-security.md) | DNSSEC, DoH/DoT, filtering/RPZ, tunneling, DGA, resolver hardening |
| [tls-and-pki.md](./references/tls-and-pki.md) | TLS versions/ciphers, certificates, PKI, mTLS, CT, inspection, HSTS |
| [network-hardening-baselines.md](./references/network-hardening-baselines.md) | CIS Controls/Benchmarks, STIGs, device hardening, AAA, logging |
| [network-monitoring-detection.md](./references/network-monitoring-detection.md) | Visibility, flow, DPI, NDR, IDS/IPS, PCAP, SIEM, detection engineering |
| [encrypted-traffic-analysis.md](./references/encrypted-traffic-analysis.md) | JA3/JA4, ETA, TLS metadata, beaconing detection |
| [network-detection-engineering.md](./references/network-detection-engineering.md) | Detection lifecycle, rules (Suricata/Snort/Zeek/Sigma), tuning, metrics |
| [network-threat-hunting.md](./references/network-threat-hunting.md) | Hypothesis-driven hunting, beaconing, C2, lateral movement |
| [network-forensics.md](./references/network-forensics.md) | PCAP capture, triage, Zeek logs, timeline, artifact extraction |
| [ddos-mitigation.md](./references/ddos-mitigation.md) | DDoS types, amplification, scrubbing, anycast, rate limiting, testing |
| [network-attack-surface-trends.md](./references/network-attack-surface-trends.md) | MITM, DNS, BGP, lateral movement, C2, encrypted malware, trends |
| [cloud-container-networking.md](./references/cloud-container-networking.md) | VPC, Kubernetes networking, CNI, NetworkPolicy, service mesh, zero trust |
| [kubernetes-network-security.md](./references/kubernetes-network-security.md) | CNI, NetworkPolicy, Cilium, service mesh, policy-as-code |
| [wifi-8021x-eap-radius.md](./references/wifi-8021x-eap-radius.md) | Wi-Fi 802.1X, EAP methods, RADIUS, MAB, guest VLAN |
| [wifi-6-7-security.md](./references/wifi-6-7-security.md) | Wi-Fi 6/7 (802.11ax/be): mandatory WPA3, OWE, BSS coloring, OFDMA, MLO, 6 GHz rules |
| [wifi-wifite-tooling.md](./references/wifi-wifite-tooling.md) | Wifite automated wireless auditing: WEP/WPA/WPA2/WPS, dependencies, detection, hardening |
| [wifi-wpa2-attacks.md](./references/wifi-wpa2-attacks.md) | WPA2 4-way handshake, PMKID, KRACK, deauth/disassoc, evil twin, WPS brute force, offline dictionary, weak PSK, detection, hardening |
| [wifi-wpa3-protocol.md](./references/wifi-wpa3-protocol.md) | WPA3-Personal (SAE), WPA3-Enterprise (CNSA), OWE, PMF, SAE-PK, transition/downgrade |
| [wireless-iot-ot-network-security.md](./references/wireless-iot-ot-network-security.md) | Wi-Fi, Bluetooth, IoT protocols, OT/ICS, IEC 62443, data diodes |
| [wifi-enterprise-hardening.md](./references/wifi-enterprise-hardening.md) | Enterprise Wi-Fi hardening: WIPS/WIDS, rogue APs, spectrum, RADIUS, certs, SIEM |
| [wifi-controller-architecture.md](./references/wifi-controller-architecture.md) | Wi-Fi controller architectures (centralized/distributed/cloud), CAPWAP/LWAPP, roaming, AP join, HA, hardening |
| [wifi-rf-security.md](./references/wifi-rf-security.md) | Wi-Fi RF planning: site surveys, coverage vs capacity, interference, AP physical security, antennas, rogue detection, guest isolation, jamming |
| [network-security-tools-ecosystem.md](./references/network-security-tools-ecosystem.md) | Tools: nmap, Zeek, Suricata, Wireshark, firewalls, VPNs, frameworks |

## Progressive Disclosure

| When you need... | Load this file |
|------------------|----------------|
| Fundamentals and standards | [network-security-fundamentals.md](./references/network-security-fundamentals.md) |
| Modern protocols and emerging trends | [modern-network-protocols.md](./references/modern-network-protocols.md) |
| Architecture and segmentation | [network-architecture-segmentation.md](./references/network-architecture-segmentation.md) |
| Zero Trust design | [zero-trust-architecture.md](./references/zero-trust-architecture.md) |
| SASE/SSE | [sase-and-sse.md](./references/sase-and-sse.md) |
| Firewalls and VPNs | [firewall-and-vpn-technologies.md](./references/firewall-and-vpn-technologies.md) |
| DNS | [dns-security.md](./references/dns-security.md) |
| TLS/PKI | [tls-and-pki.md](./references/tls-and-pki.md) |
| Hardening baselines | [network-hardening-baselines.md](./references/network-hardening-baselines.md) |
| Monitoring and detection | [network-monitoring-detection.md](./references/network-monitoring-detection.md) |
| Encrypted traffic analysis | [encrypted-traffic-analysis.md](./references/encrypted-traffic-analysis.md) |
| Detection engineering | [network-detection-engineering.md](./references/network-detection-engineering.md) |
| Threat hunting | [network-threat-hunting.md](./references/network-threat-hunting.md) |
| Forensics | [network-forensics.md](./references/network-forensics.md) |
| DDoS | [ddos-mitigation.md](./references/ddos-mitigation.md) |
| Attack trends | [network-attack-surface-trends.md](./references/network-attack-surface-trends.md) |
| Cloud/container networking | [cloud-container-networking.md](./references/cloud-container-networking.md) |
| Kubernetes networking | [kubernetes-network-security.md](./references/kubernetes-network-security.md) |
| Wireless/IoT/OT | [wireless-iot-ot-network-security.md](./references/wireless-iot-ot-network-security.md) |
| Wi-Fi enterprise hardening | [wifi-enterprise-hardening.md](./references/wifi-enterprise-hardening.md) |
| Wi-Fi controller architecture | [wifi-controller-architecture.md](./references/wifi-controller-architecture.md) |
| Wi-Fi RF security | [wifi-rf-security.md](./references/wifi-rf-security.md) |
| WPA3 protocol | [wifi-wpa3-protocol.md](./references/wifi-wpa3-protocol.md) |
| Wi-Fi 6/7 | [wifi-6-7-security.md](./references/wifi-6-7-security.md) |
| Wifite tooling | [wifi-wifite-tooling.md](./references/wifi-wifite-tooling.md) |
| WPA2 attacks | [wifi-wpa2-attacks.md](./references/wifi-wpa2-attacks.md) |
| Wi-Fi 802.1X/EAP/RADIUS | [wifi-8021x-eap-radius.md](./references/wifi-8021x-eap-radius.md) |
| Tools ecosystem | [network-security-tools-ecosystem.md](./references/network-security-tools-ecosystem.md) |

## Gotchas

1. **VLANs ≠ segmentation**: VLANs provide broadcast isolation only; enforce policy with firewalls/ACLs or microsegmentation.
2. **Security groups stateful, NACLs stateless**: both directions must be allowed in NACLs.
3. **NetworkPolicy is additive**: an allow in one policy cannot be overridden by a deny in another; default-deny requires a policy selecting the pod.
4. **TLS inspection tradeoffs**: breaks pinning, privacy/compliance concerns, performance; document exceptions.
5. **SPAN ports drop under load**: use TAPs for high-fidelity capture.
6. **OT safety first**: controls must not impair safety functions or real-time determinism.
7. **0-RTT replay risk**: never use QUIC 0-RTT for non-idempotent operations.
8. **eBPF privilege**: requires CAP_BPF/CAP_SYS_ADMIN; audit programs; rootkit risk.
9. **WireGuard UDP-only**: no TCP fallback; plan reachability.
10. **HTTP/2 Rapid Reset (CVE-2023-44487)**: rate-limit streams/resets or disable HTTP/2 where unnecessary.
11. **WPA3 transition mode membuka downgrade**: selama SSID masih menerima WPA2, klien dapat dipaksa turun; matikan mode transisi setelah inventaris klien selesai.
12. **PMF harus aktif di kedua sisi**: 802.11w yang hanya aktif di AP membuat klien lama gagal asosiasi — uji perangkat sebelum menegakkan.
13. **PMKID membuat serangan WPA2 clientless**: handshake tidak lagi diperlukan; PSK lemah dapat diuji offline dari satu frame. Mitigasi utama adalah frasa sandi panjang + WPA3/SAE.
14. **Wifite dan alat sejenis adalah alat uji berizin**: hanya pada jaringan milik sendiri atau dengan izin tertulis; deauth dan rogue AP mengganggu layanan dan dapat melanggar hukum.
15. **CAPWAP tidak mengenkripsi payload data klien secara default**: control channel DTLS opsional; jangan menganggap jalur AP–controller aman tanpa memeriksa konfigurasi.

## License

MIT
