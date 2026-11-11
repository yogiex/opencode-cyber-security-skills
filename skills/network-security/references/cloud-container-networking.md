---
name: "Cloud & Container Networking Security"
description: "Cloud primitives, shared responsibility, Kubernetes networking, multi-cloud/hybrid connectivity, cloud firewalls/WAF, misconfigurations, and zero trust for cloud-native defenses."
tags: [cloud, vpc, kubernetes, cni, cilium, ebpf, service-mesh, networkpolicy, waf, nat, load-balancer, zero-trust, multi-cloud, hybrid]
---

# Cloud & Container Networking Security

## Overview

Cloud and container platforms shift network control from physical devices to software-defined APIs. Security now depends on correct configuration of virtual networks, identity, and policy-as-code. This reference covers cloud primitives, shared-responsibility boundaries, Kubernetes networking, hybrid connectivity, edge protection, common misconfigurations, and zero trust in cloud.

## Cloud Primitives

### VPC and Subnets

A **Virtual Private Cloud (VPC)** is an isolated virtual network with its own CIDR block, route tables, and gateways. **Subnets** partition the VPC by availability zone and trust tier (public, private, data). Public subnets have a route to an internet gateway; private subnets route outbound via NAT. Place internet-facing load balancers in public subnets and workloads in private subnets.

### Route Tables

Route tables determine traffic paths. Each subnet associates with one route table. Key routes: `0.0.0.0/0` to internet gateway (public), `0.0.0.0/0` to NAT gateway (private), VPC peering CIDRs to peer connections, and transit gateway attachments. Implicit local route covers the VPC CIDR. **Gotcha**: a subnet with a route to an internet gateway is "public" regardless of naming.

### NAT

**NAT Gateway** (managed) or **NAT Instance** (self-managed) provides outbound internet access for private subnets without allowing inbound connections. NAT is stateful and scales per AZ; deploy one per AZ for HA. NAT does not protect against egress data exfiltration—combine with egress filtering and proxies.

### Load Balancers

- **Application Load Balancer (ALB)**: L7, HTTP/HTTPS, path/host routing, WAF integration, TLS termination.
- **Network Load Balancer (NLB)**: L4, TCP/UDP, static IP, ultra-low latency, preserves source IP.
- **Classic/Global**: legacy or cross-region anycast.

Terminate TLS at the LB for operational simplicity, or use end-to-end (passthrough) for regulated data. Enable access logs and health checks.

### Security Groups (SG)

Stateful virtual firewalls attached to ENIs/instances. Rules are allow-only (default deny inbound, allow outbound). Stateful: return traffic allowed automatically. Reference other SGs as sources for microsegmentation. Limits: ~60 inbound rules per SG. SGs are the primary enforcement point in most VPCs.

### Network ACLs (NACL)

Stateless subnet-level filters with numbered rules evaluated in order, plus an implicit deny. Support both allow and deny rules. Use NACLs for coarse subnet boundaries and explicit deny (e.g., block known bad IPs). Because they are stateless, you must allow ephemeral return ports.

### Comparison

| Control | Level | Stateful | Allow/Deny | Typical Use |
|---------|-------|----------|------------|-------------|
| Security Group | Instance/ENI | Yes | Allow only | Primary workload firewall |
| NACL | Subnet | No | Allow + Deny | Coarse boundary, explicit blocks |
| Route table | Subnet | N/A | N/A | Traffic steering |

## Shared Responsibility Model

Cloud security is split between provider and customer.

- **Provider**: physical data centers, host hardware, hypervisor, global network backbone, managed service internals.
- **Customer**: data classification, IAM, OS patching (IaaS), application security, network configuration (VPC, SG, NACL, routing), encryption key management, logging/monitoring.

The boundary shifts by service model: IaaS (customer manages most), PaaS (shared), SaaS (customer manages data/identity). **Misconfiguration is the customer's responsibility** and the leading cause of cloud breaches. Treat infrastructure-as-code and policy-as-code (OPA, Sentinel, AWS Config rules) as first-class controls.

## Kubernetes Networking

### CNI (Container Network Interface)

CNI plugins assign IPs and configure routes for pods. Common: Calico, Cilium, Flannel, Weave, AWS VPC CNI, Azure CNI. Choice affects performance, policy enforcement, and observability. CNI runs on every node; a compromised CNI can redirect all pod traffic.

### Pods and Services

- **Pod**: smallest deployable unit; gets a unique IP; containers share network namespace (localhost).
- **Service**: stable virtual IP (ClusterIP) fronting pods via kube-proxy (iptables/IPVS) or eBPF. Types: ClusterIP (internal), NodePort, LoadBalancer, ExternalName.
- **Headless Service**: no ClusterIP; returns pod IPs directly (for StatefulSets).
- **EndpointSlices**: scalable backend lists.

Pod IPs are ephemeral; never rely on them for policy—use labels and Services.

### Ingress

Ingress resources define L7 routing (host/path) to Services, implemented by an Ingress controller (NGINX, Traefik, HAProxy, cloud ALB). Ingress handles TLS termination, rewriting, and WAF integration. **Gateway API** is the newer, role-oriented successor with richer traffic management.

### NetworkPolicy

Kubernetes `NetworkPolicy` is the native L3/L4 firewall for pods. Default: all traffic allowed. Once any policy selects a pod, only explicitly allowed traffic passes. Policies are additive (union of allows). Limitations: most CNIs implement only pod/namespace selectors and ports; no FQDN, no L7, no logging in basic implementations. Use Cilium/Calico for richer policies.

Example:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels: { app: backend }
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels: { app: frontend }
    ports:
    - protocol: TCP
      port: 8080
```

### eBPF and Cilium

**eBPF** runs sandboxed programs in the kernel for high-performance packet processing, observability, and policy. **Cilium** uses eBPF to replace kube-proxy, provide identity-based (label) network policy, L7 (HTTP/gRPC/Kafka) policy, transparent encryption (WireGuard/IPsec), and Hubble for flow observability. eBPF reduces iptables overhead and enables kernel-level enforcement that survives userspace compromise—but requires kernel support and careful privilege management.

### Service Mesh

A service mesh (Istio, Linkerd, Consul) adds a sidecar proxy per pod for mTLS, traffic management, retries, and telemetry. **mTLS** provides strong service identity and encryption in transit. Tradeoffs: latency, resource overhead, operational complexity, and a new control plane to secure. Ambient mesh (Istio) reduces sidecar overhead using node-level proxies.

## Multi-Cloud and Hybrid Connectivity

- **VPN (IPsec/IKEv2)**: site-to-site tunnels over internet; cost-effective, higher latency, less predictable. Use for backup/low-bandwidth.
- **Direct Connect / ExpressRoute / Cloud Interconnect**: dedicated private circuits; lower latency, higher cost, SLA-backed. Preferred for production hybrid.
- **Transit Gateway / Cloud Router**: hub for VPC-to-VPC and on-prem connectivity; centralizes routing.
- **SD-WAN**: overlays multiple transports with policy-based path selection.
- **Service mesh federation / multi-cluster**: extend mTLS and policy across clusters/clouds.

Design for: asymmetric routing (avoid), MTU issues (1500 vs 9000, VXLAN overhead), overlapping CIDRs (use unique ranges per environment), and DNS resolution across boundaries (private zones, conditional forwarding).

## Cloud Firewall and WAF at the Edge

- **Cloud firewalls**: managed NGFW services (AWS Network Firewall, Azure Firewall, GCP Cloud Firewall) with stateful inspection, IPS, TLS inspection, and centralized policy. Deploy at VPC boundaries and transit hubs.
- **WAF**: protects HTTP/S apps from OWASP Top 10 (SQLi, XSS, RCE). Managed rule sets (AWS Managed Rules, OWASP CRS) plus custom rules. Deploy at ALB/CloudFront/API Gateway. Rate limiting, bot management, and geo-blocking are common additions.
- **DDoS protection**: AWS Shield, Azure DDoS Protection, GCP Cloud Armor. Combine with anycast and scrubbing.

Place WAF in front of every public endpoint; enable logging to SIEM; tune rules to reduce false positives before enforcing block mode.

## Common Misconfigurations

- **Public S3/Blob buckets** or overly permissive bucket policies exposing data.
- **Open security groups** (`0.0.0.0/0` on SSH/RDP/DB ports) on internet-facing instances.
- **Overly broad IAM roles** attached to compute (instance profiles with `*:*`).
- **Exposed Kubernetes API server** or etcd without auth/TLS.
- **Default service accounts** with cluster-admin bindings.
- **Secrets in env vars / container images** instead of secret managers.
- **Unrestricted egress** allowing data exfiltration and C2.
- **Missing NetworkPolicies** leaving pod-to-pod traffic flat.
- **Disabled flow logs** removing visibility.
- **Shared VPC peering** without segmentation, enabling lateral movement.
- **Stale load balancer listeners** pointing at decommissioned targets.

## Zero Trust in Cloud

Apply NIST SP 800-207 principles: no implicit trust based on network location. In cloud:

- **Identity as perimeter**: verify user/device/workload identity on every request (IAM, SPIFFE/SPIRE for workloads).
- **Microsegmentation**: SGs, NetworkPolicies, and service mesh mTLS enforce per-workload policy.
- **Continuous verification**: device posture, risk signals, session re-evaluation.
- **Least privilege**: scoped IAM, short-lived credentials, no long-lived keys.
- **Encryption everywhere**: TLS 1.3 in transit, encryption at rest, CMKs.
- **Visibility**: flow logs, audit logs, runtime detection (Falco, eBPF).

Zero trust is an architecture, not a product—requires identity, device, network, and data pillars.

## Best Practices

- Default-deny security groups; allow only documented flows; reference SGs, not CIDRs, where possible.
- Put workloads in private subnets; expose only via load balancers/WAF.
- Enable VPC Flow Logs and Kubernetes audit logs; ship to SIEM.
- Use IaC + policy-as-code (OPA/Conftest, Checkov, tfsec) in CI/CD.
- Implement NetworkPolicies with default-deny per namespace.
- Use Cilium/eBPF for L7 policy and observability where supported.
- Enforce mTLS in service mesh for east-west traffic.
- Segment by environment (dev/stage/prod) with separate accounts/projects.
- Rotate and scope credentials; prefer workload identity over static secrets.
- Test failover, backup restore, and incident response regularly.

## Gotchas

- A subnet is "public" if its route table points to an internet gateway—naming doesn't matter.
- Security Groups are stateful but NACLs are stateless; forgetting return ports in NACLs breaks traffic.
- Kubernetes NetworkPolicy is allow-list only and additive; a missing policy means allow-all.
- Pod IPs change; policies must use labels, not IPs.
- eBPF requires recent kernels and can conflict with other kernel modules.
- Service mesh sidecars add latency and can become a bottleneck; profile before rollout.
- NAT Gateways are per-AZ; cross-AZ traffic incurs cost and latency.
- Overlapping CIDRs break peering and VPN routing—plan address space early.
- WAF in count mode doesn't block; confirm mode before declaring protection.
- Cloud provider default VPCs are often overly permissive; create custom VPCs.
- Flow logs have cost and sampling; tune retention and filters.
- "Zero Trust" products without identity/workload verification are marketing.

---

*Reference — Cloud & Container Networking Security.*
