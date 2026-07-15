import streamlit as st

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="청소년 피로도 지수(PFI) 진단", page_icon="📊", layout="centered")

# 2. 질문 데이터 구성
questions = [
    # 성과압박 (SA) 문항 7개 (index 0 ~ 6)
    {"type": "SA", "text": "나는 남들보다 뒤처지면 안 된다는 불안감을 자주 느낀다."},
    {"type": "SA", "text": "나에게 설정한 학습 목표는 타인이나 스스로에게 매우 높은 편이다."},
    {"type": "SA", "text": "시험 성적이 떨어지면 내 존재 가치가 낮아지는 것 같다."},
    {"type": "SA", "text": "아무것도 하지 않고 쉬는 시간에는 불안해서 무언가 해야 할 것 같다."},
    {"type": "SA", "text": "나를 끊임없이 계발하고 채찍질해야 마음이 놓인다."},
    {"type": "SA", "text": "주변(부모님, 선생님, 친구들)의 기대에 부응해야 한다는 부담감이 크다."},
    {"type": "SA", "text": "미래의 성공을 위해 지금의 힘듦은 당연히 참아야 한다고 생각한다."},
    # 회복 수준 (RA) 문항 10개 (index 7 ~ 16)
    {"type": "RA", "text": "하루 평균 6~7시간 이상의 양질의 수면을 취하고 있다."},
    {"type": "RA", "text": "피곤할 때 언제든 편하게 쉴 수 있는 나만의 공간이나 시간이 있다."},
    {"type": "RA", "text": "지친 마음을 달래줄 수 있는 나만의 확실한 취미 생활이 있다."},
    {"type": "RA", "text": "스트레스를 받았을 때 건강하게 해소하는 구체적인 방법을 알고 실행한다."},
    {"type": "RA", "text": "불안하거나 힘들 때 마음을 터놓고 이야기할 수 있는 사람이 있다."},
    {"type": "RA", "text": "하루 중 아무 생각 없이 온전히 쉴 수 있는 '멍 때리는' 시간이 있다."},
    {"type": "RA", "text": "비교적 사소한 일에도 긍정적인 감정을 느끼고 여유를 가질 수 있다."},
    {"type": "RA", "text": "주말이나 휴일에는 학업 생각을 잊고 충분히 리프레시한다."},
    {"type": "RA", "text": "나의 신체적, 정신적 한계를 스스로 인지하고 조절할 수 있다."},
    {"type": "RA", "text": "하루의 일과 끝에 내 마음 상태를 돌아보고 챙겨주는 편이다."}
]

total_questions = len(questions)

# 3. 세션 상태(Session State) 초기화
# 사용자가 버튼을 누를 때마다 화면이 초기화되는 것을 방지하고 데이터를 저장하는 기억 장치입니다.
if "current_step" not in st.session_state:
    st.session_state.current_step = 0  # 현재 질문 번호 (0부터 시작)
if "answers" not in st.session_state:
    st.session_state.answers = {}  # 질문별 답변 저장소
if "survey_completed" not in st.session_state:
    st.session_state.survey_completed = False  # 설문 완료 여부

# 처음 화면 또는 완료 후 다시 하기 화면
def reset_survey():
    st.session_state.current_step = 0
    st.session_state.answers = {}
    st.session_state.survey_completed = False

# --- 메인 헤더 ---
st.title("📊 청소년 피로도 지수(PFI) 자가진단")
st.markdown("현대 성과사회 속에서 나의 **성과압박(SA)**과 **회복 수준(RA)**을 진단합니다.")
st.markdown("---")

# --- 설문이 진행 중일 때 ---
if not st.session_state.survey_completed:
    step = st.session_state.current_step
    q = questions[step]
    
    # 상단 진행 바 (Progress Bar)
    progress_val = (step) / total_questions
    st.progress(progress_val)
    st.write(f"**진행률: {step}/{total_questions} 문항**")
    
    # 카드 스타일 박스
    with st.container(border=True):
        st.write(f"### Q{step+1}. {q['text']}")
        st.caption(f"분류: {'성과압박 요인(SA)' if q['type'] == 'SA' else '회복 능력 요인(RA)'}")
        
        # 기본 선택값 설정 (기존에 선택한 적이 있다면 그 값으로, 없으면 중간값 '보통이다')
        default_idx = st.session_state.answers.get(step, 3) - 1
        
        # 선택형 라디오 버튼 (가로 정렬)
        choice = st.radio(
            "보기를 선택해 주세요:",
            options=["전혀 아니다 (1점)", "아니다 (2점)", "보통이다 (3점)", "그렇다 (4점)", "매우 그렇다 (5점)"],
            index=default_idx,
            horizontal=True
        )
        
        # 문항 선택 점수 추출
        score_map = {
            "전혀 아니다 (1점)": 1,
            "아니다 (2점)": 2,
            "보통이다 (3점)": 3,
            "그렇다 (4점)": 4,
            "매우 그렇다 (5점)": 5
        }
        current_score = score_map[choice]

    # 좌우 이동 버튼 레이아웃
    col_prev, col_spacer, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if step > 0:
            if st.button("⬅️ 이전"):
                # 현재 선택값 임시 저장 후 이전으로
                st.session_state.answers[step] = current_score
                st.session_state.current_step -= 1
                st.rerun()
                
    with col_next:
        if step < total_questions - 1:
            if st.button("다음 ➡️"):
                # 현재 선택값 저장 후 다음으로
                st.session_state.answers[step] = current_score
                st.session_state.current_step += 1
                st.rerun()
        else:
            if st.button("제출하기 🚀"):
                # 마지막 응답 저장 후 결과 페이지로
                st.session_state.answers[step] = current_score
                st.session_state.survey_completed = True
                st.rerun()

# --- 설문이 완료되어 결과를 보여줄 때 ---
else:
    # 1. 성과압박(SA) 및 회복수준(RA) 점수 분리 및 평균 계산
    sa_scores = [st.session_state.answers[i] for i in range(7)]
    ra_scores = [st.session_state.answers[i] for i in range(7, 17)]
    
    sa_avg = sum(sa_scores) / len(sa_scores)
    ra_avg = sum(ra_scores) / len(ra_scores)
    
    # 2. 회귀 모델 기반 PFI 연산식 (PFI = 4.151 + 0.282*SA - 0.571*RA)
    pfi_raw = 4.151 + (0.282 * sa_avg) - (0.571 * ra_avg)
    
    # 3. 점수 백분위 가공 (0~100점 스케일링)
    pfi_percentage = int(((pfi_raw - 1.578) / (4.991 - 1.578)) * 100)
    pfi_percentage = max(0, min(100, pfi_percentage))
    
    # 4. 피로도 상태 단계 분류
    if pfi_percentage < 40:
        status = "🟢 안정 단계"
        status_desc = "신체적, 심리적 균형이 아주 잘 잡혀 있습니다."
    elif pfi_percentage < 70:
        status = "🟡 주의 단계"
        status_desc = "피로가 점차 누적되고 있습니다. 성과 압박을 덜거나 적극적인 휴식이 필요합니다."
    else:
        status = "🔴 위험 단계"
        status_desc = "번아웃 직전입니다! 학업 부담을 조절하고 휴식 시간을 늘려야 합니다."
        
    # 5. 4분면 알고리즘을 활용한 4대 피로 유형 분류
    threshold = 3.0
    if sa_avg >= threshold and ra_avg >= threshold:
        type_name = "🎯 도전형"
        type_desc = "높은 성과 압박을 받고 있지만, 스스로를 관리하고 피로를 풀어내는 회복 습관 또한 잘 형성되어 있습니다."
        recommendations = [
            "훌륭한 에너지 균형 감각을 보이고 있습니다. 지금의 건강한 루틴을 계속 유지하세요.",
            "신체가 보내는 조용한 경고음(안구 건조, 집중력 저하 등)이 있다면 즉시 펜을 내려놓고 쉬어주세요."
        ]
    elif sa_avg < threshold and ra_avg >= threshold:
        type_name = "🌱 균형형"
        type_desc = "과도한 성적 스트레스가 없으며, 건강하고 바람직한 휴식 습관을 유지하고 있는 이상적인 멘탈 상태입니다."
        recommendations = [
            "타인의 속도에 휩쓸리지 않는 단단한 마음을 지녔습니다. 최고의 상태를 즐기세요!",
            "주변 친구들에게 여러분만의 효율적인 스트레스 해소 꿀팁을 공유해 주어도 좋습니다."
        ]
    elif sa_avg < threshold and ra_avg < threshold:
        type_name = "🌧 회복부족형"
        type_desc = "학업에 대한 부담감이 엄청나게 크진 않지만, 기본적인 숙면이 부족하거나 마음 놓고 쉴 시간이 없어 에너지가 방전되어 가고 있습니다."
        recommendations = [
            "유튜브, 릴스 등 뇌를 지치게 만드는 '가짜 휴식' 시간을 낮잠이나 가벼운 스트레칭으로 대체해 보세요.",
            "하루 수면 시간을 최소 6.5시간 확보하는 것을 이번 주 최우선 행동 목표로 잡아보세요."
        ]
    else: # sa_avg >= threshold and ra_avg < threshold
        type_name = "🔥 과부하형"
        type_desc = "성공해야 한다는 강한 심리적 채찍질 아래 밤낮으로 달리고 있지만, 지친 나를 충전해 줄 회복 도구는 턱없이 부족한 극심한 소모 상태입니다."
        recommendations = [
            "스스로에게 부여한 완벽주의적인 기준을 조금 내려놓고, '이 정도면 충분히 잘했다'고 말해주는 연습이 필요합니다.",
            "하루에 단 20분이라도 공부 생각을 완전히 지우는 '의무적 오프라인 시간'을 만들어 음악 감상 등을 즐겨보세요."
        ]

    # --- 결과 시각화 레이아웃 ---
    st.success("🎉 진단이 무사히 완료되었습니다!")
    st.header("📋 나의 피로도 자가진단 결과서")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="나의 피로도 지수 (PFI)", value=f"{pfi_percentage} 점")
        st.subheader(status)
        st.caption(status_desc)
    with col2:
        st.markdown(f"**📈 성과압박(SA) 평균 점수:** `{sa_avg:.2f} / 5.0`")
        st.markdown(f"**🧘 회복수준(RA) 평균 점수:** `{ra_avg:.2f} / 5.0`")
        
    st.markdown("---")
    st.subheader(f"🔍 종합 진단 유형: **{type_name}**")
    st.info(type_desc)
    
    st.subheader("💊 맞춤형 회복 처방전")
    for rec in recommendations:
        st.write(f"- {rec}")
        
    st.markdown("---")
    # 다시 하기 버튼
    if st.button("🔄 테스트 다시 하기"):
        reset_survey()
        st.rerun()
