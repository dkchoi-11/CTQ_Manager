"""
관리도(Control Chart) 생성 함수 모음
"""
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import streamlit as st


def calculate_control_limits(data: np.ndarray, chart_type: str = 'i-mr'):
    """
    관리도 한계선 계산

    Args:
        data (np.ndarray): 입력 데이터
        chart_type (str): 관리도 유형 ('i-mr', 'xbar-r', 'xbar-s')

    Returns:
        dict: 관리 한계선 정보
    """
    mean = np.mean(data)

    if chart_type == 'i-mr':
        moving_ranges = np.abs(np.diff(data))
        mr_mean = np.mean(moving_ranges)

        # 계수 (d2 = 1.128 for sample size 2)
        d2 = 1.128

        return {
            'mean': mean,
            'ucl': mean + 3 * (mr_mean / d2),
            'lcl': mean - 3 * (mr_mean / d2)
        }

    elif chart_type in ['xbar-r', 'xbar-s']:
        # 평균 범위나 표준편차 계산
        if chart_type == 'xbar-r':
            ranges = np.max(data, axis=1) - np.min(data, axis=1)
            r_bar = np.mean(ranges)

            # 계수 (A2 = 1.023 for sample size 5)
            A2 = 1.023

            return {
                'mean': mean,
                'ucl': mean + A2 * r_bar,
                'lcl': mean - A2 * r_bar
            }
        else:
            # Xbar-S 차트 로직 추가 필요
            pass

    return None


def create_individual_moving_range_chart(data: np.ndarray):
    """
    개별값-이동범위(I-MR) 관리도 생성

    Args:
        data (np.ndarray): 입력 데이터

    Returns:
        plotly 그래프 객체
    """
    # 개별값 차트
    individual_limits = calculate_control_limits(data, 'i-mr')

    fig = go.Figure()

    # 개별값 트렌드
    fig.add_trace(go.Scatter(
        y=data,
        mode='lines+markers',
        name='개별값'
    ))

    # 중심선
    fig.add_trace(go.Scatter(
        y=[individual_limits['mean']] * len(data),
        mode='lines',
        name='중심선',
        line=dict(color='green', dash='dash')
    ))

    # UCL, LCL
    fig.add_trace(go.Scatter(
        y=[individual_limits['ucl']] * len(data),
        mode='lines',
        name='UCL',
        line=dict(color='red', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        y=[individual_limits['lcl']] * len(data),
        mode='lines',
        name='LCL',
        line=dict(color='red', dash='dot')
    ))

    fig.update_layout(
        title='개별값-이동범위(I-MR) 관리도',
        xaxis_title='관찰 순서',
        yaxis_title='측정값'
    )

    return fig


def xbar_r_chart(data: np.ndarray):
    """
    X-bar & R 관리도 생성

    Args:
        data (np.ndarray): 샘플 데이터 (2D numpy array)

    Returns:
        tuple: Xbar 차트와 R 차트의 plotly 그래프 객체
    """
    # 각 샘플의 평균 계산
    sample_means = np.mean(data, axis=1)

    # 각 샘플의 범위 계산
    sample_ranges = np.max(data, axis=1) - np.min(data, axis=1)

    # 관리 한계선 계산
    xbar_limits = calculate_control_limits(data, 'xbar-r')
    r_limits = calculate_control_limits(data, 'xbar-r')

    # Xbar 차트
    xbar_fig = go.Figure()
    xbar_fig.add_trace(go.Scatter(
        y=sample_means,
        mode='lines+markers',
        name='샘플 평균'
    ))
    xbar_fig.add_trace(go.Scatter(
        y=[xbar_limits['mean']] * len(sample_means),
        mode='lines',
        name='중심선',
        line=dict(color='green', dash='dash')
    ))
    xbar_fig.add_trace(go.Scatter(
        y=[xbar_limits['ucl']] * len(sample_means),
        mode='lines',
        name='UCL',
        line=dict(color='red', dash='dot')
    ))
    xbar_fig.add_trace(go.Scatter(
        y=[xbar_limits['lcl']] * len(sample_means),
        mode='lines',
        name='LCL',
        line=dict(color='red', dash='dot')
    ))
    xbar_fig.update_layout(
        title='X-bar 관리도',
        xaxis_title='샘플 그룹',
        yaxis_title='샘플 평균'
    )

    # R 차트
    r_fig = go.Figure()
    r_fig.add_trace(go.Scatter(
        y=sample_ranges,
        mode='lines+markers',
        name='샘플 범위'
    ))
    r_fig.add_trace(go.Scatter(
        y=[r_limits['mean']] * len(sample_ranges),
        mode='lines',
        name='중심선',
        line=dict(color='green', dash='dash')
    ))
    r_fig.add_trace(go.Scatter(
        y=[r_limits['ucl']] * len(sample_ranges),
        mode='lines',
        name='UCL',
        line=dict(color='red', dash='dot')
    ))
    r_fig.add_trace(go.Scatter(
        y=[r_limits['lcl']] * len(sample_ranges),
        mode='lines',
        name='LCL',
        line=dict(color='red', dash='dot')
    ))
    r_fig.update_layout(
        title='R 관리도',
        xaxis_title='샘플 그룹',
        yaxis_title='샘플 범위'
    )

    return xbar_fig, r_fig