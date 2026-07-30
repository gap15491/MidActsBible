import html

MAP = [
 ("I","The Prophetic Program","s1","God's dealings with Israel — the kingdom line",
  [("Law","Genesis, Exodus, Leviticus, Numbers, Deuteronomy"),
   ("History","Joshua, Judges, Ruth, 1–2 Samuel, 1–2 Kings, 1–2 Chronicles, Ezra, Nehemiah, Esther"),
   ("Poetry","Job, Psalms, Proverbs, Ecclesiastes, Song of Solomon"),
   ("Prophets","Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, Hosea, Joel, Amos, Obadiah, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi"),
   ("Gospels","Matthew, Mark, Luke, John")]),
 ("II","The Transition","s2","The hinge — where the Body of Christ begins",
  [("Acts 9 — the pivot","The risen Lord raises up Paul; the Body of Christ begins here. NOT Acts 13, and NOT Bullinger's Acts 28."),
   ("Through Acts","The prophetic program to Israel recedes as Israel is set aside in unbelief")]),
 ("III","The Mystery","s3","Paul's epistles to the Body of Christ",
  [("Foundational","Romans, 1 Corinthians, 2 Corinthians, Galatians"),
   ("Prison / the Mystery","Ephesians, Philippians, Colossians, Philemon"),
   ("The blessed hope","1 Thessalonians, 2 Thessalonians"),
   ("Pastoral order","1 Timothy, 2 Timothy, Titus")]),
 ("IV","Prophetic Epistles & Consummation","s4","To the circumcision believers; the prophetic close",
  [("Hebrews — non-Pauline, to the Jews","Written to the Hebrews, not to the Body of Christ; kept out of Paul's thirteen"),
   ("Jewish / circumcision epistles","James, 1 Peter, 2 Peter, 1 John, 2 John, 3 John, Jude"),
   ("Consummation","Revelation")]),
]

HINGE = [
 ("2 Timothy 2:15","“Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth.”","The command that grounds the whole method."),
 ("Ephesians 3:1-9","“…the dispensation of the grace of God which is given me to you-ward: how that by revelation he made known unto me the mystery…”","The mystery, hid in God, revealed to Paul."),
 ("Romans 16:25","“…according to the revelation of the mystery, which was kept secret since the world began.”","The mystery was unknown to the prophets."),
 ("Acts 3:21","“…which God hath spoken by the mouth of all his holy prophets since the world began.”","The prophetic program — foretold, not hidden."),
 ("Galatians 1:11-12","“…the gospel which was preached of me is not after man… but by the revelation of Jesus Christ.”","Paul's gospel came by direct revelation."),
 ("Romans 15:8","“…Jesus Christ was a minister of the circumcision for the truth of God, to confirm the promises made unto the fathers.”","Christ's earthly ministry served the prophetic program."),
 ("Colossians 1:24-27","“…to fulfil the word of God; even the mystery which hath been hid from ages and from generations, but now is made manifest to his saints.”","The mystery now made manifest in the Body."),
 ("1 Corinthians 15:1-4","“…how that Christ died for our sins according to the scriptures; and that he was buried, and that he rose again…”","The gospel of grace Paul preaches for today."),
]

DIST = [
 ("Audience","Israel / the nations through Israel","The Body of Christ (Jew and Gentile, one new man)"),
 ("Revealed through","The prophets, “since the world began”","Paul, by revelation of the mystery"),
 ("Gospel emphasis","The gospel of the kingdom","The gospel of the grace of God (1 Cor. 15:1-4)"),
 ("The hope","An earthly kingdom; Messiah reigning from Jerusalem","Caught up to meet the Lord in the air (1 Thess. 4)"),
 ("Israel's standing","Covenant people, promises confirmed","Set aside in unbelief during this present age"),
 ("Water baptism","Prominent (John's, kingdom baptism)","One baptism — the Spirit into the body (Eph. 4:5; 1 Cor. 12:13)"),
 ("The believer's identity","Servants awaiting the kingdom","Sons, seated in heavenly places (Eph. 2:6)"),
 ("Time frame","This age & the age to come (prophecy)","The dispensation of grace (the mystery)"),
]

p=[]
p.append('''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rightly Dividing the Word — Companion Chart</title>
<style>
:root{--ink:#2b2622;--soft:#6b6259;--rule:#e6ded2;--bg:#faf7f2;--paper:#fffdf9;
--s1:#7c9c8e;--s1b:#eef3f0;--s2:#c9a35b;--s2b:#f7f0e0;--s3:#8f6b9e;--s3b:#f1ebf4;--s4:#a76a5a;--s4b:#f5ebe7;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;line-height:1.6;font-size:17px}
.wrap{max-width:940px;margin:0 auto;padding:0 24px}
header{text-align:center;padding:60px 24px 34px;background:var(--paper);border-bottom:1px solid var(--rule)}
header h1{font-size:2.3rem;margin:0 0 8px;font-weight:600}
header .sub{color:var(--soft);font-style:italic;margin:0;font-size:1.05rem}
h2.sec{font-size:.82rem;letter-spacing:.22em;text-transform:uppercase;color:var(--soft);
font-weight:700;text-align:center;margin:56px 0 26px}
.legend{display:flex;justify-content:center;flex-wrap:wrap;gap:10px 18px;margin:28px 0 6px}
.legend span{display:inline-flex;align-items:center;gap:8px;font-size:.86rem;color:var(--soft)}
.dot{width:13px;height:13px;border-radius:50%;display:inline-block}
.map{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:16px;margin-top:8px}
.card{background:var(--paper);border:1px solid var(--rule);border-radius:12px;overflow:hidden;border-top:5px solid var(--accent)}
.card .hd{padding:14px 16px 10px}
.card .rn{font-size:.68rem;letter-spacing:.16em;color:var(--soft);font-weight:700}
.card .nm{font-size:1.12rem;font-weight:600;margin:2px 0 2px}
.card .ds{font-size:.82rem;color:var(--soft);font-style:italic}
.card .grp{padding:0 16px 14px}
.card .g{margin-top:12px}
.card .gt{font-size:.7rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:3px}
.card .gb{font-size:.9rem;line-height:1.45}
.s1{--accent:var(--s1)}.s2{--accent:var(--s2)}.s3{--accent:var(--s3)}.s4{--accent:var(--s4)}
.s1 .card,.s1.card{background:var(--s1b)}.s2.card{background:var(--s2b)}.s3.card{background:var(--s3b)}.s4.card{background:var(--s4b)}
.hinge{max-width:760px;margin:0 auto}
.h{background:var(--paper);border:1px solid var(--rule);border-left:4px solid var(--s3);
border-radius:8px;padding:16px 20px;margin:12px 0}
.h .ref{font-weight:700;font-size:.92rem;color:var(--s3);letter-spacing:.02em}
.h .q{margin:6px 0 6px;font-size:1rem}
.h .n{font-size:.85rem;color:var(--soft);font-style:italic}
table{width:100%;border-collapse:collapse;margin-top:10px;background:var(--paper);
border:1px solid var(--rule);border-radius:10px;overflow:hidden;font-size:.92rem}
th{text-align:left;padding:14px 16px;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:#fff}
th.k{background:#8a8178}th.p{background:var(--s1)}th.b{background:var(--s3)}
td{padding:13px 16px;border-top:1px solid var(--rule);vertical-align:top}
td.k{font-weight:700;color:var(--ink);width:20%}
td.p{color:#4a5a52;width:40%}td.b{color:#5a4a62;width:40%}
tr:nth-child(even) td{background:#fbf9f5}
footer{text-align:center;padding:56px 24px;color:var(--soft);font-size:.84rem;border-top:1px solid var(--rule);margin-top:56px}
.note{max-width:740px;margin:26px auto 0;font-size:.88rem;color:var(--soft);text-align:center;font-style:italic}
@media print{body{background:#fff}.card,.h,table{break-inside:avoid}}
</style></head><body>''')

p.append('''<header><h1>Rightly Dividing the Word of Truth</h1>
<p class="sub">A companion map to the two programs of God — the Prophetic and the Mystery</p></header><div class="wrap">''')

# legend
p.append('<div class="legend">')
for cls,label in [("s1","Prophetic Program"),("s2","Transition (Acts)"),("s3","The Mystery — Body of Christ"),("s4","Prophetic Epistles & Consummation")]:
    p.append(f'<span><span class="dot" style="background:var(--{cls.replace("s","s")})"></span>{label}</span>')
p.append('</div>')
# fix dot colors
p_str=""

# map
p.append('<h2 class="sec">The Whole Bible at a Glance</h2><div class="map">')
for rn,name,cls,desc,groups in MAP:
    p.append(f'<div class="card {cls}"><div class="hd"><div class="rn">SECTION {rn}</div><div class="nm">{html.escape(name)}</div><div class="ds">{html.escape(desc)}</div></div><div class="grp">')
    for gt,gb in groups:
        p.append(f'<div class="g"><div class="gt">{html.escape(gt)}</div><div class="gb">{html.escape(gb)}</div></div>')
    p.append('</div></div>')
p.append('</div>')
p.append('<p class="note">Paul’s thirteen epistles form one bounded unit (Section III); the prophetic program brackets the mystery on both sides — itself a teaching point of right division.</p>')

# hinge verses
p.append('<h2 class="sec">The Hinge Verses</h2><div class="hinge">')
for ref,q,n in HINGE:
    p.append(f'<div class="h"><div class="ref">{html.escape(ref)}</div><div class="q">{html.escape(q)}</div><div class="n">{html.escape(n)}</div></div>')
p.append('</div>')

# distinctives table
p.append('<h2 class="sec">Distinctives of the Two Programs</h2>')
p.append('<table><tr><th class="k">&nbsp;</th><th class="p">The Prophetic Program (Israel)</th><th class="b">The Mystery (Body of Christ)</th></tr>')
for k,pp,bb in DIST:
    p.append(f'<tr><td class="k">{html.escape(k)}</td><td class="p">{html.escape(pp)}</td><td class="b">{html.escape(bb)}</td></tr>')
p.append('</table>')
p.append('<p class="note">Framework: mid-Acts right division — the Body of Christ begins at <strong>Acts 9</strong> (not Acts 13, not Bullinger&rsquo;s Acts 28), in the tradition of C. R. Stam / the Berean Bible Society. Hebrews is treated as a non-Pauline epistle written to the Jews and grouped with the prophetic epistles.</p>')

p.append('<footer><a href="index.html" style="color:inherit;font-weight:600">&larr; The Bible</a> &middot; Scripture: King James Version (Public Domain) &middot; “Rightly dividing the word of truth.” — 2 Timothy 2:15</footer>')
p.append('</div></body></html>')

out="".join(p)
# patch legend dot colors correctly
out=out.replace('background:var(--s1)"></span>Prophetic Program','background:#7c9c8e"></span>Prophetic Program')
out=out.replace('background:var(--s2)"></span>Transition','background:#c9a35b"></span>Transition')
out=out.replace('background:var(--s3)"></span>The Mystery','background:#8f6b9e"></span>The Mystery')
out=out.replace('background:var(--s4)"></span>Prophetic Epistles','background:#a76a5a"></span>Prophetic Epistles')
open("KJV_Division_Companion_Chart.html","w",encoding="utf-8").write(out)
print("chart bytes:", len(out.encode()))
