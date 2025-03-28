import streamlit as st
import pandas as pd
from io import BytesIO

# 모듈 import
from modules.file_handler import (
    clean_string,
    get_excel_download_buffer,
    generate_filename,
    download_excel
)

# 문자열 변환용 함수
def clean_string(s):
    return str(s).strip().replace("/", "-")

# 결과 저장 함수
def save_to_excel(df: pd.DataFrame) -> None:

    # 중복 제거 후 고유값 추출
    first_company = clean_string(df['1차 업체명'].unique()[0])
    region = clean_string(df['지역명'].unique()[0])
    second_company = clean_string(df['2차업체명'].unique()[0])
    model = clean_string(df['모델명'].unique()[0])
    part_name = clean_string(df['부품명'].unique()[0])

    # 날짜 형식 변환 및 정렬
    df["측정일자"] = pd.to_datetime(df["측정일자"])
    start_date = df["측정일자"].min().strftime("%Y%m%d")
    end_date = df["측정일자"].max().strftime("%Y%m%d")

    # 파일명 생성
    filename = f"CTQ_{first_company}_{region}_{second_company}_{model}_{part_name}_{start_date}_{end_date}.xlsx"

    # 엑셀 저장 (시트 이름 toLGE)
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='toLGE', index=False)

def download_data_page():
    """데이터 다운로드 페이지 (Data Download Page)"""
    st.header("데이터 다운로드")

    # 변환된 데이터 확인
    if 'transformed_data' not in st.session_state:
        st.warning("먼저 데이터를 업로드하고 변환해주세요.")
        return

    df = st.session_state.transformed_data

    # 다운로드 옵션
    download_type = st.selectbox("다운로드할 데이터 선택", [
        "변환된 데이터"
    ])

    if download_type == "변환된 데이터":
        download_data = df
    elif download_type == "이상치 데이터":
        # 이전에 검출된 이상치 데이터 또는 새로 탐지
        download_data = detect_outliers(df)
    else:
        # 품질 분석 보고서 생성
        download_data = pd.DataFrame.from_dict(
            get_data_quality_report(df),
            orient='index'
        )

    # 엑셀 다운로드 버튼
    download_excel(download_data, f"{download_type}.xlsx")