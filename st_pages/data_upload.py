import streamlit as st
import pandas as pd
from datetime import date


# 모듈 import
from modules.data_transformer import transform_data


def data_upload_page():
    """데이터 업로드 및 변환 페이지 (Data Upload and Transformation Page)"""
    st.header("Upload and Convert DATA")

    file_col1, file_col2 =st.columns(2)
    date_col1, date_col2 =st.columns(2)

    # 세션 상태에서 이전 값 불러오기
    input_file = st.session_state.get("input_file", None)
    master_file = st.session_state.get("master_file", None)
    start_date = st.session_state.get("start_date", None)
    end_date = st.session_state.get("end_date", date.today())

    # 파일 업로드
    with file_col1:
        uploaded_input_file = st.file_uploader(
            "📄 Upload Measurement Excel File", type=['xlsx', 'xls'],
            key="input_file", label_visibility="visible"
        )
        if uploaded_input_file:
            st.session_state.input_file = uploaded_input_file

    with file_col2:
        uploaded_master_file = st.file_uploader(
            "📄 Upload Master Excel File", type=["xlsx"],
            key="master_file", label_visibility="visible"
        )
        if uploaded_master_file:
            st.session_state.master_file = uploaded_master_file
            master_file = uploaded_master_file

    with date_col1:
        selected_start_date = st.date_input(
            "Start Date", value=start_date, key="start_date"
        )
        if selected_start_date:
            st.session_state.start_date = selected_start_date
            start_date = selected_start_date

    with date_col2:
        selected_end_date = st.date_input(
            "End Date", value=end_date, key="end_date"
        )
        if selected_end_date:
            st.session_state.end_date = selected_end_date
            end_date = selected_end_date

    if input_file and master_file and start_date and end_date:
        try:
            transformed_df = transform_data(
                input_file=input_file,
                master_file=master_file,
                start_date=start_date,
                end_date=end_date
            )

            st.success("✅ Success!")

            # 변환된 데이터 미리보기
            st.subheader("Preview converted data")
            st.dataframe(transformed_df.head())

            # 추가 정보 표시
            st.write(f"Total number of rows: {len(transformed_df)}")
            st.write(f"Total number of columns: {len(transformed_df.columns)}")

        except Exception as e:
            st.error(f"Error during data conversion: {e}")