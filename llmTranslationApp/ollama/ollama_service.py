import requests
from decouple import config
from .utils import check_microservice_health, MicroserviceHealthError

OLLAMA_API_URL = config('OLLAMA_API_URL', default="http://localhost:11434")

def query_mistral(prompt: str):
    """
    Send a query to the Mistral model hosted by Ollama and stream the response in chunks.
    """

    try:
        check_microservice_health(f"{OLLAMA_API_URL}/")
    except MicroserviceHealthError as e:
        yield f"Error: {str(e)}\n"
        return
    
    url = f"{OLLAMA_API_URL}/api/generate"
    payload = {
        "model": "mistral",
        "prompt": f"{prompt}"
    }
    
    try:
        with requests.post(url, json=payload, stream=True, timeout=10) as response:
            response.raise_for_status()

            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    data = chunk.decode('utf-8')
                    print(f"Received chunk: {data}")
                    yield data
                if '"done": true' in chunk.decode('utf-8'):
                    break

    except requests.exceptions.RequestException as e:
        yield {"error": str(e)}
