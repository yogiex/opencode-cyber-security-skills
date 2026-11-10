# Analisis Kebutuhan — Publikasi Skill ke Direktori Eksternal

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-10
**Pertanyaan yang dijawab:** apakah `git push` memperbarui skills.rest; jika tidak, apa yang dibutuhkan agar isi yang tampil di sana sesuai kondisi repo, dan bagaimana menjaganya tetap sesuai setelah setiap rilis.
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md) (analisis kebutuhan), [PERSONA-CONVERSION.md](PERSONA-CONVERSION.md) (standar konversi)

---

## 1. Ringkasan

Tidak. `git push` ke `dev` hanya memperbarui GitHub. skills.rest adalah direktori pihak ketiga yang mengindeks repo sekali pada saat di-submit, lalu membekukan hasilnya. Halaman repo kita di sana masih menampilkan **24 skill dari 26** yang dijanjikan, sedangkan `manifest.json` sudah berisi **29**, dan deskripsinya masih memuat materi ujian yang sudah dihapus pada 0.19.0.

Masalahnya bukan kosmetik. Repo ini sedang mengubah sembilan skill dari "pembimbing ujian" menjadi "persona praktisi". Halaman publik yang masih menulis *"OSWE certification"* dan *"Certification & Career Path"* membatalkan sebagian hasil kerja itu di mata orang yang menemukan repo lewat skills.rest — dan orang itulah yang menjalankan `npx skills add` untuk memasang skill kita.

Yang belum ada di repo: **definisi operasional "terbit"**, **catatan kapan dan pada kondisi apa publikasi dilakukan**, dan **prosedur rilis** yang memuat langkah publikasi. Dokumen ini mengisi kekosongan itu, sekaligus menetapkan apa yang **tidak** akan dikerjakan.

---

## 2. Temuan (bukti terukur)

Diukur 2026-11-10 terhadap repo `yogiex/opencode-cyber-security-skills` (commit `7e45850`) dan halaman publik skills.rest.

| # | Temuan | Cara memeriksa | Akibat |
|---|---|---|---|
| T1 | Remote hanya punya `refs/heads/dev`; `main` tidak ada | `git ls-remote --heads origin` | semua tautan `/tree/main/` di skills.rest menuju 404 |
| T2 | Cabang default GitHub = `dev` | `GET api.github.com/repos/yogiex/opencode-cyber-security-skills` → `"default_branch":"dev"` | skill tetap bisa ditampilkan walau `main` tidak ada, jadi konten tidak bergantung pada `main` |
| T3 | Halaman repo menulis "24 Agent Skills Included" dan "26 ready-to-use" | halaman `/repo/yogiex/opencode-cyber-security-skills` | isi beku di sekitar Juni 2026 |
| T4 | `security-auditor` masih memuat "Certification & Career Path" (CISA, CISSP, ISO 27001 Lead Auditor) | halaman `/skill/security-auditor-yogiex` | bagian itu dihapus di `cd8a471` |
| T5 | `offsec-web-300` masih memuat "OSWE certification", "47h45m", "85 dari 100 untuk lulus" | halaman `/skill/offsec-web-300-yogiex` | materi ujian yang sengaja dibuang masih tayang |
| T6 | Tanggal "Updated" setiap skill sama dengan `created_at` repo GitHub, bukan `pushed_at` | bandingkan `obra/superpowers` (created 2025-10-09, pushed 2026-11-03, tayang "Oct 9, 2025") dan repo ini (created 2026-06-05, pushed 2026-11-10, tayang "Jun 5, 2026") | tidak ada crawl ulang terhadap repo yang sudah terindeks |
| T7 | Tidak ada integrasi teknis antara repo dan skills.rest | `grep -r "skills.rest"` → 0 kecocokan; workflow CI tidak punya langkah publish | tidak ada jalur apa pun yang bisa memperbarui skills.rest dari sisi repo |
| T8 | Homepage repo GitHub diarahkan ke `https://skills.rest/company/yogiex` | field `homepage` pada API GitHub | penghubung satu-satunya adalah keputusan manual, bukan konfigurasi repo |
| T9 | Halaman skill mencantumkan "Verified: Website `yogiex.github.io`" | halaman `/skill/offsec-web-300-yogiex` | pernah ada pendaftaran/verifikasi; submit ulang semestinya bisa dilakukan dengan akun yang sama |

### 2.1 Mekanisme skills.rest

Berdasarkan perilaku yang teramati, bukan dokumentasi internal mereka:

1. URL repo masuk lewat formulir `/contribute` atau proses verifikasi.
2. Sistem mengambil isi repo, mem-parse `SKILL.md`, lalu **menulis ulang** ringkasan dan FAQ dengan model mereka. Teks di halaman bukan salinan frontmatter kita.
3. Halaman diterbitkan dan dibekukan. Tidak ada langkah berikutnya yang kembali memeriksa repo.
4. `sitemap.xml` berisi 76 berkas indeks dengan `lastmod` seragam `2026-11-01` — pola regenerasi massal, bukan pemutakhiran bertahap.

Klaim "Updated daily" pada footer situs tidak didukung perilaku pada dua repo yang diperiksa.

---

## 3. Definisi

**Terbit (published)** — sebuah skill dapat ditemukan dan dipasang orang luar tanpa mengakses repo secara langsung. Untuk repo ini kanal terbitnya: listing skills.rest, perintah `npx skills add yogiex/opencode-cyber-security-skills`, dan manifest plugin Claude/Cursor/opencode.

**Segar (fresh)** — isi halaman publik mencerminkan `HEAD` cabang `dev` pada saat pemeriksaan: jumlah skill sama, deskripsi sama, dan tidak memuat konten yang sudah dihapus dari repo.

**Snapshot** — kondisi isi repo pada saat terakhir di-ingest, dikenali dari jumlah skill dan judul deskripsi.

**Ingest** — proses pengambilan dan penerbitan ulang oleh skills.rest, dipicu submit, bukan dipicu push.

**Basi (stale)** — halaman publik menampilkan snapshot yang berbeda dari `HEAD`. Basi **bukan** kegagalan repo; itu kondisi normal dari sistem tanpa sinkronisasi. Yang bisa kita kendalikan hanya pemicu dan verifikasinya.

---

## 4. Ruang lingkup

**Termasuk:**

- Listing skills.rest untuk repo ini (halaman repo dan 29 halaman skill).
- Konsistensi antara deskripsi publik dan frontmatter `SKILL.md`.
- Catatan status publikasi yang dapat diaudit.
- Prosedur rilis yang memuat langkah publikasi.

**Tidak termasuk:**

- Membuat cabang `main` — hanya dibahas sebagai fallback bersyarat (§7, opsi A).
- Mengubah konten skill. Refactor persona sudah selesai dan tidak dibuka kembali di sini.
- Menjadikan kesegaran publik sebagai gate CI — ditolak secara eksplisit (§6, NFR-1).
- Direktori lain di luar skills.rest.
- Memperbaiki template tautan `/tree/main/` milik skills.rest — di luar kendali kita (§5, LI-1).

---

## 5. Kebutuhan fungsional

| ID | Kebutuhan | Alasan | Prioritas |
|---|---|---|---|
| **FR-1** | Setiap rilis yang mengubah isi `skills/**` wajib diikuti submit ulang ke skills.rest | push tidak memicu ingest (T7, T6); submit adalah satu-satunya pemicu | Wajib |
| **FR-2** | Setelah submit, isi halaman diverifikasi terhadap `HEAD`: jumlah skill, deskripsi 9 skill persona, dan tidak adanya kata ujian | tanpa verifikasi, basi tidak terdeteksi dan tidak bisa dibedakan dari "sedang diproses" | Wajib |
| **FR-3** | Status publikasi dicatat: tanggal submit, snapshot sebelum, snapshot sesudah, dan hasil verifikasi | repo mewajibkan jejak audit untuk setiap perubahan (§Aturan changelog); status publikasi saat ini tidak tercatat di mana pun | Wajib |
| **FR-4** | Prosedur rilis terdokumentasi dan memuat langkah publikasi sebagai langkah bernomor | langkah manual yang hanya ada di kepala akan terlewat pada rilis berikutnya | Wajib |
| **FR-5** | Definisi "rilis yang memicu publikasi" dibatasi pada perubahan yang terlihat publik | submit untuk perubahan `docs/` atau `scripts/` internal hanya menambah beban tanpa mengubah tampilan | Sebaiknya |
| **FR-6** | Keputusan cabang kanonik ditetapkan dan dicatat | selama tidak ada `main`, setiap direktori yang mengasumsikan `main` akan menghasilkan tautan mati; keputusan ini harus eksplisit, bukan dibiarkan | Wajib |
| **FR-7** | Pemeriksaan isi halaman dapat dijalankan ulang tanpa langkah manual berurutan | verifikasi manual 29 halaman tidak realistis dan tidak konsisten antar-rilis | Sebaiknya |
| **FR-8** | Kegagalan ingest tercatat sebagai kegagalan, bukan dibiarkan senyap | halaman basi yang tampak normal adalah mode kegagalan paling berbahaya di sini | Wajib |

### Keterbatasan yang diterima

| ID | Keterbatasan | Mengapa diterima |
|---|---|---|
| **LI-1** | Tautan GitHub di skills.rest memakai `/tree/main/` dan akan tetap 404 | template milik mereka; satu-satunya cara mengubahnya adalah membuat `main` (opsi A), yang biayanya lebih besar daripada manfaatnya |
| **LI-2** | Teks ringkasan dan FAQ ditulis model mereka, bukan frontmatter kita | tidak bisa dikendalikan; konsekuensinya kriteria penerimaan hanya memeriksa **ketiadaan** kata ujian, bukan kecocokan kata per kata |
| **LI-3** | Waktu ingest tidak dapat dipastikan (klaim mereka: 24 jam) | tidak ada API status; verifikasi dilakukan pada jadwal, bukan menunggu konfirmasi |

---

## 6. Kebutuhan non-fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| **NFR-1** | Kesegaran publik **tidak** menjadi gate CI | workflow tidak boleh gagal karena layanan pihak ketiga; CI yang bergantung pada jaringan eksternal akan rapuh dan memblokir pekerjaan lain |
| **NFR-2** | Tidak menambah dependensi runtime pada repo | tidak ada paket baru di `scripts/`; pemeriksaan memakai Node bawaan |
| **NFR-3** | Dapat diaudit | setiap submit dan verifikasi punya entri bernomor di dokumen status, bukan hanya di riwayat obrolan |
| **NFR-4** | Idempoten | submit ulang untuk isi yang sama tidak merusak apa pun; aman diulang bila hasil verifikasi meragukan |
| **NFR-5** | Batas waktu yang eksplisit | submit dalam 24 jam setelah rilis; verifikasi dalam 7 hari; jika lewat, dicatat sebagai gagal |
| **NFR-6** | Tidak mengubah alur kerja yang sudah ada | `check-changelog.js`, `check-fact-notes.js`, dan `sync-skills.js` tetap menjadi satu-satunya validator repo |

---

## 7. Opsi dan matriks keputusan

| Kriteria | **A. Buat `main` dari `dev`** | **B. Submit ulang lewat `/contribute`** | **C. Biarkan** |
|---|---|---|---|
| Menyentuh akar masalah (tidak ada pemicu ingest) | Tidak — menambah pemicu baru justru tidak terjadi; crawl tetap tidak berjalan | Ya — submit adalah pemicu yang memang dipakai sistem | Tidak |
| Usaha | Sedang: buat cabang, atur default, jaga dua cabang sinkron | Rendah: satu formulir | Nol |
| Risiko baru | Dua cabang menyimpang; `AGENTS.md` melarang push ke `main` tanpa permintaan eksplisit; CI `sync` job (`refs/heads/main`) tiba-tiba aktif dan melakukan auto-commit | Hampir nol; dapat diulang | Reputasi: materi ujian yang sudah dibuang tetap tayang |
| Dapat dibalik | Ya, tapi meninggalkan cabang menganggur | Ya | Ya |
| Menyelesaikan tautan `/tree/main/` 404 | Ya | Tidak (LI-1) | Tidak |
| Sesuai bukti T6 (tidak ada crawl berulang) | Tidak relevan — tidak ada crawl untuk dipicu | Ya | — |

**Rekomendasi: B**, dengan A disimpan sebagai fallback bersyarat: hanya dijalankan bila submit ulang terbukti tidak menghasilkan ingest dalam 3 hari.

Alasan utama memilih B bukan karena lebih murah, melainkan karena **A tidak menyentuh akar masalah**. Membuat `main` tidak menciptakan crawler; yang berubah hanya resolusi tautan. Jika setelah `main` dibuat isi tetap beku, kita sudah menanggung biaya struktur cabang tanpa memperoleh apa pun.

---

## 8. Kriteria penerimaan

Dinyatakan **terbit dan segar** bila seluruh butir berikut terbukti pada pemeriksaan yang dijalankan setelah ingest:

| ID | Kriteria | Cara verifikasi |
|---|---|---|
| **AC-1** | Halaman repo menampilkan **29** skill | buka `/repo/yogiex/opencode-cyber-security-skills`, hitung kartu skill |
| **AC-2** | Tidak ada halaman skill yang memuat kata `certification`, `exam`, `passing score`, atau `practice question` | ambil 9 halaman skill persona, cari pola tersebut |
| **AC-3** | Halaman `security-auditor` tidak memuat "Certification & Career Path", CISA, atau CISSP | buka halaman, cari ketiga istilah |
| **AC-4** | Halaman `offsec-web-300` tidak memuat "OSWE certification", "47h45", atau "85 dari 100" | buka halaman, cari ketiga istilah |
| **AC-5** | Deskripsi 9 skill persona menyebut peran praktisi, bukan persiapan ujian | bandingkan dengan frontmatter `HEAD`; kecocokan kata-per-kata tidak disyaratkan (LI-2) |
| **AC-6** | Tanggal submit dan snapshot hasil verifikasi tercatat di dokumen status | periksa entri bernomor pada dokumen status |

Kriteria yang **tidak** dipakai: tautan `/tree/main/` yang berfungsi (LI-1) dan kesesuaian teks FAQ (LI-2). Keduanya di luar kendali dan tidak boleh dijadikan syarat, agar kegagalan yang tak terhindarkan tidak menyamarkan kegagalan yang bisa dihindari.

---

## 9. Risiko dan antipattern

### 9.1 Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Submit ulang diabaikan karena repo dianggap sudah terdaftar | tetap basi tanpa tanda | catat submit; verifikasi pada hari ke-3; jika tetap basi, eskalasi ke opsi A atau hubungi kanal dukungan mereka |
| Ingest berhasil tapi hanya sebagian skill masuk | hitungan 29 tidak terpenuhi | AC-1 sebagai pemeriksaan tunggal yang paling cepat membaca keadaan |
| Ringkasan model mereka menulis ulang persona menjadi bahasa ujian lagi | melanggar tujuan refactor | AC-2 dan AC-3 memeriksa hasil akhir, bukan niat |
| Pemeriksaan isi halaman dilakukan manual dan terlewat | basi berkepanjangan | FR-3 dan FR-7: catatan status + skrip pemeriksa |
| Pekerjaan ini menyerap waktu yang mestinya untuk konten skill | prioritas bergeser | batasi: satu kali submit, satu kali verifikasi, satu dokumen |

### 9.2 Antipattern yang dilarang

| ID | Antipattern | Mengapa dilarang |
|---|---|---|
| **AP-1** | Menambah langkah publish di CI | NFR-1: CI menjadi bergantung pada layanan pihak ketiga yang tidak punya API |
| **AP-2** | Membuat `main` sebagai reaksi refleks terhadap tautan 404 | menyelesaikan gejala, bukan penyebab (T6); menambah risiko cabang ganda |
| **AP-3** | Menyalin teks halaman skills.rest ke dalam repo sebagai "sumber kebenaran" | repo adalah sumbernya; halaman itu turunan yang bisa basi kapan saja |
| **AP-4** | Menulis ulang entri changelog lama untuk "memperbaiki" status publikasi | Aturan changelog 6: koreksi lewat entri baru |
| **AP-5** | Menyatakan "sudah terbit" tanpa memeriksa isi halaman | bertentangan dengan disiplin verifikasi repo ini |
| **AP-6** | Menyesuaikan konten skill agar cocok dengan selera ringkasan model pihak ketiga | arah ketergantungan terbalik; repo yang menentukan, bukan direktori |

---

## 10. Prosedur rilis (usulan)

Berlaku setiap kali rilis mengubah `skills/**`:

1. Selesaikan perubahan, jalankan validator repo (`check-changelog.js`, `check-fact-notes.js`), commit, push ke `dev`.
2. Catat snapshot sebelum: jumlah skill di `HEAD` dan jumlah skill yang tampil di skills.rest.
3. Submit `https://github.com/yogiex/opencode-cyber-security-skills` (URL root, bukan URL folder) lewat `/contribute`.
4. Catat tanggal submit di dokumen status dengan status `menunggu`.
5. Pada hari ke-3 dan ke-7, jalankan pemeriksaan AC-1 sampai AC-6.
6. Perbarui status menjadi `segar` atau `gagal`, sertakan snapshot sesudah.
7. Jika gagal pada hari ke-7, jalankan opsi A atau hubungi kanal dukungan skills.rest, lalu catat keputusannya.

Langkah 3–7 saat ini manual. Otomatisasinya memerlukan keputusan tersendiri (§11, D4).

---

## 11. Keputusan yang dibutuhkan

| ID | Keputusan | Pilihan | Dampak bila ditunda |
|---|---|---|---|
| **D1** | Menjalankan opsi B sekarang? | ya / tidak | halaman publik tetap menampilkan materi ujian |
| **D2** | Membuat dokumen status publikasi sebagai ledger terpisah? | ya (disarankan) / cukup di `CHANGELOG.md` | tidak ada catatan yang bisa diaudit untuk status publikasi |
| **D3** | Membuat `main`? | tidak (disarankan) / ya | tidak ada perubahan sampai submit terbukti gagal |
| **D4** | Membuat skrip pemeriksa isi halaman (FR-7)? | ya / tunda | verifikasi tetap manual dan mudah terlewat |

---

## 12. Metrik

| Metrik | Kondisi awal (2026-11-10) | Target |
|---|---|---|
| Jumlah skill yang tampil di skills.rest | 24 | 29 |
| Skill persona yang deskripsinya masih memuat kata ujian | 9 | 0 |
| Selisih waktu rilis ke submit | tidak tercatat | ≤ 24 jam |
| Selisih waktu submit ke verifikasi | tidak tercatat | ≤ 7 hari |
| Status publikasi tercatat | tidak ada | satu entri per rilis |

Angka kondisi awal pada baris kedua berasal dari pemeriksaan dua halaman (`offsec-web-300`, `security-auditor`) ditambah deskripsi repo yang menyebut "26 ready-to-use"; bukan hasil memeriksa kesembilan halaman satu per satu.
