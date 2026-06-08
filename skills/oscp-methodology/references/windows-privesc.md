---
name: "Windows Privilege Escalation — 6 Attack Vectors"
description: "Windows privilege escalation methodology for OSCP covering token abuse (SeImpersonate, SeBackup), service misconfigurations (unquoted paths, weak permissions), AlwaysInstallElevated, credential hunting, scheduled tasks, and startup applications."
tags: [windows, privilege-escalation, token-abuse, service-misconfig, alwaysinstallelevated, credential-hunting]
---

# Windows Privilege Escalation

## Enumerasi Prioritas

```
1. whoami /all              # Tokens & group memberships
2. systeminfo               # OS version, patches, hotfixes
3. wmic qfe get Caption     # Installed patches
4. WinPEAS                  # Automated enumeration
5. cmdkey /list             # Stored credentials
6. netstat -ano             # Listening ports
```

## Vector 1 — Token Abuse

SeImpersonatePrivilege atau SeAssignPrimaryTokenPrivilege:
- Potato family: GodPotato, PrintSpoofer, SweetPotato, JuicyPotato
- Biasanya dimiliki service accounts (IIS, MSSQL)
- Instant SYSTEM level access

Cek juga: SeBackupPrivilege, SeRestorePrivilege, SeDebugPrivilege, SeTakeOwnershipPrivilege

## Vector 2 — Service Misconfigurations

```powershell
# PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1; Invoke-AllChecks
```

Tiga jenis:
1. **Unquoted Service Path**: path mengandung spasi tanpa quotes
2. **Writable Service Binary**: bisa di-overwrite
3. **Weak Service Permissions**: bisa dimodifikasi oleh low-privileged user

## Vector 3 — AlwaysInstallElevated

```powershell
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
```

Jika keduanya = 1 → buat MSI payload → SYSTEM shell.

## Vector 4 — Credential Hunting

- LSASS dump: procdump, Task Manager
- SAM: `reg save HKLM\SAM sam.save`
- Unattended files: C:\Windows\Panther\unattend.xml
- PowerShell history: `(Get-PSReadLineOption).HistorySavePath`
- Registry AutoLogon
- Browser saved passwords: LaZagne, SharpChrome

## Vector 5 — Scheduled Tasks

```powershell
schtasks /query /fo LIST /v
Get-ScheduledTask | Get-ScheduledTaskInfo
```

## Vector 6 — Startup Applications

```powershell
wmic startup get caption,command
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

## Best Practices

- WinPEAS untuk fast enumeration, manual checks untuk confirmation
- Potato exploits sering work di Windows Server 2016/2019
- Unquoted service paths adalah vector paling umum
- Selalu cek unattended install files setelah dapat shell
