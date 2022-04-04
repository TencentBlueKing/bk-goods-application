from apps.good_apply.models import OrganizationMember
from apps.good_apply.serializers import OrgIDSerializer
from apps.tools.param_check import get_error_message
from apps.tools.response import get_result
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.db.models import Q


def valid_user_in_the_org(org_id, username):
    """通过组id和用户名验证用户是否在此组中"""
    org_id_serializer = OrgIDSerializer(data={'org_id_': org_id})
    if not org_id_serializer.is_valid():
        message = get_error_message(org_id_serializer)
        return get_result({"code": 400, "result": False, "message": message})
    query = Q(org_id=org_id) & Q(username=username)
    if not OrganizationMember.objects.filter(query).exists():
        raise BusinessException(StatusEnums.AUTHORITY_ERROR)
