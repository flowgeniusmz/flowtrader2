import streamlit as st
from config import pagesetup as ps
from openai import OpenAI
from tavily import TavilyClient

# 1. Set Page Header
title = "FlowTrader"
subtitle = "Trading Assistant"
divider = True
ps.set_header(title=title, subtitle=subtitle, divider=divider)

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



# # 2. Set Variables
# #### 2A. OpenAI Variables
# client = OpenAI(api_key=st.secrets.openai.api_key)
# assistant_id = st.secrets.openai.assistant_id
# vector_id = st.secrets.openai.vector_id
# model_normal = st.secrets.openai.model_4o_recent
# model_fast = st.secrets.openai.model_4o_mini
# model_advanced = st.secrets.openai.model_o1_preview
# model_advanced_fast = st.secrets.openai.model_o1_mini
# model_options = ["Normal", "Fast", "Advanced", "Advanced Fast"]

# #### 2B. Chat Variables
# initial_assistant_message = "Welcome to FlowTrader - how can I assist?"
# initial_assistant_json = {"role": "assistant", "content": initial_assistant_message}
# initial_assistant_messages = [initial_assistant_json]
# toast_waiting_message = "⏳ Thinking...please wait."
# toast_completed_message = "✅ Response completed!"

# # 3. Session State
# if "messages" not in st.session_state:
#     st.session_state.messages = initial_assistant_messages
#     st.session_state.prompt = None
#     st.session_state.response = None

# if "thread_id" not in st.session_state:
#     st.session_state.thread = client.beta.threads.create()
#     st.session_state.thread_id = st.session_state.thread.id

# if "run_id" not in st.session_state:
#     st.session_state.run = None
#     st.session_state.run_id = None


# # 4. Initial Display
# #### 4A. Set Containers
# chat_container = st.container(height=400, border=True)
# prompt_container = st.container(height=200, border=False)

# #### 4B. Populate Containers - Chat
# with chat_container:
#     for message in st.session_state.messages:
#         role = message['role']
#         content = message['content']
#         with st.chat_message(name=role):
#             st.markdown(body=content)

# #### 4C. Populate Containers - Prompt
# with prompt_container:
#     if prompt := st.chat_input(placeholder="Enter your question here..."):
#         #4C.1 - Set Session State
#         st.session_state.prompt = prompt
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
#         with chat_container:
#             with st.chat_message(name="user"):
#                 st.markdown(body=prompt)
            
            







