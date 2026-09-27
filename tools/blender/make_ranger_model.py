"""
Scripted 3D chibi ranger that follows assets/classes/ranger.png (wolf hood, silver hair, green tunic, bow).
Test model for the sprite pipeline - saved as tools/blender/ranger_model.blend

  blender -b --factory-startup -P tools/blender/make_ranger_model.py
  blender -b tools/blender/ranger_model.blend -P tools/blender/render_sprites.py -- --name ranger3d
"""
import bpy, math, os
from mathutils import Matrix

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
R = math.radians


def mat(name, hexcol, rough=0.6):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    h = hexcol.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1)
    bsdf.inputs["Roughness"].default_value = rough
    return m


M = {k: mat(k, v) for k, v in {
    "skin": "#fbe3cc", "hair": "#d9dce6", "hood": "#55565e", "cream": "#efe2c4", "ink": "#2a1c1c",
    "iris": "#4a7fb5", "white": "#ffffff", "blush": "#f4a3a3", "tunic": "#5f9440", "cape": "#4e7d34",
    "trim": "#d9c68f", "leather": "#7a4a24", "dark_leather": "#5a3418", "gold": "#e9b84a",
    "legging": "#3a302c", "boot": "#8a5a30", "shorts": "#6b4428", "wood": "#8a5a2a", "string": "#efe8d8"}.items()}

# ---------------- armature ----------------
arm_data = bpy.data.armatures.new("Rig")
rig = bpy.data.objects.new("Rig", arm_data)
sc.collection.objects.link(rig)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="EDIT")
B = {}


def bone(name, head, tail, parent=None):
    b = arm_data.edit_bones.new(name)
    b.head, b.tail = head, tail
    if parent:
        b.parent = B[parent]
    B[name] = b


bone("root", (0, 0, 0), (0, 0, 0.1))
bone("body", (0, 0, 0.30), (0, 0, 0.58), "root")
bone("head", (0, 0, 0.58), (0, 0, 1.0), "body")
bone("arm.L", (0.17, 0, 0.56), (0.21, 0, 0.37), "body")
bone("arm.R", (-0.17, 0, 0.56), (-0.21, 0, 0.37), "body")
bone("leg.L", (0.07, 0, 0.30), (0.07, 0, 0.03), "root")
bone("leg.R", (-0.07, 0, 0.30), (-0.07, 0, 0.03), "root")
bpy.ops.object.mode_set(mode="OBJECT")


def attach(o, bone_name):
    bpy.context.view_layer.update()
    pb = rig.pose.bones[bone_name]
    pm = rig.matrix_world @ pb.matrix @ Matrix.Translation((0, pb.bone.length, 0))
    o.parent, o.parent_type, o.parent_bone = rig, "BONE", bone_name
    o.matrix_parent_inverse = pm.inverted()


def finish(o, material, bone_name, scale=(1, 1, 1), smooth=True):
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if smooth:
        bpy.ops.object.shade_smooth()
    o.data.materials.append(M[material])
    attach(o, bone_name)
    return o


def sphere(loc, scale, material, bone_name, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=loc, rotation=rot)
    return finish(bpy.context.active_object, material, bone_name, scale)


def cyl(loc, r, depth, material, bone_name, rot=(0, 0, 0), r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    return finish(bpy.context.active_object, material, bone_name)


def torus(loc, R_, r, material, bone_name, rot=(0, 0, 0), scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R_, minor_radius=r, major_segments=40, minor_segments=10, location=loc, rotation=rot)
    return finish(bpy.context.active_object, material, bone_name, scale)


def box(loc, scale, material, bone_name, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=2, location=loc, rotation=rot)
    return finish(bpy.context.active_object, material, bone_name, scale, smooth=False)


def cone(loc, r, depth, material, bone_name, rot=(0, 0, 0), scale=(1, 1, 1), verts=24):
    bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=0, depth=depth, location=loc, rotation=rot)
    return finish(bpy.context.active_object, material, bone_name, scale)


def cut(obj, cutter):
    mod = obj.modifiers.new("cut", "BOOLEAN")
    mod.operation, mod.object = "DIFFERENCE", cutter
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    bpy.data.objects.remove(cutter, do_unlink=True)


# ---------------- head ----------------
sphere((0, 0, 0.79), (0.2, 0.19, 0.195), "skin", "head")
sphere((0, 0.04, 0.80), (0.2, 0.19, 0.2), "hair", "head")                      # hair volume behind the face
for i, x in enumerate((-0.12, -0.06, 0.0, 0.06, 0.12)):                            # bangs
    sphere((x, -0.168 + abs(x) * 0.35, 0.85 - abs(x) * 0.2), (0.042, 0.03, 0.075), "hair", "head", rot=(R(-12), R(x * 180), 0))
for k in (-1, 1):                                                                  # side locks to the chin
    sphere((k * 0.15, -0.13, 0.7), (0.028, 0.024, 0.085), "hair", "head", rot=(0, R(-k * 8), 0))
for k in (-1, 1):                                                                  # anime eyes
    x = k * 0.078
    sphere((x, -0.176, 0.765), (0.046, 0.014, 0.06), "iris", "head", rot=(0, 0, R(k * 22)))
    sphere((x - k * 0.004, -0.186, 0.745), (0.022, 0.008, 0.028), "ink", "head", rot=(0, 0, R(k * 22)))
    sphere((x - 0.014, -0.19, 0.785), (0.012, 0.006, 0.014), "white", "head")
    box((x + k * 0.004, -0.182, 0.822), (0.044, 0.006, 0.0065), "ink", "head", rot=(0, R(k * 10), R(k * 22)))
    sphere((k * 0.118, -0.155, 0.715), (0.032, 0.006, 0.016), "blush", "head", rot=(0, 0, R(k * 35)))
sphere((0, -0.19, 0.695), (0.02, 0.006, 0.007), "ink", "head")                     # smile

# wolf hood with an opening for the face
hood = sphere((0, 0.035, 0.835), (0.235, 0.23, 0.225), "hood", "head")
bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=(0, -0.15, 0.72))
cutter = bpy.context.active_object
cutter.scale = (0.165, 0.17, 0.2)
cut(hood, cutter)
sphere((0, -0.15, 0.97), (0.13, 0.07, 0.065), "cream", "head", rot=(R(-25), 0, 0))   # wolf face patch
for k in (-1, 1):
    sphere((k * 0.062, -0.207, 0.995), (0.017, 0.012, 0.019), "ink", "head")
    cone((k * 0.05, -0.2, 0.9), 0.014, 0.04, "white", "head", rot=(R(180), 0, 0))    # fangs
    cone((k * 0.14, 0.03, 1.1), 0.09, 0.2, "hood", "head", rot=(0, R(k * 22), 0), scale=(1, 0.55, 1))   # ears
    cone((k * 0.138, -0.005, 1.09), 0.055, 0.13, "cream", "head", rot=(0, R(k * 22), 0), scale=(1, 0.3, 1))
sphere((0, -0.222, 0.935), (0.028, 0.02, 0.02), "ink", "head")                      # nose

# ---------------- body ----------------
cyl((0, 0.01, 0.6), 0.165, 0.07, "hood", "body", r2=0.12)                             # hood cowl on the shoulders
sphere((0, -0.178, 0.595), (0.028, 0.028, 0.028), "gold", "body")                 # bell
cyl((0, 0, 0.43), 0.19, 0.30, "tunic", "body", r2=0.12)
cyl((0, 0, 0.53), 0.2, 0.09, "cape", "body", r2=0.14)                             # shoulder capelet
torus((0, 0, 0.49), 0.195, 0.012, "trim", "body")
torus((0, 0, 0.29), 0.19, 0.014, "trim", "body")                                  # tunic hem trim
cyl((0, 0, 0.395), 0.168, 0.035, "dark_leather", "body")                         # belt
box((0, -0.17, 0.395), (0.03, 0.01, 0.022), "gold", "body")
for k in (-1, 1):
    box((k * 0.13, -0.12, 0.35), (0.045, 0.03, 0.042), "leather", "body", rot=(0, 0, R(k * 30)))  # pouches
box((0.0, -0.152, 0.47), (0.018, 0.008, 0.19), "leather", "body", rot=(0, R(48), 0))   # cross strap
cyl((0, 0, 0.265), 0.172, 0.07, "shorts", "body", r2=0.155)
# quiver on the back
q = cyl((-0.07, 0.16, 0.52), 0.04, 0.3, "leather", "body", rot=(R(-15), R(-25), 0))
for i in range(3):
    cone((-0.14 + i * 0.022, 0.2 + i * 0.01, 0.7 + i * 0.01), 0.018, 0.06, "cream", "body", rot=(R(-15), R(-25), 0))

# ---------------- arms ----------------
for side, k in (("L", 1), ("R", -1)):
    b = f"arm.{side}"
    cyl((k * 0.19, 0, 0.47), 0.047, 0.18, "tunic", b, rot=(0, R(k * 12), 0))
    torus((k * 0.205, 0, 0.39), 0.045, 0.018, "cream", b, rot=(0, R(k * 12), 0))  # fur cuffs
    sphere((k * 0.212, -0.01, 0.35), (0.043, 0.043, 0.045), "leather", b)          # fingerless gloves

# bow in the left hand (character's left = +X)
cu = bpy.data.curves.new("Bow", "CURVE")
cu.dimensions, cu.bevel_depth, cu.bevel_resolution = "3D", 0.012, 3
sp = cu.splines.new("BEZIER")
sp.bezier_points.add(2)
for bp, co in zip(sp.bezier_points, [(0.22, 0.03, 0.73), (0.26, -0.07, 0.36), (0.22, 0.03, 0.02)]):
    bp.co = co
    bp.handle_left_type = bp.handle_right_type = "AUTO"
bow = bpy.data.objects.new("Bow", cu)
sc.collection.objects.link(bow)
bpy.context.view_layer.objects.active = bow
bow.select_set(True)
bpy.ops.object.convert(target="MESH")
bow = bpy.context.active_object
bow.data.materials.append(M["wood"])
bpy.ops.object.shade_smooth()
attach(bow, "arm.L")
s = cyl((0.22, 0.03, 0.375), 0.004, 0.71, "string", "arm.L")                     # bow string
box((0.26, -0.07, 0.36), (0.02, 0.02, 0.045), "trim", "arm.L")                    # grip wrap

# ---------------- legs ----------------
for side, k in (("L", 1), ("R", -1)):
    b = f"leg.{side}"
    cyl((k * 0.07, 0, 0.19), 0.05, 0.2, "legging", b)
    cyl((k * 0.07, -0.005, 0.07), 0.062, 0.11, "boot", b)
    sphere((k * 0.07, -0.04, 0.03), (0.06, 0.085, 0.035), "boot", b)
    torus((k * 0.07, 0, 0.13), 0.06, 0.022, "cream", b)                             # fur boot cuffs

# ---------------- actions ----------------
rig.animation_data_create()
for pb in rig.pose.bones:
    pb.rotation_mode = "XYZ"


def action(name, keys):
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    rig.animation_data.action = act
    for frame, pose in keys.items():
        for pb in rig.pose.bones:
            rx, ry, rz, lz = pose.get(pb.name, (0, 0, 0, 0))
            pb.rotation_euler = [R(v) for v in (rx, ry, rz)]
            pb.location = (0, lz, 0)
            pb.keyframe_insert("rotation_euler", frame=frame)
            pb.keyframe_insert("location", frame=frame)
    return act


action("Idle", {
    1: {},
    17: {"root": (0, 0, 0, 0.012), "head": (-3, 0, 2, 0), "arm.L": (0, 0, -3, 0), "arm.R": (0, 0, 3, 0)},
    33: {},
})
action("Walk", {
    1: {"leg.L": (-30, 0, 0, 0), "leg.R": (30, 0, 0, 0), "arm.L": (18, 0, 0, 0), "arm.R": (-24, 0, 0, 0)},
    5: {"root": (0, 0, 0, 0.03)},
    9: {"leg.L": (30, 0, 0, 0), "leg.R": (-30, 0, 0, 0), "arm.L": (-18, 0, 0, 0), "arm.R": (24, 0, 0, 0)},
    13: {"root": (0, 0, 0, 0.03)},
    17: {"leg.L": (-30, 0, 0, 0), "leg.R": (30, 0, 0, 0), "arm.L": (18, 0, 0, 0), "arm.R": (-24, 0, 0, 0)},
})
action("Attack", {   # upright archer: raise bow, draw the string back, release - no body lean
        1: {},
        4: {"arm.L": (-84, 0, 0, 0), "arm.R": (-80, 0, 0, 0), "body": (0, 8, 0, 0)},
        8: {"arm.L": (-86, 0, 0, 0), "arm.R": (-52, 0, 0, 0), "body": (0, 12, 0, 0)},
        10: {"arm.L": (-86, 0, 0, 0), "arm.R": (-28, 0, 0, 0), "body": (0, 12, 0, 0)},
        13: {}})
rig.animation_data.action = bpy.data.actions["Idle"]

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranger_model.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("make_ranger_model: saved", out)
