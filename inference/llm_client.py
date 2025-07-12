import requests

class LLMClient:
    def __init__(self, base_url="http://localhost:8000/v1"):
        self.url = base_url

    def complete(self, prompt: str, model: str = "meta-llama/Llama-3.2-1B-Instruct", temperature: float = 0.7, max_tokens: int = 256) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = requests.post(f"{self.url}/completions", json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["text"]
        except requests.RequestException as e:
            print(f"[LLMClient Error] {e}")
            return ""
