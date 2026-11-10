---
name: "Network Architecture — Zonasi dan Segmentasi"
description: "Desain zonasi dan segmentasi jaringan dari sudut pandang defender: trust zone, DMZ, pilihan level segmentasi, kontrol east-west, NAC, Zero Trust/SDP, hardening routing/switching, dan cara membuktikan segmentasi benar-benar bekerja."
tags: [segmentation, dmz, trust-zone, vlan, nac, zero-trust, sdp, routing, switching, ipv6, egress]
---

# Network Architecture — Zonasi dan Segmentasi

Segmentasi bukan daftar VLAN. Segmentasi adalah **kebijakan tentang siapa boleh berbicara dengan siapa**, yang ditegakkan di titik kontrol. VLAN tanpa aturan antar-VLAN hanyalah jaringan datar dengan nama baru.

## 1. Trust zone

| Zone | Isi khas | Aturan dasar |
|---|---|---|
| Internet / untrusted | semua yang tidak dikenal | tidak ada akses masuk kecuali layanan publik |
| DMZ | reverse proxy, mail gateway, jump host | satu arah ke internal, tidak pernah sebaliknya |
| User / workstation | endpoint pengguna | tidak boleh langsung ke server manajemen |
| Server / data | aplikasi, database, file | hanya port aplikasi dari zone yang berhak |
| Management | jump host, monitoring, backup | hanya dari workstation admin, sering out-of-band |
| OT / ICS | PLC, HMI, historian | read-only dari IT, perubahan lewat prosedur |
| Guest | perangkat tamu | internet saja, terisolasi penuh |

Zone adalah keputusan bisnis dan teknis sekaligus. Pemilik aset harus menyetujui isi dan aturan tiap zone.

## 2. Prinsip DMZ

- **Satu arah.** Koneksi dimulai dari luar ke DMZ; DMZ ke internal hanya untuk tujuan spesifik dan tercatat.
- **Tidak ada penyimpanan data sensitif** di DMZ. Bila ada, perlakukan sebagai zona berisiko tinggi.
- **Bukan tempat tinggal.** DMZ untuk layanan yang memang harus terpapar, bukan untuk semua aplikasi.
- **Logging penuh.** Trafik masuk-keluar DMZ adalah salah satu sumber sinyal terbaik yang dimiliki defender.

## 3. Pilihan level segmentasi

| Level | Kekuatan | Batas |
|---|---|---|
| VLAN / subnet | murah, cepat, dipahami tim jaringan | hanya efektif bila ada ACL/firewall antar-VLAN |
| Firewall zone | kebijakan eksplisit, logging, NAT | biaya, kompleksitas, sering jadi bottleneck |
| Microsegmentation | granular per workload, mengurangi lateral | operasional berat, butuh inventaris akurat |
| Host firewall | lokal, tetap jalan saat jaringan gagal | dikelola per host, mudah menyimpang |

Aturan praktis: pilih level termurah yang menutup **akar masalah**, lalu pastikan ada kontrol penegak. Dua VLAN yang saling terbuka bukan segmentasi.

## 4. Kontrol east-west

Sebagian besar pergerakan lateral terjadi di dalam perimeter. Yang perlu dibatasi:

- workstation → workstation (SMB, RDP, WinRM),
- workstation → server database,
- server → server lintas aplikasi tanpa kebutuhan,
- management plane (SSH, RDP, API) dari user zone,
- backup dan monitoring (sering diberi akses luas "karena perlu").

Mulai dari peta flow nyata, bukan dari daftar keinginan. Flow matrix yang divalidasi pemilik aplikasi adalah dokumen kontrol, bukan sekadar diagram.

## 5. NAC dan 802.1X

- **802.1X** untuk perangkat yang mendukung suplikasi; MAB untuk yang tidak — dengan kesadaran bahwa MAB mudah dipalsukan.
- **Posture check** hanya berguna bila ada konsekuensi (VLAN remediasi, bukan penolakan total).
- **Guest dan BYOD** di zone terpisah, tanpa akses ke internal.
- **Port tidak terpakai** di-shutdown, bukan sekadar diberi VLAN default.

## 6. Zero Trust dan SDP

Zero Trust bukan produk. Yang bisa diterapkan defender:

- identitas sebagai kontrol utama, bukan lokasi jaringan;
- akses per aplikasi, bukan per jaringan;
- verifikasi berkelanjutan (perangkat, posture, konteks);
- log akses yang bisa dikorelasikan ke identitas.

Software-Defined Perimeter (SDP) membantu menyembunyikan layanan dari pemindaian, tetapi tidak menggantikan patch, hardening, dan segmentasi internal. Hindari mengklaim "Zero Trust selesai" karena satu gateway terpasang.

## 7. Hardening routing dan switching

**Control plane:** autentikasi routing (OSPF MD5/SHA, BGP TTL security dan prefix filter), manajemen akses ke perangkat (SSH, ACL manajemen, TACACS/RADIUS), nonaktifkan layanan tidak perlu (CDP/LLDP ke luar, HTTP, Telnet).

**Data plane / L2:** DHCP snooping, dynamic ARP inspection, port security, BPDU guard, storm control, native VLAN terpisah, trunk hanya ke port yang membutuhkan, disabled unused ports.

**IPv6:** jangan diabaikan. Bila tidak dipakai, nonaktifkan atau filter dengan sadar; bila dipakai, perlakukan sebagai zone penuh dengan aturan sendiri.

**Contoh verifikasi read-only:**

```bash
# Linux router/host
ip -6 addr; ip -6 route; sysctl net.ipv6.conf.all.disable_ipv6

# Switch (vendor CLI, contoh umum)
show ip arp inspection; show ip dhcp snooping; show port-security
show spanning-tree summary
```

## 8. DNS dan egress

- **DNS internal** terpisah dari resolver publik; forwarder dikendalikan.
- **Egress filtering** default deny: port 80/443 ke proxy, DNS ke resolver internal, NTP ke sumber internal.
- **DNS over HTTPS** dari endpoint bisa melewati kontrol — putuskan secara sadar, jangan dibiarkan.
- **Proxy** memberi visibilitas dan kategori; TLS inspection punya konsekuensi (lihat `perimeter-controls.md`).

## 9. Remote access

- VPN dengan MFA, bukan password saja.
- Split tunnel hanya bila ada alasan dan kontrol; full tunnel untuk perangkat yang menangani data sensitif.
- Sesi berbatas waktu, logging akses, dan pencabutan otomatis untuk akun yang tidak aktif.
- Pilih ZTNA bila kebutuhan utamanya akses per aplikasi, bukan akses ke seluruh jaringan.

## 10. Membuktikan segmentasi bekerja

Segmentasi yang tidak diuji adalah asumsi. Bukti minimum:

1. **Peta aturan** — siapa boleh ke siapa, port apa, dari dokumen kontrol.
2. **Uji konektivitas** dari dua arah, termasuk yang seharusnya ditolak.
3. **Uji dari host yang dikompromikan** — apakah lateral path tertutup.
4. **Log** — trafik yang ditolak tercatat di titik kontrol.
5. **Review berkala** — aturan bertambah seiring waktu; segmentasi perlu dirawat.

## Best Practices

- Mulai dari aset dan pemilik, bukan dari alat.
- Tulis aturan sebagai kebijakan yang bisa diaudit, bukan sebagai konfigurasi yang hanya dipahami satu orang.
- Uji penolakan, bukan hanya keberhasilan koneksi.
- Perlakukan management plane sebagai zone tersendiri.
- Dokumentasikan pengecualian beserta tanggal kedaluwarsanya.
