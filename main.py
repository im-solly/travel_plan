import numpy as np
from PIL import Image
import streamlit as st
import openai
import requests

# OpenAI API 키 설정
openai.api_key = 'api-key'

def get_openai_response(prompt):
    """
    OpenAI에게 프롬프트를 전달하고, 답변을 받아오는 함수.
    """
    response = openai.ChatCompletion.create(
 #       model="gpt-4-turbo-preview",
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,  # 필요에 따라 조정
        temperature=0.7,
    )
    return response.choices[0].message['content']

def main():
    st.title('여행 계획 세우기 귀찮지? 생성 AI에게 물어보자!')
    st.image("travel.jpg", use_column_width=True)
    # 사이드바에서 사용자 정보 입력받기
    question_gender = st.selectbox("성별을 입력해주세요", ("남자", "여자"))
    question_age = st.text_input("나이를 입력해 주세요")
    question_place = st.text_input("가고 싶은 여행지를 입력해 주세요")
#    question_date = st.text_input("원하는 여행 기간(날짜)을 입력해 주세요")
    question_start_date = st.date_input("여행 시작 날짜를 입력해 주세요")
    question_end_date = st.date_input("여행 종료 날짜를 입력해 주세요")

    if st.button("Send"):
        if question_place and question_gender and question_age and question_start_date and question_end_date:
            # 사용자 입력과 사이드바 정보를 프롬프트에 포함
            prompt = (f"성별: {question_gender}, 나이: {question_age}. "
                      f"여행지: {question_place}, 여행기간: {question_start_date} ~ {question_end_date}. "
                      f"이 정보를 바탕으로 여행 스케줄을 추천해줘.")
            with st.spinner('생성 AI로 답변을 생성하는 중입니다 ...'):
                response = get_openai_response(prompt)
            st.markdown(f'**Bot:**\n{response}')
        else:
            st.warning("모든 필드를 입력해 주세요!")

if __name__ == '__main__':
    main()
