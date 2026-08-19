#!/usr/bin/env python3
# Stacked topic key-verses with per-reference comments (add / edit / delete).
# Run against BOTH:
#   python3 patch_topic_verse_notes.py index.html
#   python3 patch_topic_verse_notes.py ~/bible/build_bible.py
# (build_bible.py regenerates index.html, so it must be patched too.)
import io, sys

# ---------------------------------------------------------------- CSS
OLD_CSS = ".td-verses{display:flex;flex-wrap:wrap;gap:7px;align-items:center;margin-bottom:20px}"
NEW_CSS = (
    ".td-verses{display:block;margin-bottom:20px}\n"
    ".td-vrow{background:#fff;border:1px solid #ddd0e6;border-radius:10px;padding:9px 12px;margin-bottom:8px}\n"
    ".td-vhead{display:flex;align-items:flex-start;gap:6px}\n"
    ".td-vrow .xref-link{border:none;background:none;padding:1px 0;margin:0;color:#6b4a7a;flex:1 1 auto;text-align:left;white-space:normal}\n"
    ".td-vrow .xref-link:hover{background:none;color:var(--s3);text-decoration:underline}\n"
    ".td-vacts{display:flex;gap:1px;flex:0 0 auto}\n"
    ".td-vbtn{font-family:inherit;background:none;border:none;color:#b0a0bb;font-size:.95rem;line-height:1;cursor:pointer;padding:4px 7px;border-radius:6px}\n"
    ".td-vbtn:hover{color:var(--s3);background:#f3eef6}\n"
    ".td-vrow .td-vdel:hover{color:#b3402f;background:#fbeeec}\n"
    ".td-vnote{margin-top:6px;font-size:.9rem;line-height:1.5;color:#5a4a63;white-space:pre-wrap;border-left:2px solid #ddd0e6;padding-left:9px}\n"
    ".td-ved{margin-top:8px}\n"
    ".td-ved .td-vta{width:100%;box-sizing:border-box;font-family:inherit;font-size:.92rem;line-height:1.5;color:var(--ink);background:#fdfcfd;border:1px solid #ddd0e6;border-radius:8px;padding:8px 10px;min-height:74px;resize:vertical}\n"
    ".td-vedrow{display:flex;gap:7px;margin-top:7px;align-items:center}\n"
    ".td-vsave{font-family:inherit;font-size:.72rem;font-weight:700;color:#fff;background:var(--s3);border:1px solid var(--s3);border-radius:14px;padding:5px 13px;cursor:pointer}\n"
    ".td-vcancel{font-family:inherit;font-size:.72rem;font-weight:700;color:#7a6a84;background:#fff;border:1px solid var(--rule);border-radius:14px;padding:5px 13px;cursor:pointer}\n"
    ".td-vstat{font-size:.72rem;color:#8a7a94}\n"
    ".td-vadd{margin-top:2px}"
)

# ------------------------------------------------- modal: topic-verse edit mode
OLD_OPENTV = ("function openTopicVerse(key,title){if(!ME){openAuth();return;}XR_MODE='topic';XR_TOPIC=key;"
              "document.getElementById('xrSrc').innerHTML='Add a key verse to <b>'+esc(title)+'</b>:';"
              "document.getElementById('xrNote').style.display='none';fillXrefBooks();"
              "var bsel=document.getElementById('xrBook');if(!bsel.value)bsel.value='Romans';xrBookChange();"
              "document.getElementById('xrErr').textContent='';"
              "document.getElementById('xrefmodal').classList.remove('hidden');}")
NEW_OPENTV = (
    "var XR_TV_EDIT=null;  // existing topic ref being re-pointed\n"
    "function parseRef(ref){ref=String(ref||'').trim();var i=ref.lastIndexOf(' ');if(i<0)return null;"
    "var book=ref.slice(0,i),rest=ref.slice(i+1);var c=rest.split(':');if(c.length!==2)return null;"
    "var vv=c[1].split('-');return {book:book,chap:c[0],verse:vv[0],end:vv[1]||''};}\n"
    "function openTopicVerse(key,title,editRef){if(!ME){openAuth();return;}XR_MODE='topic';XR_TOPIC=key;"
    "XR_TV_EDIT=editRef||null;"
    "document.getElementById('xrSrc').innerHTML=(editRef?'Change the reference for <b>'+esc(editRef)+'</b>:'"
    ":'Add a key verse to <b>'+esc(title)+'</b>:');"
    "document.getElementById('xrNote').style.display='none';"
    "document.getElementById('xrSave').textContent=(editRef?'Save changes':'Add verse');fillXrefBooks();"
    "var bsel=document.getElementById('xrBook');var p=editRef?parseRef(editRef):null;"
    "if(p&&CHAPVERSES[p.book]){bsel.value=p.book;xrBookChange();"
    "document.getElementById('xrChap').value=p.chap;xrChapChange();"
    "document.getElementById('xrVerse').value=p.verse;xrStartChange();"
    "if(p.end){document.getElementById('xrVerse2').value=p.end;}xrPreview();}"
    "else{if(!bsel.value)bsel.value='Romans';xrBookChange();}"
    "document.getElementById('xrErr').textContent='';"
    "document.getElementById('xrefmodal').classList.remove('hidden');}"
)

# ------------------------------------------------------ saveXref: topic branch
OLD_SAVE = ("  if(XR_MODE==='topic'){var key=XR_TOPIC,cur=TOPICMAP[key],row=TC[key]||{verses:[],body:'',"
            "title:cur?cur.title:''};var vs=(row.verses||[]).slice();if(vs.indexOf(ref)<0)vs.push(ref);"
            "var d=await api('PUT','/api/topics',{key:key,title:cur?cur.title:(row.title||''),"
            "body:row.body||'',verses:vs,is_custom:!cur});TC[key]=d;closeXref();"
            "if(CURTOPIC===key)renderTopicDetail(key);}")
NEW_SAVE = ("  if(XR_MODE==='topic'){var key=XR_TOPIC,cur=TOPICMAP[key],row=TC[key]||{verses:[],body:'',"
            "title:cur?cur.title:''};var rv=tvNorm(row.verses);var keep='';"
            "if(XR_TV_EDIT){for(var qi=0;qi<rv.length;qi++){if(rv[qi].ref===XR_TV_EDIT){keep=rv[qi].note;"
            "rv.splice(qi,1);break;}}}"
            "var ex=-1;for(var qj=0;qj<rv.length;qj++){if(rv[qj].ref===ref)ex=qj;}"
            "if(ex<0){rv.push({ref:ref,note:keep});}else if(keep&&!rv[ex].note){rv[ex].note=keep;}"
            "var d=await api('PUT','/api/topics',{key:key,title:cur?cur.title:(row.title||''),"
            "body:row.body||'',verses:tvPack(rv),is_custom:!cur});TC[key]=d;XR_TV_EDIT=null;closeXref();"
            "if(CURTOPIC===key)renderTopicDetail(key);}")

# ------------------------------------------------- renderTopicDetail: verse list
OLD_REND = ("  var cv=cur?(cur.verses||[]):[];var uv=(row.verses||[]).filter(function(r){return cv.indexOf(r)<0;});\n"
            "  h+='<div class=\"td-vlabel\">Key verses</div><div class=\"td-verses\">';\n"
            "  cv.forEach(function(ref){h+='<span class=\"td-vitem\"><button class=\"xref-link\" data-ref=\"'"
            "+escq(ref)+'\">'+esc(ref)+'</button></span>';});\n"
            "  uv.forEach(function(ref){h+='<span class=\"td-vitem\"><button class=\"xref-link\" data-ref=\"'"
            "+escq(ref)+'\">'+esc(ref)+'</button><button class=\"td-vdel\" type=\"button\" data-vdel=\"'"
            "+escq(ref)+'\" title=\"Remove verse\">&times;</button></span>';});\n"
            "  h+='<button class=\"td-vadd\" type=\"button\" data-vadd=\"1\">+ add verse</button></div>';\n")
NEW_REND = "  h+=topicVersesHtml(cur,row);\n"

# --------------------------------------------- new helpers + rewritten remover
OLD_REMOVE = ("async function topicRemoveVerse(key,ref){var cur=TOPICMAP[key],row=TC[key];if(!row)return;"
              "var vs=(row.verses||[]).filter(function(r){return r!==ref;});"
              "try{var d=await api('PUT','/api/topics',{key:key,title:cur?cur.title:(row.title||''),"
              "body:row.body||'',verses:vs,is_custom:!cur});if(d&&d.deleted){delete TC[key];}else{TC[key]=d;}"
              "renderTopicDetail(key);}catch(e){}}")
NEW_REMOVE = (
    "/* topic key verses: each entry is either \"Book C:V\" (no comment) or {ref,note} */\n"
    "function tvRef(v){return (v&&typeof v==='object')?String(v.ref||''):String(v||'');}\n"
    "function tvNote(v){return (v&&typeof v==='object')?String(v.note||''):'';}\n"
    "function tvNorm(list){var out=[];(list||[]).forEach(function(v){var r=tvRef(v);"
    "if(r)out.push({ref:r,note:tvNote(v)});});return out;}\n"
    "function tvPack(list){return list.map(function(e){"
    "return (e.note&&e.note.trim())?{ref:e.ref,note:e.note}:e.ref;});}\n"
    "function tvRowHtml(ref,note,own){var h='<div class=\"td-vrow\" data-vref=\"'+escq(ref)+'\">"
    "<div class=\"td-vhead\"><button class=\"xref-link\" data-ref=\"'+escq(ref)+'\">'+esc(ref)+'</button>"
    "<span class=\"td-vacts\">';"
    "h+='<button class=\"td-vbtn td-vnedit\" type=\"button\" data-vnedit=\"'+escq(ref)+'\" title=\"'"
    "+(note?'Edit my comment':'Add a comment')+'\">&#9998;</button>';"
    "if(own){h+='<button class=\"td-vbtn td-vswap\" type=\"button\" data-vswap=\"'+escq(ref)+'\" "
    "title=\"Change this reference\">&#8646;</button>';"
    "h+='<button class=\"td-vbtn td-vdel\" type=\"button\" data-vdel=\"'+escq(ref)+'\" "
    "title=\"Remove this verse\">&times;</button>';}"
    "h+='</span></div>';"
    "if(note&&note.trim())h+='<div class=\"td-vnote\">'+esc(note)+'</div>';"
    "return h+'</div>';}\n"
    "function topicVersesHtml(cur,row){var cv=cur?(cur.verses||[]):[];var rv=tvNorm(row.verses);"
    "var nmap={};rv.forEach(function(e){nmap[e.ref]=e.note;});"
    "var uv=rv.filter(function(e){return cv.indexOf(e.ref)<0;});"
    "var h='<div class=\"td-vlabel\">Key verses</div><div class=\"td-verses\">';"
    "cv.forEach(function(ref){h+=tvRowHtml(ref,nmap[ref]||'',false);});"
    "uv.forEach(function(e){h+=tvRowHtml(e.ref,e.note,true);});"
    "h+='<button class=\"td-vadd\" type=\"button\" data-vadd=\"1\">+ add verse</button></div>';return h;}\n"
    "function tvRowEl(ref){var rows=document.querySelectorAll('#topicdetail .td-vrow');"
    "for(var i=0;i<rows.length;i++){if(rows[i].getAttribute('data-vref')===ref)return rows[i];}return null;}\n"
    "function topicEditNote(key,ref){if(!ME){openAuth();return;}var el=tvRowEl(ref);if(!el)return;"
    "if(el.querySelector('.td-ved'))return;var row=TC[key]||{};var nmap={};"
    "tvNorm(row.verses).forEach(function(e){nmap[e.ref]=e.note;});"
    "var nd=el.querySelector('.td-vnote');if(nd)nd.style.display='none';"
    "var box=document.createElement('div');box.className='td-ved';"
    "box.innerHTML='<textarea class=\"td-vta\" placeholder=\"Why did you include this reference?\"></textarea>"
    "<div class=\"td-vedrow\"><button class=\"td-vsave\" type=\"button\">Save comment</button>"
    "<button class=\"td-vcancel\" type=\"button\">Cancel</button><span class=\"td-vstat\"></span></div>';"
    "el.appendChild(box);var ta=box.querySelector('.td-vta');ta.value=nmap[ref]||'';ta.focus();"
    "box.querySelector('.td-vcancel').onclick=function(){box.parentNode.removeChild(box);"
    "if(nd)nd.style.display='';};"
    "box.querySelector('.td-vsave').onclick=function(){topicSaveVerseNote(key,ref,ta.value,box);};}\n"
    "async function topicSaveVerseNote(key,ref,note,box){var st=box?box.querySelector('.td-vstat'):null;"
    "if(st)st.textContent='Saving\\u2026';var cur=TOPICMAP[key],row=TC[key]||{verses:[],body:'',"
    "title:cur?cur.title:''};var cv=cur?(cur.verses||[]):[];var rv=tvNorm(row.verses);var found=false;"
    "rv.forEach(function(e){if(e.ref===ref){e.note=note;found=true;}});"
    "if(!found)rv.push({ref:ref,note:note});"
    "if(!note.trim()&&cv.indexOf(ref)>=0)rv=rv.filter(function(e){return e.ref!==ref;});"
    "try{var d=await api('PUT','/api/topics',{key:key,title:cur?cur.title:(row.title||''),"
    "body:row.body||'',verses:tvPack(rv),is_custom:!cur});if(d&&d.deleted){delete TC[key];}else{TC[key]=d;}"
    "renderTopicDetail(key);}catch(e){if(st)st.textContent=String(e);}}\n"
    "function topicSwapVerse(key,ref){if(!ME){openAuth();return;}var cur=TOPICMAP[key];"
    "openTopicVerse(key,cur?cur.title:((TC[key]&&TC[key].title)||'topic'),ref);}\n"
    "async function topicRemoveVerse(key,ref){var cur=TOPICMAP[key],row=TC[key];if(!row)return;"
    "var vs=tvNorm(row.verses).filter(function(e){return e.ref!==ref;});"
    "try{var d=await api('PUT','/api/topics',{key:key,title:cur?cur.title:(row.title||''),"
    "body:row.body||'',verses:tvPack(vs),is_custom:!cur});if(d&&d.deleted){delete TC[key];}else{TC[key]=d;}"
    "renderTopicDetail(key);}catch(e){}}"
)

# ------------------------------------------------------------- click handlers
OLD_CLICK = ("  var vd=t.closest('.td-vdel');if(vd){topicRemoveVerse(CURTOPIC,vd.getAttribute('data-vdel'));return;}")
NEW_CLICK = ("  var vn=t.closest('.td-vnedit');if(vn){topicEditNote(CURTOPIC,vn.getAttribute('data-vnedit'));return;}\n"
             "  var vw=t.closest('.td-vswap');if(vw){topicSwapVerse(CURTOPIC,vw.getAttribute('data-vswap'));return;}\n"
             "  var vd=t.closest('.td-vdel');if(vd){topicRemoveVerse(CURTOPIC,vd.getAttribute('data-vdel'));return;}")

PATCHES = [
    ("css: stacked verse rows", OLD_CSS, NEW_CSS),
    ("js: topic-verse modal edit mode", OLD_OPENTV, NEW_OPENTV),
    ("js: saveXref topic branch", OLD_SAVE, NEW_SAVE),
    ("js: renderTopicDetail verse list", OLD_REND, NEW_REND),
    ("js: verse-note helpers + remover", OLD_REMOVE, NEW_REMOVE),
    ("js: click handlers", OLD_CLICK, NEW_CLICK),
]


def main(path):
    with io.open(path, encoding="utf-8") as f:
        s = f.read()
    orig = s
    ok = True
    for name, old, new in PATCHES:
        n = s.count(old)
        if n == 1:
            s = s.replace(old, new)
            print("  [ok]   %s" % name)
        elif s.count(new) >= 1:
            print("  [skip] %s (already applied)" % name)
        else:
            print("  [FAIL] %s (anchor found %d times)" % (name, n))
            ok = False
    if not ok:
        print("\nNothing written - fix the failing anchors first.")
        return 1
    if s == orig:
        print("\nNo changes needed.")
        return 0
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print("\nPatched %s" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "index.html"))
