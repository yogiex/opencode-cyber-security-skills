---
name: "Wireless, IoT & OT/SCADA — Permukaan Non-Konvensional"
description: "Eksploitasi wireless, IoT, dan OT/SCADA untuk operator: WPA/WPA2/PMKID, evil twin, default credential perangkat, UART/JTAG, analisis firmware, MQTT, Modbus/DNP3/BACnet/S7 — dengan aturan keselamatan read-only pada sistem industri."
tags: [wireless, iot, scada, modbus, dnp3, bacnet, mqtt, ot-security, firmware]
---

# Wireless, IoT & OT/SCADA

Tiga permukaan ini punya kesamaan: perangkat jarang bisa dipatch, protokol sering tanpa autentikasi, dan dampak kesalahan bisa fisik. Kecepatan bukan prioritas; keselamatan dan bukti yang bisa dipertanggungjawabkan yang utama.

## 1. Wireless

| Serangan | Prasyarat | Catatan |
|---|---|---|
| Handshake WPA2 | Client terhubung, capture pasif | Deauth untuk mempercepat, hati-hati mengganggu |
| PMKID | Router mengirim PMKID di assoc | Tanpa client; `hcxdumptool` |
| WPS PIN | WPS aktif | Rentan brute force; banyak AP modern sudah menonaktifkan |
| Evil twin | AP palsu + captive portal | Untuk uji kesadaran, bukan pencurian kredensial nyata |
| WPA3 SAE | — | Tidak ada offline crack; fokus ke downgrade/transisi mode |

```bash
airmon-ng start wlan0
airodump-ng -w cap wlan0mon
hcxdumptool -i wlan0mon -o pmkid.pcapng
hashcat -m 22000 pmkid.pcapng wordlist.txt
```

Adapter eksternal dengan mode monitor dan packet injection hampir selalu diperlukan.

## 2. IoT

- **Default credential** — `admin:admin`, `root:root`, kredensial di manual.
- **Debug interface** — UART (paling umum), JTAG, SWD, telnet, SSH dengan password lemah.
- **Firmware** — ekstrak dengan `binwalk`/`unblob`, cari hardcoded secret, skrip startup, dan update mechanism.
- **MQTT** — port 1883/8883, sering tanpa autentikasi; enumerasi topik dan baca pesan.
- **Web interface** — paling sering menjadi pintu masuk ke jaringan internal.

```bash
nmap -Pn -sV -p 23,80,443,1883,8883,554,8080 $TARGET
mosquitto_sub -h $TARGET -t '#' -v
binwalk -e firmware.bin
```

UART: identifikasi pin (GND, TX, RX, VCC) dengan multimeter/logic analyzer, sambung ke adapter USB-TTL, buka serial dengan baudrate umum (115200, 57600, 38400).

## 3. OT/SCADA

### Protokol

| Protokol | Port | Fungsi |
|---|---|---|
| Modbus TCP | 502 | Baca/tulis coil dan register |
| DNP3 | 20000 | Telemetri SCADA |
| BACnet | 47808/udp | Building automation |
| S7comm | 102 | Siemens PLC |
| EtherNet/IP | 44818/tcp, 2222/udp | Rockwell/ODVA |

```bash
nmap -Pn -sV -p 502 --script modbus-discover $PLC
nmap -Pn -sV -p 102 --script s7-info $PLC
nmap -Pn -sV -p 47808 --script bacnet-info $HOST
mbpoll -a 1 -t 4 -r 1 -c 10 $PLC
```

### Aturan keselamatan

1. **Read-only default.** Enumerasi register dan identifikasi perangkat tidak mengubah state.
2. **Write hanya dengan izin tertulis**, pendamping operator, dan prosedur rollback.
3. **Jangan pernah** menulis coil/register yang menggerakkan aktuator tanpa rencana eksplisit.
4. Uji di lab atau replika dulu; produksi adalah tempat terakhir.
5. Catat setiap paket yang dikirim, termasuk yang read-only.

> Modbus tidak punya autentikasi. Satu fungsi write yang salah bisa mengubah posisi valve atau status breaker. Perlakukan setiap target OT sebagai sistem yang sedang beroperasi.

## 4. Pivot dari perangkat

Perangkat IoT/OT yang dual-homed adalah jembatan ke jaringan kontrol. Setelah shell:

```bash
ip a; ip route; arp -a
cat /proc/net/route
```

Dari situ, peta segmen mengikuti prosedur di `network-topologies.md`, dengan aturan level Purdue.

## 5. Jebakan

1. **Deauth berlebihan** — mengganggu pengguna dan bisa dianggap insiden.
2. **Firmware terenkripsi** — butuh analisis runtime, bukan hanya binwalk.
3. **Protokol proprietary** — dokumentasi vendor atau reverse engineering engine.
4. **Device watchdog** — perangkat reboot saat disalahgunakan; siapkan akses ulang.
5. **Uji OT di jam produksi** — selalu jadwalkan di luar operasi normal.

## 6. Best Practices

- Wireless: catat channel, BSSID, dan waktu capture.
- IoT: simpan firmware asli dan hash-nya sebelum modifikasi apa pun.
- OT: read-only sampai izin write eksplisit; dampingi operator.
- Semua: bukti identitas perangkat (model, firmware, IP) di frame yang sama.
