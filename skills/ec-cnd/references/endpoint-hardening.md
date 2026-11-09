---
name: "Endpoint Hardening — Windows, Linux, Mobile, IoT"
description: "Baseline hardening endpoint dari sudut pandang defender: pendekatan baseline dan test ring, hardening Windows/Active Directory, Linux, perangkat mobile lewat MDM, serta penempatan dan pengamanan IoT/OT."
tags: [endpoint, hardening, windows, active-directory, linux, ssh, mdm, iot, cis-benchmark, baseline]
---

# Endpoint Hardening — Windows, Linux, Mobile, IoT

Endpoint adalah tempat data berada dan tempat pengguna mengklik. Perimeter yang rapi tidak menolong bila host di dalamnya menjalankan layanan default, akun lokal bersama, dan patch tertinggal dua tahun.

## 1. Pendekatan baseline

1. **Pilih baseline** — CIS Benchmark, STIG, atau baseline internal; satu sumber, bukan campuran tanpa alasan.
2. **Ukur kondisi awal** — jangan mengubah sebelum tahu selisihnya.
3. **Test ring** — pilot di kelompok kecil, bukan langsung seluruh armada.
4. **Terapkan bertahap** dengan mekanisme pusat (GPO, Intune, Ansible, image).
5. **Catat pengecualian** — aturan yang tidak diterapkan, alasannya, pemilik, tanggal review.
6. **Ukur ulang** — skor kepatuhan tanpa drift check hanyalah foto lama.

Baseline yang tidak pernah diuji ulang akan menyimpang; hardening adalah proses, bukan proyek sekali jalan.

## 2. Windows dan Active Directory

**Host:**

- Patch OS dan aplikasi dengan SLA berdasarkan eksposur, bukan sekadar jadwal bulanan.
- Aktifkan Windows Firewall di semua profil; jangan matikan untuk "mempermudah troubleshooting".
- BitLocker dengan kunci yang dikelola (bukan hanya disimpan di endpoint).
- LAPS untuk akun administrator lokal; akun lokal bersama dilarang.
- PowerShell logging (script block, module, transcription) bila kebijakan mengizinkan.
- ASR/EDR dalam mode block setelah masa monitor; kurangi noise sebelum menyalakan block.
- Nonaktifkan layanan dan protokol legacy yang tidak dipakai (SMBv1, LLMNR, NBT-NS bila memungkinkan).

**Active Directory:**

- Pisahkan tier: Domain Admin tidak login ke workstation pengguna.
- Kurangi anggota privileged groups; review berkala, bukan setahun sekali.
- Kelola `krbtgt` (rotasi terkontrol) dan waspadai delegasi yang tidak perlu.
- Lindungi akun layanan (gMSA), audit SPN yang tidak dipakai.
- Waspadai serangan klasik: Kerberoasting, AS-REP roasting, password spraying — kontrolnya ada di kebijakan dan deteksi, bukan di satu alat.

## 3. Linux

| Area | Kontrol minimum |
|---|---|
| SSH | key-based, `PermitRootLogin no`, batasi user dan sumber, banner, rate limit |
| Akun | tidak ada akun default, `sudo` terbatas dan tercatat, password policy |
| Patch | repositori tepercaya, jadwal, reboot terkendali |
| Layanan | nonaktifkan yang tidak dipakai; ketahui port yang mendengar (`ss -tunlp`) |
| Audit | `auditd` untuk perintah sensitif, file konfigurasi, dan perubahan akun |
| MAC | SELinux enforcing atau AppArmor profile, bukan permissive |
| File | permission ketat pada `/etc`, kunci privat, direktori home |
| Log | syslog/journal terkirim ke pusat, waktu tersinkron (NTP/chrony) |

## 4. Mobile dan MDM

- **Enrollment wajib** untuk perangkat yang mengakses data perusahaan.
- **Pemisahan kerja/pribadi** (work profile/container) untuk BYOD.
- **Enkripsi perangkat** dan **screen lock** sebagai syarat akses.
- **App allowlist** dan larangan sideloading sesuai kebijakan.
- **Remote wipe** hanya untuk data kerja; pahami batas hukum dan privasi.
- **Deteksi root/jailbreak** sebagai sinyal, bukan satu-satunya kontrol.

## 5. IoT dan OT

- **Jangan taruh langsung di internet.** Segmentasi dan akses lewat perantara.
- **Ganti kredensial default** sebelum perangkat dipasang; dokumentasikan.
- **Firmware** diperbarui bila vendor mendukung; bila tidak, kompensasi lewat segmentasi dan monitoring.
- **Monitoring pasif** (flow, DHCP, ARP) untuk perangkat yang tidak bisa diagen.
- **802.1X/MAB** dengan kesadaran bahwa MAB bisa dipalsukan.
- **OT read-only** dari sisi IT; perubahan lewat prosedur dan jendela pemeliharaan.

## 6. Verifikasi

```powershell
# Windows
Get-MpComputerStatus | Select-Object AMServiceEnabled, RealTimeProtectionEnabled
Get-BitLockerVolume | Select-Object MountPoint, ProtectionStatus
Get-LocalUser | Where-Object Enabled -eq $true
Get-NetFirewallProfile | Select-Object Name, Enabled
```

```bash
# Linux
ss -tunlp
sudo sshd -T | grep -Ei 'permitrootlogin|passwordauthentication|pubkeyauthentication'
sudo systemctl list-unit-files --state=enabled
getenforce 2>/dev/null || aa-status
sudo auditctl -l
timedatectl
```

## 7. Kesalahan umum

1. **Hardening langsung ke seluruh armada** — aplikasi legacy mati, lalu kebijakan dicabut total.
2. **Pengecualian tanpa tanggal** — baseline melemah perlahan tanpa ada yang menyadarinya.
3. **Mematikan firewall host** untuk menyelesaikan masalah aplikasi, tanpa mengembalikannya.
4. **Mengandalkan antivirus signature** sebagai satu-satunya kontrol endpoint.
5. **Akun layanan dengan password statis** dan hak berlebih.
6. **EDR mode block tanpa masa monitor** — false positive memutus operasi.
7. **IoT di VLAN default** "karena belum sempat dipindahkan".

## Best Practices

- Satu baseline, satu sumber, satu mekanisme penerapan.
- Ukur, terapkan bertahap, ukur ulang; catat pengecualian.
- Prioritaskan patch berdasarkan eksposur dan eksploitasi nyata.
- Perlakukan tiering admin sebagai kontrol, bukan saran.
- Verifikasi dengan perintah read-only sebelum mengklaim "sudah diperkuat".
