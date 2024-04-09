from langchain.tools import tool
from langgraph.graph import StateGraph,END
from langchain_community.llms import Ollama
from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]

def warning():
    print("warning")
graph =  StateGraph(AgentState)
llm=Ollama(model="qwen")
graph.add_node('start',llm)
graph.add_node('Consultants',llm)
graph.add_node('warning',warning)
graph.add_node('repository',llm)
graph.set_entry_point('start')

@tool("web_search")
def  web_search(query: str) -> str:
    """Useful for when you need to answer questions about current events.
    You should ask targeted questions"""
    return ''

graph.add_conditional_edges()
