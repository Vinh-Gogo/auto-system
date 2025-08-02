# pip install diffusers==0.34.0 torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128
# pip install transformers accelerate pillow matplotlib hf_xet sentencepiece

from diffusers import DiffusionPipeline
import matplotlib.pyplot as plt

pipe = DiffusionPipeline.from_pretrained("UnfilteredAI/NSFW-gen-v2") # OKE L4

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]

image.save("astronaut_rides_horse.jpg")

plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis("off")
plt.show()