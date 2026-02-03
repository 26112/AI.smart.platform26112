"""
Response utilities for standardized API responses

Ensures consistent response format across all AI services
"""


def success_response(service_name, data):
    """
    Create a standardized success response
    
    Args:
        service_name: Name of the AI service
        data: Response data from the service
        
    Returns:
        dict: Standardized success response
    """
    return {
        "success": True,
        "service": service_name,
        "data": data,
        "error": None
    }


def error_response(service_name, error_message, error_code=None):
    """
    Create a standardized error response
    
    Args:
        service_name: Name of the AI service (or "system" for system errors)
        error_message: Human-readable error message
        error_code: Optional error code for client-side handling
        
    Returns:
        dict: Standardized error response
    """
    response = {
        "success": False,
        "service": service_name,
        "data": None,
        "error": {
            "message": error_message
        }
    }
    
    if error_code:
        response["error"]["code"] = error_code
    
    return response
