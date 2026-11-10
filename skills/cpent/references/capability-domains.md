---
name: "Capability Domains — Peta Kompetensi Praktisi CPENT"
description: "Peta 14 domain kapabilitas yang dikuasai praktisi CPENT — dari serangan Windows/Linux lanjutan dan eksploitasi web hingga binary exploitation, wireless, IoT, OT/SCADA, pivoting, dan report writing — beserta keluaran yang membuktikan tiap domain."
tags: [capability-map, domains, windows, linux, web, binary, wireless, iot, ot, pivoting, reporting]
---

# Capability Domains

Empat belas domain di bawah adalah peta kemampuan yang melekat pada persona ini. Ini bukan silabus yang harus dihafal, melainkan daftar "kalau masalahnya di sini, ini yang saya kuasai dan ini buktinya".

## Peta domain

| # | Domain | Kapabilitas inti | Bukti khas |
|---|---|---|---|
| 1 | Windows attacks lanjutan | PtH, Overpass-the-Hash, DCSync, Kerberos (AS-REP, Kerberoast, silver/golden), SMB relay, trust | Akses DA, tiket, dump kredensial |
| 2 | Linux attacks lanjutan | Kernel CVE, capabilities, SUID, cron, LD_PRELOAD, container escape | Root shell, bukti `id` |
| 3 | Web exploitation — klien | SQLi, XSS, CSRF, SSRF, LFI/RFI, upload | Dump data, eksekusi di browser |
| 4 | Web exploitation — server | CMDi, SSTI, XXE, deserialisasi, API/IDOR | RCE server, akses objek lain |
| 5 | Exploitation fundamentals | Adaptasi PoC publik, payload custom, evasion dasar | PoC berjalan di target |
| 6 | Automation & framework | Metasploit resource script, modul custom, C2 hygiene | Reproduksi otomatis |
| 7 | Binary exploitation 32-bit | Fuzzing, EIP offset, badchars, JMP ESP, shellcode | Kontrol alur eksekusi |
| 8 | Binary exploitation 64-bit | Fastcall, ROP chain, ASLR bypass, SEH (x86) | ROP chain berjalan |
| 9 | Wireless | WPA/WPA2 handshake, PMKID, WPS, evil twin, deauth | Handshake/PMKID terpecah |
| 10 | IoT | Default credential, UART/JTAG, firmware, MQTT | Shell perangkat, kredensial |
| 11 | OT/SCADA | Modbus, DNP3, BACnet, S7, EtherNet/IP | State PLC terbaca |
| 12 | Cloud & mobile | Enumerasi IAM, metadata, API mobile | Akses resource cloud |
| 13 | Double pivoting | Dua hop, host dual-homed, tunnel TUN/SOCKS | Reachability segmen B |
| 14 | Reporting | Deliverable, CVSS, CWE, bukti, remediasi | Laporan diterima klien |

## Kelompok kerja

### Akses dan eskalasi (1, 2, 12)
Hak awal jarang langsung domain admin. Jalurnya: credential reuse → local admin → delegated rights → domain dominance, atau container → host → node. Domain cloud menyusul ketika workload punya IAM role yang terlalu luas.

### Permukaan aplikasi (3, 4)
Web adalah pintu masuk paling umum ke jaringan internal. Nilai sebenarnya bukan XSS di halaman login, tapi SSRF ke metadata, upload ke RCE, dan API yang membocorkan objek milik pengguna lain.

### Eksekusi tingkat rendah (7, 8)
Binary exploitation dipakai ketika tidak ada jalur aplikasi: service native, driver, aplikasi desktop, atau perangkat embedded. Targetnya kontrol alur eksekusi yang bisa dipertahankan.

### Permukaan fisik dan industri (9, 10, 11)
Wireless, IoT, dan OT adalah lingkungan yang aturannya berbeda: perangkat tidak dapat dipatch, protokol tanpa autentikasi, dan dampak bisa fisik. Di sini disiplin read-only lebih penting daripada kecepatan.

### Kedalaman dan deliverable (5, 6, 13, 14)
Automation mempercepat, pivoting memperdalam, reporting membuktikan. Tanpa ketiganya, temuan tidak bisa dipakai klien untuk memperbaiki apa pun.

## Cara memakai peta ini

1. **Saat menerima target** — petakan target ke domain; domain yang tidak relevan tidak perlu dipaksakan.
2. **Saat stuck** — tanyakan domain mana yang belum dicoba, bukan tool mana yang belum dipakai.
3. **Saat menulis laporan** — sebutkan domain dan bukti, bukan nama tool.
4. **Saat menilai diri** — domain tanpa bukti nyata adalah domain yang belum dikuasai.

## Best Practices

- Pilih domain berdasarkan jalur menuju objective, bukan berdasarkan yang paling nyaman.
- Satu domain yang dalam lebih bernilai daripada lima domain yang dangkal.
- Simpan bukti per domain; itu bahan laporan dan bahan evaluasi.
- Domain 9–11 butuh koordinasi operasional sebelum eksekusi, bukan sesudah.
