from apps.good_apply.models import OrganizationMember, Secretary


def tool_get_normal_member(org_id):
    """获取组内普通成员"""

    # 根据组id查秘书表，将此组秘书查询出来
    sec_objs = Secretary.objects.filter(org_id=org_id)
    sec_objs_list = [sec.username for sec in sec_objs]

    # 根据组id查组成员表
    all_member = OrganizationMember.objects.filter(org_id=org_id)
    normal_member = all_member.exclude(username__in=sec_objs_list)

    return normal_member
