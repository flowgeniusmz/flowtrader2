import streamlit as st
from openai import OpenAI
from typing import Literal

# 1. Create Client
client = OpenAI(api_key=st.secrets.openai.api_key)

# 2. Set Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome to FlowTrader - how can I assist?"}]

if "thread_id" not in st.session_state:
    st.session_state.thread_id = client.beta.threads.create().id
    st.session_state.assistant_id = st.secrets.openai.assistant_id
    st.session_state.vector_id = st.secrets.openai.vector_id
    st.session_state.run_id = None




chat_container = st.container(height=400, border=True)
with chat_container:
    # 1. Display the messages
    for message in st.session_state.messages:
        with st.chat_message(name=message['role']):
            st.markdown(body=message['content'])

prompt_container = st.container(height=200, border=False)
with prompt_container:
    if prompt := st.chat_input(placeholder="Enter question here..."):
    # 1. Append Message
        st.session_state.messages.append({"role": "user", "content": prompt})
    # 2. Display Message
        with chat_container:
            with st.chat_message(name="user"):
                st.markdown(body=prompt)
    # 3. Assistant Step 1 - Create Thread Message
    user_thread_message = client.beta.threads.messages.create(thread_id=st.session_state.thread_id, content=prompt, role="user")
    user_thread_message_id = user_thread_message.id
    # 4. Assistant Step 2 - Create a Run
    run = client.beta.threads.runs.create_and_poll(assistant_id=st.session_state.assistant_id, thread_id=st.session_state.thread_id)
    # 5. Assistant Step 3 - List Messages When Completed
    if run.status == "completed":
        thread_messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id, run_id=run.id)
    # 6. Assistant Step 4 - Get the Assistant Message
        for thread_message in thread_messages:
            if thread_message.role == "assistant":
                response = thread_message.content[0].text.value
    # 7. Append Message
                st.session_state.messages.append({"role": "assistant", "content": response})
    # 8. Display Message
                with chat_container:
                    with st.chat_message(name="assistant"):
                        st.markdown(body=response)




    




