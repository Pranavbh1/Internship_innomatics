from openai import OpenAI
import streamlit as st

f = open("keys/.openai_api_key.txt")
key = f.read()
client = OpenAI(api_key=key)
st.snow()
st.title(":rainbow[Pranav's Billion 💲 GenAI]")
st.header('MCQ GENERATOR APP', divider='rainbow')

# client.create_completion("Hello world")

prompt = st.text_input('Enter a data science topic')
if st.button("Generate"):
    st.balloons()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"Generate 5 data Science questions and answer for MCQ test in MCQ format."},
            {"role":"user","content":prompt}
    ]
    )

    if response.choices:
        st.write(response.choices[0].message.content)
