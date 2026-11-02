import streamlit as st
import pandas as pd
import json
import html
import streamlit.components.v1 as components

st.set_page_config(page_title="나만의 단어장 만들기", page_icon="🐱", layout="centered")

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #fff2f7 0%, transparent 28%),
        radial-gradient(circle at top right, #eef8ff 0%, transparent 28%),
        linear-gradient(180deg, #fffdfd 0%, #f6fbf8 100%);
}

.block-container {
    max-width: 850px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

.main-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 900;
    color: #344054;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #7a8498;
    font-size: 1rem;
    margin-bottom: 1.8rem;
}

.mascot {
    text-align: center;
    font-size: 4rem;
    margin-bottom: 0px;
}

.guide-box {
    background: rgba(255,255,255,0.92);
    border-radius: 20px;
    padding: 17px 20px;
    margin-bottom: 24px;
    border: 1px solid #ebeef3;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
    text-align: center;
    color: #667085;
    line-height: 1.7;
}

.word-card {
    background: white;
    border-radius: 30px;
    padding: 35px 28px;
    text-align: center;
    border: 2px solid #f0e8ff;
    box-shadow: 0 13px 32px rgba(70, 60, 100, 0.08);
    margin-top: 18px;
    margin-bottom: 18px;
}

.word-number {
    color: #a59ab8;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.06rem;
    margin-bottom: 8px;
}

.word-main {
    font-size: 3rem;
    font-weight: 900;
    color: #303747;
    margin-bottom: 14px;
}

.word-meaning {
    font-size: 1.35rem;
    font-weight: 750;
    color: #554b64;
    background: #fff7fb;
    border: 1px solid #f7dfea;
    border-radius: 18px;
    padding: 13px;
    margin-top: 10px;
    margin-bottom: 18px;
}

.example-label {
    font-size: 0.8rem;
    font-weight: 800;
    color: #7d91ad;
    margin-bottom: 4px;
}

.example {
    font-size: 1.03rem;
    color: #475467;
    line-height: 1.7;
    background: #f5f9ff;
    border: 1px solid #ddeafb;
    border-radius: 18px;
    padding: 14px 17px;
}

.saved-box {
    background: #f3fff7;
    border: 1px solid #d3eadb;
    border-radius: 20px;
    padding: 17px;
    margin-top: 17px;
    margin-bottom: 17px;
    color: #405748;
    text-align: center;
}

.finish-card {
    background: white;
    border-radius: 30px;
    padding: 32px 25px;
    text-align: center;
    border: 2px solid #e8e2ff;
    box-shadow: 0 12px 30px rgba(70,60,100,0.08);
    margin-top: 20px;
}

.finish-emoji {
    font-size: 3.5rem;
    margin-bottom: 4px;
}

.finish-title {
    font-size: 1.8rem;
    font-weight: 900;
    color: #344054;
    margin-bottom: 10px;
}

.finish-text {
    color: #667085;
    font-size: 1.02rem;
    margin-top: 5px;
}

.finish-count {
    font-size: 1.22rem;
    color: #475467;
    margin-top: 16px;
    line-height: 1.8;
}

.unit-title {
    text-align: center;
    font-size: 1.25rem;
    font-weight: 850;
    color: #344054;
    padding-top: 10px;
}

.unit-count {
    text-align: center;
    padding-top: 11px;
    color: #667085;
    font-weight: 700;
}

.question-text {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 800;
    color: #344054;
    margin: 14px 0 16px 0;
}

div.stButton > button {
    border-radius: 17px;
    min-height: 52px;
    font-size: 1rem;
    font-weight: 800;
    border: 1px solid #d0d5dd;
    transition: 0.15s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}

</style>
""", unsafe_allow_html=True)

# 기존 CSV 형식을 그대로 사용합니다.
@st.cache_data
def load_words():
    df = pd.read_csv("data/wordlist_1001.csv", dtype={"word_id": str}).fillna("")
    required = ["word_id", "unit", "word", "meaning", "example", "pronunciation_caution"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"CSV에 다음 열이 없습니다: {missing}")
    if df["word_id"].duplicated().any():
        raise ValueError("word_id는 전체 CSV에서 중복되면 안 됩니다.")
    return df

try:
    df = load_words()
except Exception as e:
    st.error("단어 파일을 불러오지 못했어요.")
    st.code(str(e))
    st.stop()

# 기존 학습 페이지와의 호환성을 위해 saved_words/discarded_words 유지
for key, default in {
    "selected_unit": None,
    "word_positions": {},
    "saved_words": {},
    "discarded_words": {},
    "word_history": {},
    "self_assessments": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

preferred_order = ["Unit 4", "Unit 5", "Unit 6", "Unit 7", "Special Reading 1", "Special Reading 2"]
available_units = df["unit"].unique().tolist()
units = [u for u in preferred_order if u in available_units] + [u for u in available_units if u not in preferred_order]
unit_mascots = {"Unit 4": "🐰", "Unit 5": "🐱", "Unit 6": "🐻", "Unit 7": "🐶", "Special Reading 1": "🐹", "Special Reading 2": "🦊"}


def speak_button(word, unique_id):
    # 브라우저 음성합성: 인터넷 TTS API 키가 필요 없지만 브라우저별 음질은 다를 수 있습니다.
    js_word = json.dumps(str(word), ensure_ascii=False)
    components.html(f"""
    <div style="display:flex;justify-content:center">
      <button id="play_{unique_id}" style="background:#fff0f7;border:2px solid #efc7de;
       border-radius:22px;padding:20px 28px;font-size:23px;cursor:pointer;font-weight:700">
       🔊 단어 듣기 (클릭)
      </button>
    </div>
    <script>
    document.getElementById('play_{unique_id}').onclick = () => {{
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance({js_word});
      utterance.lang = 'en-US'; utterance.rate = 0.85;
      window.speechSynthesis.speak(utterance);
    }};
    </script>
    """, height=92)


st.markdown('<div class="mascot">🐾</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">🐱 나만의 단어장 만들기</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">소리를 듣고 내가 아는 단어인지 확인해요!</div>', unsafe_allow_html=True)

if st.session_state.selected_unit is None:
    st.markdown('<div class="guide-box">🪨 단원을 선택하고 단어를 들어보세요.<br>뜻을 알면 <b>알아요</b>, 모르면 <b>잘 모르겠어요</b>를 선택해요.</div>', unsafe_allow_html=True)
    st.markdown('### 🌈 어디부터 건너볼까요?')
    for i, unit in enumerate(units):
        unit_df = df[df['unit'] == unit]
        completed = len(st.session_state.self_assessments.get(unit, {}))
        total = len(unit_df)
        mascot = unit_mascots.get(unit, '🐾')
        left, center, right = st.columns([0.3, 2.4, 1.1] if i % 2 == 0 else [1.1, 2.4, 0.3])
        with center:
            if st.button(f'🪨 {mascot} {unit}\n\n{completed}/{total}개 확인', key=f'unit_{unit}', use_container_width=True):
                st.session_state.selected_unit = unit
                st.session_state.word_positions.setdefault(unit, 0)
                st.session_state.saved_words.setdefault(unit, [])
                st.session_state.discarded_words.setdefault(unit, [])
                st.session_state.word_history.setdefault(unit, [])
                st.session_state.self_assessments.setdefault(unit, {})
                st.rerun()
    st.stop()

unit = st.session_state.selected_unit
unit_df = df[df['unit'] == unit].reset_index(drop=True)
total_words = len(unit_df)
current_index = st.session_state.word_positions.get(unit, 0)
saved_ids = st.session_state.saved_words.setdefault(unit, [])
discarded_ids = st.session_state.discarded_words.setdefault(unit, [])
history = st.session_state.word_history.setdefault(unit, [])
assessments = st.session_state.self_assessments.setdefault(unit, {})
mascot = unit_mascots.get(unit, '🐾')

left, center, right = st.columns([1.1, 2.5, 1.3])
with left:
    if st.button('← Unit', use_container_width=True):
        st.session_state.selected_unit = None
        st.rerun()
with center:
    st.markdown(f'<div class="unit-title">{mascot} {html.escape(unit)}</div>', unsafe_allow_html=True)
with right:
    st.markdown(f'<div class="unit-count">🎧 {len(assessments)}/{total_words}</div>', unsafe_allow_html=True)

if total_words == 0:
    st.warning('이 단원에는 단어가 없습니다.')
    st.stop()

if current_index >= total_words:
    st.progress(1.0)
    st.success(f'{unit} 자기평가 완료! 🎉')
    st.write(f'잘 모르겠어요: **{len(saved_ids)}개** / 알아요: **{len(discarded_ids)}개**')
    if saved_ids:
        st.markdown('### 📦 나의 학습 단어')
        selected = unit_df[unit_df['word_id'].astype(str).isin(saved_ids)]
        for _, item in selected.iterrows():
            st.write(f'🐾 **{item["word"]}** — {item["meaning"]}')
    else:
        st.info('모든 단어를 안다고 선택했어요. 형성평가에서는 모든 단어를 다시 확인해야 해요.')
    st.caption('최초 자기평가 결과는 현재 브라우저 세션에만 보관됩니다. 연구용 영구 저장은 추후 추가해야 합니다.')
    c1, c2 = st.columns(2)
    with c1:
        if st.button('🔄 다시 고르기', use_container_width=True):
            st.session_state.word_positions[unit] = 0
            st.session_state.saved_words[unit] = []
            st.session_state.discarded_words[unit] = []
            st.session_state.word_history[unit] = []
            st.session_state.self_assessments[unit] = {}
            st.rerun()
    with c2:
        if st.button('🎧 학습하러 가기 →', type='primary', use_container_width=True):
            st.session_state.learning_unit = unit
            st.switch_page('pages/03🎀_Word_Learning_APP.py')
    st.stop()

st.progress(current_index / total_words)
st.caption(f'🌱 {current_index + 1} / {total_words}번째 단어')
row = unit_df.iloc[current_index]
word_id = str(row['word_id'])
st.markdown(f'<div class="word-card"><div class="word-number">WORD {current_index + 1}</div><div class="word-main">🎧</div><div class="question-text">소리를 듣고 뜻을 알 수 있나요?</div></div>', unsafe_allow_html=True)
speak_button(row['word'], current_index)
st.caption('소리가 들리지 않으면 브라우저의 음성 출력 설정을 확인해 주세요.')


def record_choice(choice):
    # 최초 판단만 기록하고, 기존 학습 페이지에서 사용하는 단어 보관함도 갱신
    assessments[word_id] = choice
    if word_id in saved_ids:
        saved_ids.remove(word_id)
    if word_id in discarded_ids:
        discarded_ids.remove(word_id)
    if choice == 'unknown':
        saved_ids.append(word_id)
        action = 'saved'
    else:
        discarded_ids.append(word_id)
        action = 'discarded'
    history.append({'word_id': word_id, 'action': action})
    st.session_state.word_positions[unit] += 1
    st.rerun()

c1, c2 = st.columns(2)
with c1:
    if st.button('😊 뜻을 알아요', type='primary', use_container_width=True):
        record_choice('known')
with c2:
    if st.button('🤔 잘 모르겠어요', use_container_width=True):
        record_choice('unknown')

if history:
    if st.button('↩️ 이전 선택 취소', use_container_width=True):
        previous = history.pop()
        prev_id = previous['word_id']
        assessments.pop(prev_id, None)
        if prev_id in saved_ids:
            saved_ids.remove(prev_id)
        if prev_id in discarded_ids:
            discarded_ids.remove(prev_id)
        st.session_state.word_positions[unit] = max(0, current_index - 1)
        st.rerun()

st.divider()
st.caption(f'📦 학습할 단어 {len(saved_ids)}개  |  😊 안다고 선택한 단어 {len(discarded_ids)}개')
