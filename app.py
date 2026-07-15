import streamlit as st
import pandas as pd

# 1. 웹페이지 기본 설정 및 미려한 CSS 스타일
st.set_page_config(page_title="청소년 피로도 지수(PFI) 진단", page_icon="🧘", layout="centered")

# [글자 크기를 줄이고 깔끔한 UI를 연출한 CSS (하단 배지 제거 버전)]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght=300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        word-break: keep-all; /* 단어 단위 줄바꿈 */
    }
    
    /* ------------------------------------------- */
    /* 🚀 스트림릿 기본 하단 배지 및 푸터 강제 제거 */
    footer {visibility: hidden !important;}
    div[data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    div.embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden !important;}
    /* ------------------------------------------- */
    
    /* 성과압박 카드 (텍스트 크기 축소) */
    .sp-card {
        background-color: #FFF5F2;
        border-left: 5px solid #FF8A65;
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 16px;
        word-break: keep-all;
    }
    .sp-card h4 {
        font-size: 0.95rem !important;
        margin: 0 0 4px 0 !important;
    }
    .sp-card p {
        font-size: 0.8rem !important;
        margin: 0 !important;
    }
    
    /* 회복경험 카드 (텍스트 크기 축소) */
    .ra-card {
        background-color: #F0F9F4;
        border-left: 5px solid #4CAF50;
        padding: 14px 16px;
        border-radius: 10px;
        margin-bottom: 16px;
        word-break: keep-all;
    }
    .ra-card h4 {
        font-size: 0.95rem !important;
        margin: 0 0 4px 0 !important;
    }
    .ra-card p {
        font-size: 0.8rem !important;
        margin: 0 !important;
    }
    
    /* 결과 박스 */
    .result-card {
        background-color: #FAFAFA;
        border: 1px solid #E2E8F0;
        padding: 18px;
        border-radius: 12px;
        margin-top: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.02);
        word-break: keep-all;
    }
    
    /* 문항 글씨 크기 축소 */
    .q-text {
        font-size: 13.5px;
        font-weight: 500;
        color: #1E293B;
        margin-bottom: 4px;
        line-height: 1.4;
        word-break: keep-all;
    }
    
    .stMarkdown p {
        font-size: 13.5px;
        word-break: keep-all;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 업데이트된 최종 문항 데이터 정의
sp_questions = [
    "좋은 성적을 받아야 한다는 부담을 느꼈다.",
    "기대한 성적을 받지 못할까 봐 걱정한 적이 있었다.",
    "다른 학생들과 나를 비교하며 부담을 느꼈다.",
    "쉬고 있을 때에도 공부나 해야 할 일이 계속 떠올랐다.",
    "스스로에게 높은 학업 성과를 기대했다.",
    "기대한 만큼의 성과를 내지 못했을 때 스스로를 많이 탓했다.",
    "우리 학교는 성적과 결과를 중요하게 여기는 분위기라고 느꼈다.",
    "휴식을 취하면서도 공부를 해야 한다는 생각이 자주 들었다."
]

ra_questions = [
    "공부를 잠시 잊고 편안하게 쉬는 시간을 가졌다.",
    "충분한 휴식을 취했다고 느꼈다.",
    "학업으로 인한 부담감을 내려놓고 쉴 수 있었다.",
    "여가 시간을 보내며 재충전할 수 있었다.",
    "내가 하고 싶은 활동을 할 시간을 가졌다.",
    "편안한 활동을 하며 긴장을 풀 수 있었다.",
    "공부와 휴식 시간을 스스로 조절할 수 있었다.",
    "힘들 때 편하게 이야기할 수 있는 사람이 있었다.",
    "하루를 마친 뒤 피로가 어느 정도 해소되었다고 느꼈다.",
    "다음 날을 시작할 에너지가 충분하다고 느꼈다."
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
    <div style="text-align: center; margin-bottom: 20px; word-break: keep-all;">
        <h1 style="color: #0F172A; font-weight: 700; font-size: 1.7rem; margin-bottom: 6px;">
            🧘 청소년 피로도 지수(PFI) 자가진단
        </h1>
        <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4;">
            스스로를 다그치는 성과압박(SP)과 충전 에너지인 회복경험(RA)을 다차원적으로 평가하여<br>
            현재 나의 심리적 피로도를 정밀하게 측정합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 공통 라벨 옵션
    options = ["전혀 그렇지 않았다", "그렇지 않았다", "보통이다", "그렇다", "매우 그렇다"]
    score_map = {"전혀 그렇지 않았다": 1, "그렇지 않았다": 2, "보통이다": 3, "그렇다": 4, "매우 그렇다": 5}
    
    with st.form("pfi_survey_form"):
        # Section 1. 성과압박 (8문항)
        st.markdown("""
        <div class="sp-card">
            <h4 style="color: #D32F2F; font-weight: 700;">Section 1. 성과압박 (Success Pressure, SP)</h4>
            <p style="color: #C62828; line-height: 1.4;">
                다음 문항은 최근 한 달 동안 학교생활과 학업을 하면서 느낀 경험에 관한 내용입니다. 각 문항을 읽고 자신의 경험과 가장 가까운 정도를 선택해 주세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        sp_answers = []
        for i, q in enumerate(sp_questions):
            st.markdown(f'<p class="q-text"><b>Q{i+1}.</b> {q}</p>', unsafe_allow_html=True)
            # [수정] index=None으로 설정하여 초기 체크상태 해제
            choice = st.radio(f"sp_{i}", options=options, index=None, horizontal=True, label_visibility="collapsed")
            sp_answers.append(choice)
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Section 2. 회복경험 (10문항)
        st.markdown("""
        <div class="ra-card">
            <h4 style="color: #2E7D32; font-weight: 700;">Section 2. 회복경험 (Recovery Experience, RA)</h4>
            <p style="color: #1B5E20; line-height: 1.4;">
                다음 문항은 최근 한 달 동안 학교 수업과 공부를 마친 후 얼마나 충분히 휴식하고 회복했는지에 관한 내용입니다. 자신의 경험과 가장 가까운 정도를 선택해 주세요.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        ra_answers = []
        for i, q in enumerate(ra_questions):
            st.markdown(f'<p class="q-text"><b>Q{i+9}.</b> {q}</p>', unsafe_allow_html=True)
            # [수정] index=None으로 설정하여 초기 체크상태 해제
            choice = st.radio(f"ra_{i}", options=options, index=None, horizontal=True, label_visibility="collapsed")
            ra_answers.append(choice)
            st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Section 3. 주관적 인지 피로도 (분석용 선택 문항)
        st.markdown("""
        <div style="background-color: #F8FAFC; border-left: 5px solid #64748B; padding: 14px 16px; border-radius: 10px; margin-bottom: 16px; word-break: keep-all;">
            <h4 style="color: #334155; margin: 0 0 4px 0; font-weight: 700; font-size: 0.95rem;">Section 3. 주관적 피로도 (Self-Perceived Fatigue)</h4>
            <p style="color: #475569; font-size: 0.8rem; margin: 0;">스스로 인지하고 있는 현재의 전반적인 에너지 상태를 선택적으로 체크합니다.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="q-text"><b>Q19.</b> 현재 나의 전반적인 피로 수준은 어느 정도라고 생각하나요?</p>', unsafe_allow_html=True)
        subjective_options = ["매우 낮다", "낮다", "보통이다", "높다", "매우 높다"]
        # [수정] index=None으로 설정하여 초기 체크상태 해제
        subjective_choice = st.radio("subjective_fatigue", options=subjective_options, index=None, horizontal=True, label_visibility="collapsed")
        
        st.markdown("---")
        
        submit_btn = st.form_submit_button("🔍 내 피로도 상태 분석하기", use_container_width=True)
        
    if submit_btn:
        # [수정] 필수 질문 답변 여부 검증 (답변이 안 된 None 값이 하나라도 있을 경우)
        if None in sp_answers or None in ra_answers or subjective_choice is None:
            st.error("⚠️ 아직 답변하지 않은 문항이 있습니다. 모든 질문에 답한 뒤 다시 제출해 주세요!")
        else:
            # 매핑 테이블을 이용해 텍스트 값을 숫자로 변환
            sp_scores = [score_map[ans] for ans in sp_answers]
            ra_scores = [score_map[ans] for ans in ra_answers]
            subjective_score = subjective_options.index(subjective_choice) + 1
            
            sp_avg = sum(sp_scores) / len(sp_scores)
            ra_avg = sum(ra_scores) / len(ra_scores)
            
            # [수학적 보정 적용] 오차 없는 백분율 변환 (8문항 및 10문항 기준 가중치 계산)
            pfi_raw = 4.151 + (0.282 * sp_avg) - (0.571 * ra_avg)
            pfi_min, pfi_max = 1.578, 4.991
            pfi_percentage = int(((pfi_raw - pfi_min) / (pfi_max - pfi_min)) * 100)
            pfi_percentage = max(0, min(100, pfi_percentage))
            
            st.session_state.calculated_data = {
                "sp_avg": sp_avg,
                "ra_avg": ra_avg,
                "pfi": pfi_percentage,
                "subjective_score": subjective_score
            }
            st.session_state.show_result = True
            st.rerun()

# --- [ 화면 2: 직관적인 리포트 결과 화면 ] ---
else:
    data = st.session_state.calculated_data
    sp_avg = data["sp_avg"]
    ra_avg = data["ra_avg"]
    pfi_percentage = data["pfi"]
    subjective_score = data["subjective_score"]
    
    # PFI 백분율 기반 위험 단계 정의
    if pfi_percentage < 35:
        risk_level = "안정 (Low Risk)"
        risk_color = "#4CAF50"
        risk_desc = "신체적·정신적 에너지가 건강하게 잘 분배되고 있는 상태입니다."
    elif pfi_percentage < 70:
        risk_level = "주의 (Moderate Risk)"
        risk_color = "#FF9800"
        risk_desc = "서서히 피로가 쌓이고 있습니다. 일상 속에서 가벼운 휴식을 의도적으로 배치해야 합니다."
    else:
        risk_level = "위험 (High Risk)"
        risk_color = "#F44336"
        risk_desc = "번아웃 및 심한 피로 축적 상태입니다. 학업 계획을 조정하고 적극적인 휴식을 권장합니다."

    # 4가지 핵심 유형 판정 로직 (기준값 3.0점)
    threshold = 3.0
    
    if sp_avg < threshold and ra_avg >= threshold:
        # 🌿 Recovery Type (회복 충분 유형)
        type_emoji = "🌿"
        type_id = "Recovery Type"
        type_title = "Recovery Type (회복 충분 유형)"
        status_color = "#4CAF50"
        
        state_desc = "성과와 회복의 균형이 비교적 잘 유지되고 있습니다. 현재의 생활 방식이 피로를 예방하는 보호 요인으로 작용하고 있습니다."
        proposals = [
            "🌿 **회복 시간을 일정처럼 예약해 보세요.**  \n→ 시험 기간에도 휴식 시간을 '남으면 쉬는 시간'이 아니라 계획된 일정으로 남겨두세요.",
            "🌿 **회복 효과가 컸던 활동 하나를 계속 이어가세요.**  \n→ 산책, 운동, 음악 감상 등 나에게 잘 맞는 회복 방법은 바꾸기보다 꾸준히 유지하는 것이 중요합니다."
        ]
        message_to_me = "회복은 성과를 방해하는 시간이 아니라, 성과를 오래 지속하게 하는 힘입니다. 지금의 균형을 지켜가는 것이 가장 큰 경쟁력이 될 수 있습니다."
        
    elif sp_avg >= threshold and ra_avg >= threshold:
        # 🎯 Challenge Type (도전형)
        type_emoji = "🎯"
        type_id = "Challenge Type"
        type_title = "Challenge Type (도전형)"
        status_color = "#2196F3"
        
        state_desc = "높은 목표 의식과 회복 능력을 함께 갖춘 상태입니다. 다만 목표가 계속 높아질수록 자신에게 요구하는 기준도 함께 높아질 수 있습니다."
        proposals = [
            "🎯 **오늘 해야 할 일과 하면 좋은 일을 구분해 보세요.**  \n→ 모든 계획을 반드시 달성해야 한다는 부담을 줄이면 피로 누적을 예방할 수 있습니다.",
            "🎯 **하루를 마무리하며 결과보다 과정을 기록해 보세요.**  \n→ '몇 점을 받았는가'보다 '어떤 노력을 했는가'를 돌아보는 습관이 성과 압박을 줄이는 데 도움이 됩니다."
        ]
        message_to_me = "높은 목표를 향해 나아가는 힘은 큰 장점입니다. 하지만 오래 달리는 사람은 속도를 조절할 줄 아는 사람입니다."

    elif sp_avg >= threshold and ra_avg < threshold:
        # ⚡ Burnout Type (성과과부하 유형)
        type_emoji = "⚡"
        type_id = "Burnout Type"
        type_title = "Burnout Type (성과과부하 유형)"
        status_color = "#FF5722"
        
        state_desc = "성과를 향한 압박은 높지만 충분히 회복하지 못하고 있습니다. 지금의 피로는 노력이 부족해서가 아니라, 회복보다 성과를 우선하게 되는 생활 방식에서 비롯될 가능성이 있습니다."
        proposals = [
            "⚡ **해야 할 일 목록에서 '미뤄도 되는 일' 한 가지를 지워보세요.**  \n→ 모든 일을 같은 중요도로 다루지 않는 것만으로도 부담을 줄일 수 있습니다.",
            "⚡ **공부 시간을 늘리기보다 집중이 잘되는 시간을 찾아보세요.**  \n→ 시간의 양보다 집중의 질을 높이는 것이 더 효율적일 수 있습니다."
        ]
        message_to_me = "잠시 속도를 늦추는 것은 포기가 아닙니다. 더 오래 나아가기 위한 선택입니다."

    else: # sp_avg < threshold and ra_avg < threshold
        # 🌧 Fatigue Type (피로 누적 유형)
        type_emoji = "🌧"
        type_id = "Fatigue Type"
        type_title = "Fatigue Type (피로 누적 유형)"
        status_color = "#475569"
        
        state_desc = "성과 압박보다 회복 부족이 피로의 주요 원인으로 나타납니다. 에너지를 계속 사용하는 데 비해 충분히 충전하지 못하고 있는 상태입니다."
        proposals = [
            "🌧 **오늘 하루를 돌아보며 '하지 않아도 되었던 일'을 하나 찾아보세요.**  \n→ 피로를 줄이는 첫걸음은 해야 할 일을 늘리는 것이 아니라 불필요한 부담을 줄이는 것입니다.",
            "🌧 **잠들기 전 30분은 휴대폰 대신 몸과 마음을 쉬게 하는 시간을 가져보세요.**  \n→ 회복은 잠드는 순간보다 잠들기 전부터 시작됩니다."
        ]
        message_to_me = "지금 필요한 것은 더 많은 노력이 아니라, 다시 움직일 수 있는 에너지를 회복하는 시간입니다."

    # 3. 결과 대시보드 렌더링
    st.markdown("""
    <div style="text-align: center; margin-top: 10px; word-break: keep-all;">
        <h2 style="color: #0F172A; font-weight: 700; margin-bottom: 4px; font-size: 1.5rem;">📊 나의 진단 결과 리포트</h2>
    </div>
    """, unsafe_allow_html=True)

    # [유형, 점수 카드 구성]
    st.markdown(f"""
    <div class="result-card" style="border-top: 5px solid {status_color};">
        <div style="text-align: center; margin-bottom: 12px;">
            <p style="color: #64748B; font-size: 0.85rem; margin-bottom: 2px; font-weight: 500;">나의 최종 피로도 지수 (PFI)</p>
            <h1 style="font-size: 2.7rem; color: #0F172A; margin: 0; font-weight: 800;">{pfi_percentage} <span style="font-size: 1.1rem; font-weight: 500; color: #64748B;">점 / 100</span></h1>
            <h3 style="color: {status_color}; font-weight: 700; margin-top: 8px; font-size: 1.15rem;">{type_emoji} {type_title}</h3>
        </div>
        <hr style="border: 0; border-top: 1px solid #E2E8F0; margin: 12px 0;">
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div>
                <p style="margin: 0; color: #E64A19; font-size: 0.75rem; font-weight: 600;">📈 성과압박 평균 (SP)</p>
                <p style="margin: 3px 0 0 0; font-size: 1.1rem; font-weight: 700; color: #1E293B;">{sp_avg:.2f} <span style="font-size: 0.75rem; font-weight: 400; color: #94A3B8;">/ 5</span></p>
            </div>
            <div style="border-left: 1px solid #E2E8F0;"></div>
            <div>
                <p style="margin: 0; color: #388E3C; font-size: 0.75rem; font-weight: 600;">🧘 회복경험 평균 (RA)</p>
                <p style="margin: 3px 0 0 0; font-size: 1.1rem; font-weight: 700; color: #1E293B;">{ra_avg:.2f} <span style="font-size: 0.75rem; font-weight: 400; color: #94A3B8;">/ 5</span></p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. 피로 위험도 수준 카드 (결과 카드 바로 밑에 배치, 글씨 크기 축소)
    st.markdown(f"""
    <div style="background-color: #FAFAFA; border-left: 5px solid {risk_color}; border-radius: 10px; padding: 14px 16px; margin-top: 15px; word-break: keep-all;">
        <span style="color: {risk_color}; font-weight: 700; font-size: 0.8rem;">⚠️ 피로 위험도 수준</span>
        <h4 style="margin: 3px 0 3px 0; color: #1E293B; font-weight: 700; font-size: 1.05rem;">{risk_level}</h4>
        <p style="margin: 0; color: #475569; font-size: 0.85rem; line-height: 1.4;">{risk_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # 5. PFI 점수 vs 주관적 인지 피로도의 격차 분석 피드백
    # 주관적 피로 점수를 백분율 느낌으로 대치 (1->10%, 2->30%, 3->50%, 4->70%, 5->90%)
    subjective_mapped = [10, 30, 50, 70, 90][subjective_score - 1]
    gap = pfi_percentage - subjective_mapped
    
    sub_text = ["매우 낮음", "낮음", "보통", "높음", "매우 높음"][subjective_score - 1]
    
    st.markdown("### 💡 피로 인식 격차 분석 (PFI vs 주관적 체감)")
    
    # [주관적 피로 문항 내 모든 볼드체(**) 제거 및 차분한 네이비/인디고 그레이 적용]
    if gap >= 20:
        gap_desc = f"현재 검사상 측정된 객관적 피로 지수({pfi_percentage}점)에 비해 본인이 느끼는 주관적 피로({sub_text})가 상대적으로 매우 낮게 나타납니다. 이는 피로를 의식적으로 무시하며 계속 달리는 과적응(Over-adaptation) 상태이거나 한병철 철학에서 말하는 '자기착취형 성과주체'의 전형적인 모습일 수 있습니다. 몸과 마음이 보내는 미세한 피로 신호에 더 예민하게 주의를 기울여 보세요."
        gap_bg = "#FFF9E6"
        gap_border = "#FFB300"
    elif gap <= -20:
        gap_desc = f"현재 객관적 질문들을 조합한 피로 지수({pfi_percentage}점) 대비 본인은 주관적으로 훨씬 심한 피로({sub_text})를 호소하고 있습니다. 단순한 학업량이나 물리적 수면 부족 이외의 심리적 탈진, 동기 저하, 스트레스 조절의 한계가 체감 피로를 급격히 끌어올리고 있을 수 있습니다. 체력을 기르는 것도 좋지만 지금은 마음의 긴장을 이완하는 활동이 우선입니다."
        gap_bg = "#F1F5F9"
        gap_border = "#64748B"
    else:
        gap_desc = f"현재 지표상 피로 지수({pfi_percentage}점)와 스스로가 체감하는 피로 수준({sub_text})이 매우 일관되게 잘 맞닿아 있습니다. 자신의 에너지를 정확히 모니터링하고 조절하고 있는 훌륭한 상태입니다. 앞으로도 이 감각을 신뢰하며 일상을 스스로 조율해 가세요."
        gap_bg = "#E8F5E9"
        gap_border = "#4CAF50"

    st.markdown(f"""
    <div style="background-color: {gap_bg}; border-left: 5px solid {gap_border}; border-radius: 10px; padding: 14px 16px; word-break: keep-all;">
        <p style="margin: 0; color: #334155; font-size: 0.85rem; line-height: 1.5;">{gap_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 6. 피로도 유형 총괄 표 구현
    st.markdown("### 📋 피로도 유형 핵심 행동 한눈에 보기")
    
    summary_data = {
        "유형": ["🌿 Recovery Type", "🎯 Challenge Type", "⚡ Burnout Type", "🌧 Fatigue Type"],
        "구분": ["회복 충분 유형", "도전형", "성과과부하 유형", "피로 누적 유형"],
        "핵심 행동": ["현재 회복 습관 유지하기", "목표 관리 + 과부하 예방하기", "목표 줄이기 + 회복 시간 확보하기", "수면·생활 리듬 회복하기"]
    }
    
    df_summary = pd.DataFrame(summary_data)
    
    st.dataframe(
        df_summary, 
        use_container_width=True, 
        hide_index=True
    )
    
    st.markdown("---")
    
    # 7. 개인 유형별 상세 진단 리포트 출력 (글씨 크기 및 여백 소폭 감소)
    st.markdown(f"### 상세 분석: {type_emoji} {type_title}")
    
    # 상태 진단란
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border-radius: 8px; padding: 12px 14px; border-left: 4px solid {status_color}; margin-bottom: 15px; word-break: keep-all;">
        <strong>📌 지금의 상태</strong><br>
        <p style="margin: 4px 0 0 0; color: #334155; font-size: 0.85rem;">{state_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 실질적 해결책(Action Plans)
    st.markdown("#### 💡 오늘부터 실천해 보기")
    for prop in proposals:
        st.markdown(f"{prop}")
        st.markdown("<div style='margin-bottom: 6px;'></div>", unsafe_allow_html=True)
        
    # 나에게 보내는 메시지
    st.markdown(f"""
    <div style="background-color: #F1F5F9; border-radius: 8px; padding: 14px 16px; border: 1px solid #E2E8F0; margin-top: 15px; word-break: keep-all;">
        <strong style="color: #0F172A; font-size: 0.9rem;">💌 나에게 보내는 메시지</strong><br>
        <p style="margin: 6px 0 0 0; color: #1E293B; font-weight: 500; font-size: 0.85rem; line-height: 1.5; white-space: pre-wrap;">{message_to_me}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 8. 전체 공통 메시지 (결과 페이지 가장 하단 배치, 쌍따옴표 제거)
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 18px 20px; text-align: center; margin-top: 20px; margin-bottom: 20px; word-break: keep-all;">
        <h4 style="margin: 0 0 8px 0; color: #475569; font-weight: 700; font-size: 0.95rem;">💬 피로를 마주하는 우리의 자세</h4>
        <p style="color: #475569; font-size: 0.85rem; line-height: 1.6; margin: 0; font-weight: 500;">
            피로는 개인의 나약함을 의미하지 않습니다.<br>
            끊임없는 성과 요구 속에서 나타나는 <b>자연스러운 하나의 신호</b>일 수 있습니다.<br><br>
            이 진단의 목적은 나를 평가하거나 자책하기 위한 것이 아니라,<br>
            나에게 필요한 <b>진정한 회복 방향</b>을 찾기 위함입니다.<br><br>
            <b>나만의 건강한 균형을 찾아가는 것</b>이 지속 가능한 성장의 진짜 시작입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        reset_survey()
        st.rerun()

# --- [ 화면 공통: ✉️ 글로벌 푸터 문의 영역 ] ---
st.markdown("""
    <hr style="border: 0; border-top: 1px solid #E2E8F0; margin-top: 40px; margin-bottom: 16px;">
    <div style="text-align: center; color: #94A3B8; font-size: 0.8rem; padding-bottom: 20px;">
        ✉️ <b>문의:</b> <a href="mailto:241511@ggg.hs.kr" style="color: #64748B; text-decoration: underline; font-weight: 500;">241511@ggg.hs.kr</a>
    </div>
    """, unsafe_allow_html=True)

# 스트림릿 호스팅 배지를 강제로 지우는 스크립트 주입
st.components.v1.html(
    """
    <script>
        // iframe 외부 부모창의 도메인(streamlit.io) 링크를 찾아 화면에서 감춥니다.
        window.parent.document.querySelectorAll('a[href*="streamlit.io"]').forEach(el => {
            el.style.display = 'none';
        });
    </script>
    """,
    height=0
)
