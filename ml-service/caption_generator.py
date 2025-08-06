# caption_generator.py

from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os

# Correct model name
# model_name = "Salesforce/blip2-opt-2.7b"

# Load model once
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path: str) -> str:
    """
    Generates a caption for the image at image_path using BLIP2.
    """
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt").to(device)
    output = model.generate(**inputs)
    return processor.decode(output[0], skip_special_tokens=True)


def caption_keyframes(keyframe_paths: list) -> dict:
    """
    Returns a dict of {filename: caption} for each keyframe.
    """
    captions = {}
    for path in keyframe_paths:
        try:
            print(f"🖼️ Captioning {path}...")
            caption = generate_caption(path)
            captions[os.path.basename(path)] = caption
        except Exception as e:
            print(f"❌ Failed to caption {path}: {e}")
    return captions