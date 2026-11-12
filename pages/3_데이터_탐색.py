import streamlit as st

from 모음 import load_data

st.set_page_config(
    page_title="데이터 탐색",
    page_icon="📁"
)

st.title("📁 식품 데이터 탐색")
st.write("실제 식품 영양 성분 데이터의 내용을 확인합니다.")

try:
    df = load_data()

    col1, col2 = st.columns(2)

    col1.metric("전체 데이터 수", f"{len(df):,}개")
    col2.metric("전체 항목 수", f"{len(df.columns)}개")

    if "식품대분류명" in df.columns:
        categories = sorted(
            df["식품대분류명"].dropna().unique().tolist()
        )

        selected_category = st.selectbox(
            "확인할 식품 유형을 선택하세요.",
            ["전체"] + categories
        )

        if selected_category == "전체":
            filtered_data = df
        else:
            filtered_data = df[
                df["식품대분류명"] == selected_category
            ]
    else:
        filtered_data = df

    st.subheader("데이터 미리보기")
    st.write(f"검색된 데이터: {len(filtered_data):,}개")

    st.dataframe(
        filtered_data.head(200),
        use_container_width=True
    )

    csv_data = filtered_data.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="CSV 파일 다운로드",
        data=csv_data,
        file_name="food_data.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
