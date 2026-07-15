import streamlit as st
import pandas as pd

# 1. 웹페이지 기본 설정 및 미려한 CSS 스타일
st.set_page_config(page_title="청소년 피로도 지수(PFI) 진단", page_icon="🧘", layout="centered")

# [글자 끊김 방지 및 UI 가독성을 극대화한 CSS]
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
        word-break: keep-all; /* 단어 단위 줄바꿈으로 가독성 향상 */
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
        # 🌿 Recovery Type (회복 충분 유형)
        type_emoji = "🌿"
        type_id = "Recovery Type"
        type_title = "Recovery Type (회복 충분 유형)"
        status_color = "#4CAF50"
        
        state_desc = "현재 피로 관리 능력이 좋은 상태. 다만 학업량 증가 시 균형이 깨질 수 있음."
        sample_text = "현재 당신은 학업과 회복 사이의 균형을 잘 유지하고 있습니다. 높은 성과를 위해 무리하기보다, 지금 가지고 있는 회복 습관을 지키는 것이 앞으로의 지속적인 성장에 도움이 됩니다."
        
        proposals = [
            "**시험 2주 전부터 수면 시간 확보 계획 세우기**  \n→ 시험 직전에 수면을 몰아서 급격히 줄이는 패턴을 미리 방지합니다.",
            "**주 1회 '학업 없는 시간' 확보하기**  \n→ 단순히 공부 효율을 높이기 위함이 아니라, 장기적인 뇌의 회복 능력을 유지하는 목적입니다.",
            "**현재 효과가 있는 회복 활동 기록해두기**  \n→ 가벼운 산책, 운동, 취미 등 나에게 가장 잘 맞는 회복 루틴을 지속해 나갑니다."
        ]
        
    elif sa_avg >= threshold and ra_avg >= threshold:
        # 🎯 Challenge Type (도전형)
        type_emoji = "🎯"
        type_id = "Challenge Type"
        type_title = "Challenge Type (도전형)"
        status_color = "#2196F3"
        
        state_desc = "목표 의식과 회복 능력이 모두 높은 상태. 다만 과도한 목표 설정 시 위험 가능."
        sample_text = "당신은 높은 목표를 향해 나아가는 힘과 스스로 회복하는 능력을 함께 가지고 있습니다. 더 멀리 나아가기 위해서는 노력하는 시간만큼 멈추고 충전하는 시간도 중요합니다."
        
        proposals = [
            "**플래너 작성 시 '최소 목표'와 '최대 목표' 구분하기**  \n- *최소 목표*: 어떤 상황에서도 반드시 달성할 핵심 계획  \n- *최대 목표*: 여유가 있을 때 추가로 도전해볼 계획",
            "**시험 기간에도 하루 30분 회복 시간 고정하기**  \n→ 공부를 다 마치고 쉬는 게 아니라, 휴식 시간 자체를 학습 계획표의 정식 일정으로 포함합니다.",
            "**성과 기준을 '결과'만으로 평가하지 않기**  \n- ❌ *모의고사 등급*에만 집착하기보다  \n- ⭕ *오답 정리 완료, 오늘 계획 실천율* 같은 과정형 목표 위주로 성취감을 얻습니다."
        ]

    elif sa_avg >= threshold and ra_avg < threshold:
        # ⚡ Burnout Type (성과과부하 유형)
        type_emoji = "⚡"
        type_id = "Burnout Type"
        type_title = "Burnout Type (성과과부하 유형)"
        status_color = "#FF5722"
        
        state_desc = "성과 압박은 높고 회복은 부족한 가장 위험한 고위험군 유형."
        sample_text = "현재 당신에게 필요한 것은 더 많은 노력이 아니라, 잠시 속도를 조절하는 시간입니다. 성취를 향한 노력은 충분히 가치 있지만, 회복 없는 노력은 오래 지속되기 어렵습니다."
        
        proposals = [
            "**현재 진행 중인 목표를 '필수'와 '선택'으로 분류하기**  \n- *예시*: 반드시 해야 하는 수행평가(필수) / 하면 좋은 추가 문제풀이(선택)  \n→ 모든 공부 목록을 동일한 우선순위에 두며 자신을 압박하지 않습니다.",
            "**무작정 공부 시간을 늘리는 대신 '집중 세션' 관리하기**  \n- *기존*: 밤 12시까지 무조건 책상에 버티기  \n- *변경*: 90분 집중 학습 + 10분 온전한 휴식 루틴 반복",
            "**주 1회 학업 목표를 정기적으로 점검하고 덜어내기**  \n- '이번 주 세웠던 목표가 현실적이었는가?'  \n- '스스로를 망가뜨리지 않기 위해 줄여도 되는 일정은 없는가?'"
        ]

    else: # sa_avg < threshold and ra_avg < threshold
        # 🌧 Fatigue Type (피로 누적 유형)
        type_emoji = "🌧"
        type_id = "Fatigue Type"
        type_title = "Fatigue Type (피로 누적 유형)"
        status_color = "#9C27B0"
        
        state_desc = "성과 압박 자체보다 절대적인 회복 능력과 환경 부족이 주요 원인."
        sample_text = "지금의 피로는 부족한 의지의 문제가 아니라, 회복이 필요하다는 신호일 수 있습니다. 더 나아가기 위해서는 먼저 충분히 쉬고 에너지를 다시 채우는 과정이 필요합니다."
        
        proposals = [
            "**취침 및 기상 시간부터 먼저 확실하게 고정하기**  \n→ 평일 취침 시간 변동을 30분 내외로 통제하고, 주말에도 기상 시간이 크게 늦어지지 않게 관리합니다.",
            "**하루에 10~20분이라도 무자극 회복 활동 배치하기**  \n→ 조용히 산책하기, 가벼운 스트레칭, 음악 감상, 또는 친구와의 수다 시간을 가집니다.",
            "**해야 할 일의 가짓수를 적극적으로 줄이는 '정리 시간' 가지기**  \n- 매일 밤: '내일 꼭 해야 할 핵심 공부 3개'만 정하고 불필요한 과부하 일정은 삭제합니다."
        ]

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
    
    # 5. 개인 유형별 상세 진단 리포트 출력
    st.markdown(f"### 상세 분석: {type_emoji} {type_title}")
    
    # 상태 진단란
    st.markdown(f"""
    <div style="background-color: #F8FAFC; border-radius: 8px; padding: 15px; border-left: 4px solid {status_color}; margin-bottom: 20px; word-break: keep-all;">
        <strong>📌 나의 상태 진단</strong><br>
        <p style="margin: 5px 0 0 0; color: #334155; font-size: 0.95rem;">{state_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 실질적 해결책(Action Plans)
    st.markdown("#### 💡 학생을 위한 실질적 해결책")
    for prop in proposals:
        st.markdown(f"- {prop}")
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        
    # 결과 문구 예시
    st.markdown(f"""
    <div style="background-color: #F1F5F9; border-radius: 8px; padding: 18px; border: 1px solid #E2E8F0; margin-top: 20px; word-break: keep-all;">
        <strong style="color: #0F172A; font-size: 1rem;">📢 분석 총평</strong><br>
        <p style="margin: 8px 0 0 0; color: #1E293B; font-weight: 500; font-size: 0.95rem; line-height: 1.6; white-space: pre-wrap;">"{sample_text}"</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 6. 전체 공통 메시지 (결과 페이지 가장 하단 배치)
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 22px; text-align: center; margin-top: 25px; margin-bottom: 25px; word-break: keep-all;">
        <h4 style="margin: 0 0 12px 0; color: #475569; font-weight: 700;">💬 피로를 마주하는 우리의 자세</h4>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.7; margin: 0; font-weight: 500;">
            "피로는 개인의 나약함을 의미하지 않습니다.<br>
            끊임없는 성과 요구 속에서 나타나는 <b>자연스러운 하나의 신호</b>일 수 있습니다.<br><br>
            이 진단의 목적은 나를 평가하거나 자책하기 위한 것이 아니라,<br>
            나에게 필요한 <b>진정한 회복 방향</b>을 찾기 위함입니다.<br><br>
            <b>나만의 건강한 균형을 찾아가는 것</b>이 지속 가능한 성장의 진짜 시작입니다."
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 처음으로 돌아가기", use_container_width=True):
        reset_survey()
        st.rerun()

# --- [ 화면 공통: ✉️ 글로벌 푸터 문의 영역 ] ---
st.markdown("""
    <hr style="border: 0; border-top: 1px solid #E2E8F0; margin-top: 50px; margin-bottom: 20px;">
    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem; padding-bottom: 30px;">
        ✉️ <b>문의:</b> <a href="mailto:241511@ggg.hs.kr" style="color: #64748B; text-decoration: underline; font-weight: 500;">241511@ggg.hs.kr</a>
    </div>
    """, unsafe_allow_html=True)
