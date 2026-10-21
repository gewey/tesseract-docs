# Template Literals — the `${...}` book of spells

A JavaScript template literal is a string built at the moment it is evaluated. Anything inside
`${...}` is a **JavaScript expression**, and its result is coerced to a string.

```js
const who = "world";
`hello ${who}`        // "hello world"
```

That is the whole rule. Everything below is just a catalogue of what you are allowed to put in
the braces. The expression runs **when the string is built**, not when it is later used, and it
runs in whatever scope the literal sits in.

> Stored here because looking at the list is like reading a book of spells. Keep it handy.

---

## 1. Variables and object properties

```js
${baseURL}
${user.name}
${config.theme}
${items[0]}
${items.at(-1)}
```

## 2. Browser, window, document

| Expression | Returns |
|---|---|
| `document.URL` | full page URL |
| `document.domain` | domain only |
| `document.title` | current `<title>` |
| `document.referrer` | referring page |
| `document.characterSet` | e.g. `UTF-8` |
| `document.lastModified` | last modified date |
| `document.cookie` | all cookies as one string |
| `window.location.href` | full URL |
| `window.location.protocol` | `https:` or `file:` |
| `window.location.host` | `host:port` |
| `window.location.pathname` | path only |
| `window.location.search` | query string |
| `window.location.hash` | `#fragment` |
| `navigator.userAgent` | browser string |
| `navigator.language` | e.g. `en-US` |
| `navigator.platform` | OS string |
| `navigator.onLine` | `true` / `false` |
| `screen.width` / `screen.height` | screen px |
| `screen.colorDepth` | e.g. `24` |
| `window.devicePixelRatio` | e.g. `2` |
| `window.innerWidth` / `innerHeight` | viewport px |
| `Intl.DateTimeFormat().resolvedOptions().timeZone` | e.g. `America/Chicago` |

## 3. Storage and state

```js
${localStorage.getItem('theme') || 'dark'}
${sessionStorage.getItem('lang')}
${JSON.parse(localStorage.getItem('user') || '{}').name}
```

## 4. Time and performance

```js
${new Date().getFullYear()}
${new Date().toISOString()}
${Date.now()}
${performance.now()}
```

## 5. Math and random

```js
${Math.random()}
${Math.PI}
${Math.max(a, b)}
${Math.random().toString(36).slice(2, 10)}   // nonce
```

## 6. Function calls

Anything that returns a value works, including calls defined in the same script.

```js
${getTheme()}
${detectBrowser()}
${generateNonce()}
```

## 7. Ternaries and conditionals

```js
${isMobile ? '/css/mobile.css' : '/css/desktop.css'}
${darkMode ? '#0a0a0a' : '#ffffff'}
${user?.role === 'admin' ? '/js/admin.js' : ''}
```

## 8. Logical short-circuits

```js
${debug && '/js/debug-overlay.js'}   // false -> empty string
${region || 'us-east'}               // fallback
${token ?? 'anonymous'}              // nullish fallback
```

## 9. String operations

```js
${baseURL.replace(/^http:/, 'https:')}
${userAgent.split(' ')[0]}
${path.split('/').pop()}
${String(42).padStart(4, '0')}
```

## 10. Nested templates

```js
`<link rel='stylesheet' href='${baseURL}/css/${themeName}.css'>`
```

## 11. Tagged templates

A tag function receives the literal parts and the evaluated values separately. `String.raw`
disables escape processing, which is useful for paths and regexes.

```js
String.raw`V:\__marinus__\01_Docs`   // backslashes stay intact
```

## 12. Async values

`${}` cannot await by itself. Await first, then interpolate:

```js
const data = await fetch(url).then(r => r.json());
`<h1>${data.title}</h1>`
```

---

## Safety, in four lines

- **Nothing is escaped.** If the value comes from a URL, a form, or storage, it is raw HTML.
  Interpolating user input into a template that becomes markup is an XSS hole.
- **It runs at build time, not render time.** A value captured in a literal is frozen at the
  moment the string is created.
- **It runs in scope.** If the name is not in scope, you get a `ReferenceError`, not `undefined`.
- **`undefined` becomes the text `"undefined"`.** It does not throw and it does not disappear.

---

## How this site uses it: the `baseURL` ladder

`js/dynamichead.js` is the only script a page needs in its head. It derives `baseURL` from its own
`<script src>`, then decides which base every asset should use:

| Page opened from | Derived base | Probe | Final base |
|---|---|---|---|
| `https://gewey.github.io/...` | https | not run | https |
| `file:///.../js/dynamichead.js` with the site on the same disk | file | loads `falling_up_steps.js` | file |
| `file:///...` with no site on that disk | file | `falling_up_steps.js` 404s | https://gewey.github.io |
| `file:///...` whose head was loaded from the live site | https | not run | https |

One decision, made once, applied to every `${baseURL}` in the head. `falling_up_steps.js` exists
to be requested: if the request succeeds, a local mirror exists; if it fails, the failure is the
answer. Pages opened online never probe, so their behaviour is unchanged.

---

*Reference compiled into website form by `docs_compiler.py` alongside the rest of the docs module.*
