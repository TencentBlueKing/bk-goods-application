import json
import os

from apps.good_purchase.serializers import delExcelSerializer
from apps.tools.response import get_result
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.conf import settings
from django.views.decorators.http import require_POST


@require_POST
def del_excel(request):
    """
    删除excel
    """
    body = request.body
    body = json.loads(body)

    dir_name = body.get('dirName')
    file_name = body.get('fileName')
    username = request.user.username
    del_serializer = delExcelSerializer(data={"username": username})

    if not del_serializer.is_valid():
        pass

    if not dir_name or not file_name:  # 判空
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    if file_name.split('_')[0] != username:
        raise BusinessException(StatusEnums.AUTHORITY_ERROR)

    # 拼接路径
    file_path = os.path.join(settings.MEDIA_ROOT, dir_name, file_name)

    # 删除文件
    os.remove(file_path)
    result = {
        "code": 200,
        "result": True,
        "message": "Delete Done",
        "data": {}
    }
    return get_result(result)
