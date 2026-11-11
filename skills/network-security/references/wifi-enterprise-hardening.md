---
name: "Wi-Fi Enterprise Hardening"
description: "Enterprise Wi-Fi hardening: WIPS/WIDS, rogue AP detection, spectrum analysis, AP hardening, guest isolation, VLAN-per-SSID, RADIUS redundancy, certificate lifecycle, SIEM integration, and physical security."
tags: [wifi, enterprise, wips, wids, rogue-ap, spectrum-analysis, ap-hardening, guest-network, vlan, radius, certificates, siem, physical-security, 802.1x, eap-tls]
---

# Wi-Fi Enterprise Hardening

Enterprise wireless is a perimeter that moves with every laptop, phone, and sensor. Radio waves cross walls and property lines, so the air interface cannot be bounded by cable. Hardening combines RF monitoring, strong authentication, segmentation, resilient back-end services, and physical controls.

## WIDS and WIPS

A **WIDS** passively monitors the RF environment and reports anomalies; a **WIPS** additionally takes automated action such as blocking a rogue AP or deauthenticating a client. Most vendors ship both in the same controller or cloud plane.

**What to monitor.** Rogue and neighbor APs, evil-twin SSIDs, ad-hoc networks, misconfigured APs, deauth/disassoc floods, EAP failure storms, weak or open SSIDs, and clients associating to unknown APs.

**Sensor placement.** Dedicated sensor APs provide continuous RF visibility; serving APs only scan during off-channel dwell windows, creating blind spots. High-risk zones warrant dedicated sensors with overlapping coverage.

**Detection vs. prevention.** Start detection-only to build a baseline. Enable automated prevention only after tuning, with allow-lists for known neighbors and an exception process. Automated deauth containment can itself be a DoS vector if misconfigured.

**Tuning.** WIDS is noisy from neighbors, hotspots, and IoT. Maintain an authorized-AP inventory keyed on MAC/BSSID, SSID, and location; mark neighbors "known." Review alerts weekly, retire stale signatures, track true-positive rate.

## Rogue AP Detection

Rogue APs fall into categories with different risk profiles:

- **Unauthorized/rogue**: insider/attacker devices on the corporate network (often consumer routers).
- **Misconfigured**: legitimate hardware with wrong SSID, security mode, or VLAN.
- **Evil twin**: clones an enterprise SSID/BSSID to harvest credentials or MITM traffic.
- **Neighbor/external**: off-network APs visible on site; benign but monitored.

**Detection methods.** Combine RF discovery with wired-side correlation: RF scanning finds APs by beacons/probe responses; wired-side checks (switch MAC tables, DHCP/ARP logs, vendor OUIs) confirm whether an AP is attached to the corporate network.

**Response workflow.** (1) Classify the AP. (2) For confirmed rogues on the wired network, identify the switch port via MAC table/LLDP and shut it down or quarantine the VLAN. (3) For evil twins with no wired attachment, rely on RF containment and user education; do not deauth indiscriminately. (4) Document, notify the asset owner, update the authorized-AP inventory, and re-scan to confirm remediation.

**Gotcha:** deauth containment is regulated and can disrupt neighbors. Prefer wired-side port shutdown; use RF containment as a last resort with change approval.

## Spectrum Analysis

Wi-Fi shares 2.4/5/6 GHz with microwaves, Bluetooth, Zigbee, cordless phones, video senders, radar (DFS), and industrial gear. Interference raises the noise floor, lowers SNR, and degrades throughput and roaming.

**Tools.** Dedicated spectrum analyzers (hardware or SDR) visualize energy across frequencies, unlike Wi-Fi scanners. Many enterprise APs include built-in spectrum analysis; use them during site surveys and investigations.

**Channel planning.** In 2.4 GHz, use only channels 1, 6, and 11 at 20 MHz; avoid 40 MHz. In 5/6 GHz, prefer 20 or 40 MHz for density; reserve 80/160 MHz for low-density, high-throughput areas. Enable DFS where radar is present but validate client support. Re-survey after construction or new equipment. Track RSSI (−65 dBm target), SNR (≥25 dB), utilization, retry rates, and roam success; alert on rising noise floor or >50% sustained utilization.

## AP Hardening

Treat each AP as a network device, not a consumer gadget.

- **Firmware**: maintain inventory and patch cadence; subscribe to advisories; stage updates; verify signatures; roll back on failure. Replace EOL APs.
- **Management plane**: disable HTTP, Telnet, SNMPv1/v2c; require HTTPS/SSH with keys; restrict management to a dedicated VLAN/OOB network; change default credentials; protect console/USB ports.
- **Radios**: disable unused bands; enable PMF (802.11w) as *required*; disable WPS; disable legacy data rates (1/2/5.5/11 Mbps); set transmit power to planned values.
- **Authentication**: WPA3-Enterprise (192-bit where required) or WPA2-Enterprise with PMF required; prefer EAP-TLS; validate RADIUS server certs on clients.
- **Physical ports**: disable unused Ethernet ports; enable port security/sticky MAC on uplinks.
- **Time and config**: synchronize clocks via NTP; back up configs to version control; detect drift.


## Guest Network Isolation

Guest access is untrusted by definition and must be isolated from corporate resources.

- Dedicated SSID and VLAN with no route to internal networks; default-deny firewall from guest VLAN to corporate VLANs, allowing only required egress (internet, DNS).
- Captive portal for terms acceptance and registration; rate-limit and time-limit sessions.
- Client isolation (Layer 2) prevents guest-to-guest communication; combine with per-user PSK or 802.1X.
- Bandwidth throttling per client and per SSID to protect corporate capacity.
- DNS and web filtering on guest egress; block SMTP and other abuse-prone protocols.
- Logging: capture guest MAC, IP, session time, and portal identity.
- Privacy: post a notice; minimize retention and collection.

## VLAN per SSID

Mapping each SSID to a VLAN (or VLAN pool) is the foundation of wireless segmentation, but VLANs alone are not segmentation — enforce policy with firewalls/ACLs.

- **Static mapping**: one SSID → one VLAN. Simple and predictable.
- **Dynamic VLAN (RADIUS-assigned)**: RADIUS returns `Tunnel-Private-Group-ID` (plus tunnel type/medium) to place the user in a VLAN based on identity/group. Enables one SSID to land different users in different VLANs.
- **VLAN pooling**: distribute clients across multiple VLANs within a subnet group to reduce broadcast domain size; requires consistent DHCP/DNS/firewall rules across the pool.
- **Inter-VLAN control**: route guest, IoT, and corporate VLANs through a firewall with default-deny.
- **Supporting controls**: DHCP snooping, Dynamic ARP Inspection (DAI), and IP Source Guard on access switches; BPDU Guard and port security on AP uplinks.

## RADIUS Redundancy

Authentication is a single point of failure without redundancy.

- **Primary/secondary**: configure at least two RADIUS servers per SSID; most controllers support ordered lists with failover.
- **Load balancing**: round-robin or least-connections across healthy servers.
- **Failover tuning**: short dead-server detection intervals and retry counts; avoid long timeouts. Test under load.
- **Geographic redundancy**: servers in different sites/failure domains; consider a RADIUS proxy for remote sites.
- **RadSec (RADIUS over TLS, RFC 6614)**: encrypts RADIUS over untrusted networks.
- **Session resumption**: enable TLS session resumption/fast reconnect for EAP-TLS/PEAP.
- **Monitoring**: track auth success/failure rates, latency, and server health; alert on spikes or all-servers-down.
- **Maintenance**: patch and restart servers one at a time; keep configs in version control; test restore.

## Certificate Lifecycle

EAP-TLS and server-certificate validation depend on a well-managed PKI.

- **Hierarchy**: offline root CA plus online issuing CA; protect root in an HSM. Issue server certs for RADIUS and client certs for devices.
- **Validity**: short-lived server certs (e.g., ≤1 year) reduce exposure; automate renewal to avoid expired-cert outages.
- **Issuance/automation**: use SCEP, EST, or ACME with an MDM for client certs; automate server cert renewal. Manual processes fail at scale.
- **Revocation**: publish CRLs and/or OCSP; ensure clients can reach them (or use OCSP stapling). Plan for mass revocation (lost device, CA compromise).
- **Client validation**: clients must validate the RADIUS server certificate (name, chain, expiry, revocation). Disable "allow any cert"; distribute the CA via MDM/GPO.
- **Monitoring**: alert on certificates expiring within 30/14/7 days; maintain an inventory of all certs.
- **Key protection**: store CA private keys in HSMs; rotate compromised keys; document recovery.
- **Gotcha:** clock skew breaks cert validation. Ensure NTP on APs, clients, and RADIUS servers.

## Logging and SIEM Integration

Wireless telemetry is high-value for detection and forensics.

- **Sources**: AP/controller syslog (associations, disassoc, auth events, rogue AP alerts), RADIUS accounting/auth logs, DHCP/DNS logs, firewall logs, WIPS alerts.
- **Collect**: 802.11 association/disassociation with MAC and AP; EAP success/failure with user identity; rogue AP detections; deauth floods; config changes; admin logins.
- **Correlation ideas**: repeated EAP failures → brute force; new MAC on a privileged VLAN → bypass; rogue AP with enterprise SSID → evil twin; mass deauth → DoS; off-hours associations in restricted zones.
- **Normalization**: standardize MAC format, timestamps (UTC), and field names; enrich with asset/identity context.
- **Retention**: align with policy/legal requirements; keep ≥90 days hot, longer cold for investigations.
- **Privacy**: pseudonymize where required; restrict access to identity-linked logs.

## Physical Security

Radio can be attacked physically as well as over the air.

- **AP placement**: mount above reach, in locked enclosures or ceilings; avoid locations where units or cables can be tapped.
- **Tamper resistance**: tamper-evident/resistant enclosures and locks; enable tamper alerts if supported.
- **Cabling**: route in conduit; lock telecom closets; disable unused switch ports; port security on AP uplinks.
- **Antenna placement**: avoid leaking signal outside the building; use directional antennas; conduct RF leakage surveys.
- **Rogue device hunts**: physical walkthroughs with spectrum/Wi-Fi scanners; coordinate with facilities.
- **Site surveys**: validate coverage and interference after any change; document AP locations.

## Best Practices

- Require WPA3-Enterprise (or WPA2-Enterprise + PMF required) and EAP-TLS for corporate SSIDs.
- Enable PMF as required; segment or upgrade legacy clients.
- Prefer wired-side port shutdown over RF deauth containment for confirmed rogues.
- Isolate guest and IoT traffic on dedicated VLANs with default-deny firewall rules.
- Assign VLANs per SSID or dynamically via RADIUS; enforce policy at the firewall.
- Automate certificate issuance and renewal; monitor expiry proactively.
- Harden APs: patch, restrict management plane, disable legacy rates.

## Gotchas

- VLANs are not segmentation; without firewall enforcement, VLAN-per-SSID provides only broadcast isolation.
- WPA3-Transition mode is downgradeable; prefer WPA3-only SSIDs.
- PMF "capable" (optional) allows deauth injection; require it.
- Automated WIPS containment can cause outages and legal issues; tune and get approval first.
- RADIUS failover that is never tested usually fails when needed; test under load.
- Expired RADIUS server certificates cause sudden, widespread auth failures; monitor expiry.
- Clock skew breaks certificate validation; keep NTP consistent.
- Dynamic VLAN requires consistent DHCP/DNS/firewall config across all possible VLANs.

---

*Reference — Wi-Fi Enterprise Hardening.*
