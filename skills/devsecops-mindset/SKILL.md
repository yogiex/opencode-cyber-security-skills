---
name: devsecops-mindset
description: Panduan pola pikir dan mindset DevSecOps untuk mengintegrasikan keamanan dalam siklus pengembangan secara berkelanjutan, tanpa fokus pada alat/tools tertentu.
license: MIT
compatibility: opencode
metadata:
  audience: developer, security engineer, platform engineer, tech lead, product manager
  approach: principles-first
---

# DevSecOps Mindset

## Apa itu DevSecOps Mindset

DevSecOps bukanlah peran, tools, atau pipeline — melainkan **cara berpikir** tentang keamanan sebagai bagian integral dari pengembangan perangkat lunak, bukan sebagai fase terpisah atau pintu gerbang di akhir.

### Prinsip Dasar

- **Security is Everyone's Responsibility** — bukan hanya tugas tim keamanan. Developer, Ops, Product, QA — semua punya peran.
- **Shift-Left Security** — semakin awal keamanan dipertimbangkan, semakin murah dan cepat perbaikannya.
- **Security as Code** — kebijakan keamanan, konfigurasi, dan pengujian diperlakukan seperti kode: versi-controlled, reviewable, testable, automatable.

## Pergeseran Pola Pikir

Bukan Ini → Ini:

| Mindset Lama | Mindset DevSecOps |
|---|---|
| "Tim keamanan memeriksa di akhir" | "Semua orang bertanggung jawab sejak awal" |
| "Cari semua kerentanan" | "Kurangi risiko secara berkelanjutan" |
| "Keamanan menghambat rilis" | "Keamanan memungkinkan rilis yang aman" |
| "Kepatuhan adalah checklist" | "Kepatuhan berkelanjutan terotomasi" |
| "Takut temuan keamanan" | "Transparansi dan perbaikan berkelanjutan" |
| "Security gate di akhir pipeline" | "Security feedback loop di setiap tahap" |
| "Tools akan menyelesaikan masalah" | "Proses dan budaya lebih penting dari tools" |

## Prinsip Inti DevSecOps

### 1. Continuous Security (Bukan Security Checkpoint)

Keamanan berjalan **sepanjang siklus hidup**, bukan hanya di fase tertentu:

- **Planning** — threat modeling saat mendesain fitur, bukan setelah jadi
- **Coding** — IDE plugin, pre-commit hooks, dependency check otomatis
- **Review** — security-aware code review checklist
- **CI/CD** — automated security test sebagai pipeline stage
- **Deploy** — infrastructure security validation
- **Operate** — monitoring, alerting, incident response siap

### 2. Automate Security Feedback

Setiap keputusan keamanan yang bisa di-automasi, harus di-automasi:

- SAST, DAST, SCA di pipeline
- Policy as code (OPA, Rego, etc.)
- Threshold-based gating (bukan human gate)
- Auto-remediation untuk isu umum

### 3. Fail Fast, Belajar Lebih Cepat

- Temukan kerentanan sedini mungkin saat dampak masih kecil
- Setiap temuan adalah data untuk memperbaiki proses, bukan menyalahkan orang
- Post-mortem tanpa blame — fokus pada sistem dan proses

### 4. Keamanan yang Terukur

Ukur keamanan seperti metrik lainnya:

- **Lead time** untuk perbaikan kerentanan (MTTR)
- **Waktu deteksi** kerentanan dari commit ke temuan
- **Jumlah temuan** yang terblokir di pipeline (sebelum produksi)
- **Coverage** — berapa persen dependensi yang discan, berapa persen kode yang di-test keamanannya
- **False positive rate** — agar tim tidak lelah dengan alert noise

### 5. Blameless Culture

- Kerentanan yang ditemukan adalah kemenangan, bukan kegagalan
- Insiden adalah kesempatan belajar, bukan mencari siapa yang salah
- Reward perilaku yang mengutamakan keamanan (mis: melaporkan kerentanan, mengusulkan perbaikan)

## Pola Perilaku DevSecOps

Seorang praktisi DevSecOps berpikir seperti ini di setiap fase:

### Saat Planning

- "Apa data sensitif yang akan ditangani fitur ini?"
- "Siapa yang seharusnya punya akses? Siapa yang tidak?"
- "Bagaimana jika user jahat menggunakan fitur ini?"
- "Apa asumsi keamanan yang kita buat?"

### Saat Coding

- "Input apa yang tidak saya validasi?"
- "Bagaimana error handling saya? Apakah bocor informasi?"
- "Apakah library ini punya kerentanan?"
- "Bagaimana secret/hardcoded credential terhindar?"

### Saat CI/CD

- "Apa yang terjadi jika pipeline ini di-tamper?"
- "Apakah artifact yang di-build sudah diverifikasi?"
- "Siapa yang bisa merge ke branch produksi?"
- "Apakah ada perubahan infrastructure yang tidak terduga?"

### Saat Operasi

- "Apa yang akan kita lakukan jika aplikasi ini diserang sekarang?"
- "Apakah logging kita cukup untuk forensic analysis?"
- "Siapa yang punya akses ke production?"
- "Apakah backup bisa dipulihkan?"

## Anti-Patterns

- **Security as a phase** — menambahkan keamanan hanya di akhir siklus
- **Tool-first approach** — beli tools dulu, baru pikirkan proses
- **Alert fatigue** — terlalu banyak scanning tanpa prioritas dan triase
- **Gatekeeper mentality** — tim keamanan jadi bottleneck approval
- **Perfect security** — menunggu solusi sempurna, padahal incremental improvement lebih baik
- **Checkbox compliance** — melakukan scanning hanya karena regulasi, bukan untuk keamanan nyata
- **Security theater** — tampak aman tapi tidak benar-benar aman

## Pertanyaan Kunci DevSecOps Engineer

Tanyakan ini pada diri sendiri saat bekerja:

1. "How do we **know** this is secure enough?"
2. "What's the **fastest feedback loop** we can give to developers?"
3. "Can we **automate** this check so no human has to remember it?"
4. "What would **break** if this component is compromised?"
5. "Are we **measuring** the right thing?"
6. "What's the **blast radius** of this change?"
7. "If this goes wrong, how fast can we **detect** and **respond**?"

## Ketika Menggunakan Skill Ini

**Gunakan ketika:**
- Mendesain atau mengevaluasi workflow pengembangan
- Ditanya tentang prinsip DevSecOps
- Membantu tim mengadopsi praktik keamanan
- Merencanakan integrasi keamanan dalam pipeline CI/CD
- Mereview arsitektur atau proses dari sisi keamanan
- Membangun budaya keamanan dalam organisasi

**Jangan gunakan ketika:**
- Membutuhkan panduan teknis spesifik (scanning tool, pipeline config) — gunakan skill web-app-scan atau security-documentation
- Membutuhkan threat modeling teknis — gunakan skill threat-modeling
- Sudah jelas tool dan proses yang dibutuhkan — skill ini hanya untuk mindset
