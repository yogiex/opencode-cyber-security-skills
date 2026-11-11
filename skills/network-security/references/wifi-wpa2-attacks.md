---
name: "Wi-Fi WPA2 Attack Techniques"
description: "WPA2 4-way handshake, PMKID clientless attack, KRACK, deauth/disassoc, evil twin/rogue AP, WPS PIN brute force, offline dictionary, weak PSK, detection, hardening, and authorized testing context."
tags: [wifi, wpa2, wpa3, 4-way-handshake, pmkid, krack, deauth, evil-twin, rogue-ap, wps, dictionary, psk, pmf, '802.11', wireless, pentest, hardening, detection]
---

# Wi-Fi WPA2 Attack Techniques

Wi-Fi attacks against WPA2-Personal and WPA2-Enterprise networks target key exchange, management frames, and configuration weaknesses rather than AES-CCMP itself. AES-CCMP remains sound; the failures are in authentication, key derivation, and unauthenticated management frames. This reference covers the 4-way handshake, PMKID, KRACK, deauthentication/disassociation, evil twin/rogue AP, WPS PIN brute force, offline dictionary attacks, weak PSKs, detection, and hardening. All commands are for an **authorized lab only**.

## Authorized Testing Context

Wireless testing is only lawful and ethical with written authorization covering the specific SSIDs, BSSIDs, channels, and physical locations in scope. Unauthorized interception or disruption of Wi-Fi traffic is illegal in most jurisdictions (e.g., CFAA in the US, Computer Misuse Act in the UK). Use an isolated lab: your own AP, test clients, and a monitor-mode adapter; never capture real user handshakes or crack real PSKs. Techniques such as deauthentication and evil twin disrupt or impersonate service, so coordinate timing and avoid production impact. WPS brute force can lock an AP or trigger lockouts; evil twin can harvest credentials. Treat captured hashes and credentials as sensitive data, store them encrypted, and delete them after the engagement. Document scope, rules of engagement, commands run, and findings, and verify remediation by re-testing in the lab.

## 4-Way Handshake

In WPA2-Personal, the Pairwise Master Key (PMK) is derived from the PSK via PBKDF2-HMAC-SHA1 with the SSID as salt and 4096 iterations. The 4-way handshake derives the Pairwise Transient Key (PTK) from the PMK, the AP nonce (ANonce), the client nonce (SNonce), and both MAC addresses via a pseudo-random function. The AP sends ANonce (M1), the client replies with SNonce and a Message Integrity Code (MIC) over M2, the AP sends the Group Temporal Key (GTK) with MIC (M3), and the client acknowledges (M4). The MIC lets an attacker verify a candidate PSK offline: recompute the PMK and PTK for each guess and check the MIC. Capturing all four messages (or just M2) is sufficient to attempt an offline dictionary attack. Monitor mode and channel locking are required to avoid missing frames.

```bash
# Authorized lab only
airmon-ng start wlan0
airodump-ng --bssid AA:BB:CC:DD:EE:FF --channel 6 -w capture wlan0mon
# Trigger a handshake in the lab (disruptive):
aireplay-ng -0 2 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# Crack with aircrack-ng:
aircrack-ng -w wordlist.txt -b AA:BB:CC:DD:EE:FF capture*.cap
# Or convert to hashcat format (hc22000):
hcxpcapngtool -o hash.hc22000 capture*.cap
hashcat -m 22000 hash.hc22000 wordlist.txt
```

## Offline Dictionary and Weak PSK

Because PBKDF2 uses only 4096 iterations, GPU-based cracking is practical, and weak or common PSKs fall quickly. Attackers combine dictionaries (e.g., rockyou), rules (hashcat `-r`), and masks for known patterns such as phone numbers or SSID-derived passwords. Defenses center on entropy: use long, random PSKs (20+ characters, mixed charset), avoid SSID/organization-derived passwords, rotate periodically, and use unique PSKs per site. Better, migrate to WPA3-Personal (SAE) or WPA2-Enterprise with 802.1X/EAP-TLS, which remove offline dictionary feasibility.

## PMKID Attack (Clientless)

Some APs (hostapd-based and many consumer routers) include a PMKID in the first EAPOL frame (M1) when the RSN IE carries it. The PMKID is derived from the PMK, AP MAC, client MAC, and the string "PMK Name", so it can be cracked offline without capturing a client handshake and without sending deauthentication frames. The attacker associates to the AP (or passively observes) and extracts the PMKID. This is a clientless attack that works even when no clients are present.

```bash
# Authorized lab only
hcxdumptool -i wlan0mon -o pmkid.pcapng --enable_status=1
# Target a specific AP:
hcxdumptool -i wlan0mon -o pmkid.pcapng --filterlist_ap=targets.txt --filtermode=2
# Convert and crack:
hcxpcapngtool -o pmkid.hc22000 pmkid.pcapng
hashcat -m 22000 pmkid.hc22000 wordlist.txt
```

Not all APs/firmware include a PMKID, so results vary. Defenses: strong random PSKs, WPA3-SAE (no equivalent PMKID exposure), firmware updates, and disabling WPS where present.

## KRACK (Key Reinstallation)

KRACK (CVE-2017-13077 and related) exploits the 4-way handshake by replaying M3, causing the client to reinstall an already-used key and reset the nonce/counter. Nonce reuse in CCMP/GCMP then allows decryption and injection of frames. It requires a man-in-the-middle position on the channel (often achieved by forcing a channel change and blocking/delaying frames) and affects unpatched WPA2 clients and APs. Patches prevent key reinstallation by tracking replayed messages and refusing to reinstall keys. Defenses: patch clients and APs, prefer WPA3 (with its own updated handshake), and monitor for anomalous EAPOL retransmissions. PMF protects management frames but does not by itself stop KRACK; firmware updates are the fix.

## Deauthentication and Disassociation

In WPA2, deauthentication and disassociation management frames are unauthenticated, so an attacker can spoof them using a known AP or client MAC to disconnect stations. Uses include denial of service, forcing handshake capture, and pushing clients toward an evil twin. Tools include aireplay-ng and mdk4.

```bash
# Authorized lab only
aireplay-ng -0 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
mdk4 wlan0mon d -b targets.txt
```

Defense is Protected Management Frames (PMF, IEEE 802.11w), which authenticates and encrypts robust management frames with CMAC. WPA3 requires PMF; WPA2 should set PMF to required rather than capable to prevent downgrade. Detection focuses on deauthentication floods and sudden mass disconnects.

## Evil Twin and Rogue AP

An evil twin clones a legitimate SSID (and BSSID if feasible) with a stronger signal or weaker security to lure clients, then performs man-in-the-middle, credential harvesting via captive portals, or traffic inspection. Rogue APs are unauthorized APs on the network. Tools include hostapd, airbase-ng, wifiphisher, and fluxion (authorized lab only). Defenses: 802.1X with server certificate validation, WPA3, PMF, WIDS/WIPS, RF monitoring against an authorized AP inventory (MAC, location, SSID), client-side disabling of auto-connect to open networks, and segmentation of guest traffic. Evil twin captive portals are increasingly detected by HSTS and certificate pinning.

## WPS PIN Brute Force

Wi-Fi Protected Setup (WPS) uses an 8-digit PIN with a checksum; the registrar PIN is split into two halves, reducing an online brute force to roughly 11,000 attempts. Tools include reaver and bully.

```bash
# Authorized lab only
reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv
bully -b AA:BB:CC:DD:EE:FF -c 6 wlan0mon
# Pixie Dust (offline PIN recovery via weak RNG in E-S1/E-S2):
reaver -i wlan0mon -b AA:BB:CC:DD:EE:FF -vv -K
```

Some APs lock after failed attempts; Pixie Dust targets weak E-S1/E-S2 generation and can recover the PIN quickly without completing the online brute force. Defenses: disable WPS entirely (best practice), enable lockout, patch firmware, and prefer WPA3 (WPS is not part of WPA3). Detection: repeated WPS association/authentication attempts and lockout log events.

## Detection

- Deploy WIDS/WIPS sensors in monitor mode to detect deauthentication floods, rogue/evil twin APs, WPS brute force, and KRACK-like retransmissions.
- Maintain an authorized AP inventory (SSID, BSSID, channel, location) and alert on unknown or duplicate SSIDs.
- Forward AP and RADIUS logs to a SIEM and correlate client connect/disconnect storms, WPS failures, PMF downgrades, and repeated EAPOL messages.
- Baseline normal client counts and channels; alert on anomalies.
- Use Kismet or airodump-ng for RF surveys and rogue detection.

## Hardening

- Prefer WPA3-Personal (SAE) or WPA2-Enterprise with 802.1X/EAP-TLS.
- If WPA2-Personal is unavoidable: long random PSK (20+ characters), rotate, and use unique PSKs per site.
- Set PMF to required, not capable, to prevent downgrade.
- Disable WPS.
- Patch AP and client firmware promptly (KRACK and WPS fixes).
- Validate RADIUS server certificates on clients; prefer EAP-TLS.
- Segment guest and IoT traffic; restrict lateral movement.
- Reduce RF coverage and secure physical access to APs.
- Avoid WPA3-Transition mode or use separate SSIDs; prefer WPA3-only.
- Monitor with WIDS and SIEM alerting.

## Best Practices

- Obtain written authorization and a defined scope before any wireless testing.
- Use isolated lab hardware; never capture or crack production handshakes.
- Lock the channel with `airodump-ng --channel` to avoid missing frames.
- Restore interfaces after testing (`airmon-ng stop`, manage mode).
- Secure and delete captured hashes and credentials after the engagement.
- Verify remediation by re-testing in the lab.
- Educate users on strong PSKs and captive-portal phishing from evil twins.

## Gotchas

- Monitor mode and injection require compatible adapters (chipset/driver); not all support both.
- Handshake capture needs all four messages; PMF blocks deauth-based capture.
- PMKID is present only on some APs/firmware; absence is not proof of safety.
- Hashcat modes differ (22000 vs legacy 16800); conversion tools and formats change.
- WPS lockout can disrupt service; coordinate with the owner.
- Evil twins are defeated by HSTS and certificate pinning in modern clients.
- KRACK requires patching both client and AP; mixed environments remain exposed.
- Unauthorized wireless testing is illegal; always get written authorization.
- GPU cracking speed depends on PSK length and charset; long random PSKs are not feasible to crack.

---

*Reference — Wi-Fi WPA2 Attack Techniques.*
