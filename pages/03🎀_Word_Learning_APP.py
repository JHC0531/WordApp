import streamlit as st
import pandas as pd
from io import BytesIO
from gtts import gTTS


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="소리로 익히기",
    page_icon="🎧",
    layout="centered"
)


# =========================================================
# STYLE
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        linear-gradient(
            180deg,
            #fffaf5 0%,
            #f8fbff 100%
        );
}

.block-container {
    max-width: 820px;
    padding-top: 1.4rem;
    padding-bottom: 4rem;
}


/* ---------------------------------------------------------
   TITLE
--------------------------------------------------------- */

.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 900;
    color: #403846;
    margin-bottom: 0.3rem;
}

.subtitle {
    text-align: center;
    color: #7a7280;
    font-size: 1rem;
    line-height: 1.7;
    margin-bottom: 1.2rem;
}

.info-card {
    background: #fff7e8;
    border: 1px solid #f3dfbc;
    border-radius: 18px;
    padding: 14px 16px;
    text-align: center;
    color: #665542;
    margin: 10px 0 18px 0;
    line-height: 1.6;
}


/* ---------------------------------------------------------
   TAB 1
--------------------------------------------------------- */

.study-card {
    text-align: center;
    background: white;
    border: 2px solid #ece5f2;
    border-radius: 28px;
    padding: 34px 24px;
    margin: 12px 0 14px 0;
    box-shadow:
        0 10px 24px
        rgba(70, 60, 100, 0.07);
}

.study-label {
    font-size: 0.95rem;
    color: #9a8ca2;
    font-weight: 800;
    margin-bottom: 10px;
}

.study-word {
    font-size: 3.3rem;
    font-weight: 900;
    color: #382f3d;
    line-height: 1.15;
    word-break: break-word;
}

.study-meaning {
    font-size: 2.25rem;
    font-weight: 900;
    color: #443a48;
    line-height: 1.35;
    word-break: keep-all;
}

.study-example {
    margin-top: 18px;
    color: #7b7280;
    font-size: 1rem;
    line-height: 1.6;
}


/* ---------------------------------------------------------
   TAB 2 FRONT
--------------------------------------------------------- */

.recall-card-pink {
    text-align: center;
    background: white;
    border: 2px solid #f0d9e8;
    border-radius: 28px;
    padding: 42px 24px;
    margin: 12px 0 14px 0;

    box-shadow:
        0 10px 24px
        rgba(70, 60, 100, 0.08);
}

.recall-hint-pink {
    font-size: 0.95rem;
    color: #a3839a;
    font-weight: 800;
    margin-bottom: 14px;
}

.recall-meaning {
    font-size: 2.7rem;
    font-weight: 900;
    color: #3f3345;
    line-height: 1.35;
    word-break: keep-all;
}


/* ---------------------------------------------------------
   TAB 3 FRONT
--------------------------------------------------------- */

.recall-card-blue {
    text-align: center;
    background: white;
    border: 2px solid #dbe7ff;
    border-radius: 28px;
    padding: 42px 24px;
    margin: 12px 0 14px 0;

    box-shadow:
        0 10px 24px
        rgba(70, 60, 100, 0.08);
}

.recall-hint-blue {
    font-size: 0.95rem;
    color: #7890b0;
    font-weight: 800;
    margin-bottom: 14px;
}

.recall-word {
    font-size: 3.6rem;
    font-weight: 900;
    color: #34445d;
    line-height: 1.15;
    word-break: break-word;
}

.think-text {
    font-size: 0.95rem;
    color: #9a8ca2;
    margin-top: 16px;
}


/* ---------------------------------------------------------
   ANSWER CARDS
--------------------------------------------------------- */

.answer-green {
    text-align: center;
    background: #f3fff7;
    border: 2px solid #d6f2df;
    border-radius: 28px;
    padding: 40px 24px;
    margin: 12px 0;
}

.answer-peach {
    text-align: center;
    background: #fff8f3;
    border: 2px solid #f2dfcf;
    border-radius: 28px;
    padding: 40px 24px;
    margin: 12px 0;
}

.answer-label {
    font-size: 0.9rem;
    font-weight: 800;
    color: #7d8a82;
    margin-bottom: 12px;
}

.answer-word {
    font-size: 3.6rem;
    font-weight: 900;
    color: #2f4638;
    line-height: 1.15;
    word-break: break-word;
}

.answer-meaning {
    font-size: 2.7rem;
    font-weight: 900;
    color: #4a3c35;
    line-height: 1.35;
    word-break: keep-all;
}


/* ---------------------------------------------------------
   REVIEW
--------------------------------------------------------- */

.review-box {
    background: #fff9dc;
    border: 1px solid #f0df9f;
    border-radius: 16px;
    padding: 11px 14px;
    color: #6b5b22;
    margin-top: 12px;
}


/* ---------------------------------------------------------
   BUTTON
--------------------------------------------------------- */

div.stButton > button {
    border-radius: 17px;
    min-height: 52px;
    font-weight: 800;
    font-size: 1rem;
}


/* ---------------------------------------------------------
   TAB
--------------------------------------------------------- */

div[data-baseweb="tab-list"] {
    gap: 8px;
}

button[data-baseweb="tab"] {
    font-weight: 800;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# DATA
# =========================================================

@st.cache_data
def load_words():

    df = pd.read_csv(
        "data/wordlist_1001.csv"
    )

    df = df.fillna("")

    required_columns = [
        "word_id",
        "unit",
        "word",
        "meaning",
        "example",
        "pronunciation_caution"
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"CSV에 다음 열이 없습니다: {missing}"
        )

    return df


# =========================================================
# AUDIO
# =========================================================

@st.cache_data(
    show_spinner=False
)
def make_audio(text):

    fp = BytesIO()

    tts = gTTS(
        text=str(text),
        lang="en"
    )

    tts.write_to_fp(fp)

    fp.seek(0)

    return fp.getvalue()


# =========================================================
# LOAD
# =========================================================

try:

    df = load_words()

except Exception as e:

    st.error(
        "단어 파일을 불러오지 못했어요."
    )

    st.code(
        str(e)
    )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

if "saved_words" not in st.session_state:

    st.session_state.saved_words = {}


if "review_words" not in st.session_state:

    st.session_state.review_words = []


if "learning_unit" not in st.session_state:

    unit_list = (
        df["unit"]
        .drop_duplicates()
        .tolist()
    )

    if unit_list:

        st.session_state.learning_unit = (
            unit_list[0]
        )


defaults = {

    "tab1_index": 0,

    "tab2_index": 0,

    "tab3_index": 0,

    "tab2_flip": False,

    "tab3_flip": False,

    "last_learning_unit": None

}


for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# =========================================================
# FUNCTIONS
# =========================================================

def safe_index(
    value,
    length
):

    if length <= 0:

        return 0

    return min(
        max(
            int(value),
            0
        ),
        length - 1
    )


def add_review(
    word_id
):

    if (
        word_id
        not in
        st.session_state.review_words
    ):

        st.session_state.review_words.append(
            word_id
        )


def next_card(
    tab_name,
    total
):

    index_key = (
        f"{tab_name}_index"
    )

    flip_key = (
        f"{tab_name}_flip"
    )

    if (
        st.session_state[index_key]
        <
        total - 1
    ):

        st.session_state[
            index_key
        ] += 1

        if (
            flip_key
            in st.session_state
        ):

            st.session_state[
                flip_key
            ] = False

        st.rerun()

    else:

        st.success(
            "🎉 이 학습을 모두 마쳤어요!"
        )


def previous_card(
    tab_name
):

    index_key = (
        f"{tab_name}_index"
    )

    flip_key = (
        f"{tab_name}_flip"
    )

    if (
        st.session_state[index_key]
        >
        0
    ):

        st.session_state[
            index_key
        ] -= 1

        if (
            flip_key
            in st.session_state
        ):

            st.session_state[
                flip_key
            ] = False

        st.rerun()


# =========================================================
# LEARNING WORDS
# =========================================================

current_unit = (
    st.session_state.learning_unit
)


# Unit이 바뀌면 카드 위치 초기화
if (
    st.session_state.last_learning_unit
    !=
    current_unit
):

    st.session_state.tab1_index = 0

    st.session_state.tab2_index = 0

    st.session_state.tab3_index = 0

    st.session_state.tab2_flip = False

    st.session_state.tab3_flip = False

    st.session_state.last_learning_unit = (
        current_unit
    )


saved_ids = (
    st.session_state.saved_words.get(
        current_unit,
        []
    )
)


learning_df = df[
    (
        df["unit"]
        ==
        current_unit
    )
    &
    (
        df["word_id"]
        .isin(
            saved_ids
        )
    )
].reset_index(
    drop=True
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
<div class="main-title">
🎧 소리로 익히기
</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    f"""
<div class="subtitle">
<b>{current_unit}</b>에서 내가 골라둔 단어를 공부해요.<br>
보고, 떠올리고, 필요하면 다시 들어보세요.
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# NO SAVED WORDS
# =========================================================

if learning_df.empty:

    st.info(
        "📦 아직 이 Unit에서 보관한 단어가 없어요. "
        "먼저 ‘나만의 단어 골라보기’에서 "
        "공부할 단어를 골라주세요."
    )

    if st.button(
        "🐱 단어 골라보러 가기",
        type="primary",
        use_container_width=True
    ):

        st.switch_page(
            "pages/01🐱_Wordlist.py"
        )

    st.stop()


st.markdown(
    f"""
<div class="info-card">
📦 <b>{len(learning_df)}개</b>의 단어를 학습해요.<br>
⭐ 헷갈리는 단어는 <b>다시 볼래요</b>에 저장할 수 있어요.
</div>
""",
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(
    [
        "🎧 보고 듣기",
        "🇰🇷 뜻 → 영어",
        "🇬🇧 영어 → 뜻"
    ]
)


# =========================================================
# TAB 1
# 보고 듣기
# =========================================================

with tab1:

    idx = safe_index(
        st.session_state.tab1_index,
        len(learning_df)
    )

    row = learning_df.iloc[
        idx
    ]


    st.progress(
        (idx + 1)
        /
        len(learning_df)
    )


    st.caption(
        f"🎧 {idx + 1} / "
        f"{len(learning_df)}"
    )


    st.markdown(
        f"""
<div class="study-card">

<div class="study-label">
🇬🇧 WORD
</div>

<div class="study-word">
{row["word"]}
</div>

<div style="height:16px;"></div>

<div class="study-label">
🇰🇷 MEANING
</div>

<div class="study-meaning">
{row["meaning"]}
</div>

<div class="study-example">
📖 {row["example"]}
</div>

</div>
""",
        unsafe_allow_html=True
    )


    if st.button(
        f"🔊 {row['word']} 듣기",
        key=(
            f"tab1_audio_"
            f"{row['word_id']}"
        ),
        type="primary",
        use_container_width=True
    ):

        try:

            st.audio(
                make_audio(
                    row["word"]
                ),
                format="audio/mp3",
                autoplay=True
            )

        except Exception:

            st.caption(
                "음성을 불러오지 못했어요."
            )


    c1, c2, c3 = st.columns(
        [
            1,
            1.5,
            1.5
        ]
    )


    with c1:

        if idx > 0:

            if st.button(
                "← 이전",
                key="tab1_prev",
                use_container_width=True
            ):

                previous_card(
                    "tab1"
                )


    with c2:

        if st.button(
            "⭐ 다시 볼래요",
            key=(
                f"tab1_review_"
                f"{row['word_id']}"
            ),
            use_container_width=True
        ):

            add_review(
                row["word_id"]
            )

            next_card(
                "tab1",
                len(learning_df)
            )


    with c3:

        if st.button(
            "다음 →",
            key="tab1_next",
            use_container_width=True
        ):

            next_card(
                "tab1",
                len(learning_df)
            )


# =========================================================
# TAB 2
# 뜻 → 영어
# =========================================================

with tab2:

    idx = safe_index(
        st.session_state.tab2_index,
        len(learning_df)
    )

    row = learning_df.iloc[
        idx
    ]


    st.progress(
        (idx + 1)
        /
        len(learning_df)
    )


    st.caption(
        f"🐱 {idx + 1} / "
        f"{len(learning_df)}"
    )


    # -----------------------------------------------------
    # FRONT
    # -----------------------------------------------------

    if not st.session_state.tab2_flip:

        st.markdown(
            f"""
<div class="recall-card-pink">

<div class="recall-hint-pink">
🇰🇷 뜻을 보고 영어를 떠올려 보세요
</div>

<div class="recall-meaning">
{row["meaning"]}
</div>

<div class="think-text">
머릿속으로 영어 단어를 생각해 봐요 💭
</div>

</div>
""",
            unsafe_allow_html=True
        )


        if st.button(
            "👆 눌러서 영어 확인하기",
            key=(
                f"tab2_card_"
                f"{row['word_id']}"
            ),
            type="primary",
            use_container_width=True
        ):

            st.session_state.tab2_flip = True

            st.rerun()


    # -----------------------------------------------------
    # BACK
    # -----------------------------------------------------

    else:

        st.markdown(
            f"""
<div class="answer-green">

<div class="answer-label">
🇬🇧 ENGLISH
</div>

<div class="answer-word">
{row["word"]}
</div>

</div>
""",
            unsafe_allow_html=True
        )


        if row["example"]:

            st.caption(
                f'📖 {row["example"]}'
            )


        review_col, next_col = (
            st.columns(2)
        )


        with review_col:

            if st.button(
                "⭐ 다시 볼래요",
                key=(
                    f"tab2_review_"
                    f"{row['word_id']}"
                ),
                use_container_width=True
            ):

                add_review(
                    row["word_id"]
                )

                next_card(
                    "tab2",
                    len(learning_df)
                )


        with next_col:

            if st.button(
                "다음 →",
                key=(
                    f"tab2_next_"
                    f"{row['word_id']}"
                ),
                type="primary",
                use_container_width=True
            ):

                next_card(
                    "tab2",
                    len(learning_df)
                )


        st.write("")


        if st.button(
            "🔊 발음이 헷갈리면 다시 듣기",
            key=(
                f"tab2_audio_"
                f"{row['word_id']}"
            ),
            use_container_width=True
        ):

            try:

                st.audio(
                    make_audio(
                        row["word"]
                    ),
                    format="audio/mp3",
                    autoplay=True
                )

            except Exception:

                st.caption(
                    "음성을 불러오지 못했어요."
                )


    # -----------------------------------------------------
    # PREVIOUS
    # -----------------------------------------------------

    if idx > 0:

        if st.button(
            "← 이전",
            key="tab2_previous"
        ):

            previous_card(
                "tab2"
            )


# =========================================================
# TAB 3
# 영어 → 뜻
# =========================================================

with tab3:

    idx = safe_index(
        st.session_state.tab3_index,
        len(learning_df)
    )

    row = learning_df.iloc[
        idx
    ]


    st.progress(
        (idx + 1)
        /
        len(learning_df)
    )


    st.caption(
        f"🐻 {idx + 1} / "
        f"{len(learning_df)}"
    )


    # -----------------------------------------------------
    # FRONT
    # -----------------------------------------------------

    if not st.session_state.tab3_flip:

        st.markdown(
            f"""
<div class="recall-card-blue">

<div class="recall-hint-blue">
🇬🇧 영어를 보고 뜻을 떠올려 보세요
</div>

<div class="recall-word">
{row["word"]}
</div>

<div class="think-text">
머릿속으로 뜻을 생각해 봐요 💭
</div>

</div>
""",
            unsafe_allow_html=True
        )


        if st.button(
            "👆 눌러서 뜻 확인하기",
            key=(
                f"tab3_card_"
                f"{row['word_id']}"
            ),
            type="primary",
            use_container_width=True
        ):

            st.session_state.tab3_flip = True

            st.rerun()


    # -----------------------------------------------------
    # BACK
    # -----------------------------------------------------

    else:

        st.markdown(
            f"""
<div class="answer-peach">

<div class="answer-label">
🇰🇷 MEANING
</div>

<div class="answer-meaning">
{row["meaning"]}
</div>

</div>
""",
            unsafe_allow_html=True
        )


        if row["example"]:

            st.caption(
                f'📖 {row["example"]}'
            )


        review_col, next_col = (
            st.columns(2)
        )


        with review_col:

            if st.button(
                "⭐ 다시 볼래요",
                key=(
                    f"tab3_review_"
                    f"{row['word_id']}"
                ),
                use_container_width=True
            ):

                add_review(
                    row["word_id"]
                )

                next_card(
                    "tab3",
                    len(learning_df)
                )


        with next_col:

            if st.button(
                "다음 →",
                key=(
                    f"tab3_next_"
                    f"{row['word_id']}"
                ),
                type="primary",
                use_container_width=True
            ):

                next_card(
                    "tab3",
                    len(learning_df)
                )


        st.write("")


        if st.button(
            "🔊 발음이 헷갈리면 다시 듣기",
            key=(
                f"tab3_audio_"
                f"{row['word_id']}"
            ),
            use_container_width=True
        ):

            try:

                st.audio(
                    make_audio(
                        row["word"]
                    ),
                    format="audio/mp3",
                    autoplay=True
                )

            except Exception:

                st.caption(
                    "음성을 불러오지 못했어요."
                )


    # -----------------------------------------------------
    # PREVIOUS
    # -----------------------------------------------------

    if idx > 0:

        if st.button(
            "← 이전",
            key="tab3_previous"
        ):

            previous_card(
                "tab3"
            )


# =========================================================
# REVIEW WORDS
# =========================================================

st.divider()


review_ids = set(
    st.session_state.review_words
)


review_df = df[
    (
        df["unit"]
        ==
        current_unit
    )
    &
    (
        df["word_id"]
        .isin(
            review_ids
        )
    )
]


if not review_df.empty:

    st.markdown(
        f"""
<div class="review-box">
⭐ <b>다시 볼 단어 {len(review_df)}개</b><br>
헷갈렸던 단어를 표시해 두었어요.
</div>
""",
        unsafe_allow_html=True
    )


    with st.expander(
        "⭐ 다시 볼 단어 확인하기"
    ):

        for _, review_row in (
            review_df.iterrows()
        ):

            st.markdown(
                f"""
**{review_row["word"]}**  
{review_row["meaning"]}
"""
            )


# =========================================================
# PRONUNCIATION APP
# =========================================================

st.write("")


if st.button(
    "🐶 콩이와 발음 도전하러 가기 →",
    type="primary",
    use_container_width=True
):

    st.switch_page(
        "pages/04🐥_발음짱이 될거야.py"
    )
