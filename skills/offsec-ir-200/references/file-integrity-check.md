---
name: "File Integrity Check"
description: "Membuktikan file mana yang diubah penyerang: membaca metadata dengan stat, memverifikasi paket dengan rpm -Va dan dpkg -V, membedakan false positive, dan mendeteksi manipulasi database paket."
tags: [file-integrity, stat, rpm-va, dpkg-verify, debsums, checksum, mtime, ctime, baseline, integrity-monitoring]
---

# File Integrity Check — Apa yang Diubah Penyerang

File paling berbahaya adalah file yang **terlihat normal**: `/usr/bin/ps` yang ditambal agar menyembunyikan proses, `libc` yang memuat hook, atau `sshd_config` yang ditambah satu baris. Mencari berdasarkan nama tidak akan menemukannya — yang membedakan adalah **metadata** dan **hash**.

Dua alat utama, dua pertanyaan berbeda:

| Alat | Menjawab | Cakupan |
|---|---|---|
| `stat` | Kapan dan bagaimana file ini disentuh? | semua file, termasuk yang tidak dipasang paket |
| `rpm -Va` / `dpkg -V` | Apakah isi file menyimpang dari yang tercatat paket? | hanya file milik paket |

Keduanya tidak saling menggantikan. Metadata bisa dipalsukan tanpa menyentuh isi; hash bisa cocok tetapi metadata bohong.

## Decision Frame

1. **Urutkan dari yang termurah.** Metadata sweep hitungan detik, verifikasi paket hitungan menit, hashing penuh hitungan jam. Mulai dari yang murah.
2. **Paket menjawab sebagian.** File baru, file di webroot, dan file tanpa pemilik tidak tercakup `rpm -Va`. Jangan simpulkan "bersih" dari hasil kosong.
3. **Database paket bisa diubah.** Penyerang dengan root dapat memperbarui rpmdb atau status dpkg. Hasil "OK" hanya kuat bila database-nya sendiri tidak dicurigai.
4. **Perbedaan bukan otomatis serangan.** Upgrade, conffile yang diedit admin, dan restore dari backup menghasilkan flag yang sama.
5. **Tanpa baseline, bandingkan dengan paket.** Kalau tidak ada host pembanding, paket resmi adalah baseline paling murah.

## 1. `stat` — membaca metadata dengan benar

```bash
stat file
stat -c 'name=%n size=%s blocks=%b inode=%i links=%h mode=%a owner=%u:%g mtime=%y ctime=%z atime=%x' file
stat -c '%d %i' file          # device + inode: menentukan filesystem dan identitas file
```

Field yang perlu dibaca, bukan sekadar dilihat:

| Field | Arti | Kenapa penting |
|---|---|---|
| `Size` | ukuran logis | berubah tanpa upgrade = isi berubah |
| `Blocks` | blok fisik | `Blocks` 0 dengan `Size` besar = sparse file, mungkin hasil penyalinan aneh |
| `Inode` | nomor inode | berubah walau nama sama = file diganti, bukan diedit |
| `Links` | hardlink count | > 1 pada file yang seharusnya tunggal = ada salinan tersembunyi |
| `Mode` | permission + setuid/sticky | `4755` baru = eskalasi privilege |
| `Uid/Gid` | kepemilikan | binary sistem jadi milik user web adalah anomali berat |
| `Modify` (mtime) | isi terakhir diubah | mudah dipalsukan |
| `Change` (ctime) | metadata terakhir diubah | lebih sulit dipalsukan |
| `Birth` | waktu dibuat | hanya ada di filesystem yang mendukung (xfs, ext4 dengan `newext4`) |

### Apa yang bisa dipalsukan

| Field | Bisa dipalsukan | Catatan |
|---|---|---|
| mtime | mudah | `touch -d '2023-01-01' file` |
| atime | mudah dan tidak reliabel | `relatime`/`noatime` membuat atime hampir tak bermakna |
| ctime | sulit | hanya lewat manipulasi jam sistem atau penyuntingan filesystem langsung |
| mode, owner | mudah (dengan root) | `chmod`, `chown` |
| size | mudah | menimpa isi file |
| inode | tidak | tanpa menyentuh struktur filesystem |
| blocks | tidak langsung | — |

Karena itu, **selisih mtime tua vs ctime baru** adalah sinyal paling berguna: isi diklaim lama, tetapi metadatanya baru disentuh.

### Sweep metadata

```bash
# File yang isinya berubah dalam jendela insiden
find / -xdev -type f -newermt '2026-11-08 00:00' \
  -printf '%TY-%Tm-%Td %TH:%TM %6s %4m %u %p\n' | sort

# ctime baru tetapi mtime lama — metadata disentuh belakangan
find / -xdev -type f -newerct '-3 days' ! -newermt '-3 days' \
  -printf 'mtime=%TY-%Tm-%Td ctime=%CY-%Cm-%Cd %p\n'

# Hardlink tak wajar
find / -xdev -type f -links +1 -printf 'links=%n %p\n' 2>/dev/null
```

Jalankan pada mount yang relevan, bukan hanya `/`. `-xdev` melewatkan tmpfs dan volume lain — lihat `hidden-file-hunting.md`.

## 2. `rpm -Va` — membaca hasil verifikasi paket

```bash
rpm -Va                              # seluruh paket: lambat, tapi menyeluruh
rpm -Va --nofiledigest               # lewati hashing, hanya metadata (lebih cepat)
rpm -V openssh-server                # satu paket
rpm -Vf /usr/bin/ssh                 # paket pemilik file tertentu
rpm -qf /usr/bin/ssh                 # siapa pemiliknya
rpm -q --dump openssh-server | awk '$1 == "/usr/bin/ssh"'   # catatan paket: ukuran, mtime, mode, digest
```

Keluaran `rpm -V` berupa kode 8 karakter diikuti path. Titik berarti lolos; huruf berarti menyimpang:

| Flag | Arti | Prioritas investigasi |
|---|---|---|
| `5` | digest (hash isi) berbeda | **tertinggi** — kode berubah |
| `S` | ukuran berbeda | tinggi — indikasi isi berubah |
| `M` | mode berbeda | tinggi bila setuid bertambah |
| `U` / `G` | owner / group berbeda | tinggi bila binary sistem jadi milik user web |
| `D` | major/minor device berbeda | sedang — file device diganti |
| `L` | target symlink berbeda | tinggi bila menunjuk ke `/tmp` |
| `T` | mtime berbeda | rendah sendiri; sedang bila digabung `5`/`S` |
| `P` | capability berbeda | tinggi — `cap_setuid` pada binary biasa |
| (hilang) | file tidak ada | tinggi untuk file keamanan (`sshd`, `pam`, `sudo`) |

Contoh membaca:

```text
S.5....T.  c /usr/bin/ssh        # isi berubah + ukuran + mtime; flag 'c' = conffile
.M.......  /usr/bin/passwd       # permission berubah — cek apakah setuid bertambah
missing    /etc/pam.d/sshd       # file hilang — sangat mencurigakan
```

### Tiga jebakan `rpm -Va`

1. **Conffile memang berbeda.** File bertanda `c` (mis. `/etc/ssh/sshd_config`) wajar menyimpang setelah admin mengedit. Perlakukan sebagai hipotesis, bukan bukti.
2. **Ada file yang dikecualikan dari verifikasi.** Direktif `%verify(not md5 size mtime)` membuat file tertentu tidak pernah diperiksa. Tidak adanya temuan bukan jaminan.
3. **Database bisa ditambal.** `rpm -Va` membaca `/var/lib/rpm`. Penyerang dapat membangun ulang database setelah mengganti binary. Bandingkan mtime database dengan riwayat transaksi:

```bash
stat -c '%y %s %n' /var/lib/rpm/rpmdb.sqlite
rpm -qa --last | head -20        # transaksi terakhir — harus konsisten dengan mtime DB
```

## 3. `dpkg -V` dan `debsums` — ekuivalen Debian

```bash
dpkg -V                              # checksum + metadata seluruh file paket
dpkg --verify openssh-server         # satu paket
debsums -c 2>/dev/null               # hanya file yang checksum-nya menyimpang
debsums -s openssh-server 2>/dev/null  # senyap: hanya cetak kesalahan
dpkg -S /usr/bin/ssh                 # paket pemilik
dpkg --audit                         # paket yang tidak selesai dipasang
```

`dpkg -V` mencetak baris seperti `??5??????   /usr/bin/passwd`. Artinya: serangkaian penanda status (`?` = tidak ada informasi atau tidak diperiksa, `5` = checksum berbeda), lalu path. Baris `missing` berarti file tidak ada. Untuk arti tiap posisi, `man dpkg` adalah rujukan yang benar — jangan menebak dari urutan huruf.

`debsums -c` adalah cara tercepat mendapat daftar file yang isinya menyimpang dari paket. Cocok dijalankan lebih dulu, baru `dpkg -V` untuk detail metadata.

## 4. Yang tidak dicakup paket — dan justru di situ webshell

`rpm -Va` dan `dpkg -V` hanya tahu file yang dipasang lewat paket. Semua yang berikut tidak akan pernah muncul:

- `/var/www`, `/opt`, `/usr/local`, `/root`, `/home`
- file baru di `/usr/bin` yang tidak dimiliki paket mana pun
- paket yang database-nya sudah dihapus penyerang
- direktori upload, cache framework, dan volume container

Untuk area ini, baseline harus dibuat sendiri:

```bash
# Manifest isi untuk webroot
find /var/www -type f -print0 | xargs -0 sha256sum > /root/ir-*/www.sha256
sha256sum -c /root/ir-*/www.sha256 --quiet    # cocokkan kemudian

# Manifest metadata ringan untuk seluruh sistem
find / -xdev -type f -printf '%p\t%s\t%T@\t%m\t%u:%g\n' 2>/dev/null | sort > /root/ir-*/fs-manifest.tsv
```

Manifest ini juga berfungsi sebagai pembanding antar-host: dua server yang seharusnya identik tetapi manifest-nya berbeda menyempitkan pencarian dengan cepat.

Tool yang memang dirancang untuk ini — AIDE, Tripwire, OpenSCAP, mtree — hanya berguna bila baseline dibuat **sebelum** insiden. Pada insiden mendadak, image atau host saudara lebih realistis dijadikan pembanding.

## 5. Menyatukan temuan: dari flag ke kesimpulan

| Temuan | Kemungkinan | Langkah berikut |
|---|---|---|
| `5` pada binary sistem | binary diganti | bandingkan dengan `/proc/<pid>/exe` bila sedang berjalan; audit paket asli |
| `M` + setuid baru | eskalasi privilege | cari proses yang memakainya; periksa log `sudo`/`auth` |
| `T` saja pada conffile | admin edit atau upgrade | cocokkan dengan timeline perubahan resmi |
| `missing` pada file kemanan | sabotase atau pembersihan | periksa image dan backup; cari pengganti di path lain |
| File di `/usr/bin` tanpa pemilik | ditanam manual | `stat`, `sha256sum`, `strings`, karantina |
| `dpkg -V` bersih tetapi ada proses aneh | file berjalan dari memori atau `/tmp` | lanjut ke `live-response.md` (`/proc/<pid>/exe`) |

Urutan kerjanya: **sweep waktu → curiga satu file → `stat` → verifikasi paket → hash → korelasikan dengan proses dan jaringan**. Jangan menjalankan hashing seluruh disk sebelum sempitkan dengan waktu dan kepemilikan paket.

## False positive

| Temuan | Biasanya normal karena |
|---|---|
| Ratusan file berubah bersamaan | upgrade paket atau patch keamanan |
| `....T` pada `/etc/*.conf` | conffile diedit admin, atau `%config(noreplace)` |
| `U`/`G` berbeda massal | restore dari backup atau migrasi host |
| `dpkg -V` berbeda pada `/var/lib/*` | file state yang memang berubah saat layanan berjalan |
| `missing` pada dokumentasi | paket `-doc` dipangkas untuk menghemat ruang |
| Binary berbeda pada container | image diperbarui, bukan host yang berubah |

## Batas

- Penyerang dengan root dapat mengubah database paket, memalsukan ctime lewat manipulasi jam, atau melakukan bind-mount binary asli saat pemindaian. Untuk kepastian, verifikasi offline dari image.
- Rootkit kernel dapat mengembalikan metadata palsu pada `stat` dan `open`. Semua pembacaan live bisa dibohongi; ini alasan `rpm -Va` bukan bukti akhir.
- `atime` hampir tidak berguna pada sistem modern (`relatime`), jangan dipakai menyimpulkan akses.
- Hashing seluruh filesystem mahal dan mengubah atime. Batasi ke area yang relevan dan catat bahwa pemindaian itu sendiri mengubah metadata.
- `rpm -Va` pada sistem besar bisa memakan puluhan menit dan I/O tinggi; pertimbangkan dampaknya pada layanan produksi.

## Referensi Terkait

- Menemukan file yang disembunyikan: `hidden-file-hunting.md`
- Proses, cron, dan koneksi keluar: `live-response.md`
- Verifikasi offline dari image dan timeline: `digital-forensics.md`
- Eradikasi dan validasi pasca-pembersihan: `containment-eradication-recovery.md`
- Order of volatility dan chain of custody: `../../ec-ecih/references/containment-evidence.md`

## Best Practices

- Mulai dari waktu, bukan dari hash. Sweep `-newermt`/`-newerct` mempersempit dari jutaan file ke puluhan dalam hitungan detik.
- Perlakukan `rpm -Va`/`dpkg -V` sebagai penyaring, bukan hakim. Setiap flag perlu penjelasan dari timeline.
- Simpan keluaran verifikasi ke file dan hash-kan; pemindaian berikutnya butuh pembanding.
- Catat versi paket saat insiden (`rpm -qa`, `dpkg-query -W`) — bila penyerang mengubah database kemudian, catatan ini menjadi bukti.
- Ingat batas cakupan: paket tidak memverifikasi webroot, dan webroot justru tempat webshell biasanya mendarat.
