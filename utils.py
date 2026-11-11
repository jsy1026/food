
import streamlit as st
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 데이터 설정
BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "20260828_음식DB_19617건.xlsx"

TARGET = "식품대분류명"

FEATURES = [
    "에너지(kcal)",
    "단백질(g)",
    "나트륨(mg)",
    "당류(g)",
    "포화지방산(g)"
]


# 1. 엑셀 데이터 불러오기
@st.cache_data
def load_data():
    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"엑셀 파일을 찾을 수 없습니다: {FILE_PATH.name}"
        )

    return pd.read_excel(FILE_PATH)


# 2. 데이터 전처리
@st.cache_data
def prepare_data():
    df = load_data()

    required = FEATURES + [TARGET]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"필요한 열이 없습니다: {missing}")

    data = df[required].copy()

    for col in FEATURES:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    data = data.dropna()
    data = data[data[TARGET].notna()]

    # 데이터가 10개 미만인 식품 유형 제외
    counts = data[TARGET].value_counts()
    valid = counts[counts >= 10].index
    data = data[data[TARGET].isin(valid)].copy()

    if data[TARGET].nunique() < 2:
        raise ValueError("학습할 식품 유형이 2개 이상 필요합니다.")

    return data


# 3. 인공지능 모델 학습
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
