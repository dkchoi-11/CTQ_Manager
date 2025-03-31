import numpy as np
import plotly.graph_objs as go
import pandas as pd

def create_imr_chart(data, x=None, return_summary=False, show_outliers=False):
    mean = np.mean(data)
    mr = np.abs(np.diff(data))
    mr_bar = np.mean(mr)
    d2 = 1.128
    sigma = mr_bar / d2
    ucl = mean + 3 * sigma
    lcl = mean - 3 * sigma

    outliers = (data > ucl) | (data < lcl)
    x_vals = x if x is not None else list(range(len(data)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=data, mode='lines+markers', name='개별값'))

    if show_outliers:
        outlier_indices = [x_vals[i] for i in np.where(outliers)[0]]
        fig.add_trace(go.Scatter(x=outlier_indices, y=data[outliers], mode='markers', name='이상치', marker=dict(color='red', size=10)))

    fig.add_trace(go.Scatter(x=x_vals, y=[mean] * len(data), mode='lines', name='중심선', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=x_vals, y=[ucl] * len(data), mode='lines', name='UCL', line=dict(color='red', dash='dot')))
    fig.add_trace(go.Scatter(x=x_vals, y=[lcl] * len(data), mode='lines', name='LCL', line=dict(color='red', dash='dot')))

    fig.update_layout(title='I-MR control chart', xaxis_title='Date' if x is not None else '순서', yaxis_title='값')

    summary = {
        'Mean': [mean],
        'UCL': [ucl],
        'LCL': [lcl],
        'outlier number': [int(np.sum(outliers))]
    }

    if return_summary:
        return fig, pd.DataFrame(summary)
    return fig

def create_xbar_r_chart(data, sample_size, x=None, return_summary=False, show_outliers=False):
    sample_means = np.mean(data, axis=1)
    sample_ranges = np.ptp(data, axis=1)
    xbar_bar = np.mean(sample_means)
    r_bar = np.mean(sample_ranges)

    A2_TABLE = {2: 1.88, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483, 7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308}
    D3_TABLE = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0.076, 7: 0.136, 8: 0.184, 9: 0.223, 10: 0.256}
    D4_TABLE = {2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004, 7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777}

    A2 = A2_TABLE.get(sample_size, 0.577)
    D3 = D3_TABLE.get(sample_size, 0.076)
    D4 = D4_TABLE.get(sample_size, 1.924)

    xbar_ucl = xbar_bar + A2 * r_bar
    xbar_lcl = xbar_bar - A2 * r_bar
    r_ucl = D4 * r_bar
    r_lcl = D3 * r_bar

    xbar_outliers = (sample_means > xbar_ucl) | (sample_means < xbar_lcl)
    r_outliers = (sample_ranges > r_ucl) | (sample_ranges < r_lcl)

    x_vals = x if x is not None else list(range(len(sample_means)))

    xbar_fig = go.Figure()
    xbar_fig.add_trace(go.Scatter(x=x_vals, y=sample_means, mode='lines+markers', name='샘플 평균'))
    if show_outliers:
        xbar_fig.add_trace(go.Scatter(x=[x_vals[i] for i in np.where(xbar_outliers)[0]], y=sample_means[xbar_outliers], mode='markers', name='이상치', marker=dict(color='red', size=10)))
    xbar_fig.add_trace(go.Scatter(x=x_vals, y=[xbar_bar]*len(sample_means), mode='lines', name='중심선', line=dict(dash='dash', color='green')))
    xbar_fig.add_trace(go.Scatter(x=x_vals, y=[xbar_ucl]*len(sample_means), mode='lines', name='UCL', line=dict(dash='dot', color='red')))
    xbar_fig.add_trace(go.Scatter(x=x_vals, y=[xbar_lcl]*len(sample_means), mode='lines', name='LCL', line=dict(dash='dot', color='red')))
    xbar_fig.update_layout(title='X-bar control chart', xaxis_title='측정일자' if x is not None else '샘플 그룹', yaxis_title='평균')

    r_fig = go.Figure()
    r_fig.add_trace(go.Scatter(x=x_vals, y=sample_ranges, mode='lines+markers', name='샘플 범위'))
    if show_outliers:
        r_fig.add_trace(go.Scatter(x=[x_vals[i] for i in np.where(r_outliers)[0]], y=sample_ranges[r_outliers], mode='markers', name='이상치', marker=dict(color='red', size=10)))
    r_fig.add_trace(go.Scatter(x=x_vals, y=[r_bar]*len(sample_ranges), mode='lines', name='중심선', line=dict(dash='dash', color='green')))
    r_fig.add_trace(go.Scatter(x=x_vals, y=[r_ucl]*len(sample_ranges), mode='lines', name='UCL', line=dict(dash='dot', color='red')))
    r_fig.add_trace(go.Scatter(x=x_vals, y=[r_lcl]*len(sample_ranges), mode='lines', name='LCL', line=dict(dash='dot', color='red')))
    r_fig.update_layout(title='R control chart', xaxis_title='Date' if x is not None else 'Sample Group', yaxis_title='Range')

    if return_summary:
        xbar_summary = pd.DataFrame({'Mean': [xbar_bar], 'UCL': [xbar_ucl], 'LCL': [xbar_lcl], '이상치 수': [int(np.sum(xbar_outliers))]})
        r_summary = pd.DataFrame({'Mean': [r_bar], 'UCL': [r_ucl], 'LCL': [r_lcl], '이상치 수': [int(np.sum(r_outliers))]})
        return xbar_fig, r_fig, xbar_summary, r_summary

    return xbar_fig, r_fig
