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

if 'flow' not in app.config:
        app.config['flow'] = [
            SystemMessage(content="You are a financial adviser AI assistant")
        ]

def get_openai_response(question):
    app.config['flow'].append(HumanMessage(content=question))
    chat = ChatOpenAI(api_key=api_key, temperature=0.5)
    answer=chat(app.config['flow'])
    app.config['flow'].append(AIMessage(content=answer.content))

    return answer.content

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/chat', methods=['POST'])
def chat():
    question = request.form.get('input', '')
    response = get_openai_response(question)
    messages = []
    for msg in app.config['flow']:
         if isinstance(msg, HumanMessage):
              messages.append({'role': 'user', 'content': msg.content})
         elif isinstance(msg, AIMessage):
              messages.append({'role': 'assistant', 'content': msg.content})

    #return render_template('index.html', response=response, messages=messages)
    return jsonify({'response':response, 'messages':messages})


if __name__ == '__main__':
    app.run(debug=True)



