from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.llms import OpenAI
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Loading environment variables from .env file
load_dotenv()


