---
name: "Network Architecture & Segmentation"
description: "Network segmentation and architecture patterns: traditional VLAN/ACL/DMZ, microsegmentation, Zero Trust (NIST SP 800-207), SASE/SSE, SD-WAN security, and service-mesh mTLS/SPIFFE, with east-west vs north-south traffic and selection criteria."
tags: [network-architecture, segmentation, vlan, acl, dmz, microsegmentation, zero-trust, nist-800-207, sase, sse, casb, swg, ztna, fwaas, sd-wan, service-mesh, mtls, spiffe, east-west, north-south]
---

# Network Architecture & Segmentation

Segmentation is the practice of dividing a network into zones or enclaves so that a compromise in one area cannot freely propagate. Modern architectures layer several approaches — traditional VLAN/ACL boundaries, microsegmentation, Zero Trust, SASE/SSE, SD-WAN, and service meshes — chosen by trust model, scale, and threat profile.

## East-West vs North-South Traffic

- **North-south** traffic crosses the perimeter: clients to services, users to the internet, site-to-site. It is the traditional focus of firewalls and DMZs.
- **East-west** traffic moves laterally inside the data center or cloud: service-to-service, pod-to-pod, VM-to-VM. It now dominates volume in microservices/cloud environments and is where most lateral movement occurs.

Design implication: north-south controls (edge firewalls, WAFs) alone cannot stop east-west lateral movement; internal enforcement (microsegmentation, service mesh) is required. East-west inspection must be low-latency and distributed, because centralizing it creates a bottleneck and single point of failure.

## Traditional Segmentation: VLANs, ACLs, DMZ

### VLANs

Virtual LANs (IEEE 802.1Q) partition a switched network into broadcast domains. Each VLAN is a separate L2 segment; inter-VLAN routing occurs at a router or L3 switch where policy can be applied. VLANs provide isolation of broadcast traffic and coarse grouping (e.g., users, servers, management, guests).

Limits: VLANs are L2 constructs. They do not encrypt, do not authenticate endpoints, and are bypassable if an attacker gains access to a trunk port or misconfigures a native VLAN. VLAN hopping (double-tagging, switch spoofing) is a known risk. VLANs alone are not segmentation without firewall enforcement between them.

### ACLs

Access Control Lists filter traffic by source/destination IP, port, protocol, and sometimes application. They are applied on routers, switches, host firewalls, and cloud security groups. Stateful ACLs track connections; stateless ACLs evaluate each packet independently.

Best practice: default-deny, explicit allow, least privilege, documented justification per rule, periodic review and removal of stale entries. ACLs scale poorly with hundreds of microservices and are coarse (IP/port), which is why microsegmentation and identity-based policy emerged.

### DMZ (Demilitarized Zone)

A DMZ is a semi-trusted zone hosting public-facing services (web, mail, DNS) between the untrusted internet and the trusted internal network. Traffic flows: Internet → edge firewall → DMZ (reverse proxy/WAF) → internal firewall → internal. The DMZ has no direct route to internal networks; only specific, inspected flows are permitted (e.g., DMZ web server → internal DB on a single port).

Design points: dual-homed or screened-subnet topologies; separate DMZ for different trust levels; no management interfaces exposed to DMZ; log all DMZ traffic; treat DMZ hosts as compromised-prone and harden them.

## Microsegmentation

Microsegmentation enforces policy at the workload level (host, container, or process) rather than at network boundaries, enabling fine-grained, dynamic control of east-west traffic.

### Host-based

Policy enforced by an agent on the endpoint (host firewall, eBPF, or endpoint protection). Strengths: follows the workload anywhere, precise process-level rules, no network re-architecture. Weaknesses: agent dependency, kernel compatibility, performance overhead, blind to encrypted traffic unless TLS is terminated locally.

### Network-based

Policy enforced by switches, hypervisors, or SDN controllers (distributed firewalls, NSX, ACI). Strengths: centralized visibility, no agent on guest OS. Weaknesses: tied to infrastructure, less granular than host-level, harder in multi-cloud/heterogeneous estates.

### Identity-based

Policy keyed on identity (user, service account, workload identity) rather than IP. This is the Zero Trust approach: access decisions use identity + device posture + context. It decouples policy from network location, enabling mobility and cloud. Requires robust identity infrastructure (IdP, SPIFFE/SPIRE, mTLS).

Microsegmentation gotchas: policy explosion (thousands of rules), visibility gaps before enforcement (need flow mapping first), breakage of legacy apps with hard-coded IPs, and the need for a phased rollout (monitor → alert → enforce).

## Zero Trust (NIST SP 800-207)

NIST SP 800-207 defines Zero Trust Architecture (ZTA): no implicit trust based on network location; every request is authenticated, authorized, and continuously evaluated.

### Core Components

- **Policy Engine (PE)** — computes the access decision using identity, device posture, threat intelligence, and policy. Produces allow/deny plus confidence.
- **Policy Administrator (PA)** — establishes/tears down the communication path (e.g., configures PEP, issues session credentials) based on PE decision.
- **Policy Enforcement Point (PEP)** — the gatekeeper that enables/blocks the session (gateway, agent, proxy, firewall). All traffic passes through a PEP.

Supporting: identity providers, device management (MDM/EDR), SIEM/analytics for continuous monitoring, and a trust algorithm that weights signals.

### Deployment Models

1. **Device agent / gateway (ZTNA client-to-app)** — agent on endpoint, gateway in front of app; user connects via encrypted tunnel; app not exposed to internet.
2. **Enclave / microsegmentation (network-based)** — gateways segment networks; workloads placed in enclaves with policy between them.
3. **Resource portal (browser-based, agentless)** — users access apps via an identity-aware proxy in the browser; no client install; good for contractors/BYOD.
4. **Hybrid** — combine models by use case (managed devices use agent; unmanaged use portal).

### Migration Approach

- Start with identity: centralize IdP, MFA, SSO, and device inventory.
- Map flows and data: identify critical assets and access patterns.
- Pilot ZTNA for a subset of apps/users; run in monitor mode first.
- Replace VPN remote access with ZTNA incrementally.
- Extend to internal east-west via microsegmentation.
- Continuous: tune policy, monitor, retire legacy trust assumptions.

Gotcha: "Zero Trust" is an architecture, not a product. Buying a ZTNA product without identity hygiene and flow visibility yields a false sense of security.

## SASE / SSE

SASE (Secure Access Service Edge) converges networking (SD-WAN) and security (SSE) into a cloud-delivered service. SSE (Security Service Edge) is the security half: CASB, SWG, ZTNA, FWaaS.

- **CASB (Cloud Access Security Broker)** — visibility and control over SaaS usage: shadow IT discovery, DLP, compliance, and access policies for cloud apps.
- **SWG (Secure Web Gateway)** — filters web traffic: URL filtering, malware inspection, SSL inspection, acceptable-use enforcement for all user traffic.
- **ZTNA (Zero Trust Network Access)** — identity- and context-based access to private apps, replacing VPN; apps are hidden from the internet.
- **FWaaS (Firewall as a Service)** — cloud-delivered firewall with consistent policy across sites and remote users.

Benefits: unified policy, reduced backhauling (users connect to nearest PoP), simpler branch operations, consistent security for remote workers. Tradeoffs: vendor lock-in, latency to PoP, inspection of encrypted traffic, and data-residency/sovereignty constraints.

## SD-WAN Security

SD-WAN abstracts WAN connectivity, using multiple transports (MPLS, broadband, LTE/5G) with dynamic path selection. Security considerations:

- Encrypt all overlay tunnels (IPsec/WireGuard) regardless of underlay; do not trust the internet path.
- Authenticate peers (certificates, PSK rotation); protect the SD-WAN controller (it is a high-value target).
- Segment overlays by tenant/class; enforce QoS and policy per overlay.
- Integrate with SSE/SASE for consistent security at branches.
- Monitor for controller compromise, route manipulation, and tunnel downgrades.
- Beware: centralized orchestration is a single point of compromise; secure management plane (MFA, RBAC, audit).

## Service Mesh (mTLS, SPIFFE)

A service mesh (Istio, Linkerd, Consul) manages service-to-service communication in Kubernetes/microservices, providing mTLS, traffic management, and observability.

- **mTLS** — mutual authentication and encryption between services; both sides present certificates. Prevents impersonation and eavesdropping east-west.
- **SPIFFE (Secure Production Identity Framework For Everyone)** — standard for workload identity via SVIDs (X.509 or JWT). **SPIRE** is the reference implementation that issues and rotates SVIDs. Identity is cryptographic and short-lived, not IP-based.
- Benefits: automatic cert rotation, fine-grained authorization policies, telemetry. Costs: sidecar proxy overhead (CPU/memory/latency), operational complexity, cert-management burden, and debugging encrypted traffic.

## Decision Criteria

| Requirement | Recommended Approach |
|-------------|----------------------|
| Coarse zone isolation, low cost | VLANs + L3 firewall/ACLs |
| Public-facing services | DMZ with screened subnet |
| Lateral-movement reduction in data center | Microsegmentation (host or network) |
| Remote access replacing VPN | ZTNA (SASE/SSE) |
| Cloud/SaaS visibility and control | CASB + SWG |
| Branch WAN with multiple transports | SD-WAN + integrated SSE |
| Microservices east-west security | Service mesh with mTLS/SPIFFE |
| Full Zero Trust program | Combine identity + ZTNA + microsegmentation + continuous monitoring |

Choose based on: trust model (perimeter vs Zero Trust), scale and number of workloads, cloud/multi-cloud footprint, legacy app constraints, skills/budget, and compliance (data residency, inspection mandates).

## Best Practices

- Default-deny between all zones; require documented justification for every allow.
- Enforce encryption on all paths, including east-west and underlay overlays.
- Base policy on identity, not IP, wherever feasible; use SPIFFE for workloads.
- Start segmentation with flow discovery and monitoring before enforcement.
- Centralize logging and correlate across network, identity, and endpoint.
- Phase rollouts: pilot, monitor, then enforce; keep rollback plans.
- Review and prune rules regularly; automate policy-as-code with CI/CD.
- Protect control/management planes with MFA, RBAC, OOB access, and audit.

## Gotchas

- VLANs alone are not segmentation; without firewall enforcement they are just broadcast domains.
- Microsegmentation without flow visibility causes outages; map first.
- Zero Trust products do not replace identity hygiene or patching.
- TLS inspection breaks certificate pinning and some apps; document exceptions.
- SASE PoP latency and data residency can violate compliance; validate regions.
- Service-mesh sidecars add latency and resource overhead; benchmark before full rollout.
- SD-WAN controllers are high-value targets; secure them as critical assets.
- Legacy apps with hard-coded IPs and no TLS break under identity-based policy.
