
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="식품 영양성분 분류", page_icon="🍎")

st.title("🍎 식품 영양성분 유형 분류")
st.write("영양성분을 입력하면 식품 유형을 예측합니다.")

uploaded_file = st.file_uploader("음식 DB 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    st.write("전체 데이터 수:", len(df))

    st.subheader("모델 학습")

    target = "식품대분류명"

    features = [
        "에너지(kcal)",
        "단백질(g)",
        "나트륨(mg)",
        "당류(g)",
        "포화지방산(g)"
    ]

    if target not in df.columns or not all(c in df.columns for c in features):
        st.error("엑셀의 열 이름이 코드와 일치하지 않습니다.")
        st.write("실제 열 이름:", df.columns.tolist())

    else:
        data = df[features + [target]].copy()

        for col in features:
            data[col] = pd.to_numeric(data[col], errors="coerce")

        data = data.dropna()

        # 데이터가 너무 적은 분류 제거
        counts = data[target].value_counts()
        valid = counts[counts >= 10].index
        data = data[data[target].isin(valid)]

        if data[target].nunique() < 2:
            st.error("학습할 식품 유형이 2개 이상 필요합니다.")
        else:
            X = data[features]
            y = data[target]

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2,
                random_state=42, stratify=y
            )

            model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight="balanced"
            )

            model.fit(X_train, y_train)

            predictions = model.predict(X_test)
            accuracy = accuracy_score(y_test, predictions)

            st.success("모델 학습 완료!")
            st.metric("모델 정확도", f"{accuracy * 100:.2f}%")

            st.subheader("식품 유형 예측")

            values = []
            for col in features:
                values.append(
                    st.number_input(
                        col,
                        min_value=0.0,
                        value=10.0
                    )
                )

            if st.button("식품 유형 예측하기"):
                result = model.predict(
                    pd.DataFrame([values], columns=features)
                )

                st.success(f"예측된 식품 유형: {result[0]}")

            st.subheader("식품 유형별 데이터 수")
            st.bar_chart(data[target].value_counts())

else:
    st.info("먼저 음식 DB 엑셀 파일을 업로드해 주세요.")
