---
name: "Network Hunting with Suricata, Zeek & PCAP"
description: "Network-based threat hunting using Suricata IDS/IPS, Zeek logs, PCAP analysis, and network IOC hunting patterns."
tags: [suricata, zeek, pcap, ids, ips, network-hunting, dns]
---

# Network Hunting with Suricata, Zeek & PCAP

## Suricata IDS/IPS

Open-source IDS/IPS engine with rule-based detection.

**Rule Structure:**
```
action protocol src_ip src_port -> dst_ip dst_port
(msg:"message"; content:"pattern"; sid:1000001; rev:1;)
```

**Key Rule Categories:** ET (Emerging Threats), protocol anomalies, file extraction, DNS detection (DGA, tunneling).

**High Severity Alerts:**
```spl
index=suricata sourcetype=suricata:alert alert_severity=1
| stats count by alert_category, src_ip, dest_ip
```

**Alerts by Target:**
```spl
index=suricata sourcetype=suricata:alert
| stats count by dest_ip, alert_category
```

**Alerts by Signature:**
```spl
index=suricata sourcetype=suricata:alert
| stats count by alert_signature, src_ip
```

## Zeek (formerly Bro)

Provides high-level network analysis:

**conn.log — Suspicious Connections:**
```spl
index=zeek sourcetype=zeek:conn
| where duration > 3600 AND orig_bytes > 10000000
| table ts, id.orig_h, id.resp_h, proto, duration, orig_bytes
```

**dns.log — Unusual Queries:**
```spl
index=zeek sourcetype=zeek:dns
| eval query_len = len(query)
| where query_len > 40
| table ts, id.orig_h, query, qtype_name
```

**http.log — Suspicious User-Agents:**
```spl
index=zeek sourcetype=zeek:http
| search user_agent="curl*" OR user_agent="wget*" OR user_agent="python*"
| table ts, id.orig_h, id.resp_h, uri, user_agent
```

**ssl.log — Suspicious Certificates:**
```spl
index=zeek sourcetype=zeek:ssl
| search NOT server_name="*"
| stats count by id.orig_h, id.resp_h
| where count > 5
```

## Network IOC Hunting

**Known Bad IP/Domain:**
```spl
index=*
| search src_ip IN ("<malicious_ip>") OR dest_ip IN ("<malicious_ip>")
  OR query IN ("<malicious_domain>")
| table _time, src_ip, dest_ip, query, sourcetype
```

**Unusual Port/Protocol:**
```spl
index=*
| search port=4444 OR port=8443 OR port=1337 OR port=31337
| stats count by src_ip, dest_ip, dest_port
```

**Protocol Mismatch:**
```spl
| search sourcetype=dns AND dest_port=80
  OR sourcetype=http AND dest_port=53
```

## C2 Detection with Network Data

**Beaconing Analysis:**
```spl
index=proxy sourcetype=proxylogs
| stats count, dc(dest_ip) as UniqueDests, values(dest_ip) by src_ip
| where count > 100 AND UniqueDests < 3
| eval beacon_ratio = count / UniqueDests
```

**DNS Tunneling:**
```spl
index=dns sourcetype=dns
| eval domain_length = len(query)
| where domain_length > 50
| stats count by query, src_ip
```

**Data Exfiltration via HTTP:**
```spl
index=proxy sourcetype=proxylogs
| stats sum(bytes_out) as TotalBytes by src_ip, dest_ip
| where TotalBytes > 10000000
```

## Gotchas

- Suricata alerts di exam mungkin tidak 100% akurat — selalu verifikasi dengan data sources lain
- Zeek logs memiliki field names yang berbeda dari Suricata — jangan tertukar
- PCAP analysis biasanya tidak diperlukan di exam — fokus pada Suricata dan Zeek logs yang sudah diparse ke Splunk
- DNS tunneling detection perlu threshold yang tepat — domain length > 50 adalah indikasi tapi bukan konfirmasi

## Best Practices

- Selalu korelasikan network alerts dengan endpoint data untuk konfirmasi
- Gunakan Suricata alert severity sebagai prioritas triase (Severity 1 = critical)
- Untuk beaconing detection, gunakan kombinasi count + regularity analysis
- DNS logs adalah sumber paling underrated untuk threat hunting — prioritaskan analisis ini
