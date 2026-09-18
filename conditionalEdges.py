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
    operation : Literal['Add','Sub']
    result : int

def add(state:OperationsState)->OperationsState:
    return {
        'result' : [{'add' : state['a'] + state['b']}]
    }

def sub(state:OperationsState)->OperationsState:
    return {
            'result' : [{'sub' : state['a'] - state['b']}]
        }

def decision(state:OperationsState)->Literal['add','sub']:
    if state['operation'] == 'Add':
        return 'add'
    return 'sub'

state_graph = StateGraph(OperationsState)

state_graph.add_node('sum_node',add)
state_graph.add_node('sub_node',sub)

state_graph.add_conditional_edges(START,
    decision,
    {
            'add':'sum_node',
            'sub':'sub_node'
    }
)


state_graph.add_edge('sum_node',END)
state_graph.add_edge('sub_node',END)


graph = state_graph.compile()

def collect_input(val):
    return (f'What is the value of {val}')

if __name__ == '__main__':
    a = int(input(collect_input('a')))
    b = int(input(collect_input('b')))
    state01 = OperationsState(a=a,b=b,operation='Sub')
    result = graph.invoke(state01)
    print(result)   