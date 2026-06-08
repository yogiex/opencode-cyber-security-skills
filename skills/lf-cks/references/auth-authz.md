---
name: "Authentication & Authorization Framework"
description: "Kubernetes authentication methods (x509, OIDC, ServiceAccount), RBAC design patterns, anti-patterns, and API server access control."
tags: [authentication, authorization, rbac, serviceaccount, oidc, api-server]
---

# Authentication & Authorization Framework

## Authentication Methods

| Metode | Trust Model | Use Case | Risiko |
|--------|-------------|----------|--------|
| **x509 Client Certs** | Certificate Authority | Cluster admin, kubelet | Private key exposure |
| **Static Token** | Token file di disk | Bootstrap, legacy | Token tidak bisa di-revoke |
| **Bootstrap Token** | Short-lived token | Node join cluster | Exposure during join |
| **ServiceAccount Token** | Auto-mounted di pod | Pod → API communication | Token bisa dicuri dari pod |
| **OIDC** | External IdP | Integration with SSO | Dependency on external service |
| **Webhook Token** | External auth service | Custom authentication | Latency, availability |
| **Anonymous** | No auth | Tidak pernah untuk production | Siapa pun bisa akses |

## Authorization Modes

| Mode | Berbasis | Cocok untuk |
|------|----------|-------------|
| **RBAC** | Role + Binding | Hampir semua kasus (default) |
| **ABAC** | User attributes | Policy kompleks (tapi deprecated) |
| **Node** | Node identity | Kubelet authorization |
| **Webhook** | External decision | Custom authorization logic |

## RBAC Design

```
Users / Groups / ServiceAccounts
        │
        ▼
    Role / ClusterRole
  (verbs + resources + apiGroups)
        │
        ▼
RoleBinding / ClusterRoleBinding
(menghubungkan subject ke role)
        │
        ▼
   API Access Granted
```

### RBAC Anti-patterns

| Anti-pattern | Kenapa Berbahaya | Fix |
|-------------|------------------|-----|
| `*` wildcard verbs | Akses tak terbatas | Explicit verbs: `get, list, watch` |
| `cluster-admin` untuk semua | Blast radius maksimal | ClusterRole khusus per use case |
| SA ke cluster-admin | Pod akses penuh | Minimal Role, scoped ke namespace |
| Binding ke `system:authenticated` | Semua user login bisa | Spesifik ke user/group |
| `*` di apiGroups | Akses ke API groups tidak perlu | Sebutkan apiGroups eksplisit |

## ServiceAccount: The Overlooked Identity

| Masalah | Kenapa | Mindset |
|---------|--------|---------|
| **Auto-mount token** | Setiap pod punya token API | Container yang tidak perlu API — disable |
| **Default SA** | Semua pakai SA default — sulit audit | Buat SA dedicated per workload |
| **Long-lived tokens** | Token di Secret tidak expire | Projected volumes dengan short TTL |
| **No authz checks** | SA bisa akses tanpa RBAC | RBAC untuk SA yang perlu akses |

**Decision Framework:**
```
Apakah container perlu akses API K8s?
├── TIDAK → automountServiceAccountToken: false
└── YA → Apakah perlu akses spesifik?
    ├── YA → Buat SA + Role + RoleBinding
    └── TIDAK → Minimal Role dulu, audit setelahnya
```

## API Server Access Control

```
Request → API Server
   1. Authentication (who are you?)
   2. Authorization (what can you do?)
   3. Admission Control (should this be allowed?)
   4. Audit Logging (what happened?)
   5. etcd Storage (is it encrypted?)
```

Setiap langkah adalah opportunity to deny or log.

## Gotchas

- ServiceAccount token otomatis di-mount di setiap pod — selalu disable dengan `automountServiceAccountToken: false` untuk pod yang tidak perlu akses API
- RBAC `*` wildcard adalah musuh — gunakan explicit verbs dan apiGroups
- OIDC memerlukan external dependency — jika IdP down, cluster authentication bisa terganggu
- Node authorization mode hanya untuk kubelet — jangan digunakan untuk user

## Best Practices

- Gunakan ClusterRole untuk shared permissions, Role untuk namespace-specific
- Audit binding ke `cluster-admin` secara berkala
- Gunakan projected volume dengan `expirationSeconds` untuk ServiceAccount tokens
- Set `--anonymous-auth=false` di API server production
