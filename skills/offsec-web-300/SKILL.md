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

## How to Use This Skill

Load the right reference file based on what you need:

| When you need to... | Load this file |
|---------------------|----------------|
| Review a specific vulnerability class in depth | `references/dotnet-deserialization.md`, `references/php-auth-bypass.md`, `references/injection-attacks.md`, `references/ssrf-xxe.md`, `references/prototype-pollution.md` |
| Get full 17-module case study overview + tool guide + references | `references/modules-overview.md` |
| Write a Python exploit script | Use the template in this SKILL.md (Section 4) |
| Plan exam strategy or write the report | Use the strategy in this SKILL.md (Section 5) |

---

## Daftar Isi

1. [Overview & Exam Structure](#1-overview--exam-structure)
2. [White-Box Testing Mindset & Methodology](#2-white-box-testing-mindset--methodology)
3. [Gotchas — Common OSWE Mistakes](#3-gotchas--common-oswe-mistakes)
4. [Custom Exploit Development in Python](#4-custom-exploit-development-in-python)
5. [Exam Strategy & Report Template](#5-exam-strategy--report-template)
6. [Referensi](#6-referensi)

---

## 1. Overview & Exam Structure

### Apa Itu WEB-300 / OSWE?

WEB-300 (Advanced Web Application Security Assessment) adalah sertifikasi **white-box web application security** dari OffSec. Mengajarkan **source code review** dan **custom exploit development** — membaca source code lengkap aplikasi web, mengidentifikasi kerentanan, dan menulis **exploit Python yang fully automated**.

### Perbedaan OSWE vs OSCP vs OSEP

| Aspek | OSWE (WEB-300) | OSCP+ (PEN-200) | OSEP (PEN-300) |
|-------|---------------|-----------------|----------------|
| **Pendekatan** | **White-box** — source code diberikan | Black-box | Black-box |
| **Fokus** | Source code review, custom exploit | Enumeration, exploitation | Evasion, EDR bypass |
| **Durasi exam** | 47h45m | 24h | 47h45m |
| **Report window** | 24 jam | 24 jam | 24 jam |
| **Passing score** | **85/100** | 50/100 (Booster) | 85/100 |
| **Languages** | Java, C#, PHP, Python, JavaScript | Semua umum | C#, PowerShell, C |

### Scoring & Passing

| Komponen | Detail |
|----------|--------|
| **Durasi exam** | 47 jam 45 menit proctored |
| **Report deadline** | 24 jam setelah exam selesai |
| **Total machines** | 3 machines (20pts + 35pts + 45pts) |
| **Passing score** | **85/100** |
| **Tools utama** | Burp Suite, Python, dnSpy, JD-GUI, Visual Studio |
| **No-go tools** | SQLmap, Burp Suite Pro automation, source code analyzers, AI tools |

### 47h45m Time Management Strategy

```
Hour 0-2:   Initial recon — baca source code semua aplikasi
              → Identifikasi entry points, routes, file structure
Hour 2-6:   Deep source code review per aplikasi
              → Machine 1 (20pts): 1-2 vulnerabilities
              → Machine 2 (35pts): 2-3 vulnerabilities, chaining
              → Machine 3 (45pts): hardest, multi-step exploit chain
Hour 6-24:  Exploit development
              → Write exploit.py → get Local.txt + Proof.txt
Hour 24-47: Continue machines + verification
Hour 47-71: Report writing (24h window)
```

---

## 2. White-Box Testing Mindset & Methodology

### Filosofi Dasar

OSWE berbeda dari OSCP/OSEP karena **source code sudah diberikan**. Tidak perlu blind guessing atau fuzzing buta. Strateginya:

```
Source Code → Identify Vulnerability → Verify via Burp → Write Exploit
```

### Source Code Review Methodology

**1. Map Entry Points**
- Identifikasi semua routes, controllers, servlets, endpoints
- Cari file yang menangani HTTP request (routes.php, controllers/, views.py, servlets/)
- Catat parameter input, metode HTTP, format data

```
Web Server → Routes → Controllers → Models/DB → Views/Response
              (cari di sini)          (sink di sini)
```

**2. Trace Data Flow**
```
Input (GET/POST/Cookie) → Validation → Processing → Sink
  (cari sanitasi)                    (database, exec, deserialize)
```
- Ikuti perjalanan data dari entry point ke sink berbahaya
- Cek apakah ada validasi/sanitasi di tengah jalan
- Jika ada filtering, apakah bisa di-bypass?

**3. Cari Vulnerability Patterns**

| Language | High-Risk Functions/Sinks |
|----------|--------------------------|
| **Java** | `Runtime.exec()`, `Statement.executeQuery()`, `ObjectInputStream.readObject()`, `new ProcessBuilder()` |
| **C#** | `BinaryFormatter.Deserialize()`, `LosFormatter.Deserialize()`, `Process.Start()`, `SqlCommand()` |
| **PHP** | `eval()`, `system()`, `exec()`, `strcmp()`, `unserialize()`, `==` |
| **Python** | `eval()`, `exec()`, `os.system()`, `subprocess.Popen()`, `render_template_string()` |
| **JavaScript** | `eval()`, `child_process.exec()`, `prototype.__proto__`, `merge()` |

**4. Validate via Burp Suite**
- Kirim request yang dimodifikasi ke aplikasi via Burp Repeater
- Konfirmasi bahwa vulnerability benar-benar bisa dieksploitasi
- Catat request/response untuk report

**5. Write Custom Exploit**
- Setelah manual validation berhasil, tulis Python script exploit
- Exploit harus: **fully automated, satu command, zero interaction**

### Vulnerable Code Patterns by Language

**Java — RCE via Runtime.exec()**:
```java
// Look for: Runtime.getRuntime().exec(cmd);
// Look for: new ProcessBuilder(cmd).start();
String userInput = request.getParameter("cmd");
Runtime.getRuntime().exec(userInput);
```

**Java — SQL Injection**:
```java
// Look for: Statement.executeQuery(), string concatenation in query
String query = "SELECT * FROM users WHERE id=" + request.getParameter("id");
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);
```

**C# — Deserialization**:
```csharp
// Look for: BinaryFormatter, LosFormatter, ObjectStateFormatter
BinaryFormatter formatter = new BinaryFormatter();
object obj = formatter.Deserialize(stream);
```

**PHP — Type Juggling**:
```php
// Look for: == (loose comparison), strcmp(), in_array() without strict
if (strcmp($_POST['password'], $hash) == 0) { }
```

**PHP — Command Injection**:
```php
// Look for: system(), exec(), shell_exec(), passthru(), `backticks`
$output = shell_exec("ping " . $_GET['ip']);
```

**Python — SSTI**:
```python
# Look for: render_template_string() with user input
from flask import render_template_string
return render_template_string("Hello " + user_input)
```

**JavaScript — Prototype Pollution**:
```javascript
// Look for: recursive merge, Object.assign, lodash.merge
function merge(a, b) {
    for (let key in b) {
        if (typeof b[key] === 'object') merge(a[key], b[key]);
        else a[key] = b[key];
    }
}
```

---

## 3. Gotchas — Common OSWE Mistakes

- **SQLmap is FORBIDDEN** in the OSWE exam. All SQLi must be manual.
- **Exploit MUST be fully automated**: one command, no interaction, no `input()`, no `raw_input()`.
- **Proof.txt is ALWAYS on a different privilege level** than Local.txt — privilege escalation is always required.
- **Passing score is 85/100** — you can lose max 15 points. Skipping the 20pt machine is not an option.
- **Source code is provided** — always check config files first: `web.config`, `appsettings.json`, `composer.json`, `package.json`.
- **ysoserial.net gadget chains are .NET framework version dependent** — check the target's .NET version before generating payload.
- **No hardcoded sessions** in exploit — the script must obtain its own session through the login process.
- **Report window is only 24 hours** — don't leave all report writing to the last minute. Write as you go.
- **Screenshot everything**: Burp requests/responses, terminal output, Local.txt, Proof.txt.
- **Test from fresh VPN connection** before submitting — what works in lab may not work in exam environment.
- **Magic hashes in PHP** are case-sensitive and hash-algorithm specific. Test your payload.
- **JWT `alg: none`** only works if the server library doesn't enforce algorithm restriction. Check the library version.

---

## 4. Custom Exploit Development in Python

### OSWE Exploit Requirements

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

TARGET = sys.argv[1] if len(sys.argv) > 1 else "http://target:port"

def get_session() -> requests.Session:
    s = requests.Session()
    s.verify = False
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    return s

def login(session: requests.Session, username: str, password: str) -> bool:
    r = session.post(f"{TARGET}/login.php", data={
        "username": username, "password": password
    })
    return "dashboard" in r.text

def exploit(session: requests.Session) -> Tuple[str, str]:
    # Step 1: Initial access
    # Step 2: Privilege escalation
    # Return: (local_txt, proof_txt)
    pass

def main():
    session = get_session()
    print(f"[*] Target: {TARGET}")
    
    # Login
    if not login(session, "admin", "admin"):
        print("[-] Login failed")
        sys.exit(1)
    print("[+] Login successful")
    
    # Exploit
    local, proof = exploit(session)
    print(f"[+] Local.txt: {local}")
    print(f"[+] Proof.txt: {proof}")

if __name__ == "__main__":
    main()
```

### Exploit Development Workflow

```
1. Manual validation via Burp Repeater → confirm vulnerability
2. Write Python script that mimics Burp requests
3. Test exploit.py against local target
4. Fix any issues (status codes, CSRF tokens, session handling)
5. Test from fresh state (new VPN, no browser cookies)
6. Screenshot successful run
```

### Common Snippet Library

**CSRF Token Extraction**:
```python
def get_csrf(session, url):
    r = session.get(url)
    match = re.search(r'name="csrf_token" value="([^"]+)"', r.text)
    return match.group(1) if match else None
```

**Blind SQLi Time-Based**:
```python
def test_blind_sqli(session, payload):
    start = time.time()
    r = session.get(f"{TARGET}/api?q={urllib.parse.quote(payload)}")
    return time.time() - start > 5
```

**WebSocket Command Injection**:
```python
import websocket, json
ws = websocket.WebSocket()
ws.connect(f"wss://{TARGET}/ws")
ws.send(json.dumps({"cmd": "ping", "host": f"127.0.0.1; {command}"}))
```

**SSTI Jinja2 RCE**:
```python
payload = "{{ self.__init__.__globals__.__builtins__.__import__('os').popen('cat /root/proof.txt').read() }}"
r = session.post(TARGET, data={"template": payload})
```

---

## 5. Exam Strategy & Report Template

### Machine Strategy

**Machine 1 (20pts)** — Quick win, 2-4 jam:
1. Source code review — cari vulnerable entry point (biasanya 1-2 bugs)
2. Verify dengan Burp Repeater
3. Tulis exploit.py
4. Test dari fresh state → screenshot flags
5. Lanjut ke Machine 2

**Machine 2 (35pts)** — Medium, 8-12 jam:
1. Source code review — map all entry points
2. Identify 2-3 vulnerabilities yang perlu chain
3. Develop exploit chain: Auth bypass → RCE → PE
4. Test exploit chain from fresh state
5. Screenshot + flags

**Machine 3 (45pts)** — Hard, 12-18 jam:
1. Comprehensive source code review — aplikasi paling kompleks
2. Multiple chaining: SSRF → internal API → admin → RCE
3. Exploit development — mungkin perlu multiple Python scripts
4. Integration test — full chain from zero
5. Screenshot + flags

### Report Template

```markdown
## Target Information
- **IP Address**: <target_ip>
- **Application**: <name>
- **Language/Framework**: <language>

## Vulnerability Summary
1. **<Vuln Type 1>** — <CVE if applicable>
   - Location: <file_path:line>
   - Impact: <description>

## Source Code Review
```<language>
// Highlight vulnerable code
```

## Exploitation
### Step 1: <Step Name>
**Request**: <Burp request>
**Response**: <Burp response>

### Flags
- **Local.txt**: `<hash>`
- **Proof.txt**: `<hash>`

## Remediation
1. <fix 1>
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

## 6. Referensi

### OffSec Official
- Course: https://www.offsec.com/courses/web-300/
- Exam Guide: https://help.offsec.com/hc/en-us/articles/360049792232-OSWE-Exam-Guide

### Reference Files
- `references/dotnet-deserialization.md` — .NET gadget chains, BinaryFormatter, LosFormatter
- `references/php-auth-bypass.md` — PHP type juggling, magic hashes, JWT attacks
- `references/injection-attacks.md` — SQLi, SSTI, OS command injection, WebSocket
- `references/ssrf-xxe.md` — SSRF bypass techniques, blind XXE, DTD inclusion
- `references/prototype-pollution.md` — PP detection, server-side RCE gadgets
- `references/modules-overview.md` — Full 17 module case studies + tools + all references

### Key Resources
| Resource | URL |
|----------|-----|
| Burp Suite | https://portswigger.net/burp/communitydownload |
| dnSpy | https://github.com/dnSpy/dnSpy |
| ysoserial | https://github.com/frohoff/ysoserial |
| ysoserial.net | https://github.com/pwntester/ysoserial.net |
| HackTricks | https://book.hacktricks.wiki |
| PayloadsAllTheThings | https://github.com/swisskyrepo/PayloadsAllTheThings |
| PortSwigger Academy | https://portswigger.net/web-security |
| OSWE-Prep | https://github.com/Xcatolin/OSWE-Prep |

---

> **Catatan Akhir**: OSWE adalah salah satu sertifikasi web application tersulit di industri — membutuhkan kemampuan membaca dan memahami source code dalam 5 bahasa (Java, C#, PHP, Python, JavaScript) dan menulis exploit Python yang fully automated. Kunci sukses:
> 1. **Kuasai source code review** — cari vulnerable patterns dengan cepat
> 2. **Pahami gadget chains** — .NET deserialization, Java ysoserial, prototype pollution gadgets
> 3. **Exploit Python harus clean** — fully automated, no hardcoded sessions
> 4. **Report adalah 85/100 minimum** — dokumentasi setiap langkah exploit
> 5. **Praktik, praktik, praktik** — kerjakan semua Challenge Labs sampai exploit jalan tanpa error
>
> Ingat: "Source code is the ultimate documentation. Everything you need to exploit the application is right there."

*Based on OffSec WEB-300 / OSWE curriculum*
*License: MIT*
