---
name: "Zero Trust Architecture (NIST SP 800-207)"
description: "NIST SP 800-207 zero trust architecture: principles, Policy Engine/Administrator/Enforcement Point, trust algorithms, deployment models, migration phases, identity and device posture, continuous verification, data flow mapping, and legacy coexistence."
tags: [zero-trust, nist-sp-800-207, zta, policy-engine, policy-administrator, pep, trust-algorithm, ztna, microsegmentation, continuous-verification, identity, device-posture, data-flow-mapping, legacy-coexistence]
---

# Zero Trust Architecture (NIST SP 800-207)

Zero Trust Architecture (ZTA) is a cybersecurity paradigm defined by NIST SP 800-207 (2020) that eliminates implicit trust based on network location. In a traditional perimeter model, any subject inside the trusted network is granted broad access; in ZTA, **no subject, device, or network segment is inherently trusted**. Every access request to a resource is authenticated, authorized, and continuously re-evaluated regardless of where the request originates.

## Core Principles (NIST SP 800-207)

NIST articulates the following foundational principles:

1. **All data sources and computing services are resources** — networks, devices, APIs, SaaS, data stores, not just servers behind a firewall.
2. **All communication is secured regardless of network location** — no trust from internal subnet; TLS, mutual auth, encryption everywhere.
3. **Access is granted per-session, per-resource** — authorization per request/session to a specific resource, not standing network access.
4. **Access determination is dynamic** — policy uses identity, device posture, behavioral/environmental context; can change mid-session.
5. **The enterprise monitors and measures integrity and security posture** — asset inventory, patch state, config, vuln data feed decisions.
6. **Authentication and authorization are strictly enforced before access** — no resource reachable without a policy decision; default-deny at PEP.
7. **The enterprise collects and uses telemetry to improve security posture** — logs/analytics/feedback refine policies and detect anomalies.

> Note: "Zero Trust" is an architecture/strategy, not a product; it needs identity, device, network, and data planes together.

## Core Components

ZTA separates decision-making from enforcement into three logical components.

### Policy Engine (PE)

The Policy Engine is the brain of ZTA. It evaluates access requests against enterprise policy and external inputs (threat intelligence, CISA KEV, identity providers, device management, SIEM) and produces a **grant/deny/step-up** decision. The PE is the only component that "decides"; it holds no direct network path to resources. Decisions are typically expressed as allow/deny plus conditions (e.g., require MFA, restrict to read-only, limit session duration).

### Policy Administrator (PA)

The Policy Administrator executes the PE's decision by establishing and terminating the session between subject and resource. It issues session-specific credentials/tokens, configures the Policy Enforcement Point (e.g., opens a micro-tunnel, injects allow rules, provisions a short-lived certificate), and tears them down on expiry or revocation. The PA is the "actuator" of the decision; it does not itself evaluate policy.

### Policy Enforcement Point (PEP)

The PEP is the gatekeeper placed in front of (or inline with) the resource. It intercepts every access request, forwards context to the PE/PA, and enforces the resulting decision: allowing the session, denying it, or redirecting to an authentication/step-up flow. PEPs can be agents, gateways, proxies, or embedded in the resource. A resource should have **no alternate network path** that bypasses its PEP.

## Trust Algorithm

The trust algorithm is the logic the PE uses to compute a trust score/decision. Typical inputs:

- **Subject identity** — user/service account, auth strength, group/role.
- **Device posture** — managed/unmanaged, patch level, EDR health, encryption, jailbreak/root.
- **Behavioral/context signals** — geo-velocity, impossible travel, time of day, request rate, volume.
- **Resource sensitivity** — target classification (public, internal, confidential, regulated).
- **Threat intelligence** — known-bad IPs, compromised creds, active campaigns.
- **Environmental context** — network type, IP reputation, TLS posture.

The algorithm combines these into a decision that may be binary (allow/deny) or graduated (allow read-only, require step-up MFA, quarantine device). Decisions are **re-evaluated continuously** during the session, not only at login; a drop in trust (e.g., device becomes non-compliant) can terminate or downgrade access mid-session.

## Deployment Models

NIST SP 800-207 describes several deployment patterns; most enterprises combine them.

### Device Agent / Gateway-Based

A lightweight agent on the endpoint plus a gateway (cloud/on-prem) in front of resources. The agent collects posture/identity; the gateway enforces policy and brokers connections (often outbound-only tunnel). Common for remote access and SaaS/SSH/RDP replacement. Strength: strong device posture; weakness: agent deployment/maintenance.

### Enclave-Based (Microsegmentation)

Resources are grouped into small "enclaves" (workloads, VLANs, service meshes) protected by PEPs. East-west traffic between enclaves needs policy approval. Implemented via host firewalls, service mesh mTLS, or SDN. Strength: limits lateral movement; weakness: boundary/policy complexity.

### Resource Portal (Broker)

A portal/gateway brokers access to resources without exposing them directly; users authenticate to the portal, which then proxies to the backend. The backend is never directly reachable. Common for legacy apps and web resources. Strength: works without agents on endpoints and hides resource topology; weakness: portal becomes a critical chokepoint and potential single point of failure.

Other patterns include **software-defined perimeter (SDP)** and **SASE** (Secure Access Service Edge), which converge networking and security in the cloud. Many real deployments are hybrids.

## Migration Phases

ZTA is adopted incrementally; a typical phased migration:

1. **Inventory and baseline.** Catalog resources, data, identities, devices, and flows; establish authoritative sources (IdP, MDM/UEM, CMDB).
2. **Identity foundation.** Centralize identity (SSO, MFA, lifecycle), eliminate shared accounts, govern service accounts.
3. **Device posture.** Deploy MDM/UEM and EDR; define compliance policies; quarantine non-compliant devices.
4. **Pilot PEPs on low-risk resources.** Put a small set of resources behind a PEP; validate logging, UX, and policy tuning.
5. **Expand to high-value resources.** Migrate sensitive datastores, admin interfaces, and production workloads; add microsegmentation.
6. **Continuous verification and optimization.** Tune trust algorithms, automate response (SOAR), measure KPIs, retire legacy VPNs/flat networks.
7. **Decommission legacy perimeter.** Remove broad VPN access, flatten exceptions, default-deny residual paths.

Each phase should include change management, user communication, and rollback plans; avoid big-bang cutovers.

## Identity and Device Posture

Identity is the new perimeter. Key practices:

- **Strong, phishing-resistant auth** (FIDO2/WebAuthn, smart cards) for users; cert/workload identity (SPIFFE/SPIRE, mTLS) for services.
- **Least privilege and JIT access** — time-boxed elevation over standing admin rights.
- **Device compliance** — managed, patched, encrypted, EDR-healthy; unmanaged get reduced access (browser-only).
- **Non-human identities** — service accounts/APIs/workloads need lifecycle, rotation, scoping.
- **Identity governance** — periodic reviews, deprovisioning on role change, separation of duties.

Measure posture continuously; drift triggers re-auth or session termination.

## Continuous Verification

ZTA requires ongoing evaluation rather than a single login gate:

- **Session re-evaluation** — re-check identity, device, and context at intervals or on risk signals.
- **Behavioral analytics (UEBA)** — detect anomalous access patterns; feed trust scoring.
- **Micro-segmentation enforcement** — re-validate every flow, not just the initial connection.
- **Revocation** — immediate session kill on compromise, device loss, or policy violation.
- **Telemetry feedback** — PEP/PE logs feed SIEM and policy tuning; closed loop.

## Data Flow Mapping

Before enforcing policy, map how data actually moves:

- **Identify resources and data classes** (PII, PHI, PCI, secrets) and their locations.
- **Map subjects to resources** — who/what accesses what, via which protocols.
- **Document trust boundaries and chokepoints** — where PEPs fit with least disruption.
- **Find shadow paths** — direct DB access, shared creds, legacy VPNs, SSO bypass.
- **Prioritize by risk** — start where sensitivity × exposure is highest.

Data flow mapping is often the most valuable step; it reveals access perimeter controls never saw.

## Coexistence with Legacy Systems

Few enterprises can replace everything at once. Strategies for coexistence:

- **Wrap, don't rewrite** — put legacy apps behind a portal/PEP to inherit ZT controls without code changes.
- **Segmentation + allowlists** — quarantine legacy systems in enclaves with strictly defined, monitored flows.
- **Compensating controls** — where PEP insertion is impossible (embedded/OT), use enhanced monitoring, jump hosts, time-limited access.
- **Identity bridging** — federate legacy auth (LDAP/Kerberos) into the modern IdP; avoid long-lived shared creds.
- **Phased retirement** — maintain an exception register with owners/expiry; review quarterly.
- **Avoid "ZT washing"** — labeling a legacy VPN "zero trust" without per-resource policy gives false assurance.

## Best Practices

- Start with identity and data flow mapping; technology comes after understanding.
- Enforce default-deny with explicit allow policies per resource.
- Use phishing-resistant MFA and short-lived, session-scoped credentials.
- Keep PEPs as the only path to resources; eliminate bypass routes.
- Automate posture collection and policy decisions.
- Log all access decisions at PEP/PE/PA; feed SIEM for detection/audit.
- Pilot on a small, low-risk set; iterate before broad rollout.
- Measure outcomes: MFA coverage, non-compliant access rate, mean time to revoke.
- Align with compliance frameworks (NIST 800-53, CIS, ISO 27001); document exceptions.

## Gotchas

- **"Zero Trust product" myth** — a ZTNA tool alone isn't an architecture; without identity, posture, and policy it's a VPN rebrand.
- **Agent sprawl / unmanaged devices** — contractors/BYOD may lack agents; design reduced-access paths (browser isolation) instead of exempting.
- **Legacy app incompatibility** — apps assuming network trust break under ZT; budget refactoring or portal wrapping.
- **Overly coarse policies** — grouping too many resources recreates flat-network risk; aim per-resource granularity.
- **Performance/latency** — inline PEPs add hops; benchmark and place enforcement near users (edge/SASE).
- **Certificate/key management** — mTLS/ZT at scale demands robust PKI; expired certs cause outages.
- **User friction** — repeated MFA erodes adoption; use risk-based step-up and device trust.
- **Incomplete data flow maps** — undocumented paths become blind spots; invest in discovery.
- **OT/IoT/embedded** — may not support agents or modern auth; use compensating controls and isolated enclaves.
- **Vendor lock-in** — proprietary policy formats hinder portability; prefer open standards.

---

*Reference: NIST SP 800-207 (2020), "Zero Trust Architecture."*