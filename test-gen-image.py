# pip install diffusers==0.34.0 torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128
# pip install transformers accelerate pillow matplotlib hf_xet sentencepiece

import matplotlib.pyplot as plt

from diffusers import StableDiffusionPipeline
import torch
model_id = "prompthero/openjourney" # OK
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

# Game Result Orb: A front-facing purple circle with a gold border, showcasing multi-colored spheres and a central gold star. Rendered with an embossed 3D effect, lustrous polish, and intense reflectivity. 4K resolution. Isolated on transparent.
# Kết quả trò chơi Orb: Một vòng tròn màu tím mặt trước với đường viền vàng, thể hiện các quả cầu nhiều màu và một ngôi sao vàng trung tâm. Được thể hiện bằng hiệu ứng 3D nổi, đánh bóng bóng và độ phản xạ dữ dội. Độ phân giải 4K. Bị cô lập trên minh bạch.

# Spin Dial: An impeccably polished, lustrous metallic gold cylinder featuring crisp, deep vertical grooves. Hyper-detailed front view 4K game asset, isolated on transparent background. Iconic spin-to-win symbol.
# Quay số quay: Một xi lanh vàng kim loại được đánh bóng hoàn hảo, bóng bẩy có các rãnh thẳng đứng sâu, sâu. Tài sản trò chơi 4K phía trước siêu chi tiết, bị cô lập trên nền trong suốt. Biểu tượng spin-to-win mang tính biểu tượng.
prompt = ["Game Result Orb: A front-facing purple circle with a gold border, showcasing multi-colored spheres and a central gold star. Rendered with an embossed 3D effect, lustrous polish, and intense reflectivity. 4K resolution. Isolated on transparent."] * 5
image = pipe(prompt).images[-1]

plt.figure(figsize=(10, 10))
plt.imshow(image)
plt.axis("off")
plt.show()