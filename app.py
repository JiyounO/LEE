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
        
        state_desc = "성과와 회복의 균형이 비교적 잘 유지되고 있습니다. 현재의 생활 방식이 피로를 예방하는 보호 요인으로 작용하고 있습니다."
        sample_text = "현재 당신은 학업과 회복 사이의 균형을 잘 유지하고 있습니다. 높은 성과를 위해 무리하기보다, 지금 가지고 있는 회복 습관을 지키는 것이 앞으로의 지속적인 성장에 도움이 됩니다."
        
        proposals = [
            "**회복 시간을 일정처럼 예약해 보세요.**  \n→ 시험 기간에도 휴식 시간을 '남으면 쉬는 시간'이 아니라 계획된 일정으로 남겨두세요.",
            "**회복 효과가 컸던 활동 하나를 계속 이어가세요.**  \n→ 산책, 운동, 음악 감상 등 나에게 잘 맞는 회복 방법은 바꾸기보다 꾸준히 유지하는 것이 중요합니다."
        ]
        message_to_me = "회복은 성과를 방해하는 시간이 아니라, 성과를 오래 지속하게 하는 힘입니다. 지금의 균형을 지켜가는 것이 가장 큰 경쟁력이 될 수 있습니다."
        
    elif sa_avg >= threshold and ra_avg >= threshold:
        # 🎯 Challenge Type (도전형)
        type_emoji = "🎯"
        type_id = "Challenge Type"
        type_title = "Challenge Type (도전형)"
        status_color = "#2196F3"
        
        state_desc = "높은 목표 의식과 회복 능력을 함께 갖춘 상태입니다. 다만 목표가 계속 높아질수록 자신에게 요구하는 기준도 함께 높아질 수 있습니다."
        sample_text = "당신은 높은 목표를 향해 나아가는 힘과 스스로 회복하는 능력을 함께 가지고 있습니다. 더 멀리 나아가기 위해서는 노력하는 시간만큼 멈추고 충전하는 시간도 중요합니다."
        
        proposals = [
            "**오늘 해야 할 일과 하면 좋은 일을 구분해 보세요.**  \n→ 모든 계획을 반드시 달성해야 한다는 부담을 줄이면 피로 누적을 예방할 수 있습니다.",
            "**하루를 마무리하며 결과보다 과정을 기록해 보세요.**  \n→ '몇 점을 받았는가'보다 '어떤 노력을 했는가'를 돌아보는 습관이 성과 압박을 줄이는 데 도움이 됩니다."
        ]
        message_to_me = "높은 목표를 향해 나아가는 힘은 큰 장점입니다. 하지만 오래 달리는 사람은 속도를 조절할 줄 아는 사람입니다."

    elif sa_avg >= threshold and ra_avg < threshold:
        # ⚡ Burnout Type (성과과부하 유형)
        type_emoji = "⚡"
        type_id = "Burnout Type"
        type_title = "Burnout Type (성과과부하 유형)"
        status_color = "#FF5722"
        
        state_desc = "성과를 향한 압박은 높지만 충분히 회복하지 못하고 있습니다. 지금의 피로는 노력이 부족해서가 아니라, 회복보다 성과를 우선하게 되는 생활 방식에서 비롯될 가능성이 있습니다."
        sample_text = "현재 당신에게 필요한 것은 더 많은 노력이 아니라, 잠시 속도를 조절하는 시간입니다. 성취를 향한 노력은 충분히 가치 있지만, 회복 없는 노력은 오래 지속되기 어렵습니다."
        
        proposals = [
            "**해야 할 일 목록에서 '미뤄도 되는 일' 한 가지를 지워보세요.**  \n→ 모든 일을 같은 중요도로 다루지 않는 것만으로도 부담을 줄있 수 있습니다.",
            "**공부 시간을 늘리기보다 집중이 잘되는 시간을 찾아보세요.**  \n→ 시간의 양보다 집중의 질을 높이는 것이 더 효율적일 수 있습니다."
        ]
        message_to_me = "잠시 속도를 늦추는 것은 포기가 아닙니다. 더 오래 나아가기 위한 선택입니다."

    else: # sa_avg < threshold and ra_avg < threshold
        # 🌧 Fatigue Type (피로 누적 유형)
        type_emoji = "🌧"
        type_id = "Fatigue Type"
        type_title = "Fatigue Type (피로 누적 유형)"
        status_color = "#9C27B0"
        
        state_desc = "성과 압박보다 회복 부족이 피로의 주요 원인으로 나타납니다. 에너지를 계속 사용하는 데 비해 충분히 충전하지 못하고 있는 상태입니다."
        sample_text = "지금의 피로는 부족한 의지의 문제가 아니라, 회복이 필요하다는 신호일 수 있습니다. 더 나아가기 위해서는 먼저 충분히 쉬고 에너지를 다시 채우는 과정이 필요합니다."
        
        proposals = [
            "**오늘 하루를 돌아보며 '하지 않아도 되었던 일'을 하나 찾아보세요.**  \n→ 피로를 줄이는 첫걸음은 해야 할 일을 늘리는 것이 아니라 불필요한 부담을 줄이는 것입니다.",
            "**잠들기 전 30분은 휴대폰 대신 몸과 마음을 쉬게 하는 시간을 가져보세요.**  \n→ 회복은 잠드는 순간보다 잠들기 전부터 시작됩니다."
        ]
        message_to_me = "지금 필요한 것은 더 많은 노력이 아니라, 다시 움직일 수 있는 에너지를 회복하는 시간입니다."

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
        <strong>📌 지금의 상태</strong><br>
        <p style="margin: 5px 0 0 0; color: #334155; font-size: 0.95rem;">{state_desc}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 실질적 해결책(Action Plans)
    st.markdown("#### 💡 오늘부터 실천해 보기")
    for prop in proposals:
        st.markdown(f"{prop}")
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
        
    # 나에게 보내는 메시지
    st.markdown(f"""
    <div style="background-color: #F1F5F9; border-radius: 8px; padding: 18px; border: 1px solid #E2E8F0; margin-top: 20px; word-break: keep-all;">
        <strong style="color: #0F172A; font-size: 1rem;">💌 나에게 보내는 메시지</strong><br>
        <p style="margin: 8px 0 0 0; color: #1E293B; font-weight: 500; font-size: 0.95rem; line-height: 1.6; white-space: pre-wrap;">{message_to_me}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 6. 전체 공통 메시지 (결과 페이지 가장 하단 배치, 쌍따옴표 제거)
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 22px; text-align: center; margin-top: 25px; margin-bottom: 25px; word-break: keep-all;">
        <h4 style="margin: 0 0 12px 0; color: #475569; font-weight: 700;">💬 피로를 마주하는 우리의 자세</h4>
        <p style="color: #475569; font-size: 0.95rem; line-height: 1.7; margin: 0; font-weight: 500;">
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
    <hr style="border: 0; border-top: 1px solid #E2E8F0; margin-top: 50px; margin-bottom: 20px;">
    <div style="text-align: center; color: #94A3B8; font-size: 0.85rem; padding-bottom: 30px;">
        ✉️ <b>문의:</b> <a href="mailto:241511@ggg.hs.kr" style="color: #64748B; text-decoration: underline; font-weight: 500;">241511@ggg.hs.kr</a>
    </div>
    """, unsafe_allow_html=True)
