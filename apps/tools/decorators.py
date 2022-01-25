from apps.good_apply.views import is_secretary
from apps.tools.response import get_result


def check_secretary_permission(func):
    """
    判断是否有管理员权限
    """
    def inner(request, *args, **kwargs):
        username = request.user.username
        if not is_secretary(username):
            return get_result({"code": 1, "result": False, "message": "您没有权限进行相关操作"})
        else:
            return func(request, *args, **kwargs)

    return inner
