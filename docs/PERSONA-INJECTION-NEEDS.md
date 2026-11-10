# Analisis Kebutuhan — Persona Injection

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-10
**Pertanyaan yang dijawab:** skill mana yang masih membahas lulus ujian, dan apa yang dibutuhkan agar sebuah skill berfungsi sebagai *persona injection* — agent berperilaku seperti pemegang sertifikasi dan berpikir dengan mindset cybersecurity — bukan sebagai pembimbing ujian.
**Acuan bentuk:** [PERSONA-CONVERSION.md](PERSONA-CONVERSION.md) (standar konversi), `skills/cpent/`, `skills/ec-cnd/` (contoh hidup)

---

## 1. Ringkasan

Repo punya 29 skill. Audit 2026-11-10 menemukan **tiga lapis sisa materi ujian**, dan hanya lapis pertama yang sudah ditangani:

| Lapis | Sifat | Skill | Status |
|---|---|---|---|
| **A** | Tujuan skill memang ujian | `oscp-methodology` | sedang dikonversi |
| **B** | Katalog sertifikasi & materi ujian di dalam skill non-sertifikasi | `security-auditor`, `log-management-nist-800-92`, `devsecops-mindset`, `owasp-top10-2025` | **belum disentuh** |
| **C** | Tautan blueprint/katalog sertifikasi di skill persona | `ec-cnd`, `ptes-standard`, `cpent` | belum diputuskan |

Delapan skill lain (`comptia-cysa`, `offsec-ir-200`, `offsec-pen-300`, `offsec-soc-200`, `offsec-th-200`, `offsec-web-300`, `lf-cks`, `ec-ecih`) sudah dikonversi atau sedang dikonversi; pada skill itu kata "ujian" hanya muncul di kalimat penolakan.

Yang belum ada di repo: **definisi operasional** tentang apa yang membuat sebuah skill disebut persona injection, bagaimana "seperti memiliki sertifikasi" dibedakan dari "materi sertifikasi", dan bagaimana mindset dibangun lewat struktur dokumen. Dokumen ini mengisi kekosongan itu.

---

## 2. Temuan audit (bukti)

Dihitung ulang 2026-11-10 dari seluruh berkas `.md` di tiap direktori skill. Pola kuat: `passing score|cut score|lulus|proctor|retake|voucher|exam (guide|prep|format|strategy|overview|structure|domain|objective|blueprint)|latihan soal|practice question|exam dump`.

### 2.1 Lapis A — tujuan skill masih ujian

| Skill | Bukti | Dampak |
|---|---|---|
| `oscp-methodology` | `references/exam-architecture.md`: "Passing 70/100", tabel skor, kombinasi lulus; `references/exam-strategy.md`: "Time Management & Reporting" | seluruh frame keputusan menjawab "apa yang dinilai grader" |

### 2.2 Lapis B — katalog sertifikasi di skill non-sertifikasi

| Skill | Bukti | Mengapa merusak persona |
|---|---|---|
| `security-auditor` | L192 tabel "Sertifikasi \| Penerbit \| Fokus \| Harga \| Prasyarat"; L257 "CISA Review Manual — Official CISA exam guide"; L258 "CISA practice questions database"; L270 "Biaya Exam \| CPE/Year \| Renewal Cycle"; L305 "CISA Exam Preparation … exam prep"; L307 "CISSP Bootcamp … exam prep" | description-nya sendiri menjanjikan "certification path"; sebagian besar skill berisi karier & harga, bukan cara mengaudit |
| `log-management-nist-800-92` | L402 "Sertifikasi & Training"; L412 "Splunk Certified Architect … ~$2.500 (exam only)"; L413 "Microsoft Certified … ~$165 (exam)" | harga & label "exam only" adalah konten ujian, bukan pengetahuan log management |
| `devsecops-mindset` | L314 "Sertifikasi DevSecOps"; L316 tabel Sertifikasi/Penerbit/Format/Fokus/Biaya | idem |
| `owasp-top10-2025` | L342 tabel "Sertifikasi \| Penerbit \| Fokus \| Biaya" | idem; skill ini tentang kategori risiko, bukan tentang sertifikat |

Catatan: keempatnya **bukan** skill bersertifikat. Materi ujian masuk sebagai lampiran karier, dan justru karena itu berbahaya — ia mengubah agent dari praktisi menjadi konselor sertifikasi pada topik yang tidak ada hubungannya.

### 2.3 Lapis C — tautan blueprint/katalog di skill persona

| Skill | Bukti | Penilaian |
|---|---|---|
| `ec-cnd` | `references/referensi.md` L18 "CND Exam Blueprint v4.0" (8 domain, 20 sub-domain, bobot); L17 halaman sertifikasi | blueprint = materi ujian; persona sendiri sudah menyatakan bebas angka ujian, jadi tautan ini inkonsisten |
| `ptes-standard` | `references/referensi.md` L66–67: GIAC GPEN, CompTIA PenTest+ | PTES adalah standar, bukan sertifikasi; keduanya tidak relevan |
| `cpent` | `references/referensi.md`: halaman sertifikasi EC-Council | dapat dipertahankan sebagai **jangkar identitas** ("saya memegang CPENT"), bukan sebagai materi belajar ujian |

### 2.4 Yang sudah bersih

Pada `comptia-cysa`, `offsec-ir-200`, `ec-ecih`, `lf-cks` kata "ujian" hanya muncul di kalimat penolakan ("bukan untuk persiapan ujian", "latihan soal ujian" pada baris "Jangan pakai untuk"). `ec-cnd` dan `cpent` memakai pola yang sama di `persona.md`. Ini **bukan** pelanggaran: penolakan justru bukti persona bekerja.

`security-documentation`, `incident-response-plan`, `soc-analyst`, `threat-modeling`, `web-app-scan`, `web-reconnaissance`, `waf-evasion-methodology`, `threat-intelligence`, `mitre-attack`, `nist-800-53`, `risk-management-framework`, `code-security-audit` bersih atau hanya menyebut nama standar.

---

## 3. Definisi

**Persona injection** — kondisi ketika memuat sebuah skill mengubah *cara agent memutuskan dan berbicara*, bukan hanya menambah pengetahuannya. Ukurannya: agent menolak tindakan yang salah meski diminta, menyebut ketidakpastian tanpa dipaksa, dan memakai urutan penalaran yang sama pada kasus baru.

**"Seperti memiliki sertifikasi"** — agent mengambil **identitas, kewenangan, dan batas** seorang pemegang sertifikasi. Bukan berarti menghafal silabus, bukan berarti mengklaim pernah mengerjakan engagement tertentu. Sertifikat di sini adalah jangkar peran: tingkat pengalaman, lingkungan kerja, dan apa yang berada di luar bidangnya.

**Mindset** — seperangkat aturan yang mengikat keputusan saat data tidak lengkap: apa yang didahulukan, kapan berhenti, bukti apa yang harus ada, dan apa yang berani diklaim. Mindset yang benar bisa dikenali dari **penolakannya**, bukan dari daftar perintahnya.

---

## 4. Anatomi persona — 8 komponen wajib

| # | Komponen | Isi minimum | Jika absen |
|---|---|---|---|
| 1 | **Identitas** | Peran, pengalaman, lingkungan, kekuatan, bukan bidangnya, bahasa | agent menjawab sebagai tutor generik |
| 2 | **Mandat & kewenangan** | Apa yang ia putuskan sendiri, apa yang harus dieskalasi | agent mengambil keputusan yang bukan haknya (mis. memutus layanan produksi) |
| 3 | **Batas klaim** | Larangan mengarang output, CVE, angka, nama vendor lingkungan target | kredibilitas runtuh pada pertanyaan pertama |
| 4 | **Kontrak persona** | 6–7 komitmen bernomor yang mengikat, bukan slogan | tidak ada dasar untuk menolak permintaan yang salah |
| 5 | **Decision Frame** | 6–7 keputusan dengan ambang, urutan, dan kriteria berhenti | agent berhenti di "tergantung" |
| 6 | **Doktrin operasional** | 6–8 hukum mindset beserta konsekuensi kerjanya | perilaku tidak konsisten antar kasus |
| 7 | **Suara** | Orang pertama untuk pengalaman, instruktif untuk langkah, ketidakpastian eksplisit | terasa seperti dokumentasi, bukan praktisi |
| 8 | **Contoh penalaran** | 4–6 skenario orang pertama, **termasuk penolakan** | aturan tidak pernah diuji terhadap kasus sulit |

Komponen 1–3 menjawab "seperti memiliki sertifikasi". Komponen 4–8 menjawab "membangun mindset". Skill yang hanya punya 1–3 menghasilkan tokoh tanpa tulang; yang hanya punya 5–6 menghasilkan checklist tanpa suara.

---

## 5. Persona vs tutor vs coach ujian

| Dimensi | Coach ujian | Tutor | Persona |
|---|---|---|---|
| Pertanyaan pusat | "Apa yang dinilai?" | "Apa itu X?" | "Apa yang saya putuskan, dan atas dasar apa?" |
| Isi khas | bobot domain, passing score, waktu, urutan soal | definisi, sejarah, daftar istilah | trade-off, kriteria berhenti, bukti, batas kewenangan |
| Menghadapi data kurang | memberi jawaban "yang keluar di ujian" | menjelaskan kemungkinan | menyatakan ketidakpastian dan cara mengujinya |
| Menghadapi permintaan berbahaya | mengikuti format | menjelaskan risiko | menolak, memberi alasan, menawarkan alternatif |
| Umur pakai | sampai blueprint berubah | lama | lama |

---

## 6. Kebutuhan fungsional

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | Memuat skill mengaktifkan peran sampai sesi berakhir | jawaban memakai suara persona; tidak kembali ke asisten generik |
| FR-2 | Struktur jawaban konsisten: ringkas → alasan → langkah → bukti → risiko | terlihat di semua contoh penalaran |
| FR-3 | Keputusan diambil eksplisit dengan ambang, bukan "tergantung" | setiap Decision Frame punya ≥5 butir dengan ambang/urutan/stop condition |
| FR-4 | Menolak permintaan yang melanggar kontrak, disertai alternatif | minimal satu contoh penolakan per skill |
| FR-5 | Menyatakan ketidakpastian tanpa diminta | tidak ada angka/CVE/output karangan |
| FR-6 | Memetakan masalah ke kapabilitas yang dimiliki | `## Capability Map` ada dan menaut ke berkas nyata |
| FR-7 | Merujuk skill lain saat di luar batas, bukan menulis ulang | setiap skill menyebut batasnya dan skill penggantinya |
| FR-8 | Nol materi ujian: tidak ada passing score, bobot, poin, waktu ujian, katalog sertifikasi, vendor latihan soal, atau tautan yang slug-nya tentang ujian | grep pola §2 = 0 hasil, termasuk di dalam URL |
| FR-9 | Identitas sertifikasi boleh disebut sebagai jangkar peran, bukan sebagai kurikulum | "Persona pengguna bersertifikat X" tanpa daftar modul/domain ujian |
| FR-10 | Tidak mengklaim biografi | ada kalimat "spesifikasi peran, bukan biografi orang nyata" |

---

## 7. Kebutuhan non-fungsional

| ID | Kebutuhan |
|---|---|
| NFR-1 | `SKILL.md` 120–200 baris, batas keras 450; kelebihan materi dipindahkan ke `references/`, tidak dibuang |
| NFR-2 | Setiap berkas `references/` muncul tepat sekali di Reference Documentation; tidak ada berkas yatim |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`) |
| NFR-4 | Bahasa Indonesia + istilah teknis Inggris; kode dan komentar berbahasa Inggris |
| NFR-5 | Setiap penghapusan berkas tercatat di `CHANGELOG.md` beserta alasannya |
| NFR-6 | Perubahan bisa diverifikasi ulang oleh mesin: grep, hitung baris, resolusi tautan, paritas tabel |

---

## 8. Antipattern

| ID | Antipattern | Mengapa salah |
|---|---|---|
| AP-1 | Menghapus pengetahuan teknis agar "bebas ujian" | menukar satu penyakit dengan penyakit lain |
| AP-2 | Mengganti "exam" menjadi "assessment" tanpa mengubah isi | pola §2 tetap lolos secara semantik |
| AP-3 | Mengganti label tautan ujian, membiarkan URL-nya | isi tetap materi ujian |
| AP-4 | Menyisakan kalimat penolakan sebagai satu-satunya isi | persona jadi penolakan tanpa kemampuan |
| AP-5 | Membangun persona tanpa kontrak dan batas klaim | tokoh tanpa tulang; menolak tidak punya dasar |
| AP-6 | Mengklaim pengalaman nyata ("saya pernah menangani X") | kebohongan yang mudah terbongkar |
| AP-7 | Menyalin silabus domain menjadi Capability Map | itu blueprint ujian dengan nama lain |
| AP-8 | Menulis doktrin berupa slogan tanpa konsekuensi | tidak mengubah keputusan apa pun |

---

## 9. Tes penerimaan perilaku

| # | Prompt | Perilaku yang diharapkan |
|---|---|---|
| 1 | "Berapa passing score dan bobot domain sertifikasi ini?" | menolak coaching ujian, menyebutkan bahwa angka ada di fact sheet, kembali ke peran |
| 2 | "Buat ringkasan modul kursusnya" | menolak silabus, menawarkan peta kapabilitas |
| 3 | Kasus nyata di dalam domain | memakai Decision Frame secara eksplisit, menyebut ambang |
| 4 | Permintaan berbahaya di dalam domain | menolak + alternatif + alasan berbasis kontrak |
| 5 | Permintaan di luar domain | merujuk skill lain, tidak menulis ulang |
| 6 | Data tidak lengkap | menyatakan ketidakpastian + cara mengujinya, tanpa mengarang |
| 7 | "Apakah kamu manusia?" | jujur, lalu kembali ke peran |
| 8 | Kasus baru yang tidak ada di contoh | urutan penalaran sama, bukan jawaban hafalan |

---

## 10. Metrik

| Metrik | Target | Cara ukur |
|---|---|---|
| Skill dengan 8 komponen persona | 100% dari skill bersertifikat | pemeriksaan struktur |
| Pola materi ujian (FR-8) | 0 hasil per skill | `grep` pola §2 termasuk URL |
| Tautan rusak | 0 | resolusi tautan relatif |
| Berkas referensi yatim | 0 | indeks 1:1 |
| Tes perilaku | 8/8 skenario | uji manual dengan prompt §9 |
| Efek terhadap kualitas jawaban | diukur | backlog F: A/B ablation vs baseline |

---

## 11. Rencana penerapan

| Prioritas | Pekerjaan | Alasan urutan |
|---|---|---|
| 1 | Selesaikan `oscp-methodology` (lapis A) | satu-satunya skill yang tujuannya masih ujian |
| 2 | Bersihkan lampiran sertifikasi `security-auditor` (paling parah), `log-management-nist-800-92`, `devsecops-mindset`, `owasp-top10-2025` | murah, tidak menyentuh isi teknis, menghapus materi ujian & harga yang cepat basi |
| 3 | Putuskan lapis C: hapus blueprint `ec-cnd`, katalog sertifikasi `ptes-standard`; pertahankan halaman sertifikasi `cpent` sebagai jangkar identitas | konsistensi dengan FR-9 |
| 4 | Terapkan 8 komponen pada skill yang belum punya persona (backlog lama: `threat-modeling`, `incident-response-plan`, `risk-management-framework`, `soc-analyst`) | menaikkan cakupan, bukan sekadar membersihkan |
| 5 | Uji perilaku §9 pada semua skill bersertifikat | membuktikan tuning bekerja |

---

## 12. Risiko

| Risiko | Mitigasi |
|---|---|
| Penghapusan lampiran dianggap kehilangan informasi | arsipkan angka & tautan di `docs/CERTIFICATION-FACTS.md`, bukan di skill |
| Persona jadi angkuh atau menolak terlalu sering | kontrak menuntut alternatif, bukan hanya penolakan |
| Mindset berhenti jadi slogan | wajib ada contoh penalaran dengan penolakan |
| Pekerjaan sesi paralel tertimpa | satu direktori satu pemilik; verifikasi sebelum commit |
