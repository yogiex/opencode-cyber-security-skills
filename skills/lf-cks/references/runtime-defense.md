---
name: "Runtime Defense Framework"
description: "Behavioral vs signature-based detection, immutable container principle, audit logging levels, Falco runtime security, syscall analysis, and incident response for Kubernetes."
tags: [runtime, falco, audit-logging, detection, incident-response, crictl, forensics]
---

# Runtime Defense Framework

## Behavioral vs Signature-Based Detection

| Approach | Cara Kerja | Cocok untuk | Kelemahan |
|----------|------------|-------------|-----------|
| **Signature-based** | Mencocokkan pattern known attacks | Known malware, CVEs | Zero-day, polymorphic |
| **Behavioral** | Mendeteksi anomali dari baseline | Unknown threats, zero-day | False positives tinggi |

Runtime security di K8s menggunakan keduanya.

## The Immutable Container Principle

Container seharusnya immutable — sekali jalan, isinya tidak berubah.

```
Mutable: Attacker masuk → install tools → modify config → persist backdoor → compromised forever
Immutable: Attacker masuk → FS read-only → tools tidak bisa diinstall → restart = clean state
```

**Apa yang perlu di-write?** Temporary data → `emptyDir`. Logs → stdout. Secrets → projected volumes (read-only).

## Audit Logging

| Level | Detail | Volume | Use Case |
|-------|--------|--------|----------|
| `None` | Tidak dicatat | 0 | Health checks |
| `Metadata` | User, timestamp, resource, verb | Rendah | Compliance dasar |
| `Request` | Metadata + request body | Sedang | Forensic investigation |
| `RequestResponse` | Metadata + request + response | Tinggi | Full audit trail |

**What to audit:** Secret access (Metadata), Pod creation (Metadata), RBAC changes (Request), ClusterRole bindings (RequestResponse), anonymous requests (Metadata), 403 Forbidden (Metadata).

## Falco Runtime Security

Falco adalah CNCF runtime security tool yang mendeteksi anomali di container dan host.

**Key capabilities:**
- Syscall analysis (Linux kernel)
- Container drift detection (processes spawning, file changes)
- Kubernetes audit event detection
- Custom rule engine

## Container Runtime Security: Syscall Perspective

```
Legitimate Container:          Compromised Container:
├── read()                     ├── read()
├── write()                    ├── write()
├── open()                     ├── open()
├── close()                    ├── close()
├── socket()                   ├── socket() ← unexpected
├── bind()                     ├── bind()   ← unexpected
└── ...                        ├── ptrace() ← SUSPICIOUS!
                               ├── exec()   ← SHELL SPAWNED!
                               └── setuid() ← PRIVILEGE ESCALATION!
```

Semakin sedikit syscall yang diizinkan, semakin kecil attack surface.

## Incident Response untuk Kubernetes

| Aspek | Traditional | Kubernetes |
|-------|-------------|------------|
| **Unit investigasi** | Host/VM | Pod/Container |
| **Persistence** | Install tools | Read-only FS — tidak bisa persist |
| **Lateral movement** | SSH | API server → service account |
| **Evidence** | Hard drive, memory | Container logs, audit logs |
| **Containment** | Isolate host | Kill pod, cordon node |
| **Eradication** | Patch host | Delete pod, rebuild image |

### Forensic Artifacts

| Artifact | Lokasi | Penggunaan |
|----------|--------|------------|
| **Audit logs** | `/var/log/kubernetes/audit.log` | Siapa, apa, kapan ke API |
| **Container logs** | `kubectl logs` / `crictl logs` | Aplikasi output, error |
| **kubelet logs** | `journalctl -u kubelet` | Node-level events |
| **etcd snapshot** | Backup atau live | Semua resource cluster |

### Investigasi Container Compromise

```
Step 1: Identifikasi Pod — unexpected pods, unknown images, recent creation
Step 2: Cek Container — shell spawned? Suspicious processes? Network connections?
Step 3: Cek Audit Log — siapa create pod? Dari mana image pull?
Step 4: Containment — delete pod, cordon node, revoke credentials
```

### Immutable Recovery

```
Traditional: Investigate → Find malware → Clean → Patch → Test → Deploy (hours)
K8s Immutable: Identify → Delete pod → Redeploy from clean image → Done (minutes)
```

Jangan repair container compromised. **Bunuh dan ganti dengan yang baru.**

## crictl: Runtime Investigation

Ketika `kubectl` tidak cukup, `crictl` adalah interface langsung ke container runtime:

- `crictl ps` — list containers (include yang tidak visible via kubectl)
- `crictl logs <container>` — container logs
- `crictl exec <container> <cmd>` — execute command di container
- `crictl inspect <container>` — detailed container info

## Gotchas

- Audit logging level `Request` menghasilkan volume data besar — siapkan storage yang adequate
- Falco rule yang terlalu broad akan menghasilkan banyak false positive — tune secara bertahap
- Immutable container ≠ container tanpa logs — gunakan sidecar atau stdout
- `crictl` hanya bisa digunakan di node (SSH), bukan dari kubectl
- Di CKS exam, Falco rules biasanya sudah pre-installed — fokus pada analisis alert, bukan instalasi

## Best Practices

- Set audit logging ke `Metadata` sebagai minimum, `Request` untuk sensitive namespaces
- Gunakan Falco untuk behavioral detection di lingkungan production
- Implementasikan immutable container dengan `readOnlyRootFilesystem: true`
- Untuk incident response, selalu mulai dari audit logs untuk rekonstruksi timeline
- Gunakan `kubectl get events --all-namespaces` untuk deteksi awal anomali
