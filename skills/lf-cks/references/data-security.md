---
name: "Data Security at Rest & In Transit"
description: "etcd encryption (AES-CBC, Secretbox, KMS v1/v2), Secrets management, TLS/mTLS for data in transit, and encryption decision framework."
tags: [encryption, etcd, secrets, kms, tls, mtls, data-security]
---

# Data Security at Rest & In Transit

## Encryption Philosophy

Data di Kubernetes mengalir melalui tiga state:
- **At Rest** (stored) → Encryption at rest (etcd, storage)
- **In Transit** (network) → TLS/mTLS (ingress, mTLS)
- **In Use** (memory/CPU) → Limited control di K8s level

## Data at Rest: etcd Encryption

etcd adalah single source of truth — siapa pun yang bisa akses etcd bisa baca SEMUA data cluster.

| Provider | Kekuatan | Key Rotation | Performance |
|----------|----------|--------------|-------------|
| **AES-CBC** | 256-bit symmetric | Tidak auto-rotate | Fast |
| **Secretbox** | XSalsa20-Poly1305 | Tidak auto-rotate | Fastest |
| **KMS v1** (deprecated) | External key mgmt | Manual | Latency |
| **KMS v2** | External key mgmt, keyID, status | **Native rotation** | Latency |

**KMS v2 vs KMS v1:**

| Aspek | KMS v1 | KMS v2 |
|-------|--------|--------|
| Key ID visibility | Tidak ada | Key ID di metadata |
| Status reporting | Tidak ada | DEK status (rotated/pending) |
| Performance | Encrypt/Decrypt per API call | Encrypt write, decrypt read |
| Key rotation | Manual | Built-in |
| Status | **Deprecated** | Recommended |

## Secrets Management

**Keyakinan Salah vs Kenyataan:**
- "Secret sudah aman karena base64" → base64 = encoding, BUKAN encryption
- "Secret hanya bisa dibaca oleh yang punya akses" → RBAC bisa salah konfigurasi
- "Secret otomatis terproteksi" → Banyak komponen bisa baca Secret
- "Token cukup disimpan di Secret" → Long-lived, tidak bisa revoke per pod

**The Secret Lifecycle:**
```
Create → Store (etcd) → Mount → Use → Rotate → Delete
  │         │           │       │       │        │
  ▼         ▼           ▼       ▼       ▼        ▼
Encrypt   Encrypt     Bind    Read    Ganti   Hapus
at rest   at rest     ke Pod  dari    key &   expired
via KMS   via KMS     (volume) FS     redeploy
```

## Data in Transit: TLS dan mTLS

| Level | Melindungi | Implementasi |
|-------|------------|--------------|
| **Ingress → Service** | Traffic dari luar ke cluster | Ingress dengan TLS certificate |
| **Pod → Pod** | Internal traffic | Service mesh (Istio, Cilium) atau mTLS |
| **Node → Control Plane** | Kubelet → API Server | TLS certs (built-in) |
| **API Server → etcd** | Data sensitif di network | etcd TLS (built-in) |

Traffic internal tidak otomatis aman — di network yang compromised, semua traffic bisa disniff.

## Encryption Decision Framework

```
Apakah data ini sensitif?
├── Tidak perlu enkripsi → Kompresi saja
└── Ya → Tentukan state:
    ├── At Rest (etcd) →
    │   ├── KMS v2 (production, multi-cluster)
    │   └── AES-CBC/Secretbox (single cluster, low budget)
    ├── In Transit (network) →
    │   ├── Between clusters → mTLS
    │   ├── Internal K8s → Service Mesh
    │   └── External → Ingress TLS
    └── In Memory → (diluar scope K8s, aplikasi tanggung jawab)
```

## Gotchas

- Secret di Kubernetes hanya base64-encoded secara default — selalu enable encryption at rest
- KMS v1 sudah deprecated — gunakan KMS v2 untuk produksi
- etcd encryption hanya mengenkripsi data di disk, bukan di network — pastikan etcd TLS juga enabled
- Key rotation untuk AES-CBC/Secretbox memerlukan restart API server
- Secret yang sudah di-mount ke pod tidak otomatis terupdate setelah rotasi — pod perlu di-restart

## Best Practices

- Enable encryption at rest dengan KMS v2 untuk production cluster
- Gunakan external Secrets management (HashiCorp Vault, AWS Secrets Manager) untuk workload secrets
- Set `automountServiceAccountToken: false` untuk pod yang tidak perlu akses API
- Gunakan projected volume dengan `expirationSeconds` untuk ServiceAccount tokens short-lived
- Enable TLS untuk semua komponen control plane (API server, etcd, kubelet)
