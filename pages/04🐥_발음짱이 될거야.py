import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

st.set_page_config(
    page_title="발음짱이 될거야",
    page_icon="🐥",
    layout="centered"
)

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
        "pronunciation_caution",
    ]

    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        raise ValueError(f"CSV에 다음 열이 없습니다: {missing}")

    return df

try:
    df = load_words()
except Exception as e:
    st.error("단어 파일을 불러오지 못했어요.")
    st.code(str(e))
    st.stop()

word_data = []
for _, row in df.iterrows():
    word_data.append({
        "id": str(row["word_id"]),
        "u": str(row["unit"]),
        "t": str(row["word"]),
        "m": str(row["meaning"]),
        "e": str(row["example"]),
        "caution": str(row["pronunciation_caution"]),
    })

WORDS_JSON = json.dumps(word_data, ensure_ascii=False)

practice_html = r"""<title>멍멍 발음 친구</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Jua&family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
<style>
  :root{
    --bg:#FFF8EE;
    --surface:#FFFFFF;
    --surface-2:#FFF1DC;
    --ink:#3A2E27;
    --ink-soft:#8A7A6B;
    --accent:#FF9A4D;
    --accent-dark:#E67E2E;
    --accent-ink:#5A2E0A;
    --sky:#4FB6E0;
    --success:#3FAE68;
    --success-soft:#DFF5E6;
    --miss:#E8825C;
    --miss-soft:#FDEAE1;
    --line:#F0DEC5;
    --shadow:rgba(58,46,39,0.14);
    --water-a:#CDEFF8;
    --water-b:#9FDCEE;
    --water-c:#5FB6D9;
    --stone:#A3907C;
    --stone-dark:#7C6A58;
    --stone-ink:#FFF8EE;
    --lily:#4FAE6E;
    --dog-fur:#E8A765;
    --dog-fur-dark:#C9823E;
    --dog-eye:#17120F;
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --bg:#20180F;
      --surface:#2C2116;
      --surface-2:#38291A;
      --ink:#F6ECDD;
      --ink-soft:#C4AF9A;
      --accent:#FFA75C;
      --accent-dark:#FFB979;
      --accent-ink:#2E1704;
      --sky:#6FCBEF;
      --success:#6BCB8D;
      --success-soft:#22392A;
      --miss:#F0987A;
      --miss-soft:#3B2A21;
      --line:#493725;
      --shadow:rgba(0,0,0,0.45);
      --water-a:#123042;
      --water-b:#184358;
      --water-c:#1F5A78;
      --stone:#6B5B4C;
      --stone-dark:#493D32;
      --stone-ink:#FFEFDC;
      --lily:#3E8F5C;
      --dog-fur:#F0BD7E;
      --dog-fur-dark:#D4934E;
      --dog-eye:#17120F;
    }
  }
  :root[data-theme="dark"]{
    --bg:#20180F;
    --surface:#2C2116;
    --surface-2:#38291A;
    --ink:#F6ECDD;
    --ink-soft:#C4AF9A;
    --accent:#FFA75C;
    --accent-dark:#FFB979;
    --accent-ink:#2E1704;
    --sky:#6FCBEF;
    --success:#6BCB8D;
    --success-soft:#22392A;
    --miss:#F0987A;
    --miss-soft:#3B2A21;
    --line:#493725;
    --shadow:rgba(0,0,0,0.45);
    --water-a:#123042;
    --water-b:#184358;
    --water-c:#1F5A78;
    --stone:#6B5B4C;
    --stone-dark:#493D32;
    --stone-ink:#FFEFDC;
    --lily:#3E8F5C;
    --dog-fur:#F0BD7E;
    --dog-fur-dark:#D4934E;
    --dog-eye:#17120F;
  }

  *{box-sizing:border-box;}
  body{
    background:var(--bg);
    color:var(--ink);
    font-family:'Noto Sans KR',system-ui,sans-serif;
    padding-inline:16px;
    padding-block:20px;
    display:flex;
    justify-content:center;
  }
  .page{
    width:100%;
    max-width:460px;
    display:flex;
    flex-direction:column;
    gap:14px;
  }

  .topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:8px;
  }
  .brand{
    display:flex;
    align-items:center;
    gap:8px;
    font-family:'Jua',sans-serif;
    font-size:18px;
    color:var(--accent-dark);
    min-width:0;
  }
  .brand svg{width:26px;height:26px;flex:none;}
  .brand-text{display:flex;flex-direction:column;line-height:1.15;min-width:0;}
  .brand-sub{font-family:'Noto Sans KR',sans-serif;font-weight:500;font-size:11px;color:var(--ink-soft);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
  .score{
    font-family:'Baloo 2',sans-serif;
    font-weight:700;
    font-size:14px;
    background:var(--surface-2);
    color:var(--accent-ink);
    padding:6px 12px;
    border-radius:999px;
    font-variant-numeric:tabular-nums;
    flex:none;
    white-space:nowrap;
  }

  .progress-wrap{display:flex;flex-direction:column;gap:4px;}
  .progress-row{display:flex;justify-content:space-between;align-items:baseline;font-size:12px;color:var(--ink-soft);}
  .progress-row b{font-family:'Baloo 2',sans-serif;color:var(--ink);font-variant-numeric:tabular-nums;}
  .progress-track{height:8px;border-radius:999px;background:var(--surface-2);overflow:hidden;}
  .progress-fill{height:100%;background:var(--accent);border-radius:999px;transition:width .3s ease;}
  .finish-link{
    align-self:flex-end;
    background:none;border:none;
    font-size:12px;
    color:var(--ink-soft);
    text-decoration:underline;
    cursor:pointer;
    padding:2px 0;
  }
  .finish-link:focus-visible{outline:2px solid var(--sky);outline-offset:2px;}
  .progress-links{display:flex;gap:12px;}

  .pond-view{display:flex;flex-direction:column;gap:14px;}
  .pond{
    position:relative;
    background:linear-gradient(165deg,var(--water-a),var(--water-b) 55%,var(--water-c));
    border-radius:32px;
    padding:28px 18px 34px;
    overflow:hidden;
    box-shadow:0 8px 24px var(--shadow);
  }
  .lily{position:absolute;border-radius:50%;background:var(--lily);opacity:.4;}
  .ripple{position:absolute;border:2px solid rgba(255,255,255,.45);border-radius:50%;}
  .pond-path{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;gap:8px;}
  .stone{
    font-family:'Jua',sans-serif;
    font-size:13px;
    line-height:1.2;
    white-space:pre-line;
    text-align:center;
    color:var(--stone-ink);
    background:linear-gradient(160deg,var(--stone),var(--stone-dark));
    border:none;
    border-radius:48% 52% 50% 50% / 58% 46% 54% 42%;
    width:92px;
    min-height:58px;
    padding:6px 8px;
    box-shadow:0 5px 0 var(--stone-dark), 0 9px 16px rgba(0,0,0,.2);
    cursor:pointer;
    transition:transform .15s ease, box-shadow .15s ease;
  }
  .stone:hover{transform:translateY(-3px);}
  .stone:active{transform:translateY(3px);box-shadow:0 2px 0 var(--stone-dark);}
  .stone:focus-visible{outline:3px solid var(--accent);outline-offset:3px;}
  .pond-hint{text-align:center;font-size:12px;color:var(--ink-soft);margin:0;}
  .back-link{
    align-self:center;
    background:none;border:none;
    font-size:13px;color:var(--ink-soft);
    text-decoration:underline;cursor:pointer;padding:4px 0;
  }
  .back-link:focus-visible{outline:2px solid var(--sky);outline-offset:2px;}

  .stage{
    position:relative;
    background:linear-gradient(180deg,var(--surface-2),var(--surface));
    border-radius:28px;
    padding:20px 16px 6px;
    display:flex;
    flex-direction:column;
    align-items:center;
    box-shadow:0 8px 24px var(--shadow);
    overflow:hidden;
  }
  .speech-bubble{
    font-family:'Jua',sans-serif;
    font-size:14px;
    line-height:1.5;
    color:var(--ink);
    background:var(--surface);
    border:2px solid var(--line);
    border-radius:18px;
    padding:10px 14px;
    max-width:300px;
    text-align:center;
    position:relative;
    margin-bottom:6px;
    min-height:1.5em;
  }
  .speech-bubble::after{
    content:"";
    position:absolute;
    left:50%;
    bottom:-9px;
    transform:translateX(-50%);
    border-width:9px 8px 0 8px;
    border-style:solid;
    border-color:var(--surface) transparent transparent transparent;
    filter:drop-shadow(0 1px 0 var(--line));
  }

  .dog-wrap{position:relative;width:200px;height:200px;}
  .dog-svg{width:100%;height:100%;overflow:visible;}
  [hidden]{display:none!important;}

  .ear{transform-box:fill-box;transform-origin:top center;transition:transform .25s ease;}
  .dog-wrap[data-state="listening"] .ear-left{animation:earPerk 1s ease-in-out infinite alternate;}
  .dog-wrap[data-state="listening"] .ear-right{animation:earPerk 1s ease-in-out infinite alternate-reverse;}
  @keyframes earPerk{ from{transform:rotate(0deg) scale(1);} to{transform:rotate(-8deg) scale(1.03);} }

  .tail{transform-box:fill-box;transform-origin:20% 60%;}
  .dog-wrap[data-state="idle"] .tail{animation:tailSway 2.6s ease-in-out infinite;}
  .dog-wrap[data-state="happy"] .tail{animation:tailWag .28s ease-in-out infinite;}
  .dog-wrap[data-state="listening"] .tail{animation:tailSway 1.6s ease-in-out infinite;}
  @keyframes tailSway{ 0%,100%{transform:rotate(0deg);} 50%{transform:rotate(10deg);} }
  @keyframes tailWag{ 0%,100%{transform:rotate(-14deg);} 50%{transform:rotate(14deg);} }

  .dog-wrap[data-state="idle"] .head-group{animation:bob 3.2s ease-in-out infinite;}
  .dog-wrap[data-state="happy"] .head-group{animation:hop .5s ease-in-out 2;}
  @keyframes bob{ 0%,100%{transform:translateY(0);} 50%{transform:translateY(-4px);} }
  @keyframes hop{ 0%,100%{transform:translateY(0);} 50%{transform:translateY(-14px);} }

  .soundwave{opacity:0;}
  .dog-wrap[data-state="listening"] .soundwave{animation:wavePulse 1.2s ease-out infinite;}
  @keyframes wavePulse{ 0%{opacity:0;transform:scale(.7);} 40%{opacity:1;} 100%{opacity:0;transform:scale(1.25);} }

  .qmark{opacity:0;transform:translateY(4px);}
  .dog-wrap[data-state="confused"] .qmark{opacity:1;transform:translateY(0);animation:qBounce 1.4s ease-in-out infinite;}
  @keyframes qBounce{ 0%,100%{transform:translateY(0);} 50%{transform:translateY(-6px);} }

  .confetti-layer{position:absolute;inset:0;pointer-events:none;overflow:visible;}
  .confetti-piece{position:absolute;top:46%;left:50%;width:9px;height:9px;border-radius:2px;opacity:0;}
  @keyframes confettiFly{
    0%{opacity:1;transform:translate(0,0) rotate(0deg) scale(1);}
    100%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(var(--rot)) scale(.5);}
  }

  .word-card{
    display:flex;
    flex-direction:column;
    gap:6px;
    background:var(--surface);
    border:2px solid var(--line);
    border-radius:20px;
    padding:14px 16px;
  }
  .unit-badge{
    align-self:flex-start;
    font-size:11px;
    font-weight:700;
    color:var(--accent-ink);
    background:var(--surface-2);
    border-radius:999px;
    padding:2px 10px;
  }
  .word-text{
    font-family:'Baloo 2',sans-serif;
    font-weight:800;
    font-size:28px;
    color:var(--ink);
    word-break:break-word;
  }
  .word-meaning{font-size:14px;color:var(--ink-soft);}
  .word-example{font-size:12.5px;color:var(--ink-soft);font-style:italic;line-height:1.4;}

  .mic-btn{
    display:flex;
    align-items:center;
    justify-content:center;
    gap:10px;
    width:100%;
    border:none;
    cursor:pointer;
    background:var(--accent);
    color:var(--accent-ink);
    font-family:'Jua',sans-serif;
    font-size:17px;
    padding:16px;
    border-radius:999px;
    box-shadow:0 6px 0 var(--accent-dark);
    transition:transform .08s ease, box-shadow .08s ease;
  }
  .mic-btn:active{transform:translateY(4px);box-shadow:0 2px 0 var(--accent-dark);}
  .mic-btn:focus-visible{outline:3px solid var(--sky);outline-offset:3px;}
  .mic-btn svg{width:22px;height:22px;flex:none;}
  .mic-btn.listening{background:var(--sky);box-shadow:0 6px 0 #2E93BC;animation:micPulse 1s ease-in-out infinite;}
  @keyframes micPulse{ 0%,100%{transform:scale(1);} 50%{transform:scale(1.03);} }
  .mic-btn:disabled{opacity:.55;cursor:not-allowed;box-shadow:none;}

  .hint{text-align:center;font-size:12px;color:var(--ink-soft);margin:0;}

  .feedback{
    background:var(--surface);
    border-radius:18px;
    padding:14px 16px;
    display:flex;
    flex-direction:column;
    gap:8px;
    border:2px solid var(--line);
  }
  .feedback.correct{border-color:var(--success);background:var(--success-soft);}
  .feedback.retry{border-color:var(--miss);background:var(--miss-soft);}
  .heard{font-size:14px;color:var(--ink-soft);margin:0;}
  .heard b{color:var(--ink);font-family:'Baloo 2',sans-serif;}
  .verdict{font-family:'Jua',sans-serif;font-size:16px;margin:0;color:var(--ink);}
  .feedback-actions{display:flex;gap:10px;margin-top:4px;}
  .btn-primary,.btn-secondary{
    flex:1;border:none;border-radius:999px;padding:11px 14px;
    font-family:'Noto Sans KR',sans-serif;font-weight:700;font-size:14px;cursor:pointer;
  }
  .btn-primary{background:var(--success);color:#fff;}
  .btn-secondary{background:var(--surface-2);color:var(--ink);}
  .btn-primary:focus-visible,.btn-secondary:focus-visible{outline:3px solid var(--sky);outline-offset:2px;}

  .unsupported{
    background:var(--miss-soft);border:2px solid var(--miss);color:var(--ink);
    border-radius:14px;padding:12px 14px;font-size:13px;text-align:center;line-height:1.5;
  }

  /* name entry overlay */
  .overlay{
    position:fixed;inset:0;background:rgba(0,0,0,.45);
    display:flex;align-items:center;justify-content:center;padding:20px;z-index:30;
  }
  .overlay-card{
    background:var(--surface);border-radius:24px;padding:28px 24px;text-align:center;
    max-width:320px;width:100%;box-shadow:0 12px 30px var(--shadow);
  }
  .overlay-emoji{font-size:48px;}
  .overlay-card h2{font-family:'Jua',sans-serif;font-size:20px;margin:6px 0 4px;}
  .overlay-card p{color:var(--ink-soft);font-size:13.5px;margin:0 0 16px;line-height:1.5;}
  .name-input{
    width:100%;border:2px solid var(--line);border-radius:14px;
    padding:12px 14px;font-size:16px;font-family:'Noto Sans KR',sans-serif;
    margin-bottom:12px;background:var(--bg);color:var(--ink);
  }
  .name-input:focus{outline:none;border-color:var(--sky);}
  .overlay-card .btn-primary{width:100%;padding:13px;font-size:15px;}

  .celebrate-score{
    font-family:'Baloo 2',sans-serif;font-size:34px;font-weight:800;
    color:var(--success);margin:4px 0;font-variant-numeric:tabular-nums;
  }
  .celebrate-sub{font-size:13px;color:var(--ink-soft);margin:-8px 0 14px;}
  .celebrate-actions{display:flex;flex-direction:column;gap:10px;}
  .btn-form{
    background:var(--sky);color:#0B3E52;border:none;border-radius:999px;
    padding:13px;font-size:14px;font-weight:700;cursor:pointer;font-family:'Noto Sans KR',sans-serif;
  }
  .btn-form:focus-visible{outline:3px solid var(--accent);outline-offset:2px;}
  .form-note{font-size:11px;color:var(--ink-soft);margin-top:2px;}

  @media (prefers-reduced-motion: reduce){
    *{animation-duration:.001ms!important;animation-iteration-count:1!important;transition-duration:.001ms!important;}
  }
</style>

<div class="page">
  <header class="topbar">
    <div class="brand">
      <svg viewBox="0 0 24 24" fill="none"><path d="M12 21c-4 0-7-2.6-7-6.4C5 10.6 8 6 12 6s7 4.6 7 8.6C19 18.4 16 21 12 21Z" fill="currentColor"/><ellipse cx="8.3" cy="8" rx="2.1" ry="2.8" fill="currentColor"/><ellipse cx="15.7" cy="8" rx="2.1" ry="2.8" fill="currentColor"/></svg>
      <div class="brand-text">
        <span>멍멍 발음 친구</span>
        <span class="brand-sub" id="studentLabel"></span>
      </div>
    </div>
    <div class="score" id="scoreDisplay">콩이가 알아들은 단어 0개</div>
  </header>

  <!-- unit selection: stepping stones across the pond -->
  <div class="pond-view" id="pondView" hidden>
    <div class="speech-bubble">어느 유닛부터 건너볼까? 🐾</div>
    <div class="pond">
      <div class="lily" style="width:34px;height:22px;top:14px;left:18px;"></div>
      <div class="lily" style="width:26px;height:18px;top:70%;right:14px;"></div>
      <div class="ripple" style="width:46px;height:46px;top:40%;left:60%;"></div>
      <div class="pond-path" id="stonesContainer"></div>
    </div>
    <p class="pond-hint">돌다리를 누르면 그 유닛 단어만 연습해요</p>
  </div>

  <div id="practiceView" hidden>
  <div class="progress-wrap">
    <div class="progress-row">
      <span>진행 <b id="progressCurrent">1</b> / <span id="progressTotal">127</span></span>
      <div class="progress-links">
        <button class="finish-link" id="backToPondBtn" type="button">유닛 바꾸기</button>
        <button class="finish-link" id="finishBtn" type="button">그만하고 결과 보기</button>
      </div>
    </div>
    <div class="progress-track"><div class="progress-fill" id="progressFill" style="width:1%"></div></div>
  </div>

  <section class="stage">
    <div class="speech-bubble" id="speechBubble">안녕! 나는 콩이야. 아래 단어를 나한테 말해줘! 🐾</div>

    <div class="dog-wrap" id="dogWrap" data-state="idle">
      <svg class="dog-svg" viewBox="0 0 240 260" aria-hidden="true">
        <path class="tail" d="M182 188 C 214 176, 226 146, 208 124 C 222 142, 216 174, 190 194 Z" fill="var(--dog-fur)"/>
        <ellipse class="body" cx="120" cy="206" rx="76" ry="46" fill="var(--dog-fur)"/>
        <ellipse cx="93" cy="244" rx="17" ry="11" fill="var(--surface)"/>
        <ellipse cx="147" cy="244" rx="17" ry="11" fill="var(--surface)"/>

        <g class="head-group">
          <circle class="head" cx="120" cy="118" r="78" fill="var(--dog-fur)"/>
          <path class="ear ear-left" d="M65 55 C 25 70, 15 118, 48 175 C 67.8 209.2, 42 95, 78 100 Z" fill="var(--dog-fur-dark)"/>
          <path class="ear ear-right" d="M175 55 C 215 70, 225 118, 192 175 C 172.2 209.2, 198 95, 162 100 Z" fill="var(--dog-fur-dark)"/>
          <ellipse cx="80" cy="138" rx="15" ry="9" fill="#FF6E6E" opacity=".35"/>
          <ellipse cx="160" cy="138" rx="15" ry="9" fill="#FF6E6E" opacity=".35"/>
          <ellipse class="snout" cx="120" cy="146" rx="40" ry="29" fill="var(--surface)"/>
          <ellipse cx="120" cy="130" rx="11" ry="8" fill="var(--ink)"/>

          <g class="eyes-normal">
            <circle cx="90" cy="103" r="8" fill="var(--dog-eye)"/>
            <circle cx="150" cy="103" r="8" fill="var(--dog-eye)"/>
            <circle cx="92.5" cy="100" r="2.2" fill="#fff"/>
            <circle cx="152.5" cy="100" r="2.2" fill="#fff"/>
          </g>
          <g class="eyes-happy" hidden>
            <path d="M80 106 Q90 92 100 106" stroke="var(--dog-eye)" stroke-width="6" stroke-linecap="round" fill="none"/>
            <path d="M140 106 Q150 92 160 106" stroke="var(--dog-eye)" stroke-width="6" stroke-linecap="round" fill="none"/>
          </g>
          <g class="eyes-listening" hidden>
            <circle cx="90" cy="103" r="9.5" fill="var(--dog-eye)"/>
            <circle cx="150" cy="103" r="9.5" fill="var(--dog-eye)"/>
            <circle cx="93.5" cy="99" r="2.6" fill="#fff"/>
            <circle cx="153.5" cy="99" r="2.6" fill="#fff"/>
          </g>
          <g class="eyes-confused" hidden>
            <circle cx="90" cy="103" r="8" fill="var(--dog-eye)"/>
            <path d="M141 103 Q150 97 159 103" stroke="var(--dog-eye)" stroke-width="6" stroke-linecap="round" fill="none"/>
          </g>

          <g class="mouth-normal">
            <path d="M104 160 Q120 170 136 160" stroke="var(--ink)" stroke-width="4" stroke-linecap="round" fill="none"/>
          </g>
          <g class="mouth-happy" hidden>
            <path d="M98 158 Q120 192 142 158 Z" fill="var(--ink)"/>
            <ellipse cx="120" cy="176" rx="13" ry="9" fill="#FF9AA6"/>
          </g>
          <g class="mouth-confused" hidden>
            <path d="M106 163 Q113 156 120 163 T134 163" stroke="var(--ink)" stroke-width="4" stroke-linecap="round" fill="none"/>
          </g>

          <text class="qmark" x="176" y="58" font-family="Baloo 2, sans-serif" font-size="34" font-weight="800" fill="var(--ink)">?</text>

          <g class="soundwave" stroke="var(--sky)" fill="none" stroke-width="3" stroke-linecap="round">
            <path d="M40 92 Q30 100 40 108"/>
            <path d="M30 86 Q14 100 30 114"/>
          </g>
        </g>
      </svg>
      <div class="confetti-layer" id="confettiLayer"></div>
    </div>
  </section>

  <section class="word-card" id="wordCard">
    <span class="unit-badge" id="wordUnit">Unit 4</span>
    <span class="word-text" id="wordText">dog</span>
    <span class="word-meaning" id="wordMeaning">개</span>
    <span class="word-example" id="wordExample">This is a dog.</span>
  </section>

  <button class="mic-btn" id="micBtn" type="button">
    <svg viewBox="0 0 24 24" fill="none"><path d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3Z" fill="currentColor"/><path d="M19 11a7 7 0 0 1-14 0M12 18v3" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>
    <span id="micLabel">눌러서 말해보세요</span>
  </button>
  <p class="hint" id="hintText">Chrome 브라우저 추천 · 마이크 권한을 허용해주세요</p>

  <section class="feedback" id="feedback" hidden>
    <p class="heard" id="heardText"></p>
    <p class="verdict" id="verdictText"></p>
    <div class="feedback-actions">
      <button class="btn-secondary" id="retryBtn" type="button" hidden>다시 말해보기</button>
      <button class="btn-primary" id="nextBtn" type="button" hidden>다음 단어 ▶</button>
    </div>
  </section>

  <div class="unsupported" id="unsupportedBox" hidden>
    🙈 이 브라우저는 음성 인식을 지원하지 않아요. 최신 Chrome 브라우저에서 이 페이지를 열어주세요.
  </div>
  </div>
</div>

<!-- name entry overlay -->
<div class="overlay" id="nameOverlay">
  <div class="overlay-card">
    <div class="overlay-emoji">🐶</div>
    <h2>이름을 알려줘!</h2>
    <p>콩이가 누구랑 발음 연습을 하는지 알아야 기록을 남길 수 있어요.</p>
    <input type="text" id="nameInput" class="name-input" placeholder="이름을 입력하세요" maxlength="20">
    <button class="btn-primary" id="startBtn" type="button">연습 시작하기</button>
  </div>
</div>

<!-- completion overlay -->
<div class="overlay" id="celebrateOverlay" hidden>
  <div class="overlay-card">
    <div class="overlay-emoji" id="celebrateEmoji">🏆</div>
    <h2 id="celebrateName">수고했어요!</h2>
    <div class="celebrate-score" id="celebrateScore">0 / 127</div>
    <p class="celebrate-sub" id="celebrateEncourage">콩이가 목표 단어로 알아들은 단어 개수예요.</p>
    <div class="celebrate-actions">
      <button class="btn-form" id="recordBtn" type="button">📋 구글 설문지로 기록 남기기</button>
      <button class="btn-secondary" id="anotherUnitBtn" type="button">다른 유닛 연습하기</button>
      <button class="btn-primary" id="restartBtn" type="button">다음 학생 시작하기</button>
    </div>
    <p class="form-note" id="formNote"></p>
  </div>
</div>

<script>
(function(){
  var WORDS_RAW = __WORDS_JSON__;
  var WORDS_ALL = WORDS_RAW.map(function(w){ return { unit:w.u, text:w.t, meaning:w.m, example:w.e }; });
  var UNITS = [];
  WORDS_ALL.forEach(function(w){ if (UNITS.indexOf(w.unit) === -1) UNITS.push(w.unit); });
  function unitLabel(u){ return u.indexOf('Special Reading') === 0 ? u.replace('Special ', '') : u; }

  /* ---- Google Form hook: paste real values here once the form exists ---- */
  var FORM_CONFIG = {
    baseUrl: 'https://docs.google.com/forms/d/e/1FAIpQLScO37vlswQSm6N-mqx1w5VrYeCnsao1JVlK-WqzJME82imV-A/viewform',
    nameEntry: 'entry.1598372142',
    scoreEntry: 'entry.1041762124',
    totalEntry: ''    /* optional e.g. 'entry.333333333' */
  };
  function formReady(){ return !!(FORM_CONFIG.baseUrl && FORM_CONFIG.nameEntry && FORM_CONFIG.scoreEntry); }
  function buildFormUrl(name, correct, total){
    var params = ['usp=pp_url'];
    params.push(FORM_CONFIG.nameEntry + '=' + encodeURIComponent(name));
    params.push(FORM_CONFIG.scoreEntry + '=' + encodeURIComponent(correct));
    if (FORM_CONFIG.totalEntry) params.push(FORM_CONFIG.totalEntry + '=' + encodeURIComponent(total));
    return FORM_CONFIG.baseUrl + '?' + params.join('&');
  }

  var state = { index:0, correct:new Set(), attempted:new Set(), listening:false, name:'', words:[], currentUnit:'' };

  var els = {
    studentLabel: document.getElementById('studentLabel'),
    score: document.getElementById('scoreDisplay'),
    pondView: document.getElementById('pondView'),
    stonesContainer: document.getElementById('stonesContainer'),
    practiceView: document.getElementById('practiceView'),
    backToPondBtn: document.getElementById('backToPondBtn'),
    anotherUnitBtn: document.getElementById('anotherUnitBtn'),
    progCurrent: document.getElementById('progressCurrent'),
    progTotal: document.getElementById('progressTotal'),
    progFill: document.getElementById('progressFill'),
    finishBtn: document.getElementById('finishBtn'),
    bubble: document.getElementById('speechBubble'),
    dogWrap: document.getElementById('dogWrap'),
    confetti: document.getElementById('confettiLayer'),
    unit: document.getElementById('wordUnit'),
    text: document.getElementById('wordText'),
    meaning: document.getElementById('wordMeaning'),
    example: document.getElementById('wordExample'),
    micBtn: document.getElementById('micBtn'),
    micLabel: document.getElementById('micLabel'),
    hint: document.getElementById('hintText'),
    feedback: document.getElementById('feedback'),
    heard: document.getElementById('heardText'),
    verdict: document.getElementById('verdictText'),
    retryBtn: document.getElementById('retryBtn'),
    nextBtn: document.getElementById('nextBtn'),
    unsupported: document.getElementById('unsupportedBox'),
    nameOverlay: document.getElementById('nameOverlay'),
    nameInput: document.getElementById('nameInput'),
    startBtn: document.getElementById('startBtn'),
    overlay: document.getElementById('celebrateOverlay'),
    celebrateName: document.getElementById('celebrateName'),
    celebrateScore: document.getElementById('celebrateScore'),
    celebrateEncourage: document.getElementById('celebrateEncourage'),
    recordBtn: document.getElementById('recordBtn'),
    formNote: document.getElementById('formNote'),
    restartBtn: document.getElementById('restartBtn')
  };

  function renderStones(){
    els.stonesContainer.innerHTML = '';
    UNITS.forEach(function(u, i){
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'stone';
      btn.style.marginLeft = (i % 2 === 0) ? '-20px' : '20px';
      btn.textContent = unitLabel(u);
      btn.addEventListener('click', function(){ selectUnit(u); });
      els.stonesContainer.appendChild(btn);
    });
  }

  function selectUnit(unit){
    state.currentUnit = unit;
    state.words = WORDS_ALL.filter(function(w){ return w.unit === unit; });
    state.correct = new Set();
    state.attempted = new Set();
    els.progTotal.textContent = state.words.length;
    updateScore();
    els.pondView.hidden = true;
    els.practiceView.hidden = false;
    loadWord(0);
  }

  function backToPond(){
    els.overlay.hidden = true;
    els.practiceView.hidden = true;
    els.pondView.hidden = false;
  }
  els.backToPondBtn.addEventListener('click', backToPond);
  els.anotherUnitBtn.addEventListener('click', backToPond);

  function setDogState(s){ els.dogWrap.setAttribute('data-state', s); }
  function showGroup(prefix, name){
    ['normal','happy','listening','confused'].forEach(function(n){
      var g = els.dogWrap.querySelector('.'+prefix+'-'+n);
      if(g) g.hidden = (n !== name);
    });
  }
  function setFace(name){
    showGroup('eyes', name === 'listening' ? 'listening' : (name === 'happy' ? 'happy' : (name === 'confused' ? 'confused' : 'normal')));
    showGroup('mouth', name === 'happy' ? 'happy' : (name === 'confused' ? 'confused' : 'normal'));
  }

  function updateScore(){ els.score.textContent = '콩이가 알아들은 단어 ' + state.correct.size + '개'; }
  function updateProgress(){
    els.progCurrent.textContent = state.index + 1;
    els.progFill.style.width = Math.max(4, ((state.index+1)/state.words.length)*100) + '%';
  }

  function loadWord(i){
    state.index = i;
    var w = state.words[i];
    els.unit.textContent = w.unit;
    els.text.textContent = w.text;
    els.meaning.textContent = w.meaning;
    els.example.textContent = w.example;
    els.feedback.hidden = true;
    els.feedback.className = 'feedback';
    els.retryBtn.hidden = true;
    els.nextBtn.hidden = true;
    els.bubble.textContent = '이 단어를 나한테 말해줘! 🎧';
    setDogState('idle');
    setFace('normal');
    updateProgress();
    if (recognitionSupported){
      els.micBtn.disabled = false;
      els.micLabel.textContent = '눌러서 말해보세요';
    }
  }

  function normalize(s){
    return (s || '').toLowerCase().replace(/[^a-z' ]/g, ' ').replace(/\s+/g,' ').trim();
  }
  function isMatch(transcript, target){
    var t = normalize(transcript);
    var tgt = normalize(target);
    if(!t) return false;
    if(t === tgt) return true;
    return t.split(' ').indexOf(tgt) !== -1;
  }

  function burstConfetti(){
    var colors = ['#FF9A4D','#4FB6E0','#3FAE68','#FFD166','#EF476F'];
    for (var i=0;i<16;i++){
      var p = document.createElement('span');
      p.className = 'confetti-piece';
      var angle = Math.random()*Math.PI*2;
      var dist = 60 + Math.random()*70;
      p.style.setProperty('--dx', Math.cos(angle)*dist + 'px');
      p.style.setProperty('--dy', (Math.sin(angle)*dist - 30) + 'px');
      p.style.setProperty('--rot', (Math.random()*360) + 'deg');
      p.style.background = colors[i % colors.length];
      p.style.animation = 'confettiFly .9s ease-out forwards';
      p.style.animationDelay = (Math.random()*0.08) + 's';
      els.confetti.appendChild(p);
      (function(node){ setTimeout(function(){ node.remove(); }, 1100); })(p);
    }
  }

  function showCorrect(heardWord){
    state.attempted.add(state.index);
    setDogState('happy');
    setFace('happy');
    burstConfetti();
    state.correct.add(state.index);
    updateScore();
    els.bubble.textContent = '멍멍! 내가 알아들었어! 🎉';
    els.feedback.hidden = false;
    els.feedback.className = 'feedback correct';
    els.heard.innerHTML = '내가 들은 말: <b>"' + heardWord + '"</b>';
    els.verdict.textContent = '목표 단어로 인식되었어요! 👏';
    els.retryBtn.hidden = true;
    els.nextBtn.hidden = false;
    els.micBtn.disabled = true;
    els.micLabel.textContent = '완료!';
  }

  function showRetry(heardWord){
    state.attempted.add(state.index);
    setDogState('confused');
    setFace('confused');
    els.bubble.textContent = '음... 다시 한번 말해줄래? 🤔';
    els.feedback.hidden = false;
    els.feedback.className = 'feedback retry';
    els.heard.innerHTML = heardWord ? ('내가 들은 말: <b>"' + heardWord + '"</b>') : '아무 소리도 못 들었어요.';
    els.verdict.textContent = '조금 다르게 들렸어요. 다시 말해볼까요?';
    els.retryBtn.hidden = false;
    els.nextBtn.hidden = false;
    els.micBtn.disabled = false;
    els.micLabel.textContent = '눌러서 말해보세요';
  }

  function encouragementFor(ratio){
    if (ratio >= 0.9) return '완벽해요! 발음 천재예요! 🌟';
    if (ratio >= 0.7) return '정말 잘했어요! 계속 이렇게 해봐요! 🎉';
    if (ratio >= 0.4) return '멋진 시도예요! 조금만 더 연습해볼까요? 💪';
    return '시작이 반이에요! 다음엔 더 잘할 수 있어요 🐾';
  }

  function finishSession(){
    var attemptedCount = state.attempted.size;
    var correctCount = state.correct.size;
    var ratio = attemptedCount ? (correctCount/attemptedCount) : 0;
    els.celebrateName.textContent = (state.name ? state.name + '님, ' : '') + '수고했어요!';
    els.celebrateScore.textContent = correctCount + ' / ' + attemptedCount;
    els.celebrateEncourage.textContent = unitLabel(state.currentUnit) + ' · 도전한 ' + attemptedCount + '개 중 ' + correctCount + '개 정확! ' + encouragementFor(ratio) + ' (이 유닛 전체 ' + state.words.length + '개)';
    els.formNote.textContent = formReady() ? '' : '선생님이 구글 설문지를 연결하면 이 버튼으로 바로 기록돼요.';
    setDogState('happy');
    setFace('happy');
    els.overlay.hidden = false;
  }

  els.nextBtn.addEventListener('click', function(){
    if (state.index >= state.words.length - 1){ finishSession(); return; }
    loadWord(state.index + 1);
  });
  els.finishBtn.addEventListener('click', finishSession);
  els.retryBtn.addEventListener('click', function(){
    els.feedback.hidden = true;
    setDogState('idle');
    setFace('normal');
    els.bubble.textContent = '괜찮아요, 다시 해봐요! 🐾';
  });
  els.recordBtn.addEventListener('click', function(){
    var attemptedCount = state.attempted.size;
    var correctCount = state.correct.size;
    if (!formReady()){
      els.formNote.textContent = '아직 구글 설문지가 연결되지 않았어요. 선생님께 알려주세요!';
      return;
    }
    var nameForForm = (state.name || '이름없음') + ' (' + unitLabel(state.currentUnit) + ')';
    var scoreForForm = correctCount + '/' + attemptedCount;
    var url = buildFormUrl(nameForForm, scoreForForm, attemptedCount);
    window.open(url, '_blank', 'noopener');
  });
  els.restartBtn.addEventListener('click', function(){
    state.correct = new Set();
    state.attempted = new Set();
    state.name = '';
    state.words = [];
    state.currentUnit = '';
    els.overlay.hidden = true;
    els.practiceView.hidden = true;
    els.pondView.hidden = true;
    els.nameInput.value = '';
    els.nameOverlay.hidden = false;
    setTimeout(function(){ els.nameInput.focus(); }, 50);
  });

  function beginSession(){
    var name = els.nameInput.value.trim();
    if (!name){ els.nameInput.focus(); return; }
    state.name = name;
    els.studentLabel.textContent = name + ' 학생 연습 중';
    els.nameOverlay.hidden = true;
    renderStones();
    els.pondView.hidden = false;
  }
  els.startBtn.addEventListener('click', beginSession);
  els.nameInput.addEventListener('keydown', function(e){ if (e.key === 'Enter') beginSession(); });

  var SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
  var recognitionSupported = !!SpeechRecognitionCtor;
  var recognition = null;

  if (recognitionSupported){
    recognition = new SpeechRecognitionCtor();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 5;
    recognition.continuous = false;

    recognition.onstart = function(){
      state.listening = true;
      setDogState('listening');
      setFace('listening');
      els.micBtn.classList.add('listening');
      els.micLabel.textContent = '듣는 중...';
      els.bubble.textContent = '귀 기울이고 있어요... 🎧';
      els.feedback.hidden = true;
    };
    recognition.onresult = function(e){
      var results = e.results[0];
      var alts = [];
      for (var i=0;i<results.length;i++){ alts.push(results[i].transcript); }
      var best = alts[0] || '';
      var target = state.words[state.index].text;
      var matched = alts.some(function(a){ return isMatch(a, target); });
      if (matched){ showCorrect(best.trim()); } else { showRetry(best.trim()); }
    };
    recognition.onerror = function(e){
      state.listening = false;
      els.micBtn.classList.remove('listening');
      setDogState('idle');
      setFace('normal');
      if (e.error === 'not-allowed' || e.error === 'service-not-allowed'){
        els.hint.textContent = '마이크 권한이 필요해요! 브라우저 주소창 옆 마이크 아이콘을 확인해보세요.';
      } else if (e.error === 'no-speech'){
        showRetry('');
      }
      els.micLabel.textContent = '눌러서 말해보세요';
    };
    recognition.onend = function(){
      state.listening = false;
      els.micBtn.classList.remove('listening');
    };
  } else {
    els.unsupported.hidden = false;
  }

  els.micBtn.addEventListener('click', function(){
    if (!recognitionSupported){ els.unsupported.hidden = false; return; }
    if (state.listening) return;
    try{ recognition.start(); }
    catch(err){ /* already starting, ignore */ }
  });

  setTimeout(function(){ els.nameInput.focus(); }, 100);
})();
</script>"""
practice_html = practice_html.replace("__WORDS_JSON__", WORDS_JSON)

components.html(
    practice_html,
    height=1150,
    scrolling=True,
)
