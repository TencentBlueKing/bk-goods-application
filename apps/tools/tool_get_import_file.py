import json
import os

from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException


def tool_get_import_file(req_body, dir_path, param_file, param_file_name):
    # 导入文件处理
    """
    req_body: 请求体
    dir_path: 文件路径
    param_file: 前端传入文件参数名
    param_file_name: 前端传入文件名参数名
    """
    body = json.loads(req_body)
    if not body.get(param_file):
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    file = body.get(param_file)

    # 判空
    if not body.get(param_file_name):
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    file_name = body.get(param_file_name)

    # 检查文件夹是否存在
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 拼接文件路径
    file_path = os.path.join(dir_path, file_name)
    return file, file_path
