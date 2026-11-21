import json
B=[0,9.6,18.25,26.4,35.35,42.65,51.6,59.0]
tm=json.load(open('tm59.json'))
def st(si,k=0):
    L=[t for t in tm if t[0]==si];return L[k][1]

BG='<defs><radialGradient id="g%d" cx="50%%" cy="42%%" r="75%%"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="#050a14"/></radialGradient></defs><rect width="1080" height="1920" fill="url(#g%d)"/>'
body=[];js=[]
def clip(id,cls,a,b,tr,inner): body.append(f'<div id="{id}" class="clip {cls}" data-start="{a:.2f}" data-duration="{b-a:.2f}" data-track-index="{tr}">{inner}</div>')
def sat(id,B0,B1,ox,oy,s0,s1,tx0,ty0,tx1,ty1):
    js.append(f'gsap.set("#{id}i",{{transformOrigin:"{ox}px {oy}px"}});tl.fromTo("#{id}i",{{scale:{s0},x:{tx0},y:{ty0}}},{{scale:{s1},x:{tx1},y:{ty1},duration:{B1-B0:.2f},ease:"none"}},{B0:.2f});')
    return f'<div class="satw"><img id="{id}i" class="sat" src="assets/sat.jpg"/></div>'
E=B[6]
# map scenes (window 1080x1180)
sc=[(0,572,1158,1.0,1.25,0,0,-32,0),(1,572,1158,1.25,1.7,-32,0,-32,0),(2,525,1150,1.9,2.2,15,0,15,0),(3,700,560,1.5,1.8,-120,520,-120,520),(4,572,1158,1.5,1.3,-20,0,-20,0),(5,572,1158,1.3,1.0,-32,0,0,0)]
for i,ox,oy,s0,s1,tx0,ty0,tx1,ty1 in sc:
    clip(f's{i}','full',B[i],B[i+1],1,sat(f'e{i}',B[i],B[i+1],ox,oy,s0,s1,tx0,ty0,tx1,ty1))
clip('redbg','full',0,E,2,'<div class="redbg"></div>')
heads=[('ĐỪNG MUA ĐẤT','CHỈ VÌ GIÁ RẺ!'),('KHU DÂN CƯ DARESCO','LONG AN'),('MUA ĐỂ Ở: NHÌN VÀO','NHU CẦU THỰC TẾ'),('ĐẦU TƯ: PHẢI','CÓ CƠ SỞ'),('TÌM HIỂU KỸ QUY HOẠCH','VÀ GIÁ THỰC TẾ'),('HIỂU ĐÚNG – CHỌN ĐÚNG','ĐẦU TƯ CÓ CƠ SỞ')]
for i,(a,b) in enumerate(heads):
    clip(f'h{i}','txt',B[i]+0.15,B[i+1]-0.1,4,f'<div class="in head"><div>{a}</div><div>{b}</div></div>')
    js.append(f'tl.fromTo("#h{i} .in",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.5,ease:"power3.out"}},{B[i]+0.25:.2f});')
rows=[('KHU DÂN CƯ DARESCO','LONG AN',B[1]+0.6),('MUA ĐỂ Ở','NHU CẦU THỰC TẾ',st(2,0)+2.0),('ĐẦU TƯ','PHẢI CÓ CƠ SỞ',B[3]+1.8),('TÌM HIỂU KỸ','QUY HOẠCH',st(4,0)+1.2),('XEM GIÁ','GIAO DỊCH THỰC TẾ',st(4,0)+2.8)]
for k,(l,v,t) in enumerate(rows):
    clip(f'r{k}','txt',t,E,5,f'<div class="in card" style="top:{690+k*112}px"><div class="cl">{l}</div><div class="cv">{v}</div></div>')
    js.append(f'tl.fromTo("#r{k} .in",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.45,ease:"power3.out"}},{t:.2f});')
clip('hook','txt',0,E,6,'<div class="hookb"><div class="btag">MR DI • PHÂN TÍCH ĐẤT NỀN</div><div class="hk1">KDC DARESCO LONG AN</div><div class="hk2">CÓ NÊN MUA ĐẤT NỀN?</div></div>')
# brand end card
s6=f'<svg class="bgsvg" viewBox="0 0 1080 1920" width="1080" height="1920">{BG%(6,"#183c68",6)}<g id="rg" opacity=".5">'+''.join(f'<circle cx="540" cy="860" r="{r}" fill="none" stroke="#ffd34a" stroke-opacity=".25" stroke-width="2"/>' for r in (180,300,420,540))+'</g></svg>'
clip('s6','full',B[6],B[7],1,s6)
t6='<div class="in tt t6" style="top:560px"><div class="mini">MR DI</div><div class="logo2">PHÂN TÍCH</div><div class="logo2">ĐẤT NỀN</div><div class="tagl">HIỂU ĐẤT TRƯỚC KHI XUỐNG TIỀN!</div></div>'
clip('t6','txt',B[6]+0.1,B[7],4,t6)
js.append(f'tl.fromTo("#t6 .in",{{opacity:0,y:50,scale:0.92}},{{opacity:1,y:0,scale:1,duration:0.7,ease:"power3.out"}},{B[6]+0.3:.2f});tl.fromTo("#rg",{{opacity:0,scale:0.7,svgOrigin:"540 860"}},{{opacity:.5,scale:1,duration:1.2,ease:"power2.out"}},{B[6]:.2f});')
page=f"""<!doctype html>
<html lang="vi"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face{{font-family:"InterX";src:url("assets/fonts/Inter-ExtraBold.otf");font-weight:800}}
@font-face{{font-family:"InterX";src:url("assets/fonts/Inter-Bold.otf");font-weight:700}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:#050a14}}
#root{{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:"InterX",sans-serif;color:#fff}}
.clip{{position:absolute}}
.satw{{position:absolute;left:0;top:0;width:1080px;height:1180px;overflow:hidden;background:#0a1018}}
.sat{{position:absolute;left:0;top:-568px;width:1080px;height:2250px}}
.full,.bgsvg{{position:absolute;left:0;top:0;width:1080px;height:1920px}}
.txt{{left:0;top:0;width:1080px;height:1920px}}
.redbg{{position:absolute;left:0;top:0;width:1080px;height:1920px;background:linear-gradient(to bottom,rgba(0,0,0,.72) 0,rgba(0,0,0,.55) 300px,rgba(0,0,0,0) 420px,rgba(0,0,0,0) 640px,rgba(150,20,25,.93) 1180px,#6a0e15 1500px,#3d070d 1920px)}}
.head{{position:absolute;left:40px;width:1000px;top:190px;text-align:center;font-weight:800;font-size:68px;line-height:80px;color:#FFD34A;text-shadow:0 4px 16px rgba(0,0,0,.9)}}
.card{{position:absolute;left:50px;width:980px;height:98px;background:rgba(10,14,22,.9);border-left:10px solid #c0392b;border-radius:10px;display:flex;align-items:center;justify-content:space-between;padding:0 28px}}
.cl{{font-weight:800;font-size:38px;color:#FFD34A}}.cv{{font-weight:800;font-size:38px;color:#fff;text-align:right}}
.hookb{{position:absolute;left:0;top:1330px;width:1080px;text-align:center}}
.btag{{font-weight:800;font-size:28px;letter-spacing:.08em;color:#fff;opacity:.85;margin-bottom:26px}}
.hk1{{font-weight:800;font-size:66px;line-height:80px;color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.7)}}
.hk2{{font-weight:800;font-size:66px;line-height:80px;color:#FFD34A;text-shadow:0 4px 14px rgba(0,0,0,.7)}}
.tt{{position:absolute;left:100px;width:880px;text-align:center}}
.mini{{font-weight:800;font-size:50px;line-height:60px;color:#fff;letter-spacing:.04em}}
.logo2{{font-weight:800;font-size:112px;line-height:124px;color:#FFD34A}}
.tagl{{margin-top:40px;font-weight:800;font-size:44px;line-height:56px;color:#fff;background:rgba(185,28,28,.9);padding:14px 22px;border-radius:14px;display:inline-block}}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="59" data-width="1080" data-height="1920">
{chr(10).join(body)}
<audio id="vo" src="assets/mix.mp3" data-start="0" data-duration="59" data-track-index="7" data-volume="1"></audio>
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{chr(10).join(js)}
window.__timelines["main"]=tl;tl.seek(0);
</script></body></html>"""
open('vid/index.html','w',encoding='utf-8').write(page)
print('ok')
