import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

app = FastAPI()

# Allows your Telegram interface to communicate with this server safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pulls the secret API key securely from your server's settings panel
openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="Server configuration error: API Key is missing.")
        
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",  # Best native model for Amharic language accuracy
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Always reply fluently in Amharic (አማርኛ)."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"reply": response.choices.message.content}
    except Exception as e:
        return {"reply": "ይቅርታ፣ ስህተት ተፈጥሯል። እባክዎ እንደገና ይሞክሩ።"}

if __name__ == "__main__":
    # Dynamically reads the server's open port or defaults to 8000
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
