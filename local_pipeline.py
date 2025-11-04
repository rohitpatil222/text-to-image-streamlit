import torch
from diffusers import StableDiffusionPipeline
from io import BytesIO
from PIL import Image

MODEL_ID = "runwayml/stable-diffusion-v1-5"
_pipeline = None

def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        _pipeline = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
        _pipeline = _pipeline.to("cuda")
    return _pipeline

def generate_image_local(prompt, width=512, height=512, steps=25, guidance_scale=7.5):
    pipe = _get_pipeline()
    result = pipe(prompt, num_inference_steps=int(steps), guidance_scale=float(guidance_scale))
    image = result.images[0]
    buf = BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()
