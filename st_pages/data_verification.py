import pandas as pd
import streamlit as st
import io
import numpy as np

from modules import transform_data
# 모듈 import
from modules.data_utils import get_spec_from_master, verify_data, get_spec_for_measured_ctq

def data_verification_page():
    """이상 데이터 검증 페이지 (Anomaly Data Verification Page)"""
    st.header("이상 데이터 검증")

    # 변환된 데이터 확인
    if st.session_state.transformed_data is None or st.session_state.transformed_data.empty:
        st.warning("먼저 데이터를 업로드하고 변환해주세요.")
        return


    df = st.session_state.transformed_data

    # 이상치 탐지 방법 선택
    method = st.selectbox("이상치 탐지 방법 선택",
                          ['규격 한계', 'IQR 방법', 'Z-점수'])

    st.subheader("📋 관리번호별 스펙 정보 (USL, LSL, Target, UCL, LCL)")
    spec_df = get_spec_for_measured_ctq()
    if not spec_df.empty:
        st.dataframe(spec_df)
    else:
        st.info("스펙 정보를 찾을 수 없습니다.")

    # 이상치 탐지 옵션
    if method == '규격 한계':
        verify_result_df = verify_data()

        st.subheader("📊 스펙 초과 검출 결과")
        st.write(f"총 데이터 수: {len(df)}")

        if verify_result_df is None:
            st.warning("스펙 검증 결과를 가져올 수 없습니다.")
            return

        st.write(f"스펙 초과된 데이터 수: {len(verify_result_df)}")

        if verify_result_df.empty:
            st.success("✅ 스펙 초과된 데이터 없음")
        else:
            st.error("❗스펙 초과된 데이터가 존재합니다.")
            st.dataframe(verify_result_df)

            # 엑셀로 다운로드 버튼 추가
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                verify_result_df.to_excel(writer, index=False, sheet_name='Spec Over Data')

            st.download_button(
                label="📥 스펙 초과 데이터 Excel 다운로드",
                data=output.getvalue(),
                file_name="spec_over_data.xlsx",
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )