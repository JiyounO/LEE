%%writefile app.py
import streamlit as st

# 1. 웹페이지 기본 설정 및 미려한 CSS 스타일 입히기
st.set_page_config(page_title="청소년 피로도 지수(PFI) 진단", page_icon="🧘", layout="centered")

# 고급스러운 커스텀 CSS 주입 (안 예쁜 기본 테마 탈피)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    /* 전체 폰트 적용 */
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    /* 성과압박 카드 스타일 */
    .sa-card {
        background-color: #FFF5F2;
        border-left: 5px solid #FF8A65;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* 회복수준 카드 스타일 */
    .ra-card {
        background-color: #F0F9F4;
        border-left: 5px solid #4CAF50;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* 메인 결과 카드 스타일 */
    .result-card {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        padding: 25px;
        border-radius: 16px;
        margin-top: 20px;
        box-shadow: 0 10px 15px rgba(0,0,0,0.05);
    }
    
    /* 질문 텍스트 스타일 */
    .q-text {
        font-size: 16px;
        font-weight: 500;
        color: #2C3E50;
        margin-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 질문 데이터 구성
sa_questions = [
    "나는 남들보다 뒤처지면 안 된다는 불안감을 자주 느낀다.",
    "나에게 설정한 학업 및 성장 목표는 스스로에게 매우 높은 편이다.",
    "시험 성적이나 성과가 떨어지면 내 존재 가치마저 낮아지는 것 같다.",
    "아무것도 하지 않고 쉴 때조차 불안해서 무언가 학습을 해야 할 것 같다.",
    "끊임없이 나를 채찍질하고 자기계발을 해야만 마음이 놓인다.",
    "부모님, 선생님, 혹은 친구들의 기대에 부응해야 한다는 부담감이 크다.",
    "더 나은 미래의 성공을 위해 지금의 신체적·심리적 고통은 당연히 참아야 한다."
]

ra_questions = [
    "하루 평균 6~7시간 이상의 규칙적이고 질 좋은 수면을 취하고 있다.",
    "지치고 피곤할 때 언제든 완전히 방해받지 않고 쉴 수 있는 나만의 시공간이 있다.",
    "학업 스트레스를 완전히 잊고 몰입할 수 있는 나만의 확실한 취미 생활이 있다.",
    "지친 마음과 스트레스를 해소할 수 있는 건강하고 구체적인 방법을 알고 실천한다.",
    "불안하거나 힘들 때 언제든 마음을 터놓고 의지할 수 있는 지지자(친구, 가족 등)가 있다.",
    "하루 중 아무런 생각이나 생산적인 활동을 하지 않고 온전히 뇌를 쉬어주는 시간이 있다.",
    "비교적 일상적인 소소한 일에서도 쉽게 행복감을 느끼고 마음에 여유가 있는 편이다.",
    "주말이나 방학, 공휴일에는 학업에 대한 긴장을 내려놓고 리프레시를 잘하는 편이다.",
    "내 몸과 마음이 한계에 도달했다는 위험 신호를 스스로 인지하고 휴식을 결정할 수 있다.",
    "바쁜 하루 끝에 오늘 고생한 내 마음에 질문을 던지고 다독여주는 감정적 여유가 있다."
]

# 세션 상태(결과 보기 화면 제어용)
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "calculated_data" not in st.session_state:
    st.session_state.calculated_data = {}

def reset_survey():
    st.session_state.show_result = False
    st.session_state.calculated_data = {}

# --- [ 화면 1: 설문지 및 설명란 작성 화면 ] ---
if not st.session_state.show_result:
    
    # 3. 플랫폼 설명란 수정 (학술적이고 세련되게 수정)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #1E293B; font-weight: 700; font-size: 2.2rem; margin-bottom: 10px;">
            🧘 청소년 피로도 지수(PFI) 자가진단
        </h1>
        <p style="color: #64748B; font-size: 1.05rem; line-height: 1.6;">
            현대 성과사회는 강요가 아닌 <b>'스스로 더 높은 성과를 요구하는 자기착취'</b>를 만들어냅니다.<br>
            본 진단은 고등학생이 겪는 <b>성과압박(Success Pressure)</b>과 이를 정화하는 <b>회복능력(Recovery Ability)</b>을<br>
            동시에 분석하여 수치화한 개인 맞춤형 피로도 예측 프로그램입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 선택지 옵션 정의
    options = ["전혀 아니다", "아니다", "보통이다", "그렇다", "매우 그렇다"]
    score_map = {"전혀 아니다": 1, "아니다": 2, "보통이다": 3, "그렇다": 4, "매우 그렇다": 5}
    
    # 폼 영역 시작
    with st.form("pfi_full_survey"):
        
        # 성과압박(SA) 섹션 카드 디자인
        st.markdown("""
        <div class="sa-card">
            <h3 style="color: #D32F2F; margin-top: 0; font-weight: 700;">Section 1. 성과압박 (Success Pressure) 요인</h3>
            <p style="color: #E64A19; font-size: 0.9rem; margin-bottom: 0;">나를 갉아먹는 학습 성과에 대한 집착, 타인의 기대, 실패에 대한 불안 지수를 측정합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sa_answers = []
        for i, q in enumerate(sa_questions):
            st.markdown(f'<p class="q-text"><b>Q{i+1}.</b> {q}</p>', unsafe_allow_html=True)
            choice = st.radio(
                f"sa_q_{i}", 
                options=options, 
                index=2, 
                horizontal=True, 
                label_visibility="collapsed"
            )
            sa_answers.append(score_map[choice])
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # 회복수준(RA) 섹션 카드 디자인
        st.markdown("""
        <div class="ra-card">
            <h3 style="color: #2E7D32; margin-top: 0; font-weight: 700;">Section 2. 회복 수준 (Recovery Ability) 요인</h3>
            <p style="color: #388E3C; font-size: 0.9rem; margin-bottom: 0;">피로를 밀어내는 건강한 신체 수면 환경, 심리적 여유, 스트레스 방어 능력을 측정합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        ra_answers = []
        for i, q in enumerate(ra_questions):
            st.markdown(f'<p class="q-text"><b>Q{i+8}.</b> {q}</p>', unsafe_allow_html=True)
            choice = st.radio(
                f"ra_q_{i}", 
                options=options, 
                index=2, 
                horizontal=True, 
                label_visibility="collapsed"
            )
            ra_answers.append(score_map[choice])
            st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # 제출 버튼
        submit_button = st.form_submit_button(
            "🔒 응답 제출하고 피로도 분석 결과 확인하기", 
            use_container_width=True
        )
        
    if submit_button:
        # 데이터 연산 처리 및 결과 페이지로 상태 변경
        sa_avg = sum(sa_answers) / len(sa_answers)
        ra_avg = sum(ra_answers) / len(ra_answers)
        
        pfi_raw = 4.151 + (0.282 * sa_avg) - (0.571 * ra_avg)
        pfi_percentage = int(((pfi_raw - 1.578) / (4.991 - 1.578)) * 100)
        pfi_percentage = max(0, min(100, pfi_percentage))
        
        st.session_state.calculated_data = {
            "sa_avg": sa_avg,
            "ra_avg": ra_avg,
            "pfi": pfi_percentage
        }
        st.session_state.show_result = True
        st.rerun()

# --- [ 화면 2: 결과를 눌렀을 때만 나타나는 깔끔한 리포트 화면 ] ---
else:
    data = st.session_state.calculated_data
    sa_avg = data["sa_avg"]
    ra_avg = data["ra_avg"]
    pfi_percentage = data["pfi"]
    
    # 4. 결과에 따른 상태 및 피드백 알고리즘
    if pfi_percentage < 40:
        status = "🟢 안정 단계"
        status_desc = "성과에 매몰되지 않고 일상의 에너지를 훌륭하게 회복 및 보존하고 있습니다."
        accent_color = "#4CAF50"
    elif pfi_percentage < 70:
        status = "🟡 주의 단계"
        status_desc = "피로가 점차 쌓이고 있습니다. 성과 압박의 속도를 늦추거나 휴식 비중을 올리세요."
        accent_color = "#FF9800"
    else:
        status = "🔴 위험 단계"
        status_desc = "번아웃 경보! 가혹한 학업 자극을 통제하고 반드시 충분한 숙면과 휴식이 동반되어야 합니다."
        accent_color = "#F44336"
        
    threshold = 3.0
    if sa_avg >= threshold and ra_avg >= threshold:
        type_name = "🎯 도전형 (High SA, High RA)"
        type_desc = "목표 달성에 대한 욕심과 성과 압박이 강하지만, 이를 완충해 줄 건강한 휴식 습관과 에너지를 갖춘 다이내믹한 밸런서 유형입니다."
        recommendations = [
            "학업 추진력은 훌륭하나, 신체 피로(어깨 결림, 만성 눈 피로 등)를 당연한 희생으로 여기지 않도록 신체 신호를 적극 살피세요.",
            "주기적인 '완벽한 멍 때리기' 또는 디지털 디톡스(스마트폰과 단절된 쉼)를 의도적으로 도입해 보세요."
        ]
    elif sa_avg < threshold and ra_avg >= threshold:
        type_name = "🌱 균형형 (Low SA, High RA)"
        type_desc = "현대 성과사회의 압박에 휩쓸리지 않으며, 나를 소중히 보살피는 훌륭한 회복 루틴을 정착시킨 가장 이상적이고 단단한 평정형 인재입니다."
        recommendations = [
            "현재의 바람직한 가치관과 생활 밸런스를 지켜나가며 주체적인 성장을 이어 나가세요.",
            "성과에 대한 몰두가 필요할 때도 조급함 없이 페이스를 건강하게 유지할 수 있는 에너지가 있습니다."
        ]
    elif sa_avg < threshold and ra_avg < threshold:
        type_name = "🌧 회복부족형 (Low SA, Low RA)"
        type_desc = "달려야 한다는 심리적 압박 수준 자체는 보통이거나 낮은 편이지만, 불규칙한 생활 패턴이나 휴식 방법 부재로 일상의 활력이 꺼져가는 상태입니다."
        recommendations = [
            "수면 시간을 30분 늘리고, 자기 전 스마트폰 블루라이트를 차단하는 미시적인 변화부터 정교하게 시작해 보세요.",
            "단순 수동적인 영상 시청 대신 몸을 살짝 움직이는 산책이나 좋아하는 음악 감상 같은 진짜 스트레스 해소법을 탐색해 보세요."
        ]
    else: # sa_avg >= threshold and ra_avg < threshold
        type_name = "🔥 과부하형 (High SA, Low RA)"
        type_desc = "한병철이 말하는 전형적인 '자기착취적 성과주체'입니다. 목표는 지나치게 높고 스스로를 향한 채찍질은 강하나, 안식을 취할 도피처가 없어 연소해 버린 상태입니다."
        recommendations = [
            "마음의 성과 기준선을 강제로 15% 깎아보고, 성적이 나의 존엄함을 결정하지 않는다는 사실을 인지적으로 수용해야 합니다.",
            "하루 일과표 중 반드시 '학업 및 생산적 활동 완전 금지 영역(최소 40분)'을 시간표에 고정 배치하세요."
        ]

    # 결과 전용 UI 렌더링
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <span style="font-size: 3rem;">📋</span>
        <h2 style="color: #1E293B; font-weight: 700; margin-top: 10px;">청소년 피로도 진단 리포트</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 세련된 단독 결과 상자
    st.markdown(f"""
    <div class="result-card" style="border-top: 6px solid {accent_color};">
        <div style="text-align: center; margin-bottom: 20px;">
            <p style="color: #64748B; font-size: 1rem; margin-bottom: 2px; font-weight: 500;">나의 최종 개인 피로도 지수 (PFI)</p>
            <h1 style="font-size: 3.5rem; color: #1E293B; margin: 0; font-weight: 800;">{pfi_percentage} <span style="font-size: 1.5rem; font-weight: 500; color: #64748B;">점 / 100</span></h1>
            <h3 style="color: {accent_color}; font-weight: 700; margin-top: 10px; font-size: 1.4rem;">{status}</h3>
            <p style="color: #475569; font-size: 0.95rem; line-height: 1.5; max-width: 500px; margin: 0 auto; margin-top: 5px;">{status_desc}</p>
        </div>
        <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 20px 0;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <p style="margin: 0; color: #E64A19; font-size: 0.85rem; font-weight: 600;">📈 성과압박 평균 (SA)</p>
                <p style="margin: 5px 0 0 0; font-size: 1.4rem; font-weight: 700; color: #1E293B;">{sa_avg:.2f} <span style="font-size: 0.9rem; font-weight: 400; color: #94A3B8;">/ 5</span></p>
            </div>
            <div style="border-left: 1px solid #E2E8F0;"></div>
            <div>
                <p style="margin: 0; color: #388E3C; font-size: 0.85rem; font-weight: 600;">🧘 회복수준 평균 (RA)</p>
                <p style="margin: 5px 0 0 0; font-size: 1.4rem; font-weight: 700; color: #1E293B;">{ra_avg:.2f} <span style="font-size: 0.9rem; font-weight: 400; color: #94A3B8;">/ 5</span></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 4대 피로 유형 안내 박스
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border-radius: 12px; padding: 20px; border: 1px solid #E2E8F0; margin-bottom: 25px;">
        <h4 style="margin: 0 0 10px 0; color: #0F172A; font-size: 1.15rem; font-weight: 700;">🧩 나의 다차원 유형 진단: <span style="color: #3B82F6;">{type_name}</span></h4>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.6; margin: 0;">{type_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 맞춤 처방전 리스트
    st.subheader("💡 개인 맞춤형 피로 조절 솔루션")
    for rec in recommendations:
        st.markdown(f"- {rec}")
        
    st.markdown("<div style='margin-bottom: 40px;'></div>", unsafe_allow_html=True)
    
    # 다시 하기 버튼
    if st.button("🔄 처음으로 돌아가 자가진단 다시 하기", use_container_width=True):
        reset_survey()
        st.rerun()
