import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any


def detect_outliers(df: pd.DataFrame,
                    columns: list = None,
                    method: str = 'iqr',
                    usl: float = None,
                    lsl: float = None) -> pd.DataFrame:
    """
    데이터에서 이상치를 검출하는 함수

    Parameters:
    -----------
    df : pandas.DataFrame
        입력 데이터프레임
    columns : list, optional
        이상치 검출을 수행할 컬럼 리스트 (None일 경우 모든 숫자형 컬럼)
    method : str, optional
        이상치 탐지 방법
        - 'iqr': IQR 방법 (1.5 * IQR)
        - 'spec_limit': 규격 한계(USL, LSL) 기반
        - 'z_score': 표준 편차 기반 (z-score)
    usl : float, optional
        Upper Specification Limit (규격 상한)
    lsl : float, optional
        Lower Specification Limit (규격 하한)

    Returns:
    --------
    pandas.DataFrame
        이상치 정보가 포함된 데이터프레임
    """
    # 숫자형 컬럼 선택
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # 이상치 결과를 저장할 데이터프레임
    outliers_df = pd.DataFrame()

    for col in columns:
        series = df[col]

        if method == 'iqr':
            # IQR 방법
            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = series[(series < lower_bound) | (series > upper_bound)]

        elif method == 'spec_limit':
            # 규격 한계 기반 이상치 탐지
            if usl is None or lsl is None:
                raise ValueError("USL과 LSL 값을 모두 제공해야 합니다.")

            outliers = series[(series < lsl) | (series > usl)]

        elif method == 'z_score':
            # Z-score 방법 (표준편차 기반)
            z_scores = np.abs((series - series.mean()) / series.std())
            outliers = series[z_scores > 3]  # 3 표준편차 이상

        else:
            raise ValueError("유효하지 않은 이상치 탐지 방법입니다.")

        # 이상치가 있는 경우 결과 저장
        if not outliers.empty:
            temp_df = pd.DataFrame({
                'Column': [col] * len(outliers),
                'Index': outliers.index,
                'Value': outliers.values
            })
            outliers_df = pd.concat([outliers_df, temp_df], ignore_index=True)

    return outliers_df


def clean_data(df: pd.DataFrame,
               remove_outliers: bool = False,
               method: str = 'iqr',
               usl: float = None,
               lsl: float = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    데이터 클리닝 및 이상치 처리 함수

    Parameters:
    -----------
    df : pandas.DataFrame
        입력 데이터프레임
    remove_outliers : bool, optional
        이상치 제거 여부
    method : str, optional
        이상치 탐지 방법
    usl : float, optional
        Upper Specification Limit
    lsl : float, optional
        Lower Specification Limit

    Returns:
    --------
    Tuple[pandas.DataFrame, pandas.DataFrame]
        (클리닝된 데이터프레임, 이상치 데이터프레임)
    """
    # 이상치 탐지
    outliers_df = detect_outliers(df, method=method, usl=usl, lsl=lsl)

    # 이상치 제거 옵션
    if remove_outliers and not outliers_df.empty:
        cleaned_df = df.drop(outliers_df['Index'])
    else:
        cleaned_df = df.copy()

    return cleaned_df, outliers_df


def get_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """
    데이터 품질 보고서 생성

    Parameters:
    -----------
    df : pandas.DataFrame
        입력 데이터프레임

    Returns:
    --------
    Dict[str, Any]
        데이터 품질 관련 정보
    """
    # 기본 품질 정보
    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().to_dict(),
        'data_types': df.dtypes.to_dict(),
        'duplicates': df.duplicated().sum()
    }

    # 숫자형 컬럼에 대한 추가 분석
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    if len(numeric_columns) > 0:
        quality_report['numeric_summary'] = df[numeric_columns].describe().to_dict()

    return quality_report


# 예외 처리 관련 사용자 정의 예외 클래스
class DataCleaningError(Exception):
    """데이터 클리닝 중 발생하는 예외"""
    pass