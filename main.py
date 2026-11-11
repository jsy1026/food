
import streamlit as st
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 페이지 설정
st.set_page_config(
    page_title="식품 영양성분 분류",
    page_icon="🍎"
)

# 제목
st.title("🍎 식품 영양성분 유형 분류")
st.write("영양성분을 입력하면 식품 유형을 예측합니다.")

# 1. 엑셀 파일 자동 불러오기
file_path = Path(__file__).parent / "20260828_음식DB_19617건.xlsx"

if not file_path.exists():
    st.error("음식 DB 파일을 찾을 수 없습니다.")
    st.write("GitHub에 엑셀 파일이 있는지 확인해 주세요.")
    st.stop()

try:
    df = pd.read_excel(file_path)
    st.success("식품 데이터 자동 불러오기 완료!")

except Exception as e:
    st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {e}")
    st.stop()

# 2. 데이터 미리보기
st.subheader("📋 데이터 미리보기")
st.dataframe(df.head())

st.write("전체 데이터 수:", len(df))

# 3. 모델 학습 준비
st.subheader("🤖 모델 학습")

target = "식품대분류명"

features = [
    "에너지(kcal)",
    "단백질(g)",
    "나트륨(mg)",
    "당류(g)",
    "포화지방산(g)"
]

# 필요한 열이 있는지 확인
if target not in df.columns or not all(c in df.columns for c in features):
    st.error("엑셀의 열 이름이 코드와 일치하지 않습니다.")
    st.write("실제 열 이름:", df.columns.tolist())
    st.stop()

# 4. 데이터 전처리
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
    st.stop()

# 5. 인공지능 모델 학습
X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# 6. 모델 정확도 평가
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

st.success("모델 학습 완료!")
st.metric("모델 정확도", f"{accuracy * 100:.2f}%")

# 7. 식품 유형 예측
st.subheader("🔍 식품 유형 예측")

st.write("영양성분 수치를 입력해 보세요.")

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
    input_data = pd.DataFrame(
        [values],
        columns=features
    )

    result = model.predict(input_data)

    st.success(f"예측된 식품 유형: {result[0]}")

# 8. 식품 유형별 데이터 수 그래프
st.subheader("📊 식품 유형별 데이터 수")

type_counts = data[target].value_counts()

st.bar_chart(type_counts)

# 9. 식품 유형별 평균 영양성분 분석
st.subheader("📈 식품 유형별 평균 영양성분")

average_data = data.groupby(target)[features].mean()

st.dataframe(average_data.round(2))

for col in features:
    st.write(f"**{col} 평균 비교**")
    st.bar_chart(average_data[col])
