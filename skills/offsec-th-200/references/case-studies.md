---
name: "Ransomware & APT Case Studies"
description: "Real-world ransomware attack chains (LockBit) and APT case studies (APT29, Lazarus) with TTP mappings and hunt indicators for each phase."
tags: [case-studies, ransomware, apt, lockbit, apt29, lazarus, attack-chain]
---

# Ransomware & APT Case Studies

## Ransomware Attack Chain (LockBit)

```
Phase 1: Initial Access (T1190)
  - Exploit Citrix/Verizon VPN vulnerability
  - Gain foothold on edge server
  Hunt: VPN connection logs, web shell creation

Phase 2: Defense Evasion (T1070)
  - Disable Windows Defender via registry
  - Delete logs, disable auditing
  Hunt: Registry changes to Defender, Event 1102 (log clear)

Phase 3: Credential Access (T1003)
  - Dump LSASS via comsvcs.dll
  - Extract domain admin hashes
  Hunt: LSASS access (Sysmon 10), comsvcs.dll usage

Phase 4: Lateral Movement (T1021)
  - PsExec to domain controllers
  - Deploy ransomware via GPO
  Hunt: PsExec execution (Sysmon 1), service creation (7045)

Phase 5: Exfiltration (T1048)
  - StealBit tool exfiltrates data
  - Encrypted upload to adversary server
  Hunt: Large outbound data transfers, unusual DNS queries

Phase 6: Impact (T1486)
  - Encrypt files with AES+RSA
  - Deploy ransom note
  - Data leak site if unpaid
  Hunt: Mass file operations (Sysmon 11), extension changes
```

## APT Case Study: APT29 (Cozy Bear)

**Profile:** Russia's SVR, targets government/think tanks/academia/IT, motivation espionage.

**TTPs:**
- Initial access: Spear phishing, supply chain (SolarWinds)
- Persistence: Golden SAML, Azure AD application registration
- C2: Cloud API abuse (Microsoft Graph, Dropbox, Google Drive)
- Tools: PowerShell, Cobalt Strike, custom backdoors

**Detection Opportunities:**
- PowerShell with cloud API URLs
- Azure AD app registration by non-admin accounts
- Beaconing via HTTPS to cloud services
- Unusual OAuth token usage

## APT Case Study: Lazarus Group

**Profile:** North Korea (RGB), targets financial/crypto/defense, motivation financial gain + espionage.

**TTPs:**
- Initial access: Social engineering, malicious npm packages
- Tools: macOS malware (Dacom, AppleJeus), TraderTraitor
- C2: HTTPS, sometimes compromised legitimate servers
- Persistence: Launch agents (macOS), scheduled tasks (Windows)

**Detection Opportunities:**
- npm/pip packages with typosquatting domains
- macOS launch agent plist files
- Process executing from userspace with network connections
- Crypto transaction monitoring

## Hunt Methodology for Case Studies

1. **Map to Kill Chain phase** — Identify which phase each finding represents
2. **Map to MITRE ATT&CK** — TTP-level mapping for standardization
3. **Identify hunt gaps** — Which phases have no findings? (blind spots)
4. **Build full timeline** — Chronological reconstruction of entire attack
5. **Document containment priority** — Earlier phases = better containment

## Gotchas

- Case studies di exam mungkin menggunakan threat actor yang berbeda dari yang dipelajari — fokus pada TTP pattern, bukan nama group
- LockBit adalah contoh paling umum — pahami full attack chain-nya
- APT29 sering muncul karena kaitannya dengan SolarWinds supply chain attack
- Jangan hanya menghafal case studies — pahami methodology hunting untuk setiap fase
- Setiap fase Kill Chain memiliki hunt indicators yang berbeda — pastikan semua fase tercakup

## Best Practices

- Buat template mapping ATT&CK untuk setiap case study
- Identifikasi detection blind spots per case study
- Praktikkan menulis hunt narrative untuk setiap case study
- Gunakan case studies sebagai referensi untuk hypothesis development
