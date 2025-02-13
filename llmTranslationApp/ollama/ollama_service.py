import requests
import json
from decouple import config
from .utils import check_microservice_health, MicroserviceHealthError

OLLAMA_API_URL = config("OLLAMA_API_URL", default="http://localhost:11434")


def query_ai(prompt: str):
    """
    Send a query to the AI model hosted by Ollama and stream the response in chunks.
    """
    try:
        check_microservice_health(f"{OLLAMA_API_URL}/")
    except MicroserviceHealthError as e:
        yield json.dumps({"error": str(e)})
        return

    url = f"{OLLAMA_API_URL}/api/generate"
    payload = {"model": "deepseek-r1:1.5b", "prompt": prompt}

    try:
        with requests.post(url, json=payload, stream=True, timeout=60) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    yield json.dumps(json_response)
                    if json_response.get("done", False):
                        break

    except requests.exceptions.RequestException as e:
        yield json.dumps({"error": str(e)})
