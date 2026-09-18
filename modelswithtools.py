from langchain.chat_models import init_chat_model, BaseChatModel
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage,AIMessage,SystemMessage,HumanMessage
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
import os
import operator
from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.graph import StateGraph, MessagesState, START, END
from typing import TypedDict, Annotated, Literal, Required, NotRequired


from langchain_core.tools import tool


@tool
def get_currency(country: str) -> str:
    """
    Get the currency used in a given country.

    Use this tool when you need to find out the currency
    associated with a specific country.

    Args:
        country: The name of the country whose currency is required.

    Returns:
        A string containing the currency of the specified country.
    """
    return f'The currency of the {country} is Euros'


@tool
def get_weather(city: str) -> str:
    """
    Get the current weather information for a given city.

    Use this tool when you need to find the weather conditions
    of a specific city.

    Args:
        city: The name of the city for which weather information is required.

    Returns:
        A string describing the weather conditions in the specified city.
    """
    return f'The weather in {city} is sunny'


@tool
def get_capital(country: str) -> str:
    """
    Get the capital city of a given country.

    Use this tool when you need to find the capital of
    a specific country.

    Args:
        country: The name of the country whose capital is required.

    Returns:
        A string containing the capital city of the specified country.
    """
    return f'The capital of {country} is Paris'


all_tools = [get_capital,get_currency,get_weather]

model_name = 'google_genai:gemini-3.1-flash-lite'
llm = init_chat_model(
    model=model_name
)

tool_node = ToolNode(tools=all_tools)

llm_with_tools = llm.bind_tools(tools=all_tools)

def chat(state:MessagesState)->MessagesState:
    state['messages'] = llm_with_tools.invoke(state['messages'])
    return state

state_graph = StateGraph(MessagesState)

state_graph.add_node('tools',tool_node)
state_graph.add_node('chat_node',chat)

state_graph.add_edge(START,'chat_node')
state_graph.add_conditional_edges(
    'chat_node',
    tools_condition
)
state_graph.add_edge('tools','chat_node')
state_graph.add_edge('chat_node',END)

graph = state_graph.compile()

if __name__ == '__main__':
    response = graph.invoke({
        'messages':[
        SystemMessage('You are a brainless model who returns whatever your tools returns without thinking anything'),
        HumanMessage('What is the capital of India ?')
    ]
    })

    for message in response['messages']:
        print(message)
