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

# Text-to-Text Generation
import google.generativeai as genai

import glob
from dotenv import load_dotenv
import os

# Load từ .env
load_dotenv()

# Truy xuất biến
SHEET_ID = os.getenv("SHEET_ID")
FOLDER_DRIVE_ID = os.getenv("FOLDER_DRIVE_ID")
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
MODEL_ID = os.getenv("MODEL_ID")
FOLDER_GENERATOR_PATH = os.getenv("FOLDER_GENERATOR_PATH")

print("Sheet ID:", SHEET_ID)
print("Folder Drive ID:", FOLDER_DRIVE_ID)
print("Credentials path:", CREDENTIALS_PATH)
print("Model ID:", MODEL_ID)
print("Folder generated path:", FOLDER_GENERATOR_PATH)

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
data = pd.DataFrame(data[1:], columns=data[0])
# get rows have 'Status' is pending
data = data[data['Status'] == 'pending']
data['ID'] = data['ID'].astype(int)
# Visualize sheet data important
# print(data['Description'].values); print(data['Name'].values); print(data['Model'].values)
rows = data[['ID', 'Name', 'Description', 'Upgrade Description', 'Model', 'Type']].values

# ============== UPGRADE TEXT REQUIREMENTS (Text-to-Text) ==============
# Configure the API key directly
genai.configure(api_key="AIzaSyAERRGM2EsZvyhIXhD3umhyQbiLuhGCqVo")
model = genai.GenerativeModel("gemini-2.5-flash")

for row in rows:
  id, name, description, upgrade_description, model_name, type = row
  print(f'Task for id={id}: ({name}) {description}')
  
  # Generate content
  response = model.generate_content(
      contents=
      f'''
      Nhiệm vụ chính: tạo ra 1 *lời nhắc (prompt) tiếng Anh nâng cấp dưới 40 từ* mới.
      Yêu cầu: Ngắn gọn, mạnh mẽ cho AI, Tập trung Chi tiết, Độ bóng cho Game, Độ phân giải 4k, Tách nền.
      Đầu vào: {description}.
      Đầu ra: Title của content: Content.
      Ví dụ đầu ra: A meticulously crafted, hyper-detailed 2D game UI icon: a right-pointing triangular arrow. Rendered in lustrous metallic gold, featuring a pronounced 3D embossed effect with high polish and intense reflectivity. 4K resolution. Isolated on a transparent background.
      '''
  )
  
  index = id + 1
  sheet.update_acell(f"E{index}", f"{response.text}")  # Update Upgrade Description
  print(f'\n{response.text}\n')  # Print the generated text content

# ============== UPLOAD IAMGE TO GOOGLE DRIVE ==============

google_auth = GoogleAuth() # Yêu cầu xác thực Google 'client_secrets.json' đã được cấu hình
drive_app = GoogleDrive(google_auth)

# ============== IMAGE GENERATION & UPDATE SHEET ==============

# Generate images using the model
pipe = DiffusionPipeline.from_pretrained(MODEL_ID)
pipe.safety_checker = None # Tắt safety checker để tránh lỗi
pipe.enable_attention_slicing() # Tăng tốc độ sinh ảnh

def get_current_time():
  from datetime import datetime
  return f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

for row in rows:
  id, name, description, upgrade_description, model_name, type = row
  print(f'Task for id={id}: ({name}) {upgrade_description}')
  
  try:
    prompt = upgrade_description
    image = pipe(prompt).images[0]
    
    # save image
    path_image = f"{FOLDER_GENERATOR_PATH}/{name}.{type.lower()}"
    image.save(path_image)
    index = id + 1
  except Exception as e:
    print(f"Error generating image for {name}: {e}")
    index = id + 1
    # update sheet with ERROR status
    try:
      sheet.update_acell(f"B{index}", f"{get_current_time()}")
      sheet.update_acell(f"I{index}", f"ERROR")
      sheet.update_acell(f"H{index}", f"{MODEL_ID}")
    except Exception as e:
      print(f"don't update values sheet at row {index} ! an unexpected error occurred: {e}")
    continue

  # update sheet
  try:
    # Update SUCCESS
    sheet.update_acell(f"B{index}", f"{get_current_time()}")
    sheet.update_acell(f"I{index}", f"SUCCESS")
    sheet.update_acell(f"H{index}", f"{MODEL_ID}")
  
  except Exception as e:
    print(f"don't update values sheet at row {index} ! an unexpected error occurred: {e}")
  finally:
    index += 1
    print(f"Created image: {name}.{type.lower()} at index {index}")

  file = drive_app.CreateFile({'title': f'{get_current_time()}_{name}', 'parents': [{'id': FOLDER_DRIVE_ID}]})
  file.SetContentFile(path_image)
  file.Upload()
  print(f"Uploaded {name} with ID: {file['id']}")

  path_drive = f"https://drive.google.com/file/d/{file['id']}/view"
  sheet.update_acell(f"G{index-1}", f"{path_drive}")

# ====================== TEMPORARY CODE TO UPLOAD IMAGES ======================
# image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif']
# # Tạo danh sách file ảnh
# ls_files = []
# for ext in image_extensions:
#     ls_files.extend(glob.glob(os.path.join(str(FOLDER_GENERATOR_PATH), ext)))

# # Thực hiện upload các tệp lên Google Drive
# for file_name in ls_files:
#   file = drive_app.CreateFile({'title': f'{}_{file_name}', 'parents': [{'id': FOLDER_DRIVE_ID}]})
#   file.SetContentFile(file_name)
#   file.Upload()
#   print(f"Uploaded {file_name} with ID: {file['id']}")