from langchain.chat_models import init_chat_model, BaseChatModel
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage,AIMessage,SystemMessage,HumanMessage
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os

from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict, Annotated, Literal, Required, NotRequired


class OperationsState(TypedDict):
    a:int
    b:int
    add:int
    sub:int
    mul:int

def add(state:OperationsState)->OperationsState:
    state['add'] = state['a'] + state['b']
    return state

def sub(state:OperationsState)->OperationsState:
    state['sub'] = state['a'] - state['b']
    return state

def mul(state:OperationsState)->OperationsState:
    state['mul'] = state['a'] * state['b']
    return state

state_graph = StateGraph(OperationsState)

state_graph.add_node('add',add)
state_graph.add_node('sub',sub)
state_graph.add_node('mul',mul)

state_graph.add_edge(START,'add')
state_graph.add_edge('add','sub')
state_graph.add_edge('sub','mul')
state_graph.add_edge('mul',END)

graph = state_graph.compile()

if __name__ == '__main__':
    result = graph.invoke(OperationsState(a=20,b=3))
    print(result)