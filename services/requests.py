import json
import logging
from django.http import QueryDict

logger = logging.getLogger(__name__)

def get_request_data(request):
    """
    Extracts and returns request data based on content type.
    Supports JSON, form-data, and GET parameters.
    """
    try:
        if request is None:
            return QueryDict()

        content_type = request.META.get("CONTENT_TYPE", "")

        if content_type == "application/json":
            return json.loads(request.body)
        elif content_type.startswith("multipart/form-data"):
            return request.POST.copy()  # Preserve multi-value parameters
        elif request.method == "GET":
            return request.GET.copy()
        elif request.method == "POST":
            return request.POST.copy()
        return QueryDict()

    except json.JSONDecodeError:
        logger.warning("Invalid JSON received in request body.")
        return QueryDict()
    except Exception as e:
        logger.error(f"Error parsing request data: {e}", exc_info=True)
        return QueryDict()

def get_clean_data(request):
    """
    Cleans the extracted request data by stripping extra spaces and sanitizing input.
    """
    data = get_request_data(request)

    if isinstance(data, dict):  # JSON data
        return {key: value.strip() if isinstance(value, str) else value for key, value in data.items()}
    elif isinstance(data, QueryDict):  # Form or GET data
        cleaned_data = QueryDict(mutable=True)
        for key, values in data.lists():
            cleaned_values = [v.strip() if isinstance(v, str) else v for v in values]
            cleaned_data.setlist(key, cleaned_values)
        return cleaned_data

    return data