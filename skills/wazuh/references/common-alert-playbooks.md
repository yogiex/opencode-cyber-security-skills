---
name: "Playbook Alert Wazuh"
description: "Playbook triage per kelas alert Wazuh: SSH dan autentikasi Linux, autentikasi Windows, file integrity monitoring, malware, privilege escalation, serangan web, CVE/SCA, dan perangkat USB — masing-masing dengan bukti, pohon keputusan, eskalasi, dan opsi tuning."
tags: [wazuh, playbook, ssh, brute-force, windows, 4625, fim, syscheck, malware, yara, virustotal, sudo, auditd, web, cve, sca, usb]
---

# Playbook Alert Wazuh

Setiap playbook memakai format: **pemicu → bukti → pohon keputusan → eskalasi → tuning**. Angka rule di bawah adalah contoh rule bawaan yang umum; verifikasi `rule.id` pada instance Anda karena ruleset dapat berubah antar versi.

## 1. SSH / Autentikasi Linux

**Pemicu:** rule 5710 (user tidak valid), 5712 (password salah), 5760/5715, atau `rule.groups: authentication_failed`.

**Bukti:** `data.srcuser`/`data.dstuser`, `data.srcip`, jumlah percobaan per IP, ada/tidak `authentication_success` setelahnya, apakah user ada di sistem.

```text
Ada login sukses dari IP yang sama dalam ±30 menit?
├─ Ya  -> TP (kemungkinan berhasil brute force) -> P1, eskalasi + containment
└─ Tidak
   ├─ IP sumber = scanner/pemantau internal (terverifikasi) -> Benign -> tuning CDB
   ├─ 1-2 percobaan dari IP tak dikenal -> monitor, cek reputasi bila diizinkan -> P3
   └─ Banyak percobaan, tak ada sukses -> TP gagal -> blokir bila kebijakan mengizinkan, P2
```

**Tuning:** whitelist IP scanner lewat CDB list, bukan menurunkan level rule global; atau `frequency`/`timeframe` yang lebih ketat untuk rule korelasi.

## 2. Autentikasi Windows

**Pemicu:** event 4625 berulang, 4624 mencurigakan, 4672 di luar jam kerja, atau rule group `windows`.

**Bukti:** `data.win.system.eventID`, `targetUserName`, `logonType` (2 interaktif, 3 jaringan, 10 RDP), `ipAddress`, `workstationName`; event 4688 pada window sama.

```text
4625 banyak lalu 4624 sukses?
├─ Ya, logonType 3/10 dari host asing -> TP -> P1 (cek lateral movement)
├─ 4672 untuk akun non-admin -> TP -> P1
├─ 4625 dari satu workstation ke banyak akun -> kemungkinan password spray -> P2
└─ 4625 terisolasi, akun diketahui salah password -> FP -> catat, jangan tuning dulu
```

**Tuning:** jangan menonaktifkan 4625; bila noise dari service account, buat rule pengecualian sempit (`if_sid` + `field` user) dan catat alasannya.

## 3. File Integrity Monitoring

**Pemicu:** rule 550 (modified), 553 (deleted), 554 (added), atau `location: syscheck`.

**Bukti:** `syscheck.path`, `syscheck.event`, `syscheck.changed_attributes`, hash, `syscheck.diff` (bila `report_changes="yes"`), `syscheck.audit.*` (bila who-data).

```text
Path termasuk jalur kritikal (biner sistem, kunci SSH, cron, webroot)?
├─ Ya -> cek perubahan tidak terjadwal?
│        ├─ Ada change request/tiket -> Benign
│        └─ Tidak ada -> TP -> P1/P2, cek proses yang menulis
└─ Tidak -> cek pola: berulang tiap deploy?
         ├─ Ya -> tuning terarah (nodiff/ignore path spesifik)
         └─ Tidak -> monitor
```

**Tuning:** `ignore`/`nodiff` untuk path yang benar-benar diketahui berubah rutin (log aplikasi, cache), bukan untuk direktori konfigurasi demi kenyamanan.

## 4. Malware (YARA / VirusTotal / ClamAV)

**Pemicu:** rule group `malware`, `yara`, atau alert integration VirusTotal.

**Bukti:** path, hash, hasil multi-engine (bila tersedia), proses induk, koneksi keluar, apakah file masih ada.

```text
Hash dikenal jahat oleh > 1 engine independen?
├─ Ya -> TP -> P0/P1: isolasi host, eskalasi IR
├─ Ya, tapi file di karantina/backup -> TP tanpa dampak aktif -> P1 (verifikasi)
└─ Tidak / 1 engine saja -> Unknown -> eskalasi L2, jangan hapus bukti
```

**Tuning:** false positive YARA sering berasal dari aturan terlalu generik; perbaiki aturan YARA, bukan menonaktifkan integrasi.

## 5. Privilege Escalation (sudo / auditd)

**Pemicu:** `data.audit.command` mencurigakan, sudo ke root oleh akun tak biasa, 4672, atau rule group `audit_command`.

**Bukti:** `data.audit.exe`, `.command`, `.uid`, `.auid`, `.key`, jam kejadian, riwayat login user.

```text
User berwenang + jam kerja + ada tiket?
├─ Ya -> Benign
└─ Tidak
   ├─ Perintah pengubah sistem (chmod, useradd, setcap, insmod) -> TP -> P1
   └─ Perintah baca saja -> monitor, catat
```

**Catatan:** auditd harus dikonfigurasi untuk menangkap `execve`; tanpa itu, bukti hanya dari sudo log dan tidak lengkap.

## 6. Serangan Web (nginx/Apache/WAF)

**Pemicu:** rule group `web|attack`, `data.url` mencurigakan, atau alert WAF.

**Bukti:** `data.url`, `data.srcip`, status respons, pola payload, apakah ada respons sukses (200), perubahan file setelahnya.

```text
Payload terkirim dan dibalas 200 dengan indikasi eksekusi?
├─ Ya -> TP -> P1 (RCE/LFI/SQLi berhasil)
├─ Diblokir WAF / 403 -> TP gagal -> P3, korelasi IP
└─ Scanner otomatis (user-agent, pola acak) -> P4, catat
```

**Tuning:** jangan whitelist path aplikasi secara luas; sempitkan ke parameter yang memang tidak relevan.

## 7. CVE dan SCA

**Pemicu:** state kerentanan (4.8+) dengan severity critical, atau `data.sca.check.result: failed`.

**Bukti:** `vulnerability.id`, `severity`, `package.name/version`, apakah paket masih terpasang, apakah layanan terekspos (syscollector ports).

```text
CVE critical + layanan terekspos internet?
├─ Ya -> eskalasi patch darurat, P1 (bukan insiden, tetapi risiko tinggi)
├─ Critical tetapi layanan internal/tidak berjalan -> P2
└─ SCA gagal -> temuan kepatuhan -> jalur hardening, bukan triage serangan
```

**Tuning:** SCA hanya mengirim perubahan status; "tidak ada alert SCA" bukan berarti semua check lolos.

## 8. Perangkat USB / Removable

**Pemicu:** rule group `usb` atau `data.audit` untuk mount.

**Bukti:** perangkat, user, waktu, apakah ada penyalinan file (korelasi FIM pada path mount).

```text
Kebijakan organisasi melarang?
├─ Ya, ada penyalinan data -> TP -> P1 (kemungkinan eksfiltrasi)
├─ Ya, tanpa penyalinan -> pelanggaran kebijakan -> P2
└─ Tidak dilarang / perangkat sah -> Benign
```

## Best Practices

- Playbook adalah titik awal, bukan pengganti penalaran; bila fakta tidak cocok dengan cabang mana pun, tulis `Unknown` dan eskalasi.
- Satu playbook per kelas alert menjaga konsistensi antar analis dan shift.
- Setiap tuning yang lahir dari playbook harus menyebut sampel alert dan playbook mana yang memicunya.
- Perbarui playbook ketika rule bawaan berubah setelah upgrade; ID rule bisa bergeser.
