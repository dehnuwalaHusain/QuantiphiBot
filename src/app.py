from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retriever import get_chain
from memory_store import MEMORY_STORE

app = FastAPI()

class ChatRequest(BaseModel):
    user_email: str
    query: str

@app.post("/chat")
def chat(payload: ChatRequest):
    try:
        chain = get_chain(payload.user_email)
        response = chain.invoke({"question": payload.query})
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def history(user_email):
    memory = MEMORY_STORE.get(user_email)
    if not memory:
        return {"history": []}
    
    msgs = memory.chat_memory.messages
    return {"history": [{"role": m.type, "content": m.content} for m in msgs]}