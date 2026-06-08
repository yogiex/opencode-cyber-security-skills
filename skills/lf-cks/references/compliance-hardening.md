---
name: "Compliance & Hardening Posture"
description: "CIS Kubernetes Benchmark, hardening decision tree, kube-bench, security scorecard model, and component-level hardening guidance."
tags: [cis-benchmark, hardening, kube-bench, compliance, security-scorecard]
---

# Compliance & Hardening Posture

## CIS Kubernetes Benchmark

CIS (Center for Internet Security) Kubernetes Benchmark adalah standard industri untuk mengevaluasi security posture cluster.

| Section | Apa yang Diukur | Kenapa Penting |
|---------|-----------------|----------------|
| **Control Plane** | API Server, Controller Manager, Scheduler, etcd | Gatekeeper — jika compromised, cluster hilang |
| **Worker Nodes** | Kubelet, kube-proxy, node config | Execution environment — jika compromised, data hilang |
| **Policies** | RBAC, ServiceAccount, Pod Security | Access control — jika lemah, siapa pun bisa apa pun |
| **Data Protection** | Secrets, encryption, audit | Confidentiality — jika bocor, data exposure |

### Kategori Check CIS

| Kategori | Arti | Tindakan |
|----------|------|----------|
| **Scored** | Jelas impact keamanan — harus diperbaiki | Prioritaskan remediasi |
| **Not Scored** | Kontekstual — tergantung environment | Evaluasi manual |
| **Automated** | Bisa dicek dengan tool (kube-bench) | Gunakan tool |
| **Manual** | Perlu review manual | Dokumentasikan keputusan |

## Hardening: Reduce Attack Surface

| Komponen | Default | Hardened |
|----------|---------|----------|
| API Server | Profiling ON, anonymous auth ON | Profiling OFF, anonymous OFF |
| etcd | Default ports, no TLS auth | TLS auth, firewall, encryption |
| Kubelet | Anonymous auth ON (dulu) | Webhook auth, cert rotation |
| Dashboard | Exposed, cluster-admin | Disabled atau RBAC restricted |
| ServiceAccount | Token auto-mount | Disable yang tidak perlu |
| Container | Root user, privileged | Non-root, read-only, no caps |

**Prinsip:** "If you don't need it, remove it. If you can't remove it, restrict it."

## Hardening Decision Tree

```
Apakah komponen ini diperlukan?
├── TIDAK → Remove / Disable
└── YA → Apakah defaultnya aman?
    ├── YA → Verify dengan CIS check
    └── TIDAK → Konfigurasi secure:
        ├── Authentication → enable
        ├── Authorization → restrictive
        ├── Encryption → enable
        ├── Audit → enable
        └── Network → restrict
```

## Security Scorecard Model

```
Cluster Security Scorecard:
┌──────────────────────────────────┬───────┐
│ Domain                           │ Score │
├──────────────────────────────────┼───────┤
│ API Server Hardening             │ 8/10  │
│ RBAC Least Privilege             │ 7/10  │
│ Network Segmentation             │ 5/10  │ ❌
│ Pod Security                     │ 9/10  │
│ Supply Chain                     │ 4/10  │ ❌
│ Runtime Detection                │ 6/10  │
│ Data Encryption                  │ 8/10  │
│ Audit Logging                    │ 7/10  │
└──────────────────────────────────┴───────┘
```

Fokus pada area dengan skor terendah — itu adalah risk terbesar.

## Tools for Hardening

| Tool | Fungsi | Link |
|------|--------|------|
| kube-bench | CIS benchmark scanner | github.com/aquasecurity/kube-bench |
| kube-hunter | Vulnerability scanner | github.com/aquasecurity/kube-hunter |
| Kubescape | K8s security posture | github.com/kubescape/kubescape |
| KubeLinter | Static analysis | github.com/stackrox/kube-linter |
| Kubesec | Security risk analysis | github.com/controlplaneio/kubesec |

## Gotchas

- CIS benchmark bukan checklist mutlak — fail di satu check tidak berarti cluster tidak aman, tapi perlu justifikasi
- Scored checks harus diprioritaskan — not scored bersifat kontekstual
- kube-bench hanya mengecek konfigurasi — tidak bisa mendeteksi misconfig di admission policy atau RBAC
- Hardening tanpa memahami konsekuensi operasional bisa membreak aplikasi — testing diperlukan
- Setiap versi K8s memiliki CIS benchmark yang berbeda — gunakan versi yang sesuai

## Best Practices

- Jalankan kube-bench secara berkala (setiap cluster change atau minimal bulanan)
- Prioritaskan remediasi scored checks
- Dokumentasikan justifikasi untuk setiap not-scored check yang di-skip
- Gunakan Kubescape untuk holistic security posture assessment
- Implementasikan hardening secara bertahap — mulai dari control plane, lalu worker nodes, lalu policies
- Kombinasikan CIS benchmark dengan threat model spesifik organisasi
