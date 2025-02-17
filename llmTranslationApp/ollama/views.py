from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .ollama_service import query_ai
import json


@csrf_exempt
def ai_model(request):
    if request.method == "OPTIONS":
        response = HttpResponse()
        response["Access-Control-Allow-Headers"] = "Content-Type"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        return response

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
                for chunk in query_ai(prompt):
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
