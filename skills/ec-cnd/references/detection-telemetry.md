---
name: "Detection and Telemetry — Trafik, Log, Baseline"
description: "Membangun deteksi dari telemetri: penempatan sensor, pilihan pcap/flow/metadata, sumber log yang bernilai, baseline trafik, alur analisis Wireshark, sentralisasi log dan waktu, serta pengukuran cakupan deteksi."
tags: [detection, telemetry, pcap, netflow, zeek, suricata, wireshark, logging, siem, baseline, coverage]
---

# Detection and Telemetry — Trafik, Log, Baseline

Deteksi dimulai dari pertanyaan: **normal seperti apa?** Tanpa baseline, alert hanyalah selisih yang tidak bisa dijelaskan. Defender yang baik menghabiskan lebih banyak waktu memahami normal daripada menambah signature.

## 1. Penempatan sensor

| Titik | Melihat | Catatan |
|---|---|---|
| Perimeter (north-south) | trafik masuk/keluar | wajib; titik paling banyak sinyal |
| Antar-segmen (east-west) | pergerakan lateral | butuh TAP/SPAN di titik kunci, bukan semua |
| Endpoint | proses, koneksi, file | EDR; detail tinggi, biaya lisensi |
| Cloud flow log | koneksi VPC | murah, tanpa payload |
| DNS | pola resolusi | sinyal C2 dan tunneling yang kuat |

Jangan memasang sensor di semua titik tanpa kemampuan menganalisis. Sensor yang tidak dibaca sama dengan tidak ada.

## 2. Pilihan data

- **Full packet capture (pcap)** — forensik dan analisis protokol; mahal dalam storage.
- **Flow (NetFlow/IPFIX/sFlow)** — metadata koneksi; murah, bagus untuk baseline dan anomali volume.
- **Zeek logs** — ringkasan sesi, DNS, HTTP, TLS, file; kaya konteks dengan storage wajar.
- **Alert** — keluaran IDS/IPS/EDR; titik awal triase, bukan kebenaran final.

Kombinasi lazim: flow untuk gambaran besar, Zeek untuk konteks, pcap selektif untuk verifikasi.

## 3. Baseline

Bangun baseline untuk:

- volume per jam/hari dan pola musiman;
- port dan protokol yang wajar per segmen;
- top talkers dan pasangan komunikasi tetap;
- pola DNS (domain, volume, NXDOMAIN);
- jam kerja dan jadwal backup;
- perubahan yang dijadwalkan (deployment, patch).

Baseline bukan angka statis; ia bergerak. Catat perubahan yang disengaja agar tidak menjadi alert palsu.

## 4. Alur analisis trafik

1. **Tentukan pertanyaan** — apa yang ingin dibuktikan? ("Apakah host ini menghubungi C2?")
2. **Pilih data** — flow dulu, lalu pcap pada host/waktu spesifik.
3. **Filter** — persempit ke IP/port/waktu; hindari capture ulang tanpa batas.
4. **Periksa konteks** — proses apa, user siapa, jadwal apa.
5. **Simpulkan dengan derajat keyakinan** — bukan "pasti", tapi "konsisten dengan".
6. **Simpan bukti** — pcap/flow/log dengan timestamp dan hash bila untuk forensik.

Contoh filter Wireshark yang sering dipakai:

```
ip.addr == 10.10.5.23 && tcp.port == 443
dns.qry.name contains "example"
tls.handshake.extensions_server_name contains "domain"
http.request.method == "POST"
```

## 5. Sumber log

| Sumber | Nilai utama |
|---|---|
| Firewall | koneksi ditolak/diizinkan, NAT, rule hit |
| Router/switch | perubahan konfigurasi, login, interface down |
| Proxy/web gateway | URL, kategori, upload, user-agent |
| DNS | query, NXDOMAIN, volume per host |
| Autentikasi (AD/LDAP/SSO) | login gagal, akun baru, perubahan grup |
| Endpoint/EDR | proses, command line, koneksi, file |
| Aplikasi/web server | error, 4xx/5xx, pola request |
| Cloud audit | perubahan IAM, konfigurasi, eksposur |

Prioritaskan sumber yang menjawab pertanyaan investigasi, bukan yang paling mudah dikumpulkan.

## 6. Sentralisasi dan waktu

- **NTP** di semua perangkat; korelasi lintas sumber tanpa jam yang sama adalah tebakan.
- **Format dan parsing** konsisten; simpan log mentah, jangan hanya hasil parsing.
- **Retensi** memadai untuk dwell time yang realistis; 7 hari hampir selalu kurang.
- **Akses** ke log dibatasi dan diaudit; penyerang yang bisa menghapus log mematikan deteksi.
- **Redaksi** data sensitif sesuai kebijakan privasi.

## 7. SIEM dan korelasi

- **Parsing** yang benar lebih penting daripada rule yang banyak.
- **Enrichment** (aset, pemilik, GeoIP, threat intel) mengubah alert menjadi keputusan.
- **Korelasi** untuk pola lintas sumber (login gagal → sukses → akses file).
- **Tuning** berkelanjutan: alert yang tidak pernah ditindaklanjuti harus diperbaiki atau dihapus.
- **Runbook** per alert: siapa pemilik, langkah triase, kapan eskalasi.

## 8. Cakupan deteksi

- Petakan deteksi ke taktik/teknik (MITRE ATT&CK) untuk melihat lubang.
- Ukur **kualitas**, bukan jumlah: rasio false positive, waktu triase, waktu deteksi.
- Uji deteksi dengan simulasi terkontrol (atomic testing/purple team) dan catat hasilnya.
- Perlakukan cakupan sebagai peta hidup; teknik baru menuntut deteksi baru.

## 9. Kesalahan umum

1. **Capture semuanya tanpa rencana retensi** — storage penuh, analisis lumpuh.
2. **Alert tanpa pemilik** — menumpuk sampai diabaikan.
3. **Baseline tidak diperbarui** setelah perubahan besar.
4. **Log hanya di host** yang bisa dihapus penyerang.
5. **Sensor mati tidak terdeteksi** — perlu health check.
6. **Mengukur deteksi dari jumlah alert**, bukan dari kualitas keputusan.
7. **Pcap berisi data sensitif** disimpan tanpa kontrol akses.

## Best Practices

- Mulai dari pertanyaan investigasi, bukan dari alat.
- Bangun baseline sebelum menambah signature.
- Simpan log mentah dan sinkronkan waktu.
- Beri setiap alert pemilik dan runbook.
- Uji deteksi secara berkala, lalu perbaiki lubang yang terbukti.
