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

## Daftar Isi

1. [Kubernetes Security Mindset](#1-kubernetes-security-mindset)
2. [Exam Overview & Strategy](#2-exam-overview--strategy)
3. [Trust Boundaries & Attack Surface](#3-trust-boundaries--attack-surface)
4. [Cluster Isolation Model](#4-cluster-isolation-model)
5. [Authentication & Authorization Framework](#5-authentication--authorization-framework)
6. [Workload Security Posture](#6-workload-security-posture)
7. [Data Security at Rest & In Transit](#7-data-security-at-rest--in-transit)
8. [Supply Chain Trust Model](#8-supply-chain-trust-model)
9. [Runtime Defense Framework](#9-runtime-defense-framework)
10. [Compliance & Hardening Posture](#10-compliance--hardening-posture)
11. [Network Security Architecture](#11-network-security-architecture)
12. [Incident Response untuk Kubernetes](#12-incident-response-untuk-kubernetes)
13. [Decision Framework & Trade-offs](#13-decision-framework--trade-offs)
14. [Study Strategy & Mindset](#14-study-strategy--mindset)
15. [Referensi Lengkap](#15-referensi-lengkap)

---

## 1. Kubernetes Security Mindset

### Filosofi Dasar

Kubernetes security bukan tentang menghafal command kubectl atau configurasi YAML. Ini tentang **memahami bagaimana komponen cloud native berinteraksi** dan di mana **trust boundaries** berada. Seorang Kubernetes Security Specialist berpikir dalam layer:

```
User → API → AuthN/AuthZ → Admission → Workload → Network → Storage → Runtime
```

Setiap panah adalah **trust boundary**. Setiap boundary adalah titik di mana keamanan bisa gagal.

### Prinsip Inti

| Prinsip | Artinya | Pertanyaan Kritis |
|---------|---------|------------------|
| **Defense in Depth** | Jangan bergantung pada satu lapis keamanan | "Kalau firewall tembus, apa masih aman?" |
| **Least Privilege** | Beri akses minimum yang diperlukan | "Apa workload ini BENAR-BENAR perlu akses API?" |
| **Secure by Default** | Konfigurasi default harus aman | "Apa yang terjadi kalau lupa set X?" |
| **Assume Breach** | Desain seolah sudah dikompromikan | "Kalau container ini ditembus, apa yang bisa attacker lakukan?" |
| **Immutable Infrastructure** | Jangan patch di production; rebuild dari image baru | "Kenapa container bisa diubah isinya?" |
| **Continuous Verification** | Policy harus diperiksa terus, bukan cuma di deploy | "Apa yang berubah sejak deploy?" |

### Cloud Native Security Taxonomy

Kubernetes security bisa dibagi ke 4 domain besar yang saling terkait:

```
┌─────────────────────────────────────────────┐
│            Supply Chain Security              │
│  (source → build → registry → deploy)        │
├─────────────────────────────────────────────┤
│         Infrastructure Security              │
│  (cluster setup, node hardening, network)    │
├─────────────────────────────────────────────┤
│         Workload Security                    │
│  (pod security, secrets, runtime)            │
├─────────────────────────────────────────────┤
│         Detection & Response                 │
│  (audit, monitoring, incident response)      │
└─────────────────────────────────────────────┘
```

Paradigma penting: **keamanan Kubernetes bersifat kumulatif**. Kalau supply chain sudah compromised, tidak ada jumlah network policy yang bisa menyelamatkan. Urutan prioritas harus dimulai dari hulu:

1. **Supply chain** — pastikan image dan artifact yang masuk trusted
2. **Infrastructure** — pastikan cluster dan node secure
3. **Workload** — pastikan container jalan dengan privilege minimal
4. **Detection** — pastikan ada monitoring kalau semua di atas gagal

### The "Why" Before The "How"

CKS mengajarkan **mengapa** sesuatu perlu diamankan, bukan hanya **bagaimana** cara mengamankannya. Contoh:

| Tool/Config | Pertanyaan Mindset |
|-------------|-------------------|
| `automountServiceAccountToken: false` | "Kenapa container perlu token API? Apa yang terjadi kalau dicuri?" |
| `readOnlyRootFilesystem: true` | "Apa alasan legitimate container perlu write ke filesystem?" |
| NetworkPolicy default-deny | "Kenapa zero-trust networking penting di lingkungan multi-tenant?" |
| Pod Security Standards | "Apa risiko membiarkan container jalan sebagai root?" |

### Security Posture Spectrum

Setiap keputusan keamanan adalah **trade-off** antara security dan operasional:

```yaml
Too Permissive:       Too Restrictive:
  Semua boleh akses     Tidak ada yang bisa jalan
  Pod sebagai root      Semua app butuh config khusus
  No network policy     Developer blocked terus
  ↓                     ↓
  [_____Balance_____]
       |
  Risk-informed decision
```

CKS mindset adalah menemukan **balance yang tepat** untuk konteks organisasi, bukan menerapkan semua control secara membabi buta.

---

## 2. Exam Overview & Strategy

### Format Exam

CKS adalah performance-based exam yang menguji **kemampuan praktikal** dalam mengamankan Kubernetes cluster. Bukan hafalan teori, tapi implementasi di cluster live.

| Item | Detail |
|------|--------|
| **Provider** | Linux Foundation + CNCF |
| **Prasyarat** | CKA aktif (wajib) — bukti kemampuan administrasi K8s |
| **Format** | Remote proctored, browser-based terminal |
| **Durasi** | 2 jam |
| **Jumlah task** | 15-20 soal praktik |
| **Multiple clusters** | Soal tersebar di beberapa cluster context |
| **Passing score** | 67% |
| **Biaya** | $445 (termasuk 1 retake) |
| **Masa berlaku** | 2 tahun |
| **Dokumentasi** | Buka docs.kubernetes.io + beberapa tool docs |
| **K8s version** | v1.34 (update tiap rilis minor) |
| **Simulator** | Killer.sh (2 sesi × 36 jam akses) |

### 6 Domain & Filosofi di Baliknya

| Domain | Weight | Bukan Tentang | Tapi Tentang |
|--------|--------|---------------|--------------|
| Cluster Setup | 15% | Cara setup cluster | Memahami apa yang membuat cluster aman sejak awal |
| Cluster Hardening | 15% | Command RBAC | Filosofi akses siapa punya apa |
| System Hardening | 10% | Install AppArmor | Konsep pembatasan proses di kernel |
| Minimize Microservice Vuln | 20% | Setup PSA labels | Memahami isolasi workload |
| Supply Chain Security | 20% | Command Trivy/Cosign | Trust model dari dev sampai deploy |
| Monitoring/Logging/Runtime | 20% | Syntax Falco rules | Deteksi anomali dan investigasi |

### Tipe Soal

Soal CKS umumnya masuk ke 3 kategori:

| Kategori | Weight | Contoh |
|----------|--------|--------|
| **Configuration** | ~40% | "Apply RBAC sehingga SA ini hanya bisa list pods" |
| **Troubleshooting** | ~35% | "Pod X gagal jalan karena security — fix tanpa mengubah image" |
| **Hardening** | ~25% | "Buat pod ini lebih secure dengan security context minimal" |

### Strategi 3-Pass

```
Pass 1 (30 menit): Kerjakan soal termudah dulu (biasanya configuration tasks)
  - Cluster Setup: labels, namespace, simple RBAC
  - ServiceAccount: disable automounting
  - Ingress TLS

Pass 2 (60 menit): Soal medium-hard (troubleshooting + hardening)
  - NetworkPolicy dengan label selectors
  - Pod Security Standards enforcement
  - RBAC multi-step
  - Seccomp/AppArmor profile

Pass 3 (30 menit): Soal paling berat + validasi
  - Falco rules / audit log analysis
  - Supply chain tasks (signed images, admission control)
  - Verify semua task: test connection, check auth
```

### Common Mistakes

| Mistake | Dampak |
|---------|--------|
| **Perfeksionis** — menghabiskan 20 menit di satu soal | Kehabisan waktu untuk soal lain |
| **Lupa switch context** — mengerjakan soal di cluster salah | Semua jawaban salah |
| **Tidak test hasil kerja** — kira-kira sudah benar | Misconfig tidak ketahuan |
| **Lupa allow DNS di NetworkPolicy** | Pod tidak bisa resolve service name |
| **Mengubah komponen sistem** — reboot base, edit static pod terlalu agresif | Cluster crash |

### PSI Environment Tips

- Browser terminal dengan Linux desktop + Firefox
- Firefox restricted ke docs.kubernetes.io + beberapa whitelist
- Task list di panel kiri, terminal di kanan
- **Jangan pernah reboot base node** — cluster akan mati total
- **Hindari Ctrl+W** — bisa nutup tab exam
- Set alias `k=kubectl` segera setelah exam mulai
- Gunakan `--dry-run=client -o yaml` untuk generate manifest
- Bookmark halaman: NetworkPolicy, RBAC, Pod Security Standards, AppArmor, Seccomp

---

## 3. Trust Boundaries & Attack Surface

### Trust Boundary Diagram

Setiap komponen di Kubernetes memiliki trust boundary yang harus dipahami:

```
External User
    │
    │ TLS
    ▼
┌──────────────┐     ┌──────────────┐
│  API Server   │────▶│   Auth (x509,│
│  (kube-apiserver)  │    Bearer,    │
│              │     │    OIDC)      │
└──────┬───────┘     └──────────────┘
       │
       │ Authorization (RBAC/ABAC)
       ▼
┌──────────────┐     ┌──────────────┐
│  Admission    │────▶│  Mutating    │
│  Controllers  │     │  Webhooks    │
└──────┬───────┘     └──────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│  Validating   │────▶│  OPA/Kyverno │
│  Webhooks     │     │  Constraints │
└──────┬───────┘     └──────────────┘
       │
       ▼
    etcd ─── Data at rest encryption
       │
       ▼
  Scheduler → Kubelet → Container Runtime
       │
       ▼
  Pod Network ─── NetworkPolicy
```

Setiap boundary adalah **attack surface**. Pertanyaan mindset:
- "Apa yang terjadi kalau X ditembus?"
- "Apa mitigasi yang ada sebelum X?"
- "Apa yang bisa dilakukan attacker dari posisi X?"

### Attack Vectors per Layer

#### Layer 1: Supply Chain (Pre-deploy)

| Vector | Bagaimana | Dampak |
|--------|-----------|--------|
| Compromised base image | Image public mengandung malware | Container berisi backdoor sejak lahir |
| Dependency poisoning | Library vulnerable diinstall | RCE via known CVE |
| Unsigned image | Attacker push image malicious | Image malicious dianggap legitimate |
| CI/CD pipeline breach | Build environment compromised | Semua image dari pipeline terinfeksi |

**Mindset**: Anggap semua image tidak trustworthy sampai diverifikasi. Trust harus dibangun, bukan diberikan default.

#### Layer 2: Cluster Infrastructure

| Vector | Bagaimana | Dampak |
|--------|-----------|--------|
| Unauthenticated API access | `--anonymous-auth=true` (default) | Siapa pun bisa akses API |
| Insecure etcd | etcd tanpa auth + encryption | Semua data cluster bisa dibaca |
| Kubelet API terbuka | kubelet port 10250 tanpa auth | Remote command execution di node |
| Dashboard exposed | Kubernetes Dashboard tanpa RBAC | Full cluster admin dari browser |
| Cloud metadata accessible | Pod bisa akses 169.254.169.254 | Cloud credentials leaked |

**Mindset**: Default Kubernetes mengutamakan kemudahan (convenience) di atas keamanan. Setiap komponen harus **explicitly secured**.

#### Layer 3: Workload

| Vector | Bagaimana | Dampak |
|--------|-----------|--------|
| Container sebagai root | `securityContext` tidak diset | Container escape lebih mudah |
| Privileged container | `privileged: true` | Akses penuh ke host kernel |
| HostPath volume | Mount direktori host | Baca/tulis filesystem host |
| ServiceAccount token di-mount | Token API selalu ada di pod | Lateral movement via API |
| Container writable FS | `readOnlyRootFilesystem: false` | Malware bisa install tools |

**Mindset**: Setiap container adalah **potential breach**. Desain seolah container sudah compromised.

#### Layer 4: Network

| Vector | Bagaimana | Dampak |
|--------|-----------|--------|
| Flat network | Pod-to-pod tanpa batasan | Lateral movement bebas |
| Egress tidak dibatasi | Pod bisa connect ke internet | Data exfiltration |
| DNS spoofing | Cluster DNS tanpa verifikasi | Redirect traffic ke attacker |
| Service tanpa TLS | Internal traffic plaintext | Sniffing di compromised node |

**Mindset**: Network policy bukan fitur optional — ini **minimum requirement** untuk cluster production.

#### Layer 5: Runtime

| Vector | Bagaimana | Dampak |
|--------|-----------|--------|
| No audit logging | Tidak ada log API calls | Blind terhadap serangan |
| No runtime detection | Anomali tidak terdeteksi | Attacker leluasa |
| Immutable violated | Container bisa di-write | Malware persist |
| No syscall filtering | Semua system call allowed | Kernel exploit |

**Mindset**: Detection adalah **last line of defense**. Jangan asumsikan semua control di atas berhasil.

### Threat Modeling untuk Kubernetes

STRIDE yang diadaptasi untuk K8s:

| Threat | K8s Contoh | Mitigasi |
|--------|------------|----------|
| **S**poofing | Attacker pura-pura jadi admin via anonymous auth | x509 certs, OIDC, Webhook token |
| **T**ampering | Image diganti di registry | Image signing + verification |
| **R**epudiation | Attacker hapus pod tanpa jejak | Audit logging |
| **I**nformation Disclosure | Secret terbaca dari etcd | Encryption at rest |
| **D**enial of Service | Resource exhaustion via pods tanpa limits | ResourceQuota, LimitRange |
| **E**levation of Privilege | Pod escape ke host | Seccomp, AppArmor, drop capabilities |

### The "What If" Framework

Untuk setiap resource yang dibuat, tanya:

```
1. "What if someone accesses this resource who shouldn't?"
   → RBAC + NetworkPolicy

2. "What if this container is compromised?"
   → Read-only FS, no shell, drop capabilities

3. "What if the API server is exposed?"
   → Authentication + authorization + audit

4. "What if the image has a vulnerability?"
   → Image scanning + admission control

5. "What if someone gets access to etcd?"
   → Encryption at rest + network isolation
```

---

## 4. Cluster Isolation Model

### Namespace Isolation: What It Does and Doesn't

Namespace adalah **unit organisasi logis**, BUKAN security boundary yang kuat.

| Dilindungi Namespace? | Ya | Tidak |
|----------------------|----|-------|
| Resource naming | ✅ Nama unik per namespace | ❌ |
| Resource quotas | ✅ Limit per namespace | ❌ |
| RBAC scoping | ✅ Role bisa di-scope ke namespace | ❌ |
| Network isolation | ❌ Pod beda namespace bisa saling connect | ✅ Harus pakai NetworkPolicy |
| Cluster-wide resources | ❌ ClusterRole, ClusterRole binding lintas namespace | ✅ |
| Pod security policies | ❌ PSA label per namespace | ✅ Tapi perlu admission controller |

**Mindset**: Namespace untuk **organisasi**, NetworkPolicy untuk **isolasi**.

### Multi-tenancy di Kubernetes

Multi-tenancy adalah topik kompleks. Ada beberapa model:

| Model | Isolasi | Cocok untuk | Kompleksitas |
|-------|---------|-------------|-------------|
| **Soft multi-tenancy** | Namespace + RBAC + NetworkPolicy | Internal teams, non-critical | Rendah |
| **Hard multi-tenancy** | Cluster terpisah | External customers, regulated | Tinggi |
| **Sandboxed** | gVisor/Kata per namespace | Untrusted workloads | Sedang |
| **Hierarchical** | vCluster, project namespaces | Enterprise | Tinggi |

**Prinsip**: Semakin banyak trust yang diberikan ke tenant, semakin kuat isolasi yang diperlukan.

### Control Plane vs Data Plane Security

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

**Mindset**:
- Control plane adalah **gatekeeper** — semua request lewat sini
- Data plane adalah **execution environment** — workload jalan di sini
- Attacker menarget control plane untuk kontrol penuh
- Attacker menarget data plane untuk akses data

### Node-Level Isolation

| Aspek | Tanpa Isolasi | Dengan Isolasi |
|-------|---------------|----------------|
| Pod placement | Pod random di node mana pun | Node pool terpisah per workload tier |
| Container escape | Langsung ke host kernel | Sandboxed runtime / kernel terpisah |
| Resource contention | Semua pod compete di node sama | Pod sensitive di dedicated node |
| Compliance | Satu node untuk semua | Node pool khusus untuk regulated data |

**Mindset**: Node bukan security boundary — container di node yang sama bisa saling mempengaruhi. Gunakan **node pool + taint/toleration** untuk isolate workload yang membutuhkan.

---

## 5. Authentication & Authorization Framework

### Authentication: Siapa Kamu?

Kubernetes memiliki beberapa metode autentikasi. Masing-masing dengan trust model berbeda:

| Metode | Trust Model | Use Case | Risiko |
|--------|-------------|----------|--------|
| **x509 Client Certs** | Certificate Authority | Cluster admin, kubelet | Private key exposure |
| **Static Token** | Token file di disk | Bootstrap, legacy | Token tidak bisa di-revoke |
| **Bootstrap Token** | Short-lived token | Node join cluster | Exposure during join |
| **ServiceAccount Token** | Auto-mounted di pod | Pod → API communication | Token bisa dicuri dari pod |
| **OIDC** | External IdP | Integration with SSO | Dependency on external service |
| **Webhook Token** | External auth service | Custom authentication | Latency, availability |
| **Anonymous** | No auth | Tidak pernah untuk production | Siapa pun bisa akses |

**Mindset Question**: "Metode autentikasi apa yang paling sesuai dengan trust model organisasi?"

### Authorization: Kamu Boleh Apa?

Kubernetes punya beberapa mode authorization:

| Mode | Berbasis | Cocok untuk |
|------|----------|-------------|
| **RBAC** | Role + Binding | Hampir semua kasus (default) |
| **ABAC** | User attributes | Policy kompleks (tapi deprecated) |
| **Node** | Node identity | Kubelet authorization |
| **Webhook** | External decision | Custom authorization logic |

**RBAC Philosophy**:

RBAC bukan cuma tentang membuat Role dan Binding. Ini tentang **siapa punya akses ke resource apa, dan mengapa**.

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

| Anti-pattern | Kenapa Berbahaya | Mindset Fix |
|-------------|------------------|-------------|
| `*` wildcard verbs | "Biar mudah" — memberikan akses tak terbatas | Explicit verbs: `get, list, watch` |
| `cluster-admin` untuk semua | "Admin bisa semuanya" — blast radius maksimal | ClusterRole khusus per use case |
| ServiceAccount ke cluster-admin | "Pod ini perlu akses penuh" | Minimal Role, scoped ke namespace |
| Binding ke `system:authenticated` | "Semua user login bisa" | Spesifik ke user/group |
| `*` di apiGroups | Akses ke API groups yang tidak perlu | Sebutkan apiGroups eksplisit |

**Mindset Question**: "Apa minimal verbs yang diperlukan resource ini untuk berfungsi?"

### ServiceAccount: The Overlooked Identity

ServiceAccount adalah identitas untuk **program** (pods), bukan manusia. Ini sering diabaikan:

| Masalah | Kenapa | Mindset |
|---------|--------|---------|
| **Auto-mount token** | Setiap pod punya token API | Container yang tidak perlu API — disable |
| **Default SA** | Semua pakai SA default — sulit audit | Buat SA dedicated per workload |
| **Long-lived tokens** | Token di Secret tidak expire | Projected volumes dengan short TTL |
| **No authz checks** | SA bisa akses tanpa RBAC | RBAC untuk SA yang perlu akses |

**Decision Framework**:

```
Apakah container perlu akses API K8s?
├── TIDAK → automountServiceAccountToken: false
└── YA → Apakah perlu akses spesifik?
    ├── YA → Buat SA + Role + RoleBinding
    └── TIDAK (kebetulan perlu) → Minimal Role dulu, audit setelahnya
```

### API Server Access Control Mindset

API server adalah **pintu masuk tunggal** ke semua operasi cluster. Mengamankannya berarti mengontrol siapa yang bisa lewat dan apa yang bisa mereka lakukan.

```
Request → API Server
   1. Authentication (who are you?)
   2. Authorization (what can you do?)
   3. Admission Control (should this be allowed?)
   4. Audit Logging (what happened?)
   5. etcd Storage (is it encrypted?)
```

Setiap langkah adalah **opportunity to deny or log**.

---

## 6. Workload Security Posture

### Container Security Philosophy

Container bukan virtual machine. Container berbagi kernel dengan host. Implikasi keamanannya fundamental:

```
Virtual Machine:
┌─────────┐ ┌─────────┐ ┌─────────┐
│  App A  │ │  App B  │ │  App C  │
├─────────┤ ├─────────┤ ├─────────┤
│ Guest OS│ │ Guest OS│ │ Guest OS│
├─────────┤ ├─────────┤ ├─────────┤
│  Hypervisor (isolasi hardware)   │
├───────────────────────────────────┤
│           Host Kernel             │
└───────────────────────────────────┘

Container:
┌─────────┐ ┌─────────┐ ┌─────────┐
│  App A  │ │  App B  │ │  App C  │
├─────────┤ ├─────────┤ ├─────────┤
│  Shared Host Kernel (namespaces) │
├───────────────────────────────────┤
│           Host OS                 │
└───────────────────────────────────┘
```

Konsekuensi: **Container escape = akses ke host kernel = akses ke semua container lain**.

### The Three Pillars of Container Security

```
┌────────────────────────────────────────────┐
│          Container Security                │
├──────────────────┬─────────────────────────┤
│  Build Time      │  Run Time               │
├──────────────────┼─────────────────────────┤
│ • Minimal base   │ • Non-root user         │
│ • Multi-stage    │ • Read-only filesystem  │
│ • Scan vulns     │ • Drop capabilities     │
│ • Sign images    │ • Seccomp profile       │
│ • SBOM           │ • AppArmor/SELinux      │
│ • Distroless     │ • Resource limits       │
└──────────────────┴─────────────────────────┘
```

### Pod Security Standards: The Three Profiles

Pod Security Standards (PSS) adalah framework untuk mengkategorikan security posture workload:

| Profile | Filosofi | Kubernetes Default? | Siapa yang perlu akses? |
|---------|----------|-------------------|----------------------|
| **Privileged** | "Trust but verify" — tidak ada pembatasan | Default untuk cluster tanpa PSA | System components, monitoring agents, network plugins |
| **Baseline** | "Known-safe defaults" — cegah privilege escalation yang diketahui | Recommended minimum | General workloads — kebanyakan apps |
| **Restricted** | "Assume breach" — heavily hardened | Hardening target | Sensitive workloads, multi-tenant, external-facing |

**Mindset**: Bukan soal "mana profile yang paling aman", tapi **profile apa yang sesuai untuk workload ini?**

### SecurityContext: The Pod's Security Contract

SecurityContext adalah tempat di mana administrator mendefinisikan **kontrak keamanan** antara pod dan cluster:

| Field | Fungsi | Mindset |
|-------|--------|---------|
| `runAsNonRoot` | Cegah container sebagai root | "Apa alasan container perlu jadi root?" |
| `runAsUser` | Set UID spesifik | "User apa yang minimal diperlukan?" |
| `capabilities.drop` | Hapus Linux capabilities | "Linux capability apa yang TIDAK diperlukan?" |
| `readOnlyRootFilesystem` | Filesystem immutable | "Apa yang perlu di-write dan kenapa?" |
| `allowPrivilegeEscalation` | Cegah privilege escalation via setuid | "Apakah container perlu escalasi?" |
| `seccompProfile` | Filter system calls | "Syscall apa yang TIDAK diperlukan?" |

**Decision Framework** untuk SecurityContext:

```
Untuk setiap container:
1. Apakah perlu root? → NO → runAsNonRoot: true
2. Apakah perlu write ke FS? → NO → readOnlyRootFilesystem: true
3. Apakah perlu Linux capabilities? → minimal → drop: ["ALL"], add: [specific]
4. Apakah perlu privilege escalation? → NO → allowPrivilegeEscalation: false
5. Apakah perlu semua syscall? → NO → seccompProfile: RuntimeDefault
```

### Admission Control Philosophy

Admission controller adalah **guardian at the gate** — setiap request ke API server lewat sini. Ada dua tipe:

| Tipe | Fungsi | Contoh |
|------|--------|--------|
| **Mutating** | Ubah request sebelum diproses | Inject default labels, sidecar, security context |
| **Validating** | Tolak request yang tidak sesuai policy | Cegah image dari registry tidak dikenal |

**Kenapa admission control penting?** Karena RBAC tidak cukup. RBAC bilang "siapa yang bisa create pods", admission control bilang "pods seperti APA yang boleh dibuat".

```
RBAC: "User A boleh create pods di namespace B"
       ↓
Admission: "Tapi pods yang dibuat HARUS:
            - Non-root user
            - Read-only filesystem
            - Dari registry trusted"
```

### Sandboxing: Kapan Diperlukan?

Sandboxing menambah layer isolasi antara container dan host kernel:

| Approach | Isolasi | Overhead | Use Case |
|----------|---------|----------|----------|
| **No sandbox** (runc) | Namespaces + cgroups | Minimal | Trusted workloads |
| **gVisor** | User-space kernel | Syscall overhead | Multi-tenant, untrusted code |
| **Kata Containers** | Lightweight VM | VM boot time | High isolation, regulated |

**Decision Framework**:

```
Apakah workload ini untrusted atau multi-tenant?
├── YES → Sandboxing (gVisor/Kata)
│   ├── Butuh kompatibilitas tinggi? → Kata
│   └── Butuh startup cepat? → gVisor
└── NO → Standard runc dengan security context yang ketat
```

### Resource Constraints as Security Control

Resource limits bukan cuma untuk stabilitas — ini juga security:

| Kontrol | Fungsi Keamanan | Tanpa Ini |
|---------|-----------------|-----------|
| `resources.limits.cpu` | Cegah CPU starvation | Satu pod bisa starve node |
| `resources.limits.memory` | Cegah memory exhaustion | OOM kills semua pod |
| `ResourceQuota` | Batasi total resource per namespace | Satu namespace bisa boros semua |
| `LimitRange` | Default limits untuk pod tanpa limit | Pod tanpa limit bisa konsumsi tak terbatas |

**Mindset**: Resource exhaustion adalah DoS vector. Setiap pod harus punya resource boundaries.

---

## 7. Data Security at Rest & In Transit

### Encryption Philosophy

Data di Kubernetes mengalir melalui beberapa state. Masing-masing perlu pendekatan enkripsi berbeda:

```
Data States:
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   At Rest     │    │   In Transit  │    │   In Use     │
│  (stored)     │    │  (network)    │    │ (memory/CPU) │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       ▼                   ▼                   ▼
  Encryption at rest   TLS/mTLS           (limited control
  (etcd, storage)      (ingress, mTLS)    di K8s level)
```

### Data at Rest: etcd Encryption

etcd adalah **single source of truth** untuk semua data cluster. Siapa pun yang bisa akses etcd bisa baca SEMUA Secret, ConfigMap, dan resource.

| Provider | Kekuatan Enkripsi | Key Rotation | Performance |
|----------|-------------------|--------------|-------------|
| **AES-CBC** | 256-bit symmetric | Tidak support auto-rotate | Fast |
| **Secretbox** | XSalsa20-Poly1305 | Tidak support auto-rotate | Fastest |
| **KMS v1** (deprecated) | External key management | Manual | Latency ke KMS |
| **KMS v2** | External key management, status, keyID in plaintext | **Native rotation support** | Latency ke KMS |

**KMS v2 vs KMS v1 — Mengapa v2 lebih baik:**

| Aspek | KMS v1 | KMS v2 |
|-------|--------|--------|
| Key ID visibility | Tidak ada | Key ID dienkripsi di metadata — audit rotation |
| Status reporting | Tidak ada | DEK status (rotated/pending) |
| Performance | Encrypt/Decrypt per API call | Encrypt di write, decrypt di read (batch) |
| Key rotation | Manual, kompleks | Built-in via `--encryption-provider-config` |
| Status | **Deprecated** | Recommended |

### Secrets Management Mindset

Secret bukan fitur ajaib. Secret adalah resource yang **base64-encoded** (bukan encrypted) secara default.

| Keyakinan Salah | Kenapa Salah | Yang Seharusnya |
|----------------|--------------|-----------------|
| "Secret sudah aman karena base64" | base64 = encoding, BUKAN encryption | Secret harus di-encrypt di etcd |
| "Secret hanya bisa dibaca oleh yang punya akses" | RBAC bisa salah konfigurasi | Audit log akses Secret |
| "Secret otomatis terproteksi" | Banyak komponen bisa baca Secret | Least privilege untuk akses Secret |
| "Token cukup disimpan di Secret" | Long-lived, tidak bisa revoke per pod | Projected volumes + short TTL |

**The Secret Lifecycle**:

```
Create ──→ Store (etc) ──→ Mount ──→ Use ──→ Rotate ──→ Delete
  │           │             │         │        │          │
  ▼           ▼             ▼         ▼        ▼          ▼
Encrypt    Encrypt     Bind ke    Read dari  Ganti    Hapus
at rest    at rest     Pod        filesystem key     expired
via KMS    via KMS     (volume)             & redeploy
```

**Mindset**: Treat Secrets seperti **ammunition** — hanya berikan ke workload yang benar-benar membutuhkan, dan hanya selama diperlukan.

### Data in Transit: TLS dan mTLS

| Level | Melindungi | Implementasi |
|-------|------------|--------------|
| **Ingress → Service** | Traffic dari luar ke cluster | Ingress dengan TLS certificate |
| **Pod → Pod** | Internal traffic | Service mesh (Istio, Cilium) atau mTLS |
| **Node → Control Plane** | Kubelet → API Server | TLS certs (built-in) |
| **API Server → etcd** | Data sensitif di network | etcd TLS (built-in) |

**Mindset**: Traffic internal tidak otomatis aman. Di network yang compromised, semua traffic bisa disniff.

### Encryption Decision Framework

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

---

## 8. Supply Chain Trust Model

### The Software Supply Chain for Containers

Supply chain security untuk container tidak sederhana — ada banyak link dalam rantai:

```
Source Code → Build → Artifact → Registry → Deploy → Runtime
    │           │         │          │         │        │
    ▼           ▼         ▼          ▼         ▼        ▼
  Code      Build      Image      Image     Admission Runtime
  Review    Security   Signing    Scanning  Control   Monitoring
  SAST      SBOM       Cosign/    Trivy     Verify    Falco
  SCA       Sigstore   Notary     Grype     Policy    Audit
```

**Mindset**: Setiap link adalah opportunity for compromise. Supply chain security memastikan setiap langkah diverifikasi.

### The Principle of Trust

Ada **dua model trust** dalam supply chain:

| Model | Filosofi | Implementasi |
|-------|----------|--------------|
| **Trust on First Use (TOFU)** | "Pertama kali percaya, setelahnya selalu percaya" | Pull image sekali, cache selamanya |
| **Verify Every Time** | "Jangan pernah percaya tanpa verifikasi" | Setiap deploy: verifikasi signature, scan, admission check |

CKS mindset adalah **Verify Every Time**.

### Image Integrity vs Image Provenance

| Konsep | Artinya | Contoh |
|--------|---------|--------|
| **Integrity** | Image tidak diubah sejak build | SHA256 digest, signing |
| **Provenance** | Image berasal dari source yang legitimate | SBOM, signed commit, CI/CD pipeline attestation |

```
Integrity: "Apakah image INI sama dengan yang dibuild?"
Provenance: "Apakah image INI berasal dari SOURCE yang terpercaya?"
```

### SBOM: The Bill of Materials

SBOM (Software Bill of Materials) adalah **inventaris** dari semua komponen dalam image:

| Ada di SBOM | Tidak Ada di SBOM |
|-------------|-------------------|
| OS packages (Alpine, Ubuntu) | Source code |
| Library dependencies | Business logic |
| Language runtimes | Configuration files |
| Known versions | Runtime behavior |

**Kenapa SBOM penting?**
1. Ketika CVE baru keluar → cek image mana yang terpengaruh
2. Ketika library diketahui compromised → cari semua image yang menggunakannya
3. Ketika audit → bukti due diligence

**Mindset**: "Kalau besok Log4j 2.0 ditemukan RCE critical, berapa lama kamu tahu image mana yang terpengaruh?"

### Image Signing Philosophy

Image signing bukan tentang "mencegah attacker sign image" — ini tentang **membuktikan identity publisher**:

```
Developer sign image dengan private key
        ↓
Registry menyimpan signature
        ↓
K8s cluster verify dengan public key
        ↓
Admission controller cek signature sebelum deploy
```

**Kenapa signing diperlukan?**
- Image tag bisa di-push ulang (tag:latest adalah musuh)
- Registry bisa compromised
- MitM antara registry dan cluster (registry mirror)

### Admission Control untuk Supply Chain

Admission controller adalah **enforcement point** untuk supply chain policy:

| Policy | Cegah | Implementasi |
|--------|-------|--------------|
| **Allowed registries only** | Pod dari registry tidak dikenal | ImagePolicyWebhook, OPA, Kyverno |
| **Signed images only** | Image yang tidak diverifikasi | Cosign + admission controller |
| **No latest tag** | Image dengan tag tidak stabil | OPA/Kyverno pattern matching |
| **Specific digest only** | Image tanpa hash spesifik | Image dengan `@sha256:...` |
| **Scan results gating** | Image dengan critical vuln | Trivy + webhook |

**Mindset**: Admission control untuk supply chain bukan opsional — ini adalah **satu-satunya cara** enforce policy sebelum workload masuk cluster.

### Supply Chain Attack Vectors

| Attack | Tahap | Bagaimana Terjadi | Mitigasi |
|--------|-------|-------------------|----------|
| **Dependency confusion** | Build | Package manager install dari public, bukan private | Pinned versions, private registry mirror |
| **Typosquatting** | Build | Package nama mirip dengan yang asli | SBOM + vulnerability scanning |
| **Compromised base image** | Build | Official base image malicious | Multi-stage build + minimal base |
| **Registry poisoning** | Registry | Push image malicious ke registry | Image signing + verification |
| **Tag mutability** | Registry | Tag `latest` di-overwrite dengan image beda | Gunakan digest (`@sha256`) |
| **CI/CD pipeline breach** | Build | Access token dicuri dari CI | Short-lived tokens, signed attestations |

### The SLSA Framework (Supply-chain Levels for Software Artifacts)

SLSA adalah framework maturity untuk supply chain security:

| Level | Artinya | Di K8s |
|-------|---------|--------|
| **SLSA 1** | Build process documented | Dockerfile + README |
| **SLSA 2** | Signed provenance + hosted build | Signed images, CI/CD |
| **SLSA 3** | Hardened build + no user influence | Reproducible builds, hermetic |
| **SLSA 4** | Two-party review + hermetic | Full audit trail, signed every step |

**Mindset**: Target minimum untuk production adalah SLSA 2 — signed build dengan provenance.

---

## 9. Runtime Defense Framework

### Behavioral vs Signature-Based Detection

| Approach | Cara Kerja | Cocok untuk | Kelemahan |
|----------|------------|-------------|-----------|
| **Signature-based** | Mencocokkan pattern known attacks | Known malware, CVEs | Zero-day, polymorphic |
| **Behavioral** | Mendeteksi anomali dari baseline | Unknown threats, zero-day | False positives tinggi |

Runtime security di K8s menggunakan **keduanya** — signature untuk known threats, behavioral untuk anomaly detection.

### The Immutable Container Principle

Container seharusnya **immutable** — sekali jalan, isinya tidak berubah. Kenapa?

```
Mutable Container:                       Immutable Container:
───────────────────────                  ───────────────────────
Container berjalan                       Container berjalan
Attacker masuk                          Attacker masuk
Attacker install tools                  Tools tidak bisa diinstall
Attacker modify config                  Filesystem read-only
Attacker persist backdoor               Backdoor hilang setelah restart
Container = compromised forever         Restart = clean state
```

**Apa yang perlu di-write di container?**
- Temporary data → `emptyDir`
- Logs → sidecar container atau stdout
- Cache → `emptyDir` dengan size limit
- Secrets → projected volumes (read-only)

**Mindset**: "Kalau container ini direstart, apakah state berbahaya hilang?"

### Audit Logging: The Forensic Foundation

Audit logging adalah **single source of truth** untuk investigasi. Setiap request ke API server bisa dicatat dengan level detail berbeda:

| Level | Detail | Volume | Use Case |
|-------|--------|--------|----------|
| `None` | Tidak dicatat | 0 | Health checks, liveness probes |
| `Metadata` | User, timestamp, resource, verb | Rendah | Compliance, audit dasar |
| `Request` | Metadata + request body | Sedang | Forensic investigation |
| `RequestResponse` | Metadata + request + response | Tinggi | Full audit trail |

**Apa yang harus diaudit?**

| Event | Level | Kenapa |
|-------|-------|--------|
| Secret access | `Metadata` | Mencegah data leak |
| Pod creation | `Metadata` | Deteksi workload tidak dikenal |
| RBAC changes | `Request` | Siapa yang ubah izin? |
| ClusterRole bindings | `RequestResponse` | Escalation detection |
| Anonymous requests | `Metadata` | Potensi attack |
| 403 Forbidden | `Metadata` | Reconnaissance detection |

**Konsekuensi memilih level audit:**
- `None` → Buta terhadap serangan
- `Metadata` → Tahu ada serangan tapi tidak tahu detailnya
- `Request` → Tahu persis apa yang dikirim attacker
- `RequestResponse` → Tahu respons API-nya juga

**Mindset**: Audit logging adalah **insurance policy**. Mahal (storage, performance) tapi tidak ternilai saat terjadi breach.

### Container Runtime Security: Syscall Perspective

Setiap container adalah kumpulan **system calls** ke kernel. Runtime security melihat syscall mana yang legitimate dan mana yang mencurigakan:

```
Legitimate Container:         Compromised Container:
├── read()                    ├── read()
├── write()                   ├── write()
├── open()                    ├── open()
├── close()                   ├── close()
├── socket()                  ├── socket() ← unexpected
├── bind()                    ├── bind()   ← unexpected
└── ...                       ├── ptrace() ← SUSPICIOUS!
                              ├── exec()   ← SHELL SPAWNED!
                              └── setuid() ← PRIVILEGE ESCALATION!
```

**Prinsip**: Semakin sedikit syscall yang diizinkan, semakin kecil attack surface.

### The Detection-Response Gap

Runtime detection hanya berguna kalau diikuti **response**:

```
Detect → Analyze → Contain → Eradicate → Recover → Learn
  │         │          │          │          │        │
  ▼         ▼          ▼          ▼          ▼        ▼
Falco    jq query   cordon pod  delete pod  restart  update
audit    /audit.log taint node  rebuild                              policy
```

Di CKS, fokusnya pada **deteksi dan analisis awal** — bukan full incident response. Tapi mindset-nya harus end-to-end.

### crictl: Runtime Investigation

Ketika pod bermasalah (crash, OOM, hang), `kubectl` kadang tidak cukup. `crictl` adalah interface langsung ke container runtime:

```
kubectl describe pod → info dari API server
crictl ps → info dari container runtime (lebih detail)

Kenapa perlu crictl?
- Pod dalam status `ContainerCreating` — image pull issue
- Container crash loop — cek exit code dan logs
- Resource issues — cek cgroup stats
- Runtime errors — containerd/cri-o logs
```

---

## 10. Compliance & Hardening Posture

### CIS Benchmarks: The Evaluation Framework

CIS (Center for Internet Security) Kubernetes Benchmark adalah **standard industri** untuk mengevaluasi security posture cluster. Bukan tentang cara menjalankan kube-bench, tapi tentang **apa yang diukur dan kenapa**.

| Section | Apa yang Diukur | Kenapa Penting |
|---------|-----------------|----------------|
| **Control Plane** | API Server, Controller Manager, Scheduler, etcd | Gatekeeper cluster — jika compromised, cluster hilang |
| **Worker Nodes** | Kubelet, kube-proxy, node config | Execution environment — jika compromised, data hilang |
| **Policies** | RBAC, ServiceAccount, Pod Security | Access control — jika lemah, siapa pun bisa apa pun |
| **Data Protection** | Secrets, encryption, audit | Confidentiality — jika bocor, data exposure |

### Kategori Check CIS

| Kategori | Arti | Tindakan |
|----------|------|----------|
| **Scored** | Jelas impact keamanannya — harus diperbaiki | Prioritaskan remediasi |
| **Not Scored** | Kontekstual — tergantung environment | Evaluasi manual |
| **Automated** | Bisa dicek dengan tool (kube-bench) | Gunakan tool |
| **Manual** | Perlu review manual | Dokumentasikan keputusan |

**Mindset**: CIS bukan checklist mutlak. Ini adalah **framework evaluasi** — fail di satu check tidak berarti cluster tidak aman, tapi perlu justifikasi.

### Hardening: Reduce Attack Surface

Hardening adalah proses **menghilangkan yang tidak perlu**:

| Komponen | Default | Hardened |
|----------|---------|----------|
| API Server | Profiling ON, anonymous auth ON | Profiling OFF, anonymous OFF |
| etcd | Default ports, no TLS auth | TLS auth, firewall, encryption |
| Kubelet | Anonymous auth ON (dulu) | Webhook auth, cert rotation |
| Dashboard | Exposed, cluster-admin | Disabled atau RBAC restricted |
| ServiceAccount | Token auto-mount | Disable yang tidak perlu |
| Container | Root user, privileged | Non-root, read-only, no caps |

**Prinsip**: "If you don't need it, remove it. If you can't remove it, restrict it."

### The Hardening Decision Tree

Untuk setiap komponen:

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

### Security Scorecard Mental Model

Bayangkan cluster memiliki scorecard seperti ini:

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
├──────────────────────────────────┼───────┤
│ Overall                          │ 6.8   │
└──────────────────────────────────┴───────┘
```

**Mindset**: Fokus pada area dengan skor terendah — itu adalah risk terbesar.

---

## 11. Network Security Architecture

### Zero Trust Networking untuk Kubernetes

Network default di Kubernetes: **semua pod bisa bicara ke semua pod**. Ini zero trust? Justru sebaliknya — ini **maximum trust**.

```
Default: Zero Isolation               Zero Trust:
┌──────────┐    ┌──────────┐          ┌──────────┐    ┌──────────┐
│  Pod A   │◀──▶│  Pod B   │          │  Pod A   │    │  Pod B   │
│ (web)    │    │ (db)     │          │ (web)    │    │ (db)     │
└──────────┘    └──────────┘          └────┬─────┘    └────┬─────┘
       │                                      │             │
       ▼                                      ▼             ▼
┌──────────┐                            ┌──────────┐
│  Pod C   │                            │  Allowed │
│ (evil)   │                            │  traffic  │
└──────────┘                            │  ONLY    │
                                        └──────────┘
```

**Prinsip zero trust di K8s**:
1. Default deny — semua traffic diblok
2. Explicit allow — hanya traffic yang perlu diizinkan
3. Verify every connection — identity-aware policies
4. Least privilege — izinkan port dan protocol minimal

### Micro-segmentation

Micro-segmentation membagi cluster menjadi segmen kecil dengan policy spesifik:

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

### Network Policy: Design Patterns

| Pattern | Deskripsi | Kapan Digunakan |
|---------|-----------|-----------------|
| **Default-deny all** | Blok semua ingress dan egress | Foundation untuk semua namespace |
| **Allow ingress from specific** | Izinkan traffic masuk dari pods tertentu | Service → frontend hanya dari ingress |
| **Allow egress to specific** | Izinkan traffic keluar ke pods tertentu | Backend hanya ke database |
| **DNS allow** | Izinkan egress ke CoreDNS | Semua pods perlu DNS |
| **ipBlock except** | Blok IP range tertentu kecuali | Cegah akses ke metadata service |
| **Namespace selector** | Izinkan traffic dari namespace tertentu | Multi-tier apps |

**The DNS Trap**:
Ketika menerapkan egress policy, DNS request ke CoreDNS di kube-system harus diizinkan. Tanpa ini, pod tidak bisa resolve service names.

### Egress Control dan Data Exfiltration

Egress control sering diabaikan — fokus biasanya di ingress. Tapi egress adalah **exfiltration path**:

```
Attacker di Pod → Egress:
├── ke database → steal data (allowed)
├── ke internet → exfiltrate (should be blocked)
├── ke metadata service → cloud creds (blocked via ipBlock)
├── ke external C2 → command & control (blocked)
└── ke DNS → data encoding via DNS queries (hard to block)
```

**Mindset**: Assume container compromised — apa yang bisa keluar?

### mTLS dan Service Mesh

mTLS (mutual TLS) memastikan **kedua sisi** komunikasi terverifikasi:

```
Without mTLS:                        With mTLS:
Pod A ──── HTTP ────▶ Pod B         Pod A ──── HTTPS ────▶ Pod B
(identity?)         (identity?)      (cert A → verify)    (cert B → verify)
```

| Approach | Complexity | Coverage | Management |
|----------|------------|----------|------------|
| **Manual mTLS** | Tinggi (kelola certs sendiri) | Per service | Manual |
| **Service Mesh (Istio)** | Sedang | All traffic via sidecar | Automated |
| **Cilium** | Rendah | L3/L7 dengan eBPF | Automated |

**Mindset**: mTLS bukan solusi untuk semua masalah — network policy dan encryption adalah complementary controls.

---

## 12. Incident Response untuk Kubernetes

### IR di Kubernetes vs Traditional

| Aspek | Traditional Server | Kubernetes Container |
|-------|-------------------|---------------------|
| **Unit investigasi** | Host/VM | Pod/Container |
| **Persistence** | Attacker install tools | Read-only FS — tidak bisa persist |
| **Lateral movement** | SSH ke host lain | API server → service account |
| **Evidence** | Hard drive, memory | Container logs, audit logs |
| **Containment** | Isolate host | Kill pod, cordon node |
| **Eradication** | Patch host | Delete pod, rebuild image |

### Forensic Artifacts di Kubernetes

| Artifact | Lokasi | Apa yang Bisa Ditemukan |
|----------|--------|------------------------|
| **Audit logs** | `/var/log/kubernetes/audit.log` | Siapa, apa, kapan ke API server |
| **Container logs** | `kubectl logs` / `crictl logs` | Aplikasi output, error |
| **kubelet logs** | `journalctl -u kubelet` | Node-level events |
| **Container filesystem** | Worker node filesystem | Config, malware |
| **etcd snapshot** | Backup atau live | Semua resource cluster |
| **Events** | `kubectl get events` | Cluster events (warnings, errors) |

### Investigasi Container Compromise

```
Step 1: Identifikasi Pod Mencurigakan
  - Unexpected pods: `kubectl get pods -A | grep -v Running`
  - Unknown images: `kubectl get pods -A -o wide`
  - Recent creation: `kubectl get pods -A --sort-by=.metadata.creationTimestamp`

Step 2: Cek Container
  - Shell spawned: cek dengan runtime tool
  - Suspicious processes: `crictl ps`, `crictl exec`
  - Network connections: `crictl exec <container> netstat -tlnp`

Step 3: Cek Audit Log
  - Siapa yang create pod ini?
  - Dari mana image pull?
  - Apakah ada event anomali sebelumnya?

Step 4: Containment
  - Delete pod yang compromised
  - Cordoning node jika perlu
  - Revoke credentials yang terexpose
```

### IR Decision Framework

```
Apakah pod compromised?
├── Tidak yakin → Investigation mode:
│   ├── Cek audit log untuk source
│   ├── Cek container logs untuk anomaly
│   └── Cek network connections
├── Ya, confirmed → Containment:
│   ├── Is critical? → Shutdown immediately
│   ├── Is isolated? → Network policy block egress
│   └── Is persistent? → Delete + rebuild image
└── After containment → Recovery:
    ├── Revoke semua credentials yang mungkin terexpose
    ├── Rotate cluster CA jika SA keys compromised
    ├── Run vulnerability scan
    └── Post-mortem: "Bagaimana ini bisa terjadi?"
```

### Immutable Recovery

Di Kubernetes, recovery dari incident lebih mudah daripada traditional:

```
Traditional:
  Investigate → Find malware → Clean → Patch → Test → Deploy
  (berjam-jam, risk of missing something)

Kubernetes Immutable:
  Identify → Delete pod → Redeploy from clean image → Done
  (beberapa menit, clean state guaranteed)
```

**Mindset**: Jangan repair container compromised. **Bunuh dan ganti dengan yang baru**. Itulah keunggulan immutable infrastructure.

---

## 13. Decision Framework & Trade-offs

### Security vs Operability Matrix

Setiap kontrol keamanan punya **cost**:

| Kontrol | Security Benefit | Operasional Cost | Kapan Worth It? |
|---------|-----------------|------------------|-----------------|
| Read-only root FS | High | Rendah (butuh emptyDir) | Selalu |
| Drop all capabilities | High | Rendah (kecuali app butuh cap) | Selalu |
| Seccomp RuntimeDefault | Medium | Minimal | Selalu |
| Pod Security Standards | High | Sedang (butuh audit) | Semua production |
| NetworkPolicy | High | Sedang | Multi-tier apps |
| Image signing | High | Tinggi (key mgmt) | Regulated, production |
| mTLS (service mesh) | High | Tinggi (resource, complexity) | Multi-service, sensitive data |
| Sandboxed runtime | Very High | Tinggi (performance) | Untrusted workloads |

**Decision Framework**: "Apakah benefit keamanan > operasional cost?"

### When to Use What: Admission Control

| Kebutuhan | PSA Labels | OPA Gatekeeper | Kyverno |
|-----------|------------|---------------|---------|
| Enforce PSS profiles | ✅ Built-in | ✅ Via Rego | ✅ Via YAML |
| Custom policy logic | ❌ | ✅ Rego | ✅ YAML patterns |
| Mutation (auto-inject) | ❌ | Limited | ✅ Native |
| Complexity | Rendah | Tinggi | Rendah-Sedang |
| Learning curve | Minimal | Tinggi (Rego) | Rendah (YAML) |

**Decision**: 
- Simple PSS enforcement → **PSA labels** (built-in, zero maintenance)
- Complex policy logic → **OPA Gatekeeper** (expressive Rego)
- Kubernetes-native policy with mutation → **Kyverno** (YAML-based)

### When to Use What: Network Security

| Kebutuhan | Native NetworkPolicy | Cilium | Service Mesh |
|-----------|---------------------|--------|--------------|
| L3/L4 segmentation | ✅ | ✅ | ✅ (via sidecar) |
| L7 filtering | ❌ | ✅ (L7 policies) | ✅ |
| Encryption | ❌ | ✅ (WireGuard) | ✅ (mTLS) |
| Observability | ❌ | ✅ (Hubble) | ✅ |
| Complexity | Rendah | Sedang | Tinggi |

**Decision**:
- Basic pod isolation → **Native NetworkPolicy**
- Need encryption + observability → **Cilium**
- Need L7 traffic management + mTLS → **Service Mesh**

### Risk-Based Approach

Tidak semua workload butuh level keamanan yang sama:

```
Risk = (Likelihood of compromise) × (Impact of compromise)

High Impact → Lebih ketat (restricted PSS, sandboxing, mTLS)
Low Impact → Baseline (standard PSA, network policy dasar)

Contoh:
├── External API (High Impact) → Restricted + mTLS + audit
├── Internal Service (Medium) → Baseline + network policy
└── Dev/Staging (Low) → Baseline, enforce via warn mode
```

**Mindset**: Keamanan bukan absolut — ini tentang **risk management**. Investasi keamanan proporsional dengan risk.

### The "Enforce vs Audit" Decision

Ketika menerapkan policy baru, selalu mulai dari **audit mode**:

```
Phase 1: Audit (warn)
  - Terapkan policy di mode warn/audit
  - Lihat workload mana yang melanggar
  - Tidak ada downtime

Phase 2: Fix
  - Perbaiki workload yang melanggar
  - Bekerja sama dengan developer

Phase 3: Enforce
  - Setelah semua compliant, ubah ke enforce
  - Monitor untuk regresi
```

---

## 14. Study Strategy & Mindset

### Cara Belajar CKS Mindset

Bukan dengan menghafal command, tapi dengan:

| Metode | Deskripsi | Durasi |
|--------|-----------|--------|
| **Baca policy, bukan tutorial** | Baca dokumentasi resmi K8s tentang security concepts | 1-2 minggu |
| **Analisa misconfig** | Cari cluster yang misconfigured di internet, analisa dampaknya | 1-2 minggu |
| **Threat modeling** | Setiap workload: "Apa yang terburuk yang bisa terjadi?" | Ongoing |
| **Buat policy dari 0** | Jangan copy-paste — tulis policy sendiri, pahami setiap field | 2-3 minggu |
| **Review CIS benchmark** | Baca CIS K8s benchmark — pahami rationale setiap check | 1 minggu |
| **Practice under pressure** | Gunakan killer.sh — latihan dengan timer | 2-3 sesi |

### Recommended Study Path

```
Foundation (2-3 minggu):
├── Pahami arsitektur K8s (prasyarat CKA)
├── Pahami container security fundamentals
└── Pahami trust boundaries

Core Security Concepts (3-4 minggu):
├── RBAC design patterns
├── Network policy architecture
├── Pod security standards
└── Secrets management

Advanced (2-3 minggu):
├── Supply chain trust model
├── Runtime defense
├── Admission control philosophy
└── Compliance framework

Practice (2 minggu):
├── killer.sh sesi 1
├── Analisa kesalahan
├── killer.sh sesi 2
└── Review konsep yang lemah
```

### The "Why" Drill

Untuk setiap task latihan, tanya 3 pertanyaan:

```
1. WHY is this control needed?
   - Apa yang terjadi tanpanya?
   - Attack vector apa yang dicegah?

2. HOW does it work?
   - Apa mekanisme di belakang?
   - Bagaimana enforcement-nya?

3. WHAT are the trade-offs?
   - Apa yang dikorbankan?
   - Kapan tidak perlu dilakukan?
```

### Exam Day Mental Checklist

| Sebelum Exam | Selama Exam |
|-------------|-------------|
| ✅ Sleep enough | 🎯 Set alias `k=kubectl` dulu |
| ✅ PSI compatibility test | 🎯 Baca semua soal sebelum mulai |
| ✅ ID card ready | 🎯 Prioritaskan soal termudah |
| ✅ Clean desk, no notes | 🎯 Switch context setiap soal |
| ✅ Charger connected | 🎯 Test hasil kerja |
| ✅ No other monitors | 🎯 Kalau stuck >5 menit, skip |

### What CKS Does NOT Teach

| Tidak Diajarkan | Kenapa |
|----------------|--------|
| **Cloud-specific security** | CKS K8s-native — tidak cover AWS IAM, GCP SA |
| **Full incident response** | IR level dasar — fokus deteksi |
| **Kernel exploitation** | Hanya syscall filtering, bukan exploit dev |
| **Web app security** | Fokus container/platform, bukan aplikasi |
| **Network engineering** | Policy-level, bukan routing/switching |

---

## 15. Referensi Lengkap

### Official Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | CNCF CKS Page | https://www.cncf.io/training/certification/cks/ |
| 2 | Linux Foundation CKS Page | https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/ |
| 3 | CKS Candidate Handbook | https://docs.linuxfoundation.org/tc-docs/certification/lf-candidate-handbook |
| 4 | CKS Program Changes (Oct 2024) | https://training.linuxfoundation.org/cks-program-changes/ |
| 5 | CKS Curriculum Overview | https://github.com/cncf/curriculum |
| 6 | CKS FAQ | https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/faq/ |
| 7 | CKA Prerequisite | https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/ |
| 8 | LF Certification FAQ | https://docs.linuxfoundation.org/tc-docs/certification/important-faq-cks |
| 9 | PSI Exam Platform Guide | https://docs.linuxfoundation.org/tc-docs/certification/important-tips-cks |

### Official Kubernetes Documentation

| # | Topic | URL |
|---|-------|-----|
| 10 | Kubernetes Security Documentation | https://kubernetes.io/docs/concepts/security/ |
| 11 | Security Best Practices | https://kubernetes.io/docs/concepts/security/best-practices/ |
| 12 | Security Checklist | https://kubernetes.io/docs/concepts/security/security-checklist/ |
| 13 | Pod Security Standards | https://kubernetes.io/docs/concepts/security/pod-security-standards/ |
| 14 | Pod Security Admission | https://kubernetes.io/docs/concepts/security/pod-security-admission/ |
| 15 | Enforce PSS with Namespace Labels | https://kubernetes.io/docs/tasks/configure-pod-container/enforce-standards-namespace-labels/ |
| 16 | Network Policies | https://kubernetes.io/docs/concepts/services-networking/network-policies/ |
| 17 | RBAC Authorization | https://kubernetes.io/docs/reference/access-authn-authz/rbac/ |
| 18 | Service Accounts | https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/ |
| 19 | Secrets | https://kubernetes.io/docs/concepts/configuration/secret/ |
| 20 | Encryption at Rest | https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/ |
| 21 | KMS Provider | https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/ |
| 22 | Audit Logging | https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/ |
| 23 | AppArmor | https://kubernetes.io/docs/tutorials/security/apparmor/ |
| 24 | Seccomp | https://kubernetes.io/docs/tutorials/security/seccomp/ |
| 25 | SecurityContext | https://kubernetes.io/docs/tasks/configure-pod-container/security-context/ |
| 26 | Admission Controllers | https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/ |
| 27 | Kubelet Security | https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/ |
| 28 | API Server Security | https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/ |
| 29 | Controlling Access to API | https://kubernetes.io/docs/concepts/security/controlling-access/ |
| 30 | TLS in Kubernetes | https://kubernetes.io/docs/concepts/cluster-administration/certificates/ |
| 31 | Ingress TLS | https://kubernetes.io/docs/concepts/services-networking/ingress/#tls |
| 32 | ResourceQuota | https://kubernetes.io/docs/concepts/policy/resource-quotas/ |
| 33 | LimitRange | https://kubernetes.io/docs/concepts/policy/limit-range/ |
| 34 | Runtime Class | https://kubernetes.io/docs/concepts/containers/runtime-class/ |
| 35 | Container Runtime Interface | https://kubernetes.io/docs/concepts/architecture/cri/ |

### CIS Benchmark

| # | Resource | URL |
|---|----------|-----|
| 36 | CIS Kubernetes Benchmark | https://www.cisecurity.org/benchmark/kubernetes |
| 37 | CIS Benchmark v1.30 PDF (free registration) | https://workbench.cisecurity.org/benchmarks/12788 |
| 38 | Understanding CIS Benchmarks | https://www.cisecurity.org/insights/blog/understanding-cis-benchmarks |

### Supply Chain Security

| # | Resource | URL |
|---|----------|-----|
| 39 | SLSA Framework | https://slsa.dev/ |
| 40 | Sigstore / Cosign | https://www.sigstore.dev/ |
| 41 | SBOM Overview (NTIA) | https://www.ntia.gov/SBOM |
| 42 | SPDX SBOM Format | https://spdx.dev/ |
| 43 | Supply Chain Security (K8s docs) | https://kubernetes.io/docs/concepts/security/supply-chain-security/ |
| 44 | OWASP CycloneDX | https://cyclonedx.org/ |
| 45 | Docker Multi-stage Builds | https://docs.docker.com/build/building/multi-stage/ |
| 46 | Distroless Images | https://github.com/GoogleContainerTools/distroless |

### Runtime Security

| # | Resource | URL |
|---|----------|-----|
| 47 | Falco Documentation | https://falco.org/docs/ |
| 48 | Falco Rules Official | https://github.com/falcosecurity/rules |
| 49 | Tetragon (eBPF-based security) | https://tetragon.io/ |
| 50 | Tracee (eBPF runtime) | https://aquasecurity.github.io/tracee/ |
| 51 | Container Runtime Security Overview | https://kubernetes.io/docs/concepts/security/runtime-class/ |
| 52 | gVisor (sandboxed runtime) | https://gvisor.dev/ |
| 53 | Kata Containers | https://katacontainers.io/ |

### Incident Response & Forensics

| # | Resource | URL |
|---|----------|-----|
| 54 | Kubernetes Incident Response | https://kubernetes.io/docs/tasks/debug/debug-cluster/ |
| 55 | crictl Cheat Sheet | https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md |
| 56 | Forensic Container Analysis | https://www.cisa.gov/resources-tools/resources/incident-response-plan |
| 57 | Kubernetes Forensics (Aqua) | https://blog.aquasec.com/kubernetes-forensics |

### Community & Learning

| # | Resource | URL |
|---|----------|-----|
| 58 | Killer.sh (CKS Simulator) | https://killer.sh/cks |
| 59 | KodeKloud CKS Course | https://kodekloud.com/courses/certified-kubernetes-security-specialist-cks/ |
| 60 | KodeKloud CKS Mock Exam | https://kodekloud.com/courses/ultimate-certified-kubernetes-security-specialist-cks-mock-exam-series/ |
| 61 | LFS460 Kubernetes Security Essentials | https://training.linuxfoundation.org/training/kubernetes-security-essentials-lfs460/ |
| 62 | LFS258 Kubernetes Fundamentals | https://training.linuxfoundation.org/training/kubernetes-fundamentals-lfs258/ |
| 63 | Pluralsight CKS Path | https://www.pluralsight.com/paths/kubernetes-security |
| 64 | Kubernetes Security Guide (k8s-security.guru) | https://k8s-security.guru/ |
| 65 | Kubernetes Security (kubescape.io) | https://kubescape.io/ |
| 66 | CKS Study Guide (sailor.sh) | https://sailor.sh/blog/cks-exam-guide-2026/ |
| 67 | CKS Exam Topics (sailor.sh) | https://sailor.sh/blog/cks-exam-topics/ |
| 68 | CKS Exam Guide (kodekloud blog) | https://kodekloud.com/blog/certified-kubernetes-security-specialist-cks-exam-verification-guide/ |
| 69 | CKS Study Guide (CertLand) | https://certland.net/blog/cks-certified-kubernetes-security-specialist-study-guide-2026/ |
| 70 | CKS Deep Dive: Supply Chain (CertLand) | https://certland.net/blog/cks-deep-dive-supply-chain-falco-opa-gatekeeper-runtime-security/ |
| 71 | DevOpsCube CKS Guide | https://devopscube.com/cks-exam-guide-tips/ |
| 72 | CKS Tips (examcert.app) | https://www.examcert.app/blog/cks-exam-tips-pass-first-attempt-2026/ |

### GitHub Repositories

| # | Repository | Focus | URL |
|---|------------|-------|-----|
| 73 | leandrocostam/cks-preparation-guide | Comprehensive CKS prep | https://github.com/leandrocostam/cks-preparation-guide |
| 74 | techiescamp/cks-certification-guide | CKS study guide | https://github.com/techiescamp/cks-certification-guide |
| 75 | mikonoid/CKS-exam-cheat-sheets | CKS cheat sheets per domain | https://github.com/mikonoid/CKS-exam-cheat-sheets |
| 76 | snigdhasambitak/cks | CKS practice questions | https://github.com/snigdhasambitak/cks |
| 77 | ggnanasekaran77/cks-exam-tips | CKS exam tips | https://github.com/ggnanasekaran77/cks-exam-tips |
| 78 | moabukar/CKS-Exercises | CKS mock exam questions | https://github.com/moabukar/CKS-Exercises-Certified-Kubernetes-Security-Specialist |
| 79 | dmpe/cka-setup-examples | CKS notes | https://github.com/dmpe/cka-setup-examples |

### Security Tools (Official Docs)

| # | Tool | URL |
|---|------|-----|
| 80 | kube-bench (CIS scanner) | https://github.com/aquasecurity/kube-bench |
| 81 | Trivy (vulnerability scanner) | https://github.com/aquasecurity/trivy |
| 82 | Cosign (image signing) | https://github.com/sigstore/cosign |
| 83 | Syft (SBOM generator) | https://github.com/anchore/syft |
| 84 | Grype (vulnerability scanner) | https://github.com/anchore/grype |
| 85 | OPA Gatekeeper | https://github.com/open-policy-agent/gatekeeper |
| 86 | Kyverno (K8s policy engine) | https://github.com/kyverno/kyverno |
| 87 | KubeLinter (static analysis) | https://github.com/stackrox/kube-linter |
| 88 | Kubesec (security risk analysis) | https://github.com/controlplaneio/kubesec |
| 89 | Kubescape (K8s security posture) | https://github.com/kubescape/kubescape |
| 90 | Falco (runtime security) | https://github.com/falcosecurity/falco |
| 91 | Cilium (network + security) | https://github.com/cilium/cilium |
| 92 | Tetragon (eBPF security) | https://github.com/cilium/tetragon |

### Blog Posts & Papers

| # | Resource | URL |
|---|----------|-----|
| 93 | NSA/CISA Kubernetes Hardening Guide | https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.1_20220829.PDF |
| 94 | NIST SP 800-190 Application Container Security | https://csrc.nist.gov/publications/detail/sp/800-190/final |
| 95 | NIST SP 800-204 Security of Microservices | https://csrc.nist.gov/publications/detail/sp/800-204/final |
| 96 | OWASP Kubernetes Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Kubernetes_Security_Cheat_Sheet.html |
| 97 | Sysdig 2025 Cloud-Native Threat Report | https://sysdig.com/resources/reports/cloud-native-threat-report/ |
| 98 | Aqua Security: Container Escape Methods | https://blog.aquasec.com/container-escape-techniques |
| 99 | Kubernetes Security: Focus on Pod Security (Puru Tuladhar) | https://ptuladhar3.medium.com/ |
| 100 | Kubesimplify YouTube: CKS Playlist | https://www.youtube.com/playlist?list=PLFcNfkVk3QhJdOaohHcqMVW-OM5fATrO8 |

### Communities

| # | Community | URL |
|---|-----------|-----|
| 101 | CNCF Slack (#cks channel) | https://slack.cncf.io/ |
| 102 | Reddit r/kubernetes | https://reddit.com/r/kubernetes |
| 103 | Kubernetes Security Discourse | https://discuss.kubernetes.io/c/security/ |
| 104 | Kubernetes Security LinkedIn Group | https://linkedin.com/groups/13854190 |
| 105 | Stack Overflow Kubernetes | https://stackoverflow.com/questions/tagged/kubernetes |

---

> **Catatan Akhir**: CKS mindset bukan tentang menghafal tools atau command — ini tentang **memahami mengapa cluster perlu diamankan, di mana letak trust boundaries, dan bagaimana defense-in-depth diterapkan di cloud native world**. Seorang Kubernetes Security Specialist berpikir dalam layer, bukan dalam tools. Mereka tahu bahwa keamanan bukan produk yang bisa dibeli — ini adalah **proses berkelanjutan** yang dimulai dari supply chain dan berakhir di runtime detection.
>
> Ingat: "In Kubernetes, security is not a destination. It's a practice."
