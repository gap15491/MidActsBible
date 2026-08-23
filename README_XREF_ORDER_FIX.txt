CROSS-REFERENCE ORDER FIX — 2026-08-23
======================================
Repo: gap15491/MidActsBible   Branch: main

WHAT WAS WRONG
--------------
1. "My cross-references" was sorted by TARGET CHAPTER then TARGET VERSE, with the
   target BOOK ignored entirely. So a freshly added ref looked right (the add path
   just appends to the client cache) but jumped somewhere else the moment you
   navigated away and came back and the list reloaded from the server.
       app.py  ->  .order_by(Xref.verse, Xref.tchapter, Xref.tverse)

2. The pencil (edit) button DELETEd the row and POSTed a new one. That minted a new
   row id, so every edited cross-reference moved to the bottom of the list.

WHAT CHANGED
------------
app.py
  * GET  /api/xrefs  -> .order_by(Xref.verse, Xref.id)   = the order you added them.
  * POST /api/xrefs  -> accepts an optional "id" and updates that row IN PLACE
                        (ownership-checked), so an edit keeps its id and its slot.

index.html  (saveXref)
  * No longer DELETEs before saving an edit; posts {id: editId, ...} instead.
  * Replaces the item in the XC cache at its existing index instead of pushing it
    onto the end.

local-build-patches/patch_xref_order.py   (NEW)
  * Applies the same saveXref change to your LOCAL src/build_bible.py.

HOW TO INSTALL
--------------
STEP 1 — Deploy (this is what makes the live site correct)
  Upload app.py and index.html to the repo, committing DIRECTLY TO main (not a new
  PR branch). Push BOTH — they must ship together. A new index.html against the old
  app.py would send an "id" the server ignores and create duplicate rows on edit.
  Railway auto-deploys. Confirm via the "Updated ... UTC" stamp at the bottom of the
  home page.

STEP 2 — Protect your local build (do this or the next rebuild undoes step 1)
  Your src/ folder is not in the repo, so build_bible.py still has the old saveXref()
  and `bash src/build.sh` would regenerate index.html with the bug. From your local
  project root:

      python local-build-patches/patch_xref_order.py

  (Or pass the path: python local-build-patches/patch_xref_order.py src/build_bible.py)
  It writes a .bak, is idempotent, and tells you if the code has drifted. Then rebuild.

DATABASE
--------
No schema change. Existing cross-references keep their ids, so they come back in the
order you originally entered them. Nothing to migrate.

VERIFIED
--------
Ran your John 8:44 list (all 16 refs, in your order) through Flask's test client on
SQLite. Against the ORIGINAL code the test reproduced your screenshot exactly --
1 Corinthians 5:5-13 landing between Ephesians 4:14 and 1 Timothy 6:9. Against the
patched code: order preserved, last-added stays last, an edit keeps position 5 and
creates no duplicate, delete still works, and a re-add lands at the bottom.

NOT INCLUDED (possible next step)
---------------------------------
Drag-to-reorder. This fix orders by WHEN you added a cross-reference; moving an
existing one up or down would need a sort_order column plus a reorder endpoint.
