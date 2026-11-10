---
name: "Live Response — Host Triage"
description: "Live triage host Linux saat insiden: enumerasi proses berjalan, cron dan penjadwal semua user, serta koneksi jaringan keluar, lengkap dengan korelasi PID, indikator, false positive, dan batasannya."
tags: [live-response, host-triage, processes, cron, persistence, network-connections, ss, lsof, proc, linux, dfir]
---

# Live Response — Host Triage

Dipakai saat host diduga terkompromi — defacement, web shell, koneksi anomali, atau CPU naik tanpa sebab — dan host **belum** boleh dimatikan atau di-rebuild. Tujuan: mengambil tiga artefak yang paling cepat hilang (koneksi keluar, tabel proses, persistence terjadwal) dengan cara yang tidak merusak bukti.

Untuk host Windows, lihat padanan singkat di bagian akhir; alur penalarannya sama.

## Decision Frame

1. **Masih ada penyebaran aktif?** Jika ya, isolasi jaringan dulu, triage kemudian. Jika tidak, triage dulu — mematikan host menghapus semua yang ada di daftar ini.
2. **Urutan volatilitas**: koneksi jaringan → tabel proses → cron di disk. Ketiganya diambil dalam satu pass kurang dari 10 menit; urutan itu hanya berlaku bila harus memilih.
3. **Jangan kill sebelum menyalin.** `kill` menghapus `cmdline`, `environ`, `fd`, dan `maps` di `/proc/<pid>`. Salin dulu, tindakan kemudian.
4. **PID adalah kunci korelasi**, bukan nama proses. Nama bisa dipalsukan; PID menghubungkan proses ↔ socket ↔ file di disk.
5. **Tanpa baseline, itu bukan bukti.** Catat sebagai "unknown, perlu verifikasi" kecuali jelas melanggar: binary berjalan dari `/tmp`, `bash` punya socket keluar, cron berisi `curl | sh`.

## Aturan Main

```bash
export TZ=UTC
date -u; hostname; uname -a; id; cat /etc/os-release | head -2
mkdir -p /root/ir-$(date -u +%Y%m%dT%H%M%SZ)
```

- Jalankan sebagai **root**. Tanpa root, kolom PID di `ss` kosong dan `/proc/<pid>/environ` tidak terbaca.
- Simpan setiap output ke file, bukan hanya ke layar. Menulis ke disk mengubah disk — catat di log, dan bila tersedia arahkan output ke USB atau network share.
- Catat **jam host vs jam dinding**. Host yang jamnya digeser membuat timeline menyesatkan; `lstart` proses menjadi tidak bisa dipercaya.

## 1. Proses Berjalan

### Perintah

```bash
# Snapshot utama — -ww mencegah args terpotong lebar terminal
ps -eo pid,ppid,user,lstart,etime,stat,pcpu,pmem,args --sort=-pcpu | tee ps-full.txt
ps auxww --forest | tee ps-tree.txt
pstree -alp | tee pstree.txt

# Bandingkan jumlah proses dengan /proc (deteksi rootkit userland)
ps -e --no-headers | wc -l
ls -d /proc/[0-9]* | wc -l

# Binary yang sudah dihapus setelah dijalankan
ls -l /proc/*/exe 2>/dev/null | grep '(deleted)'

# Binary yang berjalan dari direktori writable
ls -l /proc/*/exe 2>/dev/null | grep -E '/tmp|/dev/shm|/var/tmp|/run/user'

# Executable anonim / fileless
grep -lE 'memfd|/dev/shm' /proc/*/maps 2>/dev/null
```

### Yang dicari

- **Binary `(deleted)`** — klasik malware yang menghapus dirinya setelah berjalan. Selalu prioritas tertinggi.
- **Rantai parent yang tidak wajar**: `nginx`/`apache2`/`php-fpm` → `sh`/`bash`/`python` menandakan RCE dari web.
- **`www-data` punya shell** atau proses yang seharusnya service sekarang punya child interaktif.
- **`cmdline` kosong** padahal proses aktif dan punya socket.
- **Nama menyamar**: proses bernama `[kworker/0:2]` tetapi punya `exe` di disk (kernel thread asli tidak punya `exe`), atau nama `sshd`, `crond` yang menunjuk `/tmp`.
- **Proses sangat baru** — `lstart` dalam jendela insiden, terutama setelah jam kerja.
- **CPU tinggi + koneksi keluar** — ada di dua daftar sekaligus berarti miner atau tunnel.

### Korelasi per PID

```bash
PID=<pid>
tr '\0' ' ' < /proc/$PID/cmdline; echo
tr '\0' '\n' < /proc/$PID/environ | sort
readlink -f /proc/$PID/exe /proc/$PID/cwd
ls -l /proc/$PID/fd
grep -E 'Uid|Gid|CapEff|Seccomp|Threads' /proc/$PID/status
grep -E '/tmp|/dev/shm|memfd' /proc/$PID/maps
ls -l /proc/$PID/ns/          # bandingkan dengan /proc/1/ns/pid untuk deteksi namespace lain
ss -tnp | grep "pid=$PID"
```

`environ` sering memuat kredensial yang dipakai proses — perlakukan sebagai rahasia. `cwd` di `/tmp` untuk daemon produksi adalah sinyal kuat.

### Lacak File yang Dijalankan

`cmdline` adalah klaim proses tentang dirinya sendiri dan bisa dipalsukan. Yang otoritatif adalah tautan kernel di `/proc/<pid>/exe`.

```bash
PID=<pid>
readlink -f /proc/$PID/exe          # path absolut binary yang benar-benar dieksekusi
ls -l /proc/$PID/exe                # ada embel-embel "(deleted)" bila file sudah dihapus
head -1 /proc/$PID/status           # Name dari kernel, bukan argv[0]
head -c 64 /proc/$PID/exe | xxd     # magic bytes: ELF, shebang, arsip

# Semua file yang dipetakan: library, jar, template, skrip yang di-load
awk '{print $6}' /proc/$PID/maps | grep -v '^$' | sort -u
```

Empat bentuk yang sering tertukar saat mencari "file yang dijalankan":

| Isi `exe` | Artinya | Di mana file sebenarnya |
|---|---|---|
| `/usr/bin/python3` | skrip Python | skripnya adalah `argv[1]` di `cmdline`, bukan `exe` |
| `/usr/bin/java` | aplikasi JVM | jar/class ada di `cmdline` dan `/proc/<pid>/maps` |
| `/opt/php/sbin/php-fpm` | worker PHP | skrip dipilih per request — cari di access log, bukan di proses |
| `/memfd:payload (deleted)` | binary hidup di memori, tanpa file di disk | salin dari `/proc/<pid>/exe`, jangan cari di disk |

> Jangan percaya `argv[0]`. Malware lazim menamai dirinya `sshd` atau `[kworker/0:2]`; `readlink /proc/<pid>/exe` tidak bisa dibohongi selama proses masih hidup.

### Temukan File di Disk

```bash
PID=<pid>
EXE=$(readlink -f /proc/$PID/exe)

# 1. Masih ada? Masih sama dengan yang berjalan?
stat "$EXE" 2>/dev/null
sha256sum "$EXE" /proc/$PID/exe          # hash berbeda = file di disk sudah ditimpa

# 2. Milik paket apa? (tidak ketemu = tidak ada paket yang mengakuinya)
command -v dpkg >/dev/null && dpkg -S "$EXE"
command -v rpm  >/dev/null && rpm -qf "$EXE"

# 3. Cari lewat inode — menembus hardlink dan nama yang diubah
stat -c '%d:%i' "$EXE"
find / -xdev -inum <inode> 2>/dev/null

# 4. Selamatkan binary yang sudah dihapus, selagi proses masih hidup
cp /proc/$PID/exe /root/ir-*/pid-$PID.exe
sha256sum /root/ir-*/pid-$PID.exe
```

- **Hash berbeda antara path di disk dan `/proc/<pid>/exe`** berarti file ditimpa setelah proses jalan. Yang di `/proc` adalah yang benar-benar berjalan — jadikan itu bukti.
- `dpkg -S` / `rpm -qf` yang kosong adalah sinyal kuat: binary tidak dipasang lewat paket resmi.
- Jalur di dalam container berbeda dengan jalur host. `readlink` dari host memberi path di namespace proses; bacanya lewat `/proc/<pid>/root/<path>`.
- File tidak ada di disk tetapi prosesnya hidup bukan jalan buntu — salin, hash, lalu lanjut menganalisis isinya. Binary yang menghapus dirinya sendiri adalah pola malware, bukan kesalahan administrasi.

### Periksa Isi & Perilaku File

Analisis statis dulu karena tidak mengeksekusi apa pun. Baru setelah itu perilaku proses yang sedang hidup.

```bash
BIN=/root/ir-*/pid-1234.exe

# Statis — tidak menjalankan apa pun
file "$BIN"
strings -n 8 "$BIN" | grep -E 'https?://|([0-9]{1,3}\.){3}[0-9]{1,3}|/dev/tcp|curl|wget|base64|cron|authorized_keys|ld\.so|chmod'
readelf -hd "$BIN" 2>/dev/null | grep -E 'NEEDED|INTERP|Type'
objdump -p "$BIN" 2>/dev/null | grep NEEDED
yara -s /path/to/rules.yara "$BIN"
binwalk -E "$BIN" 2>/dev/null | head -20      # entropi tinggi = kemungkinan packed
```

> **Jangan pakai `ldd` pada binary yang tidak dipercaya.** `ldd` menjalankan dynamic loader pada binary itu dan pada sejumlah kasus mengeksekusi kodenya. Gunakan `objdump -p ... | grep NEEDED` atau `readelf -d`.

```bash
# Dinamis — apa yang dijalankan proses ini sekarang
pstree -p $PID                                   # anak proses: eksekusi turunan
ps --ppid $PID -o pid,args                       # satu generasi di bawahnya
ls -l /proc/$PID/fd | grep -vE '/dev/(null|pts)' # file dan socket yang sedang dibuka
ss -tnp | grep "pid=$PID"

# Syscall, hanya bila perlu dan diizinkan
timeout 30 strace -f -p $PID -e trace=execve,connect,openat -o /root/ir-*/strace-$PID.txt
```

> `strace` menghentikan proses sesaat dan terlihat dari dalam. Malware yang memeriksa `TracerPid` di `/proc/self/status` akan mendeteksinya dan bisa berhenti berperilaku. Jangan jadikan langkah pertama, dan **jangan pernah** menjalankan sampel di host yang sedang diinvestigasi — detonasi di VM atau container terisolasi tanpa jaringan, hasilnya cocokkan dengan hash.

Cara membaca hasilnya:

- `execve` baru ke `sh -c`, `curl`, atau `wget` → binary itu dropper atau stager.
- `connect` ke IP:port yang sama dengan `ss` → konfirmasi C2, bukan sekadar koneksi bisnis.
- `openat` ke `/etc/cron*`, `authorized_keys`, atau `ld.so.preload` → arah persistence-nya.
- `strings` yang memuat path cron plus perintah `chmod` sudah cukup menyimpulkan hal yang sama tanpa perlu mengeksekusi apa pun.

Urutan kerjanya: **exe → path → inode/hash → pemilik paket → isi statis → perilaku (child, socket, syscall)**. Setiap langkah mempersempit ruang: dari daftar proses ke satu file, dari satu file ke satu keluarga malware.

### False positive

| Temuan | Biasanya normal karena |
|---|---|
| `[kworker/*]`, `[ksoftirqd/*]`, `[migration/*]` | kernel thread — `readlink /proc/<pid>/exe` kosong, wajar |
| Ratusan proses `java`, `node`, `go` | thread terhitung sebagai proses di tool tertentu; cek jumlah thread dengan `ps -eLf` |
| `args` tampak pendek dan tidak berbahaya | `ps aux` tanpa `ww` memotong sesuai `COLUMNS` |
| Proses tanpa `exe` di container | `/proc` namespace container, bukan host |
| Jumlah proses sedikit | image minimal (distroless) — sedikit proses bukan berarti bersih |

### Batas

- Rootkit userland bisa menyembunyikan proses dari `ps` **dan** `/proc` sekaligus. Bandingkan dengan sumber eksternal: netflow, `ss` dari host lain, auditd, EDR, log auth.
- Proses dalam namespace PID lain terlihat atau tidak tergantung privilege; `docker top` atau `nsenter` bila perlu.
- Ini sampel sesaat. Dropper yang hidup dua detik tidak tertangkap — untuk itu butuh auditd/eBPF, bukan triage manual.

## 2. Cron & Penjadwal Semua User

### Perintah

```bash
# Crontab seluruh user (butuh root)
for u in $(cut -d: -f1 /etc/passwd); do
  printf '===== %s\n' "$u"
  crontab -l -u "$u" 2>/dev/null
done | tee crontabs-all.txt

# Jadwal tingkat sistem
cat /etc/crontab
find /etc/cron.d /etc/cron.hourly /etc/cron.daily /etc/cron.weekly /etc/cron.monthly \
  -type f -print -exec cat {} \; 2>/dev/null | tee cron-system.txt

# Spool: siapa yang benar-benar punya crontab, dan kapan berubah
ls -la /var/spool/cron/crontabs/ 2>/dev/null    # Debian/Ubuntu
ls -la /var/spool/cron/ 2>/dev/null             # RHEL/CentOS

# Penjadwal lain yang sering terlewat
systemctl list-timers --all
atq 2>/dev/null; ls -la /var/spool/cron/atjobs/ 2>/dev/null
cat /etc/anacrontab

# Timer milik user (tidak muncul di list-timers sistem)
for h in /root /home/*; do
  echo "--- $h"; ls -la "$h/.config/systemd/user/" 2>/dev/null
done
```

### Yang dicari

- Isi yang menjalankan kode dari jaringan atau base64: `curl|wget ... | sh`, `bash -c "$(curl ...)"`, `base64 -d`, `python -c`, `nc -e`, `/dev/tcp/`.
- `@reboot` dan `* * * * *` (tiap menit) pada host yang tidak butuh.
- User non-root punya crontab — apalagi `www-data`, `apache`, `nginx` — menunjuk direktori writable (`/tmp`, `/dev/shm`, home miliknya).
- **Mtime spool lebih baru dari aktivitas sah**. Bandingkan dengan `last` dan `lastlog`:

```bash
stat -c '%y %n' /var/spool/cron/crontabs/* 2>/dev/null
last -a | head -20
lastlog | grep -v 'Never logged in'
```

- Permission spool bukan `600` — cron Debian mengabaikan file yang bisa dibaca user lain.
- Nama file di `/etc/cron.d` mengandung titik. Debian melewatinya, distro lain belum tentu; file itu tetap bukti, bukan alasan untuk mengabaikannya.
- Job `at` yang tidak pernah dibuat admin — biasanya dipakai untuk backdoor sekali jalan.

### Bukti dari log

```bash
grep -i cron /var/log/syslog | tail -50          # Debian
grep -i cron /var/log/cron | tail -50            # RHEL
journalctl -u cron --since '-2 days'             # unit crond di RHEL
```

### False positive

| Temuan | Biasanya normal karena |
|---|---|
| `e2scrub_all`, `logrotate`, `apt-compat`, `man-db`, `dpkg` di `cron.daily` | paket distro |
| `certbot renew`, `backup`, job monitoring | operasional rutin |
| User `deploy`, `gitlab-runner`, `jenkins` punya crontab | deployment pipeline |
| `@reboot /opt/app/start.sh` | aplikasi mengurus dirinya sendiri |

### Batas — cron bukan satu-satunya persistence

Bila cron bersih tetapi gejala tetap ada, periksa daftar berikut sebelum menyimpulkan host bersih:

- systemd unit dan timer, termasuk `~/.config/systemd/user`
- `/etc/rc.local`, `/etc/init.d`, `/etc/profile.d`, `~/.bashrc`, `~/.profile`
- `~/.ssh/authorized_keys` — jalur masuk ulang, bukan eksekusi
- `/etc/ld.so.preload` — favorit untuk menyembunyikan proses dan library
- PAM (`pam_exec`, modul tambahan), `cron.allow`/`cron.deny` yang diubah
- Container: `restart: always` dengan image yang sudah teracuni, Kubernetes `CronJob`
- Web shell: file yang dieksekusi atas permintaan HTTP, tidak butuh jadwal sama sekali

## 3. Koneksi Jaringan Keluar

### Perintah

```bash
# Established saja, dengan proses (butuh root untuk kolom pid)
ss -tunp state established | tee net-established.txt

# Semua socket, termasuk listener
ss -tunap

# Extended info: bytes_sent/bytes_received/rtt — dasar mendeteksi beacon
ss -tinp state established

# Filter tujuan
ss -tnp dst :443
ss -tnp '( dport = :80 or dport = :443 )'

# Alternatif bila ss tidak ada
lsof -i -n -P | grep -v LISTEN
netstat -antp

# Cadangan terakhir: file mentah /proc (simpan apa adanya sebagai bukti)
cat /proc/net/tcp /proc/net/tcp6
awk 'NR>1 && $4=="01" {print $8}' /proc/net/tcp | sort -u | while read -r uid; do
  getent passwd "$uid"
done
```

Di `/proc/net/tcp`, status `01` berarti ESTABLISHED, alamat IPv4 ditulis little-endian dalam hex (mis. `0100007F:1F90` = `127.0.0.1:8080`), dan kolom ke-8 adalah UID pemilik socket. Simpan file mentahnya; jangan mengandalkan pembacaan manual saat tekanan tinggi.

### Yang dicari

- **`bash`, `sh`, `nc`, `socat`, `python`, `perl` punya ESTABLISHED ke internet** — reverse shell, hampir tanpa false positive di server produksi.
- **Beacon**: sesi panjang, `bytes_sent` kecil dan konsisten, interval teratur. `ss -tinp` menampilkan penghitungnya.
- **Tujuan tidak relevan dengan bisnis**: ASN hosting murah, negara yang tidak pernah muncul di baseline, IP tanpa PTR yang cocok.
- **`169.254.169.254` dari proses web** (bukan agent cloud) — SSRF ke metadata, jalur panen kredensial IAM.
- **Koneksi keluar dari proses yang `exe`-nya `(deleted)`** — gabungkan temuan 1 dan 3; ini biasanya puncak gunung es.
- **Unix socket milik proses tak dikenal** (`ss -x`) — backdoor lokal, sering dipicu cron.

### Korelasi

```bash
ss -tnp | grep 'pid='
lsof -p <pid> -a -i
```

Pasangkan hasilnya dengan `readlink -f /proc/<pid>/exe` dan `cwd`. Urutan bukti yang kuat: **socket → PID → binary di disk → hash**. Bila binary hilang, ambil `/proc/<pid>/exe` sebagai bukti memori (`cp /proc/<pid>/exe /evidence/`).

### False positive

| Temuan | Biasanya normal karena |
|---|---|
| `apt`, `yum`, `dnf`, `snapd` keluar ke repo | manajemen paket |
| Node exporter, Zabbix, Datadog, OSSEC push | monitoring |
| `chronyd`/`ntpd` ke UDP 123 | sinkronisasi waktu |
| SMTP relay, backup agent, agent cloud ke metadata | operasional |
| `node`/`chrome` di host developer | banyak koneksi keluar itu normal |

### Batas

- Ini **snapshot**. Koneksi berumur detik hilang sebelum sempat terbaca; beacon 30 detik bisa terlewat. Ambil 2–3 sampel dengan jeda, atau pakai `conntrack -L`, netflow, dan log firewall.
- Tanpa root, `ss` tetap menampilkan socket tetapi kolom PID kosong — jangan simpulkan "tidak ada proses" dari output itu.
- TLS menyembunyikan isi. Yang terlihat hanya IP dan port; untuk klasifikasi perlu PCAP + SNI/JA3 (`tcpdump -i any -w evidence.pcap`), dengan kesadaran ukuran file dan privasi.
- IPv6 ada di `/proc/net/tcp6` dan ditampilkan `ss`, tetapi sering terlewat saat difilter manual.

## Urutan Eksekusi 10 Menit

| Menit | Langkah | Output |
|---|---|---|
| 0–1 | Konteks: jam, hostname, kernel, siapa yang login (`w`, `last`) | `context.txt` |
| 1–3 | Snapshot koneksi keluar, ulangi setelah 60 detik | `net-established.txt`, `net-established-2.txt` |
| 3–6 | Snapshot proses, lalu `/proc/<pid>` untuk kandidat | `ps-full.txt`, `pid-<n>.txt` |
| 6–8 | Cron semua user dan penjadwal sistem | `crontabs-all.txt`, `cron-system.txt` |
| 8–10 | Persistence di luar cron, buat manifest hash | `persistence.txt`, `manifest.sha256` |

## Higiene Bukti

```bash
# Catat seluruh sesi (bila tool tersedia)
script -q -c bash /root/ir-*/session.log

# Manifest hash untuk semua output
cd /root/ir-* && sha256sum ./* > manifest.sha256
```

- Jangan `reboot` atau `shutdown` sebelum snapshot selesai — memory dan socket hilang permanen.
- Jangan menghapus apa pun sebelum eradikasi diputuskan bersama; hapus web shell tanpa memahami cara masuknya hanya mengundang kedatangan kedua.
- Simpan keputusan dan alasannya (contain dulu vs akuisisi dulu) di laporan, bukan hanya di kepala.

## Padanan Windows

| Kebutuhan | Perintah |
|---|---|
| Proses | `Get-CimInstance Win32_Process \| Select-Object ProcessId,ParentProcessId,Name,CommandLine` |
| Scheduled task | `Get-ScheduledTask \| Where-Object State -ne 'Disabled'`; `schtasks /query /fo LIST /v` |
| Koneksi keluar | `Get-NetTCPConnection -State Established \| Select-Object RemoteAddress,RemotePort,OwningProcess`; `netstat -ano` |
| Autorun | `Get-CimInstance Win32_StartupCommand`; Run key registry |
| Service | `Get-CimInstance Win32_Service \| Select-Object Name,PathName,StartMode,State` |

Padanan konsepnya sama: korelasi PID ↔ socket ↔ binary, dan curigai binary yang berjalan dari `%TEMP%`.

## Referensi Terkait

- Urutan volatilitas dan order of volatility: `../../ec-ecih/references/containment-evidence.md`
- File tersembunyi, webshell, dan file tanpa pemilik paket: `hidden-file-hunting.md`
- Akuisisi disk dan memory setelah triage: `digital-forensics.md`
- Containment, eradikasi, dan recovery: `containment-eradication-recovery.md`
- Triase malware dan YARA: `malware-triage.md`
- Query SIEM untuk log yang berkorelasi: `splunk-siem.md`

## Best Practices

- Snapshot dulu, simpulkan kemudian. Satu kali salah `kill` menghapus bukti yang tidak bisa diambil ulang.
- Selalu korelasikan tiga lapis: proses, socket, file. Satu lapis saja mudah dibantah.
- Simpan output ke file dengan hash; triage tanpa artefak tidak bisa dipertahankan di rapat maupun di pengadilan.
- Catat yang normal, bukan hanya yang anomali. Baseline kecil (mis. daftar proses standar satu host) membuat triage berikutnya jauh lebih cepat.
- Perlakukan `environ` dan file kredensial sebagai rahasia sejak detik pertama.
