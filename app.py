import streamlit as st
import math
import colorsys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import streamlit.components.v1 as components

st.set_page_config(page_title="Rainbow Flower", layout="centered")
st.title("🌈 Rainbow Flower Animation")

# --- ओरिजिनल पैरामीटर्स ---
N, L, W, R = 18, 290, 70, 22

def bez(x0, y0, x1, y1, x2, y2, n=30):
    pts = []
    # यहाँ X और Y के गणित को पूरी तरह अलग-अलग वेरिएबल्स से फिक्स किया गया है
    for i in range(n + 1):
        t = i / n
        x = (1 - t)**2 * x0 + 2 * (1 - t) * t * x1 + t**2 * x2
        y = (1 - t)**2 * y0 + 2 * (1 - t) * t * y1 + t**2 * y2
        pts.append((x, y))
    return pts

def petal(a, L, w, s):
    dx, dy = math.cos(a), math.sin(a)
    px, py = -math.sin(a), math.cos(a)
    
    # कोआर्डिनेट्स (X, Y) को पूरी तरह अलग करके वेरिएबल्स बनाए गए
    x0, y0 = 0, 0
    x1, y1 = dx * L * 0.55 * s + px * w * s, dy * L * 0.55 * s + py * w * s
    x2, y2 = dx * L * s, dy * L * s
    
    x3, y3 = dx * L * 0.55 * s - px * w * s, dy * L * 0.55 * s - py * w * s
    
    return bez(x0, y0, x1, y1, x2, y2) + bez(x2, y2, x3, y3, x0, y0)

# --- डेटा कलेक्शन ---
segs = []
cols = []
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
FPS = 30
DRAW_F = FPS * 16
FRAMES = DRAW_F + 60
per = max(1, total // DRAW_F)

# --- प्लॉटर सेटअप ---
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

# यह बिना किसी external package के सीधे ब्राउज़र में लाइव HTML प्लेयर बना देगा
html_js = ani.to_jshtml()
plt.close(fig)

# स्क्रीन पर HTML प्लेयर लोड करना
components.html(html_js, height=650)
