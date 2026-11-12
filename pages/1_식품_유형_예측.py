import streamlit as st
import pandas as pd

from 모음 import FEATURES, get_model

st.set_page_config(
    page_title="식품 유형 예측",
    page_icon="🔍"
)

st.title("🔍 식품 유형 예측")
st.write("영양 성분을 입력하면 AI가 식품 유형을 예측합니다.")

try:
    model, accuracy = get_model()

    st.caption(f"AI 모델 정확도: {accuracy * 100:.2f}%")

    st.subheader("영양 성분 입력")

    col1, col2 = st.columns(2)

    with col1:
        energy = st.number_input(
            "에너지(kcal)", min_value=0.0, value=100.0
        )
        protein = st.number_input(
            "단백질(g)", min_value=0.0, value=5.0
        )
        sodium = st.number_input(
            "나트륨(mg)", min_value=0.0, value=100.0
        )

    with col2:
        sugar = st.number_input(
            "당류(g)", min_value=0.0, value=5.0
        )
        saturated_fat = st.number_input(
            "포화지방산(g)", min_value=0.0, value=2.0
        )

    if st.button("식품 유형 예측하기", type="primary"):
        input_data = pd.DataFrame(
            [[energy, protein, sodium, sugar, saturated_fat]],
            columns=FEATURES
        )

        prediction = model.predict(input_data)[0]

        st.success(f"AI 예측 결과: **{prediction}**")

        probabilities = model.predict_proba(input_data)[0]

        result = pd.DataFrame({
            "식품 유형": model.classes_,
            "예측 확률": probabilities
        })

        result = result.sort_values(
            "예측 확률",
            ascending=False
        ).head(5)

        st.subheader("예측 결과 상위 5개")

        st.bar_chart(
            result.set_index("식품 유형")["예측 확률"]
        )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
