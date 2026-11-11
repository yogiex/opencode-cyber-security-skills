---
name: "SSRF ke Jaringan Internal — Metadata, Admin API, Headless"
description: "Peta sink SSRF, bypass per lapisan, header wajib metadata cloud (AWS IMDSv2, GCP, Azure), rantai ke admin API internal (Kong, Docker, kubelet, Redis), dan headless renderer/CDP beserta bukti dan false positive yang harus dihindari."
tags: [ssrf, metadata, imdsv2, gcp, azure, kong, docker, kubelet, redis, headless, cdp, gopher]
---

# SSRF ke Jaringan Internal — Metadata, Admin API, Headless

SSRF bukan bug filter, melainkan bug **"siapa yang memutuskan host"**. Selama validasi host dan koneksi TCP dilakukan komponen berbeda (parser vs HTTP client), selalu ada ruang TOCTOU: DNS rebinding, redirect, dan parser disagreement.

Nilai SSRF ditentukan tujuannya, bukan status 200-nya. Tujuan bernilai: metadata cloud, admin API internal, dan renderer headless yang punya jalur eksekusi.

## 1. Peta sink

| Sink | API khas | Rantai |
|---|---|---|
| HTTP client keluar | `requests`, `httpx`, OkHttp, `HttpClient`, `axios`, `got`, Go `http.Get` | metadata/internal API → kredensial |
| Image/avatar fetch | `getimagesize`, `ImageIO.read(URL)`, `sharp`, ImageMagick | blind SSRF, port scan |
| PDF/HTML renderer | wkhtmltopdf, Puppeteer/Playwright, Chrome `printToPDF` | fetch internal + eksekusi JS |
| Webhook / unfurl | "test connection", `notify_url`, oEmbed, screenshot | blind SSRF, bukti egress |
| Import URL | CSV/XLSX/RSS/sitemap dari URL | SSRF + XXE bergabung |
| XML parser | JAXP, SAX/StAX, lxml, `simplexml_load_string`, `XmlDocument` | XXE → file read / SSRF |
| Proxy/gateway | parameter `target`/`path`, absolute-form request line | forward proxy pra-auth |
| Worker/queue | URL di message, cron fetch | egress & ACL berbeda dari web |

Pola review: cari **asal URL** (`@RequestParam url`, `params[:url]`, `req.body.url`) lalu telusuri sampai fungsi koneksi. `new URL(userInput)` tanpa cek skema + host + IP hasil resolve adalah kandidat.

## 2. Bypass per lapisan

| Lapisan | Teknik | Contoh | Batas |
|---|---|---|---|
| Blacklist string | IP encoding | `2130706433`, `0x7f000001`, `017700000001`, `127.1`, `0`, `[::ffff:127.0.0.1]` | Java Commons & Node `ip-address` tahan; .NET `IPAddress.TryParse` menerima hex/octal/dword |
| Authority | userinfo, fragment | `https://expected.com@attacker/`, `https://attacker/#expected.com`, `expected.com.attacker` | tergantung parser; uji dua arah |
| Parser disagreement | backslash, `;`, `*` | `http://example.com\@evil.com` (WHATWG → `example.com`; CPython → `evil.com`), Spring `;@evil` | hanya bila string diparse dua kali |
| Encoding | percent/double/unicode | `%31%32%37.0.0.1`, `%2568ttp://`, `＠`, `FILE://` | butuh decode berlapis |
| Redirect | status & protokol | 302→internal, 307 pertahankan method+body, redirect ke `gopher://` | client harus follow; periksa URL final |
| DNS | rebinding, wildcard | TTL 0 → `127.0.0.1` lalu `169.254.169.254`; `127.0.0.1.nip.io` | validasi-lalu-koneksi = TOCTOU |
| Scheme | protokol | `file:///etc/passwd`, `gopher://127.0.0.1:6379/_...`, `dict://`, `ftp://` | `requests` menolak `gopher`/`file`; PHP cURL mengizinkan |
| Method | verb tampering | `GET`→`POST/PUT/PATCH`, `X-HTTP-Method-Override`, body hanya pada 307 | filter sering hanya memeriksa GET |
| Header | Referer, Host, SNI | `Referer: http://169.254.169.254/...`, SNI proxy | butuh fitur yang memanggil URL dari header |
| ACL | egress allowlist | `[fe80::]`, `[fd00:ec2::254]` | ACL sering hanya memblokir IPv4 privat |

## 3. Metadata cloud dan header wajib

| Cloud | Endpoint kredensial | Header / metode wajib | Catatan |
|---|---|---|---|
| AWS IMDSv1 | `169.254.169.254/latest/meta-data/iam/security-credentials/<role>` | – | hanya bila IMDSv1 aktif; hop limit default 1 |
| AWS IMDSv2 | `PUT /latest/api/token` lalu `GET` | `X-aws-ec2-metadata-token-ttl-seconds` (PUT), `X-aws-ec2-metadata-token` (GET) | `PUT` + larangan `X-Forwarded-For`; **SSRF GET-only gagal** |
| AWS IPv6 | `[fd00:ec2::254]` | sama | Nitro + subnet IPv6 |
| GCP | `metadata.google.internal/computeMetadata/v1/` → `/instance/service-accounts/default/token` | `Metadata-Flavor: Google` | tanpa header ditolak → butuh kontrol header |
| Azure | `169.254.169.254/metadata/identity/oauth2/token` | `Metadata: true`, `api-version` wajib, tanpa `X-Forwarded-For` | path per `api-version`: **[UNVERIFIED]** |
| Lain | Alibaba `100.100.100.200`, Tencent `metadata.tencentyun.com` | bervariasi | **[UNVERIFIED]** |

Kredensial berumur pendek: pakai segera, catat scope, redaksi di laporan. AWS → `sts get-caller-identity`; GCP → bearer token ke API; Azure → token ARM.

## 4. Rantai ke layanan internal

| Target | Prasyarat | Batas |
|---|---|---|
| Kong Admin API (`8001`) | listen non-loopback, tanpa auth | default loopback; **[UNVERIFIED]** |
| Docker Engine `2375`/`2376` | daemon `-H tcp://`, tanpa mTLS | default unix socket tidak terjangkau HTTP |
| kubelet `10250` | `anonymous-auth=true` atau token SA | RBAC memblokir exec |
| Redis `6379` via gopher | tanpa password, `CONFIG` tidak di-rename | protected-mode default |
| Consul `8500`, etcd `2379`, Jenkins `/script`, Actuator `/env` | auth lemah | bervariasi |
| Chrome CDP `9222` | port debug terbuka + reachable | default loopback; **[UNVERIFIED]** |

**Docker**: `POST /containers/{id}/exec` lalu `POST /exec/{id}/start` — dua request, bukan satu. **Redis**: `CONFIG SET dir` + `dbfilename` + `SAVE` → webshell/cron/`authorized_keys`; `gopher://` diperlukan untuk RESP mentah. **kubelet**: `GET /pods`, lalu `POST /run/{ns}/{pod}/{container}`.

**Headless renderer**: renderer yang membuka URL/HTML dari user dapat digunakan untuk fetch internal dari konteks container. CDP memberi jalur eksekusi (`/json/version` → WebSocket `Runtime.evaluate`). Batas: CSP hanya mengikat dokumen, bukan renderer; `--disable-javascript`, seccomp, dan egress ACL memutus rantai. Eksfiltrasi: `fetch()`/`<img>`/`sendBeacon` ke host penyerang, atau DNS.

## 5. Bukti

- **Callback OOB**: subdomain unik per uji; simpan log DNS+HTTP (timestamp, request line, IP sumber). Membuktikan egress, **belum** membuktikan akses data.
- **Metadata**: dump JSON dengan kunci diredaksi; lanjut `sts get-caller-identity` sebagai bukti kredensial valid.
- **Layanan internal**: banner/versi, status code, hash body; Redis `INFO`, Docker `/version`.
- **RCE**: output `id`/`hostname` bertimestamp atau callback dari perintah; minimal, tanpa persistensi.
- **Reproduksi**: request/response + skrip yang menjalankan ulang dari nol.

## 6. Jebakan

- Halaman error 200 atau "URL tidak valid" bukan bukti SSRF; tanpa callback atau data terpantul, statusnya dugaan.
- Filter string (`strpos($url,'169.254')`) gugur oleh desimal/hex; allowlist prefix `https://api.example.com` gugur oleh `api.example.com.attacker` atau `@`.
- Validasi host awal tetapi `follow_redirects` aktif = bypass.
- Validasi resolve lalu client resolve ulang = TOCTOU; pin IP hasil resolve.
- ACL hanya IPv4 privat: `::1`, link-local, dan `fd00:ec2::254` lolos.
- Jangan samakan XXE dengan file read: XInclude tetap ada meski DOCTYPE diblokir.
- Default parser tidak universal: libxml2 ≥ 2.9 menonaktifkan entity eksternal, JAXP default permisif.
- Timing blind SSRF mudah disalahartikan; ulangi dan bandingkan baseline.
- Jangan sebut port/path/CVE/versi tanpa verifikasi; tandai **[UNVERIFIED]**.

## 7. Best Practices

- Mulai dari asal URL di source, bukan dari daftar payload.
- Tentukan target bernilai lebih dulu (metadata, admin API, renderer), baru cari sink.
- Uji dengan callback unik; satu uji satu subdomain.
- Periksa URL final setelah redirect, bukan URL awal.
- Simpan bukti egress dan data terpantul secara terpisah.
- Jangan menyerang layanan internal di luar scope hanya karena terjangkau.

## 8. Rujukan

- [ssrf-xxe.md](./ssrf-xxe.md) — tipe SSRF, bypass dasar, XXE in-band/blind/DTD.
- [waf-bypass-payloads.md](./waf-bypass-payloads.md) — bila ada filter/WAF di depan.
- [source-recovery-debugging.md](./source-recovery-debugging.md) — memetakan sink dari artefak.
