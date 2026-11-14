# Analisis Kebutuhan — Network VA (Vulnerability Assessment Jaringan)

**Status:** Analisis kebutuhan (belum implementasi)
**Tanggal:** 2026-11-14
**Acuan bentuk:** [PERSONA-INJECTION-NEEDS.md](PERSONA-INJECTION-NEEDS.md), [PUBLISHING-NEEDS.md](PUBLISHING-NEEDS.md)
**Skill terkait:** `skills/vulnerability-assessment/`
**Sumber ringkasan brainstorming:** output subagent `brainstorm-network-va` (14 topik, 8 file baru, 4 file existing diperluas, 18 gotchas)

---

## 1. Ringkasan

Skill `vulnerability-assessment` sudah punya metodologi VA umum, asset discovery, konfigurasi scanner, CVSS, prioritisasi, pelaporan, remediasi, dan persona. Namun aspek **Network VA** (VA pada jaringan: scanning, protokol, segmentasi, device, wireless, VPN, DNS/DHCP, TLS, IPv6, IoT/OT, NAC) hampir tidak ada: hanya 4 baris di `references/va-methodology.md` ("### Network VA") dan satu baris di `SKILL.md` ("Network (host/port) | Nessus, OpenVAS, Qualys"). Tidak ada referensi khusus. Akibatnya agent VA tidak mampu melakukan Network VA secara sistematis dan mendalam: tidak tahu urutan scanning jaringan (host discovery → port scan → service detection → vuln scan), tidak tahu tuning per protokol (SMB/RDP/SSH/TLS), tidak tahu audit segmentasi/firewall/device, tidak tahu wireless/VPN/DNS/DHCP, tidak tahu TLS deep, IPv6, IoT/OT, NAC.

Yang dibutuhkan: menambah 8 file referensi baru dan memperluas 4 file existing, plus pembaruan `SKILL.md` (capability map, reference documentation, progressive disclosure, gotchas) — **tanpa** mengubah persona atau menambah materi ujian. Dokumen ini mendefinisikan kebutuhan tersebut sebelum implementasi.

---

## 2. Temuan audit (bukti terukur)

Diukur 2026-11-14 terhadap `skills/vulnerability-assessment/`.

### 2.1 Apa yang ada

| # | Bukti | Cara memeriksa | Lokasi |
|---|---|---|---|
| E1 | `SKILL.md` 136 baris, mencakup profil persona, kapan dipakai, cara memerankan, persona contract (6), decision frame (7), siklus kerja, capability map (9 baris), reference documentation (9 file), gotchas (10), progressive disclosure | `wc -l SKILL.md` | `skills/vulnerability-assessment/SKILL.md` |
| E2 | `references/` berisi 9 file: `va-methodology.md`, `asset-discovery.md`, `scanner-config.md`, `cvss-scoring.md`, `prioritization.md`, `reporting.md`, `remediation-verification.md`, `persona.md`, `referensi.md` | `ls references/` | `skills/vulnerability-assessment/references/` |
| E3 | Network VA disebut hanya 4 baris di `va-methodology.md` ("### Network VA": port scan → service detection → vulnerability scan; credentialed scan; perhatikan firewall, IPS, rate limit, segment tidak reachable) | `grep -n "Network VA" va-methodology.md` → 1 hit, 4 baris konten | `references/va-methodology.md` L75-79 |
| E4 | `scanner-config.md` punya bagian "### Network (Nessus/OpenVAS/Qualys)" 5 baris: policy, exclude, schedule | `grep -n "Network" scanner-config.md` | `references/scanner-config.md` L70-74 |
| E5 | `asset-discovery.md` menyebut "Network scan (ARP, ping sweep)" sebagai sumber inventaris dan "Segmen yang Tidak Bisa Dijangkau" (VLAN, firewall, VPN khusus, IP diblokir) | `grep -n -i "network\|segment" asset-discovery.md` | `references/asset-discovery.md` |
| E6 | `reporting.md` struktur laporan umum; tidak ada bagian network-specific (topology, segment, device) | baca file | `references/reporting.md` |
| E7 | Gotchas `SKILL.md` 10 butir; tidak ada gotchas network-specific (firewall blocking, IPS, IPv6, IoT/OT, TLS, dll.) | baca file L107-119 | `SKILL.md` |
| E8 | `referensi.md` menyebut Nmap, Nessus, OpenVAS, Qualys sebagai tool network | baca file | `references/referensi.md` |

### 2.2 Apa yang tidak ada (gap)

| # | Gap | Bukti tidak ada | Dampak |
|---|---|---|---|
| G1 | Tidak ada file `network-scanning.md` (metodologi scanning jaringan: host discovery, port scan TCP/UDP, SYN vs connect, service/version detection, OS fingerprinting, timing, evasion, segment traversal) | `ls references/` tidak memuat file dengan prefix network | Agent tidak tahu urutan dan tuning scan jaringan |
| G2 | Tidak ada `network-vulnerabilities.md` (kerentanan jaringan umum: weak protocols, default creds, legacy services, misconfig) | idem | Agent tidak punya katalog kerentanan jaringan |
| G3 | Tidak ada `network-segmentation.md` (segmentasi, VLAN, firewall zones, micro-segmentation, audit) | idem | Agent tidak bisa audit segmentasi |
| G4 | Tidak ada `network-protocol-va.md` (SMB, RDP, SSH, TLS, protocol-specific VA) | idem | Agent tidak tahu per-protokol |
| G5 | Tidak ada `network-device-va.md` (router/switch/firewall config audit) | idem | Agent tidak bisa audit device jaringan |
| G6 | Tidak ada `vpn-remote-access.md` (VPN, remote access, ZTNA) | idem | Agent tidak tahu remote access VA |
| G7 | Tidak ada `wireless-va.md` (Wi-Fi, 802.11, WPA, rogue AP) | idem | Agent tidak tahu wireless VA |
| G8 | Tidak ada `dns-dhcp-va.md` (DNS, DHCP, poisoning, hijacking) | idem | Agent tidak tahu DNS/DHCP VA |
| G9 | Tidak ada pembahasan TLS deep (cipher, cert, protocol version, HSTS, pinning) | grep "TLS\|cipher\|certificate" di references → 0 hasil | Agent tidak bisa audit TLS mendalam |
| G10 | Tidak ada IPv6 (dual-stack, NDP, RA, IPv6-specific vulns) | grep "IPv6\|NDP" → 0 hasil | Agent melewatkan permukaan IPv6 |
| G11 | Tidak ada IoT/OT (embedded, ICS/SCADA, protokol OT) | grep "IoT\|OT\|ICS\|SCADA" → 0 hasil | Agent tidak bisa VA IoT/OT |
| G12 | Tidak ada NAC/802.1X (port-based access control, bypass) | grep "NAC\|802.1X\|802\.1x" → 0 hasil | Agent tidak tahu NAC assessment |
| G13 | Tidak ada passive topology discovery (ARP, LLDP, CDP, SNMP, passive sniffing) | grep "passive\|topology\|LLDP\|CDP\|SNMP" → 0 hasil | Agent hanya tahu active scan |
| G14 | Tidak ada firewall audit (ruleset review, shadow rules, unused rules) | grep "firewall audit\|ruleset\|shadow rule" → 0 hasil | Agent tidak bisa audit firewall |
| G15 | Capability Map `SKILL.md` tidak punya baris Network VA | baca `SKILL.md` L79-92 | Agent tidak tahu ada referensi network (karena memang belum ada) |
| G16 | Progressive Disclosure `SKILL.md` tidak punya entri network | baca `SKILL.md` L120-133 | idem |
| G17 | Gotchas `SKILL.md` tidak ada network-specific | baca L107-119 | Agent tidak punya peringatan network |

### 2.3 Statistik ringkas

- File referensi saat ini: 9. Target setelah implementasi: 17 (9 existing + 8 baru).
- Baris Network VA saat ini: ~9 (4 di `va-methodology` + 5 di `scanner-config`). Target: ratusan baris terstruktur di 8 file baru + perluasan 4 file.
- Gotchas saat ini: 10 (umum). Target tambahan: ≥ 18 (network-specific).

---

## 3. Definisi (istilah operasional)

| Istilah | Definisi operasional |
|---|---|
| **Network VA** | Proses identifikasi dan pelaporan kerentanan pada infrastruktur jaringan: host, port, service, protokol, konfigurasi device, segmentasi, wireless, VPN, DNS/DHCP, TLS, IPv6, IoT/OT, NAC. Berhenti di identifikasi dan pelaporan — bukan eksploitasi. |
| **Host discovery** | Tahap menemukan host aktif di jaringan (ping sweep, ARP, TCP/UDP probe) sebelum port scan. |
| **Port scan** | Probe port TCP/UDP untuk menentukan state (open/closed/filtered) pada host target. |
| **Service/version detection** | Identifikasi service dan versi yang berjalan pada port terbuka (banner grabbing, probe khusus). |
| **OS fingerprinting** | Inferensi sistem operasi dari perilaku TCP/IP stack. |
| **Credentialed network scan** | Scan jaringan dengan kredensial host (SSH/WinRM) untuk akurasi patch dan konfigurasi; berbeda dari unauthenticated network scan. |
| **Passive discovery** | Penemuan aset/topologi tanpa mengirim probe aktif (sniffing, ARP cache, LLDP/CDP, SNMP polling, DNS zone). |
| **Topology discovery** | Pemetaan struktur jaringan (subnet, VLAN, router, firewall, link) untuk menentukan reachability dan blind spot. |
| **Segmentation audit** | Verifikasi bahwa kontrol segmentasi (VLAN, firewall zone, ACL) benar-benar membatasi traffic sesuai desain. |
| **Network device VA** | Audit konfigurasi router/switch/firewall/load balancer (hardening, default creds, management plane, firmware). |
| **Protocol VA** | Assessment keamanan protokol spesifik (SMB, RDP, SSH, TLS, DNS, DHCP) termasuk versi, cipher, konfigurasi, dan misconfig. |
| **TLS deep assessment** | Analisis mendalam TLS: versi protokol, cipher suite, sertifikat (chain, expiry, key size, SAN), HSTS, OCSP stapling, pinning. |
| **Wireless VA** | Assessment keamanan jaringan nirkabel (802.11): enkripsi (WEP/WPA/WPA2/WPA3), rogue AP, evil twin, WPS, client isolation. |
| **VPN/remote access VA** | Assessment VPN dan akses jarak jauh (IPsec, SSL VPN, WireGuard, ZTNA, MFA, split tunneling). |
| **DNS/DHCP VA** | Assessment layanan DNS dan DHCP: poisoning, hijacking, zone transfer, dynamic update, rogue DHCP. |
| **IPv6 VA** | Assessment permukaan IPv6: dual-stack, NDP, RA, tunneling, IPv6-only services yang terlupakan. |
| **IoT/OT VA** | Assessment perangkat embedded (IoT) dan sistem kontrol industri (OT/ICS/SCADA) dengan batasan keselamatan. |
| **NAC/802.1X VA** | Assessment Network Access Control dan port-based authentication (802.1X, MAB, bypass). |
| **Firewall audit** | Review ruleset firewall: shadow rules, unused rules, overly permissive rules, urutan, logging. |
| **Blind spot** | Segmen/aset yang tidak bisa dijangkau scanner; didokumentasikan sebagai temuan. |

---

## 4. Ruang lingkup

### Termasuk

- Network layer L2–L7: host discovery, port scan, service detection, OS fingerprinting, vulnerability scan.
- Protokol jaringan: SMB, RDP, SSH, TLS, DNS, DHCP, SNMP, NTP, LDAP, Kerberos (aspek VA).
- Segmentasi dan firewall: VLAN, zone, ACL, ruleset audit, micro-segmentation.
- Network device: router, switch, firewall, load balancer, WLC, proxy.
- Wireless: 802.11 a/b/g/n/ac/ax, WPA/WPA2/WPA3, rogue AP, evil twin (deteksi).
- VPN dan remote access: IPsec, SSL VPN, WireGuard, ZTNA, MFA, split tunnel.
- TLS deep assessment.
- IPv6.
- IoT/OT (dengan batasan keselamatan — lihat LI).
- NAC/802.1X.
- Passive topology discovery.
- Pelaporan network-specific: topology, segment, device, protokol, blind spot.

### Tidak termasuk

- Eksploitasi dan pengambilalihan sistem (gunakan `ptes-standard` / `offsec-pen-300`).
- Web application VA mendalam (gunakan `web-app-scan`); Network VA hanya menyentuh service web pada level port/protokol.
- Cloud VA mendalam (AWS/Azure/GCP audit) — sudah ada di `va-methodology`; Network VA fokus on-prem/network.
- Audit kepatuhan/GRC penuh (gunakan `security-auditor`).
- Threat modeling (gunakan `threat-modeling`).
- Wireless exploitation aktif (hanya assessment konfigurasi dan deteksi rogue AP; bukan deauth/evil twin exploitation).
- Manipulasi sistem OT keselamatan-kritis (hanya observasi pasif dan inventaris).
- Implementasi file reference (dokumen ini hanya analisis).

---

## 5. Kebutuhan fungsional

| ID | Kebutuhan | Prioritas | Kriteria lulus |
|---|---|---|---|
| FR-1 | Skill memuat metodologi Network VA end-to-end: host discovery → port scan → service detection → vuln scan → triase → scoring → pelaporan, dengan urutan dan keputusan eksplisit | Wajib | `network-scanning.md` ada dan memuat pipeline lengkap dengan keputusan (kapan pakai SYN vs connect, kapan scan semua port) |
| FR-2 | Tersedia referensi kerentanan jaringan umum (weak protocols, default creds, legacy services, misconfig) dengan cara verifikasi | Wajib | `network-vulnerabilities.md` ada, ≥ 15 entri dengan verifikasi |
| FR-3 | Tersedia referensi audit segmentasi (VLAN, firewall zone, ACL, micro-segmentation) dengan cara verifikasi efektivitas | Wajib | `network-segmentation.md` ada |
| FR-4 | Tersedia referensi protocol VA untuk SMB, RDP, SSH, TLS (versi, cipher, konfigurasi, misconfig, cara verifikasi) | Wajib | `network-protocol-va.md` ada, mencakup 4 protokol minimum |
| FR-5 | Tersedia referensi network device VA (router/switch/firewall/LB/WLC) dengan hardening checklist dan cara verifikasi | Wajib | `network-device-va.md` ada |
| FR-6 | Tersedia referensi VPN dan remote access VA (IPsec, SSL VPN, WireGuard, ZTNA, MFA, split tunnel) | Sebaiknya | `vpn-remote-access.md` ada |
| FR-7 | Tersedia referensi wireless VA (802.11, WPA2/WPA3, rogue AP, client isolation, WPS) | Sebaiknya | `wireless-va.md` ada |
| FR-8 | Tersedia referensi DNS/DHCP VA (poisoning, hijacking, zone transfer, rogue DHCP, dynamic update) | Sebaiknya | `dns-dhcp-va.md` ada |
| FR-9 | TLS deep assessment tercakup (versi, cipher, cert chain/expiry/key size/SAN, HSTS, OCSP stapling) — bisa di `network-protocol-va.md` atau file tersendiri; putuskan di D-1 | Wajib | ada bagian TLS deep dengan checklist verifikasi |
| FR-10 | IPv6 tercakup (dual-stack, NDP, RA, tunneling, IPv6-only services) | Sebaiknya | ada bagian IPv6 di salah satu file (putuskan D-2) |
| FR-11 | IoT/OT tercakup dengan batasan keselamatan (hanya observasi pasif + inventaris) | Sebaiknya | ada bagian IoT/OT |
| FR-12 | NAC/802.1X tercakup (port-based auth, MAB, bypass assessment) | Sebaiknya | ada bagian NAC |
| FR-13 | Passive topology discovery tercakup (ARP, LLDP, CDP, SNMP, sniffing) sebagai alternatif/pelengkap active scan | Wajib | ada bagian passive discovery |
| FR-14 | Firewall audit tercakup (ruleset review, shadow/unused/overly-permissive rules, urutan, logging) | Wajib | ada bagian firewall audit |
| FR-15 | `SKILL.md` diperbarui: Capability Map, Reference Documentation, Progressive Disclosure memuat semua file baru; Gotchas ditambah network-specific (minimal 18 baru) | Wajib | paritas 1:1 antara file di `references/` dan tabel Reference Documentation |
| FR-16 | `va-methodology.md` diperluas: Network VA bukan lagi 4 baris; memuat sub-fase network-specific dan referensi ke file baru | Wajib | bagian Network VA ≥ 30 baris dengan tautan |
| FR-17 | `asset-discovery.md` diperluas: network discovery mendalam (active + passive, IPv6, wireless, IoT/OT) | Sebaiknya | ada bagian network discovery |
| FR-18 | `scanner-config.md` diperluas: konfigurasi per-protokol dan per-device (SMB/RDP/SSH/TLS, IoT, OT, rate limit untuk IPS) | Sebaiknya | ada bagian per-protokol |
| FR-19 | `reporting.md` diperluas: bagian network-specific (topology, segment, device, protokol, blind spot) | Sebaiknya | ada template network section |
| FR-20 | Setiap file baru memiliki frontmatter YAML (`name`, `description`, `tags`) sesuai konvensi repo | Wajib | pemeriksaan frontmatter |
| FR-21 | Persona contract dan decision frame `SKILL.md` tidak berubah arah (tetap VA, bukan pentest) — Network VA berhenti di identifikasi/pelaporan | Wajib | review manual |
| FR-22 | Tidak ada materi ujian (passing score, bobot, poin, waktu ujian, katalog sertifikasi, vendor latihan soal, tautan ujian) di file baru | Wajib | grep pola §2 `PERSONA-INJECTION-NEEDS.md` = 0 hasil termasuk URL |

---

## 6. Kebutuhan non-fungsional

| ID | Kebutuhan | Ukuran |
|---|---|---|
| NFR-1 | Bahasa Indonesia + istilah teknis Inggris; kode dan komentar berbahasa Inggris | review manual |
| NFR-2 | Setiap berkas `references/` muncul tepat sekali di Reference Documentation `SKILL.md`; tidak ada berkas yatim | paritas 1:1 (grep) |
| NFR-3 | Skill berdiri sendiri saat dipasang (tanpa ketergantungan `docs/`) | review manual |
| NFR-4 | `SKILL.md` tetap 120–200 baris (batas keras 450); kelebihan materi di `references/` | hitung baris |
| NFR-5 | Setiap file referensi fokus pada satu domain (satu topik per file), sesuai konvensi repo | review manual |
| NFR-6 | Setiap file diakhiri "Best Practices" section (konvensi repo) | review manual |
| NFR-7 | Konsisten dengan persona existing (suara, batas klaim, struktur jawaban ringkas→alasan→langkah→bukti→risiko) | review manual |
| NFR-8 | Tidak mengubah frontmatter skill yang merusak discovery (`name`/`description` tetap) | diff review |
| NFR-9 | Setiap penghapusan/penambahan berkas tercatat di `CHANGELOG.md` | `check-changelog.js` |
| NFR-10 | Perubahan bisa diverifikasi oleh mesin: grep, hitung baris, resolusi tautan, paritas tabel | skrip |

---

## 7. Keterbatasan yang diterima

| ID | Keterbatasan | Mengapa diterima |
|---|---|---|
| LI-1 | IoT/OT hanya observasi pasif + inventaris; tidak ada instruksi manipulasi sistem keselamatan-kritis | keselamatan fisik; VA tidak boleh mengganggu OT |
| LI-2 | Wireless exploitation aktif (deauth, evil twin exploitation) tidak dicakup; hanya assessment konfigurasi dan deteksi rogue AP | batas persona VA (bukan pentest) |
| LI-3 | IPv6 mungkin digabung ke file existing (bukan file tersendiri) jika volume kecil | menghindari file yatim; putuskan D-2 |
| LI-4 | TLS deep mungkin digabung ke `network-protocol-va.md` (bukan file tersendiri) | volume dan fokus; putuskan D-1 |
| LI-5 | Tidak ada tool/vendor lock-in: sebut tool sebagai contoh, bukan wajib | skill bersifat metodologi, bukan manual tool |
| LI-6 | Tidak ada jaminan akurasi CVE spesifik; selalu verifikasi dengan vendor advisory/NVD | batas klaim persona |
| LI-7 | Tidak menambah dependensi runtime baru (Node bawaan) | NFR repo |
| LI-8 | Implementasi file reference tidak dilakukan dalam dokumen ini; hanya analisis | scope dokumen ini |

---

## 8. Rekomendasi struktur file

### 8.1 File baru (8)

| File | Isi utama | Topik brainstorming yang dicakup |
|---|---|---|
| `references/network-scanning.md` | Metodologi scanning jaringan: host discovery, port scan TCP/UDP, SYN vs connect, service/version detection, OS fingerprinting, timing, evasion, segment traversal, passive discovery | network scanning methodology, topology passive discovery |
| `references/network-vulnerabilities.md` | Katalog kerentanan jaringan umum (weak protocols, default creds, legacy services, misconfig) + verifikasi | common network vulns |
| `references/network-segmentation.md` | Segmentasi: VLAN, firewall zones, ACL, micro-segmentation, audit efektivitas, firewall audit | segmentation, firewall audit |
| `references/network-protocol-va.md` | Protocol VA: SMB, RDP, SSH, TLS deep, DNS, DHCP, SNMP, NTP, LDAP, Kerberos | protocol VA, TLS deep, DNS/DHCP |
| `references/network-device-va.md` | Network device VA: router/switch/firewall/LB/WLC/proxy hardening checklist | network device VA |
| `references/vpn-remote-access.md` | VPN & remote access: IPsec, SSL VPN, WireGuard, ZTNA, MFA, split tunnel, assessment | VPN/remote access |
| `references/wireless-va.md` | Wireless VA: 802.11, WPA2/WPA3, rogue AP, evil twin (deteksi), client isolation, WPS | wireless |
| `references/dns-dhcp-va.md` | DNS/DHCP VA: poisoning, hijacking, zone transfer, rogue DHCP, dynamic update | DNS/DHCP |

Catatan: IPv6, IoT/OT, NAC/802.1X, TLS deep, passive topology, firewall audit dapat menjadi bagian dari file di atas (lihat D-1, D-2, D-3) atau file tambahan jika volume cukup. Brainstorming awal menyebut 8 file baru; 14 topik dipetakan ke 8 file + perluasan 4 file existing.

### 8.2 File existing yang diperluas (4)

| File | Perluasan |
|---|---|
| `references/va-methodology.md` | Bagian "### Network VA" diperluas dari 4 baris menjadi sub-fase network-specific (discovery, scanning, protocol, segmentation, device, wireless, VPN, DNS/DHCP, TLS, IPv6, IoT/OT, NAC, passive, firewall) dengan tautan ke file baru |
| `references/asset-discovery.md` | Tambah bagian network discovery mendalam (active + passive, IPv6, wireless, IoT/OT, segment tidak reachable, blind spot) |
| `references/scanner-config.md` | Tambah konfigurasi per-protokol dan per-device (SMB/RDP/SSH/TLS, IoT, OT, rate limit untuk IPS, IPv6) |
| `references/reporting.md` | Tambah bagian network-specific: topology, segment, device, protokol, blind spot, TLS findings |

### 8.3 File yang juga diperbarui (bukan "diperluas" konten besar)

| File | Perubahan |
|---|---|
| `SKILL.md` | Capability Map + Reference Documentation + Progressive Disclosure + Gotchas (network-specific) |

---

## 9. Gotchas tambahan (daftar bernomor)

Gotchas network-specific yang harus ditambahkan (di `SKILL.md` atau di file referensi terkait; minimal 18):

1. **Firewall/IPS memblokir scan.** Scan intensif bisa di-drop; hasil tidak lengkap. Kurangi rate, jangan tingkatkan agresivitas; dokumentasikan segmen yang tidak bisa dijangkau.
2. **IPS/IDS mendeteksi scan sebagai serangan.** Koordinasi dengan SOC sebelum scan; gunakan window waktu dan whitelist IP scanner.
3. **Segment yang tidak reachable.** VLAN, VPN, dan firewall membatasi jangkauan scanner. Dokumentasikan blind spot — itu temuan.
4. **IPv6 terlupakan.** Dual-stack host punya permukaan IPv6 yang tidak discan jika hanya IPv4. Scan kedua stack.
5. **Service detection salah karena backported patch.** Versi lama bisa aman. Verifikasi dengan vendor advisory sebelum melaporkan CVE.
6. **Banner grabbing gagal pada service di port non-standar.** Jangan asumsi port = service; verifikasi dengan probe.
7. **UDP scan lambat dan tidak andal.** UDP stateless; banyak false negative. Gunakan `nmap -sU` dengan timing tepat dan verifikasi manual.
8. **OS fingerprinting tidak akurat pada VM/container.** Virtualisasi mengaburkan fingerprint. Laporkan sebagai "tidak terverifikasi" jika ragu.
9. **Credentialed scan memerlukan akun dengan hak tepat.** Terlalu rendah melewatkan patch; terlalu tinggi berisiko. Gunakan akun dedicated minimal.
10. **TLS cipher lemah masih dipakai untuk kompatibilitas.** Jangan hanya cek versi protokol; audit cipher suite dan key exchange.
11. **Sertifikat kadaluarsa / self-signed / chain tidak lengkap.** Audit chain, SAN, expiry, key size (≥ 2048 RSA / ≥ 256 ECDSA).
12. **SMB v1 masih aktif.** SMBv1 rentan (EternalBlue). Verifikasi versi minimum yang diizinkan.
13. **RDP tanpa NLA dan tanpa MFA.** NLA wajib; MFA untuk internet-facing. Cek port RDP yang terekspos.
14. **SSH dengan algoritma lemah / password auth.** Audit cipher, MAC, KEX, dan disable password auth.
15. **DNS zone transfer terbuka.** AXFR/IXFR tanpa pembatasan membocorkan topologi. Verifikasi.
16. **Rogue DHCP server.** DHCP starvation/rogue server bisa redirect traffic. Deteksi dengan passive monitoring.
17. **Wireless WPS aktif.** WPS PIN brute-force. Disable WPS.
18. **IoT/OT tidak bisa di-scan aktif.** Perangkat embedded rapuh; gunakan passive discovery dan inventaris; jangan scan aktif tanpa izin eksplisit dan window.
19. **NAC bypass via MAC spoofing / VLAN hopping.** NAC bukan silver bullet; uji bypass secara pasif/observasi.
20. **Firewall ruleset memiliki shadow/unused rules.** Review berkala; hapus yang tidak terpakai; verifikasi urutan.
21. **VPN split tunneling bocor.** Audit konfigurasi split tunnel dan DNS leak.
22. **Rate limiting membuat scan tidak lengkap.** Dokumentasikan yang terlewat, jangan paksa.

---

## 10. Kriteria penerimaan

Dinyatakan selesai bila seluruh butir berikut terbukti:

| ID | Kriteria | Cara verifikasi |
|---|---|---|
| AC-1 | 8 file baru ada di `references/` dengan frontmatter valid (`name`, `description`, `tags`) | `ls` + cek frontmatter |
| AC-2 | 4 file existing diperluas sesuai §8.2 (Network VA bagian ≥ 30 baris, network discovery, per-protokol config, network reporting) | hitung baris / grep |
| AC-3 | `SKILL.md` Capability Map, Reference Documentation, Progressive Disclosure memuat semua 17 file (paritas 1:1) | grep + hitung |
| AC-4 | `SKILL.md` Gotchas memuat ≥ 10 gotchas network-specific (target 18) | hitung |
| AC-5 | Tidak ada materi ujian di file baru (grep pola §2 `PERSONA-INJECTION-NEEDS.md` = 0 hasil termasuk URL) | grep |
| AC-6 | Tidak ada berkas referensi yatim (setiap file di `references/` muncul di Reference Documentation) | paritas 1:1 |
| AC-7 | `SKILL.md` ≤ 450 baris (target 120–200) | `wc -l` |
| AC-8 | Setiap file referensi diakhiri "Best Practices" | grep |
| AC-9 | Frontmatter `SKILL.md` tidak berubah `name`/`description` (discovery tetap) | diff |
| AC-10 | Semua tautan relatif di `SKILL.md` dan file baru resolve | resolusi tautan |
| AC-11 | Persona contract & decision frame tetap VA (bukan pentest) | review manual |
| AC-12 | `CHANGELOG.md` mencatat semua file baru/perluasan | `check-changelog.js` |
| AC-13 | `check-fact-notes.js` lulus (jika menyentuh exam facts; di sini tidak) | jalankan skrip |
| AC-14 | Network VA coverage: 14 topik brainstorming tercakup (network scanning, common vulns, segmentation, wireless, VPN, device, DNS/DHCP, protocol, topology passive, firewall, TLS deep, IPv6, IoT/OT, NAC) | mapping review |

---

## 11. Risiko dan antipattern

### 11.1 Risiko

| Risiko | Dampak | Mitigasi |
|---|---|---|
| File baru terlalu panjang → `SKILL.md` melampaui batas | melanggar NFR-4 | pindahkan detail ke `references/`; `SKILL.md` hanya indeks |
| Overlap antar file baru (mis. TLS di protocol + segmentation) | duplikasi, bingung | tentukan satu owner per topik; cross-reference, bukan salin |
| Persona bergeser ke pentest karena konten network scanning | melanggar batas persona | tekankan "berhenti di identifikasi/pelaporan"; tambah gotcha |
| Materi ujian tidak sengaja masuk (mis. sertifikasi network) | melanggar FR-22 | grep pola §2 sebelum commit |
| Implementasi melebihi scope (menulis reference sekarang) | melanggar LI-8 | dokumen ini hanya analisis; implementasi terpisah |
| File yatim (tidak masuk `SKILL.md`) | melanggar NFR-2 | paritas 1:1 wajib |
| IPv6/IoT/OT/NAC/TLS tidak tercakup karena "nanti" | AC-14 gagal | masukkan ke file yang ada sejak awal (LI-3/LI-4) |

### 11.2 Antipattern

| ID | Antipattern | Mengapa salah |
|---|---|---|
| AP-1 | Menulis file reference sekarang (implementasi sebelum analisis disetujui) | melanggar tujuan dokumen ini |
| AP-2 | Menyalin silabus sertifikasi network (mis. CEH/OSCP network module) sebagai Capability Map | itu blueprint ujian dengan nama lain (AP-7 dokumen persona) |
| AP-3 | Mengganti "exam" menjadi "assessment" tanpa mengubah isi | pola tetap lolos secara semantik |
| AP-4 | Menambah tool/vendor lock-in (mis. "harus pakai Nessus") | skill metodologi, bukan manual tool |
| AP-5 | Menghapus pengetahuan teknis agar "ringkas" | menukar satu penyakit dengan penyakit lain (AP-1 dokumen persona) |
| AP-6 | Membuat file tersendiri untuk topik kecil (IPv6, NAC) tanpa volume cukup | file yatim / over-engineering |
| AP-7 | Tidak memperbarui `SKILL.md` (capability map, progressive disclosure) | agent tidak tahu file baru ada |
| AP-8 | Memasukkan eksploitasi dalam Network VA | melanggar batas persona VA |

---

## 12. Prosedur implementasi (langkah bernomor)

1. Review dan setujui dokumen ini (`docs/VA-NETWORK-NEEDS.md`).
2. Putuskan keputusan D-1..D-7 (§13).
3. Buat 8 file baru di `skills/vulnerability-assessment/references/` dengan frontmatter valid, isi per §8.1, akhiri "Best Practices".
4. Perluas 4 file existing per §8.2.
5. Perbarui `SKILL.md`: Capability Map, Reference Documentation, Progressive Disclosure, Gotchas (network-specific).
6. Jalankan verifikasi: paritas 1:1, hitung baris `SKILL.md`, grep materi ujian (0 hasil), resolusi tautan, frontmatter.
7. Catat semua perubahan di `CHANGELOG.md`.
8. Jalankan `node scripts/check-changelog.js` dan `node scripts/check-fact-notes.js`.
9. Jalankan `node scripts/sync-skills.js` jika frontmatter `SKILL.md` berubah.
10. Review manual persona (contract & decision frame tetap VA).
11. Commit di branch (bukan `main`) per `AGENTS.md`.

---

## 13. Keputusan yang dibutuhkan

| ID | Keputusan | Pilihan | Dampak bila ditunda |
|---|---|---|---|
| D-1 | Apakah TLS deep jadi file tersendiri atau bagian dari `network-protocol-va.md`? | bagian (disarankan) / file tersendiri | volume & fokus; jika tersendiri tambah 1 file |
| D-2 | Apakah IPv6, IoT/OT, NAC jadi file tersendiri atau bagian dari file existing? | bagian (disarankan) / file tersendiri | menghindari file yatim |
| D-3 | Apakah passive topology discovery & firewall audit jadi file tersendiri atau bagian dari `network-scanning.md`/`network-segmentation.md`? | bagian (disarankan) / file tersendiri | idem |
| D-4 | Apakah `wireless-va.md`, `vpn-remote-access.md`, dan `dns-dhcp-va.md` tetap 3 file terpisah (sesuai brainstorming) atau digabung? | terpisah (disarankan, sesuai 8 file) / gabung | jumlah file & indeks |
| D-5 | Apakah gotchas network-specific (18+) ditaruh di `SKILL.md` atau di file referensi terkait? | `SKILL.md` (global) + referensi (detail) (disarankan) | konsistensi dengan pola existing (10 gotchas di `SKILL.md`) |
| D-6 | Prioritas implementasi: semua 8 file sekaligus atau bertahap (Wajib dulu, Sebaiknya belakangan)? | semua sekaligus (disarankan) / bertahap | waktu & cakupan AC-14 |
| D-7 | Apakah perlu update `referensi.md` dengan sumber network-specific (Nmap docs, TLS guides, dll.)? | ya (disarankan) / tidak | kelengkapan sumber |

---

## 14. Metrik

| Metrik | Kondisi awal (2026-11-14) | Target |
|---|---|---|
| File referensi skill | 9 | 17 |
| Baris Network VA (`va-methodology` + `scanner-config`) | ~9 | ≥ 60 (di file dedicated) |
| Topik brainstorming tercakup (14) | 3 (network scan, segment, scanner) | 14 |
| Gotchas network-specific | 0 | ≥ 18 |
| Paritas file vs Reference Documentation | 9/9 | 17/17 |
| Materi ujian (grep pola) | 0 | 0 |
| `SKILL.md` baris | 136 | 120–200 (≤ 450) |

---

Selesai. Dokumen ini hanya analisis kebutuhan; implementasi file reference belum dilakukan.
