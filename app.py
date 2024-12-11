import streamlit as st
import time
import json

# JSON 파일에서 FAQ 데이터 로드
def load_faq(file_path="faq.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# FAQ 데이터 로드
faq = load_faq()

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

st.title("대구대 문헌정보학과 챗봇")

st.markdown("""
    대구대학교 문헌정보학과에서 운영하는 챗봇입니다.\n
    입학 및 학과에 관해 궁금한 점이 있다면 챗봇에게 질문해주시길 바랍니다.\n
    질문 시에는 정확한 키워드로 질문해주시길 바랍니다.\n
    챗봇이 답변하지 못하는 질문들은 학과사무실 또는 학과홈페이지 참고 부탁드립니다.\n
    대구대학교 문헌정보학과 학과 사무실 전화번호: **053-850-6350**\n
    대구대학교 문헌정보학과 학교홈페이지: https://lis.daegu.ac.kr/hakgwa_home/lis/index.php
""")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Accept user input
if prompt := st.chat_input("Ask me something!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt, unsafe_allow_html=True)

    # 기본 응답
    response = "죄송합니다. 보다 정확한 답변을 위해 상세한 키워드를 넣어주세요."

    # 단독 키워드 처리 (문헌정보학과, 문정과 등)
    if "문헌정보학과" in prompt and not any(keyword in prompt for keyword in [ "문정","독서", "책", "차별", "특징", "취업", "취직", "진로", "취업률","수학","과학","이과","외국어","입학","준비","적응","적성","장점","과목","수업"]):
        response = faq.get("문헌정보학과", response)

    elif "문정" in prompt and not any(keyword in prompt for keyword in [ "문헌정보학과","독서", "책", "차별", "특징", "취업", "취직", "진로", "취업률","수학","과학","이과","외국어","입학","준비","적응","적성","장점","과목","수업"]):
        response = faq.get("문정", response)


    # 정확한 키워드 매칭을 위한 우선 처리
    elif "취업률" in prompt:
        if "취업" not in prompt:  # "취업"이 포함되지 않으면 취업률 관련 답변만
            response = faq.get("취업률", response)
        else:  # "취업"과 "취업률" 둘 다 포함되면 취업률에 관한 답변
            response = faq.get("취업률", response)
    elif "취업" in prompt:
        if "취업률" not in prompt:  # "취업률"이 포함되지 않으면 취업 관련 답변만
            response = faq.get("취업", response)
    

    # 수학, 과학, 이과에 대한 처리
    elif "수학" in prompt and "과학" not in prompt and "이과" not in prompt:
        response = faq.get("수학", response)  # "수학"만 있을 때
    elif "과학" in prompt and "수학" not in prompt and "이과" not in prompt:
        response = faq.get("과학", response)  # "과학"만 있을 때
    elif "이과" in prompt and "수학" not in prompt and "과학" not in prompt:
        response = faq.get("이과", response)  # "이과"만 있을 때

    # 수학과 과학, 이과 키워드가 함께 있으면 우선순위로 처리
    elif "수학" in prompt and "과학" in prompt and "이과" not in prompt:
        response = faq.get("수학", response)  # 수학과 과학 중 우선순위가 높은 수학에 대한 답변
    elif "과학" in prompt and "수학" in prompt and "이과" not in prompt:
        response = faq.get("과학", response)  # 수학과 과학 중 우선순위가 높은 과학에 대한 답변
    elif "이과" in prompt and "수학" in prompt and "과학" not in prompt:
        response = faq.get("이과", response)  # 수학과 과학 중 우선순위가 높은 이과에 대한 답변
    
    # 과학과 이과 키워드가 함께 있을 때 과학에 대한 답변 우선 처리
    elif "과학" in prompt and "이과" in prompt:
        response = faq.get("과학", response)  # 과학이 포함되면 과학에 대한 답변 우선 처리

    elif "독서" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("독서", response)  # "독서"가 포함되면 독서에 대한 답변 출력
    
    elif "책" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("책", response)  # "책"가 포함되면 책에 대한 답변 출력

    elif "차별" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("차별", response)  # "차별"가 포함되면 차별에 대한 답변 출력

    elif "특징" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("특징", response)  # "특징"가 포함되면 특징에 대한 답변 출력

    elif "취직" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("취직", response)  # "진로"가 포함되면 진로에 대한 답변 출력

    elif "진로" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("진로", response)  # "진로"가 포함되면 진로에 대한 답변 출력

    elif "외국어" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("외국어", response)  # "외국어"가 포함되면 외국어에 대한 답변 출력
    
    elif "입학준비" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("입학준비", response)  # "입학 준비"가 포함되면 입학 준비에 대한 답변 출력

    elif "장점" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("장점", response)  # "장점"가 포함되면 입학 준비에 대한 답변 출력

    elif "수업" in prompt.lower():  # 소문자 처리로 정확한 매칭
        response = faq.get("수업", response)  # "수업"가 포함되면 입학 준비에 대한 답변 출력

    
    elif "입학" in prompt and "준비" in prompt and "과목" not in prompt:
        response = faq.get("입학", response)  
    elif "준비" in prompt and "입학" in prompt and "과목" not in prompt:
        response = faq.get("입학", response) 
    elif "과목" in prompt and "입학" in prompt and "준비" not in prompt:
        response = faq.get("과목", response)  

    elif "입학" in prompt and "준비" not in prompt and "과목" not in prompt:
        response = faq.get("입학", response)  
    elif "준비" in prompt and "입학" not in prompt and "과목" not in prompt:
        response = faq.get("준비", response)  
    elif "과목" in prompt and "준비" not in prompt and "입학" not in prompt:
        response = faq.get("과목", response)  

    
    # 과학과 이과 키워드가 함께 있을 때 과학에 대한 답변 우선 처리
    elif "과목" in prompt and "입학" in prompt:
        response = faq.get("과목", response)  # 과학이 포함되면 과학에 대한 답변 우선 처리


    elif "적응" in prompt:
        if "적성" not in prompt:  # "준비"이 포함되지 않으면 입학 관련 답변만
            response = faq.get("적응", response)
        else:  # "입학"과 "준비" 둘 다 포함되면 입학에 관한 답변
            response = faq.get("적성", response)
    elif "적성" in prompt:
        if "적응" not in prompt:  # "입학"이 포함되지 않으면 준비 관련 답변만
            response = faq.get("적성", response)


    

    # 줄바꿈을 <br>로 변환
    response_with_br = response.replace("\n", "<br>")

    # Display assistant response in chat message container with <br> for line breaks
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response_generator(response_with_br):
            full_response += chunk
            message_placeholder.markdown(full_response, unsafe_allow_html=True)  # HTML 허용

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
