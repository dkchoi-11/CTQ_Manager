import pandas as pd
import streamlit as st

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

    if "관리번호" not in transformed_df.columns or "관리번호" not in master_df.columns:
        st.error("관리번호 컬럼이 존재하지 않습니다.")
        return pd.DataFrame()

    unique_ids = transformed_df["관리번호"].dropna().unique()
    filtered_master = master_df[master_df["관리번호"].isin(unique_ids)]

    required_columns = ['관리번호', '부품', '공정CTQ/CTP 관리 항목명', 'USL', 'LSL', 'Target', 'UCL', 'LCL']
    available_columns = [col for col in required_columns if col in filtered_master.columns]
    if len(available_columns) < len(required_columns):
        st.warning("Master 파일에 일부 품질 관리 기준 컬럼이 누락되었습니다.")

    result_df = filtered_master[available_columns].drop_duplicates()
    return result_df

def verify_data():
    """
        spec_df와 transformed_data를 비교하여
        USL/LSL 초과 데이터를 spev_over_data로 반환합니다.
    """
    spec_df = get_spec_from_master()
    if spec_df.empty:
        st.warning("스펙 데이타가 없습니다.")
        return pd.DataFrame(), pd.DataFrame()

    if "transformed_data" not in st.session_state:
        st.warning("변환된 데이터가 없습니다.")
        return pd.DataFrame(), pd.DataFrame()

    df = st.session_state.transformed_data.copy()

    if "관리번호" not in df.columns or "측정값" not in df.columns:
        st.error("transformed_data에 '관리번호' 또는 '측정값' 컬럼이 없습니다.")
        return pd.DataFrame(), pd.DataFrame()

    # 스펙과 transformed_data 병합
    merged_df = pd.merge(df, spec_df, on="관리번호", how="left")

    # USL, LSL 벗어난 값 찾기
    over_condition = (
            (merged_df["USL"].notnull() & (merged_df["측정값"] > merged_df["USL"])) |
            (merged_df["LSL"].notnull() & (merged_df["측정값"] < merged_df["LSL"]))
    )

    # 원본 데이터에 spec_over 추가 벗어난 경우 NG 표기.
    merged_df["spec_over"] =""
    merged_df.loc[over_condition, 'spec_over'] = "NG"
    merged_df = merged_df.drop(columns=merged_df.columns[[12,13]])

    spec_over_data = merged_df[over_condition].copy()

    return spec_over_data, merged_df

def get_spec_for_measured_ctq():
    """
    transformed_data에 있는 관리번호 기준으로 필터링된 spec_df를 반환하고
    st.session_state['spec_for_measured_ctq']에 저장합니다.
    """
    spec_df = get_spec_from_master()
    if spec_df.empty:
        st.warning("스펙 정보가 없습니다.")
        st.session_state.spec_df_filtered = pd.DataFrame()
        return pd.DataFrame()

    df = st.session_state.transformed_data
    if "관리번호" not in df.columns:
        st.error("transformed_data에 '관리번호' 컬럼이 없습니다.")
        st.session_state.spec_for_measured_ctq = pd.DataFrame()
        return pd.DataFrame()

    used_ids = df["관리번호"].dropna().unique()
    filtered_spec = spec_df[spec_df["관리번호"].isin(used_ids)].copy()

    # 세션 상태에 저장 (다른 페이지에서 재사용 가능)
    st.session_state.spec_for_measured_ctq = filtered_spec

    return filtered_spec



