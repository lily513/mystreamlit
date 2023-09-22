


"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
hello this is lily 
"""
import openai
import streamlit as st

st.title("ChatGPT-like clone")

if "pwd" not in st.session_state:
    with st.form("password"):
        password=st.text_input("password",type="password")
        if st.form_submit_button("submit"):
            if password==st.secrets["PASSWORD"]:
                st.session_state.pwd=password 
            else:
                st.error("password incorrect")
               
            

openai.api_key = st.secrets["OPENAI_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.question="what is the name of the 7th book?"
    st.session_state.answer= "Flashback"
 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(st.session_state.question):
    user_answer=prompt
    full_prompt=f"""
    the user was asked "{st.session_state.question}".
    the user answered "{user_answer}".
    the correct answer is "{st.session_state.answer}".
    respond by telling the user whether they are substantially correct. 
    if they are wrong, explain why. 
    """
    st.session_state.messages.append({"role": "user", "content": full_prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})


