from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.llms import OpenAI
from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os


app = Flask(__name__)

# Loading environment variables from .env file
load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

#initialising the chat


if 'flow' not in session:
    session['flow'] = [
        SystemMessage(content="You are a financial adviser AI assistant")
    ]


def get_openai_response(question):
    session['flow'].append(HumanMessage(content=question))
    chat = ChatOpenAI(api_key=api_key, temperature=0.5)
    answer=chat(session['flow'])
    session['flow'].append(AIMessage(content=answer.content))

    return answer.content


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    input_text = request.form['input_text']
    response = get_openai_response(input_text)

    return render_template('index.html', input_text=input_text, response=response)

if __name__ == '__main__':
    app.run(debug=True)



