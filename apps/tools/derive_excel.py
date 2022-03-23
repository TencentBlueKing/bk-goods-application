import json

from apps.good_purchase.models import UserInfo
from apps.tools.response import get_result
from apps.utils.deriveClass import DeriveModel
from apps.utils.enums import StatusEnums
from apps.utils.exceptions import BusinessException
from django.views.decorators.http import require_POST


# TODO: 导出后要用celery定时删除
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

    if not UserInfo.objects.filter(username=username).exists():
        raise BusinessException(StatusEnums.USER_NOT_EXIST_ERROR)
    if not model or not goods or not username:  # 判空
        raise BusinessException(StatusEnums.PARAMS_ERROR)

    derive = DeriveModel(model, goods, username)
    derive.run()

    return get_result(derive.result)
