import streamlit as st

# 세션 상태 키 정의
SESSION_KEYS = {
    'UPLOADED_DATA': 'uploaded_data',
    'TRANSFORMED_DATA': 'transformed_data',
    'ANALYSIS_RESULTS': 'analysis_results',
    'CONFIG_SETTINGS': 'config_settings'
}

def initialize_session_state():
    """
    Streamlit 세션 상태를 초기화하는 함수
    
    모든 주요 세션 상태 변수를 초기 상태로 설정
    """
    # 업로드된 원본 데이터
    if SESSION_KEYS['UPLOADED_DATA'] not in st.session_state:
        st.session_state[SESSION_KEYS['UPLOADED_DATA']] = None
    
    # 변환된 데이터
    if SESSION_KEYS['TRANSFORMED_DATA'] not in st.session_state:
        st.session_state[SESSION_KEYS['TRANSFORMED_DATA']] = None
    
    # 분석 결과
    if SESSION_KEYS['ANALYSIS_RESULTS'] not in st.session_state:
        st.session_state[SESSION_KEYS['ANALYSIS_RESULTS']] = {}
    
    # 설정값
    if SESSION_KEYS['CONFIG_SETTINGS'] not in st.session_state:
        st.session_state[SESSION_KEYS['CONFIG_SETTINGS']] = {
            'USL': None,  # Upper Specification Limit
            'LSL': None,  # Lower Specification Limit
            'UCL': None,  # Upper Control Limit
            'LCL': None   # Lower Control Limit
        }

def reset_session_state():
    """
    모든 세션 상태를 완전히 초기화하는 함수
    
    주의: 모든 저장된 데이터와 분석 결과를 제거함
    """
    # 모든 세션 상태 키 초기화
    for key in SESSION_KEYS.values():
        if key in st.session_state:
            st.session_state[key] = None
    
    # 세션 상태 재초기화
    initialize_session_state()
    
    # 사용자에게 초기화 완료 알림
    st.success("모든 세션 데이터가 초기화되었습니다.")

def update_session_data(key, value):
    """
    특정 세션 상태 값을 업데이트하는 함수
    
    매개변수:
    - key (str): 업데이트할 세션 상태의 키
    - value: 업데이트할 값
    """
    if key in SESSION_KEYS.values():
        st.session_state[key] = value
    else:
        st.warning(f"유효하지 않은 세션 키: {key}")

def get_session_data(key, default=None):
    """
    특정 세션 상태 값을 가져오는 함수
    
    매개변수:
    - key (str): 가져올 세션 상태의 키
    - default: 키가 존재하지 않을 경우 반환할 기본값
    
    반환값:
    - 세션 상태 값 또는 기본값
    """
    return st.session_state.get(key, default)

def display_session_reset_button():
    """
    세션 초기화 버튼을 표시하는 함수
    
    사이드바에 세션 초기화 버튼 생성
    """
    if st.sidebar.button("🔄 세션 초기화", help="모든 데이터와 분석 결과를 초기화합니다."):
        reset_session_state()

def main():
    """
    세션 관리자 모듈 테스트용 메인 함수
    """
    st.title("세션 관리자 테스트")
    
    # 세션 상태 초기화
    initialize_session_state()
    
    # 세션 상태 정보 표시
    st.write("현재 세션 상태:")
    for key, value in SESSION_KEYS.items():
        st.write(f"{key}: {st.session_state.get(value, '초기화되지 않음')}")
    
    # 세션 초기화 버튼
    display_session_reset_button()

if __name__ == '__main__':
    main()