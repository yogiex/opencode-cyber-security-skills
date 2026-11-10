---
name: "Tools and Diagnostics — Field Kit Read-Only"
description: "Perangkat dan perintah diagnostik yang dipakai defender: inventaris, firewall, trafik, log, endpoint, kerentanan, cloud, dan wireless — dengan prinsip read-only, otorisasi, dan cara menyimpan bukti."
tags: [tools, diagnostics, tcpdump, wireshark, nftables, iptables, ss, journalctl, sysinternals, osquery, cloud-cli]
---

# Tools and Diagnostics — Field Kit Read-Only

Alat bukan identitas. Defender dinilai dari keputusan, bukan dari panjang daftar tool. Namun tanpa kemampuan mengukur, keputusan hanya opini.

## 1. Prinsip

- **Read-only lebih dulu.** Perintah yang mengubah state hanya setelah desain, otorisasi, dan rollback.
- **Otorisasi jelas.** Pemindaian dan capture pada jaringan pihak lain memerlukan izin.
- **Simpan bukti** ke file dengan timestamp; jangan mengandalkan scrollback terminal.
- **Privasi.** pcap dan log bisa memuat data pribadi; batasi akses dan retensi.
- **Satu perintah, satu tujuan.** Catat mengapa perintah dijalankan.

## 2. Inventaris dan topologi

```bash
ip -br a; ip r; ip neigh
ss -tunlp
sudo lldpctl 2>/dev/null || sudo lldpcli show neighbors
arp -a
```

```powershell
Get-NetIPConfiguration
Get-NetRoute
Get-NetTCPConnection -State Listen
```

Pemindaian hanya bila diotorisasi:

```bash
sudo nmap -sn 10.10.0.0/24          # host discovery
sudo nmap -sT -p 22,80,443 10.10.5.10
```

## 3. Firewall dan routing

```bash
sudo nft list ruleset -a
sudo iptables -S; sudo iptables -vnL --line-numbers
sudo nft list counters
```

```powershell
Get-NetFirewallRule | Where-Object Enabled -eq True |
  Select-Object DisplayName, Direction, Action, Profile
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction
```

Perangkat jaringan (vendor CLI): `show running-config`, `show access-lists`, `show ip route`, `show conn` (conntrack), `show log`. Simpan output ke file sebelum mengubah apa pun.

## 4. Trafik

```bash
sudo tcpdump -i any -nn -c 500 -w capture.pcap
sudo tcpdump -i eth0 -nn 'tcp port 443 and host 10.10.5.23'
sudo tshark -r capture.pcap -Y 'dns' -T fields -e dns.qry.name | sort | uniq -c | sort -rn | head
```

Filter Wireshark yang sering dipakai:

```
ip.addr == 10.10.5.23 && tcp.flags.syn == 1
dns.qry.name contains "suspicious"
tls.handshake.extensions_server_name contains "example"
http.request.method == "POST"
```

Zeek/Suricata (bila tersedia): `zeek -i eth0 local`, `suricata -i eth0 -c suricata.yaml`, lalu baca `conn.log`, `dns.log`, `http.log`, `fast.log`.

Monitoring volume: `iftop`, `nload`, `vnstat`, atau metrik interface.

## 5. Log

```bash
journalctl -u ssh --since "2026-11-09 00:00" --no-pager
sudo ausearch -m USER_LOGIN -ts recent
sudo grep -i "failed password" /var/log/auth.log | tail -50
```

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625; StartTime=(Get-Date).AddDays(-1)} |
  Select-Object TimeCreated, Id, Message -First 20
wevtutil qe Security /q:"*[System[(EventID=4624)]]" /c:20 /f:text
```

Sumber yang perlu dicek: auth (SSO/AD), firewall, proxy, DNS, EDR, web server, cloud audit.

## 6. Endpoint

```bash
sudo auditctl -l
sudo ss -tunap
sudo lsof -i -P -n | head
sudo ps auxf
```

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 15
Get-CimInstance Win32_Service | Where-Object State -eq 'Running'
Get-MpComputerStatus
```

osquery (bila ada): `osqueryi "select * from listening_ports;"`, `osqueryi "select * from processes where cmdline like '%powershell%';"`.

Sysinternals: Autoruns, Process Explorer, TCPView — untuk melihat persisten dan koneksi.

## 7. Kerentanan dan baseline

- Scanner (Nessus/OpenVAS) — hanya pada scope yang disetujui, dengan jadwal.
- `nmap --script vuln` — kasar, untuk indikasi awal, bukan bukti.
- CIS-CAT / Lynis untuk baseline host.
- Patch level: `apt list --upgradable`, `dnf check-update`, `Get-HotFix`, `wmic qfe` (legacy).

Hasil scanner adalah kandidat temuan; verifikasi dan konteks eksposur tetap diperlukan.

## 8. Cloud

```bash
aws ec2 describe-security-groups --query "SecurityGroups[?IpPermissions[?IpRanges[?CidrIp=='0.0.0.0/0']]]"
aws s3api get-bucket-acl --bucket NAME
aws cloudtrail lookup-events --max-results 20
```

```bash
az network nsg list --query "[].{name:name, rules:securityRules}" -o json
gcloud compute firewall-rules list
```

Gunakan kredensial read-only dan catat akun/region yang dipakai. Perubahan lewat CLI memerlukan persetujuan yang sama seperti perubahan lainnya.

## 9. Wireless

```bash
iw dev
sudo iw dev wlan0 scan | grep -E "SSID|RSN|WPA|channel"
```

`airodump-ng` dan alat sejenis hanya untuk audit yang diotorisasi; jangan menangkap trafik pihak ketiga.

## 10. Menyimpan bukti

- Nama file: `YYYYMMDD-HHMMSS-host-perintah.pcap/.log`.
- Sertakan perintah, waktu, dan siapa yang menjalankan di catatan terpisah.
- Hash file bukti bila akan diserahkan (`sha256sum`).
- Simpan di lokasi dengan kontrol akses, bukan folder bersama.

## Best Practices

- Read-only sebelum write; ukur sebelum ubah.
- Otorisasi dan jadwal untuk pemindaian/capture.
- Simpan output ke file, jangan mengandalkan terminal.
- Lindungi bukti dan data pribadi.
- Pilih alat yang bisa dijelaskan, bukan yang paling populer.
