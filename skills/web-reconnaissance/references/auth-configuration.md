---
name: "Konfigurasi Autentikasi: JWT, Cookie, dan OAuth"
description: "Membaca skema autentikasi aplikasi dari recon: JWT dan klaimnya, atribut cookie sesi, alur OAuth2/OIDC dan SAML, rotasi refresh token, CSRF, serta MFA — plus apa yang boleh disimpulkan dan apa yang harus dibuktikan di tahap pengujian."
tags: [authentication, jwt, cookie, oauth, oidc, saml, session, refresh-token, csrf, mfa, webauthn]
---

# Konfigurasi Autentikasi

Recon harus bisa menjawab tiga pertanyaan ini sebelum pengujian dimulai:

1. **Skema apa** yang dipakai — sesi cookie, bearer token, keduanya, atau OIDC?
2. **Di mana** kredensial disimpan, dan siapa yang bisa membacanya?
3. **Bagaimana** ia dikirim, diperbarui, dan diakhiri?

Ketiganya terlihat dari tiga sumber yang sudah Anda kumpulkan: bundle, traffic, dan storage. Dokumen ini menyatukannya — pembacaan storage yang mendetail ada di [browser-storage.md](browser-storage.md).

## 1. Temukan Skemanya

```bash
grep -nE 'Bearer|Authorization|refresh_token|id_token|access_token' main.pretty.js
grep -nE 'response_type=|code_challenge|client_id|redirect_uri|scope=' main.pretty.js
grep -nE '/oauth/|/oidc/|openid-configuration|/saml|/auth/token|/auth/refresh' main.pretty.js
grep -nE 'navigator\.credentials|PublicKeyCredential|totp|otp|mfa' main.pretty.js
```

| Petunjuk | Skema yang mungkin |
|---|---|
| Header `Authorization: Bearer …` | token bearer (JWT atau opaque) |
| Cookie sesi + `credentials: "include"` | sesi berbasis cookie |
| `response_type=code` + `code_challenge` | OAuth2 authorization code + PKCE |
| `response_type=token` atau `id_token` di fragmen | implicit flow (usang, tapi masih ada) |
| `SAMLResponse` + `POST` ke `/saml/consume` | SAML 2.0 |
| `credentials.get()` | WebAuthn / passkey |

Banyak aplikasi memakai **dua** skema sekaligus: cookie untuk halaman, bearer untuk API. Catat keduanya; jangan menyimpulkan salah satu.

## 2. JWT

JWT dikenali dari tiga segmen dipisah titik. Yang direkonstruksi bukan isinya saja, tetapi posisinya dalam alur.

| Yang dicatat | Cara | Kenapa penting |
|---|---|---|
| Lokasi penyimpanan | storage / cookie / memori | menentukan siapa yang bisa membacanya |
| Cara pengiriman | header, cookie, query | query bocor ke log dan `Referer` |
| `alg` | decode header | `none`/`HS256` berbeda risiko dari `RS256` |
| `exp`, `iat` | decode payload | sesi panjang memperbesar jendela penyalahgunaan |
| `iss`, `aud` | decode payload | penerbit dan penerima yang sah |
| `sub`, `role`, `scope` | decode payload | hak yang diklaim, dan apakah hak itu dipercaya klien |
| `kid` | decode header | penanda rotasi kunci |
| Endpoint refresh | interceptor 401 / `/auth/refresh` | titik yang menjaga sesi tetap hidup |

Decode tanpa verifikasi ada di [browser-storage.md](browser-storage.md) §6. Di sini yang penting adalah **pembacaan alur**:

```text
login  → POST /auth/token           → access_token (exp 15m) + refresh_token
request→ Authorization: Bearer …    → 401 bila kedaluwarsa
401    → POST /auth/refresh         → access_token baru (rotasi refresh?)
logout → POST /auth/logout          → refresh dicabut? cookie dihapus?
```

Pertanyaan yang harus terjawab dari traffic, bukan dari tebakan:

- Apakah `refresh_token` disimpan di tempat yang terbaca JS, atau di cookie `HttpOnly`?
- Apakah token berganti setelah refresh (rotasi), atau sama saja (dapat dipakai ulang)?
- Apakah `exp` benar-benar dihormati — ada request yang berhasil dengan token kedaluwarsa?
- Apakah logout mencabut token di server, atau hanya menghapusnya di klien?
- Apakah token yang sama dikirim ke host pihak ketiga?

**Yang tidak bisa disimpulkan dari recon:** apakah tanda tangan diverifikasi server, apakah `alg` dapat ditukar, atau apakah rahasia HMAC lemah. Ketiganya butuh pengujian aktif — dan izin. Jangan menulis "JWT dapat dipalsukan" hanya karena payload terbaca; payload JWT memang selalu terbaca.

## 3. Cookie Sesi

Atribut cookie sudah dibahas di [browser-storage.md](browser-storage.md) §3. Yang ditambahkan di sini adalah perilakunya:

| Perilaku | Cara memeriksa | Arti bila salah |
|---|---|---|
| Rotasi saat login | bandingkan nilai cookie sebelum dan sesudah login | nilai sama = session fixation |
| Pencabutan saat logout | pakai cookie lama setelah logout | masih berlaku = sesi tidak dicabut |
| Cakupan domain | atribut `Domain` | domain induk = terbaca semua subdomain |
| Prefiks | `__Host-`, `__Secure-` | tanpa prefiks, proteksi bergantung pada atribut lain |
| Umur | `Expires`/`Max-Age` | sesi panjang = jendela penyalahgunaan lebar |
| Konkurensi | login di dua perangkat | sesi lama tetap sah atau tidak |

Cookie sesi yang **dapat dibaca JavaScript** (tanpa `HttpOnly`) adalah temuan Medium (CWE-1004) — naikkan hanya bila ada jalur XSS yang terbukti.

## 4. OAuth2 / OIDC

Yang dipetakan: penyedia identitas, alur, dan tujuan token.

```text
GET  auth.target.tld/oauth/authorize?response_type=code&client_id=web
     &redirect_uri=https://app.target.tld/callback&scope=openid profile
     &state=…&code_challenge=…&code_challenge_method=S256
POST auth.target.tld/oauth/token   → access_token, id_token, refresh_token
GET  app.target.tld/callback?code=…
```

| Yang dicatat | Contoh | Kenapa |
|---|---|---|
| IdP | `auth.target.tld`, `login.microsoftonline.com` | pihak ketiga di luar scope pengujian |
| Alur | code + PKCE, implicit, hybrid | implicit membawa token di URL |
| `redirect_uri` | `https://app.target.tld/callback` | hanya dicatat; pengujian allowlist butuh izin |
| `scope` | `openid profile email offline_access` | `offline_access` berarti refresh token ada |
| `state`, `nonce` | ada / tidak | ketiadaannya kandidat CSRF/replay, bukan bukti |
| Penyimpanan token | cookie, memory, storage | token di storage = terbaca XSS |
| Metadata | `/\.well-known/openid-configuration` | issuer, endpoint, algoritma yang didukung |

Metadata OIDC adalah **GET** dan biasanya publik — aman dibaca bila host ada di scope. Bila IdP-nya pihak ketiga, cukup dicatat sebagai konteks.

## 5. SAML

Tanda: form yang auto-submit ke `/saml/consume` atau `/acs`, parameter `SAMLResponse` (base64), `RelayState`.

Yang dicatat: IdP, endpoint ACS, apakah `RelayState` divalidasi (hanya diamati), dan apakah respons dapat dibaca dari browser. Jangan mengubah assertion — itu tindakan aktif di luar recon.

## 6. Sesi vs Token

| Aspek | Sesi cookie | Bearer JWT |
|---|---|---|
| Terbaca JS | hanya bila tanpa `HttpOnly` | selalu, bila disimpan di storage |
| Pencabutan | mudah (hapus sesi server) | sulit tanpa daftar cabut |
| CSRF | relevan | tidak, bila tidak dikirim via cookie |
| XSS | terbatas pada aksi, bukan pencurian | token dapat dicuri utuh |
| Cakupan | satu origin | dapat dipakai lintas host |
| Rotasi | nilai cookie berganti | `exp` pendek + refresh |

Tabel ini menjelaskan mengapa lokasi penyimpanan menentukan severity: token yang tidak dapat dicabut dan dapat dicuri lebih berbahaya daripada cookie sesi yang dapat dicabut.

## 7. CSRF

| Pola | Terlihat dari | Kekuatan |
|---|---|---|
| Token ganda (cookie + header) | header `X-CSRF-Token` di traffic | kuat bila nilainya acak per sesi |
| Token sinkron di form | hidden input di HTML | kuat bila divalidasi server |
| `SameSite=Lax/Strict` saja | atribut cookie | cukup untuk banyak kasus, bukan semua |
| Tidak ada keduanya | cookie sesi tanpa token, `SameSite=None` | kandidat CSRF |

Catat polanya; pembuktian butuh dua sesi dan izin.

## 8. MFA

| Faktor | Petunjuk di bundle | Catatan recon |
|---|---|---|
| TOTP | `totp`, `otpauth`, `QRCode` | enrollment terlihat setelah login |
| SMS/email OTP | endpoint `verify-otp`, timer | catat laju dan masa berlaku dari traffic |
| WebAuthn | `navigator.credentials.create/get`, `PublicKeyCredential` | passkey; MCP menyediakan `configure_webauthn` untuk emulasi — hanya untuk pengujian berizin |
| Push | SDK vendor | pihak ketiga |

Recon cukup mencatat faktor mana yang aktif dan pada langkah mana ia diminta.

## 9. Mesin Keadaan Autentikasi

```text
[anonim]
  │ buka /login
  ▼
[login form] ──POST /auth/token──► [sesi aktif]
  │                                    │ 401 → /auth/refresh → [sesi diperpanjang]
  │                                    │ logout → POST /auth/logout → [anonim]
  ▼                                    ▼
[MFA challenge] ──verify──► [sesi aktif]   [kedaluwarsa] → login ulang
```

Gambar ini yang membuat laporan mudah dibaca; setiap panah harus punya bukti request.

## 10. Dari Observasi ke Prioritas

| Kondisi teramati | Prioritas awal | Butuh bukti tambahan |
|---|---|---|
| Refresh token di `localStorage` | Tinggi | jalur XSS |
| Token dikirim sebagai parameter query | Tinggi | apakah tercatat di log/Referer |
| Token dikirim ke host pihak ketiga | Tinggi | apakah host itu di scope |
| Sesi tidak dicabut saat logout | Sedang | request dengan cookie lama |
| Cookie sesi tanpa `HttpOnly` | Sedang | jalur XSS |
| Cookie sesi tanpa `Secure` | Sedang | apakah HTTP tersedia |
| Session fixation (cookie tidak berubah saat login) | Sedang | dua sesi |
| `SameSite` tidak diset | Rendah–Sedang | apakah ada aksi perubahan state |
| `id_token` dipakai sebagai access token | Sedang | audiens token |
| MFA ada tetapi dapat dilewati | Tinggi | langkah yang melewati |

Semua baris di atas adalah **kandidat** sampai dibuktikan. Istilah "kandidat" bukan kehati-hatian berlebihan: recon melihat konfigurasi, bukan dampak.

## Jebakan

- **Payload JWT selalu terbaca.** Itu desain, bukan kerentanan. Yang menjadi masalah adalah lokasi penyimpanan dan masa berlaku.
- **`alg:none` di header tidak berarti diterima server.** Hanya pengujian aktif yang membuktikan.
- **Cookie yang tidak terlihat di `document.cookie` tetap terkirim.** Periksa header request.
- **Satu aplikasi bisa punya dua skema.** Cookie untuk halaman, bearer untuk API — menguji satu saja memberi kesimpulan setengah.
- **Token di memori tidak terlihat di storage.** Bila storage kosong, periksa header per request.
- **Refresh token di cookie `HttpOnly` adalah pilihan yang baik**, bukan temuan — kecuali ada masalah lain (tidak dirotasi, tidak dicabut).
- **Menguji token pada akun pengguna lain adalah pelanggaran.** Gunakan akun sendiri.
- **Metadata OIDC pihak ketiga di luar scope.** Catat, jangan diuji.

## Best Practices

1. Jawab tiga pertanyaan pembuka sebelum menyentuh endpoint lain — skema auth menentukan seluruh strategi.
2. Simpan potongan traffic login, refresh, dan logout; tiga itu menjelaskan siklus hidup sesi.
3. Catat `exp` dan waktu sesi nyata; selisihnya sering menjadi temuan.
4. Tuliskan apa yang **tidak** dapat disimpulkan dari recon, agar laporan tidak melebihkan bukti.
5. Serahkan tabel prioritas §10 ke `web-app-scan` sebagai hipotesis, bukan sebagai temuan.
