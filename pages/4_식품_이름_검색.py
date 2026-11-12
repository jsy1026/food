import streamlit as st

from 모음 import load_data

st.set_page_config(
    page_title="식품 이름 검색",
    page_icon="🍎"
)

st.title("🍎 식품 이름 검색")
st.write("식품 이름을 검색하여 영양 성분 정보를 확인할 수 있습니다.")

try:
    df = load_data()

    # 식품 이름 열 확인
    if "식품명" not in df.columns:
        st.error("엑셀 파일에서 '식품명' 열을 찾을 수 없습니다.")
        st.stop()

    # 검색어 입력
    search_word = st.text_input(
        "검색할 식품 이름을 입력하세요.",
        placeholder="예: 불고기, 사과, 치킨"
    )

    if search_word.strip():

        # 식품 이름에 검색어가 포함된 데이터 찾기
        results = df[
            df["식품명"].astype(str).str.contains(
                search_word.strip(),
                case=False,
                na=False
            )
        ]

        st.subheader("검색 결과")
        st.write(f"총 {len(results):,}개의 식품을 찾았습니다.")

        if len(results) == 0:
            st.warning("검색 결과가 없습니다. 다른 이름으로 검색해 보세요.")

        else:
            # 검색 결과에서 식품 하나 선택
            food_names = results["식품명"].dropna().unique().tolist()

            selected_food = st.selectbox(
                "자세히 확인할 식품을 선택하세요.",
                food_names
            )

            # 선택한 식품의 정보 가져오기
            food_info = results[
                results["식품명"] == selected_food
            ].iloc[0]

            st.divider()

            st.subheader(f"🍽️ {selected_food}")

            if "식품대분류명" in df.columns:
                st.write(
                    f"식품 유형: {food_info['식품대분류명']}"
                )

            st.subheader("영양 성분 정보")

            nutrition_columns = [
                "에너지(kcal)",
                "단백질(g)",
                "나트륨(mg)",
                "당류(g)",
                "포화지방산(g)"
            ]

            col1, col2 = st.columns(2)

            for index, column in enumerate(nutrition_columns):
                if column in df.columns:
                    value = food_info[column]

                    if index % 2 == 0:
                        with col1:
                            st.metric(column, value)
                    else:
                        with col2:
                            st.metric(column, value)

            st.divider()

            st.subheader("검색된 식품 목록")

            st.dataframe(
                results,
                use_container_width=True
            )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
