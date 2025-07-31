import os
import requests
import matplotlib.pyplot as plt

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
# Set your HuggingFace token here if not set in environment
HF_TOKEN = os.environ.get('HF_TOKEN')
if HF_TOKEN is None:
    raise ValueError("Please set the HF_TOKEN environment variable or assign your token to HF_TOKEN.")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

image_bytes = query({
    "inputs": "Beautiful girl in Vietnamese, wearing white dress, standing on the beach, sunlight shining",
})

# You can access the image with PIL.Image for example
import io
from PIL import Image
image = Image.open(io.BytesIO(image_bytes))

plt.imshow(image)
plt.axis("off")
plt.show()