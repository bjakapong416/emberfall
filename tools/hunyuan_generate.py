"""
Image -> textured 3D model (GLB) with Hunyuan3D-2 (portable pack in D:\\AI\\Hunyuan3D2_WinPortable), no web UI.
Runs with the pack's own Python:

  D:\\AI\\Hunyuan3D2_WinPortable\\python_standalone\\python.exe -s tools\\hunyuan_generate.py ^
      --image images\\tripo\\ranger_front.png --out models\\ranger.glb

Options: --no-tex (shape only)  --faces 40000  --steps 30  --seed 1234  --octree 256  --profile 2
Profile 2 = "high RAM, low VRAM" (fits an 8 GB GPU with 32 GB+ system RAM). Use 4 or 5 on machines with less RAM.
"""
import argparse, os, sys, time

PACK = os.environ.get("HY3D_PACK", r"D:\AI\Hunyuan3D2_WinPortable")
REPO = os.path.join(PACK, "Hunyuan3D-2")
os.environ.setdefault("HF_HUB_CACHE", os.path.join(PACK, "HuggingFaceHub"))
os.environ.setdefault("HY3DGEN_MODELS", os.path.join(PACK, "HuggingFaceHub"))

ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--no-tex", action="store_true")
ap.add_argument("--faces", type=int, default=40000)
ap.add_argument("--steps", type=int, default=30)
ap.add_argument("--seed", type=int, default=1234)
ap.add_argument("--octree", type=int, default=256)
ap.add_argument("--guidance", type=float, default=5.0)
ap.add_argument("--profile", type=int, default=2)
ap.add_argument("--model", default="tencent/Hunyuan3D-2mini")
ap.add_argument("--subfolder", default="hunyuan3d-dit-v2-mini-turbo")
a = ap.parse_args()
img_path, out_path = os.path.abspath(a.image), os.path.abspath(a.out)

sys.path.insert(0, REPO)
os.chdir(REPO)  # the library loads some assets relative to the repo
import torch
from PIL import Image
from mmgp import offload
from hy3dgen.shapegen import FaceReducer, FloaterRemover, DegenerateFaceRemover, Hunyuan3DDiTFlowMatchingPipeline
from hy3dgen.shapegen.pipelines import export_to_trimesh
from hy3dgen.rembg import BackgroundRemover


def replace_property_getter(instance, name, getter):
    cls = type(instance)
    custom = type(f"Custom{cls.__name__}", (cls,), {name: property(getter, getattr(cls, name).fset)})
    instance.__class__ = custom


t0 = time.time()
torch.set_default_device("cpu")
tex = None
if not a.no_tex:
    from hy3dgen.texgen import Hunyuan3DPaintPipeline
    tex = Hunyuan3DPaintPipeline.from_pretrained("tencent/Hunyuan3D-2")
    tex.enable_model_cpu_offload()
shape = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(a.model, subfolder=a.subfolder, use_safetensors=True, device="cuda")
if "turbo" in a.subfolder:
    shape.enable_flashvdm(mc_algo="mc")
replace_property_getter(shape, "_execution_device", lambda self: "cuda")
pipe = offload.extract_models("i23d_worker", shape)
if tex is not None:
    pipe.update(offload.extract_models("texgen_worker", tex))
    tex.models["multiview_model"].pipeline.vae.use_slicing = True
kw = {}
if a.profile < 5:
    kw["pinnedMemory"] = "i23d_worker/model"
if a.profile not in (1, 3):
    kw["budgets"] = {"*": 2200}
offload.profile(pipe, profile_no=a.profile, verboseLevel=1, **kw)
print(f"hunyuan_generate: models ready in {time.time() - t0:.0f}s")

image = Image.open(img_path)
image = BackgroundRemover()(image.convert("RGB")) if image.mode != "RGBA" else image
# Hunyuan composites the input on WHITE: white objects (chef hat, fur trim) vanish. Grey the near-white parts
# for the shape pass only - the texture pass still gets the original colours.
import numpy as np
arr = np.asarray(image.convert("RGBA")).astype(np.float32)
rgb, al = arr[..., :3], arr[..., 3:]
mx, mn = rgb.max(-1, keepdims=True), rgb.min(-1, keepdims=True)
white = (mn > 215) & ((mx - mn) < 25) & (al > 10)
if white.mean() > 0.002:
    rgb = np.where(white, rgb * 0.8, rgb)
    print(f"hunyuan_generate: {white[..., 0].sum() / max(1, (al[..., 0] > 10).sum()):.0%} of the item is near-white: greyed for the shape pass")
shape_image = Image.fromarray(np.concatenate([rgb, al], -1).clip(0, 255).astype(np.uint8), "RGBA")
def gen(seed, guidance, steps):
    out = shape(image=shape_image, num_inference_steps=steps, guidance_scale=guidance,
                generator=torch.Generator().manual_seed(seed), octree_resolution=a.octree,
                num_chunks=200000, output_type="mesh")
    m = export_to_trimesh(out)[0]
    if m is None or len(m.faces) == 0:
        raise ValueError("empty mesh")
    return m
# some images give an empty volume with some seeds: fall back to the standard decoder, then to other seeds/settings
attempts = [(a.seed, a.guidance, a.steps), (7, 7.5, 50), (2024, 3.5, 30), (99, 5.0, 40)]
mesh, fast = None, "turbo" in a.subfolder
for n, (sd, gd, st) in enumerate(attempts):
    for _ in range(2):
        try:
            mesh = gen(sd, gd, st); break
        except (IndexError, RuntimeError, ValueError, AttributeError) as e:
            if fast:
                print(f"hunyuan_generate: fast decoder failed ({type(e).__name__}), switching to the standard volume decoder")
                shape.vae.enable_flashvdm_decoder(enabled=False); fast = False; continue
            print(f"hunyuan_generate: attempt {n + 1} (seed {sd}) gave no shape ({type(e).__name__})")
            break
    if mesh is not None: break
if mesh is None:
    raise SystemExit("hunyuan_generate: no shape after all attempts - try another image")
mesh = FloaterRemover()(mesh)
mesh = DegenerateFaceRemover()(mesh)
mesh = FaceReducer()(mesh, max_facenum=a.faces)
print(f"hunyuan_generate: shape done ({mesh.faces.shape[0]} faces) at {time.time() - t0:.0f}s")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
if tex is None:
    mesh.export(out_path)
else:
    textured = tex(mesh, image)
    textured.export(out_path, include_normals=True)
print(f"hunyuan_generate: wrote {out_path} in {time.time() - t0:.0f}s")
