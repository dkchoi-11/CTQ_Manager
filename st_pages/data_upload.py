import streamlit as st
import pandas as pd
from datetime import date


# 모듈 import
from modules.data_transformer import transform_data
from modules.file_handler import upload_excel_file


def data_upload_page():
    """데이터 업로드 및 변환 페이지 (Data Upload and Transformation Page)"""
    st.header("Upload and Convert DATA")

    file_col1, file_col2 =st.columns(2)
    date_col1, date_col2 =st.columns(2)

    # 파일 업로드
    with file_col1:
        input_file = st.file_uploader("📄 Upload Measurement Excel File", type=['xlsx', 'xls'], key="input_file")
    with file_col2:
        master_file = st.file_uploader("📄 Upload Master Excel File", type=["xlsx"], key="master_file")
    with date_col1:
        start_date = st.date_input("Start Date", value=None, key="start_date")
    with date_col2:
        end_date = st.date_input("End Date", value=date.today(), key="end_date")

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