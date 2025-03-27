import streamlit as st

# 모듈 import
from modules.data_cleaner import get_data_quality_report

def quality_analysis_page():
    """품질 분석 페이지 (Quality Analysis Page)"""
    st.header("품질 분석")

    # 변환된 데이터 확인
    if 'transformed_data' not in st.session_state:
        st.warning("먼저 데이터를 업로드하고 변환해주세요.")
        return

    df = st.session_state.transformed_data

    # 탭 설정
    tab1, tab2, tab3, tab4 = st.tabs([
        "기본 통계",
        "관리도",
        "공정능력 분석",
        "박스플롯 및 추세 분석"
    ])

    with tab1:
        # 기본 통계 분석
        st.subheader("기본 통계 분석")
        quality_report = get_data_quality_report(df)
        st.json(quality_report)

    with tab2:
        # 관리도 분석 (자리 표시)
        st.subheader("관리도 분석")
        st.write("TODO: 관리도 생성")

    with tab3:
        # 공정능력 분석 (자리 표시)
        st.subheader("공정능력 분석")
        st.write("TODO: 공정능력 분석")

    with tab4:
        # 박스플롯 및 추세 분석 (자리 표시)
        st.subheader("박스플롯 및 추세 분석")
        st.write("TODO: 박스플롯 및 추세 분석")