import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="소리로 익히기",
    page_icon="🎧",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #fff0f6 0%, transparent 30%),
        radial-gradient(circle at top right, #eef7ff 0%, transparent 30%),
        linear-gradient(180deg, #fffdfd 0%, #f8fbff 100%);
}

.block-container {
    max-width: 820px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* ------------------------------
   TITLE
------------------------------ */

.main-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 900;
    color: #38445a;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    color: #7a8498;
    font-size: 1rem;
    margin-bottom: 1.4rem;
}

.mascot {
    text-align: center;
    font-size: 4rem;
    margin-bottom: 0px;
}

/* ------------------------------
   SMALL INFO CARD
------------------------------ */

.info-card {
    background: rgba(255,255,255,0.85);
    border: 1px solid #edf0f5;
    border-radius: 20px;
    padding: 14px 18px;
    text-align: center;
    color: #667085;
    margin-bottom: 18px;
    box-shadow: 0 6px 18px rgba(50,60,80,0.04);
}

/* ------------------------------
   MAIN WORD CARD
------------------------------ */

.word-card {
    background: white;
    border: 2px solid #f0e8ff;
    border-radius: 32px;
    padding: 28px 26px 30px 26px;
    text-align: center;
    box-shadow: 0 14px 35px rgba(90, 70, 120, 0.09);
    margin-top: 14px;
    margin-bottom: 12px;
}

.card-label {
    font-size: 0.82rem;
    color: #a59ab8;
    font-weight: 800;
    letter-spacing: 0.08rem;
    margin-bottom: 8px;
}

.word-preview {
    font-size: 2.8rem;
    font-weight: 900;
    color: #35384a;
    margin-top: 4px;
    margin-bottom: 3px;
}

.listen-hint {
    font-size: 0.9rem;
    color: #a18daf;
    margin-bottom: 5px;
}

/* ------------------------------
   MEANING
------------------------------ */

.meaning-box {
    background: #fff7fb;
    border: 1px solid #f7dfea;
    border-radius: 20px;
    padding: 16px;
    margin-top: 17px;
}

.meaning-main {
    font-size: 1.35rem;
    font-weight: 800;
    color: #554b64;
}

/* ------------------------------
   EXAMPLE
------------------------------ */

.example-box {
    background: #f5f9ff;
    border: 1px solid #ddeafb;
    border-radius: 20px;
    padding: 16px 18px;
    margin-top: 14px;
    color: #475467;
    font-size: 1.03rem;
    line-height: 1.7;
}

.example-label {
    color: #7d91ad;
    font-size: 0.82rem;
    font-weight: 800;
    margin-bottom: 5px;
}

/* ------------------------------
   QUESTION CARD
------------------------------ */

.question-card {
    background: white;
    border: 2px solid #dfeaff;
    border-radius: 30px;
    padding: 35px 25px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(70,90,130,0.07);
    margin-top: 15px;
    margin-bottom: 15px;
}

.question-main {
    font-size: 1.8rem;
    font-weight: 850;
    color: #38445a;
}

.think-text {
    margin-top: 12px;
    color: #8a94a6;
    font-size: 0.95rem;
}

/* ------------------------------
   ANSWER
------------------------------ */

.answer-box {
    background: #f3fff7;
    border: 2px solid #d6f2df;
    border-radius: 25px;
    padding: 23px;
    text-align: center;
    margin-top: 15px;
}

.answer-label {
    font-size: 0.8rem;
    color: #7c9a86;
    font-weight: 800;
}

.answer-word {
    font-size: 2.6rem;
    font-weight: 900;
    color: #30483a;
    margin-top: 3px;
}

.answer-meaning {
    font-size: 1.4rem;
    font-weight: 800;
    color: #405748;
    margin-top: 5px;
}

/* ------------------------------
   BUTTONS
------------------------------ */

div.stButton > button {
    border-radius: 18px;
    min-height: 52px;
    font-size: 1rem;
    font-weight: 800;
    transition: 0.15s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}

/* primary button */
button[kind="primary"] {
    font-size: 1.15rem !important;
}

/* ------------------------------
   TABS
------------------------------ */

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 16px;
    padding: 10px 14px;
    font-weight: 800;
}

/* ------------------------------
   AUDIO PLAYER
------------------------------ */

audio {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_words():
    df = pd.read_csv("data/wordlist_1001.csv")
    df = df.fillna("")
    return df


try:
    df = load_words()

except Exception as e:
    st.error("단어 파일을 불러오지 못했어요.")
    st.code(str(e))
    st.stop()

# =========================================================
# AUDIO
# =========================================================

@st.cache_data(show_spinner=False)
def make_audio(text):
    if not text:
        return None

    fp = BytesIO()

    tts = gTTS(
        text=text,
        lang="en"
    )

    tts.write_to_fp(fp)

    return fp.getvalue()

# =========================================================
# SAVED WORDS CHECK
# =========================================================

if "saved_words" not in st.session_state:

    st.warning(
        "🐾 아직 보관한 단어가 없어요. "
        "먼저 Word List에서 공부할 단어를 골라 주세요!"
    )

    st.stop()


saved_units = [
    unit
    for unit, ids
    in st.session_state.saved_words.items()
    if len(ids) > 0
]


if not saved_units:

    st.warning(
        "🐾 아직 보관한 단어가 없어요. "
        "먼저 Word List에서 공부할 단어를 골라 주세요!"
    )

    st.stop()

# =========================================================
# UNIT SELECT
# =========================================================

if "learning_unit" not in st.session_state:
    st.session_state.learning_unit = saved_units[0]

if st.session_state.learning_unit not in saved_units:
    st.session_state.learning_unit = saved_units[0]


if len(saved_units) > 1:

    selected_unit = st.selectbox(
        "📚 공부할 Unit",
        saved_units,
        index=saved_units.index(
            st.session_state.learning_unit
        )
    )

    st.session_state.learning_unit = selected_unit


current_unit = st.session_state.learning_unit

saved_ids = st.session_state.saved_words.get(
    current_unit,
    []
)

learning_df = (
    df[df["word_id"].isin(saved_ids)]
    .reset_index(drop=True)
)


if len(learning_df) == 0:

    st.warning(
        f"{current_unit}에 보관한 단어가 없어요."
    )

    st.stop()

# =========================================================
# UNIT MASCOTS
# =========================================================

unit_mascots = {
    "Unit 4": "🐰",
    "Unit 5": "🐱",
    "Unit 6": "🐻",
    "Unit 7": "🐶",
    "Special Reading 1": "🐹",
    "Special Reading 2": "🦊"
}

mascot = unit_mascots.get(
    current_unit,
    "🐾"
)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "tab1_index": 0,
    "tab2_index": 0,
    "tab3_index": 0,

    "tab2_flip": False,
    "tab3_flip": False,

    "review_words": [],

    "play_tab1_word": False,
    "play_tab1_example": False,

    "play_tab2_word": False,
    "play_tab3_word": False
}


for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# HELPERS
# =========================================================

def safe_index(index):

    if index < 0:
        return 0

    if index >= len(learning_df):
        return len(learning_df) - 1

    return index


def add_review(word_id):

    if word_id not in st.session_state.review_words:
        st.session_state.review_words.append(word_id)


def reset_audio_flags():

    st.session_state.play_tab1_word = False
    st.session_state.play_tab1_example = False
    st.session_state.play_tab2_word = False
    st.session_state.play_tab3_word = False

# =========================================================
# HEADER
# =========================================================

st.markdown(
    f'<div class="mascot">{mascot}</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">🎧 소리로 익히기</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
<div class="subtitle">
{current_unit} · 내가 골라 둔 <b>{len(learning_df)}개</b> 단어
</div>
""",
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="info-card">
🎧 단어를 눈으로만 보지 말고<br>
<b>듣고, 뜻을 떠올리고, 다시 확인</b>해 보세요!
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([
    "🐰 1. 보고 듣기",
    "🐱 2. 뜻 → 영어",
    "🐻 3. 영어 → 뜻"
])

# =========================================================
# TAB 1
# 보고 듣기
# =========================================================

with tab1:

    idx = safe_index(
        st.session_state.tab1_index
    )

    row = learning_df.iloc[idx]

    st.progress(
        (idx + 1) / len(learning_df)
    )

    st.caption(
        f"🌱 {idx + 1} / {len(learning_df)}"
    )

    # -------------------------
    # MAIN CARD
    # -------------------------

    st.markdown(
        f"""
<div class="word-card">
<div class="card-label">🎧 TAP & LISTEN</div>
<div class="word-preview">{row["word"]}</div>
<div class="listen-hint">아래 단어 버튼을 눌러 소리를 들어보세요!</div>
</div>
""",
        unsafe_allow_html=True
    )

    # -------------------------
    # WORD SOUND = MAIN BUTTON
    # -------------------------

    if st.button(
        f"🔊  {row['word']}  듣기",
        key=f"listen_word_{row['word_id']}",
        type="primary",
        use_container_width=True
    ):

        st.session_state.play_tab1_word = True
        st.session_state.play_tab1_example = False

        st.rerun()

    if st.session_state.play_tab1_word:

        try:

            word_audio = make_audio(
                row["word"]
            )

            if word_audio:

                st.audio(
                    word_audio,
                    format="audio/mp3",
                    autoplay=True
                )

        except Exception:

            st.caption(
                "🐾 음성을 불러오지 못했어요."
            )

    # -------------------------
    # MEANING
    # -------------------------

    st.markdown(
        f"""
<div class="meaning-box">
<div class="meaning-main">
💗 {row["meaning"]}
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # -------------------------
    # EXAMPLE
    # -------------------------

    if row["example"]:

        st.markdown(
            f"""
<div class="example-box">
<div class="example-label">📖 EXAMPLE</div>
{row["example"]}
</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            "🎧 예문도 들어볼래요",
            key=f"listen_example_{row['word_id']}",
            use_container_width=True
        ):

            st.session_state.play_tab1_example = True
            st.session_state.play_tab1_word = False

            st.rerun()

        if st.session_state.play_tab1_example:

            try:

                example_audio = make_audio(
                    row["example"]
                )

                if example_audio:

                    st.audio(
                        example_audio,
                        format="audio/mp3",
                        autoplay=True
                    )

            except Exception:

                st.caption(
                    "예문 음성을 불러오지 못했어요."
                )

    # -------------------------
    # PRONUNCIATION CAUTION
    # -------------------------

    if row["pronunciation_caution"]:

        with st.expander(
            "👂 비슷하게 들리는 단어도 볼까요?"
        ):

            st.write(
                row["pronunciation_caution"]
            )

    # -------------------------
    # REVIEW
    # -------------------------

    if st.button(
        "⭐ 이 단어는 한 번 더 볼래요",
        key=f"tab1_review_{row['word_id']}",
        use_container_width=True
    ):

        add_review(
            row["word_id"]
        )

        st.toast(
            "⭐ 다시 볼 단어에 넣었어요!"
        )

    # -------------------------
    # NAVIGATION
    # -------------------------

    prev_col, next_col = st.columns(2)

    with prev_col:

        if st.button(
            "🐾 이전",
            key="tab1_prev",
            use_container_width=True,
            disabled=idx == 0
        ):

            st.session_state.tab1_index -= 1

            reset_audio_flags()

            st.rerun()

    with next_col:

        if st.button(
            "다음 🐾",
            key="tab1_next",
            type="primary",
            use_container_width=True,
            disabled=idx >= len(learning_df) - 1
        ):

            st.session_state.tab1_index += 1

            reset_audio_flags()

            st.rerun()

# =========================================================
# TAB 2
# 뜻 → 영어
# =========================================================

with tab2:

    idx = safe_index(
        st.session_state.tab2_index
    )

    row = learning_df.iloc[idx]

    st.progress(
        (idx + 1) / len(learning_df)
    )

    st.caption(
        f"🐱 {idx + 1} / {len(learning_df)}"
    )

    # -----------------------------------------
    # FRONT
    # -----------------------------------------

    if not st.session_state.tab2_flip:

        st.markdown(
            """
<div style="
text-align:center;
font-size:0.9rem;
color:#98a2b3;
margin-bottom:8px;
">
🇰🇷 뜻을 보고 영어 단어를 떠올려 보세요
</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            f"🇰🇷\n\n{row['meaning']}\n\n👆 눌러서 확인하기",
            key=f"tab2_card_{row['word_id']}",
            use_container_width=True
        ):

            st.session_state.tab2_flip = True
            st.rerun()

    # -----------------------------------------
    # BACK
    # -----------------------------------------

    else:

        st.markdown(
            f"""
<div class="answer-box">
<div class="answer-label">🇬🇧 ENGLISH</div>
<div class="answer-word">{row["word"]}</div>
</div>
""",
            unsafe_allow_html=True
        )

        if row["example"]:

            st.caption(
                f'📖 {row["example"]}'
            )

        # -------------------------------------
        # REVIEW / NEXT
        # -------------------------------------

        review_col, next_col = st.columns(2)

        with review_col:

            if st.button(
                "⭐ 다시 볼래요",
                key=f"tab2_review_{row['word_id']}",
                use_container_width=True
            ):

                add_review(
                    row["word_id"]
                )

                if idx < len(learning_df) - 1:

                    st.session_state.tab2_index += 1
                    st.session_state.tab2_flip = False

                    reset_audio_flags()
                    st.rerun()

                else:

                    st.success(
                        "⭐ 다시 볼 단어에 저장했어요!"
                    )

        with next_col:

            if st.button(
                "다음 →",
                key=f"tab2_next_{row['word_id']}",
                type="primary",
                use_container_width=True
            ):

                if idx < len(learning_df) - 1:

                    st.session_state.tab2_index += 1
                    st.session_state.tab2_flip = False

                    reset_audio_flags()
                    st.rerun()

                else:

                    st.success(
                        "🎉 뜻 → 영어 학습 완료!"
                    )

        # -------------------------------------
        # OPTIONAL AUDIO
        # -------------------------------------

        st.write("")

        if st.button(
            "🔊 발음이 헷갈리면 다시 듣기",
            key=f"tab2_audio_{row['word_id']}",
            use_container_width=True
        ):

            try:

                audio = make_audio(
                    row["word"]
                )

                if audio:

                    st.audio(
                        audio,
                        format="audio/mp3",
                        autoplay=True
                    )

            except Exception:

                st.caption(
                    "음성을 불러오지 못했어요."
                )

    # -----------------------------------------
    # PREVIOUS
    # -----------------------------------------

    if idx > 0:

        if st.button(
            "← 이전",
            key="tab2_previous"
        ):

            st.session_state.tab2_index -= 1
            st.session_state.tab2_flip = False

            reset_audio_flags()

            st.rerun()
            

# =========================================================
# TAB 3
# 영어 → 뜻
# =========================================================

with tab3:

    idx = safe_index(
        st.session_state.tab3_index
    )

    row = learning_df.iloc[idx]

    st.progress(
        (idx + 1) / len(learning_df)
    )

    st.caption(
        f"🐻 {idx + 1} / {len(learning_df)}"
    )

    # -----------------------------------------
    # FRONT
    # -----------------------------------------

    if not st.session_state.tab3_flip:

        st.markdown(
            """
<div style="
text-align:center;
font-size:0.9rem;
color:#98a2b3;
margin-bottom:8px;
">
🇬🇧 영어 단어를 보고 뜻을 떠올려 보세요
</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            f"🇬🇧\n\n{row['word']}\n\n👆 눌러서 확인하기",
            key=f"tab3_card_{row['word_id']}",
            use_container_width=True
        ):

            st.session_state.tab3_flip = True
            st.rerun()

    # -----------------------------------------
    # BACK
    # -----------------------------------------

    else:

        st.markdown(
            f"""
<div class="answer-box">
<div class="answer-label">🇰🇷 MEANING</div>
<div class="answer-meaning">{row["meaning"]}</div>
</div>
""",
            unsafe_allow_html=True
        )

        if row["example"]:

            st.caption(
                f'📖 {row["example"]}'
            )

        # -------------------------------------
        # REVIEW / NEXT
        # -------------------------------------

        review_col, next_col = st.columns(2)

        with review_col:

            if st.button(
                "⭐ 다시 볼래요",
                key=f"tab3_review_{row['word_id']}",
                use_container_width=True
            ):

                add_review(
                    row["word_id"]
                )

                if idx < len(learning_df) - 1:

                    st.session_state.tab3_index += 1
                    st.session_state.tab3_flip = False

                    reset_audio_flags()
                    st.rerun()

                else:

                    st.success(
                        "⭐ 다시 볼 단어에 저장했어요!"
                    )

        with next_col:

            if st.button(
                "다음 →",
                key=f"tab3_next_{row['word_id']}",
                type="primary",
                use_container_width=True
            ):

                if idx < len(learning_df) - 1:

                    st.session_state.tab3_index += 1
                    st.session_state.tab3_flip = False

                    reset_audio_flags()
                    st.rerun()

                else:

                    st.success(
                        "🎉 영어 → 뜻 학습 완료!"
                    )

        # -------------------------------------
        # OPTIONAL AUDIO
        # -------------------------------------

        st.write("")

        if st.button(
            "🔊 발음이 헷갈리면 다시 듣기",
            key=f"tab3_audio_{row['word_id']}",
            use_container_width=True
        ):

            try:

                audio = make_audio(
                    row["word"]
                )

                if audio:

                    st.audio(
                        audio,
                        format="audio/mp3",
                        autoplay=True
                    )

            except Exception:

                st.caption(
                    "음성을 불러오지 못했어요."
                )

    # -----------------------------------------
    # PREVIOUS
    # -----------------------------------------

    if idx > 0:

        if st.button(
            "← 이전",
            key="tab3_previous"
        ):

            st.session_state.tab3_index -= 1
            st.session_state.tab3_flip = False

            reset_audio_flags()

            st.rerun()
