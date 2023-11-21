


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
hello this is lily 
"""
from openai import OpenAI
import streamlit as st
import json

st.title("Book Quizzes")



if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    st.session_state["client"]=OpenAI(api_key=st.secrets["OPENAI_KEY"])
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.questions=[
                               " Who are the 5 collective members ?",
                               " What is Aldens catch phrase?",
                               " How many levels can you do in foxfire?",
                               " Who burned down Eternalia?"]
    st.session_state.answers= [
        "The five collective members are Blur,wraith,squall,Granite and Mr.Forkle.",
        "No reason to worry.",
        "8 levels",
        "Fintan"]
    st.session_state.number=0 
    st.session_state.yesnumber=0                         
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "pwd" in st.session_state:
    if prompt := st.chat_input(st.session_state.questions[st.session_state.number]):
        user_answer=prompt
        full_prompt=f"""
        the user was asked "{st.session_state.questions[st.session_state.number]}".
        the user answered "{user_answer}".
        the correct answer is "{st.session_state.answers[st.session_state.number]}".
        respond by telling the user whether they are substantially correct. 
        ignore capitalization or lack of capitalization.
        order of a list doesnt matter.
        if they are wrong, explain why.
        Your response should be a json string with the key "correct" having a value of either "Yes" or "No" and the key "reason" having a value of text explaining your reasoning in answering yes or no.
        """
        st.session_state.messages.append({"role": "user", "content": full_prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
    
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            #full_response = ""
            response =st.session_state['client'].chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )
                  
            data= json.loads(response.choices[0].message.content)
            message_placeholder.markdown(data["reason"])
            if data["correct"]== "Yes":
                st.session_state.yesnumber+=1
        st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.session_state.number+=1
        if st.session_state.number==len(st.session_state.questions):
           message=f'you completed the quiz. You got {st.session_state.yesnumber} crrect'
           st.session_state.messages.append({"role": "assistant", "content": message}) 
        st.chat_input(st.session_state.questions[st.session_state.number])
 
if "pwd" not in st.session_state:
    with st.form("password"):
        password=st.text_input("password",type="password")
        if st.form_submit_button("submit"):
            if password==st.secrets["PASSWORD"]:
                st.session_state.pwd=password 
            else:
                st.error("password incorrect")
               

