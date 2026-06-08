---
name: "Digital Forensics Reference"
description: "Disk forensics with Autopsy and FTK Imager, memory forensics with Volatility 3, forensic artifacts, and evidence handling procedures."
tags: [autopsy, volatility, ftk-imager, forensics, memory-analysis, disk-forensics, evidence]
---

# Digital Forensics Reference

## Evidence Handling

**Order of Volatility (RFC 3227):**
1. CPU registers, cache
2. RAM (memory dump)
3. Network connections
4. Running processes
5. Disk (forensic image)
6. Archive/backup

**Chain of Custody:** Who → What → When → Where → How → Why

**Write blockers:** Hardware write blocker untuk imaging

## Disk Imaging

```
FTK Imager: GUI-based, supports E01/raw
dd: Linux CLI, bit-for-bit copy
  dd if=/dev/sda of=evidence.dd bs=4M conv=noerror,sync
Guymager: Linux GUI imager with hash verification
```

## Disk Forensics with Autopsy

**Autopsy Workflow:**
```
1. Create Case: Name, number, examiner
2. Add Data Source: Disk image (dd/E01/VMDK/VHD)
3. Configure Ingest Modules:
   - Recent Activity (browser, documents)
   - Hash Lookup (NSRL known-good, known-bad)
   - File Type Identification (magic bytes)
   - Keyword Search (full-text index)
   - Extension Mismatch Detector
4. Manual Analysis:
   - File system tree + deleted files (marked with X)
   - Keyword hits review
   - Timeline analysis (Tools → Timeline)
   - Tag evidence (Evidence-Critical, Supporting)
5. Generate Report: HTML/Excel/Text
```

**Key Autopsy Ingest Modules:**
```
Recent Activity: Browser history, downloads, cookies
Hash Lookup: Compare against NSRL (NIST known-good) + known-bad
File Type Identification: Magic byte signature matching
Keyword Search: Index content for full-text search
Extension Mismatch Detector: Find file rename attempts
Email Parser: PST, MBOX, EML extraction
Exif Parser: Image metadata (GPS, timestamps)
Encryption Detection: Find encrypted files/containers
Interesting Files Identifier: Custom rule-based flagging
Picture Analyzer: Image categorization
Data Source Integrity: Verify image hash
```

**Sleuth Kit CLI Commands:**
```bash
# Verify image
img_stat evidence.dd

# Partition layout
mmls evidence.dd

# List files (with deleted)
fls -r -o 2048 evidence.dd

# Recover file by inode
icat -o 2048 evidence.dd 14523 > recovered.doc

# Generate timeline bodyfile
fls -r -m "/" -o 2048 evidence.dd > bodyfile.txt
mactime -b bodyfile.txt -d > timeline.csv

# Search file signatures
sigfind -o 2048 evidence.dd 25504446  # PDF header
```

## Memory Forensics with Volatility 3

**Essential Volatility 3 Commands:**
```bash
# Identify system
vol -f memory.raw windows.info

# List processes
vol -f memory.raw windows.pslist
vol -f memory.raw windows.pstree
vol -f memory.raw windows.psscan       # Finds hidden processes

# Command lines
vol -f memory.raw windows.cmdline
vol -f memory.raw windows.cmdline --pid 1234

# Network
vol -f memory.raw windows.netscan
vol -f memory.raw windows.netstat

# Malware detection
vol -f memory.raw windows.malfind       # Injected code / RWX regions
vol -f memory.raw windows.malfind --dump
vol -f memory.raw windows.apihooks      # API hook detection
vol -f memory.raw windows.ssdt          # SSDT hook detection

# Process details
vol -f memory.raw windows.dlllist --pid 1234
vol -f memory.raw windows.modules
vol -f memory.raw windows.handles --pid 1234
vol -f memory.raw windows.cmdline --pid 1234

# Registry
vol -f memory.raw windows.registry.hives
vol -f memory.raw windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"

# Dump artifacts
vol -f memory.raw windows.dumpfiles --pid 1234
vol -f memory.raw windows.memmap --pid 1234 --dump

# Timeline
vol -f memory.raw timeliner.Timeliner
```

**Memory Analysis Workflow:**
```
1. Identify profile: windows.info
2. Process list: windows.pslist + windows.psscan — compare for hidden
3. Process tree: pstree — unusual parent-child
4. Command line: cmdline — encoded PowerShell, suspicious args
5. Injected code: malfind — process injection indicators
6. Network: netscan — C2 connections from suspicious PIDs
7. Dump: dumpfiles on suspicious processes → malware analysis
```

**Suspicious Process Indicators:**
- **Hidden process**: In psscan but NOT in pslist → DKOM manipulation
- **No parent**: process with PPID 0 or orphaned
- **Suspicious path**: Running from `C:\Users\*\AppData\Local\Temp\`, `C:\Windows\Temp\`
- **Mismatched name**: `svchost.exe` in wrong path
- **RWX memory**: `malfind` shows executable + writable regions (code injection)
- **Network connections**: Process with no reason to be on network (e.g., notepad.exe calling out)

## Windows Forensic Artifacts

```
$MFT: Master File Table — all files, timestamps, sizes
$LogFile: Transaction log of NTFS changes
$UsnJrnl: Update sequence number journal — file change history
Prefetch: Application execution traces (last 8 runs)
Amcache: Application compatibility cache (installed executables)
ShimCache: Application compatibility cache (another source)
ShellBags: Folder view settings (user directory navigation)
Registry: HKLM\System, HKLM\Sam, HKLM\Security, NTUSER.DAT
Event Logs: Security.evtx, System.evtx, PowerShell.evtx
SRUM: System Resource Usage Monitor (network, energy usage)
```

## Linux Forensic Artifacts

```
/var/log/auth.log: Authentication logs
/var/log/syslog: System logs
/var/log/kern.log: Kernel messages
/var/log/apache2/ or /var/log/nginx/: Web server logs
.bash_history: User command history
/var/log/lastlog: Last login records
/var/log/wtmp: Login records (who/w)
/var/log/btmp: Failed login records
journalctl: Systemd journal
/etc/shadow: Password hashes
/etc/passwd: User accounts
```

## Gotchas

- Di exam, Autopsy ingest bisa memakan waktu 20-30 menit — jangan tunggu pasif, kerjakan Phase 1 sambil menunggu
- Volatility 3 tidak memerlukan profile (berbeda dengan Volatility 2) — cukup `windows.info` untuk identifikasi
- `windows.psscan` bisa menemukan process yang di-hidden oleh rootkit — selalu bandingkan dengan `pslist`
- Chain of custody harus diisi untuk setiap evidence item — ini bagian dari penilaian report

## Best Practices

- Screenshot setiap langkah forensik dengan timestamp visible
- Gunakan keyword search di Autopsy untuk IP addresses, domain, dan username
- Selalu dump suspicious process dengan `malfind --dump` dan `dumpfiles` untuk analisis lanjutan
- Buat timeline dari memory (timeliner.Timeliner) dan bandingkan dengan timeline dari Splunk
