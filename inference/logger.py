import time

class Logger:
    @staticmethod
    def log_request(prompt: str, response: str, latency_ms: float):
        print("\n=== LLM Request Log ===")
        print(f"Prompt     : {prompt}")
        print(f"Response   : {response.strip()[:200]}...")
        print(f"Latency    : {latency_ms:.2f} ms")
        print("========================\n")
