---
name: "Burp Suite — Alur Kerja Profesional"
description: "Cara memakai Burp Suite secara disiplin pada engagement: konfigurasi scope dan TLS, Repeater untuk hipotesis, Intruder terbatas, Collaborator untuk OOB, triage scanner, ekstensi minimum, disiplin bukti, higiene data klien, dan kapan tidak memakai Burp."
tags: [burp, proxy, repeater, intruder, collaborator, scanner, evidence, web]
---

# Burp Suite — Alur Kerja Profesional

Burp adalah proxy, bukan penyelesai masalah. Nilainya datang dari hipotesis yang diuji manual, bukan dari jumlah request yang dilewatkan ke scanner.

## 1. Prinsip

- **Manual dulu, otomatis kemudian.** Repeater membuktikan hipotesis; scanner mencari kandidat.
- **Satu request, satu bukti.** Request mentah + response + waktu adalah bukti; screenshot UI bukan.
- **Scope mengikat.** Semua tool di Burp hanya boleh menyentuh host di scope.
- **Batas noise.** Scan, Intruder, dan fuzzing adalah pengeluaran noise; hitung sebelum menjalankan.

## 2. Konfigurasi awal

1. **Target → Scope** — tambahkan host/CIDR di scope; aktifkan "Use advanced scope control"; keluarkan host di luar kontrak.
2. **Proxy → Options** — listener hanya di `127.0.0.1`; jangan buka ke `0.0.0.0` di jaringan klien.
3. **TLS** — instal CA Burp di browser khusus engagement; jangan di browser harian.
4. **Browser terpisah** — profil bersih tanpa ekstensi, cookie, dan sesi pribadi.
5. **Project file** — simpan di direktori engagement, bukan folder bersama.
6. **Sessions** — atur macro/login bila aplikasi memakai token berumur pendek.
7. **Intercept** — matikan intercept global; pakai "Intercept is off" dan andalkan HTTP history.
8. **Match/Replace** — hanya untuk header yang memang perlu (mis. `User-Agent` uji), bukan menutupi bug.

## 3. Alur kerja

```
Browse terkontrol → HTTP history → pilih request → Repeater (hipotesis)
→ konfirmasi → bukti → lanjutkan
```

- **HTTP history** adalah peta permukaan: endpoint, parameter, status, panjang respons.
- **Repeater** untuk mengubah satu variabel dan membandingkan respons; beri nama tab sesuai temuan.
- **Intruder** hanya ketika ruang uji terbatas dan terukur.
- **Scanner** dijalankan di background setelah permukaan dipahami, lalu **setiap temuan diverifikasi**.

## 4. Repeater

- Ubah satu variabel per request; catat sebelum/sesudah.
- Gunakan "Send to Repeater" dari history, bukan mengetik ulang request.
- Untuk perbandingan, simpan dua tab: baseline dan payload.
- Tandai temuan dengan nama yang konsisten: `SQLi-item-id`, `IDOR-invoice`.
- Ekspor request/response sebagai bukti sebelum menutup project.

## 5. Intruder

| Tipe | Kapan dipakai | Catatan |
|---|---|---|
| Sniper | Satu parameter, banyak payload | Default untuk enumerasi kecil |
| Battering ram | Payload sama di banyak posisi | Uji konsistensi |
| Pitchfork | Pasangan kredensial/parameter paralel | Login matrix |
| Cluster bomb | Kombinasi parameter | Hati-hati ledakan jumlah request |

- Atur **concurrency** rendah (1–5) dan tambahkan delay untuk target produksi.
- Gunakan **payload processing** untuk encoding, bukan payload yang tidak terbaca.
- Hentikan bila status/response menunjukkan lockout atau rate limit.
- Simpan hasil ke file untuk analisis, bukan menilai dari UI.

## 6. Collaborator dan OOB

- Cocok untuk SSRF, blind XSS, blind injection, XXE, dan deserialisasi.
- Generate payload unik per uji; jangan memakai domain yang sama untuk semua.
- Poll setelah request dikirim; catat waktu dan protokol yang masuk.
- Jika tidak ada callback, jangan langsung menyimpulkan "tidak rentan" — cek egress target dan filter.

## 7. Scanner

- Scan hanya host di scope; batasi crawl dan audit.
- Verifikasi manual setiap issue; scanner sering salah pada:
  - reflected XSS di response yang tidak dirender;
  - SQLi time-based karena latensi;
  - "sensitive data" pada halaman publik.
- Jangan mengandalkan scan untuk logika bisnis, otorisasi, dan IDOR — itu kerja manual.
- Catat konfigurasi scan (crawl, audit, throttle) di laporan bila hasilnya dikutip.

## 8. Ekstensi minimum

| Ekstensi | Kegunaan |
|---|---|
| Param Miner | Menemukan parameter tersembunyi |
| Autorize | Matriks otorisasi antar peran |
| JWT Editor | Inspeksi dan uji token |
| Logger++ | Arsip request/response untuk bukti |
| Turbo Intruder | Uji throughput tinggi yang terukur |

Pasang hanya yang dipakai; setiap ekstensi menambah permukaan dan noise.

## 9. Disiplin bukti dan data

- Simpan request/response mentah, timestamp, dan host di catatan temuan.
- Redaksi cookie, token, dan PII sebelum masuk laporan.
- Jangan menyimpan data klien di project file yang berpindah antar mesin.
- Hapus project, browser profile, dan CA saat engagement selesai (kecuali arsip yang disepakati).

## 10. Kapan tidak memakai Burp

- Protokol non-HTTP (SMB, LDAP, Modbus, MQTT) — gunakan tool khusus.
- Binary dan driver — debugger, bukan proxy.
- Uji volume tinggi yang berisiko DoS — hentikan dan minta izin.
- Aplikasi dengan certificate pinning yang tidak bisa diuji di klien uji.

## 11. Jebakan umum

1. **CA belum terpasang** — traffic HTTPS tidak terlihat, lalu disimpulkan "tidak ada API".
2. **Scope tidak diatur** — scanner menyentuh host pihak ketiga.
3. **Intercept global aktif** — browser terasa hang dan sesi rusak.
4. **Intruder tanpa batas** — lockout akun atau rate limit klien.
5. **Scanner dipercaya mentah** — laporan berisi false positive.
6. **Bukti dari UI** — tidak bisa direproduksi reviewer.
7. **Project berisi data klien** — risiko kebocoran sekunder.

## 12. Manipulasi header request

- **Repeater** adalah alat utama: duplikasi baseline, tambah satu header, bandingkan status/panjang/waktu/body.
- **Match/Replace** untuk menyuntikkan header ke semua request; matikan setelah uji selesai.
- **Intruder** dengan posisi payload di nilai header; Pitchfork untuk kombinasi, bukan Cluster Bomb.
- **Collaborator** untuk OOB saat header diteruskan ke shell, SSRF, atau layanan internal.
- **HTTP Request Smuggler / Turbo Intruder** hanya untuk desync dengan izin eksplisit.

Katalog header, payload, verifikasi, dan batas etikanya ada di [header-manipulation.md](./header-manipulation.md). Untuk encoding berlapis saat melewati WAF, gunakan Hackvertor dan prosedur di [waf-evasion.md](./waf-evasion.md).

## Best Practices

- Mulai dari history, bukan scanner.
- Satu hipotesis, satu request, satu bukti.
- Hormati scope, rate limit, dan window di RoE.
- Verifikasi setiap temuan sebelum menulisnya.
- Bersihkan artefak Burp sebelum keluar.
