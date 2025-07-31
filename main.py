# import os
# import requests
# import matplotlib.pyplot as plt
# # You can access the image with PIL.Image for example
# import io
# from PIL import Image

# API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
# HF_TOKEN = os.environ.get('HF_TOKEN') # Set HuggingFace environment

# # check
# if HF_TOKEN is None:
#     raise ValueError("Please set the HF_TOKEN environment variable or assign your token to HF_TOKEN.")

# headers = {
#     "Authorization": f"Bearer {HF_TOKEN}",
# }

# # Get API URL
# def query(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.content

# def get_image(request):
#     payload = { "inputs": request,}
#     img_bytes = query(payload)
#     image = Image.open(io.BytesIO(img_bytes))
#     return img_bytes, image

# bytes, image = get_image("A photo of a cat")
# plt.imshow(image)
# plt.axis("off")
# plt.show()

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

# URL of the image you want to insert
# SỬ DỤNG URL HÌNH ẢNH THÔ TỪ GITHUB
image_url = "https://raw.githubusercontent.com/Vinh-Gogo/auto-system/main/Header-Gift-BarYellow.png"

# target cell
cell_address = "B2"

# build the IMAGE formula (optional arguments control sizing)
formula = f'=IMAGE("{image_url}", 4, 100, 100)'

try:
    sheet.update(cell_address, formula)
    print(f"Đã cập nhật ô {cell_address} thành công với công thức: {formula}")
except gspread.exceptions.APIError as e:
    print(f"Lỗi API khi cập nhật ô {cell_address}: {e}")
except Exception as e:
    print(f"Một lỗi không mong muốn đã xảy ra: {e}")


# today = datetime.today()
# formatted = today.strftime("%d/%m/%Y")  # dạng: DD/MM/YYYY
# print("Hôm nay là:", formatted)

# def get_pending_rows(data) -> pd.DataFrame:
#     df = pd.DataFrame(data[1:], columns=data[0])
#     pending_rows = df[df['Status'] == 'pending']
#     return pending_rows

# pending_df = get_pending_rows(data).head(3)
# # print(f"Descriptions: {pending_df.shape[0]}\n", pending_df[['ID', 'Description', 'Status']])  # Assuming the first row is the header
# # print(f"Descriptions values:\n", pending_df['Description'].values)

# for x,y in zip(pending_df['ID'].astype(int), pending_df['Description']):
#     print(type(x), type(y))
#     print(f"ID: {x}, Description: {y}")
#     print()
#     byte, image = get_image(y)
#     pending_df.at[x, 'bytes'] = byte

#     sheet.update_cell(x + 2, 6, str(byte))  # Assuming the 'bytes' column is the 4th column in the sheet
#     plt.imshow(image)
#     plt.axis("off")
#     plt.show()

# # for idx, row in pending_df.iterrows():
# #     print(f"Processing row {idx}: ID={row['ID']}, Description={row['Description']}, Status={row['Status']}")
# #     print()
# #     print(row['Description'])
# #     print()
# #     # # Get images from descriptions
# #     img_bytes, image = get_image(row['Description'])
# #     # plt.imshow(image)
# #     # plt.axis("off")
# #     # plt.show()

# #     # Save bytes images to pending_df
# #     pending_df.at[idx, 'bytes'] = str(img_bytes)

# # # Save the updated DataFrame back to the Google Sheet
# # for idx, row in pending_df.iterrows():
# #     sheet.update_cell(idx + 2, 6, row['bytes'])  # Assuming the 'bytes' column is the 4th column in the sheet

    

