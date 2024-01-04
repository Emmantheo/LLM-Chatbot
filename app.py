from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from flask import Flask, render_template, request, jsonify
import streamlit as st
from dotenv import load_dotenv
import os

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

def get_openai_response(question):
    st.session_state["flow"].append(HumanMessage(content=question))
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
    if isinstance(message, SystemMessage):
        st.text(f"System: {message.content}")
    elif isinstance(message, HumanMessage):
        st.text(f"You: {message.content}")
    elif isinstance(message, AIMessage):
        st.text(f"AI: {message.content}")