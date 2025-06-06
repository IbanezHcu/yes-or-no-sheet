import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# === CONNECT TO GOOGLE SHEET ===
SHEET_NAME = "yes-or-no-data"  # ตั้งชื่อให้ตรงกับ Google Sheet ที่สร้าง

@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_dict = st.secrets["gsheets"]  # ดึง credentials จาก secrets
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    return client.open(SHEET_NAME).sheet1

sheet = connect_sheet()

def read_state():
    records = sheet.get_all_records()
    return {row["key"]: json.loads(row["value"]) for row in records}

def write_state(state):
    for key, val in state.items():
        cell = sheet.find(key)
        if cell:
            sheet.update_cell(cell.row, 2, json.dumps(val))
        else:
            sheet.append_row([key, json.dumps(val)])
