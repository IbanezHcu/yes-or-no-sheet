import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# === CONNECT TO GOOGLE SHEET ===
SHEET_NAME = "yes-or-no-data"
CREDENTIALS_PATH = "utility-chimera-462014-j5-697d9dc3758e.json"  # ชื่อไฟล์ .json service account ที่ push ขึ้น Git แล้ว

@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)
    try:
        spreadsheet = client.open(SHEET_NAME)
        st.success("✅ เชื่อมต่อ Google Sheet สำเร็จ")
        return spreadsheet.sheet1
    except Exception as e:
        st.error(f"❌ ไม่สามารถเปิดชีทชื่อ '{SHEET_NAME}' ได้")
        st.exception(e)
        return None

sheet = connect_sheet()

def read_state():
    if not sheet:
        return []
    records = sheet.get_all_records()
    st.write("📄 ข้อมูลทั้งหมดในชีท:", records)
    return [{ 'key': row['key'], 'value': json.loads(row['value']) } for row in records]

# แสดงผลในหน้าแอป
st.title("🎮 เกม ใช่หรือไม่ - ทดสอบ Google Sheet")
read_state()
