#!/usr/bin/env python3
import subprocess, os
BASE="/tmp/claude-0/-home-user-book-genesis-v4/0e2967a7-e82c-584e-8195-1db54c7e81ac/scratchpad/covers"
CHROME="/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
W,H=1000,1600

# corrected palette
PLUM="#43182B"      # deep true plum (was reading magenta before)
PLUM2="#5A1E3A"
CREAM="#FBF6F0"
INK="#2A1220"
ROSE="#C98498"      # soft dusty rose accent (not hot bubblegum)
GOLD="#E0A64B"
SAGE="#8CA893"
BLUE="#3B5488"

SHELL='''<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;padding:0;width:{W}px;height:{H}px;overflow:hidden}}
*{{box-sizing:border-box}}
.cover{{position:relative;width:{W}px;height:{H}px;background:{bg};font-family:'DejaVu Sans',sans-serif}}
.serif{{font-family:'Bitstream Charter','Liberation Serif',serif}}
.center{{position:absolute;left:0;right:0;text-align:center}}
</style></head><body><div class="cover">{body}</div></body></html>'''

def page(name, bg, body):
    html=SHELL.format(W=W,H=H,bg=bg,body=body)
    p=os.path.join(BASE,name+".html"); open(p,"w").write(html)
    out=os.path.join(BASE,name+".png")
    subprocess.run([CHROME,"--headless=new","--no-sandbox","--disable-gpu",
        "--hide-scrollbars","--force-device-scale-factor=1",
        "--virtual-time-budget=1500","--screenshot="+out,
        f"--window-size={W},{H}","file://"+p],
        stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    print("rendered",out)

# ---------- Direction A: Set Boundaries model (cream + color blocks + clean type) ----------
blob="border-radius:46% 54% 43% 57% / 55% 44% 56% 45%;"
blobs=f'''
<div style="position:absolute;top:70px;left:70px;width:250px;height:230px;background:{GOLD};{blob}"></div>
<div style="position:absolute;top:70px;right:70px;width:250px;height:230px;background:{ROSE};border-radius:54% 46% 57% 43% / 44% 56% 45% 55%;"></div>
<div style="position:absolute;bottom:70px;left:70px;width:250px;height:230px;background:{SAGE};border-radius:55% 45% 50% 50% / 50% 55% 45% 50%;"></div>
<div style="position:absolute;bottom:70px;right:70px;width:250px;height:230px;background:{PLUM};border-radius:48% 52% 45% 55% / 57% 46% 54% 43%;"></div>
'''
A=f'''{blobs}
<div class="center" style="top:520px;font-size:24px;letter-spacing:10px;color:{ROSE};font-weight:600">CHOOSE &nbsp;&middot;&nbsp; BUILD &nbsp;&middot;&nbsp; OWN</div>
<div class="center" style="top:585px;font-size:118px;line-height:1.0;letter-spacing:6px;color:{PLUM};font-weight:700">THE THIRD<br>OPTION</div>
<div class="center serif" style="top:900px;font-size:44px;font-style:italic;color:{PLUM2}">How to Choose, Build, and Own<br>a Life That Fits</div>
<div class="center" style="top:1205px;font-size:34px;letter-spacing:6px;color:{PLUM};font-weight:700">JENA CROSSLAND BROOKS</div>
'''

# ---------- Direction B: deep plum field + cream Charter serif + door motif ----------
def arches(fillthird, stroke, fill):
    w,h,gap=150,262,60; total=3*w+2*gap; x0=(W-total)/2; y=0
    svg=f'<svg width="{total}" height="{h}" viewBox="0 0 {total} {h}">'
    for i in range(3):
        x=i*(w+gap); r=w/2
        d=f"M {x},{h} L {x},{r} A {r},{r} 0 0 1 {x+w},{r} L {x+w},{h} Z"
        if i==2 and fillthird:
            svg+=f'<path d="{d}" fill="{fill}"/>'
            svg+=f'<line x1="{x+w/2}" y1="{r}" x2="{x+w/2}" y2="{h}" stroke="{PLUM}" stroke-width="4"/>'
        else:
            svg+=f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="5"/>'
    svg+='</svg>'
    return svg
B=f'''
<div class="center" style="top:300px;font-size:26px;letter-spacing:12px;color:{ROSE};font-weight:600">CHOOSE &middot; BUILD &middot; OWN</div>
<div class="center serif" style="top:400px;font-size:150px;line-height:0.98;color:{CREAM};font-weight:700">THE<br>THIRD<br>OPTION</div>
<div class="center serif" style="top:930px;font-size:46px;font-style:italic;color:#E9D9DF">How to Choose, Build, and Own<br>a Life That Fits</div>
<div class="center" style="top:1055px;">{arches(True,CREAM,ROSE)}</div>
<div class="center" style="top:1440px;font-size:32px;letter-spacing:6px;color:{CREAM};font-weight:700">JENA CROSSLAND BROOKS</div>
'''

# ---------- Direction C: warm field + deep plum Charter serif (Blueprint echo) ----------
C=f'''
<div class="center" style="top:300px;font-size:26px;letter-spacing:12px;color:{PLUM};font-weight:600">CHOOSE &middot; BUILD &middot; OWN</div>
<div class="center serif" style="top:400px;font-size:150px;line-height:0.98;color:{PLUM};font-weight:700">THE<br>THIRD<br>OPTION</div>
<div class="center serif" style="top:930px;font-size:46px;font-style:italic;color:{PLUM2}">How to Choose, Build, and Own<br>a Life That Fits</div>
<div class="center" style="top:1055px;">{arches(True,PLUM,PLUM)}</div>
<div class="center" style="top:1440px;font-size:32px;letter-spacing:6px;color:{PLUM};font-weight:700">JENA CROSSLAND BROOKS</div>
'''

page("dirA", CREAM, A)
page("dirB", PLUM, B)
page("dirC", "#EBC067", C)
