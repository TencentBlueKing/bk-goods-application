from django.http import JsonResponse


def get_result(data: dict) -> dict:
    """
    统一api返回格式
    """
    result = {
        "code": 0,
        "result": True,
        "message": "OK",
        "data": {}
    }
    if data:
        if "code" in data:
            result["code"] = data["code"]
        if "result" in data:
            result["result"] = data["result"]
        if "data" in data:
            result["data"] = data["data"]
        if "message" in data and data["message"]:
            result["message"] = data["message"]
    return JsonResponse(result)
