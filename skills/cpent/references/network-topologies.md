---
name: "Network Topologies — Arketipe Segmen dan Pemetaan Kedalaman"
description: "Arketipe jaringan yang dihadapi operator CPENT: flat internal, single pivot, double pivot berlapis, DMZ, hybrid cloud, dan zona IoT/OT — plus prosedur memetakan jalur terdalam, membuktikan reachability, dan memilih tunnel yang tepat."
tags: [topology, pivoting, segmentation, dual-homed, dmz, ot-segment, reachability]
---

# Network Topologies

Serangan berlapis adalah masalah topologi, bukan masalah tool. Sebelum memilih Ligolo-ng, Chisel, atau SSH, jawab dulu: host ini punya antarmuka apa, route ke mana, dan segmen mana yang hanya bisa dicapai dari sini.

## 1. Arketipe segmen

| Arketipe | Ciri | Titik masuk umum | Objektif khas |
|---|---|---|---|
| Flat internal | Semua host saling reachable | Satu workstation terkompromi | Domain dominance, data store |
| Single pivot | Entry di DMZ, internal tersegmentasi | Web server dual-homed | Server aplikasi, database |
| Double pivot | Dua lapis; target hanya reachable dari hop kedua | Host dual-homed di segmen A | Segmen B yang terisolasi |
| DMZ berlapis | Reverse proxy → app → data | Proxy atau app server | Layanan internal |
| Hybrid cloud | VPC/VNet, peering, metadata service | Workload dengan IAM role | Bucket, secret, kontrol plane |
| Zona IoT/OT | Perangkat tidak dikelola, protokol industri | Web interface perangkat | PLC, HMI, historian |

## 2. Discovery setiap kali mendapat host baru

Urutan ini dijalankan sebelum eksploitasi berikutnya:

```bash
# Identitas dan posisi jaringan
hostname; whoami; id
ip a; ip route
cat /etc/resolv.conf
arp -a
cat /etc/hosts

# Layanan dan koneksi yang sudah ada
ss -tunlp
ps aux | head -50

# Windows
ipconfig /all
route print
arp -a
netstat -ano
Get-SmbShare
```

Yang dicari: antarmuka kedua, route default tambahan, gateway internal, DNS internal, host di ARP, dan share yang menandakan peran server.

## 3. Mendeteksi host dual-homed

Host dual-homed adalah jembatan alami ke segmen berikutnya — dan alasan double pivot mungkin.

- Bandingkan jumlah `ip a` dengan route: dua subnet berbeda = kandidat pivot.
- Cek `ip route get <ip>` untuk memastikan paket keluar lewat antarmuka mana.
- Windows: `Get-NetIPAddress`, `Get-NetRoute`; container: `docker network ls`.
- Host dengan dua NIC sering VM hypervisor, jump host, atau appliance — periksa proses dan service-nya.

## 4. Membuktikan reachability

Jangan menganggap reachable hanya karena routing ada. Buktikan dari host pivot:

```bash
# TCP connect (aman melewati tunnel yang tidak mendukung raw socket)
nc -vz -w 3 10.10.20.5 445
curl -sk -o /dev/null -w '%{http_code}\n' https://10.10.20.5/

# Scan yang tidak butuh raw socket
nmap -Pn -sT -p 22,80,443,445,3389 10.10.20.0/24
```

Catat bukti reachability per segmen; itu yang membedakan "mungkin bisa" dari "terbukti bisa".

## 5. Memilih tunnel

| Tool | Kapan dipakai | Catatan |
|---|---|---|
| Ligolo-ng | Butuh tool native (nmap -sS, Responder, Impacket) | TUN interface; agent single binary |
| Chisel | Egress hanya HTTP/HTTPS | SOCKS5; tool harus proxy-aware |
| SSH `-L/-R/-D` | Ada SSH di pivot | Paling sederhana, mudah diaudit |
| socat | Port forward satu port | Tidak cocok untuk scan luas |
| sshuttle | Butuh routing transparan tanpa agent | Perlu Python di pivot |

Aturan praktis: kalau tool berikutnya tidak proxy-aware, pakai tunnel yang memberi interface (Ligolo-ng), bukan SOCKS.

## 6. Peta kedalaman

Simpan artefak ini dan perbarui setiap hop:

| Hop | Host | Segmen | Akses | Bukti | Berikutnya |
|---|---|---|---|---|---|
| 0 | attacker | — | — | — | DMZ |
| 1 | web01 | 10.10.10.0/24 | www-data | `id`, `ip a` | subnet 10.10.20.0/24 |
| 2 | fs01 | 10.10.20.0/24 | local admin | share list | domain controller |

Peta ini menjadi bahan diagram serangan di laporan dan mencegah pekerjaan diulang.

## 7. Zona OT dan model Purdue

Segmen industri biasanya mengikuti pembagian level:

| Level | Isi | Aturan uji |
|---|---|---|
| L0 | Sensor, aktuator | Tidak disentuh |
| L1 | PLC, RTU | Read-only kecuali diizinkan tertulis |
| L2 | HMI, SCADA server | Read-only default |
| L3 | Historian, engineering workstation | Uji terkendali, dampingi operator |
| L3.5 | DMZ industri | Titik masuk paling aman |
| L4 | Enterprise | Sama seperti jaringan korporat |

Melintasi level adalah perubahan risiko, bukan pencapaian teknis. Setiap perpindahan level butuh persetujuan eksplisit di RoE.

## 8. Jebakan

1. **DNS lewat pivot** — tool resolving nama internal gagal karena resolver tidak ikut di-tunnel; arahkan ke DNS internal atau pakai IP.
2. **IPv6** — segmen "terisolasi" kadang punya IPv6 link-local atau ULA yang reachable.
3. **Egress stateful** — koneksi keluar dari pivot boleh, koneksi masuk tidak; pilih arah tunnel sesuai itu.
4. **Double NAT** — dua lapis NAT membuat agent tidak bisa callback; siapkan reverse tunnel dari dalam.
5. **Host dual-homed palsu** — dua antarmuka tapi satu tanpa route; verifikasi dengan `ip route get`.
6. **Proxy environment** — variabel `http_proxy` di host pivot bisa membelokkan tool tanpa disadari.

## 9. Best Practices

- Peta topologi sebelum mengeksploitasi; satu host baru = satu pembaruan peta.
- Buktikan reachability dengan paket nyata, bukan asumsi route.
- Catat hop dan trust boundary di laporan; kedalaman adalah temuan.
- Di OT, default read-only; write adalah keputusan kontrak, bukan keputusan teknis.
- Bersihkan tunnel dan agent di akhir engagement; dokumentasikan yang tertinggal.
