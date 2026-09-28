"""
Remove the paper/white background (and the soft ground shadow) from one full-body character image.
Runs inside Blender for numpy:
  blender -b --factory-startup -P tools/blender/cutout_image.py -- --in images/x.jpg --out images/tripo/x_cutout.png [--crop x0,y0,x1,y1]
Output: square RGBA PNG (1024 px) with the character centred - the input format image-to-3D tools like best.
"""
import bpy, os, sys
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
A = {"in": None, "out": None, "crop": None, "size": "1024", "art": None, "portrait": None}
for i in range(0, len(argv), 2):
    A[argv[i].lstrip("-")] = argv[i + 1]


def load(path):
    im = bpy.data.images.load(path)
    w, h = im.size
    px = np.empty(w * h * 4, dtype=np.float32)
    im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    return np.flipud(px.reshape(h, w, 4)).copy()


def flood(mask, seeds):
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


def erode(m, k):
    for _ in range(k):
        e = m.copy()
        e[1:] &= m[:-1]; e[:-1] &= m[1:]; e[:, 1:] &= m[:, :-1]; e[:, :-1] &= m[:, 1:]
        m = e
    return m


a = load(os.path.abspath(A["in"]))
if A["crop"]:
    x0, y0, x1, y1 = [int(v) for v in A["crop"].split(",")]
    a = a[y0:y1, x0:x1].copy()
# work at <= 900 px on the long side (flood fill cost), upscale again when saving
H0, W0 = a.shape[:2]
sc = min(1.0, 900 / max(H0, W0))
if sc < 1:
    im = bpy.data.images.new("w", W0, H0, alpha=True)
    im.pixels.foreach_set(np.flipud(a).ravel()); im.scale(int(W0 * sc), int(H0 * sc))
    px = np.empty(im.size[0] * im.size[1] * 4, dtype=np.float32); im.pixels.foreach_get(px)
    a = np.flipud(px.reshape(im.size[1], im.size[0], 4)).copy(); bpy.data.images.remove(im)
rgb = a[..., :3]
bright, chroma = rgb.min(-1), rgb.max(-1) - rgb.min(-1)
H, W = bright.shape
edge = [(y, x) for y in (0, H - 1) for x in range(0, W, 2)] + [(y, x) for x in (0, W - 1) for y in range(0, H, 2)]
bg = flood((bright > 0.72) & (chroma < 0.07), edge)                 # paper, grid lines, ground shadow
white = (bright > 0.93) & (chroma < 0.04)
bg |= flood(white, list(zip(*np.nonzero(erode(white, 8)))))          # enclosed paper gaps (between legs, bow and body)
a[bg, :3] = (0.16, 0.09, 0.08)
a[bg, 3] = 0.0
# crop to the character and centre it on a square canvas
ys, xs = np.nonzero(~bg)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
cut = a[y0:y1, x0:x1]
side = int(max(cut.shape[:2]) * 1.08)
canvas = np.zeros((side, side, 4), dtype=np.float32)
oy, ox = (side - cut.shape[0]) // 2, (side - cut.shape[1]) // 2
canvas[oy:oy + cut.shape[0], ox:ox + cut.shape[1]] = cut
out = os.path.abspath(A["out"])
os.makedirs(os.path.dirname(out), exist_ok=True)
im = bpy.data.images.new("o", side, side, alpha=True)
im.pixels.foreach_set(np.flipud(canvas).ravel()); im.scale(int(A["size"]), int(A["size"]))
scn = bpy.context.scene
scn.view_settings.view_transform, scn.view_settings.look = "Standard", "None"
st = scn.render.image_settings
st.file_format, st.color_mode, st.color_depth, st.compression = "PNG", "RGBA", "8", 90
im.save_render(out, scene=scn)
print("cutout_image: wrote", out)


def save_arr(arr, path, w, h):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im = bpy.data.images.new("x", arr.shape[1], arr.shape[0], alpha=True)
    im.pixels.foreach_set(np.flipud(arr).ravel()); im.scale(w, h); im.save_render(path, scene=scn); bpy.data.images.remove(im)
    print("cutout_image: wrote", path)


if A["art"]:        # full-body art for the class select stage
    save_arr(cut, os.path.abspath(A["art"]), 420, int(420 * cut.shape[0] / cut.shape[1]))
if A["portrait"]:   # head crop for the HUD portrait (chibi: the head is the top ~45% of the body)
    hh = int(cut.shape[0] * 0.46); cx = cut.shape[1] // 2
    x0p = max(0, cx - hh // 2); sq = cut[0:hh, x0p:x0p + hh]
    pad = np.zeros((hh, hh, 4), dtype=np.float32); pad[:sq.shape[0], :sq.shape[1]] = sq
    save_arr(pad, os.path.abspath(A["portrait"]), 256, 256)
