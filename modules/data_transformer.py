"""
데이터 변환 및 전처리 함수 모음
"""
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import re
from typing import Optional, List, Dict, Union


# 날짜 형식이 가장 많이 들어있는 열의 인덱스를 찾는 함수
def find_date_start_col(df: pd.DataFrame, sample_row_count: int = 10) -> int:
    def is_date(x: Union[str, datetime]) -> bool:
        if not isinstance(x, str):
            return False
        x = x.strip()

        # 날짜 형식 패턴 (예: 1/6, 01-07-2024, 2024.01.08)
        date_pattern = re.compile(r'^\d{1,4}[/.-]\d{1,2}([/.-]\d{2,4})?$')

        if date_pattern.match(x):
            return True

        try:
            converted = pd.to_datetime(x, errors='coerce')
            return pd.notna(converted)
        except:
            return False

    date_counts = [
        sum(df.iloc[:sample_row_count, col_idx].astype(str).apply(is_date))
        for col_idx in range(df.shape[1])
    ]
    best_col = date_counts.index(max(date_counts))

    if date_counts[best_col] == 0:
        raise ValueError("No date column found")

    print(best_col)
    return best_col

# 날짜가 포함된 첫 번째 행의 인덱스를 찾는 함수
def find_date_row(df: pd.DataFrame, date_start_col: Optional[int] = None,
                  min_date_count: int = 1, max_row_check: int = 20) -> int:
    if date_start_col is None:
        date_start_col = find_date_start_col(df)

    def is_date(x: Union[str, datetime, pd.Timestamp]) -> bool:
        if isinstance(x, (pd.Timestamp, datetime)):
            return True
        if isinstance(x, str):
            try:
                pd.to_datetime(x)
                return True
            except:
                return False
        return False

    for i in range(min(max_row_check, len(df))):
        row = df.iloc[i, date_start_col:]
        if row.apply(is_date).sum() >= min_date_count:
            return i

    raise ValueError("No date row found")

# 날짜가 들어 있는 셀들의 열 인덱스를 실제 날짜 값과 매핑하는 함수
def get_date_mapping(df: pd.DataFrame, date_row_index: int,
                     date_start_col: Optional[int] = None) -> Dict[int, pd.Timestamp]:
    if date_start_col is None:
        date_start_col = find_date_start_col(df)

    date_row = df.iloc[date_row_index, date_start_col:]
    dates = pd.to_datetime(date_row, errors='coerce')

    mapping = {}
    for col_idx, date in zip(range(date_start_col, len(df.columns)), dates):
        if pd.notna(date):
            mapping[col_idx] = date

    return mapping

# 측정 데이터를 추출하는 함수
def extract_measurement_data(
        df: pd.DataFrame,
        info_dict: Dict[str, str],
        date_mapping: Dict[int, pd.Timestamp],
        date_row_index: int,
        search_cols: List[int] = list(range(0, 11))
) -> pd.DataFrame:
    results = []
    search_cols = [col for col in search_cols if col < df.shape[1]]

    point_indices = []
    for i in range(date_row_index, len(df)):
        for col in search_cols:
            if col >= df.shape[1]:
                continue
            cell_value = df.iloc[i, col]
            if "POINT" in str(cell_value).strip().upper():
                ctq_col = col + 1
                if ctq_col < df.shape[1]:
                    # 4/3일 Master 파일의 공정ctq/ctp 관리 항목명에 -을 공백으로 변경.
                    # Data 관리하는 시트에서 CTQ 명에 -을 없애라고 공지를 했으나, 없애지 않은 경우 대비하여
                    # - 있는 경우 공백으로 변경하도록 함.
                    ctq_name = df.iloc[i, ctq_col].replace('-', ' ').strip()
                    if pd.notna(ctq_name):
                        point_indices.append((i, ctq_name))
                break

    for idx, (start_idx, ctq_name) in enumerate(point_indices):
        if idx + 1 < len(point_indices):
            end_idx = point_indices[idx + 1][0]
        else:
            end_idx = start_idx + 1
            while end_idx < len(df):
                if df.iloc[end_idx, min(date_mapping.keys()):].notna().sum() > 0:
                    end_idx += 1
                else:
                    break

        for i in range(start_idx, end_idx):
            for col in date_mapping:
                if col < df.shape[1] and i < df.shape[0]:
                    value = df.iloc[i, col]
                    if pd.notna(value):
                        results.append({
                            '1차 업체명': str(info_dict.get("1차 업체명", "")).strip(),
                            '지역명': str(info_dict.get("지역명", "")).strip(),
                            '2차업체명': str(info_dict.get("2차업체명", "")).strip(),
                            '모델명': str(info_dict.get("모델명", "")).strip(),
                            '측정자': str(info_dict.get("측정자", "")).strip(),
                            '측정장비': str(info_dict.get("측정장비", "")).strip(),
                            '부품명': str(info_dict.get("부품명", "")).strip(),
                            'CTQ/P 관리항목명': str(ctq_name).strip(),
                            '측정일자': date_mapping[col],
                            '측정값': value,
                            'Part No': str(info_dict.get("Part No", "")).strip()
                        })

    return pd.DataFrame(results)

# 관리번호를 매핑하는 함수
def add_management_code(results_df: pd.DataFrame, master_key_df: pd.DataFrame) -> pd.DataFrame:
    merge_keys = ["1차 업체명", "지역명", "2차업체명", "부품명", "CTQ/P 관리항목명", "모델명", "Part No"]

    master_key_df_renamed = master_key_df.rename(columns={
        "부품": "부품명",
        "공정CTQ/CTP 관리 항목명": "CTQ/P 관리항목명",
        "2차 업체명": "2차업체명"
    })

    master_key_df_renamed = master_key_df_renamed.loc[:, merge_keys + ["관리번호"]]

    for key in merge_keys:
        results_df[key] = results_df[key].astype(str).str.strip()
        master_key_df_renamed[key] = master_key_df_renamed[key].astype(str).str.strip()

    merged_df = pd.merge(results_df, master_key_df_renamed, on=merge_keys, how='left')

    # 관리번호를 첫 번째 열로 이동
    if "관리번호" in merged_df.columns:
        cols = merged_df.columns.tolist()
        cols.remove("관리번호")
        merged_df = merged_df[["관리번호"] + cols]

    return merged_df

# 전체 프로세스를 실행하는 함수, input, master 수정 필요, start, end 수정 필요
def transform_data(
        input_file,
        master_file,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search_cols: List[int] = list(range(0, 11))
) -> pd.DataFrame:

    info_df = pd.read_excel(input_file, sheet_name="Information", engine="openpyxl")
    info_dict = info_df.set_index("Contents")['Value'].to_dict()

    original_df = pd.read_excel(input_file, sheet_name=info_dict["Data_sheet"], header=None, engine="openpyxl")
    master_df = pd.read_excel(master_file, sheet_name="Master", engine="openpyxl")
    st.session_state.master_data = master_df

    date_row_idx = find_date_row(original_df)
    date_map = get_date_mapping(original_df, date_row_idx)

    df_result = extract_measurement_data(original_df, info_dict, date_map, date_row_idx, search_cols)
    df_result = add_management_code(df_result, master_df)

    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        df_result = df_result[
            (df_result["측정일자"] >= start_date) &
            (df_result["측정일자"] <= end_date)
        ]

    df_result_sorted = df_result.sort_values(by=["측정일자", "CTQ/P 관리항목명"]).reset_index(drop=True)
    st.session_state.transformed_data = df_result_sorted

    return df_result_sorted