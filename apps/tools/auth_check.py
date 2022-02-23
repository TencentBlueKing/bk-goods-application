from apps.good_apply.models import Secretary
from apps.utils.exceptions import BusinessException
from blueapps.utils import get_client_by_request
from django.core.cache import cache


def is_secretary(username):
    if Secretary.objects.filter(username=username).exists():
        return True
    return False


def get_users_in_group(request, group_id) -> list:
    """获取组内成员"""
    client = get_client_by_request(request=request)
    # 查询组内用户信息
    response = client.usermanage.list_department_profiles(id=group_id)
    if not response.get('result'):
        raise BusinessException((5004, response.get('message')))
    users = response.get('data').get('results')  # 组内用户列表
    return users


def sub_users_in_group(request, username, group_id) -> list:
    """校验用户username在组内是否有管理的人员，返回成员列表，没有则为空列表"""
    users = get_users_in_group(request, group_id)
    sub_users = []
    # 循环用户信息，查看导员username是否和导员username匹配，匹配则该导员管辖的成员
    for user in users:
        leaders = user.get('leader')
        for leader in leaders:
            if leader.get('username') == username:
                sub_users.append({'id': user.get('id'),
                                  'username': user.get('username'),
                                  'display_name': user.get('display_name')})
    return sub_users


def is_leader_or_secretary(request):
    """校验是否是秘书或者导员"""
    username = request.user.username
    # 是否是秘书
    if is_secretary(username=username):
        return True, 0  # 0表示是秘书

    # 是否是导员
    # 一期先使用group_id=6的组(唯一组)，二期丰富多个组的情况
    group_id = 6
    key = username + '_is_leader'
    if cache.get(key):
        is_leader = cache.get(key)
        if is_leader:
            return True, 1  # 1表示是导员
        else:
            return False, None  # 不是导员也不是秘书
    # 缓存中不存在记录，再查询数据库
    sub_users = sub_users_in_group(request, username=username, group_id=group_id)
    if sub_users:
        cache.set(key=key, value=1, timeout=21600)  # 是导员
        return True, 1
    else:
        cache.set(key=key, value=0, timeout=21600)  # 不是导员，没有下级组员
        return False, None
