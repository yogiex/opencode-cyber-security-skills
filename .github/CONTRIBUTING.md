# Panduan Kontribusi

Terima kasih sudah meluangkan waktu. Repo ini memelihara **Agent Skills** untuk keamanan siber — unit instruksi terstruktur yang dipakai agen AI untuk bekerja lebih akurat, bukan sekadar kumpulan prompt.

Dokumen ini menjelaskan cara berkontribusi dan pola penulisan yang terbukti efektif. Sebelum mulai, baca juga:

- [README.md](../README.md) — gambaran repo dan daftar skill
- [ARCHITECTURE.md](../ARCHITECTURE.md) — alur data dan bagian yang dibuat otomatis
- [AGENTS.md](../AGENTS.md) — instruksi operasional untuk agen AI yang bekerja di repo ini
- [docs/SKILL-QUALITY.md](../docs/SKILL-QUALITY.md) — matriks kualitas per skill dan backlog

## Daftar Isi

- [Alur Kerja](#alur-kerja)
- [Standar Struktur Skill](#standar-struktur-skill)
- [Pola Penulisan yang Efektif](#pola-penulisan-yang-efektif)
- [Provenance dan Fact Sheet](#provenance-dan-fact-sheet)
- [Changelog](#changelog)
- [Checklist Sebelum PR](#checklist-sebelum-pr)
- [Gaya Commit dan Branch](#gaya-commit-dan-branch)
- [Etika dan Batas](#etika-dan-batas)

## Alur Kerja

1. **Scaffold** — `node scripts/add-skill.js <nama> "<deskripsi>"` atau sunting skill yang ada.
2. **Tulis referensi** di `skills/<name>/references/` dengan frontmatter wajib (lihat di bawah).
3. **Perbarui indeks referensi** di `SKILL.md` jika ada file yang ditambah, diubah namanya, atau dihapus.
4. **Sinkronkan artefak turunan** — `node scripts/sync-skills.js` (menulis `manifest.json`, `.claude-plugin/*`, `.cursor-plugin/plugin.json`, `skills/index.json`).
5. **Verifikasi** — `node scripts/check-fact-notes.js` dan `node scripts/check-changelog.js`.
6. **Catat perubahan** di [CHANGELOG.md](../CHANGELOG.md) dalam perubahan yang sama.
7. **Buka PR** ke `dev` (atau `main` sesuai alur) dengan conventional commit.

> **Jangan mengedit artefak turunan secara manual.** `manifest.json`, `skills/index.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` dihasilkan oleh `scripts/sync-skills.js` dari `SKILL.md`. `README.md` dan `docs/` dipelihara manual.

## Standar Struktur Skill

Setiap skill adalah folder dengan bentuk:

```text
skills/<skill-name>/
├── SKILL.md          # Wajib — frontmatter + gambaran + indeks referensi
├── references/       # Dokumentasi bertingkat
├── scripts/          # Skrip pendukung
└── assets/           # Templat, gambar, CSS
```

### Frontmatter `SKILL.md`

```yaml
---
name: skill-name
description: Satu kalimat yang dipakai untuk discovery dan pencocokan.
license: MIT
compatibility: opencode
metadata:
  audience: target-audience
  workflow: reporting
  source: reference-standard
---
```

`name` dan `description` menentukan kapan agen memuat skill. Tulis `description` sebagai kondisi pemakaian, bukan ringkasan isi.

### Frontmatter referensi

Setiap file di `references/` wajib punya tiga field:

```yaml
---
name: "Human-Readable Title"
description: "One-line summary of the file's contents."
tags: [tag1, tag2, tag3]
---
```

- **name** — judul deskriptif (mis. `Elements API`)
- **description** — satu kalimat, fokus pada isi
- **tags** — kata kunci yang dapat dicari: nama method API, istilah kategori, konsep kunci

### Aturan isi referensi

- Markdown polos — tanpa komponen JSX (`<Tabs>`, `<Steps>`, `<Note>`, `<Frame>`).
- Blok kode wajib memakai penanda bahasa (```` ```bash ````, ```` ```typescript ````).
- Data terstruktur memakai tabel markdown.
- Catatan dan peringatan memakai blockquote (`>`).
- Satu file fokus pada satu domain atau topik.
- Akhiri dengan bagian **Best Practices** bila relevan.

Saat mengonversi dokumentasi eksternal yang memakai komponen JSX:

| Komponen sumber | Konversi |
|---|---|
| `<Tabs>` / `<Tab>` | Bagian terpisah dengan heading `###` |
| `<Note>` / `<Warning>` | Blockquote (`>`) |
| `<Steps>` / `<Step>` | Daftar bernomor dengan sub-heading `###` |
| `<Accordion>` | Tabel markdown atau bagian biasa |
| `<Frame>` / `<img>` | Hapus (URL gambar tidak dapat diresolusi) |
| `<Button>` / `<a>` | Tautan markdown inline |

### Kerangka `SKILL.md`

- `## Kapan Digunakan` — kondisi pemakaian dan pengecualian
- `## Decision Frame` — aturan keputusan: kapan berhenti, bukti minimum, urutan langkah
- `## Cara Pakai` — workflow langkah demi langkah
- `## Gotchas` — jebakan lingkungan-spesifik yang melawan asumsi umum
- `## Referensi` — tautan ke setiap file di `references/`
- `## Best Practices` — batas dan etika penggunaan

## Pola Penulisan yang Efektif

Panduan ini berdasarkan [Agent Skills Best Practices](https://agentskills.io/skill-creation/best-practices).

### 1. Spending Context Wisely

Setiap token dalam skill bersaing dengan conversation history dan skill lain di context window.

**Tambahkan yang tidak diketahui agen, hilangkan yang sudah diketahui.** Jangan jelaskan konsep umum (apa itu HTTP, PDF, SQL injection). Fokus ke pengetahuan domain-spesifik, edge case yang tidak obvious, dan konvensi proyek.

```markdown
<!-- Terlalu panjang — agen sudah tahu apa itu PDF -->
## Extract PDF text
PDF (Portable Document Format) files are a common file format...

<!-- Lebih baik — langsung ke yang agen belum tahu -->
## Extract PDF text
Use pdfplumber for text extraction. For scanned documents, fall back to
pdf2image with pytesseract.
```

Tanyakan untuk setiap konten: *"Akankah agen salah tanpa instruksi ini?"* Jika tidak, potong.

**Rancang unit yang koheren.** Terlalu sempit → beberapa skill harus dimuat untuk satu task. Terlalu luas → sulit diaktivasi secara presisi.

**Kedalaman sedang.** Dokumentasi komprehensif bisa kontraproduktif. Panduan ringkas dan bertahap + satu contoh yang berjalan lebih berguna daripada dokumentasi menyeluruh.

**Progressive disclosure untuk skill besar.** `SKILL.md` wajib <500 baris / 5K token. Detail dipindah ke `references/`. Instruksi spesifik lebih berguna daripada rujukan kabur:

> "Baca `references/api-errors.md` jika API mengembalikan non-200" — bukan "lihat `references/` untuk detail".

### 2. Favor Procedures over Declarations

Ajarkan *cara mendekati* kelas masalah, bukan *apa yang dihasilkan* untuk satu instance.

```markdown
<!-- Jawaban spesifik — hanya berguna untuk task ini -->
Join the `orders` table to `customers` on `customer_id`, filter where
`region = 'EMEA'`, and sum the `amount` column.

<!-- Metode yang dapat dipakai ulang -->
1. Read the schema from `references/schema.yaml` to find relevant tables
2. Join tables using the `_id` foreign key convention
3. Apply any filters from the user's request as WHERE clauses
4. Aggregate numeric columns as needed and format as a markdown table
```

### 3. Provide Defaults, Not Menus

Pilih satu default, sebut alternatif secara singkat.

```markdown
<!-- Terlalu banyak pilihan -->
You can use pypdf, pdfplumber, PyMuPDF, or pdf2image...

<!-- Default jelas dengan escape hatch -->
Use pdfplumber for text extraction. For scanned PDFs requiring OCR,
use pdf2image with pytesseract instead.
```

### 4. Calibrate Control — Match Specificity to Fragility

**Fleksibel** untuk task yang toleran variasi — beri tujuan tanpa langkah rigid.

```markdown
## Code review process
1. Check all database queries for SQL injection (use parameterized queries)
2. Verify authentication checks on every endpoint
3. Look for race conditions in concurrent code paths
```

**Preskriptif** untuk operasi fragile — urutan spesifik, jangan dimodifikasi.

```markdown
## Database migration
Run exactly this sequence:
python scripts/migrate.py --verify --backup
Do not modify the command or add additional flags.
```

### 5. Instruction Patterns yang Efektif

**Gotchas** — perilaku lingkungan-spesifik yang melawan asumsi umum. Simpan di `SKILL.md`, bukan `references/`, agar terbaca sebelum agen menemui situasi.

```markdown
## Gotchas
- The `users` table uses soft deletes. Queries must include
  `WHERE deleted_at IS NULL`.
- The `/health` endpoint returns 200 even if DB is down. Use `/ready`.
```

> Saat agen membuat kesalahan, tambahkan koreksinya ke bagian Gotchas. Ini cara paling langsung untuk perbaikan iteratif.

**Templates** — pendek inline di `SKILL.md`, panjang di `assets/`.

**Checklists** — untuk workflow multi-langkah, bantu agen melacak progres.

```markdown
Progress:
- [ ] Step 1: Analyze the form (run `scripts/analyze_form.py`)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping (run `scripts/validate_fields.py`)
```

**Validation loops** — jalankan → validasi → perbaiki → ulangi sampai lolos.

**Plan-validate-execute** — untuk operasi destruktif: susun rencana antara → validasi → baru eksekusi.

### 6. Refine dengan Eksekusi Nyata

Draf pertama hampir selalu perlu refinement. Jalankan skill terhadap task nyata, lalu masukkan hasilnya (kegagalan maupun keberhasilan) kembali ke proses. Minimal satu putaran execute-then-revise.

Baca *execution trace*, bukan hanya output akhir. Jika agen membuang waktu pada langkah tidak produktif, cari sebabnya:

- Instruksi terlalu kabur → agen mencoba beberapa pendekatan
- Instruksi tidak relevan → agen tetap mengikutinya
- Terlalu banyak opsi tanpa default jelas

## Provenance dan Fact Sheet

Setiap skill yang memuat klaim faktual (angka versi standar, statistik ujian, nomor domain sertifikasi) wajib punya catatan provenance ke [docs/CERTIFICATION-FACTS.md](../docs/CERTIFICATION-FACTS.md), dengan tanggal yang sama seperti fact sheet, dapat diresolusi, dan diletakkan tepat setelah Decision Frame.

Verifikasi:

```bash
node scripts/check-fact-notes.js
```

Jika angka belum ada di fact sheet, tambahkan sumbernya lebih dulu — jangan mengarang rujukan.

## Changelog

Setiap perubahan file wajib tercatat di [CHANGELOG.md](../CHANGELOG.md) dalam perubahan yang sama.

- Satu entri per perubahan set: tanggal ISO, ruang lingkup, dan tabel `File | Perubahan | Alasan | Verifikasi`.
- Setiap path yang ditambah, diubah, diganti nama, atau dihapus harus disebut namanya dalam backtick.
- Artefak turunan (`manifest.json`, `skills/index.json`, kedua `plugin.json`, `marketplace.json`) juga dicatat, dengan perintah generator sebagai verifikasi.
- Jangan menulis ulang atau menghapus entri lama; koreksi memakai entri baru.
- Verifikasi: `node scripts/check-changelog.js` (working tree) atau `--base <ref>` (rentang commit).

## Checklist Sebelum PR

```bash
node scripts/sync-skills.js          # artefak turunan segar
node scripts/check-fact-notes.js    # provenance lengkap
node scripts/check-changelog.js --base origin/main
```

- [ ] `SKILL.md` <500 baris dan <5K token
- [ ] Setiap file `references/` punya frontmatter `name`, `description`, `tags`
- [ ] Semua tautan relatif di `SKILL.md` dapat diresolusi
- [ ] Tidak ada tabel dengan jumlah kolom tidak konsisten
- [ ] Deskripsi di `SKILL.md` menyatakan kapan skill dipakai
- [ ] `README.md` diperbarui bila skill ditambah, dihapus, atau diubah lingkupnya
- [ ] `docs/SKILL-QUALITY.md` diperbarui bila status kualitas berubah
- [ ] `CHANGELOG.md` mencakup setiap file yang berubah

CI (`.github/workflows/validate-and-sync.yml`) akan memvalidasi setiap skill yang berubah, memvalidasi plugin terhadap JSON Schema, dan memeriksa kelengkapan changelog.

## Gaya Commit dan Branch

- Gunakan **conventional commit**: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
- Contoh: `feat(web-reconnaissance): fingerprint technology with confidence levels`
- Jangan push langsung ke `main`. Buat branch fitur dan buka PR.
- Jangan force push, amend, atau menulis ulang sejarah tanpa permintaan eksplisit.

## Etika dan Batas

Repo ini memuat materi ofensif. Itu bukan izin.

- Gunakan hanya terhadap sistem yang Anda miliki atau yang Anda punya **izin tertulis** untuk menguji.
- Setiap skill ofensif wajib menyatakan syarat otorisasi, penandaan payload destruktif, baseline, dan batas berhenti.
- Jangan menambahkan payload yang dirancang untuk merusak, menghapus data, atau menargetkan infrastruktur publik tanpa konteks laboratorium.
- Perlakukan data target, kredensial, dan bukti sebagai material sensitif: redaksi sebelum dipublikasikan.
- Kontribusi yang melanggar batas ini akan ditolak.

## Lisensi

Dengan berkontribusi, Anda menyetujui bahwa kontribusi Anda dirilis di bawah [MIT License](../LICENSE).
