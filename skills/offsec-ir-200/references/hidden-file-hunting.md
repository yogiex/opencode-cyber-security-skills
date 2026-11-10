---
name: "Hidden File Hunting"
description: "Menemukan file dan direktori yang disembunyikan di server Linux: nama aneh, lokasi tak lazim, atribut waktu dan permission, file yang tidak diakui paket, trik rootkit, selisih ruang disk, dan webshell di webroot."
tags: [hidden-files, hunting, webshell, persistence, dotfiles, rootkit, timeline, file-integrity, df-du, linux]
---

# Hidden File Hunting

Mencari file tersembunyi bukan soal menghafal `-name '.*'`. File jarang benar-benar tak terlihat — ia hanya tidak terlihat oleh **perintah yang kita pakai**. Karena itu, mulailah dengan tiga pertanyaan yang menutup semua celah:

1. **Apakah saya melihat semua nama?** Dotfile, nama berspasi, nama berisi karakter kontrol.
2. **Apakah saya melihat semua lokasi?** tmpfs, mount lain, direktori yang ditimpa bind mount.
3. **Apakah saya melihat semua atribut?** Waktu, permission, kepemilikan, atribut filesystem, kepemilikan paket.

Kalau satu pertanyaan belum dijawab, "tidak ada file mencurigakan" belum bisa disimpulkan.

## Decision Frame

1. **Live atau image?** Selama host hidup, rootkit bisa membohongi `ls`, `find`, bahkan `ps`. Untuk kepastian, ambil image dan periksa offline (lihat `digital-forensics.md`).
2. **Cari berdasarkan apa?** Nama mudah dipalsukan. Waktu, kepemilikan paket, dan hash lebih sulit — prioritaskan itu.
3. **Jangan mengubah apa pun saat mencari.** `chattr`, `mv`, `rm` merusak bukti; salin dulu, tindakan kemudian.
4. **Selisih kecil itu normal.** `df` vs `du` berbeda karena reserved block dan journal; hanya selisih besar yang berarti.
5. **Temuan harus bisa dijelaskan.** File aneh tanpa korelasi waktu, proses, atau jaringan adalah kandidat, bukan kesimpulan.

## 1. Nama: dotfile, spasi, newline, escape

`ls` biasa menyembunyikan dotfile, memotong nama panjang, dan — yang paling berbahaya — menampilkan karakter kontrol apa adanya. Nama file berisi escape ANSI bisa memalsukan output terminal atau menimpa baris di layar Anda.

```bash
# Listing aman: escape karakter kontrol, kutip gaya shell
LC_ALL=C ls -lab --quoting-style=shell-escape

# Termasuk nama yang berisi newline
find . -maxdepth 1 -mindepth 1 -print0 | xargs -0 -r ls -ldb

# Semua dotfile di luar /proc /sys /dev
find / -xdev \( -path /proc -o -path /sys -o -path /dev \) -prune -o -type f -name '.*' -print

# Nama dengan spasi di awal atau akhir
find / -xdev \( -name ' *' -o -name '* ' \) -print

# Nama berisi karakter kontrol (termasuk newline)
find / -xdev -regextype posix-extended -regex '.*[[:cntrl:]].*' -print
```

- Nama berawalan `-` akan dibaca `rm`/`cat` sebagai opsi. Selalu pakai `--` atau awali `./`.
- Membaca isi file bernama aneh: `cat -- "$file"`, dan sudah escape-kan namanya lebih dulu dengan `printf '%q\n'`.
- `find` tidak bisa mencocokkan NUL di nama file, tetapi newline dan tab bisa.

## 2. Lokasi: mount yang sering terlewat

File yang "hilang" sering ada di filesystem lain — tmpfs yang tidak ikut `-xdev`, atau direktori yang ditimpa `mount --bind`.

```bash
findmnt -rno TARGET,FSTYPE,OPTIONS
df -hT

# Enumerasi per mount: tmpfs di /dev/shm, /run, /run/user/* tidak tersentuh oleh -xdev pada /
findmnt -rno TARGET | while read -r t; do
  case "$t" in /proc|/sys|/dev) continue;; esac
  find "$t" -xdev -type f -newermt '-3 days' 2>/dev/null
done
```

Lokasi yang layak diperiksa lebih dulu:

| Lokasi | Kenapa |
|---|---|
| `/dev/shm`, `/run`, `/run/user/*` | tmpfs, hilang saat reboot, tidak terlihat di `du` biasa |
| `/var/tmp` | seperti `/tmp` tetapi bertahan setelah reboot |
| `/lost+found` | nama file bisa tidak bermakna; jarang diperiksa |
| `/var/www/**/uploads`, `storage/`, `var/cache` | direktori writable, tempat webshell mendarat |
| `/root/.cache`, `/root/.local` | ruang kerja yang tidak pernah dibersihkan |
| `/var/lib/docker`, `/var/lib/containerd` | layer image dan volume, jalur host ≠ jalur container |

Periksa juga **direktori yang ditimpa**. Penyerang dengan root bisa `mount --bind` direktori lain di atas path yang sah, sehingga isi asli tak terlihat:

```bash
cat /proc/self/mountinfo | awk '{print $5}' | sort | uniq -c | sort -rn | head
```

Nama direktori yang muncul berulang sebagai mount point adalah kandidat kuat. Bandingkan dengan isi direktori setelah mount dilepas (dari image, bukan dari host hidup).

## 3. Atribut: waktu, permission, capability, xattr

```bash
# File yang berubah dalam jendela insiden
find / -xdev -type f -newermt '2026-11-01 00:00' ! -newermt '2026-11-10 00:00' \
  -printf '%TY-%Tm-%Td %TH:%TM %10s %p\n' | sort

# ctime (metadata) — lebih sulit dipalsukan daripada mtime
find / -xdev -type f -cnewermt '-2 days' -printf '%TY-%Tm-%Td %TH:%TM %p\n'

# setuid/setgid, world-writable, capability
find / -xdev -perm -4000 -type f -printf '%m %u %p\n' 2>/dev/null
find /var/www -xdev -perm -0002 -type d -printf '%m %u %p\n' 2>/dev/null
getcap -r / 2>/dev/null

# Atribut filesystem: immutable (i) dan append-only (a)
lsattr -R /var/www 2>/dev/null | grep -E '^[^ ]*[ia][^ ]* '
getfattr -R -d -m - /var/www 2>/dev/null | head -40
getfacl -R /var/www 2>/dev/null | grep -E '^(user|group):[^:]+:'

# File yatim: UID/GID tidak punya akun
find / -xdev \( -nouser -o -nogroup \) -printf '%u:%g %p\n' 2>/dev/null
```

Kenapa ini penting:

- `touch -d` bisa memalsukan **mtime**, tetapi mengubah metadata ikut memperbarui **ctime**. Selisih besar antara mtime tua dan ctime baru adalah sinyal klasik.
- `chattr +i` membuat file tidak bisa dihapus atau diubah — dipakai penyerang agar webshell-nya bertahan, dan dipakai defender untuk melindungi bukti. Daftar file immutable di webroot hampir selalu layak dipertanyakan.
- `setuid` di `/tmp` atau di direktori writable adalah eskalasi privilege yang menunggu dipakai.
- File dengan UID yang tidak punya akun (`-nouser`) sering sisa akun yang dihapus setelah dipakai.

## 4. Kepemilikan paket: file yang tidak diakui siapa pun

Cara paling efisien memisahkan "file sistem normal" dari "sesuatu yang baru" adalah bertanya kepada manajer paket. File yang tidak dimiliki paket mana pun di direktori sistem adalah kandidat utama.

```bash
# Integritas paket terpasang
dpkg -V 2>/dev/null | head -50        # Debian/Ubuntu
rpm -Va 2>/dev/null | head -50        # RHEL/CentOS

# File di direktori sensitif yang tidak diakui paket
for d in /usr/local/bin /usr/local/sbin /etc/systemd/system /usr/lib/systemd/system /etc/cron.d /etc/init.d; do
  find "$d" -xdev -type f 2>/dev/null | while read -r f; do
    dpkg -S "$f" >/dev/null 2>&1 || rpm -qf "$f" >/dev/null 2>&1 || printf 'UNOWNED %s\n' "$f"
  done
done
```

Batalkan anggapan "ada di `/usr/bin` berarti resmi". Malware rutin menaruh dirinya di `/usr/bin`, `/usr/sbin`, atau `/usr/lib` justru karena tempat itu tidak pernah dicurigai. Untuk membaca hasil verifikasi paket secara rinci — arti tiap flag, konffile yang wajar menyimpang, dan manipulasi database paket — lihat `file-integrity-check.md`.

## 5. Ketika file tidak muncul di daftar sama sekali

`ls` dan `find` sama-sama membaca direktori lewat `getdents`. Rootkit yang mem-patch `readdir` akan menyembunyikan file dari **keduanya**, jadi membandingkan `ls` dengan `find` tidak membuktikan apa-apa. Yang benar adalah membandingkan dengan sumber independen.

```bash
# 1. Selisih ruang: file tersembunyi dan file terhapus yang masih dibuka memakan blok
df -k / | awk 'NR==2 {print "df  used (KiB):", $3}'
du -xsk / 2>/dev/null | tail -1 | awk '{print "du  seen (KiB):", $1}'

# 2. File terhapus yang masih dibuka proses (link count 0)
lsof +L1 2>/dev/null | head -40

# 3. Sumber independen: baca struktur direktori langsung dari device (ext4)
debugfs -R 'ls -l /var/www' <dev> 2>/dev/null | tail -n +2
```

- `debugfs` pada filesystem yang sedang di-mount read-write **tidak aman**; lakukan pada snapshot atau image (lihat `digital-forensics.md`).
- Selisih `df` vs `du` sebesar 5–10% normal (reserved block, journal, metadata). Selisih puluhan persen, atau selisih yang persis seukuran file terhapus, baru bermakna.
- `lsof +L1` menampilkan file yang sudah tidak punya nama tetapi masih terbuka — jalur favorit menyimpan payload yang tidak terlihat `ls`.
- Tool bantu: `unhide quick`, `unhide sys`, `rkhunter --check --sk`, `chkrootkit -q`. Semuanya punya false positive; jadikan pemicu pemeriksaan manual, bukan vonis.

Rootkit berbasis `LD_PRELOAD` menyembunyikan file tanpa menyentuh kernel:

```bash
cat /etc/ld.so.preload 2>/dev/null
grep -l 'LD_PRELOAD' /proc/*/environ 2>/dev/null
dpkg -V libc6 2>/dev/null | head        # hash libc berbeda dari paket = kandidat hook
```

## 6. Isi: cari makna, bukan nama

Webshell jarang bernama `shell.php`. Cari berdasarkan isi dan konteks.

```bash
# Pola webshell umum di webroot
grep -rIl --exclude-dir={proc,sys,dev} \
  -E 'eval\(\$_|base64_decode\(|shell_exec\(|passthru\(|assert\(\$_|preg_replace\(.*/e' /var/www

# File yang diubah dalam 7 hari terakhir
find /var/www -type f -mtime -7 -printf '%TY-%Tm-%Td %TH:%TM %p\n' | sort

# Gambar yang sebenarnya PHP atau ELF
find /var/www -type f \( -name '*.jpg' -o -name '*.png' -o -name '*.ico' \) -print0 \
  | xargs -0 -r file | grep -iE 'php|ELF'

# Ekstensi yang tetap dieksekusi sebagai PHP
find /var/www -type f \( -name '*.phtml' -o -name '*.phar' -o -name '*.inc' -o -name '*.php.*' \)
```

Yang sering terlewat di webroot:

| File | Kenapa berbahaya |
|---|---|
| `.user.ini` | `auto_prepend_file` menjalankan kode PHP di setiap request |
| `.htaccess` | mengubah handler, menyembunyikan akses, atau mengaktifkan CGI |
| `.env`, `.git/config` | kredensial dan riwayat yang bisa dipulihkan penyerang |
| `index.php.bak`, `config.php~` | kode lama dengan kredensial, sering diabaikan developer |
| `uploads/.htaccess` | membalikkan `php_flag engine off` yang dipasang defender |

Perlakukan setiap file baru di direktori writable sebagai tersangka sampai terbukti sebaliknya.

## 7. Timeline: urutkan, jangan tebak

```bash
# Daftar file dalam jendela waktu, urut kronologis
find / -xdev -type f -newermt '2026-11-08 00:00' \
  -printf '%T@ %TY-%Tm-%Td %TH:%TM:%TS %p\n' 2>/dev/null | sort -n | tail -60

# Timeline lengkap dari image (Sleuth Kit), termasuk file terhapus
fls -r -m / -o 2048 evidence.dd > body.txt
mactime -b body.txt -d 2026-11-01..2026-11-10 > timeline.csv
```

Timeline dari image lebih dipercaya karena memuat entri terhapus dan tidak bisa dibohongi rootkit userland. Cocokkan jam file dengan jam log (`syslog`, access log) — perbedaan zona waktu adalah penyebab kesalahan korelasi paling umum.

## Checklist 15 Menit

| Menit | Langkah | Perintah kunci |
|---|---|---|
| 0–2 | Semua mount dan tmpfs | `findmnt -rno TARGET,FSTYPE` |
| 2–5 | Dotfile dan nama aneh di area sensitif | `find /var/www /etc /usr/local -name '.*'` |
| 5–8 | File baru dalam jendela insiden | `find / -xdev -newermt '<tgl>'` |
| 8–11 | File tak diakui paket | `dpkg -V`, loop `dpkg -S` |
| 11–13 | Webshell dan `.user.ini` | `grep -rIl 'eval(\$_' /var/www` |
| 13–15 | Selisih ruang dan file terhapus terbuka | `df` vs `du`, `lsof +L1` |

## False positive

| Temuan | Biasanya normal karena |
|---|---|
| `.well-known/`, `.git/`, `.env` | konvensi framework dan standar ACME |
| `dpkg -V` melaporkan file berubah | conffile yang diedit admin, atau paket di-upgrade tanpa restart |
| `lsof +L1` berisi banyak file | rotasi log — syslog/nginx masih memegang file lama |
| `df` vs `du` berbeda | reserved block, journal, overlayfs, snapshot |
| `setuid` di `/usr/bin` | `passwd`, `sudo`, `mount`, `su` memang setuid |
| File immutable di `/etc` | dikonfigurasi sengaja oleh admin atau CIS hardening |
| `-nouser` | sisa paket yang dihapus, bukan bukti kompromi |

## Batas

- **Rootkit kernel (LKM/eBPF)** bisa menyembunyikan file dari semua tool userland. Satu-satunya jawaban: image dan pemeriksaan offline.
- `debugfs` hanya untuk ext2/3/4. XFS memakai `xfs_db`, Btrfs memakai `btrfs inspect-internal`; keduanya lebih terbatas.
- File terenkripsi atau terkompresi (`.zip`, `.gz`, arsip bertumpuk) harus dibuka di lingkungan terisolasi, bukan di host yang diperiksa.
- Semua teknik di sini **membaca**. Jangan `chattr`, `mv`, atau `rm` sebelum eradikasi diputuskan bersama.

## Referensi Terkait

- Triase proses, cron, dan koneksi keluar: `live-response.md`
- Image disk, timeline offline, dan debugging filesystem: `digital-forensics.md`
- Eradikasi dan validasi pasca-pembersihan: `containment-eradication-recovery.md`
- YARA untuk file yang sudah dikarantina: `malware-triage.md`
- Order of volatility dan chain of custody: `../../ec-ecih/references/containment-evidence.md`

## Best Practices

- Tanyakan tiga hal setiap kali: semua nama, semua lokasi, semua atribut. Satu perintah tidak pernah cukup.
- Prioritaskan pencarian berdasarkan waktu dan kepemilikan paket, bukan nama — nama itu gratis untuk dipalsukan.
- Simpan daftar hasil ke file dan hash-kan, sama seperti artefak lain.
- Bandingkan selalu dengan baseline: paket, image, atau host lain yang setara. Tanpa pembanding, "aneh" hanya opini.
- Setelah menemukan satu webshell, cari **semua** file yang dibuat pada menit yang sama. Penyerang jarang menanam satu file saja.
