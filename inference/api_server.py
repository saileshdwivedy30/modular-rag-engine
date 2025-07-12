from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import os

app = FastAPI()

# Load model at startup
model_id = "meta-llama/Llama-3.2-1B-Instruct"
token = os.getenv("HF_TOKEN")

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(model_id, use_auth_token=token)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, use_auth_token=token)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

print("Model loaded.")


class CompletionRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.7


@app.post("/v1/completions")
def complete(request: CompletionRequest):
    response = generator(
        request.prompt,
        max_new_tokens=request.max_tokens,
        temperature=request.temperature,
        do_sample=True,
        repetition_penalty=1.2,
        top_p=0.9,
    )[0]["generated_text"]

    return {
        "id": "cmpl-123",
        "object": "text_completion",
        "model": request.model,
        "choices": [{"text": response, "index": 0}],
    }
