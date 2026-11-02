"""기존 WordApp pages/01🐱_Wordlist.py 대체용.
설치: pip install streamlit pandas gTTS
실행: streamlit run HOME.py
"""
import html
from io import BytesIO

import pandas as pd
import streamlit as st

st.set_page_config(page_title="나만의 단어장 만들기", page_icon="🐱", layout="centered")

st.markdown("""
<style>
.stApp {background:radial-gradient(circle at top left,#fff2f7 0%,transparent 28%),radial-gradient(circle at top right,#eef8ff 0%,transparent 28%),linear-gradient(180deg,#fffdfd,#f6fbf8)}
.block-container {max-width:850px;padding-top:1.5rem;padding-bottom:4rem}
.main-title {text-align:center;font-size:2.3rem;font-weight:900;color:#344054}
.subtitle {text-align:center;color:#7a8498;margin-bottom:1.5rem}
.guide-box {background:white;border:1px solid #ebeef3;border-radius:20px;padding:18px;text-align:center;color:#667085;line-height:1.8;margin:15px 0 22px}
.word-card {background:white;border:2px solid #f0e8ff;border-radius:28px;padding:28px;text-align:center;margin:18px 0;box-shadow:0 10px 25px rgba(70,60,100,.06)}
.word-number {font-size:.85rem;font-weight:800;color:#a59ab8}
.question {font-size:1.15rem;font-weight:800;color:#344054;text-align:center;margin:20px 0}
div.stButton > button {border-radius:17px;min-height:50px;font-weight:750}
</style>
""", unsafe_allow_html=True)

CSV_PATH = "data/wordlist_1001.csv"
LEARNING_PAGE = "pages/03🎀_Word_Learning_APP.py"

@st.cache_data
def load_words():
    data = pd.read_csv(CSV_PATH, dtype={"word_id": str}).fillna("")
    required = ["word_id", "unit", "word", "meaning", "example", "pronunciation_caution"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError(f"CSV에 필요한 열이 없습니다: {', '.join(missing)}")
    data["word_id"] = data["word_id"].astype(str)
    if data["word_id"].duplicated().any():
        raise ValueError("word_id는 모든 단어에서 고유해야 합니다.")
    return data

@st.cache_data(show_spinner=False)
def word_audio(word):
    # Streamlit 자체 오디오 컨트롤을 사용하므로 iframe/HTML 클릭 문제가 없음.
    from gtts import gTTS
    out = BytesIO()
    gTTS(text=str(word), lang="en", tld="com").write_to_fp(out)
    return out.getvalue()

try:
    df = load_words()
except Exception as exc:
    st.error("단어 CSV를 읽지 못했습니다.")
    st.code(str(exc))
    st.stop()

# 기존 학습 페이지와 호환되는 상태 변수 유지
for key in ("word_positions", "saved_words", "discarded_words", "word_history", "self_assessments"):
    if key not in st.session_state:
        st.session_state[key] = {}
if "selected_unit" not in st.session_state:
    st.session_state.selected_unit = None

preferred = ["Unit 4", "Unit 5", "Unit 6", "Unit 7", "Special Reading 1", "Special Reading 2"]
available = df["unit"].astype(str).unique().tolist()
units = [u for u in preferred if u in available] + [u for u in available if u not in preferred]
mascots = {"Unit 4": "🐰", "Unit 5": "🐱", "Unit 6": "🐻", "Unit 7": "🐶", "Special Reading 1": "🐹", "Special Reading 2": "🦊"}

st.markdown('<div style="text-align:center;font-size:3.5rem">🐾</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🐱 나만의 단어장 만들기</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">소리를 듣고 내가 아는 단어인지 확인해 봐요!</div>', unsafe_allow_html=True)

if st.session_state.selected_unit is None:
    st.markdown('<div class="guide-box">🪨 돌다리를 골라 단원을 선택하세요.<br>단어의 <b>소리만 듣고</b> 뜻을 아는지 판단해요.</div>', unsafe_allow_html=True)
    for i, unit_name in enumerate(units):
        unit_data = df[df["unit"].astype(str) == unit_name]
        done = len(st.session_state.self_assessments.get(unit_name, {}))
        left, center, right = st.columns([0.3, 2.4, 1.1] if i % 2 == 0 else [1.1, 2.4, 0.3])
        with center:
            if st.button(f"🪨 {mascots.get(unit_name, '🐾')} {unit_name}\n\n{done}/{len(unit_data)}개 확인", key=f"unit_{unit_name}", use_container_width=True):
                st.session_state.selected_unit = unit_name
                st.session_state.word_positions.setdefault(unit_name, 0)
                st.session_state.saved_words.setdefault(unit_name, [])
                st.session_state.discarded_words.setdefault(unit_name, [])
                st.session_state.word_history.setdefault(unit_name, [])
                st.session_state.self_assessments.setdefault(unit_name, {})
                st.rerun()
    st.stop()

unit = st.session_state.selected_unit
unit_df = df[df["unit"].astype(str) == unit].reset_index(drop=True)
if unit_df.empty:
    st.warning("이 단원에는 단어가 없습니다.")
    st.stop()

saved = st.session_state.saved_words.setdefault(unit, [])
discarded = st.session_state.discarded_words.setdefault(unit, [])
history = st.session_state.word_history.setdefault(unit, [])
ratings = st.session_state.self_assessments.setdefault(unit, {})
position = st.session_state.word_positions.setdefault(unit, 0)

nav_left, nav_mid, nav_right = st.columns([1, 2.3, 1])
with nav_left:
    if st.button("← Unit", use_container_width=True):
        st.session_state.selected_unit = None
        st.rerun()
with nav_mid:
    st.markdown(f"<div style='text-align:center;font-weight:800;padding:10px'>{mascots.get(unit, '🐾')} {html.escape(unit)}</div>", unsafe_allow_html=True)
with nav_right:
    st.caption(f"📦 {len(saved)}개")

if position >= len(unit_df):
    st.progress(1.0)
    st.success(f"🎉 {unit} 자기평가 완료! {len(unit_df)}개 단어를 확인했어요.")
    st.write(f"🤔 잘 모르겠어요: **{len(saved)}개** · 😊 뜻을 알아요: **{len(discarded)}개**")
    if saved:
        st.markdown("### 📦 나의 학습 단어")
        # 자기평가가 끝난 뒤에만 철자와 뜻을 공개
        for _, item in unit_df[unit_df["word_id"].isin(saved)].iterrows():
            st.write(f"🐾 **{item['word']}** — {item['meaning']}")
    else:
        st.info("모든 단어를 안다고 선택했어요. 형성평가에서는 전체 단어를 확인하게 됩니다.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 다시 평가하기", use_container_width=True):
            st.session_state.word_positions[unit] = 0
            st.session_state.saved_words[unit] = []
            st.session_state.discarded_words[unit] = []
            st.session_state.word_history[unit] = []
            st.session_state.self_assessments[unit] = {}
            st.rerun()
    with col2:
        if st.button("🎧 학습하러 가기 →", type="primary", use_container_width=True, disabled=not bool(saved)):
            st.session_state.learning_unit = unit
            try:
                st.switch_page(LEARNING_PAGE)
            except Exception as exc:
                st.error("학습 페이지 경로를 확인해 주세요.")
                st.code(str(exc))
    st.caption("※ 현재 선택은 브라우저 세션에만 저장됩니다. 연구용 영구 저장 기능은 추후 연결해야 합니다.")
    st.stop()

row = unit_df.iloc[position]
word_id = str(row["word_id"])
word = str(row["word"])
st.progress(position / len(unit_df))
st.caption(f"🌱 {position + 1} / {len(unit_df)}번째 단어")
st.markdown(f'<div class="word-card"><div class="word-number">WORD {position + 1}</div><div style="font-size:3rem;margin:10px">🎧</div><div style="color:#667085">아래 ▶ 버튼을 눌러 들어 보세요.</div></div>', unsafe_allow_html=True)

try:
    audio = word_audio(word)
    st.audio(audio, format="audio/mp3")
except Exception as exc:
    st.error("음성을 만들지 못했습니다. requirements.txt의 gTTS 설치 및 서버 인터넷 연결을 확인해 주세요.")
    st.caption(f"오류 정보: {exc}")
    st.stop()  # 음성이 없으면 듣기 기반 자기평가를 진행하지 않음

st.markdown('<div class="question">🐾 들은 단어의 뜻을 알고 있나요?</div>', unsafe_allow_html=True)

def record_choice(choice):
    ratings[word_id] = choice
    if choice == "unknown":
        if word_id not in saved:
            saved.append(word_id)
        if word_id in discarded:
            discarded.remove(word_id)
    else:
        if word_id not in discarded:
            discarded.append(word_id)
        if word_id in saved:
            saved.remove(word_id)
    history.append({"word_id": word_id, "action": choice})
    st.session_state.word_positions[unit] += 1
    st.rerun()

left, right = st.columns(2)
with left:
    if st.button("😊 뜻을 알아요", type="primary", use_container_width=True):
        record_choice("known")
with right:
    if st.button("🤔 잘 모르겠어요", use_container_width=True):
        record_choice("unknown")

if history:
    if st.button("↩️ 이전 선택 취소", use_container_width=True):
        previous = history.pop()
        previous_id = previous["word_id"]
        ratings.pop(previous_id, None)
        if previous_id in saved:
            saved.remove(previous_id)
        if previous_id in discarded:
            discarded.remove(previous_id)
        st.session_state.word_positions[unit] = max(0, position - 1)
        st.rerun()

st.divider()
st.caption(f"🤔 모르는 단어 {len(saved)}개 · 😊 아는 단어 {len(discarded)}개")
