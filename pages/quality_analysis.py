import streamlit as st

from modules.data_utils import get_spec_for_measured_ctq
from modules.statistics_analyzer import basic_statistics, normality_test
from modules.control_chart import create_imr_chart, create_xbar_r_chart
from modules.capability_analysis import process_capability_histogram
from modules.boxplot_trend import create_boxplot, trend_analysis
import numpy as np


def quality_analysis_page():
    """품질 분석 페이지 (Quality Analysis Page)"""
    st.header("📊 품질 분석")

    if 'transformed_data' not in st.session_state:
        st.warning("먼저 데이터를 업로드하고 변환해주세요.")
        return

    df = st.session_state.transformed_data

    ctq_options = df['관리번호'].unique().tolist()
    selected_ctq = st.selectbox("분석할 관리번호 선택", ctq_options)
    filtered_df = df[df['관리번호'] == selected_ctq]

    if filtered_df.empty:
        st.info("선택한 관리번호에 대한 데이터가 없습니다.")
        return

    filtered_spec = get_spec_for_measured_ctq()
    selected_spec = filtered_spec[filtered_spec['관리번호'] == selected_ctq]

    usl = selected_spec['USL'].values[0] if 'USL' in selected_spec.columns and not selected_spec['USL'].isnull().all() else None
    lsl = selected_spec['LSL'].values[0] if 'LSL' in selected_spec.columns and not selected_spec['LSL'].isnull().all() else None
    target = selected_spec['Target'].values[0] if 'Target' in selected_spec.columns and not selected_spec['Target'].isnull().all() else None

    st.write(f"🔍 선택한 CTQ: **{selected_ctq}**")
    st.write(f"데이터 수: {len(filtered_df)}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "기본 통계",
        "관리도",
        "공정능력 분석",
        "박스플롯 및 추세 분석"
    ])

    with tab1:
        st.subheader("📌 기본 통계 분석")
        stats_df = basic_statistics(filtered_df[['측정값']])
        st.dataframe(stats_df)

        st.subheader("📈 정규성 검정")
        normal_df = normality_test(filtered_df[['측정값']])
        st.dataframe(normal_df)

    with tab2:
        st.subheader("📉 I-MR 관리도")
        imr_x = filtered_df['측정일자'].tolist() if '측정일자' in filtered_df.columns else list(range(len(filtered_df)))
        fig, imr_summary = create_imr_chart(filtered_df['측정값'].to_numpy(), x=imr_x, return_summary=True, show_outliers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**관리도 요약 결과**")
        st.dataframe(imr_summary)

        st.subheader("📏 X-bar & R 관리도")
        group_size = st.number_input("샘플 크기 (X-bar 관리도용)", min_value=2, max_value=20, value=5)
        values = filtered_df['측정값'].to_numpy()
        num_groups = len(values) // group_size

        if num_groups < 2:
            st.warning("X-bar 관리도를 그리려면 최소 2개 이상의 샘플 그룹이 필요합니다.")
        else:
            grouped_data = values[:num_groups * group_size].reshape(num_groups, group_size)
            group_dates = (
                filtered_df['측정일자'].iloc[:num_groups * group_size]
                .groupby(np.arange(num_groups * group_size) // group_size)
                .first().tolist()
                if '측정일자' in filtered_df.columns else list(range(num_groups))
            )
            xbar_fig, r_fig, xbar_summary, r_summary = create_xbar_r_chart(grouped_data, group_size, x=group_dates, return_summary=True, show_outliers=True)
            st.plotly_chart(xbar_fig, use_container_width=True)
            st.markdown("**X-bar 요약 결과**")
            st.dataframe(xbar_summary)
            st.plotly_chart(r_fig, use_container_width=True)
            st.markdown("**R 요약 결과**")
            st.dataframe(r_summary)

    with tab3:
        st.subheader("🏭 공정능력 분석")
        if usl is not None and lsl is not None and target is not None:
            cap_fig, cap_indices = process_capability_histogram(filtered_df['측정값'].to_numpy(), usl, lsl, target)
            st.plotly_chart(cap_fig, use_container_width=True)
            st.json(cap_indices)
        else:
            st.warning("USL, LSL 또는 Target 값이 누락되어 공정능력 분석을 수행할 수 없습니다.")

    with tab4:
        st.subheader("📦 박스플롯 분석")
        fig = create_boxplot(filtered_df[['측정값']])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 추세 분석")
        if '측정일자' in filtered_df.columns:
            trend_fig = trend_analysis(filtered_df, '측정일자', ['측정값'])
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.warning("추세 분석을 위한 '측정일자' 컬럼이 없습니다.")
