---
name: "Wireless, IoT & OT Network Security"
description: "Security of Wi-Fi (WPA2/WPA3, 802.1X/EAP, evil twin, deauth, PMF), Bluetooth/BLE, IoT protocols (MQTT, CoAP, AMQP, Zigbee, Z-Wave, Matter), and OT/ICS networks (Purdue, IEC 62443 zones/conduits, Modbus/DNP3/OPC UA/PROFINET, safety vs security, segmentation, data diodes), plus 5G/edge, pitfalls, and best practices."
tags: [wireless, wifi, wpa2, wpa3, 802.1x, eap, evil-twin, deauth, pmf, bluetooth, ble, iot, mqtt, coap, amqp, zigbee, z-wave, matter, ot, ics, purdue, iec-62443, modbus, dnp3, opc-ua, profinet, data-diode, 5g, edge, segmentation]
---

# Wireless, IoT & OT Network Security

Wireless, IoT, and OT networks extend the IT perimeter into spaces with weak physical control, long device lifecycles, and safety-critical consequences. This reference covers Wi-Fi/BLE, IoT protocols, OT/ICS architectures, 5G/edge, pitfalls, and best practices.

## Wi-Fi Security

### WPA2 and WPA3

**WPA2** (IEEE 802.11i) uses AES-CCMP (Counter Mode with CBC-MAC Protocol) for confidentiality and integrity. The Personal mode derives keys from a pre-shared key (PSK) via PBKDF2-HMAC-SHA1 (4096 iterations), making it vulnerable to offline dictionary attacks against captured 4-way handshakes. The Enterprise mode uses 802.1X/EAP for per-user authentication and per-session keys.

**WPA3** improves both modes. **WPA3-Personal** replaces PSK with SAE (Simultaneous Authentication of Equals, Dragonfly key exchange), providing forward secrecy and offline-dictionary resistance even with weak passwords. **WPA3-Enterprise** mandates 192-bit security (CNSA suite) and requires PMF. **WPA3-Transition mode** allows mixed clients but is downgradeable (transition-disable attack).

### 802.1X and EAP

802.1X port-based access control has three roles: **supplicant** (client), **authenticator** (AP/switch), and **authentication server** (RADIUS). EAP methods vary in security:

| EAP Method | Auth | Tunnel | Notes |
|------------|------|--------|-------|
| EAP-TLS | Certificates | TLS | Strongest; requires PKI |
| PEAP | Password (MSCHAPv2) | TLS | Common; vulnerable to rogue RADIUS |
| EAP-TTLS | Password/PAP | TLS | Flexible inner methods |
| EAP-FAST | PAC | TLS | Cisco; PAC provisioning risk |
| EAP-PSK | PSK | None | Weak; avoid |
| LEAP | MSCHAPv1 | None | Broken; deprecated |

Key risks: rogue RADIUS servers (evil twin APs offering a weaker EAP method), credential theft via MSCHAPv2 challenge capture, and missing server certificate validation on clients.

### Evil Twin and Rogue APs

An **evil twin** clones a legitimate SSID/BSSID to lure clients, then performs MITM, credential harvesting, or traffic inspection. Defenses: 802.1X with server cert validation, WPA3, WIDS/WIPS, RF monitoring, and disabling auto-connect to open networks. **Rogue AP** detection compares discovered APs against an authorized inventory (MAC, location, SSID).

### Deauthentication Attacks

Deauth frames (management frames in 802.11) are unauthenticated in WPA2, allowing attackers to send spoofed deauth/disassoc frames to disconnect clients, enabling handshake capture or denial of service. **Protected Management Frames (PMF / 802.11w)** authenticates and encrypts management frames, mitigating deauth/disassoc spoofing. WPA3 requires PMF; WPA2 makes it optional (should be required).

### PMF (Protected Management Frames)

PMF authenticates robust management frames (deauth, disassoc, action) with CMAC. Without it, any client on the channel can inject deauth frames. Enable PMF as "required"; segment or upgrade legacy clients lacking support.

## Bluetooth and BLE

**Classic Bluetooth** (BR/EDR) uses pairing (PIN/passkey), encryption (E0 stream cipher, now considered weak), and frequency hopping. **BLE** (Bluetooth Low Energy) uses pairing modes: Just Works (no MITM protection), Passkey Entry, Out of Band (OOB), and Numeric Comparison (LE Secure Connections). LE Secure Connections (introduced in 4.2) uses ECDH (P-256) for key agreement.

Threats: BlueBorne (RCE via Bluetooth stack flaws), KNOB (key-negotiation downgrade), BIAS (impersonation), BLESA (spoofing), tracking via static MACs (mitigated by address randomization), and sniffing of unencrypted advertising data. Defenses: disable Bluetooth when unused, require LE Secure Connections + Numeric Comparison, randomize addresses, patch firmware, restrict pairing windows, and segment Bluetooth devices.

## IoT Protocols

### MQTT

Pub/sub broker model (v3.1.1/5.0); TCP 1883 or TLS 8883. Security: TLS, username/password or client certs, per-topic ACLs, QoS 0/1/2. Risks: anonymous brokers, wildcard subscriptions leaking data, retained messages exposing state, weak defaults. Mitigate: TLS, per-device credentials, topic ACLs, disable anonymous access.

### CoAP

REST-like, UDP-based (port 5683) for constrained devices. Security via DTLS (5684) or OSCORE (RFC 8613) for end-to-end object-level security. Risks: UDP amplification (DDoS reflector), missing DTLS, resource exhaustion.

### AMQP

Enterprise messaging (RabbitMQ, Service Bus); TCP 5672 or TLS 5671. Security: TLS, SASL (PLAIN/EXTERNAL/SCRAM), vhost isolation, per-user permissions. Risks: default guest/guest, exposed management port (15672), federation misconfig.

### Zigbee

IEEE 802.15.4 mesh. Security: AES-128-CCM*, shared network key, optional link keys. Joining uses install codes or default trust-center keys (well-known keys are a major weakness). Threats: key extraction, replay, worm propagation, traffic analysis. Mitigate: install codes, unique network keys, disable legacy join, monitor joins.

### Z-Wave

Sub-GHz mesh for home automation. S2 uses ECDH + AES-128; legacy S0 uses a known key. Auth via DSK QR code. Risks: S0 downgrade, key extraction. Use S2 devices, verify DSKs, segment gateways.

### Matter

CSA standard unifying smart home; Thread or Wi-Fi transport, Bluetooth commissioning. Security: DAC device attestation, CASE with SPAKE2+ during commissioning, AES-128-CCM sessions, fabric-scoped keys. Risks: commissioning-window exposure, fabric-admin compromise, attestation key leakage. Keep commissioning time-limited; secure fabric admins.

## OT / ICS Security

### Purdue Model

The **Purdue Enterprise Reference Architecture (PERA)** layers industrial networks:

| Level | Name | Contents |
|-------|------|----------|
| 0 | Physical Process | Sensors, actuators, field devices |
| 1 | Basic Control | PLCs, RTUs, DCS controllers |
| 2 | Area Supervisory | HMIs, SCADA servers, engineering workstations |
| 3 | Site Operations | Historians, MES, patch servers, site DMZ |
| 3.5 | Industrial DMZ | Data diodes, firewalls between IT and OT |
| 4 | Enterprise IT | Business systems, ERP, email |
| 5 | External | Internet, cloud, partners |

Key principle: traffic flows vertically between adjacent levels; direct Level 0/1 to Level 4/5 access is prohibited. The industrial DMZ (Level 3.5) mediates all IT/OT data exchange.

### IEC 62443 Zones and Conduits

IEC 62443 (ISA-99) defines **zones** (assets with common security requirements) and **conduits** (communication paths with defined controls). Each zone has a Security Level (SL 0–4) by threat/consequence; conduits enforce the communicating zones' SL (firewall, data diode, encrypted tunnel). Foundational requirements: I&A, use control, system integrity, data confidentiality, restricted data flow, timely response to events, resource availability.

### Industrial Protocols

| Protocol | Transport | Security | Notes |
|----------|-----------|----------|-------|
| Modbus (TCP/RTU) | TCP 502 / serial | None native | No auth/encryption; legacy; needs gateway protection |
| DNP3 | TCP/UDP 20000 / serial | Secure Authentication (SAv5) optional | Used in utilities; SAv5 adds HMAC |
| OPC UA | TCP 4840 / HTTPS | Certificates, signing, encryption | Modern; supports user auth and audit |
| PROFINET | Ethernet (RT) | PROFINET Security (optional) | Real-time; security add-on |
| EtherNet/IP | TCP/UDP 44818 | CIP Security (optional) | Rockwell ecosystem |
| BACnet | IP/MS/TP | BACnet/SC (secure connect) | Building automation |

Most legacy protocols lack authentication, integrity, or confidentiality; protect via network segmentation, protocol-aware gateways, and monitoring rather than retrofitting.

### Safety vs Security

**Safety** ensures fail-safe state (IEC 61508/61511, ISO 13849); **security** protects against intentional harm. They conflict: patches may add latency breaking real-time loops; safety-required open ports may be security holes; E-stop must stay available under attack. Integrate IEC 62443 with functional safety; run safety-impact assessments. Never block safety-critical traffic without safety review.

### Segmentation and Data Diodes

OT segmentation uses VLANs, firewalls, and unidirectional **data diodes** (hardware-enforced one-way flow) between IT and OT, letting monitoring data out with no inbound path. Diodes are the strongest guarantee for unidirectional flows (historian replication, telemetry). Combine with allowlisted protocols, DPI gateways, separate management domains. Avoid bidirectional paths bypassing the diode ("temporary" VPNs).

## 5G and Edge

5G attack surface: **network slicing** (isolation must be enforced), **MEC/edge** (distributed compute at base stations, physical-access risk), **NFV** (VNFs share hypervisors), **SUPI/SUCI** (subscriber identity protection via PK encryption), and **SBA** APIs secured via OAuth/TLS. Edge lacks physical security; use TPM/secure boot, remote attestation, encrypted storage, zero-trust management. Private 5G for OT needs integration with IEC 62443 zones.

## Pitfalls

- WPA2-Personal PSKs are offline-crackable; PMF "capable" allows downgrade.
- Unvalidated RADIUS certs enable evil-twin credential theft.
- Anonymous/default-cred IoT brokers exposed to the internet.
- VLANs without firewall enforcement ≠ segmentation.
- OT patching without safety review risks process disruption.
- "Temporary" bidirectional links across OT DMZs become permanent.
- BLE "Just Works" has no MITM protection.
- 5G slicing isolation must be verified, not assumed.
- Default Zigbee trust-center keys compromise whole networks.

## Best Practices

- Require WPA3 (or WPA2+PMF required) and 802.1X/EAP-TLS for enterprise Wi-Fi.
- Validate server certs in EAP; prefer EAP-TLS.
- Enable PMF required; segment legacy clients.
- Disable Bluetooth/BLE when unused; require LE Secure Connections.
- Encrypt IoT traffic (TLS/DTLS/OSCORE); per-device creds and ACLs.
- Commission Matter in time-limited windows; secure fabric admins.
- Apply Purdue layering + IEC 62443 zones/conduits with SLs.
- Use data diodes for IT→OT flows; allowlist protocols.
- Separate safety/security change control; safety impact assessments.
- Monitor wireless/OT with dedicated IDS; baseline traffic.
- Maintain asset inventories; track EOL/firmware.

## Gotchas

- WPA3-Transition is downgradeable; prefer WPA3-only SSIDs.
- Deauth persists where PMF isn't required.
- BLE advertising data is often unencrypted/trackable.
- MQTT retained messages and wildcards leak state/data.
- CoAP's UDP nature enables amplification.
- Modbus/DNP3 lack native security; rely on network controls.
- Data diodes break bidirectional protocols; use gateways.
- OT patch windows are rare; compensating controls essential.
- 5G edge nodes often have weak physical security.

---

*Reference — Wireless, IoT & OT Network Security.*
