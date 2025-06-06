import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

@st.cache_resource
def connect_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds_info = json.loads(st.secrets["gsheets"]["GCP_SERVICE_ACCOUNT"])
    creds = Credentials.from_service_account_info(creds_info, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("yes-or-no-data").sheet1
    return sheet

sheet = connect_sheet()
st.write(sheet.get_all_values())
