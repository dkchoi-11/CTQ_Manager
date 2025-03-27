import streamlit as st
import pandas as pd
from holoviews.plotting.util import within_range

# 모듈 import
from modules.data_cleaner import clean_data, get_data_quality_report, detect_outliers
from modules.data_transformer import transform_data
from modules.file_handler import upload_excel_file


def data_upload_page():
    """데이터 업로드 및 변환 페이지 (Data Upload and Transformation Page)"""
    st.header("데이터 업로드 및 변환")

    # 파일 업로드
    input_file = st.file_uploader("📄 측정값 Excel 파일 업로드", type=['xlsx', 'xls'])
    master_file = st.file_uploader("📄 마스터 키 Excel 파일 업로드", type=["xlsx"])
    start_date = st.date_input("시작 날짜", value=None)
    end_date = st.date_input("종료 날짜", value=None)

    if input_file and master_file and start_date and end_date:
        try:
            transformed_df = transform_data(
                input_file=input_file,
                master_file=master_file,
                start_date=start_date,
                end_date=end_date
            )

            st.success("✅ 변환 완료!")

            # 변환된 데이터 미리보기
            st.subheader("변환된 데이터 미리보기")
            st.dataframe(transformed_df.head())

            # 추가 정보 표시
            st.write(f"총 행 수: {len(transformed_df)}")
            st.write(f"총 열 수: {len(transformed_df.columns)}")

        except Exception as e:
            st.error(f"데이터 변환 중 오류 발생: {e}")