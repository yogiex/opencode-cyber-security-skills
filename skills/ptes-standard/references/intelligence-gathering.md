---
name: "Phase 2 — Intelligence Gathering"
description: "PTES Phase 2 covering passive OSINT (DNS, WHOIS, Google dorks, Shodan, social media) and active reconnaissance (Nmap scanning, service enumeration, directory brute-force, technology fingerprinting) with three levels of intelligence gathering depth."
tags: [ptes, intelligence-gathering, osint, reconnaissance, nmap, dns-enumeration]
---

# Phase 2: Intelligence Gathering

## Objectives

Collect as much information as possible about target. Passive gathering (no direct interaction). Active gathering (direct probing, may be detectable).

## Passive OSINT Techniques

- DNS enumeration (NS, MX, TXT, subdomains)
- WHOIS records
- Google dorks (`site:target.com filetype:pdf`)
- Shodan, Censys (exposed services)
- Social media (LinkedIn, GitHub for employee info)
- Wayback Machine for historical pages

## Active Reconnaissance

- Network scanning (Nmap: `-sS -sV -O -p-`)
- Service enumeration (banner grabbing)
- Directory brute-force (gobuster, dirb)
- Technology fingerprinting (Wappalyzer, whatweb)

## OSINT Levels (PTES)

| Level | Effort | Techniques |
|-------|--------|------------|
| L1 (Basic) | 1-2 days | DNS, WHOIS, Google dorks, Shodan, social media |
| L2 (Intermediate) | 3-5 days | Cert transparency logs, job postings, dark web |
| L3 (Advanced) | 1-2 weeks | Social profiling, dumpster diving, RF scanning |

## Key Commands

```bash
amass enum -passive -d target.com -o passive.txt
sublist3r -d target.com -o subdomains.txt
dnsrecon -d target.com -t axfr
theHarvester -d target.com -b all -l 500
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq .
```

## Tools

Nmap, Amass, Sublist3r, Recon-ng, Maltego, Burp Suite, Shodan, Censys.

## Best Practices

- Start passive before active to avoid detection
- DNS enumeration first — fastest way to map attack surface
- Store all output for reproducibility and reporting
- Check certificate transparency logs for subdomains
