from fastapi import FastAPI
from pydantic import BaseModel
from inference.llm_client import LLMClient
from inference.logger import Logger
import time

app = FastAPI()
client = LLMClient()

class CompletionRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 256

@app.post("/completion")
def completion(req: CompletionRequest):
    start = time.time()
    result = client.complete(
        prompt=req.prompt,
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )
    latency = (time.time() - start) * 1000
    Logger.log_request(req.prompt, result, latency)
    return {"result": result, "latency_ms": round(latency, 2)}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}
