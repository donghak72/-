import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

DATA_FILE = "mood_data_web.json"

st.set_page_config(page_title="감정 트래커", page_icon="😊")
st.title("😊 나의 감정 트래커")

# 데이터 로드/저장 함수
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

data = load_data()

# 기분 선택 및 입력
mood_options = {
    "매우 좋음 😊": 5,
    "좋음 🙂": 4,
    "보통 😐": 3,
    "나쁨 🙁": 2,
    "매우 나쁨 😫": 1
}

selected_mood = st.radio("지금 이 순간의 기분은 어떠신가요?", list(mood_options.keys()), index=2)

if st.button("현재 기분 기록하기"):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    data[now_str] = {
        "mood": selected_mood,
        "score": mood_options[selected_mood]
    }
    save_data(data)
    st.success(f"[{now_str}] 기분이 기록되었습니다!")

# 최근 15분 데이터 시각화
st.subheader("📈 최근 15분간의 감정 변화")
now = datetime.now()
chart_data = []

for i in range(14, -1, -1):
    target_time = now - timedelta(minutes=i)
    time_key = target_time.strftime("%Y-%m-%d %H:%M")
    display_time = target_time.strftime("%H:%M")
    
    score = data[time_key]["score"] if time_key in data else None
    chart_data.append({"시간": display_time, "점수": score})

df = pd.DataFrame(chart_data).set_index("시간")
st.line_chart(df)
