import numpy as np
import plotly.graph_objs as go

def create_imr_chart(data, return_summary=False, show_outliers=False):
    mean = np.mean(data)
    mr = np.abs(np.diff(data))
    mr_bar = np.mean(mr)
    d2 = 1.128
    sigma = mr_bar / d2
    ucl = mean + 3 * sigma
    lcl = mean - 3 * sigma

    outliers = (data > ucl) | (data < lcl)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=data, mode='lines+markers', name='개별값'))

    if show_outliers:
        outlier_indices = np.where(outliers)[0]
        fig.add_trace(go.Scatter(x=outlier_indices, y=data[outliers], mode='markers', name='이상치', marker=dict(color='red', size=10)))

    fig.add_trace(go.Scatter(y=[mean] * len(data), mode='lines', name='중심선', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(y=[ucl] * len(data), mode='lines', name='UCL', line=dict(color='red', dash='dot')))
    fig.add_trace(go.Scatter(y=[lcl] * len(data), mode='lines', name='LCL', line=dict(color='red', dash='dot')))

    fig.update_layout(title='I-MR 관리도', xaxis_title='순서', yaxis_title='값')

    summary = {
        '평균': [mean],
        'UCL': [ucl],
        'LCL': [lcl],
        '이상치 수': [int(np.sum(outliers))]
    }

    if return_summary:
        import pandas as pd
        return fig, pd.DataFrame(summary)
    return fig


def create_xbar_r_chart(data, sample_size, return_summary=False, show_outliers=False):
    sample_means = np.mean(data, axis=1)
    sample_ranges = np.ptp(data, axis=1)
    xbar_bar = np.mean(sample_means)
    r_bar = np.mean(sample_ranges)

    A2_TABLE = {
        2: 1.88, 3: 1.023, 4: 0.729, 5: 0.577, 6: 0.483,
        7: 0.419, 8: 0.373, 9: 0.337, 10: 0.308
    }
    D3_TABLE = {
        2: 0, 3: 0, 4: 0, 5: 0, 6: 0.076,
        7: 0.136, 8: 0.184, 9: 0.223, 10: 0.256
    }
    D4_TABLE = {
        2: 3.267, 3: 2.574, 4: 2.282, 5: 2.114, 6: 2.004,
        7: 1.924, 8: 1.864, 9: 1.816, 10: 1.777
    }

    A2 = A2_TABLE.get(sample_size, 0.577)
    D3 = D3_TABLE.get(sample_size, 0.076)
    D4 = D4_TABLE.get(sample_size, 1.924)

    xbar_ucl = xbar_bar + A2 * r_bar
    xbar_lcl = xbar_bar - A2 * r_bar
    r_ucl = D4 * r_bar
    r_lcl = D3 * r_bar

    xbar_outliers = (sample_means > xbar_ucl) | (sample_means < xbar_lcl)
    r_outliers = (sample_ranges > r_ucl) | (sample_ranges < r_lcl)

    xbar_fig = go.Figure()
    xbar_fig.add_trace(go.Scatter(y=sample_means, mode='lines+markers', name='샘플 평균'))
    if show_outliers:
        xbar_fig.add_trace(go.Scatter(x=np.where(xbar_outliers)[0], y=sample_means[xbar_outliers], mode='markers', name='이상치', marker=dict(color='red', size=10)))
    xbar_fig.add_trace(go.Scatter(y=[xbar_bar]*len(sample_means), mode='lines', name='중심선', line=dict(dash='dash', color='green')))
    xbar_fig.add_trace(go.Scatter(y=[xbar_ucl]*len(sample_means), mode='lines', name='UCL', line=dict(dash='dot', color='red')))
    xbar_fig.add_trace(go.Scatter(y=[xbar_lcl]*len(sample_means), mode='lines', name='LCL', line=dict(dash='dot', color='red')))
    xbar_fig.update_layout(title='X-bar 관리도', xaxis_title='샘플 그룹', yaxis_title='평균')

    r_fig = go.Figure()
    r_fig.add_trace(go.Scatter(y=sample_ranges, mode='lines+markers', name='샘플 범위'))
    if show_outliers:
        r_fig.add_trace(go.Scatter(x=np.where(r_outliers)[0], y=sample_ranges[r_outliers], mode='markers', name='이상치', marker=dict(color='red', size=10)))
    r_fig.add_trace(go.Scatter(y=[r_bar]*len(sample_ranges), mode='lines', name='중심선', line=dict(dash='dash', color='green')))
    r_fig.add_trace(go.Scatter(y=[r_ucl]*len(sample_ranges), mode='lines', name='UCL', line=dict(dash='dot', color='red')))
    r_fig.add_trace(go.Scatter(y=[r_lcl]*len(sample_ranges), mode='lines', name='LCL', line=dict(dash='dot', color='red')))
    r_fig.update_layout(title='R 관리도', xaxis_title='샘플 그룹', yaxis_title='범위')

    if return_summary:
        import pandas as pd
        xbar_summary = pd.DataFrame({
            '평균': [xbar_bar], 'UCL': [xbar_ucl], 'LCL': [xbar_lcl], '이상치 수': [int(np.sum(xbar_outliers))]
        })
        r_summary = pd.DataFrame({
            '평균': [r_bar], 'UCL': [r_ucl], 'LCL': [r_lcl], '이상치 수': [int(np.sum(r_outliers))]
        })
        return xbar_fig, r_fig, xbar_summary, r_summary

    return xbar_fig, r_fig