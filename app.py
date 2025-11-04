import sys
if sys.platform.startswith("win"):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import streamlit as st

from hf_api_client import generate_image_hf
from local_pipeline import generate_image_local
from io import BytesIO
import base64

st.set_page_config(page_title="Text → Image Generator", layout="centered")

st.title("🎨 Text → Image Generator")

backend = st.radio(
    "Choose backend:",
    ("HuggingFace Inference API (Recommended)", "Local Diffusers (GPU Only)")
)

prompt = st.text_area(
    "Enter your prompt:",
    "A cinematic portrait of a fox wearing a leather jacket, dramatic lighting",
    height=120
)

with st.sidebar:
    st.header("⚙️ Options")
    steps = st.slider("Inference steps", 1, 50, 25)
    guidance_scale = st.slider("Guidance scale", 1.0, 20.0, 7.5)
    width = st.selectbox("Width", [256, 512, 768], index=1)
    height = st.selectbox("Height", [256, 512, 768], index=1)
    hf_token = st.text_input("Hugging Face API Token (for HF backend)", type="password")

if st.button("🚀 Generate"):
    if not prompt.strip():
        st.error("Please enter a text prompt.")
    else:
        with st.spinner("Generating image... please wait"):
            try:
                if backend.startswith("HuggingFace"):
                    if not hf_token:
                        st.error("⚠️ Hugging Face API token is required. Get one from https://huggingface.co/settings/tokens")
                    else:
                        img_bytes = generate_image_hf(
                            prompt, hf_token,
                            width=width, height=height,
                            steps=steps, guidance_scale=guidance_scale
                        )
                else:
                    img_bytes = generate_image_local(
                        prompt, width=width, height=height,
                        steps=steps, guidance_scale=guidance_scale
                    )

                if img_bytes is None:
                    st.error("❌ Image generation failed. Check logs.")
                else:
                    st.image(img_bytes, use_column_width=True)
                    b64 = base64.b64encode(img_bytes).decode()
                    href = f"data:image/png;base64,{b64}"
                    st.markdown(f"[💾 Download image]({href})", unsafe_allow_html=True)
            except Exception as e:
                st.exception(e)
