---
name: "Password Cracking Methodology — Hashcat & Rules"
description: "Password cracking strategy for OSCP covering hash identification, layered hashcat attack strategy (wordlist → rules → hybrid → mask), common hash modes, and rule-based attack optimization."
tags: [password-cracking, hashcat, john, rules, wordlist, mask-attack]
---

# Password Cracking Methodology

## Hash Identification

```bash
hashid hash.txt
hash-identifier
```

Format prefix: `$1$` = MD5 crypt, `$5$` = SHA256 crypt, `$6$` = SHA512 crypt, `$2y$` = bcrypt.

## Layered Attack Strategy

| Layer | Strategy | Command |
|-------|----------|---------|
| 1 | Wordlist langsung | `hashcat -m 0 -a 0 hashes.txt rockyou.txt` |
| 2 | best64 rules | `-r /usr/share/hashcat/rules/best64.rule` |
| 3 | Hybrid wordlist+mask | `-a 6 rockyou.txt '?d?d'` |
| 4 | dive.rule / OneRuleToRuleThemAll | `-r dive.rule` |
| 5 | Mask attack | `-a 3 ?a?a?a?a?a?a?a` |

## Rule-Based Attack

Rules transform setiap word di wordlist sebelum di-hash. Rule `c $1$2$3` mengubah `password` menjadi `Password123`. Dengan best64 (64 rules), 14 juta kata rockyou menjadi 900 juta candidates — semua di RAM.

## Hashcat Modes for OSCP

| Hash Type | Mode (-m) |
|-----------|-----------|
| MD5 | 0 |
| SHA1 | 100 |
| SHA256 | 1400 |
| SHA512 | 1700 |
| NTLM | 1000 |
| NetNTLMv2 | 5600 |
| bcrypt | 3200 |
| SHA512crypt ($6$) | 1800 |
| Kerberos 5 TGS-REP | 13100 |
| AS-REP | 18200 |

## Best Practices

- Mulai dengan wordlist langsung (rockyou) sebelum rules
- best64 adalah minimal viable rule — cukup untuk OSCP
- Cracking di VM dengan GPU passthrough jauh lebih cepat
- Prioritaskan NTLM (mode 1000) dan NetNTLMv2 (mode 5600)
