---
name: "DNS Security"
description: "DNS fundamentals, DNSSEC, DoH/DoT enterprise considerations, RPZ/filtering, tunneling/exfiltration detection, DGA and fast flux, cache poisoning, resolver hardening, split-horizon, monitoring, and operational best practices."
tags: [dns, dnssec, doh, dot, rpz, dns-filtering, dns-tunneling, exfiltration, dga, fast-flux, cache-poisoning, resolver, split-horizon, bind, unbound, dns-over-https, dns-over-tls]
---

# DNS Security

DNS is the Internet's directory service and a critical control point: every connection starts with a name lookup, so whoever controls or observes DNS controls reachability, privacy, and much of the detection surface. This reference covers DNS fundamentals, DNSSEC, encrypted DNS (DoH/DoT), filtering and RPZ, tunneling and exfiltration detection, DGA and fast flux, cache poisoning, resolver hardening, split-horizon, monitoring, and operational best practices.

## DNS Fundamentals

DNS is a distributed, hierarchical, eventually consistent database. Names are resolved top-down from the root (`.`) through TLD servers to authoritative servers. Key record types: `A`/`AAAA` (address), `CNAME` (alias), `MX` (mail), `NS` (delegation), `SOA` (zone authority), `TXT` (text/SPF/DKIM/DMARC), `SRV`, `PTR` (reverse), `CAA` (cert issuance policy), and `HTTPS`/`SVCB` (service binding, RFC 9460).

Resolution modes:

- **Recursive resolver** — accepts client queries and walks the hierarchy (or uses a forwarder) to return a final answer; caches results per TTL.
- **Authoritative server** — holds zone data and answers only for its zones.
- **Stub resolver** — OS/library client that forwards to a configured resolver.

Key properties: UDP transport (truncation → TCP fallback), TTL caching, negative caching (RFC 2308), case randomization (0x20), EDNS0 (RFC 6891). DNS lacks built-in auth/confidentiality — DNSSEC, DoT, and DoH fill that gap.

## DNSSEC

DNSSEC (RFC 4033–4035, updated by 6840/8198) adds origin authentication and data integrity via public-key signatures; it does **not** provide confidentiality. Each zone is signed with a Zone Signing Key (ZSK); the Key Signing Key (KSK) signs the DNSKEY RRset. A parent publishes a `DS` (Delegation Signer) record matching the child's KSK, forming a chain of trust from the root.

Core records: `DNSKEY`, `RRSIG` (signature), `DS`, `NSEC`/`NSEC3` (authenticated denial of existence). Validation outcomes: `AD` (authentic data) bit set by a validating resolver; `SERVFAIL` on validation failure (by default).

Operational practices:

- Automate key rollover with RFC 7583 timing; prefer ECDSA P-256 (algorithm 13) or Ed25519 (15) over RSA for smaller signatures and better performance.
- Use NSEC3 with a salt and reasonable iterations (avoid high iteration counts — CPU DoS) to prevent zone enumeration, or NSEC for simpler, faster negative answers.
- Monitor expiration: RRSIGs expire; a missed re-signing breaks the zone. Alert on validation failures and on `DS`/`DNSKEY` mismatches.
- Keep the parent `DS` in sync; a stale `DS` after a KSK rollover causes a validation break.
- DNSSEC does not stop a compromised authoritative server from serving valid (but malicious) signed data — it authenticates the zone owner, not intent.

## DoH and DoT Enterprise Considerations

**DoT (RFC 7858)** runs DNS over TLS on port 853; **DoH (RFC 8484)** carries DNS as HTTPS on port 443; **DoQ (RFC 9250)** uses QUIC. All provide confidentiality and integrity and defeat on-path spoofing.

Enterprise tradeoffs:

- **Bypass risk:** browsers and OSes may enable DoH to public resolvers by default, bypassing corporate DNS filtering, RPZ, logging, and DLP. Mitigate with MDM/GPO to set the OS resolver and disable browser DoH auto-upgrade (Firefox `network.trr.mode`, Chrome policies), and by blocking outbound 443 to known DoH endpoints where policy allows.
- **Centralized trust:** the chosen resolver sees all queries; prefer internal validating resolvers or contracted providers.
- **Detection loss:** encrypted DNS hides queries from passive sensors; move detection to resolver logs.
- **Performance:** DoH adds HTTP overhead; DoT is leaner; DoQ helps on lossy links.
- **Keep DNSSEC validation** even with DoH/DoT — encryption protects the channel, DNSSEC authenticates the data.

## DNS Filtering and RPZ

Response Policy Zones (RPZ, RFC draft / ISC implementation) let a resolver rewrite answers based on policy: return `NXDOMAIN`, a sinkhole IP, or a redirect for malicious domains. Combined with threat-intelligence feeds, RPZ is a high-leverage control.

Example (BIND 9 RPZ):

```text
// named.conf
options {
    response-policy { zone "rpz.local"; };
};

zone "rpz.local" {
    type master;
    file "rpz.local.zone";
    allow-query { none; };
    allow-transfer { none; };
};
```

```text
; rpz.local.zone
$TTL 300
@   SOA ns.example.com. admin.example.com. (1 3600 600 86400 300)
    NS  ns.example.com.

; Sinkhole known bad domain
bad.example.com     CNAME .
*.bad.example.com   CNAME .

; Redirect C2 to a walled garden
c2.example.net      A 10.0.0.99
```

Filtering approaches: RPZ at the resolver, cloud DNS filtering (Cisco Umbrella, Cloudflare Gateway), and endpoint agents. Layer them; a single RPZ zone is a single point of failure for policy. Maintain an allowlist for false positives and a change process for feed updates. RPZ actions should be logged for incident response.

## DNS Tunneling and Exfiltration Detection

DNS tunneling encodes data in query names (subdomains) and responses, using DNS as a covert channel (e.g., `iodine`, `dnscat2`, `dns2tcp`). Detection signals:

- Unusually long query names or many labels; high entropy in subdomain labels; base32/base64-like strings.
- High query volume to a single domain or to newly registered/low-reputation domains.
- TXT record abuse; large response sizes; DNS over non-standard resolvers.
- Beaconing cadence; queries for random-looking names with consistent length.

Detections: statistical entropy scoring on labels, length thresholds, volume per registrable domain, allowlisting of known CDNs/anycast. Correlate with proxy/EDR telemetry. Block or rate-limit at the resolver; alert rather than silently drop to preserve evidence.

## DGA and Fast Flux

**Domain Generation Algorithms (DGAs)** produce pseudo-random domains seeded by date/seed so malware can find C2 even when domains are taken down. Detection: entropy, n-gram/linguistic scoring, domain age, registration patterns, and ML classifiers trained on known DGA families. Many DGAs are seeded by the current date, so pre-generate candidate domains and blocklist proactively.

**Fast flux** rapidly rotates A records across many IPs (often compromised hosts) to evade IP-based blocking and takedowns; double flux also rotates NS records. Signals: very short TTLs, many distinct IPs per domain, IP diversity across ASNs/geos, and low reuse. Mitigate with TTL floors at the resolver, reputation feeds, and correlation with IP/ASN reputation.

## Cache Poisoning

Cache poisoning injects false records into a resolver's cache, redirecting users (Kaminsky attack: flooding with spoofed responses matching a pending query's TXID/port). Defenses:

- Source port randomization and TXID randomization (RFC 5452).
- 0x20 case randomization in query names.
- Bailiwick checking: a resolver must not accept records for names outside the queried zone's authority (prevents injecting `example.com` A from a `evil.com` response).
- DNSSEC validation — the strongest defense; a poisoned unsigned answer fails validation.
- Short cache TTLs for unvalidated data; DNS cookies (RFC 7873) for resolver-server authentication.
- Patch and keep resolver software current; disable recursion for untrusted clients.

## Resolver Hardening

Harden recursive resolvers (BIND, Unbound, Knot Resolver, PowerDNS Recursor):

- Restrict recursion to trusted networks (`allow-recursion`/`access-control`).
- Disable version disclosure (`version none` / `hide-version`).
- Rate-limit queries per client (`rate-limit` in BIND; `ratelimit` in Unbound) to mitigate amplification and abuse.
- Enable DNSSEC validation; set trust anchors (root KSK) and auto-update (`auto-trust-anchor-file`).
- Minimize caching of unvalidated data; set sensible TTL caps.
- Run as non-root; chroot/jail; keep patched.
- Log queries and responses with client IP; forward to SIEM.
- Use anycast for resilience; monitor resolver health.

Unbound example:

```yaml
server:
    interface: 0.0.0.0
    access-control: 10.0.0.0/8 allow
    access-control: 0.0.0.0/0 refuse
    hide-version: yes
    harden-glue: yes
    harden-dnssec-stripped: yes
    harden-below-nxdomain: yes
    use-caps-for-id: yes
    prefetch: yes
    rrset-roundrobin: yes
    minimal-responses: yes
    val-clean-additional: yes
    auto-trust-anchor-file: "/var/lib/unbound/root.key"
    verbosity: 1
    log-queries: yes
```

## Split-Horizon DNS

Split-horizon (split-brain) serves different answers for the same name based on client source (internal vs external), commonly for internal-only hostnames or private IPs. Risks: information leakage if internal names resolve externally; inconsistency causing debugging pain; DNSSEC complexity (different views need separate signing or unsigned internal zones). Best practices: keep internal zone names distinct where possible (e.g., `corp.example.com` vs `example.com`); restrict internal view to trusted networks; document views; avoid publishing internal records in public zones; monitor for leakage; consider zero-trust alternatives (private DNS in cloud) instead of split-horizon where feasible.

## Monitoring

- Query volume, response codes (`NXDOMAIN`, `SERVFAIL`), latency, cache hit rate.
- DNSSEC validation failure rates; RRSIG expiry countdown.
- Top talkers and top queried domains; new/rare domains; entropy scores.
- Tunneling/DGA/fast-flux alerts; RPZ hit counts.
- Resolver availability and anycast health; amplification indicators (large responses to small queries).
- Log retention per compliance; correlate DNS with DHCP/identity for attribution.

## Best Practices

- Use DNSSEC-validating resolvers; validate from root trust anchor.
- Enforce encrypted DNS (DoT/DoH) to approved resolvers only; block unauthorized endpoints.
- Deploy RPZ with curated, reviewed threat feeds and an allowlist process.
- Restrict recursion; rate-limit; disable version disclosure.
- Monitor for tunneling, DGA, and fast flux with entropy/volume analytics.
- Keep resolver software patched; run least-privilege.
- Use split-horizon carefully; avoid internal name leakage.
- Retain query logs in SIEM; correlate with identity and endpoint telemetry.
- Test failover and anycast; document resolver topology.

## Gotchas

- DNSSEC breaks if RRSIGs expire or parent `DS` is stale — automate signing and monitor.
- DoH can silently bypass corporate controls; enforce resolver policy via MDM/GPO.
- RPZ can cause outages if a feed has false positives; always maintain an allowlist and rollback.
- DNS tunneling detection has false positives on CDNs and DGA-like but legitimate domains (e.g., some cloud storage); tune with allowlists.
- Split-horizon complicates DNSSEC and troubleshooting; keep views documented.
- Case randomization (0x20) and EDNS0 may break broken middleboxes/old resolvers.
- Negative caching can prolong outages after a fix; flush caches or wait for TTL.
- Clock skew breaks DNSSEC validation (signature validity windows).
- Amplification attacks exploit open resolvers; never expose recursion publicly.

---

*Reference — DNS Security (network-security skill).*
