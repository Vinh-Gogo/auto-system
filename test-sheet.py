import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd

scrope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scrope)
client = gspread.authorize(creds)

sheet_id = "1stgBPwj0oNmUseNZES0_-4Ua5r4HScLFA6DdmVVqLog"
workbook = client.open_by_key(sheet_id)

sheets = map(lambda x: x.title, workbook.worksheets())
print(f"Number of sheets: {list(sheets)}")

sheet = workbook.worksheet("Sheet1")
data = sheet.get_all_values()
data = pd.DataFrame(data[1:], columns=data[0])  # Convert to DataFrame for easier manipulation

print(data['Description'].values)