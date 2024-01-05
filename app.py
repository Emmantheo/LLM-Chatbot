from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from flask import Flask, render_template, request, jsonify
import streamlit as st
from dotenv import load_dotenv
import os
from fin_advisory_data import financial_advisory_data

# Streamlit UI
st.set_page_config(page_title="Conversational Chatbot")
st.header("Hey, Let's Chat")

# Loading environment variables from .env file
load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

# Initialize the chat
chat = ChatOpenAI(api_key=api_key, temperature=0.5)

if 'flow' not in st.session_state:
    st.session_state['flow'] = [
        SystemMessage(content="You are a financial adviser AI assistant")
    ]

#@st.cache_resource
def get_openai_response(question):
    st.session_state["flow"].append(HumanMessage(content=question))
    # Check if the user query is related to financial advisory
    # if "investment options" in question.lower():
    #     answer = financial_advisory_data["faq"]["investment_planning"]
    # elif "risk tolerance" in question.lower():
    #     answer = financial_advisory_data["faq"]["risk_management"]
    # elif "retirement plans" in question.lower():
    #     answer = financial_advisory_data["faq"]["retirement_planning"]

    # else:
    answer = chat(st.session_state['flow'])
    st.session_state["flow"].append(AIMessage(content=answer.content))
    return answer.content

# User input
input = st.text_input("Input: ", key="input")

submit = st.button("Ask me")

if submit:
    # Get response
    response = get_openai_response(input)

    # Display response
    #st.text(f"AI: {response}")

# Display previous messages
for message in st.session_state['flow']:
    # if isinstance(message, SystemMessage):
    #     st.text(f"System: {message.content}")
    if isinstance(message, HumanMessage):
        st.text(f"You: {message.content}")
    elif isinstance(message, AIMessage):
        st.text(f"AI: {message.content}")

# Add a sidebar for the "Clear chat" button
with st.sidebar:
    if st.button(":red[Delete Chat]"):
        st.session_state.clear()
        #st.success("Chat history cleared!", icon="🚨")
        st.stop()

# CSS to style the chat layout
# st.markdown(
#     """
#     <style>
#         .chat-container {
#             display: flex;
#             flex-direction: row;
#             justify-content: space-between;
#             align-items: flex-start;
#         }

#         .user-chat {
#             background-color: #aa00aa;  /* Light red for user chat */
#             padding: 8px;
#             border-radius: 8px;
#             margin-bottom: 8px;
#             max-width: 70%;
#             align-self: flex-end;
#         }

#         .ai-chat {
#             background-color: #007acc;  /* Lighter blue for AI chat */
#             padding: 8px;
#             border-radius: 8px;
#             margin-bottom: 8px;
#             max-width: 70%;
#             align-self: flex-start;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # Display messages with the new layout
# st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# for message in st.session_state['flow']:
#     if isinstance(message, HumanMessage):
#         st.markdown(f'<div class="user-chat">{message.content}</div>', unsafe_allow_html=True)
#     elif isinstance(message, AIMessage):
#         st.markdown(f'<div class="ai-chat">{message.content}</div>', unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)