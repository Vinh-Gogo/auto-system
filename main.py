import os
import requests
import matplotlib.pyplot as plt
# You can access the image with PIL.Image for example
import io
from PIL import Image

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
HF_TOKEN = os.environ.get('HF_TOKEN') # Set HuggingFace environment

# check
if HF_TOKEN is None:
    raise ValueError("Please set the HF_TOKEN environment variable or assign your token to HF_TOKEN.")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

# Get API URL
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

def get_image(request):
    payload = { "inputs": request,}
    img_bytes = query(payload)
    image = Image.open(io.BytesIO(img_bytes))
    return image

image = get_image("Beautiful girl in Vietnamese, wearing white dress, standing on the beach, sunlight shining")
plt.imshow(image)
plt.axis("off")
plt.show()