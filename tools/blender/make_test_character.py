"""
Builds a small rigged chibi test character with Idle / Walk / Attack actions and saves it
as tools/blender/test_character.blend - used to check the sprite pipeline end to end.

  blender -b --factory-startup -P tools/blender/make_test_character.py
"""
import bpy, math, os
from mathutils import Matrix, Vector

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def mat(name, hexcol):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    h = hexcol.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]  # sRGB -> linear
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (*rgb, 1)
    return m


SKIN, TUNIC, HAIR, PANTS, BOOT, EYE, BLADE = (mat("Skin", "#ffd9b8"), mat("Tunic", "#3f7fd0"), mat("Hair", "#e8b84a"),
                                              mat("Pants", "#4a3a5a"), mat("Boot", "#6b3f22"), mat("Eye", "#2a1c3a"),
                                              mat("Blade", "#dfe7f2"))

# --- armature (character faces -Y, left side is +X) ---
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
bone("body", (0, 0, 0.42), (0, 0, 0.72), "root")
bone("head", (0, 0, 0.72), (0, 0, 1.1), "body")
bone("arm.L", (0.2, 0, 0.7), (0.2, 0, 0.44), "body")
bone("arm.R", (-0.2, 0, 0.7), (-0.2, 0, 0.44), "body")
bone("leg.L", (0.09, 0, 0.42), (0.09, 0, 0.04), "root")
bone("leg.R", (-0.09, 0, 0.42), (-0.09, 0, 0.04), "root")
bpy.ops.object.mode_set(mode="OBJECT")


def part(kind, bone_name, loc, scale, material, rot=(0, 0, 0)):
    if kind == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc, rotation=rot)
    elif kind == "cyl":
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.active_object
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bpy.ops.object.shade_smooth()
    o.data.materials.append(material)
    # rigid bone parenting that keeps the current world transform
    bpy.context.view_layer.update()
    pb = rig.pose.bones[bone_name]
    parent_mat = rig.matrix_world @ pb.matrix @ Matrix.Translation((0, pb.bone.length, 0))
    o.parent, o.parent_type, o.parent_bone = rig, "BONE", bone_name
    o.matrix_parent_inverse = parent_mat.inverted()
    return o


part("cyl", "body", (0, 0, 0.58), (0.17, 0.15, 0.17), TUNIC)
part("sphere", "head", (0, 0, 0.94), (0.25, 0.24, 0.24), SKIN)
part("sphere", "head", (0, 0.04, 1.0), (0.27, 0.26, 0.24), HAIR)
part("sphere", "head", (0, -0.12, 1.13), (0.12, 0.1, 0.06), HAIR)                   # fringe
part("sphere", "head", (0.085, -0.225, 0.92), (0.035, 0.02, 0.05), EYE)
part("sphere", "head", (-0.085, -0.225, 0.92), (0.035, 0.02, 0.05), EYE)
for side, x in (("L", 0.2), ("R", -0.2)):
    part("cyl", f"arm.{side}", (x, 0, 0.58), (0.055, 0.055, 0.13), TUNIC)
    part("sphere", f"arm.{side}", (x, 0, 0.44), (0.06, 0.06, 0.06), SKIN)
for side, x in (("L", 0.09), ("R", -0.09)):
    part("cyl", f"leg.{side}", (x, 0, 0.25), (0.07, 0.07, 0.17), PANTS)
    part("sphere", f"leg.{side}", (x, -0.03, 0.05), (0.08, 0.11, 0.06), BOOT)
part("cube", "arm.R", (-0.2, -0.22, 0.44), (0.02, 0.22, 0.035), BLADE)                  # sword pointing forward


# --- actions ---
rig.animation_data_create()
for pb in rig.pose.bones:
    pb.rotation_mode = "XYZ"


def action(name, keys):
    """keys: {frame: {bone: (rx, ry, rz, lz)}} in degrees; lz = root lift"""
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    rig.animation_data.action = act
    for frame, pose in keys.items():
        for pb in rig.pose.bones:
            rx, ry, rz, lz = pose.get(pb.name, (0, 0, 0, 0))
            pb.rotation_euler = [math.radians(v) for v in (rx, ry, rz)]
            pb.location = (0, lz, 0)  # bone-local Y is up for the upright root bone
            pb.keyframe_insert("rotation_euler", frame=frame)
            pb.keyframe_insert("location", frame=frame)
    return act


action("Idle", {
    1: {"root": (0, 0, 0, 0), "head": (0, 0, 0, 0)},
    17: {"root": (0, 0, 0, 0.018), "head": (-4, 0, 0, 0), "arm.L": (0, 0, -4, 0), "arm.R": (0, 0, 4, 0)},
    33: {"root": (0, 0, 0, 0), "head": (0, 0, 0, 0)},
})
action("Walk", {
    1: {"leg.L": (-32, 0, 0, 0), "leg.R": (32, 0, 0, 0), "arm.L": (28, 0, 0, 0), "arm.R": (-28, 0, 0, 0)},
    5: {"root": (0, 0, 0, 0.035)},
    9: {"leg.L": (32, 0, 0, 0), "leg.R": (-32, 0, 0, 0), "arm.L": (-28, 0, 0, 0), "arm.R": (28, 0, 0, 0)},
    13: {"root": (0, 0, 0, 0.035)},
    17: {"leg.L": (-32, 0, 0, 0), "leg.R": (32, 0, 0, 0), "arm.L": (28, 0, 0, 0), "arm.R": (-28, 0, 0, 0)},
})
action("Attack", {
    1: {"arm.R": (0, 0, 0, 0)},
    4: {"arm.R": (-150, 0, 0, 0), "body": (0, 0, 12, 0)},
    8: {"arm.R": (70, 0, 0, 0), "body": (8, 0, -18, 0)},
    13: {"arm.R": (0, 0, 0, 0), "body": (0, 0, 0, 0)},
})
rig.animation_data.action = bpy.data.actions["Idle"]

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_character.blend")
bpy.ops.wm.save_as_mainfile(filepath=out)
print("make_test_character: saved", out)
