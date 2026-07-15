import streamlit as st
import pandas as pd

# 1. 웹페이지 기본 설정 및 미려한 CSS 스타일
st.set_page_config(page_title="청소년 피로도 지수(PFI) 진단", page_icon="🧘", layout="centered")

# [업그레이드] 글자 끊김 방지(keep-all) 및 가독성을 극대화한 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        word-break: keep-all; /* 단어 단위로 줄바꿈되어 글자가 어색하게 잘리는 현상 방지 */
    }
    
    /* 성과압박 카드 */
    .sa-card {
        background-color: #FFF5F2;
        border-left: 5px solid #FF8A65;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 20px;
        word-break: keep-all;
    }
    
    /* 회복수준 카드 */
    .ra-card {
        background-color: #F0F9F4;
        border-left: 5px solid #4CAF50;
        padding: 18px;
        border-radius: 10px;
        margin-bottom: 20px;
        word-break: keep-all;
    }
    
    /* 결과 박스 */
    .result-card {
        background-color: #FAFAFA;
        border: 1px solid #E2E8F0;
        padding: 22px;
        border-radius: 14px;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        word-break: keep-all;
    }
    
    .q-text {
        font-size: 15px;
        font-weight: 500;
        color: #1E293B;
        margin-bottom: 6px;
        line-height: 1.5;
        word-break: keep-all;
    }
    
    .stMarkdown p {
        word-break: keep-all;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 원본 17문항 데이터 정의 (SA 7개, RA 10개)
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

# 세션 상태 제어
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "calculated_data" not in st.session_state:
    st.session_state.calculated_data = {}

def reset_survey():
    st.session_state.show_result = False
    st.session_state.calculated_data = {}

# --- [ 화면 1: 설문지 작성 화면 ] ---
if not st.session_state.show_result:
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px; word-break: keep-all;">
        <h1 style="color: #0F172A; font-weight: 700; font-size: 2.1rem; margin-bottom: 8px;">
            🧘 청소년 피로도 지수(PFI) 자가진단
        </h1>
        <p style="color: #64748B; font-size: 0.95rem; line-height: 1.5;">
            스스로를 다그치는 <b>성과압박(SA)</b>과 충전 에너지인 <b>회복수준(RA)</b>을 다차원적으로 평가하여<br>
            현재 나의 심리적 피로도를 정밀하게 측정합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    options = ["전혀 아니다", "아니다", "보통이다", "그렇다", "매우 그렇다"]
    score_map = {"전혀 아니다": 1, "아니다": 2, "보통이다": 3, "그렇다": 4, "매우 그렇다": 5}
    
    with st.form("pfi_survey_form"):
        # Section 1. 성과압박 (7문항)
        st.markdown("""
        <div class="sa-card">
            <h4 style="color: #D32F2F; margin: 0 0 5px 0; font-weight: 700;">Section 1. 성과압박 (Success Pressure)</h4>
            <p style="color: #C62828; font-size: 0.85rem; margin: 0;">나를 갉아먹는 학습 성과에 대한 집착, 주변의 기대감, 실패에 대한 불안 지수를 측정합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sa_answers = []
        for i, q in enumerate(sa_questions):
            st.markdown(f'<p class="q-text"><b>Q{i+1}.</b> {q}</p>', unsafe_allow_html=True)
            choice = st.radio(f"sa_{i}", options=options, index=2, horizontal=True, label_visibility="collapsed")
            sa_answers.append(score_map[choice])
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Section 2. 회복수준 (10문항)
        st.markdown("""
        <div class="ra-card">
            <h4 style="color: #2E7D32; margin: 0 0 5px 0; font-weight: 700;">Section 2. 회복 수준 (Recovery Ability)</h4>
            <p style="color: #1B5E20; font-size: 0.85rem; margin: 0;">피로를 밀어내는 건강한 신체 수면 환경, 스트레스 방어 및 심리적 완충 능력을 측정합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        ra_answers = []
        for i, q in enumerate(ra_questions):
            st.markdown(f'<p class="q-text"><b>Q{i+8}.</b> {q}</p>', unsafe_allow_html=True)
            choice = st.radio(f"ra_{i}", options=options, index=2, horizontal=True, label_visibility="collapsed")
            ra_answers.append(score_map[choice])
            st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        submit_btn = st.form_submit_button("🔍 내 피로도 상태 분석하기", use_container_width=True)
        
    if submit_btn:
        sa_avg = sum(sa_answers) / len(sa_answers)
        ra_avg = sum(ra_answers) / len(ra_answers)
        
        # [수학적 보정 적용] 오차 없는 백분율 변환 (최하 1.578점 ~ 최고 4.991점 범위 기준)
        pfi_raw = 4.151 + (0.282 * sa_avg) - (0.571 * ra_avg)
        pfi_min, pfi_max = 1.578, 4.991
        pfi_percentage = int(((pfi_raw - pfi_min) / (pfi_max - pfi_min)) * 100)
        pfi_percentage = max(0, min(100, pfi_percentage))
        
        st.session_state.calculated_data = {
            "sa_avg": sa_avg,
            "ra_avg": ra_avg,
            "pfi": pfi_percentage
        }
        st.session_state.show_result = True
        st.rerun()

# --- [ 화면 2: 직관적인 리포트 결과 화면 ] ---
else:
    data = st.session_state.calculated_data
    sa_avg = data["sa_avg"]
    ra_avg = data["ra_avg"]
    pfi_percentage = data["pfi"]
    
    # 4가지 핵심 유형 판정 로직 (기준값 3.0점)
    threshold = 3.0
    
    if sa_avg < threshold and ra_avg >= threshold:
        # 🌿 Recovery Type (회복 충분)
        type_emoji = "🌿"
        type_id = "Recovery Type"
        type_title = "Recovery Type (회복 충분 유형)"
        status_color = "#4CAF50"
        
        key_issue = "현재 균형 유지"
        keywords = "안정적 회복 및 셀프 케어 지속"
        
        features = ["회복 수준(RA)이 높고 스트레스 자가 조절 능력이 뛰어남.", "현재 신체 및 심리적 균형이 비교적 안정적임."]
        direction = "현재의 효율적인 회복 시스템을 유지하고 학습과의 균형 예방적 관리"
        proposals = [
            "현재 좋은 퀄리티를 보이는 수면·휴식 루틴을 타협하지 말고 유지하기",
            "바쁜 학기 중에도 자신만의 스트레스 해소 시간(코인노래방, 산책 등) 거르지 않기",
            "학습 목표를 세울 때 신체 한계를 시험하는 무리한 계획으로 넘어가지 않기"
        ]
        sample_text = "현재 충분한 회복 능력을 가지고 있습니다. 높은 성과보다 지속 가능한 생활 균형을 유지하는 것이 중요합니다."
        
    elif sa_avg >= threshold and ra_avg >= threshold:
        # 🎯 Challenge Type (도전형)
        type_emoji = "🎯"
        type_id = "Challenge Type"
        type_title = "Challenge Type (도전형)"
        status_color = "#2196F3"
        
        key_issue = "가속 뒤의 브레이크 확인"
        keywords = "적절한 오프(Off) 스위치 확보"
        
        features = ["열정이 높고 성취 의욕도 강하지만, 동시에 쉬어갈 줄 아는 똑똑한 생존자 유형.", "동기부여 수준이 매우 높음."]
        direction = "높은 텐션을 유지하되 시험 기간 일시적 과부하 방지"
        proposals = [
            "수행평가 집중 기간처럼 압박이 급증할 때 회복 밸런스가 무너지지 않게 브레이크 점검하기",
            "플래너를 작성할 때 하루 최소 30분은 '학업 생각 멈춤 세션'을 강제 배치하기",
            "피로 누적으로 인한 긴장성 두통이나 안구 건조 등 신체 신호를 무시하지 않기"
        ]
        sample_text = "뜨거운 열정만큼 회복하는 법도 잘 아는 훌륭한 상태입니다. 지치지 않는 영리한 완급 조절이 무기입니다."

    elif sa_avg >= threshold and ra_avg < threshold:
        # 🔥 Overdrive Type (성과압박 과다)
        type_emoji = "🔥"
        type_id = "Overdrive Type"
        type_title = "Overdrive Type (성과과부하 유형)"
        status_color = "#FF5722"
        
        key_issue = "끊임없이 더 잘해야 한다는 압박 (자기착취)"
        keywords = "목표 조절 및 완벽주의 완화"
        
        features = ["목표 수준과 기대치가 지나치게 높아 스스로를 가혹하게 몰아세움.", "휴식을 취할 때조차 무언가를 안 하면 심한 불안을 느낌."]
        direction = "타이트한 성과 기준 하향 조정 및 강박적 자기압박 완화"
        proposals = [
            "목표 설정을 결과 중심('무조건 1등급')에서 과정 중심('오늘 계획한 분량 채우기')으로 바꾸기",
            "하루 중 아무런 생산적 활동을 하지 않는 '합법적 멍 때리기 시간' 선물하기",
            "시험 점수가 곧 나의 인간적 가치와 존엄을 정하지 않는다는 사실을 인지하기"
        ]
        sample_text = "높은 목표 의식은 좋으나 스스로를 낭떠러지로 몰아세우고 있습니다. 노력의 양보다 '지속 가능한 방식'을 찾는 것이 우선입니다."

    else: # sa_avg < threshold and ra_avg < threshold
        # 🌧 Fatigue Type (피로 누적)
        type_emoji = "🌧"
        type_id = "Fatigue Type"
        type_title = "Fatigue Type (피로 누적 유형)"
        status_color = "#9C27B0"
        
        key_issue = "너무 많이 하는 것보다 회복의 절대적 부족"
        keywords = "수면 시간 확보 및 자극 배제"
        
        features = ["학업 압박감 자체가 숨 막힐 정도는 아니지만, 생활 리듬이 깨져 에너지가 바닥난 상태.", "만성 피로 호소."]
        direction = "기본적인 생활 리듬 및 신체 에너지 복원"
        proposals = [
            "하원 후나 취침 전 침대에 누워 스마트폰(릴스, 쇼츠)을 보며 뇌를 자극하는 행동 줄이기",
            "단 10분이라도 낮시간에 햇볕을 쬐며 걷는 등의 무자극적 충전 시간 가지기",
            "우선순위가 낮은 활동을 정리하여 절대적인 밤 수면 시간(최소 6시간 이상) 늘리기"
        ]
        sample_text = "현재 에너지가 바닥나 피로가 해소되지 못하는 상태입니다. 더 쥐어짜기보다 온전한 수면과 휴식을 챙길 때입니다."

    # 3. 결과 대시보드 렌더링
    st.markdown("""
    <div style="text-align: center; margin-top: 15px; word-break: keep-all;">
        <h2 style="color: #0F172A; font-weight: 700; margin-bottom: 5px;">📊 나의 진단 결과 리포트</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card" style="border-top: 5px solid {status_color};">
        <div style="text-align: center; margin-bottom: 15px;">
            <p style="color: #64748B; font-size: 0.9rem; margin-bottom: 2px; font-weight: 500;">나의 최종 피로도 점수 (PFI)</p>
            <h1 style="font-size: 3.2rem; color: #0F172A; margin: 0; font-weight: 800;">{pfi_percentage} <span style="font-size: 1.3rem; font-weight: 500; color: #64748B;">점 / 100</span></h1>
            <h3 style="color: {status_color}; font-weight: 700; margin-top: 10px; font-size: 1.3rem;">{type_emoji} {type_title}</h3>
        </div>
        <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 15px 0;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <p style="margin: 0; color: #E64A19; font-size: 0.8rem; font-weight: 600;">📈 성과압박 평균 (SA)</p>
                <p style="margin: 3px 0 0 0; font-size: 1.25rem; font-weight: 700; color: #1E293B;">{sa_avg:.2f} <span style="font-size: 0.8rem; font-weight: 400; color: #94A3B8;">/ 5</span></p>
            </div>
            <div style="border-left: 1px solid #E2E8F0;"></div>
            <div>
                <p style="margin: 0; color: #388E3C; font-size: 0.8rem; font-weight: 600;">🧘 회복수준 평균 (RA)</p>
                <p style="margin: 3px 0 0 0; font-size: 1.25rem; font-weight: 700; color: #1E293B;">{ra_avg:.2f} <span style="font-size: 0.8rem; font-weight: 400; color: #94A3B8;">/ 5</span></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # 4. 피로도 유형 총괄 표 구현
    st.markdown("### 📋 피로도 유형 총괄 요약")
    
    summary_data = {
        "유형": ["🌿 Recovery", "🎯 Challenge", "🔥 Overdrive", "🌧 Fatigue"],
        "구분": ["회복 충분", "도전형 (균형)", "성과 압박 과다", "회복 부족"],
        "핵심 문제": ["안정적 회복", "가속/감속 균형", "끊임없는 학업 부담 (자기착취)", "절대적 충전 시간 부족"],
        "추천 키워드": ["현재 균형 유지", "적절한 오프 확보", "목표 조절·완벽주의 완화", "수면·휴식 환경 개선"]
    }
    
    df_summary = pd.DataFrame(summary_data)
    
    st.dataframe(
        df_summary, 
        use_container_width=True, 
        hide_index=True
    )
    
    st.markdown("---")
    
    # 5. 개인 유형별 상세 진단 리포트 출력
    st.markdown(f"### 상세 분석: {type_emoji} {type_title}")
    
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border-radius: 8px; padding: 15px; border-left: 4px solid {status_color}; margin-bottom: 20px; word-break: keep-all;">
        <strong>📢 한줄 진단</strong><br>
        <p style="margin: 5px 0 0 0; color: #334155;"><em>"{sample_text}"</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📌 나의 특징 및 문제점**")
        for ft in features:
            st.markdown(f"- {ft}")
            
    with col2:
        st.markdown("**🧭 앞으로 나아갈 방향**")
        st.markdown(f"- **{direction}**")
        
    st.markdown("#### 💡 학생을 위한 실천 행동 제안")
    for prop in proposals:
        st.markdown(f"- {prop}")

    st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)
    
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        reset_survey()
        st.rerun()
