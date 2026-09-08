import streamlit as st
import math
import colorsys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import tempfile

st.set_page_config(page_title="Rainbow Flower", layout="centered")
st.title("🌈 Rainbow Flower Animation")

# --- ओरिजिनल पैरामीटर्स ---
N, L, W, R = 18, 290, 70, 22

def bez(p0, p1, p2, n=30):
    pts = []
    # यहाँ टुपल्स (x, y) को खोलकर बेज़ियर कर्व का एकदम सटीक फॉर्मूला लगाया गया है
    for i in range(n + 1):
        t = i / n
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts

def petal(a, L, w, s):
    dx, dy = math.cos(a), math.sin(a)
    px, py = -math.sin(a), math.cos(a)
    
    # कोऑर्डिनेट्स को सही टुपल फॉर्मेट (X, Y) में सेट किया गया
    tip = (dx * L * s, dy * L * s)
    cl = (dx * L * 0.55 * s + px * w * s, dy * L * 0.55 * s + py * w * s)
    cr = (dx * L * 0.55 * s - px * w * s, dy * L * 0.55 * s - py * w * s)
    
    return bez((0, 0), cl, tip) + bez(tip, cr, (0, 0))

# --- डेटा इकट्ठा करना ---
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
HOLD_F = FPS * 2
FRAMES = DRAW_F + HOLD_F
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

# --- कैशिंग के साथ वीडियो जनरेट करना ---
@st.cache_resource
def generate_flower_video():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        v_path = tmp.name
    writer = animation.FFMpegWriter(fps=FPS, bitrate=2500)
    ani.save(v_path, writer=writer, dpi=120, savefig_kwargs={"facecolor": "black"})
    plt.close(fig)
    return v_path

# स्क्रीन पर लोडिंग स्पिनर और वीडियो प्लेयर
with st.spinner("🎬 बैकएंड में एनिमेशन वीडियो जनरेट हो रही है... कृपया 30 सेकंड रुकें।"):
    try:
        video_file_path = generate_flower_video()
        st.video(video_file_path, autoplay=True, loop=True, muted=True)
        st.success("वीडियो एनिमेशन सफलतापूर्वक लोड हो गया!")
    except Exception as err:
        st.error(f"त्रुटि: {err}")
        
