import streamlit as st
from 모음 import FEATURES, prepare_data

st.set_page_config(page_title="영양 성분 분석", page_icon="📊")

st.title("📊 영양 성분 분석")
st.write("식품 유형에 따라 영양 성분이 어떻게 다른지 분석합니다.")

try:
    data = prepare_data()

    selected_feature = st.selectbox(
        "분석할 영양 성분을 선택하세요.",
        FEATURES
    )

    average_data = (
        data.groupby("식품대분류명")[selected_feature]
        .mean()
        .sort_values(ascending=False)
    )

    st.subheader(f"식품 유형별 평균 {selected_feature}")

    st.bar_chart(average_data)

    st.subheader("평균 영양 성분 표")

    average_table = (
        data.groupby("식품대분류명")[FEATURES]
        .mean()
        .round(2)
    )

    st.dataframe(average_table, use_container_width=True)

    st.subheader("식품 유형별 데이터 개수")

    category_counts = data["식품대분류명"].value_counts()

    st.bar_chart(category_counts)

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
