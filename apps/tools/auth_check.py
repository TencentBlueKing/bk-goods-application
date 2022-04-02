from apps.good_apply.models import Secretary
from django.db.models import Q


def if_secretary(request, org_id):
    """判断身份"""
    query = Q(username=request.user.username) & Q(org_id=org_id)
    sec_obj = Secretary.objects.filter(query).first()
    if sec_obj:
        return True
    else:
        return False
