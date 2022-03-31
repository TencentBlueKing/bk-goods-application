import json

from apps.tools.response import get_result
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from bkstorages.backends.bkrepo import BKRepoStorage


def tool_delpic(request):
    body = request.body
    file_paths = json.loads(body)
    storage = BKRepoStorage()
    if file_paths:
        for file_path in file_paths:
            if storage.exists(file_path):
                storage.delete(file_path)
        return get_result({'message': '删除成功'})
    raise BusinessException(StatusEnums.MYDELETE_ERROR)
