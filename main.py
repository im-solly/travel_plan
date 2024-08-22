import numpy as np
from PIL import Image
import streamlit as st
import openai
import requests
import os

# OpenAI API 키 설정
API_KEY = os.environ['API_KEY']
openai.api_key = API_KEY

col1, col2 = st.columns(2)

def get_openai_response(prompt):
    """
    OpenAI에게 프롬프트를 전달하고, 답변을 받아오는 함수.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo-preview",
#        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,  # 필요에 따라 조정
        temperature=0.7,
    )
    return response.choices[0].message['content']

def main():
    with col1:
        st.title('여행 계획 세우기 귀찮지? 내가 알려줄게!')
        st.image("travel.jpg", use_column_width=True)

        # 사이드바에서 사용자 정보 입력받기
        question_gender = st.selectbox("성별을 입력해주세요", ("남자", "여자"))
        question_age = st.text_input("나이를 입력해 주세요")
        question_place = st.text_input("가고 싶은 여행지를 입력해 주세요")
        question_must = st.text_input("꼭 가보고 싶었던 장소가 있나요?")
        question_transportation = st.selectbox("어떤 교통수단을 이용하나요?", ("렌트카", "대중교통"))
        question_start_date = st.date_input("여행 시작 날짜를 입력해 주세요")
        question_end_date = st.date_input("여행 종료 날짜를 입력해 주세요")
        
    with col2: 
        if st.button("Send"):
            if question_place and question_gender and question_age and question_start_date and question_end_date:
                # 사용자 입력과 사이드바 정보를 프롬프트에 포함
                prompt = (f"너는 고객의 정보를 받아 여행 경로를 추천해주는 전문가야. 성별: {question_gender}, 나이: {question_age}. "
                        f"여행지: {question_place}, 여행기간: {question_start_date} ~ {question_end_date}. "
                        f"이 정보를 바탕으로 여행 스케줄을 추천해줘. {question_must}는 꼭 방문하고 싶고, 스케줄을 추천해줄 때 이동 시에는 {question_transportation}을 이용할 거야."
                        f"사용되어야 하는 교통수단, 교통비, 입장료 등을 계산해서 같이 알려줘. 추천하는 관광지의 사진도 같이 보내줬으면 좋겠어. ")
                with st.spinner('생성 AI로 답변을 생성하는 중입니다 ...'):
                    response = get_openai_response(prompt)
                st.markdown(f'**Bot:**\n{response}')
            else:
                st.warning("모든 필드를 입력해 주세요!")

if __name__ == '__main__':
    main()
