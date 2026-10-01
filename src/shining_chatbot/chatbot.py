import streamlit as st
import pandas as pd

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from langchain.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

@st.cache_resource
def get_model():
    return init_chat_model("openai:gpt-6-luna", reasoning_effort="none")

model = get_model()

st.set_page_config(
    page_title="챗봇",
    page_icon="😂",
    layout="wide"
)

# 모델 로드하기 -> 사용자마다 다를 필요 없음 -> 캐시에 저장
# cache_data : 데이터(표, 숫자, 리스트) -> 미리 가져올 때 사용
# cache_resource : 모델, DB연결, 에이전트 등과 같이 한번 만들어서 재사용하는 객체


# 대화 내용 누적돼야
if "messages" not in st.session_state:
    st.session_state['messages'] = [] # 초기화

# 기존 대화 있다면 -> 화면에 그리기
for message in st.session_state['messages']:
    with st.chat_message(message['role']):  # user랑 ai 있음
        st.markdown(message['content'])

question = st.chat_input("무엇이든 물어보세요")

# 채팅을 입력하면 -> 모델에 요청 들어가야 -> 답변을 받으면 출력
if question:    # 채팅을 입력하면
    with st.chat_message("user"):
        st.markdown(question)

    # 질문한 내역도 messages 에 저장
    st.session_state['messages'].append({'role' : 'user', 'content' : question})

    # 모델 통한 답변 출력
    with st.chat_message('assistant'):
        with st.spinner("답변하는 중..."):
            answer = model.invoke(st.session_state['messages']) # question 아니라, 대화내용 전체 들어가야 한다!
        st.markdown(answer.content)

    # 답변도 messages에 저장
    st.session_state['messages'].append({'role' : 'assistant', 'content' : answer.content})