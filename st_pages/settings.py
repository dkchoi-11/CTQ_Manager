import streamlit as st

# 모듈 import
from modules.session_manager import reset_session_state

def settings_page():
    """설정 페이지 (Settings Page)"""
    st.header("Setting")

    # 세션 초기화 버튼
    if st.button("Initialize all session data", type="primary"):
        reset_session_state()
        st.success("Session data initialized.")