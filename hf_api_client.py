import requests
from PIL import Image
from io import BytesIO


HF_TTI_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_TTI_MODEL}"

def generate_image_hf(prompt, hf_token, width=512, height=512, steps=25, guidance_scale=7.5):
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Accept": "image/png"
    }

    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True},
        "params": {
            "width": width,
            "height": height,
            "num_inference_steps": steps,
            "guidance_scale": guidance_scale,
        }
    }

    response = requests.post(HF_API_URL, headers=headers, json=payload, stream=True)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content)).convert("RGB")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    else:
        try:
            error = response.json()
        except Exception:
            error = response.text
        raise RuntimeError(f"Hugging Face API error ({response.status_code}): {error}")
