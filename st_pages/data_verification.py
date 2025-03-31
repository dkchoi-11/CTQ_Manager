import pandas as pd
import streamlit as st
import io
import numpy as np

# 모듈 import
from modules.data_utils import get_spec_from_master, verify_data, get_spec_for_measured_ctq


def data_verification_page():
    """이상 데이터 검증 페이지 (Anomaly Data Verification Page)"""
    st.header("이상 데이터 검증")

    # 변환된 데이터 확인
    if 'transformed_data' not in st.session_state:
        st.warning("먼저 데이터를 업로드하고 변환해주세요.")
        return

    try:
        df = st.session_state.transformed_data

        # 데이터프레임이 비어있는지 확인
        if df.empty:
            st.warning("변환된 데이터가 비어 있습니다. 유효한 데이터를 업로드해주세요.")
            return

        # 이상치 탐지 방법 선택
        method = st.selectbox("이상치 탐지 방법 선택",
                              ['규격 한계', 'IQR 방법', 'Z-점수'])

        st.subheader("📋 관리번호별 스펙 정보 (USL, LSL, Target, UCL, LCL)")

        try:
            spec_df = get_spec_for_measured_ctq()
            if not spec_df.empty:
                st.dataframe(spec_df)
            else:
                st.info("스펙 정보를 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"스펙 정보를 불러오는 중 오류가 발생했습니다: {str(e)}")
            return

        # 이상치 탐지 옵션
        if method == '규격 한계':
            try:
                verify_result_df = verify_data()

                st.subheader("📊 스펙 초과 검출 결과")
                st.write(f"총 데이터 수: {len(df)}")

                if verify_result_df is None:
                    st.warning("스펙 검증 결과를 가져올 수 없습니다.")
                    return

                st.write(f"스펙 초과된 데이터 수: {len(verify_result_df)}")

                if verify_result_df.empty:
                    st.success("✅ 스펙 초과된 데이터 없음")
                else:
                    st.error("❗스펙 초과된 데이터가 존재합니다.")
                    st.dataframe(verify_result_df)

                    # 엑셀로 다운로드 버튼 추가
                    try:
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            verify_result_df.to_excel(writer, index=False, sheet_name='Spec Over Data')

                        st.download_button(
                            label="📥 스펙 초과 데이터 Excel 다운로드",
                            data=output.getvalue(),
                            file_name="spec_over_data.xlsx",
                            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                        )
                    except Exception as e:
                        st.error(f"엑셀 파일 생성 중 오류가 발생했습니다: {str(e)}")
            except Exception as e:
                st.error(f"데이터 검증 중 오류가 발생했습니다: {str(e)}")

        elif method == 'IQR 방법':
            st.info("IQR 방법 구현 예정입니다.")
            # 여기에 IQR 방법 구현

        elif method == 'Z-점수':
            st.info("Z-점수 방법 구현 예정입니다.")
            # 여기에 Z-점수 방법 구현

    except Exception as e:
        st.error(f"예상치 못한 오류가 발생했습니다: {str(e)}")