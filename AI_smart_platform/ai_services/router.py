from .services.fix_json import fix_json
from .response_utils import error_response


def ai_router(service_name, payload):
    """
    Central AI router
    Decides which AI service to execute
    
    Args:
        service_name: Name of the AI service to run
        payload: Input data for the AI service
        
    Returns:
        dict: Standardized response from the AI service
    """
    
    if service_name == "fix_json":
        return fix_json(payload)
    
    # Add more AI services here as they are developed
    # if service_name == "cyber_security":
    #     return run_security_agent(payload)
    
    return error_response(
        service_name=service_name,
        error_message=f"Unknown AI service: {service_name}",
        error_code="UNKNOWN_SERVICE"
    )
