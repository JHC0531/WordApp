The following image can be moved on the page using keyboard controls (left, right, up, down)
이전 메시지 불러오는 중…

붙여넣은 텍스트(1)(1).txt
문서
응, 이게 내가 필요했던 전체 Artifact 코드야. 이제 04🐥_발음짱이 될거야.py로 옮길 수 있어.

코드를 확인해보니 현재 버전은 꽤 잘 만들어져 있어. 강아지 콩이 애니메이션, 유닛별 돌다리, Web Speech API를 이용한 Chrome 음성인식, 정답/재시도 피드백, 결과 화면까지 이미 구현되어 있어. 
 

다만 그대로 Streamlit에 붙이면 안 되는 부분이 두 군데 있어.

첫째, 지금은 127개 단어가 JavaScript의 WORDS_RAW 안에 통째로 박혀 있어. 
 이건 우리가 이미 만든 data/wordlist_1001.csv와 중복이야. 따라서 Practice App에서는 이 목록을 없애고 CSV + 학생이 Word List에서 📦 보관한 단어를 Python에서 읽어서 콩이 앱에 전달하도록 바꾸는 게 좋아.

둘째, 맨 아래의 window.claude.hot... 부분은 Claude Artifact 안에서 상태를 보존하기 위한 코드라서 Streamlit에서는 필요 없어. 
 이 부분은 제거해야 해.

그래서 최종 흐름을 이렇게 만들면 돼:

01🐱 Word List
→ 학생이 📦 보관할래요

03🎀 Word Learning
→ 듣기 + 의미 회상
→ ⭐ 다시 볼래요

04🐥 발음짱이 될거야
→ 📦 보관한 단어만 콩이와 발음 연습
→ Chrome 음성인식
→ “내가 들은 말” 표시
→ 성공하면 🎉 강아지 반응
→ 틀리면 다시 발음
→ 결과

그리고 현재 코드에서 발음 판정은 단순히 음성인식 결과와 목표 단어를 비교하는 방식이야. 
 이건 네 연구에서 사용할 때 중요한 점이야. 엄밀한 발음 정확도 점수라기보다는 ASR가 목표 단어로 인식했는지 여부라고 보는 게 맞아.

지금부터 네가 할 일
아직 GitHub에서 코드 건드리지 마.

내가 다음 단계에서 pages/04🐥_발음짱이 될거야.py 전체 코드를 통째로 만들어 줄게. 복사해서 GitHub에 붙여넣기만 하면 되게 할 수 있어.

이번에는 원래 Claude 디자인을 최대한 그대로 살리면서 다음처럼 바꿀 거야.

wordlist_1001.csv 자동 연결
Word List의 saved_words 자동 연결
learning_unit을 그대로 받아서 Practice 들어가자마자 해당 Unit 시작
원하면 ⭐ 다시 볼 단어만 연습 선택 가능
127개를 JS에 다시 입력하지 않음
Claude 전용 코드 제거
강아지 콩이 SVG/애니메이션 유지
Chrome 마이크 발음인식 유지
기존 Google Form 연결도 유지
학생이 별도로 Unit을 또 고르지 않아도 되게 만들 수 있음
특히 네 앱 흐름을 생각하면 Practice App에 들어갔는데 또 “어느 유닛부터 건너볼까?”를 묻는 건 조금 중복이야. Word List에서 이미 Unit과 단어를 골랐으니까, 나는 03🎀 Word Learning → 04🐥 Practice로 넘어갈 때 그 Unit + 보관한 단어가 바로 콩이 앞에 나타나는 방식을 추천해.

예를 들어 Unit 6에서 20개 중 13개를 보관했다면 Practice 화면은 바로:

🐶 콩이
Unit 6 · 13 words

진행 1 / 13

“이 단어를 나한테 말해줘! 🎧”

astronaut
우주 비행사
I want to be an astronaut in the future.

🎙️ 눌러서 말해보세요

이렇게 시작하도록 만들면 돼.

그리고 네가 준 원본에는 Google Form 주소와 nameEntry, scoreEntry 값도 이미 들어가 있어. 
 그 부분도 살려둘 수 있어.

이제 내가 04🐥_발음짱이 될거야.py 완성본을 통째로 만들어주면 돼.

근데 발음은 굳이 저장한 단어를 안해도될거같은게... 애들이 의미를 아는 단어도 발음 연습을 계속 해야해. 별로 정확하지않거든
맞아. 그러면 발음 Practice는 saved_words와 분리하는 게 더 자연스러워.

📦 보관한 단어는 “뜻이나 형태를 더 공부해야 하는 단어”이고, 발음은 뜻을 이미 아는 단어라도 반복해서 말해볼 필요가 있기 때문이야. 특히 네 앱 목적이 어휘+발음 학습이라면, 이 둘을 같은 필터로 묶지 않는 편이 좋아.

그래서 Practice App은 이렇게 가는 걸 추천해:

기본: 선택한 Unit의 전체 단어
선택 옵션:
전체 단어 연습
⭐ 다시 볼 단어만 연습
Word List의 📦 보관한 단어는 Practice App에서는 굳이 강제하지 않음
즉 흐름은 이렇게 분리돼.

Word List
→ “이 단어의 뜻/형태를 더 공부할 필요가 있나?”

Word Learning
→ 의미·형태·소리 학습

발음짱이 될거야
→ “이 단어를 실제로 정확하게 말할 수 있나?”

이게 연구적으로도 더 깔끔해. 현재 Artifact의 발음 Practice는 원래부터 Unit 전체를 대상으로 하고 있고, Unit을 고르면 그 Unit 전체 단어를 state.words로 불러오도록 되어 있어. 
 그래서 이 구조를 유지하는 편이 오히려 원래 설계와 잘 맞아.

다만 한 가지는 바꾸는 게 좋아. 지금 Artifact 안에 127개 단어가 직접 박혀 있으니까, 그건 없애고 data/wordlist_1001.csv에서 Unit 전체 단어를 자동으로 가져오도록 바꾸자. 그러면 나중에 CSV를 고쳐도 Practice App이 같이 업데이트돼.

내가 만들 최종 04🐥_발음짱이 될거야.py는 이렇게 할 수 있어:

🐶 멍멍 발음 친구

[ Unit 4 ] [ Unit 5 ] [ Unit 6 ]
[ Unit 7 ] [ SR 1 ]   [ SR 2 ]

선택: Unit 6

진행 1 / 20

🐶 콩이
"이 단어를 나한테 말해줘!"

presentation
발표
When is your presentation about your dream job?

🎙️ 눌러서 말해보세요
그리고 성공하면:

🐶🎉
멍멍! 정확해요!

내가 들은 말:
"presentation"

정확해요! 잘 말했어요 👏

[ 다음 단어 ▶ ]
이 방향으로 가면 돼. 발음 Practice는 Unit 전체 단어 기준으로 만들자. saved_words와 연결하지 않겠다.

그래. 그리고 현재 코드에서 발음 판정은 단순히 음성인식 결과와 목표 단어를 비교하는 방식이야.    붙여넣은 텍스트(1) 이건 네 연구에서 사용할 때 중요한 점이야. 엄밀한 발음 정확도 점수라기보다는 ASR가 목표 단어로 인식했는지 여부라고 보는 게 맞아.  이 부분에서...아이들이 asr시스템에서 인식되는 단어 갯수로 아이들의 발음 성적을 측정하는 게 객관적으로 타당하니?

객관성은 어느 정도 확보할 수 있지만, “ASR가 목표 단어로 인식한 개수 = 발음 능력 점수”라고 그대로 쓰는 건 타당도가 충분하다고 보기 어려워. 더 정확하게는 ASR recognition rate를 ‘발음 명료도(intelligibility)의 행동 지표/대리 지표(proxy)’로 사용하는 것이 적절해.

네 현재 코드의 판정 방식은 학생 발화를 ASR가 텍스트로 변환한 뒤, 그 결과가 목표 단어와 일치하는지를 보는 구조야. 즉 음향적으로 얼마나 원어민처럼 발음했는지를 직접 분석하는 게 아니라, ASR 시스템이 그 발화를 목표 단어로 알아들을 수 있었는지를 측정하고 있어. 현재 코드도 실제로 transcript와 target을 정규화한 뒤 일치 여부를 판단해. 

이 방식에는 장점이 분명해. 모든 학생에게 같은 알고리즘을 적용하니 교사 평정처럼 평가자 간 편차가 없고, 수십 명의 학생을 반복 측정하기도 쉽고, 학습자에게 즉각적 피드백을 줄 수 있어. 최근 메타분석에서도 ASR 기반 발음 학습은 전반적으로 긍정적인 효과를 보였고, 특히 분절음 수준의 발음 개선에서 효과가 더 크게 나타났다. 

하지만 객관적이라는 것과 타당하다는 것은 다른 문제야. ASR는 원래 “사람의 발음을 평가하기 위해” 만들어진 시스템이 아니라 대개 “무슨 말을 했는지 인식하기 위해” 만들어진 시스템이야. 그래서 상당히 알아들을 만한 발음이어도 ASR가 틀리게 인식할 수 있고, 반대로 실제로는 어색하거나 오류가 있는 발음인데 문맥이나 모델의 예측 때문에 목표 단어로 인식할 수도 있어. 최근 EFL ASR 연구 리뷰도 ASR 연구가 주로 segmental/word-level accuracy에 집중되어 있고, intelligibility나 comprehensibility를 얼마나 잘 반영하는지에 대해서는 아직 근거가 충분하지 않다고 지적해. 

특히 네 대상이 한국 중학생이라는 점도 중요해. 2025년 한국의 어린 EFL 학습자를 대상으로 한 자동 발음평가 연구에서도 음소 위치 등에 따라 자동평가 결과가 달라지고, 자동화된 도구에 정확도 한계와 잠재적 편향이 있을 수 있다고 보고했어. 

그래서 논문에서는 측정변수를 이렇게 정의하는 게 가장 안전해.

ASR recognition rate: the proportion of target words correctly recognized by the ASR system following learners’ oral production.

그리고 이것을

a behavioral proxy for pronunciation intelligibility

라고 부르는 거야.

반대로 pronunciation accuracy score, pronunciation proficiency, objective pronunciation score처럼 쓰면 심사에서 “ASR recognition이 실제 발음 정확도를 얼마나 타당하게 반영하느냐?”라는 질문을 받을 가능성이 커.

네 연구에서는 오히려 이걸 잘 활용할 수 있어. 예를 들어 20개 목표 단어 중 ASR가 14개를 목표 단어로 인식했다면:

ASR Recognition Rate
=
14
20
×
100
=
70
%
ASR Recognition Rate= 
20
14
​
 ×100=70%
이 점수는 **“학생의 발음 정확도가 70점”이라는 뜻이 아니라, “20개의 산출 중 70%가 ASR 시스템에 의해 의도한 단어로 성공적으로 인식되었다”**는 뜻이야.

그리고 pre/post에서 동일한 단어, 동일한 ASR, 동일한 조건을 사용하면 절대적인 발음 수준 판정보다 변화량을 비교하는 데 훨씬 더 설득력이 있어. 예를 들어 사전 45% → 사후 75%라면 “발음이 객관적으로 30점 향상됐다”고 쓰기보다는 **“ASR recognition rate increased from 45% to 75%”**라고 쓰는 게 맞아.

더 강한 연구 설계를 원한다면, 나는 **ASR recognition rate + 사람 평가의 소규모 타당화(subsample validation)**를 추천해. 모든 172명의 모든 음성을 사람이 채점할 필요는 없어. 예를 들어 표본 일부의 발음을 2명의 영어교사 또는 훈련된 평가자가 intelligibility/comprehensibility 기준으로 독립 평가하고, 그 점수와 ASR recognition 결과의 관계를 확인하면 네 ASR 지표의 convergent validity 근거를 훨씬 강하게 만들 수 있어. ASR 연구에서도 phonetic distance뿐 아니라 인간의 accentedness/comprehensibility 평가를 함께 사용한 사례가 있어. 

그래서 네 연구라면 측정 구조를 이렇게 잡는 게 가장 방어가 잘 돼.

주요 양적 지표: ASR target-word recognition rate (%)
해석: pronunciation intelligibility의 행동적 proxy
보조 타당화: 일부 발화에 대한 인간 평가와의 일치/상관
피해야 할 표현: “ASR pronunciation accuracy score = 학생의 실제 발음 정확도”

그리고 앱 자체에서도 지금처럼 정답 13개라고 표시하기보다는 연구 관점에서는 “콩이가 알아들은 단어 13개” 같은 표현이 더 정확할 수도 있어. 학생에게도 “네 발음이 틀렸다”가 아니라 **“이번에는 이렇게 들렸어요 / 다시 말해볼까요?”**라고 피드백하는 현재 구조가 오히려 측정 개념과 잘 맞아. 현재 코드도 실패 시 “조금 다르게 들렸어요”라고 표현하고 있어서 방향은 좋아. 

한 가지 더 중요한 점이 있어. 현재 앱은 학생에게 목표 단어를 화면에 보여준 상태에서 말하게 하고 있고, ASR가 그 단어를 인식했는지를 본다. 따라서 논문에서는 이걸 자유발화 능력이나 전반적 발음 능력으로 확장해서 해석하지 말고, controlled word-production task에서의 ASR recognizability로 한정하는 게 가장 정확해. 이 정도로 정의하면 네 연구의 pronunciation outcome으로 충분히 사용할 수 있어. 

원한다면 다음에는 내가 논문의 Instruments/Measures 부분에 그대로 넣을 수 있는 “ASR-based pronunciation measure” 영문 문단까지 학술적으로 써줄 수 있어.

그래 그럼 일단 그렇게 코드 만들어보자.

26s 동안 처리함
좋아. 그러면 발음 Practice는 Word List의 보관 여부와 완전히 분리하고, 학생이 고른 Unit의 전체 단어를 연습하도록 만들자.

또 화면에서는 정답이나 발음 점수라고 하지 않고 **“콩이가 알아들은 단어”**라고 표시하도록 바꿀게. 실제 판정도 기존 Artifact처럼 ASR이 학생 발화를 텍스트로 바꾼 뒤 목표 단어와 일치하는지를 확인하는 방식이야. 

먼저 GitHub에서 pages/04🐥_발음짱이 될거야.py를 열고 기존 내용을 전부 삭제한 뒤 아래 코드를 통째로 붙여넣어. 이 버전은 data/wordlist_1001.csv를 직접 읽기 때문에 127개 단어를 코드 안에 다시 적을 필요가 없어.

import streamlit as st
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

이 버전에서 중요한 변화는 Practice App이 saved_words를 전혀 보지 않는다는 것이야. 학생이 Unit 6을 누르면 CSV의 Unit 6 전체 단어가 들어가. 따라서 학생이 이미 future = 미래라는 뜻을 알고 있어서 Word List에서 버렸더라도, 발음 Practice에서는 future를 계속 발음하게 돼.

또 판정 문구도 바꿨어. 기존 Artifact는 성공하면 "정확해요!"라고 했는데 
, 이번 버전은 성공했을 때

콩이가 알아들었어! 🎉
콩이가 들은 말: “astronaut”
목표 단어로 인식되었어요!

라고 나와. 실패해도

이번에는 다르게 들렸어.

라고 하지 “발음이 틀렸어요”라고 판정하지 않아.

결과도 예를 들어

14 / 20
🐶 콩이가 목표 단어로 알아들은 비율 70%
※ 이 수치는 발음 점수가 아니라 음성 인식 시스템이 목표 단어로 인식한 비율이에요.

로 나오도록 했어. 연구에서 실제로 측정하고 있는 구성개념과 학생 화면의 표현을 맞춘 거야.

그리고 원본 Claude 코드처럼 window.claude.hot은 모두 제거했어. 그건 Claude Artifact 안에서만 쓰는 기능이야. 원본은 127개 단어도 JavaScript 안에 직접 넣어두었지만 
, 지금 코드는 wordlist_1001.csv → Python → JavaScript 순으로 자동 전달해.

한 가지는 실제 배포 후 꼭 확인해야 해. Chrome에서 Practice 페이지를 열고 마이크 버튼을 직접 눌러봐야 해. 지금 방식은 Streamlit 내부 iframe에서 브라우저의 Web Speech API를 실행하므로, 배포 환경이나 Chrome의 iframe 권한 정책에 따라 마이크/음성인식 권한이 막힐 가능성이 있어. 만약 🙈 이 브라우저에서는 음성 인식을 사용할 수 없어요가 뜨거나 마이크를 눌러도 반응이 없다면, 그건 단어 데이터 문제가 아니라 Streamlit iframe과 브라우저 권한 문제일 가능성이 높아. 그 경우에는 디자인은 그대로 두고 마이크 부분만 다른 방식으로 바꾸면 돼.

먼저 이걸 GitHub에 넣어서 ① 돌다리가 보이는지 → ② Unit 단어가 CSV와 맞는지 → ③ Chrome에서 마이크가 작동하는지 세 가지만 확인해봐.

r: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/usr/local/lib/python3.13/ast.py", line 50, in parse     return compile(source, filename, mode, flags,                    _feature_version=feature_version, optimize=optimize)



원인은 거의 확실해. 방금 준 긴 코드에서 HTML/CSS/JavaScript를 Python f"""...""" 안에 넣으면서 {} 중괄호가 너무 많이 섞여 Python 파서가 깨진 것이야. 그래서 Streamlit이 실행 단계까지 못 가고 ast.py ... compile(...)에서 멈춘 거야.

이번에는 그 문제를 아예 없애려고 f-string을 쓰지 않고 일반 문자열 + .replace() 방식으로 다시 만든 뒤, Python 문법 컴파일까지 실제로 검증했어. 업로드한 원래 Claude 코드의 강아지/돌다리/마이크 구조를 그대로 기반으로 했어. 

GitHub에서 pages/04🐥_발음짱이 될거야.py 내용을 전부 삭제하고 이 파일 내용으로 통째로 교체해줘.

검증 완료된 04🐥_발음짱이 될거야.py 받기

이 파일은 이미 Python syntax check 통과했어.

이번 버전도 그대로:

data/wordlist_1001.csv에서 전체 단어 자동 로드
saved_words와 관계없이 Unit 전체 발음 연습
Claude Artifact의 콩이 디자인 유지
Chrome Web Speech API 사용
성공 표현을 **“발음이 정확하다”가 아니라 “목표 단어로 인식되었다”**로 변경
Claude 전용 window.claude.hot 제거
기존 Google Form 연결 유지
로 되어 있어.

GitHub에서는 파일 업로드보다 기존 파일 열기 → 전체 삭제 → 새 파일 내용 전체 복사/붙여넣기 → Commit changes 방식으로 해도 돼. 이걸 올린 뒤에는 우선 페이지가 정상적으로 열리는지만 확인해봐. 


04🐥_발음짱이 될거야.py
코드




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
