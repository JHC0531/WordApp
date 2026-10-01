import streamlit as st
import pandas as pd
import json
import html
import streamlit.components.v1 as components

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="발음짱이 될거야",
    page_icon="🐥",
    layout="centered"
)

# =========================================================
# LOAD WORD DATA
# =========================================================

@st.cache_data
def load_words():
    df = pd.read_csv("data/wordlist_1001.csv")
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
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"CSV에 다음 열이 없습니다: {missing}"
        )

    return df


try:
    df = load_words()

except Exception as e:
    st.error("단어 파일을 불러오지 못했어요.")
    st.code(str(e))
    st.stop()

# =========================================================
# CONVERT CSV -> JAVASCRIPT DATA
# =========================================================

word_data = []

for _, row in df.iterrows():

    word_data.append({
        "id": str(row["word_id"]),
        "unit": str(row["unit"]),
        "text": str(row["word"]),
        "meaning": str(row["meaning"]),
        "example": str(row["example"]),
        "caution": str(row["pronunciation_caution"])
    })

WORDS_JSON = json.dumps(
    word_data,
    ensure_ascii=False
)

# =========================================================
# GOOGLE FORM
# =========================================================
#
# 기존 Claude Artifact에 있던 Google Form 값을 그대로 넣었어요.
# 나중에 연구 기록 방식을 바꾸고 싶으면 이 부분만 수정하면 됩니다.
#

FORM_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLScO37vlswQSm6N-mqx1w5VrYeCnsao1JVlK-WqzJME82imV-A/viewform"
)

FORM_NAME_ENTRY = "entry.1598372142"
FORM_SCORE_ENTRY = "entry.1041762124"

# =========================================================
# HTML / CSS / JAVASCRIPT
# =========================================================

practice_html = f"""
<!DOCTYPE html>
<html lang="ko">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>멍멍 발음 친구</title>

<link
    rel="preconnect"
    href="https://fonts.googleapis.com"
>

<link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Jua&family=Noto+Sans+KR:wght@400;500;700;900&display=swap"
>

<style>

:root {{

    --bg: #FFF8EE;

    --surface: #FFFFFF;

    --surface2: #FFF1DC;

    --ink: #3A2E27;

    --soft: #8A7A6B;

    --accent: #FF9A4D;

    --accent-dark: #E67E2E;

    --sky: #5BC0EB;

    --success: #3FAE68;

    --success-soft: #E3F8EA;

    --retry: #E8825C;

    --retry-soft: #FFF0E9;

    --line: #F0DEC5;

    --water1: #D8F4FB;

    --water2: #AEE5F3;

    --water3: #73C8E4;

    --stone: #A38D76;

    --stone-dark: #776451;

    --dog: #E8A765;

    --dog-dark: #C9823E;

}}

* {{
    box-sizing: border-box;
}}

html,
body {{

    margin: 0;

    padding: 0;

    background: var(--bg);

    color: var(--ink);

    font-family:
        "Noto Sans KR",
        sans-serif;
}}

body {{

    padding: 16px;

    display: flex;

    justify-content: center;
}}

.page {{

    width: 100%;

    max-width: 520px;

    display: flex;

    flex-direction: column;

    gap: 14px;
}}

/* =============================================
   TOP
============================================= */

.topbar {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 8px;
}}

.brand {{

    display: flex;

    align-items: center;

    gap: 8px;

    font-family: "Jua", sans-serif;

    font-size: 20px;

    color: var(--accent-dark);
}}

.brand-icon {{

    font-size: 27px;
}}

.student-label {{

    display: block;

    margin-top: 2px;

    font-family: "Noto Sans KR", sans-serif;

    font-size: 11px;

    font-weight: 500;

    color: var(--soft);
}}

.score {{

    background: var(--surface2);

    border-radius: 999px;

    padding: 7px 12px;

    font-family: "Jua", sans-serif;

    font-size: 13px;

    color: #734014;

    white-space: nowrap;
}}

/* =============================================
   UNIT POND
============================================= */

.pond-view {{

    display: flex;

    flex-direction: column;

    gap: 14px;
}}

.speech-bubble {{

    background: white;

    border: 2px solid var(--line);

    border-radius: 19px;

    padding: 11px 14px;

    text-align: center;

    font-family: "Jua", sans-serif;

    font-size: 15px;

    line-height: 1.5;
}}

.pond {{

    position: relative;

    overflow: hidden;

    border-radius: 32px;

    padding: 28px 18px;

    background:
        linear-gradient(
            165deg,
            var(--water1),
            var(--water2) 55%,
            var(--water3)
        );

    box-shadow:
        0 8px 24px rgba(58,46,39,.14);
}}

.pond-path {{

    position: relative;

    z-index: 2;

    display: flex;

    flex-direction: column;

    align-items: center;

    gap: 10px;
}}

.stone {{

    width: 122px;

    min-height: 65px;

    border: 0;

    border-radius:
        48% 52% 50% 50% /
        58% 46% 54% 42%;

    padding: 8px 10px;

    background:
        linear-gradient(
            160deg,
            var(--stone),
            var(--stone-dark)
        );

    color: #FFF8EE;

    font-family: "Jua", sans-serif;

    font-size: 14px;

    cursor: pointer;

    box-shadow:
        0 5px 0 var(--stone-dark),
        0 9px 16px rgba(0,0,0,.17);

    transition: .15s;
}}

.stone:nth-child(odd) {{

    transform: translateX(-32px);
}}

.stone:nth-child(even) {{

    transform: translateX(32px);
}}

.stone:hover {{

    margin-top: -3px;

    margin-bottom: 3px;
}}

.pond-hint {{

    text-align: center;

    color: var(--soft);

    font-size: 12px;
}}

/* =============================================
   PRACTICE HEADER
============================================= */

.practice-view {{

    display: flex;

    flex-direction: column;

    gap: 13px;
}}

.progress-top {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 8px;

    color: var(--soft);

    font-size: 12px;
}}

.progress-links {{

    display: flex;

    gap: 10px;
}}

.text-button {{

    padding: 0;

    border: 0;

    background: transparent;

    color: var(--soft);

    font-size: 12px;

    text-decoration: underline;

    cursor: pointer;
}}

.progress-track {{

    height: 9px;

    overflow: hidden;

    border-radius: 999px;

    background: var(--surface2);
}}

.progress-fill {{

    height: 100%;

    width: 0%;

    border-radius: 999px;

    background: var(--accent);

    transition: width .3s ease;
}}

/* =============================================
   DOG
============================================= */

.stage {{

    position: relative;

    overflow: hidden;

    display: flex;

    flex-direction: column;

    align-items: center;

    min-height: 315px;

    padding: 18px 15px 5px;

    border-radius: 28px;

    background:
        linear-gradient(
            180deg,
            var(--surface2),
            white
        );

    box-shadow:
        0 8px 24px rgba(58,46,39,.12);
}}

.dog-wrap {{

    position: relative;

    width: 225px;

    height: 225px;

    margin-top: 4px;
}}

.dog-svg {{

    width: 100%;

    height: 100%;

    overflow: visible;
}}

.ear,
.tail,
.head-group {{

    transform-box: fill-box;
}}

.ear {{

    transform-origin: top center;
}}

.tail {{

    transform-origin: 20% 60%;
}}

.dog-wrap[data-state="idle"] .tail {{

    animation:
        tailSway 2.4s ease-in-out infinite;
}}

.dog-wrap[data-state="listening"] .ear-left {{

    animation:
        earLeft .7s ease-in-out infinite alternate;
}}

.dog-wrap[data-state="listening"] .ear-right {{

    animation:
        earRight .7s ease-in-out infinite alternate;
}}

.dog-wrap[data-state="happy"] .tail {{

    animation:
        tailWag .24s ease-in-out infinite;
}}

.dog-wrap[data-state="happy"] .head-group {{

    animation:
        happyHop .45s ease-in-out 2;
}}

.dog-wrap[data-state="confused"] .head-group {{

    animation:
        confusedTilt .65s ease-in-out;
}}

@keyframes tailSway {{

    0%,100% {{
        transform: rotate(-5deg);
    }}

    50% {{
        transform: rotate(12deg);
    }}
}}

@keyframes tailWag {{

    0%,100% {{
        transform: rotate(-17deg);
    }}

    50% {{
        transform: rotate(18deg);
    }}
}}

@keyframes earLeft {{

    from {{
        transform: rotate(0deg);
    }}

    to {{
        transform: rotate(-12deg);
    }}
}}

@keyframes earRight {{

    from {{
        transform: rotate(0deg);
    }}

    to {{
        transform: rotate(12deg);
    }}
}}

@keyframes happyHop {{

    0%,100% {{
        transform: translateY(0);
    }}

    50% {{
        transform: translateY(-13px);
    }}
}}

@keyframes confusedTilt {{

    0% {{
        transform: rotate(0deg);
    }}

    50% {{
        transform: rotate(7deg);
    }}

    100% {{
        transform: rotate(0deg);
    }}
}}

/* =============================================
   WORD CARD
============================================= */

.word-card {{

    display: flex;

    flex-direction: column;

    gap: 7px;

    padding: 16px 17px;

    border: 2px solid var(--line);

    border-radius: 21px;

    background: white;
}}

.unit-badge {{

    align-self: flex-start;

    padding: 3px 10px;

    border-radius: 999px;

    background: var(--surface2);

    color: #70431E;

    font-size: 11px;

    font-weight: 700;
}}

.word-text {{

    font-family:
        "Baloo 2",
        sans-serif;

    font-size: 32px;

    font-weight: 800;

    line-height: 1.1;
}}

.word-meaning {{

    color: var(--soft);

    font-size: 14px;
}}

.word-example {{

    color: var(--soft);

    font-size: 12.5px;

    font-style: italic;

    line-height: 1.5;
}}

/* =============================================
   MIC
============================================= */

.mic-btn {{

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 9px;

    width: 100%;

    padding: 16px;

    border: 0;

    border-radius: 999px;

    background: var(--accent);

    color: #5A2E0A;

    font-family: "Jua", sans-serif;

    font-size: 18px;

    cursor: pointer;

    box-shadow:
        0 6px 0 var(--accent-dark);
}}

.mic-btn:active {{

    transform: translateY(4px);

    box-shadow:
        0 2px 0 var(--accent-dark);
}}

.mic-btn.listening {{

    background: var(--sky);

    box-shadow:
        0 6px 0 #3299BF;

    animation:
        micPulse .9s ease-in-out infinite;
}}

@keyframes micPulse {{

    0%,100% {{
        transform: scale(1);
    }}

    50% {{
        transform: scale(1.025);
    }}
}}

.mic-btn:disabled {{

    opacity: .55;

    cursor: not-allowed;

    box-shadow: none;
}}

.hint {{

    margin: 0;

    text-align: center;

    color: var(--soft);

    font-size: 11.5px;
}}

/* =============================================
   FEEDBACK
============================================= */

.feedback {{

    display: flex;

    flex-direction: column;

    gap: 8px;

    padding: 14px 16px;

    border: 2px solid var(--line);

    border-radius: 18px;

    background: white;
}}

.feedback.correct {{

    border-color: var(--success);

    background: var(--success-soft);
}}

.feedback.retry {{

    border-color: var(--retry);

    background: var(--retry-soft);
}}

.heard {{

    margin: 0;

    color: var(--soft);

    font-size: 13px;
}}

.heard b {{

    color: var(--ink);

    font-family:
        "Baloo 2",
        sans-serif;

    font-size: 16px;
}}

.verdict {{

    margin: 0;

    font-family:
        "Jua",
        sans-serif;

    font-size: 16px;
}}

.feedback-actions {{

    display: flex;

    gap: 8px;
}}

.btn-primary,
.btn-secondary,
.btn-blue {{

    flex: 1;

    border: 0;

    border-radius: 999px;

    padding: 12px 13px;

    font-family:
        "Noto Sans KR",
        sans-serif;

    font-size: 13px;

    font-weight: 700;

    cursor: pointer;
}}

.btn-primary {{

    background: var(--success);

    color: white;
}}

.btn-secondary {{

    background: var(--surface2);

    color: var(--ink);
}}

.btn-blue {{

    background: var(--sky);

    color: #163E4D;
}}

/* =============================================
   UNSUPPORTED
============================================= */

.unsupported {{

    padding: 13px;

    border: 2px solid var(--retry);

    border-radius: 16px;

    background: var(--retry-soft);

    text-align: center;

    font-size: 13px;

    line-height: 1.6;
}}

/* =============================================
   OVERLAY
============================================= */

.overlay {{

    position: fixed;

    inset: 0;

    z-index: 99;

    display: flex;

    justify-content: center;

    align-items: center;

    padding: 20px;

    background:
        rgba(0,0,0,.42);
}}

.overlay-card {{

    width: 100%;

    max-width: 330px;

    padding: 27px 23px;

    border-radius: 25px;

    background: white;

    text-align: center;

    box-shadow:
        0 14px 35px rgba(0,0,0,.2);
}}

.overlay-emoji {{

    font-size: 53px;
}}

.overlay-card h2 {{

    margin:
        7px 0 5px;

    font-family:
        "Jua",
        sans-serif;
}}

.overlay-card p {{

    margin:
        0 0 15px;

    color: var(--soft);

    font-size: 13px;

    line-height: 1.55;
}}

.name-input {{

    width: 100%;

    margin-bottom: 12px;

    padding: 12px 13px;

    border: 2px solid var(--line);

    border-radius: 14px;

    font-size: 16px;
}}

.big-score {{

    margin: 3px 0;

    color: var(--success);

    font-family:
        "Baloo 2",
        sans-serif;

    font-size: 35px;

    font-weight: 800;
}}

.rate-box {{

    margin:
        10px 0 17px;

    padding: 11px;

    border-radius: 15px;

    background: #F4FAFF;

    color: #426275;

    font-size: 13px;
}}

.result-actions {{

    display: flex;

    flex-direction: column;

    gap: 9px;
}}

[hidden] {{

    display: none !important;
}}

</style>

</head>

<body>

<div class="page">

    <!-- =========================================
         TOP
    ========================================== -->

    <header class="topbar">

        <div class="brand">

            <div class="brand-icon">
                🐶
            </div>

            <div>

                멍멍 발음 친구

                <span
                    class="student-label"
                    id="studentLabel"
                ></span>

            </div>

        </div>

        <div
            class="score"
            id="scoreDisplay"
        >
            콩이가 알아들은 단어 0개
        </div>

    </header>

    <!-- =========================================
         UNIT SELECTION
    ========================================== -->

    <div
        class="pond-view"
        id="pondView"
        hidden
    >

        <div class="speech-bubble">

            🐾 어느 유닛부터 건너볼까?

        </div>

        <div class="pond">

            <div
                class="pond-path"
                id="stonesContainer"
            ></div>

        </div>

        <div class="pond-hint">

            돌다리를 누르면 그 Unit의
            모든 단어를 발음 연습해요 🎤

        </div>

    </div>

    <!-- =========================================
         PRACTICE
    ========================================== -->

    <div
        class="practice-view"
        id="practiceView"
        hidden
    >

        <div class="progress-top">

            <span>

                진행

                <b id="progressCurrent">
                    1
                </b>

                /

                <span id="progressTotal">
                    1
                </span>

            </span>

            <div class="progress-links">

                <button
                    class="text-button"
                    id="backToPondBtn"
                    type="button"
                >
                    유닛 바꾸기
                </button>

                <button
                    class="text-button"
                    id="finishBtn"
                    type="button"
                >
                    결과 보기
                </button>

            </div>

        </div>

        <div class="progress-track">

            <div
                class="progress-fill"
                id="progressFill"
            ></div>

        </div>

        <!-- DOG -->

        <section class="stage">

            <div
                class="speech-bubble"
                id="speechBubble"
            >

                안녕! 나는 콩이야.
                아래 단어를 나한테 말해줘! 🐾

            </div>

            <div
                class="dog-wrap"
                id="dogWrap"
                data-state="idle"
            >

                <svg
                    class="dog-svg"
                    viewBox="0 0 240 260"
                    aria-hidden="true"
                >

                    <!-- tail -->

                    <path
                        class="tail"
                        d="
                        M182 188
                        C214 176,
                        226 146,
                        208 124
                        C222 142,
                        216 174,
                        190 194 Z
                        "
                        fill="var(--dog)"
                    />

                    <!-- body -->

                    <ellipse
                        cx="120"
                        cy="206"
                        rx="76"
                        ry="46"
                        fill="var(--dog)"
                    />

                    <ellipse
                        cx="93"
                        cy="244"
                        rx="17"
                        ry="11"
                        fill="white"
                    />

                    <ellipse
                        cx="147"
                        cy="244"
                        rx="17"
                        ry="11"
                        fill="white"
                    />

                    <!-- HEAD -->

                    <g class="head-group">

                        <circle
                            cx="120"
                            cy="118"
                            r="78"
                            fill="var(--dog)"
                        />

                        <path
                            class="ear ear-left"
                            d="
                            M65 55
                            C25 70,
                            15 118,
                            48 175
                            C67 208,
                            42 95,
                            78 100 Z
                            "
                            fill="var(--dog-dark)"
                        />

                        <path
                            class="ear ear-right"
                            d="
                            M175 55
                            C215 70,
                            225 118,
                            192 175
                            C173 208,
                            198 95,
                            162 100 Z
                            "
                            fill="var(--dog-dark)"
                        />

                        <!-- cheeks -->

                        <ellipse
                            cx="80"
                            cy="138"
                            rx="15"
                            ry="9"
                            fill="#FF6E6E"
                            opacity=".35"
                        />

                        <ellipse
                            cx="160"
                            cy="138"
                            rx="15"
                            ry="9"
                            fill="#FF6E6E"
                            opacity=".35"
                        />

                        <!-- muzzle -->

                        <ellipse
                            cx="120"
                            cy="146"
                            rx="40"
                            ry="29"
                            fill="white"
                        />

                        <!-- nose -->

                        <ellipse
                            cx="120"
                            cy="130"
                            rx="11"
                            ry="8"
                            fill="#30231C"
                        />

                        <!-- eyes -->

                        <g id="normalEyes">

                            <circle
                                cx="90"
                                cy="103"
                                r="8"
                                fill="#17120F"
                            />

                            <circle
                                cx="150"
                                cy="103"
                                r="8"
                                fill="#17120F"
                            />

                            <circle
                                cx="92.5"
                                cy="100"
                                r="2.2"
                                fill="white"
                            />

                            <circle
                                cx="152.5"
                                cy="100"
                                r="2.2"
                                fill="white"
                            />

                        </g>

                        <g
                            id="happyEyes"
                            hidden
                        >

                            <path
                                d="M80 106 Q90 92 100 106"
                                stroke="#17120F"
                                stroke-width="6"
                                stroke-linecap="round"
                                fill="none"
                            />

                            <path
                                d="M140 106 Q150 92 160 106"
                                stroke="#17120F"
                                stroke-width="6"
                                stroke-linecap="round"
                                fill="none"
                            />

                        </g>

                        <!-- mouth -->

                        <g id="normalMouth">

                            <path
                                d="M104 160 Q120 170 136 160"
                                stroke="#3A2E27"
                                stroke-width="4"
                                stroke-linecap="round"
                                fill="none"
                            />

                        </g>

                        <g
                            id="happyMouth"
                            hidden
                        >

                            <path
                                d="
                                M98 158
                                Q120 192
                                142 158 Z
                                "
                                fill="#3A2E27"
                            />

                            <ellipse
                                cx="120"
                                cy="176"
                                rx="13"
                                ry="9"
                                fill="#FF9AA6"
                            />

                        </g>

                    </g>

                </svg>

            </div>

        </section>

        <!-- WORD -->

        <section class="word-card">

            <span
                class="unit-badge"
                id="wordUnit"
            ></span>

            <span
                class="word-text"
                id="wordText"
            ></span>

            <span
                class="word-meaning"
                id="wordMeaning"
            ></span>

            <span
                class="word-example"
                id="wordExample"
            ></span>

        </section>

        <!-- MIC -->

        <button
            class="mic-btn"
            id="micBtn"
            type="button"
        >

            🎙️

            <span id="micLabel">
                눌러서 말해보세요
            </span>

        </button>

        <p
            class="hint"
            id="hintText"
        >

            Chrome 브라우저 권장 ·
            마이크 사용을 허용해주세요

        </p>

        <!-- FEEDBACK -->

        <section
            class="feedback"
            id="feedback"
            hidden
        >

            <p
                class="heard"
                id="heardText"
            ></p>

            <p
                class="verdict"
                id="verdictText"
            ></p>

            <div class="feedback-actions">

                <button
                    class="btn-secondary"
                    id="retryBtn"
                    type="button"
                    hidden
                >
                    🎙️ 다시 말하기
                </button>

                <button
                    class="btn-primary"
                    id="nextBtn"
                    type="button"
                    hidden
                >
                    다음 단어 ▶
                </button>

            </div>

        </section>

        <!-- UNSUPPORTED -->

        <div
            class="unsupported"
            id="unsupportedBox"
            hidden
        >

            🙈 이 브라우저에서는
            음성 인식을 사용할 수 없어요.<br>

            최신 Chrome 브라우저에서
            다시 열어주세요.

        </div>

    </div>

</div>

<!-- =============================================
     NAME OVERLAY
============================================= -->

<div
    class="overlay"
    id="nameOverlay"
>

    <div class="overlay-card">

        <div class="overlay-emoji">
            🐶
        </div>

        <h2>
            콩이랑 연습할 준비됐나요?
        </h2>

        <p>
            이름을 입력한 뒤
            발음 연습을 시작해요.
        </p>

        <input
            class="name-input"
            id="nameInput"
            type="text"
            maxlength="20"
            placeholder="이름"
        >

        <button
            class="btn-primary"
            id="startBtn"
            type="button"
            style="
            width:100%;
            font-size:15px;
            "
        >
            🐾 연습 시작하기
        </button>

    </div>

</div>

<!-- =============================================
     RESULTS
============================================= -->

<div
    class="overlay"
    id="resultOverlay"
    hidden
>

    <div class="overlay-card">

        <div class="overlay-emoji">
            🏆
        </div>

        <h2 id="resultName">
            수고했어요!
        </h2>

        <div
            class="big-score"
            id="resultScore"
        >
            0 / 0
        </div>

        <p>
            콩이가 목표 단어로 알아들은 횟수예요.
        </p>

        <div
            class="rate-box"
            id="resultRate"
        ></div>

        <div class="result-actions">

            <button
                class="btn-blue"
                id="recordBtn"
                type="button"
            >
                📋 결과 기록하기
            </button>

            <button
                class="btn-secondary"
                id="anotherUnitBtn"
                type="button"
            >
                🪨 다른 Unit 연습하기
            </button>

            <button
                class="btn-primary"
                id="retryUnitBtn"
                type="button"
            >
                🐶 같은 Unit 다시 연습
            </button>

        </div>

    </div>

</div>

<script>

(function() {{

// =========================================================
// WORD DATA FROM STREAMLIT CSV
// =========================================================

const WORDS_ALL = {WORDS_JSON};

const FORM_CONFIG = {{

    baseUrl:
        {json.dumps(FORM_URL)},

    nameEntry:
        {json.dumps(FORM_NAME_ENTRY)},

    scoreEntry:
        {json.dumps(FORM_SCORE_ENTRY)}

}};

// =========================================================
// STATE
// =========================================================

const state = {{

    name: "",

    currentUnit: "",

    words: [],

    index: 0,

    recognized: new Set(),

    attempted: new Set(),

    listening: false

}};

// =========================================================
// ELEMENTS
// =========================================================

const els = {{

    studentLabel:
        document.getElementById("studentLabel"),

    score:
        document.getElementById("scoreDisplay"),

    pondView:
        document.getElementById("pondView"),

    stones:
        document.getElementById("stonesContainer"),

    practiceView:
        document.getElementById("practiceView"),

    progressCurrent:
        document.getElementById("progressCurrent"),

    progressTotal:
        document.getElementById("progressTotal"),

    progressFill:
        document.getElementById("progressFill"),

    backToPond:
        document.getElementById("backToPondBtn"),

    finish:
        document.getElementById("finishBtn"),

    bubble:
        document.getElementById("speechBubble"),

    dog:
        document.getElementById("dogWrap"),

    normalEyes:
        document.getElementById("normalEyes"),

    happyEyes:
        document.getElementById("happyEyes"),

    normalMouth:
        document.getElementById("normalMouth"),

    happyMouth:
        document.getElementById("happyMouth"),

    wordUnit:
        document.getElementById("wordUnit"),

    wordText:
        document.getElementById("wordText"),

    wordMeaning:
        document.getElementById("wordMeaning"),

    wordExample:
        document.getElementById("wordExample"),

    mic:
        document.getElementById("micBtn"),

    micLabel:
        document.getElementById("micLabel"),

    hint:
        document.getElementById("hintText"),

    feedback:
        document.getElementById("feedback"),

    heard:
        document.getElementById("heardText"),

    verdict:
        document.getElementById("verdictText"),

    retry:
        document.getElementById("retryBtn"),

    next:
        document.getElementById("nextBtn"),

    unsupported:
        document.getElementById("unsupportedBox"),

    nameOverlay:
        document.getElementById("nameOverlay"),

    nameInput:
        document.getElementById("nameInput"),

    start:
        document.getElementById("startBtn"),

    resultOverlay:
        document.getElementById("resultOverlay"),

    resultName:
        document.getElementById("resultName"),

    resultScore:
        document.getElementById("resultScore"),

    resultRate:
        document.getElementById("resultRate"),

    record:
        document.getElementById("recordBtn"),

    anotherUnit:
        document.getElementById("anotherUnitBtn"),

    retryUnit:
        document.getElementById("retryUnitBtn")

}};

// =========================================================
// UNIT LIST
// =========================================================

const preferredUnits = [

    "Unit 4",

    "Unit 5",

    "Unit 6",

    "Unit 7",

    "Special Reading 1",

    "Special Reading 2"

];

const availableUnits = [

    ...new Set(
        WORDS_ALL.map(
            w => w.unit
        )
    )

];

const units = preferredUnits.filter(
    u => availableUnits.includes(u)
);

availableUnits.forEach(
    function(u) {{

        if (!units.includes(u)) {{

            units.push(u);

        }}

    }}
);

// =========================================================
// DOG
// =========================================================

function setDogState(stateName) {{

    els.dog.setAttribute(
        "data-state",
        stateName
    );

    const happy =
        stateName === "happy";

    els.normalEyes.hidden =
        happy;

    els.happyEyes.hidden =
        !happy;

    els.normalMouth.hidden =
        happy;

    els.happyMouth.hidden =
        !happy;

}}

// =========================================================
// UNIT STONES
// =========================================================

function unitShortName(unit) {{

    return unit.replace(
        "Special Reading",
        "Reading"
    );

}}

function renderUnits() {{

    els.stones.innerHTML = "";

    units.forEach(

        function(unit) {{

            const count =
                WORDS_ALL.filter(
                    w => w.unit === unit
                ).length;

            const button =
                document.createElement(
                    "button"
                );

            button.type =
                "button";

            button.className =
                "stone";

            button.innerHTML =
                unitShortName(unit)
                +
                "<br>"
                +
                count
                +
                " words";

            button.addEventListener(
                "click",
                function() {{

                    selectUnit(
                        unit
                    );

                }}
            );

            els.stones.appendChild(
                button
            );

        }}

    );

}}

// =========================================================
// SELECT UNIT
// =========================================================

function selectUnit(unit) {{

    state.currentUnit =
        unit;

    state.words =
        WORDS_ALL.filter(
            w => w.unit === unit
        );

    state.index = 0;

    state.recognized =
        new Set();

    state.attempted =
        new Set();

    els.pondView.hidden =
        true;

    els.practiceView.hidden =
        false;

    els.progressTotal.textContent =
        state.words.length;

    updateScore();

    loadWord(0);

}}

// =========================================================
// SCORE
// =========================================================

function updateScore() {{

    els.score.textContent =
        "콩이가 알아들은 단어 "
        +
        state.recognized.size
        +
        "개";

}}

// =========================================================
// PROGRESS
// =========================================================

function updateProgress() {{

    els.progressCurrent.textContent =
        state.index + 1;

    const percent =
        (
            (state.index + 1)
            /
            state.words.length
        )
        * 100;

    els.progressFill.style.width =
        Math.max(
            4,
            percent
        )
        +
        "%";

}}

// =========================================================
// LOAD WORD
// =========================================================

function loadWord(index) {{

    state.index =
        index;

    const word =
        state.words[index];

    els.wordUnit.textContent =
        word.unit;

    els.wordText.textContent =
        word.text;

    els.wordMeaning.textContent =
        word.meaning;

    els.wordExample.textContent =
        word.example;

    els.feedback.hidden =
        true;

    els.feedback.className =
        "feedback";

    els.retry.hidden =
        true;

    els.next.hidden =
        true;

    els.mic.disabled =
        false;

    els.micLabel.textContent =
        "눌러서 말해보세요";

    els.bubble.textContent =
        "이 단어를 나한테 말해줘! 🎧";

    setDogState(
        "idle"
    );

    updateProgress();

}}

// =========================================================
// NORMALIZE
// =========================================================

function normalize(text) {{

    return (
        text || ""
    )
    .toLowerCase()
    .replace(
        /[^a-z' ]/g,
        " "
    )
    .replace(
        /\\s+/g,
        " "
    )
    .trim();

}}

// =========================================================
// ASR MATCH
// =========================================================

function isMatch(
    transcript,
    target
) {{

    const heard =
        normalize(
            transcript
        );

    const expected =
        normalize(
            target
        );

    if (!heard) {{

        return false;

    }}

    if (
        heard === expected
    ) {{

        return true;

    }}

    /*
    단일 단어의 경우

    "I said astronaut"

    처럼 주변 단어가 함께 인식된 경우에도
    목표 단어가 들어 있으면 인정합니다.
    */

    if (
        !expected.includes(" ")
    ) {{

        const tokens =
            heard.split(" ");

        return tokens.includes(
            expected
        );

    }}

    /*
    구/표현의 경우에는
    전체 표현이 연속해서 인식되어야 합니다.
    */

    return heard.includes(
        expected
    );

}}

// =========================================================
// RECOGNIZED
// =========================================================

function showRecognized(
    heardWord
) {{

    state.attempted.add(
        state.index
    );

    state.recognized.add(
        state.index
    );

    updateScore();

    setDogState(
        "happy"
    );

    els.bubble.textContent =
        "멍멍! 내가 알아들었어! 🎉";

    els.feedback.hidden =
        false;

    els.feedback.className =
        "feedback correct";

    els.heard.innerHTML =
        '콩이가 들은 말: <b>"'
        +
        heardWord
        +
        '"</b>';

    els.verdict.textContent =
        "목표 단어로 인식되었어요! 👏";

    els.retry.hidden =
        true;

    els.next.hidden =
        false;

    els.mic.disabled =
        true;

    els.micLabel.textContent =
        "인식 완료!";

}}

// =========================================================
// RETRY
// =========================================================

function showRetry(
    heardWord
) {{

    state.attempted.add(
        state.index
    );

    setDogState(
        "confused"
    );

    els.bubble.textContent =
        "음... 이번에는 다르게 들렸어 🤔";

    els.feedback.hidden =
        false;

    els.feedback.className =
        "feedback retry";

    if (
        heardWord
    ) {{

        els.heard.innerHTML =
            '콩이가 들은 말: <b>"'
            +
            heardWord
            +
            '"</b>';

    }}

    else {{

        els.heard.textContent =
            "이번에는 소리를 인식하지 못했어요.";

    }}

    els.verdict.textContent =
        "다시 한 번 말해볼까요?";

    els.retry.hidden =
        false;

    els.next.hidden =
        false;

    els.mic.disabled =
        false;

    els.micLabel.textContent =
        "눌러서 다시 말해보세요";

}}

// =========================================================
// NEXT
// =========================================================

els.next.addEventListener(

    "click",

    function() {{

        if (
            state.index
            >=
            state.words.length - 1
        ) {{

            finishSession();

        }}

        else {{

            loadWord(
                state.index + 1
            );

        }}

    }}

);

// =========================================================
// RETRY BUTTON
// =========================================================

els.retry.addEventListener(

    "click",

    function() {{

        els.feedback.hidden =
            true;

        els.retry.hidden =
            true;

        els.next.hidden =
            true;

        setDogState(
            "idle"
        );

        els.bubble.textContent =
            "괜찮아! 다시 한번 말해줘 🐾";

    }}

);

// =========================================================
// RESULT
// =========================================================

function finishSession() {{

    const attempted =
        state.attempted.size;

    const recognized =
        state.recognized.size;

    const rate =
        attempted > 0
        ?
        Math.round(
            recognized
            /
            attempted
            *
            100
        )
        :
        0;

    els.resultName.textContent =
        (
            state.name
            ?
            state.name + "님, "
            :
            ""
        )
        +
        "수고했어요!";

    els.resultScore.textContent =
        recognized
        +
        " / "
        +
        attempted;

    els.resultRate.innerHTML =
        "🐶 콩이가 목표 단어로 알아들은 비율 "
        +
        "<b>"
        +
        rate
        +
        "%</b>"
        +
        "<br><br>"
        +
        "<span style='font-size:11px;color:#8A7A6B;'>"
        +
        "※ 이 수치는 발음 점수가 아니라 "
        +
        "음성 인식 시스템이 목표 단어로 "
        +
        "인식한 비율이에요."
        +
        "</span>";

    els.resultOverlay.hidden =
        false;

}}

// =========================================================
// FINISH BUTTON
// =========================================================

els.finish.addEventListener(

    "click",

    finishSession

);

// =========================================================
// BACK TO UNIT
// =========================================================

function goToUnits() {{

    els.resultOverlay.hidden =
        true;

    els.practiceView.hidden =
        true;

    els.pondView.hidden =
        false;

}}

els.backToPond.addEventListener(

    "click",

    goToUnits

);

els.anotherUnit.addEventListener(

    "click",

    goToUnits

);

// =========================================================
// RETRY SAME UNIT
// =========================================================

els.retryUnit.addEventListener(

    "click",

    function() {{

        els.resultOverlay.hidden =
            true;

        selectUnit(
            state.currentUnit
        );

    }}

);

// =========================================================
// GOOGLE FORM
// =========================================================

els.record.addEventListener(

    "click",

    function() {{

        const attempted =
            state.attempted.size;

        const recognized =
            state.recognized.size;

        const score =
            recognized
            +
            "/"
            +
            attempted;

        const studentAndUnit =
            state.name
            +
            " ("
            +
            state.currentUnit
            +
            ")";

        const params =
            new URLSearchParams();

        params.set(
            "usp",
            "pp_url"
        );

        params.set(
            FORM_CONFIG.nameEntry,
            studentAndUnit
        );

        params.set(
            FORM_CONFIG.scoreEntry,
            score
        );

        const url =
            FORM_CONFIG.baseUrl
            +
            "?"
            +
            params.toString();

        window.open(
            url,
            "_blank"
        );

    }}

);

// =========================================================
// NAME
// =========================================================

function beginSession() {{

    const name =
        els.nameInput.value.trim();

    if (!name) {{

        els.nameInput.focus();

        return;

    }}

    state.name =
        name;

    els.studentLabel.textContent =
        name
        +
        " 학생 연습 중";

    els.nameOverlay.hidden =
        true;

    renderUnits();

    els.pondView.hidden =
        false;

}}

els.start.addEventListener(

    "click",

    beginSession

);

els.nameInput.addEventListener(

    "keydown",

    function(event) {{

        if (
            event.key === "Enter"
        ) {{

            beginSession();

        }}

    }}

);

// =========================================================
// SPEECH RECOGNITION
// =========================================================

const SpeechRecognition =
    window.SpeechRecognition
    ||
    window.webkitSpeechRecognition;

const recognitionSupported =
    !!SpeechRecognition;

let recognition =
    null;


if (
    recognitionSupported
) {{

    recognition =
        new SpeechRecognition();

    recognition.lang =
        "en-US";

    recognition.interimResults =
        false;

    recognition.maxAlternatives =
        5;

    recognition.continuous =
        false;


    recognition.onstart =
        function() {{

            state.listening =
                true;

            setDogState(
                "listening"
            );

            els.mic.classList.add(
                "listening"
            );

            els.micLabel.textContent =
                "콩이가 듣는 중...";

            els.bubble.textContent =
                "귀 기울이고 있어... 🎧";

            els.feedback.hidden =
                true;

        };


    recognition.onresult =
        function(event) {{

            const result =
                event.results[0];

            const alternatives =
                [];

            for (
                let i = 0;
                i < result.length;
                i++
            ) {{

                alternatives.push(
                    result[i].transcript
                );

            }}

            const best =
                alternatives[0]
                ||
                "";

            const target =
                state.words[
                    state.index
                ].text;

            const matched =
                alternatives.some(

                    function(text) {{

                        return isMatch(
                            text,
                            target
                        );

                    }}

                );

            if (
                matched
            ) {{

                showRecognized(
                    best.trim()
                );

            }}

            else {{

                showRetry(
                    best.trim()
                );

            }}

        };


    recognition.onerror =
        function(event) {{

            state.listening =
                false;

            els.mic.classList.remove(
                "listening"
            );

            setDogState(
                "idle"
            );

            els.micLabel.textContent =
                "눌러서 말해보세요";


            if (
                event.error
                ===
                "not-allowed"
                ||
                event.error
                ===
                "service-not-allowed"
            ) {{

                els.hint.textContent =
                    "마이크 권한이 필요해요. "
                    +
                    "브라우저 주소창의 마이크 권한을 확인해주세요.";

            }}

            else if (
                event.error
                ===
                "no-speech"
            ) {{

                showRetry(
                    ""
                );

            }}

        };


    recognition.onend =
        function() {{

            state.listening =
                false;

            els.mic.classList.remove(
                "listening"
            );

        };

}}

else {{

    els.unsupported.hidden =
        false;

    els.mic.disabled =
        true;

}}


// =========================================================
// MIC BUTTON
// =========================================================

els.mic.addEventListener(

    "click",

    function() {{

        if (
            !recognitionSupported
        ) {{

            els.unsupported.hidden =
                false;

            return;

        }}

        if (
            state.listening
        ) {{

            return;

        }}

        try {{

            recognition.start();

        }}

        catch(error) {{

            // already started

        }}

    }}

);


// =========================================================
// INITIAL FOCUS
// =========================================================

setTimeout(

    function() {{

        els.nameInput.focus();

    }},

    100

);

}})();

</script>

</body>
</html>
"""

# =========================================================
# DISPLAY
# =========================================================

components.html(
    practice_html,
    height=1150,
    scrolling=True
)
