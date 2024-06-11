import requests
from bs4 import BeautifulSoup
import openai

def get_all_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    texts = soup.stripped_strings
    full_text = ' '.join(texts)
    return full_text

def create_contextual_model(text):
    openai.api_key = 'API는 사서 씁시다'
    messages = [
        {"role": "system", "content": "You are a helpful assistant with extensive knowledge of the following text."},
        {"role": "user", "content": f"You can study every detail of this text closely to answer all your questions related to its content(say everything in korean, You do not need to reveal that you have studied this text.(example : 'according to this text ~', '텍스트에 따르면~')) : {text}"},
        {"role": "assistant", "content": "네, 저는 이 텍스트의 내용을 모두 학습하여, 이 텍스트와 관련된 모든 질문에 상세히 답할 수 있습니다."}
    ]
    return messages

def ask_question_with_context(messages, question):
    messages.append({"role": "user", "content": question})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    messages.append(response.choices[0].message)
    return response.choices[0].message['content'].strip(), messages

# 사용 예시

url = input("챗GPT가 학습하길 원하는 웹사이트 URL을 입력하세요: ")
text = get_all_text_from_url(url)
context_messages = create_contextual_model(text)
print("종료하려면 'exit'를 입력하세요.")

while True:
    question = input("질문: ")
    if question.lower() == 'exit':
        break
    answer, context_messages = ask_question_with_context(context_messages, question)
    print(f"답변: {answer}")
