---
name: "TLS & PKI"
description: "TLS protocol versions and cipher suites, X.509 certificate types and lifecycle, PKI components, mutual TLS, legacy certificate pinning, Certificate Transparency, TLS inspection tradeoffs, Mozilla SSL configuration, HSTS, OCSP stapling, and hardening best practices."
tags: [tls, pki, x509, cipher-suites, mtls, certificate-pinning, certificate-transparency, ocsp-stapling, hsts, mozilla-ssl-config, hardening, acme, ocsp, caa]
---

# TLS & PKI

TLS (Transport Layer Security) provides confidentiality, integrity, and authenticity for data in transit. PKI (Public Key Infrastructure) is the system of CAs, certificates, and validation rules that lets endpoints trust each other's public keys.

## TLS Versions

| Version | Status | RFC | Notes |
|---------|--------|-----|-------|
| SSL 2.0 / 3.0 | Broken / removed | — | Do not enable; POODLE, etc. |
| TLS 1.0 | Deprecated (RFC 8996) | RFC 2246 | Disable |
| TLS 1.1 | Deprecated (RFC 8996) | RFC 4346 | Disable |
| TLS 1.2 | Allowed with strong ciphers | RFC 5246 | Still widely used |
| TLS 1.3 | Recommended | RFC 8446 | 1-RTT, mandatory forward secrecy |

TLS 1.3 removes RSA key transport, CBC mode, RC4, 3DES, compression, renegotiation, and SHA-1 in signatures. It mandates AEAD cipher suites and ephemeral key exchange (forward secrecy). The handshake is encrypted except for a few fields (SNI unless ECH is used). Downgrade protection is built in via `supported_versions`. TLS 1.3 supports 0-RTT early data, which is replayable and must not carry state-changing requests.

## TLS 1.3 Cipher Suites

TLS 1.3 decouples key exchange and authentication from the cipher suite; the suite specifies only the AEAD and hash.

| Cipher Suite | AEAD | Hash |
|---|---|---|
| `TLS_AES_128_GCM_SHA256` | AES-128-GCM | SHA-256 |
| `TLS_AES_256_GCM_SHA384` | AES-256-GCM | SHA-384 |
| `TLS_CHACHA20_POLY1305_SHA256` | ChaCha20-Poly1305 | SHA-256 |

Key exchange uses named groups (`X25519`, `secp256r1`, `secp384r1`, `X448`); authentication uses ECDSA, RSA-PSS, or Ed25519. TLS 1.3 is the only version permitted for QUIC.

## TLS 1.2 Cipher Suite Selection

In TLS 1.2 the suite bundles key exchange, authentication, bulk cipher, and MAC. Prefer ECDHE/DHE with AEAD; avoid CBC, static RSA, export, anon, NULL, and 3DES/RC4.

Recommended OpenSSL cipher string (Mozilla intermediate profile):

```text
ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
```

Minimum key sizes: RSA 2048 (3072 preferred), DH 2048, ECDSA P-256 or stronger. Disable TLS compression (CRIME) and session renegotiation.

## Certificate Types

| Type | Validation | Use |
|------|-----------|-----|
| DV (Domain Validated) | Domain control only | General web, automation |
| OV (Organization Validated) | Org identity verified | Business sites |
| EV (Extended Validation) | Rigorous org vetting | High-assurance (UI indicator largely removed by browsers) |
| Wildcard (`*.example.com`) | DV/OV | Many subdomains, one cert |
| SAN / multi-domain | Listed SANs | Multiple distinct hostnames |
| Code signing | Publisher identity | Software/binaries |
| Client authentication | Identity of user/service | mTLS, device auth |
| S/MIME | Email identity | Encrypted/signed email |
| Root / intermediate CA | CA identity | Issuing other certs |
| Short-lived | Same as DV/OV | Frequent rotation, reduced revocation reliance |

Publicly trusted certificates are capped at 398 days validity (CA/Browser Forum). Internal/private PKI can set its own lifetimes but should follow similar discipline. Let's Encrypt issues DV certs with 90-day lifetimes to encourage automation.

## Certificate Lifecycle

1. **Key generation** — generate private key (RSA 2048+/ECDSA P-256) in an HSM or secure keystore; never transmit the private key.
2. **CSR** — create a Certificate Signing Request with the public key and subject/SANs.
3. **Issuance** — CA validates (DV via ACME HTTP-01/DNS-01/TLS-ALPN-01; OV/EV via manual checks) and issues.
4. **Deployment** — install cert + intermediate chain; verify chain and hostname.
5. **Renewal/rotation** — automate with ACME before expiry; overlap deploys to avoid downtime.
6. **Revocation & monitoring** — revoke on compromise; alert at 30/14/7 days before expiry.

## PKI Components

- **End entity (leaf)** — the server/client certificate.
- **RA / CA** — RA validates identity; CA (offline root + online intermediates) issues certs.
- **CRL / CDP** and **OCSP responder** — revocation publication and online status.
- **Trust store** — OS/browser root anchors; **HSM** protects CA keys.
- **Enrollment protocols** — ACME, SCEP, EST (RFC 7030), CMP (RFC 4210); **AIA** fetches issuer/OCSP URLs.

Path validation (RFC 5280) builds the chain leaf→trust anchor, checking signatures, validity, name constraints, EKU, key usage, and revocation. Cross-signed intermediates ease root transitions.

## Mutual TLS (mTLS)

In mTLS both peers present certificates. The server requests a client cert, validates its chain and hostname/identity, and maps it to an authorization decision (often via a SAN URI such as a SPIFFE ID `spiffe://trust-domain/workload`).

Use cases: service meshes (Istio/Linkerd), API gateways, zero-trust east-west traffic, device authentication, B2B integrations.

nginx mTLS example:

```nginx
server {
    listen 443 ssl;
    ssl_certificate     /etc/nginx/server.crt;
    ssl_certificate_key /etc/nginx/server.key;
    ssl_client_certificate /etc/nginx/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;
}
```

Operational challenges: provisioning/rotating client certs at scale, distributing trust bundles, revocation propagation, and clock skew. SPIFFE/SPIRE automates workload identity and short-lived certs.

## Certificate Pinning (Legacy)

HTTP Public Key Pinning (HPKP, RFC 7469) let sites pin expected public-key hashes via the `Public-Key-Pins` header. It is **deprecated and removed** from browsers because misconfiguration could permanently brick access (no recovery if keys lost). Mobile apps still sometimes pin, but it is discouraged.

Legacy HPKP header (do not use in new designs):

```http
Public-Key-Pins: pin-sha256="base64=="; pin-sha256="backup=="; max-age=5184000; includeSubDomains
```

Modern alternatives: CAA DNS records, CT monitoring, short-lived certs with automated renewal, and ACME. If pinning in mobile, include at least one backup pin and a remote kill switch.

## Certificate Transparency (CT)

CT (RFC 6962 / 9162) is an append-only, cryptographically verifiable log of issued certificates. CAs submit certs and return Signed Certificate Timestamps (SCTs); browsers require SCTs for publicly trusted certs. Monitors and auditors detect misissuance and unauthorized certs for your domains.

Operational steps:

- Ensure your CA logs certificates (most public CAs do).
- Monitor CT logs for unexpected issuance (e.g., crt.sh).
- Publish CAA records to restrict issuance (example above).

## TLS Inspection Tradeoffs

TLS inspection (SSL/TLS decryption) has a middlebox terminate TLS, inspect plaintext, and re-encrypt.

Pros: malware/phishing detection, DLP, compliance visibility. Cons: privacy and legal concerns, latency and failure points, breakage of pinning, app incompatibility, and key-management risk (the inspection CA key is high-value). TLS 1.3 makes passive inspection impossible; active MITM needs a proxy supporting TLS 1.3, and ECH/SNI encryption complicates hostname policy.

Best practice: prefer endpoint security and ZTNA; where inspection is required, use selective decryption with a bypass list for pinned apps (banking, healthcare, identity providers), and monitor TLS errors.

## Hardening Configs (Mozilla SSL Configuration)

Mozilla's SSL Configuration Generator provides three profiles: **Modern** (TLS 1.3 only), **Intermediate** (TLS 1.2+ with strong suites), and **Old** (legacy compatibility). Prefer Modern for new services, Intermediate for broad compatibility.

nginx (Intermediate profile):

```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

Apache (Intermediate profile):

```apache
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder off
SSLSessionTickets off
```

Disable session tickets or rotate ticket keys; enable OCSP stapling; keep the intermediate in the served chain.

## HSTS

HTTP Strict Transport Security (RFC 6797) tells browsers to always use HTTPS for a host.

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

- `max-age` in seconds (at least 1 year / 31536000 for preload).
- `includeSubDomains` applies to all subdomains — ensure they all support HTTPS first.
- `preload` opts into the browser preload list (hstspreload.org); submission is effectively permanent, so plan carefully.

HSTS prevents SSL-stripping/downgrade and cookie hijacking. Once deployed, removing it is hard; test on a short max-age first.

## OCSP Stapling

OCSP stapling (RFC 6066 / 6961) has the server fetch and staple a fresh OCSP response into the TLS handshake, so clients need not contact the CA's OCSP responder directly.

Benefits: faster handshakes, better privacy (client IP not leaked to CA), and resilience when the OCSP responder is down.

nginx:

```nginx
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/nginx/chain.pem;
```

Requirements: serve the full chain (leaf + intermediate), configure a resolver, and ensure the server can reach the OCSP responder. OCSP Must-Staple extension forces clients to require a staple; if stapling fails the cert is treated as invalid, so monitor stapling health. Multi-staple (RFC 6961) staples responses for intermediates too.

## Best Practices

- Enforce TLS 1.3 minimum where possible; otherwise TLS 1.2 with AEAD-only suites.
- Automate issuance and renewal with ACME; never let certs expire.
- Use ECDSA P-256 or RSA 2048+ keys; protect private keys in HSMs/keystores.
- Serve the complete chain; verify with `openssl s_client -connect host:443 -showcerts`.
- Enable HSTS with a long max-age and preload after validation.
- Enable OCSP stapling and monitor it; publish CAA records; monitor CT logs.
- Use mTLS for service-to-service and device auth; automate with SPIFFE/SPIRE.
- Maintain a cert inventory with owners and expiry; alert early.

## Gotchas

- 0-RTT early data is replayable; never use for state-changing requests.
- HSTS `includeSubDomains` can break subdomains without HTTPS; preload is nearly irreversible.
- OCSP stapling silently fails if the responder is unreachable or the chain is incomplete.
- Certificate pinning (HPKP) is dead in browsers; do not deploy it for web.
- Wildcard certs do not cover the apex domain.
- Clock skew breaks validation; enforce NTP.
- Self-signed/internal CAs must be distributed to all trust stores; missing intermediates cause errors.
- TLS inspection breaks pinned apps and some APIs; maintain bypass lists.
- Let's Encrypt rate limits can block bulk issuance; revocation is unreliable (soft-fail).

---

*Reference — TLS & PKI (network-security skill).*
