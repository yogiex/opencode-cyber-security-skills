# Konversi Skill Bersertifikat Menjadi Persona

**Status:** Standar kerja — dipakai sebagai acuan refactor `0.17.0`
**Tanggal:** 2026-11-10
**Ruang lingkup:** skill yang tujuannya lulus ujian sertifikasi → skill yang tujuannya *persona injection*

---

## 1. Masalah

Repo ini ada untuk membuat agent **memahami cybersecurity** dengan memerankan praktisi yang kompeten, bukan untuk meluluskan siapa pun dari ujian sertifikasi.

Dua tujuan itu menghasilkan dokumen yang berbeda secara struktural:

| Aspek | Tujuan ujian | Tujuan persona |
|---|---|---|
| Pertanyaan yang dijawab | "Apa yang dinilai grader?" | "Keputusan apa yang harus saya ambil, dan atas dasar apa?" |
| Isi khas | bobot domain, passing score, alokasi menit, urutan mengerjakan soal | trust boundary, kriteria berhenti, bukti yang harus diamankan, trade-off |
| Efek pada agent | menghafal format | bernalar seperti orang yang pernah melakukannya |
| Saat dihadapkan target nyata | buntu — tidak ada grader | lanjut — ada metode |

Angka ujian juga cepat basi (versi blueprint berubah tiap 1–3 tahun) sementara cara berpikir praktisi tidak. Karena itu angka ujian **dipindahkan keluar** dari skill: tetap tersedia di `docs/CERTIFICATION-FACTS.md` sebagai arsip fakta, tidak lagi menjadi isi skill.

---

## 2. Audit — bukti, bukan dugaan

Kriteria "skill bertujuan lulus ujian" diuji dengan tiga sinyal yang bisa diperiksa ulang:

- **S1** — `description` atau bagian pembuka menyatakan skill untuk persiapan/menghadapi ujian.
- **S2** — ada artefak yang hanya berguna untuk ujian (`exam-strategy.md`, `exam-architecture.md`, `exam-overview.md`, `exam-checklist.md`, `pre-exam-checklist.md`, bagian "Exam Format", "Time Management", "Scoring", "Strategi 3-Pass").
- **S3** — `Decision Frame` memuat taktik ujian (alokasi waktu, passing score, "apakah ini dapat poin").

Hitungan kata kunci memakai pola ketat `\bexam(s|ination)?\b|\blulus\b|\bpassing\b|\bsertifikasi\b` pada seluruh berkas `.md` di direktori skill (kata "example" tidak ikut terhitung).

| Skill | Hit | S1 | S2 | S3 | Keputusan |
|---|---|---|---|---|---|
| `comptia-cysa` | 22 | ya — "untuk mempersiapkan sertifikasi" | `exam-overview.md` | #6 "Waktu ujian cukup?" | konversi |
| `oscp-methodology` | 45 | ya — "strategi untuk PEN-200/OSCP+" | `exam-strategy.md`, `exam-architecture.md` | #1,#3,#4,#5 | konversi |
| `offsec-pen-300` | 57 | tidak | `exam-strategy.md`, `assets/exam-checklist.md` | #1–#5 seluruhnya | konversi |
| `offsec-soc-200` | 62 | tidak | `overview-exam.md`, `assets/pre-exam-checklist.md`, `challenge-labs.md` | #4,#5,#6 | konversi |
| `offsec-web-300` | 29 | tidak | §1 "Overview & Exam Structure", §5 "Exam Strategy" | #4 | konversi |
| `offsec-th-200` | 27 | tidak | "Scoring & Exam Environment", "8h Time Management" | #4,#5 | konversi |
| `lf-cks` | 5 | tidak | "Exam Format", "Strategi 3-Pass" | #5 | konversi |
| `ec-ecih` | 5 | tidak | §2 "ECIH Exam Overview & Strategy" | — | konversi |
| `offsec-ir-200` | 31 | tidak | "Time Management" (rencana ujian 8 jam) | #3 "Sudah aman di ambang lulus?" | konversi, dikerjakan terakhir |
| `cpent` | 1 | — | — | — | sudah persona (0.12.0) |
| `ec-cnd` | 7 | — | — | — | sudah persona (0.16.0) |

Sembilan skill dinyatakan **exam-goal** dan dikonversi. Skill non-sertifikasi (`threat-intelligence`, `ptes-standard`, `web-reconnaissance`, dan seterusnya) tidak tersentuh: tidak ada sinyal S1–S3 di sana.

---

## 3. Bentuk akhir yang wajib

Acuan hidup: `skills/cpent/SKILL.md` dan `skills/ec-cnd/SKILL.md`. Urutan bagian **persis** seperti ini:

```markdown
---
name: <nama-direktori>
description: Persona <peran> bersertifikat <CERT> — <kapabilitas konkret>. Pakai saat agent harus berperan sebagai <peran> pada <pekerjaan nyata> — bukan untuk persiapan ujian.
license: MIT
compatibility: opencode
metadata:
  audience: <audiens>
  workflow: <alur>
  source: <sumber>
  standard: <standar>
  year: "2026"
  keywords: "<kata kunci dipisah koma>"
---

# <CERT> — Persona <Peran> Bersertifikat

Skill ini bukan materi persiapan ujian. Tujuannya mengajari agent **memerankan
<peran> yang sudah memegang <CERT>**: <apa yang ia putuskan / pegang / sampaikan>.
<Pengetahuan bisa dicari; yang mahal adalah keputusan.>

## Profil Persona                       ← tabel 6 baris: Peran, Pengalaman, Lingkungan,
                                          Kekuatan, Bukan bidangnya, Bahasa
                                          + satu kalimat "spesifikasi peran, bukan biografi"

## Kapan Skill Ini Dipakai             ← 4–5 kondisi kerja nyata
                                          + "Jangan pakai untuk:" dengan rujukan skill lain

## Cara Memerankan Persona             ← 6 butir, mengikuti cpent/ec-cnd
                                          (Aktivasi, orang pertama, ringkas & tenang,
                                           ketidakpastian eksplisit, struktur jawaban,
                                           tetap dalam peran tapi jujur)
                                          + tautan ke references/persona.md

## Persona Contract                    ← 6–7 komitmen bernomor, spesifik peran

## Decision Frame                      ← 6–7 pertanyaan operasional (lihat §5)

## Operating Doctrine — "<tagline>"    ← 6–8 butir

## Workflow                            ← siklus kerja nyata (bukan jadwal ujian)

## Capability Map                      ← kelompok kapabilitas → tautan referensi

## Reference Documentation             ← 1:1 dengan isi references/ dan assets/

## Gotchas                             ← minimal 8 butir

## Progressive Disclosure              ← "Ketika butuh... | Muat berkas ini"

## License
```

Aturan tambahan:

- `## Decision Frame` dan `## Gotchas` **wajib** memakai judul itu apa adanya (dipakai ledger dan checker).
- Panjang `SKILL.md` 120–200 baris, dengan batas keras 450 (aturan `ARCHITECTURE.md`). Bila materi teknis melebihi batas, **pindahkan ke `references/`** — jangan dibuang.
- Setiap berkas di `references/` wajib ber-frontmatter `name`/`description`/`tags` dan muncul **tepat sekali** di tabel Reference Documentation. Tidak ada berkas yatim, tidak ada baris ganda (drift `cpent` tidak boleh terulang).
- Tidak ada tautan ke `../../docs/` — skill dipasang sebagai direktori mandiri.

---

## 4. Suara

| Wajib | Dilarang |
|---|---|
| Orang pertama untuk pengalaman: "Saya biasanya menolak…" | "Anda adalah seorang…" (tutor generik) |
| Instruktif untuk langkah: "Cek `ip route` dulu…" | Hype: "sangat penting", "wajib banget" |
| Ketidakpastian eksplisit: "belum saya verifikasi", "tergantung versi" | Mengarang output tool, CVE, ambang, atau hasil |
| Ringkas → alasan → langkah → bukti → risiko | Daftar perintah tanpa alasan |
| Istilah teknis Inggris, kalimat Indonesia | Campur Inggris penuh |

---

## 5. Larangan keras — isi yang harus hilang

| Dilarang | Contoh yang sekarang ada | Ganti dengan |
|---|---|---|
| Passing/cut score | "Passing score 85/100", "Lulus 50/70" | kriteria "bukti ini cukup atau belum" |
| Alokasi waktu ujian | "8h Time Management", "Strategi 3-Pass", "1,9 menit per soal" | anggaran waktu engagement + aturan berhenti |
| Skema poin | "7 exercise × 10 poin", "mesin 20 pt" | tingkat keyakinan bukti |
| Logistik ujian | proctor, retake, voucher, biaya, masa berlaku sertifikat | — (hapus; arsip ada di fact sheet) |
| Aturan khusus ujian | "Metasploit hanya boleh di satu mesin", "SQLmap dilarang di ujian" | batasan teknis nyata, atau hapus |
| Tautan `CERTIFICATION-FACTS.md` + catatan provenance | blockquote "Angka ujian di skill ini…" | hapus; skill juga dicabut dari `check-fact-notes.js` |

Kata `ujian` hanya boleh muncul di kalimat penanda **"bukan untuk persiapan ujian"** (di `description`, paragraf pembuka, dan baris "Jangan pakai untuk:"). Selain itu nol.

**Pola verifikasi akhir:**

```
(?i)passing score|cut score|proctor|retake|voucher|exam (format|strategy|overview|structure|domain|objective|blueprint)|CERTIFICATION-FACTS\.md|\bjam ujian\b|\bwaktu ujian\b
```

harus **0 hasil** untuk setiap skill yang dikonversi. Baris yang memuat `ujian` harus memuat `persiapan ujian`.

---

## 6. Disposisi berkas

| Berkas sekarang | Perlakuan |
|---|---|
| `references/exam-strategy.md` | **Tulis ulang** menjadi `engagement-playbook.md` — disiplin penyampaian: scope/otorisasi, bukti, urutan laporan, kriteria berhenti. Bila isinya murni logistik ujian, hapus saja dan catat alasannya. |
| `references/exam-architecture.md` | **Hapus** — mekanika penilaian, tidak ada padanan kerja. |
| `references/exam-overview.md` | **Hapus** — bobot domain adalah cetak biru ujian. Pengetahuan domainnya sudah ada di `domain*.md`. |
| `assets/exam-checklist.md`, `assets/pre-exam-checklist.md` | **Hapus** — checklist hari-H ujian. |
| `references/modules-overview.md` | **Ubah nama + tulis ulang** menjadi `capability-domains.md` (taksonomi kapabilitas, tanpa bobot/modul/poin). Bila >90% isinya silabus kursus, hapus dan lipat tabel kapabilitasnya ke `SKILL.md`. |
| `references/challenge-labs.md` (soc-200) | **Tulis ulang** menjadi `detection-labs.md` — latihan mandiri yang bisa dijalankan di lingkungan sendiri, atau hapus. |
| Aset nyata: `report-template.md`, `scripts/*.kql`, `scripts/*.spl`, `scripts/payload-encoder.py` | **Pertahankan**, hanya bersihkan bahasa ujian. Ini deliverable kerja, bukan artefak ujian. |
| Referensi teknik (`linux-privesc`, `ad-attack-chain`, `elk-kql`, `crowdstrike-cql`, …) | **Pertahankan**, hapus hanya kalimat yang menunjuk ujian. |

Penghapusan berkas wajib disebut di `CHANGELOG.md` beserta alasannya.

---

## 7. Batas kerja

- **Jangan sentuh** `manifest.json`, `skills/index.json`, `.claude-plugin/*`, `.cursor-plugin/*`, `README.md`, `docs/SKILL-QUALITY.md`, `CHANGELOG.md`, `scripts/*` — semua itu diurus sekali di akhir oleh koordinator.
- **Jangan sentuh** skill lain, termasuk yang sedang dipegang sesi paralel (`cpent`, `ec-cnd`, `offsec-ir-200`).
- **Pertahankan** seluruh isi teknis: perintah, tabel teknik, tautan sumber. Yang berubah adalah bingkai, bukan pengetahuan.
- **Jangan mengarang** fakta baru. Kalau butuh angka, ambil dari isi yang sudah ada atau dari fact sheet, dan sebutkan sumbernya di `referensi.md`.
- Hindari duplikasi: bila topik sudah punya rumah (`ptes-standard` untuk fase pentest, `ec-ecih` untuk siklus IR, `web-reconnaissance` untuk recon web, `threat-intelligence` untuk CTI), **rujuk**, jangan tulis ulang.

---

## 8. Kriteria selesai

Sebuah skill dinyatakan selesai bila seluruh butir ini benar:

1. `description` memuat "Persona" dan diakhiri "bukan untuk persiapan ujian".
2. Sembilan bagian wajib §3 ada, berurutan, dengan judul yang sama.
3. `## Decision Frame` berisi 6–7 keputusan operasional; tidak ada taktik ujian.
4. Nol hasil pada pola verifikasi §5.
5. Setiap berkas `references/`/`assets/` muncul tepat sekali di Reference Documentation; setiap tautan mengarah ke berkas yang ada.
6. `node scripts/check-fact-notes.js` tidak lagi menyebut skill ini, dan blockquote provenance sudah hilang.
7. Tidak ada tabel rusak: jumlah sel tiap baris = jumlah sel header, tidak ada `|` tak ter-escape di dalam sel, tidak ada heading di dalam sel.
8. `referensi.md` (bila ada) tetap ada dan tidak menautkan halaman ujian sebagai sumber utama.
