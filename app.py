import streamlit as st
import math
import colorsys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import tempfile

st.set_page_config(page_title="Rainbow Flower", layout="centered")
st.title("🌈 Rainbow Flower Animation")

# --- ओरिजिनल लॉजिक ---
N, L, W, R = 18, 290, 70, 22

def bez(p0, p1, p2, n=30):
    pts = []
    for i in range(n + 1):
        t = i / n
        x = (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
        y = (1 - t)**2 * p0 + 2 * (1 - t) * t * p1 + t**2 * p2
        pts.append((x, y))
    return pts

def petal(a, L, w, s):
    d = (math.cos(a), math.sin(a))
    p = (-math.sin(a), math.cos(a))
    tip = (d * L * s, d * L * s)
    cl = (d * L * 0.55 * s + p * w * s, d * L * 0.55 * s + p * w * s)
    cr = (d * L * 0.55 * s - p * w * s, d * L * 0.55 * s - p * w * s)
    return bez((0, 0), cl, tip) + bez(tip, cr, (0, 0))

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
FPS, DRAW_F, HOLD_F = 30, 30 * 16, 30 * 2
FRAMES = DRAW_F + HOLD_F
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

@st.cache_resource
def generate_anim_video():
    # फोन या क्लाउड सर्वर पर बिना एरर के वीडियो सेव करने के लिए अस्थायी पाथ
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        video_p = tmpfile.name
    writer = animation.FFMpegWriter(fps=FPS, bitrate=2500)
    ani.save(video_p, writer=writer, dpi=120, savefig_kwargs={"facecolor": "black"})
    plt.close(fig)
    return video_p

# एनिमेटेड वीडियो को लोड करके दिखाना
with st.spinner("एनिमेशन की वीडियो बन रही है... (इसमें 10-20 सेकंड का समय लग सकता है)"):
    try:
        final_video = generate_anim_video()
        st.video(final_video, autoplay=True, loop=True, muted=True)
        st.success("एनिमेशन तैयार है!")
    except Exception as error:
        st.error(f"त्रुटि: {error}")
      
