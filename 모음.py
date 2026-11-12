import streamlit as st
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# 엑셀 파일 위치
BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "20260828_음식DB_19617건.xlsx"

# 예측할 대상과 영양 성분
TARGET = "식품대분류명"

FEATURES = [
    "에너지(kcal)",
    "단백질(g)",
    "나트륨(mg)",
    "당류(g)",
    "포화지방산(g)"
]


# 엑셀 데이터 불러오기
@st.cache_data
def load_data():
    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"엑셀 파일을 찾을 수 없습니다: {FILE_PATH.name}"
        )

    return pd.read_excel(FILE_PATH)


# AI 학습에 사용할 데이터 정리
@st.cache_data
def prepare_data():
    df = load_data()

    required_columns = FEATURES + [TARGET]
    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"엑셀에 필요한 열이 없습니다: {missing_columns}"
        )

    data = df[required_columns].copy()

    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna()

    # 데이터가 너무 적은 식품 유형은 제외
    counts = data[TARGET].value_counts()
    valid_categories = counts[counts >= 10].index
    data = data[data[TARGET].isin(valid_categories)]

    if data[TARGET].nunique() < 2:
        raise ValueError("AI 학습에 필요한 식품 유형이 부족합니다.")

    return data


# AI 모델 학습 및 정확도 계산
@st.cache_resource
def get_model():
    data = prepare_data()

    X = data[FEATURES]
    y = data[TARGET]

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

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy
