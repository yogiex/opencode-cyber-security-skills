---
name: "Wireless, IoT & OT/SCADA Exploitation"
description: "Specialized exploitation techniques for CPENT covering wireless attacks (WPA/WPA2 cracking, Evil Twin), IoT exploitation (default creds, firmware, MQTT), and OT/SCADA (Modbus, PLC, DNP3, industrial protocols) with protocol-specific tooling."
tags: [wireless, iot, scada, modbus, plc, ot-security, industrial-controls]
---

# Wireless, IoT & OT/SCADA

## Wireless Attacks (Modul 9)

- WPA/WPA2 cracking: handshake capture, PMKID
- WPS PIN attack: brute force PIN
- Evil Twin: fake AP untuk capture handshake
- Deauthentication: force client reconnect
- Wireless reconnaissance: airodump-ng, Kismet

## IoT Exploitation (Modul 10)

- Default credentials: admin:admin, root:root
- Exposed debug interfaces: UART, JTAG, telnet
- Firmware analysis: binwalk, strings, firmware extraction
- MQTT enumeration: mosquitto_sub, common topics
- Web interface → internal network access

## OT/SCADA Exploitation (Modul 11)

**Key Protocols:**
- **Modbus** (port 502): Read/write coils, registers
- **DNP3** (port 20000): SCADA communication protocol
- **BACnet** (port 47808): Building automation

**Modbus Enumeration:**
```bash
nmap -sV -p 502 $TARGET --script modbus-discover
mbtget -w 0 $TARGET
```

**Mindset:**
- Industrial protocols menggunakan port non-standard
- Web interface sering jadi entry point ke SCADA network
- Insecure protocols (plaintext) adalah vector umum
- PLC manipulation bisa memberikan control system access

## Best Practices

- IoT/SCADA adalah zone-specific — pelajari protocol dasar sebelum exam
- Prioritaskan web interface untuk entry ke IoT devices
- Modbus adalah protokol SCADA paling umum di CPENT
- Wireless tools siapkan sebelum exam (external adapter mungkin diperlukan)
