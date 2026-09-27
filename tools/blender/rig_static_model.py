"""
Auto-rig a static AI-generated character (Hunyuan3D / TRELLIS / Tripo GLB, OBJ or FBX without a skeleton)
and add Idle / Walk / Attack actions, so render_sprites.py can turn it into game sprites.

  blender -b --factory-startup -P tools/blender/rig_static_model.py -- --in models/ranger.glb --out tools/blender/ranger_ai.blend
  blender -b tools/blender/ranger_ai.blend -P tools/blender/render_sprites.py -- --name ranger

Options: --height 1.1 (metres after normalising)   --faces 60000 (decimate above this)   --depth auto|1.4 (front-to-back thickening)   --turn 0 (extra Z rotation in degrees
if the model does not face -Y)   --attack bow|sword
Assumes a chibi humanoid standing upright, arms down. Weights are computed from distance to the bones (robust on messy AI meshes).
"""
import bpy, bmesh, sys, os, math
import numpy as np
from mathutils import Vector, Matrix

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
A = {"in": None, "out": None, "height": "1.1", "faces": "60000", "turn": "0", "attack": "bow", "depth": "auto"}
for i in range(0, len(argv), 2):
    A[argv[i].lstrip("-")] = argv[i + 1]
if not A["in"] or not A["out"]:
    raise SystemExit("rig_static_model: --in and --out are required")
H = float(A["height"])

bpy.ops.wm.read_factory_settings(use_empty=True)
ext = os.path.splitext(A["in"])[1].lower()
if ext in (".glb", ".gltf"):
    bpy.ops.import_scene.gltf(filepath=A["in"])
elif ext == ".fbx":
    bpy.ops.import_scene.fbx(filepath=A["in"])
elif ext == ".obj":
    bpy.ops.wm.obj_import(filepath=A["in"])
else:
    raise SystemExit("rig_static_model: unsupported file " + ext)

# drop any imported armatures/empties; keep meshes and join them into one character mesh
meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
for o in list(bpy.context.scene.objects):
    if o.type != "MESH":
        for m in meshes:
            if m.parent == o:
                mw = m.matrix_world.copy(); m.parent = None; m.matrix_world = mw
        bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.object.select_all(action="DESELECT")
for m in meshes:
    m.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
body = bpy.context.active_object
body.name = "Character"
for mod in list(body.modifiers):
    bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# normalise: facing -Y (extra --turn if needed), feet on Z=0, centred, fixed height
if float(A["turn"]):
    body.rotation_euler = (0, 0, math.radians(float(A["turn"])))
    bpy.ops.object.transform_apply(rotation=True)
co = np.empty(len(body.data.vertices) * 3, dtype=np.float64)
body.data.vertices.foreach_get("co", co)
co = co.reshape(-1, 3)
lo, hi = co.min(0), co.max(0)
s = H / (hi[2] - lo[2])
co = (co - [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]]) * s
# single-image AI models come out flat front-to-back: thicken them so side views keep chibi proportions
hb = co[(co[:, 2] > 0.6 * H) & (co[:, 2] < 0.95 * H)]
hw = np.percentile(hb[:, 0], 98) - np.percentile(hb[:, 0], 2)
hd = np.percentile(hb[:, 1], 98) - np.percentile(hb[:, 1], 2)
depth = min(max(0.85 * hw / hd, 1.0), 1.8) if A["depth"] == "auto" else float(A["depth"])
co[:, 1] *= depth
print(f"rig_static_model: head depth/width {hd / hw:.2f} -> depth x{depth:.2f}")
body.data.vertices.foreach_set("co", co.ravel())
body.data.update()

# decimate heavy AI meshes (they are often 0.5-2M triangles)
nf = len(body.data.polygons)
target = int(A["faces"])
if nf > target:
    dec = body.modifiers.new("dec", "DECIMATE")
    dec.ratio = target / nf
    bpy.ops.object.modifier_apply(modifier=dec.name)
    print(f"rig_static_model: decimated {nf} -> {len(body.data.polygons)} faces")
bpy.ops.object.shade_smooth()

# --- estimate joints from the silhouette ---
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
def band(z0, z1):
    return co[(co[:, 2] >= z0 * H) & (co[:, 2] < z1 * H)]
feet = band(0.0, 0.12)
legx = max(0.03, np.median(np.abs(feet[:, 0]))) if len(feet) else 0.07
waist = band(0.30, 0.36)
halfw = np.percentile(np.abs(waist[:, 0]), 90) if len(waist) else 0.17
arms = band(0.30, 0.42)
handx = np.percentile(np.abs(arms[:, 0]), 97) if len(arms) else 0.22
handx = min(max(handx * 0.9, halfw * 0.9), halfw * 1.8)
shx = halfw * 0.85
hip, neck = 0.30 * H, 0.55 * H
print(f"rig_static_model: legs x={legx:.3f} waist={halfw:.3f} hands x={handx:.3f}")

arm_data = bpy.data.armatures.new("Rig")
rig = bpy.data.objects.new("Rig", arm_data)
bpy.context.scene.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
EB = {}
def bone(n, h, t, p=None):
    b = arm_data.edit_bones.new(n); b.head, b.tail = h, t
    if p: b.parent = EB[p]
    EB[n] = b
bone("root", (0, 0, 0), (0, 0, 0.1 * H))
bone("body", (0, 0, hip), (0, 0, neck), "root")
bone("head", (0, 0, neck), (0, 0, H), "body")
for sd, k in (("L", 1), ("R", -1)):
    bone(f"arm.{sd}", (k * shx, 0, neck - 0.02 * H), (k * handx, 0, 0.33 * H), "body")
    bone(f"leg.{sd}", (k * legx, 0, hip), (k * legx, 0, 0.03 * H), "root")
segs = {n: (np.array(b.head), np.array(b.tail)) for n, b in EB.items() if n != "root"}
bpy.ops.object.mode_set(mode="OBJECT")

# --- skin weights: Blender heat weighting (clean arm/torso separation), distance weights as fallback ---
names = list(segs)
def distance_weights():
    for vg in list(body.vertex_groups):
        body.vertex_groups.remove(vg)
    D = np.zeros((len(co), len(names)))
    for j, n in enumerate(names):
        a, b = segs[n]; ab = b - a
        t = np.clip(((co - a) @ ab) / (ab @ ab), 0, 1)
        D[:, j] = np.linalg.norm(co - (a + t[:, None] * ab), axis=1)
    D[co[:, 2] > neck + 0.02 * H, :] += 10; D[co[:, 2] > neck + 0.02 * H, names.index("head")] = 0
    for n in ("leg.L", "leg.R"):
        D[co[:, 2] > hip + 0.03 * H, names.index(n)] += 10
    W = 1.0 / np.maximum(D, 1e-4) ** 4
    keep = np.argsort(-W, axis=1)[:, :2]
    groups = {n: body.vertex_groups.new(name=n) for n in names}
    Wn = np.take_along_axis(W, keep, 1); Wn /= Wn.sum(1, keepdims=True)
    for j, n in enumerate(names):
        for c in (0, 1):
            for i in np.nonzero(keep[:, c] == j)[0]:
                groups[n].add([int(i)], float(Wn[i, c]), "REPLACE")
    mod = body.modifiers.new("Armature", "ARMATURE"); mod.object = rig
    body.parent = rig

bpy.ops.object.select_all(action="DESELECT")
bpy.context.view_layer.objects.active = body; body.select_set(True)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT"); bpy.ops.mesh.remove_doubles(threshold=0.0005); bpy.ops.object.mode_set(mode="OBJECT")
co = np.empty(len(body.data.vertices) * 3); body.data.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
rig.select_set(True); bpy.context.view_layer.objects.active = rig
heat_ok = False
try:
    bpy.ops.object.parent_set(type="ARMATURE_AUTO")
    unweighted = sum(1 for v in body.data.vertices if not any(g.weight > 0.01 for g in v.groups))
    heat_ok = unweighted < 0.03 * len(body.data.vertices)
    print(f"rig_static_model: heat weights, unweighted vertices {unweighted}/{len(body.data.vertices)}")
except Exception as e:
    print("rig_static_model: heat weighting failed:", e)
if not heat_ok:
    body.parent = None
    for m in list(body.modifiers):
        if m.type == "ARMATURE": body.modifiers.remove(m)
    distance_weights(); print("rig_static_model: using distance weights")

# arms touching the tunic drag the cloth up when raised: below the shoulders, inside the torso width, arms have no say
if heat_ok:
    zz, xx = co[:, 2], co[:, 0]
    torso = np.nonzero((np.abs(xx) < 0.8 * handx) & (zz < neck - 0.05 * H) & (zz > 0.12 * H))[0]
    vg_body, arm_idx = body.vertex_groups["body"], [body.vertex_groups[n].index for n in ("arm.L", "arm.R")]
    moved = 0
    for i in torso:
        v = body.data.vertices[int(i)]
        w = sum(g.weight for g in v.groups if g.group in arm_idx)
        if w > 0:
            for n in ("arm.L", "arm.R"):
                body.vertex_groups[n].remove([int(i)])
            vg_body.add([int(i)], w + sum(g.weight for g in v.groups if g.group == vg_body.index), "REPLACE"); moved += 1
    print(f"rig_static_model: {moved} torso vertices freed from arm influence")

# a hand-held bow must follow the hand rigidly (its lower limb sits next to the leg bones)
if A["attack"] == "bow":
    zz, xx = co[:, 2], co[:, 0]
    bow = ((zz < 0.28 * H) & (xx > legx + 0.08 * H / 1.1)) | ((zz >= 0.28 * H) & (zz < neck) & (xx > handx * 0.97))
    idx = [int(i) for i in np.nonzero(bow)[0]]
    for vg in body.vertex_groups:
        vg.remove(idx) if vg.name != "arm.L" else None
    body.vertex_groups["arm.L"].add(idx, 1.0, "REPLACE")
    print(f"rig_static_model: {len(idx)} bow vertices bound to arm.L")

# --- actions (same conventions as make_ranger_model.py) ---
rig.animation_data_create()
for pb in rig.pose.bones:
    pb.rotation_mode = "XYZ"
def action(name, keys):
    act = bpy.data.actions.new(name); act.use_fake_user = True
    rig.animation_data.action = act
    for frame, pose in keys.items():
        for pb in rig.pose.bones:
            rx, ry, rz, lz = pose.get(pb.name, (0, 0, 0, 0))
            pb.rotation_euler = [math.radians(v) for v in (rx, ry, rz)]
            pb.location = (0, lz, 0)
            pb.keyframe_insert("rotation_euler", frame=frame); pb.keyframe_insert("location", frame=frame)
action("Idle", {1: {}, 17: {"root": (0, 0, 0, 0.011 * H), "head": (-3, 0, 2, 0), "arm.L": (0, 0, -3, 0), "arm.R": (0, 0, 3, 0)}, 33: {}})
action("Walk", {
    1: {"leg.L": (-26, 0, 0, 0), "leg.R": (26, 0, 0, 0), "arm.L": (14, 0, 0, 0), "arm.R": (-20, 0, 0, 0)},
    5: {"root": (0, 0, 0, 0.025 * H)},
    9: {"leg.L": (26, 0, 0, 0), "leg.R": (-26, 0, 0, 0), "arm.L": (-14, 0, 0, 0), "arm.R": (20, 0, 0, 0)},
    13: {"root": (0, 0, 0, 0.025 * H)},
    17: {"leg.L": (-26, 0, 0, 0), "leg.R": (26, 0, 0, 0), "arm.L": (14, 0, 0, 0), "arm.R": (-20, 0, 0, 0)}})
if A["attack"] == "sword":
    action("Attack", {1: {}, 4: {"arm.R": (-150, 0, 0, 0), "body": (0, 14, 0, 0)}, 8: {"arm.R": (60, 0, 0, 0), "body": (6, -16, 0, 0)}, 13: {}})
else:
    action("Attack", {   # upright archer: raise bow, draw the string back, release - no body lean
        1: {},
        4: {"arm.L": (-84, 0, 0, 0), "arm.R": (-80, 0, 0, 0), "body": (0, 8, 0, 0)},
        8: {"arm.L": (-86, 0, 0, 0), "arm.R": (-52, 0, 0, 0), "body": (0, 12, 0, 0)},
        10: {"arm.L": (-86, 0, 0, 0), "arm.R": (-28, 0, 0, 0), "body": (0, 12, 0, 0)},
        13: {}})
rig.animation_data.action = bpy.data.actions["Idle"]
out = os.path.abspath(A["out"])
bpy.ops.wm.save_as_mainfile(filepath=out)
print("rig_static_model: saved", out)
