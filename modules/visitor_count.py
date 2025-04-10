import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Google Sheets 연동을 위한 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Streamlit secrets.toml에서 credentials 가져오기
credentials_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

# 구글 시트 접근
client = gspread.authorize(credentials)
sheet = client.open("VisitorCounter").count

def get_visitor_count():
    try:
        value = sheet.acell("A1").value
        return int(value)
    except Exception:
        return 0

def increment_visitor_count():
    count = get_visitor_count() + 1
    sheet.update_acell("A1", str(count))
    return count
