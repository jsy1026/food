import streamlit as st
from 모음 import load_data, prepare_data, get_model

st.set_page_config(
    page_title="식품 영양 성분 분석",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 식품 영양 성분 분석 프로그램")

st.write(
    "식품의 영양 성분 데이터를 이용하여 식품 유형을 예측하고 "
    "영양 정보를 분석하는 프로그램입니다."
)

st.divider()

try:
    df = load_data()
    data = prepare_data()
    model, accuracy = get_model()

    col1, col2, col3 = st.columns(3)

    col1.metric("전체 데이터 수", f"{len(df):,}개")
    col2.metric("분석 가능한 데이터", f"{len(data):,}개")
    col3.metric(
        "식품 유형 수",
        f"{data['식품대분류명'].nunique()}개"
    )

    st.subheader("🤖 AI 모델 성능")
    st.metric("모델 정확도", f"{accuracy * 100:.2f}%")

    st.info(
        "왼쪽 메뉴에서 식품 이름 검색, 식품 유형 예측, "
        "영양 성분 분석, 데이터 탐색 기능을 이용할 수 있습니다."
    )

    st.subheader("📌 프로젝트 주요 기능")

    st.markdown("""
    - **식품 이름 검색:** 식품 이름을 검색하여 영양 정보를 확인합니다.
    - **식품 유형 예측:** 영양 성분을 입력하면 AI가 식품 유형을 예측합니다.
    - **영양 성분 분석:** 식품 유형별 평균 영양 성분을 비교합니다.
    - **데이터 탐색:** 실제 식품 영양 성분 데이터를 확인합니다.
    """)

except Exception as e:
    st.error(f"프로그램을 불러오는 중 오류가 발생했습니다: {e}")
