# Analisis Kebutuhan — Skill Persona CND (Certified Network Defender)

**Status:** Draf — menunggu persetujuan sebelum implementasi
**Tanggal:** 2026-11-09
**Target:** `skills/ec-cnd/` (belum ada)
**Sumber fakta:** [halaman sertifikasi CND](https://cert.eccouncil.org/certified-network-defender.html) dan [CND Exam Blueprint v4.0](https://cert.eccouncil.org/wp-content/uploads/2024/04/CND-Exam-Blueprint-v4.pdf), diakses 2026-11-09

---

## 1. Ringkasan

Repo punya 28 skill, dua di antaranya EC-Council: `cpent` (persona ofensif) dan `ec-ecih` (incident handler). Tidak ada satu pun yang memerankan **network defender** — peran yang justru menjadi inti CND: orang yang memiliki, mengoperasikan, dan mempertanggungjawabkan kontrol jaringan.

Rekomendasi: bangun `ec-cnd` dengan pola yang sama seperti `cpent` — **persona praktisi bersertifikat, bukan materi persiapan ujian**, dengan 8 domain CND sebagai jangkar kapabilitas. Fakta ujian tidak dimasukkan ke skill; bila angka ujian tetap diinginkan, jalur alternatifnya adalah menambah baris CND ke `docs/CERTIFICATION-FACTS.md` dan mendaftarkan skill ke `scripts/check-fact-notes.js`.

Yang membuat skill ini bernilai bukan pengetahuan CND-nya (itu bisa dicari), melainkan **cara memutuskan**: layer kontrol mana yang dipilih, kapan perubahan ditolak, bukti apa yang diambil, dan kapan eskalasi. Itu bagian yang belum ada di repo.

**Klarifikasi tujuan (2026-11-10):** target akhirnya adalah **persona injection pengguna** yang memegang CND — agent meminjam persona pengguna (profil, suara, preferensi, batas klaim), bukan memerankan praktisi generik atau tutor. Karena itu `SKILL.md` dan `persona.md` memakai framing "persona pengguna" dan memuat bagian mekanika injection eksplisit (aktivasi, konsistensi, kepemilikan, keluar peran).

---

## 2. Kondisi Repo Saat Ini

### 2.1 Inventaris yang relevan

| Skill | Posisi | Kedekatan dengan CND |
|---|---|---|
| `offsec-soc-200` | 🔵 Blue team | Deteksi jaringan/endpoint, SIEM — **paling dekat**, tapi berpusat pada analis SOC |
| `offsec-th-200` | 🔵 Blue team | Threat hunting, Suricata IDS/IPS |
| `ec-ecih` | 🔵 Blue team | IR lifecycle, containment, forensics |
| `offsec-ir-200` | 🔵 Blue team | Live response, forensik host |
| `comptia-cysa` | 🟢 General | SecOps, vulnerability management |
| `log-management-nist-800-92` | 🔵 Blue team | Log sources, retensi |
| `nist-800-53` | 🔵 Blue team | Katalog kontrol (termasuk SC/SI/AU) |
| `threat-intelligence`, `mitre-attack` | 🔵 Blue team | CTI, TTP mapping |
| `lf-cks` | 🔵 Blue team | Kubernetes security |
| `waf-evasion-methodology`, `web-pentest-payloads` | 🔴 Red team | Ofensif — bukan sudut pandang defender |

### 2.2 Kesenjangan terhadap 8 domain CND

| Domain CND | Cakupan sekarang | Verdict |
|---|---|---|
| 1. Network Defense Management | tersebar di `threat-modeling`, `risk-management-framework`, `security-auditor` | konsep ada, persona tidak |
| 2. Network Perimeter Protection | tidak ada (deteksi ada di SOC-200/TH-200; WAF baru dari sisi ofensif) | **gap terbesar** |
| 3. Endpoint Protection | SOC-200/IR-200 mendeteksi & mentriage; hardening tidak ada | sebagian |
| 4. Application & Data Protection | `web-app-scan`/`owasp-top10` ofensif; `security-auditor` GRC | gap defensif |
| 5. Enterprise Virtual/Cloud/Wireless | `lf-cks` (k8s saja) | gap |
| 6. Incident Detection | SOC-200, TH-200, log-management | tercakup |
| 7. Incident Response | ECIH, IR-200, incident-response-plan | tercakup |
| 8. Incident Prediction | CTI, MITRE, RMF, NIST 800-53 | konsep tercakup, operasional tidak |

Kesimpulan: domain 1–5 adalah ruang kosong yang hanya bisa diisi persona yang **memiliki kontrol** — bukan analis yang membaca alert, bukan auditor yang memeriksa kepatuhan.

### 2.3 Catatan kondisi kerja

- Working tree sedang memuat perubahan belum-commit untuk `cpent` (0.12.0) dan `offsec-ir-200` (0.13.0). Implementasi CND tidak boleh me-revert keduanya.
- `cpent` saat analisis punya **16 berkas referensi**, tetapi `SKILL.md` hanya mengindeks 12 dan `docs/SKILL-QUALITY.md` saat itu mencatat 12. Hitungan dapat berubah karena sesi lain masih aktif; yang tidak boleh ditiru adalah **drift**-nya: setiap berkas referensi CND wajib muncul di indeks.

---

## 3. Fakta Terverifikasi (CND)

### 3.1 Ujian

| Item | Nilai | Sumber |
|---|---|---|
| Kode ujian | **312-38** | halaman sertifikasi |
| Jumlah soal | **100** | halaman sertifikasi |
| Durasi | **4 jam** | halaman sertifikasi |
| Cut score | **60–85% per form** | halaman sertifikasi |
| Blueprint | **v4.0** (berkas 2024/04) | PDF blueprint |

> Catatan kualitas sumber: sampul PDF menulis "v4.0", tetapi footer setiap halaman masih "v3.0" — kemungkinan template yang tidak diperbarui. Bila angka ini masuk fact sheet, ketidakcocokan itu harus dicatat, bukan disembunyikan.

### 3.2 Struktur blueprint v4.0

Setiap sub-domain berbobot 5 soal; bobot domain = jumlah sub-domain × 5%.

| # | Domain | Bobot | Sub-domain |
|---|---|---|---|
| 1 | Network Defense Management | 10% | Network Attacks and Defense Strategies; Administrative Network Security |
| 2 | Network Perimeter Protection | 10% | Technical Network Security; Network Perimeter Security |
| 3 | Endpoint Protection | **20%** | Windows Systems; Linux Systems; Mobile Devices; IoT Devices |
| 4 | Application and Data Protection | 10% | Administrative Application Security; Data Security |
| 5 | Enterprise Virtual, Cloud, and Wireless Network Protection | 15% | Enterprise Virtual Network Security; Enterprise Cloud Network Security; Enterprise Wireless Network Security |
| 6 | Incident Detection | 10% | Network Traffic Monitoring and Analysis; Network Logs Monitoring and Analysis |
| 7 | Incident Response | 10% | Incident Response and Forensic Investigation; Business Continuity and Disaster Recovery |
| 8 | Incident Prediction | 15% | Risk Anticipation with Risk Management; Threat Assessment with Attack Surface Analysis; Threat Prediction with Cyber Threat Intelligence |

Total 20 sub-domain = 100 soal. Bobot terbesar ada di domain 3 (endpoint, 20%), disusul domain 5 dan 8 (masing-masing 15%) — sinyal bahwa CND bukan sekadar "firewall engineer".

---

## 4. Definisi Persona

### 4.1 Profil

| Aspek | Isi |
|---|---|
| Peran | Network security engineer / network defender |
| Pengalaman | 6–10 tahun: jaringan dulu, lalu keamanan jaringan |
| Lingkungan | Enterprise dengan segmen (DMZ, internal, kadang OT) atau MSSP |
| Kekuatan | Perimeter, segmentasi, hardening endpoint, monitoring trafik/log, first responder |
| Bukan bidangnya | exploit development, reverse engineering malware, GRC audit formal, arsitektur Kubernetes mendalam |
| Bahasa | Indonesia dengan istilah teknis Inggris; tenang, prosedural, berbasis bukti |

Berbasis pada target audiens resmi CND: network administrator, network security engineer, network defense technician, security analyst/operator.

### 4.2 Persona Contract (usulan 7 butir)

1. **Ketersediaan adalah properti keamanan.** Kontrol yang memutus layanan adalah insiden baru.
2. **Kontrol di layer yang benar.** Segmentasi sebelum WAF; hardening sebelum deteksi tambahan.
3. **Default deny, least privilege, explicit allow.**
4. **Baseline sebelum anomali.** Tanpa baseline, tidak ada klaim.
5. **Satu perubahan, satu variabel.** Rollback disiapkan sebelum eksekusi.
6. **Setiap aturan/log punya pemilik dan masa berlaku.**
7. **Eskalasi bukan kegagalan.** First responder menjaga bukti, bukan memperbaiki.

### 4.3 Decision Frame (usulan 7 pertanyaan)

1. Aset apa yang dilindungi, milik siapa, seberapa kritis?
2. Layer mana yang paling murah dan efektif: data, aplikasi, host, atau jaringan?
3. Berapa blast radius perubahan ini, dan apa rollback-nya?
4. Apakah baseline dan telemetri cukup untuk membuktikan klaim?
5. Siapa yang berwenang menyetujui perubahan atau pemutusan?
6. Bukti apa yang hilang jika aku bertindak sekarang?
7. Bagaimana kita tahu kontrol ini benar-benar bekerja — metrik, alert, atau uji?

### 4.4 Doktrin kerja (usulan)

- Pahami normal sebelum mengejar abnormal.
- Segmentasi mengikuti trust, bukan kemudahan.
- Setiap aturan punya pemilik dan tanggal kedaluwarsa.
- Deteksi tanpa respons hanyalah log yang mahal.
- Ubah satu hal, ukur, lalu lanjut.
- Defense-in-depth adalah kegagalan berlapis, bukan tumpukan alat.
- First responder menjaga, bukan memperbaiki.
- Ketersediaan adalah bagian CIA, bukan lawannya.

---

## 5. Peta Kapabilitas → Domain

| Domain CND | Kapabilitas yang diperankan | Bukti khas |
|---|---|---|
| 1. Defense management | Klasifikasi serangan, strategi pertahanan, kebijakan, awareness, asset inventory | risk register, attack-surface inventory |
| 2. Perimeter | Firewall policy, rule hygiene, IDS/IPS tuning, router/switch hardening, Zero Trust/SDP, NAC | rule review, alert quality, segment test |
| 3. Endpoint | Baseline Windows/AD, Linux, mobile/MDM, IoT | skor CIS, GPO, cakupan EDR |
| 4. App & data | App control, patch, WAF lifecycle, enkripsi at-rest/in-transit, DLP, backup/restore | TLS config, DLP policy, restore test |
| 5. Virtual/cloud/wireless | SDN/NFV, container baseline, AWS/Azure/GCP, Wi-Fi | security group review, CSPM, WLC config |
| 6. Detection | Traffic monitoring (Wireshark/pcap), log sumber (Win/Linux/firewall/router/web), sentralisasi, anomali | baseline, detection coverage matrix |
| 7. Response | First responder, EDR/MDR/XDR/SOAR, forensik jaringan, BC/DR | runbook, tabletop, image |
| 8. Prediction | RMF, vulnerability management, attack surface/IoE, simulasi, CTI/IoC/IoA, hunting | SLA patch, attack-surface map, TI-driven detection |

---

## 6. Arsitektur Referensi Usulan

14 berkas, mengikuti pola `cpent` (SKILL.md tipis + referensi berfokus):

| # | Berkas | Isi | Domain |
|---|---|---|---|
| 1 | `persona.md` | Profil, suara, preferensi, batas klaim, contoh jawaban | — |
| 2 | `defense-playbook.md` | Siklus assess → design → implement → operate → respond → improve; change management; otorisasi; runbook | 1, 7 |
| 3 | `network-architecture.md` | Trust zone, DMZ, segmentasi, NAC, Zero Trust/SDP, routing/switching | 2 |
| 4 | `perimeter-controls.md` | Desain kebijakan firewall, rule hygiene, IDS/IPS tuning, VPN/TLS, penempatan WAF | 2 |
| 5 | `endpoint-hardening.md` | Windows/AD, Linux, mobile/MDM, IoT | 3 |
| 6 | `app-data-protection.md` | App control/sandbox, patch, WAF rule lifecycle, enkripsi, DLP, backup/retensi/destruksi | 4 |
| 7 | `cloud-virtual-wireless.md` | SDN/NFV, container/Kubernetes baseline, AWS/Azure/GCP, wireless | 5 |
| 8 | `detection-telemetry.md` | pcap/traffic, sumber log, baseline, anomali, centralized logging, metrik deteksi | 6 |
| 9 | `incident-response.md` | First responder, EDR/MDR/XDR/SOAR, forensik tingkat jaringan, BC/DR, serah-terima ke tim IR | 7 |
| 10 | `risk-threat-intel.md` | RMF, vulnerability management, attack surface, konsumsi CTI, hunting | 8 |
| 11 | `capability-domains.md` | Peta 8 domain + bukti + cara memakainya | semua |
| 12 | `tools-diagnostics.md` | Field kit & perintah read-only (nft/iptables, tcpdump, ss, Zeek/Suricata, Wireshark, Nessus/OpenVAS, CIS-CAT) | 2, 3, 6 |
| 13 | `reasoning-examples.md` | 5–6 skenario first-person: perubahan rule, alert storm, segmentasi, serah-terima insiden, eksposur cloud | semua |
| 14 | `referensi.md` | Sumber eksternal: blueprint, NIST 800-41/94/61, CIS, MITRE ATT&CK/D3FEND, dokumentasi vendor | — |

Aturan: setiap berkas wajib muncul di tabel **Reference Documentation**; Capability Map dan Progressive Disclosure boleh merujuk ulang. Tidak boleh ada berkas yatim, dan tidak boleh ada baris indeks ganda. Ini menutup drift yang terjadi di `cpent`.

---

## 7. Batas Scope dan Anti-Duplikasi

| Skill existing | Yang TIDAK diduplikasi CND | Batas yang diambil CND |
|---|---|---|
| `ec-ecih` | IR lifecycle, eradication, reporting | first responder tingkat jaringan + serah-terima |
| `offsec-ir-200` | Forensik host, volatile evidence, live response | preserve & eskalasi, bukan akuisisi penuh |
| `offsec-soc-200` | Detection engineering, query SIEM | cakupan sumber log & kualitas alert |
| `soc-analyst` | Triage mindset | kepemilikan kontrol & perubahan |
| `offsec-th-200` | Metodologi hunting (PEAK/SEARCH) | hunting sebagai konsumsi prioritas |
| `threat-intelligence` | Siklus CTI, TIP, STIX | memakai TI untuk memprioritaskan kontrol |
| `mitre-attack` | Struktur ATT&CK | gap analysis & pemetaan coverage |
| `nist-800-53` | Katalog & assessment kontrol | implementasi teknis SC/SI/AU |
| `lf-cks` | Kubernetes mendalam | baseline container secukupnya |
| `risk-management-framework` | RMF penuh | risk register & keputusan mitigasi operasional |
| `waf-evasion-methodology` | Teknik bypass | lifecycle aturan WAF dan validasinya |
| `web-pentest-payloads`, `ptes-standard` | Ofensif | validasi defensif saja, tanpa instruksi eksploitasi |

Prinsip: CND boleh **merujuk** skill lain, tetapi setiap kali topik mendalam dibutuhkan, ia menunjuk file yang sudah ada alih-alih menulis ulang.

---

## 8. Kebutuhan Fungsional & Non-Fungsional

### 8.1 Fungsional

| ID | Kebutuhan | Kriteria lulus |
|---|---|---|
| FR-1 | Agent mengadopsi persona network defender saat skill dimuat | jawaban memakai suara persona, bukan tutor generik |
| FR-2 | Struktur jawaban ringkas → alasan → langkah → bukti → risiko | konsisten di semua contoh |
| FR-3 | Menolak perubahan berisiko tanpa otorisasi/rollback | skenario 1 & 6 lulus |
| FR-4 | Memetakan masalah ke salah satu 8 domain | setiap skenario menyebut domain |
| FR-5 | Menyediakan diagnostik read-only sebelum rekomendasi | perintah aman, tanpa perubahan state |
| FR-6 | Merujuk skill lain saat di luar batas | tidak menduplikasi IR dalam/k8s/GRC |
| FR-7 | Tidak membahas soal, bobot, atau strategi ujian | grep angka ujian = 0 |

### 8.2 Non-fungsional

| ID | Kebutuhan |
|---|---|
| NFR-1 | `SKILL.md` ≤ 500 baris; total referensi ≤ 16 |
| NFR-2 | Tidak mengarang CVE, ambang, atau output tool; ketidakpastian eksplisit |
| NFR-3 | Bahasa Indonesia + istilah teknis Inggris, konsisten |
| NFR-4 | Klaim teknis dapat dilacak ke `referensi.md` |
| NFR-5 | Progressive disclosure: indeks 1:1, tanpa berkas yatim |
| NFR-6 | Skill berdiri sendiri saat dipasang (tidak bergantung `docs/`) |

### 8.3 Konstrain

| ID | Konstrain |
|---|---|
| C-1 | Ikuti `AGENTS.md`: frontmatter, frontmatter referensi, changelog, sync |
| C-2 | Tidak mengubah skill lain; perubahan hanya file baru + generated + CHANGELOG/README/SKILL-QUALITY |
| C-3 | Jangan me-revert perubahan 0.12.0/0.13.0 yang belum commit |
| C-4 | Lisensi MIT |
| C-5 | Persona, bukan exam prep |

---

## 9. Risiko dan Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Cakupan 20 sub-domain membanjiri persona | jawaban dangkal di semua topik | jangkar 8 domain; referensi berisi keputusan, bukan tutorial |
| Duplikasi dengan ECIH/SOC-200/IR-200 | repo redundan, user bingung | tabel batas + rujukan silang di setiap berkas |
| Drift ke exam prep | skill kehilangan identitas persona | tanpa angka ujian; deskripsi menegaskan "bukan persiapan ujian" |
| Vendor lock-in | jawaban tidak portabel | konsep dulu, contoh vendor diberi label |
| Klaim CVE/ambang karangan | kredibilitas rusak | aturan ketidakpastian + larangan output palsu |
| Perubahan konfigurasi memutus layanan | bahaya nyata | contract #1, decision frame #3, rollback wajib |
| Scope creep ke ofensif | salah fungsi | validasi defensif saja; rujuk skill red team |
| Berkas yatim seperti `cpent` | indeks tidak sinkron | uji 1:1 indeks–berkas di kriteria penerimaan |

---

## 10. Kriteria Penerimaan

### 10.1 Struktural

- `SKILL.md` memuat: Profil Persona, Kapan Dipakai, Cara Memerankan, Persona Contract, Decision Frame, Operating Doctrine, Workflow, Capability Map, Reference Documentation, Gotchas (≥ 6), Progressive Disclosure, License.
- 14 berkas referensi, masing-masing ber-frontmatter `name`/`description`/`tags` dan diakhiri Best Practices.
- Setiap berkas muncul di tabel Reference Documentation (tidak ada berkas yatim); tidak ada baris indeks ganda.
- `node scripts/sync-skills.js` memperbarui `manifest.json`, `skills/index.json`, dan plugin.
- `README.md` (tabel Blue Team) dan `docs/SKILL-QUALITY.md` diperbarui.
- `node scripts/check-fact-notes.js` lulus **tanpa** mendaftarkan `ec-cnd` (persona-only).
- `node scripts/check-changelog.js --base HEAD` lulus dengan entri 0.14.0.
- `grep -R` untuk `312-38|100 soal|cut score` di `skills/ec-cnd/` = 0 hasil.

### 10.2 Perilaku (6 skenario uji)

| # | Prompt | Perilaku yang diharapkan |
|---|---|---|
| 1 | "Buka RDP dari internet untuk vendor" | tolak default-deny; tawarkan VPN/allowlist + perubahan terkelola |
| 2 | "IDS alert storm setelah rule baru" | triage false positive, tuning, baseline |
| 3 | "Ransomware di satu segmen" | containment, preservasi bukti, eskalasi, trade-off ketersediaan |
| 4 | "Security group 0.0.0.0/0 di cloud" | triase eksposur, blast radius, urutan perbaikan |
| 5 | "Berapa soal ujian CND?" | menolak coaching ujian, kembali ke persona |
| 6 | "TLS lama di aplikasi legacy" | risk acceptance, compensating control, jalur migrasi |

Lulus bila: persona konsisten, decision frame dipakai eksplisit, tidak ada fakta karangan, dan setiap perubahan punya otorisasi + rollback.

---

## 11. Keputusan yang Perlu Disetujui

| # | Keputusan | Opsi | Rekomendasi |
|---|---|---|---|
| D1 | Angka ujian | persona-only / tambah fact sheet + checker | **persona-only** (paritas `cpent`, hindari exam drift) |
| D2 | Nama skill | `ec-cnd` / `cnd` | **`ec-cnd`** (konsisten dengan `ec-ecih`) |
| D3 | Kedalaman referensi | 10 ringkas / 14 / 16 | **14** (cukup untuk 8 domain, di bawah batas 16) |
| D4 | Cloud & Kubernetes | ringkas / mendalam | **ringkas** (mendalam sudah ada di `lf-cks`) |
| D5 | IR | tingkat jaringan + serah-terima / penuh | **tingkat jaringan** (penuh sudah ada di `ec-ecih`/`offsec-ir-200`) |
| D6 | Bahasa | Indonesia + istilah Inggris / Inggris | **Indonesia + istilah Inggris** (mayoritas repo) |
| D7 | Dokumen ini | `docs/` permanen / hapus setelah implementasi | **permanen** (jejak keputusan desain) |
| D8 | Penomoran changelog | satu entri 0.14.0 saat implementasi | **0.14.0** |

---

## 12. Rencana Implementasi (bila disetujui)

1. **Fase A — kerangka:** buat `skills/ec-cnd/`, tulis `SKILL.md` + `persona.md` + `capability-domains.md`.
2. **Fase B — domain:** `network-architecture`, `perimeter-controls`, `endpoint-hardening`, `app-data-protection`, `cloud-virtual-wireless`.
3. **Fase C — operasi:** `detection-telemetry`, `incident-response`, `risk-threat-intel`, `defense-playbook`, `tools-diagnostics`, `reasoning-examples`, `referensi`.
4. **Fase D — integrasi:** `node scripts/sync-skills.js`, baris README + SKILL-QUALITY, entri `CHANGELOG.md` 0.14.0.
5. **Fase E — verifikasi:** tiga checker repo, uji indeks 1:1, grep angka ujian, jalankan 6 skenario uji.

---

## Lampiran — Log Sumber

| Sumber | Yang diambil | Status |
|---|---|---|
| `cert.eccouncil.org/certified-network-defender.html` | kode ujian, 100 soal, 4 jam, cut 60–85%, audiens | terverifikasi 2026-11-09 |
| `cert.eccouncil.org/wp-content/uploads/2024/04/CND-Exam-Blueprint-v4.pdf` | 8 domain, 20 sub-domain, bobot, isi tiap sub-domain | terverifikasi via `pdftotext`, 2026-11-09 |
| `docs/CERTIFICATION-FACTS.md` | format provenance & tanggal snapshot | dibaca, belum memuat CND |
| `skills/cpent/SKILL.md` + `references/persona.md` | model persona, kontrak, decision frame, struktur indeks | dibaca |
