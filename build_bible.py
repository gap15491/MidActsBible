import json, os, html, urllib.parse, datetime
import content
BUILD_STAMP = datetime.datetime.utcnow().strftime("Updated %d %b %Y %H:%M UTC")

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
html{scroll-behavior:auto}
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
.tocbtn{font-family:inherit;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;
color:var(--soft);background:#fff;border:1px solid var(--rule);border-radius:16px;padding:4px 13px;
text-decoration:none;transition:.15s;white-space:nowrap}
.tocbtn:hover{border-color:var(--accent);color:var(--accent)}
@media print{.tocbtn{display:none}}
.floatcontents{position:fixed;right:18px;bottom:18px;z-index:100;background:var(--s3);color:#fff;
padding:11px 18px;border-radius:26px;font-size:.74rem;letter-spacing:.12em;text-transform:uppercase;
font-weight:700;text-decoration:none;box-shadow:0 3px 12px rgba(60,40,80,.28);font-family:inherit}
.floatcontents:hover{background:#7a5a89}
@media print{.floatcontents{display:none}}
.buildstamp{margin-top:14px;font-size:.7rem;letter-spacing:.1em;color:var(--soft);opacity:.8}
/* auth + notes */
#authbar{position:fixed;top:12px;right:14px;z-index:110;font-size:.8rem}
#authinfo{background:rgba(255,255,255,.93);border:1px solid var(--rule);border-radius:20px;padding:6px 14px;
box-shadow:0 1px 6px rgba(0,0,0,.08);display:inline-block}
.whoami{color:var(--s3);font-weight:600}
.linkbtn{background:none;border:none;color:var(--s3);font-weight:600;cursor:pointer;font-family:inherit;font-size:inherit;text-decoration:underline;padding:0}
.linkbtn:hover{color:#5a4270}
#authmodal,#booknotemodal{position:fixed;inset:0;background:rgba(30,22,40,.45);z-index:200;display:flex;align-items:center;justify-content:center}
#authmodal.hidden,#booknotemodal.hidden{display:none}
.modalbox{background:var(--paper);border-radius:14px;padding:28px 26px;width:320px;max-width:92vw;position:relative;box-shadow:0 10px 40px rgba(0,0,0,.3)}
.modalbox h3{margin:0 0 16px;font-size:1.3rem;font-weight:600;text-align:center}
.booknotebox{width:460px}
.booknotebox .mynote{margin-top:0}
.booknotebox .mnta{min-height:150px}
.modalbox input{display:block;width:100%;padding:10px 12px;margin:0 0 12px;border:1px solid var(--rule);border-radius:8px;font-size:1rem;font-family:inherit;box-sizing:border-box}
.modalbox input:focus{outline:none;border-color:var(--s3)}
#authsubmit{width:100%;padding:11px;background:var(--s3);color:#fff;border:none;border-radius:8px;font-weight:700;font-size:.95rem;cursor:pointer;font-family:inherit}
#authsubmit:hover{background:#7a5a89}
.autherr{color:#a7443a;font-size:.85rem;min-height:1.1em;margin-bottom:8px;text-align:center}
#authtoggle{display:block;text-align:center;margin-top:14px;font-size:.85rem;cursor:pointer}
.modalx{position:absolute;top:8px;right:12px;background:none;border:none;font-size:1.4rem;color:var(--soft);cursor:pointer;line-height:1}
.chapnotebtn{font-family:inherit;font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;
color:#3f7377;background:#eef3f4;border:1px solid #cddbdc;border-radius:16px;padding:4px 12px;cursor:pointer;white-space:nowrap}
.chapnotebtn:hover{border-color:#4d8b8f}
.chapnotebtn.has-note{background:#4d8b8f;color:#fff;border-color:#4d8b8f}
.chapnotepanel{max-width:600px;margin:8px auto 16px}
.mynote{background:#f3f7f7;border:1px solid #cddbdc;border-left:3px solid #4d8b8f;border-radius:8px;padding:10px 13px;margin-top:10px;text-indent:0}
.mynote .mnlbl{display:block;font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:#3f7377;font-weight:700;margin-bottom:6px}
.mynote .mnlogin{font-size:.9rem;color:var(--soft)}
.mynote .mnta{width:100%;min-height:64px;border:1px solid #cddbdc;border-radius:6px;padding:8px;font-family:inherit;font-size:.92rem;resize:vertical;box-sizing:border-box}
.mynote .mnta:focus{outline:none;border-color:#4d8b8f}
.mynote .mnrow{display:flex;align-items:center;gap:8px;margin-top:8px}
.mynote .mnsave{background:#4d8b8f;color:#fff;border:none;border-radius:14px;padding:5px 14px;font-weight:600;font-size:.82rem;cursor:pointer;font-family:inherit}
.mynote .mnsave:hover{background:#3f7377}
.mynote .mndel{background:#fff;color:#8a6b6b;border:1px solid #d8c4c4;border-radius:14px;padding:5px 12px;font-size:.82rem;cursor:pointer;font-family:inherit}
.mynote .mnstatus{font-size:.8rem;color:var(--soft);font-style:italic}
.v.has-note::after{content:"\\2022";color:#4d8b8f;font-size:.7em;vertical-align:super;margin-left:1px}
@media print{#authbar,#authmodal,.chapnotebtn,.mynote{display:none}}
/* --- drill-down navigation: books -> chapters -> verses --- */
#readbar{display:none;position:sticky;top:0;z-index:90;align-items:center;gap:10px;
background:rgba(255,253,249,.97);border-bottom:1px solid var(--rule);padding:10px 16px}
body.reading #readbar{display:flex}
#readbar .rb{font-family:inherit;font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;
color:var(--s3);background:#fff;border:1px solid var(--rule);border-radius:16px;padding:6px 14px;cursor:pointer}
#readbar .rb:hover{border-color:var(--s3)}
#readbar .rbcrumb{font-weight:600;color:var(--ink);font-size:.95rem}
body.home article.book,body.home .section-divider,body.home .floatcontents{display:none}
body.reading header.masthead,body.reading .matter,body.reading nav.toc,body.reading .section-divider{display:none}
body.reading article.book{display:none}
body.reading article.book.active{display:block}
body.reading .chap{display:none}
body.reading .chap.active{display:block}
body.chapter .chapgrid,body.chapter .bookintro,body.chapter .commentary{display:none}
.chapgrid{max-width:640px;margin:16px auto 24px;display:flex;flex-wrap:wrap;gap:9px;justify-content:center}
.gridlabel{text-align:center;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;color:var(--soft);font-weight:700;margin:6px 0 2px}
.chapgrid .chapnum{font-family:inherit;font-size:1rem;font-weight:600;min-width:48px;height:48px;padding:0 6px;
border:1px solid var(--rule);background:#fff;border-radius:10px;cursor:pointer;color:var(--ink);transition:.12s}
.chapgrid .chapnum:hover{border-color:var(--s3);color:var(--s3);background:#f6f1f8}
.chapgrid .chapnum.has-note{border-color:#4d8b8f}
.chapgrid .chapnum.has-note::after{content:"\\2022";color:#4d8b8f;margin-left:2px;font-size:.8em;vertical-align:super}
.tocbtn{cursor:pointer}
@media print{#readbar{display:none}}
/* --- Strong's concordance --- */
.strbtn{font-family:inherit;font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;
color:#7a5a3a;background:#f4ede1;border:1px solid #e0d3c0;border-radius:12px;padding:2px 9px;margin-left:8px;cursor:pointer;vertical-align:middle}
.strbtn:hover{border-color:#b8925f;color:#5a4020}
.strbtn.on{background:#b8925f;color:#fff;border-color:#b8925f}
.chap:not(.verse) .strbtn{display:none}
.strongspanel{display:block;margin:8px 0 16px;padding:12px 15px;background:#fbf7f0;border:1px solid #e6d9c5;
border-left:3px solid #b8925f;border-radius:8px;text-indent:0;font-size:.92rem;line-height:1.5}
.strongspanel .sp-title{font-size:.66rem;letter-spacing:.14em;text-transform:uppercase;color:#a07a4a;font-weight:700;margin-bottom:8px}
.strongspanel .sw{padding:8px 0;border-top:1px solid #efe4d2}
.strongspanel .sw:first-of-type{border-top:none}
.strongspanel .sw-en{font-weight:700;color:#33281a}
.strongspanel .sw-e{margin-top:3px}
.strongspanel .sw-num{font-size:.7rem;font-weight:700;color:#8a6634;background:#f0e6d4;border-radius:8px;padding:1px 7px;margin-right:6px}
.strongspanel .sw-o{font-size:1.08rem;color:#4a3a28;margin-right:6px}
.strongspanel .sw-t{font-style:italic;color:#6b5a44;margin-right:6px}
.strongspanel .sw-p{font-size:.8rem;color:#8a7a60}
.strongspanel .sw-d{margin-top:2px;color:#33281a}
.strongspanel .sw-u{margin-top:2px;font-size:.86rem;color:#6b5a44}
@media print{.strbtn,.strongspanel{display:none}}
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
</style></head><body class="show-ga show-lf show-sg home">
<a class="floatcontents" href="#/" onclick="showHome();return false;" title="Back to the book list">&#9776;&nbsp;Books</a>
<div id="readbar"><button class="rb" type="button" onclick="showHome()">&#9776; Books</button><button class="rb" id="rbChapters" type="button" onclick="showChapters()">Chapters</button><button class="rb" id="rbBookNote" type="button" onclick="toggleBookNote()">&#9998; Book note</button><span class="rbcrumb" id="rbCrumb"></span></div>
<div id="booknotemodal" class="hidden" onclick="if(event.target===this)closeBookNote()"><div class="modalbox booknotebox"><button class="modalx" type="button" onclick="closeBookNote()">&times;</button><h3 id="bnTitle">Book note</h3><div class="mynote" id="bnBox" data-kind="book" data-book="" data-chap="0" data-verse=""></div></div></div>
<div id="authbar"><span id="authinfo"></span></div>
<div id="authmodal" class="hidden">
  <div class="modalbox">
    <button class="modalx" type="button" onclick="closeAuth()">&times;</button>
    <h3 id="authtitle">Log in</h3>
    <input id="authemail" type="email" placeholder="Email" autocomplete="username">
    <input id="authpass" type="password" placeholder="Password (8+ characters)" autocomplete="current-password">
    <div id="autherr" class="autherr"></div>
    <button id="authsubmit" type="button" onclick="submitAuth()">Log in</button>
    <a id="authtoggle" class="linkbtn" onclick="toggleAuthMode()">Need an account? Register</a>
  </div>
</div>''')

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
<div class="buildstamp">''' + html.escape(BUILD_STAMP) + '''</div>
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
parts.append('<nav class="toc" id="contents"><h2>Contents</h2>')
for rn, name, desc, books in SECTIONS:
    sc = {"I":"s1","II":"s2","III":"s3","IV":"s4"}[rn]
    parts.append(f'<div class="toc-sec {sc}"><div class="lbl"><span class="rn">SECTION {rn}</span><span class="nm">{html.escape(name)}</span></div><div class="booklist">')
    for b in books:
        parts.append(f'<a class="toclink" href="#/" data-book="{html.escape(b)}">{html.escape(b)}</a>')
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
        # chapter picker grid (shown in book view)
        parts.append(f'<div class="gridlabel">Select a chapter</div><div class="chapgrid" data-book="{html.escape(b)}">')
        for ch in d["chapters"]:
            parts.append(f'<button class="chapnum" type="button" data-chap="{ch["chapter"]}">{ch["chapter"]}</button>')
        parts.append('</div>')
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
            parts.append('<div class="ctrlrow"><span class="vhint">tap a verse number for commentary &rsaquo;</span><button class="chapnotebtn" type="button" onclick="toggleChapNote(this)">&#9998; Note</button><button class="tocbtn" type="button" onclick="showHome()">&#9776; Books</button><button class="vtoggle" type="button" onclick="toggleChap(this)" aria-expanded="false">Verse view</button></div>')
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
function verseInfo(vu){var art=vu.closest('article.book');var chap=vu.closest('.chap');var book=art?art.getAttribute('data-book'):'';var c=chap?(chap.getAttribute('data-chap')||'1'):'1';var vs=vu.querySelector('.v');var v=vs?vs.textContent.trim():'';return {book:book,ref:book+' '+c+':'+v,c:c,v:v};}
function buildPanel(vu){var info=verseInfo(vu);var p=document.createElement('div');p.className='vpanel';p.setAttribute('data-ref',info.ref);var h='';var note=NOTES[info.ref];if(note){h+='<div class="vn">'+note+'</div>';}var btns='';['ga','lf','sg'].forEach(function(src){if(covers(src,info.book)&&document.body.classList.contains('show-'+src)){var url=SEARCH[src]+encodeURIComponent('"'+info.ref+'"');btns+='<a class="vb" href="'+url+'" target="_blank" rel="noopener">'+SRCNAME[src]+' ↗</a>';}});if(btns){h+='<div><span class="vbl">Commentary on '+info.ref+'</span>'+btns+'</div>';}if(!note&&!btns){h+='<div class="vn muted">No commentary source is enabled for this verse.</div>';}p.innerHTML=h;var nb=document.createElement('div');nb.className='mynote';nb.setAttribute('data-kind','verse');nb.setAttribute('data-book',info.book);nb.setAttribute('data-chap',info.c);nb.setAttribute('data-verse',info.v);p.appendChild(nb);if(window.renderNoteBox){renderNoteBox(nb);loadNoteBox(nb);}return p;}
function rebuildPanels(){document.querySelectorAll('.vpanel').forEach(function(p){var vu=p.parentNode;p.remove();if(vu&&vu.classList&&vu.classList.contains('vu'))vu.appendChild(buildPanel(vu));});}
document.addEventListener('click',function(e){var t=e.target;if(!t||!t.closest)return;var v=t.closest('.v');if(!v)return;var vu=v.closest('.vu');if(!vu)return;var chap=vu.closest('.chap');if(!chap||!chap.classList.contains('verse'))return;e.preventDefault();var ex=vu.querySelector('.vpanel');if(ex){ex.remove();return;}vu.appendChild(buildPanel(vu));});
refreshComm();
</script>'''
parts.append(script)

parts.append(r'''<script>
/* ---------- auth + per-user notes ---------- */
var ME=null;        // current user's email or null
var NC={};          // note cache: "Book|chap" -> {loaded, chapter_note, verses:{}}
function esc(s){return (s||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
async function api(method,path,body){
  var opt={method:method,headers:{'Content-Type':'application/json'},credentials:'same-origin'};
  if(body)opt.body=JSON.stringify(body);
  var r=await fetch(path,opt);
  var j={}; try{j=await r.json();}catch(e){}
  if(!r.ok) throw (j.error||('Error '+r.status));
  return j;
}
async function refreshAuth(){try{var j=await api('GET','/api/me');ME=j.email;}catch(e){ME=null;}renderAuth();}
function renderAuth(){
  var el=document.getElementById('authinfo'); if(!el)return;
  if(ME){el.innerHTML='<span class="whoami">'+esc(ME)+'</span> &middot; <button class="linkbtn" onclick="doLogout()">Log out</button>';}
  else{el.innerHTML='<button class="linkbtn" onclick="openAuth()">Log in / Register</button>';}
}
var authMode='login';
function openAuth(){document.getElementById('authmodal').classList.remove('hidden');setAuthMode('login');document.getElementById('authemail').focus();}
function closeAuth(){document.getElementById('authmodal').classList.add('hidden');seterr('');}
function setAuthMode(m){authMode=m;
  document.getElementById('authtitle').textContent=m==='login'?'Log in':'Create account';
  document.getElementById('authsubmit').textContent=m==='login'?'Log in':'Register';
  document.getElementById('authtoggle').textContent=m==='login'?'Need an account? Register':'Have an account? Log in';
  seterr('');}
function toggleAuthMode(){setAuthMode(authMode==='login'?'register':'login');}
function seterr(m){var e=document.getElementById('autherr');if(e)e.textContent=m||'';}
async function submitAuth(){
  var email=document.getElementById('authemail').value.trim();
  var pass=document.getElementById('authpass').value;
  try{var j=await api('POST',authMode==='login'?'/api/login':'/api/register',{email:email,password:pass});
    ME=j.email;closeAuth();NC={};clearIndicators();renderAuth();reloadOpenNotes();
  }catch(e){seterr(String(e));}
}
async function doLogout(){try{await api('POST','/api/logout');}catch(e){}ME=null;NC={};clearIndicators();renderAuth();reloadOpenNotes();}
async function ensureNotes(book,chap){
  var k=book+'|'+chap; if(NC[k]&&NC[k].loaded)return NC[k];
  if(!ME){NC[k]={loaded:true,chapter_note:null,verses:{}};return NC[k];}
  try{var j=await api('GET','/api/notes?book='+encodeURIComponent(book)+'&chapter='+chap);
    NC[k]={loaded:true,chapter_note:j.chapter_note,verses:j.verses||{}};}
  catch(e){NC[k]={loaded:true,chapter_note:null,verses:{}};}
  return NC[k];
}
function renderNoteBox(nb){
  var book=nb.getAttribute('data-book'),chap=nb.getAttribute('data-chap'),verse=nb.getAttribute('data-verse');
  var kind=nb.getAttribute('data-kind')||'verse';
  if(!ME){nb.innerHTML='<span class="mnlbl">My note</span><div class="mnlogin"><button class="linkbtn" onclick="openAuth()">Log in</button> to save your own notes.</div>';return;}
  var k=book+'|'+chap;var val='';
  if(NC[k]&&NC[k].loaded){val=(kind==='verse'?((NC[k].verses||{})[verse]||''):(NC[k].chapter_note||''));}
  var suffix=(kind==='chapter'?' &middot; whole chapter':(kind==='book'?' &middot; whole book':''));
  nb.innerHTML='<span class="mnlbl">My note'+suffix+'</span>'+
    '<textarea class="mnta" placeholder="Write a private note…">'+esc(val)+'</textarea>'+
    '<div class="mnrow"><button class="mnsave" onclick="saveNote(this)">Save</button>'+
    '<button class="mndel" onclick="deleteNote(this)">Delete</button><span class="mnstatus"></span></div>';
}
async function loadNoteBox(nb){var book=nb.getAttribute('data-book'),chap=nb.getAttribute('data-chap');if(!book)return;await ensureNotes(book,chap);renderNoteBox(nb);}
async function saveNote(btn){
  var nb=btn.closest('.mynote');var ta=nb.querySelector('.mnta');
  var book=nb.getAttribute('data-book'),chap=nb.getAttribute('data-chap'),verse=nb.getAttribute('data-verse');
  var kind=nb.getAttribute('data-kind')||'verse';var status=nb.querySelector('.mnstatus');status.textContent='Saving…';
  try{await api('PUT','/api/notes',{book:book,chapter:parseInt(chap),verse:kind==='verse'?parseInt(verse):null,text:ta.value});
    var k=book+'|'+chap;NC[k]=NC[k]||{loaded:true,chapter_note:null,verses:{}};
    if(kind!=='verse'){NC[k].chapter_note=ta.value.trim()||null;}
    else{if(ta.value.trim())NC[k].verses[verse]=ta.value.trim();else delete NC[k].verses[verse];}
    status.textContent=ta.value.trim()?'Saved':'Cleared';markIndicators(book,chap);
  }catch(e){status.textContent=String(e);}
}
async function deleteNote(btn){var nb=btn.closest('.mynote');nb.querySelector('.mnta').value='';await saveNote(btn);}
function toggleChapNote(btn){
  if(!ME){openAuth();return;}
  var chap=btn.closest('.chap');var ex=chap.querySelector('.chapnotepanel');if(ex){ex.remove();return;}
  var book=chap.closest('article.book').getAttribute('data-book');var c=chap.getAttribute('data-chap');
  var panel=document.createElement('div');panel.className='chapnotepanel';
  var nb=document.createElement('div');nb.className='mynote';nb.setAttribute('data-kind','chapter');
  nb.setAttribute('data-book',book);nb.setAttribute('data-chap',c);nb.setAttribute('data-verse','');
  panel.appendChild(nb);btn.closest('.ctrlrow').insertAdjacentElement('afterend',panel);
  renderNoteBox(nb);loadNoteBox(nb);
}
function markIndicators(book,chap){
  var k=book+'|'+chap;var c=NC[k];if(!c)return;
  var art=document.querySelector('article.book[data-book="'+book+'"]');if(!art)return;
  var chapEl=art.querySelector('.chap[data-chap="'+chap+'"]');if(!chapEl)return;
  var cbtn=chapEl.querySelector('.chapnotebtn');if(cbtn)cbtn.classList.toggle('has-note',!!c.chapter_note);
  chapEl.querySelectorAll('.vu').forEach(function(vu){var vs=vu.querySelector('.v');if(!vs)return;
    var vn=vs.textContent.trim();vs.classList.toggle('has-note',!!((c.verses||{})[vn]));});
}
function clearIndicators(){document.querySelectorAll('.v.has-note').forEach(function(e){e.classList.remove('has-note');});
  document.querySelectorAll('.chapnotebtn.has-note').forEach(function(e){e.classList.remove('has-note');});}
function reloadOpenNotes(){document.querySelectorAll('.mynote').forEach(function(nb){renderNoteBox(nb);if(ME)loadNoteBox(nb);});
  Object.keys(NC).forEach(function(k){var p=k.split('|');markIndicators(p[0],p[1]);});}
/* lazily flag which chapters hold notes as they scroll into view (logged-in only) */
var noteObserver=new IntersectionObserver(function(entries){
  entries.forEach(function(en){ if(!en.isIntersecting)return; var chapEl=en.target;
    if(!ME){noteObserver.unobserve(chapEl);return;}
    var art=chapEl.closest('article.book');if(!art)return;
    var book=art.getAttribute('data-book');var c=chapEl.getAttribute('data-chap');
    ensureNotes(book,c).then(function(){markIndicators(book,c);});
    noteObserver.unobserve(chapEl);
  });
},{rootMargin:'400px'});
function observeChapters(){document.querySelectorAll('.chap[data-chap]').forEach(function(ch){noteObserver.observe(ch);});}
refreshAuth().then(observeChapters);
</script>''')

parts.append(r'''<script>
/* ---------- drill-down navigation controller ---------- */
var CURBOOK=null, CURCHAP=null;
function bookArticle(book){return document.querySelector('article.book[data-book="'+book+'"]');}
function chapCount(book){var a=bookArticle(book);return a?a.querySelectorAll('.chap').length:0;}
function setMode(mode){document.body.classList.remove('home','reading','book','chapter');
  if(mode==='home')document.body.classList.add('home');else document.body.classList.add('reading',mode);
  var bnm=document.getElementById('booknotemodal');if(bnm)bnm.classList.add('hidden');}
function clearActive(){document.querySelectorAll('article.book.active').forEach(function(a){a.classList.remove('active');});
  document.querySelectorAll('.chap.active').forEach(function(c){c.classList.remove('active');});}
function showHome(){setMode('home');clearActive();CURBOOK=null;CURCHAP=null;if(location.hash)location.hash='';var toc=document.getElementById('contents');if(toc){toc.scrollIntoView(true);}else{window.scrollTo(0,0);}}
function openBook(book){var a=bookArticle(book);if(!a)return;
  if(chapCount(book)<=1){openChapter(book,'1');return;}
  clearActive();a.classList.add('active');CURBOOK=book;CURCHAP=null;setMode('book');
  var nh='#/'+encodeURIComponent(book);if(location.hash!==nh)location.hash=nh;window.scrollTo(0,0);updateReadbar();}
function openChapter(book,chap){var a=bookArticle(book);if(!a)return;
  clearActive();a.classList.add('active');
  var ch=a.querySelector('.chap[data-chap="'+chap+'"]');if(!ch)return;
  ch.classList.add('active','verse');injectStrongsButtons(ch);
  var vt=ch.querySelector('.vtoggle');if(vt){vt.textContent='Paragraph view';vt.setAttribute('aria-expanded','true');}
  CURBOOK=book;CURCHAP=chap;setMode('chapter');
  var nh='#/'+encodeURIComponent(book)+'/'+chap;if(location.hash!==nh)location.hash=nh;window.scrollTo(0,0);updateReadbar();
  if(window.ensureNotes&&ME){ensureNotes(book,parseInt(chap)).then(function(){markIndicators(book,chap);});}}
function showChapters(){if(CURBOOK)openBook(CURBOOK);}
function injectStrongsButtons(chapEl){chapEl.querySelectorAll('.vu').forEach(function(vu){
  if(vu.querySelector('.strbtn'))return;
  var b=document.createElement('button');b.className='strbtn';b.type='button';b.textContent="Strong's";
  b.onclick=function(){showStrongs(b);};vu.appendChild(b);});}
async function showStrongs(btn){
  var vu=btn.closest('.vu');if(!vu)return;
  var ex=vu.querySelector('.strongspanel');if(ex){ex.remove();btn.classList.remove('on');return;}
  var art=vu.closest('article.book'),chap=vu.closest('.chap');
  var book=art.getAttribute('data-book'),c=chap.getAttribute('data-chap');
  var vs=vu.querySelector('.v'),v=vs?vs.textContent.trim():'';
  var panel=document.createElement('div');panel.className='strongspanel';
  panel.innerHTML='<div class="sw-u">Loading Strong’s…</div>';vu.appendChild(panel);btn.classList.add('on');
  try{
    var r=await fetch('/api/strongs?book='+encodeURIComponent(book)+'&chapter='+c+'&verse='+v);
    var d=await r.json();
    if(!d.available||!d.words.length){panel.innerHTML='<div class="sw-u">No Strong’s data for this verse.</div>';return;}
    var h='<div class="sp-title">Strong’s &middot; '+esc(d.ref)+'</div>';
    d.words.forEach(function(w){
      h+='<div class="sw"><span class="sw-en">'+esc(w.w)+'</span>';
      w.entries.forEach(function(en){
        h+='<div class="sw-e"><span class="sw-num">'+esc(en.num)+'</span>';
        if(en.o)h+='<span class="sw-o">'+esc(en.o)+'</span>';
        if(en.t)h+='<span class="sw-t">'+esc(en.t)+'</span>';
        if(en.p)h+='<span class="sw-p">'+esc(en.p)+'</span>';
        if(en.d)h+='<div class="sw-d">'+esc(en.d)+'</div>';
        if(en.u)h+='<div class="sw-u">'+esc(en.u)+'</div>';
        h+='</div>';});
      h+='</div>';});
    panel.innerHTML=h;
  }catch(err){panel.innerHTML='<div class="sw-u">Could not load Strong’s data.</div>';}
}
function toggleBookNote(){
  if(!ME){openAuth();return;}
  if(!CURBOOK)return;
  var m=document.getElementById('booknotemodal');
  if(!m.classList.contains('hidden')){closeBookNote();return;}
  var box=document.getElementById('bnBox');box.setAttribute('data-book',CURBOOK);
  document.getElementById('bnTitle').textContent=CURBOOK+' — overview note';
  renderNoteBox(box);loadNoteBox(box);m.classList.remove('hidden');
}
function closeBookNote(){document.getElementById('booknotemodal').classList.add('hidden');}
function updateReadbar(){var crumb=document.getElementById('rbCrumb');var chBtn=document.getElementById('rbChapters');if(!crumb)return;
  if(document.body.classList.contains('chapter')){crumb.textContent=CURBOOK+' '+CURCHAP;chBtn.style.display=(chapCount(CURBOOK)>1)?'':'none';}
  else{crumb.textContent=CURBOOK||'';chBtn.style.display='none';}}
document.addEventListener('click',function(e){var t=e.target;if(!t||!t.closest)return;
  var tl=t.closest('.toclink');if(tl){e.preventDefault();openBook(tl.getAttribute('data-book'));return;}
  var cn=t.closest('.chapnum');if(cn){var g=cn.closest('.chapgrid');if(g)openChapter(g.getAttribute('data-book'),cn.getAttribute('data-chap'));return;}});
function route(){var h=location.hash||'';
  if(h.indexOf('#/')===0){var parts=h.slice(2).split('/');var book=decodeURIComponent(parts[0]||'');
    if(book&&bookArticle(book)){if(parts[1])openChapter(book,parts[1]);else openBook(book);return;}}
  showHome();}
window.addEventListener('hashchange',route);
route();
</script>''')
parts.append('</body></html>')

out = "".join(parts)
open("KJV_Rightly_Divided.html","w",encoding="utf-8").write(out)
print("bytes:", len(out.encode()))
print("MB:", round(len(out.encode())/1048576,2))
