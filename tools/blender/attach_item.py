"""
Attach an equipment item rigidly to a bone of a rigged base character, so it can be rendered as its own sprite layer.

  blender -b tools/blender/novice_ai.blend -P tools/blender/attach_item.py -- --glb models/item_straw_hat.glb --slot head --out <tmp>.blend
  blender -b tools/blender/novice_ai.blend -P tools/blender/attach_item.py -- --proc sword --slot hand_r --out <tmp>.blend

--slot    head (hats, helmets) | hand_r (weapons) | hand_l (bows) | arm_l (shields) | back (capes, wings)
--size    item size as a fraction of the character height (defaults per slot)
--sink    head items: how far the item's bottom sits below the top of the head, as a fraction of the head height
--grip    weapons: where the hand holds it, as a fraction of the length from the handle end
--rot     extra rotation x,y,z in degrees     --offset  extra offset x,y,z as fractions of the character height
Item images are expected upright and seen from the front (hats: opening at the bottom; weapons: handle at the bottom).
"""
import bpy, os, sys, math
from mathutils import Matrix, Vector, Euler

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
A = {"glb": None, "proc": None, "slot": "head", "out": None, "size": None, "sink": "0.2", "grip": "0.1", "rot": "0,0,0", "offset": "0,0,0"}
for i in range(0, len(argv), 2):
    A[argv[i].lstrip("-")] = argv[i + 1]
DEF_SIZE = {"head": 1.0, "hand_r": 0.62, "hand_l": 0.70, "arm_l": 0.30, "back": 0.55}   # head: x head width; others: x character height
size = float(A["size"]) if A["size"] else DEF_SIZE[A["slot"]]

sc = bpy.context.scene
rig = next(o for o in sc.objects if o.type == "ARMATURE")
body = [o for o in sc.objects if o.type == "MESH" and o.name in ("Character", "Hair")]
dg = bpy.context.evaluated_depsgraph_get()
pts = [o.matrix_world @ v.co for o in body for v in o.data.vertices]
H = max(p.z for p in pts)


def mat(name, hexcol):
    m = bpy.data.materials.new(name); m.use_nodes = True
    h = hexcol.lstrip("#"); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*rgb, 1)
    return m


def prim(kind, loc, scale, material, rot=(0, 0, 0), **kw):
    getattr(bpy.ops.mesh, f"primitive_{kind}_add")(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object; o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if kind != "cube": bpy.ops.object.shade_smooth()
    o.data.materials.append(material); return o


# ---------- build or import the item as one object named "Item" ----------
before = set(sc.objects)
if A["glb"]:
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(A["glb"]))
    parts = [o for o in sc.objects if o not in before and o.type == "MESH"]
    for o in [o for o in sc.objects if o not in before and o.type != "MESH"]:
        for p in parts:
            if p.parent == o: mw = p.matrix_world.copy(); p.parent = None; p.matrix_world = mw
        bpy.data.objects.remove(o, do_unlink=True)
else:  # built-in test shapes (the same orientation rules as item images)
    k = A["proc"]
    if k == "straw_hat":
        straw, band = mat("Straw", "#e8c46a"), mat("Band", "#c0443a")
        parts = [prim("cylinder", (0, 0, 0.03), (0.62, 0.62, 0.03), straw, vertices=48),
                 prim("uv_sphere", (0, 0, 0.06), (0.34, 0.34, 0.3), straw, segments=48, ring_count=24),
                 prim("cylinder", (0, 0, 0.11), (0.345, 0.345, 0.05), band, vertices=48)]
    elif k == "sword":
        steel, gold, grip = mat("Steel", "#dfe7f2"), mat("Gold", "#e9b84a"), mat("Grip", "#6b3f22")
        parts = [prim("cylinder", (0, 0, 0.09), (0.035, 0.035, 0.09), grip, vertices=16),
                 prim("uv_sphere", (0, 0, 0.0), (0.05, 0.05, 0.05), gold),
                 prim("cube", (0, 0, 0.2), (0.16, 0.04, 0.025), gold),
                 prim("cube", (0, 0, 0.62), (0.055, 0.012, 0.4), steel),
                 prim("cone", (0, 0, 1.06), (0.055, 0.012, 0.05), steel, vertices=4, rot=(0, 0, math.radians(45)))]
    elif k == "shield":
        wood, iron = mat("Wood", "#8a5a2a"), mat("Iron", "#aab7c4")
        parts = [prim("cylinder", (0, 0, 0), (0.5, 0.5, 0.05), wood, rot=(math.radians(90), 0, 0), vertices=48),
                 prim("torus", (0, -0.02, 0), (1, 1, 1), iron, rot=(math.radians(90), 0, 0), major_radius=0.5, minor_radius=0.04),
                 prim("uv_sphere", (0, -0.06, 0), (0.12, 0.08, 0.12), iron)]
    else:
        raise SystemExit("attach_item: --glb or --proc straw_hat|sword|shield is required")
bpy.ops.object.select_all(action="DESELECT")
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active = parts[0]
if len(parts) > 1: bpy.ops.object.join()
item = bpy.context.active_object; item.name = "Item"
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def bbox(o):
    vs = [o.matrix_world @ v.co for v in o.data.vertices]
    return Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs))), Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))


def move(o, m):
    o.data.transform(m); o.data.update()


lo, hi = bbox(item)
move(item, Matrix.Translation(-(lo + hi) / 2))   # centre on the origin
flat = (hi.y - lo.y) / max(hi.x - lo.x, 1e-6)
if flat < 0.2:
    print(f"attach_item: WARNING flat item (depth/width {flat:.2f}) - fine for headbands; hats/hoods need an image seen from slightly above")
rx, ry, rz = [math.radians(float(v)) for v in A["rot"].split(",")]
ox, oy, oz = [float(v) * H for v in A["offset"].split(",")]
slot = A["slot"]

if slot == "head":
    head = [p for p in pts if p.z > 0.58 * H]
    hx0, hx1 = min(p.x for p in head), max(p.x for p in head); hy0, hy1 = min(p.y for p in head), max(p.y for p in head)
    htop, hbot = max(p.z for p in head), 0.58 * H
    move(item, Euler((rx, ry, rz)).to_matrix().to_4x4())
    lo, hi = bbox(item); s = (hx1 - hx0) * size / (hi.x - lo.x)
    move(item, Matrix.Scale(s, 4)); lo, hi = bbox(item)
    target = Vector(((hx0 + hx1) / 2, (hy0 + hy1) / 2, htop - float(A["sink"]) * (htop - hbot) - lo.z))
    move(item, Matrix.Translation(target + Vector((ox, oy, oz)))); bone = "head"
elif slot == "hand_r":
    lo, hi = bbox(item); length = hi.z - lo.z
    move(item, Matrix.Scale(size * H / length, 4)); lo, hi = bbox(item)
    gz = lo.z + float(A["grip"]) * (hi.z - lo.z)
    move(item, Matrix.Translation((0, 0, -gz)))                                   # grip point at the origin
    held = Euler((math.radians(180 - 20) + rx, ry, rz)).to_matrix().to_4x4()      # blade down, tipped 20° forward
    move(item, held)
    hand = rig.matrix_world @ rig.pose.bones["arm.R"].tail
    move(item, Matrix.Translation(hand + Vector((ox, oy - 0.01 * H, oz)))); bone = "arm.R"
elif slot == "hand_l":   # bows: upright at the left side, held at the grip (default: the middle)
    lo, hi = bbox(item); move(item, Matrix.Scale(size * H / (hi.z - lo.z), 4)); lo, hi = bbox(item)
    grip = float(A["grip"]) if A["grip"] != "0.1" else 0.5
    move(item, Matrix.Translation((0, 0, -(lo.z + grip * (hi.z - lo.z)))))
    move(item, Euler((rx, ry, rz)).to_matrix().to_4x4())
    hand = rig.matrix_world @ rig.pose.bones["arm.L"].tail
    move(item, Matrix.Translation(hand + Vector((0.02 * H + ox, -0.02 * H + oy, oz)))); bone = "arm.L"
elif slot == "arm_l":
    lo, hi = bbox(item); d = max(hi.x - lo.x, hi.z - lo.z)
    move(item, Matrix.Scale(size * H / d, 4))
    move(item, Euler((rx, ry, math.radians(55) + rz)).to_matrix().to_4x4())       # face out and forward
    pb = rig.pose.bones["arm.L"]; at = rig.matrix_world @ (pb.head + (pb.tail - pb.head) * 0.7)
    move(item, Matrix.Translation(at + Vector((0.07 * H + ox, -0.02 * H + oy, oz)))); bone = "arm.L"
elif slot == "back":
    lo, hi = bbox(item); move(item, Matrix.Scale(size * H / (hi.z - lo.z), 4))
    move(item, Euler((rx, ry, rz)).to_matrix().to_4x4())
    chest = [p for p in pts if 0.35 * H < p.z < 0.55 * H]; back_y = max(p.y for p in chest)
    lo, hi = bbox(item)
    move(item, Matrix.Translation(Vector((0, back_y - lo.y + 0.01 * H, 0.46 * H)) + Vector((ox, oy, oz)))); bone = "body"
else:
    raise SystemExit("attach_item: unknown --slot " + slot)

# rigid bone parenting that keeps the placed world transform
bpy.context.view_layer.update()
pb = rig.pose.bones[bone]
pm = rig.matrix_world @ pb.matrix @ Matrix.Translation((0, pb.bone.length, 0))
item.parent, item.parent_type, item.parent_bone = rig, "BONE", bone
item.matrix_parent_inverse = pm.inverted()
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(A["out"]))
print(f"attach_item: {slot} item on bone {bone}, saved {os.path.abspath(A['out'])}")
