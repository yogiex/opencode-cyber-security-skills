---
name: "Capability Domains — Peta Kapabilitas Detection Analyst"
description: "Sembilan domain kapabilitas detection and defensive analyst — kerangka serangan, telemetri Windows, akses awal dan eksekusi, eskalasi hak istimewa, persistence, telemetri Linux, jaringan dan C2, Active Directory, serta SIEM dan korelasi — beserta pola deteksi dan buktinya."
tags: [capability-map, detection, windows, sysmon, powershell, linux, active-directory, siem, c2]
---

# Capability Domains

Sembilan domain di bawah adalah peta kemampuan yang melekat pada persona ini. Ini bukan daftar bab yang harus dihafal, melainkan "kalau masalahnya di sini, ini yang saya kuasai, ini telemetri yang saya pakai, dan ini buktinya". Semua pola di sini adalah pola yang saya cari di data, bukan urutan materi.

## Peta domain

| # | Domain | Yang harus bisa | Bukti khas |
|---|---|---|---|
| 1 | Kerangka serangan | memetakan teknik ke telemetri yang seharusnya merekamnya | pemetaan ATT&CK per temuan, catatan teknik |
| 2 | Telemetri Windows | membaca Security/System/Sysmon/PowerShell dan arti tiap event | query, event ID, rantai PID |
| 3 | Akses awal dan eksekusi | mengenali eksekusi dari web, dokumen Office, dan PowerShell | IIS log, 4688, Sysmon 1, 4104 |
| 4 | Eskalasi hak istimewa | membedakan perubahan hak yang sah dari penyalahgunaan | 7045, Sysmon 13, konteks akun sebelum/sesudah |
| 5 | Persistence | menemukan mekanisme yang bertahan setelah reboot atau logoff | 7045/4697/4698, Sysmon 13, Sysmon 7 |
| 6 | Deteksi Linux | membaca auth.log, web daemon log, dan jejak hak akses | auth.log, access log, perubahan file |
| 7 | Jaringan dan C2 | mengenali beaconing, tunneling, dan egress yang menyimpang | Sysmon 22/3, IDS alert, flow |
| 8 | Active Directory | memisahkan administrasi domain dari penyalahgunaan | 4662, 4768/4769, 4728/4732/4756 |
| 9 | SIEM dan korelasi | merangkai beberapa sumber menjadi satu alur yang bisa direplikasi | pipeline ELK, query, dashboard, laporan |

## 1. Kerangka serangan dan pemetaan deteksi

Cara berpikirnya: attacker bergerak dalam tahap, dan setiap tahap meninggalkan jejak di sumber yang berbeda. Kerangka kerja memberi saya pertanyaan, bukan jawaban — "di tahap ini, sumber mana yang seharusnya berbicara?".

**Lockheed Martin Cyber Kill Chain:**

```text
Reconnaissance → Weaponization → Delivery → Exploitation
  → Installation → C2 → Actions on Objectives
```

**MITRE ATT&CK:** taktik, teknik, dan sub-teknik dipakai untuk memberi nama pada apa yang saya lihat, bukan untuk menebak apa yang terjadi. Pemetaan dilakukan setelah temuannya ada. Teknik yang sering muncul di lingkungan ini termasuk eksekusi PowerShell, service creation, akses LSASS, Kerberos ticket abuse, dan WMI.

Pola yang saya kenali lebih dulu, karena paling sering muncul berurutan:

| Tindakan | Telemetri yang menghubungkan |
|---|---|
| Akses awal lewat web | IIS/access log → 4688 di host web → proses anak dari `w3wp.exe` |
| Phishing dengan makro | dokumen Office → `winword.exe` memunculkan `cmd.exe`/`powershell.exe` → 4104 |
| Eskalasi hak istimewa | 7045 atau perubahan registry → proses berjalan sebagai `NT AUTHORITY\SYSTEM` |
| Persistence | 7045/4697, 4698, Sysmon 13 pada Run key |
| Akses kredensial | Sysmon 10 ke `lsass.exe`, 4662 pada objek domain |
| Lateral movement | 4624 Type 3, 4648, service baru di host tujuan |
| Persistence domain | 4768/4769 dengan enkripsi tidak wajar, 4728/4732/4756 |

Tabel lengkap teknik ke event ID ada di [windows-event-logs.md](./windows-event-logs.md).

## 2. Telemetri endpoint Windows

**Proses yang harus dikenal sebelum menyebut sesuatu aneh:** `System`, `svchost.exe`, `lsass.exe`, `winlogon.exe`, `explorer.exe`. Rantai induk-anaknya adalah peta jalan investigasi: `winword.exe` yang memunculkan `cmd.exe` adalah anomali struktural, dan `svchost.exe` yang memunculkan `cmd.exe` juga perlu dijelaskan — yang membedakan biasanya konteks host, akun, dan jalur binary-nya.

**Registry dan lokasi auto-start:** hive `HKLM`, `HKCU`, `HKCR`, `HKU`, `HKCC`. Lokasi yang dipantau: Run key, Winlogon, Services. Perubahan di sana adalah persistence atau privesc sampai terbukti sebaliknya.

**Channel event log:** Security, System, Application, PowerShell, Sysmon. Struktur event: Event ID, Level, Task Category, Keywords. Query lokal memakai `Get-WinEvent -FilterHashtable`; di SIEM, field ECS memetakan `event.code`, `winlog.event_data`, dan `host.name`.

**Sysmon** memberi kedalaman yang tidak dimiliki event log standar: command line lengkap, parent process, hash, koneksi jaringan, dan DNS. Event yang paling sering saya pakai: 1 (process creation), 3 (network connection), 7 (image load), 11 (file create), 13 (registry value set), 22 (DNS query). Aktivasi dan cakupannya bergantung config — event yang tidak muncul harus dicek konfigurasinya dulu sebelum disebut evasion.

Event dasar yang muncul di hampir setiap investigasi:

```text
4624 — Successful logon (perhatikan Logon Type)
4625 — Failed logon
4688 — Process creation (butuh command line auditing)
4672 — Special privileges assigned
7045 — Service installed (System log)
```

## 3. Akses awal dan eksekusi

**Server-side.** Web server adalah entry point paling umum di lingkungan Windows. IIS menulis log W3C berisi status code dan URI; pola yang dicari: traversal `../` untuk LFI, parameter yang memuat perintah untuk command injection, dan file creation di direktori web (Sysmon 11) untuk upload shell. Eksekusi setelahnya terlihat sebagai proses anak dari `w3wp.exe` di 4688 atau Sysmon 1. Buffer overflow pada layanan biasanya meninggalkan jejak lewat event Windows Defender Exploit Guard dan proses yang lahir dari proses induk yang salah.

**Client-side.** Dokumen Office dengan makro adalah jalur klasik. Indikatornya parent-child yang tidak mungkin: `winword.exe` atau `excel.exe` memunculkan `cmd.exe`, `powershell.exe`, atau `wscript.exe`. Aplikasi Office tidak seharusnya memunculkan shell; kalau muncul, itu yang dicatat lebih dulu.

**PowerShell logging** adalah tempat paling produktif:

| Event | Isi | Nilai |
|---|---|---|
| 4103 | module logging — cmdlet dan parameter | melihat apa yang dipanggil, tanpa isi script |
| 4104 | script block logging — isi script penuh | menangkap kode setelah deobfuskasi |
| transcription | rekaman sesi penuh | konteks urutan perintah |

Alur yang saya susun ketika phishing dicurigai:

```text
email → dokumen Office → makro → PowerShell → 4104 (kode hasil deobfuskasi)
  → AMSI bypass? → koneksi C2
```

**AMSI dan antivirus.** Deteksi antivirus bersifat signature (paling mudah dilewati), heuristic/behavioral (berbasis perilaku runtime), dan AMSI untuk pemindaian script. Bypass AMSI lewat refleksi biasa terlihat di 4104 sebagai kode yang menambal AMSI; bypass lewat registry terlihat sebagai perubahan `AmsiEnable` di Sysmon 13. Alarm AV yang mati mendadak di tengah aktivitas PowerShell adalah sinyal tersendiri, dan alert AV itu sendiri adalah IoC yang sah — didokumentasikan, bukan dibuang.

## 4. Eskalasi hak istimewa

**Windows.** Empat jalur yang paling sering muncul, dan jejaknya berbeda:

| Jalur | Jejak |
|---|---|
| UAC bypass berbasis registry (fodhelper, eventvwr) | Sysmon 13 pada key terkait + proses dengan induk tidak wajar |
| Unquoted service path | 7045 dengan path tanpa kutip + Sysmon 1 saat service dijalankan |
| Permission service lemah | perubahan registry service, penggantian binary di `Program Files` (Sysmon 11) |
| Token abuse (`SeImpersonate`, `SeAssignPrimaryToken`) | proses anak tidak wajar dari service berjalan sebagai SYSTEM |

Indikator yang saya pakai untuk membedakan eskalasi dari aktivitas administrasi normal:

```text
Sebelum: proses berjalan sebagai user low-priv
Sesudah: proses berjalan sebagai NT AUTHORITY\SYSTEM
Cari: 7045 → proses sebagai SYSTEM, atau UAC bypass → perubahan registry + proses baru
```

**Linux.** `.bashrc`/`.profile` yang diubah adalah persistence tingkat user; `authorized_keys` yang bertambah adalah backdoor SSH. Di tingkat sistem: `chmod u+s` pada binary (SUID), `/etc/shadow` yang menjadi world-readable, dan kernel exploit yang jejaknya berupa proses dengan nama tidak lazim. Pola yang dicari: dari `www-data` atau user low-priv menjadi `root` lewat `sudo` atau SUID, dan apa yang berubah tepat sebelum itu.

## 5. Persistence

**Di disk.** Windows Service (`sc create`, `New-Service`) → 7045 atau 4697. Scheduled Task (`schtasks`) → 4698. DLL sideloading/hijacking → Sysmon 7 dengan image load dari path tidak standar.

**Di registry.** Run key `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` → Sysmon 13. Winlogon helper `HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon` → Sysmon 13.

Query yang saya pakai untuk menyapu satu host:

```kql
event.code : (7045 OR 4698 OR 13 OR 12) AND host.name : "TARGET_HOST"
```

**Di Linux.** Perubahan `.bashrc`/`.profile`, penambahan kunci di `authorized_keys`, dan SUID baru. Jejaknya ada di perubahan file dan di auth log pada login berikutnya.

Persistence adalah jembatan antar tahap. Kalau mekanismenya tidak ditemukan, rantai ke host dan sesi berikutnya akan terputus, dan laporan berhenti di tengah cerita.

## 6. Telemetri dan deteksi Linux

Linux di estate ini jarang sekomplet Windows, jadi fokusnya sempit dan dalam: autentikasi dan web server.

| Berkas | Isi |
|---|---|
| `/var/log/auth.log` | autentikasi (Debian/Ubuntu) |
| `/var/log/secure` | autentikasi (RHEL/CentOS) |
| `/var/log/syslog` | event sistem |
| `/var/log/kern.log` | pesan kernel |
| `/var/log/messages` | pesan umum (RHEL) |
| `/var/log/apache2/`, `/var/log/nginx/` | access log dan error log web |

Selain berkas, `journalctl` membaca journald, dan `syslog`/`rsyslog` menentukan ke mana event dikirim. Bila host tidak meneruskan log ke SIEM, seluruh domain ini hanya bisa dijawab dari data yang tersisa.

Pola yang saya cari:

```text
auth.log: "Failed password for root" berulang dari satu sumber = brute force
auth.log: "Accepted publickey for www-data"              = autentikasi berhasil, cek konteksnya
apache2/access.log: "GET /index.php?cmd=id"              = command injection
```

Auth log hanya mencatat autentikasi. Eksekusi setelah login harus dicari di web daemon log, process accounting, atau perubahan file — dan bila tidak ada, itu batas yang harus disebutkan.

## 7. Jaringan, C2, dan evasion

**IDS/IPS.** Snort mendefinisikan aturan dengan komponen: action, protocol, source/destination, dan content detection.

```text
alert tcp $HOME_NET any -> $EXTERNAL_NET $HTTP_PORTS
```

Signature mengenali pola yang sudah dikenal; anomaly mengenali penyimpangan dari baseline. Keduanya punya mode gagal yang berbeda: signature melewatkan yang baru, anomaly menghasilkan noise pada trafik yang belum pernah dilihat.

**C2.** Beaconing terlihat sebagai koneksi dengan interval teratur dan ukuran payload yang berulang. DGA terlihat sebagai subdomain acak dalam jumlah besar. DNS tunneling terlihat sebagai lonjakan query DNS dari satu host, sering dengan record panjang atau tipe yang tidak lazim. Telemetrinya: Sysmon 22 (DNS query), Sysmon 3 (network connection), rule Snort, dan log proxy/firewall bila ada.

**Evasion jaringan.** Segmen seharusnya tidak bisa saling bicara kecuali lewat firewall; bila ada jalur yang tidak dirancang, itu temuan tersendiri. Egress busting terlihat sebagai percobaan koneksi dari satu host internal ke banyak port keluar. Port forwarding dan tunneling (SSH, Chisel, Ligolo-ng, socat) terlihat sebagai koneksi keluar yang tidak wajar atau port tinggi yang listen di server. Verifikasi state dengan OSQuery: `SELECT * FROM listening_ports`.

| Normal | Mencurigakan |
|---|---|
| Internal ke internet lewat 443 (HTTPS) | Internal ke internet lewat 53 padahal bukan resolver (DNS tunneling) |
| Server internal hanya listen di port layanannya | Server internal listen di port tinggi (>1024) tanpa penjelasan |
| Koneksi keluar dari proses yang punya fungsi jaringan | Koneksi keluar dari proses yang tidak seharusnya berbicara ke internet |

## 8. Active Directory dan lateral movement

**Enumeration.** PowerView (`Get-NetUser`, `Get-NetComputer`, `Get-NetGroup`) menghasilkan volume query LDAP yang besar dari host non-admin. Event 4662 (operasi pada objek) mencatat akses ke objek sensitif. Yang membuat ini bisa dibaca adalah baseline: berapa banyak query LDAP yang wajar untuk host itu, dan jam berapa. Honey token — objek palsu yang tidak pernah dipakai proses sah — mengubah akses tak sengaja menjadi detection.

**Lateral movement.** Empat jalur dengan jejak masing-masing:

| Jalur | Jejak |
|---|---|
| Pass-the-Hash (Impacket wmiexec/psexec/smbexec) | 4624 Type 3 + 7045 di host tujuan + 4688 |
| Pass-the-Ticket (Rubeus, Mimikatz) | 4768/4769 dengan enkripsi tidak sesuai kebiasaan |
| Kerberoasting | 4769 dengan RC4 (`0x17`) berulang dari satu user dalam waktu singkat |
| RDP | 4624 Type 10, termasuk restricted admin mode |

Rantai yang saya susun untuk satu perpindahan host:

```text
Sumber: Host A (sudah compromise)
Metode: wmiexec / psexec / winrm
Tujuan: Host B
Telemetri:
  - koneksi A → B (Sysmon 3 atau firewall log)
  - service dibuat di B (7045)
  - proses baru di B (4688) dengan command line
  - konteks akun: Administrator atau Domain Admin
```

**Persistence domain.** Penambahan user ke Domain Admins (4728) atau Enterprise Admins (4756), dan perubahan grup lokal (4732), terutama bila event-nya datang dari host non-DC. Golden ticket terlihat pada 4768 dengan masa berlaku di luar kebiasaan (default 10 jam) atau tipe enkripsi yang tidak sesuai, ditambah 4672 untuk akun yang seharusnya tidak punya hak istimewa. Silver ticket terlihat pada 4624 Type 3 dari machine account yang konteksnya janggal. DCSync terlihat pada 4662 dengan hak replikasi, dan bila penyerang memilih jalur langsung, pada akses ke `ntds.dit`.

## 9. SIEM dan korelasi

**Pipeline.** Rantai datanya harus dipahami sebelum hasil query dipercaya:

```text
Beats (Winlogbeat, Filebeat) → Logstash → Elasticsearch → Kibana
  Winlogbeat  : mengumpulkan Windows Event Log dan Sysmon
  Filebeat    : mengumpulkan log berbasis berkas (syslog, IIS, auth.log)
  Logstash    : parsing, filter, transformasi
  Elasticsearch: index dan penyimpanan
  Kibana      : pencarian, visualisasi, dashboard
```

Bila satu host tidak muncul di Kibana, pertanyaan pertama bukan "apa yang attacker lakukan", melainkan "apakah jalur ini masih mengalir". Audit pipeline adalah bagian dari deteksi.

**OSQuery** terpasang sebagai Elastic Agent integration dan memberi state langsung: proses, port yang listen, koneksi terbuka, service, scheduled task, user, firewall rule. Ia menjawab "apa yang ada sekarang", bukan "apa yang terjadi kemarin" — pembagian kerja ini yang menjaga keduanya tetap berguna.

**Fitur ELK untuk analisis:** rule dan alert berbasis KQL, timeline untuk case management, dan dashboard untuk gambaran cepat. Dashboard pra-buat berguna sebagai titik awal, tetapi tidak pernah saya pakai sebagai kesimpulan: sebagian alert adalah rabbit hole, dan sebagian aktivitas jahat tidak memicu alert sama sekali.

**Rantai deteksi lintas host.** Nilai SIEM muncul ketika beberapa host dirangkai menjadi satu alur:

```text
Tahap akses awal   : web01 — enumerasi + command injection
                     IIS log dikorelasikan dengan 4688 dan Sysmon 1
Tahap perpindahan  : appsrv01 — brute force lalu autentikasi berhasil
                     PID dan waktu dari web01 dipakai untuk mencari jejak di appsrv01
Tahap persistence  : appsrv01 — service creation, registry, scheduled task
Tahap domain       : DC — akses database AD, DCSync, perubahan grup
```

Yang membuat rantai ini bisa dipertanggungjawabkan adalah tiga hal: rentang waktu yang konsisten antar host, field yang ekuivalen (`user.name`, `source.ip`, `process.pid`), dan catatan tentang sambungan yang hilang. Sambungan yang hilang adalah temuan, bukan alasan untuk mengarang jembatan.

## Cara memakai peta ini

1. **Saat menerima masalah** — petakan ke satu atau dua domain; jangan memaksakan kesembilan domain relevan.
2. **Saat memilih sumber** — tanyakan domain mana yang seharusnya merekam tindakan ini, lalu periksa apakah sumber itu memang aktif.
3. **Saat melapor** — sebut domain, telemetri, query, dan keyakinannya; bukan nama alat atau nama teknik saja.
4. **Saat menilai diri** — domain tanpa bukti nyata di data adalah domain yang belum dikuasai, seberapa pun hafalnya tabel event.

## Best Practices

- Pilih domain berdasarkan pertanyaan investigasi, bukan berdasarkan alat yang paling nyaman.
- Satu pola yang terbukti lebih bernilai daripada sepuluh pola yang diingat tanpa pernah diuji.
- Selalu bedakan pola yang berasal dari dokumentasi dengan pola yang saya ukur sendiri di data.
- Simpan query per domain; itu bahan laporan sekaligus bahan untuk menguji ulang.
- Domain 8 dan 9 sering butuh koordinasi dengan pemilik platform sebelum tindakan, bukan sesudahnya.
