---
name: "Kubernetes Network Security"
description: "Kubernetes networking security: CNI selection, pod/Service/Ingress traffic, NetworkPolicy semantics and pitfalls, Cilium/eBPF policies, service mesh mTLS, and policy-as-code with OPA and Kyverno."
tags: [kubernetes, cni, pod, service, ingress, networkpolicy, cilium, ebpf, service-mesh, mtls, opa, kyverno, policy-as-code, dns, gateway-api]
---

# Kubernetes Network Security

## Overview

Kubernetes gives every pod its own IP in a flat space where, by default, any pod can talk to any other pod. That default is convenient and dangerous: one compromised pod can scan the whole cluster. Securing Kubernetes networking means choosing a policy-capable CNI, shrinking the allow-all default with NetworkPolicies, hardening Service and Ingress exposure, layering identity-based controls (Cilium/eBPF, service mesh mTLS), and enforcing admission-time policy-as-code (OPA, Kyverno). This reference covers each layer, the semantics that trip people up, and controls that hold up under attack.

## CNI Choices

The CNI plugin assigns pod IPs, wires veth pairs, programs routes on every node, and is the enforcement point for NetworkPolicy (and L7 policy/encryption in advanced plugins). Selection is a security decision.

| CNI | Data plane | NetworkPolicy | L7 policy | Encryption |
|-----|-----------|---------------|-----------|------------|
| Flannel | VXLAN/host-gw | No | No | No |
| Calico | BGP/VXLAN/eBPF | Yes (full) | Enterprise only | WireGuard |
| Cilium | eBPF | Yes (extended) | HTTP/gRPC/Kafka/DNS | WireGuard/IPsec |
| AWS VPC CNI | VPC ENIs | Via add-on | Via add-on | No |

Considerations: iptables-based plugins degrade at scale; eBPF (Cilium) avoids O(n) chains. Only plugins implementing the spec enforce NetworkPolicy—Flannel alone does not. eBPF needs Linux 5.4+ (5.10+ recommended) and a mounted BPF filesystem. CNI runs as a privileged DaemonSet; compromise equals node compromise—pin versions, verify images, restrict RBAC. VPC/Azure CNI consume real VPC IPs per pod; size subnets. If the CNI does not encrypt pod-to-pod traffic, east-west is plaintext—add WireGuard or a mesh.

> Standardize on one CNI. Mixing across node pools creates policy gaps and routing surprises.

## Pod Networking

- **Pod IP**: cluster-unique, from the CNI pool; containers in a pod share one namespace and reach each other over `localhost`.
- **Ephemeral**: pod IPs change on restart/reschedule. Never encode them in policy, DNS, or firewalls—use labels and Services.
- **DNS**: CoreDNS resolves `service.namespace.svc.cluster.local`; pods use `ndots:5`, which can amplify queries—tune `ndots` and use FQDNs with trailing dots.
- **hostNetwork / hostPort**: pods sharing the node's namespace bypass pod policy and collide on ports. Restrict via policy-as-code; reserve for infrastructure with justification.
- **Privileged pods / `NET_ADMIN` / `NET_RAW`**: can manipulate node networking and sniff traffic. Drop capabilities, use seccomp/AppArmor, avoid `privileged: true`.
- **Egress**: default egress is open—add egress NetworkPolicies and consider an egress gateway/proxy.

## Services and Ingress

### Services

Services provide a stable virtual IP (ClusterIP) over ephemeral backends, programmed by kube-proxy (iptables/IPVS) or eBPF (Cilium).

| Type | Exposure |
|------|----------|
| ClusterIP | Internal only |
| NodePort | Node IP + high port |
| LoadBalancer | External LB |
| ExternalName | DNS CNAME |
| Headless (`clusterIP: None`) | Pod IPs directly |

- **EndpointSlices** replace Endpoints for scale and topology-aware routing.
- **Session affinity** (`sessionAffinity: ClientIP`) pins clients; pair with health checks.
- **Source IP**: `externalTrafficPolicy: Local` preserves client IP but drops traffic with no local backend; `Cluster` SNATs to node IP.
- **Internal LB annotations** keep load balancers off the public internet.

### Ingress

Ingress resources define L7 host/path routing to Services, implemented by a controller (NGINX, Traefik, HAProxy, cloud ALB).

- Terminate TLS at the controller; store certs in Secrets or external secret managers. Enforce TLS 1.2+.
- WAF at the controller or cloud LB; rate limiting and bot management at the edge.
- **Gateway API** is the successor: role-oriented, richer matching, better multi-tenancy. Prefer for new workloads.
- Watch NGINX path traversal/rewrite pitfalls (`use-regex`, `rewrite-target`) and controllers with excessive privileges.

## NetworkPolicy

`NetworkPolicy` is the native L3/L4 firewall for pods. Key semantics:

- **Default allow-all**: with no policy selecting a pod, all ingress and egress are permitted.
- **Selection**: a policy applies to pods matching `spec.podSelector` (empty selector = all pods in namespace). Once *any* policy selects a pod for a direction, that direction becomes default-deny and only allowed traffic passes.
- **Additive**: multiple policies selecting the same pod are unioned (OR), not intersected. You cannot "subtract" an allow. Stacking only widens access.
- **policyTypes**: declare `Ingress` and/or `Egress`. If omitted, implementations may default to Ingress only—always set explicitly.
- **DNS allow**: egress default-deny breaks DNS unless you allow UDP/TCP 53 to kube-dns/CoreDNS.

### Default-deny baseline

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: app
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

### Allow app traffic plus DNS

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
  namespace: app
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
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns-egress
  namespace: app
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to:
    - namespaceSelector:
        matchLabels: { kubernetes.io/metadata.name: kube-system }
      podSelector:
        matchLabels: { k8s-app: kube-dns }
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
```

### ipBlock limitations

- `ipBlock` matches CIDRs only—no FQDNs, no named ports, no dynamic endpoints. Rotating IPs need an egress proxy or Cilium FQDN policy.
- `except` subtracts CIDRs only within the stated `cidr`.
- Cross-namespace traffic needs `namespaceSelector`; combining `podSelector` and `namespaceSelector` in one `from` entry is AND, separate items are OR.
- Named ports must match the pod spec port name—mismatches silently fail.
- No logging, counters, L7, or time-based rules in the core spec; enforcement depends on the CNI.

> Test policies with `kubectl exec` and a traffic generator (e.g., `nicolaka/netshoot`) before and after applying; a bad egress deny can break the app silently.

## Cilium and eBPF Policies

Cilium extends Kubernetes policy with identity-based enforcement and L7 awareness, backed by eBPF.

- **CiliumNetworkPolicy / CiliumClusterwideNetworkPolicy**: adds `toEntities` (world, cluster, host, remote-node), `toFQDNs`, `toServices`, and L7 rules (`toPorts.rules.http`, `kafka`, `dns`, `grpc`).
- **Identity**: policy keyed on pod labels (security identity), not IPs—survives rescheduling.
- **FQDN egress**: `toFQDNs` with `matchPattern` allows egress to external domains, enforced at DNS—solves ipBlock limits for SaaS.

- **Transparent encryption**: WireGuard (node-to-node) or IPsec; verify with `cilium encrypt status`.
- **Hubble**: flow observability and policy verdicts (`hubble observe --verdict DROPPED`).
- **kube-proxy replacement**: Cilium can replace kube-proxy via eBPF; requires `kubeproxy-replacement: strict`.
- **Requirements**: recent kernel, BPF filesystem, and (some features) `CAP_BPF`. Managed add-ons vary—verify before relying on L7.

```yaml
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: allow-api-egress
  namespace: app
spec:
  endpointSelector:
    matchLabels: { app: api }
  egress:
  - toFQDNs:
    - matchPattern: "*.example.com"
    toPorts:
    - ports:
      - port: "443"
        protocol: TCP
      rules:
        http:
        - method: GET
          path: "/v1/.*"
```

## Service Mesh mTLS

A service mesh (Istio, Linkerd, Consul) injects a sidecar proxy per pod for mTLS, traffic management, and telemetry.

- **Identity**: SPIFFE/SPIRE issues X.509 certs bound to workload identity (namespace + service account); mTLS authenticates peers cryptographically.
- **Istio PeerAuthentication**: `mode: STRICT` requires mTLS cluster-wide or per namespace; `PERMISSIVE` during migration.
- **AuthorizationPolicy**: L7-aware allow/deny (method, path, JWT claims, source principal) beyond NetworkPolicy's L4.
- **Linkerd**: lighter, auto-mTLS by default, simpler ops; fewer L7 features than Istio.
- **Ambient mesh (Istio)**: moves proxying to node-level ztunnels, removing sidecar overhead while keeping L4 mTLS; L7 via waypoint proxies.
- **Tradeoffs**: added latency (1-5ms), CPU/memory overhead, a control plane (istiod) that is a high-value target, cert rotation complexity.
- **Interaction**: mesh handles east-west mTLS; NetworkPolicy still needed for non-mesh traffic, node-level access, and defense in depth.

Set `mode: STRICT` cluster-wide or per namespace.

## Policy-as-Code (OPA / Kyverno)

Admission control enforces cluster-wide rules at create/update time, complementing runtime network policy.

- **OPA Gatekeeper**: ConstraintTemplates (Rego) + Constraints; validates resources; good for complex logic.
- **Kyverno**: Kubernetes-native YAML policies; validate, mutate, generate, cleanup. Lower barrier; supports image verification.
- **Network-relevant rules**: require a default-deny NetworkPolicy per namespace; forbid `hostNetwork`/`hostPort`; forbid `privileged` and `NET_RAW`.
- **Generate policies**: Kyverno can generate a default-deny NetworkPolicy on namespace creation.
- **CI integration**: run `conftest`/`kyverno apply` on manifests before merge.

_(Kyverno can generate the same default-deny policy on namespace creation.)_

## Common Pitfalls

- Default-deny egress without a DNS allow, breaking all name resolution.
- Stacking NetworkPolicies expecting intersection; they are additive (union).
- Using `podSelector` alone for cross-namespace traffic.
- Relying on `ipBlock` for external services with rotating IPs.
- Forgetting `policyTypes: [Egress]` and assuming egress is restricted.
- Treating a service mesh as a substitute for NetworkPolicy and node hardening.

## Best Practices

- Start every namespace with default-deny-all for ingress and egress, then add explicit allows.
- Use labels consistently; document the label contract for policy selection.
- Allow DNS explicitly and narrowly (to kube-dns/CoreDNS pods).
- Prefer Cilium/eBPF where kernel support allows, for L7 policy and observability.
- Enforce strict mTLS in the mesh for east-west.
- Gate cluster changes with OPA/Kyverno: require policies, forbid host networking and privileged pods.
- Generate default-deny policies on namespace creation (Kyverno).
- Validate manifests in CI (`conftest`, `kyverno apply`, `kube-score`) before admission.
- Test policies in staging with synthetic traffic before production rollout.

## Gotchas

- A NetworkPolicy with empty `podSelector: {}` selects **all** pods in the namespace, not "none".
- Combining selectors in one `from`/`to` entry is AND; separate array items are OR.
- `ipBlock.except` only refines the parent `cidr`.
- Named ports resolve at evaluation time against pod spec; a typo yields silent allow/deny.
- Policy changes can take seconds to propagate; tests right after apply may be flaky.

---

*Reference — Kubernetes Network Security.*