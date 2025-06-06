import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# เชื่อมต่อ Google Sheet ด้วย credentials ที่เก็บไว้ใน Streamlit secrets
@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gsheets"],
        scopes=scope
    )
    client = gspread.authorize(creds)

    # เปลี่ยนชื่อ Sheet ด้านล่างให้ตรงกับชื่อใน Google Sheet ของคุณ
    sheet = client.open("ใช่หรือไม่").sheet1
    return sheet

# เรียกใช้งาน sheet
sheet = connect_sheet()

# ลองแสดงข้อมูลออกมาเพื่อทดสอบ
st.write(sheet.get_all_values())
