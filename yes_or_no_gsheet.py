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
    
    # ใช้ open_by_key เพื่อให้แม่นยำและเร็วกว่า
    sheet = client.open_by_key("1KWTWLUIM_tMumZxUgFMKUHpU7iU4YtN4ezcz4IXxNvw").sheet1
    return sheet

sheet = connect_sheet()
