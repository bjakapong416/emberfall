"""
Emberfall sprite renderer - turns a rigged Blender character into game sprite sheets.

Usage (from the emberfall folder):
  blender -b path/to/character.blend -P tools/blender/render_sprites.py -- --name ranger

Options (after the "--"):
  --name NAME        pack name. Player packs use the class id: knight / ranger / witch.
                     Other ids the game understands: slime, king, bee, scarecrow, glowslime,
                     treant, moth, mushking, pet, npc0, npc1, npc2
  --out DIR          sprites folder (default: <emberfall>/sprites)
  --idle ACTION      action name for idle   (default: first action whose name contains "idle")
  --walk ACTION      action name for walk   (default: contains "walk" or "run")
  --attack ACTION    action name for attack (default: contains "attack", "slash", "shoot", "cast")
  --size WxH         frame size in pixels (default 320x400 = 4x the game's 80x100 frame)
  --elev DEG         camera elevation in degrees (default 30)
  --fill F           how much of the frame height the character fills, 0..1 (default 0.72)
  --mirror           render 5 directions and mirror the other 3 (faster, for symmetric characters)
  --no-toon          keep the original materials (skip cel shading)
  --outline W        outline width as a fraction of character height (default 0.012, 0 = off)

The character must stand on the world origin, feet at Z=0, facing -Y (Blender "front" view).
Output: sprites/<name>/idle.png, walk.png, attack.png (8 rows = directions, columns = frames)
and a registration line in sprites/packs.js that the game loads at startup.
"""
import bpy, sys, os, math, json, re, tempfile, shutil, time
import numpy as np
from mathutils import Vector

# Must match the game (index.html): ANIM counts and direction order 0=S 1=SW 2=W 3=NW 4=N 5=NE 6=E 7=SE
ANIM = {"idle": 8, "walk": 16, "attack": 12}
DV = [(0, 1), (-.71, .71), (-1, 0), (-.71, -.71), (0, -1), (.71, -.71), (1, 0), (.71, .71)]
FOOT_FROM_TOP = 0.92  # game draws the frame with the feet 8 of 100 units above the bottom


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    a = {"name": None, "out": None, "idle": None, "walk": None, "attack": None, "size": "320x400",
         "elev": 30.0, "fill": 0.72, "mirror": False, "toon": True, "outline": 0.012}
    i = 0
    while i < len(argv):
        k = argv[i].lstrip("-").replace("-", "_")
        if k == "mirror":
            a["mirror"] = True
        elif k == "no_toon":
            a["toon"] = False
        else:
            a[k] = argv[i + 1]; i += 1
        i += 1
    if not a["name"]:
        raise SystemExit("render_sprites: --name is required (e.g. --name ranger)")
    here = os.path.dirname(os.path.abspath(__file__))
    a["out"] = a["out"] or os.path.normpath(os.path.join(here, "..", "..", "sprites"))
    a["w"], a["h"] = [int(x) for x in a["size"].lower().split("x")]
    a["elev"], a["fill"], a["outline"] = float(a["elev"]), float(a["fill"]), float(a["outline"])
    return a


def find_rig():
    arms = [o for o in bpy.context.scene.objects if o.type == "ARMATURE"]
    if arms:
        return arms[0]
    anim = [o for o in bpy.context.scene.objects if o.animation_data and o.animation_data.action]
    return anim[0] if anim else None


def pick_action(explicit, keys):
    if explicit:
        act = bpy.data.actions.get(explicit)
        if not act:
            raise SystemExit(f"render_sprites: action '{explicit}' not found. Actions: {[a.name for a in bpy.data.actions]}")
        return act
    for act in bpy.data.actions:
        if any(k in act.name.lower() for k in keys):
            return act
    return None


def assign_action(obj, act):
    if obj is None:
        return
    if obj.animation_data is None:
        obj.animation_data_create()
    obj.animation_data.action = act
    # Blender 4.4+ slotted actions: make sure a slot is bound
    if act is not None and hasattr(obj.animation_data, "action_slot") and obj.animation_data.action_slot is None:
        slots = getattr(act, "slots", None)
        if slots and len(slots):
            obj.animation_data.action_slot = slots[0]


def char_meshes():
    return [o for o in bpy.context.scene.objects if o.type == "MESH" and o.visible_get()]


def char_height(meshes):
    zs = []
    dg = bpy.context.evaluated_depsgraph_get()
    for o in meshes:
        ev = o.evaluated_get(dg)
        for c in ev.bound_box:
            zs.append((ev.matrix_world @ Vector(c)).z)
    return max(max(zs), 0.1) if zs else 1.8


def toonify(meshes, outline_w):
    """Cel shading: base color x stepped light, plus an inverted-hull outline."""
    done = {}
    ink = bpy.data.materials.new("EF_Outline")
    ink.use_nodes = True
    nt = ink.node_tree
    nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs[0].default_value = (0.09, 0.05, 0.03, 1)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(em.outputs[0], out.inputs[0])
    ink.use_backface_culling = True

    for o in meshes:
        for slot in o.material_slots:
            m = slot.material
            if not m or m.name in done or not m.use_nodes:
                continue
            done[m.name] = 1
            nt = m.node_tree
            bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            outn = next((n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"), None)
            if not bsdf or not outn:
                continue
            base_in = bsdf.inputs["Base Color"]
            alpha_in = bsdf.inputs["Alpha"]
            diff = nt.nodes.new("ShaderNodeBsdfDiffuse")
            s2r = nt.nodes.new("ShaderNodeShaderToRGB")
            bw = nt.nodes.new("ShaderNodeRGBToBW")
            ramp = nt.nodes.new("ShaderNodeValToRGB")
            ramp.color_ramp.interpolation = "CONSTANT"
            ramp.color_ramp.elements[0].position = 0.0
            ramp.color_ramp.elements[0].color = (0.62, 0.58, 0.66, 1)   # shadow tone (slightly cool)
            ramp.color_ramp.elements[1].position = 0.28
            ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
            mul = nt.nodes.new("ShaderNodeMix"); mul.data_type = "RGBA"; mul.blend_type = "MULTIPLY"
            mul.inputs["Factor"].default_value = 1.0
            emit = nt.nodes.new("ShaderNodeEmission")
            nt.links.new(diff.outputs[0], s2r.inputs[0])
            nt.links.new(s2r.outputs["Color"], bw.inputs[0])
            nt.links.new(bw.outputs[0], ramp.inputs[0])
            if base_in.is_linked:
                nt.links.new(base_in.links[0].from_socket, mul.inputs[6])
            else:
                mul.inputs[6].default_value = base_in.default_value
            nt.links.new(ramp.outputs["Color"], mul.inputs[7])
            nt.links.new(mul.outputs[2], emit.inputs[0])
            shader = emit.outputs[0]
            if alpha_in.is_linked:
                tr = nt.nodes.new("ShaderNodeBsdfTransparent")
                mix = nt.nodes.new("ShaderNodeMixShader")
                nt.links.new(alpha_in.links[0].from_socket, mix.inputs[0])
                nt.links.new(tr.outputs[0], mix.inputs[1])
                nt.links.new(emit.outputs[0], mix.inputs[2])
                shader = mix.outputs[0]
            nt.links.new(shader, outn.inputs["Surface"])

    if outline_w > 0:
        for o in meshes:
            if not o.data.materials:
                o.data.materials.append(bpy.data.materials.new("EF_Base"))
            o.data.materials.append(ink)
            mod = o.modifiers.new("EF_Outline", "SOLIDIFY")
            mod.thickness = outline_w
            mod.offset = 1.0
            mod.use_flip_normals = True
            mod.use_rim = False
            mod.material_offset = len(o.data.materials) - 1


def setup_scene(a, height):
    sc = bpy.context.scene
    engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in engines else "BLENDER_EEVEE_NEXT"
    try:
        sc.eevee.taa_render_samples = 16
    except Exception:
        pass
    sc.render.film_transparent = True
    sc.render.resolution_x, sc.render.resolution_y = a["w"], a["h"]
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    try:
        sc.view_settings.view_transform = "Standard"
    except Exception:
        pass

    for o in list(sc.objects):  # remove the file's own cameras and lights
        if o.type in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(o, do_unlink=True)

    pivot = bpy.data.objects.new("EF_Pivot", None)
    sc.collection.objects.link(pivot)
    cam_data = bpy.data.cameras.new("EF_Cam")
    cam_data.type = "ORTHO"
    e = math.radians(a["elev"])
    extent = height * (math.cos(e) + 0.25 * math.sin(e)) / a["fill"]
    cam_data.ortho_scale = extent * max(1.0, a["w"] / a["h"])
    cam_data.shift_y = (FOOT_FROM_TOP - 0.5) * (a["h"] / max(a["w"], a["h"]))
    cam_data.clip_end = 1000
    cam = bpy.data.objects.new("EF_Cam", cam_data)
    sc.collection.objects.link(cam)
    cam.parent = pivot
    d = 20.0
    cam.location = (0, -d * math.cos(e), d * math.sin(e))
    cam.rotation_euler = (math.pi / 2 - e, 0, 0)
    sc.camera = cam

    sun_data = bpy.data.lights.new("EF_Sun", "SUN")
    sun_data.energy = 3.0
    sun_data.use_shadow = False  # self-shadow aliases into blocky patches on toon materials
    sun = bpy.data.objects.new("EF_Sun", sun_data)
    sc.collection.objects.link(sun)
    sun.parent = pivot
    sun.rotation_euler = (math.radians(50), 0, math.radians(-35))  # key light from upper-left of camera

    if sc.world is None:
        sc.world = bpy.data.worlds.new("EF_World")
    sc.world.use_nodes = True
    bg = sc.world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (1, 1, 1, 1)
        bg.inputs[1].default_value = 0.35
    return pivot


def read_png(path):
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    bpy.data.images.remove(img)
    return np.flipud(px.reshape(h, w, 4))  # to top-down rows


def write_png(path, arr):
    h, w = arr.shape[:2]
    img = bpy.data.images.new("EF_Sheet", w, h, alpha=True)
    img.pixels.foreach_set(np.flipud(arr).ravel())
    sc = bpy.context.scene
    st = sc.render.image_settings
    st.file_format, st.color_mode, st.color_depth, st.compression = "PNG", "RGBA", "8", 90
    img.save_render(path, scene=sc)
    bpy.data.images.remove(img)


def main():
    a = parse_args()
    sc = bpy.context.scene
    rig = find_rig()
    actions = {
        "idle": pick_action(a["idle"], ["idle"]),
        "walk": pick_action(a["walk"], ["walk", "run"]),
        "attack": pick_action(a["attack"], ["attack", "slash", "shoot", "cast"]),
    }
    print("render_sprites: rig =", rig.name if rig else None, {k: (v.name if v else None) for k, v in actions.items()})

    meshes = char_meshes()
    assign_action(rig, actions["idle"])
    sc.frame_set(int(actions["idle"].frame_range[0]) if actions["idle"] else sc.frame_start)
    height = char_height(meshes)
    if a["toon"]:
        toonify(meshes, a["outline"] * height)
    pivot = setup_scene(a, height)

    pack_dir = os.path.join(a["out"], a["name"])
    os.makedirs(pack_dir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="ef_sprites_")
    dirs = [0, 4, 5, 6, 7] if a["mirror"] else list(range(8))
    manifest = {"fw": a["w"], "fh": a["h"], "v": int(time.time()), "anims": {}}

    try:
        for anim, n in ANIM.items():
            act = actions[anim]
            if act is None and anim != "idle":
                print(f"render_sprites: no {anim} action, game will reuse idle")
                continue
            assign_action(rig, act)
            f0, f1 = (act.frame_range if act else (sc.frame_current, sc.frame_current + 1))
            sheet = np.zeros((8 * a["h"], n * a["w"], 4), dtype=np.float32)
            for d in dirs:
                dx, dy = DV[d]
                pivot.rotation_euler = (0, 0, math.atan2(-dx, dy))
                for f in range(n):
                    t = f0 + (f1 - f0) * f / n
                    sc.frame_set(int(t), subframe=t - int(t))
                    sc.render.filepath = os.path.join(tmp, f"{anim}_{d}_{f}.png")
                    bpy.ops.render.render(write_still=True)
                    sheet[d * a["h"]:(d + 1) * a["h"], f * a["w"]:(f + 1) * a["w"]] = read_png(sc.render.filepath)
                print(f"render_sprites: {anim} dir {d} done")
            if a["mirror"]:
                for dst, src in ((1, 7), (2, 6), (3, 5)):
                    for f in range(n):
                        cell = sheet[src * a["h"]:(src + 1) * a["h"], f * a["w"]:(f + 1) * a["w"]]
                        sheet[dst * a["h"]:(dst + 1) * a["h"], f * a["w"]:(f + 1) * a["w"]] = cell[:, ::-1]
            write_png(os.path.join(pack_dir, anim + ".png"), sheet)
            manifest["anims"][anim] = {"n": n, "file": f"sprites/{a['name']}/{anim}.png"}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # register the pack: one line per pack in sprites/packs.js (other packs are kept)
    reg = os.path.join(a["out"], "packs.js")
    lines = []
    if os.path.exists(reg):
        with open(reg, encoding="utf8") as fh:
            lines = [l for l in fh.read().splitlines()
                     if l.strip() and not l.startswith(f'registerSpritePack("{a["name"]}"')]
    if not any(l.startswith("//") for l in lines):
        lines.insert(0, "// generated by tools/blender/render_sprites.py - one line per sprite pack")
    lines.append(f'registerSpritePack("{a["name"]}",{json.dumps(manifest)});')
    with open(reg, "w", encoding="utf8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"render_sprites: wrote {pack_dir} and registered '{a['name']}' in {reg}")


main()
