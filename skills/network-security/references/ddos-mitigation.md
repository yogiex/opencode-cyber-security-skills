---
name: "DDoS Mitigation & Resilience"
description: "DDoS attack taxonomy, amplification vectors, detection, scrubbing, rate limiting, blackholing/RTBH, capacity planning, CDN/edge defense, BCP38, and game-day testing."
tags: [ddos, denial-of-service, volumetric, protocol-flood, application-layer, amplification, reflection, scrubbing, rate-limiting, blackhole, rtbh, bgp-flowspec, anycast, bcp38, urpf, cdn, waf, capacity-planning, game-day, resilience]
---

# DDoS Mitigation & Resilience

Distributed Denial of Service (DDoS) attacks exhaust bandwidth, state, compute, or application capacity so legitimate users cannot reach a service. Defense is layered: reduce attack surface, detect early, absorb where possible, and scrub or shed malicious traffic before it reaches critical systems. Volumetric, protocol, and application attacks need different signals and controls.

## Attack Taxonomy

| Class | Vectors | Primary Impact |
|---|---|---|
| Volumetric | UDP/ICMP floods, DNS/NTP amplification, reflection floods | Link, router, or transit saturation |
| Protocol | SYN/ACK/RST floods, fragmented packets, state-table exhaustion | Firewall/router state exhaustion, half-open connections |
| Application (L7) | HTTP GET/POST floods, Slowloris, RUDY, cache busting, API abuse, TLS handshake floods | Worker/thread exhaustion, database load, latency collapse |

- Volumetric attacks are measured in bps/pps and often require upstream capacity, anycast, or scrubbing.
- Protocol attacks exploit finite tables and state machines; use SYN cookies/proxies, connection limits, and state-aware firewalls.
- Application attacks can be low bandwidth but expensive; use WAF rules, bot management, caching, normalization, and per-endpoint limits.

## Amplification and Reflection Vectors

Amplification attacks spoof the victim's source address and send small requests to services that return much larger responses.

| Vector | Amplification | Defense |
|---|---:|---|
| DNS (open resolvers) | 28-54x | Disable open recursion, restrict by ACL, response rate limiting |
| NTP (monlist) | 200-500x+ | Disable monlist, restrict queries, patch |
| SNMP | 6-10x+ | Remove public communities, restrict, use v3 |
| SSDP/UPnP | 30x+ | Disable UPnP, filter UDP/1900 |
| Memcached | 10,000-50,000x | Bind to localhost, disable UDP, firewall |
| CLDAP | 50-70x | Restrict CLDAP, patch, filter UDP/389 |
| CoAP | 10-50x | Restrict endpoints, filter UDP/5683 |

Operators should disable unnecessary UDP services, restrict queries, patch software, and filter spoofed traffic at the edge.

## Detection

### Baselines and Telemetry

Baseline normal traffic using metrics such as bps/pps by interface, prefix, and protocol; new flows and unique sources/destinations; TCP SYN/SYN-ACK/RST ratios; HTTP request, error, cache-hit, and latency percentiles; DNS query rate, response size, and NXDOMAIN ratio; firewall state usage; and CPU, memory, drops, and interface errors. Use rolling windows, seasonal baselines, and rate-of-change alerts; correlate network, application, and endpoint telemetry to distinguish attacks from spikes.

Useful sources include NetFlow/IPFIX, sFlow, SNMP, BGP state, DNS/WAF/load-balancer logs, and host metrics; retain history for comparison.

### Anycast and Distributed Detection

Anycast advertises the same prefix from multiple PoPs, routing users to the nearest healthy site. It distributes attack traffic, enables local absorption, and allows overloaded PoPs to be drained with BGP.

For detection:

- Collect per-PoP flow and application metrics
- Compare site-level baselines, not only global totals
- Use health checks and BGP communities to drain overloaded sites
- Send suspicious traffic to regional scrubbing while keeping clean PoPs online
- Monitor BGP withdrawals, flaps, and asymmetric paths

Anycast aids DNS, CDN, and API entry points but does not replace scrubbing or rate limiting.

## Mitigation Techniques

### Scrubbing Centers

Scrubbing centers receive diverted traffic, remove malicious flows, and forward clean traffic. Diversion uses BGP, GRE tunnels, or DNS redirection.

- Always-on: simpler operations, higher cost and latency
- On-demand: lower cost, depends on fast detection and BGP convergence
- Partial proxy: scrubs L3/L4; full proxy: terminates TLS/HTTP and inspects L7

Example BGP diversion concept:

```text
route-map DDOS-DIVERT permit 10
  set community 65000:666 additive
  set local-preference 200

router bgp 65000
  neighbor 198.51.100.1 remote-as 65001
  neighbor 198.51.100.1 send-community
```

Validate capacity, latency, TLS handling, and return paths before an incident.

### Rate Limiting

Apply limits at L3/L4 (pps, new connections, SYN rate, fragments), L7 (requests per second/URI, logins, API calls), and DNS (queries per source, response rate limiting). Use token-bucket or leaky-bucket algorithms with burst allowances. Key by source IP, ASN, user agent, JA3/JA4, API key, or session. Be careful with CGNAT and shared egress IPs.

Example `nftables` rate limit:

```nftables
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        ct state established,related accept
        tcp dport 443 ct state new limit rate 2000/second burst 4000 packets accept
        tcp dport 443 ct state new drop
    }
}
```

Example nginx request rate limit:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    listen 443 ssl;
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_req_status 429;
        proxy_pass http://backend;
    }
}
```

### Blackholing and RTBH

Blackholing routes traffic for a victim address to `Null0`. It is fast but drops all traffic, including legitimate traffic; use as a last resort. RTBH uses BGP communities to signal an upstream provider or peer to discard traffic for a prefix.

Example RTBH concept:

```text
ip route 203.0.113.10 255.255.255.255 Null0

route-map RTBH-TRIGGER permit 10
  set community 65000:666

router bgp 65000
  redistribute static route-map RTBH-TRIGGER
  neighbor 198.51.100.1 send-community
```

For granular control, use BGP Flowspec to match protocol, port, packet length, or flags and apply discard, rate-limit, or redirect actions; validate rules carefully.

### Additional Mitigations

Enable SYN cookies/proxies, connection limits, L7 challenges, DNS rate limiting, caching/origin shielding, and origin-IP secrecy; filter by geography or ASN only with business justification.

## Capacity Planning

Plan for normal growth and attack conditions. State, CPU, memory, and connection tracking often fail before bandwidth.

| Resource | Metric | Guidance |
|---|---|---|
| Bandwidth | bps by direction | Provision headroom above peak; know transit/peering limits |
| Packets | pps | Size for small-packet floods; pps often limits routers first |
| Connections | new/sec, concurrent | Size firewall/LB state tables and worker pools |
| CPU | percent, softirq | Monitor per-core saturation; offload crypto/checksums |
| Memory | conntrack, caches, buffers | Set explicit limits and eviction policies |
| Scrubbing | contracted bps/pps | Verify limits, burst, and regional capacity |
| DNS | qps, response size | Size resolvers and anycast nodes; limit amplification |

Baseline peak traffic for 30-90 days including seasonal events. Add growth margin plus attack headroom. Prefer horizontal scaling and anycast over one large appliance. Include third-party dependencies and re-test after changes.

## CDN and Edge Defense

CDNs and edge networks distribute load and provide managed scrubbing.

- Terminate TLS/HTTP at the edge; use modern TLS carefully.
- Cache aggressively and use origin shielding.
- Deploy WAF rules, bot management, and rate limits at the edge.
- Hide origin IPs; allow origin traffic only from CDN/scrubbing ranges.
- Use health checks and automatic failover.
- Configure stale-while-revalidate and graceful degradation.

Example origin protection:

```nginx
allow 192.0.2.0/24;
allow 198.51.100.0/24;
deny all;
```

A CDN cannot protect an origin whose IP is directly reachable.

## BCP38 and Source Address Validation

BCP38 (RFC 2827) recommends ingress filtering to drop spoofed or invalid source addresses. It reduces reflection/amplification traffic and improves attribution.

- Deploy ingress filters at customer edges, ISPs, and hosting providers.
- Use uRPF:
  - Strict: source reachable via the same ingress interface
  - Loose: source reachable via any route
  - Feasible: alternate paths for multihomed/asymmetric networks
- Combine uRPF with ACLs for invalid ranges (RFC 1918, documentation prefixes, multicast, bogons).
- Participate in MANRS and require source validation from providers.

Example Cisco uRPF:

```text
interface GigabitEthernet0/0
  ip verify unicast source reachable-via rx
```

BCP38 does not stop attacks from legitimate source addresses.

## Testing and Game Days

Exercise readiness before a real incident:

- Tabletop exercises for detection, escalation, communication, and mitigation decisions
- Controlled load tests in staging or isolated environments
- Game days simulating attacks with clear abort criteria
- Red/purple team exercises against realistic floods and L7 abuse
- Vendor drills for scrubbing diversion, BGP communities, DNS changes, and support contacts
- Runbook validation for who can announce RTBH, change DNS TTL, enable WAF rules, or contact providers

Measure time to detect, time to mitigate, false positive rate, customer impact, and recovery time. Document findings, assign owners, and re-test after fixes.

## Best Practices

- Build defense in depth across network, edge, application, and DNS layers.
- Baseline traffic and alert on meaningful deviations, not just volume.
- Use anycast and CDN/edge absorption for internet-facing services.
- Keep scrubbing, RTBH, and Flowspec procedures documented and tested.
- Protect origin IPs and restrict direct access.
- Apply BCP38/uRPF and require it from providers.
- Use adaptive rate limits with business-aware thresholds.
- Maintain out-of-band access, DNS, and monitoring during incidents.
- Automate high-confidence mitigation; keep human approval for destructive actions.
- Run game days and post-incident reviews; update runbooks from lessons learned.

## Gotchas

- Blackholing a shared IP can impact many customers; prefer specific prefixes or L7 controls.
- RTBH and Flowspec changes can propagate slowly or be filtered by peers.
- Per-IP limits can harm users behind CGNAT or corporate proxies.
- Scrubbing can break protocols needing source IP preservation or specific TLS behavior.
- On-demand scrubbing depends on fast detection and BGP convergence.
- Application attacks may stay below volumetric thresholds while exhausting workers.
- CDN protection fails if origin IPs are exposed.
- Strict uRPF can drop legitimate traffic in asymmetric or multihomed networks.
- Load tests can become real incidents if not isolated.
- Game days need clear stop conditions.
- Metrics without baselines create noisy alerts.
- Amplification factors change as software and protocols evolve.<|end|><|start|>Assistant to=pwsh<|channel|>analysis <|constrain|>xml<|message|><rfl:parameter name="command">
(Get-Content 'skills/network-security/references/ddos-mitigation.md' | Measure-Object -Word).Words