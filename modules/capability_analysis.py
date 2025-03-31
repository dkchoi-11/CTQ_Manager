import numpy as np
import plotly.graph_objs as go
from scipy.stats import norm


def calculate_capability_indices(data: np.ndarray, usl: float, lsl: float):
    """
    공정능력지수 계산 (Cp, Cpk)
    """
    mean = np.mean(data)
    std = np.std(data, ddof=1)

    Cp = (usl - lsl) / (6 * std)
    Cpk = min((usl - mean) / (3 * std), (mean - lsl) / (3 * std))

    return {
        'mean': mean,
        'std': std,
        'Cp': Cp,
        'Cpk': Cpk
    }


def process_capability_histogram(data: np.ndarray, usl: float, lsl: float):
    """
    공정능력 히스토그램 + 정규분포 곡선 시각화
    """
    stats = calculate_capability_indices(data, usl, lsl)
    mean, std = stats['mean'], stats['std']

    # 히스토그램 설정
    hist_trace = go.Histogram(
        x=data,
        nbinsx=20,
        histnorm='probability density',
        name='Measurement Distribution',
        opacity=0.6
    )

    # 정규분포 곡선
    x_range = np.linspace(mean - 4*std, mean + 4*std, 500)
    pdf = norm.pdf(x_range, mean, std)
    bin_width = (max(data) - min(data)) / 20
    pdf_scaled = pdf * len(data) * bin_width

    normal_curve = go.Scatter(
        x=x_range,
        y=pdf_scaled,
        mode='lines',
        name='Normal distribution curve',
        line=dict(color='blue', dash='dot')
    )

    # 사양 상한/하한선
    usl_line = go.Scatter(x=[usl, usl], y=[0, max(pdf_scaled)], name='USL', line=dict(color='red', dash='dash'))
    lsl_line = go.Scatter(x=[lsl, lsl], y=[0, max(pdf_scaled)], name='LSL', line=dict(color='red', dash='dash'))

    # 그래프 구성
    fig = go.Figure(data=[hist_trace, normal_curve, usl_line, lsl_line])
    fig.update_layout(
        title='Capability Analysis Histogram',
        xaxis_title='Measurements',
        yaxis_title='frequency',
        bargap=0.05
    )

    return fig, stats
