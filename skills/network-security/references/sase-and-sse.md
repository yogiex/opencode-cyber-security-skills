---
name: "SASE & SSE (Secure Access Service Edge)"
description: "SASE/SSE architecture: components (CASB, SWG, ZTNA, FWaaS), deployment models, SD-WAN integration, VPN migration, data residency, offline resilience, vendor evaluation, and best practices."
tags: [sase, sse, casb, swg, ztna, fwaas, sd-wan, vpn-migration, data-residency, zero-trust, secure-web-gateway, cloud-security]
---

# SASE & SSE (Secure Access Service Edge)

## Overview

SASE (Secure Access Service Edge), coined by Gartner (2019), converges SD-WAN networking and network security into one cloud-delivered service. SSE (Security Service Edge) is the security half — CASB, SWG, ZTNA, and FWaaS delivered from cloud PoPs. In short, **SASE = SSE + SD-WAN**. Security moves from data-center appliances to distributed points of presence (PoPs) near users, apps, and data, with policy driven by identity rather than network location. SASE is an architecture and delivery model, not a single product; most vendors offer subsets.

## SASE Definition and Core Attributes

Core attributes:

- **Cloud-native and globally distributed** — security functions run in PoPs near users and apps.
- **Converged network + security** — SD-WAN and SSE share one control plane and policy model.
- **Identity-centric policy** — decisions use user, device, app, and data context; location is not trusted by default.
- **Single-pass processing** — one engine applies all policies in one pass to reduce latency and avoid inconsistent enforcement.
SASE aligns with Zero Trust (NIST SP 800-207): never trust, always verify, enforce least privilege per session.

## SSE Components

### CASB (Cloud Access Security Broker)

Mediates between users and cloud services:

- **Discovery** of shadow IT and unsanctioned SaaS.
- **Risk scoring** of cloud apps and tenants.
- **Access control** — allow, block, coach, or limit (view-only, no download).
- **Data protection** — DLP for cloud, encryption/tokenization, watermarking.
- **Threat protection** — malware in cloud storage and collaboration tools.
- **Compliance** — audit trails for SOC 2, GDPR, HIPAA, PCI.

Modes: **API** (out-of-band, deep visibility into sanctioned SaaS), **inline** (proxy, real-time control, needs TLS inspection), **reverse proxy** (protects apps for unmanaged devices).

### SWG (Secure Web Gateway)

Filters and secures web traffic anywhere:

- URL/category filtering and acceptable-use enforcement.
- Malware scanning, file-type control, download sandboxing.
- SSL/TLS inspection (full or selective).
- DLP for web uploads and forms.
- Threat intelligence (IP/domain reputation, known-bad URLs).
- Remote Browser Isolation (RBI) for high-risk categories.

SWG operates as a cloud proxy with global PoPs; users connect via PAC files or an endpoint agent.

### ZTNA (Zero Trust Network Access)

Replaces VPN with per-application, identity- and context-aware access:

- Users get no network-level access; only specific apps after auth and authorization.
- Outbound-only tunnels from endpoint agent or site connector to the cloud broker; the app is never exposed to the internet.
- Continuous verification of identity, device posture, and context; sessions can be terminated mid-flight.
- **Client-based** (agent) for full TCP/UDP; **clientless** (browser) for web apps and contractors.

ZTNA hides app topology, shrinks attack surface, and limits lateral movement versus VPN.

### FWaaS (Firewall as a Service)

Cloud-delivered NGFW: stateful inspection, IPS/IDS, DNS filtering, application identification, TLS inspection, anti-malware, centralized policy across users, branches, and cloud workloads. Replaces or augments on-premises NGFW without hardware refresh.

## Architecture

### Single-Pass Unified Policy

Traffic enters the nearest PoP and one engine applies SWG, CASB, ZTNA, FWaaS, and DLP policy in a single pass — avoiding multiple decryption hops, reducing latency, and ensuring consistent enforcement and simpler auditing.

### PoPs, Backbone, and Connectors

- **PoPs**: globally distributed sites with compute for security; users connect via anycast to the nearest.
- **Backbone**: PoP-to-PoP private network; peering with AWS/Azure/GCP for low-latency cloud/SaaS access.
- **Connectors**: lightweight agents or gateways in customer networks/clouds that open outbound tunnels to PoPs, exposing private apps without inbound firewall rules.

### Traffic Flows

1. User → SaaS: user → PoP → policy → SaaS.
2. User → private app: user → PoP → connector → private app.
3. Branch → internet/SaaS: site CPE → PoP → destination (security at PoP).
4. Cloud workload → workload: workload → PoP/connector → policy → destination.
### TLS Inspection

SASE decrypts TLS at the PoP using a vendor or customer CA, inspects, then re-encrypts. Requires distributing the inspection CA to endpoints. Certificate pinning, client-cert auth, and QUIC may need bypass rules.

## Use Cases

Remote/hybrid workforce access without VPN; branch simplification (replace MPLS + on-prem firewall); M&A rapid connectivity; multi-cloud access; contractors/BYOD via clientless ZTNA/RBI; regulated-industry DLP and audit; IoT/OT restricted access; consistent SWG protection.
## Deployment Models

- **Single-vendor SASE**: one vendor for SD-WAN + SSE. Unified policy and console; risk of lock-in and a weaker side.
- **Dual-vendor (best-of-breed)**: separate SD-WAN and SSE integrated via APIs. Best components but integration complexity and policy sprawl.
- **SSE-only**: adopt SSE for users/remote access while keeping existing WAN; common first step.
- **Phased/hybrid**: start with ZTNA, add SWG/CASB, then FWaaS, then SD-WAN; coexist with legacy during migration.
- **Private/on-premises SASE**: deploy in customer DCs/private cloud for sovereignty/air-gapped; higher ops burden.

## Integration with SD-WAN

SD-WAN provides transport intelligence: path selection across MPLS/broadband/LTE, application-aware routing, QoS, failover. SASE steers traffic to the nearest PoP by app and policy.

- Tunnels: SD-WAN CPE to SASE PoPs (IPsec/GRE).
- Application-aware steering: SaaS to PoP, private apps via PoP, voice/video optimized paths.
- Unified policy: SD-WAN QoS + SASE security in one console (single-vendor) or via APIs.
- Local internet breakout: branch egress through SASE instead of backhauling to a DC.
- Failover: automatic transport failover with cached security policy.

Benefits: lower latency, reduced MPLS spend, consistent security, better UX. Watch tunnel overhead/MTU, interoperability, and policy sync.

## Migration from VPN

Traditional VPN grants network-level (flat) access, scales poorly, and enables lateral movement. Migration:

1. Inventory apps/users; classify private apps (web, SSH, RDP, SMB, custom TCP/UDP).
2. Identity foundation: SSO, MFA, device posture, group-based access.
3. Pilot ZTNA on a few low-risk web apps; validate UX and policy.
4. Migrate in waves: web (clientless) → TCP/UDP (client-based) → legacy via connectors/bastions.
5. Parallel run: VPN and ZTNA coexist; move users gradually; keep VPN for exceptions.
6. Enforce: disable VPN for migrated apps; monitor; revoke broad network rights.
7. Decommission VPN after validation; retain emergency access.

Considerations: apps assuming network trust may break; DNS across boundaries; split tunneling; PoP proximity/performance; training; rollback. ZTNA does not replace site-to-site — keep SD-WAN/IPsec for branch links.

## Data Residency

SASE processes traffic (including TLS decryption) in PoPs; payloads, logs, and metadata may cross jurisdictions.

- **PoP selection**: restrict processing to approved regions; configure steering.
- **Localization**: store logs, DLP incidents, metadata in-region.
- **Encryption**: TLS in transit; encryption at rest; customer-managed keys where supported.
- **Compliance**: GDPR, Schrems II, sovereignty laws, HIPAA, PCI; review DPAs and sub-processors.
- **Inspection boundaries**: TLS inspection of regulated data may be restricted; maintain bypass lists.
- **Log access**: define who can access logs; maintain audit trails.

Gotcha: by default, cloud SASE may route through non-compliant PoPs — configure and verify.

## Offline Resilience

When connectivity to a PoP or internet is lost:

- **Fail-open vs. fail-closed**: fail-open allows direct access (security risk); fail-closed blocks all (availability risk). Choose per risk tier.
- **Local caching**: SWG may cache policies and allow approved destinations; inspection/DLP may be skipped offline.
- **ZTNA**: cached tokens may permit short offline access; re-evaluate on reconnect.
- **SD-WAN**: automatic transport failover with cached policy.
- **Compensating controls**: EDR and local firewall protect when cloud enforcement is unreachable.
- **Monitoring**: alert on fail-open; review logs after restore.

Prefer fail-closed for high-risk users/data; ensure critical apps have an alternate path; test offline scenarios.

## Vendor Evaluation

Criteria: coverage (all SSE + SD-WAN; PoP count/locations; protocols TCP/UDP, QUIC, SSH, RDP, SMB); performance (PoP latency, throughput, TLS-inspection speed, backbone); security efficacy (detection, sandbox, threat intel, DLP accuracy, false positives); policy/management (unified engine, granularity, usability, API/automation, RBAC); identity integration (IdP SAML/OIDC, SCIM, device posture, MDM); compliance/residency (regional PoPs, SOC 2, ISO 27001, FedRAMP); client/agent (OS support, stability, clientless); support (onboarding, SLA, references); cost (per-user, bandwidth, egress, storage); lock-in (export, portability, openness).
Run a PoC with real traffic and apps; measure latency, false positives, UX; speak with same-industry references.

## Best Practices

- Start with identity and data-flow mapping; SASE without identity is just a proxy.
- Adopt SSE-first if WAN is stable; add SD-WAN where branch simplification pays off.
- Prefer single-vendor SASE when maturity allows; otherwise integrate with clear ownership.
- Enforce TLS inspection with bypasses for sensitive categories; manage CA certs.
- Use ZTNA per-app access; never grant network-level access; keep VPN only for exceptions.
- Implement DLP aligned to data classification; tune before blocking.
- Configure PoPs for residency; verify no unintended cross-border routing.
- Define offline fail-open/fail-closed per risk tier; monitor fail-open.
- Integrate with SIEM/SOAR; forward logs and alerts; automate response.
- Pilot small, iterate, and communicate changes; maintain rollback plans.
## Gotchas

- **"SASE in a box" marketing**: many vendors offer only SSE or only SD-WAN; verify convergence.
- **TLS inspection breaks apps**: pinning, QUIC/HTTP3, client-cert auth; maintain bypass lists.
- **PoP latency**: poor coverage increases latency; test from all user locations.
- **Agent sprawl**: multiple agents conflict; consolidate where possible.
- **Policy inconsistency**: different engines for web vs. private apps create gaps; prefer unified policy.
- **Residency defaults**: traffic may route through non-compliant PoPs unless configured.
- **Offline fail-open risk**: security bypass when disconnected; monitor and limit.
- **Migration complexity**: legacy apps assuming network trust may break; budget wrapping.
- **Cost surprises**: inspection, log storage, and egress can exceed base licensing.
- **Vendor lock-in**: proprietary policy formats hinder migration.

---

*Reference: Gartner SASE (2019) and SSE; vendor architectures; NIST SP 800-207.*