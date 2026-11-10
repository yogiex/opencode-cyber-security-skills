---
name: "Tools Matrix — Field Kit Operator"
description: "Perangkat kerja operator penetration testing: tool inti per fase, binary statis untuk diunggah ke target, wordlist, dan aturan pemilihan tool berdasarkan egress, agen, dan tujuan — bukan berdasarkan kebiasaan."
tags: [tools, nmap, burp, sqlmap, metasploit, ligolo-ng, netexec, impacket, wordlists]
---

# Tools Matrix

Tool bukan identitas. Yang menentukan hasil adalah urutan kerja, kualitas enumerasi, dan bukti. Daftar ini adalah field kit minimum yang membuat operator bisa bekerja di lingkungan terbatas.

## 1. Tool inti per fase

| Fase | Tool | Kegunaan |
|---|---|---|
| Recon | nmap, masscan, naabu | Port dan service discovery |
| Recon | ffuf, feroxbuster, gobuster | Direktori dan parameter |
| Recon | subfinder, amass | Subdomain |
| Web | Burp Suite Pro | Proxy, repeater, scanner — prosedur di [burp-workflow.md](./burp-workflow.md) |
| Web | HTTP Request Smuggler, Turbo Intruder | Desync dan uji header/throughput terukur |
| Web | WAFW00F, whatwaf | Identifikasi WAF dan perilakunya |
| Web | Hackvertor | Encoding berlapis saat bypass WAF |
| Web | sqlmap | SQLi (dengan batas risk/thread) |
| Web | nuclei | Template scanning terkurasi |
| AD | netexec, Impacket | SMB/LDAP/WMI/WinRM |
| AD | BloodHound | Peta jalur serangan |
| AD | Certipy | ADCS enumeration dan abuse |
| AD | Responder | NTLM capture |
| Exploit | Metasploit | Framework dan resource script |
| Pivot | Ligolo-ng, Chisel, socat, sshuttle | Tunnel |
| Binary | pwntools, ROPgadget, Ropper, mona | Exploit development |
| Binary | gdb+pwndbg, x64dbg | Debugging |
| Cracking | hashcat, john | Hash offline |
| Wireless | aircrack-ng, hcxdumptool, bettercap | WPA/PMKID |
| OT | nmap NSE, mbpoll, s7-info | Enumerasi protokol |

## 2. Binary statis untuk target

Sering kali target tidak punya compiler atau package manager. Siapkan sebelum bergerak:

- `agent` (Ligolo-ng) — pivot single binary.
- `chisel` — tunnel HTTP.
- `socat` — forward port.
- `nc`/`ncat` — shell dan uji koneksi.
- `tcpdump` — capture di pivot.
- `busybox` — utilitas embedded.
- `python3` statis, `curl`, `wget` — bila target minim.
- `linpeas.sh`, `winPEASx64.exe` — enumerasi lokal.

Cocokkan arsitektur (x86/x64, arm/arm64) dan pastikan binary bisa dieksekusi sebelum diunggah ke banyak host.

## 3. Wordlist

```bash
/usr/share/wordlists/rockyou.txt                     # password
/usr/share/seclists/Discovery/Web-Content/common.txt # direktori
/usr/share/seclists/Usernames/Names/names.txt        # user
/usr/share/seclists/Passwords/Common-Credentials/    # password umum
```

Untuk engagement, wordlist besar memperlambat dan menaikkan noise. Mulai dari daftar kecil yang relevan, lalu perluas bila perlu.

## 4. Memilih tool berdasarkan kendala

| Kendala | Pilihan |
|---|---|
| Egress hanya HTTP/HTTPS | Chisel, ligolo-ng via HTTP, DNS tunnel (jarang) |
| Butuh tool native di segmen | Ligolo-ng TUN |
| Tidak bisa upload binary | Living-off-the-land (PowerShell, certutil, curl) |
| Target Windows tanpa PowerShell | WMI, SMB exec, scheduled task |
| Target embedded | busybox, dropbear, shell bawaan |
| OT | Tool read-only bawaan protokol |

## 5. Higiene tool

- Simpan tool di direktori kerja per engagement; jangan mencampur bukti antar klien.
- Catat versi tool di laporan bila hasilnya dipakai sebagai bukti.
- Bersihkan binary yang diunggah ke target sebelum keluar.
- Jangan menjalankan scanner dengan default agresif di produksi.

## 6. Best Practices

- Enumerasi dulu; tool eksploitasi menunggu hipotesis.
- Satu tool untuk satu tujuan; jangan menumpuk scanner tanpa membaca hasil.
- Siapkan field kit sebelum engagement, bukan saat terdesak.
- Verifikasi setiap temuan tool secara manual.
- Perbarui tool secara berkala; payload dan deteksi berubah cepat.
