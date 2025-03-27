import streamlit as st

# 모듈 import
from modules.session_manager import reset_session_state

def settings_page():
    """설정 페이지 (Settings Page)"""
    st.header("설정")

    # 세션 초기화 버튼
    if st.button("모든 세션 데이터 초기화", type="primary"):
        reset_session_state()
        st.success("세션 데이터가 초기화되었습니다.")