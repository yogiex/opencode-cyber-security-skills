---
name: "Source Review Playbook — Metodologi White-Box per Bahasa"
description: "Metodologi review source code white-box: memetakan entry point, menelusuri data flow ke sink, daftar fungsi berisiko per bahasa (Java, C#, PHP, Python, JavaScript), pola kode rentan, urutan pemeriksaan konfigurasi, dan verifikasi manual sebelum exploit ditulis."
tags: [white-box, source-review, data-flow, sinks, java, dotnet, php, python, javascript, methodology]
---

# Source Review Playbook — Metodologi White-Box

White-box berarti source code sudah diberikan: tidak perlu blind guessing atau fuzzing buta. Urutan kerjanya tetap:

```
Source Code → Identify Vulnerability → Verify via Burp → Write Exploit
```

## 1. Petakan entry point

- Identifikasi semua route, controller, servlet, dan endpoint — termasuk yang tidak ditautkan dari UI.
- Cari file yang menangani HTTP request: `routes.php`, `controllers/`, `views.py`, `servlets/`, `Startup.cs`, `app.js`.
- Jangan lupakan kanal non-HTTP: WebSocket handler, job queue consumer, CLI cron, webhook, dan upload handler.
- Catat per entry point: parameter input, metode HTTP, format data (form, JSON, XML, multipart), dan autentikasi yang berlaku.

```
Web Server → Routes → Controllers → Models/DB → Views/Response
              (cari di sini)          (sink di sini)
```

## 2. Telusuri data flow

```
Input (GET/POST/Cookie/Header/JSON/WS) → Validation → Processing → Sink
  (cari sanitasi)                                    (database, exec, deserialize, template)
```

- Ikuti perjalanan data dari entry point ke sink berbahaya.
- Cek apakah ada validasi atau sanitasi di tengah jalan; kalau ada, apakah bisa di-bypass?
- Perhatikan transformasi: decode base64, JSON parse, unserialize, normalisasi path, dan konversi tipe.
- Tandai data yang berasal dari sumber tepercaya (konfigurasi, session server-side) — bukan kandidat.

## 3. Cari vulnerability pattern

| Language | High-Risk Functions/Sinks |
|---|---|
| **Java** | `Runtime.exec()`, `Statement.executeQuery()`, `ObjectInputStream.readObject()`, `new ProcessBuilder()` |
| **C#** | `BinaryFormatter.Deserialize()`, `LosFormatter.Deserialize()`, `Process.Start()`, `SqlCommand()` |
| **PHP** | `eval()`, `system()`, `exec()`, `strcmp()`, `unserialize()`, `==` |
| **Python** | `eval()`, `exec()`, `os.system()`, `subprocess.Popen()`, `render_template_string()` |
| **JavaScript** | `eval()`, `child_process.exec()`, `prototype.__proto__`, `merge()` |

Pencarian awal yang cukup untuk mempersempit area baca:

```bash
grep -rnE "Runtime\.getRuntime\(\)\.exec|ProcessBuilder|executeQuery|readObject" src/
grep -rnE "BinaryFormatter|LosFormatter|ObjectStateFormatter|TypeNameHandling" src/
grep -rnE "eval\(|system\(|shell_exec|unserialize\(|render_template_string" src/
grep -rnE "child_process|__proto__|Object\.assign|merge\(" src/
```

Hasil grep adalah peta, bukan temuan: setiap kandidat masih harus ditelusuri ke input yang bisa dikendalikan.

## 4. Periksa konfigurasi lebih dulu

Konfigurasi sering memuat kunci, kredensial, dan saklar yang mengubah kelas kerentanan:

| Berkas | Yang dicari |
|---|---|
| `web.config` / `appsettings.json` | machine key, connection string, `TypeNameHandling`, mode debug |
| `composer.json` / `package.json` | versi library dengan CVE merge/deserialization yang diketahui |
| `.env`, `config.php`, `settings.py` | secret JWT, kunci enkripsi cookie, kredensial database |
| Dockerfile / compose | versi runtime, layanan internal, port yang diekspos |

Kunci enkripsi yang hardcoded mengubah cookie atau token yang tampak aman menjadi vektor deserialization atau forgery.

## 5. Pola kode rentan per bahasa

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

Detail per kelas kerentanan ada di berkas lain: [injection-attacks.md](./injection-attacks.md), [dotnet-deserialization.md](./dotnet-deserialization.md), [php-auth-bypass.md](./php-auth-bypass.md), [ssrf-xxe.md](./ssrf-xxe.md), [prototype-pollution.md](./prototype-pollution.md).

## 6. Verifikasi manual sebelum exploit

1. Kirim request yang dimodifikasi ke aplikasi lewat Burp Repeater.
2. Konfirmasi bahwa kerentanan benar-benar bisa dieksploitasi, bukan hanya terlihat berbahaya di kode.
3. Catat request/response yang membuktikannya, beserta lokasi kode yang bertanggung jawab.
4. Baru setelah itu tulis script Python yang meniru request tersebut.

Verifikasi tanpa pemahaman kode menghasilkan klaim yang tidak bisa dipertahankan saat developer bertanya "kenapa ini bisa terjadi?".

## 7. Best Practices

- Baca dari route ke sink, bukan dari sink ke belakang: pertanyaan pertama selalu "siapa yang bisa mengirim data ini?".
- Catat kandidat yang gugur beserta alasannya — itu bukti bahwa area sudah diperiksa.
- Prioritaskan area yang menyentuh autentikasi, otorisasi, upload, dan serialisasi.
- Jangan menganggap framework aman: framework menyediakan helper, tetapi developer bisa melewatinya.
- Simpan catatan review (route, file, sink, status) agar laporan dan retest memakai jalur yang sama.

## 8. Sumber

- OWASP WSTG — <https://owasp.org/www-project-web-security-testing-guide/>
- OWASP ASVS — <https://owasp.org/www-project-application-security-verification-standard/>
- HackTricks — <https://book.hacktricks.wiki>
