from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import os

api_key = os.getenv("GOOGLE_API_KEY") #importing api key
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key) #setting llm

class State(TypedDict): # basically a memory type thing for agent and can be called a scratchpad for agent
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State) #basically creating a state and giving it all the messages.

def chatbot(state: State):# defines what chatbot does when it runs
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot) #adds a step, when the bot gets here  it runs the chatbot function
graph_builder.add_edge(START, "chatbot") # when bot runs it goes to chatbot node first
graph_builder.add_edge("chatbot", END) # when the jobs done it ends
graph = graph_builder.compile() # compiles all the graphs and nodes you've built until now.

# initial_state = {
#     "messages": [
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
# }
#
# result = graph.invoke(initial_state)
# print(result)