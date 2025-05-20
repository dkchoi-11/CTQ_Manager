import streamlit as st
import pandas as pd
from datetime import date, timedelta

# 모듈 import
from modules.data_transformer import transform_data


def data_upload_page():
    """데이터 업로드 및 변환 페이지 (Data Upload and Transformation Page)"""
    st.header("Upload and Convert DATA")

    """ 기본 세션 상태 초기화
    if "start_date" not in st.session_state:
        st.session_state.start_date = date.today() - timedelta(days=7)
    if "end_date" not in st.session_state:
        st.session_state.end_date = date.today()
    """
    default_start = date.today() - timedelta(days=7)
    default_end = date.today()

    file_col1, file_col2 =st.columns(2)
    date_col1, date_col2 =st.columns(2)

    # 🔹 위젯으로부터 직접 읽어오기 (key 사용, 수동 할당 금지)
    with file_col1:
        st.file_uploader("📄 Upload Measurement Excel File", type=["xlsx", "xls"], key="input_file")

    with file_col2:
        st.file_uploader("📄 Upload Master Excel File", type=["xlsx"], key="master_file")
    """
    with date_col1:
        st.date_input("Start Date", value=st.session_state.start_date, key="start_date")

    with date_col2:
        st.date_input("End Date", value=st.session_state.end_date, key="end_date")
    """
    with date_col1:
        st.date_input("Start Date", value=st.session_state.get("start_date", default_start), key="start_date")

    with date_col2:
        st.date_input("End Date", value=st.session_state.get("end_date", default_end), key="end_date")

    # 위젯 값들은 session_state에서 읽기
    input_file = st.session_state.get("input_file")
    master_file = st.session_state.get("master_file")
    start_date = st.session_state.get("start_date")
    end_date = st.session_state.get("end_date")

    # 임시 디버깅
    if master_file is not None:
        st.write("Master file uploaded", master_file.name)
    else:
        st.warning("Please uploaded master file")

    # 모든 입력이 있을 때 처리
    if input_file and master_file and start_date and end_date:

        try:
            transformed_df = transform_data(
                input_file=input_file,
                master_file=master_file,
                start_date=start_date,
                end_date=end_date
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