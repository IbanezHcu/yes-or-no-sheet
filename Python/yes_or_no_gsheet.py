import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

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
    sheet = client.open("yes-or-no-data").sheet1
    return sheet

sheet = connect_sheet()

# ตัวอย่าง: แสดงข้อมูลทั้งหมด
st.write(sheet.get_all_values())
