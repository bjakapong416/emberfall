"""
Turns the AI concept images in images/ into game assets (runs inside Blender for its bundled numpy):
  blender -b --factory-startup -P tools/process_art.py

- assets/portraits/ranger.png : head crop from the ranger design sheet (front view)
- assets/icons/silver_ring.png : ring icon with the fake checkerboard background removed
"""
import bpy, os
import numpy as np

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "images")


def load(path):
    im = bpy.data.images.load(path)
    w, h = im.size
    px = np.empty(w * h * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    return np.flipud(px.reshape(h, w, 4)).copy()  # top-down rows


def save(arr, path, size):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    h, w = arr.shape[:2]
    im = bpy.data.images.new("tmp", w, h, alpha=True)
    im.pixels.foreach_set(np.flipud(arr).ravel())
    im.scale(size, size)
    sc = bpy.context.scene
    sc.view_settings.view_transform, sc.view_settings.look = "Standard", "None"  # AgX would wash colors out
    st = sc.render.image_settings
    st.file_format, st.color_mode, st.color_depth, st.compression = "PNG", "RGBA", "8", 90
    im.save_render(path, scene=sc)
    bpy.data.images.remove(im)
    print("process_art: wrote", path)


def square(arr, cx, cy, side):
    h, w = arr.shape[:2]
    x0, y0 = max(0, cx - side // 2), max(0, cy - side // 2)
    x1, y1 = min(w, x0 + side), min(h, y0 + side)
    return arr[y0:y1, x0:x1].copy()


def flood(mask, seeds):
    """Grow from seed pixels through mask==True (4-connected)."""
    reg = np.zeros_like(mask)
    for (y, x) in seeds:
        if mask[y, x]:
            reg[y, x] = True
    while True:
        g = reg.copy()
        g[1:] |= reg[:-1]; g[:-1] |= reg[1:]; g[:, 1:] |= reg[:, :-1]; g[:, :-1] |= reg[:, 1:]
        g &= mask
        if (g == reg).all():
            return reg
        reg = g


src = [f for f in os.listdir(IMG) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
sheet = next(f for f in src if "nq1tj6" in f)
ring = next(f for f in src if "te0pr6" in f)

# --- portrait: front-view head of the design sheet ---
a = load(os.path.join(IMG, sheet))
save(square(a, 405, 470, 520), os.path.join(ROOT, "assets", "portraits", "ranger.png"), 256)

# --- ring icon: crop, remove the painted checkerboard ---
a = load(os.path.join(IMG, ring))
a = square(a, 1430, 790, 1300)
im = bpy.data.images.new("crop", a.shape[1], a.shape[0], alpha=True)
im.pixels.foreach_set(np.flipud(a).ravel()); im.scale(640, 640)
px = np.empty(640 * 640 * 4, dtype=np.float32); im.pixels.foreach_get(px); bpy.data.images.remove(im)
a = np.flipud(px.reshape(640, 640, 4)).copy()
rgb = a[..., :3]
bright, chroma = rgb.min(-1), rgb.max(-1) - rgb.min(-1)
bgish = (bright > 0.74) & (chroma < 0.07)
H, W = bgish.shape
seeds = [(y, x) for y in (0, H - 1) for x in range(0, W, 4)] + [(y, x) for x in (0, W - 1) for y in range(0, H, 4)]
seeds += [(412, 300), (440, 350), (380, 330), (470, 320)]  # inside the ring band hole
seeds += [tuple(int(v) for v in s.split(",")) for s in os.environ.get("RING_HOLE_SEEDS", "").split(";") if s]
bg = flood(bgish, seeds)
a[bg, :3] = (0.16, 0.09, 0.08)  # dark fill under transparent pixels -> no white halo when scaled
a[bg, 3] = 0.0
save(a, os.path.join(ROOT, "assets", "icons", "silver_ring.png"), 256)
