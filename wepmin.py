import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

# 1. 한글 폰트 및 마이너스 깨짐 방지
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="감정 트래커", page_icon="😊")
st.title("😊 나의 감정 트래커")

# 2. 한국 시간(KST, UTC+9) 설정 함수
def get_kst_now():
    return datetime.now(timezone(timedelta(hours=9)))

# 3. Streamlit 세션 상태(st.session_state)를 활용한 데이터 유지
if "mood_data" not in st.session_state:
    st.session_state.mood_data = {}

# 4. 감정 점수 매핑
mood_options = {
    "매우 좋음 😊": 5,
    "좋음 🙂": 4,
    "보통 😐": 3,
    "나쁨 🙁": 2,
    "매우 나쁨 😫": 1
}

# UI 부분
selected_mood = st.radio("지금 이 순간의 기분은 어떠신가요?", list(mood_options.keys()), index=2)

if st.button("현재 기분 기록하기"):
    now_kst = get_kst_now()
    now_str = now_kst.strftime("%Y-%m-%d %H:%M")
    
    # 세션 데이터에 저장
    st.session_state.mood_data[now_str] = {
        "mood": selected_mood,
        "score": mood_options[selected_mood]
    }
    st.success(f"[{now_kst.strftime('%H:%M')}] 기분이 성공적으로 기록되었습니다!")

# 5. 그래프 영역 생성
st.subheader("📈 최근 15분간의 감정 변화")

now_kst = get_kst_now()
times = []
scores = []

# 최근 15분간 데이터 수집
for i in range(14, -1, -1):
    target_time = now_kst - timedelta(minutes=i)
    time_key = target_time.strftime("%Y-%m-%d %H:%M")
    display_time = target_time.strftime("%H:%M")
    
    times.append(display_time)
    if time_key in st.session_state.mood_data:
        scores.append(st.session_state.mood_data[time_key]["score"])
    else:
        scores.append(None)

# Matplotlib를 이용해 직관적으로 그래프 그리기
fig, ax = plt.subplots(figsize=(7, 3.5), dpi=100)

ax.plot(times, scores, color='#6C5CE7', marker='o', linewidth=2, markersize=6)
ax.set_ylim(0.5, 5.5)
ax.set_yticks([1, 2, 3, 4, 5])
ax.set_yticklabels(["매우 나쁨", "나쁨", "보통", "좋음", "매우 좋음"])
ax.grid(True, linestyle='--', alpha=0.5)
plt.xticks(rotation=45, fontsize=8)
fig.tight_layout()

# Streamlit 화면에 그래프 출력
st.pyplot(fig)
