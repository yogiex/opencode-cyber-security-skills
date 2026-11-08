---
name: lf-cks
description: Certified Kubernetes Security Specialist (CKS) — Kubernetes security mindset, defense-in-depth framework, cluster isolation models, workload segmentation, supply chain trust, authentication & authorization philosophy, network security architecture, runtime protection, compliance posture, dan decision framework untuk securing container platforms. Berbasis CNCF CKS curriculum dan CIS Kubernetes Benchmark.
license: MIT
compatibility: opencode
metadata:
  audience: kubernetes-security
  workflow: hardening
  source: cncf-cks
  standard: cks
  year: "2026"
---

# CKS — Kubernetes Security Specialist Mindset

Kubernetes security bukan tentang command kubectl — ini tentang **memahami trust boundaries** dan **defense-in-depth** di cloud native world. Seorang KSS berpikir dalam layer: `User → API → AuthN/AuthZ → Admission → Workload → Network → Storage → Runtime`. Setiap panah adalah trust boundary.

| Domain | Weight | Mindset |
|--------|--------|---------|
| Cluster Setup | 15% | Memahami apa yang membuat cluster aman sejak awal |
| Cluster Hardening | 15% | Filosofi akses siapa punya apa |
| System Hardening | 10% | Konsep pembatasan proses di kernel |
| Minimize Microservice Vuln | 20% | Memahami isolasi workload |
| Supply Chain Security | 20% | Trust model dari dev sampai deploy |
| Monitoring/Logging/Runtime | 20% | Deteksi anomali dan investigasi |

## Decision Frame

1. Apakah context cluster sudah benar sebelum menjalankan perintah?
2. Apakah YAML sudah divalidasi dengan `kubectl apply --dry-run=server` sebelum diterapkan?
3. Apakah field berada di level yang benar (pod vs container) dan nama field-nya tepat?
4. Apakah ada jalur lebih cepat: `kubectl auth can-i --as`, `get events`, `crictl`, audit log?
5. Jika ragu, bisakah dokumentasi resmi dibuka dalam 30 detik?

Berhenti jika `apply` akan mengubah state tanpa backup manifest. Waktu ujian 2 jam untuk 15–20 task: kerjakan yang pasti dulu, verifikasi di pass ketiga.

> Angka ujian di skill ini (termasuk di `references/`) disalin dari [docs/CERTIFICATION-FACTS.md](../../docs/CERTIFICATION-FACTS.md) — diverifikasi 2026-11-08. Jika dokumen itu tidak tersedia di lingkunganmu, perlakukan angka ini sebagai snapshot dan periksa ulang ke sumber resmi sebelum dipakai untuk keputusan berbayar.

## Exam Format

Performance-based — 2 jam, 15–20 task, Kubernetes **v1.37**. Passing **67%**. Prasyarat: **telah lulus CKA** (status aktif tidak disyaratkan eksplisit). Biaya $445, valid 2 tahun, 1 retake. Dokumentasi: browser di VM (kubernetes.io/docs). Simulator: killer.sh (2 sesi × 36 jam, 17 soal/sesi).

## Strategi 3-Pass

**Pass 1 (30m):** Soal termudah — labels, namespace, simple RBAC, SA disable automount, Ingress TLS.
**Pass 2 (60m):** Soal medium-hard — NetworkPolicy, PSA enforcement, RBAC multi-step, Seccomp/AppArmor.
**Pass 3 (30m):** Soal terberat — Falco/audit analysis, supply chain tasks, verify semua task.

**Common Mistakes:** Lupa switch context, perfeksionis di satu soal, tidak test hasil kerja, lupa allow DNS di NetworkPolicy, mengubah komponen sistem.

## How to Use This Skill

| When you need to... | Load this file |
|---------------------|----------------|
| Understand RBAC, ServiceAccount, OIDC, auth methods | `references/auth-authz.md` |
| Secure pods with PSS, SecurityContext, seccomp, AppArmor | `references/workload-security.md` |
| Harden supply chain: signing, SBOM, SLSA, admission | `references/supply-chain.md` |
| Detect runtime threats with Falco, audit logs, crictl | `references/runtime-defense.md` |
| Design NetworkPolicy, micro-segmentation, egress, mTLS | `references/network-security.md` |
| Encrypt data at rest (etcd, KMS) and in transit (TLS) | `references/data-security.md` |
| Understand namespace isolation & multi-tenancy models | `references/cluster-isolation.md` |
| Apply CIS Benchmark, hardening, compliance | `references/compliance-hardening.md` |
| Browse all reference links (official, tools, communities) | `references/referensi.md` |

## Gotchas

- **Prasyarat CKA**: CKS hanya bisa diambil setelah **lulus CKA**. Halaman resmi tidak menyatakan bahwa status CKA harus masih aktif saat mendaftar — konfirmasi ke Linux Foundation sebelum membeli voucher, jangan mengandalkan asumsi.
- **Multiple contexts**: Soal tersebar di beberapa cluster — setiap soal menentukan context yang harus digunakan. Lupa switch context = jawaban di cluster salah.
- **NetworkPolicy DNS trap**: Saat menerapkan default-deny egress, DNS ke CoreDNS harus diizinkan. Tanpa ini, pod tidak bisa resolve service names.
- **PSA labels tidak retroaktif**: Label Pod Security Admission hanya berlaku untuk pod baru — pod existing tidak terpengaruh.
- **Immutable recovery**: Jangan repair container compromised — delete pod dan redeploy. Di K8s, recovery dari clean image memakan menit, bukan jam.
- **Seccomp ≠ AppArmor**: Seccomp membatasi syscalls, AppArmor membatasi file/network access. Keduanya komplementer, bukan substitusi.
- **KMS v1 deprecated**: Jangan gunakan KMS v1 untuk produksi baru — migrasi ke KMS v2 yang support native key rotation.

## Decision Framework — Security vs Operability

| Kontrol | Security Benefit | Operasional Cost | Kapan Worth It? |
|---------|-----------------|------------------|-----------------|
| Read-only root FS | High | Rendah | Selalu |
| Drop all capabilities | High | Rendah | Selalu |
| Seccomp RuntimeDefault | Medium | Minimal | Selalu |
| Pod Security Standards | High | Sedang | Semua production |
| NetworkPolicy | High | Sedang | Multi-tier apps |
| Image signing | High | Tinggi | Regulated, production |
| mTLS (service mesh) | High | Tinggi | Multi-service, sensitive data |
| Sandboxed runtime | Very High | Tinggi | Untrusted workloads |

**Risk = Likelihood × Impact.** Investasi keamanan proporsional dengan risk. Mulai dari audit mode, lalu enforce.

## Quick Reference — Key Commands

```bash
# RBAC test
kubectl auth can-i <verb> <resource> --as <user>

# Generate manifest
kubectl create <resource> --dry-run=client -o yaml

# Pod security
kubectl label ns <ns> pod-security.kubernetes.io/enforce=restricted

# NetworkPolicy test
kubectl run test --image=busybox -- sleep 3600
kubectl exec test -- wget -O- <service>:<port>

# Audit log check
kubectl logs kube-apiserver-<node> -n kube-system | grep -i forbidden

# Container runtime
crictl ps
crictl logs <container>
```

## License

MIT — see LICENSE file in repository root.
