from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.llms import OpenAI
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import logging



# Loading environment variables from .env file
load_dotenv()

# Accessing environment variables
host_no = os.getenv("host")
port_no = os.getenv("port")
debug_mode = os.getenv("DEBUG")

logging.basicConfig(filename='app.log', level=logging.DEBUG)
app = Flask(__name__)

# Loading environment variables from .env file
load_dotenv()
api_key = os.getenv("OPEN_AI_KEY")

#initialising the chat

if 'flow' not in app.config:
        app.config['flow'] = [
            SystemMessage(
                content="You are a financial adviser AI assistant and also a Transaction assistant who help customers carry out bank transfers straight from the chat platform.You should also be able to help buy airtime, data and electricity units for customers"          
                          )
        ]

# def get_openai_response(question):
#     app.config['flow'].append(HumanMessage(content=question))
#     chat = ChatOpenAI(api_key=api_key, temperature=0.5)
#     answer=chat(app.config['flow'])
#     app.config['flow'].append(AIMessage(content=answer.content))

#     return answer.content

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/chat', methods=['POST'])
def chat():
    input=None
    if request.headers['Content-Type']=='application/json':
        question = request.get_json()['input']
    else:
        question = request.form.get('input', '')
    
    app.config['flow'].append(HumanMessage(content=question))
    chat = ChatOpenAI(api_key=api_key, temperature=0.5)
    answer = chat(app.config['flow'])
    app.config['flow'].append(AIMessage(content=answer.content))

    response = answer.content

    # Log the question and response
    logging.info(f"User question: {question}")
    logging.info(f"AI response: {response}")

    #get response
    #response = get_openai_response(question)
    messages = []
    for msg in app.config['flow']:
        if isinstance(msg, HumanMessage):
            messages.append({'role': 'user', 'content': msg.content})
        elif isinstance(msg, AIMessage):
            messages.append({'role': 'ai', 'content': msg.content})

    #return render_template('index.html', response=response, messages=messages)
    return jsonify({'response':response, 'messages':messages})



if __name__ == '__main__':
    app.run(debug=debug_mode, host=host_no, port=port_no)



