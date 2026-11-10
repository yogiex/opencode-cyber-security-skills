---
name: "Decision Trees — Pohon Keputusan Lapangan"
description: "Pohon keputusan operasional untuk situasi yang paling sering ditemui: foothold Windows dan Linux, web ke RCE, pemilihan jalur AD, eskalasi versus lateral, pemilihan tunnel pivot, go/no-go binary exploitation, dan pendekatan OT."
tags: [decision-trees, windows, linux, web, active-directory, pivoting, binary, ot]
---

# Decision Trees

Pohon ini bukan algoritma kaku. Fungsinya mempercepat keputusan saat informasi belum lengkap, dan mencegah dua kesalahan umum: berhenti terlalu awal dan melangkah terlalu jauh tanpa bukti.

## 1. Foothold Windows — 30 menit berikutnya

```
Shell/user di Windows
├─ Punya kredensial domain yang valid?
│  ├─ ya → BloodHound (jalur) → Kerberoast/ADCS/share → cari DA path
│  └─ tidak → cari kredensial lokal: SAM/LSA, GPP, config, history, browser
├─ Local admin?
│  ├─ ya → dump LSA/SAM, cek tiket, cek delegasi, siapkan pivot
│  └─ tidak → service config, unquoted path, token, scheduled task,
│             AlwaysInstallElevated, writable service binary
├─ Domain controller reachable dan SMB signing mati?
│  └─ ya → relay/coercion (butuh izin RoE) → LDAP → RBCD
└─ Tidak ada jalur jelas?
   └─ kembali ke enumerasi: share, sesi, proses, ARP, DNS, trust
```

## 2. Foothold Linux — urutan yang benar

```
Shell user di Linux
├─ sudo -l          → NOPASSWD/wildcard → GTFOBins
├─ SUID/capabilities → escape atau setuid
├─ cron/timer        → script writable atau PATH
├─ docker/lxd group  → socket atau mount host
├─ kredensial file   → ssh key, .env, config, history
├─ kernel versi      → CVE (pilihan terakhir, risiko panic)
└─ container?        → cek socket, privileged, hostPath, cgroup
```

Aturan: konfigurasi sebelum CVE. Kernel exploit hanya setelah jalur lain habis dan ada rencana rollback.

## 3. Web menuju RCE

```
Ada permukaan menulis/mengeksekusi?
├─ Upload        → bypass ekstensi/MIME/magic → webshell → cek eksekusi
├─ LFI           → log poisoning / session / filter chain → RCE
├─ SQLi (FILE)   → INTO OUTFILE (MySQL) atau xp_cmdshell (MSSQL)
├─ SSTI          → engine-specific payload → RCE
├─ Deserialisasi → gadget chain sesuai library
├─ CMDi          → perintah identitas dulu, shell kemudian
├─ SSRF          → layanan internal tanpa auth (Redis/ES/Docker API)
└─ Admin panel   → plugin/template upload, backup restore, DB console
```

Jika tidak ada yang bisa dieksekusi: cari kredensial, token, atau akses ke host lain — bukan memaksa RCE.

## 4. Memilih jalur AD

```
Punya kredensial domain?
├─ ya → BloodHound.shortest_paths(owned, DA)
│      → pilih jalur dengan langkah paling sedikit DAN noise paling rendah
│      → kerberoast/AS-REP/ADCS/delegasi/ACL abuse
└─ tidak → relay, coercion, LLMNR/NBT-NS, kredensial di share
Domain dominance sudah tercapai?
├─ ya → berhenti menambah akses; ambil bukti dan laporan
└─ tidak → jangan DCSync dulu; cari jalur yang menuju DA
```

Urutan biaya: ACL abuse < ADCS < Kerberoast < delegation < relay < DCSync.

## 5. Eskalasi atau lateral?

```
Punya akses ke host A
├─ Akses A bisa membuka host B yang lebih dekat ke objective?
│  └─ ya → lateral dulu; root di A tidak menambah nilai
├─ Akses A dibutuhkan untuk pivot?
│  └─ ya → eskalasi secukupnya, lalu pivot
└─ A adalah tujuan akhir?
   └─ ya → eskalasi penuh, ambil bukti, berhenti
```

Lateral yang murah sering lebih bernilai daripada root lokal yang mahal.

## 6. Memilih tunnel

```
Butuh tool native (nmap -sS, Responder, Impacket)?
├─ ya → Ligolo-ng (TUN)
└─ tidak
   ├─ Egress hanya HTTP/HTTPS? → Chisel (SOCKS)
   ├─ Ada SSH? → ssh -D / -L / -R
   ├─ Satu port saja? → socat
   └─ Butuh routing transparan tanpa agent? → sshuttle
```

Jika tunnel naik tapi tidak ada trafik: cek route di sisi attacker, firewall egress, dan DNS.

## 7. Binary exploitation: go / no-go

```
Ada crash yang bisa dikontrol?
├─ ya
│  ├─ Offset terkontrol? → lanjut
│  ├─ Proteksi (ASLR/NX/CFG)? → butuh leak atau ROP
│  └─ Ada salinan/replika untuk uji? → uji dulu
└─ tidak → hentikan; cari jalur aplikasi, konfigurasi, atau kredensial
```

No-go jika: tidak ada replika, service produksi tanpa izin crash, atau waktu tersisa lebih berharga untuk jalur lain.

## 8. Pendekatan OT

```
Ada segment OT dalam scope?
├─ ya → konfirmasi izin read/write dan pendamping operator
│      → enumerasi read-only: identitas PLC, register, protokol
│      → pivot lewat DMZ industri (L3.5), bukan langsung L1
│      → write hanya dengan prosedur rollback
└─ tidak → jangan sentuh; catat sebagai out of scope
```

Read-only adalah default. Write adalah keputusan kontrak.

## 9. Kapan berhenti mengeksploitasi

- Objective kontrak tercapai dan bukti lengkap.
- Jalur berikutnya menambah noise tanpa menambah kedalaman.
- Risiko produksi melebihi nilai temuan.
- Tiga hipotesis berturut-turut gagal — kembali ke enumerasi.
- Window RoE berakhir.

## Best Practices

- Pilih cabang berdasarkan bukti, bukan harapan.
- Catat alasan setiap perpindahan cabang; itu yang membuat laporan bisa dipertanggungjawabkan.
- Jika pohon tidak cocok dengan kenyataan, percayai kenyataan dan perbarui pohonnya.
- Jangan mengeksploitasi hanya karena cabangnya tersedia.
