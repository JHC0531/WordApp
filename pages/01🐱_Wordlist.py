import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Word Journey",
    page_icon="🐱",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================

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

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_words():
    df = pd.read_csv("data/wordlist_1001.csv")

    required_columns = [
        "word_id",
        "unit",
        "word",
        "meaning",
        "example",
        "pronunciation_caution"
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"CSV에 다음 열이 없습니다: {missing}"
        )

    df = df.fillna("")

    return df


try:
    df = load_words()

except Exception as e:
    st.error("단어 파일을 불러오지 못했어요.")
    st.code(str(e))
    st.stop()

# =========================================================
# SESSION STATE
# =========================================================

if "selected_unit" not in st.session_state:
    st.session_state.selected_unit = None

if "word_positions" not in st.session_state:
    st.session_state.word_positions = {}

if "saved_words" not in st.session_state:
    st.session_state.saved_words = {}

if "discarded_words" not in st.session_state:
    st.session_state.discarded_words = {}

if "word_history" not in st.session_state:
    st.session_state.word_history = {}

# =========================================================
# UNITS
# =========================================================

preferred_order = [
    "Unit 4",
    "Unit 5",
    "Unit 6",
    "Unit 7",
    "Special Reading 1",
    "Special Reading 2"
]

available_units = df["unit"].unique().tolist()

units = [
    unit
    for unit in preferred_order
    if unit in available_units
]

for unit in available_units:
    if unit not in units:
        units.append(unit)

unit_mascots = {
    "Unit 4": "🐰",
    "Unit 5": "🐱",
    "Unit 6": "🐻",
    "Unit 7": "🐶",
    "Special Reading 1": "🐹",
    "Special Reading 2": "🦊"
}

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="mascot">🐾</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">Word Journey</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="subtitle">
내가 집중해서 공부할 단어를 골라볼까요?
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# UNIT SELECTION
# =========================================================

if st.session_state.selected_unit is None:

    st.markdown(
        """
<div class="guide-box">
🪨 아래 돌다리를 하나 골라 주세요.<br>
선택한 Unit의 단어를 하나씩 만나면서<br>
<b>공부하고 싶은 단어만 보관</b>해요!
</div>
""",
        unsafe_allow_html=True
    )

    st.markdown("### 🌈 어디부터 건너볼까요?")

    for i, unit in enumerate(units):

        unit_df = df[
            df["unit"] == unit
        ]

        saved_count = len(
            st.session_state.saved_words.get(
                unit,
                []
            )
        )

        total_count = len(unit_df)

        mascot = unit_mascots.get(
            unit,
            "🐾"
        )

        if i % 2 == 0:
            empty1, stone, empty2 = st.columns(
                [0.3, 2.4, 1.1]
            )
        else:
            empty1, stone, empty2 = st.columns(
                [1.1, 2.4, 0.3]
            )

        with stone:

            if saved_count > 0:

                button_label = (
                    f"🪨 {mascot} {unit}\n\n"
                    f"📦 {saved_count}/{total_count}개 보관"
                )

            else:

                button_label = (
                    f"🪨 {mascot} {unit}\n\n"
                    f"{total_count} words"
                )

            if st.button(
                button_label,
                key=f"unit_{unit}",
                use_container_width=True
            ):

                st.session_state.selected_unit = unit

                if unit not in st.session_state.word_positions:
                    st.session_state.word_positions[unit] = 0

                if unit not in st.session_state.saved_words:
                    st.session_state.saved_words[unit] = []

                if unit not in st.session_state.discarded_words:
                    st.session_state.discarded_words[unit] = []

                if unit not in st.session_state.word_history:
                    st.session_state.word_history[unit] = []

                st.rerun()

    st.stop()

# =========================================================
# SELECTED UNIT DATA
# =========================================================

unit = st.session_state.selected_unit

unit_df = (
    df[
        df["unit"] == unit
    ]
    .reset_index(drop=True)
)

total_words = len(unit_df)

current_index = st.session_state.word_positions.get(
    unit,
    0
)

saved_ids = st.session_state.saved_words.get(
    unit,
    []
)

discarded_ids = st.session_state.discarded_words.get(
    unit,
    []
)

history = st.session_state.word_history.get(
    unit,
    []
)

mascot = unit_mascots.get(
    unit,
    "🐾"
)

# =========================================================
# TOP NAVIGATION
# =========================================================

top_left, top_middle, top_right = st.columns(
    [1.1, 2.5, 1.3]
)

with top_left:

    if st.button(
        "← Unit",
        use_container_width=True
    ):

        st.session_state.selected_unit = None

        st.rerun()

with top_middle:

    st.markdown(
        f"""
<div class="unit-title">
{mascot} {unit}
</div>
""",
        unsafe_allow_html=True
    )

with top_right:

    st.markdown(
        f"""
<div class="unit-count">
📦 {len(saved_ids)}
</div>
""",
        unsafe_allow_html=True
    )

# =========================================================
# COMPLETE
# =========================================================

if current_index >= total_words:

    st.progress(1.0)

    st.markdown(
        f"""
<div class="finish-card">
<div class="finish-emoji">{mascot}🎉</div>
<div class="finish-title">{unit} 선택 완료!</div>
<div class="finish-text">
총 {total_words}개의 단어를 모두 확인했어요.
</div>
<div class="finish-count">
📦 보관한 단어 <b>{len(saved_ids)}</b>개<br>
🗑️ 보내준 단어 <b>{len(discarded_ids)}</b>개
</div>
</div>
""",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # SAVED WORDS
    # -----------------------------------------------------

    if saved_ids:

        saved_df = unit_df[
            unit_df["word_id"].isin(
                saved_ids
            )
        ]

        st.markdown("### 📦 나의 단어 보관함")

        st.markdown(
            """
<div class="saved-box">
🎧 다음 단계에서는 이 단어들만<br>
소리와 함께 집중해서 공부해요!
</div>
""",
            unsafe_allow_html=True
        )

        for _, saved_row in saved_df.iterrows():

            st.markdown(
                f"""
**🐾 {saved_row["word"]}**  
{saved_row["meaning"]}
"""
            )

    else:

        st.info(
            "📦 보관한 단어가 없어요. "
            "필요하면 다시 골라볼 수 있어요."
        )

    st.divider()

    # -----------------------------------------------------
    # COMPLETE BUTTONS
    # -----------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        if st.button(
            "🔄 다시 고르기",
            use_container_width=True
        ):

            st.session_state.word_positions[unit] = 0

            st.session_state.saved_words[unit] = []

            st.session_state.discarded_words[unit] = []

            st.session_state.word_history[unit] = []

            st.rerun()

    with c2:

        if saved_ids:

            if st.button(
                "🎧 학습하러 가기 →",
                type="primary",
                use_container_width=True
            ):

                st.session_state.learning_unit = unit

                st.switch_page(
                    "pages/03🎀_Word_Learning_APP.py"
                )

    st.stop()

# =========================================================
# PROGRESS
# =========================================================

progress = (
    current_index + 1
) / total_words

st.progress(progress)

st.caption(
    f"🌱 {current_index + 1} / {total_words}번째 단어"
)

# =========================================================
# CURRENT WORD
# =========================================================

row = unit_df.iloc[
    current_index
]

word = row["word"]
meaning = row["meaning"]
example = row["example"]

st.markdown(
    f"""
<div class="word-card">
<div class="word-number">WORD {current_index + 1}</div>
<div class="word-main">{word}</div>
<div class="word-meaning">{meaning}</div>
<div class="example-label">📖 EXAMPLE</div>
<div class="example">{example}</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# QUESTION
# =========================================================

st.markdown(
    """
<div class="question-text">
🐾 이 단어를 더 공부하고 싶나요?
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# KEEP / DISCARD
# =========================================================

keep_col, discard_col = st.columns(2)

with keep_col:

    if st.button(
        "📦 보관할래요",
        type="primary",
        use_container_width=True
    ):

        word_id = row["word_id"]

        if word_id not in st.session_state.saved_words[unit]:

            st.session_state.saved_words[
                unit
            ].append(
                word_id
            )

        if word_id in st.session_state.discarded_words[unit]:

            st.session_state.discarded_words[
                unit
            ].remove(
                word_id
            )

        st.session_state.word_history[
            unit
        ].append(
            {
                "word_id": word_id,
                "action": "saved"
            }
        )

        st.session_state.word_positions[
            unit
        ] += 1

        st.rerun()

with discard_col:

    if st.button(
        "🗑️ 버릴래요",
        use_container_width=True
    ):

        word_id = row["word_id"]

        if word_id not in st.session_state.discarded_words[unit]:

            st.session_state.discarded_words[
                unit
            ].append(
                word_id
            )

        if word_id in st.session_state.saved_words[unit]:

            st.session_state.saved_words[
                unit
            ].remove(
                word_id
            )

        st.session_state.word_history[
            unit
        ].append(
            {
                "word_id": word_id,
                "action": "discarded"
            }
        )

        st.session_state.word_positions[
            unit
        ] += 1

        st.rerun()

# =========================================================
# UNDO
# =========================================================

st.write("")

undo_left, undo_center, undo_right = st.columns(
    [1, 2, 1]
)

with undo_center:

    if history:

        if st.button(
            "↩️ 이전 선택 취소",
            use_container_width=True
        ):

            last_action = (
                st.session_state
                .word_history[unit]
                .pop()
            )

            previous_id = last_action[
                "word_id"
            ]

            if last_action["action"] == "saved":

                if previous_id in st.session_state.saved_words[unit]:

                    st.session_state.saved_words[
                        unit
                    ].remove(
                        previous_id
                    )

            elif last_action["action"] == "discarded":

                if previous_id in st.session_state.discarded_words[unit]:

                    st.session_state.discarded_words[
                        unit
                    ].remove(
                        previous_id
                    )

            st.session_state.word_positions[
                unit
            ] = max(
                0,
                st.session_state.word_positions[unit] - 1
            )

            st.rerun()

# =========================================================
# STATUS
# =========================================================

st.divider()

status1, status2 = st.columns(2)

with status1:

    st.caption(
        f"📦 보관함: {len(saved_ids)}개"
    )

with status2:

    st.caption(
        f"🗑️ 넘어간 단어: {len(discarded_ids)}개"
    )
