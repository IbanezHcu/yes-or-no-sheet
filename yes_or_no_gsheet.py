import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def connect_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"  # ✅ เพิ่มสิทธิ์เข้าถึง Google Drive
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gsheets"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1pffDWgP4_JR9WUNcyqPK5FVR27yy5NTZWQX_V6daxT8").sheet1
    return sheet

# เรียกใช้งาน
sheet = connect_sheet()
