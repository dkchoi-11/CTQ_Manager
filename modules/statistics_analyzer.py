"""
기본 통계 분석 함수 모음
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import streamlit as st


def basic_statistics(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    기본 통계 분석

    Args:
        df (pd.DataFrame): 입력 데이터프레임
        columns (list, optional): 분석할 컬럼 리스트

    Returns:
        pd.DataFrame: 통계 분석 결과
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns

    stat_results = df[columns].describe().T

    # 추가 통계량 계산
    stat_results['skewness'] = df[columns].skew()
    stat_results['kurtosis'] = df[columns].kurtosis()

    return stat_results


def normality_test(df: pd.DataFrame, columns: list = None, alpha: float = 0.05) -> pd.DataFrame:
    """
    정규성 검정

    Args:
        df (pd.DataFrame): 입력 데이터프레임
        columns (list, optional): 검정할 컬럼 리스트
        alpha (float): 유의수준

    Returns:
        pd.DataFrame: 정규성 검정 결과
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns

    results = []
    for col in columns:
        # Shapiro-Wilk 검정
        statistic, p_value = stats.shapiro(df[col])
        is_normal = p_value > alpha

        results.append({
            'column': col,
            'statistic': statistic,
            'p_value': p_value,
            'is_normal_distribution': is_normal
        })

    return pd.DataFrame(results)


def correlation_analysis(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    상관관계 분석

    Args:
        df (pd.DataFrame): 입력 데이터프레임
        columns (list, optional): 분석할 컬럼 리스트

    Returns:
        pd.DataFrame: 상관관계 행렬
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns

    return df[columns].corr()


def confidence_interval(df: pd.DataFrame, columns: list = None, confidence: float = 0.95) -> pd.DataFrame:
    """
    평균의 신뢰구간 계산

    Args:
        df (pd.DataFrame): 입력 데이터프레임
        columns (list, optional): 분석할 컬럼 리스트
        confidence (float): 신뢰수준

    Returns:
        pd.DataFrame: 신뢰구간 결과
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns

    results = []
    for col in columns:
        data = df[col]
        mean = data.mean()
        std_error = stats.sem(data)

        # t-분포를 사용한 신뢰구간 계산
        ci = stats.t.interval(
            alpha=confidence,
            df=len(data) - 1,
            loc=mean,
            scale=std_error
        )

        results.append({
            'column': col,
            'mean': mean,
            'lower_ci': ci[0],
            'upper_ci': ci[1]
        })

    return pd.DataFrame(results)