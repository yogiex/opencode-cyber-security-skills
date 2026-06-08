---
name: "Eradication & Recovery"
description: "Eradication vs containment, eradication strategies (clean/rebuild/replace), step-by-step eradication, persistence mechanisms (Windows, Linux, Cloud), eradication verification, common mistakes, recovery decision framework, recovery sequence, monitoring checklist, rollback plans, and recovery validation."
tags: [ecih, eradication, recovery, persistence, malware-removal, backup-restore, post-compromise]
---

## Eradication — Removing the Threat

### Esensi Eradication

Eradication adalah **proses menghilangkan root cause dan semua artifact insiden dari lingkungan**. Containment menghentikan penyebaran, eradication membersihkan.

### Eradication vs Containment

```
Containment:  "Stop the bleeding" — tindakan sementara
Eradication:  "Heal the wound" — solusi permanen
```

Eradication TIDAK boleh dilakukan sebelum:
1. Evidence sudah dikumpulkan (jangan bersihkan bukti)
2. Root cause sudah diidentifikasi (jangan hanya treat symptom)
3. Scope sudah diketahui (jangan bersihkan hanya satu titik)
4. Containment sudah berhasil (jangan eradication di lingkungan yang masih aktif)

### Eradication Strategy

| Strategi | Deskripsi | Cocok Untuk |
|----------|-----------|-------------|
| **Clean** | Remove malware, close backdoor, patch | Infeksi ringan, root cause jelas |
| **Rebuild** | Reimage sistem dari golden image | Kompromi berat, root cause tidak jelas |
| **Replace** | Ganti dengan hardware/instance baru | Hardware compromised, cloud |
| **Patch** | Tutup vulnerability | Exploit via vulnerability |
| **Restore from backup** | Kembalikan ke state sebelum insiden | Data corruption, ransomware |
| **Reconfigure** | Perbaiki konfigurasi | Misconfiguration, policy bypass |

Pertimbangkan: **Clean vs Rebuild** adalah keputusan besar.

| Aspek | Clean | Rebuild |
|-------|-------|---------|
| **Kecepatan** | Lebih cepat | Lebih lambat |
| **Kepastian** | Kurang yakin bersih | Yakin bersih |
| **Resource** | Lebih murah | Lebih mahal |
| **Evidence** | Bisa merusak evidence | Evidence sudah diambil |
| **Root cause** | Bisa dipelajari | Root cause harus sudah diketahui |

### Langkah-langkah Eradication

1. **Identify root cause**: Bagaimana attacker masuk pertama kali?
2. **Identify all persistence**: Scheduled tasks, services, registry, startup items, cron, systemd
3. **Identify backdoors**: New accounts, SSH keys, web shells, reverse shells
4. **Identify C2 mechanisms**: Beaconing, DNS tunneling, domain fronting
5. **Remove all artifacts**: Files, registry keys, processes, services
6. **Patch vulnerability**: Fix the root cause
7. **Change compromised credentials**: All passwords, tokens, keys
8. **Verify eradication**: Scan for IOCs, check for persistence

### Common Persistence Mechanisms

**Windows**:
| Mechanism | Detection |
|-----------|-----------|
| Registry Run keys | Autoruns, Sysinternals |
| Scheduled tasks | schtasks, event log |
| Service installation | services.msc, sc query |
| Startup folder | Shell:startup |
| WMI persistence | wmic, WMI Explorer |
| DLL hijacking | Process Monitor |
| Bootkit/MBR | Secure Boot check |
| Group Policy | GPMC |
| Active Directory | ADSI Edit |

**Linux**:
| Mechanism | Detection |
|-----------|-----------|
| Cron jobs | crontab -l, /etc/cron* |
| systemd services | systemctl list-units |
| .bashrc / .profile | Check user home dirs |
| SSH authorized_keys | ~/.ssh/authorized_keys |
| LD_PRELOAD | Check environment |
| Kernel modules | lsmod |
| Web shells | Web server logs, file scan |
| init.d / rc.local | Check rc scripts |

**Cloud**:
| Mechanism | Detection |
|-----------|-----------|
| IAM backdoor users | Cloud trail, IAM audit |
| Access keys | IAM last used |
| Lambda persistence | Cloud trail |
| API Gateway | API logs |
| Container escape | Audit logs |
| Service meshes | mTLS audit |

### Eradication Verification

Setelah eradication, verifikasi:
1. **Scan ulang** — Full AV/EDR scan, YARA rules, custom IOC scan
2. **Log review** — Pastikan tidak ada aktivitas mencurigakan setelah eradication
3. **Persistence check** — Periksa semua persistence mechanisms
4. **Network monitoring** — Pantau C2 communication
5. **User activity** — Periksa user accounts yang terlibat
6. **Timeline analysis** — Pastikan semua activity berhenti di titik eradication

### Common Eradication Mistakes

| Mistake | Dampak | Pencegahan |
|---------|--------|------------|
| **Hanya hapus malware tanpa patch** | Re-infection | Fix root cause |
| **Lupa backdoor user** | Attacker masuk lagi | Full account audit |
| **Hanya bersihkan satu endpoint** | Lateral movement | Full scope eradication |
| **Skip verification** | False sense of security | Always verify |
| **Hapus evidence** | Legal implications | Evidence sudah dikumpulkan |
| **Restore dari backup terkompromi** | Re-infection | Verify backup is clean |

---

## Recovery — Restoring Operations

### Esensi Recovery

Recovery adalah **proses mengembalikan sistem ke operasi normal** setelah eradication selesai. Recovery bukan hanya "nyalakan lagi" — tapi memastikan sistem kembali dengan aman, dimonitor ketat, dan siap didukung.

### Recovery Decision Framework

```
Apakah root cause sudah diidentifikasi?
  ├── Tidak → Kembali ke Eradication
  └── Ya → Lanjut
          
Apakah eradikasi sudah diverifikasi?
  ├── Tidak → Lakukan verifikasi dulu
  └── Ya → Lanjut
          
Apa sumber recovery?
  ├── Rebuild from golden image → Paling aman
  ├── Restore from backup → Verifikasi backup bersih
  └── Clean existing system → Risiko residual terbesar
          
Bagaimana urutan recovery?
  ├── Non-critical → Critical (progressive)
  ├── Read-only → Read-write (by risk)
  └── Isolated → Connected (by trust)

Apakah monitoring diperketat?
  ├── Tidak → Jangan recovery dulu
  └── Ya → Lanjut recovery
```

### Recovery Types

| Type | Deskripsi | Cocok Untuk |
|------|-----------|-------------|
| **Rebuild from golden image** | OS + aplikasi dari image bersih | Full compromise |
| **Restore from backup** | Data dari backup pra-insiden | Ransomware, data corruption |
| **Automated recovery** | Infrastructure as Code deploy | Cloud, container |
| **Manual recovery** | Step-by-step reconfiguration | Simple systems |
| **Hot standby failover** | Switch to DR site | Critical systems |
| **Gradual recovery** | Per-service recovery | Complex environments |

### Recovery Sequence

1. **Non-critical systems first** — Test recovery process di lingkungan non-kritis
2. **Read-only systems** — Pastikan tidak ada write-back ke sistem yang belum clean
3. **Isolated validation** — Nyalakan di network terisolasi, validasi functionality
4. **Monitor intensif** — Aktifkan monitoring ekstra, pantau anomali
5. **Connect carefully** — Hubungkan ke production network secara bertahap
6. **User access restoration** — Kembalikan akses user setelah konfirmasi aman
7. **Full operation** — Kembali ke operasi normal
8. **Continued monitoring** — Pantau untuk residual activity

### Recovery Monitoring Checklist

| Monitor | What to Look For |
|---------|-----------------|
| **Authentication** | Anomalous logins, privilege escalation |
| **Network** | Unexpected outbound connections, data transfer |
| **Process** | Unknown processes, unusual parent-child |
| **File system** | New files in unusual locations |
| **Registry/Config** | Unexpected changes |
| **User activity** | Abnormal behavior |
| **Performance** | Unusual CPU/memory/disk |
| **DNS** | Queries to known-bad domains |

### Rollback Plan

Setiap recovery harus punya rollback plan:
1. **Jika monitoring mendeteksi anomali** → Apa yang dilakukan?
2. **Jika sistem tidak stabil** → Kapan kembali ke backup?
3. **Jika user melapor masalah** → Siapa yang handle?
4. **Jika compliance tidak terpenuhi** → Siapa yang approve?

### Recovery Validation

Setelah recovery:
- **Functional validation**: Apakah sistem bekerja normal?
- **Security validation**: Apakah monitoring menunjukkan aktivitas bersih?
- **Compliance validation**: Apakah kontrol keamanan masih berfungsi?
- **Performance validation**: Apakah performa normal?
- **Data integrity validation**: Apakah data akurat dan lengkap?
