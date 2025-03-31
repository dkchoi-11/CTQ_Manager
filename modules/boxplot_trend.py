import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import scipy.stats as stats


def create_boxplot(data: pd.DataFrame, columns: list = None):
    """
    주어진 데이터프레임의 지정된 열에 대해 박스 플롯을 생성합니다.

    매개변수:
    - data (pd.DataFrame): 분석할 데이터프레임
    - columns (list, 선택): 박스플롯을 그릴 열 이름 리스트 (None일 경우 모든 숫자형 열)

    반환값:
    - plotly Figure 객체: 박스플롯 그래프
    """
    # 숫자형 열 자동 선택
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()

    # 다중 박스플롯 생성
    fig = go.Figure()
    for col in columns:
        fig.add_trace(go.Box(
            y=data[col],
            name=col,
            boxpoints='all',  # 모든 포인트 표시
            jitter=0.3,  # 포인트 분산
            pointpos=-1.8  # 포인트 위치 조정
        ))

    fig.update_layout(
        title='box plot analysis',
        yaxis_title='Value',
        xaxis_title='variable',
        height=600,
        width=800
    )

    return fig


def detect_outliers_iqr(data: pd.DataFrame, columns: list = None):
    """
    IQR 방식을 사용하여 이상치를 탐지합니다.

    매개변수:
    - data (pd.DataFrame): 분석할 데이터프레임
    - columns (list, 선택): 이상치 분석할 열 이름 리스트 (None일 경우 모든 숫자형 열)

    반환값:
    - dict: 각 열별 이상치 정보
    """
    # 숫자형 열 자동 선택
    if columns is None:
        columns = data.select_dtypes(include=[np.number]).columns.tolist()

    outliers_dict = {}
    for col in columns:
        # Q1, Q3, IQR 계산
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1

        # 이상치 경계 계산 (1.5 * IQR 기준)
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # 이상치 식별
        outliers = data[(data[col] < lower_bound) | (data[col] > upper_bound)]

        outliers_dict[col] = {
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers_count': len(outliers),
            'outliers_percentage': len(outliers) / len(data) * 100,
            'outliers_indices': outliers.index.tolist()
        }

    return outliers_dict


def trend_analysis(data: pd.DataFrame, time_column: str, value_columns: list = None):
    """
    시계열 데이터의 추세를 분석하고 시각화합니다.

    매개변수:
    - data (pd.DataFrame): 분석할 데이터프레임
    - time_column (str): 시간 열 이름
    - value_columns (list, 선택): 분석할 수치 열 이름 리스트 (None일 경우 모든 숫자형 열)

    반환값:
    - plotly Figure 객체: 추세 분석 그래프
    """
    # 시간 열 datetime으로 변환
    data[time_column] = pd.to_datetime(data[time_column])

    # 숫자형 열 자동 선택
    if value_columns is None:
        value_columns = data.select_dtypes(include=[np.number]).columns.tolist()

    # 다중 라인 그래프 생성
    fig = go.Figure()
    for col in value_columns:
        # 선형 회귀 추세선 계산
        # 타임스탬프를 안전하게 숫자로 변환
        x = (data[time_column] - data[time_column].min()).dt.total_seconds()
        y = data[col]

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        # 추세선 데이터 생성
        trend_line = slope * x + intercept

        # 원본 데이터 라인 추가
        fig.add_trace(go.Scatter(
            x=data[time_column],
            y=data[col],
            mode='lines+markers',
            name=f'{col} (actual data)'
        ))

        # 추세선 추가
        fig.add_trace(go.Scatter(
            x=data[time_column],
            y=trend_line,
            mode='lines',
            name=f'{col} Trend line (R² = {r_value ** 2:.4f})',
            line=dict(dash='dot')
        ))

    fig.update_layout(
        title='Time series trend analysis',
        xaxis_title='Time',
        yaxis_title='Value',
        height=600,
        width=1000
    )

    return fig


def perform_comprehensive_trend_analysis(data: pd.DataFrame, time_column: str, value_columns: list = None):
    """
    종합적인 추세 분석 리포트를 생성합니다.

    매개변수:
    - data (pd.DataFrame): 분석할 데이터프레임
    - time_column (str): 시간 열 이름
    - value_columns (list, 선택): 분석할 수치 열 이름 리스트

    반환값:
    - dict: 추세 분석 결과 딕셔너리
    """
    # 시간 열 datetime으로 변환
    data[time_column] = pd.to_datetime(data[time_column])

    # 숫자형 열 자동 선택
    if value_columns is None:
        value_columns = data.select_dtypes(include=[np.number]).columns.tolist()

    trend_results = {}
    for col in value_columns:
        # 시간 데이터를 초 단위로 변환
        x = data[time_column].astype('int64') / 10 ** 9
        y = data[col]

        # 선형 회귀 분석
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

        trend_results[col] = {
            '기울기': slope,  # 변화율
            '절편': intercept,
            'R제곱': r_value ** 2,  # 결정계수
            'p_값': p_value,  # 통계적 유의성
            '표준오차': std_err,
            '추세 해석': (
                '강한 증가 추세' if slope > 0 and r_value ** 2 > 0.7 else
                '약한 증가 추세' if slope > 0 and r_value ** 2 > 0.3 else
                '강한 감소 추세' if slope < 0 and r_value ** 2 > 0.7 else
                '약한 감소 추세' if slope < 0 and r_value ** 2 > 0.3 else
                '추세 없음'
            )
        }

    return trend_results


# 테스트용 메인 함수 (개발 중 디버깅용)
def main():
    # 테스트용 샘플 데이터 생성
    np.random.seed(42)
    test_data = pd.DataFrame({
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'value1': np.cumsum(np.random.normal(0, 1, 100)),
        'value2': np.random.normal(50, 10, 100)
    })

    # 박스플롯 생성
    boxplot_fig = create_boxplot(test_data, ['value1', 'value2'])
    boxplot_fig.show()

    # 이상치 탐지
    outliers = detect_outliers_iqr(test_data, ['value1', 'value2'])
    print("Outlier information:", outliers)

    # 추세 분석
    trend_fig = trend_analysis(test_data, 'timestamp', ['value1', 'value2'])
    trend_fig.show()

    # 종합 추세 분석
    trend_report = perform_comprehensive_trend_analysis(test_data, 'timestamp', ['value1', 'value2'])
    print("rend Analysis Report:", trend_report)


if __name__ == '__main__':
    main()