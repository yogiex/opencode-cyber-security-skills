---
name: "Advanced Linux Attacks — Kernel Exploits & Persistence"
description: "Linux exploitation for CPENT including kernel exploit framework, Dirty Pipe (CVE-2022-0847), PwnKit (CVE-2021-4034), cron persistence, LD_PRELOAD abuse, SUID shell escape, and capabilities abuse."
tags: [linux, kernel-exploit, dirty-pipe, pwnkit, persistence, privilege-escalation]
---

# Advanced Linux Attacks

## Kernel Exploit Framework

```bash
# Automated kernel check
./linux-exploit-suggester.sh
./linux-smart-enumeration.sh

# Manual kernel version
uname -a
cat /etc/os-release
```

## Key Attack Vectors

**Dirty Pipe (CVE-2022-0847):** Overwrite read-only files, privesc via /etc/passwd.

**PwnKit (CVE-2021-4034):** pkexec buffer overflow, instant root di banyak versi.

**Cron-based Persistence:** Writable crontab → reverse shell sebagai root.

**LD_PRELOAD Abuse:** Via sudo misconfiguration.

**SUID Shell Escape:** Binary dengan SUID yang bisa spawn shell. Cek GTFOBins.

**Capabilities Abuse:**
- `cap_setuid+ep` → `python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'`
- `cap_dac_override` → baca file restricted
- `cap_sys_admin` → mount, namespace manipulation

## Best Practices

- Di CPENT, kernel exploit BOLEH digunakan — environment biasanya stable
- Cek linux-exploit-suggester sebelum mencoba exploit manual
- Prefer CVE yang sudah mature dan well-tested
- Backup sebelum execute kernel exploit
