import streamlit as st
import pandas as pd
from gtts import gTTS
from io import BytesIO


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Word Learning",
    page_icon="🌱",
    layout="centered"
)


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        180deg,
        #f9fcff 0%,
        #f2f8f5 100%
    );
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* 제목 */

.main-title {
    text-align: center;
    font-size: 2.35rem;
    font-weight: 850;
    color: #243447;
    margin-bottom: 0.3rem;
}

.subtitle {
    text-align: center;
    color: #667085;
    font-size: 1rem;
    margin-bottom: 1.8rem;
}


/* 학습 카드 */

.learning-card {
    background: white;
    border: 1px solid #e4e7ec;
    border-radius: 28px;
    padding: 38px 30px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(40, 60, 80, 0.07);
    margin-top: 18px;
    margin-bottom: 18px;
}

.card-label {
    font-size: 0.82rem;
    color: #98a2b3;
    font-weight: 700;
    letter-spacing: 0.05rem;
    margin-bottom: 9px;
}

.word-main {
    font-size: 3rem;
    font-weight: 850;
    color: #1d2939;
    margin-bottom: 15px;
}

.meaning-main {
    font-size: 1.45rem;
    font-weight: 700;
    color: #344054;
    margin-bottom: 22px;
}

.example-box {
    background: #f8fafc;
    border-radius: 16px;
    padding: 15px 18px;
    margin-top: 18px;
    color: #475467;
    font-size: 1.05rem;
    line-height: 1.65;
}

.question-text {
    font-size: 1.8rem;
    font-weight: 800;
    color: #1f2937;
    margin-top: 12px;
    margin-bottom: 12px;
}

.think-text {
    color: #667085;
    font-size: 0.95rem;
    margin-bottom: 12px;
}


/* 정답 */

.answer-box {
    background: #f0f9f4;
    border: 1px solid #d1ead9;
    border-radius: 22px;
    padding: 25px;
    margin-top: 18px;
    text-align: center;
}

.answer-title {
    color: #667085;
    font-size: 0.83rem;
    margin-bottom: 5px;
}

.answer-word {
    font-size: 2.4rem;
    font-weight: 850;
    color: #1d2939;
}

.answer-meaning {
    font-size: 1.35rem;
    font-weight: 700;
    color: #344054;
}


/* 다시보기 */

.review-box {
    background: #fff9e8;
    border: 1px solid #f3df9b;
    border-radius: 16px;
    padding: 12px;
    text-align: center;
    color: #725b17;
}


/* 버튼 */

div.stButton > button {
    border-radius: 15px;
    min-height: 50px;
    font-weight: 700;
}

div.stButton > button:hover {
    transform: translateY(-1px);
}


/* 탭 */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 14px;
    padding: 10px 16px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_words():

    df = pd.read_csv(
        "data/wordlist_1001.csv"
    )

    df = df.fillna("")

    return df


try:

    df = load_words()

except Exception as e:

    st.error(
        "단어 파일을 불러오지 못했어요."
    )

    st.code(str(e))

    st.stop()


# =========================================================
# TEXT TO SPEECH
# =========================================================

@st.cache_data(show_spinner=False)
def make_audio(text):

    if not text:
        return None

    mp3_fp = BytesIO()

    tts = gTTS(
        text=text,
        lang="en"
    )

    tts.write_to_fp(mp3_fp)

    return mp3_fp.getvalue()


# =========================================================
# CHECK SAVED WORDS
# =========================================================

if (
    "saved_words" not in st.session_state
    or not st.session_state.saved_words
):

    st.warning(
        "아직 보관한 단어가 없어요. "
        "먼저 Word List에서 공부할 단어를 골라 주세요."
    )

    st.stop()


# =========================================================
# DETERMINE UNIT
# =========================================================

if "learning_unit" in st.session_state:

    current_unit = st.session_state.learning_unit

elif "selected_unit" in st.session_state:

    current_unit = st.session_state.selected_unit

else:

    available_saved_units = [
        unit
        for unit, ids
        in st.session_state.saved_words.items()
        if len(ids) > 0
    ]

    if not available_saved_units:

        st.warning(
            "보관한 단어가 없어요."
        )

        st.stop()

    current_unit = available_saved_units[0]


# =========================================================
# UNIT SELECTOR
# =========================================================

saved_units = [
    unit
    for unit, ids
    in st.session_state.saved_words.items()
    if len(ids) > 0
]


if len(saved_units) > 1:

    default_index = (
        saved_units.index(current_unit)
        if current_unit in saved_units
        else 0
    )

    current_unit = st.selectbox(
        "공부할 Unit",
        saved_units,
        index=default_index
    )

    st.session_state.learning_unit = current_unit


# =========================================================
# GET SAVED WORDS
# =========================================================

saved_ids = st.session_state.saved_words.get(
    current_unit,
    []
)

learning_df = (
    df[
        df["word_id"].isin(saved_ids)
    ]
    .reset_index(drop=True)
)


if len(learning_df) == 0:

    st.warning(
        f"{current_unit}에서 보관한 단어가 없습니다."
    )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

state_defaults = {

    "learn_index": 0,

    "meaning_to_word_index": 0,

    "word_to_meaning_index": 0,

    "meaning_revealed": False,

    "word_revealed": False,

    "review_words": []
}


for key, value in state_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# HELPER
# =========================================================

def clamp_index(index):

    if index < 0:
        return 0

    if index >= len(learning_df):
        return len(learning_df) - 1

    return index


def mark_review(word_id):

    if word_id not in st.session_state.review_words:

        st.session_state.review_words.append(
            word_id
        )


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">🌱 Word Learning</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="subtitle">
        {current_unit} · 내가 보관한
        <b>{len(learning_df)}</b>개의 단어
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PROGRESS SUMMARY
# =========================================================

top1, top2 = st.columns(2)

with top1:

    st.metric(
        "📦 학습 단어",
        f"{len(learning_df)}개"
    )

with top2:

    st.metric(
        "⭐ 다시 볼 단어",
        f"{len(st.session_state.review_words)}개"
    )


st.write("")


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs([

    "👀 1. 보고 듣기",

    "🇰🇷 2. 뜻 → 단어",

    "🇬🇧 3. 단어 → 뜻"

])


# =========================================================
# TAB 1
# 보고 듣기
# =========================================================

with tab1:

    index = clamp_index(
        st.session_state.learn_index
    )

    row = learning_df.iloc[index]

    st.progress(
        (index + 1)
        / len(learning_df)
    )

    st.caption(
        f"{index + 1} / {len(learning_df)}"
    )


    st.markdown(
        f"""
        <div class="learning-card">

            <div class="card-label">
                WORD
            </div>

            <div class="word-main">
                {row["word"]}
            </div>

            <div class="meaning-main">
                {row["meaning"]}
            </div>

            <div class="example-box">

                <b>Example</b><br>

                {row["example"]}

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -------------------------
    # WORD AUDIO
    # -------------------------

    st.markdown(
        "#### 🔊 단어 듣기"
    )

    try:

        word_audio = make_audio(
            row["word"]
        )

        if word_audio:

            st.audio(
                word_audio,
                format="audio/mp3"
            )

    except Exception:

        st.caption(
            "음성을 불러오지 못했어요."
        )


    # -------------------------
    # SENTENCE AUDIO
    # -------------------------

    if row["example"]:

        st.markdown(
            "#### 🎧 예문 듣기"
        )

        try:

            sentence_audio = make_audio(
                row["example"]
            )

            if sentence_audio:

                st.audio(
                    sentence_audio,
                    format="audio/mp3"
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
            "👂 발음이 헷갈릴 수 있는 단어"
        ):

            st.write(
                row["pronunciation_caution"]
            )


    # -------------------------
    # REVIEW BUTTON
    # -------------------------

    if st.button(
        "⭐ 이 단어는 다시 볼래요",
        key=f"review_learn_{row['word_id']}",
        use_container_width=True
    ):

        mark_review(
            row["word_id"]
        )

        st.toast(
            "다시 볼 단어에 넣었어요 ⭐"
        )


    # -------------------------
    # NAVIGATION
    # -------------------------

    previous_col, next_col = st.columns(2)


    with previous_col:

        if st.button(
            "← 이전",
            key="learn_previous",
            use_container_width=True,
            disabled=index == 0
        ):

            st.session_state.learn_index -= 1

            st.rerun()


    with next_col:

        if st.button(
            "다음 →",
            key="learn_next",
            type="primary",
            use_container_width=True,
            disabled=index >= len(learning_df) - 1
        ):

            st.session_state.learn_index += 1

            st.rerun()


# =========================================================
# TAB 2
# 한글 → 영어
# =========================================================

with tab2:

    index = clamp_index(
        st.session_state.meaning_to_word_index
    )

    row = learning_df.iloc[index]


    st.progress(
        (index + 1)
        / len(learning_df)
    )


    st.caption(
        f"{index + 1} / {len(learning_df)}"
    )


    # -------------------------
    # FRONT
    # -------------------------

    st.markdown(
        f"""
        <div class="learning-card">

            <div class="card-label">
                WHAT IS THE ENGLISH WORD?
            </div>

            <div class="question-text">
                {row["meaning"]}
            </div>

            <div class="think-text">
                영어단어를 머릿속으로 떠올려 보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # -------------------------
    # FLIP
    # -------------------------

    if not st.session_state.meaning_revealed:

        if st.button(
            "🔄 카드 뒤집기",
            key="flip_meaning",
            type="primary",
            use_container_width=True
        ):

            st.session_state.meaning_revealed = True

            st.rerun()


    # -------------------------
    # ANSWER
    # -------------------------

    else:

        st.markdown(
            f"""
            <div class="answer-box">

                <div class="answer-title">
                    ANSWER
                </div>

                <div class="answer-word">
                    {row["word"]}
                </div>

                <div style="
                    margin-top:16px;
                    color:#475467;
                ">

                    {row["example"]}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # AUDIO

        try:

            word_audio = make_audio(
                row["word"]
            )

            if word_audio:

                st.audio(
                    word_audio,
                    format="audio/mp3"
                )

        except Exception:

            pass


        # SELF CHECK

        st.markdown(
            "#### 나는 어땠나요?"
        )


        know_col, review_col = st.columns(2)


        with know_col:

            if st.button(
                "😊 맞혔어요",
                key=f"meaning_known_{index}",
                use_container_width=True
            ):

                if index < len(learning_df) - 1:

                    st.session_state.meaning_to_word_index += 1

                    st.session_state.meaning_revealed = False

                    st.rerun()

                else:

                    st.success(
                        "이 단계의 마지막 단어예요! 🎉"
                    )


        with review_col:

            if st.button(
                "⭐ 다시 볼래요",
                key=f"meaning_review_{index}",
                use_container_width=True
            ):

                mark_review(
                    row["word_id"]
                )

                if index < len(learning_df) - 1:

                    st.session_state.meaning_to_word_index += 1

                    st.session_state.meaning_revealed = False

                    st.rerun()

                else:

                    st.success(
                        "다시 볼 단어에 저장했어요 ⭐"
                    )


    # -------------------------
    # PREVIOUS
    # -------------------------

    if index > 0:

        if st.button(
            "← 이전 단어",
            key="meaning_previous"
        ):

            st.session_state.meaning_to_word_index -= 1

            st.session_state.meaning_revealed = False

            st.rerun()


# =========================================================
# TAB 3
# 영어 → 한글
# =========================================================

with tab3:

    index = clamp_index(
        st.session_state.word_to_meaning_index
    )

    row = learning_df.iloc[index]


    st.progress(
        (index + 1)
        / len(learning_df)
    )


    st.caption(
        f"{index + 1} / {len(learning_df)}"
    )


    # -------------------------
    # FRONT
    # -------------------------

    st.markdown(
        f"""
        <div class="learning-card">

            <div class="card-label">
                WHAT DOES IT MEAN?
            </div>

            <div class="word-main">
                {row["word"]}
            </div>

            <div class="think-text">
                한글 뜻을 머릿속으로 떠올려 보세요.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # 단어 소리는 앞면에서 제공
    try:

        word_audio = make_audio(
            row["word"]
        )

        if word_audio:

            st.audio(
                word_audio,
                format="audio/mp3"
            )

    except Exception:

        pass


    # -------------------------
    # FLIP
    # -------------------------

    if not st.session_state.word_revealed:

        if st.button(
            "🔄 카드 뒤집기",
            key="flip_word",
            type="primary",
            use_container_width=True
        ):

            st.session_state.word_revealed = True

            st.rerun()


    # -------------------------
    # ANSWER
    # -------------------------

    else:

        st.markdown(
            f"""
            <div class="answer-box">

                <div class="answer-title">
                    MEANING
                </div>

                <div class="answer-meaning">
                    {row["meaning"]}
                </div>

                <div style="
                    margin-top:18px;
                    color:#475467;
                ">

                    {row["example"]}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # SELF CHECK

        st.markdown(
            "#### 나는 어땠나요?"
        )


        know_col, review_col = st.columns(2)


        with know_col:

            if st.button(
                "😊 알았어요",
                key=f"word_known_{index}",
                use_container_width=True
            ):

                if index < len(learning_df) - 1:

                    st.session_state.word_to_meaning_index += 1

                    st.session_state.word_revealed = False

                    st.rerun()

                else:

                    st.success(
                        "이 단계의 마지막 단어예요! 🎉"
                    )


        with review_col:

            if st.button(
                "⭐ 다시 볼래요",
                key=f"word_review_{index}",
                use_container_width=True
            ):

                mark_review(
                    row["word_id"]
                )

                if index < len(learning_df) - 1:

                    st.session_state.word_to_meaning_index += 1

                    st.session_state.word_revealed = False

                    st.rerun()

                else:

                    st.success(
                        "다시 볼 단어에 저장했어요 ⭐"
                    )


    # -------------------------
    # PREVIOUS
    # -------------------------

    if index > 0:

        if st.button(
            "← 이전 단어",
            key="word_previous"
        ):

            st.session_state.word_to_meaning_index -= 1

            st.session_state.word_revealed = False

            st.rerun()


# =========================================================
# REVIEW WORDS SUMMARY
# =========================================================

st.divider()


if st.session_state.review_words:

    review_df = learning_df[
        learning_df["word_id"].isin(
            st.session_state.review_words
        )
    ]

    with st.expander(
        f"⭐ 다시 볼 단어 "
        f"{len(review_df)}개"
    ):

        for _, row in review_df.iterrows():

            st.markdown(
                f"""
                **{row["word"]}**  
                {row["meaning"]}
                """
            )


else:

    st.caption(
        "⭐ 어려운 단어가 있으면 "
        "'다시 볼래요'를 눌러 주세요."
    )
