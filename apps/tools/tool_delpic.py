import json

from apps.tools.response import get_result
from apps.tools.tool_valid_user_in_the_org import valid_user_in_the_org
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from bkstorages.backends.bkrepo import BKRepoStorage


def tool_delpic(request):
    username = request.user.username
    body = request.body
    body = json.loads(body)
    file_paths = body.get('file_paths')
    org_id = body.get('org_id')
    valid_user_in_the_org(org_id, username)
    storage = BKRepoStorage()
    if file_paths:
        for file_path in file_paths:
            if storage.exists(file_path):
                storage.delete(file_path)
        return get_result({'message': '删除成功'})
    raise BusinessException(StatusEnums.MYDELETE_ERROR)
