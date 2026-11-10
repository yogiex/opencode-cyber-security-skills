---
name: "Referensi — Sumber Eksternal dan Bacaan Lanjutan"
description: "Sumber rujukan untuk platform security engineer Kubernetes: dokumentasi resmi Kubernetes, CIS Benchmark, tool supply chain/network/runtime, panduan hardening NSA/CISA dan NIST, OWASP, komunitas, serta catatan verifikasi."
tags: [references, sources, kubernetes, cis-benchmark, nist, owasp, tools, community]
---

# Referensi — Sumber Eksternal dan Bacaan Lanjutan

Daftar ini adalah sumber yang dipakai persona untuk memverifikasi klaim. Skill ini bukan salinan dokumen; bila detail teknis dibutuhkan, buka sumber aslinya.

> Catatan: tautan dapat berubah. Verifikasi ulang sebelum dipakai untuk keputusan perubahan cluster atau kepatuhan.

## 1. Sertifikasi dan cakupan

| # | Sumber | Kegunaan |
|---|---|---|
| 1 | [CNCF CKS](https://www.cncf.io/training/certification/cks/) | cakupan sertifikasi yang dipegang persona |
| 2 | [CNCF Curriculum](https://github.com/cncf/curriculum) | peta domain dan sub-domain, mengikuti rilis kurikulum |

Catatan: halaman di atas dipakai untuk mengetahui cakupan peran, bukan sebagai sumber teknis. Detail teknis selalu mengacu ke dokumentasi Kubernetes, CIS Benchmark, dan NIST di bawah.

## 2. Dokumentasi resmi Kubernetes

| # | Topik | URL |
|---|---|---|
| 3 | Security Docs | https://kubernetes.io/docs/concepts/security/ |
| 4 | Security Checklist | https://kubernetes.io/docs/concepts/security/security-checklist/ |
| 5 | Pod Security Standards | https://kubernetes.io/docs/concepts/security/pod-security-standards/ |
| 6 | Network Policies | https://kubernetes.io/docs/concepts/services-networking/network-policies/ |
| 7 | RBAC Authorization | https://kubernetes.io/docs/reference/access-authn-authz/rbac/ |
| 8 | Service Accounts | https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/ |
| 9 | Encryption at Rest | https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/ |
| 10 | KMS Provider | https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/ |
| 11 | Audit Logging | https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/ |
| 12 | AppArmor | https://kubernetes.io/docs/tutorials/security/apparmor/ |
| 13 | Seccomp | https://kubernetes.io/docs/tutorials/security/seccomp/ |
| 14 | SecurityContext | https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ |
| 15 | Admission Controllers | https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/ |
| 16 | Runtime Class | https://kubernetes.io/docs/concepts/containers/runtime-class/ |
| 17 | Supply Chain Security | https://kubernetes.io/docs/concepts/security/supply-chain-security/ |

## 3. CIS Benchmark

| # | Sumber | URL |
|---|---|---|
| 18 | CIS Kubernetes Benchmark | https://www.cisecurity.org/benchmark/kubernetes |
| 19 | CIS Benchmark PDF | https://workbench.cisecurity.org/benchmarks/12788 |

## 4. Tool keamanan

| # | Tool | URL |
|---|---|---|
| 20 | kube-bench (CIS scanner) | https://github.com/aquasecurity/kube-bench |
| 21 | Trivy (vulnerability scanner) | https://github.com/aquasecurity/trivy |
| 22 | Cosign (image signing) | https://github.com/sigstore/cosign |
| 23 | Syft (SBOM generator) | https://github.com/anchore/syft |
| 24 | Grype (vulnerability scanner) | https://github.com/anchore/grype |
| 25 | OPA Gatekeeper | https://github.com/open-policy-agent/gatekeeper |
| 26 | Kyverno (K8s policy engine) | https://github.com/kyverno/kyverno |
| 27 | Falco (runtime security) | https://github.com/falcosecurity/falco |
| 28 | Cilium (network + security) | https://github.com/cilium/cilium |
| 29 | Kubescape (security posture) | https://github.com/kubescape/kubescape |
| 30 | Tetragon (eBPF security) | https://github.com/cilium/tetragon |

## 5. Standar dan panduan hardening

| # | Sumber | URL |
|---|---|---|
| 31 | NSA/CISA Kubernetes Hardening Guide | https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.1_20220829.PDF |
| 32 | NIST SP 800-190 Container Security | https://csrc.nist.gov/publications/detail/sp/800-190/final |
| 33 | OWASP Kubernetes Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html |

## 6. Komunitas

| # | Komunitas | URL |
|---|---|---|
| 34 | CNCF Slack (#cks) | https://slack.cncf.io/ |
| 35 | Reddit r/kubernetes | https://reddit.com/r/kubernetes |
| 36 | K8s Security Discourse | https://discuss.kubernetes.io/c/security/ |

## 7. Cara memakai sumber

1. **Klaim teknis** — cek dokumentasi versi yang dipakai cluster, jangan mengandalkan ingatan.
2. **Angka dan versi** — sebut tanggal verifikasi dan sumbernya.
3. **Perubahan cepat** (CVE, field API, fitur CNI) — verifikasi ulang sebelum dipakai.
4. **Kutipan** — gunakan tautan asli, bukan ringkasan pihak ketiga bila memungkinkan.

## Best Practices

- Bedakan sumber primer (dokumentasi proyek/standar) dan sekunder (blog/ringkasan).
- Catat tanggal akses untuk klaim yang bergantung waktu.
- Jangan menyebarkan tautan yang tidak diverifikasi di laporan perubahan atau runbook.
- Perbarui daftar ini saat standar utama berubah.
