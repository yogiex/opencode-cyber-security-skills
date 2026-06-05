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
