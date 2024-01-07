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

# Loading environment variables from .env file
load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

#initialising the chat
chat = ChatOpenAI(api_key=api_key, temperature=0.5)

#initializing the flow
flow= [SystemMessage(content="You are are a financial adviser AI assistant")]

def get_openai_response(question):
    flow.append(HumanMessage(content=question))
    answer=chat(flow)
    flow.append(AIMessage(content=answer.content))

    return answer.content


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    input = request.form['input_text']
    response = get_openai_response(input)

    return render_template('index.html', input_text=input, response=response, flow=flow)

if __name__ == '__main__':
    app.run(debug=True)



