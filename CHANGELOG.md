# Changelog — Audit Trail Perubahan File

Dokumen ini adalah catatan resmi setiap perubahan file di repo ini. Tujuannya agar setiap penambahan, perubahan, penghapusan, dan penggantian nama file dapat diaudit tanpa harus membaca diff git satu per satu.

## Aturan

1. **Satu entri per perubahan set** (satu PR atau satu rangkaian commit yang koheren), dengan tanggal ISO `YYYY-MM-DD` dan judul ringkas.
2. **Setiap file wajib disebut namanya** — path lengkap relatif terhadap root, dibungkus backtick, di dalam tabel entri.
3. **Kolom wajib:** `File | Perubahan | Alasan | Verifikasi`. Verifikasi adalah perintah atau pemeriksaan yang benar-benar dijalankan.
4. **Artefak turunan tetap dicatat.** `manifest.json`, `skills/index.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, dan `.cursor-plugin/plugin.json` dicatat dengan perintah generator sebagai verifikasi.
5. **Status commit:** tulis `pending` sebelum commit, lalu perbarui dengan hash pada commit berikutnya. Karena hash sebuah commit tidak bisa mencantumkan dirinya sendiri, rujukan akhir adalah `git log -- CHANGELOG.md`; status tidak boleh dibiarkan `pending` lebih dari satu commit.
6. **Jangan menulis ulang sejarah.** Koreksi dilakukan dengan entri baru yang menyebut entri yang dikoreksi.
7. **Wildcard hanya untuk karantina.** Entri wildcard (nama direktori minimal tiga tingkat, diakhiri dua bintang) hanya boleh dipakai untuk perubahan yang bukan milik sesi ini dan belum diputuskan; validator akan menampilkannya sebagai peringatan, bukan audit eksplisit. Wildcard yang terlalu luas ditolak.
8. **Validasi wajib:** `node scripts/check-changelog.js --base <ref>` harus exit 0 sebelum commit.

## [0.1.0] — 2026-11-07 — Mekanisme changelog dan audit

**Commit dasar:** `69b436d` (branch `dev`)
**Status:** committed in `27a09bd`; revisi validator dan entri eksternal dicatat pada commit lanjutan
**Ruang lingkup:** tata kelola repo (tanpa perubahan konten skill)

### Ditambahkan

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `CHANGELOG.md` | file baru | menjadi catatan resmi perubahan file | dibaca ulang; validator menemukan path ini |
| `scripts/check-changelog.js` | file baru | menghentikan commit jika ada file berubah yang tidak tercatat | `node scripts/check-changelog.js` exit 0 |

### Diubah

| File | Perubahan | Alasan | Verifikasi |
|---|---|---|---|
| `AGENTS.md` | menambah bagian Changelog dan satu langkah workflow | agar aturan ini mengikat agen dan kontributor | dibaca ulang; perintah validasi tercantum |
| `scripts/check-changelog.js` | parser hanya membaca baris tabel; wildcard terlalu luas ditolak | menutup celah: path yang disebut di prosa/aturan tidak lagi dihitung sebagai entri audit | uji negatif `--base 69b436d~1` exit 1; uji normal exit 0 |

### Tidak diubah — perubahan eksternal terdeteksi

Direktori `skills/web-pentest-payloads/` **tidak ada** di baseline `69b436d` dan **bukan dibuat oleh sesi ini**. File muncul saat sesi berjalan (18:36–20:29) dari proses lain, dan sengaja tidak disentuh. Status: menunggu keputusan pemilik repo.

| File | Status | Catatan |
|---|---|---|
| `skills/web-pentest-payloads/**` | untracked, dikarantina | seluruh isi direktori, termasuk `SKILL.md` yang muncul pukul 20:29 |
| `manifest.json` | berubah (eksternal) | proses lain menjalankan `sync-skills.js`; kini memuat 27 skill |
| `skills/index.json` | berubah (eksternal) | 27 entri, termasuk `web-pentest-payloads` |
| `.claude-plugin/plugin.json` | berubah (eksternal) | status M karena line ending; `git diff` tidak menunjukkan perubahan konten |
| `.claude-plugin/marketplace.json` | berubah (eksternal) | idem |
| `.cursor-plugin/plugin.json` | berubah (eksternal) | idem |

Catatan: dukungan wildcard di validator hanya untuk kasus karantina seperti ini; validator tetap menampilkan setiap file yang tertutup wildcard sebagai peringatan, bukan sebagai audit eksplisit. File pukul 18:39 mengandung mojibake `â€”`, tanda encoding salah saat penulisan. Artefak turunan di atas **tidak di-commit** oleh sesi ini; hanya dicatat agar status working tree dapat diaudit.

### Baseline saat entri dibuat

- Baseline `69b436d`: 26 skill, 104 file `references/`, 0 link rusak (audit 2026-11-07).
- Setelah proses eksternal: 27 skill di `manifest.json` dan `skills/index.json` (belum di-commit oleh sesi ini).
- Satu-satunya perubahan pada subtree skills berasal dari proses eksternal di atas; tidak ada file terlacak yang diubah sesi ini.
- Temuan audit yang belum diperbaiki tidak dicatat di sini; changelog hanya mencatat perubahan, bukan backlog.
