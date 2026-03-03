from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openai import ChatOpenAI , OpenAIEmbeddings
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun, tool
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
import os
import requests
import smtplib
from email.message import EmailMessage
import sqlite3
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

load_dotenv()

#---------------------------------------------------------------------------------------------------------------------------------------

#Initialize all the Api Keys 

openai_api_key = os.getenv("Open_AI_API")
weather_api_key = os.getenv("waether_api_key")
stock_api_key = os.getenv("stock_price_api_key")

#---------------------------------------------------------------------------------------------------------------------------------------

llm = ChatOpenAI(model = "gpt-4.1-mini", api_key=openai_api_key)
parser = StrOutputParser()

#---------------------------------------------------------------------------------------------------------------------------------------
# Configure all the tools which are to be binded with the llm 

@tool
def get_stock_price(symbol:str):
    """This tool gets the latest price of the stock """

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={stock_api_key}"
    result = requests.get(url)

    return {'Symbol':symbol , "result": result.json()}

@tool
def calculator(num1:float, num2:float, operation:str):
    """This tool performs the operation between the two numbers eg: [add,sub,mul,div]"""
    if operation == 'add':
        result = num1 + num2
    elif operation == 'mul':
        result = num1 * num2 
    else:
        result = num1 - num2 
    
    return {"first_number":num1,"second_number":num2,"operation":operation,"result":result}

@tool
def get_weather_status(city:str):
    """This tool gets the temperature and condition of the city"""

    url = f"https://api.weatherstack.com/current?access_key={weather_api_key}&query={city}"
    response = requests.get(url)
    data = response.json()
    return {"weather_json":data}

@tool 
def estimate_trip_cost(days:int, budget : int, city:str):
    """This tool gives the estimated cost of the Trip """
    
    prompt = PromptTemplate(
    template="""
    Give an conclusion based on the {days} days and the budget : {budget}, how much will be the estimated cost for the trip is the amount {budget} sufficient or will they require more" \
    1. I wont spend more than 1000 Rs per night 
    2. I want to see the Night Life of {city}
    3. Cover all the Historical Places 
    """
    ,
    input_variables=["budget","days","city"]
    )

    chain = prompt | llm | parser
    response = chain.invoke({"days":days, "budget":budget, "city":city})
    return {"Estimated_cost":response}

@tool 
def send_mail(title:str, body:str, email_id:str):
    """Use this tool when the user explicitly wants to send an email.
    You must extract:
    - recipient email address
    - subject
    - body
    Do not call this tool for summaries or drafting only."""

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = email_id
    msg["Subject"] = title
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    
    return {f'result':"Mail Sent succesully to mail id {email_id}", "status":"success "}

search_tool = DuckDuckGoSearchRun()

tools = [search_tool,estimate_trip_cost,get_stock_price,get_weather_status,calculator,send_mail]

llm_with_tools = llm.bind_tools(tools)
#---------------------------------------------------------------------------------------------------------------------------------------

# Create the chatbot State
class ChatBOTState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#---------------------------------------------------------------------------------------------------------------------------------------

def chat_node(state: ChatBOTState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

#---------------------------------------------------------------------------------------------------------------------------------------

con = sqlite3.connect(database="demo.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=con)

config = {'configurable':{"thread_id":"thread_1"}}

#---------------------------------------------------------------------------------------------------------------------------------------

builder = StateGraph(ChatBOTState)
builder.add_node("chat_node", chat_node)
builder.add_node('tools',tool_node)

builder.add_edge(START, "chat_node")
builder.add_conditional_edges("chat_node",tools_condition)
builder.add_edge("tools","chat_node")

chatbot = builder.compile(checkpointer=checkpointer)

#---------------------------------------------------------------------------------------------------------------------------------------

def retrieve_all_threads():
    result = set()
    for checkpoints in checkpointer.list(None):
        result.add(checkpoints.config['configurable']['thread_id'])
    
    return list(result)

# while True:
#     user_input = input("User : ")
#     if user_input == "Exit":
#         print("You have Exited the ChatBot")
#         break
#     else:
#         response = chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)
#         print(f"Chatbot : {response['messages'][-1].content} \n")

