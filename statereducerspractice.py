# from langchain.chat_models import init_chat_model, BaseChatModel
# from langchain.agents import create_agent
# from langchain_core.messages import BaseMessage,AIMessage,SystemMessage,HumanMessage
# from langchain.tools import tool
# from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
import operator

from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict, Annotated, Literal, Required, NotRequired


class OperationsState(TypedDict,total = False):
    a:Required[int]
    b:Required[int]
    result : Annotated[list[int],operator.add]

def add(state:OperationsState)->OperationsState:
    # state['add'] = state['a'] + state['b']
    return {
        'result' : [{'add' : state['a'] + state['b']}]
    }

def sub(state:OperationsState)->OperationsState:
    # state['sub'] = state['a'] - state['b']
    return {
            'result' : [{'sub' : state['a'] - state['b']}]
        }

def mul(state:OperationsState)->OperationsState:
    # state['mul'] = state['a'] * state['b']
    return {
        'result' : [{'mul' : state['a'] * state['b']}]
    }

state_graph = StateGraph(OperationsState)

state_graph.add_node('add',add)
state_graph.add_node('sub',sub)
state_graph.add_node('mul',mul)

state_graph.add_edge(START,'add')
state_graph.add_edge(START,'sub')
state_graph.add_edge(START,'mul')
state_graph.add_edge('add',END)
state_graph.add_edge('sub',END)
state_graph.add_edge('mul',END)

graph = state_graph.compile()

def collect_input(val):
    return (f'What is the value of {val}')

if __name__ == '__main__':
    a = int(input(collect_input('a')))
    b = int(input(collect_input('b')))
    state01 = OperationsState(a=a,b=b)
    result = graph.invoke(state01)
    print(result)