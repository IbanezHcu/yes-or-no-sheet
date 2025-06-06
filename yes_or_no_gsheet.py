import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def connect_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(
        st.secrets["gsheets"],
        scopes=scope
    )
    client = gspread.authorize(creds)

    # ✅ เปิดด้วย spreadsheetId โดยตรง ไม่ใช้ชื่อ
    sheet = client.open_by_key("1pffDWgP4_JR9WUNcyqPK5FVR27yy5NTZWQX_V6daxT8").sheet1
    return sheet

# ทดลองเรียกใช้งาน
sheet = connect_sheet()
