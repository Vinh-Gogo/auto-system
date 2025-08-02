import numpy as np

# Google Drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Google Sheets
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

# Image Generation
from diffusers import DiffusionPipeline

import glob
from dotenv import load_dotenv
import os

# Load từ .env
load_dotenv()

# Truy xuất biến
SHEET_ID = os.getenv("SHEET_ID")
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
MODEL_ID = os.getenv("MODEL_ID")
FOLDER_PATH = os.getenv("FOLDER_PATH")

print("Sheet ID:", SHEET_ID)
print("Credentials path:", CREDENTIALS_PATH)
print("Model ID:", MODEL_ID)
print("Folder generated path:", FOLDER_PATH)

# ============== GET REQUIREMENTS (Google Sheet) ==============
scrope = ["https://www.googleapis.com/auth/spreadsheets"]
# json config from Google Cloud
creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scrope) 
client = gspread.authorize(creds)
workbook = client.open_by_key(str(SHEET_ID))

# Get all sheet names
sheets = map(lambda x: x.title, workbook.worksheets())
print(f"Number of sheets: {list(sheets)}")

# Choose sheet and get data
sheet = workbook.worksheet("Sheet1")
data = sheet.get_all_values()
data = pd.DataFrame(data[1:3], columns=data[0])

# Visualize sheet data important
# print(data['Description'].values); print(data['Name'].values); print(data['Model'].values)

# ============== UPGRADE TEXT REQUIREMENTS (Text-to-Text) ==============
# '''
# 
#  Chưa thực hiện 
# 
# 
# '''
#

# ============== IMAGE GENERATION & UPDATE SHEET ==============
# Generate images using the model
pipe = DiffusionPipeline.from_pretrained(MODEL_ID) # OKE L4

rows = data[['Name', 'Description', 'Model']].values

index = 2
for name, description in zip(data['Name'].values, data['Description'].values):
  print(f'Task for: {np.array([name, description])}')
  prompt = description + ", detailed, 4k"
  image = pipe(prompt).images[0]
  
  # save image
  image.save(f"{FOLDER_PATH}/{name}.jpg")
  
  # update sheet
  try:
    sheet.update_acell(f"H{index}", f"SUCCESS")
    sheet.update_acell(f"G{index}", f"{MODEL_ID}")
  except Exception as e:
    print(f"don't update values sheet at row {index} ! an unexpected error occurred: {e}")
  finally:
    index += 1
    print(f"Created image: {name}.jpg")

# ============== UPLOAD IAMGE TO GOOGLE DRIVE ==============

# google_auth = GoogleAuth() # Yêu cầu xác thực Google 'client_secrets.json' đã được cấu hình
# drive_app = GoogleDrive(google_auth)

# Các định dạng ảnh bạn muốn lọc
image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']
# Tạo danh sách file ảnh
ls_files = []
for ext in image_extensions:
    ls_files.extend(glob.glob(os.path.join(str(FOLDER_PATH), ext)))

# ls_files = ['young_man.png', 'aa.png'] # Danh sách giả lập

# # Thực hiện upload các tệp lên Google Drive
# for file_name in ls_files:
#   file = drive_app.CreateFile({'title': file_name, 'parents': [{'id': '1eik5Qr7e1S0CYwCpDFFHoV9VoCXH0Vk3'}]})
#   file.SetContentFile(file_name)
#   file.Upload()
#   print(f"Uploaded {file_name} with ID: {file['id']}")