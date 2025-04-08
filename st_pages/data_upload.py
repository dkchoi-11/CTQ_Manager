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

    # 기본 세션 상태 초기화
    if "input_file" not in st.session_state:
        st.session_state.input_file = None
    if "master_file" not in st.session_state:
        st.session_state.master_file = None
    if "start_date" not in st.session_state:
        st.session_state.start_date = None
    if "end_date" not in st.session_state:
        st.session_state.end_date = date.today()

        # 파일 업로드
        with file_col1:
            input_file = st.file_uploader(
                "📄 Upload Measurement Excel File", type=['xlsx', 'xls'],
                key="input_file"
            )

        with file_col2:
            master_file = st.file_uploader(
                "📄 Upload Master Excel File", type=["xlsx"],
                key="master_file"
            )

        # 날짜 선택
        with date_col1:
            start_date = st.date_input(
                "Start Date", value=st.session_state.start_date,
                key="start_date"
            )

        with date_col2:
            end_date = st.date_input(
                "End Date", value=st.session_state.end_date,
                key="end_date"
            )

    # 모든 입력이 있을 때 처리
    if st.session_state.input_file and st.session_state.master_file and \
       st.session_state.start_date and st.session_state.end_date:

        try:
            # 변환 함수 호출
            transformed_df = transform_data(
                input_file=st.session_state.input_file,
                master_file=st.session_state.master_file,
                start_date=st.session_state.start_date,
                end_date=st.session_state.end_date
            )

            st.success("✅ Success!")

            # 데이터 미리보기
            st.subheader("📊 Preview converted data")
            st.dataframe(transformed_df.head())

            # 정보 표시
            st.write(f"🔢 Total rows: {len(transformed_df)}")
            st.write(f"🔠 Total columns: {len(transformed_df.columns)}")

        except Exception as e:
            st.error(f"❌ Error during data conversion: {e}")