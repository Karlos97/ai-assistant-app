from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from .ollama_service import query_mistral
import json


@csrf_exempt
def mistral_chat(request):
    if request.method == "POST":
        if request.content_type != "application/json":
            return JsonResponse(
                {"error": "Content-Type must be application/json"}, status=400
            )

        try:
            body = json.loads(request.body)
            prompt = body.get("prompt", "")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)

        if not isinstance(prompt, str) or not prompt.strip():
            return JsonResponse(
                {"error": "Prompt is required and must be a non-empty string"},
                status=400,
            )

        def generate_response():
            try:
                for chunk in query_mistral(prompt):
                    if chunk:  # Only yield non-empty chunks
                        yield f"{chunk}\n"
            except Exception as e:
                yield json.dumps({"error": str(e)}) + "\n"

        response = StreamingHttpResponse(
            generate_response(), content_type="application/x-ndjson"
        )
        response["Cache-Control"] = "no-cache"
        return response

    return JsonResponse({"error": "Invalid request method"}, status=405)
