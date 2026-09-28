"""
One command: item image -> equipment sprite layers for every base character.

  python tools/item_layers.py --id straw_hat --slot head --image images/items/straw_hat.png
  python tools/item_layers.py --id iron_sword --slot hand_r --image images/items/iron_sword.png
  python tools/item_layers.py --id straw_hat --slot head --proc straw_hat        (built-in test shape, no image)

--slot  head | hand_r | hand_l (bows) | arm_l | back      --bases novice,novice_f (default: every base with a hair layer)
--size/--sink/--grip/--rot/--offset are passed to attach_item.py for fine-tuning the fit
Writes sprites/item_<id>_<base> for each base and assets/icons/<id>.png; the game draws the layer when the item is worn.
"""
import argparse, glob, os, subprocess, sys, time
sys_stdout_utf8 = __import__("sys").stdout.reconfigure(encoding="utf-8", errors="replace")   # Thai names on a cp1252 console

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BLENDER = os.environ.get("BLENDER", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
HYPY = os.environ.get("HY3D_PY", r"D:\AI\Hunyuan3D2_WinPortable\python_standalone\python.exe")
TMP = os.path.join(ROOT, "tools", "blender", "_item_tmp.blend")

ap = argparse.ArgumentParser()
ap.add_argument("--id", required=True)
ap.add_argument("--slot", required=True, choices=["head", "hand_r", "hand_l", "arm_l", "back"])
ap.add_argument("--image"); ap.add_argument("--proc"); ap.add_argument("--bases")
for k in ("size", "sink", "grip", "rot", "offset"):
    ap.add_argument("--" + k)
ap.add_argument("--from", dest="start", default="cutout", choices=["cutout", "gen", "attach"])
a = ap.parse_args()
cut = os.path.join(ROOT, "images", "items", f"{a.id}_cutout.png")
glb = os.path.join(ROOT, "models", f"item_{a.id}.glb")
bases = a.bases.split(",") if a.bases else sorted(os.path.basename(p)[5:] for p in glob.glob(os.path.join(ROOT, "sprites", "hair_*")))


def run(cmd, label):
    t = time.time(); print(f"--- {label} ...", flush=True)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf8", errors="replace")
    for l in (r.stdout + r.stderr).splitlines():
        if any(k in l for k in ("cutout_image:", "hunyuan_generate:", "attach_item:", "render_sprites: wrote")): print("    " + l)
    if r.returncode != 0:
        print("\n".join("    " + l for l in (r.stdout + r.stderr).splitlines()[-25:])); sys.exit(f"{label} failed")
    print(f"    done in {time.time() - t:.0f}s", flush=True)


steps = ["cutout", "gen", "attach"][["cutout", "gen", "attach"].index(a.start):]
if a.image and "cutout" in steps:
    run([BLENDER, "-b", "--factory-startup", "--python-exit-code", "1", "-P", "tools/blender/cutout_image.py", "--",
         "--in", a.image, "--out", cut], "cutout")
    # square icon for the inventory (the full cutout, 256 px)
    run([BLENDER, "-b", "--factory-startup", "--python-exit-code", "1", "-P", "tools/blender/cutout_image.py", "--",
         "--in", a.image, "--out", os.path.join(ROOT, "assets", "icons", f"{a.id}.png"), "--size", "256"], "icon")
if a.image and "gen" in steps:
    run([HYPY, "-s", "tools/hunyuan_generate.py", "--image", cut, "--out", glb, "--faces", "20000"], "Hunyuan3D item model")
src = ["--glb", glb] if a.image else ["--proc", a.proc or a.id]
tune = sum([["--" + k, getattr(a, k)] for k in ("size", "sink", "grip", "rot", "offset") if getattr(a, k)], [])
# hats sit on top of the hair: hair is left out (not an occluder). Everything else is hidden by body and hair where they are in front.
mask = ["--holdout", "Character", "--hide", "Hair"] if a.slot == "head" else ["--holdout", "Character,Hair"]
for base in bases:
    blend = os.path.join(ROOT, "tools", "blender", f"{base}_ai.blend")
    run([BLENDER, "-b", blend, "--python-exit-code", "1", "-P", "tools/blender/attach_item.py", "--", *src, "--slot", a.slot, "--out", TMP, *tune], f"attach to {base}")
    run([BLENDER, "-b", TMP, "--python-exit-code", "1", "-P", "tools/blender/render_sprites.py", "--",
         "--name", f"item_{a.id}_{base}", "--fill", "0.86", *mask, *(["--mirror"] if a.slot == "head" else [])], f"render layer item_{a.id}_{base}")
if os.path.exists(TMP): os.remove(TMP)
print(f"ready: {', '.join('sprites/item_%s_%s' % (a.id, b) for b in bases)}")
