"""Generate the retro CRT SVG set for the GitHub profile README.
usage: python gen.py <avatar.png> <out_dir>"""
import math, os, sys
from PIL import Image, ImageOps

AVATAR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(f"{OUT}/assets", exist_ok=True)

A, DIM, HOT, BG = "#ffb000", "#b07c1c", "#ffe2a0", "#120d07"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
CW = 0.6  # char width in em; textLength pins it so masks line up in any font


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def crt(name, w, h, body, css="", title="", wrap=""):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(title)}">
<defs>
<pattern id="sl" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".32"/></pattern>
<radialGradient id="vg" cx="50%" cy="50%" r="72%"><stop offset="62%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".7"/></radialGradient>
<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{A}" stop-opacity="0"/><stop offset=".5" stop-color="{A}" stop-opacity=".06"/><stop offset="1" stop-color="{A}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="scr"><rect width="{w}" height="{h}" rx="14"/></clipPath>
</defs>
<style>
text{{font-family:{MONO};fill:{A}}}
.dim{{fill:{DIM}}}.hot{{fill:{HOT}}}
.flk{{animation:flk 7s infinite}}
@keyframes flk{{0%,47%,49%,83%,85%,100%{{opacity:1}}48%{{opacity:.84}}84%{{opacity:.93}}}}
.band{{animation:band 6s linear infinite}}
@keyframes band{{from{{transform:translateY(-120px)}}to{{transform:translateY({h}px)}}}}
.blink{{animation:blink 1.05s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.mask{{transform-box:fill-box;transform-origin:right}}
@keyframes type{{to{{transform:scaleX(0)}}}}
@keyframes fade{{from{{opacity:0}}}}
.pw{{transform-box:view-box;transform-origin:50% 50%}}
{css}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.mask{{display:none}}}}
</style>
<g clip-path="url(#scr)">
<rect width="{w}" height="{h}" fill="{BG}"/>
<g class="pw {wrap}"><g class="flk" filter="url(#glow)">
{body}
</g></g>
<rect class="band" width="{w}" height="120" fill="url(#band)"/>
<rect width="{w}" height="{h}" fill="url(#sl)"/>
<rect width="{w}" height="{h}" fill="url(#vg)"/>
</g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="13" fill="none" stroke="#2e200d" stroke-width="2"/>
</svg>'''
    with open(f"{OUT}/assets/{name}", "w", encoding="utf-8") as f:
        f.write(svg)


def txt(x, y, s, size=14, cls="", extra="", anchor=None):
    w = len(s) * CW * size
    if anchor == "middle":
        x -= w / 2
    return (f'<text x="{x:.1f}" y="{y}" font-size="{size}" class="{cls}" {extra} '
            f'textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{esc(s)}</text>'), x, w


def typed(x, y, s, start, size=14, cls="", rate=0.022, anchor=None):
    t, x, w = txt(x, y, s, size, cls, anchor=anchor)
    dur = max(0.2, len(s) * rate)
    return t + (f'<rect class="mask" x="{x - 1:.1f}" y="{y - size:.1f}" width="{w + 3:.1f}" height="{size * 1.4:.1f}" '
                f'fill="{BG}" style="animation:type {dur:.2f}s steps({len(s)},jump-start) {start:.2f}s both"/>')


def pixels(rows, x0, y0, px, fill, gap=1):
    out = []
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c in "1X":
                out.append(f'<rect x="{x0 + i * px}" y="{y0 + j * px}" width="{px - gap}" height="{px - gap}"/>')
    return f'<g fill="{fill}">{"".join(out)}</g>'


# ---------- boot.svg ----------
FONT = {
    "T": "11111 00100 00100 00100 00100 00100 00100",
    "I": "11111 00100 00100 00100 00100 00100 11111",
    "M": "10001 11011 10101 10101 10001 10001 10001",
    "S": "01111 10000 10000 01110 00001 00001 11110",
    "U": "10001 10001 10001 10001 10001 10001 01110",
    "R": "11110 10001 10001 11110 10100 10010 10001",
    "E": "11111 10000 10000 11110 10000 10000 11111",
    "A": "01110 10001 10001 11111 10001 10001 10001",
    "L": "10000 10000 10000 10000 10000 10000 11111",
}
SHIELD = ["XXXXXXXXXXXXX", "X...........X", "X....XXX....X", "X...X...X...X", "X...X...X...X",
          "X..XXXXXXX..X", "X..XXXXXXX..X", "X..XXX.XXX..X", "X..XXX.XXX..X", "X..XXXXXXX..X",
          ".X.........X.", "..X.......X..", "...X.....X...", "....XX.XX....", "......X......"]

W, H = 900, 330
T0 = 0.6  # after power-on
post = [
    ("TSD Modular BIOS v3.97, (C) 2025-2026 timsurreal", "hot"),
    ("Main Processor : Curiosity, always on", ""),
    ("Memory Test    : 655360K OK", ""),
    ("Detecting HDD  : /dev/sda  linux, reinstall #∞", ""),
    ("Mounting       : security.target ........ [ OK ]", ""),
    ("Loading operator profile ...", "dim"),
]
body, t = [], T0
for i, (s, c) in enumerate(post):
    body.append(typed(36, 44 + i * 22, s, t, cls=c))
    t += len(s) * 0.022 + 0.12
body.append(f'<g class="shield">{pixels(SHIELD, W - 36 - 78, 26, 6, A)}</g>')

wm_start, PX = t + 0.1, 10
letters = []
for k, ch in enumerate("TIMSURREAL"):
    rows = [r for r in FONT[ch].split()]
    letters.append(f'<g class="pop" style="animation-delay:{wm_start + k * 0.07:.2f}s">'
                   f'{pixels(rows, 36 + k * 60, 172, PX, A)}</g>')
ghost = "".join(pixels(FONT[ch].split(), 36 + k * 60, 172, PX, HOT) for k, ch in enumerate("TIMSURREAL"))
body.append(f'<g class="gh" opacity="0">{ghost}</g><g class="gl">{"".join(letters)}</g>')

sub = "Timothy Sebastian Darmawan  /  cyber security  /  Jakarta, ID"
sub_t = wm_start + 10 * 0.07 + 0.3
body.append(typed(36, 280, sub, sub_t, size=15, cls="hot"))
cx = 36 + len(sub) * CW * 15 + 6
body.append(f'<rect class="blink" x="{cx:.1f}" y="267" width="9" height="16" fill="{A}" style="animation-delay:{sub_t + 1.4:.2f}s"/>')
body.append(txt(36, 314, "Press DEL to enter SETUP", 12, "dim del")[0])
body.append(txt(W - 36 - 12 * 12 * CW, 314, "ID 237275151", 12, "dim")[0])
crt("boot.svg", W, H, "\n".join(body),
    title="TIMSURREAL boot screen: Timothy Sebastian Darmawan, cyber security, Jakarta", wrap="on", css=f"""
.on{{animation:on .55s cubic-bezier(.23,1,.32,1) both}}
@keyframes on{{0%{{transform:scale(1,.004);opacity:.3}}55%{{transform:scale(1,.004);opacity:1}}100%{{transform:none}}}}
.pop{{animation:pop .2s cubic-bezier(.23,1,.32,1) both}}
@keyframes pop{{from{{opacity:0;transform:translateY(-8px)}}}}
.gl{{animation:gl 5s 6s infinite}}
@keyframes gl{{0%,89%,94%,100%{{transform:none}}90%{{transform:translateX(5px) skewX(-10deg)}}91%{{transform:translateX(-4px)}}92%{{transform:translateX(2px) skewX(6deg)}}}}
.gh{{animation:gh 5s 6s infinite}}
@keyframes gh{{0%,89%,94%,100%{{opacity:0;transform:none}}90%{{opacity:.55;transform:translate(-7px,2px)}}92%{{opacity:.35;transform:translate(6px,-1px)}}}}
.shield{{animation:fade .4s {T0 + 0.2}s both,sh 2.4s {T0 + 1}s ease-in-out infinite}}
@keyframes sh{{50%{{opacity:.55}}}}
.del{{animation:blink 1.6s steps(1) {sub_t + 1}s infinite}}
""")

# ---------- operator.svg ----------
W, H = 900, 400
img = Image.open(AVATAR).convert("L")
img = img.resize((75, 75), Image.LANCZOS).point(lambda v: 0 if v < 58 else min(255, int((v - 58) * 1.7)))
bayer = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
P, X0, Y0 = 4, 40, 44
runs = []
for y in range(75):
    x = 0
    while x < 75:
        on = lambda xx: img.getpixel((xx, y)) / 255 > (bayer[y % 4][xx % 4] + 0.5) / 16
        if on(x):
            s = x
            while x < 75 and on(x):
                x += 1
            runs.append(f'<rect x="{X0 + s * P}" y="{Y0 + y * P}" width="{(x - s) * P}" height="{P - 1}"/>')
        else:
            x += 1
body = [txt(X0, 32, "OPERATOR.PCX", 12, "dim")[0],
        f'<g fill="{A}">{"".join(runs)}</g>',
        f'<rect class="scan" x="{X0}" y="{Y0}" width="300" height="300" fill="{BG}"/>',
        f'<rect x="{X0 - 6}" y="{Y0 - 6}" width="312" height="312" fill="none" stroke="{DIM}" stroke-width="1.5"/>',
        txt(X0, 372, "75x75  1-bit  bayer 4x4", 12, "dim")[0]]

RX, VX = 384, 520
rows = [("Operator", "Timothy Sebastian Darmawan"), ("Base", "Jakarta, Indonesia"),
        ("Track", "Cyber Security"), ("Works on", "detections, infra, tools"),
        ("Desktops", "Arch+niri, Fedora+Hyprland, NixOS"), ("Into", "AI: new models, agents"),
        ("Languages", "English (IELTS 8.0), Indonesian"), ("Method", "build it, break it, rebuild it"),
        ("Status", "open to work")]
body.append(typed(RX, 50, "SYSTEM CONFIGURATION", 0.2, size=15, cls="hot"))
body.append(f'<line x1="{RX}" y1="64" x2="{W - 36}" y2="64" stroke="{DIM}" stroke-width="1.5"/>')
t, ROW0, RH = 2.4, 98, 30
body.append(f'<g class="sel"><rect x="{RX - 10}" y="{ROW0 - 19}" width="{W - 36 - RX + 14}" height="26" fill="{A}" opacity=".13"/>'
            f'<rect x="{RX - 10}" y="{ROW0 - 19}" width="3" height="26" fill="{A}"/></g>')
for i, (k, v) in enumerate(rows):
    y = ROW0 + i * RH
    body.append(f'<g style="animation:fade .15s {t:.2f}s both">{txt(RX, y, k, 14, "dim")[0]}</g>')
    body.append(typed(VX, y, v, t + 0.1))
    t += len(v) * 0.022 + 0.18
body.append(f'<circle class="blink" cx="{VX + len(rows[-1][1]) * CW * 14 + 12:.1f}" cy="{ROW0 + (len(rows) - 1) * RH - 5}" r="4.5" fill="{A}" style="animation-delay:{t:.2f}s"/>')
body.append(txt(RX, 372, "↑↓ select    Enter open    Esc exit", 12, "dim")[0])
n = len(rows)
stops = "".join(f"{i * 100 / n:.2f}%{{transform:translateY({i * RH}px)}}" for i in range(n))
crt("operator.svg", W, H, "\n".join(body), title="Operator profile: dithered avatar and system configuration", css=f"""
.scan{{transform-box:fill-box;transform-origin:bottom;animation:type 2.4s steps(30) .3s both}}
.sel{{animation:fade .2s {t:.2f}s both,sel {n * 1.4:.1f}s steps(1) {t:.2f}s infinite}}
@keyframes sel{{{stops}}}
""")

# ---------- ticker.svg ----------
W, H, SZ = 900, 44, 13
item = "  SECURITY DETECTIONS  ■  LINUX + CLOUD INFRA  ■  AI + AGENTS  ■  BACKEND SERVICES  ■  DEVELOPER TOOLS  ■"
iw = len(item) * CW * SZ
copies = math.ceil(W / iw) + 1
strip = "".join(txt(k * iw, 27, item, SZ)[0] for k in range(copies))
crt("ticker.svg", W, H, f'<g class="mq">{strip}</g>', title="Security detections, Linux and cloud infra, AI and agents, backend services, developer tools",
    css=f".mq{{animation:mq {iw / 40:.1f}s linear infinite}}@keyframes mq{{to{{transform:translateX(-{iw:.1f}px)}}}}")

# ---------- stack.svg ----------
W, H = 900, 176
stack = ["Linux", "Bash", "Python", "TypeScript", "JavaScript", "Rust",
         "C", "Nix", "React", "Node.js", "Phaser", "Git"]
CWID, CH, GAP, MX = 134, 46, 10, 23
body = [typed(MX, 32, "INSTALLED DEVICES", 0.2, size=13, cls="dim")]
for i, name in enumerate(stack):
    x, y = MX + (i % 6) * (CWID + GAP), 50 + (i // 6) * (CH + GAP)
    dur = 0.9 + (i * 0.37) % 1.6
    body.append(f'<g style="animation:fade .2s {0.5 + i * 0.07:.2f}s both">'
                f'<rect x="{x}" y="{y}" width="{CWID}" height="{CH}" rx="3" fill="#1b140a" stroke="{DIM}" stroke-width="1.2"/>'
                f'<circle cx="{x + 14}" cy="{y + CH / 2}" r="3.5" fill="{A}" style="animation:led {dur:.2f}s steps(1) {i * 0.11:.2f}s infinite"/>'
                f'{txt(x + 26, y + 28, name, 14)[0]}</g>')
crt("stack.svg", W, H, "\n".join(body), title="Stack: " + ", ".join(stack),
    css="@keyframes led{50%{opacity:.2}}")

# ---------- eof.svg ----------
W, H = 900, 120
body = [typed(W / 2, 42, "$ systemctl poweroff", 0.3, size=13, cls="dim", anchor="middle"),
        f'<g style="animation:fade .4s 1.2s both">{txt(W / 2, 80, "It is now safe to turn off your computer.", 20, "hot", anchor="middle")[0]}</g>']
crt("eof.svg", W, H, "\n".join(body), title="It is now safe to turn off your computer.", wrap="off", css="""
.off{animation:off 9s 1.2s infinite}
@keyframes off{0%,72%,100%{transform:none;opacity:1}77%{transform:scale(1,.02);opacity:1}81%{transform:scale(0,.02);opacity:.8}82%,92%{transform:scale(0,0);opacity:0}96%{transform:scale(1,.02);opacity:1}}
""")
print("ok", len(runs), "portrait runs")
