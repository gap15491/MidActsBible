# The KJV Rightly Divided

A King James Bible reordered on the **right-division** principle (2 Timothy 2:15), separating
Paul's epistles to the Body of Christ from the Prophetic Program written to Israel. Mid-Acts
framework — the Body of Christ begins at **Acts 9**.

The whole thing is two self-contained static HTML files. No server code, no database.

- `index.html` — the reordered study Bible (all 66 books, book intros, front/back matter,
  verse/paragraph toggle, commentary layer, per-verse notes).
- `chart.html` — the companion division chart.

---

## Deploy to Railway

Railway serves this as a static site via the included `Dockerfile` (Caddy). Every push
to GitHub auto-redeploys.

1. Push this repo to GitHub (see below).
2. Go to **railway.com/new** → **Deploy from GitHub repo**.
3. Connect your GitHub account and select this repository.
4. Railway builds the `Dockerfile` and deploys. When it finishes, open the generated
   `*.up.railway.app` URL.
   - The Bible is at `/` (index.html); the chart is at `/chart.html`.

### Custom domain (optional)
In your Railway service: **Settings → Networking → Custom Domain** → add your domain →
create the CNAME record Railway gives you at your DNS provider. SSL is issued automatically.

### Push this repo to GitHub
```bash
cd kjv-rightly-divided
git init
git add .
git commit -m "KJV Rightly Divided — reordered study Bible"
# create an empty repo on github.com first, then:
git remote add origin https://github.com/<you>/kjv-rightly-divided.git
git branch -M main
git push -u origin main
```
(Or with the GitHub CLI: `gh repo create kjv-rightly-divided --public --source=. --push`.)

---

## Editing the Bible (regenerating the HTML)

All authored content lives in `src/content.py`. The KJV text is in `src/books/`.

```bash
cd src
python3 build_bible.py     # regenerates ../index.html? (see note)
python3 build_chart.py
```

**Note:** the build scripts write `KJV_Rightly_Divided.html` and
`KJV_Division_Companion_Chart.html` into the current directory. After building, copy them to
the repo root as `index.html` and `chart.html`:

```bash
cp KJV_Rightly_Divided.html ../index.html
cp KJV_Division_Companion_Chart.html ../chart.html
```

Then commit and push — Railway redeploys automatically.

### Where to change things
- **Per-verse inline notes** — `content.py` → `NOTES` dict, keyed `"Book C:V"`.
- **Book introductions** — `content.py` → `INTROS`.
- **Front/back matter** — `content.py` → `HOWTO`, `TIMELINE`, `GLOSSARY`, `PLAN`.
- **Commentary sources** — `content.py` → `GA_LINKS`, `SG_LINKS`, `LF_*`.
- **Book order / sections** — `build_bible.py` → `SECTIONS`.

---

## Notes on the commentary layer

The three commentary sources (Grace Ambassadors, Les Feldick, Sufficient Grace Bible Fellowship)
are **linked, not reproduced** — their material is copyright-reserved. Per-verse buttons open a
site-scoped search for the exact verse reference. The inline per-verse notes are original.

## Credits
- KJV text: public domain (source dataset: aruljohn/Bible-kjv). Verified 1189 chapters / 31,102 verses.

---

## Troubleshooting: "Railway isn't showing my update"

Work through these in order:

1. **Confirm the version actually loaded.** Near the top of the page (under the source chips)
   there is an **"Updated <date> UTC"** stamp, and a purple **☰ Contents** button floats in the
   bottom-right corner. If you don't see them, you're looking at an old copy.

2. **The served file must be `index.html` at the repo root.** The Dockerfile serves `index.html`.
   If you committed the Bible under any other name (e.g. `KJV_Rightly_Divided.html`), Railway is
   still serving the old `index.html`. Use `src/build.sh`, which writes straight to `index.html`
   and `chart.html` — no rename step to get wrong.

3. **Hard-refresh the browser** at the Railway URL: Ctrl+Shift+R (Cmd+Shift+R on Mac). Static HTML
   caches aggressively. The Caddyfile now sends `Cache-Control: no-cache` so this stops happening
   on future deploys, but a one-time hard refresh clears what's already cached.

4. **Force a clean Railway build.** In the Railway service: open the latest deployment ->
   **⋮ menu -> Redeploy**. If it still serves stale content, add a trivial change (edit this README)
   and push, which guarantees a new commit and a fresh build.

5. **Verify what Railway is actually serving** (separates "didn't deploy" from "browser cache"):
   open the Railway URL in a private/incognito window, or `curl -s https://<your-app>.up.railway.app | grep "Updated"`
   and check the stamp date.

### Rebuild + redeploy in one go
```bash
bash src/build.sh          # writes ../index.html and ../chart.html
git add -A && git commit -m "update" && git push
```
