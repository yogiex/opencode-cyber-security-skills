---
name: "Wi-Fi 6 and Wi-Fi 7 Security (802.11ax / 802.11be)"
description: "Security-relevant features of Wi-Fi 6 (802.11ax) and Wi-Fi 7 (802.11be): mandatory WPA3, Enhanced Open (OWE), BSS coloring, OFDMA, MLO security, SAE in 6 GHz, 6 GHz band rules, transition modes, best practices, and gotchas."
tags: [wifi6, wifi7, 802.11ax, 802.11be, wpa3, owe, enhanced-open, bss-coloring, ofdma, mlo, multi-link, sae, 6ghz, pmf, transition]
---

# Wi-Fi 6 and Wi-Fi 7 Security (802.11ax / 802.11be)

Wi-Fi 6 (IEEE 802.11ax) and Wi-Fi 7 (IEEE 802.11be) are not just throughput upgrades. They change the security baseline: WPA3 becomes mandatory in the 6 GHz band and for Wi-Fi 7 certification, open networks gain optional encryption through Enhanced Open (OWE), and new PHY/MAC features (OFDMA, BSS coloring, Multi-Link Operation) introduce new operational and denial-of-service considerations. This reference focuses on the security-relevant behavior, not the PHY details.

## Standards and Certification Baseline

| Item | Wi-Fi 6 (802.11ax) | Wi-Fi 6E (6 GHz) | Wi-Fi 7 (802.11be) |
|------|---------------------|------------------|---------------------|
| Bands | 2.4 / 5 GHz | + 6 GHz | 2.4 / 5 / 6 GHz |
| Minimum security | WPA2 (legacy) | WPA3 only | WPA3 only (certified devices) |
| Open-network encryption | Optional OWE | OWE (recommended) | OWE (recommended) |
| PMF | Required with WPA3 | Required | Required |
| Legacy 802.11b/g | Allowed | Not in 6 GHz | Not in 6 GHz (for 6 GHz radios) |

> Wi-Fi 6 on 2.4/5 GHz still permits WPA2 for backward compatibility. The 6 GHz band has no legacy devices and no WPA2: this is the main security win of Wi-Fi 6E/7.

## WPA3 Mandatory

The Wi-Fi Alliance mandates WPA3 for any device operating in 6 GHz and for Wi-Fi 7 certification. Consequences for operators:

- **WPA3-Personal (SAE)** replaces the PSK four-way handshake. Keys are derived via Dragonfly (SAE), giving forward secrecy and resistance to offline dictionary attacks even with weak passwords. PMF is mandatory.
- **WPA3-Enterprise** mandates the 192-bit security suite (CNSA) for the highest tier and requires PMF. Use EAP-TLS for the authenticator; PEAP/MSCHAPv2 should be retired.
- **SAE anti-clogging**: SAE includes a token-based anti-clogging defense against resource-exhaustion floods against the AP. Tune thresholds; monitor for SAE floods as a DoS indicator.
- **SAE-PK (Public Key)**: an optional WPA3-Personal extension where the AP advertises a public key in beacons/Probe Responses. Clients verify it, mitigating evil-twin impersonation without deploying 802.1X. Recommended for high-risk or unmanaged environments.

## Enhanced Open (OWE)

Opportunistic Wireless Encryption (RFC 8110, adopted into 802.11) encrypts traffic on "open" networks without any credentials:

- Each client performs an unauthenticated Diffie-Hellman exchange with the AP during association; the resulting PMK encrypts the session (AES-CCMP/GCMP).
- Provides **confidentiality against passive eavesdroppers** and protects user data on public Wi-Fi, but **no authentication**: an active MITM or evil twin can still intercept and decrypt by terminating the OWE exchange.
- **OWE Transition Mode** broadcasts both an open SSID and an OWE SSID with matching names; clients that support OWE use the encrypted one. Like WPA3-Transition, this is downgradeable and should be treated as a migration aid, not a steady state.
- Use OWE for guest/public SSIDs where 802.1X is impractical; never treat OWE as equivalent to WPA3-Enterprise for sensitive data.

## BSS Coloring

BSS coloring is a spatial-reuse mechanism in HE (High Efficiency) and EHT (Extremely High Throughput) PHYs:

- Each BSS advertises a 6-bit "color" in the HE/EHT preamble. Stations use it to distinguish intra-BSS from inter-BSS (OBSS) frames and may transmit during OBSS traffic when signal is weak (spatial reuse), improving throughput.
- **Security implications are indirect**: color is unauthenticated metadata. A malicious or misconfigured device can advertise a colliding or spoofed color, causing excessive deferral (throughput collapse) or, conversely, aggressive transmission that raises interference. Treat as an availability/DoS surface, not a confidentiality one.
- Validate color assignments during site surveys; avoid duplicate colors on overlapping cells. Monitor for sudden throughput degradation that may indicate color collisions or spoofing.

## OFDMA

Orthogonal Frequency Division Multiple Access lets an AP schedule multiple stations on sub-channels (Resource Units) in a single TXOP:

- Improves efficiency in dense environments but makes the AP the scheduling authority. A compromised or rogue station cannot directly inject RUs, but can flood trigger frames or association requests to exhaust scheduling and airtime.
- Uplink MU (multi-user) requires the AP to poll stations; ensure trigger-based uplink is rate-limited and that management-frame protection (PMF) is on to prevent spoofed triggers.
- OFDMA does not change the cryptographic model; its risks are availability and fairness. Include OFDMA-heavy cells in RF/availability monitoring.

## Multi-Link Operation (MLO) Security (Wi-Fi 7)

MLO is the headline Wi-Fi 7 feature: a single Multi-Link Device (MLD) can establish and use multiple links (e.g., 5 GHz + 6 GHz) simultaneously, aggregating throughput and improving reliability.

Security implications:

- **Single association, multiple links**: one MLD setup authenticates the device once; per-link traffic keys are derived for each active link. A failure to bind keys to the correct link/MLD address can allow cross-link key reuse or traffic injection.
- **Link steering and downgrade**: an attacker or buggy firmware may steer traffic to a weaker link (e.g., a 2.4 GHz link with WPA2 policy) or disable a link, degrading security/availability. Enforce WPA3 on every link an MLD may use; do not allow mixed security policies across links of one SSID.
- **Setup-frame protection**: MLO setup and reconfiguration frames must be protected (PMF + WPA3). Unprotected setup is a hijack/DoS vector.
- **Traffic splitting exposure**: data may traverse different bands with different RF exposure. For sensitive traffic, prefer a single high-security link or enforce encryption at higher layers (TLS/VPN) rather than relying on link choice.
- **Rogue MLD / link injection**: validate MLD MAC addresses and link parameters; monitor for unexpected link additions.
- **Availability**: MLO increases state per client; APs must handle MLD state tables. Capacity-plan and monitor for MLD-exhaustion conditions.

## SAE in the 6 GHz Band

Because 6 GHz forbids WPA2 and legacy 802.11, SAE is the only Personal-mode option:

- No PSK capture/handshake to crack offline; forward secrecy protects past sessions if a password later leaks.
- Pair SAE with a strong, unique passphrase and, where possible, SAE-PK to authenticate the AP.
- Enterprise deployments in 6 GHz should use WPA3-Enterprise with EAP-TLS; do not fall back to PEAP for "compatibility" since 6 GHz clients are all WPA3-capable by definition.

## 6 GHz Band Rules

Regulatory constraints shape the attack surface:

- **Indoor LPI (Low Power Indoor)**: in most regions 6 GHz Wi-Fi is restricted to indoor, low-power operation. This materially reduces external RF reachability and casual eavesdropping from outside the building.
- **Standard Power + AFC**: outdoor/standard-power 6 GHz requires Automated Frequency Coordination (AFC) to avoid incumbent fixed-satellite/microwave links. AFC databases and the AP's location accuracy become security-relevant; spoofed location could cause interference or service denial.
- **No legacy coexistence**: 6 GHz has no 802.11a/b/g/n/ac devices, so there is no "lowest common denominator" forcing WEP/WPA/WPA2 or legacy data rates. This removes a whole class of downgrade and legacy-attack paths.
- **Client-to-client / peer-to-peer** restrictions may apply in some regions; verify local rules before enabling such features.

## Transition Modes and Downgrade Risks

- **WPA3-Transition (mixed mode)** advertises both WPA2 and WPA3. It is vulnerable to the transition-disable attack, where an adversary forces WPA2 association. Prefer **WPA3-only SSIDs**; keep a separate, explicitly labeled legacy SSID if migration requires it, with a retirement date.
- **OWE Transition Mode** has the same downgrade property; treat as temporary.
- **SAE vs SAE-PK**: without SAE-PK, an evil twin can still lure clients with the same SSID/passphrase; SAE alone does not authenticate the AP.
- **PMF "capable" vs "required"**: WPA3 requires PMF required. Ensure configuration is "required," not "capable," to prevent stripping.

## Security Comparison: Legacy vs Wi-Fi 6/7

| Control | WPA2 (legacy) | WPA3 (6/7) |
|---------|---------------|------------|
| Key exchange | PSK/PBKDF2 | SAE (Dragonfly) |
| Forward secrecy | No | Yes |
| Offline dict. resistance | No | Yes |
| PMF | Optional | Required |
| Open-network encryption | None | OWE (optional) |
| AP authentication | None (PSK shared) | SAE-PK (optional) |
| 6 GHz support | No | Yes |

## Best Practices

- Deploy **WPA3-only SSIDs** in 6 GHz; retire WPA2/transition modes on a documented schedule.
- Use **EAP-TLS** for WPA3-Enterprise; remove PEAP/MSCHAPv2 and validate server certificates on clients.
- Enable **PMF required** everywhere; segment or replace clients lacking support.
- Use **OWE** for guest/public SSIDs; keep it separate from corporate SSIDs and treat it as unauthenticated encryption.
- Adopt **SAE-PK** where evil-twin risk is high and 802.1X is unavailable.
- Enforce **consistent WPA3 policy across all links** in MLO deployments; monitor link steering and MLD state.
- Validate **BSS color** assignments and monitor for collisions/spoofing in dense cells.
- Rate-limit trigger frames and protect management frames (PMF) for OFDMA cells.
- Verify **AFC location accuracy** and database freshness for standard-power 6 GHz.
- Keep firmware current; Wi-Fi 6/7 features (MLO, AFC) are software-heavy and patch-dependent.
- Baseline RF/availability metrics per band to detect OFDMA/BSS-coloring abuse and MLO link issues.

## Gotchas

- WPA3-Transition and OWE-Transition are downgradeable; "capable" PMF allows stripping.
- SAE alone does not authenticate the AP; evil twins remain possible without SAE-PK or 802.1X.
- OWE encrypts but does not authenticate; MITM can still terminate the exchange.
- BSS coloring and OFDMA are availability surfaces, not crypto controls; misconfiguration causes outages, not breaches.
- MLO mixes links with potentially different policies; inconsistent config silently weakens security.
- 6 GHz indoor-only rules vary by region; verify before planning outdoor coverage.
- AFC depends on accurate location data; treat it as a trust boundary.
- Legacy clients cannot join 6 GHz at all; plan SSID/band strategy for mixed fleets.
- Firmware bugs in new features (MLO, AFC) are common early in a standard's lifecycle; stage rollouts.

---

*Reference — Wi-Fi 6 and Wi-Fi 7 Security (802.11ax / 802.11be).*
