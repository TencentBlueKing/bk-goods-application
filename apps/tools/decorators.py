from apps.tools.auth_check import is_leader_or_secretary, is_secretary
from apps.tools.response import get_result

# from apps.utils.enums import StatusEnums
# from apps.utils.exceptions import BusinessException


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


def check_leader_or_secretary_permission(func):
    """
    判断是否有导员或秘书权限
    """
    def inner(request, *args, **kwargs):
        flag, leader_or_secretary = is_leader_or_secretary(request)
        if flag:
            return func(request, leader_or_secretary=leader_or_secretary, *args, **kwargs)
        else:
            return get_result({"code": 1, "result": False, "message": "您不是秘书和导员，没有权限进行相关操作"})

    return inner
