#!/usr/bin/env python3
# Server side of "comments on topic key verses".
#   python3 patch_app_topic_verse_notes.py app.py
import io, sys

OLD_HELPER = "# ---------------- study topics (per-user notes + attached verses) ----------------\ndef _topic_row(r):"
NEW_HELPER = '''# ---------------- study topics (per-user notes + attached verses) ----------------
def _norm_topic_verses(verses):
    """A key verse is either "Book C:V" (no comment) or {"ref": ..., "note": ...}."""
    out = []
    for v in verses[:200]:
        if isinstance(v, dict):
            ref = str(v.get("ref") or "")[:60].strip()
            if not ref:
                continue
            note = str(v.get("note") or "")[:4000]
            out.append({"ref": ref, "note": note} if note.strip() else ref)
        else:
            ref = str(v)[:60].strip()
            if ref:
                out.append(ref)
    return out


def _topic_row(r):'''

OLD_NORM = "    verses = [str(v)[:60] for v in verses][:200]"
NEW_NORM = "    verses = _norm_topic_verses(verses)"

OLD_SEARCH = "    # personal cross-reference notes"
NEW_SEARCH = '''    # comments attached to topic key verses
    for t in (Topic.query.filter_by(user_id=u.id)
              .filter(db.func.lower(Topic.verses).like(like)).limit(40).all()):
        try:
            vs = json.loads(t.verses)
        except Exception:
            vs = []
        if not isinstance(vs, list):
            vs = []
        for v in vs:
            if not isinstance(v, dict):
                continue
            note = v.get("note") or ""
            if q.lower() not in note.lower():
                continue
            out.append({"kind": "topic",
                        "label": (t.title or t.key) + " \\u00b7 " + str(v.get("ref") or ""),
                        "snippet": _snippet(note, q),
                        "nav": {"type": "topic", "key": t.key}})
    # personal cross-reference notes'''

PATCHES = [
    ("py: verse normalizer", OLD_HELPER, NEW_HELPER),
    ("py: put_topic accepts comments", OLD_NORM, NEW_NORM),
    ("py: search includes verse comments", OLD_SEARCH, NEW_SEARCH),
]


def main(path):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    ok = True
    for name, old, new in PATCHES:
        n = s.count(old)
        if s.count(new) >= 1:
            print("  [skip] %s (already applied)" % name)
        elif n == 1:
            s = s.replace(old, new)
            print("  [ok]   %s" % name)
        else:
            print("  [FAIL] %s (anchor found %d times)" % (name, n))
            ok = False
    if not ok:
        print("\nNothing written.")
        return 1
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("\nPatched %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "app.py"))
