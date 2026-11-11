---
name: "Wi-Fi 802.1X, EAP, and RADIUS"
description: "Port-based network access control for Wi-Fi: 802.1X roles, EAP methods (EAP-TLS, PEAP, TEAP/EAP-FAST, EAP-TTLS), certificate requirements, RADIUS (RFC 2865/2866, attributes, CoA), deployment patterns, MAB fallback, guest VLAN, and best practices."
tags: [802.1x, eap, radius, wifi, nac, port-based-nac, eap-tls, peap, teap, eap-fast, eap-ttls, mab, guest-vlan, coa, dynamic-authorization, rfc-2865, rfc-2866, certificates, pki]
---

# Wi-Fi 802.1X, EAP, and RADIUS

Port-based Network Access Control (NAC) gates network access until a client proves identity. In Wi-Fi, **IEEE 802.1X** runs between a supplicant (client), an authenticator (access point/switch), and an authentication server (RADIUS), while **EAP** carries the credential exchange and **RADIUS** (RFC 2865/2866) transports it. This reference covers the roles, EAP methods, certificate requirements, RADIUS protocol details, deployment patterns, MAB fallback, guest VLAN, and operational gotchas.

## Port-Based NAC Roles

802.1X defines three roles:

- **Supplicant** — the client device/software requesting access (laptop, phone, IoT). Implements EAP and holds credentials (certificates or passwords).
- **Authenticator** — the network access device (AP, switch, VPN gateway) that blocks the port until authentication succeeds and enforces the resulting authorization (VLAN, ACL, QoS).
- **Authentication Server (AS)** — typically a RADIUS server that validates credentials and returns authorization attributes.

Flow: the authenticator starts in an **unauthorized** state, allowing only EAPOL (EAP over LAN, EtherType 0x888E) traffic. The supplicant sends `EAPOL-Start`; the authenticator relays EAP messages inside RADIUS `Access-Request` packets to the AS. On success the AS returns `Access-Accept` with attributes (VLAN, ACL, session timeout); the authenticator moves the port to **authorized** and applies them. On failure it returns `Access-Reject` and may place the port in a guest/quarantine VLAN.

## EAP Method Comparison

| EAP Method | Credential | Tunnel | Security | Typical Use |
|------------|-----------|--------|----------|-------------|
| EAP-TLS | Client + server certs | TLS | Strongest | Enterprise, regulated |
| PEAPv0 / EAP-MSCHAPv2 | Password | TLS | Good (if cert validated) | Windows AD environments |
| PEAPv1 / EAP-GTC | Password/token | TLS | Good | Token/OTP inner auth |
| TEAP (EAP-FAST) | PAC or certs | TLS | Good | Cisco; PAC provisioning |
| EAP-TTLS | Password/PAP/MSCHAPv2 | TLS | Good | Non-Windows, flexible inner |
| EAP-PSK / LEAP | PSK / MSCHAPv1 | None | Weak/broken | Avoid |

### EAP-TLS

Mutual certificate authentication: both server and client present X.509 certificates inside a TLS tunnel. No passwords traverse the network. Requires a PKI issuing client certificates (smart cards, MDM-delivered certs, or SCEP/EST). Strongest method and recommended for high-security environments. Downsides: PKI cost, certificate lifecycle management, and revocation checking.

### PEAPv0 / EAP-MSCHAPv2

PEAP wraps an inner EAP method in a TLS tunnel authenticated by the **server certificate only**; the client proves identity via MSCHAPv2 (challenge/response) using a password. Common in Active Directory (NPS/IAS). Risk: if clients do not validate the server certificate, a rogue AP/RADIUS can capture the MSCHAPv2 challenge and crack the password offline. Mitigate with strict server-cert validation and, where possible, migrate to EAP-TLS.

### PEAPv1 / EAP-GTC

Same outer TLS tunnel as PEAPv0 but inner authentication uses EAP-GTC (Generic Token Card), carrying a plaintext token/password inside the tunnel. Useful for OTP/hardware tokens and non-Microsoft password stores. Less common than MSCHAPv2.

### TEAP and EAP-FAST

**EAP-FAST** (Cisco) uses a Protected Access Credential (PAC) instead of certificates for the outer tunnel, avoiding PKI. PAC provisioning (phase 0) must be secured (in-band or out-of-band) — insecure provisioning is a known weakness. **TEAP** (RFC 7170) is the standards-track successor: it supports certificate-based or PAC-based tunnels, inner methods, and cryptographic binding between inner and outer methods. Prefer TEAP over legacy EAP-FAST where supported.

### EAP-TTLS

Similar to PEAP but the inner method can be any legacy authentication (PAP, CHAP, MSCHAP, MSCHAPv2) tunneled inside TLS. Flexible for environments with RADIUS backends that only understand PAP/CHAP. Security depends on inner method strength and server-cert validation.

## Certificate Requirements

For TLS-based EAP, certificate quality determines security:

- **Server certificate**: issued by a CA trusted by clients; EKU must include Server Authentication (1.3.6.1.5.5.7.3.1); subject/SAN must match the RADIUS server name clients are configured to expect; key size ≥ 2048-bit RSA or P-256 ECDSA; SHA-256+ signature; valid lifetime (≤ 1 year preferred).
- **Client certificates (EAP-TLS)**: EKU Client Authentication (1.3.6.1.5.5.7.3.2); unique per device/user; issued via SCEP/EST/MDM; include UPN/SAN for identity mapping.
- **Trust store**: clients must trust only the issuing CA (not the whole system store where avoidable) and pin the expected server name.
- **Revocation**: publish CRL/OCSP; configure RADIUS to check revocation for client certs; keep CRLs reachable.
- **Private key protection**: HSM or TPM-backed keys on the RADIUS server; never exportable client keys where possible.

> Clients that skip server certificate validation are vulnerable to evil-twin credential harvesting regardless of EAP method.

## RADIUS (RFC 2865 / 2866)

**RADIUS** (Remote Authentication Dial-In User Service) is a UDP-based AAA protocol. RFC 2865 defines authentication/authorization; RFC 2866 defines accounting.

- **Ports**: 1812 (auth), 1813 (acct); legacy 1645/1646. Shared secret between authenticator and server protects packet integrity (HMAC-MD5 over packet + secret) and obfuscates passwords (XOR with MD5 of secret + Request Authenticator).
- **Packet types**: `Access-Request`, `Access-Accept`, `Access-Reject`, `Access-Challenge`, plus accounting `Accounting-Request/Response`.
- **Attributes** (Type-Length-Value): carry identity and authorization:
  - `User-Name`, `User-Password`/`CHAP-Password`, `NAS-IP-Address`, `NAS-Port`, `NAS-Identifier`
  - `Service-Type` (Framed/Login), `Framed-Protocol`
  - `Filter-Id`, `Tunnel-Type`, `Tunnel-Medium-Type`, `Tunnel-Private-Group-ID` (VLAN assignment)
  - `Session-Timeout`, `Idle-Timeout`, `Termination-Action`
  - `Calling-Station-Id` (client MAC), `Called-Station-Id` (AP MAC/SSID)
  - Vendor-Specific Attributes (VSA) for vendor policy (ACL names, role)
- **Accounting (RFC 2866)**: `Acct-Status-Type` (Start/Stop/Interim-Update), `Acct-Session-Id`, octet/packet counters, timestamps; enables usage/audit and idle disconnect.

### Dynamic Authorization / CoA (RFC 5176)

Change of Authorization (CoA) and Disconnect Messages let the RADIUS server push policy changes to an already-authorized session without re-authentication:

- **CoA-Request**: change VLAN, ACL, or QoS mid-session (e.g., move a device from quarantine to production after posture remediation).
- **Disconnect-Request**: terminate a session (e.g., on policy violation or license expiry).

Requires the authenticator (NAS) to support RFC 5176 and a shared secret on a separate port (typically 3799, legacy 1700). CoA is essential for posture-based NAC and dynamic VLAN moves.

## Deployment Patterns

Common topologies:

1. **Single RADIUS pair (active/standby)**: simplest; RADIUS servers behind a VIP; authenticators list primary/secondary. Suitable for small/medium sites.
2. **Distributed RADIUS with site affinity**: regional RADIUS servers close to APs to reduce latency; central identity store (AD/LDAP) replicated or queried.
3. **Cloud RADIUS (IDaaS)**: RADIUS-as-a-service for cloud IdPs; good for remote/branch but depends on internet.
4. **Redundant with load balancing**: RADIUS load balancer or authenticator-level failover; ensure CoA routing works.

Authenticators should be configured with at least two RADIUS servers and retry/timeout tuned (e.g., 3 retries, 5s timeout) to avoid lockouts during failover.

## MAB (MAC Authentication Bypass) Fallback

Devices without 802.1X supplicants (printers, phones, legacy IoT) cannot do EAP. **MAB** authenticates by MAC address: the authenticator sends the client MAC as `User-Name`/`Calling-Station-Id` to RADIUS, which checks it against an allowlist. MAB is weak (MACs are spoofable) and should be:

- Restricted to specific ports/SSIDs and device types.
- Combined with device profiling and posture checks.
- Placed in a limited-access VLAN with firewall rules.
- Monitored for spoofing (duplicate MACs, new MACs).

Use MAB only where 802.1X is impossible; prefer 802.1X-capable clients and certificates.

## Guest VLAN / Quarantine

For failed or guest authentication, authenticators can assign:

- **Guest VLAN**: open/limited internet access for visitors; captive portal for terms; isolated from corporate resources.
- **Quarantine/Remediation VLAN**: for devices failing posture checks; allows access only to patch/update servers and remediation portals.
- **Critical data VLAN**: default-deny for unauthorized ports to prevent bypass.

Configure `Termination-Action` and RADIUS attributes to drive VLAN assignment; ensure guest VLANs cannot route to management or production.

## Configuration Examples

### Cisco WLC (AireOS) RADIUS + 802.1X WLAN

```
config radius auth add 1 10.0.0.10 1812 ascii Secret123
config radius auth add 2 10.0.0.11 1812 ascii Secret123
config wlan create 1 corp-ssid corp-ssid
config wlan security 802.1X enable 1
config wlan radius_server auth add 1 1
config wlan radius_server auth add 1 2
config wlan interface 1 management
```

### Windows NPS policy (conceptual)

```
# Connection Request Policy: NAS type = Wireless - IEEE 802.11
# Network Policy: Conditions: EAP type = PEAP; Windows Groups = CORP\WiFi-Users
# Constraints: Auth method = PEAP (EAP-MSCHAPv2); Encryption = AES-128/256
# Settings: Standard RADIUS attributes: Tunnel-Type=VLAN, Tunnel-Medium-Type=IEEE-802,
#           Tunnel-Private-Group-ID=20 (corp VLAN); Session-Timeout=28800
```

### FreeRADIUS users file (EAP-TLS example)

```
# /etc/freeradius/3.0/users
alice  Cleartext-Password := "unused", EAP-Type := "TLS"
       Tunnel-Type = VLAN,
       Tunnel-Medium-Type = IEEE-802,
       Tunnel-Private-Group-Id = "20",
       Session-Timeout = 28800
```

### Supplicant (wpa_supplicant) EAP-TLS

```
# /etc/wpa_supplicant/wpa_supplicant.conf
network={
  ssid="corp-ssid"
  key_mgmt=WPA-EAP
  eap=TLS
  identity="alice@corp.example"
  ca_cert="/etc/certs/ca.pem"
  client_cert="/etc/certs/alice.pem"
  private_key="/etc/certs/alice.key"
  private_key_passwd="..."
}
```

### Supplicant (wpa_supplicant) PEAP

```
network={
  ssid="corp-ssid"
  key_mgmt=WPA-EAP
  eap=PEAP
  identity="alice"
  password="..."
  ca_cert="/etc/certs/ca.pem"
  phase2="auth=MSCHAPV2"
  # require server cert validation:
  # (ensure ca_cert points to the issuing CA and server name is validated by supplicant)
}
```

## Best Practices

- Prefer EAP-TLS with per-device/user certificates; avoid password-based EAP where feasible.
- Enforce server certificate validation on every supplicant; distribute trust anchors via MDM.
- Use redundant RADIUS servers with tuned timeouts; test failover.
- Enable accounting (RFC 2866) for audit and session visibility.
- Use CoA (RFC 5176) for dynamic policy changes and quarantine release.
- Segment guest/quarantine VLANs with default-deny firewall rules.
- Rotate RADIUS shared secrets; use strong secrets; protect RADIUS traffic (RadSec/TLS where supported).
- Monitor authentication failures, duplicate MACs, and unusual EAP method downgrades.
- Keep certificate lifetimes short and automate renewal (SCEP/EST/ACME for RADIUS).

## Gotchas

- PEAP/TTLS security collapses if clients skip server cert validation (evil-twin credential theft).
- MSCHAPv2 challenges can be cracked offline if captured; prefer EAP-TLS.
- MAB MACs are spoofable; treat MAB ports as untrusted.
- CoA requires NAS support and correct shared secret/port (3799); misconfig causes silent failures.

- Guest VLAN must not bridge to management or production networks.
- RADIUS over UDP lacks confidentiality; use RadSec (RADIUS over TLS) or IPsec where required.
- PAC provisioning in EAP-FAST/TEAP must be secured; insecure provisioning undermines the tunnel.
- Certificate expiry on RADIUS servers causes mass authentication failure; monitor expiry.
- Accounting packets can be lost; use interim updates and reconcile.

---

*Reference — Wi-Fi 802.1X, EAP, and RADIUS.*
