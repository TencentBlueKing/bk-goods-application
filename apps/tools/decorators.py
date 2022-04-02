import json

from apps.tools.auth_check import if_secretary
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException


def check_secretary_permission(func):
    """
    判断是否有管理员权限
    """
    def inner(request, *args, **kwargs):
        username = request.user.username
        org_id = json.loads(request.body).get('org_id')
        if not if_secretary(username, org_id):
            raise BusinessException(StatusEnums.AUTHORITY_ERROR)
        else:
            return func(request, *args, **kwargs)

    return inner
