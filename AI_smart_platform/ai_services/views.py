import json
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .router import ai_router
from .models import AIServiceLog


@csrf_exempt
def run_ai_service(request):
    """
    Generic AI service execution endpoint with request logging
    
    POST /api/ai/run/
    
    Request body:
    {
        "service": "service_name",
        "input": "payload data"
    }
    
    Returns:
        JsonResponse: Result from the AI service
    """
    # Start timing for performance tracking
    start_time = time.time()
    
    # Default values for logging
    service_name = "unknown"
    status = "error"
    error_msg = None
    user_identifier = "anonymous"  # TODO: Extract from auth when implemented
    
    if request.method != "POST":
        response = JsonResponse({"error": "POST request required"}, status=405)
        _log_request(service_name, user_identifier, None, "error", 
                    "POST request required", start_time)
        return response
    
    try:
        data = json.loads(request.body)
        service_name = data.get("service", "unknown")
        payload = data.get("input")
        
        if not service_name or service_name == "unknown":
            error_msg = "AI service name is required"
            response = JsonResponse({"error": error_msg}, status=400)
            _log_request(service_name, user_identifier, str(payload)[:500], 
                        "error", error_msg, start_time)
            return response
        
        # Execute AI service
        result = ai_router(service_name, payload)
        
        # Determine status from result (supports both old and new format)
        if result.get("success") is True or result.get("status") == "success":
            status = "success"
        else:
            status = "error"
            # Extract error message from new format
            if result.get("error") and isinstance(result["error"], dict):
                error_msg = result["error"].get("message", "Unknown error")
            else:
                error_msg = result.get("message", "Unknown error")
        
        # Log the request
        _log_request(service_name, user_identifier, str(payload)[:500], 
                    status, error_msg, start_time)
        
        return JsonResponse(result)
    
    except json.JSONDecodeError:
        error_msg = "Invalid JSON"
        response = JsonResponse({"error": error_msg}, status=400)
        _log_request(service_name, user_identifier, None, "error", 
                    error_msg, start_time)
        return response
        
    except Exception as e:
        error_msg = f"Server error: {str(e)}"
        response = JsonResponse({"error": error_msg}, status=500)
        _log_request(service_name, user_identifier, None, "error", 
                    error_msg, start_time)
        return response


def _log_request(service_name, user_identifier, payload, status, error_msg, start_time):
    """
    Internal helper to log AI service requests
    
    Args:
        service_name: Name of the AI service
        user_identifier: User ID or 'anonymous'
        payload: Request payload (truncated for storage)
        status: 'success' or 'error'
        error_msg: Error message if status is 'error'
        start_time: Request start timestamp
    """
    response_time_ms = int((time.time() - start_time) * 1000)
    
    try:
        AIServiceLog.objects.create(
            service_name=service_name,
            user_identifier=user_identifier,
            request_payload=payload,
            status=status,
            error_message=error_msg,
            response_time_ms=response_time_ms
        )
    except Exception as e:
        # Don't fail the request if logging fails
        # In production, you'd want to log this to a monitoring service
        print(f"Failed to log request: {e}")

