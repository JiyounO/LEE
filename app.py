import streamlit as st

# 1. 웹페이지 기본 설정
st.set_page_config(page_title="청소년 피로도 지수(PFI) 진단", page_icon="📊", layout="centered")

# 2. 메인 타이틀과 소개글
st.title("📊 청소년 피로도 지수(PFI) 자가진단")
st.markdown("""
현대 성과사회 속에서 청소년인 우리는 스스로를 끝없이 채찍질하는 **'성과주체'**가 되곤 합니다.  
본 플랫폼은 여러분이 느끼는 **성과압박(SA)**과 이를 극복하는 **회복 수준(RA)**을 분석하여,  
나만의 피로 유형과 맞춤형 휴식 솔루션을 제공합니다.
""")
st.markdown("---")

# 3. 질문지 리스트 정의
sa_questions = [
    "나는 남들보다 뒤처지면 안 된다는 불안감을 자주 느낀다.",
    "나에게 설정한 학습 목표는 타인이나 스스로에게 매우 높은 편이다.",
    "시험 성적이 떨어지면 내 존재 가치가 낮아지는 것 같다.",
    "아무것도 하지 않고 쉬는 시간에는 불안해서 무언가 해야 할 것 같다.",
    "나를 끊임없이 계발하고 채찍질해야 마음이 놓인다.",
    "주변(부모님, 선생님, 친구들)의 기대에 부응해야 한다는 부담감이 크다.",
    "미래의 성공을 위해 지금의 힘듦은 당연히 참아야 한다고 생각한다."
]

ra_questions = [
    "하루 평균 6~7시간 이상의 양질의 수면을 취하고 있다.",
    "피곤할 때 언제든 편하게 쉴 수 있는 나만의 공간이나 시간이 있다.",
    "지친 마음을 달래줄 수 있는 나만의 확실한 취미 생활이 있다.",
    "스트레스를 받았을 때 건강하게 해소하는 구체적인 방법을 알고 실행한다.",
    "불안하거나 힘들 때 마음을 터놓고 이야기할 수 있는 사람이 있다.",
    "하루 중 아무 생각 없이 온전히 쉴 수 있는 '멍 때리는' 시간이 있다.",
    "비교적 사소한 일에도 긍정적인 감정을 느끼고 여유를 가질 수 있다.",
    "주말이나 휴일에는 학업 생각을 잊고 충분히 리프레시한다.",
    "나의 신체적, 정신적 한계를 스스로 인지하고 조절할 수 있다.",
    "하루의 일과 끝에 내 마음 상태를 돌아보고 챙겨주는 편이다."
]

# 4. 설문지 UI 디자인 (사용자가 입력하는 영역)
with st.form("pfi_survey_form"):
    st.subheader("Section 1: 성과압박 (SA) 자가진단")
    st.caption("나의 학습 성과 및 성장에 대해 느끼는 심리적 압박 수준을 평가합니다.")
    sa_scores = []
    for i, q in enumerate(sa_questions):
        score = st.select_slider(
            f"Q{i+1}. {q}",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: {
                1: "전혀 아니다 (1점)", 
                2: "아니다 (2점)", 
                3: "보통이다 (3점)", 
                4: "그렇다 (4점)", 
                5: "매우 그렇다 (5점)"
            }[x],
            key=f"sa_{i}"
        )
        sa_scores.append(score)
        
    st.markdown("---")
    
    st.subheader("Section 2: 회복 수준 (RA) 자가진단")
    st.caption("나의 신체적, 정신적 에너지를 재충전할 수 있는 능력과 환경을 평가합니다.")
    ra_scores = []
    for i, q in enumerate(ra_questions):
        score = st.select_slider(
            f"Q{i+8}. {q}",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: {
                1: "전혀 아니다 (1점)", 
                2: "아니다 (2점)", 
                3: "보통이다 (3점)", 
                4: "그렇다 (4점)", 
                5: "매우 그렇다 (5점)"
            }[x],
            key=f"ra_{i}"
        )
        ra_scores.append(score)
        
    st.markdown("---")
    submit_button = st.form_submit_button("나의 피로도 결과 분석하기 🚀")

# 5. 제출 버튼을 눌렀을 때 작동하는 분석 알고리즘
if submit_button:
    # 5-1. 평균값 도출
    sa_avg = sum(sa_scores) / len(sa_scores)
    ra_avg = sum(ra_scores) / len(ra_scores)
    
    # 5-2. 회귀 모델 기반 PFI 연산식 반영
    # 공식: PFI = 4.151 + 0.282*SA - 0.571*RA
    pfi_raw = 4.151 + (0.282 * sa_avg) - (0.571 * ra_avg)
    
    # 5-3. 점수 가공 (PFI 값을 이해하기 쉬운 100점 만점으로 변환하는 매핑 작업)
    # 최악 조건(SA=5, RA=1)의 PFI 최댓값 = 4.991
    # 최선 조건(SA=1, RA=5)의 PFI 최솟값 = 1.578
    pfi_percentage = int(((pfi_raw - 1.578) / (4.991 - 1.578)) * 100)
    pfi_percentage = max(0, min(100, pfi_percentage)) # 범위를 벗어나지 않도록 안전장치
    
    # 5-4. PFI 점수에 따른 직관적 상태 단계 분류
    if pfi_percentage < 40:
        status = "🟢 안정 단계"
        status_desc = "신체적, 심리적 균형이 아주 잘 잡혀 있습니다."
    elif pfi_percentage < 70:
        status = "🟡 주의 단계"
        status_desc = "피로가 누적되고 있습니다. 성과 압박을 덜거나 휴식을 늘려야 합니다."
    else:
        status = "🔴 위험 단계"
        status_desc = "번아웃 직전입니다! 적극적인 휴식과 환경 개선이 긴급히 필요합니다."
        
    # 5-5. 4분면 알고리즘을 활용한 4대 피로 유형 분류 (평균 기준값: 3.0점)
    threshold = 3.0
    if sa_avg >= threshold and ra_avg >= threshold:
        type_name = "🎯 도전형"
        type_desc = "높은 성과 압박을 받고 있지만, 그만큼 스스로를 보살피는 회복 능력과 습관도 훌륭히 갖추고 있습니다."
        recommendations = [
            "현재의 긍정적인 라이프사이클과 회복 루틴을 유지하세요.",
            "다만, 무의식적인 피로가 누적되지 않도록 주기적인 뇌 휴식(멍 때리기 등) 시간을 권장합니다."
        ]
    elif sa_avg < threshold and ra_avg >= threshold:
        type_name = "🌱 균형형"
        type_desc = "과도한 성과 압박에서 자유로우며, 건강하고 규칙적인 휴식 패턴을 유지하는 이상적인 휴식 상태입니다."
        recommendations = [
            "주변 자극에 흔들리지 않는 튼튼한 멘탈을 지니고 있습니다. 아주 훌륭합니다!",
            "지속 가능한 공부와 성장을 위해 현재의 생활 밸런스를 즐기세요."
        ]
    elif sa_avg < threshold and ra_avg < threshold:
        type_name = "🌧 회복부족형"
        type_desc = "성공에 대한 채찍질은 크지 않지만, 잠이 부족하거나 건강한 취미가 없어 에너지가 서서히 고갈되어 가는 상태입니다."
        recommendations = [
            "하루 평균 수면 시간을 최소 6.5시간 이상으로 늘리는 것부터 시작하세요.",
            "유튜브 시청 같은 도파민성 휴식 대신 산책이나 가벼운 독서 등 진정한 쉼을 정해보세요."
        ]
    else: # sa_avg >= threshold and ra_avg < threshold
        type_name = "🔥 과부하형"
        type_desc = "지나치게 높은 성과 지향적 환경에서 끊임없이 압박을 받으나, 이를 정화할 스트레스 해소 창구가 전혀 없는 위험 상태입니다."
        recommendations = [
            "스스로에게 너무 가혹한 공부 목표를 제시하고 있진 않은지 점검하고, 기준을 조금 낮춰보세요.",
            "하루 중 최소 30분은 책상에서 완전히 벗어나 학업 생각을 완전히 차단하는 '의무 휴식 시간'을 가집니다."
        ]

    # 6. 결과 화면 출력 (사용자 친화적 디자인)
    st.markdown("---")
    st.header("📊 분석 진단 리포트")
    
    # 지표 시각화 카드
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="나의 피로도 지수 (PFI)", value=f"{pfi_percentage} 점 / 100")
        st.subheader(status)
        st.caption(status_desc)
    with col2:
        st.markdown(f"**📈 성과압박(SA) 지표:** `{sa_avg:.2f} / 5.0`")
        st.markdown(f"**🧘 회복수준(RA) 지표:** `{ra_avg:.2f} / 5.0`")
        
    st.markdown("---")
    st.subheader(f"🔍 종합 진단 유형: **{type_name}**")
    st.info(type_desc)
    
    st.subheader("💊 맞춤형 회복 처방전")
    for rec in recommendations:
        st.write(f"- {rec}")
