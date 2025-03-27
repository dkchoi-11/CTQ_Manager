import streamlit as st
import sys
import os

# 프로젝트 루트 디렉토리를 시스템 경로에 추가
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# 페이지 모듈 import
from pages import (
    data_upload_page,
    data_verification_page,
    quality_analysis_page,
    download_data_page,
    settings_page
)

def main():
    # 페이지 타이틀 및 아이콘 설정
    st.set_page_config(
        page_title="품질 분석 대시보드",
        page_icon=":bar_chart:",
        layout="wide"
    )

    # 사이드바 메뉴
    menu = st.sidebar.selectbox(
        "메뉴 선택",
        [
            "데이터 업로드&변환",
            "데이터 검증",
            "품질 분석",
            "데이터 다운로드",
            "설정"
        ]
    )

    # 세션 상태 초기화 (최초 1회)
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.original_data = None
        st.session_state.transformed_data = None

    # 메뉴에 따른 페이지 라우팅
    if menu == "데이터 업로드&변환":
        data_upload_page()
    elif menu == "데이터 검증":
        data_verification_page()
    elif menu == "품질 분석":
        quality_analysis_page()
    elif menu == "데이터 다운로드":
        download_data_page()
    elif menu == "설정":
        settings_page()

    # 사이트바에 세션 초기화 버튼 추가
    if st.sidebar.button("세션 초기화"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

if __name__ == "__main__":
    main()