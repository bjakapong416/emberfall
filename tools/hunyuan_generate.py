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
out = shape(image=image, num_inference_steps=a.steps, guidance_scale=a.guidance,
            generator=torch.Generator().manual_seed(a.seed), octree_resolution=a.octree,
            num_chunks=200000, output_type="mesh")
mesh = export_to_trimesh(out)[0]
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
