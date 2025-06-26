"""
파일 업로드 및 다운로드 관련 함수 모음
"""
import os
import pandas as pd
import streamlit as st
from typing import Union
from io import BytesIO
from datetime import datetime

# 문자열 정리 함수
def clean_string(s):
    return str(s).strip().replace("/", "-")

def upload_excel_file() -> Union[pd.DataFrame, None]:
    """
    엑셀 파일 업로드 및 기본 검증 함수

    Returns:
        pd.DataFrame: 업로드된 데이터프레임
        None: 업로드 실패 시
    """
    uploaded_file = st.file_uploader(
        "Excel 파일을 업로드하세요",
        type=['xlsx', 'xls', 'csv']
    )

    if uploaded_file is not None:
        try:
            # 파일 확장자에 따라 다른 읽기 방식 적용
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            return df

        except Exception as e:
            st.error(f"파일 읽기 중 오류 발생: {e}")
            return None

    return None


# 메모리 내 엑셀 파일 객체 생성 (다운로드용)
def get_excel_download_buffer(df: pd.DataFrame, sheet_name="toLGE") -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)
    return output

# 자동 파일명 생성 함수
def generate_filename(df: pd.DataFrame) -> str:
    st.dataframe(df)
    if df is None or df.empty:
        return "empty_data"
    try:
        first_company = clean_string(df['1차 업체명'].unique()[0])
        region = clean_string(df['지역명'].unique()[0])
        second_company = clean_string(df['2차업체명'].unique()[0])
        model = clean_string(df['모델명'].unique()[0])
        part_name = clean_string(df['부품명'].unique()[0])
        ctq_name = clean_string(df['CTQ/P 관리항목명'].unique()[0])

        #df["측정일자"] = pd.to_datetime(df["측정일자"])
        #start_date = df["측정일자"].min().strftime("%Y%m%d")
        #end_date = df["측정일자"].max().strftime("%Y%m%d")
        file_date = datetime.today().strftime("%Y%m%d")

        if ctq_name == "Torque":
            save_filename = f"CTQ_{first_company}_{region}_{second_company}_{model}_{part_name}_{ctq_name}_{file_date}.xlsx"
        else:
            save_filename = f"CTQ_{first_company}_{region}_{second_company}_{model}_{part_name}_{file_date}.xlsx"

        #return f"CTQ_{first_company}_{region}_{second_company}_{model}_{part_name}_{start_date}_{end_date}.xlsx"
        return save_filename
    except Exception as e:
        st.warning("파일명 생성 오류:", e)
        return "generated_file.xlsx"

def validate_file(df: pd.DataFrame) -> bool:
    """
    업로드된 데이터프레임의 기본 유효성 검사

    Args:
        df (pd.DataFrame): 검증할 데이터프레임

    Returns:
        bool: 유효성 검사 결과
    """
    if df is None:
        st.warning("파일을 먼저 업로드해주세요.")
        return False

    if df.empty:
        st.warning("빈 데이터셋입니다.")
        return False

    return True

def download_excel(df: pd.DataFrame, filename: str = 'analyzed_data.xlsx'):
    """
    데이터프레임을 엑셀 파일로 다운로드

    Args:
        df (pd.DataFrame): 다운로드할 데이터프레임
        filename (str): 다운로드 파일명
    """

    save_filename = generate_filename(df)
    output = get_excel_download_buffer(df, "toLGE")

    st.download_button(
        label="Excel 파일로 다운로드",
        data=output,
        file_name=save_filename,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

