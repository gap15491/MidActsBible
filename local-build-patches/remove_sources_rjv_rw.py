#!/usr/bin/env python3
# Remove the "rjv" (Richard Jordan) and "rw" (Randy White) commentary sources.
# Run against BOTH:
#   python3 remove_sources_rjv_rw.py index.html
#   python3 remove_sources_rjv_rw.py ~/bible/build_bible.py
# and check ~/bible/content.py for RJV_* / RW_* blocks (see NOTE at the bottom).
import io, re, sys

# ---- literal replacements ------------------------------------------------
LITERALS = [
    ("css: show-rjv rule",
     "body:not(.show-rjv) .src-rjv{display:none}\n", ""),
    ("css: show-rw rule",
     "body:not(.show-rw) .src-rw{display:none}\n", ""),
    ("body default classes",
     'class="show-ga show-lf show-sg show-bbs show-rjv show-rw home"',
     'class="show-ga show-lf show-sg show-bbs home"'),
    ("chip: Richard Jordan",
     '<button class="srcchip" type="button" onclick="toggleSrc(this,\'rjv\')">'
     'Richard Jordan (video)</button>\n', ""),
    ("chip: Randy White",
     '<button class="srcchip" type="button" onclick="toggleSrc(this,\'rw\')">'
     'Randy White</button>\n', ""),
    ("js: covers()",
     "if(src==='lf'||src==='bbs'||src==='rjv'||src==='rw')return true;",
     "if(src==='lf'||src==='bbs')return true;"),
    ("js: SEARCH map",
     ",rjv:'https://www.youtube.com/results?search_query=Richard+Jordan+',"
     "rw:'https://www.youtube.com/results?search_query=Randy+White+Ministries+'", ""),
    ("js: SRCNAME map",
     ",rjv:'Richard Jordan (video)',rw:'Randy White'", ""),
    ("js: SRCDESC map",
     ",rjv:'verse-by-verse teaching (YouTube)',rw:'verse-by-verse teaching (YouTube)'", ""),
]

# the two source-iteration arrays (verse panel + chapter header)
ARRAY_OLD = "['ga','lf','sg','bbs','rjv','rw']"
ARRAY_NEW = "['ga','lf','sg','bbs']"

# static per-book commentary links baked into the HTML (66 of each)
ANCHOR_RE = re.compile(
    r'<a class="csrc src-(?:rjv|rw)" href="[^"]*" target="_blank" '
    r'rel="noopener" title="[^"]*">[^<]*</a>')


def main(path):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    orig = s
    ok = True

    for name, old, new in LITERALS:
        n = s.count(old)
        if n == 1:
            s = s.replace(old, new)
            print("  [ok]   %s" % name)
        elif n == 0 and (not new or s.count(new)):
            print("  [skip] %s (already removed)" % name)
        else:
            print("  [FAIL] %s (anchor found %d times)" % (name, n))
            ok = False

    n = s.count(ARRAY_OLD)
    if n:
        s = s.replace(ARRAY_OLD, ARRAY_NEW)
        print("  [ok]   js: source arrays (%d)" % n)
    else:
        print("  [skip] js: source arrays (already removed)")

    s, n = ANCHOR_RE.subn("", s)
    print("  [ok]   static book links removed: %d" % n)

    if not ok:
        print("\nNothing written - fix the failing anchors first.")
        return 1
    if s == orig:
        print("\nNo changes needed.")
        return 0

    left = len(re.findall(r"src-rjv|src-rw|show-rjv|show-rw|'rjv'|'rw'", s))
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("\nPatched %s (%d stray references remaining)" % (path, left))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "index.html"))

# NOTE for ~/bible/content.py:
#   the per-book link builders there may hold RJV_* / RW_* entries (LABEL / SEARCH /
#   COVERS). Delete those blocks and drop 'rjv' and 'rw' from any source list, or the
#   next build re-emits the links this script strips out.
