import streamlit as st
import math
import colorsys
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

st.set_page_config(page_title="Rainbow Flower", layout="centered")
st.title("🌈 Rainbow Flower Art")
st.write("आपका जनरेटिव आर्ट नीचे तैयार है:")

# --- ओरिजिनल पैरामीटर्स ---
N, L, W, R = 18, 290, 70, 22

def bez(p0, p1, p2, n=30):
    pts = []
    for i in range(n + 1):
        t = i / n
        # X और Y दोनों कोऑर्डिनेट्स को पूरी तरह अलग करके कैलकुलेशन
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    return pts

def petal(a, L, w, s):
    dx, dy = math.cos(a), math.sin(a)
    px, py = -math.sin(a), math.cos(a)
    
    # कोआर्डिनेट्स को टुपल (Tuple) के रूप में सही किया गया
    tip = (dx * L * s, dy * L * s)
    cl = (dx * L * 0.55 * s + px * w * s, dy * L * 0.55 * s + py * w * s)
    cr = (dx * L * 0.55 * s - px * w * s, dy * L * 0.55 * s - py * w * s)
    
    return bez((0, 0), cl, tip) + bez(tip, cr, (0, 0))

# --- प्लॉटिंग और डिज़ाइन लॉजिक ---
fig, ax = plt.subplots(figsize=(7, 7))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")

segs = []
cols = []

for k in range(N):
    a = 2 * math.pi * k / N
    e = colorsys.hsv_to_rgb(k / N, 0.9, 0.95)
    
    for r in range(R):
        s = (r + 1) / R
        c = tuple((1 - s) * 0.1 + e[i] * s for i in range(3))
        pts = petal(a, L, W, s)
        
        # लाइनों को आपस में जोड़ना
        segs.append(pts)
        cols.append(c)

# स्क्रीन पर लाइनों को ड्रा करना
lc = LineCollection(segs, colors=cols, linewidths=1.6)
ax.add_collection(lc)
ax.set_xlim(-330, 330)
ax.set_ylim(-330, 330)
ax.set_aspect("equal")
ax.axis("off")
plt.tight_layout(pad=0)

# सीधे इमेज को Streamlit पर दिखाना (यह कभी फेल नहीं होता)
st.pyplot(fig)
plt.close(fig)
