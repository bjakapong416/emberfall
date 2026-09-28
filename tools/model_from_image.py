"""
One command: character image -> sprites in the game.
  python tools/model_from_image.py images/ranger_male.jpg --name ranger_m
  python tools/model_from_image.py images/ranger_happy.jpg --name ranger_f3

--name   sprite pack: <class> | <class>_m (male) | <class>_f<1-3> | <class>_m_f<1-3>
--attack bow|sword   --crop x0,y0,x1,y1 (pick one figure out of a sheet)   --from cutout|gen|rig|render (resume)   --no-hair-layer
Steps: background cutout (+ stage art and portrait for base packs) -> Hunyuan3D-2 GLB -> auto-rig -> 288 sprite frames.
"""
import argparse, os, subprocess, sys, time
sys_stdout_utf8 = __import__("sys").stdout.reconfigure(encoding="utf-8", errors="replace")   # Thai names on a cp1252 console

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
HYPY = os.environ.get("HY3D_PY", r"D:\AI\Hunyuan3D2_WinPortable\python_standalone\python.exe")

ap = argparse.ArgumentParser()
ap.add_argument("image")
ap.add_argument("--name", required=True)
ap.add_argument("--attack", default="bow")
ap.add_argument("--crop")
ap.add_argument("--no-hair-layer", action="store_true", help="keep the hair inside the body sprites (no separate hair layer)")
ap.add_argument("--from", dest="start", default="cutout", choices=["cutout", "gen", "rig", "render"])
a = ap.parse_args()
steps = ["cutout", "gen", "rig", "render"][["cutout", "gen", "rig", "render"].index(a.start):]
cut = os.path.join(ROOT, "images", "tripo", f"{a.name}_cutout.png")
glb = os.path.join(ROOT, "models", f"{a.name}.glb")
blend = os.path.join(ROOT, "tools", "blender", f"{a.name}_ai.blend")
import re
is_face = bool(re.search(r"_f\d+$", a.name))   # face variants (<pack>_f1..) reuse the base art and portrait


def run(cmd, label):
    t = time.time(); print(f"--- {label} ...", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf8", errors="replace")
    keep = [l for l in (r.stdout + r.stderr).splitlines() if any(k in l for k in ("cutout_image:", "hunyuan_generate:", "rig_static_model:", "split_hair:", "render_sprites: wrote"))]
    print("\n".join("    " + l for l in keep[-8:]))
    if r.returncode != 0:   # only the exit code counts: Hunyuan prints harmless tracebacks for optional modules
        print("\n".join("    " + l for l in (r.stdout + r.stderr).splitlines()[-25:]))
        sys.exit(f"{label} failed")
    print(f"    done in {time.time() - t:.0f}s", flush=True)


if "cutout" in steps:
    cmd = [BLENDER, "-b", "--factory-startup", "--python-exit-code", "1", "-P", "tools/blender/cutout_image.py", "--", "--in", a.image, "--out", cut]
    if a.crop: cmd += ["--crop", a.crop]
    if not is_face:  # base packs also get the class-select art and HUD portrait
        cmd += ["--art", os.path.join(ROOT, "assets", "classes", f"{a.name}.png"), "--portrait", os.path.join(ROOT, "assets", "portraits", f"{a.name}.png")]
    run(cmd, "1/4 cutout")
if "gen" in steps:
    run([HYPY, "-s", "tools/hunyuan_generate.py", "--image", cut, "--out", glb], "2/4 Hunyuan3D model")
if "rig" in steps:
    run([BLENDER, "-b", "--factory-startup", "--python-exit-code", "1", "-P", "tools/blender/rig_static_model.py", "--", "--in", glb, "--out", blend, "--attack", a.attack], "3/4 auto-rig")
layered = not a.no_hair_layer and not is_face
if "rig" in steps and layered:   # hair becomes its own object -> its own recolourable sprite layer
    run([BLENDER, "-b", blend, "--python-exit-code", "1", "-P", "tools/blender/split_hair.py", "--", "--cutout", cut, "--out", blend], "3b/4 split hair")
if "render" in steps:
    body = ["--hide", "Hair"] if layered else []
    run([BLENDER, "-b", blend, "--python-exit-code", "1", "-P", "tools/blender/render_sprites.py", "--", "--name", a.name, "--fill", "0.86", *body], "4/4 render body sprites")
    if layered:
        run([BLENDER, "-b", blend, "--python-exit-code", "1", "-P", "tools/blender/render_sprites.py", "--", "--name", "hair_" + a.name, "--fill", "0.86", "--holdout", "Character"], "4b/4 render hair layer")
print(f"ready: sprites/{a.name}" + (f" + sprites/hair_{a.name}" if layered else "") + " (registered in sprites/packs.js)")
