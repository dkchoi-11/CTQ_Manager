import streamlit as st

from modules.data_utils import get_spec_for_measured_ctq
from modules.statistics_analyzer import basic_statistics, normality_test
from modules.control_chart import create_imr_chart, create_xbar_r_chart
from modules.capability_analysis import process_capability_histogram
from modules.boxplot_trend import create_boxplot, trend_analysis
import numpy as np


def quality_analysis_page():
    """품질 분석 페이지 (Quality Analysis Page)"""
    st.header("📊 Quality Analysis")

    if st.session_state.transformed_data is None or st.session_state.transformed_data.empty:
        st.warning("Please upload and convert the data first.")
        return

    df = st.session_state.transformed_data

    ctq_options = df['관리번호'].unique().tolist()
    selected_ctq = st.selectbox("Select an management number to analyze", ctq_options)
    filtered_df = df[df['관리번호'] == selected_ctq]

    if filtered_df.empty:
        st.info("There is no data for the selected management number.")
        return

    filtered_spec = get_spec_for_measured_ctq()
    selected_spec = filtered_spec[filtered_spec['관리번호'] == selected_ctq]

    usl = selected_spec['USL'].values[0] if 'USL' in selected_spec.columns and not selected_spec['USL'].isnull().all() else None
    lsl = selected_spec['LSL'].values[0] if 'LSL' in selected_spec.columns and not selected_spec['LSL'].isnull().all() else None
    target = selected_spec['Target'].values[0] if 'Target' in selected_spec.columns and not selected_spec['Target'].isnull().all() else None

    st.write(f"🔍 Selected CTQ: **{selected_ctq}**")
    st.write(f"Number of data: {len(filtered_df)}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "basic statistics",
        "control chart",
        "Process capability analysis",
        "boxplot and trend analysis"
    ])

    with tab1:
        st.subheader("📌 Basic Statistical Analysis")
        stats_df = basic_statistics(filtered_df[['측정값']])
        st.dataframe(stats_df)

        st.subheader("📈 normality test")
        normal_df = normality_test(filtered_df[['측정값']])
        st.dataframe(normal_df)

    with tab2:
        st.subheader("📉 I-MR control chart")
        imr_x = filtered_df['측정일자'].tolist() if '측정일자' in filtered_df.columns else list(range(len(filtered_df)))
        fig, imr_summary = create_imr_chart(filtered_df['측정값'].to_numpy(), x=imr_x, return_summary=True, show_outliers=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Chart Summary Results**")
        st.dataframe(imr_summary)

        st.subheader("📏 X-bar & R control chart")
        group_size = st.number_input("샘플 크기 (X-bar 관리도용)", min_value=2, max_value=20, value=5)
        values = filtered_df['측정값'].to_numpy()
        num_groups = len(values) // group_size

        if num_groups < 2:
            st.warning("At least two sample groups are required to draw an X-bar chart.")
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
            st.markdown("**X-bar Summary Results**")
            st.dataframe(xbar_summary)
            st.plotly_chart(r_fig, use_container_width=True)
            st.markdown("**R Summary Results**")
            st.dataframe(r_summary)

    with tab3:
        st.subheader("🏭 Process capability analysis")
        if usl is not None and lsl is not None and target is not None:
            cap_fig, cap_indices = process_capability_histogram(filtered_df['측정값'].to_numpy(), usl, lsl)
            st.plotly_chart(cap_fig, use_container_width=True)
            st.json(cap_indices)
        else:
            st.warning("USL, LSL, or Target values are missing and capability analysis cannot be performed.")

    with tab4:
        st.subheader("📦 box plot analysis")
        fig = create_boxplot(filtered_df[['측정값']])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("📈 Trend Analysis")
        if '측정일자' in filtered_df.columns:
            trend_fig = trend_analysis(filtered_df, '측정일자', ['측정값'])
            st.plotly_chart(trend_fig, use_container_width=True)
        else:
            st.warning("There is no 'Measurement Date' column for trend analysis.")
