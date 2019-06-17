from rest_framework.renderers import JSONRenderer
from rest_framework.status import is_success, is_client_error


class CoreJSONRenderer(JSONRenderer):
    """
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']
        success = is_success(response.status_code)
        output = {
            "status": success and "OK" or "ERROR",
        }
        if is_client_error(response.status_code):
            if "detail" in data:
                output["message"] = data["detail"]
            else:
                output["errors"] = data
        elif success:
            if data:
                if 'results' in data:
                    output.update(data)
                else:
                    output["results"] = data
        else:
            output = data
        return super(CoreJSONRenderer, self).render(output, accepted_media_type, renderer_context)