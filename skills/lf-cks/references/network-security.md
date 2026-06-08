---
name: "Network Security Architecture"
description: "Zero trust networking, NetworkPolicy design patterns, micro-segmentation, egress control, Cilium, mTLS, and service mesh for Kubernetes."
tags: [network-policy, cilium, mtls, service-mesh, zero-trust, egress, micro-segmentation]
---

# Network Security Architecture

## Zero Trust Networking

Network default di Kubernetes: **semua pod bisa bicara ke semua pod**. Ini maximum trust, bukan zero trust.

**Prinsip zero trust di K8s:**
1. Default deny — semua traffic diblok
2. Explicit allow — hanya traffic yang perlu diizinkan
3. Verify every connection — identity-aware policies
4. Least privilege — izinkan port dan protocol minimal

## NetworkPolicy Design Patterns

| Pattern | Deskripsi | Kapan Digunakan |
|---------|-----------|-----------------|
| **Default-deny all** | Blok semua ingress dan egress | Foundation untuk semua namespace |
| **Allow ingress from specific** | Izinkan traffic masuk dari pods tertentu | Service frontend hanya dari ingress |
| **Allow egress to specific** | Izinkan traffic keluar ke pods tertentu | Backend hanya ke database |
| **DNS allow** | Izinkan egress ke CoreDNS | Semua pods perlu DNS |
| **ipBlock except** | Blok IP range tertentu kecuali | Cegah akses ke metadata service |
| **Namespace selector** | Izinkan traffic dari namespace tertentu | Multi-tier apps |

**The DNS Trap:** Ketika menerapkan egress policy, DNS request ke CoreDNS di kube-system harus diizinkan. Tanpa ini, pod tidak bisa resolve service names.

## Micro-segmentation

```
┌──────────────────────────────────────────┐
│              Cluster                      │
│  ┌──────────────┐   ┌──────────────┐     │
│  │  Frontend     │   │  Backend      │     │
│  │  (DMZ)        │   │  (Internal)   │     │
│  │  - allow:80   │   │  - allow:8080 │     │
│  │  - ingress:   │   │  - ingress:   │     │
│  │    internet   │   │    frontend   │     │
│  │  - egress:    │   │  - egress:    │     │
│  │    backend    │   │    database   │     │
│  └──────────────┘   └──────┬───────┘     │
│                             │             │
│                    ┌────────▼──────┐     │
│                    │  Database     │     │
│                    │  (Restricted) │     │
│                    │  - ingress:   │     │
│                    │    backend    │     │
│                    │  - port: 5432 │     │
│                    │  - no egress  │     │
│                    └───────────────┘     │
└──────────────────────────────────────────┘
```

## Egress Control

Egress control sering diabaikan — fokus biasanya di ingress. Tapi egress adalah **exfiltration path**:

```
Attacker di Pod → Egress:
├── ke database → steal data (allowed)
├── ke internet → exfiltrate (should be blocked)
├── ke metadata service → cloud creds (blocked via ipBlock)
├── ke external C2 → command & control (blocked)
└── ke DNS → data encoding via DNS queries (hard to block)
```

## mTLS dan Service Mesh

| Approach | Complexity | Coverage | Management |
|----------|------------|----------|------------|
| **Manual mTLS** | Tinggi | Per service | Manual |
| **Service Mesh (Istio)** | Sedang | All traffic via sidecar | Automated |
| **Cilium** | Rendah | L3/L7 dengan eBPF | Automated |

**Decision Framework:**

| Kebutuhan | Native NetworkPolicy | Cilium | Service Mesh |
|-----------|---------------------|--------|--------------|
| L3/L4 segmentation | ✅ | ✅ | ✅ |
| L7 filtering | ❌ | ✅ | ✅ |
| Encryption | ❌ | ✅ (WireGuard) | ✅ (mTLS) |
| Observability | ❌ | ✅ (Hubble) | ✅ |
| Complexity | Rendah | Sedang | Tinggi |

**Decision:** Basic isolation → Native NetworkPolicy. Need encryption + observability → Cilium. Need L7 management + mTLS → Service Mesh.

## Gotchas

- NetworkPolicy default-deny akan memblok semua traffic termasuk DNS — selalu tambahkan rule untuk allow DNS ke CoreDNS
- Egress control sering dilupakan — padahal ini adalah jalur utama data exfiltration
- `ipBlock` tidak bisa digunakan bersama `podSelector` atau `namespaceSelector` dalam satu rule — harus dipisah
- NetworkPolicy bersifat additive — jika ada satu policy yang allow, traffic tersebut tetap diizinkan meskipun policy lain menolak
- Cilium L7 policies memerlukan CiliumNetworkPolicy CRD, bukan standard NetworkPolicy

## Best Practices

- Selalu mulai dengan default-deny di setiap namespace
- Gunakan label selectors yang spesifik — jangan terlalu broad
- Blok akses ke cloud metadata service (169.254.169.254) dengan ipBlock
- Untuk egress, izinkan hanya destination yang diperlukan
- Monitor network policy violations dengan audit logging
