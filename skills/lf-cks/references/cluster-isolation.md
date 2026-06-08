---
name: "Cluster Isolation Model"
description: "Namespace isolation limits, multi-tenancy models (soft/hard/sandboxed), control plane vs data plane security, node-level isolation, and trust boundaries."
tags: [namespace, multi-tenancy, isolation, control-plane, data-plane, trust-boundary, node-isolation]
---

# Cluster Isolation Model

## Trust Boundaries & Attack Surface

```
External User → API → AuthN/AuthZ → Admission → Workload → Network → Storage → Runtime
```

Setiap panah adalah trust boundary — setiap boundary adalah titik di mana keamanan bisa gagal.

### Attack Vectors per Layer

**Supply Chain:** Compromised base image, dependency poisoning, unsigned image, CI/CD breach.
Mindset: Anggap semua image tidak trustworthy sampai diverifikasi.

**Cluster Infrastructure:** Unauthenticated API access, insecure etcd, Kubelet API terbuka, Dashboard exposed, cloud metadata accessible.
Mindset: Default K8s mengutamakan convenience di atas security — setiap komponen harus explicitly secured.

**Workload:** Container sebagai root, privileged container, HostPath volume, SA token di-mount, writable FS.
Mindset: Setiap container adalah potential breach.

**Network:** Flat network, egress tidak dibatasi, DNS spoofing, service tanpa TLS.
Mindset: Network policy bukan fitur optional — ini minimum requirement.

**Runtime:** No audit logging, no runtime detection, immutable violated, no syscall filtering.
Mindset: Detection adalah last line of defense.

## Namespace Isolation

Namespace adalah **unit organisasi logis**, BUKAN security boundary yang kuat.

| Dilindungi Namespace? | Ya | Tidak |
|----------------------|----|--------|
| Resource naming | ✅ | ❌ |
| Resource quotas | ✅ | ❌ |
| RBAC scoping | ✅ | ❌ |
| Network isolation | ❌ | ✅ Harus pakai NetworkPolicy |
| Cluster-wide resources | ❌ | ✅ ClusterRole lintas namespace |
| Pod security | ❌ | ✅ Tapi perlu admission controller |

**Mindset:** Namespace untuk organisasi, NetworkPolicy untuk isolasi.

## Multi-tenancy Models

| Model | Isolasi | Cocok untuk | Kompleksitas |
|-------|---------|-------------|-------------|
| **Soft multi-tenancy** | Namespace + RBAC + NetworkPolicy | Internal teams | Rendah |
| **Hard multi-tenancy** | Cluster terpisah | External customers | Tinggi |
| **Sandboxed** | gVisor/Kata per namespace | Untrusted workloads | Sedang |
| **Hierarchical** | vCluster, project namespaces | Enterprise | Tinggi |

Prinsip: Semakin banyak trust yang diberikan ke tenant, semakin kuat isolasi yang diperlukan.

## Control Plane vs Data Plane

```
Control Plane (Master Nodes):
  ├── API Server → Autentikasi + Otorisasi + Admission
  ├── etcd → Encryption at rest + network isolation
  ├── Scheduler → Pod spec validation
  └── Controller Manager → Reconciliation loops

Data Plane (Worker Nodes):
  ├── Kubelet → Node authentication
  ├── Container Runtime → Container isolation
  ├── kube-proxy → Network rules
  └── Pods → Workload execution
```

Mindset: Control plane adalah gatekeeper. Data plane adalah execution environment.

## Node-Level Isolation

| Aspek | Tanpa Isolasi | Dengan Isolasi |
|-------|---------------|----------------|
| Pod placement | Random | Node pool terpisah per tier |
| Container escape | Langsung ke host kernel | Sandboxed runtime |
| Resource contention | Semua compete | Dedicated node |
| Compliance | Satu node untuk semua | Node pool khusus |

Gunakan **node pool + taint/toleration** untuk isolate workload sensitif.

## Threat Modeling (STRIDE untuk K8s)

| Threat | K8s Contoh | Mitigasi |
|--------|------------|----------|
| **S**poofing | Anonymous auth → admin | x509 certs, OIDC |
| **T**ampering | Image diganti di registry | Image signing + verification |
| **R**epudiation | Pod dihapus tanpa jejak | Audit logging |
| **I**nformation Disclosure | Secret terbaca dari etcd | Encryption at rest |
| **D**enial of Service | Resource exhaustion | ResourceQuota, LimitRange |
| **E**levation of Privilege | Pod escape ke host | Seccomp, AppArmor, drop caps |

## Gotchas

- Namespace BUKAN security boundary — pod beda namespace bisa saling connect
- Multi-tenancy yang benar memerlukan kombinasi: RBAC + NetworkPolicy + PSA + ResourceQuota
- Control plane compromise = total cluster compromise — prioritaskan keamanan API server dan etcd
- Node affinity/taint digunakan untuk isolation, bukan security — container escape masih bisa terjadi

## Best Practices

- Gunakan soft multi-tenancy untuk internal teams, hard multi-tenancy untuk external customers
- Selalu gunakan taint + toleration untuk memisahkan workload berdasarkan trust level
- Blok akses ke metadata service (169.254.169.254) dengan NetworkPolicy ipBlock
- Implementasikan RBAC dengan prinsip least privilege untuk setiap ServiceAccount
