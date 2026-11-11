---
name: "Network Hardening Baselines"
description: "Device and network hardening baselines: CIS Controls v8 network safeguards, CIS Benchmarks Level 1/2, DISA STIGs, router/switch/firewall hardening, AAA (TACACS+/RADIUS), SSH-only, SNMPv3, NTP auth, logging, patching, config backup, and IaC validation."
tags: [network-hardening, cis-controls-v8, cis-benchmarks, disa-stig, device-hardening, router, switch, firewall, aaa, tacacs-plus, radius, ssh, snmpv3, ntp, logging, patching, config-backup, iac, terraform, ansible, cis-cat, stig-viewer]
---

# Network Hardening Baselines

A hardening baseline is a documented, measurable, repeatable secure configuration for a network device or service. Baselines turn "secure by default" from aspiration into an auditable state: every device is compared against the same control set, deviations are tracked, and changes flow through review. This reference consolidates the common baseline sources and the concrete controls applied to routers, switches, and firewalls.

## CIS Controls v8 — Network Safeguards

CIS Controls v8 organizes network security under Safeguard 12 (*Network Infrastructure Management*). Implementation Groups (IG1/IG2/IG3) gate which safeguards are expected.

| Safeguard | Requirement | IG |
|-----------|-------------|----|
| 12.1 | Ensure network infrastructure is up to date (firmware/OS on supported releases) | IG1 |
| 12.2 | Establish and maintain a secure network architecture (segmented, documented) | IG1 |
| 12.3 | Securely manage network devices (AAA, encrypted management, hardened configs) | IG1 |
| 12.4 | Establish and maintain an isolation boundary (firewall/segmentation between zones) | IG1 |
| 12.5 | Centralize network device authentication, authorization, and accounting (AAA) | IG2 |
| 12.6 | Use secure network management protocols (SSH, SNMPv3, HTTPS; no Telnet/SNMPv1/v2c) | IG1 |
| 12.7 | Ensure remote devices connect via encrypted VPN (no plaintext remote access) | IG1 |
| 12.8 | Establish and maintain dedicated management interfaces/VLANs (OOB where possible) | IG2 |

Supporting safeguards: 1.1 (asset inventory), 4.1 (secure config process), 4.7 (remove unapproved software), 7.1 (centralized log management), 7.4 (time sync), and 10.x (malware/egress). A device cannot be "hardened" if it is not inventoried and logged.

## CIS Benchmarks: Level 1 vs Level 2

CIS Benchmarks are device- and OS-specific hardening guides scored against two profiles:

- **Level 1** — essential, low operational impact; expected on every system. Disables obvious insecure defaults (Telnet, HTTP, default accounts, unused services) without breaking typical workloads.
- **Level 2** — defense-in-depth; may reduce functionality or usability and requires testing. Adds stricter crypto, additional logging, MACsec/IPsec, control-plane policing, and restricted management sources.

Selection guidance: start at Level 1 organization-wide, then promote critical/edge devices to Level 2 after lab validation. Track compliance with CIS-CAT.

## DISA STIGs

DISA Security Technical Implementation Guides (STIGs) are the DoD baseline, widely adopted as a strong reference even outside federal environments. Key properties:

- Mandatory in US federal/DoD; mapped to NIST SP 800-53 controls.
- Severity categories: CAT I (high), CAT II (medium), CAT III (low). CAT I findings must be remediated before ATO.
- Device STIGs exist for Cisco, Juniper, Palo Alto, Fortinet, Arista, F5.
- STIG Viewer supports manual and SCAP-automated assessment; XCCDF/OVAL enables automated scans.

Use STIGs where a stronger, auditable baseline is needed; CIS Benchmarks where vendor-neutral, broader coverage is preferred. Many organizations run CIS Level 1 + STIG CAT I/II.

## Device Hardening: Routers, Switches, Firewalls

### Management Plane

The management plane is the highest-value target; compromise here equals full device control.

```
! Disable insecure services
no ip http server
ip http secure-server
ip http authentication local
!
! Restrict management sources
access-list 10 permit 10.0.0.0 0.0.0.255
line vty 0 15
 transport input ssh
 access-class 10 in
 login local
 exec-timeout 10 0
!
! Out-of-band management (preferred)
interface Mgmt0
 description OOB-MGMT
 ip address 192.168.100.10 255.255.255.0
 no shutdown
```

### Control Plane

Protect the route processor from DoS and reconnaissance with control-plane policing (CoPP) and disable unused protocols.

```
control-plane
 service-policy input COPP-POLICY
!
! Disable unnecessary services
no cdp run
no lldp run
no ip source-route
no ip redirects
no ip unreachables
no ip proxy-arp
no service pad
service tcp-keepalives-in
service tcp-keepalives-out
```

### Data Plane

Default-deny forwarding, anti-spoofing, and storm control reduce abuse and lateral movement.

```
! uRPF against spoofing
interface GigabitEthernet0/1
 ip verify unicast source reachable-via rx
!
! Storm control
 storm-control broadcast level 5.00
 storm-control multicast level 5.00
!
! Default-deny ACL applied at zone boundary
ip access-list extended EDGE-IN
 deny ip 10.0.0.0 0.255.255.255 any
 deny ip 172.16.0.0 0.15.255.255 any
 deny ip 192.168.0.0 0.0.255.255 any
 permit tcp any any eq 443
 deny ip any any log
```

## AAA: TACACS+ vs RADIUS

| Property | TACACS+ | RADIUS |
|----------|---------|--------|
| Transport | TCP 49 | UDP 1812/1813 (auth/accounting) |
| Encryption | Entire payload | Password only (attributes in clear) |
| AAA separation | Separate authz/author/accounting | Combined auth + author |
| Best for | Device administration (network gear) | Network access (802.1X, VPN users) |
| Vendor | Cisco-origin (open standard RFC 8907) | IETF standard (RFC 2865/2866) |

```
! TACACS+ for device admin
aaa new-model
tacacs server TAC1
 address ipv4 10.0.0.5
 key 0 <shared-secret>
!
aaa group server tacacs+ TACACS-GROUP
 server name TAC1
!
aaa authentication login default group TACACS-GROUP local
aaa authorization exec default group TACACS-GROUP local
aaa accounting exec default start-stop group TACACS-GROUP
!
! RADIUS for 802.1X / VPN
radius server RAD1
 address ipv4 10.0.0.6 auth-port 1812 acct-port 1813
 key 0 <shared-secret>
```

Always configure a local fallback account (break-glass) with a strong password stored in a vault, and test AAA failure (server unreachable) before deployment.

## SSH-Only Management

Disable Telnet, rlogin, and HTTP management; require SSHv2 with strong algorithms.

```
ip domain-name example.com
crypto key generate rsa modulus 2048
!
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
!
line vty 0 15
 transport input ssh
!
! Harden SSH algorithms (IOS-XE 16.9+)
ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr
ip ssh server algorithm mac hmac-sha2-256 hmac-sha2-512
ip ssh server algorithm kex diffie-hellman-group14-sha256
```

Use key-based admin authentication where supported, disable SSH password auth for privileged accounts, and rotate host keys on suspected compromise.

## SNMPv3

Remove SNMPv1/v2c communities entirely; use SNMPv3 with authentication and privacy (authPriv).

```
no snmp-server community public
no snmp-server community private
!
snmp-server group NETOPS v3 priv
snmp-server user monitor NETOPS v3 auth sha <auth-pass> priv aes 256 <priv-pass>
snmp-server host 10.0.0.20 version 3 priv monitor
!
! Restrict SNMP source
snmp-server community ...  (none)
access-list 20 permit 10.0.0.20
snmp-server group NETOPS v3 priv access 20
```

Avoid reusing auth/priv passwords across devices; store them in a secrets manager; rotate on personnel change.

## NTP Authentication

Clock skew breaks TLS, IPsec, Kerberos, and log correlation. Authenticate NTP and use at least two sources.

```
ntp authenticate
ntp trusted-key 1
ntp server 10.0.0.10 key 1 prefer
ntp server 10.0.0.11 key 2
!
ntp authentication-key 1 md5 <key1>
ntp authentication-key 2 md5 <key2>
!
clock timezone UTC 0
```

Prefer NTP over authenticated channels (NTS where supported) and monitor for large time jumps. Block NTP amplification by restricting query access to trusted sources.

## Logging

Centralize logs in a SIEM with integrity and retention controls.

```
logging host 10.0.0.20 transport tcp port 514
logging trap informational
logging source-interface Loopback0
logging on
!
! Buffered local fallback
logging buffered 65536 informational
service timestamps log datetime msec localtime show-timezone
```

## Patching & Lifecycle

- Maintain an accurate inventory with model, firmware version, and EoL/EoS dates.
- Define cadence: critical (CVSS >= 9 or exploited) within 7 days; high within 30 days; others quarterly.
- Stage patches in a lab; verify config preservation across upgrades; keep rollback images.
- Track CVEs affecting network gear (vendor advisories, CISA KEV); subscribe to PSIRT feeds.
- Retire EoL devices.

## Configuration Backup & Integrity

Back up configs automatically after every change and on a schedule; verify integrity.

```
! Archive to secure server
archive
 path tftp://10.0.0.30/$h-$t
 write-memory
 time-period 1440
```

Controls: store backups encrypted and access-controlled; hash configs (SHA-256) against a known-good baseline; alert on unauthorized changes; keep version history with change attribution; exclude secrets or store them in a vault.

## IaC Validation

Treat device configuration as code: version control, review, automated validation, and CI/CD gates.

- Store configs/templates in Git; require PR review and approval.
- Use Ansible/Terraform/Netmiko for deployment; idempotent, repeatable.
- Validate with CIS-CAT (CIS Benchmarks) and STIG Viewer/SCAP before merge.
- Lint configs (e.g., `ciscoconfparse`, Batfish) for syntax and policy violations.
- Fail the pipeline on regression; produce compliance reports as artifacts.
- Diff intended vs running config; alert on drift.

```
# Example CI step (conceptual)
cis-cat.sh -b benchmarks/CIS_Cisco_IOS_Benchmark.xml -a -r reports/
stig-viewer --scan configs/router.cfg --stig cisco-ios-stig.xml
```

## Best Practices

- Default-deny all policies; document business justification per rule.
- Disable unused services/ports; remove default accounts.
- AAA with MFA for admin access; prefer out-of-band management.
- SSH only; SNMPv3 authPriv; authenticated NTP.
- Centralized logging with integrity and retention.
- Patch on defined cadence; track and retire EoL.
- Validate baselines in CI/CD; fail on regression.
- Test backups and restores regularly.
- Separate management, control, and data planes.

## Gotchas

- Default vendor configs are insecure (default passwords, Telnet, SNMPv2c).
- CoPP misconfiguration can lock you out; test before applying broadly.
- AAA server outage locks out admins if no local fallback is configured.
- SNMPv3 user creation syntax varies by platform; verify with `show snmp user`.
- NTP auth key mismatches silently fall back to unauthenticated sync on some platforms.
- Config backups often contain secrets; encrypt and restrict access.
- CIS/STIG findings include false positives; review before remediation.
- IaC validation catches config drift, not runtime state; pair with periodic scans.
- "Compliant" is not "secure"; baselines are floors, not ceilings.
