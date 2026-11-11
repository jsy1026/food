
import streamlit as st

from utils import load_data, prepare_data, get_model

st.set_page_config(
    page_title="식품 영양성분 분석",
    page_icon="🍎",
    layout="wide"
)

st.title("🍎 식품 영양성분 분석 시스템")

st.write(
    "식품의 영양성분 데이터를 분석하고 "
    "인공지능을 활용하여 식품 유형을 예측하는 프로그램입니다."
)

try:
    df = load_data()
    data = prepare_data()
    model, accuracy = get_model()

    st.success("데이터 및 인공지능 모델 준비 완료!")

    # 핵심 통계
    col1, col2, col3 = st.columns(3)

    col1.metric("전체 데이터", f"{len(df):,}건")
    col2.metric("식품 유형", f"{data['식품대분류명'].nunique()}종")
    col3.metric("모델 정확도", f"{accuracy * 100:.2f}%")

    st.divider()

    st.header("📌 프로젝트 소개")

    st.write("""
    이 프로젝트는 식품 영양성분 데이터를 활용하여
    식품의 유형을 분류하고 영양성분을 비교 분석하는 것을 목표로 합니다.
    """)

    st.subheader("주요 기능")

    col1, col2 = st.columns(2)

    with col1:
        st.info("🔍 식품 유형 예측\n\n영양성분을 입력하여 AI 예측 결과 확인")

        st.info("📊 영양성분 분석\n\n식품 유형별 평균 영양성분 비교")

    with col2:
        st.info("📁 데이터 탐색\n\n식품 데이터 검색 및 상세 정보 확인")

        st.info("🤖 인공지능 분석\n\n랜덤 포레스트 분류 모델 활용")

    st.divider()

    st.caption(
        "분류 모델: Random Forest | "
        "데이터 출처: 식품영양성분 데이터베이스"
    )

except Exception as e:
    st.error(f"프로그램 실행 오류: {e}")
