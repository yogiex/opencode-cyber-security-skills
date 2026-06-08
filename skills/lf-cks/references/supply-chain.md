---
name: "Supply Chain Trust Model"
description: "Container supply chain security including image signing (Cosign), SBOM, SLSA framework, admission control for supply chain, and attack vectors."
tags: [supply-chain, image-signing, cosign, sbom, slsa, admission-control, registry]
---

# Supply Chain Trust Model

## The Software Supply Chain

```
Source Code → Build → Artifact → Registry → Deploy → Runtime
    │           │         │          │         │        │
    ▼           ▼         ▼          ▼         ▼        ▼
  Code      Build      Image      Image     Admission Runtime
  Review    Security   Signing    Scanning  Control   Monitoring
  SAST      SBOM       Cosign/    Trivy     Verify    Falco
  SCA       Sigstore   Notary     Grype     Policy    Audit
```

Setiap link adalah opportunity for compromise.

## Trust Models

| Model | Filosofi |
|-------|----------|
| **TOFU (Trust on First Use)** | "Pertama kali percaya, setelahnya selalu percaya" |
| **Verify Every Time** | "Jangan pernah percaya tanpa verifikasi" |

CKS mindset: **Verify Every Time**.

## Image Integrity vs Provenance

| Konsep | Artinya | Contoh |
|--------|---------|--------|
| **Integrity** | Image tidak diubah sejak build | SHA256 digest, signing |
| **Provenance** | Image berasal dari source legitimate | SBOM, signed commit, CI/CD attestation |

## SBOM (Software Bill of Materials)

SBOM adalah inventaris semua komponen dalam image.

**Ada di SBOM:** OS packages, library dependencies, language runtimes, known versions.
**Tidak Ada:** Source code, business logic, config files, runtime behavior.

**Kenapa penting?** Ketika CVE baru keluar → cek image mana yang terpengaruh.

## Image Signing

```
Developer sign image dengan private key
        ↓
Registry menyimpan signature
        ↓
K8s cluster verify dengan public key
        ↓
Admission controller cek signature sebelum deploy
```

**Kenapa signing diperlukan?** Tag bisa di-push ulang, registry bisa compromised, MitM antara registry dan cluster.

## Admission Control untuk Supply Chain

| Policy | Cegah | Implementasi |
|--------|-------|--------------|
| **Allowed registries only** | Pod dari registry tidak dikenal | ImagePolicyWebhook, OPA, Kyverno |
| **Signed images only** | Image tidak diverifikasi | Cosign + admission controller |
| **No latest tag** | Image tag tidak stabil | OPA/Kyverno pattern matching |
| **Specific digest only** | Image tanpa hash spesifik | Image dengan `@sha256:...` |
| **Scan results gating** | Image dengan critical vuln | Trivy + webhook |

## Supply Chain Attack Vectors

| Attack | Tahap | Mitigasi |
|--------|-------|----------|
| Dependency confusion | Build | Pinned versions, private registry mirror |
| Typosquatting | Build | SBOM + vulnerability scanning |
| Compromised base image | Build | Multi-stage build + minimal base |
| Registry poisoning | Registry | Image signing + verification |
| Tag mutability | Registry | Gunakan digest (`@sha256`) |
| CI/CD pipeline breach | Build | Short-lived tokens, signed attestations |

## SLSA Framework

| Level | Artinya | Di K8s |
|-------|---------|--------|
| **SLSA 1** | Build process documented | Dockerfile + README |
| **SLSA 2** | Signed provenance + hosted build | Signed images, CI/CD |
| **SLSA 3** | Hardened build, no user influence | Reproducible builds, hermetic |
| **SLSA 4** | Two-party review + hermetic | Full audit trail, signed every step |

Target minimum production: **SLSA 2**.

## Gotchas

- `latest` tag tidak bisa dipercaya — selalu gunakan digest (`@sha256:...`) di production
- Image signing bukan solusi "set and forget" — key management adalah tanggung jawab berkelanjutan
- SBOM harus di-generate saat build, bukan setelahnya — SBOM retrospektif tidak akurat
- Admission controller untuk supply chain hanya efektif jika menjadi satu-satunya pathway ke cluster

## Best Practices

- Gunakan distroless base images untuk mengurangi attack surface
- Implementasikan multi-stage builds untuk menghilangkan build tools dari final image
- Integrasikan Trivy atau Grype ke pipeline CI/CD untuk scanning otomatis
- Gunakan Cosign untuk signing image di pipeline build
- Enforce allowed registries di admission controller
