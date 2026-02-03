import json
from ..response_utils import success_response, error_response


def fix_json(payload):
    """
    AI service for fixing and validating JSON
    
    Args:
        payload: JSON string or data to fix/validate
        
    Returns:
        dict: Standardized response with status and fixed JSON
    """
    try:
        # If payload is already a dict, return it
        if isinstance(payload, dict):
            return success_response(
                service_name="fix_json",
                data={"fixed_json": payload}
            )
        
        # If it's a string, try to parse it
        if isinstance(payload, str):
            parsed = json.loads(payload)
            return success_response(
                service_name="fix_json",
                data={"fixed_json": parsed}
            )
        
        return error_response(
            service_name="fix_json",
            error_message="Invalid input type",
            error_code="INVALID_INPUT_TYPE"
        )
        
    except json.JSONDecodeError as e:
        return error_response(
            service_name="fix_json",
            error_message=f"JSON parsing error: {str(e)}",
            error_code="JSON_PARSE_ERROR"
        )
    except Exception as e:
        return error_response(
            service_name="fix_json",
            error_message=f"Unexpected error: {str(e)}",
            error_code="INTERNAL_ERROR"
        )
