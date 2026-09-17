from langgraph.graph import StateGraph,MessagesState,START,END,add_messages
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, BaseMessage, ToolMessage
from typing import TypedDict,Annotated,Optional

class prdadvisorState(TypedDict,total=False):
    # conversationHistory : Annotated[list[AnyMessage],add_messages]
    conversationHistory : Annotated[list[BaseMessage],add_messages]
    product : Optional[str]
    Phone : Optional[str]
    Name : Optional[str]
    Email : Optional[str]
    lead_status : Optional[str]

