import streamlit as st
import time

# [설정] 페이지 이름과 아이콘
st.set_page_config(page_title="복약 상식 퀴즈 앱", page_icon="💊")

# ---------------------------------------------------------
# (3) 캐싱 기능 구현: @st.cache_data 활용
# ---------------------------------------------------------
@st.cache_data
def get_quiz_data():
    time.sleep(1) 
    return [
        {"문제": "알약은 반드시 물과 함께 복용해야 하며, 콜라나 커피와 먹어도 상관없다.", "정답": "X", "해설": "커피나 콜라의 성분은 약의 흡수를 방해할 수 있으니 꼭 물과 드세요!"},
        {"문제": "증상이 나아졌다면 처방받은 항생제는 임의로 복용을 중단해도 된다.", "정답": "X", "해설": "항생제는 내성균 방지를 위해 증상이 호전되어도 끝까지 복용해야 합니다."},
        {"문제": "캡슐 형태의 약이 너무 크다면 쪼개거나 가루를 내어 먹는 것이 좋다.", "정답": "X", "해설": "캡슐은 특정 부위에서 녹도록 설계되었으므로 원형 그대로 복용해야 합니다."},
        {"문제": "유통기한이 지난 약은 효과가 조금 떨어질 뿐 먹어도 안전하다.", "정답": "X", "해설": "오래된 약은 화학 성분이 변해 부작용을 일으킬 수 있으니 반드시 폐기해야 합니다."}
    ]

# ---------------------------------------------------------
# (1) 첫 화면 조건: 학번과 이름 표시 (사이드바)
# ---------------------------------------------------------
st.sidebar.markdown("## 👤 제출자 정보")
st.sidebar.info("**학번:** 2025404066 \n\n**이름:** 부연후")

# ---------------------------------------------------------
# (2) 로그인 기능 구현
# ---------------------------------------------------------
if 'login_status' not in st.session_state:
    st.session_state.login_status = False

if not st.session_state.login_status:
    st.title("🔐 올바른 복약 상식 가이드")
    st.info("👤 제출자: 부연후 | 학번: 2025404066")  # ← 추가된 줄
    st.write("퀴즈를 풀기 위해 로그인을 진행해주세요.")
    
    with st.container(border=True):
        input_id = st.text_input("이름")
        input_pw = st.text_input("비밀번호", type="password")
        login_btn = st.button("로그인하기", use_container_width=True)
    
    if login_btn:
        if input_id == "부연후" and input_pw == "1234":
            st.session_state.login_status = True
            st.success("로그인 성공!")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("정보가 일치하지 않습니다.")

# ---------------------------------------------------------
# (4) 퀴즈 기능 구현 (로그인 성공 시 출력)
# ---------------------------------------------------------
else:
    st.title("💊 복약 상식 점검 퀴즈")
    st.write("평소 알고 있던 복약 습관이 올바른지 확인해보세요!")
    
    quiz_list = get_quiz_data()
    score = 0
    
    with st.form("quiz_form"):
        for i, q in enumerate(quiz_list):
            st.markdown(f"**Q{i+1}. {q['문제']}**")
            user_ans = st.radio(
                f"선택 {i}", 
                ["O", "X"], 
                key=f"quiz_v1_{i}",
                horizontal=True, 
                label_visibility="collapsed",
                index=None
            )
            if user_ans == q['정답']:
                score += 1
            st.write("---")
        
        submit = st.form_submit_button("나의 점수 확인하기", use_container_width=True)
        
    if submit:
        st.balloons()
        st.subheader(f"✅ 당신의 점수는 {score} / {len(quiz_list)}점 입니다!")
        with st.expander("자세한 해설 보기"):
            for q in quiz_list:
                st.write(f"**{q['문제']}**")
                st.write(f"정답: **{q['정답']}** | {q['해설']}")
                st.write("")

    if st.sidebar.button("로그아웃"):
        st.session_state.login_status = False
        st.rerun()