# 🖼️ Text-to-Image

A Streamlit app that converts **text prompts** into **AI-generated images** using:
- **Hugging Face Inference API** (recommended)
- **Local Diffusers backend** (for GPU machines)

## 🚀 Quick Start

1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run app
```bash
streamlit run app.py
```

Get a Hugging Face token from https://huggingface.co/settings/tokens and paste it in the sidebar.
