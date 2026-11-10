---
name: "Double Pivoting & Reporting — Kedalaman yang Dibuktikan"
description: "Metodologi double pivoting (dua hop, host dual-homed, Ligolo-ng/Chisel/SSH) dan penyusunan laporan pengujian kelas klien: peta serangan, bukti yang reproducible, CVSS/CWE, remediasi, dan aturan redaksi."
tags: [pivoting, double-pivot, ligolo-ng, chisel, reporting, cvss, evidence]
---

# Double Pivoting & Reporting

Pivoting menghasilkan akses; laporan membuat akses itu bernilai. Engagement yang berhenti di shell tanpa deliverable hanya menghasilkan risiko tanpa perbaikan.

## 1. Arsitektur pivot

```
Attacker → Pivot 1 (DMZ host) → Segmen A → Host dual-homed → Segmen B → Target
```

- **Pivot 1** adalah host yang sudah dikuasai di perimeter atau DMZ.
- **Host dual-homed** punya dua antarmuka; ia menjadi jembatan ke segmen B.
- **Target** hanya reachable setelah dua hop — inilah yang membedakan pengujian dangkal dari pengujian berlapis.

## 2. Langkah kerja

1. **Dapatkan agent di pivot 1** — shell, binary upload, atau eksekusi perintah.
2. **Peta antarmuka** — `ip a`, `ip route`, `arp -a`; cari subnet kedua.
3. **Buktikan reachability** — `nc -vz`, `curl`, `nmap -sT` dari pivot.
4. **Pasang tunnel** — pilih tool sesuai egress dan kebutuhan tool berikutnya.
5. **Daftarkan route** — di sisi attacker, arahkan subnet B ke interface tunnel.
6. **Scan dari attacker** — tool native berjalan seolah target langsung terhubung.
7. **Ulangi untuk hop berikutnya** — setiap host baru = pemeriksaan antarmuka baru.

### Ligolo-ng (TUN)

```bash
# Attacker: proxy
ligolo-proxy -selfcert -laddr 0.0.0.0:11601

# Pivot: agent
./agent -connect 10.10.14.5:11601 -ignore-cert

# Di konsol proxy
session          # pilih sesi
iface create --tun ligolo0
iface add -a 10.10.20.0/24 -t ligolo0
```

Kelebihan: tool native (nmap `-sS`, Responder, Impacket) langsung jalan tanpa proxy.

### Chisel (HTTP)

```bash
# Pivot
./chisel client https://attacker:8080 R:socks

# Attacker
./chisel server -p 8080 --reverse
# Tool harus proxy-aware: proxychains4 nmap -sT ...
```

### SSH

```bash
ssh -D 1080 user@pivot          # SOCKS dinamis
ssh -L 445:target:445 user@pivot # port forward
ssh -R 8080:localhost:8080 user@pivot # reverse
```

## 3. Peta serangan

Artefak yang wajib diperbarui setiap hop:

| Hop | Host | Segmen | Akses | Waktu | Berikutnya |
|---|---|---|---|---|---|
| 1 | web01 | 10.10.10.0/24 | www-data | 10:42 | 10.10.20.0/24 |
| 2 | fs01 | 10.10.20.0/24 | local admin | 11:15 | DC 10.10.20.9 |

Peta ini menjadi diagram di laporan dan dasar klaim "seberapa dalam pengujian mencapai".

## 4. Laporan

### Struktur

1. **Cover dan distribusi** — klasifikasi, penerima, versi, tanggal.
2. **Executive summary** — satu halaman: risiko utama, jalur yang berhasil, prioritas perbaikan.
3. **Metodologi** — standar (PTES, OWASP WSTG, NIST SP 800-115), fase, batasan, asumsi.
4. **Peta serangan** — diagram hop dan trust boundary.
5. **Temuan** — per temuan: judul, severity, CVSS 3.1, CWE, bukti, dampak, remediasi.
6. **Rekomendasi** — prioritas risiko, bukan urutan penemuan.
7. **Lampiran** — command log, daftar host, artefak tambahan.

### Bukti yang diterima

- Shell: `whoami`, `id`, `hostname`, `ip a`/`ipconfig` dalam satu frame.
- Objective: file, data, atau kontrol yang bisa ditunjukkan.
- Pivot: `ip route` sebelum dan sesudah, plus bukti reachability.
- Waktu: timestamp terlihat atau dicatat di log.

Screenshot tanpa identitas host tidak membuktikan apa pun dan akan ditolak reviewer.

### Kualitas temuan

| Elemen | Standar |
|---|---|
| Severity | CVSS 3.1 vector, konsisten dengan dampak |
| Klasifikasi | CWE yang tepat |
| Bukti | Request/response atau command + output |
| Reproduksi | Langkah yang bisa diulang engineer lain |
| Remediasi | Spesifik, bisa dieksekusi, bukan "perbaiki konfigurasi" |
| Redaksi | Kredensial, PII, dan data pelanggan disamarkan |

## 5. Jebakan

1. **Proxy-unaware tools** — `nmap -sS` lewat SOCKS gagal; gunakan TUN atau `-sT`.
2. **Route tidak didaftarkan** — tunnel naik tapi scan tetap ke internet.
3. **DNS internal** — resolver tidak ikut tunnel; arahkan eksplisit.
4. **Bukti direkonstruksi** — screenshot diambil setelah sesi berakhir, konteks hilang.
5. **Laporan tanpa dampak bisnis** — temuan teknis tanpa terjemahan risiko sulit diprioritaskan klien.
6. **Artefak tertinggal** — agent, file, atau akun tidak dibersihkan; ini temuan baru.

## 6. Best Practices

- Peta pivot diperbarui saat kejadian, bukan setelah engagement.
- Bukti diambil saat akses masih hidup.
- Setiap klaim kedalaman harus punya bukti reachability.
- Tulis laporan paralel dengan eksekusi; rekonstruksi selalu kehilangan detail.
- Uji buka PDF/deliverable sebelum dikirim; pastikan redaksi benar.
