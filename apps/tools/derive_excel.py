import json

from apps.tools.response import get_result
from apps.tools.tool_valid_user_in_the_org import valid_user_in_the_org
from apps.utils.deriveClass import DeriveModel
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.views.decorators.http import require_POST


@require_POST
def derive_excel(request):
    """
    导出excel表
    """
    body = request.body
    body = json.loads(body)
    model = body.get('model')
    goods = body.get('dataList')
    username = request.user.username
    org_id = body.get('org_id', None)
    valid_user_in_the_org(org_id, username)

    if not model or not goods or not username:  # 判空
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    derive = DeriveModel(model, goods, username, org_id)
    derive.run()

    return get_result(derive.result)
