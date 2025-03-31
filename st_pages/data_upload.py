import streamlit as st
import pandas as pd


# 모듈 import
from modules.data_transformer import transform_data
from modules.file_handler import upload_excel_file


def data_upload_page():
    """데이터 업로드 및 변환 페이지 (Data Upload and Transformation Page)"""
    st.header("Upload and Convert DATA")

    # 파일 업로드
    input_file = st.file_uploader("📄 Upload Measurement Excel File", type=['xlsx', 'xls'])
    master_file = st.file_uploader("📄 Upload Master Excel File", type=["xlsx"])
    start_date = st.date_input("Start Date", value=None)
    end_date = st.date_input("End Date", value=None)

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