---
name: "Referensi — Sumber Eksternal untuk Praktisi White-Box"
description: "Sumber eksternal untuk pekerjaan white-box web assessment: standar uji, referensi per kelas kerentanan (SQLi, SSTI, SSRF, XXE, prototype pollution), dokumentasi serializer dan database, tooling, serta lab latihan."
tags: [referensi, resources, owasp, portswigger, hacktricks, deserialization, ssrf, xxe, prototype-pollution]
---

# Referensi

Sumber di bawah dipilih karena relevan dengan pekerjaan lapangan: standar yang dipakai klien, referensi teknis yang dijaga komunitas, dan lab untuk menjaga ketajaman.

## Standar dan metodologi

- OWASP WSTG — <https://owasp.org/www-project-web-security-testing-guide/>
- OWASP ASVS — <https://owasp.org/www-project-application-security-verification-standard/>
- OWASP Cheat Sheet Series — <https://cheatsheetseries.owasp.org/>
- PTES — <http://www.pentest-standard.org/> (lihat skill [ptes-standard](../../ptes-standard/SKILL.md))
- MITRE ATT&CK — <https://attack.mitre.org/>

## Kelas kerentanan

- SQL Injection — <https://portswigger.net/web-security/sql-injection>
- Server-Side Template Injection — <https://portswigger.net/web-security/server-side-template-injection>
- SSTI (HackTricks) — <https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/>
- SSRF — <https://portswigger.net/web-security/ssrf>
- SSRF (HackTricks) — <https://book.hacktricks.wiki/en/pentesting-web/ssrf-server-side-request-forgery/>
- XXE — <https://portswigger.net/web-security/xxe>
- OWASP XXE Prevention — <https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html>
- Prototype Pollution — <https://portswigger.net/web-security/prototype-pollution>
- Prototype Pollution (HackTricks) — <https://book.hacktricks.wiki/en/pentesting-web/prototype-pollution/>

## Bahasa dan library

- PHP type juggling — <https://www.php.net/manual/en/language.types.type-juggling.php>
- Magic hashes — <https://github.com/spaze/hashes>
- PostgreSQL `COPY` — <https://www.postgresql.org/docs/current/sql-copy.html>
- H2 database RCE — <https://mthbernardes.github.io/pentesting/2018/02/05/h2db-rce.html>
- DotNetNuke CVE-2017-9822 (PoC publik) — <https://www.exploit-db.com/exploits/43973>
- ysoserial.net — <https://github.com/pwntester/ysoserial.net>
- ysoserial (Java) — <https://github.com/frohoff/ysoserial>

## Tooling

- Burp Suite — <https://portswigger.net/burp/communitydownload>
- dnSpy — <https://github.com/dnSpy/dnSpy>
- JD-GUI — <https://github.com/java-decompiler/jd-gui>
- PayloadsAllTheThings — <https://github.com/swisskyrepo/PayloadsAllTheThings> (lihat skill [web-pentest-payloads](../../web-pentest-payloads/SKILL.md))
- HackTricks — <https://book.hacktricks.wiki>

## Lab dan latihan

- PortSwigger Web Security Academy — <https://portswigger.net/web-security>
- OWASP Juice Shop — <https://owasp.org/www-project-juice-shop/>
- Hack The Box — <https://www.hackthebox.com/>
- Proving Grounds — <https://www.offsec.com/labs/>
- PentesterLab — <https://pentesterlab.com/>

## Internal

- [persona.md](./persona.md) — profil, gaya bicara, batas klaim.
- [source-review-playbook.md](./source-review-playbook.md) — metodologi review per bahasa.
- [injection-attacks.md](./injection-attacks.md) — SQLi, SSTI, command injection.
- [dotnet-deserialization.md](./dotnet-deserialization.md) — serializer .NET dan gadget chain.
- [php-auth-bypass.md](./php-auth-bypass.md) — type juggling dan bypass autentikasi.
- [ssrf-xxe.md](./ssrf-xxe.md) — SSRF dan XXE.
- [prototype-pollution.md](./prototype-pollution.md) — PP client dan server-side.
- [exploit-development.md](./exploit-development.md) — template dan snippet exploit Python.
- [engagement-playbook.md](./engagement-playbook.md) — scope, bukti, laporan klien.
- [capability-domains.md](./capability-domains.md) — peta kapabilitas.
- [security-documentation](../../security-documentation/SKILL.md) — standar penulisan laporan.
