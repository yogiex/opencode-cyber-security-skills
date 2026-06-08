---
name: "Incident Type Playbooks"
description: "Complete playbooks for 8 incident types: ransomware, data breach/exfiltration, account compromise, phishing/BEC, insider threat, DDoS, cloud incidents, and web application compromise. Each playbook covers triage, containment, evidence, decision points, eradication, recovery, and prevention."
tags: [ecih, playbooks, ransomware, data-breach, phishing, insider-threat, ddos, cloud-incident, web-compromise]
---

## Incident Types & Response Playbooks

### Esensi Playbook

Playbook adalah **panduan strategis untuk jenis insiden tertentu**. Setiap playbook memberikan langkah-langkah keputusan yang sudah teruji, mengurangi waktu berpikir saat krisis.

### Playbook 1: Ransomware

**Tujuan**: Menghentikan penyebaran ransomware dan meminimalkan data loss.

**Triage & Detection**:
- Endpoint melaporkan file terenkripsi
- Ransom note muncul di desktop
- File extension berubah (contoh: .encrypted, .lockbit)
- Log menunjukkan proses encryption massal

**Containment**:
1. Isolasi endpoint dari network segera
2. Disable semua network share di segment terkena
3. Block ransomware extensions di perimeter (jika sudah diketahui)
4. Jangan matikan endpoint — capture memory dulu

**Evidence**:
1. Screenshot ransom note
2. Capture memory dari affected endpoint
3. Collect sample encrypted file + ransom note
4. Log timestamps dari encryption start

**Decision Points**:
- Bayar tebusan? → Hanya keputusan EXECUTIVE, dengan input legal
- Restore dari backup? → Verifikasi backup tidak terenkripsi
- Notify law enforcement? → Ya, ransomware adalah criminal activity

**Eradication & Recovery**:
1. Reimage semua endpoint terkena
2. Restore data dari backup bersih
3. Patch initial vector (biasanya RDP, phishing, atau vulnerability)

**Prevention untuk masa depan**:
- Backup 3-2-1 rule
- Network segmentation ketat
- Disable RDP from internet
- Email security gateway
- EDR dengan anti-ransomware

### Playbook 2: Data Breach / Data Exfiltration

**Tujuan**: Menghentikan kebocoran data, menentukan scope, memenuhi kewajiban notifikasi.

**Triage & Detection**:
- DLP alert
- Unusual large outbound data transfer
- Customer notification
- Dark web discovery

**Containment**:
1. Identifikasi dan block exfiltration vector
2. Revoke compromised credentials
3. Isolasi database atau share yang bocor
4. Block IP tujuan exfiltration di firewall

**Evidence**:
1. Log transfer data (siapa, kapan, berapa)
2. Data yang bocor (sample untuk identifikasi)
3. Akses log dari akun terkompromi
4. Timeline exfiltration

**Decision Points**:
- Apakah data termasuk PII/PHI? → Regulatory notification wajib
- Apakah data finansial? → PCI DSS notification
- Apakah data terenkripsi? → Kurangi severity
- Berapa jumlah record? → Threshold notification

**Eradication & Recovery**:
1. Patch vulnerability
2. Reset semua credentials terkait
3. Implement additional monitoring
4. Prepare disclosure notifications

**Regulatory Timelines**:
- GDPR: 72 jam ke supervisory authority
- HIPAA: 60 hari ke affected + HHS
- State breach laws: 30-90 hari

### Playbook 3: Account Compromise

**Tujuan**: Menghentikan akses unauthorized dan memulihkan akun.

**Triage & Detection**:
- Successful login dari lokasi tidak biasa
- Multiple failed logins lalu success
- User reports suspicious activity dari akunnya
- SIEM alert: impossible travel

**Containment**:
1. Disable akun
2. Force logout semua sessions
3. Revoke semua tokens, API keys, sessions
4. Reset password (jika disable bukan pilihan)

**Evidence**:
1. Log login history (lokasi, IP, timestamp, user agent)
2. Email access log (email read, sent, forwarding rules)
3. File access log (files viewed, downloaded)
4. API calls log (jika cloud)

**Decision Points**:
- Apakah MFA aktif? → Jika tidak, kritikalitas lebih tinggi
- Apakah akun admin? → Scope lebih luas, prioritaskan
- Apakah email terakses? → Check forwarding rules, email content

**Eradication & Recovery**:
1. Remove malicious forwarding rules
2. Remove malicious email filters
3. Check for persistence (OAuth apps, service principals)
4. Enable MFA
5. User awareness reinforcement

### Playbook 4: Phishing / BEC (Business Email Compromise)

**Tujuan**: Mengidentifikasi scope, menghentikan propagation, memulihkan akun.

**Triage & Detection**:
- User reports suspicious email
- SIEM alert: multiple users clicking same link
- Finance department receives invoice change request
- Email security gateway alert

**Containment**:
1. Remove malicious email dari semua mailbox (search & destroy)
2. Block sender domain/IP
3. Block malicious URL di web gateway
4. Disable compromised accounts

**Evidence**:
1. Full email header
2. Email copy (with attachments)
3. URL analysis (where it leads)
4. Mailbox rules created
5. Sent items (what was sent from compromised account)

**Decision Points**:
- Apakah BEC? → Transaction reversal mungkin perlu
- Apakah credential harvesting? → Force password reset
- Apakah malware delivery? → Endpoint scan
- Scope: berapa banyak user yang menerima?

**Eradication & Recovery**:
1. Password reset untuk semua user yang klik
2. MFA enforcement
3. User training — this is a teaching moment
4. Update email security rules

### Playbook 5: Insider Threat

**Tujuan**: Menghentikan aktivitas insider sambil meminimalkan risiko legal dan mempertahankan employment rights.

**Triage & Detection**:
- Unusual data access (malam, weekend, large volume)
- HR notification (resignation, disciplinary)
- Policy violation report
- DLP alert on user

**PENTING**: Insider threat adalah **yang paling sensitif secara legal**. Koordinasi dengan HR dan Legal SEBELUM tindakan apapun.

**Containment**:
1. Disable akses secara rahasia (jangan trigger)
2. Preserve data — jangan konfrontasi
3. Monitor activity lebih ketat
4. HR involvement before any action

**Evidence**:
1. Access logs (file, system, building)
2. Email and communication
3. Data transfer logs
4. Physical security logs (badge access)
5. HR records (employment status, performance)

**Decision Points**:
- Apakah ini pelanggaran policy? → Internal action
- Apakah ini kriminal? → Law enforcement
- Apakah ini terminasi? → HR process
- Apakah ini unintentional? → Training

**Recovery**:
1. Access revocation
2. Asset return
3. IT deprovisioning
4. Documentation for legal

### Playbook 6: DDoS / Availability Attack

**Tujuan**: Mengembalikan availability layanan.

**Triage & Detection**:
- Traffic spike dari banyak source IP
- Service slow atau down
- Cloud/CDN scaling alerts
- Customer complaints

**Containment**:
1. Enable DDoS mitigation (cloud provider, CDN)
2. Rate limiting di WAF/load balancer
3. Blackhole routing jika perlu
4. Scale infrastructure

**Evidence**:
1. Traffic capture (PCAP)
2. Logs — source IPs, patterns, duration
3. Bandwidth utilization graphs
4. Mitigation effectiveness data

**Decision Points**:
- Apakah ini DDoS atau DoS? → Multiple sources?
- Apakah ini application layer atau network layer? → Layer 7 vs Layer 3/4
- Apakah ada extortion? → Law enforcement

**Recovery**:
1. Monitor traffic for residual
2. Analyze attack patterns
3. Update WAF rules
4. Implement permanent mitigation

### Playbook 7: Cloud Incident

**Tujuan**: Mengidentifikasi dan menghentikan akses unauthorized di cloud environment.

**Triage & Detection**:
- Cloud trail alert
- Unusual API calls
- New resources deployed unexpectedly
- Billing spike
- CSP notification

**Containment**:
1. Revoke compromised keys
2. Restrict IAM policy
3. Isolate compromised resources (security group, VAC)
4. Enable CloudTrail/audit logging if disabled

**Evidence**:
1. Cloud trail logs
2. IAM access logs
3. Resource configuration history
4. Billing data

**Decision Points**:
- Apakah ini misconfiguration atau intentional attack?
- Apakah data di bucket publik?
- Apakah compute instance compromised?

**Eradication & Recovery**:
1. Remove unauthorized resources
2. Fix misconfigurations
3. Rotate ALL keys (not just compromised)
4. Implement IaC with security scanning

### Playbook 8: Web Application Compromise

**Tujuan**: Mengidentifikasi dan menutup vulnerability web application.

**Triage & Detection**:
- WAF alerts
- Web server logs showing exploitation attempts
- File integrity monitoring alert
- Customer reports defacement

**Containment**:
1. Take application offline if necessary
2. Block attacking IPs
3. WAF rule update
4. Disable compromised functionality

**Evidence**:
1. Web server logs (access, error)
2. Application logs
3. Database logs
4. File system changes
5. Network connections from web server

**Eradication & Recovery**:
1. Remove web shells
2. Patch vulnerability
3. Update WAF rules
4. Code review for similar vulnerabilities
5. Re-deploy from clean codebase
