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
    return img_bytes, image

from datetime import datetime
import pandas as pd

import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

scrope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scrope)
client = gspread.authorize(creds)

sheet_id = "1DvHyHppSVrMOi-ARTo-qari95F7AS7khPhH4D4hCmsA"
workbook = client.open_by_key(sheet_id)

sheets = map(lambda x: x.title, workbook.worksheets())
print(f"Number of sheets: {list(sheets)}")

sheet = workbook.worksheet("Sheet1")
data = sheet.get_all_values()

# today = datetime.today()
# formatted = today.strftime("%d/%m/%Y")  # dạng: DD/MM/YYYY
# print("Hôm nay là:", formatted)

def get_pending_rows(data) -> pd.DataFrame:
    df = pd.DataFrame(data[1:], columns=data[0])
    pending_rows = df[df['Status'] == 'pending']
    return pending_rows

pending_df = get_pending_rows(data)
print(f"Descriptions: {pending_df.shape[0]}\n", pending_df[['Description', 'Status']])  # Assuming the first row is the header

def get_imges_from_descriptions(descriptions):
    images = []
    for desc in descriptions:
        img_bytes, image = get_image(desc)
        images.append((img_bytes, image))
    return images

# img_bytes, image = get_image("Beautiful girl 35 year old in Vietnamese, wearing white dress, standing on the beach, sunlight shining")
# print(f"Image bytes length: {len(img_bytes)}, type: {type(img_bytes)}, value: {img_bytes}...")
# plt.imshow(image)
# plt.axis("off")
# plt.show()

