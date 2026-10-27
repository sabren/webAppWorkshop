# sabren/webAppWorkshop

> An online IDE for building web applications, hosted on Google App
> Engine (Python 2.7): a host-based dispatcher serving one app per
> hostname, a login-gated master app, an Ace code editor, and a
> generic datastore-backed CRUD/REST layer ("instacrud"). The plan
> files show the ambition — a hosted workshop business — further
> than the code got.
> Repo: https://github.com/sabren/webAppWorkshop — 28 tracked files
> plus one git submodule, git history in this clone 2011-10-29 →
> 2012-12-28. **Keep — the App Engine IDE experiment and its plan
> files are a coherent record of the workshop-as-a-service idea.**

## Inventory

- **Dispatcher (`main.py`, `app.yaml`):** `application:
  webappworkshop`, `runtime: python27`, all URLs routed to `main.py`.
  `main.py` (copyright 2011 Sabren Enterprises, Inc.) subclasses
  weblib's `Engine` as `AppEngineEngine`, stripping CGI-specific
  behavior for App Engine, and describes itself as "the main
  dispatcher for http://*.webappworkshop.com/" — one app per
  hostname. It imports `weblib, handy` and `ERR, REST, CRUD` from
  `lib/` and `sub/workshop`.
- **Master app (`app/master/master.py`):** federated-login-gated
  greeting app — after `LOGIN.check`, it prints "Hello, <nickname>!
  Greetings from <host>!" and serves a one-route urlMap.
- **Editor app (`app/tangentcode/`):** serves `editor.html`, an Ace
  editor page (Ace 0.2.0 vendored under `static/js/ace-0.2.0/`,
  Eclipse theme, Java mode) with a "camera" area sized for
  screencasts. The URL map is `tangentcode.py`; `editor.py` is a
  two-line file that just writes out the HTML.
- **Library (`lib/`):** `CRUD.py` (174 lines) — "a generic data
  store and REST API": `GridModel`/`ColumnModel`/`RowModel` on
  App Engine's datastore, the "instacrud" grid API
  (`/api/g/` list/create grids, `/api/g/<type>/` per-grid). `REST.py`
  (23 lines) — urlMap routing. `LOGIN.py` (31 lines) — federated
  login logic. `ERR.py` (8 lines). `setup.py` (13 lines).
- **Tests (`tests/`):** `test_dispatch.py` (host/path-argument
  dispatch via a `RequestBuilder`) and `test_instacrud.py`
  (grid creation against a datastore testbed). The dispatch test
  notes it is "REALLY testing a new dispatch mechanism for weblib".
- **Plans (`plan/`):** `workshop.org` — business model ("Do a bunch
  of research. Share (parts of) the knowledge. Charge clients to do
  specific jobs for them.") and an implementation plan: DONE
  0000-swap-main-by-host, DONE 0001-ace-code-editor, TODO
  0002-swap-namespace, DONE 0003-crud-server-flat (with the grid
  API sketched). `tangentstuff.org` — notes for "tangentstuff
  (claritygame precursor for google app-engine)": Google-account and
  federated login done (via App Engine's OpenID example code),
  typed lists/tables, inbox processing, and values clarification
  still TODO. `scarlet.org` and `trailblazer.org` are also present
  (not read in detail for this doc).
- **Submodule (`sub/workshop`):** declared in `.gitmodules` as
  `git@github.com:sabren/workshop` — the workshop library itself,
  which `main.py` puts on `sys.path`. The directory is empty in a
  plain clone (submodule not initialized); the dependency is
  declared, not vendored.
- **Branch:** `origin/0000-swap-main-by-host` (Oct 2011) — the
  host-based-dispatch work ("Used weblib for host-based-dispatch on
  App Engine! :)"), which the plan marks DONE and master absorbed.

## Verdict

**Keep.** The code is a working sketch (dispatcher, login, editor
shell, grid CRUD) rather than a finished IDE, but the repo's value
is the combination: the App Engine architecture plus the plan files
that explain what it was meant to become. Nothing here duplicates
sabren/workshop — it depends on it.
