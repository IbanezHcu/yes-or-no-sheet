import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gsheets"],  # ✅ ใช้ dict ตรง
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open("yes-or-no-data").sheet1
    return sheet

# เรียกใช้
sheet = connect_sheet()
data = sheet.get_all_values()
st.write("✅ เชื่อมต่อสำเร็จแล้ว")
st.write(data)
