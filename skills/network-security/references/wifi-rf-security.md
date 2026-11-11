---
name: "Wi-Fi RF Security"
description: "RF planning and Wi-Fi security: site surveys, coverage vs capacity, interference, AP physical security, antennas, rogue detection, guest isolation, jamming, best practices, gotchas."
tags: [wifi, rf, site-survey, coverage, capacity, interference, antenna, rogue-ap, wids, wips, guest-network, isolation, jamming, physical-security, "802.11", pmf]
---

# Wi-Fi RF Security

Wi-Fi security starts in the physical layer: how radio frequency (RF) energy is planned, placed, and protected determines whether the network is usable, performant, and defensible. Logical controls (WPA3, 802.1X) cannot compensate for poor RF design, exposed access points (APs), or unmonitored spectrum. This reference covers RF planning, interference, hardware security, rogue detection, guest isolation, and jamming.

## Site Survey Methodology

A site survey translates business requirements into an AP placement and channel plan. Four survey types are commonly used:

- **Predictive survey**: software models RF propagation from floor plans and material attenuation. Fast and cheap, but accuracy depends on material data and cannot capture real-world interferers. Use for initial design.
- **Passive survey**: the survey tool listens without associating, recording RSSI, noise floor, channel utilization, and neighboring APs. Reveals real interference and coverage holes.
- **Active survey**: the tool associates to a test AP and measures throughput, latency, and roaming behavior. Validates user experience.
- **Post-deployment validation**: repeat passive/active surveys after installation to confirm design intent and tune power/channel settings.

Methodology steps: define requirements (coverage targets, capacity per area, roaming, client types, SLAs); gather floor plans, materials, mounting constraints, PoE, and upstream bandwidth; identify RF obstacles (metal, concrete, glass, elevators, human bodies); select calibrated tools (Ekahau, Hamina, AirMagnet, NetSpot); walk the space at client height sampling multiple points including transient areas; analyze RSSI/SNR/channel-overlap/data-rate/capacity heatmaps; adjust placement, antennas, power, or AP count and re-survey; document AP locations, antennas, channels, power, and baselines.

Key considerations: design for the weakest supported client; verify roaming thresholds (-65 to -70 dBm with 10-15 dBm cell overlap); plan DFS fallbacks; survey in representative (occupied) conditions.

## Coverage vs Capacity

**Coverage** ensures a client can hear and be heard by an AP at sufficient signal strength and SNR. **Capacity** ensures enough throughput and airtime for the number of clients and applications in an area. They are not the same: full-bar coverage can still fail under load.

- **Coverage-first design** risks overpowered APs, sticky clients, and co-channel interference in dense areas.
- **Capacity-first design** sizes cells for expected client counts and application demands, then verifies coverage across the whole space.

Practical metrics:

| Metric | Typical Target |
|--------|----------------|
| RSSI at cell edge | -67 dBm (voice/video), -70 dBm (data) |
| SNR | ≥ 25 dB (voice), ≥ 20 dB (data) |
| Clients per AP | 20-30 for data; fewer for real-time apps |
| Airtime utilization | < 50-60% sustained |
| Channel utilization | < 40-50% preferred |
| Cell overlap | 10-15 dBm for seamless roaming |

Capacity planning must include upstream (WAN/ISP) bandwidth, PoE budgets, switch backhaul, and AP radio capabilities (spatial streams, channel width). Use band steering to push capable clients to 5/6 GHz, reserving 2.4 GHz for IoT and legacy devices. Avoid "more APs = better": excessive density increases roaming events, co-channel interference, and management overhead.

## Interference Sources

Interference degrades throughput, increases latency, and can cause disconnections.

**Wi-Fi interference:**

- **Co-channel interference (CCI)**: multiple APs on the same channel within range. They share airtime, reducing throughput for all. Mitigate with proper channel planning and power control.
- **Adjacent channel interference (ACI)**: partially overlapping channels (notably 2.4 GHz with 20 MHz channels). Worse than CCI; use only non-overlapping channels (1, 6, 11 in 2.4 GHz).

**Non-Wi-Fi interferers:** microwaves, Bluetooth, Zigbee, cordless phones (2.4 GHz); radar (DFS vacating on 5 GHz); wireless cameras/audio; LED drivers, USB 3.0, motors, industrial equipment.

**Mitigation:** prefer 5/6 GHz (6 GHz less congested, shorter range); spectrum analysis (MetaGeek, Ekahau Sidekick); adjust channel width (20/40/80/160 MHz); reduce transmit power; relocate APs or shield sources; automatic channel selection with DFS constraints.

## Physical Security of APs

APs are often mounted in accessible ceilings and corridors, making them targets for theft, tampering, and rogue installation.

- **Mounting**: lockable enclosures, tamper-evident mounts, secured tiles; conceal/protect cabling (plenum-rated where required).
- **Port security**: disable unused console/USB ports; secure management; signed firmware and secure boot.
- **Outdoor/remote**: weatherproof, surge-protected, locked enclosures; monitor link status (PoE cuts are a DoS vector).
- **Asset management**: record serials, MACs, locations; tag and reconcile periodically.
- **RF impact**: avoid metal/dense enclosures—attenuation degrades coverage and tempts power increases that worsen interference.
- **Insider threat**: physical access enables firmware extraction, credential theft, rogue APs; include APs in security rounds.

## Antenna Selection

Antenna choice shapes coverage pattern, gain, and interference footprint.

| Type | Pattern | Use Case |
|------|---------|----------|
| Omni (dipole/ceiling) | 360° horizontal | Open offices, general coverage |
| Directional (patch/panel) | Focused beam | Corridors, warehouses, point-to-point |
| Semi-directional | Moderate focus | Aisles, long rooms |
| Yagi/parabolic | Narrow, high gain | Outdoor bridges, long links |

Selection factors: environment, mounting height, obstacles, cell size, interference. Higher gain extends range but increases interference and may exceed EIRP limits (FCC/ETSI)—reduce power accordingly. Use dual-polarized antennas for MIMO; match connectors (RP-SMA, N-type); document models; keep orientation consistent (misalignment creates dead zones).

## Rogue Device Detection

A rogue AP is an unauthorized device broadcasting an SSID or connected to the wired network, often used for evil-twin attacks or unauthorized access.

**Detection methods:**

- **WIDS/WIPS**: dedicated sensors or APs in monitor mode detect unknown BSSIDs, SSID spoofing, and attack signatures.
- **Wired-side correlation**: match discovered wireless MACs against switch ports, ARP tables, and DHCP logs to find rogue devices on the corporate network.
- **Network scans**: periodic scanning for unknown APs and unexpected DHCP servers.
- **Physical inspection**: walk-throughs with handheld analyzers.

**Response:**

- Classify devices as rogue (on wired network), neighbor (external), or authorized.
- Automated containment: deauth rogue clients, disable switch ports, or quarantine via NAC/802.1X.
- Maintain an authorized AP inventory (MAC, SSID, channel, location) to reduce false positives from neighbor networks and personal hotspots.
- Integrate alerts with SIEM for correlation and audit.

**Caveats:** containment can affect legitimate neighboring devices; define policy and authorization before automating. Evil-twin detection relies on BSSID/SSID/channel mismatches and signal anomalies.

## Guest/Visitor Isolation

Guest networks must provide internet access without exposing internal resources.

- **Segmentation**: dedicated SSID and VLAN; firewall rules allow only internet egress, blocking RFC1918, management networks, printers, and internal services.
- **Captive portal**: terms of service, bandwidth and time limits, and authentication via vouchers, SMS, or email.
- **Client isolation**: AP isolation prevents guest-to-guest communication.
- **DNS/DHCP**: use separate scopes and public resolvers; avoid leaking internal DNS.
- **QoS/rate limiting**: protect corporate bandwidth and prevent abuse.
- **Session expiry**: time-limited access with re-authentication.
- **Security mode**: WPA2/WPA3-Personal with rotated PSKs, or WPA3-Enterprise with guest certificates.
- **Monitoring**: log connections for compliance and abuse investigations; consider a dedicated internet circuit for high-risk environments.
- **Privacy**: inspect traffic only per policy and legal requirements.

## RF Jamming Considerations

Jamming is intentional RF interference aimed at denying wireless service. Types include constant, deceptive, reactive, and barrage jamming. Effects range from reduced throughput to complete DoS.

**Detection:**

- Spectrum analysis showing raised noise floor or unusual signals.
- Sudden channel utilization spikes and client disconnect storms.
- WIDS alerts for jamming signatures.

**Mitigation and resilience:**

- Frequency diversity: support multiple bands (2.4/5/6 GHz) and dynamic channel selection.
- Redundancy: wired fallback and cellular backup for critical systems.
- Directional antennas to reduce spill and susceptibility.
- Physical security to prevent placement of jamming devices.
- 6 GHz is less commonly targeted by off-the-shelf jammers, but not immune.

**Notes:** jamming is illegal in many jurisdictions; defensive efforts should focus on detection, documentation, and resilience. Reactive jamming may follow channel changes, so static plans are insufficient. Critical systems should not depend solely on Wi-Fi.

## Best Practices

- Perform predictive and on-site surveys before deployment; validate afterward.
- Design for capacity in dense areas; verify coverage everywhere.
- Prefer 5/6 GHz; reserve 2.4 GHz for IoT and legacy clients.
- Enable PMF as required; use WPA3 or WPA2 with 802.1X.
- Plan channels to avoid overlap; use 20 MHz in 2.4 GHz and appropriate widths in 5/6 GHz.
- Keep transmit power moderate to control cell size and interference.
- Secure APs physically: lockable mounts, tamper detection, asset inventory.
- Deploy WIDS/WIPS with documented rogue-containment policy.
- Isolate guest traffic with firewalls, captive portals, and client isolation.
- Monitor spectrum and channel utilization; alert on anomalies.
- Document AP, antenna, channel, and power settings.
- Plan for jamming: multi-band support, redundancy, wired fallback.
- Audit authorized AP inventory regularly; remove stale entries.
- Patch AP firmware and secure the management plane.

## Gotchas

- Overpowered APs cause sticky clients and co-channel interference.
- 2.4 GHz has only three non-overlapping channels; dense deployments suffer.
- DFS channels can force client disconnects when radar is detected.
- PMF "capable" allows downgrade; require it explicitly.
- Guest SSIDs on shared APs consume airtime and reduce capacity.
- Misaligned directional antennas create dead zones.
- Rogue containment can disrupt legitimate neighboring networks.
- Spectrum analysis has false positives; calibrate tools and thresholds.
- Physical access to an AP often bypasses logical controls.
- Jamming is hard to distinguish from accidental interference.
- Legacy client limitations constrain channel width and band choices.
- PoE budgets and switch backhaul are frequently overlooked.

---

*Reference — Wi-Fi RF Security.*
