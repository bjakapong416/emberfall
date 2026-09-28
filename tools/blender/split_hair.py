"""
Split the hair of a rigged AI character into its own object ("Hair"), so the game can draw it as a separate,
recolourable layer (and later swap hairstyles or hide it under hats).

  blender -b tools/blender/novice_ai.blend -P tools/blender/split_hair.py -- --cutout images/tripo/novice_cutout.png --out tools/blender/novice_ai.blend

How hair is found: a 2D hair mask is flood-filled on the source image (silver area reachable from the top of the head,
stopped by the drawn outlines), projected onto the front of the model; surfaces facing away use the silver colour above
the hair tips (hair covers the back of the head / upper back).
"""
import bpy, bmesh, os, sys
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
A = {"cutout": None, "out": None, "debug": None}
for i in range(0, len(argv), 2):
    A[argv[i].lstrip("-")] = argv[i + 1]

# ---------- 2D hair mask on the source image ----------
im = bpy.data.images.load(os.path.abspath(A["cutout"]))
w, h = im.size
px = np.empty(w * h * 4, dtype=np.float32); im.pixels.foreach_get(px)
img = np.flipud(px.reshape(h, w, 4))  # top-down
rgb, alpha = img[..., :3], img[..., 3]
mx, mn = rgb.max(-1), rgb.min(-1)
sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
silver = (alpha > .5) & (sat < .17) & (mx > .5)
ys, xs = np.nonzero(alpha > .5)
iy0, iy1, ix0, ix1 = ys.min(), ys.max(), xs.min(), xs.max()
seed = silver.copy(); seed[iy0 + int((iy1 - iy0) * .12):] = False          # silver pixels in the top 12% = hair
reg = seed
while True:
    g = reg.copy()
    g[1:] |= reg[:-1]; g[:-1] |= reg[1:]; g[:, 1:] |= reg[:, :-1]; g[:, :-1] |= reg[:, 1:]
    g &= silver
    if (g == reg).all(): break
    reg = g
mask2d = reg
tips = (np.nonzero(mask2d.any(1))[0].max() - iy0) / (iy1 - iy0)            # lowest hair row, 0=top 1=feet
print(f"split_hair: 2D hair mask {mask2d.sum()} px, hair reaches {tips:.2f} of the body height")
if A["debug"]:
    dbg = img.copy(); dbg[mask2d, :3] = (1, 0, 0)
    d2 = bpy.data.images.new("dbg", w, h, alpha=True); d2.pixels.foreach_set(np.flipud(dbg).ravel())
    d2.filepath_raw = os.path.abspath(A["debug"]); d2.file_format = "PNG"; d2.save()

# ---------- classify polygons ----------
body = bpy.data.objects["Character"]
me = body.data
H = max(v.co.z for v in me.vertices)
xs3 = [v.co.x for v in me.vertices]; X0, X1 = min(xs3), max(xs3)
tex = next(n.image for n in me.materials[0].node_tree.nodes if n.type == "TEX_IMAGE" and n.image)
tw, th = tex.size
tp = np.empty(tw * th * 4, dtype=np.float32); tex.pixels.foreach_get(tp); tp = tp.reshape(th, tw, 4)
uvl = me.uv_layers.active.data
hair = np.zeros(len(me.polygons), dtype=bool)
neck = 0.55 * H
ztips = H * (1 - tips)                                                       # model z of the hair tips
for p in me.polygons:
    u = np.mean([uvl[l].uv for l in p.loop_indices], 0)
    c = tp[min(th - 1, int(u[1] * th)), min(tw - 1, int(u[0] * tw)), :3]
    cmx, cmn = c.max(), c.min(); cs = (cmx - cmn) / cmx if cmx > 0 else 0
    x, z = p.center.x, p.center.z
    ny = p.normal.y  # +Y = back of the character
    white = cs < .03 and cmx > .9    # plain white cloth, not hair
    if ny > 0.25 and z > neck + 0.07 * H and cs < .35 and not white:   # back of the head: all of it is hair (dark strands included)
        hair[p.index] = True
        continue
    if not (cs < .17 and cmx > .42) and not (cs < .3 and cmx < .5 and z > neck):   # silver, or dark hair lines above the neck
        continue
    if z < ztips - 0.02 * H:
        continue
    if ny > 0.25 and not white:       # facing away from the camera: silver above the tips is hair
        hair[p.index] = True
        continue
    # facing the camera or sideways: look it up in the 2D mask (front orthographic projection)
    ix = int(ix0 + (x - X0) / (X1 - X0) * (ix1 - ix0)); iy = int(iy0 + (1 - z / H) * (iy1 - iy0))
    ix, iy = min(max(ix, 0), w - 1), min(max(iy, 0), h - 1)
    near = mask2d[max(0, iy - 3):iy + 4, max(0, ix - 3):ix + 4]
    if near.any() or (z > neck + 0.12 * H and abs(p.normal.x) > .6):
        hair[p.index] = True
# grow into faces mostly surrounded by hair (strand outlines, small gaps), above the hair tips only
bm0 = bmesh.new(); bm0.from_mesh(me); bm0.faces.ensure_lookup_table()
zc = np.array([f.calc_center_median().z for f in bm0.faces])
for _ in range(3):
    add = []
    for f in bm0.faces:
        if hair[f.index] or zc[f.index] < ztips: continue
        nb = {g.index for e in f.edges for g in e.link_faces if g is not f}
        if nb and sum(hair[i] for i in nb) >= max(2, len(nb) * .6): add.append(f.index)
    hair[add] = True
bm0.free()
print(f"split_hair: {hair.sum()} of {len(hair)} faces are hair")

# ---------- separate ----------
bpy.context.view_layer.objects.active = body
for o in bpy.context.selected_objects: o.select_set(False)
body.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
bm = bmesh.from_edit_mesh(me)
bm.faces.ensure_lookup_table()
for f in bm.faces: f.select = bool(hair[f.index])
bmesh.update_edit_mesh(me)
bpy.ops.mesh.separate(type="SELECTED")
bpy.ops.object.mode_set(mode="OBJECT")
new = [o for o in bpy.context.selected_objects if o is not body][0]
new.name = "Hair"
print("split_hair: objects", [o.name for o in bpy.context.scene.objects if o.type == "MESH"])
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(A["out"]))
print("split_hair: saved", os.path.abspath(A["out"]))
