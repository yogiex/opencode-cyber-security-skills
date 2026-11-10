---
name: "Linux Attacks — Kernel, Privilege Escalation & Container Escape"
description: "Eksploitasi Linux untuk operator berpengalaman: enumerasi lokal, eskalasi lewat sudo/SUID/capabilities/cron, kernel CVE (Dirty Pipe, PwnKit), persistence yang terkendali, dan escape dari container (docker socket, privileged, hostPath)."
tags: [linux, privilege-escalation, kernel-exploit, suid, capabilities, container-escape, persistence]
---

# Linux Attacks

Linux privesc hampir selalu soal konfigurasi, bukan soal CVE. Kernel exploit adalah opsi terakhir: berisiko mematikan host, sulit diprediksi, dan sering tidak perlu.

## 1. Enumerasi lokal

```bash
uname -a; cat /etc/os-release
id; sudo -l
find / -perm -4000 -type f 2>/dev/null
getcap -r / 2>/dev/null
crontab -l; ls -la /etc/cron.*; systemctl list-timers
ps aux --sort=-%cpu | head
ss -tunlp
docker ps 2>/dev/null; ls -l /var/run/docker.sock
env; cat ~/.bash_history
```

Kalau target mengizinkan upload, `linpeas.sh` mempercepat, tetapi hasilnya tetap harus diverifikasi satu per satu.

## 2. Jalur eskalasi yang paling sering berhasil

| Jalur | Yang dicari | Aksi |
|---|---|---|
| sudo | Entri NOPASSWD, wildcard, binary yang bisa spawn shell | `sudo -l`, GTFOBins |
| SUID | Binary SUID yang punya escape | GTFOBins untuk parameter |
| Capabilities | `cap_setuid`, `cap_dac_override`, `cap_sys_admin` | Eksploitasi sesuai kapabilitas |
| Cron | Script yang writable, PATH, wildcard | Tulis payload, tunggu jadwal |
| LD_PRELOAD | `env_keep+=LD_PRELOAD` di sudoers | Library jahat saat sudo |
| Service | Unit writable, `EnvironmentFile` | Ganti `ExecStart` |
| Kredensial | `.git-credentials`, config, backup, history | Reuse ke host lain |

**Capabilities contoh:**

```bash
# cap_setuid pada python/perl → root
python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'
# cap_dac_override → baca file terlarang
```

## 3. Kernel CVE

| CVE | Nama | Target | Catatan |
|---|---|---|---|
| CVE-2022-0847 | Dirty Pipe | Kernel 5.8+ | Overwrite file read-only |
| CVE-2021-4034 | PwnKit | polkit `pkexec` | Sangat luas, relatif stabil |
| CVE-2016-5195 | Dirty COW | Kernel lama | Race condition, rapuh |
| CVE-2021-3493 | OverlayFS | Ubuntu | Perlu unprivileged user namespace |

Sebelum menjalankan kernel exploit: catat versi kernel, cek apakah host punya snapshot/rollback, dan siapkan rencana jika host panic. Kernel exploit yang membuat host down adalah temuan, bukan kemenangan.

## 4. Persistence yang terkendali

Persistence hanya dipakai bila RoE mengizinkan, dan wajib didokumentasikan untuk dibersihkan:

- cron / systemd timer milik root
- `authorized_keys` baru
- `LD_PRELOAD` lewat `/etc/ld.so.preload`
- user baru dengan shell valid
- service unit baru

Setiap mekanisme yang dipasang harus punya catatan: di host mana, file apa, cara menghapusnya.

## 5. Container dan orchestrator

| Kondisi | Escape |
|---|---|
| `/var/run/docker.sock` ter-mount | `docker run -v /:/host` |
| Container privileged | Mount host, akses device |
| `hostPath`/`hostPID` | Baca proses host, nsenter |
| cgroup v1 writable | `release_agent` |

```bash
# docker.sock
docker -H unix:///var/run/docker.sock ps
docker -H unix:///var/run/docker.sock run -v /:/host -it alpine chroot /host
```

Kubernetes: cek service account token, RBAC (`kubectl auth can-i --list`), secret yang ter-mount, dan pod yang bisa membuat pod baru dengan hostPath.

## 6. Jebakan

1. **Kernel exploit di produksi** — risiko panic tinggi; snapshot dulu atau pilih jalur konfigurasi.
2. **Persistence tanpa izin** — melanggar RoE dan menyulitkan pembersihan.
3. **GTFOBins buta** — tidak semua binary di daftar punya parameter yang sama di versi target.
4. **cron timezone** — jadwal bisa jauh lebih lambat dari perkiraan.
5. **Root di container ≠ root di host** — user namespace memetakan berbeda.

## 7. Best Practices

- Enumerasi konfigurasi dulu, kernel CVE belakangan.
- Satu jalur, satu bukti: `id` dan `hostname` di frame yang sama.
- Kernel exploit terakhir, dengan persetujuan dan rencana rollback.
- Persistence seminimal mungkin, selalu dengan catatan pembersihan.
- Bersihkan artefak sebelum keluar; sisa backdoor adalah temuan baru.
