---
name: "Detection Labs — Latihan yang Bisa Dibangun Sendiri"
description: "Latihan deteksi yang bisa dijalankan di lab milik sendiri: sumber telemetri yang harus menyala lebih dulu, dataset dan pembangkit serangan, delapan latihan dengan temuan yang diharapkan, serta anti-pattern yang membuat latihan tidak bernilai."
tags: [detection-labs, practice, telemetry, sysmon, atomic-red-team, elk, dataset, anti-patterns]
---

# Detection Labs

Latihan deteksi hanya berguna kalau telemetrinya nyata dan hasilnya bisa diulang. Delapan latihan di bawah dirancang untuk lab yang Anda bangun dan miliki sendiri — VM Windows, satu DC, satu host Linux, satu ELK — bukan untuk lingkungan yang tidak boleh disentuh. Tujuannya bukan menyelesaikan latihan, melainkan bisa menulis: "saya melihat ini, dari sumber ini, dengan query ini, dan inilah yang saya yakini".

## Prinsip latihan

1. **Telemetri dulu, serangan kemudian.** Kalau Anda belum tahu event apa yang terekam, hasil negatif tidak bisa ditafsirkan.
2. **Tulis ekspektasi sebelum eksekusi.** Tentukan event yang seharusnya muncul, lalu bandingkan dengan yang benar-benar muncul. Selisihnya adalah pelajaran.
3. **Satu variabel per latihan.** Ubah satu hal, eksekusi, lihat. Perubahan bertumpuk menghapus atribusi.
4. **Hasil negatif tetap dicatat.** "Tidak terekam" adalah temuan tentang telemetri, dan sering lebih berguna daripada temuan tentang serangan.
5. **Dokumentasikan seperti untuk orang lain.** Query, host, waktu, dan hasil — bukan screenshot yang hanya bisa dibaca oleh yang mengambilnya.

## Sumber telemetri yang harus menyala

| Sumber | Yang direkam | Catatan pemasangan |
|---|---|---|
| Winlogbeat | Security, System, Application, PowerShell Operational | kirim ke Elasticsearch atau lewat Logstash |
| Sysmon | proses, jaringan, image load, registry, DNS | config menentukan segalanya; mulai dari SwiftOnSecurity atau olafhartong |
| Audit policy Windows | 4688 dengan command line, 4662, 4768/4769 | 4688 tanpa command line hampir tidak berguna untuk investigasi |
| PowerShell logging | 4103 dan 4104 | harus diaktifkan lewat kebijakan, bukan bawaan |
| Filebeat | IIS W3C, auth.log/secure, access log web | satu input per jenis berkas |
| Elastic Agent + OSQuery | state: proses, port, service, user | dipakai untuk verifikasi, bukan deteksi |
| Suricata atau Zeek | flow dan alert jaringan | opsional; berguna untuk latihan C2 dan tunneling |

Tanpa tabel ini terisi, latihan berikutnya hanya akan mengajarkan bahwa "tidak ada log" berarti "tidak ada serangan" — kesimpulan yang salah dan mahal.

## Dataset dan pembangkit

| Bahan | Isi | Kapan dipakai |
|---|---|---|
| Atomic Red Team | eksekusi teknik ATT&CK yang dapat diulang | membangkitkan telemetri untuk latihan 2–5 dan 7 |
| EVTX-ATTACK-SAMPLES | kumpulan evtx dari teknik yang sudah dijalankan | berlatih membaca tanpa membangun lab penuh |
| DetectionLab | lab Windows + AD + SIEM yang bisa dibangun ulang | latihan yang butuh domain dan beberapa host |
| HELK | ELK untuk hunting dan analisis log | latihan 1, 5, dan 8 |
| Sigma | aturan deteksi generik untuk dibandingkan | memeriksa apakah deteksi Anda menangkap hal yang sama |
| sysmon-config / sysmon-modular | konfigurasi Sysmon | menyiapkan cakupan event sebelum latihan |

Dataset pihak ketiga bagus untuk kecepatan, tetapi ia tidak mengajarkan apa yang hilang di lingkungan Anda. Lab sendiri mengajarkan itu; dataset mengajarkan pola yang sudah diketahui orang lain.

## Latihan 1 — Validasi telemetri

**Tujuan:** mengetahui apa yang benar-benar terekam sebelum menyimpulkan apa pun.

**Langkah:** nyalakan Sysmon, audit policy, dan PowerShell logging; jalankan aktivitas biasa (login, buka aplikasi, jalankan `whoami`); lalu cari di Kibana.

**Temuan yang diharapkan:** daftar event yang muncul dan yang tidak. Apakah 4688 memuat command line? Apakah 4104 muncul? Apakah Sysmon 10 merekam akses ke `lsass.exe` atau difilter oleh config?

**Kesalahan umum:** menganggap event yang tidak muncul sebagai evasion. Di lab sendiri, event yang tidak muncul hampir selalu berarti konfigurasi.

## Latihan 2 — Eksekusi PowerShell terenkode

**Tujuan:** membedakan command line yang terlihat dari isi script yang sebenarnya berjalan.

**Langkah:** jalankan PowerShell dengan parameter terenkode, lalu telusuri dari 4688/Sysmon 1 ke 4104 dan 4103.

**Temuan yang diharapkan:** command line di 4688 hanya menampilkan string terenkode, sedangkan 4104 memuat isi hasil deobfuskasi. Rantai induk-anak menunjukkan siapa yang memulai.

**Kesalahan umum:** berhenti di command line dan menyimpulkan isi script tanpa membuka 4104. Bila 4104 tidak ada, yang Anda buktikan adalah logging tidak aktif, bukan script tidak berjalan.

## Latihan 3 — Akses kredensial ke LSASS

**Tujuan:** mengenali akses ke proses kredensial dan membedakannya dari aktivitas normal.

**Langkah:** di lab, akses `lsass.exe` dengan alat yang memang tersedia di lab; cari Sysmon 10 (ProcessAccess) dan Sysmon 8 bila ada injeksi, lalu lihat proses sumbernya di Sysmon 1.

**Temuan yang diharapkan:** Sysmon 10 dengan target `lsass.exe`, disertai identitas proses sumber dan konteks akun. Bandingkan dengan akses sah dari komponen sistem yang rutin.

**Kesalahan umum:** lupa bahwa Sysmon 10 sangat bergantung config dan sering difilter; sebelum menyebut "tidak ada dumping", pastikan event-nya direkam.

## Latihan 4 — Persistence lewat service dan scheduled task

**Tujuan:** membedakan pendaftaran mekanisme persistence dari eksekusi yang dihasilkannya.

**Langkah:** buat service dan scheduled task di lab, lalu telusuri 7045/4697, 4698, Sysmon 1 saat service berjalan, dan Sysmon 13 untuk perubahan registry terkait.

**Temuan yang diharapkan:** 7045 muncul saat pendaftaran, tetapi proses yang dijalankan service baru terlihat di 4688/Sysmon 1 pada waktu berikutnya. Scheduled task memperlihatkan pola serupa lewat 4698.

**Kesalahan umum:** menganggap 7045 sebagai bukti eksekusi. Yang terbukti adalah pendaftaran; eksekusi dicari terpisah.

## Latihan 5 — Menghapus log dan mengubah audit policy

**Tujuan:** belajar membaca gap tanpa langsung menyebut anti-forensics.

**Langkah:** di lab, hapus Security log dan ubah audit policy; lalu ukur apa yang hilang dan apa yang tetap ada di sumber lain.

**Temuan yang diharapkan:** 1102 untuk penghapusan Security log, 104 untuk System log, 4719 untuk perubahan audit policy. Sysmon dan agent yang mengirim ke SIEM bisa tetap merekam, sehingga hilangnya satu sumber tidak sama dengan hilangnya semua bukti.

**Kesalahan umum:** menyimpulkan seluruh jendela waktu kosong padahal hanya satu channel yang terhapus. Cek setiap sumber secara terpisah sebelum menyebut gap.

## Latihan 6 — Linux: brute force dan command injection

**Tujuan:** membaca auth log dan web access log sebagai dua sumber yang saling melengkapi.

**Langkah:** lakukan percobaan SSH gagal berulang di lab, lalu akses endpoint web dengan parameter perintah; korelasikan `auth.log`/`secure` dengan access log Apache/Nginx.

**Temuan yang diharapkan:** pola `Failed password` berulang dari satu sumber, diikuti `Accepted` bila berhasil; access log memuat URI dengan parameter perintah; perubahan `.bashrc`, `.profile`, atau `authorized_keys` bila persistence dipasang.

**Kesalahan umum:** berhenti pada auth log. Autentikasi berhasil tidak menjelaskan apa yang dilakukan setelahnya.

## Latihan 7 — Kerberoasting dan DCSync di lab AD

**Tujuan:** memisahkan administrasi domain yang sah dari penyalahgunaan Kerberos dan replikasi.

**Langkah:** di lab dengan satu DC, minta service ticket dengan enkripsi RC4 dan lakukan replikasi direktori lewat akun uji; cari 4769, 4768, dan 4662.

**Temuan yang diharapkan:** 4769 dengan `0x17` berulang dari satu akun dalam waktu singkat; 4662 pada objek domain dengan hak replikasi disertai konteks akun dan host sumber.

**Kesalahan umum:** menyimpulkan dari volume saja. Service account yang sah juga meminta banyak ticket; yang membedakan adalah akun, waktu, dan host asal.

## Latihan 8 — Beacon dan DNS tunneling

**Tujuan:** mengenali pola berulang di jaringan, bukan sekadar alert IDS.

**Langkah:** buat koneksi periodik ke host lab dan query DNS yang tidak lazim; lihat Sysmon 22, Sysmon 3, log proxy/firewall, dan alert Suricata bila tersedia.

**Temuan yang diharapkan:** interval koneksi yang berulang dan ukuran payload yang mirip antar-request; query DNS dari satu host dengan pola nama acak atau volume yang menyimpang dari baseline.

**Kesalahan umum:** mengandalkan satu request. Beacon dinilai dari pola antar-waktu; satu koneksi tidak membuktikan apa pun.

## Cara menilai diri

- **Replikasi.** Berikan query dan catatan Anda ke orang lain; kalau ia tidak bisa mendapatkan hasil yang sama, dokumentasinya belum cukup.
- **Waktu menjawab.** Catat berapa lama dari alert ke kesimpulan pertama; itu metrik yang bisa diperbaiki.
- **Hasil negatif.** Simpan latihan yang tidak menemukan apa pun beserta alasannya; kemampuan membedakan "tidak ada" dan "tidak terlihat" adalah inti pekerjaan ini.
- **Uji ulang.** Ulangi satu latihan setelah mengubah config atau query; perubahan hasil adalah bukti bahwa Anda memahami penyebabnya.

## Anti-pattern

| Anti-pattern | Mengapa gagal | Perbaikan |
|---|---|---|
| Terpaku pada urutan timestamp | revert membuat urutan waktu menipu | susun narasi per tindakan, timestamp sebagai bukti |
| Melewati 4104 | justru di sana kode hasil deobfuskasi muncul | cari 4104 lebih dulu untuk aktivitas PowerShell |
| Tidak memasang kolom | pola tidak terlihat di tabel hasil | pasang `process.command_line` dan `user.name` sejak awal |
| Mengasumsikan success | alat berjalan belum tentu berhasil | verifikasi lewat event berikutnya |
| Melewati verifikasi OSQuery | state aktif tidak terlihat di log | pakai OSQuery untuk port, service, dan proses |
| Tidak mendokumentasikan query | tidak ada yang bisa direplikasi | query, host, waktu, hasil — satu paket |
| Terlalu percaya alert | sebagian alert adalah rabbit hole | verifikasi manual sebelum masuk laporan |

## Best Practices

- Bangun lab sekecil yang cukup: satu Windows, satu DC, satu Linux, satu ELK sudah memberi hampir semua pelajaran.
- Catat konfigurasi telemetri bersama hasil latihan; tanpa itu hasilnya tidak bisa dibandingkan antar waktu.
- Perlakukan setiap latihan sebagai investigasi kecil: hipotesis, query, bukti, keyakinan.
- Simpan laporan latihan memakai [report-template.md](../assets/report-template.md); kebiasaan menulis saat tenang akan terbawa saat terburu-buru.
- Jangan menyimpulkan pola dari satu kali eksekusi; ulangi minimal sekali sebelum menuliskan karakteristiknya.
