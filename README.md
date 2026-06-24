# mv-bench-py-web

A deliberately vulnerable **Python / FastAPI** shop API, used as a known-answer
target for benchmarking security scanners (precision / recall).

It is part of the **mv-bench** corpus:

| Repo | Stack | Purpose |
|------|-------|---------|
| `mv-bench-py-web` | Python · FastAPI | this app |
| `mv-bench-node-api` | Node · Express | sibling app |
| `mv-bench-ai-app` | Python · LLM agent | sibling app |
| `mv-bench-truth` | — | ground-truth labels + scorer for all three |

The planted vulnerabilities are intentionally realistic: most span **multiple
files** (an HTTP route in `app/main.py` flows through a service in
`app/services/*` into a sink in `app/db.py` / `app/utils/*`), so a scanner has to
trace cross-file data flow rather than pattern-match a single line. Each app also
ships **safe decoys** — code that looks dangerous but is correctly defended — so a
scanner that fires on everything is penalised on precision.

> ⚠️ **Do not deploy this.** It exists to be scanned, not run in anger.

The location and classification of every planted bug (and every decoy) lives in
[`mv-bench-truth`](https://github.com/onfafanutifafa/mv-bench-truth), kept in a
separate repo on purpose so the answer key never leaks into the code under test.

## Layout

```
app/
  main.py            # FastAPI routes — the trust boundary (untrusted input enters)
  config.py          # settings
  db.py              # SQLite data-access (raw + parameterized helpers)
  auth.py            # current-user dependency
  models.py          # dataclasses
  services/
    users.py         # user search + profile updates
    orders.py        # checkout, coupons, order lookup
    files.py         # upload read-back + document conversion
    net.py           # outbound fetch + redirect
  utils/
    crypto.py        # password hashing + token generation
    serialize.py     # session (de)serialization
```
