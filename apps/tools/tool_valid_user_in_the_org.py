from apps.good_apply.models import OrganizationMember
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.db.models import Q


def valid_user_in_the_org(org_id, username):
    """通过组id和用户名验证用户是否在此组中"""
    if not org_id or not isinstance(org_id, int):
        raise BusinessException(StatusEnums.ORG_INFO_ERROR)
    query = Q(org_id=org_id) & Q(username=username)
    if not OrganizationMember.objects.filter(query).exists():
        raise BusinessException(StatusEnums.AUTHORITY_ERROR)
