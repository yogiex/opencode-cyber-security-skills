---
name: "Containment, Eradication & Recovery"
description: "Containment strategies, eradication procedures, recovery validation, and post-incident hardening for OSIR exam scenarios."
tags: [containment, eradication, recovery, hardening, incident-response]
---

# Containment, Eradication & Recovery

## Containment Strategy Reference

| Scenario | Short-Term | Long-Term |
|----------|------------|-----------|
| **Ransomware** | Network isolate infected host, block ransomware C2 IP | Reimage host, restore from clean backup, patch entry point |
| **Phishing** | Disable compromised account, block sender domain | Password reset, MFA enrollment, user training |
| **C2 Beacon** | Block C2 IP/Domain at firewall, DNS sinkhole | Host EDR scan, remove persistence, verify clean |
| **Data Exfiltration** | Block outbound to unknown IPs, disable risky accounts | Rotate API keys, audit data access, DLP rules |
| **Lateral Movement** | Segment affected VLAN, disable source account | Credential rotation, implement LAPS, tiered admin model |

## Containment Decision Matrix

```
Ransomware in progress → Immediate network isolation
Data exfiltration detected → Block C2 IP + contain host
Insider threat → Disable account + preserve evidence
Phishing campaign → Block sender domain + email rules
```

## Eradication Checklist

```
[ ] Malware removed via AV/EDR scan
[ ] Malicious services stopped + deleted
[ ] Scheduled tasks removed
[ ] Registry persistence entries cleaned
[ ] Backdoor accounts identified + disabled
[ ] Web shells removed from web servers
[ ] Compromised creds rotated
[ ] API keys rotated
[ ] System reimaged (if necessary)
[ ] Verify eradication via re-scan
```

## Recovery Validation

```
[ ] System operational (verified by IT)
[ ] Service restored to users
[ ] Data integrity verified
[ ] Backup validated as clean
[ ] Patches applied (root cause addressed)
[ ] Monitoring re-enabled with heightened alerting
[ ] Incident documented in case management system
```

## Post-Incident Hardening

```
Phishing-resistant MFA (FIDO2/WebAuthn)
Network segmentation (DMZ, VoIP, Corp, Guest)
EDR deployment on all endpoints
Credential Guard (Windows Defender Credential Guard)
LAPS for local admin passwords
Admin tiering (Tier 0/1/2 model)
AppLocker or WDAC (Windows Defender Application Control)
```

## Gotchas

- Di OSIR report, containment strategy harus **spesifik** — jangan tulis "block the attacker" tapi sebutkan "block IP 10.0.0.5 at firewall using ACL rule #100"
- Short-term containment ≠ long-term containment — exam akan membedakan keduanya di soal
- Eradication harus diverifikasi — jangan asumsikan malware hilang setelah scan. Tulis langkah verifikasinya

## Best Practices

- Buat containment decision tree sebelum exam agar bisa mengambil keputusan cepat
- Selalu prioritaskan containment di atas forensik — data bisa dikumpulkan setelah host terisolasi
- Dokumentasikan timeline containment (siapa melakukan apa, kapan) untuk report
- Recovery validation adalah langkah yang paling sering dilupakan — pastikan monitoring diaktifkan kembali
