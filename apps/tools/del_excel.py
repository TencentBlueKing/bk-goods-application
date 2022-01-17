import json
import os

from django.views.decorators.http import require_POST

from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from apps.tools.response import get_result


@require_POST
def del_excel(request):
    """
    删除excel
    """
    body = request.body
    body = json.loads(body)

    if not body['dirName'] or not body['fileName']:  # 判空
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    # 拼接路径
    file_path = os.path.join('USERRES', body['dirName'], body['fileName'])

    # 删除文件
    os.remove(file_path)
    result = {
        "code": 200,
        "result": True,
        "message": "Delete Done",
        "data": {}
    }
    return get_result(result)