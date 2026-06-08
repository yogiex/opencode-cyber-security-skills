---
name: "Workload Security Posture"
description: "Container security philosophy, Pod Security Standards (Privileged/Baseline/Restricted), SecurityContext, admission control, sandboxing, and resource constraints."
tags: [pod-security, pss, psa, securitycontext, seccomp, apparmor, sandboxing, admission-control]
---

# Workload Security Posture

## Container Security Philosophy

Container bukan virtual machine — container berbagi kernel dengan host. Container escape = akses ke host kernel = akses ke semua container lain.

## Pod Security Standards (PSS)

| Profile | Filosofi | Use Case |
|---------|----------|----------|
| **Privileged** | "Trust but verify" — tidak ada pembatasan | System components, monitoring agents, network plugins |
| **Baseline** | "Known-safe defaults" — cegah privilege escalation | General workloads — kebanyakan apps |
| **Restricted** | "Assume breach" — heavily hardened | Sensitive workloads, multi-tenant, external-facing |

## SecurityContext: The Pod's Security Contract

| Field | Fungsi | Mindset |
|-------|--------|---------|
| `runAsNonRoot` | Cegah container sebagai root | "Apa alasan container perlu jadi root?" |
| `runAsUser` | Set UID spesifik | "User apa yang minimal diperlukan?" |
| `capabilities.drop` | Hapus Linux capabilities | "Linux capability apa yang TIDAK diperlukan?" |
| `readOnlyRootFilesystem` | Filesystem immutable | "Apa yang perlu di-write dan kenapa?" |
| `allowPrivilegeEscalation` | Cegah privilege escalation via setuid | "Apakah container perlu escalasi?" |
| `seccompProfile` | Filter system calls | "Syscall apa yang TIDAK diperlukan?" |

**Decision Framework:**
```
Untuk setiap container:
1. Apakah perlu root? → NO → runAsNonRoot: true
2. Apakah perlu write ke FS? → NO → readOnlyRootFilesystem: true
3. Apakah perlu Linux capabilities? → minimal → drop: ["ALL"], add: [specific]
4. Apakah perlu privilege escalation? → NO → allowPrivilegeEscalation: false
5. Apakah perlu semua syscall? → NO → seccompProfile: RuntimeDefault
```

## Admission Control

Admission controller adalah guardian at the gate — setiap request ke API server lewat sini.

| Tipe | Fungsi | Contoh |
|------|--------|--------|
| **Mutating** | Ubah request sebelum diproses | Inject default labels, sidecar, security context |
| **Validating** | Tolak request yang tidak sesuai policy | Cegah image dari registry tidak dikenal |

Kenapa admission control penting? RBAC bilang "siapa yang bisa create pods", admission control bilang "pods seperti APA yang boleh dibuat".

**Comparison: PSA Labels vs OPA Gatekeeper vs Kyverno**

| Kebutuhan | PSA Labels | OPA Gatekeeper | Kyverno |
|-----------|------------|---------------|---------|
| Enforce PSS profiles | ✅ Built-in | ✅ Via Rego | ✅ Via YAML |
| Custom policy logic | ❌ | ✅ Rego | ✅ YAML patterns |
| Mutation (auto-inject) | ❌ | Limited | ✅ Native |
| Complexity | Rendah | Tinggi | Rendah-Sedang |

**Decision:** PSA labels untuk PSS enforcement, OPA untuk complex policy, Kyverno untuk mutation.

## Sandboxing

| Approach | Isolasi | Overhead | Use Case |
|----------|---------|----------|----------|
| **No sandbox** (runc) | Namespaces + cgroups | Minimal | Trusted workloads |
| **gVisor** | User-space kernel | Syscall overhead | Multi-tenant, untrusted code |
| **Kata Containers** | Lightweight VM | VM boot time | High isolation, regulated |

## Resource Constraints as Security Control

| Kontrol | Fungsi Keamanan |
|---------|-----------------|
| `resources.limits.cpu` | Cegah CPU starvation |
| `resources.limits.memory` | Cegah memory exhaustion |
| `ResourceQuota` | Batasi total resource per namespace |
| `LimitRange` | Default limits untuk pod tanpa limit |

Resource exhaustion adalah DoS vector — setiap pod harus punya resource boundaries.

## Gotchas

- PSS Restricted profile cukup ketat — banyak container images siap pakai (termasuk yang official) mungkin tidak compliant
- Seccomp `RuntimeDefault` sudah cukup untuk sebagian besar workload — tidak perlu custom profile kecuali ada kebutuhan spesifik
- `allowPrivilegeEscalation: false` akan break container yang menggunakan setuid binaries
- PSA labels di namespace tidak retroaktif — hanya berlaku untuk pod yang dibuat setelah label diterapkan
- Sandboxing (gVisor/Kata) punya overhead performa signifikan — jangan digunakan untuk semua workload

## Best Practices

- Selalu set `runAsNonRoot: true` dan `readOnlyRootRootFilesystem: true` sebagai default
- Drop ALL capabilities, add hanya yang diperlukan
- Gunakan PSA labels di warn mode dulu sebelum enforce untuk lihat dampaknya
- Untuk minimum baseline, set `allowPrivilegeEscalation: false` dan `seccompProfile: RuntimeDefault`
