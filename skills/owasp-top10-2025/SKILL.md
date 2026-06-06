---
name: owasp-top10-2025
description: Complete reference for OWASP Top 10 2025 web application security risks. Use when conducting threat modeling, code review, penetration testing, secure design, or when user asks about any AXX:2025 category, vulnerability explanations, or mitigation strategies.
license: MIT
compatibility: opencode
metadata:
  source: OWASP
  year: "2025"
---

# OWASP Top 10 2025 – Comprehensive Skill

You are an expert in OWASP Top 10 2025. Provide accurate, actionable security guidance based on the official OWASP Top 10 2025 list (released November 2025).

## When to Use This Skill

Invoke this skill when:
- User asks about web application security risks or vulnerabilities.
- User mentions `OWASP`, `Top 10`, `A01`, `A02`, etc., or specific terms like `broken access control`, `supply chain`, `cryptographic failures`, `injection`, `insecure design`, `authentication failures`, `integrity failures`, `logging`, `exception handling`.
- Performing threat modeling, security code review, penetration testing, or secure architecture design.
- User needs mitigation guidance, real-world examples, or ranking changes between 2021 and 2025.

## The 2025 List (At a Glance)

| Rank | ID | Category | Change from 2021 |
|------|-----|-----------|------------------|
| 1 | A01:2025 | Broken Access Control | No change (now includes SSRF) |
| 2 | A02:2025 | Security Misconfiguration | ↑ from #5 |
| 3 | A03:2025 | Software Supply Chain Failures | New (expanded from Vulnerable Components) |
| 4 | A04:2025 | Cryptographic Failures | ↓ from #2 |
| 5 | A05:2025 | Injection | ↓ from #3 |
| 6 | A06:2025 | Insecure Design | ↓ two spots |
| 7 | A07:2025 | Authentication Failures | No change |
| 8 | A08:2025 | Software or Data Integrity Failures | No change |
| 9 | A09:2025 | Logging & Alerting Failures | No change |
| 10 | A10:2025 | Mishandling of Exceptional Conditions | New |

---

## Detailed Category Breakdown

### A01:2025 – Broken Access Control

**Description**  
Access control enforces policy such that users cannot act outside their intended permissions. Failures lead to unauthorized information disclosure, modification, destruction, or executing functions outside user limits. Now includes **Server-Side Request Forgery (SSRF)**.

**Common Examples**
- Bypass access controls by modifying URL, internal app state, or HTML page.
- Elevation of privilege: acting as admin when logged in as user.
- Insecure direct object references (IDOR) – accessing records by guessing ID.
- SSRF: attacker causes server to make requests to unintended internal systems.

**Mitigation**
- Deny by default – only grant specific access per role.
- Use access control mechanisms once and re-use throughout app.
- Log access control failures and alert on anomalies.
- Rate limit API and controller access.
- For SSRF: sanitize and validate all request URLs; use allow lists; disable HTTP redirects; segregate internal vs external networks.

---

### A02:2025 – Security Misconfiguration

**Description**  
The most common issue – insecure default configurations, incomplete setups, open cloud storage, verbose error messages, missing security headers.

**Examples**
- Default credentials (admin/admin) still active.
- Directory listing enabled on web server.
- Unpatched frameworks or dependencies.
- Unnecessary features (ports, services, pages) left enabled.

**Mitigation**
- Repeatable hardening process (CI/CD pipeline).
- Minimal platform – remove unused features.
- Review and update configs as part of patch management.
- Use automated scanners to detect missing patches or misconfigs.

---

### A03:2025 – Software Supply Chain Failures

**Description**  
Vulnerabilities introduced via third-party libraries, components, CI/CD pipelines, or build infrastructure. Attackers compromise build tools, inject backdoors, or use trojanized libraries.

**Examples**
- Using a compromised npm package with malware.
- CI pipeline with weak secrets exposing AWS keys.
- Forged open-source dependency with backdoor.

**Mitigation**
- Maintain inventory of all components (SBOM).
- Automate integrity checks (e.g., SHA hashes, signing).
- Use software composition analysis (SCA) tools.
- Harden CI/CD pipelines with least privilege and secrets management.

---

### A04:2025 – Cryptographic Failures

**Description**  
Formerly “Sensitive Data Exposure”. Failure to encrypt sensitive data at rest or in transit, weak algorithms, hard-coded keys, improper certificate validation.

**Examples**
- Transmitting credentials in plain HTTP.
- Old or weak hashing (MD5, SHA1) for passwords.
- Missing encryption on database backups.

**Mitigation**
- Classify data sensitivity.
- Encrypt all data in transit (TLS 1.3+).
- Encrypt sensitive data at rest (AES-256).
- Use strong adaptive hashing (bcrypt, PBKDF2, Argon2) for passwords.
- Disable caching for sensitive responses.

---

### A05:2025 – Injection

**Description**  
SQL, NoSQL, OS command, LDAP, etc. – untrusted data sent to interpreter as part of command/query.

**Examples**
- SQL injection: `' OR '1'='1` bypassing login.
- Command injection: `; rm -rf /` appended to input.

**Mitigation**
- Use parameterized queries / prepared statements.
- Use allow-list input validation.
- Escape special characters.
- Minimize database privileges.

---

### A06:2025 – Insecure Design

**Description**  
Missing or ineffective security design patterns. Not a coding mistake but a fundamental design flaw.

**Examples**
- No threat modeling performed.
- Trusting user-supplied data without validation at design level.
- Assuming a single layer of defense is enough.

**Mitigation**
- Establish secure design principles (defense in depth, least privilege).
- Perform threat modeling (STRIDE, LINDDUN).
- Use secure design patterns and reference architectures.
- Integrate security requirements into user stories.

---

### A07:2025 – Authentication Failures

**Description**  
Weak authentication, session management flaws, credential stuffing, lack of MFA.

**Examples**
- No rate limiting on login → brute force.
- Session IDs in URL.
- Credential stuffing using breached passwords.

**Mitigation**
- Implement multi-factor authentication (MFA).
- Use strong password policies and breach detection.
- Rate limit failed attempts.
- Use secure session handling (HttpOnly, Secure, SameSite flags).

---

### A08:2025 – Software or Data Integrity Failures

**Description**  
Failure to protect against unauthorized modifications of software, libraries, or critical data. Related to supply chain but broader – includes serialization flaws, deserialization attacks, CI/CD integrity.

**Examples**
- Deserializing untrusted objects leads to RCE.
- No integrity check on configuration files.
- Using unsigned third-party binaries.

**Mitigation**
- Use digital signatures or checksums.
- Prevent unsafe deserialization (type checking, allow lists).
- Implement integrity monitoring for critical files.

---

### A09:2025 – Logging & Alerting Failures

**Description**  
Insufficient logging, missing or low-fidelity alerts, logs not monitored. Attackers can persist without detection.

**Examples**
- Login failures not logged.
- No alert on privilege escalation attempt.
- Logs stored only locally, easily deleted.

**Mitigation**
- Log all authentication attempts, access control failures, input validation errors.
- Use centralized logging (SIEM).
- Establish alert thresholds.
- Ensure logs are immutable and protected.

---

### A10:2025 – Mishandling of Exceptional Conditions

**Description**  
**New category.** Improper handling of errors, edge cases, unexpected inputs, or exceptional conditions that lead to security failures.

**Examples**
- Stack trace exposed to user revealing internal paths.
- Application crashes into a privileged fallback mode.
- Time-of-check/time-of-use (TOCTOU) conditions in file handling.
- Race conditions in business logic.

**Mitigation**
- Use structured exception handling that doesn't expose internals.
- Fall securely – fail closed, not open.
- Validate assumptions at every boundary.
- Avoid TOCTOU by using atomic operations or locking.

---

## How to Apply OWASP Top 10 2025

1. **Threat Modeling** – identify which of the 10 risks apply.
2. **Secure Code Review** – focus on the top 3 (A01, A02, A03).
3. **Penetration Testing** – use the categories as a checklist.
4. **Training** – teach developers one category per sprint.
5. **Tooling** – configure SAST/DAST/SCA to detect these risks.

## Key Changes from 2021 to 2025

- **A03** – Software Supply Chain Failures (new, reflects real-world attacks like SolarWinds, Log4shell).
- **A10** – Mishandling of Exceptional Conditions (new).
- **SSRF** moved under Broken Access Control (A01).
- Security Misconfiguration jumped from #5 to #2.

## Response Style

When user asks about a specific risk:
- Explain the risk in one sentence.
- Give a concrete example.
- Provide 2-3 actionable mitigations.
- If relevant, note any changes from OWASP Top 10 2021.

If user asks for a full list, output the table summary and then ask which category they want to deep dive.

Always prioritize **practical, fixable advice** over academic theory.

## Reference Documentation

| File | Description |
|------|-------------|
| [payloads-cheatsheet.md](references/payloads-cheatsheet.md) | Comprehensive payload reference — vulnerable parameters, HTTP request examples, and bypass techniques for 12 OWASP categories |

## Referensi Lengkap

### Official OWASP Documentation

| Nama | Deskripsi | Link |
|------|-----------|------|
| OWASP Top 10:2025 — Official | Halaman resmi dengan data, metodologi, dan detail per kategori | [owasp.org](https://owasp.org/Top10/2025/) |
| OWASP Top 10 GitHub Project | Repositori markdown resmi, data kontribusi kuesioner, rencana remediasi | [github.com](https://github.com/owasp/top10) |
| OWASP ASVS v4.0 | Application Security Verification Standard — kerangka audit teknis mendalam | [owasp.org](https://owasp.org/www-project-application-security-verification-standard/) |
| OWASP WSTG v4.2 | Web Security Testing Guide — panduan testing untuk setiap kerentanan | [owasp.org](https://owasp.org/www-project-web-security-testing-guide/) |
| OWASP Cheat Sheet Series | Koleksi concise cheat sheet per topik keamanan | [cheatsheetseries.owasp.org](https://cheatsheetseries.owasp.org/) |
| OWASP Juice Shop | Aplikasi sengaja rentan (Node.js/Angular) untuk training dan CTF | [owasp.org](https://owasp.org/www-project-juice-shop/) |
| OWASP Dependency-Check | Open-source SCA tool untuk identifikasi komponen rentan | [owasp.org](https://owasp.org/www-project-dependency-check/) |
| OWASP ZAP | Zed Attack Proxy — open-source DAST tool terkemuka | [zaproxy.org](https://www.zaproxy.org/) |

### Buku & Publications

| Judul | Penulis | Fokus Utama |
|-------|---------|-------------|
| Alice and Bob Learn Application Security | Tanya Janca | Fondasi AppSec untuk developer — praktis, mudah dipahami |
| Agile Application Security | Laura Bell, Michael Brunton-Spall, Rich Smith, Jim Bird | Integrasi OWASP ke siklus CI/CD dan Agile |
| The Web Application Hacker's Handbook (2nd Ed.) | Dafydd Stuttard, Marcus Pinto | Bible of web app security — teknis mendalam |
| Real-World Bug Hunting | Peter Yaworski | Studi kasus bug bounty — aplikasi nyata OWASP Top 10 |
| Web Security for Developers | Malcolm McDonald | Pemrograman web aman untuk developer sehari-hari |
| OWASP Testing Guide Implementation | Packt Publishing | Implementasi praktis OWASP WSTG dalam pengujian |
| Hacking Web Apps | Mike Shema | Memahami kerentanan dari perspektif penyerang |
| Browser Security Handbook | Google (Michal Zalewski) | Keamanan browser — Same-Origin Policy, CSP, XSS vectors |

### SAST / DAST / SCA — Tools Matrix per Kategori

| Kategori OWASP | SAST | DAST | SCA | Tools Rekomendasi |
|----------------|------|------|-----|-------------------|
| A01: Broken Access Control | 🔶 Parsial | 🟢 Sangat Efektif | ❌ Tidak Efektif | Burp Suite Enterprise, OWASP ZAP, Checkmarx |
| A02: Security Misconfiguration | 🔶 Parsial (IaC) | 🟢 Sangat Efektif | ❌ Tidak Efektif | Semgrep, Trivy, OWASP ZAP |
| A03: Supply Chain Failures | ❌ Tidak Efektif | ❌ Tidak Efektif | 🟢 Sangat Efektif | Snyk, Dependabot, OWASP Dependency-Check, Cycode |
| A04: Cryptographic Failures | 🟢 Sangat Efektif | 🔶 Parsial | ❌ Tidak Efektif | SonarQube, Veracode, Fortify |
| A05: Injection | 🟢 Sangat Efektif | 🟢 Sangat Efektif | ❌ Tidak Efektif | Semgrep, sqlmap, Acunetix, Burp Suite |
| A06: Insecure Design | ❌ Sangat Lemah | ❌ Sangat Lemah | ❌ Tidak Efektif | Threat Modeling (STRIDE, LINDDUN, PASTA) |
| A07: Authentication Failures | 🔶 Parsial | 🟢 Sangat Efektif | ❌ Tidak Efektif | OWASP ZAP, Burp Suite Pro |
| A08: Integrity Failures | 🔶 Parsial | ❌ Tidak Efektif | 🟢 Sangat Efektif | Snyk, Black Duck, Sigstore/Cosign |
| A09: Logging & Alert Failures | 🟢 Sangat Efektif | ❌ Tidak Efektif | ❌ Tidak Efektif | SonarQube, CodeQL, SIEM config auditors |
| A10: Exceptional Conditions | 🟢 Sangat Efektif | 🔶 Parsial (Fuzzing) | ❌ Tidak Efektif | CodeQL, AFL++, libFuzzer |

### Real-World CVE Examples per Kategori

| Kategori | CVE | Deskripsi |
|----------|-----|-----------|
| A01: Broken Access Control | CVE-2024-21626 | Kernel container escape / access bypass via working directory |
| A01: Broken Access Control | CVE-2023-3824 | PHP memory configuration exploitation via SSRF |
| A02: Security Misconfiguration | CVE-2023-46604 | RCE pada Apache ActiveMQ via konfigurasi serialisasi |
| A03: Supply Chain Failures | CVE-2024-25062 | XML certificate validation bypass pada library populer |
| A04: Cryptographic Failures | CVE-2024-27198 | Parameter injection & bypass authentication di TeamCity |
| A05: Injection | CVE-2023-4863 | Heap buffer overflow pada WebP codec — 0-day exploited |
| A06: Insecure Design | CVE-2024-1597 | Authentication bypass pada PostgreSQL JDBC driver |
| A07: Authentication Failures | CVE-2023-38606 | Kernel integrity bypass pada iOS — digunakan oleh spyware |
| A08: Integrity Failures | CVE-2021-44228 | Log4Shell — remote code execution via logging library |
| A09: Logging & Alert Failures | CVE-2024-22024 | XML external entity processing crash — fail-open condition |
| A10: Exceptional Conditions | CVE-2024-22024 | Mishandling of exceptional XML parsing conditions |

### Cloud-Specific Guidance

| Kategori | Cloud Risk | Mitigasi |
|----------|------------|----------|
| A01: Broken Access Control | IAM policies wildcard terlalu longgar, privilege escalation via cloud API | AWS IAM Access Analyzer, least privilege, SCP tagging |
| A02: Security Misconfiguration | S3 bucket publik, Azure Blob terbuka, GCP bucket misconfigured | CSPM tools (Orca, Prisma Cloud, Wiz), account-level block public access |
| A03: Supply Chain Failures | Container base images tidak diverifikasi dari Docker Hub publik | Cosign/Sigstore signing, private registry, image scanning (Trivy, Grype) |
| A04: Cryptographic Failures | KMS key misconfiguration, expired certificates di ELB/CloudFront | AWS KMS key rotation, ACM auto-renewal, TLS inspection |
| A05: Injection | SQL injection via RDS, command injection via Lambda env vars | Parameterized queries, WAF (AWS WAF, Cloud Armor), input validation |
| A06: Insecure Design | Cloud architecture tanpa security boundaries | Well-Architected Framework security pillar, threat modeling |
| A07: Authentication Failures | Root user tanpa MFA, service account key leaked | Enforce MFA, IAM Roles Anywhere, Secrets Manager |
| A09: Logging & Alert Failures | CloudTrail/GCP Audit Logs tidak enabled | Org-level trails, detective controls, SIEM integration (Sentinel, Splunk) |

### Training & Courses

| Nama | Provider | Level | Fokus |
|------|----------|-------|-------|
| SEC522: Defending Web Applications | SANS Institute | Advanced | Web application defense, OWASP Top 10 deep dive |
| Learning the OWASP Top 10 (2025 Ver.) | LinkedIn Learning (Caroline Wong) | Beginner | Studi kasus nyata, ramah pemula |
| Practical Web Defense | TCM Security | Intermediate | Hands-on lab, mitigasi kerentanan web modern |
| Web Security Academy | PortSwigger | All levels | Ratusan lab interaktif terintegrasi OWASP |
| WeSecureApp OWASP Training | WeSecureApp | Intermediate | OWASP Top 10 hands-on training |
| Application Security & Secure Coding | Codecademy / Cybrary | Beginner-Intermediate | Secure coding fundamentals |

### Certifications

| Sertifikasi | Penerbit | Fokus | Biaya |
|-------------|----------|------|-------|
| GIAC GWEB | SANS | Web application defense, defensive techniques | ~$8,780 (incl. SEC522) |
| Certified DevSecOps Professional (CDP) | Practical DevSecOps | CI/CD security automation, SAST/DAST/SCA | $899 |
| Offensive Security Web Exploitation (OSWE) | Offensive Security | White-box code analysis, advanced manual exploitation | $1,599 |
| Burp Suite Certified Practitioner | PortSwigger | Burp Suite proficiency, web security testing | ~$200 |
| Certified Application Security Engineer (CASE) | EC-Council | Secure SDLC, OWASP Top 10 | ~$1,049 |
| eWPTX (Web Application Pentesting eXtreme) | eLearnSecurity | Advanced web pentesting, multi-stage attacks | ~$850 |

### CTF & Practice Platforms

| Platform | Deskripsi | Link |
|----------|-----------|------|
| PortSwigger Web Security Academy | Lab interaktif gratis terbaik — 100+ lab, OWASP-aligned | [portswigger.net](https://portswigger.net/web-security) |
| OWASP Juice Shop | Modern vulnerable web app (Node.js/Angular) untuk CTF internal | [owasp.org](https://owasp.org/www-project-juice-shop/) |
| Hack The Box | Guided paths "Web Application Penetration Testing", CTF machines | [hackthebox.com](https://www.hackthebox.com/) |
| TryHackMe | "OWASP Top 10" path, beginner-friendly rooms | [tryhackme.com](https://tryhackme.com/) |
| PentesterLab | Web vulnerability labs by category — progressive difficulty | [pentesterlab.com](https://pentesterlab.com/) |
| Root-Me | 400+ web challenges, OWASP-categorized | [root-me.org](https://www.root-me.org/) |
| WebSec CTF Challenges | CTF khusus web security, berbagai kategori OWASP | [websec.fr](https://websec.fr/) |
| Pentest-Training.com | Realistic attack scenarios with writeups | [pentest-training.com](https://pentest-training.com/) |

### Communities & Curated Lists

| Nama | Deskripsi | Link |
|------|-----------|------|
| OWASP Official Website | Project documentation, chapters, conferences | [owasp.org](https://owasp.org/) |
| OWASP GitHub Organization | Semua project OWASP open-source | [github.com](https://github.com/owasp) |
| PortSwigger Research | Web security research, blog posts, tool releases | [portswigger.net](https://portswigger.net/research) |
| PortSwigger Blog | Daily web security news, techniques, writeups | [portswigger.net](https://portswigger.net/blog) |
| Awesome Web Security (qazbnm456) | Curated list of web security resources (7k+ stars) | [github.com](https://github.com/qazbnm456/awesome-web-security) |
| Awesome Hacking (Hack-with-Github) | Curated list of hacking tools & resources (80k+ stars) | [github.com](https://github.com/Hack-with-Github/Awesome-Hacking) |
| Payloads All The Things | Curated payloads per vulnerability type | [github.com](https://github.com/swisskyrepo/PayloadsAllTheThings) |
| Web Security Cheatsheet (infosecB) | Concise web security testing references | [github.com](https://github.com/infosecB/awesome-web-security) |
