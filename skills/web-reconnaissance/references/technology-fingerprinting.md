---
name: "Identifikasi Teknologi dan Versi"
description: "Mengenali teknologi target secara berlapis — infrastruktur, server dan bahasa, framework frontend beserta versinya, serta layanan pihak ketiga — dari header, cookie, jalur aset, banner lisensi di bundle, sertifikat TLS, dan DNS, lengkap dengan kolom keyakinan dan batas yang tidak bisa disimpulkan."
tags: [fingerprinting, technology, headers, cookies, asset-path, version, whatweb, wappalyzer, tls, dns, cdn, waf, confidence]
---

# Identifikasi Teknologi dan Versi

"Pakai apa?" bukan pertanyaan sepele. Teknologi menentukan CVE mana yang relevan, header mana yang wajar, endpoint mana yang seharusnya ada, dan kesalahan mana yang mencurigakan. Tetapi fingerprinting juga paling mudah menghasilkan kesimpulan palsu — `X-Powered-By` bisa dipalsukan, CDN menyembunyikan origin, dan versi library di bundle belum tentu versi yang berjalan.

Karena itu aturannya: **setiap baris inventaris harus punya bukti dan tingkat keyakinan**, bukan tebakan.

## 1. Empat Lapis

| Lapis | Yang dijawab | Sinyal utama |
|---|---|---|
| **Infrastruktur** | CDN, WAF, hosting, cloud | header `Via`, `CF-Ray`, `x-vercel-id`, `x-amz-cf-id`, TLS issuer, CNAME |
| **Server dan bahasa** | nginx/Apache, Node/PHP/Java/.NET/Python | `Server`, `X-Powered-By`, cookie sesi, format `ETag` |
| **Framework frontend** | React, Vue, Angular, Next, Nuxt, Svelte | jalur aset, atribut root, variabel global, banner lisensi |
| **Pihak ketiga** | analytics, auth, pembayaran, error tracking | domain di traffic, cookie `_ga`, `__stripe_*`, SDK |

Jawab berurutan. Lapis 1 menjelaskan mengapa lapis 2 sering kosong (CDN menimpa `Server`), dan lapis 3 hanya bisa dibaca setelah Anda punya HTML atau bundle.

## 2. Header: Bukan Hanya Nilainya, Tapi Bentuknya

```bash
curl -sSI https://target.tld | tee headers.txt
curl -sSI https://target.tld | grep -iE 'server|x-powered-by|via|x-cache|x-vercel|x-amz|cf-ray|x-akamai|x-sucuri|x-fastly|x-nf-'
```

| Header | Arti | Keyakinan |
|---|---|---|
| `Server: nginx/1.24.0` | nginx + versi | tinggi bila tidak ada CDN |
| `X-Powered-By: Express` | Node.js + Express | tinggi |
| `X-Powered-By: PHP/8.2.1` | PHP + versi | tinggi |
| `X-AspNet-Version`, `X-AspNetMvc-Version` | ASP.NET klasik | tinggi |
| `X-Generator: Drupal 10` | Drupal | tinggi |
| `Via: 1.1 varnish` | Varnish cache | tinggi |
| `X-Runtime` | Rails | tinggi |
| `CF-Ray`, `Server: cloudflare` | Cloudflare (CDN + WAF) | tinggi |
| `x-vercel-id`, `x-vercel-cache` | Vercel | tinggi |
| `x-nf-request-id` | Netlify | tinggi |
| `x-amz-cf-id`, `X-Amz-Cf-Pop` | CloudFront | tinggi |
| `X-Akamai-Transformed`, `X-Akamai-Request-ID` | Akamai | tinggi |
| `X-Fastly-Request-ID`, `X-Served-By: cache-...` | Fastly | tinggi |
| `X-Sucuri-ID` | Sucuri | tinggi |
| `X-GitHub-Request-Id` | GitHub Pages | tinggi |
| `X-Azure-Ref` | Azure Front Door / App Service | tinggi |
| `X-Cache: Hit from cloudfront` | CloudFront, cache hit | tinggi |
| `Server-Timing` | framework/aplikasi tertentu | sedang |
| `ETag: W/"..."` | ETag lemah; format `"inode-size-mtime"` khas Apache | sedang |

Yang sering terlewat:

- **Urutan dan kapitalisasi header** bisa menunjukkan siapa yang menambahkan: proxy biasanya menambahkan di akhir.
- **Header duplikat** menandakan dua lapis proxy.
- **`Server` hilang sepenuhnya** bukan berarti tanpa server — banyak CDN menghapusnya. Itu sendiri informasi.
- **`OPTIONS`** kadang membalas `Allow` dan header berbeda dari `GET`.
- **Halaman error** sering memakai header berbeda dari halaman normal.

## 3. Cookie: Nama Sesi Membocorkan Stack

| Cookie | Teknologi |
|---|---|
| `PHPSESSID` | PHP |
| `JSESSIONID` | Java (Tomcat, Spring, Jetty) |
| `ASP.NET_SessionId`, `.AspNetCore.Session`, `.AspNetCore.Antiforgery.*` | ASP.NET / ASP.NET Core |
| `laravel_session`, `XSRF-TOKEN` | Laravel (PHP) |
| `csrftoken` + `sessionid` | Django (Python) |
| `_session_id`, `_rails_session` | Ruby on Rails |
| `connect.sid` | Express + express-session |
| `AWSALB`, `AWSALBCORS` | AWS Application Load Balancer |
| `__cf_bm`, `cf_clearance` | Cloudflare bot management |
| `_GRECAPTCHA` | Google reCAPTCHA |
| `_ga`, `_gid` | Google Analytics |
| `X-Magento-Vary` (header) | Magento |

Nama cookie adalah sinyal **sedang**: bisa diganti, tetapi jarang.

## 4. Jalur Aset: Paling Cepat untuk Frontend

| Pola | Teknologi |
|---|---|
| `/static/js/main.<hash>.js` + `/static/css/main.<hash>.css` | Create React App |
| `/_next/static/` | Next.js |
| `/_nuxt/` | Nuxt |
| `/assets/index-<hash>.js` + `type="module"` | Vite |
| `/build/main.<hash>.js` + `runtime.<hash>.js` + `polyfills.<hash>.js` | Angular CLI |
| `/_app/immutable/` | SvelteKit |
| `/_astro/` | Astro |
| `/packs/js/` | Rails + webpacker/shakapacker |
| `/wp-content/`, `/wp-includes/` | WordPress |
| `/sites/default/files/`, `/core/` | Drupal |
| `/static/version<id>/`, `/media/` | Magento |
| `/_framework/blazor.boot.json` | Blazor (ASP.NET) |
| `/cdn-cgi/` | Cloudflare (challenge, email protection) |

Bila jalur aset tidak cocok dengan tabel ini, jangan memaksa. Cari manifest build (lihat `js-chunk-discovery.md`) atau baca nama chunk — keduanya lebih dapat dipercaya daripada pola path.

## 5. Versi dari Bundle

Ini yang membedakan recon biasa dari recon yang berguna: **versi**, bukan hanya nama framework.

| Cara | Contoh | Catatan |
|---|---|---|
| Banner lisensi | `/*! React v18.2.0 */`, `/*! jQuery v3.6.0 */` | sering dipertahankan karena kewajiban lisensi; paling akurat |
| Konstanta versi | `version:"18.2.0"`, `jquery:"3.6.0"`, `VERSION.full="17.3.1"` | cari dengan grep string versi |
| Atribut root | `ng-version="17.3.0"` pada elemen aplikasi | Angular saja |
| State framework | `__NEXT_DATA__.buildId`, `__NUXT__.config` | build id ≠ versi, tetapi memetakan deploy |
| Source map | `webpack:///./node_modules/axios/package.json` | menyebut nama paket + versi di path |
| Sisa `package.json` | `/package.json`, `/node_modules/` | bila terekspos, daftar dependensi lengkap |

```bash
# banner lisensi dan string versi
grep -oE '/\*![^*]{0,80}\*/' main.pretty.js | head -30
grep -oiE '(react|vue|angular|jquery|bootstrap|lodash|axios|moment)[^0-9]{0,12}[0-9]+\.[0-9]+\.[0-9]+' main.pretty.js | sort -u
# nama paket dari source map
curl -s https://target.tld/main.a1b2.js.map | jq -r '.sources[]' | grep -oE 'node_modules/[^/]+' | sort -u
```

Yang perlu diingat: versi di bundle adalah versi **library yang terpasang saat build**, bukan versi server yang berjalan sekarang. Untuk aplikasi yang jarang deploy, keduanya sama; untuk yang deploy harian, bundle bisa lebih baru atau lebih lama dari header.

## 6. TLS dan DNS

| Sinyal | Arti |
|---|---|
| Issuer sertifikat | Let's Encrypt (sering otomatis), DigiCert/GlobalSign (enterprise) |
| SAN pada sertifikat | subdomain lain dari organisasi yang sama |
| CT logs (`crt.sh`) | riwayat subdomain, termasuk staging |
| CNAME `app.target.tld → cname.vercel-dns.com` | platform hosting |
| CNAME ke `*.netlify.app`, `*.github.io`, `*.herokuapp.com` | platform |
| MX ke Google/Microsoft | kecenderungan IdP dan email; bukan bukti |
| NS | registrar DNS dan penyedia zona |
| `TXT` (SPF, verification) | layanan yang pernah/ masih dipakai |

```bash
curl -s "https://crt.sh/?q=%25.target.tld&output=json" | jq -r '.[].name_value' | sort -u
```

DNS dan CT adalah sumber **pasif** — tidak menyentuh aplikasi. Lakukan lebih dulu.

## 7. Halaman Error dan Perilaku

| Sinyal | Teknologi |
|---|---|
| Stack trace `at Object.<anonymous>` + `node_modules` | Node.js |
| `Whoops!`, `Laravel` di halaman error | Laravel |
| `Whitelabel Error Page` | Spring Boot |
| `Server Error in '/' Application` | ASP.NET |
| `Traceback (most recent call last)` | Python (Django/Flask) |
| `ActionController::RoutingError` | Rails |
| `Warning: mysql_...` | PHP lama |
| `Request ID` di body + header | framework atau gateway tertentu |

Error adalah sinyal **rendah** bila halaman error dikustomisasi, dan **tinggi** bila stack trace asli terbuka. Stack trace juga temuan tersendiri: ia membocorkan path, dependensi, dan versi.

## 8. Keyakinan, Bukan Kepastian

Isi kolom keyakinan di inventaris:

| Tingkat | Kriteria | Boleh dipakai untuk |
|---|---|---|
| **Tinggi** | ≥2 sinyal independen sepakat (mis. header + cookie + jalur aset) | mencari CVE, memilih payload |
| **Sedang** | 1 sinyal kuat (header eksplisit, atribut versi) | hipotesis, bukan dasar serangan |
| **Rendah** | inferensi (teks error, pola umum, tebakan dari nama) | catatan; jangan dipakai memilih CVE |

Inventaris:

| Lapis | Teknologi | Versi | Bukti | Keyakinan |
|---|---|---|---|---|
| Infrastruktur | Cloudflare | — | `CF-Ray`, `__cf_bm` | tinggi |
| Server | nginx | 1.24.0 | `Server` (di balik CF? tidak) | sedang |
| Frontend | React | 18.2.0 | banner `/*! React v18.2.0 */` | tinggi |
| Frontend | Next.js | — | `/_next/static/` + `__NEXT_DATA__` | tinggi |
| Auth | Keycloak | — | `/realms/target/...`, cookie `KEYCLOAK_*` | sedang |
| Analytics | Google Analytics 4 | — | `googletagmanager.com/gtag/js?id=G-` | tinggi |

## 9. Dari Versi ke CVE

1. Kumpulkan pasangan **produk + versi** dengan keyakinan tinggi.
2. Cari di NVD berdasarkan produk/versi, dan `searchsploit <produk> <versi>` untuk daftar.
3. Periksa advisory vendor untuk versi yang dipakai (banyak CVE tidak masuk NVD tepat waktu).
4. Catat: **CVE ID**, **CVSS**, **versi terpengaruh**, **status** (Published/Reserved/Rejected), **apakah versi target termasuk**.
5. Jangan menyertakan exploit atau PoC di laporan recon — cukup identifikasi dan rujuk.

Kesalahan umum: mencocokkan CVE ke versi yang hanya "mirip". `React 18.2.0` bukan `18.0.0`; `nginx 1.24` bukan `1.24.0`. Bila versi tidak pasti, tuliskan kisaran, bukan angka.

## 10. Batas

| Batas | Dampak | Sikap |
|---|---|---|
| `Server`/`X-Powered-By` bisa dipalsukan | teknologi salah | minta sinyal kedua |
| CDN menimpa header origin | server asli tidak terlihat | catat CDN, jangan menebak origin |
| Versi di bundle = versi saat build | bisa beda dari runtime | beri catatan waktu build/deploy |
| Minifikasi membuang konstanta versi | versi tidak diketahui | cari banner lisensi atau source map |
| Halaman error dikustomisasi | tidak ada bocoran stack | turunkan keyakinan |
| Library vendored bisa berbeda dari package.json | salah versi | utamakan banner di berkas yang benar-benar dimuat |
| WAF memblokir probe | fingerprint gagal, bukan "tidak ada teknologi" | catat terhalang, ulangi dari IP/izin sah |

## Jebakan

- **`X-Powered-By` bukan bukti.** Mudah dipalsukan dan mudah dihapus; jangan pernah berdiri di atas satu header.
- **CDN menyembunyikan aslinya.** `server: cloudflare` menjawab "siapa di depan", bukan "siapa di belakang".
- **`ng-version` di DOM lebih dipercaya daripada versi di bundle** karena ia benar-benar dirender.
- **Banner lisensi bisa berasal dari library yang tidak dipakai.** Periksa apakah ia ada di chunk yang dimuat, bukan hanya di vendor bundle yang tak terpakai.
- **Nama cookie bisa diganti.** Gunakan sebagai sinyal pendukung, bukan bukti tunggal.
- **"React 18" bukan berarti patch terbaru.** Untuk CVE, versi minor/patch yang menentukan.
- **SPA tanpa SSR tidak memberi header framework.** Teknologi frontend hanya terbaca dari aset dan bundle.
- **`Server-Timing` mengungkap lapisan internal** tetapi sering hanya di lingkungan pengembangan.
- **Probe path (`/wp-login.php`, `/_next/`) menghasilkan 200 pada SPA apa pun.** Periksa isi, bukan status.
- **Fingerprinting aktif bisa memicu WAF.** Batasi laju dan catat bila terblokir.

## Best Practices

1. Mulai dari yang pasif: DNS, CT logs, header, HTML. Baru setelah itu probe.
2. Kumpulkan minimal dua sinyal untuk setiap klaim tingkat tinggi.
3. Selalu catat versi, bukan hanya nama — nama tanpa versi tidak bisa dipetakan ke CVE.
4. Tandai keyakinan di inventaris; pembaca laporan harus tahu mana yang terlihat dan mana yang ditebak.
5. Simpan `headers.txt` mentah sebagai bukti; header berubah antar deploy.
