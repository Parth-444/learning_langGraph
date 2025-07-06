from fastapi import FastAPI
import uvicorn
from agent import graph
from pydantic import BaseModel

app = FastAPI()

all_conversation = {"messages": []}

class Message(BaseModel):
    message: str

@app.get("/")
async def show_all_messages():
    return all_conversation

@app.post("/chat")
async def chat_with_bot(input_msg: Message):
    message = input_msg.message
    all_conversation["messages"].append({"role": "user", "content": message})

    # ✅ Pass full conversation history
    result = graph.invoke(all_conversation)

    last_msg = result["messages"][-1]

    # ✅ Add assistant reply too
    all_conversation["messages"].append({"role": "assistant", "content": last_msg.content})

    return last_msg.content

if __name__ =="__main__":
    uvicorn.run("app:app", reload=True)