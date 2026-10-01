import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="말해야 통한다! 발음 놀이터",
    page_icon="🐶",
    layout="centered"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(
            180deg,
            #fffaf4 0%,
            #f6fbff 100%
        );
}

.block-container {
    max-width: 900px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

.home-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 900;
    color: #30405a;
    margin-top: 1.2rem;
    margin-bottom: 0.4rem;
}

.home-subtitle {
    text-align: center;
    color: #667085;
    font-size: 1.05rem;
    line-height: 1.7;
    margin-bottom: 1.7rem;
}

.idea-box {
    background: white;
    border: 2px solid #f3e4c8;
    border-radius: 24px;
    padding: 22px 24px;
    margin-top: 18px;
    margin-bottom: 24px;
    box-shadow: 0 10px 26px rgba(70,60,50,0.07);
}

.idea-title {
    text-align: center;
    font-size: 1.25rem;
    font-weight: 850;
    color: #485467;
    margin-bottom: 10px;
}

.idea-text {
    text-align: center;
    color: #667085;
    font-size: 1rem;
    line-height: 1.8;
}

.step-card {
    background: white;
    border-radius: 22px;
    padding: 18px 20px;
    border: 1px solid #e8ebf0;
    box-shadow: 0 7px 18px rgba(50,60,80,0.05);
    margin-bottom: 14px;
}

.step-title {
    font-size: 1.15rem;
    font-weight: 850;
    color: #344054;
    margin-bottom: 6px;
}

.step-text {
    font-size: 0.95rem;
    color: #667085;
    line-height: 1.6;
}

div.stButton > button {
    border-radius: 18px;
    min-height: 56px;
    font-size: 1rem;
    font-weight: 800;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HERO IMAGE
# =========================================================

st.image(
    "images/말해야 통한다! 발음 놀이터.png",
    use_container_width=True
)

# =========================================================
# INTRO
# =========================================================

st.markdown(
    '<div class="home-title">🐾 말해야 통한다! 발음 놀이터</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
<div class="home-subtitle">
영어 단어를 많이 알고 있어도<br>
상대방이 내 말을 알아듣지 못하면 의사소통하기 어렵겠죠?<br><br>
<b>뜻을 알고, 소리를 듣고, 직접 말해보면서</b><br>
영어를 '아는 것'에서 '말할 수 있는 것'으로 바꿔 봐요!
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# THINKING BOX
# =========================================================

st.markdown(
    """
<div class="idea-box">
<div class="idea-title">
💡 잠깐 생각해 볼까요?
</div>
<div class="idea-text">
나는 영어 단어의 <b>뜻</b>은 아는데<br>
막상 소리 내어 말하면 잘 전달되지 않았던 적이 있나요?<br><br>
발음은 단순히 '예쁘게 말하기'가 아니라<br>
<b>내 말을 상대방이 알아듣게 만드는 연습</b>이에요. 🎧
</div>
</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# LEARNING FLOW
# =========================================================

st.markdown("## 🌱 오늘의 학습 여행")

st.markdown(
    """
<div class="step-card">
<div class="step-title">
🐱 STEP 1. 나만의 단어 고르기
</div>
<div class="step-text">
Unit의 단어를 확인하고,<br>
내가 더 공부하고 싶은 단어를 골라봐요.
</div>
</div>
""",
    unsafe_allow_html=True
)

if st.button(
    "🐱 단어 골라보러 가기",
    use_container_width=True
):
    st.switch_page("pages/01🐱_Wordlist.py")

st.markdown(
    """
<div class="step-card">
<div class="step-title">
🎧 STEP 2. 소리로 익히기
</div>
<div class="step-text">
단어의 뜻만 보지 말고,<br>
직접 듣고 따라 하면서 단어의 소리도 익혀요.
</div>
</div>
""",
    unsafe_allow_html=True
)

if st.button(
    "🎀 Word Learning 시작하기",
    use_container_width=True
):
    st.switch_page("pages/03🎀_Word_Learning_APP.py")

st.markdown(
    """
<div class="step-card">
<div class="step-title">
🐶 STEP 3. 콩이와 발음 도전
</div>
<div class="step-text">
뜻을 이미 알고 있는 단어도 괜찮아요!<br>
콩이에게 직접 말해보고<br>
음성 인식 시스템이 내 말을 어떻게 알아듣는지 확인해 봐요.
</div>
</div>
""",
    unsafe_allow_html=True
)

if st.button(
    "🐥 발음짱이 될거야!",
    type="primary",
    use_container_width=True
):
    st.switch_page("pages/04🐥_발음짱이 될거야.py")

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎧 듣고 · 🗣️ 말하고 · 🔁 다시 도전하기"
)
