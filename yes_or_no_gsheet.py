import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

@st.cache_resource
def connect_sheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gsheets"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    # เปิดโดยใช้ Spreadsheet ID
    sheet = client.open_by_key("1PdfJSe1YZRYfIseGgKngjqzv_CrwpTddLcLoaKOLw3A").sheet1
    return sheet

# ใช้งาน sheet
sheet = connect_sheet()
st.write(sheet.get_all_values())
