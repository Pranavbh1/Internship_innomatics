import streamlit as st
from dotenv import dotenv_values
import google.generativeai as genai 
import google.generativeai as gemini
config = dotenv_values(".env")


st.title("AI Tutor For DataScience 🤖📝💻")
f = open("Keys/.gemini_api_key.txt")

api_key = f.read()

gemini.configure(api_key=api_key)
# genai.configure(api_key = config["gemini"])
ai=genai.GenerativeModel(model_name="gemini-1.5-pro-latest",system_instruction="""You are helpful ai Teaching Assistant .Given a answer for the user query if you know otherwise tell i don't know if user and say Hi then say hi this is Pranav's chatbot how can i help you""")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"]=[]

chat = ai.start_chat(history=st.session_state['chat_history'])
for msg in chat.history:

    st.chat_message(msg.role).write(msg.parts[0].text)

user_prompt=st.chat_input()

if user_prompt:
    st.chat_message("user").write(user_prompt)
    response=chat.send_message(user_prompt)
    st.chat_message("ai").write(response.text)
    print(chat.history)
    st.session_state["chat_history"]=chat.history