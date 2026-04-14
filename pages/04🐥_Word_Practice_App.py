import random
import re
import io
import base64
from typing import List, Dict, Optional

import pandas as pd
import streamlit as st
from gtts import gTTS

# -------------------------------------------------
# Config
# -------------------------------------------------
st.set_page_config(page_title="Word Practice")

# -------------------------------------------------
# Data
# -------------------------------------------------
CSV_URL = "https://raw.githubusercontent.com/jihyeon0531/WordApp/main/data/2025_Ch6_8_0819.csv"


@st.cache_data(ttl=300)
def load_data(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
    except Exception as e:
        st.error(f"CSV를 불러오지 못했습니다: {e}")
        st.stop()

    needed = ["Word", "Meaning", "Sentence", "Translation", "Set"]
    for col in needed:
        if col not in df.columns:
            st.error(f"CSV is missing required column: {col}")
            st.stop()

    df = df[["Set", "Word", "Meaning", "Sentence", "Translation"]].copy()

    # 문자열화 + 결측치 처리
    for col in ["Set", "Word", "Meaning", "Sentence", "Translation"]:
        df[col] = df[col].fillna("").astype(str)

    # 줄바꿈/공백 정리
    for col in ["Set", "Word", "Meaning", "Sentence", "Translation"]:
        df[col] = (
            df[col]
            .str.replace(r"[\r\n]+", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    # Set 값을 강제로 set1, set2 형식으로 통일
    def normalize_set_value(x: str) -> str:
        x = str(x).strip().lower()
        m = re.search(r"\d+", x)
        if m:
            return f"set{int(m.group())}"
        return x

    df["Set"] = df["Set"].apply(normalize_set_value)

    # 빈 행 제거
    df = df[
        (df["Set"] != "") &
        (df["Word"] != "") &
        (df["Meaning"] != "") &
        (df["Sentence"] != "") &
        (df["Translation"] != "")
    ].reset_index(drop=True)

    return df


def build_sets(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    def _set_sort_key(val):
        m = re.search(r"\d+", str(val))
        return int(m.group()) if m else float("inf")

    clean_df = df.copy()
    clean_df["Set"] = clean_df["Set"].astype(str).str.strip().str.lower()

    groups = sorted(clean_df.groupby("Set"), key=lambda kv: _set_sort_key(kv[0]))
    result = {}
    for set_name, g in groups:
        g = g.reset_index(drop=True)
        if len(g) > 0:
            result[str(set_name)] = g
    return result


# -------------------------------------------------
# Text utilities
# -------------------------------------------------
AUX_MAP = {
    "be": r"(?:am|is|are|was|were|be|being|been)",
    "have": r"(?:have|has|had|having)",
    "do": r"(?:do|does|did|doing)",
}


def make_match_pattern(phrase: str) -> re.Pattern:
    ph = str(phrase).strip()
    parts = ph.split()

    if parts and parts[0].lower() in AUX_MAP and len(parts) > 1:
        rest = r"\s+".join(re.escape(p) for p in parts[1:])
        head = AUX_MAP[parts[0].lower()]
        pattern = rf"(?i)(?<!\w){head}\s+{rest}(?!\w)"
    else:
        escaped = r"\s+".join(re.escape(p) for p in parts) if parts else re.escape(ph)
        pattern = rf"(?i)(?<!\w){escaped}(?!\w)"

    return re.compile(pattern, flags=re.IGNORECASE)


def _simple_mask_fallback(sentence: str, phrase: str) -> str:
    blank = "<span style='border-bottom:2px solid #222;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>"
    low_sentence = sentence.lower()
    low_phrase = phrase.lower().strip()

    idx = low_sentence.find(low_phrase)
    if idx != -1:
        return sentence[:idx] + blank + sentence[idx + len(phrase):]

    return sentence


def mask_phrase(sentence: str, phrase: str) -> str:
    pat = make_match_pattern(phrase)
    blank = "<span style='border-bottom:2px solid #222;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>"

    masked, n = pat.subn(blank, sentence, count=1)
    if n > 0:
        return masked

    return _simple_mask_fallback(sentence, phrase)


def make_mcq_options(correct: str, pool: List[str], k_distractors: int = 3) -> List[str]:
    pool_unique = list(dict.fromkeys(pool))
    distractors = [w for w in pool_unique if w != correct]
    random.shuffle(distractors)
    distractors = distractors[:k_distractors]
    opts = distractors + [correct]
    random.shuffle(opts)
    opts.append("None of the above")
    return opts


def make_k_options_including_correct(correct: str, pool: List[str], k: int = 5) -> List[str]:
    pool_unique = list(dict.fromkeys(pool))
    distractors = [w for w in pool_unique if w != correct]
    random.shuffle(distractors)
    chosen = distractors[: max(0, k - 1)]
    opts = chosen + [correct]
    random.shuffle(opts)
    return opts[:k]


def normalize_answer(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(s).lower())


def highlight_phrase(sentence: str, phrase: str, color: str = "orange") -> str:
    pat = make_match_pattern(phrase)
    highlighted, n = pat.subn(
        lambda m: f"<span style='color:{color}; font-weight:bold'>{m.group(0)}</span>",
        sentence,
        count=1,
    )
    if n > 0:
        return highlighted

    low_sentence = sentence.lower()
    low_phrase = phrase.lower().strip()
    idx = low_sentence.find(low_phrase)
    if idx != -1:
        orig = sentence[idx: idx + len(phrase)]
        return (
            sentence[:idx]
            + f"<span style='color:{color}; font-weight:bold'>{orig}</span>"
            + sentence[idx + len(phrase):]
        )

    return sentence


# -------------------------------------------------
# Audio
# -------------------------------------------------
def tts_mp3(word: str, lang: str = "en") -> bytes:
    tts = gTTS(text=word, lang=lang)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()


@st.cache_data(show_spinner=False, max_entries=1000)
def tts_cached(word: str, lang: str = "en") -> bytes:
    return tts_mp3(word, lang)


def audio_html(audio_bytes: bytes, mime: str = "audio/mp3") -> str:
    b64 = base64.b64encode(audio_bytes).decode("utf-8")
    return f"""
    <audio controls>
        <source src="data:{mime};base64,{b64}" type="{mime}">
        Your browser does not support the audio element.
    </audio>
    """


# -------------------------------------------------
# Reset helpers
# -------------------------------------------------
def reset_q1_all():
    st.session_state.current_q1 = None
    st.session_state.solved_q1 = set()
    st.session_state.completed_q1 = False
    st.session_state.q1_counter = 0
    st.session_state.remaining_q1 = []
    st.session_state.feedback_q1 = None
    st.session_state.last_correct_q1 = None
    st.session_state.show_answer_q1 = False


def reset_q2_all():
    st.session_state.current_q2 = None
    st.session_state.solved_q2 = set()
    st.session_state.completed_q2 = False
    st.session_state.q2_counter = 0
    st.session_state.remaining_q2 = []
    st.session_state.feedback_q2 = None
    st.session_state.last_correct_q2 = None
    st.session_state.show_answer_q2 = False


def reset_q3_all():
    st.session_state.current_q3 = None
    st.session_state.audio_bytes_q3 = None
    st.session_state.solved_q3 = set()
    st.session_state.completed_q3 = False
    st.session_state.q3_counter = 0
    st.session_state.remaining_q3 = []
    st.session_state.feedback_q3 = None
    st.session_state.last_correct_q3 = None
    st.session_state.show_answer_q3 = False


def reset_all_for_set_change():
    reset_q1_all()
    reset_q2_all()
    reset_q3_all()


def fill_remaining_words(cur_df: pd.DataFrame):
    words = list(cur_df["Word"])
    st.session_state.remaining_q1 = words.copy()
    st.session_state.remaining_q2 = words.copy()
    st.session_state.remaining_q3 = words.copy()


def change_set(new_set: str, sets: Dict[str, pd.DataFrame]):
    st.session_state.selected_set = new_set
    cur_df = sets[new_set].copy()
    reset_all_for_set_change()
    fill_remaining_words(cur_df)


# -------------------------------------------------
# Load data
# -------------------------------------------------
df = load_data(CSV_URL)
sets = build_sets(df)
set_names = list(sets.keys())

if not set_names:
    st.error("No sets found. Please check the CSV.")
    st.stop()


def _safe_index(names: List[str], selected: Optional[str]) -> int:
    return names.index(selected) if selected in names else 0


# -------------------------------------------------
# Question generators
# -------------------------------------------------
def generate_next_q1(cur_df: pd.DataFrame):
    remaining = [w for w in st.session_state.remaining_q1 if w not in st.session_state.solved_q1]
    if not remaining:
        st.session_state.completed_q1 = True
        st.session_state.current_q1 = None
        st.session_state.show_answer_q1 = False
        return

    target_word = random.choice(remaining)
    row = cur_df[cur_df["Word"] == target_word].iloc[0]
    meaning = str(row["Meaning"])
    pool_words = [str(w) for w in cur_df["Word"].tolist()]
    options = make_k_options_including_correct(target_word, pool_words, k=5)

    st.session_state.current_q1 = {
        "word": target_word,
        "meaning": meaning,
        "options": options,
    }
    st.session_state.q1_counter += 1
    st.session_state.feedback_q1 = None
    st.session_state.last_correct_q1 = None
    st.session_state.show_answer_q1 = False


def generate_next_q2(cur_df: pd.DataFrame):
    remaining = [w for w in st.session_state.remaining_q2 if w not in st.session_state.solved_q2]
    if not remaining:
        st.session_state.completed_q2 = True
        st.session_state.current_q2 = None
        st.session_state.show_answer_q2 = False
        return

    target_word = random.choice(remaining)
    row = cur_df[cur_df["Word"] == target_word].iloc[0]
    sentence = str(row["Sentence"])
    translation = str(row["Translation"])
    masked = mask_phrase(sentence, target_word)
    pool_words = [str(w) for w in cur_df["Word"].tolist()]
    options = make_mcq_options(target_word, pool_words, k_distractors=3)

    st.session_state.current_q2 = {
        "word": target_word,
        "sentence": sentence,
        "masked": masked,
        "translation": translation,
        "options": options,
    }
    st.session_state.q2_counter += 1
    st.session_state.feedback_q2 = None
    st.session_state.last_correct_q2 = None
    st.session_state.show_answer_q2 = False


def generate_next_q3(cur_df: pd.DataFrame):
    remaining = [w for w in st.session_state.remaining_q3 if w not in st.session_state.solved_q3]
    if not remaining:
        st.session_state.completed_q3 = True
        st.session_state.current_q3 = None
        st.session_state.audio_bytes_q3 = None
        st.session_state.show_answer_q3 = False
        return

    target_word = random.choice(remaining)
    try:
        audio_bytes = tts_cached(target_word, lang="en")
    except Exception:
        audio_bytes = None

    st.session_state.current_q3 = {"word": target_word}
    st.session_state.audio_bytes_q3 = audio_bytes
    st.session_state.q3_counter += 1
    st.session_state.feedback_q3 = None
    st.session_state.last_correct_q3 = None
    st.session_state.show_answer_q3 = False


# -------------------------------------------------
# Init state
# -------------------------------------------------
if "selected_set" not in st.session_state:
    st.session_state.selected_set = set_names[0]

defaults = {
    "current_q1": None,
    "solved_q1": set(),
    "remaining_q1": [],
    "completed_q1": False,
    "current_q2": None,
    "solved_q2": set(),
    "remaining_q2": [],
    "completed_q2": False,
    "current_q3": None,
    "audio_bytes_q3": None,
    "solved_q3": set(),
    "remaining_q3": [],
    "completed_q3": False,
    "q1_counter": 0,
    "q2_counter": 0,
    "q3_counter": 0,
    "feedback_q1": None,
    "feedback_q2": None,
    "feedback_q3": None,
    "last_correct_q1": None,
    "last_correct_q2": None,
    "last_correct_q3": None,
    "show_answer_q1": False,
    "show_answer_q2": False,
    "show_answer_q3": False,
    "active_practice": "Practice 1: 단어-뜻 연습",
}

for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

current_df = sets[st.session_state.selected_set].copy()
if not st.session_state.remaining_q1:
    st.session_state.remaining_q1 = list(current_df["Word"])
if not st.session_state.remaining_q2:
    st.session_state.remaining_q2 = list(current_df["Word"])
if not st.session_state.remaining_q3:
    st.session_state.remaining_q3 = list(current_df["Word"])

# -------------------------------------------------
# Title + selectors
# -------------------------------------------------
st.markdown("### 🐥 단어 연습 앱 (Word Practice App)")

selected_set = st.selectbox(
    "Choose a word set to practice:",
    set_names,
    index=_safe_index(set_names, st.session_state.selected_set),
    key="shared_set_select",
)

if selected_set != st.session_state.selected_set:
    change_set(selected_set, sets)
    st.rerun()

cur_df = sets[st.session_state.selected_set].copy()

practice = st.radio(
    "Choose practice type:",
    [
        "Practice 1: 단어-뜻 연습",
        "Practice 2: 문장 속 단어",
        "Practice 3: 스펠링연습",
    ],
    key="active_practice",
)

# -------------------------------------------------
# Practice 1
# -------------------------------------------------
if practice == "Practice 1: 단어-뜻 연습":
    st.markdown("#### 단어-뜻 연습")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🍅 Start / Continue", key="start_q1"):
            if st.session_state.completed_q1:
                st.info("이 세트의 모든 문항을 완료했습니다. ‘초기화’로 다시 시작할 수 있어요.")
            elif st.session_state.current_q1 is None:
                generate_next_q1(cur_df)
                st.rerun()

    with col2:
        if st.button("🔁 초기화 (Reset)", key="reset_q1"):
            reset_q1_all()
            st.session_state.remaining_q1 = list(cur_df["Word"])
            st.rerun()

    if st.session_state.feedback_q1 == "correct":
        st.success(f"Correct ✅  |  정답: {st.session_state.last_correct_q1}")
    elif st.session_state.feedback_q1 == "incorrect":
        st.error(f"Incorrect ❌  |  정답: {st.session_state.last_correct_q1}")

    if st.session_state.completed_q1:
        st.success("🎉 이 세트의 단어-뜻 연습을 모두 완료했습니다!")

    if st.session_state.current_q1 and not st.session_state.completed_q1:
        q1 = st.session_state.current_q1

        st.markdown(f"**뜻:** {q1['meaning']}")

        selected_q1 = st.radio(
            "정답을 선택하세요:",
            q1["options"],
            index=None,
            key=f"mcq_choice_q1_{st.session_state.q1_counter}",
        )

        if st.button("정답 확인", key="check_q1"):
            if selected_q1 is None:
                st.warning("먼저 보기를 선택하세요.")
            elif selected_q1 == q1["word"]:
                st.session_state.solved_q1.add(q1["word"])
                st.session_state.feedback_q1 = "correct"
                st.session_state.last_correct_q1 = q1["word"]
                st.session_state.show_answer_q1 = True
                st.rerun()
            else:
                st.session_state.feedback_q1 = "incorrect"
                st.session_state.last_correct_q1 = q1["word"]
                st.session_state.show_answer_q1 = True
                st.rerun()

        if st.session_state.show_answer_q1:
            if st.button("➡️ 다음 문제", key="next_q1"):
                generate_next_q1(cur_df)
                st.rerun()

    st.caption(f"진행 상황: {len(st.session_state.solved_q1)}/{len(cur_df)} 완료")

# -------------------------------------------------
# Practice 2
# -------------------------------------------------
elif practice == "Practice 2: 문장 속 단어":
    st.markdown("#### 문장 속 단어")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🍅 Start / Continue", key="start_q2"):
            if st.session_state.completed_q2:
                st.info("이 세트의 모든 문항을 완료했습니다. ‘초기화’로 다시 시작할 수 있어요.")
            elif st.session_state.current_q2 is None:
                generate_next_q2(cur_df)
                st.rerun()

    with col2:
        if st.button("🔁 초기화 (Reset)", key="reset_q2"):
            reset_q2_all()
            st.session_state.remaining_q2 = list(cur_df["Word"])
            st.rerun()

    if st.session_state.feedback_q2 == "correct":
        st.success(f"Correct ✅  |  정답: {st.session_state.last_correct_q2}")
    elif st.session_state.feedback_q2 == "incorrect":
        st.error(f"Incorrect ❌  |  정답: {st.session_state.last_correct_q2}")

    if st.session_state.completed_q2:
        st.success("🎉 이 세트의 문장 속 단어 연습을 모두 완료했습니다!")

    if st.session_state.current_q2 and not st.session_state.completed_q2:
        q2 = st.session_state.current_q2

        st.markdown(
            f"<div style='font-size:16px; line-height:1.6'><b>문장:</b> {q2['masked']}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div style='color:gray;'>( {q2['translation']} )</div>",
            unsafe_allow_html=True,
        )

        selected_q2 = st.radio(
            "정답을 선택하세요:",
            q2["options"],
            index=None,
            key=f"mcq_choice_q2_{st.session_state.q2_counter}",
        )

        if st.button("정답 확인", key="check_q2"):
            if selected_q2 is None:
                st.warning("먼저 보기를 선택하세요.")
            elif selected_q2 == q2["word"]:
                st.session_state.solved_q2.add(q2["word"])
                st.session_state.feedback_q2 = "correct"
                st.session_state.last_correct_q2 = q2["word"]
                st.session_state.show_answer_q2 = True
                st.rerun()
            else:
                st.session_state.feedback_q2 = "incorrect"
                st.session_state.last_correct_q2 = q2["word"]
                st.session_state.show_answer_q2 = True
                st.rerun()

        if st.session_state.show_answer_q2:
            highlighted = highlight_phrase(q2["sentence"], q2["word"])
            st.markdown("**원문 표시:**")
            st.markdown(
                f"<div style='font-size:16px; line-height:1.6'>{highlighted}</div>",
                unsafe_allow_html=True,
            )

            if st.button("➡️ 다음 문제", key="next_q2"):
                generate_next_q2(cur_df)
                st.rerun()

    st.caption(f"진행 상황: {len(st.session_state.solved_q2)}/{len(cur_df)} 완료")

# -------------------------------------------------
# Practice 3
# -------------------------------------------------
elif practice == "Practice 3: 스펠링연습":
    st.markdown("#### 스펠링연습")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🍅 Start / Continue", key="start_q3"):
            if st.session_state.completed_q3:
                st.info("이 세트의 모든 문항을 완료했습니다. ‘초기화’로 다시 시작할 수 있어요.")
            elif st.session_state.current_q3 is None:
                generate_next_q3(cur_df)
                st.rerun()

    with col2:
        if st.button("🔁 초기화 (Reset)", key="reset_q3"):
            reset_q3_all()
            st.session_state.remaining_q3 = list(cur_df["Word"])
            st.rerun()

    if st.session_state.feedback_q3 == "correct":
        st.success(f"Correct ✅  |  정답: {st.session_state.last_correct_q3}")
    elif st.session_state.feedback_q3 == "incorrect":
        st.error(f"Incorrect ❌  |  정답: {st.session_state.last_correct_q3}")

    if st.session_state.completed_q3:
        st.success("🎉 이 세트의 듣고 쓰기 연습을 모두 완료했습니다!")

    if st.session_state.current_q3 and not st.session_state.completed_q3:
        q3 = st.session_state.current_q3

        if st.session_state.audio_bytes_q3:
            st.markdown(audio_html(st.session_state.audio_bytes_q3), unsafe_allow_html=True)
        else:
            st.warning("오디오 로드에 문제가 발생했습니다. 다시 시작해 주세요.")

        typed_q3 = st.text_input(
            "정답 입력:",
            value="",
            key=f"spelling_input_q3_{st.session_state.q3_counter}",
            placeholder="예: be good at",
        )

        if st.button("정답 확인", key="check_q3"):
            user_norm = normalize_answer(typed_q3)
            correct_norm = normalize_answer(q3["word"])

            if user_norm and user_norm == correct_norm:
                st.session_state.solved_q3.add(q3["word"])
                st.session_state.feedback_q3 = "correct"
                st.session_state.last_correct_q3 = q3["word"]
                st.session_state.show_answer_q3 = True
                st.rerun()
            else:
                st.session_state.feedback_q3 = "incorrect"
                st.session_state.last_correct_q3 = q3["word"]
                st.session_state.show_answer_q3 = True
                st.rerun()

        if st.session_state.show_answer_q3:
            if st.button("➡️ 다음 문제", key="next_q3"):
                generate_next_q3(cur_df)
                st.rerun()

    st.caption(f"진행 상황: {len(st.session_state.solved_q3)}/{len(cur_df)} 완료")
