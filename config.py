"""
프로젝트 전역 설정 및 임계값 정의 모듈
"""

# 품질 관리 임계값 설정
QUALITY_SETTINGS = {
    'USL': 10.5,  # Upper Specification Limit
    'LSL': 9.5,   # Lower Specification Limit
    'UCL': 11.0,  # Upper Control Limit
    'LCL': 9.0,   # Lower Control Limit
}

# 분석 옵션
ANALYSIS_OPTIONS = {
    'control_chart_types': ['i-MR', 'Xbar-R', 'Xbar-S'],
    'capability_indices': ['Cp', 'Cpk', 'Pp', 'Ppk'],
}

# 데이터 변환 설정
DATA_TRANSFORM_CONFIG = {
    'decimal_places': 3,
    'allowed_extensions': ['.xlsx', '.xls', '.csv'],
    'max_file_size_mb': 50
}

# 통계 분석 기본 설정
STAT_ANALYSIS_CONFIG = {
    'confidence_level': 0.95,
    'normality_test_alpha': 0.05
}