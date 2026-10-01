import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Word Journey",
    page_icon="🌱",
    layout="centered"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>

/* 전체 화면 */
.stApp {
    background: linear-gradient(
        180deg,
        #f9fcff 0%,
        #eef7f2 100%
    );
}

/* 기본 여백 */
.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* 제목 */
.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
    color: #243447;
    margin-bottom: 0.25rem;
}

.subtitle {
    text-align: center;
    color: #667085;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* 안내 카드 */
.guide-box {
    background: white;
    border-radius: 18px;
    padding: 18px 22px;
    margin-bottom: 25px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
    text-align: center;
    color: #475467;
}

/* 단어 카드 */
.word-card {
    background: white;
    border-radius: 28px;
    padding: 42px 30px;
    text-align: center;
    border: 1px solid #e3e8ef;
    box-shadow: 0 12px 30px rgba(50, 70, 90, 0.08);
    margin-top: 20px;
    margin-bottom: 20px;
}

.word-number {
    color: #98a2b3;
    font-size: 0.9rem;
    margin-bottom: 10px;
}

.word-main {
    font-size: 3.0rem;
    font-weight: 850;
    color: #1f2937;
    margin-bottom: 15px;
}

.word-meaning {
    font-size: 1.35rem;
    font-weight: 600;
    color: #475467;
    margin-bottom: 24px;
}

.example-label {
    font-size: 0.82rem;
    color: #98a2b3;
    margin-bottom: 4px;
}

.example {
    font-size: 1.05rem;
    color: #344054;
    font-style: italic;
    line-height: 1.7;
}

/* 보관함 결과 */
.saved-box {
    background: #f0f9f4;
    border: 1px solid #cce8d6;
    border-radius: 20px;
    padding: 22px;
    margin-top: 20px;
}

/* 완료 카드 */
.finish-card {
    background: white;
    border-radius: 28px;
    padding: 35px 25px;
    text-align: center;
    border: 1px solid #e3e8ef;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    margin-top: 20px;
}

/* Streamlit 버튼 */
div.stButton > button {
    border-radius: 16px;
    min-height: 52px;
    font-size: 1rem;
    font-weight: 700;
    border: 1px solid #d0d5dd;
    transition: 0.15s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    border-color: #98a2b3;
}

/* progress bar */
.stProgress > div > div > div > div {
    border-radius: 20px;
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
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"CSV에 다음 열이 없습니다: {missing}"
        )

    # NaN → 빈 문자열
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

# 학생이 현재 선택한 Unit
if "selected_unit" not in st.session_state:
    st.session_state.selected_unit = None

# Unit별 현재 카드 위치
if "word_positions" not in st.session_state:
    st.session_state.word_positions = {}

# 보관한 단어 ID
if "saved_words" not in st.session_state:
    st.session_state.saved_words = {}

# 버린 단어 ID
if "discarded_words" not in st.session_state:
    st.session_state.discarded_words = {}

# 선택 기록 → 이전 선택 취소용
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
    unit for unit in preferred_order
    if unit in available_units
]

# 혹시 CSV에 새 단원이 생겼을 경우 자동 추가
for unit in available_units:
    if unit not in units:
        units.append(unit)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="main-title">🌿 Word Journey</div>',
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

    st.markdown("""
    <div class="guide-box">
        아래 돌다리를 하나 골라 주세요.<br>
        선택한 Unit의 단어부터 하나씩 만나게 됩니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🪨 어디부터 건너볼까요?")

    # -----------------------------------------------------
    # 돌다리 형태
    # -----------------------------------------------------

    for i, unit in enumerate(units):

        unit_df = df[df["unit"] == unit]

        saved_count = len(
            st.session_state.saved_words.get(unit, [])
        )

        total_count = len(unit_df)

        # 지그재그 돌다리 느낌
        if i % 2 == 0:
            empty1, stone, empty2 = st.columns([0.3, 2.4, 1.1])
        else:
            empty1, stone, empty2 = st.columns([1.1, 2.4, 0.3])

        with stone:

            if saved_count > 0:
                button_label = (
                    f"🪨  {unit}\n\n"
                    f"📦 {saved_count}/{total_count}개 보관"
                )
            else:
                button_label = (
                    f"🪨  {unit}\n\n"
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
    df[df["unit"] == unit]
    .reset_index(drop=True)
)

total_words = len(unit_df)

current_index = st.session_state.word_positions.get(unit, 0)

saved_ids = st.session_state.saved_words.get(unit, [])
discarded_ids = st.session_state.discarded_words.get(unit, [])
history = st.session_state.word_history.get(unit, [])


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
        <div style="
            text-align:center;
            font-size:1.25rem;
            font-weight:800;
            padding-top:10px;
        ">
            {unit}
        </div>
        """,
        unsafe_allow_html=True
    )

with top_right:
    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding-top:11px;
            color:#667085;
        ">
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

            <div style="font-size:3rem;">
                🎉
            </div>

            <h2>{unit} 선택 완료!</h2>

            <p style="
                color:#667085;
                font-size:1.05rem;
            ">
                총 {total_words}개의 단어를 모두 확인했어요.
            </p>

            <div style="
                font-size:1.25rem;
                margin-top:18px;
            ">
                📦 보관한 단어
                <b>{len(saved_ids)}</b>개
            </div>

            <div style="
                font-size:1rem;
                color:#98a2b3;
                margin-top:7px;
            ">
                🗑️ 보낸 단어
                {len(discarded_ids)}개
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # 보관 단어 목록
    # -----------------------------------------------------

    if saved_ids:

        saved_df = unit_df[
            unit_df["word_id"].isin(saved_ids)
        ]

        st.markdown("### 📦 나의 단어 보관함")

        st.markdown(
            """
            <div class="saved-box">
            다음 단계에서는 이 단어들만 집중해서 공부해요.
            </div>
            """,
            unsafe_allow_html=True
        )

        for _, row in saved_df.iterrows():

            st.markdown(
                f"""
                **{row["word"]}**  
                {row["meaning"]}
                """
            )

    else:

        st.info(
            "보관한 단어가 없어요. "
            "필요하면 다시 골라볼 수 있어요."
        )

    st.divider()

    # -----------------------------------------------------
    # 완료 후 버튼
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
                "🔊 학습하러 가기 →",
                type="primary",
                use_container_width=True
            ):

                # Learning App에서 사용할 Unit도 저장
                st.session_state.learning_unit = unit

                st.success(
                    "보관한 단어가 준비되었어요! "
                    "다음 단계에서 이 단어들만 학습합니다."
                )

                # Learning App 파일명을 확정하면
                # 아래 코드로 바로 이동시킬 수 있음.
                #
                # st.switch_page(
                #     "pages/2_Learning_App.py"
                # )

    st.stop()


# =========================================================
# PROGRESS
# =========================================================

progress = current_index / total_words

st.progress(progress)

st.caption(
    f"{current_index + 1} / {total_words}번째 단어"
)


# =========================================================
# CURRENT WORD
# =========================================================

row = unit_df.iloc[current_index]

word = row["word"]
meaning = row["meaning"]
example = row["example"]


st.markdown(
    f"""
    <div class="word-card">

        <div class="word-number">
            WORD {current_index + 1}
        </div>

        <div class="word-main">
            {word}
        </div>

        <div class="word-meaning">
            {meaning}
        </div>

        <div class="example-label">
            Example
        </div>

        <div class="example">
            {example}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# STUDENT QUESTION
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        font-size:1.1rem;
        font-weight:700;
        color:#344054;
        margin:15px 0 17px 0;
    ">
        이 단어를 더 공부하고 싶나요?
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KEEP / DISCARD BUTTONS
# =========================================================

keep_col, discard_col = st.columns(2)


# ---------------------------------------------------------
# KEEP
# ---------------------------------------------------------

with keep_col:

    if st.button(
        "📦 보관할래요",
        type="primary",
        use_container_width=True
    ):

        word_id = row["word_id"]

        if word_id not in st.session_state.saved_words[unit]:
            st.session_state.saved_words[unit].append(word_id)

        if word_id in st.session_state.discarded_words[unit]:
            st.session_state.discarded_words[unit].remove(word_id)

        # history
        st.session_state.word_history[unit].append({
            "word_id": word_id,
            "action": "saved"
        })

        # 다음 카드
        st.session_state.word_positions[unit] += 1

        st.rerun()


# ---------------------------------------------------------
# DISCARD
# ---------------------------------------------------------

with discard_col:

    if st.button(
        "🗑️ 버릴래요",
        use_container_width=True
    ):

        word_id = row["word_id"]

        if word_id not in st.session_state.discarded_words[unit]:
            st.session_state.discarded_words[unit].append(word_id)

        if word_id in st.session_state.saved_words[unit]:
            st.session_state.saved_words[unit].remove(word_id)

        # history
        st.session_state.word_history[unit].append({
            "word_id": word_id,
            "action": "discarded"
        })

        # 다음 카드
        st.session_state.word_positions[unit] += 1

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

            previous_id = last_action["word_id"]

            if last_action["action"] == "saved":

                if previous_id in st.session_state.saved_words[unit]:
                    st.session_state.saved_words[unit].remove(
                        previous_id
                    )

            elif last_action["action"] == "discarded":

                if previous_id in st.session_state.discarded_words[unit]:
                    st.session_state.discarded_words[unit].remove(
                        previous_id
                    )

            st.session_state.word_positions[unit] = max(
                0,
                st.session_state.word_positions[unit] - 1
            )

            st.rerun()


# =========================================================
# SMALL STATUS
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
