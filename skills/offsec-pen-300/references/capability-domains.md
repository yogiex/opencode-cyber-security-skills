---
name: "Capability Domains — Peta Kompetensi Operator Evasion"
description: "Peta 8 domain kapabilitas operator evasion dan red team — payload engineering, eksekusi client-side, process injection, defense evasion, C2, movement, data platform & AD, serta integrasi rantai — lengkap dengan teknik inti dan bukti khasnya."
tags: [capability-map, domains, payload-engineering, evasion, process-injection, c2, active-directory, adcs]
---

# Capability Domains

Delapan domain di bawah adalah peta kemampuan yang melekat pada persona ini. Ini bukan silabus yang harus dihafal, melainkan daftar "kalau masalahnya di sini, ini yang saya kuasai dan ini buktinya". Penomoran hanya alat navigasi, bukan urutan penguasaan.

## Peta domain

| # | Domain | Kapabilitas inti | Bukti khas |
|---|---|---|---|
| 1 | Payload engineering | Win32 API, P/Invoke, marshaling, PEB/TEB, shellcode runner, encoding XOR/AES | loader terkompilasi, payload ter-encode, callback terverifikasi |
| 2 | Eksekusi client-side | VBA macro, PowerShell download cradle, HTA/JScript, DotNetToJScript | dokumen atau HTA yang mengeksekusi di host target |
| 3 | Process injection | remote thread, DLL injection, reflective DLL, process hollowing, migrasi | eksekusi di proses target, migrasi yang stabil |
| 4 | Defense evasion | signature, heuristic, behavior, AMSI, AppLocker, CLM, UAC | payload melewati kontrol, jejak telemetri tercatat |
| 5 | Jaringan dan C2 | DNS tunneling, domain fronting, proxy, Metasploit, Sliver, Mythic, staging | callback lolos egress, transport konsisten |
| 6 | Movement Windows/Linux | Mimikatz, SAM/LSASS, RDP/WMI/WinRM/DCOM/SMB, LD_PRELOAD, SSH, kiosk breakout | akses host berikutnya, kredensial baru |
| 7 | Data platform dan direktori | MSSQL linked server, `xp_cmdshell`, delegation, forest trust, ADCS ESC1–ESC8 | akses SQL, tiket, sertifikat, domain dominance |
| 8 | Integrasi dan bukti | rantai serangan, paket bukti, cleanup, pelaporan | rantai yang bisa direproduksi, laporan diterima |

## Teknik inti

### 1. Payload engineering

- **Win32 API**: `VirtualAlloc`, `CreateThread`, `WaitForSingleObject`, `OpenProcess`, `WriteProcessMemory`, `CreateRemoteThread`.
- **C# P/Invoke**: `DllImport`, marshaling, `StructLayout` untuk memanggil Windows API dari .NET.
- **PowerShell reflection**: akses assembly internal via `[Ref].Assembly.GetType()`.
- **Arsitektur proses**: PEB, TEB, user space versus kernel space, ring protection.
- **Runner**: shellcode di-decode di memori, dialokasikan, lalu dieksekusi lewat thread baru. Detail ada di [shellcode-runners.md](./shellcode-runners.md) dan [process-injection.md](./process-injection.md).

### 2. Eksekusi client-side

- **VBA**: `AutoOpen`/`Document_Open` sebagai entry point; XOR atau Caesar untuk menyandikan shellcode; PowerShell download cradle → AMSI bypass → shellcode runner; WMI untuk spawn proses dari VBA.
- **JScript/HTA**: `.hta` dieksekusi `mshta.exe`; `WScript.Shell`, `XMLHttpRequest`, `ADODB.Stream`; `DotNetToJScript` untuk memuat assembly .NET dari JScript.

### 3. Process injection

- **Remote thread**: `OpenProcess` → `VirtualAllocEx` → `WriteProcessMemory` → `CreateRemoteThread`.
- **Reflective DLL**: memuat DLL dari memori tanpa menyentuh disk; implementasi manual `LoadLibrary` dan resolusi import.
- **Hollowing**: `CreateProcess` dengan `CREATE_SUSPENDED` → `NtUnmapViewOfSection` → `VirtualAllocEx` → `WriteProcessMemory` → `SetThreadContext` → `ResumeThread`.
- **Alternatif stealth**: `NtCreateSection` + `NtMapViewOfSection` dibanding `VirtualAlloc`.

### 4. Defense evasion

- **AV/EDR**: deteksi signature, heuristic, dan behavior; lokasi signature dengan ThreatCheck; strategi berlapis enkripsi → loader → injection → sleep timer → AMSI bypass → AppLocker bypass. Detail ada di [av-edr-evasion.md](./av-edr-evasion.md).
- **AMSI**: enam pendekatan, termasuk `amsiInitFailed`, nulling context, patch `AmsiScanBuffer`, registry disable, custom RunSpace, dan hooking.
- **CLM**: interactive RunSpace, InstallUtil, msbuild inline, `regsvr32 .sct`, PowerShell versi 2.
- **AppLocker**: `InstallUtil.exe`, `msbuild.exe`, `cscript.exe`/`wscript.exe`, `rundll32.exe`, `regsvr32.exe`, `psexec.exe`, `bginfo.exe`.
- **UAC**: teknik bypass yang tersedia di build target; verifikasi dulu apakah jalur yang dipilih memang menaikkan integritas.

### 5. Jaringan dan C2

- **DNS filter**: DNS tunneling (iodine, dnscat2), DoH.
- **Web proxy**: domain fronting via CDN, hidden `.asmx`, bypass HTTPS inspection.
- **IDS/IPS**: fragmentasi payload, encoding, dan enkapsulasi TLS.
- **Framework**: Metasploit untuk baseline cepat, Sliver dan Mythic untuk profil beacon yang lebih terkontrol; StageListener menjembatani stager lama ke agent modern. Detail ada di [c2-strategy.md](./c2-strategy.md).

### 6. Movement Windows dan Linux

- **Kredensial Windows**: Mimikatz (`privilege::debug`, `sekurlsa::logonpasswords`, `lsadump::dcsync`), `reg save HKLM\SAM` + `impacket-secretsdump`, dump LSASS, PowerShell history, password browser, kredensial RDP, GPP `cpassword`, WSL.
- **Lateral Windows**: RDP (Restricted Admin, PTH via `xfreerdp`), WMI, WinRM, PowerShell Remoting, SMB exec, DCOM. Pola: kredensial → uji semua protokol → cari layanan yang menerima → eksekusi.
- **Linux**: shared library hijacking (`LD_PRELOAD`, `LD_LIBRARY_PATH`), backdoor Vim (modeline, plugin), persistence SSH (`authorized_keys`, config tunneling).
- **Kiosk breakout**: escape browser, Task Manager, tombol Windows, shortcut abuse, Sticky Keys, `Utilman.exe`.

### 7. Data platform dan direktori

- **MSSQL**: enumerasi linked server, eksekusi via `EXECUTE(...) AT`, aktivasi `xp_cmdshell`, PowerUpSQL, NTLM hash relay lewat `xp_dirtree`. Detail ada di [mssql-attacks.md](./mssql-attacks.md).
- **Delegation**: unconstrained (ekstraksi TGT), constrained (S4U2Self/S4U2Proxy), RBCD (`msDS-AllowedToActOnBehalfOfOtherIdentity`).
- **Forest trust**: SIDHistory abuse, trust ticket, MSSQL lintas trust.
- **ADCS**: ESC1, ESC3, ESC4, ESC6, ESC8 dengan prasyarat masing-masing. Detail ada di [ad-exploitation.md](./ad-exploitation.md).

### 8. Integrasi rantai

Rantai yang khas, bukan daftar teknik terpisah:

```
1. Phishing → VBA macro → AMSI bypass → C2 beacon
2. BloodHound → delegation misconfiguration
3. RBCD abuse → domain dominance pada Domain A
4. Dump DC → trust key → cross-forest
5. ADCS ESC1 → Enterprise Admin
6. DCSync → domain dominance → bukti dan cleanup
```

Setiap hop dicatat sebagai bagian dari narasi serangan; teknik yang gagal tetap dicatat karena menunjukkan kontrol mana yang bekerja.

## Kelompok kerja

### Membangun akses (1, 2)

Payload engineering dan eksekusi client-side adalah pintu masuk. Nilainya bukan pada kerumitan kode, tetapi pada pemahaman komponen mana yang memicu deteksi dan mana yang tidak.

### Melewati kontrol (3, 4)

Injection dan evasion saling bergantung: loader yang bersih tidak berguna kalau injection memicu behavior alert, dan sebaliknya. Uji terpisah, catat hasilnya.

### Bergerak (5, 6, 7)

C2 adalah transport untuk movement. Kredensial, delegation, ADCS, dan MSSQL adalah jalur menuju hak yang lebih tinggi; pilih jalur yang paling murah menuju objective, bukan yang paling menarik secara teknis.

### Membuktikan (8)

Tanpa bukti yang bisa direproduksi dan cleanup yang terverifikasi, seluruh rantai hanya klaim. Domain ini yang membuat pekerjaan teknis bisa dipertanggungjawabkan ke klien.

## Cara memakai peta ini

1. **Saat menerima target** — petakan pertahanan target ke domain; domain yang tidak relevan tidak perlu dipaksakan.
2. **Saat payload gagal** — tanyakan komponen mana yang belum diuji, bukan encoder mana yang belum dicoba.
3. **Saat memilih jalur** — pilih domain berdasarkan jarak ke objective, bukan berdasarkan kenyamanan.
4. **Saat melapor** — sebut domain, keputusan, dan buktinya; bukan nama tool.

## Best Practices

- Pilih teknik berdasarkan pertahanan target, bukan berdasarkan yang paling nyaman.
- Satu domain yang dalam lebih bernilai daripada lima domain yang dangkal.
- Simpan bukti per domain; itu bahan laporan sekaligus evaluasi.
- Domain 3, 4, dan 7 sering butuh koordinasi dengan pemilik layanan sebelum eksekusi, bukan sesudahnya.
