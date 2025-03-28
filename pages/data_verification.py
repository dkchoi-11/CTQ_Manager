import streamlit as st
import numpy as np

# 모듈 import
from modules.data_cleaner import detect_outliers
from modules.data_utils import get_spec_from_master

def data_verification_page():
    """이상 데이터 검증 페이지 (Anomaly Data Verification Page)"""
    st.header("이상 데이터 검증")

    # 변환된 데이터 확인
    if 'transformed_data' not in st.session_state:
        st.warning("먼저 데이터를 업로드하고 변환해주세요.")
        return

    df = st.session_state.transformed_data

    # 이상치 탐지 방법 선택
    method = st.selectbox("이상치 탐지 방법 선택",
                          ['IQR 방법', '규격 한계', 'Z-점수'])

    # 이상치 탐지 옵션
    if method == '규격 한계':
        col1, col2 = st.columns(2)
        with col1:
            usl = st.number_input("상한 규격 (USL)", value=np.inf)
        with col2:
            lsl = st.number_input("하한 규격 (LSL)", value=-np.inf)

        # 규격 한계 기반 이상치 탐지
        outliers_df = detect_outliers(df, method='spec_limit', usl=usl, lsl=lsl)
    elif method == 'IQR 방법':
        outliers_df = detect_outliers(df, method='iqr')
    else:  # Z-점수
        outliers_df = detect_outliers(df, method='z_score')

    # 이상치 결과 표시
    st.subheader("이상치 검출 결과")
    if outliers_df.empty:
        st.success("이상치가 검출되지 않았습니다.")
    else:
        st.dataframe(outliers_df)
        st.write(f"총 이상치 수: {len(outliers_df)}")