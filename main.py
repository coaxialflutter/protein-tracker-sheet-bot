from datetime import datetime
import os
import gspread
from google.oauth2.service_account import Credentials

# Auth
SERVICE_ACCOUNT_FILE = os.path.expanduser("shining-hydra-345423-cbddcee729e5.json")
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Open sheet
SPREADSHEET_NAME = "Protein"
spreadsheet = client.open(SPREADSHEET_NAME)
sheet = spreadsheet.sheet1

# Insert 12 rows at the top
sheet.insert_rows([['']] * 12, 1)

# A1: Current date
today = datetime.now().strftime("%m/%d/%y")
sheet.update_cell(1, 1, today)

# A11: Total label
sheet.update_cell(11, 1, "Total")

# B11: SUM formula
sheet.update_cell(11, 2, "=SUM(B2:B10)")

# ✨ Add thick bottom border to A11 and B11
sheet_id = sheet._properties['sheetId']
spreadsheet.batch_update({
    "requests": [
        {
            "updateBorders": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 10,  # 0-based, so row 11
                    "endRowIndex": 11,
                    "startColumnIndex": 0,
                    "endColumnIndex": 2  # A and B
                },
                "bottom": {
                    "style": "SOLID_THICK",
                    "width": 2,
                    "color": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                    }
                }
            }
        }
    ]
})

print("✅ Done: Date, total, clean spacing, and a sexy bottom border.")
