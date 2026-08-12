import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai  # Groq uses the standard OpenAI-compatible client format

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tells the server to route requests straight to Groq's fast AI system
client = openai.OpenAI(
    base_url="https://groq.com",
    api_key=os.getenv("OPENAI_API_KEY")
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="Server config error: API Key missing.")
        
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # High-performance model with excellent Amharic support
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Always reply fluently in Amharic (አማርኛ)."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"reply": response.choices.message.content}
    except Exception as e:
        return {"reply": "ይቅርታ፣ ስህተት ተፈጥሯል። እባክዎ እንደገና ይሞክሩ።"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

