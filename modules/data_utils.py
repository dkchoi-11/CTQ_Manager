import pandas as pd
import streamlit as st
from astropy.cosmology import available

from modules.data_transformer import transform_data


# master_data에서 spec (USL,LSL, Target, UCL, LCL) 가져오기
def get_spec_from_master():
    """
    세션에 저장된 transformed_data의 관리번호를 기준으로
    master_data에서 USL, LSL, Target, UCL, LCL을 추출.
    """
    if "transformed_data" not in st.session_state or "master_data" not in st.session_state:
        st.warning("데이터가 세션에 없습니다.")
        return pd.DataFrame()

    transformed_df = st.session_state.transformed_data
    master_df = st.session_state.master_data

    if "관리번호" not in transformed_df.columns or "관리버호" not in master_df.columns:
        st.error("관리번호 컬럼이 존재하지 않습니다.")
        return pd.DataFrame()

    unique_ids = transformed_df["관리번호"].dropna().unique()
    filtered_master = master_df[master_df["관리번호"].isin(unique_ids)]

    required_columns = ['관리번호', 'USL', 'LSL', 'Target', 'UCL', 'LCL']
    available_columns = [col for col in required_columns if col in filtered_master.columns]
    if len(available_columns) < len(required_columns):
        st.warning("Master 파일에 일부 품질 관리 기준 컬럼이 누락되었습니다.")

    result_df = filtered_master[available_columns].drop_duplicates()
    result_df result_df



