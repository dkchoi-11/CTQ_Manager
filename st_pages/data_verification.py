import pandas as pd
import streamlit as st
import io
import numpy as np

from modules import transform_data
# 모듈 import
from modules.data_utils import get_spec_from_master, verify_data, get_spec_for_measured_ctq

def data_verification_page():
    """이상 데이터 검증 페이지 (Anomaly Data Verification Page)"""
    st.header("Validation of anomaly data")

    # 변환된 데이터 확인
    if st.session_state.transformed_data is None or st.session_state.transformed_data.empty:
        st.warning("Please upload and convert the data first.")
        return


    df = st.session_state.transformed_data

    st.subheader("📋 Specification information by management number (USL, LSL, Target, UCL, LCL)")
    spec_df = get_spec_for_measured_ctq()
    if not spec_df.empty:
        st.dataframe(spec_df)
    else:
        st.info("Specification information not found.")

    # 이상치 탐지 옵션
    verify_result_df, add_spec_over_df = verify_data()

    st.subheader("📊 Over Specification Detection Results")
    st.write(f"Total number of data: {len(df)}")

    if verify_result_df is None:
        st.warning("Unable to get spec verification results.")
        return

    st.write(f"Number of data exceeded specification: {len(verify_result_df)}")

    if verify_result_df.empty:
        st.success("✅ No over-spec data")
    else:
        st.error("❗Exceeded Specification Data Exists.")
        st.dataframe(verify_result_df)

        # 엑셀로 다운로드 버튼 추가
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            add_spec_over_df.to_excel(writer, index=False, sheet_name='Spec Over Data')

        st.download_button(
            label="📥 Download over-spec data Excel",
            data=output.getvalue(),
            file_name="spec_over_data.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )