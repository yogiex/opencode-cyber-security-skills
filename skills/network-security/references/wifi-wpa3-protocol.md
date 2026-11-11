---
name: "Wi-Fi WPA3 Protocol"
description: "WPA3-Personal (SAE/Dragonfly), WPA3-Enterprise (192-bit CNSA), EAP-TLS, transition/downgrade risks, OWE, mandatory PMF, SAE-PK, comparison, implementation notes, best practices, and gotchas."
tags: [wifi, wpa3, wpa2, sae, dragonfly, pmf, owe, enhanced-open, eap-tls, cnsa, 192-bit, transition-mode, downgrade, sae-pk, psk, 802.11, 802.1x, radius, forward-secrecy, offline-dictionary]
---

# Wi-Fi WPA3 Protocol

WPA3 (IEEE 802.11-2020 / Wi-Fi Alliance WPA3) replaces the PSK-based key derivation of WPA2 with modern, authenticated key exchange. It hardens both Personal and Enterprise modes, makes Protected Management Frames (PMF) mandatory, and adds Opportunistic Wireless Encryption (OWE) for open networks. This reference details the protocol mechanics, deployment pitfalls, and operational best practices.

## Overview

WPA3 has two primary modes plus two add-ons:

| Mode / Feature | Purpose | Key Change vs WPA2 |
|----------------|---------|--------------------|
| WPA3-Personal | Home/SOHO pre-shared credential | SAE replaces PSK 4-way handshake |
| WPA3-Enterprise | Organization 802.1X authentication | Optional 192-bit CNSA suite; PMF required |
| WPA3-Transition | Mixed WPA2/WPA3 clients | Backward compat; downgrade-exposed |
| OWE (Enhanced Open) | Encrypt open (no-password) networks | Unauthenticated DH key exchange |
| SAE-PK | Public-key auth for WPA3-Personal | Binds SSID to a key pair; anti-evil-twin |
| PMF (802.11w) | Protect management frames | Mandatory in WPA3 |

## WPA3-Personal: SAE (Simultaneous Authentication of Equals)

SAE replaces the WPA2 PSK 4-way handshake with a Password Authenticated Key Exchange (PAKE) based on the **Dragonfly** key exchange (RFC 7664). Both parties derive a shared secret from a low-entropy password without transmitting it, and the result is a high-entropy Pairwise Master Key (PMK).

### Dragonfly Key Exchange

Dragonfly operates in two phases:

1. **Commit phase** — each side generates an ephemeral scalar and an element (point on an elliptic curve or a finite-field element), derived deterministically from the password and a random token. Both sides exchange these commitments.
2. **Confirm phase** — each side proves knowledge of the password and the derived secret; on success both derive the same PMK.

Because the exchange is authenticated by the password, an attacker cannot complete it without the password, and the resulting PMK is different for every session.

### Anti-Clogging

SAE includes an **anti-clogging** mechanism to resist denial-of-service: when a station sends many commit frames, the AP can require a token (a cookie) before processing further commits. This mirrors the SYN-cookie idea and prevents resource exhaustion from spoofed commit floods.

### Forward Secrecy

WPA2-Personal derives the PMK solely from the PSK and SSID, so a captured handshake plus a cracked PSK exposes all past sessions. SAE generates a fresh PMK per association using ephemeral secrets, providing **forward secrecy**: compromising the password later does not reveal previously recorded traffic.

### Offline Dictionary Resistance

WPA2 handshakes can be captured and cracked offline with tools like hashcat; weak PSKs fall quickly. In SAE, the PMK is not a simple function of the password — it requires an interactive exchange. An attacker who captures a handshake cannot test password guesses offline; each guess requires a live interaction with the AP (or an online oracle), making large-scale dictionary attacks impractical. SAE also limits the rate of failed attempts per peer.

### SAE Groups

SAE supports multiple cryptographic groups:

| Group | Type | Status |
|-------|------|--------|
| 19 | ECC (P-256) | Mandatory for WPA3-Personal |
| 20 | ECC (P-384) | Optional |
| 21 | ECC (P-521) | Optional |
| 1 | Finite field (2048-bit) | Optional/legacy |
| 2 | Finite field (3072-bit) | Optional |

Group 19 (P-256) is the baseline; ECC groups are preferred over finite-field groups for performance and security.

## WPA3-Enterprise

WPA3-Enterprise retains 802.1X/EAP authentication but raises the floor:

- **PMF required** for all associations.
- **192-bit mode** (optional but recommended for high-security): uses the CNSA (Commercial National Security Algorithm) suite.
- **EAP method** must be an approved, strong method (EAP-TLS preferred).

### 192-bit Mode and CNSA Suite

The CNSA suite mandates:

| Primitive | Algorithm | Minimum |
|-----------|-----------|---------|
| Key exchange | ECDH (P-384) | 192-bit security |
| Digital signature | ECDSA (P-384) or RSA (3072-bit) | 192-bit security |
| Symmetric encryption | AES-256-GCM / AES-256-CCM | 256-bit |
| Hash | SHA-384 | 384-bit |

In 192-bit mode, WPA3-Enterprise uses GCMP-256 (Galois/Counter Mode Protocol with 256-bit keys) instead of CCMP-128, and the 4-way handshake derives 256-bit PTK/GTK. This aligns Wi-Fi with NSA/CNSA requirements for protecting classified and high-value data.

## WPA3-Enterprise with EAP-TLS

EAP-TLS (RFC 5216) provides certificate-based mutual authentication: the client proves identity with a client certificate, and the server proves identity with a server certificate. Combined with WPA3-Enterprise:

- **Server certificate validation** is mandatory on the supplicant; pin or validate against a trusted CA.
- **Client certificates** enable per-device/per-user identity and per-session keys.
- **TLS 1.2+** (preferably 1.3) is used inside EAP.
- **No password** is transmitted or stored, eliminating credential-phishing and brute-force risks.

Operational requirements: a functioning PKI (issuance, renewal, revocation via OCSP/CRL), certificate lifecycle automation, and handling of expired/revoked certs on roaming clients. EAP-TLS is the strongest WPA3-Enterprise option but demands the most infrastructure.

## Transition Mode and Downgrade Risks

**WPA3-Transition mode** (also called WPA3/WPA2 mixed mode) advertises a single SSID that accepts both WPA2 and WPA3 clients. It exists for backward compatibility but introduces serious risks:

- **Transition-disable attack**: an active MITM can block SAE commit frames, forcing the client to fall back to WPA2. The client may not warn the user.
- **Downgrade to WPA2**: a WPA3-capable client associating in transition mode can be coerced into WPA2-PSK, losing forward secrecy and offline-dictionary resistance.
- **Mixed security posture**: the same SSID now has two different key-derivation strengths; auditing and policy enforcement become ambiguous.

Mitigations: prefer **WPA3-only SSIDs**; if transition is unavoidable, enable **Transition Disable** indication (the AP signals that WPA3 is available so clients refuse WPA2 on that SSID), monitor for downgrade events, and segment legacy clients onto a separate, restricted SSID/VLAN.

## OWE (Opportunistic Wireless Encryption / Enhanced Open)

OWE (RFC 8110) encrypts traffic on open (no-password) networks using an unauthenticated Diffie-Hellman key exchange during association:

- No credentials required; any client can connect.
- Provides **confidentiality and integrity** against passive eavesdroppers (but not against active MITM, since there is no authentication).
- PMF is used to protect the exchange.
- Branded as **Enhanced Open** by the Wi-Fi Alliance.

OWE is ideal for guest/public Wi-Fi where passwords are impractical but sniffing must be prevented. It does not authenticate users or devices; pair with a captive portal or 802.1X for identity.

## PMF Mandatory

Protected Management Frames (802.11w) authenticate robust management frames (deauthentication, disassociation, action frames) using CMAC, preventing spoofed deauth/disassoc injection. In WPA2, PMF is optional and frequently disabled; in WPA3 it is **mandatory**. Without PMF, deauthentication attacks and evil-twin forced reconnects remain trivial. Ensure all clients and APs support PMF before enforcing WPA3-only.

## SAE-PK (Public Key Authentication)

SAE-PK extends WPA3-Personal by binding the SSID to a public/private key pair. The AP proves possession of the private key during SAE, so clients can verify they are connecting to the legitimate network even if an attacker knows the password. This mitigates evil-twin attacks on WPA3-Personal deployments (e.g., home/SOHO where a password alone is shared). Keys are provisioned out-of-band (QR code, app, or config) and the client stores the expected public key.

## Comparison Table: WPA2 vs WPA3

| Aspect | WPA2-Personal | WPA3-Personal | WPA2-Enterprise | WPA3-Enterprise |
|--------|---------------|---------------|-----------------|-----------------|
| Key exchange | PSK (PBKDF2) | SAE (Dragonfly) | 802.1X/EAP | 802.1X/EAP |
| Forward secrecy | No | Yes | Depends on EAP | Depends on EAP |
| Offline dict. resistance | No (crackable) | Yes | N/A (passwords in EAP) | N/A |
| PMF | Optional | Mandatory | Optional | Mandatory |
| Encryption | CCMP-128 (AES) | CCMP-128/GCMP-256 | CCMP-128/GCMP-256 | CCMP-128/GCMP-256 (192-bit: GCMP-256) |
| Security level | 128-bit | 128-bit (Group 19) | 128-bit+ | 128-bit or 192-bit (CNSA) |
| Anti-evil-twin | No | SAE-PK (optional) | EAP server cert | EAP server cert |
| Open networks | Unencrypted | OWE available | N/A | N/A |

## Implementation Notes

- **Firmware/OS support**: WPA3 requires recent AP firmware and client OS (Windows 10 1903+, macOS 10.15+, iOS 13+, Android 10+, Linux wpa_supplicant 2.7+). Inventory before rollout.
- **Group negotiation**: ensure SAE group 19 is enabled; some clients default to group 2 (finite field) which is slower. Pin group policy on APs.
- **PMF interop**: legacy clients without 802.11w cannot connect when PMF is required. Use a separate legacy SSID or upgrade.
- **RADIUS/EAP**: for Enterprise, verify EAP methods, TLS versions, and certificate chains; test roaming (802.11r FT) with WPA3.
- **OWE**: requires client and AP support; many older clients fall back to open (unencrypted) — verify.
- **SAE-PK**: provision keys via trusted channel; loss of private key requires re-provisioning all clients.

## Best Practices

- Prefer **WPA3-only SSIDs** over transition mode; segment legacy clients separately.
- Use **EAP-TLS** for Enterprise; avoid PEAP/MSCHAPv2 where possible.
- Enable **PMF required** everywhere; upgrade or isolate legacy clients.
- Deploy **OWE** for guest/open networks instead of truly open SSIDs.
- Use **SAE-PK** for shared-password Personal deployments to resist evil twins.
- Enable **Transition Disable** indications and monitor downgrade attempts.
- Enforce 192-bit/CNSA mode only where required (classified/high-value data) due to client compatibility cost.
- Automate certificate lifecycle for EAP-TLS; monitor expiry and revocation.

## Gotchas

- **Dragonblood vulnerabilities**: early WPA3 implementations had side-channel and downgrade flaws; patch firmware/OS.
- **Transition mode is downgradeable** even with WPA3-capable clients present.
- **PMF "capable" ≠ "required"**: capable allows non-PMF clients and deauth injection.
- **SAE group mismatch** causes association failures or forced fallback to slower groups.
- **EAP-TLS PKI burden**: expired/revoked certs lock users out; plan renewal and revocation distribution.
- **OWE does not authenticate**: active attackers can still MITM; use for passive-eavesdropping protection only.
- **192-bit mode compatibility**: many clients lack GCMP-256/CNSA support; test before enforcing.

---

*Reference — Wi-Fi WPA3 Protocol.*
