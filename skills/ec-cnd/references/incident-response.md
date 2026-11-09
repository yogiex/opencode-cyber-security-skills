---
name: "Incident Response — First Responder Tingkat Jaringan"
description: "Peran defender sebagai first responder jaringan: urutan preservasi bukti, pilihan containment beserta trade-off ketersediaan, paket serah-terima ke tim IR/forensik, tindakan cepat per jenis insiden, komunikasi, serta dasar business continuity dan disaster recovery."
tags: [incident-response, first-responder, containment, evidence, handoff, bcp, drp, rto, rpo, crisis]
---

# Incident Response — First Responder Tingkat Jaringan

Defender bukan incident commander dan bukan analis forensik. Perannya: **mengenali, menahan penyebaran, menjaga bukti, dan menyerahkan dengan konteks lengkap**. Untuk lifecycle penuh dan eradication, rujuk `ec-ecih`; untuk forensik host mendalam, rujuk `offsec-ir-200`.

## 1. Batas peran

| Defender melakukan | Defender tidak melakukan |
|---|---|
| identifikasi dan klasifikasi awal | memutuskan strategi eradikasi organisasi |
| containment di layer jaringan | akuisisi memori/disk mendalam |
| preservasi bukti jaringan | analisis malware lanjutan |
| komunikasi teknis ke tim IR | komunikasi hukum/korporat |
| serah-terima dengan paket bukti | menutup insiden tanpa evaluasi |

## 2. Urutan preservasi (volatile lebih dulu)

Sebelum menyentuh host atau memutus koneksi, ambil yang paling cepat hilang:

1. **Sesi aktif** — `ss -tunap`, `netstat -ano`, koneksi EDR, tabel NAT.
2. **ARP dan neighbor** — `ip neigh`, `arp -a`.
3. **Routing dan firewall state** — `ip r`, `nft list ruleset`, conntrack bila ada.
4. **Log volatil** — auth, firewall, DNS, proxy (sebelum rotasi).
5. **pcap/flow** — rekam bila trafik masih berjalan dan penyimpanan memungkinkan.
6. **Konfigurasi perangkat** — backup sebelum diubah.

Catat waktu (UTC), host, dan siapa yang melakukan. Bukti tanpa metadata adalah klaim tanpa dasar.

## 3. Pilihan containment

| Tindakan | Efek | Trade-off |
|---|---|---|
| ACL block src/dst | cepat, sempit | butuh tahu alamat yang benar; bisa dilewati jalur lain |
| Shutdown port switch | memutus host | memutus semua layanan host itu |
| VLAN karantina | isolasi terkelola | butuh konfigurasi awal; host tetap hidup |
| DNS sinkhole | memutus resolusi C2 | penyerang bisa memakai IP langsung |
| Disable akun | memutus akses identitas | bisa memicu lockout layanan |
| EDR isolate | isolasi endpoint | bergantung agen; butuh lisensi/kebijakan |
| Blokir domain/IP di proxy/firewall | cepat, luas | bisa berdampak ke pengguna sah |

Aturan: pilih tindakan dengan **blast radius terkecil** yang menghentikan penyebaran. Setiap containment punya konsekuensi ketersediaan — keputusan itu milik pemilik layanan, bukan defender sendirian.

## 4. Kapan containment mendesak

- penyebaran aktif (worm, ransomware, lateral movement),
- eksfiltrasi data berjalan,
- kendali C2 aktif dan penyerang punya akses interaktif,
- risiko fisik (OT/ICS) atau keselamatan.

Bila tidak ada penyebaran aktif, **preservasi bukti lebih dulu**, containment terkoordinasi menyusul.

## 5. Tindakan cepat per jenis insiden

**C2 beaconing** — identifikasi proses/pemilik, blokir tujuan di egress, rekam pcap, cek host lain dengan pola serupa, eskalasi untuk forensik.

**Eksfiltrasi data** — identifikasi jalur dan volume, putuskan jalur (bukan host bila masih perlu bukti), simpan flow/pcap, koordinasi dengan pemilik data dan legal.

**Ransomware** — isolasi segmen, matikan akses share, preservasi bukti sebelum pembersihan, prioritaskan pemulihan dari backup yang teruji, jangan membayar tanpa keputusan eksekutif.

**DDoS** — bedakan volumetrik/protokol/aplikasi, aktifkan mitigasi penyedia, rate limit, komunikasi status.

**Insider** — jangan memberi sinyal; koordinasi HR/legal, preservasi log akses, batasi perubahan yang bisa memicu penghapusan bukti.

**Phishing massal** — blokir pengirim/domain, tarik email, reset kredensial yang terekspos, cek login yang berhasil.

## 6. Paket serah-terima

Serahkan ke tim IR/forensik dengan:

1. **Timeline** — apa terjadi kapan, berdasarkan sumber apa.
2. **Bukti** — lokasi, hash, waktu, siapa yang mengambil.
3. **Tindakan yang sudah dilakukan** — containment, perubahan konfigurasi, akun yang dinonaktifkan.
4. **Hipotesis** — apa yang dicurigai dan apa yang belum terbukti.
5. **Kontak dan pemilik layanan** — siapa harus dilibatkan.
6. **Pertanyaan terbuka** — apa yang perlu dijawab forensik.

Serah-terima yang buruk memaksa tim IR mengulang pekerjaan dan kehilangan bukti.

## 7. Komunikasi

- **Satu kanal** untuk koordinasi insiden; jangan tersebar di banyak percakapan.
- **Status berkala** ke pemangku kepentingan: apa yang diketahui, apa yang sedang dilakukan, kapan update berikutnya.
- **Jangan berspekulasi** soal penyebab atau dampak di luar bukti.
- **Catat keputusan** dan alasannya, termasuk yang ditolak.

## 8. Business continuity dan disaster recovery

- **RTO/RPO** disepakati pemilik layanan, bukan ditentukan tim keamanan.
- **Failover** diuji, bukan hanya didokumentasikan.
- **Backup teruji** dan terlindungi dari ransomware (immutable/offline).
- **Krisis** punya struktur: siapa memutuskan, siapa berkomunikasi, apa kriterianya.
- **Tabletop** berkala mengungkap asumsi yang tidak pernah diuji.

## 9. Kesalahan umum

1. **Reboot host** sebelum mengambil bukti.
2. **Memutus semua koneksi** sehingga penyerang tahu dan bukti hilang.
3. **Menghapus malware** sebelum timeline terbentuk.
4. **Containment tanpa persetujuan** yang memutus layanan kritis.
5. **Tidak mencatat perubahan** yang dilakukan saat panik.
6. **Serah-terima tanpa bukti waktu dan hash.** 
7. **Menutup insiden** tanpa memperbaiki kontrol yang gagal.

## Best Practices

- Preservasi dulu, lalu containment sesuai tingkat penyebaran.
- Pilih tindakan dengan blast radius terkecil.
- Catat waktu, sumber, dan pelaku setiap tindakan.
- Serahkan dengan timeline, bukti, dan pertanyaan terbuka.
- Perbaiki kontrol penyebab, bukan hanya gejala.
