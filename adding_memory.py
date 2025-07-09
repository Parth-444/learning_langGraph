from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
import os
from langgraph.graph.message import add_messages
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver

api_key = os.getenv("GOOGLE_API_KEY") #importing api key
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

memory = MemorySaver()

@tool
def find(query:str):
    """
    this function will perform an internet search to find how much a dollar costs against rupee.
    :param query:
    :return:
    """
    search = DuckDuckGoSearchRun()
    return search.invoke(query)

tools = [find]
llm_with_tools = llm.bind_tools(tools)

config = {"configurable":{"thread_id": "1"}}
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):# defines what chatbot does when it runs
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools))
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot") #adding this extra edge makes a call back to llm, helps to secure the question asked.
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile(checkpointer=memory)


initial_state = {
    "messages": [
        {"role": "user", "content": "how much 32234 dollars convert into rupees"}
    ]
}


tool_result = None
result = graph.invoke(initial_state, config=config)
messages = result["messages"]
print(messages[-1].content)

msg = "How many dollars did i ask to convert?"
result = graph.invoke({"messages": [{'role': 'user', 'content':msg}]}, config=config)
messages = result["messages"]
print(messages[-1].content)