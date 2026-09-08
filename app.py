import streamlit as st
import math
import colorsys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import streamlit.components.v1 as components

st.set_page_config(page_title="Rainbow Flower", layout="centered")
st.title("🌈 Rainbow Flower Animation")

N, L, W, R = 18, 290, 70, 22

def bez(p0, p1, p2, n=30):
    pts = []
    for i in range(n + 1):
        t = i / n
        # यहाँ X और Y के लिए ओरिजिनल कोआर्डिनेट्स का फॉर्मूला सही किया गया है
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts

def petal(a, L, w, s):
    dx, dy = math.cos(a), math.sin(a)
    px, py = -math.sin(a), math.cos(a)
    
    tip = (dx * L * s, dy * L * s)
    cl = (dx * L * 0.55 * s + px * w * s, dy * L * 0.55 * s + py * w * s)
    cr = (dx * L * 0.55 * s - px * w * s, dy * L * 0.55 * s - py * w * s)
    
    return bez((0, 0), cl, tip) + bez(tip, cr, (0, 0))

segs, cols = [], []
for k in range(N):
    a = 2 * math.pi * k / N
    e = colorsys.hsv_to_rgb(k / N, 0.9, 0.95)
    for r in range(R):
        s = (r + 1) / R
        c = tuple((1 - s) * 0.1 + e[i] * s for i in range(3))
        pts = petal(a, L, W, s)
        segs += list(zip(pts, pts[1:]))
        cols += [c] * (len(pts) - 1)

total = len(segs)
FPS, DRAW_F = 30, 30 * 16
FRAMES = DRAW_F + 60
per = max(1, total // DRAW_F)

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.set_xlim(-330, 330)
ax.set_ylim(-330, 330)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout(pad=0)

lc = LineCollection([], linewidths=1.6)
ax.add_collection(lc)

def update(f):
    e = min(total, (f + 1) * per)
    lc.set_segments(segs[:e])
    lc.set_color(cols[:e])
    return lc,

ani = animation.FuncAnimation(fig, update, frames=FRAMES, blit=True, interval=1000/FPS)

# इसे सीधे HTML प्लेयर में बदलें
html_js = ani.to_jshtml()
plt.close(fig)

# स्क्रीन पर लोड करना
components.html(html_js, height=650)
