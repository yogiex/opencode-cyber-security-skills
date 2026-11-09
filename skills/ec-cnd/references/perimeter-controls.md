---
name: "Perimeter Controls — Firewall, IDS/IPS, VPN, WAF"
description: "Pengelolaan kontrol perimeter: anatomi dan higiene aturan firewall, siklus tuning IDS/IPS, desain akses remote dan TLS, penempatan WAF, pengendalian DDoS, serta verifikasi dan rollback perubahan."
tags: [firewall, iptables, nftables, ids, ips, vpn, tls, waf, ddos, rule-hygiene, change-management]
---

# Perimeter Controls — Firewall, IDS/IPS, VPN, WAF

Perimeter adalah **batas kebijakan**, bukan merk perangkat. Yang dipertahankan defender adalah keputusan: siapa boleh lewat, ke mana, dengan bukti apa, dan bagaimana membatalkannya bila salah.

## 1. Anatomi aturan firewall

Setiap aturan yang baik menjawab lima hal:

| Elemen | Pertanyaan |
|---|---|
| Sumber | siapa/apa yang diizinkan — sepersempit mungkin |
| Tujuan | layanan apa, di host mana |
| Layanan | port/protokol/aplikasi, stateful bila mungkin |
| Pemilik | siapa yang meminta dan bertanggung jawab |
| Masa berlaku | kapan ditinjau atau dicabut |

Aturan tanpa pemilik dan tanpa tanggal review adalah utang operasional.

## 2. Higiene aturan

- **Default deny** di ingress dan egress; allowlist eksplisit.
- **Hindari `any`** pada sumber, tujuan, dan layanan secara bersamaan.
- **Urutan penting**: aturan spesifik sebelum umum; waspadai shadowing.
- **Review hit count** berkala. Aturan dengan hit 0 selama periode wajar adalah kandidat penghapusan.
- **Satu aturan satu tujuan**; jangan menumpuk pengecualian dalam satu baris.
- **Catat tiket** di deskripsi/komentar aturan bila platform mendukung.

**Perintah review read-only:**

```bash
# nftables
sudo nft list ruleset -a

# iptables (legacy)
sudo iptables -S; sudo iptables -vnL --line-numbers

# pfSense/OPNsense (CLI terbatas; gunakan UI untuk audit)
pfctl -sr

# Windows
Get-NetFirewallRule | Where-Object Enabled -eq True |
  Select-Object DisplayName, Direction, Action, Profile
```

## 3. Desain kebijakan

1. **Flow matrix** divalidasi pemilik aplikasi: sumber, tujuan, port, protokol, tujuan bisnis.
2. **Klasifikasi** tiap flow: wajib, opsional, terlarang.
3. **Implementasi** dengan default deny dan logging pada aturan baru.
4. **Verifikasi** dari kedua arah; pastikan yang ditolak benar-benar ditolak.
5. **Dokumentasi** aturan, pemilik, tanggal review.

Egress sering diabaikan. Default deny egress memutus banyak jalur C2 dan eksfiltrasi, tetapi menuntut disiplin proxy/allowlist.

## 4. IDS/IPS

| Aspek | IDS (passive) | IPS (inline) |
|---|---|---|
| Dampak false positive | alert saja | trafik terputus |
| Penempatan | SPAN/TAP | jalur trafik |
| Risiko | buta bila sensor mati | memutus layanan bila salah tuning |
| Kegunaan | forensik, baseline, deteksi | pencegahan aktif |

**Siklus tuning:**

1. Alert masuk → triase: true positive, false positive, atau tidak relevan.
2. Untuk false positive: pahami penyebab (aplikasi sah, signature terlalu luas, enkripsi).
3. Perbaiki dengan suppression **berbatas waktu** atau penyesuaian signature — bukan mematikan rule selamanya.
4. Catat alasan dan tanggal review; alert yang dimatikan tanpa catatan akan hilang konteksnya.
5. Ukur kualitas: rasio FP, alert per hari, waktu triase.

Jangan menilai sensor dari jumlah alert. Sensor yang berisik bukan berarti bekerja lebih baik.

## 5. VPN dan akses remote

- **MFA wajib** untuk semua akses remote; password saja bukan kontrol.
- **Split tunnel** hanya bila ada alasan dan kontrol egress di endpoint.
- **Sesi berbatas waktu** dan pencabutan otomatis untuk akun tidak aktif.
- **Logging** siapa masuk, dari mana, ke aplikasi apa.
- **Pilih ZTNA** bila kebutuhan sebenarnya akses per aplikasi, bukan seluruh jaringan.

## 6. TLS inspection

Inspeksi TLS memberi visibilitas, tetapi:

- memutus end-to-end encryption — pertimbangkan privasi, hukum, dan data sensitif;
- menambah beban dan titik kegagalan;
- memerlukan manajemen sertifikat internal dan pengecualian aplikasi tertentu;
- tidak menyelesaikan masalah bila aplikasi memakai certificate pinning.

Keputusan ini harus tertulis dan disetujui, bukan fitur yang dinyalakan diam-diam.

## 7. WAF

- Tempatkan WAF di depan aplikasi publik yang memang membutuhkannya; ia bukan pengganti patch.
- **Virtual patching** berguna saat patch belum bisa diterapkan, tetapi harus punya tanggal berakhir.
- Tuning WAF mengikuti siklus yang sama dengan IDS: alert → triase → pengecualian sempit → review.
- Uji aturan baru di mode monitor sebelum blocking.
- Detail lifecycle aturan ada di `app-data-protection.md`.

## 8. DDoS dan pembatasan laju

- Bedakan **volumetric** (butuh mitigasi penyedia/upstream), **protocol** (SYN flood, fragment), dan **application-layer** (request flood).
- Rate limit di titik masuk, prioritaskan layanan kritis.
- Siapkan runbook: siapa menghubungi penyedia, ambang eskalasi, cara mengaktifkan mitigasi.
- Jangan mengandalkan firewall tunggal untuk serangan volumetrik besar.

## 9. Verifikasi dan rollback

Setiap perubahan perimeter harus punya:

1. **Window** dan pemberitahuan ke pemilik layanan.
2. **Rollback script/perintah** yang sudah diuji, bukan ditulis saat panik.
3. **Cara verifikasi** — koneksi yang seharusnya jalan dan yang seharusnya ditolak.
4. **Pemantauan** setelah perubahan (log, alert, metrik).
5. **Catatan** perubahan, alasan, dan hasil verifikasi.

## 10. Kesalahan umum

1. **Membuka akses "sementara" tanpa tanggal pencabutan.**
2. **Mematikan signature** karena satu false positive, tanpa pengecualian sempit.
3. **Menganggap IPS aman** tanpa menguji dampak false positive ke aplikasi.
4. **Egress terbuka** karena "dibutuhkan aplikasi" tanpa inventaris tujuan.
5. **TLS inspection** dinyalakan tanpa persetujuan dan tanpa pengecualian.
6. **Perubahan tanpa rollback** karena "cuma satu baris".
7. **Mengandalkan IP allowlist** untuk layanan yang bisa diakses dari jaringan bersama.

## Best Practices

- Tulis aturan sebagai kebijakan: sumber, tujuan, layanan, pemilik, masa berlaku.
- Uji penolakan, bukan hanya keberhasilan.
- Tuning dengan pengecualian sempit dan tanggal review.
- Perlakukan TLS inspection dan WAF blocking sebagai keputusan tertulis.
- Siapkan rollback sebelum menyentuh konfigurasi.
