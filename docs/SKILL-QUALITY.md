# Skill Quality Ledger

Matriks status kualitas 29 skill. Tujuannya membuat pekerjaan tuning **terlihat** — bukan tersembunyi di riwayat commit — sampai cakupan cukup untuk ditegakkan lewat CI.

Diperbarui: **2026-11-10** (setelah 0.21.0 — cabang `feat/ec-cnd-persona-injection` digabung dan `ec-cnd` masuk matriks; 0.20.0 — katalog sertifikasi dibersihkan dan Decision Frame mencapai 23/28; 0.19.0 — sembilan skill bersertifikat menjadi persona praktisi).

> `ec-cnd` sudah berada di `dev` (berkasnya mendarat pada `abae7be`, cabangnya digabung pada 0.21.0), jadi barisnya kini ada di matriks dan jumlah skill di sini 29.

## Kriteria

| Kolom | Arti | Cara diperiksa |
|---|---|---|
| **Trigger** | Ada kondisi pemakaian eksplisit di `description` atau bagian "Kapan Digunakan" | pemeriksaan struktur, bukan uji perilaku |
| **Frame** | Ada `## Decision Frame` berisi aturan keputusan, bukan pertanyaan retoris | `grep '^## Decision Frame'` |
| **Provenance** | Angka/versi tertaut ke [CERTIFICATION-FACTS.md](CERTIFICATION-FACTS.md) | `node scripts/check-fact-notes.js` |
| **Persona** | Skill memuat blok persona (Profil, Cara Memerankan, Persona Contract) dan **nol** angka ujian | `grep` pola materi ujian = 0 hasil |
| **Refs** | Jumlah file di `references/` | hitung file `.md` |
| **Failure modes** | Ada bagian `Gotchas`/`Failure`/`Kesalahan` | `grep '^## .*Gotcha'` |

Status: **Selesai** = Frame + (Provenance **atau** Persona). **Sebagian** = salah satu dari keduanya. **Belum** = tidak keduanya.

Alasan dua jalur: skill bersertifikat memilih **persona** (tanpa angka ujian, jadi tidak ada yang perlu dilacak ke fact sheet), sedangkan skill standar memilih **provenance** (versinya harus bisa dilacak). Sebelum aturan ini, konversi persona akan tampak sebagai kemunduran — padahal sebaliknya.

## Matriks

| Skill | Trigger | Frame | Provenance | Persona | Refs | Failure modes | Status |
|---|---|---|---|---|---|---|---|
| code-security-audit | — | — | — | — | 4 | — | Belum |
| comptia-cysa | ya | ya | — | ya | 6 | ya | Selesai |
| cpent | ya | ya | — | ya | 21 | ya | Selesai |
| devsecops-mindset | — | — | — | — | 0 | — | Belum |
| ec-cnd | ya | ya | — | ya | 14 | ya | Selesai |
| ec-ecih | ya | ya | — | ya | 8 | ya | Selesai |
| incident-response-plan | — | ya | — | — | 0 | — | Sebagian |
| lf-cks | ya | ya | — | ya | 10 | ya | Selesai |
| log-management-nist-800-92 | ya | — | — | — | 0 | — | Belum |
| mitre-attack | ya | ya | ya | — | 0 | — | Selesai |
| nist-800-53 | ya | ya | ya | — | 0 | — | Selesai |
| offsec-ir-200 | ya | ya | — | ya | 11 | ya | Selesai |
| offsec-pen-300 | ya | ya | — | ya | 10 | ya | Selesai |
| offsec-soc-200 | ya | ya | — | ya | 6 | ya | Selesai |
| offsec-th-200 | ya | ya | — | ya | 10 | ya | Selesai |
| offsec-web-300 | ya | ya | — | ya | 11 | ya | Selesai |
| oscp-methodology | ya | ya | — | ya | 11 | ya | Selesai |
| owasp-top10-2025 | ya | ya | — | — | 1 | ya | Sebagian |
| ptes-standard | ya | ya | — | — | 11 | ya | Sebagian |
| risk-management-framework | ya | ya | — | — | 0 | — | Sebagian |
| security-auditor | — | — | — | — | 0 | — | Belum |
| security-documentation | ya | ya | — | — | 1 | ya | Sebagian |
| soc-analyst | ya | — | — | — | 0 | — | Belum |
| threat-intelligence | ya | ya | — | — | 8 | ya | Sebagian |
| threat-modeling | ya | ya | — | — | 0 | — | Sebagian |
| waf-evasion-methodology | ya | ya | — | — | 4 | ya | Sebagian |
| web-app-scan | ya | ya | — | — | 0 | ya | Sebagian |
| web-pentest-payloads | ya | ya | — | — | 39 | ya | Sebagian |
| web-reconnaissance | ya | ya | — | — | 9 | ya | Sebagian |

## Ringkasan

| Status | Jumlah |
|---|---|
| Selesai | 13 |
| Sebagian | 11 |
| Belum | 5 |

Cakupan **Frame 24/29 (83%)**, naik dari 19/28 pada 0.19.0 setelah `threat-modeling`, `incident-response-plan`, `risk-management-framework`, dan `owasp-top10-2025` mendapat Decision Frame operasional pada 0.20.0, lalu `ec-cnd` masuk pada 0.21.0.

Lima "Belum" yang tersisa bukan kekurangan frame semata: `security-auditor`, `log-management-nist-800-92`, `devsecops-mindset`, dan `soc-analyst` adalah skill monolitik tanpa berkas referensi (backlog C), sedangkan `code-security-audit` sudah punya 4 referensi tetapi belum punya frame.

## Backlog

| Poin | Isi | Alasan urutan |
|---|---|---|
| **C** | Pecah skill monolitik tanpa references: `security-auditor` (282 baris), `log-management-nist-800-92` (415), `devsecops-mindset` (350), `soc-analyst` | empat "Belum" terakhir ada di sini |
| **D2** | Tambahkan `Gotchas` pada `threat-modeling`, `incident-response-plan`, `risk-management-framework` | frame sudah ada, failure modes belum |
| **E** | Perluas fact sheet ke standar non-sertifikasi (PTES, STIX, TLP, OWASP CRS, PCI DSS), lalu daftarkan tiga skill "Sebagian" ke `check-fact-notes.js` | membuka jalan 3 "Sebagian" menjadi "Selesai" |
| **H** | Sisa tautan tingkat-3: exam blueprint di `ec-cnd/references/referensi.md`, halaman sertifikasi `cpent` dipertahankan sebagai jangkar identitas | `ptes-standard` sudah dibersihkan pada 0.20.0 |
| **F** | Evaluasi perilaku: himpunan tugas aktivasi + A/B ablation | membuktikan tuning menaikkan performa, bukan hanya kerapian |

## Kapan enforcement dibuat

Cakupan Frame kini **24/29 (83%)**, melewati ambang yang ditetapkan dokumen ini sejak 0.6.0 (≥80%). Artinya penegakan Frame di CI sudah bisa dinyalakan: 5 pengecualian (`security-auditor`, `log-management-nist-800-92`, `devsecops-mindset`, `soc-analyst`, `code-security-audit`) jauh lebih kecil dan lebih mudah dipertahankan daripada 9 pengecualian sebelumnya.

Keputusan menyalakannya sengaja ditunda ke pekerjaan tersendiri, karena checker baru butuh allowlist yang ditulis eksplisit dan diuji terhadap working tree yang juga dipegang sesi lain.

`check-fact-notes.js` menegakkan **2** skill (keduanya standar: `mitre-attack`, `nist-800-53`).

## Cara memperbarui

1. Jalankan tiga pemeriksaan: `node scripts/check-fact-notes.js`, `node scripts/check-changelog.js`, dan hitung ulang kolom Ref.
2. Perbarui baris yang berubah dan tanggal di atas.
3. Catat perubahan file ini di `CHANGELOG.md`.
