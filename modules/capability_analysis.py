"""
공정능력 분석 함수 모음
"""
import numpy as np
import pandas as pd
import scipy.stats as stats
import plotly.graph_objs as go
import streamlit as st


def calculate_capability_indices(data: np.ndarray, usl: float, lsl: float):
    """
    공정능력 지수 계산

    Args:
        data (np.ndarray): 입력 데이터
        usl (float): 상한 규격
        lsl (float): 하한 규격

    Returns:
        dict: 공정능력 지수
    """
    # 데이터 기술 통계량
    mean = np.mean(data)
    std = np.std(data, ddof=1)

    # 공정능력 지수 계산
    Cp = (usl - lsl) / (6 * std)
    Cpk = min(
        (usl - mean) / (3 * std),
        (mean - lsl) / (3 * std)
    )

    # 단기/장기 변동성 고려 (잠정적)
    Pp = (usl - lsl) / (6 * std)
    Ppk = min(
        (usl - mean) / (3 * std),
        (mean - lsl) / (3 * std)
    )

    return {
        'mean': mean,
        'std': std,
        'Cp': Cp,
        'Cpk': Cpk,
        'Pp': Pp,
        'Ppk': Ppk
    }


def process_capability_histogram(data: np.ndarray, usl: float, lsl: float):
    """
    공정능력 히스토그램 생성

    Args:
        data (np.ndarray): 입력 데이터
        usl (float): 상한 규격
        lsl (float): 하한 규격

    Returns:
        plotly 그래프 객체
    """
    cap_indices = calculate_capability_indices(data, usl, lsl)

    # 히스토그램 생성
    hist_trace = go.Histogram(
        x=data,
        name='데이터 분포',
        opacity=0.75
    )

    # 정규분포 곡선
    x = np.linspace(min(data), max(data), 100)
    pdf = stats.norm.pdf(x, cap_indices['mean'], cap_indices['std'])
    pdf_trace = go.Scatter(
        x=x,
        y=pdf * len(data) * (max(data) - min(data)) / 10,  # 히스토그램과 스케일 맞추기
        mode='lines',
        name='정규분포 곡선'
    )

    # 규격 한계선
    usl_trace = go.Scatter(
        x=[usl, usl],
        y=[0, np.max(pdf) * len(data)],
        mode='lines',
        name='USL',
        line=dict(color='red', dash='dot')
    )
    lsl_trace = go.Scatter(
        x=[lsl, lsl],
        y=[0, np.max(pdf) * len(data)],
        mode='lines',
        name='LSL',
        line=dict(color='red', dash='dot')
    )

    layout = go.Layout(
        title='공정능력 히스토그램',
        xaxis_title='측정값',
        yaxis_title='빈도',
        annotations=[
            dict(
                x=0.5, y=1.1,
                text=f'Cp: {cap_indices["Cp"]:.2f}, Cpk: {cap_indices["Cpk"]:.2f}',
                showarrow=False,
                xref='paper',
                yref='paper'
            )
        ]
    )

    fig = go.Figure(data=[hist_trace, pdf_trace, usl_trace, lsl_trace], layout=layout)

    return fig, cap_indices