from inference.llm_client import LLMClient

def test_completion_response():
    client = LLMClient()
    result = client.complete("What is the capital of France?")
    assert result != "", "LLM response was empty"
    assert "Paris" in result, "Expected 'Paris' in the response"
