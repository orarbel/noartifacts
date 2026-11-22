#!/usr/bin/env python3
"""Generate index.html and /<lang>/index.html from strings.py. Run: python3 build.py"""
import json, os
from string import Template
from strings import LANGS

SITE = "https://noartifacts.com"
ORDER = list(LANGS)  # 'en' first

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23f6f3ec'/%3E"
           "%3Ctext x='32' y='47' font-family='Georgia,serif' font-size='44' text-anchor='middle' fill='%231a1a1a'%3Ea%3C/text%3E"
           "%3Cline x1='12' y1='34' x2='52' y2='34' stroke='%23b3412f' stroke-width='6' stroke-linecap='round'/%3E%3C/svg%3E")

def url(code):
    return f"{SITE}/" if code == "en" else f"{SITE}/{code}/"

def path(code):
    return "/" if code == "en" else f"/{code}/"

# Only the English page (served at /) sends visitors to their browser language,
# unless they picked a language from the list (stored in localStorage).
REDIRECT = Template("""<script>
(function(){
  var L=$langs, pick=null;
  try{ pick=localStorage.getItem('lang'); }catch(e){}
  if(pick){ if(pick!=='en' && L.indexOf(pick)>-1) location.replace('/'+pick+'/'); return; }
  var prefs=navigator.languages||[navigator.language||''];
  for(var i=0;i<prefs.length;i++){
    var c=(prefs[i]||'').toLowerCase().split('-')[0]; if(c==='iw') c='he';
    if(c==='en') return;
    if(L.indexOf(c)>-1){ location.replace('/'+c+'/'); return; }
  }
})();
</script>""")

PAGE = Template("""<!DOCTYPE html>
<html lang="$code" dir="$dir">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title</title>
$redirect<meta name="description" content="$desc">
<link rel="canonical" href="$url">
$alternates
<meta property="og:type" content="website">
<meta property="og:site_name" content="no artifacts">
<meta property="og:locale" content="$locale">
<meta property="og:title" content="$title">
<meta property="og:description" content="$desc">
<meta property="og:url" content="$ogurl">
<meta property="og:image" content="https://noartifacts.com/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="no artifacts, with the word artifacts struck through in red">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="$title">
<meta name="twitter:description" content="$desc">
<meta name="twitter:url" content="$ogurl">
<meta name="twitter:image" content="https://noartifacts.com/og.png">
<link rel="icon" type="image/svg+xml" href="$favicon">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#f6f3ec; --ink:#1a1a1a; --muted:#6b675f; --line:#dcd6ca;
    --bad:#b3412f; --good:#2f6b46; --card:#fffdf8;
  }
  @media (prefers-color-scheme: dark){
    :root{ --bg:#141311; --ink:#ece8df; --muted:#9a948a; --line:#2e2b27; --bad:#e0735f; --good:#6fbf8b; --card:#1c1b18; }
  }
  *{box-sizing:border-box}
  html,body{margin:0;background:var(--bg);color:var(--ink)}
  body{font:17px/1.6 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
  main{max-width:680px;margin:0 auto;padding:72px 24px 96px}
  h1{font-family:"Instrument Serif",serif;font-weight:400;font-size:clamp(64px,14vw,120px);line-height:.9;margin:0 0 28px;letter-spacing:-.02em;overflow-wrap:anywhere}
  h1 s{text-decoration-thickness:6px;text-decoration-color:var(--bad)}
  .lede{font-size:22px;line-height:1.45;margin:0 0 56px}
  h2{font-family:"Instrument Serif",serif;font-weight:400;font-size:34px;margin:64px 0 16px;line-height:1.1}
  p{margin:0 0 16px}
  .muted{color:var(--muted)}
  .label{font:500 12px/1 "JetBrains Mono",monospace;letter-spacing:.08em;text-transform:uppercase;margin:0 0 10px;display:flex;align-items:center;gap:8px}
  .label.bad{color:var(--bad)} .label.good{color:var(--good)}
  .chat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:0 0 28px}
  .msg{display:flex;gap:12px;margin:0 0 14px}
  .msg:last-child{margin:0}
  .av{flex:none;width:36px;height:36px;border-radius:8px;object-fit:cover;background:#c9b99a}
  .who{font-weight:600;font-size:15px} .who span{font-weight:400;color:var(--muted);font-size:13px;margin-inline-start:6px}
  .txt{font-size:15.5px}
  .link{color:#3b6fd4;text-decoration:underline;word-break:break-all}
  .preview{margin-top:8px;border-inline-start:3px solid #c9b99a;padding:8px 12px;font-size:14px;background:rgba(0,0,0,.03);border-radius:0 6px 6px 0}
  [dir=rtl] .preview{border-radius:6px 0 0 6px}
  .preview b{display:block}
  ol{padding-inline-start:22px;margin:0 0 16px} li{margin:0 0 12px}
  .rule{display:grid;grid-template-columns:auto 1fr;gap:4px 16px;padding:18px 0;border-top:1px solid var(--line)}
  .rule:last-of-type{border-bottom:1px solid var(--line)}
  .rule .n{font:500 13px "JetBrains Mono",monospace;color:var(--muted);padding-top:4px}
  .rule b{font-weight:600}
  .share{margin-top:56px;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
  button{font:500 15px Inter,system-ui,sans-serif;background:var(--ink);color:var(--bg);border:0;border-radius:999px;padding:12px 20px;cursor:pointer}
  button.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
  #status{font-size:14px;color:var(--muted)}
  .langs{margin-top:56px;display:flex;flex-wrap:wrap;gap:6px 16px;font-size:14px}
  .langs a{color:var(--muted);text-decoration:none}
  .langs a:hover{color:var(--ink);text-decoration:underline}
  .langs a[aria-current]{color:var(--ink);font-weight:600}
  footer{margin-top:40px;font-size:14px;color:var(--muted)}
  footer a{color:inherit}
</style>
</head>
<body>
<main>
  <h1>$h1</h1>
  <p class="lede">$lede</p>

  <p class="label bad">$dont</p>
  <div class="chat">
    <div class="msg"><img class="av" src="/img/dana.jpg" alt="" width="36" height="36"><div>
      <div class="who">$dana <span>10:42</span></div>
      <div class="txt">$chat1<br>
        <span class="link">claude.ai/artifact/8f3k2...</span>
        <div class="preview"><b>$preview_title</b>$preview_sections</div>
      </div>
    </div></div>
    <div class="msg"><img class="av" src="/img/you.jpg" alt="" width="36" height="36"><div>
      <div class="who">$you <span>10:58</span></div>
      <div class="txt">$me</div>
    </div></div>
    <div class="msg"><img class="av" src="/img/dana.jpg" alt="" width="36" height="36"><div>
      <div class="who">$dana <span>11:31</span></div>
      <div class="txt">$dana_reply</div>
    </div></div>
  </div>

  <p class="label good">$instead</p>
  <div class="chat">
    <div class="msg"><img class="av" src="/img/dana.jpg" alt="" width="36" height="36"><div>
      <div class="who">$dana <span>10:42</span></div>
      <div class="txt">$good</div>
    </div></div>
  </div>

  <h2>$why_h</h2>
  <ol>
$why
  </ol>

  <h2>$rules_h</h2>
$rules

  <div class="share">
    <button id="copy">$btn_copy</button>
    <button class="ghost" id="copymsg">$btn_reply</button>
    <span id="status" aria-live="polite"></span>
  </div>

  <nav class="langs" aria-label="Languages">
$langs
  </nav>

  <footer>$footer <a href="https://github.com/orarbel/noartifacts">$source</a>. $inspired</footer>
</main>
<script>
  const URL_CANONICAL = 'https://noartifacts.com';
  const T = $js;
  const status = document.getElementById('status');
  async function copy(text, msg){
    try{ await navigator.clipboard.writeText(text); status.textContent = msg; }
    catch(e){ status.textContent = T.blocked; }
    setTimeout(()=>status.textContent='', 2500);
  }
  document.getElementById('copy').onclick = () => copy(URL_CANONICAL, T.copied);
  document.getElementById('copymsg').onclick = () => copy(T.reply + URL_CANONICAL, T.reply_copied);
  document.querySelectorAll('.langs a').forEach(a => a.addEventListener('click', () => {
    try{ localStorage.setItem('lang', a.hreflang); }catch(e){}
  }));
</script>
</body>
</html>
""")

def build(code):
    s = LANGS[code]
    alternates = "\n".join(f'<link rel="alternate" hreflang="{c}" href="{url(c)}">' for c in ORDER)
    alternates += f'\n<link rel="alternate" hreflang="x-default" href="{url("en")}">'
    langs = "\n".join(
        f'    <a href="{path(c)}" hreflang="{c}" lang="{c}"' + (' aria-current="page"' if c == code else "") + f'>{LANGS[c]["name"]}</a>'
        for c in ORDER)
    why = "\n".join(f"    <li><b>{b}</b> {t}</li>" for b, t in s["why"])
    rules = "\n".join(
        f'  <div class="rule"><div class="n">0{i}</div><div><b>{b}</b> <span class="muted">{t}</span></div></div>'
        for i, (b, t) in enumerate(s["rules"], 1))
    js = json.dumps({k: s[k] for k in ("reply", "copied", "reply_copied", "blocked")}, ensure_ascii=False)
    return PAGE.substitute(
        code=code, dir=s.get("dir", "ltr"), title=s["title"], desc=s["desc"], url=url(code),
        ogurl=SITE if code == "en" else url(code), locale=s["locale"], favicon=FAVICON,
        redirect=REDIRECT.substitute(langs=json.dumps([c for c in ORDER if c != "en"])) + "\n" if code == "en" else "",
        alternates=alternates, langs=langs, why=why, rules=rules, js=js,
        **{k: s[k] for k in ("h1", "lede", "dont", "instead", "dana", "you", "chat1", "preview_title",
                             "preview_sections", "me", "dana_reply", "good", "why_h", "rules_h",
                             "btn_copy", "btn_reply", "footer", "source")},
        inspired=s["inspired"].format('<a href="https://nohello.net">nohello.net</a>'))

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    for code in ORDER:
        out = os.path.join(root, "index.html") if code == "en" else os.path.join(root, code, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(build(code))
    print("built:", ", ".join(ORDER))
