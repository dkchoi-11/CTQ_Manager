import streamlit as st
import sys
import os

# 프로젝트 루트 디렉토리를 시스템 경로에 추가
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# 페이지 모듈 import
from st_pages import (
    data_upload_page,
    data_verification_page,
    quality_analysis_page,
    download_data_page,
    settings_page
)

def main():
    # 페이지 타이틀 및 아이콘 설정
    st.set_page_config(
        page_title="Quality Analysis Dashboard",
        page_icon=":bar_chart:",
        layout="wide"
    )

    # 사이드바 메뉴
    menu = st.sidebar.selectbox(
        "Select Menu",
        [
            "Upload and Convert DATA",
            "DATA Verification",
            "Quality Analysis",
            "Download conversion data",
            "Setting"
        ]
    )

    # 세션 상태 초기화 (최초 1회)
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.original_data = None
        st.session_state.transformed_data = None

    # 메뉴에 따른 페이지 라우팅
    if menu == "Upload and Convert DATA":
        data_upload_page()
    elif menu == "DATA Verification":
        data_verification_page()
    elif menu == "Quality Analysis":
        quality_analysis_page()
    elif menu == "Download conversion data":
        download_data_page()
    elif menu == "Setting":
        settings_page()

    # 사이트바에 세션 초기화 버튼 추가
    if st.sidebar.button("Initialize the session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # 푸터
    st.markdown("---")
    st.markdown("© CTQ Data 관리 대시보드 | Last Update: 2025/03/31")
    st.markdown("문의: [daekyu.choi@newoptics.net](mailto:daekyu.choi@newoptics.net)")



if __name__ == "__main__":
    main()