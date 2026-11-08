# Skill Quality Ledger

Matriks status kualitas 28 skill. Tujuannya membuat pekerjaan tuning **terlihat** — bukan tersembunyi di riwayat commit — sampai cakupan cukup untuk ditegakkan lewat CI.

Diperbarui: **2026-11-08** (setelah poin A dan B).

## Kriteria

| Kolom | Arti | Cara diperiksa |
|---|---|---|
| **Trigger** | Ada kondisi pemakaian eksplisit di `description` atau bagian "When to Use"/"Kapan Menggunakan" | pemeriksaan struktur, bukan uji perilaku |
| **Frame** | Ada `## Decision Frame` berisi aturan keputusan, bukan pertanyaan retoris | `grep '^## Decision Frame'` |
| **Provenance** | Angka/versi tertaut ke [CERTIFICATION-FACTS.md](CERTIFICATION-FACTS.md) | `node scripts/check-fact-notes.js` |
| **Refs** | Jumlah file di `references/` | hitung file `.md` |
| **Failure modes** | Ada bagian `Gotchas`/`Failure`/`Kesalahan` | `grep '^## .*Gotcha'` |

Status: **Selesai** = Frame + Provenance. **Sebagian** = salah satu. **Belum** = tidak keduanya.

## Matriks

| Skill | Trigger | Frame | Provenance | Refs | Failure modes | Status |
|---|---|---|---|---|---|---|
| code-security-audit | — | — | — | 4 | — | Belum |
| comptia-cysa | ya | ya | ya | 6 | ya | Selesai |
| cpent | — | ya | ya | 11 | ya | Selesai |
| devsecops-mindset | — | — | — | 0 | — | Belum |
| ec-ecih | — | ya | ya | 7 | ya | Selesai |
| incident-response-plan | — | — | — | 0 | — | Belum |
| lf-cks | — | ya | ya | 9 | ya | Selesai |
| log-management-nist-800-92 | ya | — | — | 0 | — | Belum |
| mitre-attack | ya | ya | ya | 0 | — | Selesai |
| nist-800-53 | ya | ya | ya | 0 | — | Selesai |
| offsec-ir-200 | — | ya | ya | 7 | ya | Selesai |
| offsec-pen-300 | — | ya | ya | 9 | ya | Selesai |
| offsec-soc-200 | — | ya | ya | 6 | ya | Selesai |
| offsec-th-200 | — | ya | ya | 8 | ya | Selesai |
| offsec-web-300 | — | ya | ya | 6 | ya | Selesai |
| oscp-methodology | — | ya | ya | 11 | ya | Selesai |
| owasp-top10-2025 | ya | — | — | 1 | ya | Belum |
| ptes-standard | ya | ya | — | 11 | ya | Sebagian |
| risk-management-framework | ya | — | — | 0 | — | Belum |
| security-auditor | — | — | — | 0 | — | Belum |
| security-documentation | ya | — | — | 0 | — | Belum |
| soc-analyst | ya | — | — | 0 | — | Belum |
| threat-intelligence | ya | ya | — | 8 | ya | Sebagian |
| threat-modeling | ya | — | — | 0 | — | Belum |
| waf-evasion-methodology | ya | ya | — | 4 | ya | Sebagian |
| web-app-scan | — | — | — | 0 | — | Belum |
| web-pentest-payloads | — | — | — | 39 | — | Belum |
| web-reconnaissance | — | — | — | 0 | — | Belum |

## Ringkasan

| Status | Jumlah |
|---|---|
| Selesai | 12 |
| Sebagian | 3 |
| Belum | 13 |

Tiga "Sebagian" adalah hasil poin B: frame sudah ada, provenance sengaja tidak dipasang karena fact sheet belum memuat PTES, STIX 2.1, TLP 2.0, atau OWASP CRS.

## Backlog

| Poin | Isi | Alasan urutan |
|---|---|---|
| **C** | Pecah skill monolitik tanpa references: `security-auditor` (17,8 KB), `log-management-nist-800-92` (24,3 KB), `devsecops-mindset` (23,5 KB), `soc-analyst` (10,1 KB) | dampak terbesar pada kualitas jawaban, tapi paling mahal dan paling berisiko |
| **D** | Skill kecil yang belum punya frame/gotchas: `threat-modeling`, `web-app-scan`, `incident-response-plan`, `security-documentation`, `web-reconnaissance`, `owasp-top10-2025`, `risk-management-framework` | murah, cepat, menaikkan cakupan |
| **E** | Perluas fact sheet ke standar non-sertifikasi (PTES, STIX, TLP, OWASP CRS, PCI DSS) lalu daftarkan `ptes-standard`, `threat-intelligence`, `waf-evasion-methodology` ke `check-fact-notes.js` | membuka jalan agar 3 "Sebagian" menjadi "Selesai" |
| **F** | Evaluasi perilaku: himpunan tugas aktifasi + A/B ablation | membuktikan tuning menaikkan performa, bukan hanya kerapian |

## Kapan enforcement dibuat

`check-fact-notes.js` sudah menegakkan provenance. Enforcement untuk **Frame** sengaja ditunda sampai cakupan ≥80% (≥23 dari 28), karena checker sekarang butuh allowlist 13 pengecualian — rapuh dan menyembunyikan pekerjaan tersisa.

## Cara memperbarui

1. Jalankan tiga pemeriksaan: `node scripts/check-fact-notes.js`, `node scripts/check-changelog.js`, dan hitung ulang kolom Ref.
2. Perbarui baris yang berubah dan tanggal di atas.
3. Catat perubahan file ini di `CHANGELOG.md`.
