import json, os, html, urllib.parse
import content

SECTIONS = [
    ("I", "The Prophetic Program", "God's dealings with Israel — the kingdom line \"since the world began\" (Acts 3:21)",
     ["Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges","Ruth",
      "1 Samuel","2 Samuel","1 Kings","2 Kings","1 Chronicles","2 Chronicles","Ezra","Nehemiah","Esther",
      "Job","Psalms","Proverbs","Ecclesiastes","Song of Solomon",
      "Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel","Hosea","Joel","Amos","Obadiah","Jonah",
      "Micah","Nahum","Habakkuk","Zephaniah","Haggai","Zechariah","Malachi",
      "Matthew","Mark","Luke","John"]),
    ("II", "The Transition", "Acts — the hinge; at chapter 9 the risen Lord raises up Paul and the Body of Christ begins",
     ["Acts"]),
    ("III", "The Mystery", "Paul's epistles to the Body of Christ (Ephesians 3:1-9)",
     ["Romans","1 Corinthians","2 Corinthians","Galatians","Ephesians","Philippians","Colossians",
      "1 Thessalonians","2 Thessalonians","1 Timothy","2 Timothy","Titus","Philemon"]),
    ("IV", "The Prophetic Epistles & Consummation", "Written to the circumcision believers; the prophetic close",
     ["Hebrews","James","1 Peter","2 Peter","1 John","2 John","3 John","Jude","Revelation"]),
]

def slug(name): return "b_" + name.replace(" ","").replace(",","")
def load(name):
    return json.load(open("books/"+name.replace(" ","")+".json"))

parts = []
parts.append('''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The KJV Rightly Divided — Reordered by Program</title>
<style>
:root{--ink:#2b2622;--soft:#6b6259;--rule:#e0d8cc;--bg:#faf7f2;--paper:#fffdf9;
--s1:#7c9c8e;--s2:#c9a35b;--s3:#8f6b9e;--s4:#a76a5a;--accent:#8f6b9e;}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);
font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;
line-height:1.62;font-size:19px;-webkit-font-smoothing:antialiased}
.wrap{max-width:760px;margin:0 auto;padding:0 22px}
header.masthead{text-align:center;padding:64px 22px 40px;border-bottom:1px solid var(--rule);background:var(--paper)}
header.masthead h1{font-size:2.35rem;margin:0 0 8px;letter-spacing:.01em;font-weight:600}
header.masthead .sub{color:var(--soft);font-size:1.02rem;font-style:italic;margin:0}
header.masthead .verse{margin-top:20px;font-size:.95rem;color:var(--soft);max-width:520px;margin-left:auto;margin-right:auto}
nav.toc{background:var(--paper);border-bottom:1px solid var(--rule);padding:34px 22px 42px}
nav.toc h2{text-align:center;font-size:.8rem;letter-spacing:.22em;text-transform:uppercase;color:var(--soft);font-weight:600;margin:0 0 26px}
.toc-sec{max-width:760px;margin:0 auto 26px}
.toc-sec .lbl{display:flex;align-items:baseline;gap:10px;border-left:4px solid var(--accent);padding-left:12px;margin-bottom:12px}
.toc-sec .rn{font-size:.72rem;letter-spacing:.15em;color:var(--soft);font-weight:700}
.toc-sec .nm{font-size:1.12rem;font-weight:600}
.toc-sec .booklist{display:flex;flex-wrap:wrap;gap:6px 8px;padding-left:16px}
.toc-sec a{display:inline-block;padding:4px 11px;border:1px solid var(--rule);border-radius:20px;
text-decoration:none;color:var(--ink);font-size:.85rem;background:#fff;transition:.15s}
.toc-sec a:hover{border-color:var(--accent);color:var(--accent)}
.s1{--accent:var(--s1)}.s2{--accent:var(--s2)}.s3{--accent:var(--s3)}.s4{--accent:var(--s4)}
.section-divider{text-align:center;padding:70px 22px 46px;margin-top:30px}
.section-divider .rn{font-size:.8rem;letter-spacing:.3em;color:var(--soft);font-weight:700}
.section-divider h2{font-size:2rem;margin:10px 0 10px;font-weight:600}
.section-divider p{color:var(--soft);font-style:italic;max-width:520px;margin:0 auto;font-size:1rem}
.section-divider .bar{width:60px;height:4px;margin:22px auto 0;border-radius:2px;background:var(--accent)}
.book{padding:30px 0 10px;border-top:1px solid var(--rule)}
.book h3.bt{font-size:1.75rem;text-align:center;margin:26px 0 4px;font-weight:600}
.book .prog{text-align:center;font-size:.68rem;letter-spacing:.18em;text-transform:uppercase;color:var(--accent);font-weight:700;margin-bottom:18px}
.chap{margin:26px 0}
.chap .cn{font-size:.72rem;letter-spacing:.15em;text-transform:uppercase;color:var(--soft);
font-weight:700;text-align:center;margin:34px 0 14px}
.chap .cn::before,.chap .cn::after{content:"\\2014";margin:0 10px;color:var(--rule)}
.vtext{text-align:justify;hyphens:auto}
.v{font-size:.62em;vertical-align:super;color:var(--accent);font-weight:700;margin:0 3px 0 6px;
line-height:0;font-family:Georgia,serif}
.v.first{margin-left:0}
.totop{display:block;text-align:center;font-size:.75rem;color:var(--soft);text-decoration:none;
margin:10px 0 6px;letter-spacing:.1em}
.totop:hover{color:var(--accent)}
.pivot{margin:44px auto;max-width:600px;text-align:center;padding:22px 26px;
border:1px solid var(--s3);border-top:5px solid var(--s3);border-radius:12px;background:#f4eff6}
.pivot .k{font-size:.68rem;letter-spacing:.2em;text-transform:uppercase;color:var(--s3);font-weight:700}
.pivot .t{font-size:1.28rem;font-weight:600;margin:6px 0 8px;color:#4a3556}
.pivot .d{font-size:.92rem;color:var(--soft);font-style:italic;line-height:1.5}
/* front & back matter */
.matter{background:var(--paper);border-bottom:1px solid var(--rule);padding:52px 22px}
.matter .inner{max-width:680px;margin:0 auto}
.matter h2.mt{text-align:center;font-size:1.7rem;font-weight:600;margin:0 0 6px}
.matter .mtsub{text-align:center;color:var(--soft);font-style:italic;font-size:.95rem;margin:0 0 30px}
.matter h3.mh{font-size:1.05rem;font-weight:600;margin:26px 0 6px;color:#4a3556}
.matter p.mp{margin:0 0 8px;font-size:1rem}
.tl{margin:6px 0 0;border-left:2px solid var(--rule);padding-left:0}
.tl .row{position:relative;padding:12px 0 12px 26px;border-left:3px solid var(--accent);margin-left:2px}
.tl .row.pph{--accent:var(--s1)}.tl .row.myst{--accent:var(--s3)}.tl .row.hid{--accent:#9a8fa8}
.tl .era{font-weight:600;font-size:1rem}
.tl .tag{display:inline-block;font-size:.64rem;letter-spacing:.14em;text-transform:uppercase;font-weight:700;
color:#fff;background:var(--accent);border-radius:10px;padding:2px 9px;margin-left:8px;vertical-align:middle}
.tl .td{color:var(--soft);font-size:.92rem;margin-top:3px}
dl.gloss{margin:0}
dl.gloss dt{font-weight:700;margin-top:18px;color:#4a3556}
dl.gloss dd{margin:4px 0 0;color:var(--ink);font-size:.97rem}
.plan .step{border:1px solid var(--rule);border-left:4px solid var(--s3);border-radius:8px;padding:12px 16px;margin:10px 0;background:#fff}
.plan .st{font-weight:600}
.plan .sb{font-size:.9rem;color:var(--accent);font-weight:600;margin:2px 0}
.plan .sw{font-size:.92rem;color:var(--soft)}
/* book intro */
.bookintro{max-width:600px;margin:0 auto 8px;background:#faf6f0;border:1px solid var(--rule);
border-left:4px solid var(--accent);border-radius:8px;padding:14px 18px}
.bookintro .bi{font-size:.99rem;line-height:1.55}
.bookintro .bk{display:block;margin-top:8px;font-size:.78rem;letter-spacing:.06em;color:var(--accent);font-weight:700}
/* chapter verse/paragraph toggle */
.ctrlrow{text-align:right;margin:-4px 0 10px}
.vtoggle{font-family:inherit;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;
color:var(--soft);background:#fff;border:1px solid var(--rule);border-radius:16px;padding:4px 13px;
cursor:pointer;transition:.15s;-webkit-appearance:none}
.vtoggle:hover{border-color:var(--accent);color:var(--accent)}
.vtoggle::before{content:"\\2630";margin-right:7px;font-size:.9em;vertical-align:-1px}
.chap.verse .vtoggle::before{content:"\\00B6"}
.vu{display:inline}
.chap.verse .vtext{text-align:left;hyphens:none}
.chap.verse .vu{display:block;padding-left:2.6em;text-indent:-2.6em;margin:.34em 0;line-height:1.5}
.chap.verse .v{font-size:.82em;vertical-align:baseline;line-height:inherit;margin:0 .55em 0 0;
display:inline-block;min-width:2.05em;text-align:right}
.chap.verse .v.first{margin-left:0}
.chap.verse .v{cursor:pointer;border-radius:3px;transition:background .12s}
.chap.verse .v:hover{background:#efe7f3;text-decoration:underline}
.vhint{display:none;font-size:.7rem;color:var(--soft);font-style:italic;margin-right:auto;letter-spacing:.02em}
.chap.verse .vhint{display:inline}
.ctrlrow{display:flex;align-items:center;gap:12px;justify-content:flex-end}
.vpanel{display:block;margin:8px 0 14px 0;padding:12px 15px;background:#f6f1f8;border:1px solid #e0d3e8;
border-left:3px solid var(--s3);border-radius:8px;text-indent:0;font-size:.9rem;line-height:1.5}
.vpanel .vn{color:#3f2b4b;margin-bottom:8px}
.vpanel .vn.muted{color:var(--soft);font-style:italic;margin:0}
.vpanel .vbl{display:block;font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--soft);font-weight:700;margin-bottom:6px}
.vpanel .vb{display:inline-block;margin:3px 6px 3px 0;padding:5px 11px;background:#fff;border:1px solid #c9b7d6;
border-radius:14px;color:#5a4270;font-weight:600;font-size:.82rem;text-decoration:none}
.vpanel .vb:hover{border-color:var(--s3);color:#3f2b4b}
@media print{.ctrlrow{display:none}.vpanel{display:none}}
/* Grace Ambassadors commentary layer */
.commentary{max-width:600px;margin:0 auto 8px;background:#eef3f4;border:1px solid #cddbdc;
border-left:4px solid #4d8b8f;border-radius:8px;padding:13px 17px}
.commentary .clbl{font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;font-weight:700;color:#3f7377}
.commentary .cbody{font-size:.95rem;margin:4px 0 0;line-height:1.5}
.commentary .csrc{font-size:.93rem;margin:6px 0;line-height:1.45}
.commentary .csd{color:#5b6f70;font-size:.85rem}
.commentary a{color:#2f6367;font-weight:600;text-decoration:none;border-bottom:1px solid #a9cccd}
.commentary a:hover{color:#204547}
.commentary .cnote{display:block;margin-top:8px;font-size:.79rem;color:#6b7f80;font-style:italic}
body.comm-off .commentary{display:none}
body:not(.show-ga) .src-ga{display:none}
body:not(.show-lf) .src-lf{display:none}
body:not(.show-sg) .src-sg{display:none}
.commbar{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;align-items:center;margin-top:14px}
.commbar .lbl{font-size:.68rem;letter-spacing:.14em;text-transform:uppercase;color:var(--soft);font-weight:700}
.srcchip{font-family:inherit;font-size:.7rem;letter-spacing:.05em;font-weight:700;color:#2f6367;background:#e6f0f0;
border:1px solid #a9cccd;border-radius:16px;padding:5px 13px;cursor:pointer;-webkit-appearance:none;transition:.15s}
.srcchip:hover{border-color:#4d8b8f}
.srcchip.chip-off{background:#fff;color:#a7b0b0;border-color:var(--rule);text-decoration:line-through}
@media print{.commbar{display:none}}
.commtoggle{font-family:inherit;font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;
color:#fff;background:#4d8b8f;border:1px solid #4d8b8f;border-radius:18px;padding:7px 16px;cursor:pointer;
margin-top:16px;-webkit-appearance:none;transition:.15s}
.commtoggle:hover{background:#3f7377;border-color:#3f7377}
body.comm-off .commtoggle{background:#fff;color:#4d8b8f}
@media print{.commtoggle{display:none}}
footer{text-align:center;padding:60px 22px;color:var(--soft);font-size:.85rem;border-top:1px solid var(--rule);margin-top:40px}
@media print{
 body{background:#fff;font-size:11.5pt;line-height:1.4}
 nav.toc a{border:none;padding:0 6px}
 .section-divider{page-break-before:always;padding:120px 0 40px}
 .book{page-break-inside:auto}
 .totop{display:none}
 header.masthead{padding-top:20px}
}
</style></head><body class="show-ga show-lf show-sg">''')

# masthead
parts.append('''<header class="masthead"><div class="wrap">
<h1>The KJV Rightly Divided</h1>
<p class="sub">The Holy Scriptures reordered according to the two programs of God</p>
<p class="verse">“Study to shew thyself approved unto God, a workman that needeth not to be ashamed, rightly dividing the word of truth.” &nbsp;— 2 Timothy 2:15</p>
<button class="commtoggle" type="button" onclick="toggleComm(this)">Commentary: On</button>
<div class="commbar"><span class="lbl">Sources:</span>
<button class="srcchip" type="button" onclick="toggleSrc(this,'ga')">Grace Ambassadors</button>
<button class="srcchip" type="button" onclick="toggleSrc(this,'lf')">Les Feldick</button>
<button class="srcchip" type="button" onclick="toggleSrc(this,'sg')">Sufficient Grace</button>
</div>
</div></header>''')

# FRONT MATTER — How to Read
parts.append('<section class="matter s3"><div class="inner">')
parts.append(f'<h2 class="mt">{html.escape(content.HOWTO_TITLE)}</h2><p class="mtsub">Rightly dividing the word of truth &mdash; 2 Timothy 2:15</p>')
for h,body in content.HOWTO:
    parts.append(f'<h3 class="mh">{html.escape(h)}</h3><p class="mp">{body}</p>')
parts.append('</div></section>')

# FRONT MATTER — Timeline
_tlcls = {"Hidden":"hid","Prophecy":"pph","The Mystery":"myst","Prophecy resumes":"pph"}
parts.append('<section class="matter"><div class="inner">')
parts.append(f'<h2 class="mt">{html.escape(content.TIMELINE_TITLE)}</h2><p class="mtsub">The parenthesis of grace, set within the line of prophecy</p><div class="tl">')
for era,tag,desc in content.TIMELINE:
    cls = _tlcls.get(tag,"pph")
    parts.append(f'<div class="row {cls}"><span class="era">{html.escape(era)}</span><span class="tag">{html.escape(tag)}</span><div class="td">{html.escape(desc)}</div></div>')
parts.append('</div></div></section>')

# TOC
parts.append('<nav class="toc"><h2>Contents</h2>')
for rn, name, desc, books in SECTIONS:
    sc = {"I":"s1","II":"s2","III":"s3","IV":"s4"}[rn]
    parts.append(f'<div class="toc-sec {sc}"><div class="lbl"><span class="rn">SECTION {rn}</span><span class="nm">{html.escape(name)}</span></div><div class="booklist">')
    for b in books:
        parts.append(f'<a href="#{slug(b)}">{html.escape(b)}</a>')
    parts.append('</div></div>')
parts.append('</nav>')

# body
for rn, name, desc, books in SECTIONS:
    sc = {"I":"s1","II":"s2","III":"s3","IV":"s4"}[rn]
    parts.append(f'<div class="section-divider {sc}"><div class="rn">SECTION {rn}</div><h2>{html.escape(name)}</h2><p>{desc}</p><div class="bar"></div></div>')
    for b in books:
        d = load(b)
        parts.append(f'<article class="book {sc}" id="{slug(b)}" data-book="{html.escape(b)}">')
        parts.append(f'<h3 class="bt">{html.escape(b)}</h3><div class="prog">Section {rn} &middot; {html.escape(name)}</div>')
        intro = content.INTROS.get(b)
        if intro:
            parts.append(f'<div class="bookintro {sc}"><div class="bi">{intro["t"]}<span class="bk">Key: {html.escape(intro["k"])}</span></div></div>')
        rows = []
        ga = content.GA_LINKS.get(b)
        if ga:
            rows.append(("ga","Grace Ambassadors", content.GA_BASE+ga, "audio, outlines &amp; written commentary"))
        if content.LF_COVERS_ALL:
            lf_url = content.LF_SEARCH + urllib.parse.quote_plus(b)
            rows.append(("lf","Les Feldick", lf_url, f"lessons on {html.escape(b)} (full 66-book study)"))
        sg = content.SG_LINKS.get(b)
        if sg:
            rows.append(("sg","Sufficient Grace", content.SG_BASE+sg, "verse-by-verse Pauline study"))
        if rows:
            parts.append('<div class="commentary"><span class="clbl">Commentary</span>')
            for cls,label,url,desc in rows:
                parts.append(f'<div class="csrc src-{cls}"><a href="{url}" target="_blank" rel="noopener">{label} &#8599;</a> <span class="csd">&mdash; {desc}</span></div>')
            parts.append('<span class="cnote">Each links to the ministry&rsquo;s own site; their material is referenced, not reproduced.</span></div>')
        for ch in d["chapters"]:
            if b == "Acts" and ch["chapter"] == "9":
                parts.append('<div class="pivot"><div class="k">The Body of Christ Begins</div>'
                             '<div class="t">Acts 9 &mdash; The Risen Lord Raises Up Paul</div>'
                             '<div class="d">From this point the prophetic program to Israel gives way to '
                             'the dispensation of the mystery, revealed to the apostle Paul (Ephesians 3:1-9). '
                             'Everything before is Israel&rsquo;s kingdom line; the Body of Christ begins here.</div></div>')
            parts.append(f'<div class="chap" data-chap="{ch["chapter"]}">')
            if len(d["chapters"])>1:
                parts.append(f'<div class="cn">Chapter {ch["chapter"]}</div>')
            parts.append('<div class="ctrlrow"><span class="vhint">tap a verse number for commentary &rsaquo;</span><button class="vtoggle" type="button" onclick="toggleChap(this)" aria-expanded="false">Verse view</button></div>')
            parts.append('<p class="vtext">')
            for i,v in enumerate(ch["verses"]):
                cls = "v first" if i==0 else "v"
                parts.append(f'<span class="vu"><span class="{cls}">{v["verse"]}</span>{html.escape(v["text"])} </span>')
            parts.append('</p></div>')
        parts.append('<a class="totop" href="#top">↑ Contents</a>')
        parts.append('</article>')

# BACK MATTER — Reading plan
parts.append('<section class="matter s3"><div class="inner plan">')
parts.append(f'<h2 class="mt">{html.escape(content.PLAN_TITLE)}</h2><p class="mtsub">{html.escape(content.PLAN_INTRO)}</p>')
for st,books,why in content.PLAN:
    parts.append(f'<div class="step"><div class="st">{html.escape(st)}</div><div class="sb">{html.escape(books)}</div><div class="sw">{html.escape(why)}</div></div>')
parts.append('</div></section>')

# BACK MATTER — Glossary
parts.append('<section class="matter"><div class="inner">')
parts.append(f'<h2 class="mt">{html.escape(content.GLOSSARY_TITLE)}</h2><p class="mtsub">The vocabulary of right division</p><dl class="gloss">')
for term,defn in content.GLOSSARY:
    parts.append(f'<dt>{html.escape(term)}</dt><dd>{defn}</dd>')
parts.append('</dl></div></section>')

parts.append('<footer>King James Version — Public Domain &middot; Reordered on the mid-Acts (Acts 9) right-division framework &middot; <a href="chart.html" style="color:inherit;font-weight:600">Companion Chart &rarr;</a><br><br>Study to shew thyself approved.</footer>')
script = "<script>\n"
script += "var COV_GA=" + json.dumps(list(content.GA_LINKS.keys())) + ";\n"
script += "var COV_SG=" + json.dumps(list(content.SG_LINKS.keys())) + ";\n"
script += "var NOTES=" + json.dumps(content.NOTES, ensure_ascii=False) + ";\n"
script += r'''var SEARCH={ga:'https://www.google.com/search?q=site:graceambassadors.com+',lf:'https://www.google.com/search?q=site:lesfeldick.org+',sg:'https://www.google.com/search?q=site:sufficientgracebiblefellowship.com+'};
var SRCNAME={ga:'Grace Ambassadors',lf:'Les Feldick',sg:'Sufficient Grace'};
function toggleChap(btn){var chap=btn.closest('.chap');var on=chap.classList.toggle('verse');btn.textContent=on?'Paragraph view':'Verse view';btn.setAttribute('aria-expanded',on?'true':'false');}
function toggleComm(btn){var off=document.body.classList.toggle('comm-off');btn.textContent=off?'Commentary: Off':'Commentary: On';}
function toggleSrc(btn,src){document.body.classList.toggle('show-'+src);btn.classList.toggle('chip-off',!document.body.classList.contains('show-'+src));refreshComm();rebuildPanels();}
function refreshComm(){document.querySelectorAll('.commentary').forEach(function(c){var vis=false;c.querySelectorAll('.csrc').forEach(function(r){if(getComputedStyle(r).display!=='none')vis=true;});c.style.display=vis?'':'none';});}
function covers(src,book){if(src==='lf')return true;if(src==='ga')return COV_GA.indexOf(book)>=0;if(src==='sg')return COV_SG.indexOf(book)>=0;return false;}
function verseInfo(vu){var art=vu.closest('article.book');var chap=vu.closest('.chap');var book=art?art.getAttribute('data-book'):'';var c=chap?(chap.getAttribute('data-chap')||'1'):'1';var vs=vu.querySelector('.v');var v=vs?vs.textContent.trim():'';return {book:book,ref:book+' '+c+':'+v};}
function buildPanel(vu){var info=verseInfo(vu);var p=document.createElement('div');p.className='vpanel';p.setAttribute('data-ref',info.ref);var h='';var note=NOTES[info.ref];if(note){h+='<div class="vn">'+note+'</div>';}var btns='';['ga','lf','sg'].forEach(function(src){if(covers(src,info.book)&&document.body.classList.contains('show-'+src)){var url=SEARCH[src]+encodeURIComponent('"'+info.ref+'"');btns+='<a class="vb" href="'+url+'" target="_blank" rel="noopener">'+SRCNAME[src]+' ↗</a>';}});if(btns){h+='<div><span class="vbl">Commentary on '+info.ref+'</span>'+btns+'</div>';}if(!note&&!btns){h+='<div class="vn muted">No commentary source is enabled for this verse.</div>';}p.innerHTML=h;return p;}
function rebuildPanels(){document.querySelectorAll('.vpanel').forEach(function(p){var vu=p.parentNode;p.remove();if(vu&&vu.classList&&vu.classList.contains('vu'))vu.appendChild(buildPanel(vu));});}
document.addEventListener('click',function(e){var t=e.target;if(!t||!t.closest)return;var v=t.closest('.v');if(!v)return;var vu=v.closest('.vu');if(!vu)return;var chap=vu.closest('.chap');if(!chap||!chap.classList.contains('verse'))return;e.preventDefault();var ex=vu.querySelector('.vpanel');if(ex){ex.remove();return;}vu.appendChild(buildPanel(vu));});
refreshComm();
</script>'''
parts.append(script)
parts.append('</body></html>')

out = "".join(parts)
open("KJV_Rightly_Divided.html","w",encoding="utf-8").write(out)
print("bytes:", len(out.encode()))
print("MB:", round(len(out.encode())/1048576,2))
