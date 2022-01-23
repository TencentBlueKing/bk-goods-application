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


def get_cart_result(data: list, source: str) -> list:
    """
    构建购物车格式数据
    """
    if data:
        result = []
        for good in data:
            if source == "shop":
                good = good.to_json()
            else:
                good = good.to_good_json(good.good_code)
            if (source == "shop" and good["status"] == 1) or source == "apply":
                has_type = False
                for type_item in result:
                    if type_item["goods_type_name"] == good["good_type_name"]:
                        type_item["goods_list"].append(good)
                        has_type = True
                        break
                if not has_type:
                    temp_obj = {
                        "goods_type_name": good["good_type_name"],
                        "goods_type_id": good["good_type_id"],
                        "goods_list": [good]
                    }
                    result.append(temp_obj)
    return result
