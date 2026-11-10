# Skill Quality Ledger

Matriks status kualitas 28 skill. Tujuannya membuat pekerjaan tuning **terlihat** — bukan tersembunyi di riwayat commit — sampai cakupan cukup untuk ditegakkan lewat CI.

Diperbarui: **2026-11-10** (setelah 0.19.0 — sembilan skill bersertifikat menjadi persona praktisi; 0.18.0 — `offsec-ir-200` verifikasi integritas file; 0.17.0 — `ec-cnd`; 0.16.0 — README dan penutupan celah repo).

> `ec-cnd` (persona network defender) berada di cabang `feat/ec-cnd-persona-injection`, belum di `dev`. Barisnya ditambahkan ke matriks ini saat cabang itu digabung. Karena itu jumlah skill di sini 28, bukan 29.

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
| ec-ecih | ya | ya | — | ya | 8 | ya | Selesai |
| incident-response-plan | — | — | — | — | 0 | — | Belum |
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
| owasp-top10-2025 | ya | — | — | — | 1 | ya | Belum |
| ptes-standard | ya | ya | — | — | 11 | ya | Sebagian |
| risk-management-framework | ya | — | — | — | 0 | — | Belum |
| security-auditor | — | — | — | — | 0 | — | Belum |
| security-documentation | ya | ya | — | — | 1 | ya | Sebagian |
| soc-analyst | ya | — | — | — | 0 | — | Belum |
| threat-intelligence | ya | ya | — | — | 8 | ya | Sebagian |
| threat-modeling | ya | — | — | — | 0 | — | Belum |
| waf-evasion-methodology | ya | ya | — | — | 4 | ya | Sebagian |
| web-app-scan | ya | ya | — | — | 0 | ya | Sebagian |
| web-pentest-payloads | ya | ya | — | — | 39 | ya | Sebagian |
| web-reconnaissance | ya | ya | — | — | 9 | ya | Sebagian |

## Ringkasan

| Status | Jumlah |
|---|---|
| Selesai | 12 |
| Sebagian | 7 |
| Belum | 9 |

Sembilan skill berpindah dari "provenance" ke "persona" pada 0.19.0 tanpa kehilangan status: `comptia-cysa`, `ec-ecih`, `lf-cks`, `offsec-ir-200`, `offsec-pen-300`, `offsec-soc-200`, `offsec-th-200`, `offsec-web-300`, `oscp-methodology`. Provenance ikut dicabut karena angka ujian memang dihapus — bukan karena note-nya hilang.

Tujuh "Sebagian" tersisa karena provenance belum bisa dipasang, bukan karena frame belum ada: fact sheet belum memuat PTES, STIX 2.1, TLP 2.0, OWASP CRS, dan versi WSTG. Rinciannya: `ptes-standard`, `security-documentation`, `threat-intelligence`, `waf-evasion-methodology`, `web-app-scan`, `web-pentest-payloads`, `web-reconnaissance`.

## Backlog

| Poin | Isi | Alasan urutan |
|---|---|---|
| **G** | Bersihkan lampiran sertifikasi (tabel biaya ujian, vendor latihan soal, "exam guide"): `security-auditor` (paling parah), `log-management-nist-800-92`, `devsecops-mindset`, `owasp-top10-2025` | murah, menghapus isi yang cepat basi, tanpa menyentuh pengetahuan teknis |
| **D** | Skill kecil yang belum punya frame/gotchas: `threat-modeling`, `incident-response-plan`, `owasp-top10-2025`, `risk-management-framework` | cepat, menaikkan cakupan frame |
| **C** | Pecah skill monolitik tanpa references: `security-auditor`, `log-management-nist-800-92`, `devsecops-mindset`, `soc-analyst` | dampak terbesar pada kualitas jawaban, tapi paling mahal |
| **E** | Perluas fact sheet ke standar non-sertifikasi (PTES, STIX, TLP, OWASP CRS, PCI DSS), lalu daftarkan tiga skill "Sebagian" ke `check-fact-notes.js` | membuka jalan 3 "Sebagian" menjadi "Selesai" |
| **H** | Putuskan tautan lapis-C: blueprint ujian di `ec-cnd`, katalog sertifikasi di `ptes-standard`; pertahankan halaman sertifikasi `cpent` sebagai jangkar identitas | konsistensi dengan aturan persona (nol materi ujian) |
| **F** | Evaluasi perilaku: himpunan tugas aktivasi + A/B ablation | membuktikan tuning menaikkan performa, bukan hanya kerapian |

## Kapan enforcement dibuat

`check-fact-notes.js` kini hanya menegakkan **2** skill (keduanya standar: `mitre-attack`, `nist-800-53`). Enforcement untuk **Frame** sengaja ditunda sampai cakupan ≥80% (≥23 dari 28), karena checker sekarang masih butuh allowlist 9 pengecualian — rapuh dan menyembunyikan pekerjaan tersisa.

## Cara memperbarui

1. Jalankan tiga pemeriksaan: `node scripts/check-fact-notes.js`, `node scripts/check-changelog.js`, dan hitung ulang kolom Ref.
2. Perbarui baris yang berubah dan tanggal di atas.
3. Catat perubahan file ini di `CHANGELOG.md`.
