# Analisis Kebutuhan — Aspek Container & Infrastructure pada Skill Vulnerability Assessment

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-14
**Target:** `skills/vulnerability-assessment/` (skill existing, diperluas)
**Pertanyaan yang dijawab:** apa yang dibutuhkan agar aspek Container & Infrastructure (container image, Kubernetes, IaC, CI/CD, registry, supply chain) pada skill `vulnerability-assessment` setara dengan aspek network/host/web/cloud/database yang sudah ada, dan bagaimana memperluasnya tanpa merusak persona dan struktur yang sudah berjalan.
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md), [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md), [CND-PERSONA-NEEDS.md](CND-PERSONA-NEEDS.md)
**Sumber brainstorming:** output subagent `brainstorm-container-va` (ringkasan 15 topik, 6 file baru, 6 file existing diperluas, 18 gotchas)

---

## 1. Ringkasan

Skill `vulnerability-assessment` saat ini sudah kuat pada VA jaringan, host, web, cloud, dan database, tetapi **aspek container dan infrastruktur (Infrastructure as Code, CI/CD, registry, supply chain, Kubernetes) hanya disinggung sekilas**. Bukti: `va-methodology.md` menyebut "Container VA" dalam satu tabel baris ("Image scan: base image, dependencies, secrets"), `scanner-config.md` punya satu sub-bagian 4 baris "Container (Trivy/Grype)", dan `asset-discovery.md` menyebut "Container ephemeral — muncul dan hilang. Scan image, bukan runtime." Tiga baris itu tidak cukup untuk memandu analis nyata yang menghadapi cluster Kubernetes, image registry, pipeline CI/CD, dan rantai pasokan perangkat lunak.

Akibatnya, agent yang memuat skill ini akan:
- menyarankan scan image sekali di registry, tanpa memahami bahwa image harus discan di tiga titik (build, registry, runtime);
- melupakan secrets yang tertanam di layer image;
- tidak membedakan kerentanan OS package dari kerentanan dependency bahasa;
- tidak memiliki kerangka untuk RBAC Kubernetes, network policy, pod security, atau admission control;
- tidak tahu cara men-scan IaC (Terraform, CloudFormation, Helm, Kustomize) sebelum deploy;
- tidak memiliki prosedur untuk registry security, image signing, dan supply chain (SBOM, provenance, SLSA);
- tidak mempertimbangkan container ephemeral dan sidecar yang muncul/hilang dalam hitungan detik.

Yang dibutuhkan: **memperluas skill secara additif** — menambah 6 file referensi baru dan memperluas 6 file existing — tanpa menulis ulang yang sudah ada, tanpa merusak persona, dan tanpa menambah materi ujian. Ini adalah pekerjaan **analisis kebutuhan**; implementasi file referensi dilakukan pada fase berikutnya sesuai rencana implementasi (§13).

**Prinsip utama:** container VA bukan "network VA yang dijalankan pada pod". Ia memiliki permukaan serangan, siklus hidup, dan model ancaman yang berbeda (image layer, registry, orchestrator, runtime). Karena itu ia butuh referensi sendiri, bukan sekadar paragraf tambahan.

---

## 2. Kondisi Repo Saat Ini

### 2.1 Inventaris skill vulnerability-assessment

| Berkas | Peran | Kedekatan dengan Container & Infra |
|---|---|---|
| `SKILL.md` | Entry point, persona, capability map, gotchas | Menyebut "container" di Kapan Skill Dipakai dan Decision Frame #3 ("Container → Trivy/Grype"); tidak ada capability group khusus container |
| `references/va-methodology.md` | Siklus 8 fase, pendekatan per target | Satu baris "Container VA" + tabel scanner "Container image → Trivy, Grype, Clair" |
| `references/asset-discovery.md` | Inventaris, scoping, coverage | Satu baris "Container ephemeral — muncul dan hilang. Scan image, bukan runtime." |
| `references/scanner-config.md` | Konfigurasi scanner, tuning, false positive | Sub-bagian 4 baris "Container (Trivy/Grype)" |
| `references/prioritization.md` | Risk-based beyond CVSS | Tidak menyebut container/infra secara spesifik |
| `references/reporting.md` | Struktur laporan multi-audiens | Contoh temuan tidak mencakup container/image/registry |
| `references/cvss-scoring.md` | CVSS v3.1/v4.0 | Berlaku umum; tidak ada konteks container runtime |
| `references/remediation-verification.md` | Tracking, re-scan | Tidak menyebut re-scan image/registry |
| `references/persona.md` | Profil, suara, batas klaim | Tidak ada batas klaim khusus container |
| `references/referensi.md` | Sumber eksternal | Tidak ada referensi container/K8s/IaC |

### 2.2 Kesenjangan terhadap 15 topik container & infra

| # | Topik | Cakupan sekarang | Verdict |
|---|---|---|---|
| 1 | Container image scanning | 1 baris di scanner-config + 1 baris di va-methodology | **gap besar** |
| 2 | Secret detection in image | tidak ada | **gap total** |
| 3 | Runtime security hardening | tidak ada | **gap total** |
| 4 | Kubernetes RBAC | tidak ada | **gap total** |
| 5 | K8s network policy & pod security | tidak ada | **gap total** |
| 6 | IaC scanning | tidak ada | **gap total** |
| 7 | CI/CD pipeline VA | tidak ada | **gap total** |
| 8 | Registry security & image signing | tidak ada | **gap total** |
| 9 | Supply chain VA | tidak ada | **gap total** |
| 10 | Container orchestration security | 1 baris di va-methodology | **gap besar** |
| 11 | Secrets management in container/K8s | tidak ada | **gap total** |
| 12 | Base image selection | tidak ada | **gap total** |
| 13 | Container compliance benchmarks | tidak ada (CIS disebut di host VA) | **gap sebagian** |
| 14 | Runtime threat detection | tidak ada | **gap total** |
| 15 | Ephemeral container coverage | 1 baris di asset-discovery | **gap sebagian** |

Kesimpulan: 12 dari 15 topik sama sekali tidak tercakup; 3 sisanya hanya satu baris. Skill ini saat ini **tidak mampu** memandu VA container secara sistematis.

### 2.3 Catatan kondisi kerja

- Working tree sedang memuat perubahan belum-commit untuk skill lain (persona-conversion). Implementasi container VA tidak boleh me-revert perubahan tersebut.
- `SKILL.md` saat ini 136 baris (di bawah batas keras 450 dan target 120–200). Ada ruang untuk menambah capability group dan gotchas, tetapi kelebihan materi wajib dipindahkan ke `references/`, bukan dibuang (NFR-1 dari PERSONA-INJECTION-NEEDS).
- Semua file `references/` wajib muncul tepat sekali di Reference Documentation (NFR-2). Setiap penambahan berkas referensi baru wajib disertai pembaruan indeks.

---

## 3. Temuan (Bukti Terukur)

### 3.1 Bukti keterbatasan saat ini

| # | Temuan | Lokasi | Cara memeriksa |
|---|---|---|---|
| E1 | "Container VA" hanya satu baris di tabel pendekatan per target | `references/va-methodology.md` baris ~103 | baca file |
| E2 | Sub-bagian "Container (Trivy/Grype)" hanya 4 baris | `references/scanner-config.md` baris ~86 | baca file |
| E3 | "Container ephemeral" hanya satu baris di Gray Area | `references/asset-discovery.md` baris ~48 | baca file |
| E4 | Decision Frame #3 menyebut "Container → Trivy/Grype" tanpa konteks | `SKILL.md` baris ~69 | baca file |
| E5 | Tidak ada file referensi khusus container/infra | `references/` listing | `ls` |
| E6 | Gotchas tidak menyebut container/image/registry/K8s | `SKILL.md` Gotchas | baca file |
| E7 | Capability Map tidak punya kelompok container | `SKILL.md` Capability Map | baca file |

### 3.2 Hasil brainstorming (ringkasan)

Dari output subagent `brainstorm-container-va`:
- **15 topik** yang harus dicakup (daftar §2.2).
- **6 file referensi baru** yang diusulkan:
  1. `container-image-scanning.md` — image scan: layer, OS package, language deps, secrets, base image
  2. `container-runtime-security.md` — runtime hardening, privilege, seccomp, AppArmor, resource limits, read-only FS
  3. `kubernetes-va.md` — RBAC, network policy, pod security, admission control, secrets, etcd
  4. `iac-scanning.md` — Terraform, CloudFormation, Helm, Kustomize, Dockerfile, policy-as-code
  5. `cicd-pipeline-va.md` — pipeline security, secrets in CI, artifact integrity, runner hardening
  6. `supply-chain-va.md` — SBOM, image signing, provenance, SLSA, dependency confusion
- **6 file existing yang diperluas**: `scanner-config.md`, `asset-discovery.md`, `va-methodology.md`, `SKILL.md`, `prioritization.md`, `reporting.md`.
- **18 gotchas** yang perlu ditambahkan (daftar lengkap di Lampiran A).

### 3.3 Risiko bila tidak ditangani

| Risiko | Dampak |
|---|---|
| Agent menyarankan scan image sekali di registry saja | Kerentanan yang muncul saat build atau runtime terlewat |
| Secrets tertanam di layer image tidak terdeteksi | Kebocoran kredensial yang tidak disengaja tetap tayang |
| Kerentanan OS package dan language deps dicampur | Prioritas remediasi salah (patch OS vs update dependency) |
| RBAC/pod security tidak diaudit | Cluster takeover via service account yang over-privileged |
| IaC tidak discan sebelum deploy | Misconfiguration yang bisa dicegah justru terdeploy |
| Registry tidak diamankan | Image berbahaya bisa di-push dan di-pull sembarangan |
| Supply chain tidak diaudit | Dependency confusion, typosquatting, compromised package |
| Container ephemeral tidak dicakup | Coverage gap yang tidak terlaporkan |

---

## 4. Definisi

**Container VA** — proses identifikasi dan pelaporan kerentanan pada image container, runtime container, orchestrator (Kubernetes), registry, pipeline CI/CD, dan rantai pasokan perangkat lunak. Berbeda dari network VA: permukaan serangannya adalah image layer, manifest, dan konfigurasi orchestrator, bukan port dan service.

**Image scanning** — analisis statis image container (layer filesystem) untuk mendeteksi CVE pada OS package dan dependency bahasa, serta secrets dan misconfiguration. Dilakukan di tiga titik: build, registry, dan (opsional) runtime.

**Runtime security hardening** — konfigurasi container saat berjalan: privilege, capabilities, seccomp, AppArmor/SELinux, read-only filesystem, resource limits, user non-root. Bukan scan CVE; ini audit konfigurasi.

**IaC scanning** — analisis statis file Infrastructure as Code (Terraform, CloudFormation, ARM/Bicep, Helm, Kustomize, Dockerfile, Ansible) untuk menemukan misconfiguration sebelum deploy.

**CI/CD pipeline VA** — audit keamanan pipeline: secrets handling, runner isolation, artifact integrity, least privilege pada service account pipeline, dan supply chain build.

**Registry security** — kontrol akses, immutability, scanning otomatis, signing, dan retention policy pada container registry.

**Image signing & provenance** — mekanisme kriptografis untuk membuktikan siapa yang membangun image dan dari source apa (Sigstore/cosign, SLSA, in-toto).

**Supply chain VA** — audit rantai pasokan perangkat lunak: SBOM, dependency confusion, typosquatting, compromised maintainer, build reproducibility, dan attestasi.

**Kubernetes VA** — audit konfigurasi cluster: RBAC, network policy, pod security standards/admission, secrets management, etcd encryption, API server hardening, dan node security.

**Ephemeral container** — container yang muncul dan hilang dalam hitungan detik (serverless, job, sidecar). Tidak bisa discan secara tradisional; harus discan via image atau admission control.

**SBOM (Software Bill of Materials)** — daftar lengkap komponen perangkat lunak dalam sebuah image/artifact. Format: SPDX, CycloneDX.

**SLSA (Supply-chain Levels for Software Artifacts)** — framework tingkat keamanan supply chain, level 1–4.

---

## 5. Ruang Lingkup

### 5.1 Termasuk

- Cakupan container image: base image, OS package, language dependencies, secrets, konfigurasi.
- Cakupan runtime container: privilege, capabilities, seccomp, AppArmor/SELinux, resource limits, read-only FS, user.
- Cakupan Kubernetes: RBAC, network policy, pod security, admission control, secrets, etcd, API server, node.
- Cakupan IaC: Terraform, CloudFormation, ARM/Bicep, Helm, Kustomize, Dockerfile, Ansible, Pulumi.
- Cakupan CI/CD: secrets, runner, artifact integrity, least privilege, supply chain build.
- Cakupan registry: akses, immutability, scanning, signing, retention.
- Cakupan supply chain: SBOM, dependency confusion, typosquatting, provenance, SLSA.
- Cakupan ephemeral container: image scan + admission control + runtime policy.
- Cakupan compliance: CIS Docker Benchmark, CIS Kubernetes Benchmark, NSA/CISA Kubernetes Hardening Guide, NIST SP 800-190.

### 5.2 Tidak termasuk

- Eksploitasi container/K8s (escape, privilege escalation) — masuk domain pentest/red team; skill ini berhenti di identifikasi dan pelaporan. Rujuk `ptes-standard` atau skill ofensif.
- Audit kepatuhan/GRC penuh — rujuk `security-auditor`.
- Threat modeling — rujuk `threat-modeling`.
- Assessment web aplikasi manual — rujuk `web-app-scan`.
- Forensik container/runtime — rujuk `offsec-ir-200` / `ec-ecih`.
- Hardening network perimeter — rujuk skill network defender (jika ada).

### 5.3 Batas dengan skill lain

| Skill existing | Yang TIDAK diduplikasi | Batas yang diambil VA container |
|---|---|---|
| `lf-cks` (Kubernetes security) | Kubernetes mendalam, CKA/CKS | VA membaca konfigurasi dari sudut pandang kerentanan dan misconfiguration, bukan administrasi K8s |
| `web-app-scan` | Assessment web manual | Image yang menjalankan web app discan sebagai container, bukan sebagai web app |
| `cloud VA` (di skill ini) | Cloud misconfiguration | Container yang berjalan di cloud discan sebagai container; cloud infra discan sebagai cloud |
| `security-auditor` | GRC/audit kepatuhan | VA container memetakan temuan ke framework, tidak melakukan audit formal |
| `threat-modeling` | Pemodelan ancaman | VA container menggunakan threat model yang sudah ada, tidak membuat baru |

Prinsip: VA container boleh **merujuk** skill lain, tetapi setiap kali topik mendalam dibutuhkan, ia menunjuk file yang sudah ada alih-alih menulis ulang.

---

## 6. Arsitektur Referensi Usulan

### 6.1 File referensi baru (6)

| # | Berkas | Isi utama | Topik yang dicakup |
|---|---|---|---|
| 1 | `container-image-scanning.md` | Image scan: layer, OS package, language deps, secrets, base image; scan di 3 titik (build/registry/runtime); scanner (Trivy, Grype, Clair, Snyk, Docker Scout); false positive khas image | 1, 2, 12 |
| 2 | `container-runtime-security.md` | Runtime hardening: privilege, capabilities, seccomp, AppArmor/SELinux, read-only FS, resource limits, user non-root; runtime threat detection; Falco/eBPF | 3, 14 |
| 3 | `kubernetes-va.md` | RBAC, network policy, pod security standards, admission control, secrets, etcd, API server, node security; CIS K8s Benchmark | 4, 5 |
| 4 | `iac-scanning.md` | Terraform, CloudFormation, ARM/Bicep, Helm, Kustomize, Dockerfile, Ansible, Pulumi; policy-as-code (OPA/Rego, Checkov, tfsec, Trivy config) | 6 |
| 5 | `cicd-pipeline-va.md` | Pipeline security: secrets, runner isolation, artifact integrity, least privilege, supply chain build, OIDC, SLSA build level | 7 |
| 6 | `supply-chain-va.md` | SBOM, dependency confusion, typosquatting, image signing (cosign/Sigstore), provenance, SLSA, in-toto, registry security | 8, 9 |

### 6.2 File existing yang diperluas (6)

| Berkas | Perluasan yang dibutuhkan |
|---|---|
| `scanner-config.md` | Sub-bagian container diperluas: scan di 3 titik, OS vs language deps, severity threshold per layer, false positive khas image (backported patches pada distro) |
| `asset-discovery.md` | Cakupan container: image inventory, registry, cluster nodes, ephemeral container via image/admission; coverage formula untuk cluster |
| `va-methodology.md` | Pendekatan per target: Container VA sebagai fase terpisah; integrasi dengan CI/CD; frekuensi scan on-push |
| `SKILL.md` | Capability Map: tambah kelompok "Container & Infra"; Gotchas: tambah 18 gotchas; Decision Frame: tambah butir container; Progressive Disclosure: 6 baris baru |
| `prioritization.md` | Konteks container: image dengan exploit publik di base image, runtime exposure, cluster criticality |
| `reporting.md` | Template temuan container: image digest, layer, base image, registry, cluster, namespace |

### 6.3 Aturan indeks

- Setiap berkas referensi baru wajib muncul di **Capability Map**, **Reference Documentation**, dan **Progressive Disclosure** di `SKILL.md`.
- Tidak boleh ada berkas yatim; tidak boleh ada baris indeks ganda.
- Ini menutup drift yang terjadi pada skill lain (mis. `cpent` yang punya 16 berkas tetapi hanya 12 diindeks).

### 6.4 Batas ukuran

| Metrik | Target | Batas keras |
|---|---|---|
| `SKILL.md` baris | 120–200 | 450 |
| Total referensi | ≤ 15 (saat ini 9 + 6 baru = 15) | — |
| Setiap file referensi baru | 80–200 baris | — |
| Gotchas | ≥ 18 (target 10 lama + 18 baru = 28) | — |

---

## 7. Kebutuhan Fungsional

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | Agent mengidentifikasi image container sebagai aset VA yang berdiri sendiri | Capability Map punya kelompok "Container & Infra" |
| FR-2 | Agent membedakan scan OS package vs language dependency dalam image | `container-image-scanning.md` punya tabel pemisah |
| FR-3 | Agent memeriksa secrets tertanam di layer image | Topik #2 tercakup dengan prosedur dan tool |
| FR-4 | Agent mengevaluasi runtime hardening container | `container-runtime-security.md` punya checklist + ambang |
| FR-5 | Agent mengaudit RBAC dan network policy Kubernetes | `kubernetes-va.md` punya checklist + contoh |
| FR-6 | Agent men-scan IaC sebelum deploy | `iac-scanning.md` punya daftar tool + policy-as-code |
| FR-7 | Agent mengevaluasi keamanan pipeline CI/CD | `cicd-pipeline-va.md` punya checklist + hardening |
| FR-8 | Agent mengevaluasi registry dan image signing | `supply-chain-va.md` + sub-bagian registry |
| FR-9 | Agent mempertimbangkan supply chain (SBOM, provenance, SLSA) | `supply-chain-va.md` punya prosedur |
| FR-10 | Agent menangani ephemeral container via image scan + admission | `asset-discovery.md` diperluas dengan formula coverage cluster |
| FR-11 | Agent memetakan temuan container ke compliance benchmark (CIS Docker/K8s, NSA/CISA) | `kubernetes-va.md` + `container-runtime-security.md` punya mapping |
| FR-12 | Agent melaporkan temuan container dengan konteks (digest, layer, base image, registry, cluster, namespace) | `reporting.md` diperluas dengan template |
| FR-13 | Agent tidak merekomendasikan eksploitasi container escape | Persona contract diperluas dengan butir baru |
| FR-14 | Agent merujuk skill lain (`lf-cks`, `web-app-scan`) saat topik mendalam | Batas scope §5.3 terdokumentasi di SKILL.md |

---

## 8. Kebutuhan Non-Fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| NFR-1 | `SKILL.md` tetap 120–200 baris; kelebihan materi dipindah ke `references/`, tidak dibuang | hitung baris |
| NFR-2 | Setiap berkas `references/` muncul tepat sekali di Reference Documentation | paritas tabel 1:1 |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`) | tidak ada tautan ke `docs/` di SKILL.md |
| NFR-4 | Bahasa Indonesia + istilah teknis Inggris; kode dan komentar berbahasa Inggris | konsistensi |
| NFR-5 | Setiap penghapusan/perubahan berkas tercatat di `CHANGELOG.md` | entri changelog |
| NFR-6 | Perubahan bisa diverifikasi ulang oleh mesin: grep, hitung baris, resolusi tautan, paritas tabel | checker repo |
| NFR-7 | Tidak menambah dependensi runtime pada repo | tidak ada paket baru |
| NFR-8 | Frontmatter YAML pada setiap file referensi baru: `name`, `description`, `tags` | validasi |
| NFR-9 | Setiap file referensi baru diakhiri dengan "Best Practices" | validasi |
| NFR-10 | Persona tetap konsisten: penolakan, ketidakpastian eksplisit, tidak ada fakta karangan | uji perilaku |

---

## 9. Konstrain

| ID | Konstrain |
|---|---|
| C-1 | Ikuti `AGENTS.md`: frontmatter, changelog, sync-skills, check-changelog, check-fact-notes |
| C-2 | Tidak mengubah skill lain; perubahan hanya file baru + generated + CHANGELOG/README/SKILL-QUALITY |
| C-3 | Jangan me-revert perubahan persona-conversion yang belum commit |
| C-4 | Lisensi MIT |
| C-5 | Persona, bukan exam prep — tidak ada passing score, bobot, katalog sertifikasi |
| C-6 | Tidak menambah materi ujian; referensi ke fakta ujian (jika ada) lewat `docs/CERTIFICATION-FACTS.md` |
| C-7 | Skill `vulnerability-assessment` bukan skill bersertifikat; tidak perlu mendaftar ke `check-fact-notes.js` |

---

## 10. Antipattern yang Dilarang

| ID | Antipattern | Mengapa salah |
|---|---|---|
| AP-1 | Menulis ulang `scanner-config.md` dari nol alih-alih memperluas | kehilangan tuning yang sudah ada; perubahan besar tanpa alasan |
| AP-2 | Menggabungkan semua topik container ke satu file besar | melanggar "satu domain per file"; sulit dipelihara |
| AP-3 | Menyalin isi `lf-cks` ke `kubernetes-va.md` | duplikasi; batas scope §5.3 dilanggar |
| AP-4 | Menambah materi ujian (CISA, CKS, dll.) ke skill | melanggar persona; FR-8 dari PERSONA-INJECTION-NEEDS |
| AP-5 | Mengklaim CVE atau ambang tanpa sumber | kredibilitas runtuh; aturan ketidakpastian |
| AP-6 | Mengabaikan ephemeral container karena "tidak bisa discan" | coverage gap tidak terlaporkan |
| AP-7 | Hanya scan image di registry, tidak di build/runtime | temuan yang muncul di build/runtime terlewat |
| AP-8 | Mencampur OS package CVE dengan language dependency CVE | prioritas remediasi salah |
| AP-9 | Tidak membedakan "kerentanan" dari "misconfiguration" pada container | semua temuan scanner dianggap kerentanan |
| AP-10 | Membuat `SKILL.md` > 450 baris | melanggar NFR-1 |
| AP-11 | Menambah berkas referensi tanpa memperbarui indeks | berkas yatim; drift |
| AP-12 | Menambah dependensi runtime baru di `scripts/` | melanggar NFR-7 |
| AP-13 | Mengubah konten skill yang tidak terkait container | scope creep |
| AP-14 | Menyatakan "sudah selesai" tanpa verifikasi indeks 1:1 | drift tidak terdeteksi |

---

## 11. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Cakupan 15 topik membanjiri persona | jawaban dangkal di semua topik | jangkar pada 6 file baru; setiap file berfokus satu domain |
| Duplikasi dengan `lf-cks` | repo redundan, user bingung | tabel batas §5.3 + rujukan silang |
| Drift ke exam prep | skill kehilangan identitas persona | tanpa angka ujian; deskripsi menegaskan "bukan persiapan ujian" |
| Vendor lock-in (tool tertentu) | jawaban tidak portabel | konsep dulu, contoh vendor diberi label "contoh" |
| Klaim CVE/ambang karangan | kredibilitas rusak | aturan ketidakpastian + larangan output palsu |
| Perubahan konfigurasi container memutus layanan | bahaya nyata | rollback wajib, window waktu, kontak darurat |
| Scope creep ke ofensif | salah fungsi | validasi defensif saja; rujuk skill red team |
| Berkas yatim | indeks tidak sinkron | uji 1:1 indeks–berkas di kriteria penerimaan |
| Ephemeral container tidak tercakup | coverage gap | image scan + admission control + runtime policy |

---

## 12. Kriteria Penerimaan

### 12.1 Struktural

- 6 file referensi baru ada di `skills/vulnerability-assessment/references/`, masing-masing dengan frontmatter `name`/`description`/`tags` dan diakhiri "Best Practices".
- 6 file existing diperluas sesuai §6.2.
- `SKILL.md` memuat: Capability Map dengan kelompok "Container & Infra", Reference Documentation dengan 15 baris (9 lama + 6 baru), Gotchas ≥ 28, Progressive Disclosure dengan 6 baris baru.
- Setiap berkas muncul di tabel Reference Documentation (tidak ada berkas yatim); tidak ada baris indeks ganda.
- `node scripts/sync-skills.js` memperbarui `manifest.json`, `skills/index.json`, dan plugin.
- `README.md` dan `docs/SKILL-QUALITY.md` diperbarui (jika skill disebut).
- `node scripts/check-changelog.js --base HEAD` lulus dengan entri baru.
- `node scripts/check-fact-notes.js` lulus tanpa mendaftarkan `vulnerability-assessment` (bukan skill bersertifikat).
- `grep -R` untuk pola materi ujian di `skills/vulnerability-assessment/` = 0 hasil (kecuali kalimat penolakan).
- Resolusi tautan relatif: 0 tautan rusak.

### 12.2 Perilaku (8 skenario uji)

| # | Prompt | Perilaku yang diharapkan |
|---|---|---|
| 1 | "Scan image nginx:latest di registry kami" | meminta digest, scan di 3 titik, bedakan OS vs language deps, sebut false positive khas image |
| 2 | "Apakah pod kami aman? Kami pakai service account default" | audit RBAC, sebut least privilege, tawarkan role terbatas |
| 3 | "Terraform kami deploy S3 bucket public" | identifikasi misconfiguration IaC, sarankan policy-as-code, sebut remediasi |
| 4 | "Pipeline CI kami simpan secret di env var plaintext" | audit pipeline, sarankan OIDC/secrets manager, sebut risiko |
| 5 | "Base image kami dari Docker Hub tanpa pin digest" | sebut supply chain risk, sarankan pin digest + signing |
| 6 | "Container kami berjalan sebagai root" | audit runtime hardening, sebut user non-root, seccomp, read-only FS |
| 7 | "Kami punya pod yang muncul 5 detik lalu hilang" | sebut ephemeral container, sarankan image scan + admission control |
| 8 | "Berapa CVE di image kami yang bisa dieksploitasi?" | bedakan CVE dari misconfiguration, sebut ketidakpastian, sarankan verifikasi |

Lulus bila: persona konsisten, decision frame dipakai eksplisit, tidak ada fakta karangan, dan setiap temuan punya bukti + remediasi.

---

## 13. Rencana Implementasi (bila disetujui)

1. **Fase A — kerangka:** buat 6 file referensi baru (kosong dengan frontmatter + skeleton), perbarui `SKILL.md` (Capability Map, Reference Documentation, Progressive Disclosure).
2. **Fase B — konten image & runtime:** isi `container-image-scanning.md` dan `container-runtime-security.md`.
3. **Fase C — konten K8s & IaC:** isi `kubernetes-va.md` dan `iac-scanning.md`.
4. **Fase D — konten pipeline & supply chain:** isi `cicd-pipeline-va.md` dan `supply-chain-va.md`.
5. **Fase E — perluasan file existing:** perluas `scanner-config.md`, `asset-discovery.md`, `va-methodology.md`, `prioritization.md`, `reporting.md`.
6. **Fase F — SKILL.md final:** tambah gotchas (18 baru), perbarui Decision Frame, Persona Contract (butir baru), dan gotchas.
7. **Fase G — integrasi:** `node scripts/sync-skills.js`, baris README + SKILL-QUALITY (jika perlu), entri `CHANGELOG.md`.
8. **Fase H — verifikasi:** tiga checker repo, uji indeks 1:1, grep angka ujian, jalankan 8 skenario uji.

---

## 14. Keputusan yang Perlu Disetujui

| # | Keputusan | Opsi | Rekomendasi |
|---|---|---|---|
| D1 | Jumlah file referensi baru | 6 (usulan) / lebih sedikit (gabung) | **6** — satu domain per file, paritas dengan pola `cpent` |
| D2 | Cakupan Kubernetes | ringkas (VA perspective) / mendalam | **ringkas** — mendalam sudah ada di `lf-cks` |
| D3 | Cakupan compliance benchmark | CIS Docker + CIS K8s + NSA/CISA + NIST 800-190 / hanya CIS | **semua 4** — mapping, bukan audit penuh |
| D4 | Gotchas baru | 18 (usulan) / lebih sedikit | **18** — sesuai brainstorming |
| D5 | Apakah perluas Persona Contract | tambah butir container / tidak | **tambah 1 butir** (tidak merekomendasikan eksploitasi container escape) |
| D6 | Apakah perluas Decision Frame | tambah butir container / tidak | **tambah 1 butir** (scan image di 3 titik) |
| D7 | Dokumen ini | `docs/` permanen / hapus setelah implementasi | **permanen** — jejak keputusan desain |
| D8 | Penomoran changelog | satu entri saat implementasi | **satu entri** dengan versi berikutnya |

---

## 15. Metrik

| Metrik | Kondisi awal (2026-11-14) | Target |
|---|---|---|
| File referensi container/infra | 0 | 6 |
| File existing diperluas | 0 (hanya 1 baris) | 6 |
| Gotchas terkait container | 0 | 18 |
| Capability group container | 0 | 1 |
| Topik tercakup (dari 15) | 3 (sebagian) | 15 |
| Indeks 1:1 | lulus (9/9) | lulus (15/15) |
| Pola materi ujian | 0 | 0 |
| Tautan rusak | 0 | 0 |

---

## Lampiran A — 18 Gotchas (dari brainstorming)

1. **Image yang discan di registry tidak sama dengan image yang berjalan.** Tag `latest` bisa berubah; digest adalah identitas nyata. Selalu referensikan image by digest, bukan tag.
2. **Secrets tertanam di layer image tetap ada meski dihapus di layer berikutnya.** `docker history` dan layer inspection menampakkan secret yang "sudah dihapus". Scan semua layer, bukan hanya final filesystem.
3. **Base image yang "slim" tidak berarti aman.** Slim mengurangi ukuran, tidak mengurangi CVE. Verifikasi CVE base image secara terpisah.
4. **OS package CVE dan language dependency CVE dicampur oleh scanner.** Pisahkan: OS package → patch OS; language dep → update lockfile. Prioritas dan remediasi berbeda.
5. **Backported patches membuat versi lama tetap aman.** Distro (Debian/Ubuntu/RHEL) backport fix tanpa bump versi upstream. Verifikasi dengan vendor advisory, bukan versi semata.
6. **Container berjalan sebagai root secara default.** Image yang tidak menentukan `USER` berjalan root. Audit `USER` directive dan runtime security context.
7. **Capabilities default container masih terlalu luas.** `CAP_NET_RAW`, `CAP_SYS_CHROOT`, dll. Drop semua, tambah hanya yang perlu.
8. **Seccomp profile default tidak cukup untuk workload sensitif.** Gunakan custom seccomp profile atau runtime default dengan review.
9. **Network policy default allow-all di banyak cluster.** Pod bisa berkomunikasi bebas. Audit NetworkPolicy per namespace.
10. **RBAC cluster-admin yang diberikan ke service account.** Service account dengan cluster-admin = cluster takeover. Audit ClusterRoleBinding.
11. **Secrets Kubernetes disimpan base64, bukan terenkripsi, di etcd.** Aktifkan encryption at rest. Jangan anggap Secret = aman.
12. **Image pull dari registry tanpa verifikasi signature.** Admission controller (Kyverno/OPA Gatekeeper) wajib memverifikasi signature.
13. **CI/CD runner yang shared dan tidak terisolasi.** Job bisa mengakses secret job lain. Gunakan runner dedicated dan least privilege.
14. **Secrets di pipeline yang di-print ke log.** Masking tidak selalu bekerja. Audit log output.
15. **Dependency confusion: package internal vs public.** Attacker upload package dengan nama internal ke registry publik. Gunakan scope/private registry.
16. **Typosquatting pada dependency.** Nama mirip package populer. Verifikasi nama package dan hash.
17. **Ephemeral container tidak muncul di inventaris tradisional.** Scan image + admission control + runtime policy; jangan andalkan network scan.
18. **SBOM yang tidak di-generate atau tidak diverifikasi.** Tanpa SBOM, tidak tahu komponen yang rentan. Generate SBOM di build, simpan, dan verifikasi.

---

## Lampiran B — Log Sumber

| Sumber | Yang diambil | Status |
|---|---|---|
| `skills/vulnerability-assessment/SKILL.md` | Capability Map, gotchas, decision frame | dibaca 2026-11-14 |
| `skills/vulnerability-assessment/references/*.md` | 9 file referensi existing | dibaca 2026-11-14 |
| `docs/PERSONA-INJECTION-NEEDS.md` | Format analisis kebutuhan, struktur, ID kebutuhan | dibaca 2026-11-14 |
| `docs/PUBLISHING-NEEDS.md` | Format, ruang lingkup, kriteria penerimaan, risiko | dibaca 2026-11-14 |
| `docs/CND-PERSONA-NEEDS.md` | Format mendalam, arsitektur referensi, batas scope | dibaca 2026-11-14 |
| Output subagent `brainstorm-container-va` | 15 topik, 6 file baru, 6 file diperluas, 18 gotchas | ringkasan dari prompt |
| `AGENTS.md` | Konvensi repo, changelog, sync | dibaca 2026-11-14 |