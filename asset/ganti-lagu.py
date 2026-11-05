#!/usr/bin/env python3
# Pakai: python3 ganti-lagu.py lagu.mp3
import base64, mimetypes, os, sys

HTML = "surat-buat-kamu-final.html"
OUT = "surat-buat-kamu-final-dengan-lagu.html"

if len(sys.argv) != 2:
    sys.exit("Cara pakai: python3 ganti-lagu.py namalagu.mp3")
song = sys.argv[1]
for f in (HTML, song):
    if not os.path.isfile(f):
        sys.exit("File tidak ketemu: " + f)

s = open(HTML, encoding="utf-8").read()
mark = s.find("// Melodi kotak musik")
if mark < 0:
    sys.exit("Bagian lagu tidak ketemu di " + HTML)
a = s.rindex("<script>", 0, mark)
b = s.index("</script>", mark) + len("</script>")

mime = {".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".aac": "audio/aac", ".wav": "audio/wav"}.get(
    os.path.splitext(song)[1].lower(), mimetypes.guess_type(song)[0] or "audio/mpeg")
data = base64.b64encode(open(song, "rb").read()).decode()

js = """<script>
(function(){
  var audio=new Audio('data:%s;base64,%s');audio.loop=true;audio.volume=.8;
  var btn=document.getElementById('musicBtn'),started=false;
  function show(on){
    btn.classList.toggle('playing',on);btn.setAttribute('aria-pressed',String(on));
    btn.setAttribute('aria-label',on?'Matikan lagu':'Nyalakan lagu');btn.firstChild.textContent=on?'\\uD83C\\uDFB5':'\\uD83D\\uDD07';
  }
  function play(){var p=audio.play();show(true);if(p&&p.catch)p.catch(function(){show(false);});}
  function start(){if(started)return;started=true;btn.classList.add('show');play();}
  btn.addEventListener('click',function(){if(audio.paused)play();else{audio.pause();show(false);}});
  document.getElementById('envelope').addEventListener('click',start);
  document.getElementById('openBtn').addEventListener('click',start);
})();
</script>""" % (mime, data)

open(OUT, "w", encoding="utf-8").write(s[:a] + js + s[b:])
print("Berhasil! Kirim file ini ke dia: %s (%.1f MB)" % (OUT, os.path.getsize(OUT) / 1e6))
